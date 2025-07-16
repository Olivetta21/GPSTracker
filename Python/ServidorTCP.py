import socket
import struct
import threading
import random

def handle_client(conn, addr):
    print(f"[+] Conectado por {addr}")
    with conn:
        while True:
            data = conn.recv(18)
            if not data:
                print(f"Cliente {addr} desconectou")
                break

            if len(data) != 18:
                print(f"Pacote incompleto ({data} - {len(data)})")
                continue

            lat, lng, token = struct.unpack('<ff10s', data)
            token = token.decode(errors='ignore').rstrip('\x00')

            print(f"-----------\n{addr}\n|→ Latitude: {lat:.6f}\n|→ Longitude: {lng:.6f}\n|→ Token: '{token}'\n-----------")
            
            conn.sendall(b'\x01')



def start_server(host='0.0.0.0', port=12345):
    print("Starting server...")
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



if __name__ == "__main__":
    start_server()
    print("tchau")