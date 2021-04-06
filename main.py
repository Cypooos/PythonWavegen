"""
import wave, struct, math, random


sampleRate = 44100.0 # hertz

obj = wave.open('sound2.wav','wb')

obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)



def get_sound(i,frequency):
    return math.sin(frequency*math.pi*2*i) # simple 0 1 2 3 4 5 ... n




time = 40
# 32767
for i in range(1,int(time*sampleRate)):

    i_c = i
    if i>= 21.5*sampleRate:
        i_c = 21.5*sampleRate + i%440
    t = get_sound(i/44100,440+((10*i_c/(2*sampleRate))**3.5))

    data = struct.pack('<h', int(t*32767))
    obj.writeframesraw( data )
obj.close()

"""

from gui import GUI

GUI()
#"""