from ctypes import *
from sys import platform
import time

# load the c++ library from the dll#
lib_path = "./"
if platform.startswith('win32'):
    lib_path = "./usb_relay_dll/usb_relay_device.dll"
try:
    relay_lib = CDLL(lib_path)
    print("Successfully loaded ", relay_lib)
except Exception as e:
    print(e)


# class for the c++ device info structure#
class RelayDeviceInfo(Structure): pass


RelayDeviceInfo._fields_ = [("serial_number", c_uint),
                            ("device_path", c_char),
                            ("type", c_uint),
                            ("next", POINTER(RelayDeviceInfo))]
# initiate relays#
relay_lib.usb_relay_init()
# enumerate relay device and save info as relay_device_info#
open_relay = RelayDeviceInfo(relay_lib.usb_relay_device_enumerate())
# open relay device and save handle#
open_relay_handle = relay_lib.usb_relay_device_open_with_serial_number(open_relay.serial_number)


# open all relay channels
# @return: 0 -- success; 1 -- error
def open_all_channels():
    return relay_lib.usb_relay_device_open_all_relay_channel(open_relay_handle)


# open relay channel of a given relay index
# @returns: 0 -- success; 1 -- error; 2 -- index is out of bounds
def open_one_relay_channel(index):
    return relay_lib.usb_relay_device_open_one_relay_channel(open_relay_handle, index)


# close all relay channels
# @returns: 0 -- success; 1 -- error
def close_all_channels():
    return relay_lib.usb_relay_device_close_all_relay_channel(open_relay_handle)


# close relay channel of a given relay index
# @returns: 0 -- success; 1 -- error; 2 -- index is out of bounds
def close_one_relay_channel(index):
    return relay_lib.usb_relay_device_close_one_relay_channel(open_relay_handle, index)


# a simple test function to open all relays given a delay time (assuming all channel's indices are 0,1....7)
def test_relays(delay_time):
    for i in range(8):
        assert open_one_relay_channel(i) == 0, "error opening relay channel number " + str(i) + ""
        print("relay channel number " + str(i) + " opened")
        time.sleep(delay_time)
