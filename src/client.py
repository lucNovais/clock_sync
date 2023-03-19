import socket
import os
import time

from constants import *


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    connected = True
    current_time = None

    current_time = request_time(sock)

    default_screen(connected, current_time, sock)

"""
- Cliente conecta no servidor de tempo pela primeira vez:
    - atualiza seu relogio

- Proxima atualizacao (a cada x segundos):
    - pegar o tempo atual - tempo recebido = valor do incremento
    - valor do incremento / 10
    - incrementar o tempo atual 10x com esse valor + RTT + tempo de recebimento ate esse momento
"""

def request_time(sock):
    sock.send(TIME_REQUEST.encode())
    try:
        data = sock.recv(BUFFER_SIZE).decode()
        print('Tempo recebido do servidor:', data)
    except:
        print('Conexao fechada pelo servidor ou parada forcada!')
        sock.close()
    
    return data

def default_screen(connected, current_time, sock):
    os.system('clear')

    if connected:
        print('Conectado ao servidor de tempo!\n')
    
    print(f'Tempo local: {current_time}')
    print(f'Periodo de atualizacao: {TIME_TO_UPDATE} segundos')

    reference_time = time.time()
    while True:
        elapsed_time = time.time() - reference_time
        if TIME_TO_UPDATE - elapsed_time == 0:
            current_time = request_time(sock)
            default_screen(connected, current_time, sock)

if __name__ == '__main__':
    connect()
