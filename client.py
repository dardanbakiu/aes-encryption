import socket
from socket import AF_INET, SOCK_STREAM
import string
from threading import Thread
from tkinter import *
from AESencrypt import encrypt
from AESdecrypt import decrypt
from textwrap import wrap

firstclick = True

aesKey = ''

def on_entry_click(event):
    global firstclick

    if firstclick:
        firstclick = False
        entry_field.delete(0, "end")


def receive():
    while True:
        try:
            global aesKey
            if aesKey == '':
                msg, getAesKey = client_socket.recv(
                    BUFSIZ).decode("utf8").split('\n')
                aesKey = getAesKey
                msg_list.insert(END, msg)
            else:
                encMsg = client_socket.recv(BUFSIZ).decode("utf8")
                dcMsg = decryptBy32(encMsg)
                msg_list.insert(END, dcMsg)
        except OSError:
            break
               
               
def encryptBy16(msg):
    #Ndaje msg nga 16 karaktere
    msg_listE = wrap(
    msg,
    16,
    drop_whitespace=False,
    break_on_hyphens=False
    )
    encMsg = ''
    for msgPiece in msg_listE:
        encMsg = encMsg + encrypt(msgPiece, aesKey)
    return encMsg
    
def decryptBy32(msg):
    #Ndaje msg nga 16 karaktere
    msg_listD = wrap(
    msg,
    32,
    drop_whitespace=True,
    break_on_hyphens=False
    )
    decMsg = ''
    for msgPiece in msg_listD:
        decMsg = decMsg + decrypt(aesKey, msgPiece)
    return decMsg


def send(event=None):
    global aesKey
    msg = encryptBy16(my_msg.get())
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))


root = Tk()
root.title("ChatIO")

messages_frame = Frame(root)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Shkruani mesazhet këtu.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=25, width=75, yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = Entry(root, textvariable=my_msg)
entry_field.bind('<FocusIn>', on_entry_click)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(root, text="Dërgo", command=send)
send_button.pack()


#Socket 
HOST = 'localhost'
PORT = 5000

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket.socket(AF_INET, SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
root.mainloop()
