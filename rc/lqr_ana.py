import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid
import matplotlib as mpl
from uncertainties import ufloat as uf

waveformtimes = np.loadtxt("lqr_waveformtimes")

lqr0_times = np.loadtxt("lqr_times0")
lqr0_chB = np.loadtxt("lqr_chB0")
lqr0_chA = np.loadtxt("lqr_chA0")


font = {'family' : "sans-serif",
        'weight' : "normal",
        'size'   : 10,
        "sans-serif":"Computer Modern Sans Serif"}
mpl.rc("font",**font)
mpl.rcParams["mathtext.fontset"] = "cm"
mpl.rcParams["text.latex.preamble"]=r"\usepackage{siunitx} \sisetup{separate-uncertainty = true}"
mpl.rc('text', usetex = True)
textwidth = 0.495*452.9678*0.0138889

#lqr0
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(lqr0_times*1000, lqr0_chB, color="gold", lw=1, label= "output",zorder= 3)
ax.plot(lqr0_times*1000, lqr0_chA, color="teal", lw=1, label="input", zorder =2)
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="upper left", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.2)
plt.savefig("lqr0_ana.pdf")
plt.close()


mask = (0.00883 <lqr0_times) & (lqr0_times < 0.014)

fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(1000*(lqr0_times[mask]-(lqr0_times[mask])[0]),lqr0_chB[mask], color="gold", lw=1, label= "output",zorder= 3)
ax.tick_params(axis='both', which='major', pad=0.5)
ax.set_xlim(0,3)
plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
ax.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xticks([0.0,0.5,1.0,1.5,2.0,2.5,3.0])

ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
fig.tight_layout(pad=0.2)
plt.savefig("lqr0_ana2.pdf")
plt.close()
lqr0_outputsq = trapezoid(lqr0_chB[mask]**2,x= lqr0_times[mask])
print("total cost lqr0:")
print(lqr0_outputsq)

#lqr1 (optimal)
lqr1_times = np.loadtxt("lqr_times1")
lqr1_chA = np.loadtxt("lqr_chA1")
lqr1_chB = np.loadtxt("lqr_chB1")
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(lqr0_times*1000, lqr1_chB, color="gold", lw=1, label= "output",zorder= 3)
ax.plot(lqr0_times*1000, lqr1_chA, color="teal", lw=1, label="input", zorder =2)
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.set_yticks([-0.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="lower left", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.2)
plt.savefig("lqr1_ana.pdf")
plt.close()

lqr1_waveform =np.loadtxt("Lqr_waveform2")

mask = (0.00882 <lqr1_times) & (lqr1_times < 0.014)

t0 = (lqr1_times[mask])[-1]- (lqr1_times[mask])[0]
mask2 = waveformtimes <= t0
inputcost = trapezoid(lqr1_waveform[mask2]**2,x= waveformtimes[mask2])
print("inputcost lqr1:")
print(inputcost)

fig, ax = plt.subplots()
ax.plot(waveformtimes[mask2],lqr1_waveform[mask2])
ax.plot(lqr1_times[mask]-(lqr1_times[mask])[0],lqr1_chB[mask])
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(1000*waveformtimes[mask2],lqr1_waveform[mask2], color="teal", lw=1, label= "input",zorder= 2)
ax.plot(1000*(lqr1_times[mask]-(lqr1_times[mask])[0]),lqr1_chB[mask], color="gold", lw=1, label="output", zorder =3)
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.set_yticks([-0.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xlim(0,3)
ax.set_xticks([0.0,0.5,1.0,1.5,2.0,2.5,3.0])
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.2)
plt.savefig("lqr1_ana2.pdf")
plt.close()
lqr1_outputsq = trapezoid(lqr1_chB[mask]**2,x=lqr1_times[mask])
print("output cost lqr1:")
print(lqr1_outputsq)
print("total cost lqr1:")
print(lqr1_outputsq+inputcost)


##lqr2

lqr2_times = np.loadtxt("lqr_times2")
lqr2_chB = np.loadtxt("lqr_chB2")
lqr2_chA = np.loadtxt("lqr_chA2")
lqr2_waveform =np.loadtxt("Lqr_waveform3")
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(lqr0_times*1000, lqr2_chB, color="gold", lw=1, label= "output",zorder= 3)
ax.plot(lqr0_times*1000, lqr2_chA, color="teal", lw=1, label="input", zorder =2)
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.set_yticks([-0.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="lower left", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.2)
plt.savefig("lqr2_ana.pdf")
plt.close()

mask = (0.00873 <lqr2_times) & (lqr2_times < 0.014)

t0 = (lqr2_times[mask])[-1]- (lqr2_times[mask])[0]
mask2 = waveformtimes <= t0

inputcost = trapezoid(lqr2_waveform[mask2]**2,x= waveformtimes[mask2])
print("inputcost lqr2")
print(inputcost)

fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.plot(1000*waveformtimes[mask2],lqr2_waveform[mask2], color="teal", lw=1, label= "input",zorder= 2)
ax.plot(1000*(lqr2_times[mask]-(lqr2_times[mask])[0]),lqr2_chB[mask], color="gold", lw=1, label="output", zorder =3)
ax.set_xlim(0,3)
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.set_yticks([-0.5,-0.25,0.0,0.25,0.5,0.75,1.0])
ax.set_xticks([0.0,0.5,1.0,1.5,2.0,2.5,3.0])
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.2)
plt.savefig("lqr2_ana2.pdf")
plt.close()

lqr2_outputsq = trapezoid(lqr2_chB[mask]**2,x=lqr2_times[mask])
print("output cost lqr2:")
print(lqr2_outputsq)
print("total cost lqr2:")
print(lqr2_outputsq+inputcost)
