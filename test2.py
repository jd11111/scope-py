import math
import numpy as np
from matplotlib import pyplot as plt
import time
from ctypes import cdll
from ctypes import byref, POINTER, create_string_buffer, c_float, c_int16, c_int32, c_uint32, c_void_p
#from ctypes import c_int32 as c_enum

lib = cdll.LoadLibrary("/home/jd/pico-python/libps2000.so")
handle = lib.ps2000_open_unit()
print(handle)
s = create_string_buffer(256)
UNIT_INFO_TYPES = {"DriverVersion": 0,
                       "USBVersion": 1,
                       "HardwareVersion": 2,
                       "VariantInfo": 3,
                       "BatchAndSerial": 4,
                       "CalibrationDate": 5,
                       "ErrorCode": 6,
                       "KernelDriverVersion": 7}
info = "DriverVersion"
for info in UNIT_INFO_TYPES.keys():
    print(info)
    lib.ps2000_get_unit_info(c_int16(handle), byref(s), c_int16(len(s)), c_int32(UNIT_INFO_TYPES[info]))
    print(s.value.decode('utf-8'))

lib.ps2000_flash_led(c_int16(handle))

c = lib.ps2000_set_channel(c_int16(handle),c_int16(0), c_int16(1),c_int16(1),c_int16(6))
print(c)

#Have: fixed time interval T (say period of signal)
#Want: smallest timebase tb such that ti*maxsamples > T
#Want: fixed nr of evenly spaced measurements
#Can ask scope: at timebase x what will be time dt between measurement, and how many measurements can we do (in one block)
#idea: loop over all timebases, check that we can do enough samples
tbs =[]
tis = []
mss = []
tb =1
cond = True
while cond:
    ti = c_int32()
    ms = c_int32()
    code = lib.ps2000_get_timebase(c_int16(handle),c_int16(tb),c_void_p(),byref(ti),c_void_p(),c_int16(1),byref(ms))
    if code==0:
        cond = False
    else:
        tis.append(ti)
        tbs.append(tb)
        mss.append(ms)
        tb+=1

print(tbs)
print(tis)
print(mss)

T = 10**9
for ind, tb in enumerate(tbs):
    if T<tis[ind].value*mss[ind].value:
        besttb = tb
        bestidx = ind
        break
print(besttb)

code = lib.ps2000_set_sig_gen_built_in(c_int16(handle),c_int32(0),c_uint32(10**6),c_int16(0),c_float(1.43),c_float(1.43),c_float(0),c_float(0),c_int16(0),c_uint32(0))
print("code for sig gen")
print(code)
oversamp =1
code = lib.ps2000_run_block(c_int16(handle),mss[bestidx],c_int16(besttb),c_int16(1),c_void_p())
print(code)

while not lib.ps2000_ready(c_int16(handle)):
    time.sleep(1)

dataA = np.zeros(mss[bestidx].value,dtype=np.int16)
dataB = np.zeros(mss[bestidx].value,dtype=np.int16)

dataAPtr = dataA.ctypes.data_as(POINTER(c_int16))
dataBPtr= dataB.ctypes.data_as(POINTER(c_int16))

code = lib.ps2000_get_values(c_int16(handle),dataAPtr,dataBPtr,c_void_p(),c_void_p(),c_void_p(),c_int32(mss[bestidx].value))

time.sleep(1)
print(dataA)
print(len(dataA))

lib.ps2000_close_unit(c_int16(handle))

fig, ax  = plt.subplots()
ax.plot(10**-9*tis[bestidx].value*np.array(range(mss[bestidx].value)),dataA/32767)

plt.savefig("test.png")
