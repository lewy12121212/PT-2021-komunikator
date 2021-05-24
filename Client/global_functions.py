#Łukasz
#active_user_list = ['nowy','kontakt','ala','olek','kasia','tomek','ania','nie_usuwaj_tych_kontaktow_na_razie_plz']
active_user_list = []
contact_user_list = []

#income_messages_list = [["a",1],["a",1],["a",1],["a",1],["a",1],["a",1],["a",1],["a",1],["Druga wiadomość",2],["qwertyui poiuytr asdfghj mnbvcx sdfghj uytre dfghj nbvcx hjk iuytr dfghj nbvcd dsds",1],["Anna",2]]
income_messages_list = [["elo",1],["Druga wiadomość",2],["qwertyui poiuytr asdfghj mnbvcx sdfghj uytre dfghj nbvcx hjk iuytr dfghj nbvcd dsds",1],["Anna",2],["Takkkkkkkkkkkkkkkkkk",2]]

class MsgList:
    def __init__(self) -> None:
        self.Chat = {}

    def _append_user(self, user):
        self.Chat[user] = []

    def _remove_user(self, user):
        del self.Chat[user]

    def _append_msg(self, user, msg):
        #["a",1]
        self.Chat[user].append(msg)

    def _get_msg(self,user):
        #zwraca tabele wiadomosci
        return self.Chat[user]
