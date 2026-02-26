# .. EJERCICIO ANTERIOR 

server_socket.setblocking(False)  # socket no bloqueante
# Para cada cliente también puedes hacer:
# client_socket.setblocking(False)

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [], 1)
    for sock in read_sockets:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                sockets_list.remove(sock)
                sock.close()
                continue
            print(f"Mensaje: {data.decode()}")
        except BlockingIOError:
            pass  # no hay datos todavía

Manejo de mensajes TCP con delimitador
# Cada cliente tiene un buffer
buffers = {client_sock: b"" for client_sock in clients}

data = client_sock.recv(BUFFER_SIZE)
buffers[client_sock] += data

while b"\n" in buffers[client_sock]:
    msg, buffers[client_sock] = buffers[client_sock].split(b"\n", 1)
    print(f"Mensaje completo: {msg.decode()}")


Servidor moderno con asyncio
import asyncio

clients = set()

async def handle_client(reader, writer):
    clients.add(writer)
    addr = writer.get_extra_info('peername')
    print(f"Cliente conectado: {addr}")
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            print(f"{addr} dice: {message}")
            # Broadcast
            for w in clients:
                if w != writer:
                    w.write(f"{addr} dice: {message}\n".encode())
                    await w.drain()
    except ConnectionResetError:
        pass
    finally:
        print(f"Cliente desconectado: {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8080)
    async with server:
        await server.serve_forever()

asyncio.run(main())

