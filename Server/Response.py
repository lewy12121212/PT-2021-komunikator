import json

def make_response(buffer):
    data = json.loads(buffer)
    print(json.dumps(data)) 