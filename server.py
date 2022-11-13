# Pjesa e serverit
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys
import random
import string
from AESdecrypt import decrypt
from AESencrypt import encrypt

aesKey = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
aesKeyModified = f"aesKey:{aesKey}"


def accept_incoming_connections():
    # Funksioni kur ndokush ben join
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s eshte lidhur." % client_address)
        client.send(
            bytes('\n'.join(["Pershendetje, shtyp emrin i cili do te shfaqet dhe pastaj shtyp butonin 'Enter' per te vazhduar!", aesKeyModified]), "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Argumenti eshte soketa e klientit.
    name = decrypt(aesKey, client.recv(BUFSIZ).decode("utf8"))
    welcome = encrypt('Miresevjen %s! Nese deshiron te largohesh, vetem shkruaj {dil}!' % name, aesKey)
    client.send(bytes(welcome, "utf8"))
    msg = "%s eshte tani i lidhur!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{dil}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{dil}", "utf8"))
            client.close()
            del clients[client]
            if len(clients) == 0:
                SERVER.close()
                sys.exit(0)
                break
            broadcast(bytes("%s u shkyq!" % name, "utf8"))
            break


# prefix perdoret per identifikim te emrit te perdoruesit.
def broadcast(msg, prefix=""):
    # Dergo mesazhin tek te gjithe klientet e lidhur dhe ruaje tek nje file
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
    # Dhe ruaje ate tek nje text file
    if prefix != '':
        with open('mesazhet.txt', 'a') as saveAt:
            saveAt.write('Mesazhi i derguar nga %s %s' % (prefix, msg))
            saveAt.write('\n')
            saveAt.close()


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
