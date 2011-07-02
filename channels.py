"""
 Python wrapper around BASS
"""

from ctypes import *
bass = windll.bass

from bass import get_last_error
from constants import *
import utils

class Channel:
	"""
	A playable thing in BASS (independent of format)
	Don't create one of these directly but create
	subclasses instead, such as a Stream
	"""
	def __init__(self,handle):
		"""
		Requires the handle to use for all BASS_Channel* calls
		"""
		self.handle = handle
	
	def bytes_to_seconds(self, bytes):
		"""
		Converts a position in the channel from bytes to seconds
		"""
		return bass.BASS_ChannelBytes2Seconds(self.handle, bytes)
	
	def seconds_to_bytes(self, secs):
		"""
		Convert a position is seconds to bytes
		"""
		return bass.BASS_ChannelSeconds2Bytes(self.handle, secs)
	
	def length(self):
		"""
		Gets the length of the channel in bytes
		You can also use len() on a channel to get the same thing
		"""
		return bass.BASS_ChannelGetLength(self.handle, BASS_POS_BYTE)
	
	def __len__(self):
		return self.length()
	
	def level(self):
		"""
		Gets the level (peak amplitude of the channel)
		Returns tuple of (Left Channel Level, Right Channel Level)
		"""
		# Loword is level of Left channel, Hiword is Right
		levels = bass.BASS_ChannelGetLevel(self.handle)
		return (utils.loword(levels), utils.hiword(levels))
	
	def pos(self):
		"""
		Current playback position of the channel
		"""
		return bass.BASS_ChannelGetPosition(self.handle, BASS_POS_BYTES)
	
	def status(self):
		"""
		Status of the channel
		BASS_ACTIVE_STOPPED, BASS_ACTIVE_PLAYING, BASS_ACTIVE_PAUSED or
		BASS_ACTIVE_STALLED
		"""
		return bass.BASS_ChannelIsActive(self.handle)
	
	def pause(self):
		"""
		Pauses the channel
		"""
		return bass.BASS_ChannelPause(self.handle)
		
	def play(self, fromstart=False):
		"""
		Plays the channel
		Set fromstart to true to restart playback from the beginning
		"""
		return bass.BASS_ChannelPlay(self.handle, fromstart)
	
	def stop(self):
		"""
		Stops the channel
		"""
		return bass.BASS_ChannelStop(self.handle)
		