import ntplib
import socket
import time
import threading

from constants import *

def update_with_ntp():
    """ Funcao que consulta o servidor de NTP e retorna o tempo atual.
    """
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(NTP_SERVER, version=3)

    return response.tx_time

# Essa funcao rodara em uma thread para cada cliente conectado
def send_time(conn, client_index):
    """ Funcao que envia para o cliente o tempo obtido pelo NTP, quando solicitado.
    """
    connected = True

    while connected:
        # Recebe uma mensagem do cliente
        msg = conn.recv(BUFFER_SIZE).decode()

        # Verifica se a mensagem foi uma requisicao de atualizacao de relogio
        if msg == TIME_REQUEST:
            try:
                ntp_time = update_with_ntp()
                local_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(ntp_time))

                conn.sendall(str(ntp_time).encode())
                print(f'Tempo enviado para o cliente {client_index}: {local_time}')
            except:
                print('Conexao encerrada pelo cliente ou parada forcada!')
                conn.close()
                connected = False
    exit()

def start():
    """ Funcao que inicia um servidor e espera por uma conexao de cliente.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    sock.listen(1)

    print(f'Servidor de tempo iniciado!\nEscutando no endereco: {SERVER_ADDRESS}:{SERVER_PORT}\n')

    while True:
        # Recebe uma nova conexao de um cliente
        conn, addr = sock.accept()
        print(f'({threading.active_count() - 1}) Cliente connectado: {addr}')

        thread = threading.Thread(
            target=send_time,
            args=[conn, threading.active_count() - 1]
        )

        # Inicia uma thread para o cliente que tentou se conectar
        thread.start()

if __name__ == '__main__':
    start()
