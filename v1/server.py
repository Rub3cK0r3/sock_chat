import socket as sc
from threading import Thread

MAXSIZE_MSG = 1024
MAXSIZE_MSGS = 20

def receive(fd,addr):
    while True:
        # Gestion de los mensajes
        msg = fd.recv(MAXSIZE_MSG)
        if msg:
            parsed_msg = f'FROM {addr} : MSG => {msg.decode()}'
            print(parsed_msg)

# Esto es el funcionamiento basico de un servidor:
socket = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

socket.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
socket.bind(("127.0.0.1",8080))

socket.listen()

print('Iniciando servicio desde la 127.0.0.1:8080 ..')
while True:
    fd,addr = socket.accept()
    print(f'Cliente conectado desde la {addr}')
    Thread(target=receive, args=(fd,addr), daemon=True).start()
