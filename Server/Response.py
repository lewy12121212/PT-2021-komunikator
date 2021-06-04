import json
import os
#from Server import self.DB

import ast



class Response:
    logOut = False
    def __init__(self, database):
        self.DB = database
        self.logOut = False

    def Make_Response(self, buffer):
        signal = ""
        dict_str = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(dict_str)
        signal = tmp["signal"]
        data = tmp["data"]

        response = {"to":"",
            "data":""}
        #print(tmp)

        if signal == "CON":
            response["data"]
        elif signal == "ACK":
            return
        
        #przesyłanie wiadomości do adresata
        elif signal == "MSG":
            path = self.DB.Contacts_Path(data["login"])
            
            response["to"] = data["to"]
            message = {"signal":"MSG", "data": {"from": data["from"], "date": data["date"], "message": data ["message"]}}
            response["data"] = str(message)
            print(message)
            return response
        
        #dodanie nowego użytwkonika
        elif signal == "LAD":
            if self.AddUser(data["login"], data["password"], data["auth_key"]):
                response["data"] = '{"signal":"ACK","data":"Dodano uzytkownika"}'
                response["to"] = "self"

                #utworzenie pliku z kontaktami
                f = open(("./Server/contacts/" + str(data["login"]) + '.txt'), "x")
                f.close()
            
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":"Uzytkownik istnieje"}'
        
        #żądanie logowania
        elif signal == "LOG":
            login = data["login"]
            password = data["password"]
            #jeśli dane do logowania poprawne zwróć ACK i login klienta
            #jeśli nie zwróć RJT i self, aby wątek wiedział, że nie może kończyś funkcji Set_Configuration
            if self.LogIn(login, password):
                response["data"] = '{"signal":"ACK","data":""}'
                response["to"] = login
                self.DB.Change_Logged(login)
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":""}'
        
        #żądanie resetowania hasła przy logowaniu
        elif signal == "LRS":
            if self.ResetPassword(data['login'], data['auth_key'], data['password']):
                response["data"] = '{"signal":"ACK","data":"Zresetowano haslo."}'
                response["to"] = 'self'
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub uzytkownik nie istnieje"}'
        
        #zmiana hasła użytkownika
        elif signal == "UCP":
            if self.ChangePassword(data['login'], data['password'], data['new_password'], data['auth_key']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":"Pomyslnie zmieniono haslo"}'
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}'
        
        #usunięcie konta przez użytkonika
        elif signal == "UDA":
            path = self.DB.Contacts_Path(data['login'])
            if self.DeleteUser(data['login'], data['password'], data['auth_key']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":"Twoje konto zostalo usuniete."}'
                self.logOut = True
                if os.path.exists(path):
                    os.remove(path)
                else:
                    print("The file does not exist") 
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}'
        elif signal == "ULO":
            self.logOut = True
            response["to"] = "self"
            response["data"] = "END"
        #dodanie użytkownika do kontaktów
        elif signal == "CAD":
            if self.DB.Exists(data['user']):
                response["to"] = data["user"]
                mess = {"signal":"CIN","data":{"user": data["login"]}}
                response["data"] = str(mess)
            else:
                response["data"] = '{"signal":"RJT","data":"Użytkownik nie istnieje."}'
                response["to"] = data["login"]

        elif signal == "CAP":
            
            path = self.DB.Contacts_Path(data["login"])
            path1 = self.DB.Contacts_Path(data["user"])

            if self.DB.Exists(data['user']):
                with open(path, 'a') as f:
                    f.write(data["user"]+'\n')

                with open(path1, 'a') as f:
                    f.write(data["login"]+'\n') 

                response["data"] = '{"signal":"CAP","data":"Dodano nowy kontakt."}'
                response["to"] = data["login"]
            else:
                response["data"] = '{"signal":"RJT","data":"Użytkownik nie istnieje."}'
                response["to"] = data["login"]

        elif signal == "CRT":
            response["data"] = '{"signal":"RJT","data":"Nie zaakceptowano zaproszenia."}'
            response["to"] = data["login"]       
        
        #usuwanie użytkownika
        elif signal == "CDL":
            #print(tmp)
            path = self.DB.Contacts_Path(data["login"])
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
                
            if data["user"] in contacts_list:
                contacts_list.remove(data["user"])
                with open(path, 'w') as f:
                    f.writelines("%s\n" % l for l in contacts_list)
            
                response["data"] = '{"signal":"ACK","data":"Pomyslnie usunięto z listy kontaktów."}'
                response["to"] = data["login"]
            else:
                response["data"] = '{"signal":"RJT","data":"Wybrany kontakt nie istnieje."}'
                response["to"] = data["login"]

            #print(contacts_list)            
        #koniec połączenia
        elif signal == "END":
            response["to"] = "self"
            response["data"] = "END"
        else:
            return response

        return response

    def LogIn(self, login, password):
        if self.DB.Exists(login):
            if not self.DB.IfLogged(login):
                user = self.DB.Select_User(login)
                #print(repr(user[0:2]))
                if user[0:2] == (login, password):
                    return True
                else:
                    return False
        else:
            return False

    def AddUser(self, login, password, auth_key):
        if self.DB.Add_User(login, password, auth_key):
            return True
        else:

            return False


    def ResetPassword(self,login, auth_key, new_password):
        if self.DB.Reset_Password(login, new_password, auth_key):
            return True
        else:
            return False

    def ChangePassword(self, login, old_password, new_password, auth_key):
        if self.DB.Change_Password(login,old_password,new_password, auth_key):
            return True
        else:
            return False

    def DeleteUser(self, login, password, auth_key):
        if self.DB.Delete_User(login, password, auth_key):
            return True
        else:
            return False

