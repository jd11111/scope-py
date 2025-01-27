from matplotlib import pyplot as plt
import scope
import numpy as np
import sys
sys.path.insert(0, '../')
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
waveform = 255*(np.sin(2*np.pi*X)+1)/2
arbwave = waveform.astype("uint8")
print(arbwave)

myscope.arb_wave_sig_gen(10**6,16,arbwave,0)

T= 2*10**9/1000 #signal generated is roughly 1000Hz
dt, n = myscope.run_block(T)
myscope.wait_ready()
dataA, dataB = myscope.get_block()
myscope.close_scope()

fig, ax  = plt.subplots()
#plot data (in volts and with time in seconds)
ax.plot(10**-9*dt*np.array(range(n)),dataA/32767)
ax.plot(10**-9*dt*np.array(range(n)),dataB/32767)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.grid()
plt.savefig("awg.png")
