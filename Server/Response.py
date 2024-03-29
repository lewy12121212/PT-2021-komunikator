import json
import os
#from Server import DB
import time
import ast

from Server import DB 


class Response:
    logOut = False
    def __init__(self, database):
        #DB = database
        self.logOut = False
        self.cur = database

    def depadding(self, message):
        #print(type(message))
        
        for it in reversed(message):
            
            if it != 125:
                message = message[:-1]
                
            else:
                break
        return message

    def Make_Response(self, buffer):
        signal = ""
        buffer = self.depadding(buffer)
        #print(buffer)
        dict_str = buffer.decode("UTF-8").replace("'", '"')
        t = time.localtime()
        #mydata = ast.literal_eval(dict_str)

        temp = json.loads(dict_str)
        signal = temp["signal"]
        data = temp["data"]

        response = {"to":"",
            "data":""}
        #print(temp)

        if signal == "CON":
            response["data"]
        elif signal == "ACK":
            return
        
        #przesyłanie wiadomości do adresata
        elif signal == "MSG":
            #path = DB.Contacts_Path(data["login"])

            response["to"] = data["to"]
            message = {"signal":"MSG", "data": {"from": data["from"], "date": data["date"], "message": data ["message"]}}
            response["data"] = str(message)
            print(time.strftime("%H:%M:%S", t), " message from: ", data["from"], " to: ", data["to"])
            return response
        
        #dodanie nowego użytwkonika
        elif signal == "LAD":
            if self.AddUser(data["login"], data["password"], data["auth_key1"], data["auth_key2"], data["auth_key3"]):
                response["data"] = '{"signal":"ACK","data":{"action":"add_user", "data":"Dodano uzytkownika"}}'
                response["to"] = "self"
                print(time.strftime("%H:%M:%S", t), " new account created - ", data["login"])
                #utworzenie pliku z kontaktami
                f = open(("./Server/contacts/" + str(data["login"]) + '.txt'), "x")
                f.close()
            
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":{"action":"add_user", "data":"Uzytkownik istnieje"}}'
        
        #żądanie logowania
        elif signal == "LOG":
            login = data["login"]
            password = data["password"]
            #print(password)
            tmp = self.LogIn(login, password)
            #jeśli dane do logowania poprawne zwróć ACK i login klienta
            #jeśli nie zwróć RJT i self, aby wątek wiedział, że nie może kończyś funkcji Set_Configuration
            if tmp == 2:
                response["data"] = '{"signal":"ACK","data":{"action":"login", "data": ""}}'
                response["to"] = login
                DB.Change_Logged(login,self.cur)
                print(time.strftime("%H:%M:%S", t),  data["login"], " logged in to system")
            elif tmp == 1:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":{"action":"login", "data": "Błędny login lub hasło."}}'
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":{"action":"login_exists", "data": "Błędny login lub hasło."}}'
            #print(response)
        
        #żądanie resetowania hasła przy logowaniu
        elif signal == "LRS":
            tmp = self.ResetPassword(data['login'], data['auth_key1'], data['auth_key2'], data['auth_key3'], data['password'])
            if tmp == 2:
                response["data"] = '{"signal":"ACK","data":{"action":"pass_reset","data":"Zresetowano haslo."}}'
                response["to"] = "self"

            elif tmp == 1:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":{"action":"pass_reset","data":"Bledna odpowiedz autoryzacyjna lub uzytkownik nie istnieje"}}'
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":{"action":"pass_reset_exists","data":"Użytkownik nie istnieje."}}'
        
        #zmiana hasła użytkownika
        elif signal == "UCP":
            if self.ChangePassword(data['login'], data['password'], data['new_password']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":{"action":"change_pass", "data": "Pomyslnie zmieniono haslo"}}'
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":{"action":"change_pass", "data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}}'
        
        #usunięcie konta przez użytkonika
        elif signal == "UDA":
            path = DB.Contacts_Path(data['login'], self.cur)
            if self.DeleteUser(data['login'], data['password'], data['auth_key1'], data['auth_key2'], data['auth_key3']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":{"action":"del_account", "data": "Twoje konto zostalo usuniete."}}'
                self.logOut = True
                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist") 
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":{"action":"del_account", "data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}}'
        elif signal == "ULO":
            self.logOut = True
            response["to"] = "self"
            response["data"] = "END"
        #dodanie użytkownika do kontaktów
        elif signal == "CAD":
            if DB.Exists(data['user'], self.cur) and data["user"] != "Inne":

                path = DB.Contacts_Path(data["login"], self.cur)
           

                if DB.Exists(data['user'], self.cur):
                    with open(path, 'a') as f:
                        f.write(data["user"]+'\n')

                if DB.IfLogged(data["user"], self.cur):
                    active = 1
                else:
                    active = 0

                response["to"] = data["login"]
                mess = {"signal":"ACK","data":{"action": "add_contact", "data": "Dodano nowy kontakt.", "user": data["user"], "active": active}}
                response["data"] = str(mess)
            else:
                response["data"] = '{"signal":"RJT","data":{"action": "add_contact", "data": "Użytkownik nie istnieje."}}'
                response["to"] = data["login"]
 
        
        #usuwanie użytkownika
        elif signal == "CDL":
            #print(tmp)
            path = DB.Contacts_Path(data["login"], self.cur)
            contacts_list = []
            with open(path, 'r') as f:
                contacts_list = f.readlines()

            
            i = 0
            #print(contacts_list)     
            for line in contacts_list:
                s = line.rstrip("\n")
                contacts_list[i] = s
                i+=1
                #contacts_list += s
            if DB.IfLogged(data["user"], self.cur):
                active = 1
            else:
                active = 0

            if data["user"] in contacts_list:
                contacts_list.remove(data["user"])
                with open(path, 'w') as f:
                    f.writelines("%s\n" % l for l in contacts_list)
            
            
                mes = {"signal":"ACK","data":{"action": "del_contact", "data": "Pomyslnie usunięto z listy kontaktów.", "user": data["user"], "active": active}}
                response["data"] = str(mes)
                response["to"] = data["login"]
            else:
                response["data"] = '{"signal":"RJT","data":{"action": "del_contact", "data": "Wybrany kontakt nie istnieje."}}'
                response["to"] = data["login"]

            #print(contacts_list)            
        #koniec połączenia
        elif signal == "END":
            response["to"] = "self"
            response["data"] = "END"
            print(time.strftime("%H:%M:%S", t), " close connection with client")
        else:
            return response

        return response

    def LogIn(self, login, password):
        #print("1")
        if DB.Exists(login, self.cur):
            #print("2")
            if not DB.IfLogged(login, self.cur):
                #print("3")
                user = DB.Select_User(login, self.cur)
                #print("4")
                #print(user[0:2])
                if user[0:2] == (login, password):
                    #print("+")
                    return 2
                    
                else:
                    #print("-")
                    return 1
            else:
                return 0
                    
        else:
            return 1

    def AddUser(self, login, password, auth_key, auth_key1, auth_key2):
        if DB.Add_User(login, password, auth_key, auth_key1, auth_key2, self.cur):
            return True
        else:

            return False


    def ResetPassword(self,login, auth_key, auth_key1, auth_key2, new_password):
        if DB.Exists(login, self.cur):
            if DB.Reset_Password(login, new_password,auth_key, auth_key1, auth_key2, self.cur):
                return 2
            else:
                return 1
        else:
            return 0

    def ChangePassword(self, login, old_password, new_password):
        if DB.Change_Password(login,old_password,new_password, self.cur):
            return True
        else:
            return False

    def DeleteUser(self, login, password, auth_key, auth_key1, auth_key2):
        if DB.Delete_User(login, password, auth_key, auth_key1, auth_key2, self.cur):
            return True
        else:
            return False

