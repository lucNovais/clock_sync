import socket
import os
import time

from constants import *

def connect():
    """
    Funcao responsavel por conectar um cliente ao servidor de tempo.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    connected = True
    current_time = None

    t0 = time.time()
    (server_time, t1) = request_time(sock)
    current_time = server_time + (t1 - t0) / 2

    default_screen(connected, current_time, sock)

def request_time(sock):
    """
    Funcao responsavel por fazer uma requisicao de atualizacao temporal para o servidor.

    Parametros:
    -----------

    `sock`: objeto socket que contem a conexao com o servidor.

    Retorno:
    --------

    `data`: tempo recebido do servidor.
    """
    sock.send(TIME_REQUEST.encode())

    try:
        data = float(sock.recv(BUFFER_SIZE).decode())
        t1 = time.time()
    except:
        print('Conexao fechada pelo servidor ou parada forcada!')
        sock.close()
    
    return (data, t1)

def default_screen(connected, current_time, sock):
    """
    Tela principal do cliente.
    """
    os.system('clear')

    if connected:
        print('Conectado ao servidor de tempo!\n')
    
    print(f"Tempo local: {time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(current_time))}")

    reference_time = time.time()
    while True:
        elapsed_time = time.time() - reference_time
        print(f'Atualizacao em: {int(TIME_TO_UPDATE - elapsed_time)} segundos.', end='\r')

        if TIME_TO_UPDATE - elapsed_time <= 0:
            t0 = time.time()
            (server_time, t1) = request_time(sock)
            current_time = server_time + (t1 - t0) / 2

            default_screen(connected, current_time, sock)

if __name__ == '__main__':
    connect()
