import socket
import struct
import threading
import time
from nacl.public import PrivateKey, PublicKey, Box
from nacl.exceptions import CryptoError
from dotenv import load_dotenv
import os

# RESPONSE TABLE
R_OK = b'\x01'
R_PK = b'\x02'
R_TK = b'\x03'

# GLOBAL VARIABLES
server_private = None
clientes = {}

def receberChavePublica(conn):
    pubkey_cliente = conn.recv(32)
    if len(pubkey_cliente) != 32:
        print("Chave pública inválida.")
        conn.close()
        return None
    return PublicKey(pubkey_cliente)

def receberTokenCliente(conn, cli_box):
    token = cli_box.decrypt(conn.recv(1024))
    if len(token) != 10:
        print("Token inválido.")
        conn.close()
        return None
    return token.decode(errors='ignore').rstrip('\x00')

def handle_client(conn, addr):
    print(f"[+] Conectado por {addr}")
    try:
        # Chave publica do cliente
        cliente_public_key = receberChavePublica(conn)
        if cliente_public_key is None:
            print(f"[!] Chave pública inválida de {addr}. Desconectando...")
            return
        conn.sendall(R_PK)
        box = Box(server_private, cliente_public_key)
        clientes[conn] = box

        # Pegar token descriptografado do cliente
        cliente_token = receberTokenCliente(conn, box)
        if cliente_token is None:
            print(f"[!] Token inválido de {addr}. Desconectando...")
            return
        conn.sendall(R_TK)

        print(f"[🔑] Chave pública recebida de {addr}: {cliente_public_key.encode().hex()}")
        print(f"[🔑] Token recebido de {addr}: '{cliente_token}'")

        while True:
            # Espera por latitude e longitude
            data = conn.recv(1024)
            if not data:
                print(f"Cliente {addr} desconectou.")
                break

            try:
                # Desencripta e separa
                decrypted = box.decrypt(data)
                if len(decrypted) != 8:
                    print(f"[!] Pacote decifrado inválido ({len(decrypted)} bytes)")
                    continue

                lat, lng = struct.unpack('<ff', decrypted)

                print(f"-----------\n{addr} {len(data)} bytes\n|→ Latitude: {lat:.6f}\n|→ Longitude: {lng:.6f}\n|→ Token: '{cliente_token}'\n-----------")
                conn.sendall(R_OK)

            except CryptoError as e:
                print("[!] Erro ao decifrar pacote:", e)
                print("[?] Pacote: ", data.hex())
                break

    except Exception as e:
        print("[Erro]", e)
        time.sleep(2)
    finally:
        conn.close()
        if conn in clientes:
            del clientes[conn]

def start_server(host='0.0.0.0', port=12345):
    print("🔐 Servidor criptografado iniciado...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escutando em {host}:{port}...")

        while True:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except KeyboardInterrupt:
                print("\n[!] Servidor encerrado.")
                break

def main():    
    load_dotenv()
    global server_private
    server_private = PrivateKey(bytes.fromhex(os.getenv('SERVER_PRIVATE_KEY', '')))
    if server_private is None or server_private == '':
        raise ValueError("Chave privada do servidor não encontrada.")

    print("[🔐] Chave pública do servidor:")
    print(server_private.public_key.encode().hex())
    start_server()


if __name__ == "__main__":
    main()