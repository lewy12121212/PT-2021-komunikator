import socket
import os
from threading import Thread, Lock
import _thread

host = '127.0.0.1'
port = 9879

class Server:
    #kontruktor
    def __init__(self):
        self.clients = []
        self.clients_lock = Lock()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.th = []
    
    #tworzenie gniazda
    def Initialize(self):
        self.s.bind((host,port))
        self.s.listen(3)

    #wątek z klientem    
    def Transfer_Data(self, client, address):
        print ("Accepted connection from: ", address)
        #dodanie klienta do listy wątków
        with self.clients_lock:
            self.clients.append(client)
        #transmisja
        try:    
            while True:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    print (repr(data))
                    #wysłanie wiadomości do wybranego klienta
                    with self.clients_lock:
                        self.clients[1].sendall(data)
       #po rozłączeniu z klientem - usuwanie z listy wątków                 
        finally:
            with self.clients_lock:
                self.clients.remove(client)
                self.client.close()

    #główna pętla klasy (zbieranie klientów)
    def Begin_Transmision(self):
        while True:
            print("Server is listening for connections...")
            client, address = self.s.accept()
            self.th.append(Thread(target=self.Transfer_Data, args = (client,address)).start())
    
    def Close_Server(self):
        self.s.close()

    #wystartowanie klienta
    def Start(self):
        self.Initialize()
        self.Begin_Transmision()

if __name__ == "__main__":
    s = Server()
    s.Start()


    

    
        

    