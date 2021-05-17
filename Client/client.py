import socket
import os
from threading import Thread, Lock
import json
import hashlib
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random


def encrypt(message, pub_key):
    cipher = PKCS1_OAEP.new(pub_key)

    return cipher.encrypt(str.encode(message))

def decrypt(ciphertext, priv_key):
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
print(public_key)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 9879)
print ('connecting to %s port %s' % server_address)
sock.connect(server_address)
print("sending public key")
sock.send(public_key.exportKey())
print("receiveing server's public key")
data = sock.recv(2048)
server_publickey = RSA.importKey(data)
print(server_publickey)

def send(message):
    while True:
        # Send data
        #message = input()
        print('sending "%s"' % message)
        to_send = encrypt(message, server_publickey)
        sock.sendall(to_send)

def recv():
    while True:
        data = sock.recv(2048)
        mess = decrypt(data, private_key)
        print('received "%s"' % mess)

#t1 = Thread(target=send)
#t1.start()
t2 = Thread(target=recv)
t2.start()
#t1.join()
t2.join()
'''
while True:{"signal":"MES","data":{"to":"admin1","from":"admin","message":"czesc"}}
    # Send data
    message = input()
    print('sending "%s"' % message)
    to_send = encrypt(message, server_publickey)
    sock.sendall(to_send)
    data = sock.recv(2048)
    mess = decrypt(data, private_key)
    print('received "%s"' % mess)
'''