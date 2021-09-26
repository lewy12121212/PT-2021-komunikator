import socket
import os
from threading import Thread, Lock
import json
import hashlib
import atexit
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes, keywrap
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import response 

class Client:
    
    
    def __init__(self):

        self.login=''

         # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #random_generator = Random.new().read
        wrapped_key = os.urandom(32)

        # Connect the socket to the port where the server is listening
        self.server_address = ('127.0.0.1', 50000)
        print ('connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)
        #print("sending public key")
        self.sock.send(wrapped_key)

        print("receiveing key")
        data = self.sock.recv(4096)
        print(data)
        #dict_str = data.decode("UTF-8").replace("'", '"')
        #print(dict_str)
        tmp = json.loads(data)
        iv=bytes.fromhex(tmp["iv"])
        wrapkey=bytes.fromhex(tmp["key"])
        key = keywrap.aes_key_unwrap(wrapped_key,wrapkey)
        self.cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        
        
    def depadding(self, message):
            #print(type(message))
        
        for it in reversed(message):
            
            if it != 125:
                message = message[:-1]
                
            else:
                break
        return message   

    #zaszyfrowanie wiadomości
    def encrypt(self, message):
        print("1")
        encryptor = self.cipher.encryptor()
        print("2")
        ciphertext = encryptor.update(message)
        print("3")
        return ciphertext

        #odszyfrowanie wiadomości
    def decrypt(self, ciphertext):
        decryptor = self.cipher.decryptor()
        plaintext = decryptor.update(ciphertext)
        return plaintext


    def send(self,message):
        
        
        if len(message)%16!=0:
            
            while(len(message)%16!=0):
                message+='0'
                
        to_send = self.encrypt(str.encode(message))
        print (len(to_send))
        self.sock.sendall(to_send)
        print("sended")

    def recv(self):
        
        data = self.sock.recv(4096)
        print(data)
        mess = self.decrypt(data)
        print('received "%s"' % mess)
        return mess

    def recv_thread(self, window, respo):
        resp = respo
        
        try:
            while True:
                
                data = self.sock.recv(4096)
                print("11")
                if len(data) != 0:
                    print('received "%s"' % len(data))
                    mess = self.decrypt(data)
                    print("22")
                    mess1 = self.depadding(mess)
                    print("33")
                    resp.Make_Response_Thread(mess1, window)
                    print("44")
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
