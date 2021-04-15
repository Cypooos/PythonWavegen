import wave, struct, math, random
from perlin_noise import PerlinNoise


noise = PerlinNoise()

sampleRate = 44100 # hertz

obj = wave.open('out.wav','wb')

obj.setnchannels(1)
obj.setsampwidth(2)
obj.setframerate(sampleRate)




def ins_square_to_triangle(i,frequency):
  freq = frequency
  tri =  i*frequency % 1
  # (i*sampleRate)%frequency / frequency
  if tri > 0.5: squ = 1
  else: squ = 0.5

  return (tri*(i/5) + squ*((5-i)/5))*2-1




def INS_1(i,frequency):
  return math.sin(frequency*math.pi*2*i) * (2-i)/2

def square_devide(i,frequency):
  t =  i*frequency % 1
  out = 1
  i2 = ((i/2)**1.5)/4
  if 0.5-i2 <= t <= 0.5+i2:out *= -1
  if t >=0.5: out *=-1

  return out

  
def INS_3(i,frequency):
  return noise(i*frequency)

notes = [(55,0,5,square_devide,1)]
#notes = [(55,0,2,INS_2,1),(110,2,2,INS_2,1),(220,4,2,INS_2,1),(440,6,2,INS_2,1),(880,8,2,INS_2,1)]
# 32767

max_len = max([x[2]+x[1] for x in notes])
if max_len > 60: max_len = 60

out = [0 for x in range(max_len*sampleRate)]

for i,(freq,start,duration,ins,volume) in enumerate(notes):
    print("Doing note:",i)
    if duration + start > max_len: duration = max_len - start
    for x in range(duration*sampleRate):
      out[start*sampleRate+x] += ins(x/sampleRate,freq)*volume

print("out = ", out[0:100])
print("Writing frames...")

for i in out:
    if i >= 1: i = 1
    elif i <= -1: i = -1
    obj.writeframesraw( struct.pack('<h',int(i*32767)) )
obj.close()