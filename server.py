# Pjesa e serverit
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
import sys


def accept_incoming_connections():
    # Funksioni kur ndokush ben join
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s eshte lidhur." % client_address)
        client.send(
            bytes("Pershendetje, shtyp emrin i cili do te shfaqet dhe pastaj shtyp butonin 'Enter' per te vazhduar!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Argumenti eshte soketa e klientit.
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Miresevjen %s! Nese deshiron te largohesh, vetem shkruaj {quit}!' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s eshte tani i lidhur!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
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
    with open('mesazhet.txt', 'a') as saveAt:
        saveAt.write('Perdoruesi %s dergoi mesazhin: %s' % (prefix, msg))
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
