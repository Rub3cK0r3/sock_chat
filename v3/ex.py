# .. EJERCICIO ANTERIOR 

# Dentro del else del loop read_sockets
message = notified_socket.recv(BUFFER_SIZE)
if not message:
    # manejar desconexión...
    continue

# Broadcast a todos menos el remitente
for client_sock in clients:
    if client_sock != notified_socket:
        client_sock.send(f"{clients[notified_socket]} dice: {message.decode()}".encode())

