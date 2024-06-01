
import serial
import time
import rtmidi
import sys
import json

contato = 'COM2'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(6)

with open('mapNotas.json') as jsonfile:
      mapNotas = json.load(jsonfile)

#Variáveis do sensor
gyro = 0
accel = 0
touch = 0

#Variáveis 
note = ('a',0)
last_note = 0
notes = [62,63,65,69,70]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 
noteHold = 0.2
soundEffectDuration = 0.2
previousSoundEffect = 1
soundeEffectInterval = 1
previousSoundEffectActiv = 0.1

print(notes_delay)

def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    if(serialPort.in_waiting > 0):
        serialString = serialPort.readline()
        sensorData = (serialString.decode('utf-8')).split('/')
        
        #print(serialString) 
        id = float(sensorData[0])
        gyro = float(sensorData[1]) * -1
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))

    if(180 >= gyro >= 137):
        note = ('a',mapNotas["A4"])
    elif(136 >= gyro >= 91):
        note = ('a',mapNotas["D#4"])

    elif(90 >= gyro >= 45):
        note = ('a',mapNotas["F#5"])
    elif(44 >= gyro >= 0):
        note = ('a',mapNotas["C5"])
    elif(-1 >= gyro >= -45):
        note = ('a',mapNotas["A4"])
    elif(-46 >= gyro >= -90):
        note = ('a',mapNotas["D#4"])

    elif(-91 >= gyro >= -136):
        note = ('a',mapNotas["F#5"])
    elif(-137 >= gyro >= -180):
        note = ('a',mapNotas["C5"])



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
                midiout.send_message([0x80,note[1],50]) 
                pass

    
    if(14000 >= accel >= 7000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["F#2"],50])
    
    elif(-7000 >= accel >= -14000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["F#2"],50]) 
    
    if(time.time() - previousSoundEffectActiv >= soundEffectDuration):
        previousSoundEffect = time.time()
        midiout.send_message([0x81,mapNotas["F#2"],50])