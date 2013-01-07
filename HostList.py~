
import wx
import threading
import asyncore

import Communicate
from MDIChat import MDIChatFrame

class HostListCtrl(wx.ListCtrl):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, wx.ID_ANY, 
			style=wx.LC_REPORT|wx.LC_HRULES)

		# Chat frame.
		self.mdi_chat_frame = wx.MDIParentFrame(None, size=(600, 400),
			title="Enjoy chatting!")
		
		# Chat server.
		self.server = Communicate.ChatServer(self)

		# Host info.
		self.host_list = []

		# MDIChatFrame threads pool.
		self.pool = []
		self.CreatePool()

		# Bind events.
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

	def OnItemActivated(self, event):
		self.mdi_chat_frame.Show(True)

		uid = event.m_itemIndex
		host_info = self.host_list[uid]

		chat_list = self.mdi_chat_frame.GetChildren()[0].GetChildren()
		chat = [frame for frame in chat_list if frame.GetName()==host_name]
		if chat.__len__():
			chat[0].Activate()
		else:
			frame = self.pool.pop()
			list_item = self.GetItem(uid)
			frame.Activate(self, host_info, list_item)
			# Add more available MDIChatFrame.
			if self.pool.__len__()<5:
				self.CreatePool()
	
	def CreatePool(self):
		for i in range(15):
			frame = MDIChatFrame(self.mdi_chat_frame)
			
			self.pool.append(frame)

	def AddHost(self, addr, host_info):
		"""Server get a new host."""
		print "Hello"

		# Host already exists.
		if [host for host in self.host_list if host['addr']==addr].__len__()!=0:
			return

		# New host.
		host_info['addr'] = addr
		self.host_list.append(host_info)
		name = host_info['name']
		index = self.GetItemCount()
		self.InsertStringItem(index, name)
		self.SetColumnWidth(0, wx.LIST_AUTOSIZE)

	
	def DelHost(self, addr):
		"""A host offline."""

class HostListPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.list = HostListCtrl(self)
		self.list.InsertColumn(0, "Hosts", wx.LIST_FORMAT_CENTRE)
		sizer.Add(self.list, 1, wx.ALIGN_CENTER)
		
		self.SetSizer(sizer)
		self.SetAutoLayout(True)
	

def asyncore_loop():
	asyncore.loop()

if __name__ == '__main__':
	app = wx.App(False)
	frame = wx.Frame(None, title="Rethal's P2P IM", size=(200, 500),
		pos=(50, 50))
	win = HostListPanel(frame)
	frame.Show(True)
	t = threading.Thread(target=asyncore_loop)
	t.daemon = True
	t.start()
	app.MainLoop()

