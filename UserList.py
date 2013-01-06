
import wx
from MDIChat import MDIChatFrame

user_list = ['Hello', 'World', 'Simple', 'Test']

class UserListCtrl(wx.ListCtrl):
	def __init__(self, parent):
		wx.ListCtrl.__init__( self, parent, -1, 
			style=wx.LC_REPORT|wx.LC_HRULES)

		# Chat frame.
		self.mdi_chat_frame = wx.MDIParentFrame(None, size=(600, 400),
			title="Enjoy chatting!")

		# Bind events.
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)


	def OnItemSelected(self, event):
		self.currentItem = event.m_itemIndex

	def OnItemActivated(self, event):
		self.mdi_chat_frame.Show(True)

		user_name = self.GetItemText(event.m_itemIndex)

		chat_list = self.mdi_chat_frame.GetChildren()[0].GetChildren()
		chat = [frame for frame in chat_list if frame.GetName()==user_name]
		if chat.__len__():
			chat[0].Activate()
		else:
			MDIChatFrame(self.mdi_chat_frame, user_name,
				self.GetItem(event.m_itemIndex))
	
	def OnItemDeselected(self, evt):
		pass

class UserListPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.list = UserListCtrl(self)
		sizer.Add(self.list, 1, wx.ALIGN_CENTER)
		
		self.PopulateList()

		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		
	def PopulateList(self):
		self.list.InsertColumn(0, "Users", wx.LIST_FORMAT_CENTRE)

		for user in user_list:
			index = self.list.GetItemCount()
			self.list.InsertStringItem(index, user)

		self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
		
if __name__ == '__main__':
	app = wx.App(False)
	frame = wx.Frame(None, title="Rethal's P2P IM", size=(200, 500),
	pos=(50, 50))
	win = UserListPanel(frame)
	frame.Show(True)
	app.MainLoop()

