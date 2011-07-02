"""
 Python Wrapper around BASS
"""

from ctypes import *
bass = windll.bass
from constants import *
from errorcodes import ErrorCodes
from devices import *
from streams import FileStream

def build_flags(flags):
	"""
	Takes a list of BASS flags and builds them
	into an int to pass to native code
	"""
	ret = 0
	for flag in flags:
		ret = ret & flag
	return ret

def get_version():
	"""
	Parses HIWORD and returns Major.Minor
	revs. This is a bit of a hack and maybe
	should be replaced with proper bit twiddling
	"""
	vh = hex(bass.BASS_GetVersion() >> 16)
	sh = str(vh)
	return sh[2:].replace("0", ".")

def error_get_code():
	"""
	Gets the code of the last error BASS encountered
	If there was no error in the last bass call then
	0 (BASS_OK) is returned
	"""
	return bass.BASS_ErrorGetCode()

def get_last_error():
	"""
	Gets the string describing the last error
	BASS_OK is returned if there is no error
	"""
	return ErrorCodes[error_get_code()]

class BASS_DEVICEINFO(Structure):
	_fields_ = [("name", c_char_p),
	              ("driver", c_char_p),
				  ("flags", c_uint)]
	
def get_device_info(device_id):
	"""
	Calls BASS_GetDeviceInfo and returns
	a dict of info about the device structured
	like the BASS_DEVICEINFO struct. Returns None
	if the device_id is invalid (ie too high or negative)
	NB: the device with id 0 is the BASS no_sound device
	    that should be used if no sound output is required
	"""
	if device_id < 0:
		return None
	
	info_out = BASS_DEVICEINFO()
	if bass.BASS_GetDeviceInfo(device_id, byref(info_out)):
		return {
			"name": info_out.name,
			"driver": info_out.driver,
			"enabled": bool(info_out.flags & BASS_DEVICE_ENABLED),
			"default": bool(info_out.flags & BASS_DEVICE_DEFAULT),
			"init": bool(info_out.flags & BASS_DEVICE_INIT)
		}
	else:
		return None
	
def enumerate_playback_devices():
	"""
	Enumerates all audio playback devices
	and returns all their info from get_device_info
	Does not include the No Sound device
	"""
	devices = []
	device_id = 1
	dev_info = get_device_info(device_id)
	while(dev_info):
		devices.append(dev_info)
		device_id = device_id + 1
		dev_info = get_device_info(device_id)
		
	return devices
	