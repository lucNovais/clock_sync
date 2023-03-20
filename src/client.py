import socket
import os
import time

from constants import *

def connect():
    """ Funcao responsavel por conectar um cliente ao servidor de tempo.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    connected = True
    current_time = None

    # Calculo da estimativa do RTT pela formula do algoritmo de Cristian:
    #         T_cliente = T_servidor + (T1 - T0) / 2
    # Como essa e a primeira requisicao de tempo para o servidor, a atribuicao
    # do tempo local nao sera feita de maneira gradual
    t0 = time.time()
    (server_time, t1) = request_time(sock)
    current_time = server_time + (t1 - t0) / 2

    default_screen(connected, current_time, sock)

def request_time(sock):
    """ Funcao responsavel por fazer uma requisicao de atualizacao temporal para o servidor.
    """
    sock.send(TIME_REQUEST.encode())

    try:
        raw_server_time = float(sock.recv(BUFFER_SIZE).decode())
        t1 = time.time()
    except:
        print('Conexao fechada pelo servidor ou parada forcada!')
        sock.close()
    
    return (raw_server_time, t1)

def default_screen(connected, current_time, sock):
    """ Tela principal do cliente.
    """
    os.system('clear')

    if connected:
        print('Conectado ao servidor de tempo!\n')
    
    print(f"Tempo local: {time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(current_time))}")

    reference_time = time.time()
    while True:
        elapsed_time = time.time() - reference_time
        print(f'Atualizacao em: {int(TIME_TO_UPDATE - elapsed_time)} segundos.', end='\r')

        # Verifica se esta no momento de solicitar uma atualizacao para o servidor atraves do timer
        if TIME_TO_UPDATE - elapsed_time <= 0:
            t0 = time.time()
            (server_time, t1) = request_time(sock)
            
            # Encontrando o incremento de tempo e dividindo entre partes menores para aumentar gradativamente
            aux_time = (current_time - (server_time + (t1 - t0) / 2)) / DIVISION_CONSTANT

            for _ in range(DIVISION_CONSTANT):
                current_time += aux_time

            default_screen(connected, current_time, sock)

if __name__ == '__main__':
    connect()
