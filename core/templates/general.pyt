import wave, struct, math, random
from perlin_noise import PerlinNoise
noise = PerlinNoise()

# Ajout possible de {#STARTDATA"} pour noise etc 

sampleRate = {#SAMPLERATE#} # hertz

obj = wave.open('{#OUT_FILE#}','wb')

obj.setnchannels(1)
obj.setsampwidth(2)
obj.setframerate(sampleRate)


{#INS_TEMPLATE#}


notes = [{#NOTES#}]
# 32767

max_len = max([x[2]+x[1] for x in notes])
if max_len > {#MAX_LEN#}: max_len = 60

out = [0 for x in range(max_len*sampleRate)]

for i,(freq,start,duration,ins,volume) in enumerate(notes):
    print("Doing note:",i)
    for x in range(duration*sampleRate):
        out[start*sampleRate+x] += ins(x/sampleRate,freq)*volume

print("out = ", out[0:100])
print("Writing frames...")

for i in out:
    if i >= 1: i = 1
    elif i <= -1: i = -1
    obj.writeframesraw( struct.pack('<h',int(i*32767)) )
obj.close()