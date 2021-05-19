import json
import global_functions


class Response:
    def __init__(self):
        self

    def Make_Response(self, buffer):
        print(buffer)
        signal = ""
        #dict_str = buffer.decode("UTF-8").replace("'", '"')
        
        #mydata = ast.literal_eval(dict_str)

        tmp = json.loads(buffer)
        signal = tmp["signal"]
        data = tmp["data"]

        if signal == "ACK":
            return True
        elif signal == "RJT":
            return False
        elif signal == "LCU":
            contact = data["contacts"].split(',')
            global_functions.contact_user_list = contact
            return True
        elif signal == "LAU":
            contact = data["contacts"].split(',')
            global_functions.active_user_list = set(global_functions.contact_user_list).intersection(contact)
        elif signal == "NUR":
            contact = data["login"]
            if contact in (global_functions.contact_user_list):
                global_functions.active_user_list += contact
        

    
