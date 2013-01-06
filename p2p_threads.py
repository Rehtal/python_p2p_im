# -*- coding: utf-8 -*-
"""p2p_threads.py

Implement the thread class we need to use.

"""
import threading
import socket
from random import randint
import msg

class P2PThread(threading.Thread):
	"""P2P thread that will be used in this im program."""
	def __init__(self, unhandled_hosts, job_event):
		"""arg:
			unhandled_hosts: a list of ip & port of destination.
			job_event: thread begin event."""

		threading.Thread.__init__(self)
		self.unhandled_hosts = unhandled_hosts
		self.job_event = job_event
		# Allocate a port for receiving.
		self.src_port = randint(49152, 65535)

	def run(self):
		"""Connect destination and communicate."""
		recv_socket = socket.socket(scoket.AF_INET, socket.SOCK_DGRAM)
		send_socket = socket.socket(scoket.AF_INET, socket.SOCK_DGRAM)
		
		recv.socket.bind(('', self.src_port))

		# Block here until new host shows up.
		self.job_event.wait()

		dest_addr = self.unhandled_hosts.pop()
		send_socket.connect(dest_addr)

		msg = msg.construct_msg(CTRL_PORT, self.src_port)
		send_socket.sent(msg)


		recv_socket.bind
