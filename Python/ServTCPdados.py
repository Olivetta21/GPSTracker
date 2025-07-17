import socket
import struct
import time
import random
from nacl.public import PrivateKey, PublicKey, Box

# RESPONSE TABLE
R_OK = b'\x01'
R_PK = b'\x02'
R_TK = b'\x03'

# SERVER AND CLIENT CONFIGURATION
HOST = '127.0.0.1'
PORT = 12345
TOKEN = b'arduino001'
INTERVAL = 5

# SERVER ENCRYPTION
SERVER_PUBLIC_HEX = '5173ed5025b8e0aabc53119349697cb2adf34236f467f89a8cd14f3f1b4e2719'
client_public = None
box = None


def formatToken(token):
    return token[:10].ljust(10, b'\x00') # Garantir 10 bytes

def enviarLocalizacao(sock, lat, lng):    
    if sock is None or sock.fileno() == -1:
        print("[!] Socket inválido.")
        return False
    
    # Montar Pacote
    encrypted = box.encrypt(
        struct.pack('<ff', lat, lng) # 8 bytes total
    )
    sock.sendall(encrypted)

    print(f"[→] Enviando: {lat:.6f}, {lng:.6f}\n[?] pacote criptografado: {encrypted.hex()}\n[~] Tamanho: {len(encrypted)} bytes")

    resposta = sock.recv(1024)
    if resposta == R_OK:
        return True
    else:
        print("[←] Resposta inesperada:", resposta)
        return False

def conectar():
    try:
        sock = socket.create_connection((HOST, PORT), timeout=5)
        # Enviando chave em plain text
        print("[→] Enviando chave pública...")
        sock.sendall(client_public.encode())
        if sock.recv(1024) != R_PK:
            print("[-] Resposta inesperada. Verifique a chave pública.")
            sock.close()
            return None
        
        # Enviando token já criptografado
        print("[→] Enviando token...")
        sock.sendall(box.encrypt(formatToken(TOKEN)))
        if sock.recv(1024) != R_TK:
            print("[-] Resposta inesperada. Verifique o token.")
            sock.close()
            return None

        return sock
    except Exception as e:
        print(f"[-] Erro de conexão: {e}.")
    return None

def main():
    global client_public, box
    client_private = PrivateKey.generate()
    client_public = client_private.public_key
    box = Box(client_private, PublicKey(bytes.fromhex(SERVER_PUBLIC_HEX)))

    sock = None
    locsNotSended = []

    # Timestamp inicial
    last_time = 0

    while True:
        try:
            # Esperar o minimo de segundos entre envios
            timestamp = time.time()
            interval = timestamp - last_time            
            if interval < INTERVAL:
                toWait = INTERVAL - interval
                print(f"[⏳] Aguardando {toWait:.2f} segundos para o próximo envio...")
                time.sleep(toWait)
            last_time = time.time()

            # Mock de localização
            lat = -20 - 10 * random.random()
            lng = -50 - 10 * random.random()
            locsNotSended.append([lat, lng])
            
            if sock is None or sock.fileno() == -1:
                sock = conectar()

            print(f"Localizações pendentes: {len(locsNotSended)}")
            while len(locsNotSended) > 0:
                
                if enviarLocalizacao(sock, locsNotSended[0][0], locsNotSended[0][1]):
                    locsNotSended.pop(0)
                    print("[←] Sucesso")
                else:
                    print("[!] Falha ao enviar localização.")
                    break
        
        except TimeoutError:
            print("[!] Tempo limite de conexão excedido.")
            continue

        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            print("[-] Conexão perdida...")
            sock.close()

        except KeyboardInterrupt:
            print("\n[!] Encerrando cliente.")
            sock.close()
            break

if __name__ == "__main__":
    main()
