    
import serial
import time
import rtmidi
import sys
import json

contato = 'COM1'
if len(sys.argv) == 3:
    arquivo = sys.argv[1]
    contato = 'COM' + sys.argv[2]

with open(arquivo) as file:
    project = json.load(file)

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
# print(midiout.get_ports())
port = midiout.open_port(project["port"])

with open('mapNotas.json') as jsonfile:
      mapNotas = json.load(jsonfile)


#Variáveis do sensor
gyro = 0
accel = 0
touch = 0

#Variáveis 
note = ('a',0)
last_note = 0
notes = project["notes"]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1  
noteHold = 0.2
soundEffectDuration = 2
previousSoundEffect = 3
soundeEffectInterval = 2
previousSoundEffectActiv = 0.1

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == mapNotas[notes[i][2]]):
            notes_delay[i] == time.time()

while(1):

    if(serialPort.in_waiting > 0):
        serialString = serialPort.readline()
        sensorData = (serialString.decode('utf-8')).split('/')

        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = int(sensorData[3])
        print(f"id: {int(id)}     gyro: {int(gyro)}     accel: {int(accel)}     t: {touch}", end="\r")



    for min_val, max_val, current_val in notes:
        if min_val >= gyro >= max_val:
            note = ('a', mapNotas[current_val])
  
    
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
            if(mapNotas[notes[i][2]] != note[1]):
                midiout.send_message([0x80,mapNotas[notes[i][2]],50])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],50])
                pass
    
    # if(10000 >= accel >= 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
    #     previousSoundEffectActiv = time.time()
    #     midiout.send_message([0x91,mapNotas["A4"],100]) 

    # elif(-8000 >= accel >= -10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
    #     previousSoundEffectActiv = time.time()
    #     midiout.send_message([0x91,mapNotas["A4"],100])
    
    # if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
    #     previousSoundEffect = time.time()
    #     midiout.send_message([0x81,mapNotas["A4"],100])
