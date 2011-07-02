"""
 Python wrapper around BASS
"""
from ctypes import *
bass = windll.bass

from channels import Channel

class FileStream(Channel):
	"""
	Creates a playback channel from a file
	"""
	def __init__(self, file, from_mem=False):
		handle = bass.BASS_StreamCreateFile(from_mem, file, c_longlong(0), c_longlong(0), 0)
		Channel.__init__(self, handle)