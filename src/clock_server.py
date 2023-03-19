import ntplib
import socket
import time

from constants import *

def update_with_ntp():
    ntp_client = ntplib.NTPClient()
    response = ntp_client.request(NTP_SERVER, version=3)
    return response.tx_time

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    sock.listen(1)

    print(f'Servidor de tempo iniciado!\nEscutando no endereco: {SERVER_ADDRESS}:{SERVER_PORT}\n')

    while True:
        conn, addr = sock.accept()
        print(f'Cliente connectado: {addr}')

        try:
            while True:
                ntp_time = update_with_ntp()
                local_time = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(ntp_time))
                conn.sendall(local_time.encode())
                print(f'Tempo enviado para o cliente: {local_time}')
                time.sleep(1)
        except:
            print('Conexao encerrada pelo cliente!')
            conn.close()

if __name__ == '__main__':
    start()
