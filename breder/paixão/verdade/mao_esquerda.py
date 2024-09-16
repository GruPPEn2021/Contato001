
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
port = midiout.open_port(3)

with open('mapNotas.json') as jsonfile:
      mapNotas = json.load(jsonfile)


#Variáveis do sensor
gyro = 0
accel = 0
touch = 0

#Variáveis 
note = ('a',0)
last_note = 0
notes = [50,52,53,54,55] 
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1  
noteHold = 0.2
soundEffectDuration = 2
previousSoundEffect = 3
soundeEffectInterval = 2
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


    if(102 >= gyro >= 62):
        note = ('a',mapNotas["G4"])
    elif(61 >= gyro >= 21):
        note = ('a',mapNotas["F#4"])
    elif(20 >= gyro >= -20):
        note = ('a',mapNotas["F4"])
    elif(-21 >= gyro >= -61):
        note = ('a',mapNotas["E4"])
    elif(-62 >= gyro >= -102):
        note = ('a',mapNotas["D4"])
  
    
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
    
    if(10000 >= accel >= 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["A4"],100]) 

    elif(-8000 >= accel >= -10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["A4"],100])
    
    if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
        previousSoundEffect = time.time()
        midiout.send_message([0x81,mapNotas["A4"],100])