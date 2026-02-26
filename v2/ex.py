import socket
import select

# Parámetros
HOST = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 1024

# Crear socket servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Lista de sockets a monitorear
sockets_list = [server_socket]  # inicialmente solo el servidor
clients = {}  # diccionario socket -> dirección

print(f"Servidor iniciado en {HOST}:{PORT}")

while True:
    # select devuelve listas de sockets listos
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        # Nuevo cliente conectado
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            sockets_list.append(client_socket)
            clients[client_socket] = client_address
            print(f"Nuevo cliente conectado: {client_address}")

        # Cliente existente envió mensaje
        else:
            try:
                message = notified_socket.recv(BUFFER_SIZE)
                if not message:
                    # Cliente se desconectó
                    print(f"Cliente {clients[notified_socket]} desconectado")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    notified_socket.close()
                    continue

                # Mostrar mensaje recibido
                print(f"Mensaje de {clients[notified_socket]}: {message.decode().strip()}")

                # Ejemplo simple de broadcast a todos los demás clientes
                for client_sock in clients:
                    if client_sock != notified_socket:
                        client_sock.send(f"{clients[notified_socket]} dice: {message.decode()}".encode())

            except Exception as e:
                # Manejar desconexión inesperada
                print(f"Error con {clients[notified_socket]}: {e}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                notified_socket.close()

    # Manejar errores de sockets
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()

