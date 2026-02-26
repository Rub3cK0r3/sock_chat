import asyncio

# Conjunto de clientes conectados
clients = set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    clients.add(writer)
    print(f"Cliente conectado: {addr}")

    try:
        while True:
            data = await reader.readline()  # Leer hasta \n
            if not data:
                # Cliente se desconectó
                break

            message = data.decode().strip()
            print(f"{addr} dice: {message}")

            # Broadcast a todos los demás clientes
            for w in clients:
                if w != writer:
                    try:
                        w.write(f"{addr} dice: {message}\n".encode())
                        await w.drain()  # Esperar que se envíe
                    except ConnectionResetError:
                        # Cliente cerrado inesperadamente
                        clients.remove(w)

    except ConnectionResetError:
        pass  # Cliente se desconectó abruptamente
    finally:
        print(f"Cliente desconectado: {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8080)
    addr = server.sockets[0].getsockname()
    print(f"Servidor asyncio iniciado en {addr}")

    async with server:
        await server.serve_forever()

# Ejecutar event loop
asyncio.run(main())

