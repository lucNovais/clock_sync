import socket

from constants import *

def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))
    print('Connected to server.')

    try:
        while True:
            data = sock.recv(BUFFER_SIZE).decode()
            print('Received time from server:', data)
    except:
        print('Connection closed by server.')
        sock.close()

if __name__ == '__main__':
    connect_to_server()
