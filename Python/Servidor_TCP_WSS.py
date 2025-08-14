import socket
import struct
import threading
import time
from nacl.public import PrivateKey, PublicKey, Box
#from nacl.exceptions import CryptoError
from dotenv import load_dotenv
import os
import asyncio
import websockets
import queue





load_dotenv()


class VehLocation:
    def __init__(self, veh, lat, lng):
        self.veh = veh
        self.lat = lat
        self.lng = lng


class TCP:
    # RESPONSE TABLE
    R_OK = b'\x01'
    R_PK = b'\x02'
    R_TK = b'\x03'

    SERVER_PRIVATE = PrivateKey(bytes.fromhex(os.getenv('SERVER_PRIVATE_KEY', '')))

    def __new__(cls):
        if not TCP.SERVER_PRIVATE:
            TCP.print("[!] Chave privada do servidor não configurada.")
            raise ValueError("Chave privada do servidor não configurada.")
        TCP.print(f"Chave pública do servidor: {TCP.SERVER_PRIVATE.public_key.encode().hex()}")
        return super().__new__(cls)

    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port    
    
    @staticmethod
    def print(msg):
        print(f"[TCP]{msg}")

    def recCliPubKey(self, conn):
        try:
            pubkey_cliente = conn.recv(32)
            if len(pubkey_cliente) != 32:
                return None
            return PublicKey(pubkey_cliente)
        except Exception as e:
            self.print(f"[!] Erro ao receber chave pública do cliente: {e}")
            return None

    def recCliToken(self, conn, BOX):
        try:
            token = BOX.decrypt(conn.recv(1024))
            if len(token) != 10:
                return None
            return token.decode(errors='ignore').rstrip('\x00')
        except Exception as e:
            self.print(f"[!] Erro ao receber token do cliente: {e}")
            return None

    def handleClient(self, conn, addr):
        self.print(f"[+] Conectado por {addr}")
        try:
            # Chave publica do cliente
            CLIENTE_PUB_KEY = self.recCliPubKey(conn)
            if CLIENTE_PUB_KEY is None:
                self.print(f"[!] Chave pública inválida de {addr}. Desconectando...")
                conn.close()
                return
            conn.sendall(TCP.R_PK)
            BOX = Box(TCP.SERVER_PRIVATE, CLIENTE_PUB_KEY)


            # Pegar token descriptografado do cliente
            CLIENTE_TK = self.recCliToken(conn, BOX)
            if CLIENTE_TK is None:
                self.print(f"[!] Token inválido de {addr}. Desconectando...")
                conn.close()
                return
            conn.sendall(TCP.R_TK)


            self.print(f"[$] Chave pública recebida de {addr}: {CLIENTE_PUB_KEY.encode().hex()}")
            self.print(f"[$] Token recebido de {addr}: '{CLIENTE_TK}'")

            while True:
                # Espera por latitude e longitude
                DATA = conn.recv(1024)
                if not DATA:
                    self.print(f"Cliente {addr} desconectou.")
                    break

                try:
                    # Desencripta e separa
                    DATA_DECRYPTED = BOX.decrypt(DATA)
                    if len(DATA_DECRYPTED) != 8:
                        self.print(f"[!] Pacote decifrado inválido ({len(DATA_DECRYPTED)} bytes)")
                        continue

                    lat, lng = struct.unpack('<ff', DATA_DECRYPTED)

                    conn.sendall(TCP.R_OK)
                    self.print(f"-----------\n{addr} {len(DATA)} bytes\n|→ Latitude: {lat:.6f}\n|→ Longitude: {lng:.6f}\n|→ Token: '{CLIENTE_TK}'\n-----------")
                    # Envia nova localização para o WebSocket
                    WSS.FILA_THREAD_NEW_LOC.put(VehLocation(CLIENTE_TK, lat, lng))

                except Exception as e:
                    self.print(f"[!] Erro ao decifrar pacote: {e}")
                    self.print(f"[?] Pacote: {DATA.hex()}")
                    break

        except Exception as e:
            self.print(f"[Erro] {e}")
            time.sleep(2)
        finally:
            conn.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.print(f"Servidor TCP escutando em {self.host}:{self.port}...")

            while True:
                try:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handleClient, args=(conn, addr), daemon=True).start()
                except Exception as e:
                    self.print(f"[Falha ao iniciar thread]: {e}")
                    break
        
        self.print("\n[!] Servidor TCP encerrado.")







class WSS:
    CLIENTS = {}
    VEHICLES = {}
    serial_id = 0
    
    FILA_THREAD_NEW_LOC = queue.Queue()
    FILA_NEW_LOC = asyncio.Queue() 

    def getNextID():
        WSS.serial_id += 1
        return WSS.serial_id

    def __init__(self, host='0.0.0.0', port=12344):
        self.host = host
        self.port = port

    @staticmethod
    def print(msg):
        print(f"[WSS]{msg}")






    async def sendNewLocToCLients(self, vl, cli_ws):
        await cli_ws.send(f"Nova localização de {vl.veh}: {vl.lat}, {vl.lng}")

    def processNewLocation(self):
        self.print("[+] Iniciando processamento de novas localizações...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            try:
                new_loc = WSS.FILA_THREAD_NEW_LOC.get()
                
                if new_loc is None or not isinstance(new_loc, VehLocation):
                    self.print("[!] Localização inválida recebida. Ignorando...")
                    continue
                
                self.print(f"[+] Processando nova localização: {new_loc.veh}, {new_loc.lat}, {new_loc.lng}")
            
                if new_loc.veh in WSS.VEHICLES:
                    for cid in WSS.VEHICLES[new_loc.veh]:
                        if cid in WSS.CLIENTS:
                            self.print(f"[+] Enviando localização para cliente {cid}: {new_loc.lat}, {new_loc.lng}")
                            loop.run_until_complete(self.sendNewLocToCLients(new_loc, WSS.CLIENTS[cid]))
            except queue.Empty:
                threading.sleep(0.1)


    async def handleClient(self, ws):
        self.print(f"[+] Cliente conectado: {ws.remote_address}")
        CID = WSS.getNextID()
        WSS.CLIENTS[CID] = ws


        # Autenticação do cliente
        try:
            async for message in ws:
                self.print(f"[@] Mensagem recebida de {ws.remote_address}: {message}")
                if message.startswith("ident:"):
                    user_token = message[6:].strip()
                    #todo: verifica se é um cliente válido
                    if user_token:
                        await ws.send(f"Cliente {CID} autenticado com token: {user_token}")
                        break
                    else:
                        await ws.send("[!] Token inválido.")
                        ws.close()
                        return
                await ws.send("Envie 'ident:<token>' para autenticar.")

        except websockets.ConnectionClosed:
            self.print(f"[!] Conexão encerrada: {ws.remote_address}")
        except Exception as e:
            self.print("[Erro]", e)


        # Trata as requisições do cliente
        try:
            async for message in ws:
                self.print(f"[$] Mensagem recebida de {ws.remote_address}: {message}")
                if message.startswith("veh:"):
                    #todo: verificar se o veiculo existe no banco antes
                    veh_id = message[4:].strip()
                    if veh_id not in WSS.VEHICLES:
                        WSS.VEHICLES[veh_id] = set()
                    WSS.VEHICLES[veh_id].add(CID)
                    await ws.send(f"Agora você está rastreando o veículo {veh_id}.")

        except websockets.ConnectionClosed:
            self.print(f"[!] Conexão encerrada: {ws.remote_address}")
        except Exception as e:
            self.print("[Erro]", e)



    async def start_(self):
        SRV = await websockets.serve(self.handleClient, self.host, self.port)
        self.print(f"Servidor WSS escutando em {self.host}:{self.port}...")
        threading.Thread(target=self.processNewLocation, daemon=True).start()

        await SRV.wait_closed()
        self.print("\n[!] Servidor WSS encerrado.")

    def start(self):
        asyncio.run(self.start_())

if __name__ == "__main__":
    threading.Thread(target=WSS().start, daemon=True).start()
    TCP().start()
    
