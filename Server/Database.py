import sqlite3
from sqlite3 import Error

# 0 - wszystko ok
# 1 - odrzucone

class Database:
    
    #konstruktor 
    #cur -> cursor
    #conn -> połączenie z bazą
    def __init__(self):
        self.conn = sqlite3.connect('C:/Python Project/PT-2021-komunikator/Server/database.db', check_same_thread=False)
        self.cur = self.conn.cursor()

    #dodaje użytkownika
    def Add_User(self, login, password, auth_key):
        #sprawdzenie czy istnieje w bazie
        if self.Exists(login)==False:
            self.cur.execute("INSERT INTO users VALUES (?,?,?)", (login, password, auth_key))
            self.conn.commit()
            print("Dodano użytkownika: ", login)
            return 0
        else:
            print("Użytkownik istnieje.")
            return 1

    def Select_All(self):
        print(self.cur.execute("SELECT * FROM users").fetchall())

    def Select_User(self, login):
        if self.Exists(login)==True:
            self.cur.execute('SELECT login, password FROM users WHERE login=?', [login])
            #print(repr(self.cur.fetchone()))
            return self.cur.fetchone()
        else:
            print("Użytkownik nie istnieje.")
            return 1

    def Delete_User(self, login,password,auth_key):
        #sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login)
        if user == (login,password,auth_key):
            self.cur.execute("DELETE FROM users WHERE login=?", [login])
            self.conn.commit()
            print("Usunięto użytkownika: ", login)
            return 0
        else:
            print("Użytkownik nie istnieje.")
            return 1

    def Change_Password(self, login, old_password, new_password, auth_key):
        #sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login)
        if user != 1:
            if user == (login, old_password, auth_key):
                self.cur.execute("UPDATE users SET password=? WHERE login=?",(new_password,login))
                self.conn.commit()
                return 0
            else:
                print("Nieudana próba zmiany hasła.")
                return 1
        else:
            #przypadek niemożliwy - użytkonik nie istnieje
            return 1        

    def Exists(self, login):
        if (self.cur.execute('SELECT * FROM users WHERE login=?', [login]).fetchone() == None):
            return False
        else:    
            return True
        
        

if __name__ == "__main__":
    d = Database()
    #b = d.Change_Password('admin3','admin2', 'admin2', 'admin1')
    #d.Add_User('admin','admin1','admin2')
    b = d.Delete_User('admin3','admin2','admin2')
    print(b)
    