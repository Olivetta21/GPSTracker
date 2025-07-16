import socket
import struct
import time
import random

HOST = '127.0.0.1'  # IP do servidor
PORT = 12345        # Porta do servidor
TOKEN = b'arduino01'  # Deve ter até 10 bytes

def montar_pacote(lat, lng, token):
    token_bytes = token[:10].ljust(10, b'\x00')
    return struct.pack('<ff10s', lat, lng, token_bytes)

def enviarPacote(sock, lat, lng):
    pacote = montar_pacote(lat, lng, TOKEN)
    sock.sendall(pacote)
    print(f"[→] Enviando pacote: {lat:.6f}, {lng:.6f}")
    
    resposta = sock.recv(1024)
    if resposta == None:
        print("[!] Erro: Resposta vazia.")
        return False

    if resposta.startswith(b'\x01'):
        print("[←] Sucesso:", resposta)
        return True
    else:
        print("[←] Resposta:", resposta)

    return False

def conectar():
    while True:
        try:
            sock = socket.create_connection((HOST, PORT), timeout=5)
            print("[+] Conectado ao servidor.")
            return sock
        except (ConnectionRefusedError, TimeoutError):
            print("[-] Conexão falhou. Tentando novamente...")
            time.sleep(2)

def main():
    sock = conectar()

    mensagensNaoEnviadas = [] # guarda ultimas 99 mensagens para reenviar no caso de falha

    while True:
        try:
            lat = -20 - 10 * random.random()
            lng = -50 - 10 * random.random()
            mensagensNaoEnviadas.append([lat, lng])

            print(f"Mensagens: {mensagensNaoEnviadas}")
            while len(mensagensNaoEnviadas) > 0:
                if enviarPacote(sock, mensagensNaoEnviadas[0][0], mensagensNaoEnviadas[0][1]):
                    mensagensNaoEnviadas.pop(0)
                else:
                    print("[!] Falha ao enviar pacotes.")
                    break

                
            time.sleep(2)

        except (TimeoutError):
            print("[-] Timeout. Tentando reconectar...")
            time.sleep(2)

        except (ConnectionResetError, BrokenPipeError):
            print("[-] Conexão perdida. Reestabelecendo...")
            sock.close()
            sock = conectar()

        except KeyboardInterrupt:
            print("\n[!] Encerrando cliente.")
            sock.close()
            break

if __name__ == "__main__":
    main()
