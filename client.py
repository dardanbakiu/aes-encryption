import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *

def on_entry_click(event):        
    global firstclick

    if firstclick:
        firstclick = False
        entry_field.delete(0, "end")

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        root.quit()