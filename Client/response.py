import json
import time
import global_functions


class Response:
    def __init__(self):
        self.accept = False


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
        print(buffer)
        signal = ""
        buffer = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]     

        if signal == "ACK":
            self.accept = True
            if data != "":
                print(type(data))
                #window.chat_window.Show_alert_window(data)
                

            #print("okejka")
        elif signal == "RJT":
            self.accept = False
            if data != "":
                print("a")
                #window.chat_window.Show_alert_window(data)
        #lista kontaktow uzytkownika
        elif signal == "LCU":
            contact = data["contacts"].split(',')
            global_functions.contact_user_list = contact
            

        #lista aktywnych kontaktow
        elif signal == "LAU":
            print(data)
            contact = data["active"].split(',')
            if global_functions.contact_user_list:
                global_functions.active_user_list = list(set(global_functions.contact_user_list).intersection(contact))
            
            if global_functions.active_user_list:
                window.chat_window.active_users()
            

        #przybycie nowego uzytkownika
        elif signal == "NUR":
            contact = data["login"]
            print(repr(contact))
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list.append(contact)
                window.chat_window.refresh_contact_list(contact)
            
            #window.refresh_contact_list()
            #window.add_contact(contact)
        
         #przybycie nowego uzytkownika
        elif signal == "NCL":
            contact = data["login"]
            print(data)
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list.remove(contact)
                window.chat_window.refresh_contact_list_out(contact)
           
        
        #odebranie wiadomosci
        elif signal == "MSG":
            mess = [data["date"] + "\n" + data["from"] + ":\n" + data["message"], 1]
            print("from ", data["from"], " who ",window.chat_window.uzytkownik)
            #global_functions.income_message_list += mess
            if data["from"] != window.chat_window.uzytkownik:
                print("nie tutaj")
                alert = "Masz nową wiadomość od użytkownika " + data["from"] +"."
                #window.chat_window.Show_alert_window(alert)
            window.chat_window.refresh_chat(mess, data["from"])

        #zaproszenie do znajomych
        elif signal == "CIN":
            #wyświetlanie okna dialogowego
            pass
        
        elif signal == "CAP":
            contact = data["user"]
            print(repr(contact))
            global_functions.contact_user_list += contact
            global_functions.active_user_list.append(contact)
            window.chat_window.refresh_contact_list(contact)

        else:
            print("oj ne ne ")
        
        return


    
