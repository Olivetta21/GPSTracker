import asyncio
import websockets
import threading
import queue
from time import sleep

# Fila para comunicação entre threads
fila_envio = queue.Queue()
print_lock = threading.Lock()  # Lock para sincronizar prints

def thread_segura_print(mensagem):
    with print_lock:
        print(mensagem)

async def cliente_ws():
    uri = "ws://localhost:12344"  # ou IP externo do servidor
    
    try:
        async with websockets.connect(uri) as websocket:
            thread_segura_print("Conectado ao servidor WebSocket")
            
            # Task para enviar mensagens
            async def enviar_mensagens():
                while True:
                    # Verificar se há mensagens na fila
                    if not fila_envio.empty():
                        msg = fila_envio.get()
                        await websocket.send(msg)
                        thread_segura_print(f"Mensagem enviada: {msg}")
                    await asyncio.sleep(0.1)
            
            # Task para receber mensagens
            async def receber_mensagens():
                while True:
                    try:
                        resposta = await websocket.recv()
                        thread_segura_print(f"Mensagem recebida do servidor: {resposta}")
                    except websockets.ConnectionClosed:
                        thread_segura_print("Conexão encerrada pelo servidor")
                        break
            
            # Executar ambas as tarefas concorrentemente
            await asyncio.gather(
                enviar_mensagens(),
                receber_mensagens()
            )
    except Exception as e:
        thread_segura_print(f"Erro na conexão: {e}")

def asyncio_thread():
    # Esta função executa o loop de eventos asyncio em uma thread separada
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cliente_ws())

def main():
    # Inicia o cliente WebSocket em uma thread separada
    ws_thread = threading.Thread(target=asyncio_thread, daemon=True)
    ws_thread.start()

    # Loop principal para receber entrada do usuário
    try:
        while True:
            mensagem = input("Digite uma mensagem para enviar (ou 'sair' para encerrar): ")
            if mensagem.lower() == 'sair':
                break
            fila_envio.put(mensagem)
    except KeyboardInterrupt:
        thread_segura_print("Cliente encerrado.")

if __name__ == "__main__":
    main()
    thread_segura_print("Programa finalizado")