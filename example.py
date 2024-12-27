from matplotlib import pyplot as plt
import scope
import numpy as np

myscope = scope.ps2000()
myscope.dump_info()
myscope.set_channel("A",True,1000,"DC")
myscope.sig_gen(10**6,"sin",1.43,1.43)

T= 10**9
dataA, dataB, dt, n = myscope.run_block(T)
myscope.close_scope()

fig, ax  = plt.subplots()
ax.plot(10**-9*dt*np.array(range(n)),dataA/32767)
plt.savefig("test.png")
