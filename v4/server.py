import asyncio

clients = set()

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    clients.add(writer)
    print(f"Cliente conectado: {addr}")

    try:
        while True:
            data = await reader.readline()
            if not data:
                break

            message = data.decode().strip()
            print(f"{addr} dice: {message}")

            for w in clients:
                if w != writer:
                    try:
                        w.write(f"{addr} dice: {message}\n".encode())
                        await w.drain()
                    except ConnectionResetError:
                        clients.remove(w)

    except ConnectionResetError:
        pass 
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

asyncio.run(main())
