import json
from Server import DB


class Response:
    def __init__(self):
        self

    def Make_Response(self, buffer):
        signal = ""

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]

        response = {"to":"",
            "data":""}

        if signal == "CON":
            response["data"]
        elif signal == "ACK":
            return
        elif signal == "MSG":
            response["to"] = data["to"]
            response["data"] = data["from"] + data ["message"]
            return response
        elif signal == "LAD":
            if self.AddUser(data["login"], data["password"], data["auth_key"]):
                response["data"] = "ACK"
                response["to"] = "self"
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":"Uzytkownik istnieje"}'
        elif signal == "LOG":
            login = data["login"]
            password = data["password"]
            #jeśli dane do logowania poprawne zwróć ACK i login klienta
            #jeśli nie zwróć RJT i self, aby wątek wiedział, że nie może kończyś funkcji Set_Configuration
            if self.LogIn(login, password):
                response["data"] = "ACK"
                response["to"] = login
            else:
                response["to"] = "self"
                response["data"] = "RJT"
        elif signal == "LRS":
            if self.ResetPassword(data['login'], data['auth_key'], data['password']):
                response["data"] = '{"signal":"ACK","data":"Zresetowano haslo."}'
                response["to"] = 'self'
            else:
                response["to"] = "self"
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub uzytkownik nie istnieje"}'
        elif signal == "UCP":
            if self.ChangePassword(data['login'], data['password'], data['new_password'], data['auth_key']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":"Pomyslnie zmieniono haslo"}'
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}'
        elif signal == "UDA":
            if self.DeleteUser(data['login'], data['password'], data['auth_key']):
                response["to"] = data["login"]
                response["data"] = '{"signal":"ACK","data":"Twoje konto zostanie usunieto po wylogowaniu."}'
            else:
                response["to"] = data["login"]
                response["data"] = '{"signal":"RJT","data":"Bledna odpowiedz autoryzacyjna lub obecne haslo."}'
        elif signal == "CLR":
            return
        else:
            return response

        return response

    def LogIn(self, login, password):
        if DB.Exists(login):
            user = DB.Select_User(login)
            if user == (login, password):
                return True
            else:
                return False
        else:
            return False

    def AddUser(self, login, password, auth_key):
        if DB.Add_User(login, password, auth_key):
            return True
        else:

            return False


    def ResetPassword(self,login, auth_key, new_password):
        if DB.Reset_Password(login, new_password, auth_key):
            return True
        else:
            return False

    def ChangePassword(self, login, old_password, new_password, auth_key):
        if DB.Change_Password(login,old_password,new_password, auth_key):
            return True
        else:
            return False

    def DeleteUser(self, login, password, auth_key):
        if DB.Delete_User(login, password, auth_key):
            return True
        else:
            return False

