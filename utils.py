"""
 Python wrapper around BASS
 
 Bunch of useful utilities
"""

from ctypes import c_short

def hiword(num):
	"""
	Assuming num is a double word
	then this returns the high word
	For example:
	33818369 is 
	0000 0010 0000 0100 0000 0111 0000 0001
	where each group is a nibble
	A word is 2 bytes so the hiword of this
	will be:
	0000 0010 0000 0100
	which is 516 (as any fule kno)
	"""
	return int(num >> 16)

def loword(num):
	"""
	Assuming num is a double world
	then this returns the low word
	For example:
	33818369 is 
	0000 0010 0000 0100 0000 0111 0000 0001
	where each group is a nibble
	A word is 2 bytes so the loword of this
	will be:
	0000 0111 0000 0001
	which is 1793 (innit)
	"""
	# This is equivalent of doing (short)num
	# or (int16_t)num
	return c_short(num).value