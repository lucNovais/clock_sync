import socket
import os

from constants import *


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    connected = True
    current_time = 0

    print_default_screen(connected, current_time, sock)

def request_time(sock):
    sock.send(TIME_REQUEST.encode())
    try:
        data = sock.recv(BUFFER_SIZE).decode()
        print('Tempo recebido do servidor:', data)
    except:
        print('Conexao fechada pelo servidor ou parada forcada!')
        sock.close()
        return None
    
    return data

def print_default_screen(connected, current_time, sock):
    os.system('clear')

    if connected:
        print('Conectado ao servidor de tempo!\n')
    
    print(f'Tempo local: {current_time}')

    while True:
        try:
            opt = int(input('Digite (1) para atualizar o tempo: '))
        except TypeError:
            print('Tipo de entrada errado!')
        if opt == 1:
            current_time = request_time(sock)
            print_default_screen(connected, current_time, sock)

if __name__ == '__main__':
    connect()
