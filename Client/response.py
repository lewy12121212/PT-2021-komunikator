import json
import time
import threading
import gi
import gui_callbacks
import global_functions
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, Gdk
from gi.repository.GdkPixbuf import Pixbuf

from split_msg import main_split
class Response:
    def __init__(self):
        self.lock = threading.Lock()
        self.accept = False
        self.exists = False


    def Make_Response(self, buffer):
        print(buffer)
        signal = ""
        #buffer = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        #print(signal)
        data = tmp["data"]

        if signal == "ACK":
            return True
        elif signal == "RJT":
            return False
        else:
            return False
        
            
    def Make_Response_Thread(self, buffer, window):

        #self.lock.acquire()
        #print(buffer)
        signal = ""
        buffer = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]     
        print(signal, " ", data)

        if signal == "ACK":
            
            with self.lock:
                self.accept = True

            if data["action"] == "login":
                print("daje okejke")
                time.sleep(0.08)
                window.login_window.After_Login()
            elif data["action"] == "add_contact":
                print("DANE: ",data["user"])
                global_functions.contact_user_list.append(str(data["user"]))
                #print(type(data["active"]))
                if data["active"] == 1:
                    #print(data["user"])
                    global_functions.active_user_list.append(data["user"])
                    #print("2")
                    time.sleep(0.08)
                    window.chat_window.refresh_contact_list(str(data["user"]))
                    #print("3")
            elif data["action"] == "del_contact":
                global_functions.contact_user_list.remove(data["user"])
                #print("aktywby ", data["active"])
                if data["active"] == 1:
                    global_functions.active_user_list.remove(data["user"])
                    #window.chat_window.czat._remove_chat(data["user"])
                    time.sleep(0.08)
                    window.chat_window.refresh_contact_list_out(data["user"])
            

            
            print(data["data"]) 
            time.sleep(0.08)
            window.alert_text = data["data"]
            return
                #window.Show_alert(data["data"])
                
                #print(type(data))
                #window.chat_window.Show_alert_window(data)
                

            #print("okejka")
        elif signal == "RJT":
            #print("rejeeect")
            with self.lock:
                self.accept = False
            if data["action"] == "pass_reset_exists":
                self.exists = True
            elif data["action"] == "login_exists":
                self.exists = True

            time.sleep(0.08)
            window.alert_text = data["data"]
            #print("rejeeect")

        #lista kontaktow uzytkownika
        elif signal == "LCU":

            contact = data["contacts"].split(',')
            #print("LCU: ", contact, " len: ", len(contact) )
            if contact[0] != '':
                global_functions.contact_user_list = contact
            

        #lista aktywnych kontaktow
        elif signal == "LAU":
            print(data)
            contact = data["active"].split(',')
            if global_functions.contact_user_list:
                global_functions.active_user_list = list(set(global_functions.contact_user_list).intersection(contact))
            
            if global_functions.active_user_list:
                time.sleep(0.08)
                window.chat_window.active_users()
            

        #przybycie nowego uzytkownika
        elif signal == "NUR":
            contact = data["login"]
            print(repr(contact))
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list.append(contact)
                print("1")
                time.sleep(0.1)
                window.chat_window.refresh_contact_list(contact)
                print("2")
                return 
            #window.refresh_contact_list()
            #window.add_contact(contact)
        
         #przybycie nowego uzytkownika
        elif signal == "NCL":
            contact = data["login"]
            print(data)
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list.remove(contact)
                time.sleep(0.08)
                window.chat_window.refresh_contact_list_out(contact)
           
        
        #odebranie wiadomosci
        elif signal == "MSG":
            mess = [data["date"] + "\n" + data["from"] + ":\n" + main_split(data["message"]), 1]
            print("from ", data["from"], " who ",window.chat_window.uzytkownik)
            #global_functions.income_message_list += mess
            time.sleep(0.08)
            window.chat_window.refresh_chat(mess, data["from"])

        #zaproszenie do znajomych
        elif signal == "CIN":
            #wy??wietlanie okna dialogowego
            pass
        
        elif signal == "CAP":
            contact = data["user"]
            print(repr(contact))
            global_functions.contact_user_list += contact
            global_functions.active_user_list.append(contact)
            time.sleep(0.08)
            window.chat_window.refresh_contact_list(contact)

        else:
            print("oj ne ne ")
        #self.lock.release()
        return


    
