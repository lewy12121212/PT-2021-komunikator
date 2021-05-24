import json
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
        request["signal"] ="LAD"
        request["data"] = {"login": login, "password": password, "auth_key": auth_key}

        return str(request)

    
    def message(self, to, sender, message):
        request = self.request
        request["signal"] ="MSG"
        request["data"] = {"to": to, "from": sender, "message": message}

        return str(request)


    def make_hash(self, to_hash):
        m = hashlib.sha512()
        m.update(to_hash)
        hash = m.hexdigest()

        return hash