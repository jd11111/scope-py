from matplotlib import pyplot as plt
import sys
sys.path.insert(0, '../')
import scope
import numpy as np
import ctypes
import math
import time

myscope = scope.ps2000()
myscope.dump_info()

myscope.set_channel("A",True,1000,"DC") #eingang
myscope.set_channel("B",True,1000,"DC") #ausgang

tau = 5.4E-4
f0 = 1/(15*tau)
ddsFreq = 48*10**6
y =32+ math.log2(f0/ddsFreq)
deltaPhaseExp = math.trunc(y)
f = ddsFreq * 2**(deltaPhaseExp-32)
TinS = 1/f

X = np.linspace(0,TinS,4096)

def opt_ctrl(u0,t):
    return -(np.sqrt(2)-1)*np.exp(-np.sqrt(2)*t/tau)*u0

def no_ctrl(t):
    return 0.0

def min_ctrl(t,u0,u1,t1):
    return 2*np.exp(-1*(t1-t)/tau)*(1-np.exp(-2*t1/tau))**-1*(u1-np.exp(-t1/tau)*u0)

u0= 1.0
waveform1 = np.piecewise(X,[X<0.5*TinS,X>=0.5*TinS],[lambda x : 0.0, lambda x : u0])
print(waveform1)
waveform2 = np.piecewise(X,[X<0.5*TinS,X>=0.5*TinS],[lambda x : opt_ctrl(u0,x), lambda x : u0])
t1 = 2*tau
print("t1=")
print(t1)
waveform3 = np.piecewise(X,[X<=t1, (t1 < X) & (X<= 0.5*TinS),0.5*TinS <X],[lambda x : min_ctrl(x,u0,0.0,t1), lambda x : 0.0, lambda x : u0])
print(waveform3)
np.savetxt("lqr_waveformtimes", X)
np.savetxt("lqr_waveform2",waveform2)
np.savetxt("lqr_waveform3", waveform3)

T= 1*10**9*TinS
for idx, waveform in enumerate([waveform1, waveform2,waveform3]):
    print(idx)
    arbwave, pk2pkr, offsetr = scope.mk_wave(waveform)
    myscope.arb_wave_sig_gen(pk2pkr,deltaPhaseExp,arbwave,offsetr)
    dt, n = myscope.run_block(T)
    myscope.wait_ready()
    dataA, dataB = myscope.get_block()
    fig, ax  = plt.subplots()
    #plot data (in volts and with time in seconds)
    times = 10**-9*dt*np.array(range(n))
    vDataA = dataA/32767
    vDataB = dataB/32767
    ax.plot(times,vDataA, label= "ch A")
    ax.plot(times,vDataB, label="ch B")
    #ax.set_ylim(-0.1,0.205)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("voltage (V)")
    plt.legend()
    plt.grid()
    plt.savefig("lqr_aq"+str(idx)+".png")
    np.savetxt("lqr_times_aq"+str(idx),times)
    np.savetxt("lqr_chA_aq"+str(idx),vDataA)
    np.savetxt("lqr_chB_aq"+str(idx),vDataB)

myscope.close_scope()
