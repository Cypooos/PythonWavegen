32767;;;out.wav;;;44100;;;60;;;(880,0,10,ins_0,1);;;ins_2;;;ins_0;;return math.sin(frequency*math.pi*2*i);;;ins_1;;t = i*frequency % 1
out = 1
i2 = ((i/2)**1.5)/4
if 0.5-i2 <= t <= 0.5+i2:out *= -1
if t >=0.5: out *=-1
return out;;;ins_2;;return noise(i*freq)