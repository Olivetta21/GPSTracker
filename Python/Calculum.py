# Estimativa de quantos bytes serão usados
def formatHR(num):
    if num < 1024:
        return f"{num} bytes"
    elif num < 1024**2:
        return f"{num / 1024:.2f} KB"
    elif num < 1024**3:
        return f"{num / 1024**2:.2f} MB"
    else:
        return f"{num / 1024**3:.2f} GB"


bPorPacote = input("Bytes por pacote: ")
frecEnvio = input("Segundos entre envios: ")

porHora = (3600 / float(frecEnvio)) * int(bPorPacote)
porDia = porHora * 24
porMes = porDia * 30
porAno = porDia * 365


print(f"Acada Hora: {formatHR(porHora)}")
print(f"Uso diário: {formatHR(porDia)}")
print(f"Uso mensal: {formatHR(porMes)}")
print(f"Uso anual: {formatHR(porAno)}")

input("Pressione Enter para sair...")