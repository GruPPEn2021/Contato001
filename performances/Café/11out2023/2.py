#Musica: Paixão 
#Mão direita

import serial
import time
import rtmidi
import sys

contato = 'COM5'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE, rtscts=True)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(1)

#Sensor variables
gyro = 0
accel = 0
touch = 0

#variables
note = ('a',0)
last_note = 0
notes = [79,81,83,86]
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

    #gyro, accel, touch = getSensorData()
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        #print(serialString)

        # Print the contents of the serial data
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))

    #print(accel)     
    if(-90 <= gyro <= -45):
        note = ('D7',notes[3])
    elif(-44 <= gyro <= 0):
        note = ('B6',notes[2])
    elif(1 <= gyro <= 45):
        note = ('A6',notes[1])
    elif(46 <= gyro <= 90):
        note = ('G6',notes[0])
  
    
    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],50])
            print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],50])
                print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],50])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],50])
                pass
