Para dispositivos na mão direita:

        gyro = (float(sensorData[1]) * -1)
        accel = (float(sensorData[2]) * -1)


    if(102 >= gyro >= 52):
        note = ('C6',notes[3])
    elif(51 >= gyro >= 1):
        note = ('D6',notes[2])
    elif(0 >= gyro >= -50):
        note = ('G#5',notes[1])
    elif(-51 >= gyro >= -101):
        note = ('B5',notes[0])

5 notas 40° de diferença entre as notas

    if(102 >= gyro >= 62):
        note = ('C6',notes[0])
    elif(61 >= gyro >= 21):
        note = ('D6',notes[1])
    elif(20 >= gyro >= -20):
        note = ('G#5',notes[2])
    elif(-21 >= gyro >= -61):
        note = ('B5',notes[3])
    elif(-62 >= gyro >= -102):
        note = ('E6',notes[4])
        

6 notas 35° de diferença entre as notas

    if(120 >= gyro >= 71):
        note = ('B5',notes[0])
    elif(70 >= gyro >= 37):
        note = ('A5',notes[1])
    elif(36 >= gyro >= 1):
        note = ('G5',notes[2])
    elif(-1 >= gyro >= -36):
        note = ('F5',notes[3])
    elif(-37 >= gyro >= -70):
        note = ('E5',notes[4])
    elif(-71 >= gyro >= -120):
        note = ('E5',notes[5])


7 notas 26° de distancia entre as notas.

    if(120 >= gyro >= 88):
        note = ('B5',notes[0])
    elif(87 >= gyro >= 51):
        note = ('A5',notes[1])
    elif(50 >= gyro >= 14):
        note = ('G5',notes[2])
    elif(13 >= gyro >= -13):
        note = ('F5',notes[3])
    elif(-14 >= gyro >= -50):
        note = ('E5',notes[4])
    elif(-51 >= gyro >= -87):
        note = ('D5',notes[5])
    elif(-88 >= gyro >= -120):
        note = ('C5',notes[6])