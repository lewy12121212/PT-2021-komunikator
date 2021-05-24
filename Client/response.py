import json
import global_functions


class Response:
    def __init__(self):
        self


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
        
            
    def Make_Response_Thread(self, buffer, window):
        print(buffer)
        signal = ""
        buffer = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]     

        #lista kontaktow uzytkownika
        if signal == "LCU":
            contact = data["contacts"].split(',')
            global_functions.contact_user_list = contact
            

        #lista aktywnych kontaktow
        elif signal == "LAU":
            print(data)
            contact = data["active"].split(',')
            global_functions.active_user_list = list(set(global_functions.contact_user_list).intersection(contact))

            window.refresh_contact_list()
            

        #przybycie nowego uzytkownika
        elif signal == "NUR":
            contact = data["login"]
            print(repr(contact))
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list.append(contact)
            
            window.refresh_contact_list()
        
        #odebranie wiadomosci
        elif signal == "MSG":
            mess = [data["from"] + ": " + data["message"], 1]
            #global_functions.income_message_list += mess
            window.refresh_chat(mess)
        
        return


    
