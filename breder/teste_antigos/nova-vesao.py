import serial
import time
import rtmidi
import sys

#port = str(input('Numero da portaCOM: '))
#portCOM = 'COM' + port

portCOM = 'COM2'
if len(sys.argv) > 1:
    portCOM = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = portCOM, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
serialString = ''


midiout = rtmidi.MidiOut()
print(midiout.get_ports())
portMIDI = midiout.open_port(2)

gyro = 0
accel = 0
touch = 0

mapNotas = { 
    "C1": 12, "C#1": 13, "D1": 14, "D#1": 15, "E1": 16, "F1": 17, "F#1": 18, "G1": 19, "G#1": 20, "A1": 21, "A#1": 22, "B1": 23,
    "C2": 24, "C#2": 25, "D2": 26, "D#2": 27, "E2": 28, "F2": 29, "F#2": 30, "G2": 31, "G#2": 32, "A2": 33, "A#2": 34, "B2": 35,
    "C3": 36, "C#3": 37, "D3": 38, "D#3": 39, "E3": 40, "F3": 41, "F#3": 42, "G3": 43, "G#3": 44, "A3": 45, "A#3": 46, "B3": 47,
    "C4": 48, "C#4": 49, "D4": 50, "D#4": 51, "E4": 52, "F4": 53, "F#4": 54, "G4": 55, "G#4": 56, "A4": 57, "A#4": 58, "B4": 59,
    "C5": 60, "C#5": 61, "D5": 62, "D#5": 63, "E5": 64, "F5": 65, "F#5": 66, "G5": 67, "G#5": 68, "A5": 69, "A#5": 70, "B5": 71,
    "C6": 72, "C#6": 73, "D6": 74, "D#6": 75, "E6": 76, "F6": 77, "F#6": 78, "G6": 79, "G#6": 80, "A6": 81, "A#6": 82, "B6": 83,
    "C7": 84, "C#7": 85, "D7": 86, "D#7": 87, "E7": 88, "F7": 89, "F#7": 90, "G7": 91, "G#7": 92, "A7": 93, "A#7": 94, "B7": 95,
    "C8": 96, "C#8": 97, "D8": 98, "D#8": 99, "E8": 100, "F8": 101, "F#8": 102, "G8": 103, "G#8": 104, "A8": 105, "A#8": 106, "B8": 107
}

note = ('a',0)
notes = [68,71,72,74,76]
last_note = 0
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1 
noteHold = 0.1
soundEffectDuration = 1
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
        gyro = float(sensorData[1]) * -1
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))
    
    
    if(102 >= gyro >= 62):
        note = ('a',mapNotas["D4"])
    elif(61 >= gyro >= 21):
        note = ('a',mapNotas["B5"])
    elif(20 >= gyro >= -20):
        note = ('a',mapNotas["B5"])
    elif(-21 >= gyro >= -61):
        note = ('a',mapNotas["B5"])
    elif(-62 >= gyro >= -102):
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
                midiout.send_message([0x80,note[1],50])
                pass

    
    if(10000 > accel > 8000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["D4"],50]) 

    elif(-8000 > accel > -10000 and (time.time() - previousSoundEffectActiv >= soundeEffectInterval)):
        previousSoundEffectActiv = time.time()
        midiout.send_message([0x91,mapNotas["D4"],50])
    
    if(time.time() - previousSoundEffectActiv >= soundeEffectInterval):
        previousSoundEffect = time.time()
        midiout.send_message([0x81,mapNotas["D4"],50]) 
