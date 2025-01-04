import sys
import time
sys.path.insert(0, '../')
from matplotlib import pyplot as plt
import scope
import numpy as np
#open the scope:
myscope = scope.ps2000()

#dump the scope info:
myscope.dump_info()

#set channel A to be active in DC coupling mode with the voltage range 1V
rangeopts = [50,100,200,500,1000,2000]
Vrange =2000
myscope.set_channel("A",True,2000,"DC")
myscope.set_channel("B",True,Vrange,"DC")
tau = 5.7E-4
f0 = 1/(2*np.pi*tau)
fs = f0*np.logspace(-2,2,num=200)
print(fs)

for idx,f in enumerate(fs):
    myscope.sig_gen(4*10**6,"sin",f,f)

    time.sleep(2)

    T0 = 2*1/f
    T = np.rint(T0*10**9)

    #measure data for 1 second (signal generator output should be connected to channel A to measure something)
    dataA, dataB, dt, n = myscope.run_block(T)
    #close scope

    fig, ax  = plt.subplots()
    #plot data (in volts and with time in seconds)
    times = 10**-9*dt*np.array(range(n))
    vDataA = dataA/32767
    vDataA = 2.0*vDataA
    vDataB = Vrange/1000*dataB/32767
    ax.plot(times,vDataA, label="ch A", zorder =3)
    ax.plot(times,vDataB, label = "ch B", zorder=4)
    ax.set_xlabel("time (s)")
    ax.set_ylabel("voltage (V)")
    ax.ticklabel_format(axis="x",style="sci", scilimits=(0,0))
    plt.grid()
    plt.legend()
    plt.savefig("rc_data/rc_tf"+str(idx)+".png")
    np.savetxt("rc_data/times_tf_"+str(idx),times)
    np.savetxt("rc_data/chA_tf"+str(idx),vDataA)
    np.savetxt("rc_data/chB_tf"+str(idx),vDataB)
    vmax = np.max(vDataB)
    for opt in rangeopts:
        if vmax<opt/1000:
            Vrange = opt
            print(Vrange)
            myscope.set_channel("B",True,Vrange,"DC")
            break
np.savetxt("rc_data/freqs",fs)
myscope.close_scope()
