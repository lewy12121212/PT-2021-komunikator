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
        elif signal == "LOR":
            return
        elif signal == "LOG":
            login = data["login"]
            password = data["password"]
            if self.LogIn(login,password):
                response["data"]="ACK"
                response["to"] = login
            else:
                response["to"] = "self"
                response["data"]="RJT"

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