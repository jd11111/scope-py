import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl
from uncertainties import ufloat as uf

times = np.loadtxt("rc_inhom_times")
chA = np.loadtxt("rc_inhom_chA")
chB = np.loadtxt("rc_inhom_chB")

def fitfun(t,tau,b):
    return (tau*(np.exp(-t/tau)-1)+t)*b

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
ax.set_xlim(2,8)
ax.tick_params(axis='both', which='major', pad=0.5)

plt.grid()
plt.legend(loc="upper right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
#ax.set_xlim(0,25)
#ax.set_yticks([0,0.2,0.4,0.6,0.8,1])
fig.tight_layout(pad=0.1)
plt.savefig("rc_inhom_ana.pdf")
plt.close()

fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
mask = (0.00345 < times) & (times <0.00507)
chAf = chA[mask]
chBf = chB[mask]
timesf = times[mask]
timesf = timesf-timesf[0]
popt, pcov = curve_fit(fitfun,timesf,chBf,p0=[0.0034,5000], bounds = ([0.0,0.0],[0.05,10**5]))
#perr = np.sqrt(np.diag(pcov))
#print("tau =")
print("optpars")
print(popt)
#print(uf(popt[0], perr[0]))
ax.plot(1000*timesf,chBf, label="output", zorder =3, color="teal",lw=2)
ax.plot(1000*timesf,chAf, label = "input", zorder=3, color ="black", lw=2)
ax.plot(1000*timesf, fitfun(timesf,*popt),zorder=4,color="gold",label = "fit", lw=2, ls="--")
ax.set_xlabel("time (\SI{}{\milli \second})", labelpad=0.5)
ax.set_ylabel(r"voltage (\SI{}{\volt})", labelpad=0.5)
ax.set_ylim(0,2)
#ax.set_xlim(0,4)
ax.set_yscale("log")
#ax.ticklabel_format(axis="x",style="sci", scilimits=(0,0))
ax.tick_params(axis='both', which='major', pad=0.5)
plt.grid()
plt.legend(loc="lower right", borderpad = 0.2, labelspacing =0.1, fontsize="small",handletextpad=0.2, borderaxespad =0.2, handlelength= 1.0)
fig.tight_layout(pad=0.1)
plt.savefig("rc_inhom_fit.pdf")
