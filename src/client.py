import socket

from constants import *

def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))
    print('Conectado ao servidor de tempo!\n')

    try:
        while True:
            data = sock.recv(BUFFER_SIZE).decode()
            print('Tempo recebido do servidor:', data)
    except:
        print('Conexao fechada pelo servidor!')
        sock.close()

if __name__ == '__main__':
    connect_to_server()
