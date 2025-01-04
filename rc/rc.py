import sys
sys.path.insert(0, '../')
from matplotlib import pyplot as plt
import scope
import numpy as np
#open the scope:
myscope = scope.ps2000()

#dump the scope info:
myscope.dump_info()

#set channel A to be active in DC coupling mode with the voltage range 1V
myscope.set_channel("A",True,1000,"DC")
myscope.set_channel("B",True,1000,"DC")

#generate a sinwave with peak to peak 1V (so 0.5V amplitude) and frequency 1.43
myscope.sig_gen(10**6,"square",100,100, offsetV=5*10**5)

T= 2*10**7
#measure data for 1 second (signal generator output should be connected to channel A to measure something)
dataA, dataB, dt, n = myscope.run_block(T)
#close scope
myscope.close_scope()

fig, ax  = plt.subplots()
#plot data (in volts and with time in seconds)
times = 10**-9*dt*np.array(range(n))
ax.plot(times,dataA/32767, label="ch A", zorder =3)
ax.plot(times,dataB/32767, label = "ch B", zorder=4)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.grid()
plt.legend()
plt.savefig("rc.png")

np.savetxt("times",times)
np.savetxt("chA",dataA/32767)
np.savetxt("chB",dataB/32767)
