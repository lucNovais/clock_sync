import ntplib
import socket
import time
import threading

from constants import *

def update_with_ntp():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(NTP_SERVER, version=3)
    return response.tx_time

def send_time(conn, client_index):
    connected = True

    while connected:
        ntp_time = update_with_ntp()
        local_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(ntp_time))
        
        msg = conn.recv(BUFFER_SIZE).decode()

        if msg == TIME_REQUEST:
            try:
                conn.sendall(local_time.encode())
                print(f'Tempo enviado para o cliente {client_index}: {local_time}')
            except:
                print('Conexao encerrada pelo cliente ou parada forcada!')
                conn.close()
                connected = False
    exit()

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    sock.listen(1)

    print(f'Servidor de tempo iniciado!\nEscutando no endereco: {SERVER_ADDRESS}:{SERVER_PORT}\n')

    while True:
        conn, addr = sock.accept()
        print(f'({threading.active_count() - 1}) Cliente connectado: {addr}')

        thread = threading.Thread(
            target=send_time,
            args=[conn, threading.active_count() - 1]
        )

        thread.start()

if __name__ == '__main__':
    start()
