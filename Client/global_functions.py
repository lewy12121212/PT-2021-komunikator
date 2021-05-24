active_user_list = ["Tytus", "Romek", "Atomek"]

income_messages_list = [["elo",1],["Druga wiadomość",2],["qwertyui poiuytr asdfghj mnbvcx sdfghj uytre dfghj nbvcx hjk iuytr dfghj nbvcd dsds",1],["Anna",2],["Takkkkkkkkkkkkkkkkkk",2]]

class MsgList:
    def __init__(self) -> None:
        self.Chat = {}

    def _append_user(self, user):
        self.Chat[user] = []

    def _remove_user(self, user):
        del self.Chat[user]

    def _append_msg(self, user, msg):
        self.Chat[user].push(msg)