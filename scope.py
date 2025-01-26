import numpy as np
import time
import math
from ctypes import cdll, byref, POINTER, create_string_buffer, c_float, c_uint8, c_int16, c_int32, c_uint32, c_void_p

lib = cdll.LoadLibrary("/home/jd/scope-py/libps2000.so")
infoOpts = {"DriverVersion": 0,
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
sigOpts = {"sin":0, "square":1,"triangle":2,"rampup":3, "rampdown":4,"dc":5,"gaussian":6, "sinc":7,"halfsin":8}
sweepOpts = {"up":0,"down":1,"updown":2,"downup":3}
triggerDirectionOpts ={"rising":0, "falling" : 1}


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
        """dump the scope info"""
        s = create_string_buffer(256)
        print("dumping scope info:")
        for info in infoOpts.keys():
            print(info+":")
            lib.ps2000_get_unit_info(c_int16(self.handle), byref(s), c_int16(len(s)), c_int32(infoOpts[info]))
            print(s.value.decode("utf-8"))

    def close_scope(self):
        """close the scope"""
        lib.ps2000_close_unit(c_int16(self.handle))

    def set_channel(self, channel, active, voltRange,coupling):
        """set channel parameters and check available timebases, time intervals and max samples.

        Parameters:
        channel : {"A","B"}
        The channel for which parameters will be set
        active: bool
        If true the channel is active
        voltRange: {20,50,100,200,500,1000,2000,5000,10000,20000}
        The voltage range the channel will measure at in milliVolts
        coupling: {"AC","DC"}
        The kind of coupling for the channel (AC or DC)
        """
        code = lib.ps2000_set_channel(c_int16(self.handle),c_int16(channelOpts[channel]), c_int16(active),c_int16(couplingOpts[coupling]),c_int16(voltRangeOpts[voltRange]))
        if code ==0:
            raise Exception("channel values out of range/error setting channel")
        print("channel set successfully")
        self.check_tb()
        self.channelset= True

    def check_tb(self):
        """check available time bases time intervals and max samples."""
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

    def sig_gen(self,PkToPk,waveForm,startFreq,stopFreq,offsetV=0,increment=0.0,dwellTime=0.0,sweepType="up",sweeps=0):
        """
        Set signal generator parameters.
        Parameters:
        PkToPk : int32
        The peak to peak voltage of the signal in micro volts
        waveForm: {"sin", "square","triangle","rampup", "rampdown","dc","gaussian", "sinc","halfsin"}
        The waveform to be generated
        startFreq : float
        The frequency the waveform will be generated with initially in Hz
        stopFreq: float
        If unequal to startFreq the signal will be generated in sweep mode. In that case stopFreq is the frequency (in Hz) at which the sweep will reverse (frequency) direction/return to startFreq based on sweepType
        offsetV : int32
        offset voltage to be applied in microvolts
        increment: float
        the amount (in Hz) the frequency increases/decreases each dwellTime in sweep mode
        dwellTime: float
        the time between frequency changes in sweep mode in seconds
        sweepType: {"up","down","updown","downup"}
        the type of sweep to run (if stopFreq is inequal to startFreq)
        sweeps: int32
        the number of times to sweep (in sweep mode)
       """
        code = lib.ps2000_set_sig_gen_built_in(c_int16(self.handle),c_int32(offsetV),c_uint32(PkToPk),c_int16(sigOpts[waveForm]),c_float(startFreq),c_float(stopFreq),c_float(increment),c_float(dwellTime),c_int16(sweepOpts[sweepType]),c_uint32(sweeps))
        if code ==0:
            raise Exception("signal generation error/parameters out of range")
        print("signal generation started sucessfully")

    def run_block(self,T):
        """
        Log data for the channels for a time T starting immediately or if a trigger is armed based on the trigger.
        Parameters:
        T : int32
        The time the measurement has to exceed. The minimal timebase/timeinterval will be selected for which measurement with the maximum number of samples will exceed T.

        Returns:
        (self.tis[bestidx]).value : int32
        the time interval between consecutive measurements in nano seconds
        (self.mss[bestidx]).value : int32
        the number of samples generated (which is the maximal possible value)
        """
        if not self.channelset:
            raise Exception("can not run block without setting up channel first")
        success = False
        for ind, tb in enumerate(self.tbs):
            if T<(self.tis[ind]).value*(self.mss[ind]).value:
                besttb = tb
                self.bestidx = ind
                success =True
                break
        if not success:
            raise Expection("Time T is too large")

        code = lib.ps2000_run_block(c_int16(self.handle),self.mss[self.bestidx],c_int16(besttb),c_int16(1),c_void_p())
        if code ==0:
            raise Exception("Error running block/Parameters out of range")
        return (self.tis[self.bestidx]).value, (self.mss[self.bestidx]).value

    def get_block(self):
        """
        Get the data block currently stored on the scope. Must run_block() before and wait for it to finish.
        returns:
        dataA : numpy.ndarray with int32 entries
        the measured voltages for channel A. Linear scale with 32767= max voltage (channel range),  -32767 = min voltage (channel range)
        dataB : numpy.ndarray with int32 entries
        the measured voltages for channel B. Linear scale with 32767= max voltage (channel range),  -32767 = min voltage (channel range)
        """

        dataA = np.zeros((self.mss[self.bestidx]).value,dtype=np.int16)
        dataB = np.zeros((self.mss[self.bestidx]).value,dtype=np.int16)
        dataAPtr = dataA.ctypes.data_as(POINTER(c_int16))
        dataBPtr= dataB.ctypes.data_as(POINTER(c_int16))

        code = lib.ps2000_get_values(c_int16(self.handle),dataAPtr,dataBPtr,c_void_p(),c_void_p(),c_void_p(),self.mss[self.bestidx])
        if code ==0:
            raise Exception("Error getting block/Parameters out of range")
        print("block received")

        return dataA, dataB

    def wait_ready(self):
        """wait until the scope has finished"""
        while not lib.ps2000_ready(c_int16(self.handle)):
            time.sleep(0.2)
        print("scope ready")


    def arm_trigger(self,ch,threshold,direction="rising",delay=0):
        """
        Arms the trigger of the scope. The next run_block() will then use this trigger.
        Parameters:
        ch : {"A","B"}
        the channel to trigger from
        treshold : int16
        threshold for the trigger in ADC counts -32767 to 32767 (scaled to voltage range).
        direction: {"rising", "falling"}
        wheter to trigger when voltage rises above treshold (rising) or when it falls below it (falling)
        delay: int16
        The delay (as a percentage of block size) between trigger signal and the start of the block that is logged in percent. Must be -100<= delay <= 100. So delay of 0 means that the block starts at the trigger event and -50 that the trigger event is in the middle of the block.
        """
        code = lib.ps2000_set_trigger(c_int16(self.handle),c_int16(channelOpts[ch]),c_int16(threshold),c_int16(triggerDirectionOpts[direction]),c_int16(delay),c_int16(0))
        if code==0:
            raise Exception("Error arming trigger/Parameters out of range")
        print("trigger armed")

    def arb_wave_sig_gen(self,pkToPkV, deltaPhaseExp, waveForm,offsetV):
        """
        Generate arbitrary waveforms with the scopes signal generator.
        The scope has a (zero initialised) phase accumulator (a 32 bit integer), the first few bits (depending on the length of the waveForm) are used to index the given waveForm and the remaining bits do nothing.
        Every ddsPeriod (1/48Mhz) the scope adds deltaPhase (:=2**deltaPhaseExp) to the phase accumulator and generates the voltage from the given waveform at the index=first 12 bits of the phase accumulator.
        The frequency of the generated signal is:
        f = ddsFreq * 2**(deltaPhaseExp-32)
        Therefore the correct deltaPhaseExp can be found by deltaPhaseExp = 32+ log_2 (f/ddsFreq)

        Parameters:
        pkToPkV: int32
        Peak to peak voltage in micro volts
        deltaPhaseExp: uint
        2**deltaPhase is the number of steps in the phase accumulator (which indexes the wave form) to go each digital synthesis step
        waveForm: 1D numpy array with entries of type uint8
        The wave form data 255 = max voltage, 0 = min (negative) voltage with a linear scale between them, the length of waveForm should be 4096 (=2**12) and must not exceed it
        offsetV: int32
        the voltage offset of the signal in micro volts
        """
        if len(waveForm) != 4096:
            raise Exception("supply waveForm of length 4096 (=2**12)")
        waveFormSize = 2**12
        deltaPhase = 2**deltaPhaseExp
        waveFormPtr = waveForm.ctypes.data_as(POINTER(c_uint8))
        code = lib.ps2000_set_sig_gen_arbitrary(
            c_int16(self.handle),
            c_int32(offsetV),
            c_uint32(pkToPkV),
            c_uint32(deltaPhase),
            c_uint32(deltaPhase),
            c_uint32(0),
            c_uint32(0),
            waveFormPtr,
            c_int32(waveFormSize),
            c_int32(0),
            c_uint32(0))
        if code == 0:
            raise Exception("Error/Parameters out of range for arbitrary signal generation")
        print("arbitrary wave form signal generator started")

def mk_wave(wave):
    """ helper function that transforms waveform given as voltage data into correct format for AWG
    Parameters:
    wave: numpy array of floats
    Must be of length 4096, this is the waveform to be generated in volts
    Returns:
    arbwave: numpy array of uint8
    the waveform prepared for the awg
    pk2pkr: int
    the peak to peak voltage of the waveform in micro volts
    offsetr: int
    the offset voltage of the waveform in micro volts
    """
    waveform = np.copy(wave)
    pk2pk = np.max(waveform)- np.min(waveform)
    offset = np.min(waveform) + pk2pk/2
    waveform  = waveform -np.min(waveform)
    waveform = waveform/pk2pk
    waveform = 255*waveform
    waveform = np.round(waveform)
    waveform = np.clip(waveform,a_min= 0, a_max = 255)
    waveform =waveform.astype("uint8")
    pk2pkr = np.round(pk2pk*10**6).astype("int")
    offsetr = np.round(offset*10**6).astype("int")
    return waveform, pk2pkr, offsetr


