import json
import time
from cryptography.hazmat.primitives import hashes
import hashlib

class Request:
    


    def __init__(self):
        self.request = {"signal":"","data":""}
        

    def logIn(self, login, password):
        request = self.request
        password = self.make_hash(str.encode(password))
        request["signal"] ="LOG"
        request["data"] = {"login": login, "password": password}
        print(str(request))

        return str(request)

    def register(self, login, password, auth_key):
        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key = self.make_hash(str.encode(auth_key))
        request["signal"] ="LAD"
        request["data"] = {"login": login, "password": password, "auth_key": auth_key}

        return str(request)

    #po poprawnej autoryzacji zmienia hasło na podane przez klienta
    def reset_password(self, login, password, auth_key):
        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key = self.make_hash(str.encode(auth_key))
        request["signal"] ="LRS"
        request["data"] = {"login": login,  "auth_key": auth_key, "password": password}

        return str(request)

    
    def message(self, to, sender, message):
        t = time.localtime()
        request = self.request
        request["signal"] ="MSG"
        request["data"] = {"to": to, "from": sender, "date": time.strftime("%H:%M:%S", t),"message": message}

        return str(request)

    def change_password(self, login, password, new_password, auth_key):

        request = self.request

        password = self.make_hash(str.encode(password))
        new_password = self.make_hash(str.encode(new_password))
        auth_key = self.make_hash(str.encode(auth_key))

        request["signal"] ="UCP"
        request["data"] = {"login": login, "password": password, "new_password": new_password, "auth_key": auth_key}

        return str(request)

    
    def delete_account(self, login, password, auth_key):

        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key = self.make_hash(str.encode(auth_key))

        request["signal"] ="UDA"
        request["data"] = {"login": login, "password": password, "auth_key": auth_key}

        return str(request)

    
    def add_contact(self, login, contact):

        request = self.request
        request["signal"] ="CAD"
        request["data"] = {"login": login, "user": contact}

        return str(request)

    def del_contact(self, login, contact):
    
        request = self.request
        request["signal"] ="CDL"
        request["data"] = {"login": login, "user": contact}
        #print(str(request))
        return str(request)


    def make_hash(self, to_hash):
        m = hashlib.sha256()
        m.update(to_hash)
        hash = m.hexdigest()

        return hash

    