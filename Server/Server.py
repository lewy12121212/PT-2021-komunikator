import socket
from threading import Thread, Lock
import Database
import Response
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

host = '127.0.0.1'
port = 9879
DB = Database.Database()


class Server:


    #kontruktor
    def __init__(self):
        self.clients = dict()
        self.clients_lock = Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.th = []
        self.clients_publickeys = dict()
        self.keys_lock = Lock()
    
    #tworzenie gniazda
    def Initialize(self):
        self.s.bind((host, port))
        self.s.listen(3)

    #przesłanie kluczy publicznych między klientem a serverem, działa do momentu zalogowania użytkonika
    #po czym mapuje login użytkonwnika z jego kanałem i kluczem publicznym 
    def Set_Parameters(self, client, public_key, private_key):
        login =''
        rs = Response.Response()
        get_client_key = client.recv(2048)
        #print(get_client_key)
        client_key = serialization.load_pem_public_key(get_client_key) 
        #print(client_key)
        client.sendall(public_key)

        s = {"to": "self", "data": ""}
        while s["to"] == "self":
            data = client.recv(2048)
            if not data:
                break
            else:
                data = self.decrypt(data, private_key)
                print(data)
                #wysłanie wiadomości do wybranego klienta    
                s = rs.Make_Response(data)
                client.sendall(self.encrypt(str.encode(s["data"]), client_key))
        login = s["to"]

        with self.keys_lock:
            self.clients_publickeys[login]=client_key
        #informowanie wszystkich klientów o nowozalogwanym
        inform_all = {"signal": "NUR", "data": {"login": login}}
        self.Send_All(str(inform_all))

        #wysłanie klientowi listy zalogowanych klientów
        if self.clients:
            list_of_users = []
            with self.clients_lock:
                for cli in self.clients:
                    list_of_users.append(cli)

            str_of_users_list = str({"signal": "LUS", "data": {"active": ','.join(list_of_users)}})
            client.sendall(self.encrypt(str.encode(str_of_users_list), client_key))

        return login


    #wątek z klientem    
    def Transfer_Data(self, client, address):
        print ("Accepted connection from: ", address)
        #generowanie kluczy rsa servera
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        public_key_to_send = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        login = self.Set_Parameters(client, public_key_to_send, private_key)
        rs = Response.Response()
        #dodanie klienta do listy wątków
        with self.clients_lock:
            self.clients[login] = client

        #transmisja
        #self.Send_All('okon')
        try:    
            while True:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    data = self.decrypt(data,private_key)
                    resp = rs.Make_Response(data)
                    #wysłanie wiadomości do wybranego klienta
                    with self.clients_lock:
                        #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                        self.clients[resp["to"]].sendall(self.encrypt(str.encode(resp["data"]), self.clients_publickeys[resp["to"]]))

       #po rozłączeniu z klientem - usuwanie z listy wątków                 
        finally:
            with self.clients_lock:
                del self.clients[login]
                del self.clients_publickeys[login]
                self.client.close()

    #główna pętla servera (akceptowanie nowych klientów i uruchamianie wątków do transmisji z nimi)
    def Begin_Transmision(self):
        while True:
            print("Server is listening for connections...")
            client, address = self.s.accept()
            self.th.append(Thread(target=self.Transfer_Data, args = (client,address)).start())


    def Send_All(self, message):

        with self.clients_lock:
            if self.clients:
                for client in self.clients:
                    #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                    self.clients[client].sendall(self.encrypt(str.encode(message), self.clients_publickeys[client]))


    def Close_Server(self):
        self.s.close()

    #zaszyfrowanie wiadomości
    def encrypt(self, message, public_key):
        ciphertext = public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return ciphertext

    #odszyfrowanie wiadomości
    def decrypt(self, ciphertext, private_key):
        plaintext = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return plaintext


    #wystartowanie klienta
    def Start(self):
        self.Initialize()
        self.Begin_Transmision()

if __name__ == "__main__":
    s = Server()
    s.Start()


    

    
        

    