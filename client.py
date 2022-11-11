import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread
from tkinter import *
from AESencrypt import encrypt

firstclick = True

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
    if msg == "{dil}":
        client_socket.close()
        root.quit()

def on_closing(event=None):
    my_msg.set("{dil}")
    send()

root = Tk()
root.title("ChatIO")

messages_frame = Frame(root)
my_msg = StringVar()  # For the messages to be sent.
my_msg.set("Shkruani mesazhet këtu.")
scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
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

root.protocol("WM_DELETE_WINDOW", on_closing)

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