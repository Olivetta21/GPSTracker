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

class AuthError(Exception):
    pass

class TCP:
    # RESPONSE TABLE
    R_OK = b'\x01'
    R_PK = b'\x02'
    R_TK = b'\x03'

    SERVER_PRIVATE = PrivateKey(bytes.fromhex(os.getenv('SERVER_PRIVATE_KEY', '')))

    def __new__(cls):
        if not TCP.SERVER_PRIVATE:
            TCP.print("[!] Chave privada do servidor não configurada.")
            raise AuthError("Chave privada do servidor não configurada.")
        TCP.print(f"Chave pública do servidor: {TCP.SERVER_PRIVATE.public_key.encode().hex()}")
        return super().__new__(cls)

    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port    
    
    @staticmethod
    def print(msg):
        print(f"[TCP]{msg}")


    class ConnVehicle:
        def recVehPubKey(self, conn):
            try:
                pubkey_veiculo = conn.recv(32)
                if len(pubkey_veiculo) != 32:
                    return None
                return PublicKey(pubkey_veiculo)
            except Exception as e:
                TCP.print(f"[!] Erro ao receber chave pública do veículo: {e}")
                return None

        def recVehToken(self, conn, BOX):
            try:
                token = BOX.decrypt(conn.recv(1024))
                if len(token) != 10:
                    return None
                return token.decode(errors='ignore').rstrip('\x00')
            except Exception as e:
                TCP.print(f"[!] Erro ao receber token do veículo: {e}")
                return None
            

        def __init__(self, conn, addr):
            self.conn = conn
            self.addr = addr
            self.pub_key = None
            self.token = None
            self.box = None

        def __enter__(self):
            TCP.print(f"[+] Veículo conectado por {self.addr}")

            # Chave publica do veículo
            self.pub_key = self.recVehPubKey(self.conn)
            if self.pub_key is None:
                TCP.print(f"[!] Chave pública inválida de {self.addr}. Desconectando...")
                raise AuthError("Chave pública inválida.")
            self.conn.sendall(TCP.R_PK)
            self.box = Box(TCP.SERVER_PRIVATE, self.pub_key)

            # Pegar token descriptografado do veículo
            self.token = self.recVehToken(self.conn, self.box)
            if self.token is None:
                TCP.print(f"[!] Token inválido de {self.addr}. Desconectando...")
                raise AuthError("Token inválido.")
            self.conn.sendall(TCP.R_TK)

            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            TCP.print(f"[!] Desligando veículo {self.token or "não identificado"}...")
            self.conn.close()

    def handleVehicle(self, connection, address):
        try:
            with TCP.ConnVehicle(connection, address) as v:
                self.print(f"[$] Chave pública recebida de {v.addr}: {v.pub_key.encode().hex()}")
                self.print(f"[$] Token recebido de {v.addr}: '{v.token}'")

                #todo: verificar se esse token é valido no banco

                while True:
                    # Espera por latitude e longitude
                    DATA = v.conn.recv(1024)
                    if not DATA:
                        self.print(f"{v.token} Data vazia.")
                        return
                    
                    lat, lng = None, None

                    try: # Desencripta e separa
                        DATA_DECRYPTED = v.box.decrypt(DATA)
                        if len(DATA_DECRYPTED) != 8:
                            self.print(f"[!] Pacote decifrado inválido ({len(DATA_DECRYPTED)} bytes)")
                            continue
                        lat, lng = struct.unpack('<ff', DATA_DECRYPTED)
                    except Exception as e:
                        self.print(f"[!] Erro ao decifrar pacote: {e}")
                        self.print(f"[?] Pacote: {DATA.hex()}")
                        break

                    v.conn.sendall(TCP.R_OK)
                    self.print(f"[v] {v.token} {len(DATA)}bytes LAT:{lat:.6f} LNG:{lng:.6f}")
                    # Envia nova localização para o WebSocket
                    WSS.FILA_THREAD_NEW_LOC.put(VehLocation(v.token, lat, lng))

        except AuthError as e:
            self.print(f"[!] Erro de autenticação: {e}")
        except (ConnectionResetError, BrokenPipeError):
            self.print(f"[!] Conexão perdida")
        except Exception as e:
            self.print(f"[Erro] {e}")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.print(f"Servidor TCP escutando em {self.host}:{self.port}...")

            while True:
                time.sleep(0.2) # Evitar sobrecarga
                try:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handleVehicle, args=(conn, addr), daemon=True).start()
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
        try:
            await cli_ws.send(f"Nova localização de {vl.veh}: {vl.lat}, {vl.lng}")
        except websockets.ConnectionClosed:
            self.print(f"[!] Tentou se comunicar com {cli_ws.remote_address} mas a conexão estava encerrada.")

    def processNewLocation(self):
        self.print("[+] Iniciando processamento de novas localizações...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        threading.Thread(target=loop.run_forever, daemon=True).start()

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
                            self.print(f"[+] Enviando localização para cliente {cid}")
                            loop.call_soon_threadsafe(
                                asyncio.create_task,
                                self.sendNewLocToCLients(new_loc, WSS.CLIENTS[cid].ws)
                            )
                            time.sleep(0.2)
            except queue.Empty:
                time.sleep(0.1)

    class ConnClient:

        async def getClientIdent(self, ws):
            async for message in ws:
                WSS.print(f"[@] Mensagem recebida de {ws.remote_address}: {message}")
                if message.startswith("ident:"):
                    user_token = message[6:].strip()
                    #todo: verifica se é um cliente válido
                    if user_token:
                        await ws.send(f"Cliente autenticado com token: {user_token}")
                        return user_token
                    else:
                        await ws.send("[!] Token inválido.")
                        return None
                await ws.send("Envie 'ident:<token>' para autenticar.")
            return None

        def __init__(self, ws):
            self.ws = ws
            self.identidade = None
            self.CID = WSS.getNextID()

        async def __aenter__(self):
            WSS.print(f"[+] Cliente conectado: {self.ws.remote_address}")
            clientIdent_task = asyncio.create_task(self.getClientIdent(self.ws))
            try:
                self.identidade = await asyncio.wait_for(clientIdent_task, timeout=5.0)
            except asyncio.TimeoutError:
                self.identidade = None
            #todo: verifica no banco
            if not self.identidade:
                WSS.print(f"[!] Cliente {self.CID} falhou na autenticação.")
                raise AuthError("Cliente não autenticado.")

            await self.ws.send(f"Cliente {self.CID} autenticado com identidade: {self.identidade}")
            WSS.CLIENTS[self.CID] = self

            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await self.ws.close()
            if self.CID in WSS.CLIENTS:
                WSS.print(f"[!] Desligando cliente {self.CID}...")
                del WSS.CLIENTS[self.CID]
            for veh_id in WSS.VEHICLES:
                if self.CID in WSS.VEHICLES[veh_id]:
                    WSS.print(f"[!] tirando o cliente {self.CID} do veiculo {veh_id}")
                    WSS.VEHICLES[veh_id].discard(self.CID)

    async def handleClient(self, websocket):
        try:
            async with WSS.ConnClient(websocket) as c:
                # Requisições do cliente
                async for message in c.ws:
                    self.print(f"[$] Mensagem recebida de {c.identidade}: {message}")
                    if message.startswith("va:"):
                        #todo: verificar se o veiculo existe no banco antes, (e se ele pode ser rastreado)
                        veh_id = message[3:].strip()
                        if veh_id not in WSS.VEHICLES:
                            WSS.VEHICLES[veh_id] = set()
                        WSS.VEHICLES[veh_id].add(c.CID)
                        await c.ws.send(f"Agora você está rastreando o veículo {veh_id}.")
                    elif message.startswith("vr:"):
                        veh_id = message[3:].strip()
                        if veh_id in WSS.VEHICLES and c.CID in WSS.VEHICLES[veh_id]:
                            WSS.VEHICLES[veh_id].remove(c.CID)
                            await c.ws.send(f"Você parou de rastrear o veículo {veh_id}.")
                        else:
                            await c.ws.send(f"[!] Você não está rastreando o veículo {veh_id}.")
        except AuthError as e:
            self.print(f"[!] {e}")
        except websockets.ConnectionClosed:
            self.print(f"[!] Conexão encerrada")
        except Exception as e:
            self.print(f"[Erro] {e}")


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
    
