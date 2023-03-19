import ntplib
import socket
import time

from constants import *

def get_ntp_time():
    client = ntplib.NTPClient()
    response = client.request(NTP_SERVER, version=3)
    return response.tx_time

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_ADDRESS, SERVER_PORT))
    sock.listen(1)
    print('Server started.')

    while True:
        conn, addr = sock.accept()
        print('Client connected:', addr)

        try:
            while True:
                ntp_time = get_ntp_time()
                local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ntp_time))
                conn.sendall(local_time.encode())
                print('Sent time to client:', local_time)
                time.sleep(1)
        except:
            print('Connection closed by client.')
            conn.close()

if __name__ == '__main__':
    start_server()
