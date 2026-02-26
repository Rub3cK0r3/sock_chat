import select 
import socket as sc

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
# Lista de sockets a monitorear
sockets_list = [socket]  # inicialmente solo el servidor
clients = {}  # diccionario socket -> dirección

print('Iniciando servicio desde la 127.0.0.1:8080 ..')
# while True:
#     fd,addr = socket.accept()
#     print(f'Cliente conectado desde la {addr}')
#     Thread(target=receive, args=(fd,addr), daemon=True).start()
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified in read_sockets:
        if notified == socket:
            client_socket, client_address = socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Nuevo cliente conectado: {client_address}") 
        else:
            
            try:
                message = notified.recv(MAXSIZE_MSG) 
           
                if message:
                    # Mostrar mensaje recibido
                    print(f"Mensaje de {clients[notified]}: {message.decode().strip()}") 

            except Exception as e:
                # Manejar desconexión inesperada
                print(f"Error con {clients[notified]}: {e}")
                sockets_list.remove(notified)
                del clients[notified]
                notified.close()
    # Manejar errores de sockets
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()
