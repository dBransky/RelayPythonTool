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


# this class represents a relay controller 
class RelayDeviceController:
    def __init__(self, lib):
        self.handle = []
        self.lib = lib
        lib.usb_relay_init()
        self.info = RelayDeviceInfo(lib.usb_relay_device_enumerate())

    # open device
    def open_relay_device(self):
        self.handle.append(self.lib.usb_relay_device_open(byref(self.info)))
        print(self.handle[0].contents)
      
    # close device
    def close_relay_device(self):
        self.lib.usb_relay_device_close(self.handle[0])

    # open all relay channels
    # @return: -1 -- device is closed; 0 -- success; 1 -- error
    def open_all_channels(self):
        if len(self.handle) == 0: return -1
        return self.lib.usb_relay_device_open_all_relay_channel(self.handle[0])

    # open relay channel of a given relay index
    # @returns: -1 -- device is closed; 0 -- success; 1 -- error; 2 -- index is out of bounds
    def open_one_relay_channel(self, index):
        if len(self.handle) == 0: return -1
        return self.lib.usb_relay_device_open_one_relay_channel(self.handle[0], index)

    # close all relay channels
    # @returns: -1 -- device is closed; 0 -- success; 1 -- error
    def close_all_channels(self):
        if len(self.handle) == 0: return -1
        return self.lib.usb_relay_device_close_all_relay_channel(self.handle[0])

    # close relay channel of a given relay index
    # @returns: -1 -- device is closed; 0 -- success; 1 -- error; 2 -- index is out of bounds
    def close_one_relay_channel(self, index):
        if len(self.handle) == 0: return -1
        return self.lib.usb_relay_device_close_one_relay_channel(self.handle[0], index)

    # clear relay device
    def clear_controller(self):
        self.lib.usb_relay_device_free_enumerate(byref(self.info))
        self.lib.usb_relay_exit()
        self.handle = []


# class for the c++ device info structure#
class RelayDeviceInfo(Structure): pass


RelayDeviceInfo._fields_ = [("serial_number", c_ubyte),
                            ("device_path", c_char),
                            ("type", c_int),
                            ("next", POINTER(RelayDeviceInfo))]


# a simple test function to open all relays given a delay time (assuming all channel's indices are 0,1....7)
def test_relays(delay_time):
    #initiate a relayDeviceController
    relay_device = RelayDeviceController(relay_lib)
    #open device
    relay_device.open_relay_device()
    for i in range(8):
        assert (relay_device.open_one_relay_channel(i)) == 0, "error opening relay channel number " + str(i) + ""
        print("relay channel number " + str(i) + " opened")
        time.sleep(delay_time)
    #close all device channels
    relay_device.close_all_channels()
    #close relay device
    relay_device.close_relay_device()
    #clear controller
    relay_device.clear_controller()
