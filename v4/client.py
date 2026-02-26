import socket as sc

socket = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

socket.connect(("127.0.0.1",8080))

while True:
    msg = input('Dame un mensaje : ').strip().encode()
    socket.send(msg)
