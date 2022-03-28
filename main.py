import time
from ctypes import *
import ctypes as ctypes
import sys
from errorCodes import checkError

__author__ = "Michael Haldimann"
__version__ = "0.1"
__email__ = "ham11@bfh.ch"
__status__ = "Testing"

"""     Datatypes c_types to MiniMACS
            c_types.c_ushort  16 bit   --> Unsigned 16
            c_types.c_short   16 bit   --> Signed 16                           
            c_types.c_uint    32 bit   --> Unsigned 32
            c_types.c_int     32 bit   --> Signed 32

            -->To find out the size
            #print("Size of:", sys.getsizeof(test))
"""

# ZbMoc Library path
path = 'C:\Program Files (x86)\Aposs\ZbMoc.dll'

# Load library
cdll.LoadLibrary(path)
MiniMACS = CDLL(path)

# Defining return variables from Library Functions
ret = 0
pErrorCode = c_uint()
pDeviceErrorCode = c_uint()


class ZbMocOpenUsbParamS(ctypes.Structure):
    _fields_ = [("baud", ctypes.c_uint), ("retry", ctypes.c_ushort), ("timeout", ctypes.c_uint),
                ("flags", ctypes.c_uint), ("latency", ctypes.c_uint)]



class ZbMocOpenTcpParamS(ctypes.Structure):
    _fields_ = [("local", ctypes.c_bool), ("address", ctypes.c_uint), ("port", ctypes.c_uint),
                ("retry", ctypes.c_ushort), ("timeout", ctypes.c_uint), ("flags", ctypes.c_uint)]


if __name__ == "__main__":
    print("The type of connection can be changed with the variable method.")
    print("0=USB, 1=TCP")
    # Input for the type of connetion
    method = 1

    # Defining return variables from Library Functions
    keyHandle = ctypes.c_short(0)

    # Close all interface
    status = ctypes.c_short(MiniMACS.ZbMocCloseAll()).value

    # ID of the MiniMACS
    MiniMACS_ID = ctypes.c_ushort(1)

    if method == 0:
        # Parameter for the connection
        paramsUBS = ZbMocOpenUsbParamS(921600, 6, 50, 2, 1)

        # Start of the USB-Connection
        # C-Implementation: SIGNED16 ZbMocOpenUsb(ZbMocOpenUsbParamS *param);
        keyHandle = ctypes.c_short(MiniMACS.ZbMocOpenUsb(byref(paramsUBS)))
        print("KeyHandle:", keyHandle)

        # Connecting
        # C-Implementation: SIGNED16 ZbMocConnect(UNSIGNED16 h, UNSIGNED16 id);
        status = ctypes.c_short(MiniMACS.ZbMocConnect(keyHandle, MiniMACS_ID)).value
        print("Status: ZbMocConnect: ")
        checkError(status)


    else:
        # The ip address of the MiniMACS from APOSS
        paramsTCP = ZbMocOpenTcpParamS(c_bool(False), c_uint(16925454187), ctypes.c_uint(23), c_ushort(1000),
                                       c_uint(500), c_uint(9))
        keyHandle = ctypes.c_short(MiniMACS.ZbMocOpenTcp(byref(paramsTCP)))
        print("KeyHandle:", keyHandle.value)

    # Connecting
    # C-Implementation: SIGNED16 ZbMocConnect(UNSIGNED16 h, UNSIGNED16 id);
    status = ctypes.c_short(MiniMACS.ZbMocConnect(keyHandle, MiniMACS_ID)).value
    print("Status: ZbMocConnect: ")
    checkError(status)
    
    # Array for the values
    size = ctypes.c_int * 4
    array_reading = size(1)
    array_reading = size(-1, -1, -1, -1)

    # Reading Values
    # C-Implementation: SIGNED16 ZbMocUserParamReadRaw(UNSIGNED16 h, UNSIGNED16 id, SIGNED32 *param, UNSIGNED16 first, UNSIGNED16 last);
    status = ctypes.c_short(
        MiniMACS.ZbMocUserParamReadRaw(keyHandle, MiniMACS_ID, byref(array_reading), ctypes.c_ushort(0),
                                       ctypes.c_ushort(3))).value
    print("Status: ZbMocUserParamReadRaw: ")
    checkError(status)
    print("The values are:", array_reading[0:4])

    # Benchmark Test
    start_time = time.time()
    seconds = 10
    counter = 0

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Connecting
        # C-Implementation: SIGNED16 ZbMocUserParamReadRaw(UNSIGNED16 h, UNSIGNED16 id, SIGNED32 *param, UNSIGNED16 first, UNSIGNED16 last);
        status = ctypes.c_short(
            MiniMACS.ZbMocUserParamReadRaw(keyHandle, MiniMACS_ID, byref(array_reading), ctypes.c_ushort(0),
                                           ctypes.c_ushort(3))).value
        counter += 1
        if elapsed_time > seconds:
            break

    print("In:", seconds, "the ZbMocUserParamReadRaw could read:", counter, " times.")
    print("Reading takes in average:", (seconds / counter * 1000), "ms")
