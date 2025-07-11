import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("10.8.0.10", 12345))  # ou IP da máquina servidora

while True:
    msg = input("Digite uma mensagem: ")
    if msg.lower() == 'sair':
        break
    client.sendall(msg.encode())
    resposta = client.recv(1024)
    print("Resposta:", resposta.decode())
client.close()
