from time import sleep

VERDE = '\033[32m'
VERMELHO = '\033[31m'
RESETAR = '\033[0m'

for i in range(100):
    sleep(1)
    print(f"id: 13, gyro: {i + 24}, acc: {i + 48}, t: {VERDE if i < 12 else VERMELHO}{True if i < 12 else False}{RESETAR}", end="\r")