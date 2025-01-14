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
myscope.set_channel("B",True,200,"DC")

tau = 5.4E-4
f0 = 1/(30*tau)
ddsFreq = 48*10**6
y =32+ math.log2(f0/ddsFreq)
print(y)
deltaPhaseExp = math.trunc(y)
f = ddsFreq * 2**(deltaPhaseExp-32)
print(f)

TinS = 1/f
print(TinS)

X = np.linspace(0,TinS,4096)

def opt_ctrl(u0,t):
    return -(1+np.sqrt(2))*np.exp(-np.sqrt(2)*t/tau)*u0

u0= 0.2
waveform = np.piecewise(X,[X<0.5*TinS,X>=0.5*TinS],[lambda x : opt_ctrl(u0,x), lambda x : u0])
#waveform = np.piecewise(X,[X<0.5*TinS,X>=0.5*TinS],[lambda x : 0.0, lambda x : u0])
pk2pk = np.max(waveform)- np.min(waveform)
offset = np.min(waveform) + pk2pk/2
waveform  = waveform -np.min(waveform)
waveform = waveform/pk2pk
print(waveform)
waveform = 255*waveform
waveform = np.round(waveform)
waveform = np.clip(waveform,a_min= 0, a_max = 255)
arbwave = waveform.astype("uint8")
print(arbwave)

pk2pkr = np.round(pk2pk*10**6).astype("int")
offsetr = np.round(offset*10**6).astype("int")

myscope.arb_wave_sig_gen(pk2pkr,deltaPhaseExp,arbwave,offsetr)

T= 1*10**9*TinS

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
vDataB = 0.2*dataB/32767
ax.plot(times,vDataA, label= "ch A")
ax.plot(times,vDataB, label="ch B")
ax.set_ylim(-0.1,0.205)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.legend()
plt.grid()
plt.savefig("lqr.png")
np.savetxt("lqr_times",times)
np.savetxt("lqr_chA",vDataA)
np.savetxt("lqr_chB",vDataB)
