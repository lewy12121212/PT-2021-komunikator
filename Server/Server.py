import socket
import os
from threading import Thread, Lock
import _thread
import Response as rs
import json
import Database

host = '127.0.0.1'
port = 9879
DB = Database.Database()

class Server:
    #DB = Database.Database()
    #kontruktor
    def __init__(self):
        self.clients = []
        self.clients_lock = Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.th = []
        self.tmp = []
    
    #tworzenie gniazda
    def Initialize(self):
        self.s.bind((host,port))
        self.s.listen(3)

    #wątek z klientem    
    def Transfer_Data(self, client, address):
        print ("Accepted connection from: ", address)
        #pobranie loginu do zmapowania go z odpowiednim indeksem w tablicy klientów
        login = self.Set_Configuration(client)

        #tmp przechowuje zmapowany login z indeksem w tablicy klientów
        with self.clients_lock:
            self.clients.append(client)
            index = self.clients.index(client)
            self.tmp.append({login,index})
            
        #transmisja
        try:    
            while True:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    print (repr(data))
                    
                    #wysłanie wiadomości do wybranego klienta
                    #założenie blokday na listę klientów
                    with self.clients_lock:
                        response = rs.Make_Response(data)
                        self.clients[tmp[response["to"]]].sendall(response["data"])
       #po rozłączeniu z klientem - usuwanie z listy wątków                 
        finally:
            with self.clients_lock:
                self.clients.remove(client)
                self.client.close()
                print("+1")

    #główna pętla klasy (zbieranie klientów)
    def Begin_Transmision(self):
        while True:
            print("Server is listening for connections...")
            client, address = self.s.accept()
            self.th.append(Thread(target=self.Transfer_Data, args = (client,address)).start())
    
    def Close_Server(self):
        self.s.close()

    #odbywa się do momemntu zalogowania się użytkownika, po czym zwraca jego login do zmapowania go z nr. wątku
    def Set_Configuration(self, client):
         #transmisja
        response = {"to":'',"data":''}
          
        while response["to"] == '':
            data = client.recv(1024)
            if not data:
                break
            else:
                print (repr(data))
                    
                #wysłanie wiadomości do wybranego klienta
                response = rs.Make_Response(data)
                client.sendall(str.encode(response["data"]))                

        return response["to"]



    #wystartowanie klienta
    def Start(self):
        self.Initialize()
        self.Begin_Transmision()

if __name__ == "__main__":
    s = Server()
    s.Start()


    

    
        

    