# -*- coding: utf-8 -*-
"""msg.py

Define protocal of communication.

The structure of the pack is like:
	unsigned short: control type.
	string(optional): information.

"""
import struct
import os

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
CTRL_HEART_BEAT = 4
# Communicate port.
CTRL_PORT = 5
# Meaningless msg.
CTRL_INFINITE = 255

# Some necessary limits.
CONTENT_LENGTH = "512" 

def construct_msg(ctrl_hdr, info=None):
	"""Construct message."""
	# Pure control pack.
	if ctrl_hdr == CTRL_RECV or\
		ctrl_hdr == CTRL_OFF or\
		ctrl_hdr == CTRL_HEART_BEAT:
		return struct.pack("!H", ctrl_hdr) + '\n'

	# New host pack will send user name as well.
	if ctrl_hdr == CTRL_NEW_HOST:
		return struct.pack("!H"+CONTENT_LENGTH+'s', ctrl_hdr,
			os.uname()[1]) + '\n'

	# New message.
	if ctrl_hdr == CTRL_MSG:
		return struct.pack("!H"+CONTENT_LENGTH+'s', ctrl_hdr, info) + '\n'

	# Communicate port pack will send local receive port number and user name.
	if ctrl_hdr == CTRL_PORT:
		return struct.pack("!HI"+CONTENT_LENGTH+'s', ctrl_hdr, info,
			os.uname()[1]) + '\n'

def deconstruct_msg(pack):
	"""Deconstruct message."""
	ctrl_hdr = CTRL_INFINITE
	info = None
	# Remove the terminator '\n.
	pack = pack[:-1]

	# Pure control pack.
	try:
		ctrl_hdr = struct.unpack("!H", pack)
	except struct.error:
		# New message & new host pack.
		try:
			ctrl_hdr, info = struct.unpack("!H"+CONTENT_LENGTH+"s", pack)
		except struct.error:
			# Port pack.
			try:
				ctrl_hdr, info, name=struct.unpack("!HI"+CONTENT_LENGTH+'s', pack)
				info = (info, name)
			except struct.error:
				print pack.__len__()
				exit()

	return ctrl_hdr, info
