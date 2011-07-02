"""
 Python Wrapper around BASS
"""
from ctypes import *
bass = windll.bass

from bass import get_last_error

class PlaybackDevice:
	"""
	A playback device
	Created from a device_id number, use enumerate_playback_devices to get an id
	Use -1 for the default device
	Don't forget to close it when done otherwise you won't be able to open it again
	"""
	def __init__(self, device_id=-1, sample_rate=44100, flags=0):
		"""
		Initialise a playback device. Note, if the same device_id has already
		been initialised you cannot initialise it again.
		Constructing with no arguments uses the default device at 44100 Hz
		"""
		self.device_id = device_id
		# Initialise the device
		nflags = build_flags(flags) if flags else 0
		if not bass.BASS_Init(device_id, sample_rate, nflags, 0, None):
			raise Exception("Unable to create Playback Device %d. Error %s" % (device_id, get_last_error()))
	
	def free(self):
		"""
		Closes the device. BASS_Free
		"""
		bass.BASS_SetDevice(self.device_id)
		return bool(bass.BASS_Free())
	
	def get_volume(self):
		"""
		Gets the master volume level of this device. BASS_GetVolume
		TODO: work out why floats don't work properly
		"""
		bass.BASS_SetDevice(self.device_id)
		return bass.BASS_GetVolume()
	
	def set_volume(self, volume):
		"""
		Sets the master volume of this device. BASS_SetVolume
		NB: I once used this method on a Gina3G soundcard and it permanently
		borked it so nothing could ever play anything through it ever again
		so proceed with caution
		"""
		bass.BASS_SetDevice(self.device_id)
		return bool(bass.BASS_SetVolume(c_float(volume)))