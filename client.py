import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *

def on_entry_click(event):        
    global firstclick

    if firstclick:
        firstclick = False
        entry_field.delete(0, "end")
