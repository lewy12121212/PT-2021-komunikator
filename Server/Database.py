import mysql.connector


# 0 - wszystko ok
# 1 - odrzucone

class Database:

    # konstruktor
    # cur -> cursor
    # conn -> połączenie z bazą
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user="root",
            database='pt_database'
        )
        self.cur = self.conn.cursor()

    # dodaje użytkownika
    def Add_User(self, login, password, auth_key):
        # sprawdzenie czy istnieje w bazie
        if self.Exists(login) == False:
            self.cur.execute("INSERT INTO users (login,password,auth_key, path) VALUES (%s,%s,%s,%s)",
                             [login, password, auth_key, ("./Server/contacts/" + login + ".txt")])
            self.conn.commit()
            print("Dodano użytkownika: ", login)
            return True
        else:
            print("Użytkownik istnieje.")
            return False

    def Select_All(self):
        self.cur.execute("SELECT * FROM users")
        print(self.cur.fetchall())

    def Select_User(self, login):
        if self.Exists(login) == True:
            self.cur.execute("SELECT login, password FROM users WHERE login=%s", [login])
            # print(repr(self.cur.fetchone()))
            return self.cur.fetchone()
        else:
            print("Użytkownik nie istnieje.")
            return 1

    def Delete_User(self, login, password, auth_key):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login)
        if user == (login, password, auth_key):
            self.cur.execute("DELETE FROM users WHERE login=%s", [login])
            self.conn.commit()
            print("Usunięto użytkownika: ", login)
            return True
        else:
            print("Użytkownik nie istnieje.")
            return False

    def Change_Password(self, login, old_password, new_password, auth_key):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login)
        if user != 1:
            if user == (login, old_password, auth_key):
                self.cur.execute("UPDATE users SET password=%s WHERE login=%s", [new_password, login])
                self.conn.commit()
                print("zmieniono haslo uzytkownika: " + login)
                return True
            else:
                print("Nieudana próba zmiany hasła.")
                return False
        else:
            # przypadek niemożliwy - użytkonik nie istnieje
            return False

    def Reset_Password(self, login, new_password, auth_key):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login)
        if self.Exists(login):
            self.cur.execute("SELECT auth_key FROM users WHERE login=%s", [login])
            user_auth_key = self.cur.fetchone()
            if user_auth_key[0] == auth_key:
                self.cur.execute("UPDATE users SET password=%s WHERE login=%s", [new_password, login])
                self.conn.commit()
                print("zresetowano hasło użytkownika: " + login)
                return True
            else:
                print("nieudana autoryzacja użytkownika: " + login)
                return False
        else:
            # przypadek niemożliwy - użytkonik nie istnieje
            return False


    def Logged(self, login):
        self.cur.execute("SELECT logged FROM users WHERE login LIKE %s", [login])
        es = self.cur.fetchall()
        print(es)
        if not es:
            return False
        else:
            return True


    def Exists(self, login):

        self.cur.execute("SELECT * FROM users WHERE login LIKE %s", [login])
        es = self.cur.fetchall()
        if not es:
            return False
        else:
            return True

    def Contacts_Path(self, login):

        self.cur.execute("SELECT path FROM users WHERE login LIKE %s", [login])
        es = self.cur.fetchall()

        if not es:
            return None
        else:
            return str(es).strip('[](),\'')




if __name__ == "__main__":
    d = Database()
    # b = d.Change_Password('admin3','admin2', 'admin2', 'admin1')d
    d.Logged("admin")
    d.Add_User('admin3', 'admin1', 'admin2')
    b = d.Change_Password('admin3', 'admin1', 'admin2', 'admin2')
    b = d.Delete_User('admin3', 'admin2', 'admin2')
    #
