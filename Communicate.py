# -*- coding: utf-8 -*-
"""(filename)

(description)

"""
import wx
import asynchat
import asyncore
import socket

import MsgStruct
import MDIChat


class ChatSession(asynchat.async_chat):
	def __init__(self, dest_addr, src_port, win):
		asynchat.async_chat.__init__(self)
		# Prepare socket and use UDP.
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.connect(dest_addr)
		self.bind(('', src_port))

		self.win = win
		self.set_terminator('\n')
		
		# Set buffers.
		self.ibuf = ""
		self.obuf = ""

	def writeable(self):
		return bool(self.obuf.__len__())

	def handle_write(self):
		sent = self.send(self.obuf)
		self.obuf = self.obuf[sent:]
	
	def collect_incoming_data(self, data):
		self.ibuf += data

	def found_terminator(self):
		# New message.
		ctrl_hdr, info = MsgStruct.deconstruct_msg(self.ibuf)
		if ctrl_hdr==MsgStruct.CTRL_INFINITE:
			pass
		elif ctrl_hdr==MsgStruct.CTRL_RECV:
			# Set new timer.
			pass
		elif ctrl_hdr==MsgStruct.CTRL_MSG:
			event = wx.CommandEvent()
			event.SetString(info)
			self.win.OnRecvMsg(event)
	
	def new_msg(self, msg):
		msg = MsgStruct.construct_msg(MsgStruct.CTRL_MSG, msg)
		self.obuf += msg
	
class ChatServer(asyncore.dispatcher):
	def __init__(self, win):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		# Begin port.
		self.curr_port = 60000

		# HostListCtrl.
		self.win = win

		# Bind socket.
		self.set_reuse_addr()
		self.bind(('', 38000))

		# Broadcast new host message ASAP.
		self.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		msg = MsgStruct.construct_msg(MsgStruct.CTRL_NEW_HOST)
		self.sendto(msg, ("255.255.255.255", 38000))

		# Buffers.
		self.ibuf = ""
		self.obuf = {}
		
		# Details about "unconnected" hosts.
		self.busy_hosts = {}

		# All chat sessions.
		self.chat_sessions = []
	
	def writeable(self):
		return bool(self.obuf.__len__())

	def handle_write(self):
		for addr, obuf in self.obuf.items():
			if obuf!="":
				sent = self.sendto(obuf, addr)
				obuf = obuf[sent:]

	def handle_read(self):
		self.ibuf, addr = self.recvfrom(int(MsgStruct.CONTENT_LENGTH)*2)
	
		# Check message type.
		ctrl_hdr, info = MsgStruct.deconstruct_msg(self.ibuf)
		if ctrl_hdr==MsgStruct.CTRL_NEW_HOST:
			self.send_port(addr, info)
		elif ctrl_hdr==MsgStruct.CTRL_PORT:
			self.recv_port(addr, info)
		elif ctrl_hdr==MsgStruct.CTRL_RECV:
			pass
		elif ctrl_hdr==MsgStruct.CTRL_OFF:
			pass
		elif ctrl_hdr==MsgStruct.CTRL_HEART_BEAT:
			pass
		elif ctrl_hdr==MsgStruct.CTRL_INFINITE:
			pass
	
	def send_port(self, addr, dest_name=None):
		
		# Init out buffer.
		if addr not in self.obuf.keys():
			self.obuf[addr] = ""

		# Send message first.
		port = self.curr_port
		self.curr_port -= 1

		msg = MsgStruct.construct_msg(MsgStruct.CTRL_PORT, port)
		self.obuf[addr] += msg

		# Consider whether to establish a session.
		# Receive new host, just record.
		if addr not in self.busy_hosts.keys():
			self.busy_hosts[addr] = {'name':dest_name.strip('\0')}
			self.busy_hosts[addr]['src_port'] = port

		# I'm new host and is able to set up a session.
		else:
			print "Hello"
			self.busy_hosts[addr]['src_port'] = port
			dest_addr = (addr[0], self.busy_hosts[addr]['dest_port'])
			self.win.AddHost(dest_addr, self.busy_hosts[addr])

			# This host is "connected".
			# Delete it from the "unconnected" dict.
			del self.busy_hosts[addr]
	
	def recv_port(self, addr, port_and_name):

		# I'm new host and should send my local port.
		if addr not in self.busy_hosts.keys():
			self.busy_hosts[addr] = {
				'dest_port': port_and_name[0],
				'name': port_and_name[1].strip('\0')}
			self.send_port(addr)

		# Receive new host.
		else:
			self.busy_hosts[addr]['dest_port'] = port_and_name[0]
			dest_addr = (addr[0], port_and_name[0])
			self.win.AddHost(dest_addr, self.busy_hosts[addr])

			# This host is "connected".
			# Delete it from the "unconnected" dict.
			del self.busy_hosts[addr]


if __name__ == "__main__":
	a = ChatServer()
	asyncore.loop()
