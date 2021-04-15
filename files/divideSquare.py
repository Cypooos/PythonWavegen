32767;;;out.wav;;;44100;;;60;;;(55*2**x,5*x,5*(x+1),ins_0,1) for x in range(3);;;ins_0;;;ins_0;;t = i*frequency % 1
out = 1
i2 = ((i/5)**1.5)/4
if 0.5-i2 <= t <= 0.5+i2:out *= -1
if t >=0.5: out *=-1
return out