import json

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

    
