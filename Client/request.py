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

    def register(self, login, password, auth_key1, auth_key2, auth_key3):
        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key1 = self.make_hash(str.encode(auth_key1))
        auth_key2 = self.make_hash(str.encode(auth_key2))
        auth_key3 = self.make_hash(str.encode(auth_key3))
        request["signal"] ="LAD"
        request["data"] = {"login": login, "password": password, "auth_key1": auth_key1, "auth_key2": auth_key2, "auth_key3": auth_key3}

        return str(request)

    #po poprawnej autoryzacji zmienia hasło na podane przez klienta
    def reset_password(self, login, password, auth_key1, auth_key2, auth_key3):
        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key1 = self.make_hash(str.encode(auth_key1))
        auth_key2 = self.make_hash(str.encode(auth_key2))
        auth_key3 = self.make_hash(str.encode(auth_key3))
        request["signal"] ="LRS"
        request["data"] = {"login": login,  "auth_key1": auth_key1, "auth_key2": auth_key2, "auth_key3": auth_key3, "password": password}

        return str(request)

    
    def message(self, to, sender, message):
        t = time.localtime()
        request = self.request
        request["signal"] ="MSG"
        request["data"] = {"to": to, "from": sender, "date": time.strftime("%H:%M:%S", t),"message": message}

        return str(request)

    def change_password(self, login, password, new_password):

        request = self.request

        password = self.make_hash(str.encode(password))
        new_password = self.make_hash(str.encode(new_password))


        request["signal"] ="UCP"
        request["data"] = {"login": login, "password": password, "new_password": new_password}

        return str(request)

    
    def delete_account(self, login, password, auth_key1, auth_key2, auth_key3):

        request = self.request
        password = self.make_hash(str.encode(password))
        auth_key1 = self.make_hash(str.encode(auth_key1))
        auth_key2 = self.make_hash(str.encode(auth_key2))
        auth_key3 = self.make_hash(str.encode(auth_key3))

        request["signal"] ="UDA"
        request["data"] = {"login": login, "password": password, "auth_key1": auth_key1, "auth_key2": auth_key2, "auth_key3": auth_key3}

        return str(request)

    
    def add_contact(self, login, contact):

        request = self.request
        request["signal"] ="CAD"
        request["data"] = {"login": login, "user": contact}
        
        return str(request)

    def accept(self):
    
        request = self.request
        request["signal"] ="ACK"
        request["data"] = {"data": "accept"}
        
        return str(request)

    def del_contact(self, login, contact):
    
        request = self.request
        request["signal"] ="CDL"
        request["data"] = {"login": login, "user": contact}
        #print(str(request))
        return str(request)

    def inform_income(self, login):
        request = self.request
        request["signal"] ="NUR"
        request["data"] = {"login": login}

        return str(request)

    def inform_outcome(self, login):
        request = self.request
        request["signal"] ="NCL"
        request["data"] = {"login": login}

        return str(request)

    def logOut(self, login):
        request = self.request
        request["signal"] ="ULO"
        request["data"] = {"login": login}
        #print(str(request))
        return str(request)


    def make_hash(self, to_hash):
        m = hashlib.sha256()
        m.update(to_hash)
        hash = m.hexdigest()

        return hash

    