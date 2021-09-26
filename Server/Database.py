import mysql.connector
import time

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
        self.conn.autocommit = True
        #cur = self.conn.cursor()

    # dodaje użytkownika
    def Add_User(self, login, password, auth_key1, auth_key2, auth_key3, cur):
        # sprawdzenie czy istnieje w bazie
        if self.Exists(login,cur) == False:
            cur.execute("INSERT INTO users (login,password,auth_key1, auth_key2, auth_key3, path) VALUES (%s,%s,%s,%s,%s,%s)",
                             [login, password, auth_key1, auth_key2, auth_key3, ("./Server/contacts/" + login + ".txt")])
            #cur.commit()
            t = time.localtime()
            self.conn.commit()
            print(time.strftime("%H:%M:%S", t)," Added user: ", login)
            return True
        else:
            #print("Użytkownik istnieje.")
            return False

    def Select_All(self,cur):
        cur.execute("SELECT * FROM users")
        #print(cur.fetchall())

    def Select_User(self, login, cur):
        if self.Exists(login, cur) == True:
            cur.execute("SELECT login, password, auth_key1, auth_key2, auth_key3  FROM users WHERE login=%s", [login])
            #print(repr(cur.fetchone()))
            return cur.fetchone()
        else:
            print("Użytkownik nie istnieje.")
            return 1

    def Delete_User(self, login, password, auth_key, auth_key1, auth_key2, cur):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login, cur)
        if user == (login, password, auth_key, auth_key1, auth_key2):
            cur.execute("DELETE FROM users WHERE login=%s", [login])
            self.conn.commit()
            t = time.localtime()
            print(time.strftime("%H:%M:%S", t)," Deleted user: ", login)
            return True
        else:
            print("Użytkownik nie istnieje.")
            return False

    def Change_Password(self, login, old_password, new_password, cur):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login, cur)
        if user != 1:
            if  user[0:2] == (login, old_password):
                cur.execute("UPDATE users SET password=%s WHERE login=%s", [new_password, login])
                self.conn.commit()
                t = time.localtime()
                print(time.strftime("%H:%M:%S", t), " ", login + " changed password")
                return True
            else:
                t = time.localtime()
                print(time.strftime("%H:%M:%S", t), " password change failure")
                return False
        else:
            # przypadek niemożliwy - użytkonik nie istnieje
            return False

    def Reset_Password(self, login, new_password, auth_key, auth_key1, auth_key2, cur):
        # sprawdzanie poprawności danych (czy z formularza zgadzają się z tymi z bazy)
        user = self.Select_User(login, cur)
        if self.Exists(login, cur):
            cur.execute("SELECT auth_key1, auth_key2, auth_key3 FROM users WHERE login=%s", [login])
            user_auth_key = cur.fetchone()
            #print(repr(user_auth_key))
            if user_auth_key == (auth_key, auth_key1, auth_key2):
                cur.execute("UPDATE users SET password=%s WHERE login=%s", [new_password, login])
                self.conn.commit()
                t = time.localtime()
                print(time.strftime("%H:%M:%S", t), " ",login + " reseted password")
                return True
            else:
                #print("nieudana autoryzacja użytkownika: " + login)
                return False
        else:
            # przypadek niemożliwy - użytkonik nie istnieje
            return False

    def Change_Logged(self, login, cur):
        
        if self.Exists(login, cur):
            if self.IfLogged(login, cur):
                cur.execute("UPDATE users SET logged=%s WHERE login=%s", ['0', login])
                self.conn.commit()
                #self.conn.close()
                
                #print(login, '+')
                return True
            else:
                cur.execute("UPDATE users SET logged=%s WHERE login=%s", ['1', login])
                self.conn.commit()
                #self.conn.close()
                
                #print(login, '-')
                return True
        else:
            #print('++')
            # przypadek niemożliwy - użytkonik nie istnieje
            return False


    def IfLogged(self, login, cur):
        cur.execute("SELECT logged FROM users WHERE login LIKE %s", [login])
        es = cur.fetchall()
        es = str(es).strip('[](),\'')
        #print(login, ' ', es)
        if es == '0':
            return False
        else:
            return True


    def Exists(self, login, cur):

        cur.execute("SELECT * FROM users WHERE login LIKE %s", [login])
        es = cur.fetchall()
        if not es:
            return False
        else:
            return True

    def Contacts_Path(self, login, cur):

        cur.execute("SELECT path FROM users WHERE login LIKE %s", [login])
        es = cur.fetchall()

        if not es:
            return None
        else:
            return str(es).strip('[](),\'')




if __name__ == "__main__":
    d = Database()
    # b = d.Change_Password('admin3','admin2', 'admin2', 'admin1')d
    print(d.IfLogged("admin"))
