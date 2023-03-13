import socket
import os
from datetime import datetime
import time

ip_address = '192.168.178.160'
port = 4455
max_size = 1024
folder_path = r"/root/whisper/received"
os.chdir(folder_path)

while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip_address, port))
    sock.listen(1)
    conn, addr = sock.accept()
    filename = f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.wav'
    file_number = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    with open(filename, 'wb') as f:
        print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] File {file_number}: {filename}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
        conn.close()