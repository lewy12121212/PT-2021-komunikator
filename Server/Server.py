import socket
from threading import Thread, Lock
import Database
import Response
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random

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
        client_key = RSA.importKey(get_client_key)
        #print(client_key)
        client.sendall(public_key.exportKey())

        s = {"to": "self", "data": ""}
        while s["to"] == "self":
            data = client.recv(2048)
            if not data:
                break
            else:
                data = self.decrypt(data, private_key)
                #wysłanie wiadomości do wybranego klienta    
                s = rs.Make_Response(data)
                client.sendall(self.encrypt(str.encode(s["data"]), client_key))
        login = s["to"]

        with self.keys_lock:
            self.clients_publickeys[login]=client_key

        return login


    #wątek z klientem    
    def Transfer_Data(self, client, address):
        print ("Accepted connection from: ", address)
        #generowanie kluczy rsa servera
        random_generator = Random.new().read
        private_key = RSA.generate(1024, random_generator)
        public_key = private_key.publickey()

        login = self.Set_Parameters(client, public_key, private_key)
        rs = Response.Response()
        #dodanie klienta do listy wątków
        with self.clients_lock:
            self.clients[login] = client

        #transmisja
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
    
    def Close_Server(self):
        self.s.close()

    #zaszyfrowanie wiadomości
    def encrypt(self, message, pub_key):
        cipher = PKCS1_OAEP.new(pub_key)
        return cipher.encrypt(message)

    #odszyfrowanie wiadomości
    def decrypt(self, ciphertext, priv_key):
        cipher = PKCS1_OAEP.new(priv_key)
        return cipher.decrypt(ciphertext)


    #wystartowanie klienta
    def Start(self):
        self.Initialize()
        self.Begin_Transmision()

if __name__ == "__main__":
    s = Server()
    s.Start()


    

    
        

    