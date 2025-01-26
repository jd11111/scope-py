import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid
import matplotlib as mpl
from uncertainties import ufloat as uf

waveformtimes = np.loadtxt("lqr_waveformtimes")

lqr0_times = np.loadtxt("lqr_times0")
lqr0_chA = np.loadtxt("lqr_chB0")

mask = (0.00883 <lqr0_times) & (lqr0_times < 0.014)

fig, ax = plt.subplots()
ax.plot(lqr0_times[mask],lqr0_chA[mask])
plt.savefig("lqr0ana.png")
lqr0_outputsq = trapezoid(lqr0_chA[mask]**2,x= lqr0_times[mask])
print("total cost lqr0:")
print(lqr0_outputsq)

#lqr1 (optimal)
lqr1_times = np.loadtxt("lqr_times1")
lqr1_chA = np.loadtxt("lqr_chB1")
lqr1_waveform =np.loadtxt("Lqr_waveform2")

mask = (0.00883 <lqr1_times) & (lqr1_times < 0.014)

t0 = (lqr1_times[mask])[-1]- (lqr1_times[mask])[0]
mask2 = waveformtimes <= t0
print(waveformtimes[mask2])

inputcost = trapezoid(lqr1_waveform[mask2]**2,x= waveformtimes[mask2])
print("inputcost lqr1")
print(inputcost)

fig, ax = plt.subplots()
ax.plot(waveformtimes[mask2],lqr1_waveform[mask2])
ax.plot(lqr1_times[mask]-(lqr1_times[mask])[0],lqr1_chA[mask])
plt.savefig("lqr1ana.png")
lqr1_outputsq = trapezoid(lqr1_chA[mask]**2,x=lqr1_times[mask])
print("output cost lqr1:")
print(lqr1_outputsq)
print("total cost lqr1:")
print(lqr1_outputsq+inputcost)


##lqr3
lqr2_times = np.loadtxt("lqr_times2")
lqr2_chA = np.loadtxt("lqr_chB2")
lqr2_waveform =np.loadtxt("Lqr_waveform3")

mask = (0.00873 <lqr2_times) & (lqr2_times < 0.014)

t0 = (lqr2_times[mask])[-1]- (lqr2_times[mask])[0]
mask2 = waveformtimes <= t0
print(waveformtimes[mask2])

inputcost = trapezoid(lqr2_waveform[mask2]**2,x= waveformtimes[mask2])
print("inputcost lqr2")
print(inputcost)

fig, ax = plt.subplots()
ax.plot(lqr2_times[mask]-(lqr2_times[mask])[0],lqr2_chA[mask])
ax.plot(waveformtimes[mask2],lqr2_waveform[mask2])
plt.savefig("lqr2ana.png")
lqr2_outputsq = trapezoid(lqr2_chA[mask]**2,x=lqr2_times[mask])
print("total cost lqr2:")
print(lqr2_outputsq+inputcost)
