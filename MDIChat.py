# -*- coding: utf-8 -*-
"""(filename)

(description)

"""
import wx
import time
import os


class MDIChatFrame(wx.MDIChildFrame):
	def __init__(self, parent):
		wx.MDIChildFrame.__init__(self, parent)

		# Attr for receiving new messages.
		self.new_msg_attr = wx.TextAttr('yellow')
		
		# Frames of history messages & new messages.
		self.history_msg = wx.TextCtrl(self,
			style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.new_msg = wx.TextCtrl(self,
			style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)

		# Combine.
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.history_msg, 2, wx.EXPAND)
		sizer.Add(self.new_msg, 1, wx.EXPAND)

		# Set border.
		border = wx.BoxSizer()
		border.Add(sizer, 1, wx.EXPAND|wx.ALL, 25)

		# Show.
		self.SetSizer(border)
		self.Show(False)

		# Bind.
		self.Bind(wx.EVT_TEXT_ENTER, self.OnSendMsg, self.new_msg)

	def Active(self, parent, host_info, list_item):
		"""Two-step construction."""
		host_name = host_info['name']
		self.Create(parent, title=host_name, name=host_name)
		self.list_item = list_item

		# Chat session.
		host_addr = host_info['addr']
		src_port = host_info['src_port']
		self.chat_session = Communicate.ChatSession(host_addr,
			src_port, self)

		self.Show(True)

	def OnSendMsg(self, event):
		"""Send new message."""
		# Send message.
		msg = event.GetString() + '\n'
		self.chat_session.new_msg(msg)

		# Flush local history.
		full_msg = u"Me" + u': '\
			+ time.strftime("%Y-%m-%d %X",
			time.localtime()).decode('utf8')\
			+ u'\n' + msg + u'\n'
		self.history_msg.AppendText(msg)
		self.new_msg.Clear()

	def OnRecvMsg(self, event):
		"""Receive new message."""
		# Get message from event.
		msg = event.GetString()
		if self.IsShownOnSceen()==False:
			self.list_item.SetBackgroundColour('yellow')
			begin = self.history_msg.GetLastPosition()
			self.history_msg.AppendText(msg)
			end = self.history_msg.GetLastPosition()
			self.history_msg.SetStyle(begin, end, self.new_msg_attr)
		else:
			self.history_msg.AppendText(msg)

if __name__ == '__main__':
	class MyApp(wx.App):
		def OnInit(self):
			wx.InitAllImageHandlers()
			parent = wx.MDIParentFrame(None, size=(600, 400))
			MDIChatFrame(parent, 'Hello')
			MDIChatFrame(parent, 'World')
			parent.Show(True)
			self.SetTopWindow(parent)
			return True

	app = MyApp(False)
	app.MainLoop()
	asyncore.loop()
