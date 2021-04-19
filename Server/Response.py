import json
import Server
import Database

def Make_Response(buffer):
    signal = ""
    #na czas korzystania z putty
    if buffer != str.encode("\r\n"):
        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]
        #print(signal)
    response = {"to":"",
        "data":""}

    if signal == "CON":
        response["data"] = Configure_Connection()
    elif signal == "ACK":
        return
    elif signal == "MSG":
        return
    elif signal == "LOR":
        return
    elif signal == "LOG":
        login = data["login"]
        password = data["password"]
        if LogIn(login,password):
            response["data"]="ACK"
            response["to"] = login
        else:
            response["data"]="RJT"
        
    elif signal == "CLR":
        return
    else:
        return response

    return response

#nie do końca wiem co przesyłać przy ustanawianiu połączenia
def Configure_Connection():
    return "ACK"

def LogIn(login, password):
    DB = Server.DB
    if DB.Exists(login):
        if DB.Select_User(login) == (login,password):
            return True
        else:
            return False
    else:
        return False