import select 
import socket as sc

MAXSIZE_MSG = 1024
MAXSIZE_MSGS = 20

def receive(fd,addr):
    while True:
        msg = fd.recv(MAXSIZE_MSG)
        if msg:
            parsed_msg = f'FROM {addr} : MSG => {msg.decode()}'
            print(parsed_msg)

socket = sc.socket(sc.AF_INET,sc.SOCK_STREAM)

socket.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
socket.bind(("127.0.0.1",8080))

socket.listen()
sockets_list = [socket]  # initially the server 
clients = {}  # dictionary socket -> address 

print('Started a service from 127.0.0.1:8080..')

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified in read_sockets:
        if notified == socket:
            client_socket, client_address = socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"CONNECTED FROM : {client_address}") 
        else:
            
            try:
                message = notified.recv(MAXSIZE_MSG) 
           
                if message:
                    print(f"MESSAGE FROM : {clients[notified]} : {message.decode().strip()}") 

            except Exception as e:
                print(f"Error con {clients[notified]}: {e}")
                sockets_list.remove(notified)
                del clients[notified]
                notified.close()
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()
