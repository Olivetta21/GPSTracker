import asyncio
import websockets

clients = {}

async def handler(websocket):
    usuario = None
    try:
        async for message in websocket:
            print(f"Mensagem recebida: {message}")
            if message.startswith("ident:"):
                if usuario:
                    await websocket.send("Você já está conectado.")
                    continue
                usuario = message.split(":")[1]
                clients[usuario] = websocket
                print(f"Cliente {usuario} conectado.")
                await websocket.send(f"Oi, {usuario}!")
            elif usuario:
                for u, client in clients.items():
                    if client != websocket:
                        await client.send(f"{usuario}: {message}")
    except:
        print("Cliente desconectado")
    finally:
        if usuario and usuario in clients:
            del clients[usuario]

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Servidor WebSocket rodando na porta 8765...")
        await asyncio.Future()

asyncio.run(main())
