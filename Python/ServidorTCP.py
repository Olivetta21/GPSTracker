import socket
import threading

# Configurações do servidor
HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
PORT = 12345      # Porta desejada

# Função que trata cada cliente
def handle_client(conn, addr):
    print(f"[+] Nova conexão de {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"[{addr}] Mensagem recebida: {data.decode().strip()}")
                conn.sendall(b"Mensagem recebida com sucesso\n")
            except ConnectionResetError:
                break
    print(f"[-] Conexão encerrada: {addr}")

# Cria o socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"[+] Servidor ouvindo em {HOST}:{PORT}")

# Loop principal do servidor
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon = True  # Thread morre quando o programa principal termina
    thread.start()
