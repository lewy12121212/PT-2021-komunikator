import socket
import os
from threading import Thread, Lock
import json
import hashlib
import atexit
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import response 

class Client:
    
    
    def __init__(self):

        self.login=''

         # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #random_generator = Random.new().read
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
        public_key = self.private_key.public_key()
        public_key_to_send = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', 9879)
        print ('connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)
        print("sending public key")
        self.sock.send(public_key_to_send)

        print("receiveing server's public key")
        data = self.sock.recv(4096)
        self.server_publickey = serialization.load_pem_public_key(data)
        print(self.server_publickey)
        

    #zaszyfrowanie wiadomości
    def encrypt(self, message):
        ciphertext = self.server_publickey.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return ciphertext

        #odszyfrowanie wiadomości
    def decrypt(self, ciphertext):
        plaintext = self.private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
        return plaintext


    def send(self,message):

        # Send data
        #message = input()
        print('sending "%s"' % len(message))
        to_send = self.encrypt(str.encode(message))
        #print(to_send)
        self.sock.sendall(to_send)

    def recv(self):
        
        data = self.sock.recv(4096)
        mess = self.decrypt(data)
        print('received "%s"' % mess)
        return mess

    def recv_thread(self, window):
        #window = arg[0]
        try:
            while True:
                resp = response.Response()

                data = self.sock.recv(4096)
                if len(data) != 0:
                    print('received "%s"' % len(data))
                    mess = self.decrypt(data)
                        #print(mess)

                    resp.Make_Response_Thread(mess, window)
        except:
            print('thread except')
            return
        finally:
            print('thread except')
            return



        #window.refresh_chat()
        #print('received "%s"' % mess)

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        

if __name__ == "__main__":
    c = Client()
    c.send("{'signal': 'LOG', 'data': {'login': 'admin', 'password': 'admin'}}")
    print(c.recv(4096))
