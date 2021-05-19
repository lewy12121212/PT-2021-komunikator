import socket
import os
from threading import Thread, Lock
import json
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

    #zaszyfrowanie wiadomości
def encrypt(message, public_key):
    ciphertext = public_key.encrypt(message,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return ciphertext

    #odszyfrowanie wiadomości
def decrypt(ciphertext, private_key):
    plaintext = private_key.decrypt(ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return plaintext

#random_generator = Random.new().read
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()
public_key_to_send = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 9879)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
print("sending public key")
sock.send(public_key_to_send)

print("receiveing server's public key")
data = sock.recv(2048)
server_publickey = serialization.load_pem_public_key(data)
print(server_publickey)


def send():
    while True:
        # Send data
        message = input()
        print('sending "%s"' % message)
        to_send = encrypt(str.encode(message), server_publickey)
        #print(to_send)
        sock.sendall(to_send)

def recv():
    while True:
        data = sock.recv(2048)
        mess = decrypt(data, private_key)
        print('received "%s"' % mess)

t1 = Thread(target=send)
t1.start()
t2 = Thread(target=recv)
t2.start()
t1.join()
t2.join()