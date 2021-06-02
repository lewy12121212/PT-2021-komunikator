import socket
import time
from threading import Thread, Lock
import Database
import Response
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

host = '127.0.0.1'
port = 9879

clients = dict()

class Server:


    #kontruktor
    def __init__(self):
        
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
    def Set_Parameters(self, client, private_key, client_key, DB):
        login =''
        rs = Response.Response(DB)


        s = {"to": "self", "data": ""}

        try:
            while s["to"] == "self":
                data = client.recv(4096)
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
            contacts_list = []
            path = DB.Contacts_Path(login)
            print(path)

            with open(path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip()
                    contacts_list.append(line)
                f.close()
            
            #print(contacts_list)

            str_of_contacts_list = str({"signal": "LCU", "data": {"contacts": ','.join(contacts_list)}})
            client.sendall(self.encrypt(str.encode(str_of_contacts_list), client_key))

            #wyslanie listy zalogowanych uzytkownikow 
            time.sleep(0.05) 
            if clients:
                
                list_of_active_users = []
                with self.clients_lock:
                    for cli in clients:
                        list_of_active_users.append(cli)

                str_of_users_list = str({"signal": "LAU", "data": {"active": ','.join(list_of_active_users)}})
                #print(str_of_users_list)
                client.sendall(self.encrypt(str.encode(str_of_users_list), client_key))
        except:
            return login

        return login


    #wątek z klientem    
    def Transfer_Data(self, client, address):
        print ("Accepted connection from: ", address)

        DB = Database.Database()

        #generowanie kluczy rsa servera
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        public_key = private_key.public_key()
        public_key_to_send = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        #pobranie klucza od klienta
        get_client_key = client.recv(4096)
        #print(get_client_key)
        client_key = serialization.load_pem_public_key(get_client_key) 
        #print(client_key)
        client.sendall(public_key_to_send)
        
        end = 0

        while(end != 1):
            login = self.Set_Parameters(client, private_key, client_key, DB)
            print(login)
            if login == '':
                client.close()
                print("ok")
                return
            else:
                end = self.MainFunctionThread(login, DB, client, private_key)
                if end == 0:
                    inform_all = {"signal": "NCL", "data": {"login": login}}
                    del clients[login]                
                    print("close client")
                    del self.clients_publickeys[login]
                    self.Send_All(str(inform_all))
                    

        
        DB.Change_Logged(login)
        with self.clients_lock:                                
            clients[login].shutdown(socket.SHUT_RDWR)
            inform_all = {"signal": "NCL", "data": {"login": login}}
            del clients[login]                
            print("close client")
            del self.clients_publickeys[login]
        
        self.Send_All(str(inform_all))  
        print("close client")
        
        

    def MainFunctionThread(self, login, DB, client, private_key):
        end = 0
        rs = Response.Response(DB)
        #dodanie klienta do listy wątków
        with self.clients_lock:
            clients[login] = client

        #transmisja
        #self.Send_All('okon')
        resp = {"to": "", "data": ""}
          
        while resp["data"] != "END":
            data = client.recv(4096)
            if not data:
                break
            else:
                data = self.decrypt(data, private_key)
                resp = rs.Make_Response(data)
                if resp["data"] != "END" and not rs.logOut:
                        #wysłanie wiadomości do wybranego klienta
                    with self.clients_lock:
                            #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                        clients[resp["to"]].sendall(self.encrypt(str.encode(resp["data"]), self.clients_publickeys[resp["to"]]))
                elif rs.logOut:
                    end = 0
                    with self.clients_lock:
                        #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                        clients[resp["to"]].sendall(self.encrypt(str.encode(resp["data"]), self.clients_publickeys[resp["to"]]))
                    break
                else:
                    end = 1 
                    break
        return end



    #główna pętla servera (akceptowanie nowych klientów i uruchamianie wątków do transmisji z nimi)
    def Begin_Transmision(self):
        while True:
            print("Server is listening for connections...")
            client, address = self.s.accept()
            self.th.append(Thread(target=self.Transfer_Data, args = (client,address)).start())


    def Send_All(self, message):

        print(message)
        with self.clients_lock:
            if clients:
                for client in clients:
                    #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                    clients[client].sendall(self.encrypt(str.encode(message), self.clients_publickeys[client]))


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


    

    
        

    