# -*- coding: utf-8 -*-
"""msg.py

Define protocal of communication.

The structure of the pack is like:
	unsigned short: control type.
	string(optional): information.

"""
import struct

# Protocal
# New host.
CTRL_NEW_HOST = 0
# Send message.
CTRL_MSG = 1
# Successfully receive a pack.
CTRL_RECV = 2
# Offline.
CTRL_OFF = 3
# Heart beat.
CRTL_HEART_BEAT = 4
# Communicate port.
CTRL_PORT = 5
# Meaningless msg.
CTRL_INFINITE = 255

# Some necessary limits.
MSG_LENGTH = 512 

def construct_msg(ctrl_hdr, info):
	"""Construct message."""
	if ctrl_hdr == CTRL_NEW_HOST or\
		ctrl_hdr == CTRL_RECV or\
		ctrl_hdr == CTRL_OFF or\
		ctrl_hdr == CTRL_HEART_BEAT:
		return struct.pack("!H", ctrl_hdr)

	if ctrl_hdr == CTRL_MSG:
		return struct.pack("!H"+MSG_LENGTH+"s", ctrl_hdr, info)

	# The number of port need to use 5 digits.
	if ctrl_hdr = CTRL_PORT:
		return struct.pack("!HI", ctrl_hdr, info)

def deconstruct_msg(pack):
	"""Deconstruct message."""
	ctrl_hdr = CTRL_INFINITE
	info = None
	try:
		ctrl_hdr = struct.unpack("!H", pack)
	except struct.error:
		try:
			ctrl_hdr, info = struct.unpack("!H"+MSG_LENGTH+"s", pack)
		except struct.error:
			ctrl_hdr, info = struct.unpack("!HI", pack)

	return ctrl_hdr, info
