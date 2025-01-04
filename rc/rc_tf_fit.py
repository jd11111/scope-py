import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from uncertainties import ufloat as uf
def shifted_sin(t,omega,phi,U0):
    return U0*np.sin(omega*t+phi)

fs = np.loadtxt("freqs")
fs = fs[0:-2]
print(len(fs))
pshifts = []
vquots = []
for idx , f in enumerate(fs):
    times = np.loadtxt("rc_data/times_tf_"+str(idx))
    chA = np.loadtxt("rc_data/chA_tf"+str(idx))
    chB = np.loadtxt("rc_data/chB_tf"+str(idx))
    v0 = np.max(chB)
    v0 = np.max([v0,0.01])
    #mask = (0.0070 < times) & (times <0.011)
    #chAf = chA[mask]
    #print(len(chAf))
    #chBf = chB[mask]
    #timesf = times[mask]
    #timesf = timesf-timesf[0]
    poptA, pcovA = curve_fit(shifted_sin,times,chA,p0=[ 2*np.pi*f, 0.0 ,2.0])#, bounds =([0.0,-2*np.pi,0.0],[10*2*np.pi*f,2*np.pi,10.0]))
    poptB, pcovB = curve_fit(shifted_sin,times,chB,p0=[ 2*np.pi*f, 0.0 ,v0])#, bounds =([0.5*np.pi*f,-2*np.pi,0.0],[5*2*np.pi*f,2*np.pi,5.0]))

    print("poptA")
    print(poptA)
    print("poptB")
    print(poptB)

    phiA = poptA[1]
    phiB = poptB[1]
    dphi = phiB-phiA
    dphi = dphi- 2*np.pi*np.rint(dphi/(2*np.pi))
    if dphi >0.1:
        dphi = dphi-np.pi
    print("phase shift")
    print(dphi)
    pshifts.append(dphi)
    print("voltage quot")
    vquot =poptB[2]/2.0 #poptA[2]
    print(vquot)
    vquots.append(vquot)
    #tau = popt[0]
    """
    fig, ax = plt.subplots()
    ax.plot(times,chA, label="ch A", zorder =3)
    ax.plot(times,chB, label = "ch B", zorder=3)
    #fitlabel = r"fit $\tau=${:.2e}".format(tau)
    ax.plot(times, shifted_sin(times,*poptA),zorder=4, ls="--", label ="fit chB")
    ax.plot(times, shifted_sin(times,*poptB),zorder=4,ls ="--", label = "fit chA")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("voltage (V)")
    ax.ticklabel_format(axis="x",style="sci", scilimits=(0,0))
    plt.grid()
    plt.legend()
    plt.savefig("rc_data/rc_tf_fit_"+str(idx)+".png")
    plt.close()
        """


font = {'family' : "sans-serif",
        'weight' : "normal",
        'size'   : 10,
        "sans-serif":"Computer Modern Sans Serif"}
mpl.rc("font",**font)
mpl.rcParams["mathtext.fontset"] = "cm"
mpl.rcParams["text.latex.preamble"]=r"\usepackage{siunitx} \sisetup{separate-uncertainty = true}"
mpl.rc('text', usetex = True)
textwidth = 0.495*452.9678*0.0138889

pshifts = np.array(pshifts)
vquots = np.array(vquots)

def args(f,f0):
    return -np.arctan(f/f0)

tau = 5.7E-4
f0 = 1/(2*np.pi*tau)
poptf0, pcovf0 = curve_fit(args,fs,pshifts,p0=[f0])
perr = np.sqrt(np.diag(pcovf0))
print("fitpars shift")
f0opt = uf(poptf0[0],perr[0])
print("shift tau")
print(1/(2*np.pi*f0opt))
#X = f0*np.logspace(-2,2,100)
X= np.logspace(0,5,500)
fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.scatter(fs,pshifts,zorder=4, label = "data", s=3, color ="teal")
ax.plot(X, args(X,*poptf0),zorder=6, label="fit", lw=1, color ="gold")
#ax.plot(X, args(X,f0),zorder=5, label="initial guess", color="yellow")
ax.set_xlabel("frequency $f$ (\SI{}{\hertz})", labelpad=0)
ax.set_ylabel(r"phase shift $\varphi$", labelpad=0)
#ax.set_ylim(-1.6,0.0)
ax.set_xscale("log")
ax.set_yticks([-np.pi/2, -np.pi/4,0.0])
ax.set_ylim(-1.1*np.pi/2,0.1)
ax.set_xlim(1,10**5)
ax.set_xticks([1E0,1E1,1E2,1E3,1E4,1E5])
ax.tick_params(axis='both', which='major', pad=0.3)
ax.set_yticklabels([r"$-\frac{\pi}{2}$",r"$-\frac{\pi}{4}$","0"])
plt.grid()
plt.legend(loc="lower left", borderpad = 0.2, labelspacing =0.1)
fig.tight_layout(pad=0.1)
#plt.savefig("shifts.pdf")
plt.close()

def abs(f,f0,c):
    return c/(np.sqrt(1+ (f/f0)**2))

vquots = np.abs(vquots)
poptf0, pcovf0 = curve_fit(abs,fs,vquots,p0=[f0,1.0])
perr = np.sqrt(np.diag(pcovf0))
print("fitpars abs")
f0opt = uf(poptf0[0],perr[0])
print("abs tau")
print(1/(2*np.pi*f0opt))
#print(1/(2*np.pi*perr))

fig, ax = plt.subplots(figsize=(textwidth,9/16*textwidth))
ax.scatter(fs,vquots, zorder=4, marker ="o", label ="data", s=3, color ="teal")
#ax.plot(X,abs(X,f0,1.0),label="initial guess", zorder=5,color="yellow", lw=2)
ax.plot(X,abs(X,*poptf0),label="fit", zorder=6, lw=1, color ="gold")
ax.set_xlabel("frequency $f$ (\SI{}{\hertz})", labelpad=0)
ax.set_ylabel("$U_\mathrm{out}/ U_\mathrm{in}$", labelpad=0)
#ax.axvline(poptf0[0], color ="black", lw=1, label ="$f_0$")
plt.grid()
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_ylim(bottom = 10**-3)
ax.set_xlim(left=1)
ax.tick_params(axis='both', which='major', pad=0.3)
#ax.set_xticks([1E0,1E1,1E2,1E3,1E4,1E5])
plt.legend(loc="lower left", borderpad = 0.2, labelspacing =0.1)
fig.tight_layout(pad=0.1)
#plt.savefig("quots.pdf")
