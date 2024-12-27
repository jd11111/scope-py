from matplotlib import pyplot as plt
import scope
import numpy as np

#open the scope:
myscope = scope.ps2000()

#dump the scope info:
myscope.dump_info()

#set channel A to be active in DC coupling mode with the voltage range 1V
myscope.set_channel("A",True,1000,"DC")

#generate a sinwave with peak to peak 1V (so 0.5V amplitude) and frequency 1.43
myscope.sig_gen(10**6,"sin",1.43,1.43)


T= 10**9
#measure data for 1 second (signal generator output should be connected to channel A to measure something)
dataA, dataB, dt, n = myscope.run_block(T)
#close scope
myscope.close_scope()

fig, ax  = plt.subplots()
#plot data (in volts and with time in seconds)
ax.plot(10**-9*dt*np.array(range(n)),dataA/32767)
ax.set_xlabel("time (s)")
ax.set_ylabel("voltage (V)")
plt.grid()
ax.set_xlim(0.0,1.4)
ax.set_ylim(-0.6,0.6)
plt.savefig("example.png")
