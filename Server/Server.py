import socket
import time
from threading import Thread, Lock
import Database
import Response
import os
import json 
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, keywrap
#from cryptography.hazmat.primitives.asymmetric import padding

host = '127.0.0.1'
port = 50000

clients = dict()

DB = Database.Database()

class Server:


    #kontruktor
    def __init__(self):
        
        self.clients_lock = Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.th = []
        self.clients_publickeys = dict()
        self.keys_lock = Lock()
        self.active_conetion = 0

    #tworzenie gniazda
    def Initialize(self):
        self.s.bind((host, port))
        self.s.listen(3)

    #przesłanie kluczy publicznych między klientem a serverem, działa do momentu zalogowania użytkonika
    #po czym mapuje login użytkonwnika z jego kanałem i kluczem publicznym 
    def Set_Parameters(self, client, cipher, cur):
        login =''
        rs = Response.Response(cur)


        s = {"to": "self", "data": ""}

        try:
            while s["to"] == "self":
                data = client.recv(4096)
                if not data:
                    break
                else:
                    data = self.decrypt(data, cipher)
                    #print(data)
                    #wysłanie wiadomości do wybranego klienta    
                    s = rs.Make_Response(data)
                    #print(s)
                    if s["data"] == "END":
                        return login
                
                pad = s["data"]
                #print(repr(pad))
                packet = self.padding(pad)
               
                client.sendall(self.encrypt(str.encode(packet), cipher))
                        
                login = s["to"]
                #print(login)
            

            #time.sleep(0.1) 
            #wysłanie klientowi listy zalogowanych klientów
            contacts_list = []
            path = DB.Contacts_Path(login, cur)
            #print(path)

            with open(path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.rstrip()
                    contacts_list.append(line)
                f.close()
            
            #print(contacts_list)

            str_of_contacts_list = str({"signal": "LCU", "data": {"contacts": ','.join(contacts_list)}})
            packet = self.padding(str_of_contacts_list)
            client.sendall(self.encrypt(str.encode(packet), cipher))

            #wyslanie listy zalogowanych uzytkownikow 
            #data = client.recv(4096)
            time.sleep(0.4)
                
            list_of_active_users = []
            if clients:
                with self.clients_lock:
                    for cli in clients:
                        list_of_active_users.append(cli)

            str_of_users_list = str({"signal": "LAU", "data": {"active": ','.join(list_of_active_users)}})
                #print(str_of_users_list)
            packet = self.padding(str_of_users_list)
            client.sendall(self.encrypt(str.encode(packet), cipher))
        except:
            self.active_conetion -= 1
            t = time.localtime()
            print(time.strftime("%H:%M:%S", t)," Active connetion: ", self.active_conetion)
            return login
        
        data = client.recv(4096)

        with self.keys_lock:
            self.clients_publickeys[login]=cipher
            #informowanie wszystkich klientów o nowozalogwanym
            inform_all = {"signal": "NUR", "data": {"login": login}}
            self.Send_All(str(inform_all))

        return login


    #wątek z klientem    
    def Transfer_Data(self, client, address):
        t = time.localtime()
        print (time.strftime("%H:%M:%S", t), " Accepted connection from: ", address)

        cur = DB.conn.cursor()

        #generowanie kluczy rsa servera
        #self.active_conetion += 1

        key = os.urandom(32)
        iv = os.urandom(16)

        wrapped_key = client.recv(256)

        wrapkey = keywrap.aes_key_wrap(wrapped_key,key)

        to_send = {'key':wrapkey.hex(),'iv':iv.hex()}
        #pakowanie klucza
        mess = json.dumps(to_send)
        client.sendall(str.encode(mess))
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        
        
        end = 0

        while(end != 1):
            login = self.Set_Parameters(client, cipher, cur)
            #print(login)
            if login == '':
                t1 = time.localtime()
                client.close()
                self.active_conetion -= 1
                print(time.strftime("%H:%M:%S", t1), " Active connection: ", self.active_conetion)
                #print("ok")
                return
            else:
                end = self.MainFunctionThread(login, cur, client, cipher)
                if end == 0:
                    
                    ack = str({"signal": "ACK", "data": {"action": "logout"}})
                    packet = self.padding(ack)
                    client.sendall(self.encrypt(str.encode(packet), cipher))
                    data = client.recv(4096)
                    inform_all = {"signal": "NCL", "data": {"login": login}}
                    DB.Change_Logged(login, cur)
                    del clients[login]
                    t2 = time.localtime()                
                    print(time.strftime("%H:%M:%S", t2), " close client ", login)
                    del self.clients_publickeys[login]
                    self.Send_All(str(inform_all))
                    

        
        DB.Change_Logged(login, cur)
        with self.clients_lock: 
            try:      
                t2 = time.localtime()                         
                clients[login].shutdown(socket.SHUT_RDWR)
                ack = str({"signal": "ACK", "data": {"action": "logout"}})
                packet = self.padding(ack)
                client.sendall(self.encrypt(str.encode(packet), cipher))
                data = client.recv(4096)
                inform_all = {"signal": "NCL", "data": {"login": login}}
                del clients[login]                
                t2 = time.localtime()                
                print(time.strftime("%H:%M:%S", t2), "close client ", login)
                del self.clients_publickeys[login]
                self.active_conetion -= 1
                print(time.strftime("%H:%M:%S", t2), " Active connetion: ", self.active_conetion)
            except:
                inform_all = {"signal": "NCL", "data": {"login": login}}
                del clients[login]                
                t2 = time.localtime()                
                print(time.strftime("%H:%M:%S", t2), "close client ", login)
                del self.clients_publickeys[login]
                self.active_conetion -= 1
                print(time.strftime("%H:%M:%S", t2), " Active connetion: ", self.active_conetion)
        
        self.Send_All(str(inform_all))  
        #print("close client")
        
        

    def MainFunctionThread(self, login, cur, client, cipher):
        end = 0
        rs = Response.Response(cur)
        #dodanie klienta do listy wątków
        with self.clients_lock:
            clients[login] = client

        #transmisja
        resp = {"to": "", "data": ""}
        try: 
            while resp["data"] != "END":
                data = client.recv(4096)
                if not data:
                    break
                else:
                    data = self.decrypt(data, cipher)
                    #print(data)
                    resp = rs.Make_Response(data)
                    #print(resp)
                    if resp["data"] != "END" and not rs.logOut:
                            #wysłanie wiadomości do wybranego klienta
                        with self.clients_lock:
                            packet = self.padding((resp["data"]))
                            #print(clients[resp["to"]])
                            clients[resp["to"]].sendall(self.encrypt(str.encode(packet), self.clients_publickeys[resp["to"]]))
                    elif rs.logOut:
                        end = 0                        
                        break
                    else:
                        end = 1 
                        break
        except:
            rs.logOut = False
            end = 1
            return end
        rs.logOut = False
        return end



    #główna pętla servera (akceptowanie nowych klientów i uruchamianie wątków do transmisji z nimi)
    def Begin_Transmision(self):
        while self.active_conetion < 100:
            
            print("Server is listening for connections...")
            client, address = self.s.accept()
            self.th.append(Thread(target=self.Transfer_Data, args = (client,address)).start())
            self.active_conetion += 1 
            t = time.localtime()
            print(time.strftime("%H:%M:%S", t), " Active connetion: ", self.active_conetion)



    def Send_All(self, message):

        #print(message)
        with self.clients_lock:
            if clients:
                for client in clients:
                    #zaszyfrowanie wiadomości kluczem publicznym adresowanego klienta i wysłanie do niego
                    packet = self.padding(message)
                    clients[client].sendall(self.encrypt(str.encode(packet), self.clients_publickeys[client]))


    def Close_Server(self):
        self.s.close()

    #zaszyfrowanie wiadomości
    def encrypt(self, message, cipher):
        #print(message)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message)
        return ciphertext

        #odszyfrowanie wiadomości
    def decrypt(self, ciphertext, cipher):
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        #print("print" + plaintext)
        return plaintext

    #dopełnia zerami wiadomość do wielokrotności bloku CBC
    def padding(self, message):
        #print(type(message))
        if len(message)%16!=0:
            while(len(message)%16!=0):
                message+='0'
       
        return message


    #wystartowanie klienta
    def Start(self):
        self.Initialize()
        self.Begin_Transmision()

if __name__ == "__main__":
    s = Server()
    s.Start()


    

    
        

    