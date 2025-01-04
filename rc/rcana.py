import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl
from uncertainties import ufloat as uf

times = np.loadtxt("times")
chA = np.loadtxt("chA")
chB = np.loadtxt("chB")

def expdecay(t,tau,V0):
    return V0*np.exp(-t/tau)

font = {'family' : "sans-serif",
        'weight' : "normal",
        'size'   : 10,
        "sans-serif":"Computer Modern Sans Serif"}
mpl.rc("font",**font)
mpl.rcParams["mathtext.fontset"] = "cm"
mpl.rcParams["text.latex.preamble"]=r"\usepackage{siunitx} \sisetup{separate-uncertainty = true}"
mpl.rc('text', usetex = True)
textwidth = 0.495*452.9678*0.0138889

fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))

ax.plot(times*1000, chA, color="gold", lw=1, label= "input",zorder= 3)
ax.plot(times*1000, chB, color="teal", lw=1, label="output", zorder =3)
#ax.ticklabel_format(axis="x",style="sci", scilimits=(0,0))
ax.set_xlabel(r"time (\SI{}{\milli \second})", labelpad= 0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})",labelpad=0.5)
ax.tick_params(axis='both', which='major', pad=0.5)

plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
ax.set_xlim(0,25)
ax.set_yticks([0,0.2,0.4,0.6,0.8,1])
fig.tight_layout(pad=0.1)
#plt.savefig("discharge.pdf")
plt.close()


fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
mask = (0.007 < times) & (times <0.011)
chAf = chA[mask]
print(len(chAf))
chBf = chB[mask]
timesf = times[mask]
timesf = timesf-timesf[0]
popt, pcov = curve_fit(expdecay,timesf,chBf,p0=[0.001,1.0])
perr = np.sqrt(np.diag(pcov))
print("tau =")
print(uf(popt[0], perr[0]))
ax.plot(1000*timesf,chBf, label="output", zorder =3, color="teal",lw=1)
#ax.plot(timesf,chBf, label = "ch B", zorder=3)
ax.plot(1000*timesf, expdecay(timesf,*popt),zorder=4,color="gold",label = "fit", lw=1, ls="--")
ax.set_xlabel("time (\SI{}{\milli \second})", labelpad=0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})", labelpad=0.5)
#ax.set_ylim(0,1)
ax.set_xlim(0,4)
ax.set_yscale("log")
#ax.ticklabel_format(axis="x",style="sci", scilimits=(0,0))
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.1)
#plt.savefig("discharge_fit.pdf")
