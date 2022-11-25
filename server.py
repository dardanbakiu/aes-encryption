import socket
import random
import string
from AESencrypt import encrypt
from AESdecrypt import decrypt

key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
# key = '1234567890123456'

def server_program():
    # get the hostname
    host = host = 'localhost'#socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    modKey = ''.join([key, 'DO_NOT_DECRYPT'])
    conn.send(modKey.encode())

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        data = encrypt(data, key)
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()