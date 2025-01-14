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
myscope.set_channel("B",True,500,"DC")

tau = 5.41E-4
f0 = 1/(20*tau)
ddsFreq = 48*10**6
y =32+ math.log2(f0/ddsFreq)
print(y)
deltaPhaseExp = math.trunc(y)
f = ddsFreq * 2**(deltaPhaseExp-32)
print(f)

TinS = 1/f
print(TinS)

X = np.linspace(0,TinS,4096)

def ctrl(t,u0,u1,t1):
    return 2*np.exp(-1*(t1-t)/tau)*(1-np.exp(-2*t1/tau))**-1*(u1-np.exp(t1/tau)*u0)

t1 = 10*tau
u0= 0.0
u1= 0.3
waveform = np.piecewise(X,[X<=t1,X>=t1],[lambda x : ctrl(x,u0,u1,t1), lambda x : 0.0])
fig,ax = plt.subplots()
ax.plot(X,waveform)
plt.savefig("ctrl_waveform.png")
#waveform = np.piecewise(X,[X<0.5*TinS,X>=0.5*TinS],[lambda x : 0.0, lambda x : u0])
pk2pk = np.max(waveform)- np.min(waveform)
print(pk2pk)
offset = np.min(waveform) + pk2pk/2
waveform  = waveform -np.min(waveform)
waveform = waveform/pk2pk
print(waveform)
waveform = 255*waveform
waveform = np.round(waveform)
waveform = np.clip(waveform,a_min= 0, a_max = 255)
arbwave = waveform.astype("uint8")
print(arbwave)

fig, ax  = plt.subplots()
ax.plot(X, waveform)
plt.savefig("waveform.png")

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
vDataB = 0.5*dataB/32767
ax.plot(times,vDataA, label= "ch A")
ax.plot(times,vDataB, label="ch B",zorder =5)
ax.axvline(tau)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.legend()
plt.grid()
plt.savefig("ctrl.png")
np.savetxt("ctrl_times",times)
np.savetxt("ctrl_chA",vDataA)
np.savetxt("ctrl_chB",vDataB)
