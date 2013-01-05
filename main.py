# -*- coding: utf-8 -*-
"""main.py

This program implement a instant messenger using p2p.

Only those computers that belong to the same LAN can communicate with
each other. To set up a server can solve this limitation.

"""
import socket

class P2PIM():
	"""A simple instant messenger using p2p technique."""
	def __init__(self):
		self.threads_pool = []
		self.hosts = []
	
	def _create_threads_pool(num):
		"""Create threads pool.
		arg:
			num: the number of threads that we need to create."""
		for i in range

def create_threads_pool()
