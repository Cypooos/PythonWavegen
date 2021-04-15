32767;;;out.wav;;;44100;;;60;;;(55*2**x,2*x,2*x+2,ins_1,1) for x in range(0,3);;;ins_1;;;ins_0;;return noise(i*freq);;;ins_1;;t = i*frequency % 1
out = 1
i2 = ((i/2)**1.5)/4
if 0.5-i2 <= t <= 0.5+i2:out *= -1
if t >=0.5: out *=-1
return out;;;ins_2;;return noise(i*freq)