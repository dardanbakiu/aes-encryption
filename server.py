# Pjesa e serverit
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys
import random
import string
from AESencrypt import encrypt
from AESdecrypt import decrypt
from textwrap import wrap

aesKey = ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def accept_incoming_connections():
    # Funksioni kur ndokush ben join
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s eshte lidhur." % client_address)
        client.send(
            bytes('\n'.join(["Pershendetje, shtyp emrin i cili do te shfaqet dhe pastaj shtyp butonin 'Enter' per te vazhduar!", aesKey]), "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Argumenti eshte soketa e klientit.
    name = decryptBy32(client.recv(BUFSIZ).decode("utf8"))
    welcome = "Miresevjen %s ne Broadcast AES Chat!" % name
    client.send(bytes(encryptBy16(welcome), "utf8"))
    msg = "%s eshte tani i lidhur!" % name
    broadcast(bytes(encryptBy16(msg), "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        broadcast(msg, name+": ")


# prefix perdoret per identifikim te emrit te perdoruesit.
def broadcast(msg, prefix=""):
    # Dergo mesazhin tek te gjithe klientet e lidhur
    for sock in clients:
        print(bytes(prefix, "utf8")+msg)
        sock.send(bytes(encryptBy16(prefix), "utf8")+msg)
    # Dhe ruaje ate tek nje text file
    if prefix != '':
        with open('mesazhet.txt', 'a') as saveAt:
            saveAt.write('Mesazhi i derguar nga %s %s' % (prefix, msg))
            saveAt.write('\n')
            saveAt.close()


def encryptBy16(msg):
    #Ndaje msg nga 16 karaktere
    msg_list = wrap(
    msg,
    16,
    drop_whitespace=False,
    break_on_hyphens=False
    )
    encMsg = ''
    for msgPiece in msg_list:
        encMsg = encMsg + encrypt(msgPiece, aesKey)
    return encMsg
    
def decryptBy32(msg):
    #Ndaje msg nga 16 karaktere
    msg_list = wrap(
    msg,
    32,
    drop_whitespace=True,
    break_on_hyphens=False
    )
    decMsg = ''
    for msgPiece in msg_list:
        decMsg = decMsg + decrypt(aesKey, msgPiece)
    return decMsg

clients = {}
addresses = {}

HOST = 'localhost'
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(AF_INET, SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Duke pritur per lidhje nga klientet...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
