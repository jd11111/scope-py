from matplotlib import pyplot as plt
import sys
sys.path.insert(0, '../')
import scope
import numpy as np
import ctypes
import math
import time
#open the scope:

myscope = scope.ps2000()

#dump the scope info:
myscope.dump_info()

#set channel A to be active in DC coupling mode with the voltage range 1V
myscope.set_channel("A",True,1000,"DC")
myscope.set_channel("B",True,1000,"DC")


X = np.linspace(0,1,4096)
waveform = np.piecewise(X,[X<0.3,X>=0.3],[lambda x : 3.33*x, lambda x : 0])
waveform = 255*(waveform+1)/2
waveform = np.clip(waveform,a_min= 0, a_max = 255)
arbwave = waveform.astype("uint8")
#print(arbwave)

tau = 5.4E-4
f0 = 1/(10*tau)
ddsFreq = 48*10**6
y =32+ math.log2(f0/ddsFreq)
print(y)
deltaPhaseExp = math.trunc(y)
f = ddsFreq * 2**(deltaPhaseExp-32)
print(f)

myscope.arb_wave_sig_gen(2*10**6,deltaPhaseExp,arbwave,0)

T= 1*10**9/f

#treshold = int(np.rint(32767*0.2))
#myscope.arm_trigger("A",treshold,delay=-20)
dt, n = myscope.run_block(T)
myscope.wait_ready()
dataA, dataB = myscope.get_block()
myscope.close_scope()

fig, ax  = plt.subplots()
#plot data (in volts and with time in seconds)
times = 10**-9*dt*np.array(range(n))
vDataA = dataA/32767
vDataB = dataB/32767
ax.plot(times,vDataA)
ax.plot(times,vDataB)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.grid()
plt.savefig("rc_inhom.png")
np.savetxt("rc_inhom_times",times)
np.savetxt("rc_inhom_chA",vDataA)
np.savetxt("rc_inhom_chB",vDataB)
