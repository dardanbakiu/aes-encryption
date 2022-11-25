import socket
from AESencrypt import encrypt
from AESdecrypt import decrypt

key = '1234567890123456'

def client_program():
    host = 'localhost'#socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if 'DO_NOT_DECRYPT' not in data:
          decryptedDate = decrypt(key, data)
          print('Received from server: ' + decryptedDate)  # show in terminal

          message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()