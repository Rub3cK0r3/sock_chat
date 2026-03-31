import socket as sc
from threading import Thread

MAXSIZE_MSG = 1024
MAXSIZE_MSGS = 20

def receive(fd,addr):
    while True:
        # Message handling..
        msg = fd.recv(MAXSIZE_MSG)
        if msg:
            parsed_msg = f'FROM {addr} : MSG => {msg.decode()}'
            print(parsed_msg)

# This is the basic behaviour for a basic server:
socket = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

socket.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
socket.bind(("127.0.0.1",8080))

socket.listen()

print('Started a service from 127.0.0.1:8080..')
while True:
    fd,addr = socket.accept()
    print(f'CONNECTED from {addr}')
    Thread(target=receive, args=(fd,addr), daemon=True).start()
