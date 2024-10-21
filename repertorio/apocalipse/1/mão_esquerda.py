import serial
import time
import rtmidi
import sys
import json

contato = 'COM1'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)

with open('mapNotas.json') as jsonfile:
      mapNotas = json.load(jsonfile)

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [68,74,75,76,78]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 
noteHold = 0.2
soundEffectDuration = 0.2
previousSoundEffect = 1
soundeEffectInterval = 1
previousSoundEffectActiv = 0.1


def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    if(serialPort.in_waiting > 0):
        serialString = serialPort.readline()
        sensorData = (serialString.decode('utf-8')).split('/')
 
        id = float(sensorData[0])
        gyro = float(sensorData[1]) 
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch)) 
    
    
    if(130 >= gyro >= 72):
        note = ('a',mapNotas["C5"])
    elif(71 >= gyro >= 25):
        note = ('a',mapNotas["D5"])
    elif(24 >= gyro >= -24):
        note = ('a',mapNotas["E5"])
    elif(-25 >= gyro >= -71):
        note = ('a',mapNotas["F5"])
    elif(-72 >= gyro >= -130):
        note = ('a',mapNotas["G5"])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],100])
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],100])
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],100])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],100])
                pass

    
    if(16000 >= accel >= 9500 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["B5"],100]) 

    elif(-9500 >= accel >= -16000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["B5"],100])
    
    if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
        previousSoundEffect = time.time()
        midiout.send_message([0x81,mapNotas["B5"],100])