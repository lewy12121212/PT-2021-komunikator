import json

class Request:

    def __init__(self):
        self.request = {"signal":"","data":""}

    def logIn(self, login, password):
        request = self.request
        request["signal"] ="LOG"
        request["data"] = {"login": login, "password": password}

        return str(request)

    def register(self, login, password, auth_key):
        request = self.request
        request["signal"] ="LAD"
        request["data"] = {"login": login, "password": password, "auth_key": auth_key}

        return str(request)

    
    def message(self, to, sender, message):
        request = self.request
        request["signal"] ="MSG"
        request["data"] = {"to": to, "from": sender, "message": message}

        return str(request)