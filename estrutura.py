#bibliotecas 
import serial
import time
import rtmidi
import sys
import json 


contato = 'COM1'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]
#Modificação para alternar porta bluetooh fora do script direto ao rodar pelo terminal

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

#imprime a lista de portas MIDI 
midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1) #seleciona port MIDI

with open('mapNotas.json') as jsonfile:
      mapNotas = json.load(jsonfile) 

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [60,62,64,65,67,69,71,82]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 #ultimo salto 
noteHold = 0.1 #tempo para segurar a nota  
soundEffectDuration = 1 #tempo limite para acionamento de disparo, caso for necessario deixar accel com tempo diferente do gyro
previousSoundEffect = 1 #tempo para acionamento do accel
soundeEffectInterval = 1 #intervalo entre os acionamentos do accel
previousSoundEffectActiv = 0.1
 

print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        #Leia os dados do buffer até que return/new line seja encontrado
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')
        #print(serialString) 

        #Print do conteudo do serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1]) # * -1 
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch)) 
    
    if(120 >= gyro >= 88):
        note = ('a',mapNotas["C5"])
    elif(87 >= gyro >= 51):
        note = ('a',mapNotas["D5"])
    elif(50 >= gyro >= 14):
        note = ('a',mapNotas["E5"])
    elif(13 >= gyro >= -13):
        note = ('a',mapNotas["F5"])
    elif(-14 >= gyro >= -50):
        note = ('a',mapNotas["G5"])
    elif(-51 >= gyro >= -87):
        note = ('a',mapNotas["A5"])
    elif(-88 >= gyro >= -120):
        note = ('a',mapNotas["B5"])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],50])
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],50])
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],50])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],50]) #0x80 desligar a nota, 100 velocidade do MiDi
                pass

    #Para mudar a sensibilidade do acelerometro alterar os limites (10000 > accel > 8000)
    
    if(10000 >= accel >= 8500 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["B5"],100]) 

    elif(-8500 >= accel >= -10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["B5"],100])

    if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
        previousSoundEffect = time.time()
        midiout.send_message([0x81,mapNotas["B5"],100]) 