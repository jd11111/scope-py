import math
import numpy as np
from matplotlib import pyplot as plt
import time
from ctypes import cdll, byref, POINTER, create_string_buffer, c_float, c_int16, c_int32, c_uint32, c_void_p
#from ctypes import c_int32 as c_enum

lib = cdll.LoadLibrary("/home/jd/scope-py/libps2000.so")
UNIT_INFO_TYPES = {"DriverVersion": 0,
                       "USBVersion": 1,
                       "HardwareVersion": 2,
                       "VariantInfo": 3,
                       "BatchAndSerial": 4,
                       "CalibrationDate": 5,
                       "ErrorCode": 6,
                       "KernelDriverVersion": 7}

voltRangeOpts= {20:1,50:2,100:3,200:4,500:5,1000:6,2000:7,5000:8,10000:9,20000:10}
couplingOpts = {"AC": 0, "DC":1}
channelOpts = {"A":0, "B" : 1}
sigOpts = {}


class ps2000():
    def __init__(self):
        code =lib.ps2000_open_unit()
        if code ==0:
            raise Exception("scope could not be found/accessed")
        self.handle = code
        self.channelset =False
        print("opening scope successful")
        lib.ps2000_flash_led(c_int16(self.handle))

    def dump_info(self):
        s = create_string_buffer(256)
        print("dumping scope info:")
        for info in UNIT_INFO_TYPES.keys():
            print(info+":")
            lib.ps2000_get_unit_info(c_int16(self.handle), byref(s), c_int16(len(s)), c_int32(UNIT_INFO_TYPES[info]))
            print(s.value.decode('utf-8'))

    def close_scope(self):
        lib.ps2000_close_unit(c_int16(self.handle))

    def set_channel(self, channel, active, voltRange,coupling):
        code = lib.ps2000_set_channel(c_int16(self.handle),c_int16(channelOpts[channel]), c_int16(active),c_int16(couplingOpts[coupling]),c_int16(voltRangeOpts[voltRange]))
        if code ==0:
            raise Exception("channel values out of range/error setting channel")
        print("channel set successfully")
        self.check_tb()
        self.channelset= True

    def check_tb(self):
        self.tbs =[]
        self.tis = []
        self.mss = []
        tb =1
        cond = True
        while cond:
            ti = c_int32()
            ms = c_int32()
            code = lib.ps2000_get_timebase(c_int16(self.handle),c_int16(tb),c_void_p(),byref(ti),c_void_p(),c_int16(1),byref(ms))
            if code==0:
                cond = False
            else:
                self.tis.append(ti)
                self.tbs.append(tb)
                self.mss.append(ms)
                tb+=1

    def sig_gen(self):











scope = ps2000()
scope.dump_info()
scope.set_channel("A",True,100,"DC")
scope.close_scope()
"""
handle = lib.ps2000_open_unit()
print(handle)
info = "DriverVersion"
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

code = lib.ps2000_set_sig_gen_built_in(c_int16(handle),c_int32(0),c_uint32(10**6),c_int16(0),c_float(1.43),c_float(1.43),c_float(0),c_float(0),c_int16(0),c_uint32(0))
print("code for sig gen")
print(code)

def run_block(T):
    for ind, tb in enumerate(tbs):
        if T<tis[ind].value*mss[ind].value:
            besttb = tb
            bestidx = ind
            success =True
            break
    if not success:
        raise Expection("Time T is too large")

    code = lib.ps2000_run_block(c_int16(handle),mss[bestidx],c_int16(besttb),c_int16(1),c_void_p())
    while not lib.ps2000_ready(c_int16(handle)):
        time.sleep(0.2)

    dataA = np.zeros(mss[bestidx].value,dtype=np.int16)
    dataB = np.zeros(mss[bestidx].value,dtype=np.int16)

    dataAPtr = dataA.ctypes.data_as(POINTER(c_int16))
    dataBPtr= dataB.ctypes.data_as(POINTER(c_int16))

    code = lib.ps2000_get_values(c_int16(handle),dataAPtr,dataBPtr,c_void_p(),c_void_p(),c_void_p(),mss[bestidx])

    return dataA, dataB, tis[bestidx].value, mss[bestidx].value

dataA, dataB, dt, n = run_block(T)

lib.ps2000_close_unit(c_int16(handle))

fig, ax  = plt.subplots()
ax.plot(10**-9*dt*np.array(range(n)),dataA/32767)

plt.savefig("test.png")
    """
