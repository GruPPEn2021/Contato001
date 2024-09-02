import time
import sys
import json

contato = 'COM1'
if len(sys.argv) == 3:
    arquivo = sys.argv[1]
    contato = 'COM' + sys.argv[2]

with open(arquivo) as file:
    config = json.load(file)

print(config, contato)