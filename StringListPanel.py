import wx
import string
import os
import sys

import wx.lib.mixins.listctrl  as  listmix

class StringListCtrl(wx.ListCtrl,
		     listmix.ListCtrlAutoWidthMixin,
		     listmix.TextEditMixin):

	strings = []

	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

		listmix.ListCtrlAutoWidthMixin.__init__(self)
		self.Populate()
		self.ReloadStrings()
		listmix.TextEditMixin.__init__(self)

	def Populate(self):
		self.InsertColumn(0, "ID")
		self.InsertColumn(1, "String")

		self.SetColumnWidth(0, 20)
		self.SetColumnWidth(1, wx.LIST_AUTOSIZE)

	def ReloadStrings(self):
		self.DeleteAllItems()

		for s in self.strings:
			index = self.InsertStringItem(sys.maxint, "")
			self.SetStringItem(index, 0, "%d" % index)
			self.SetStringItem(index, 1, s)
			self.SetItemData(index, index)

		self.RefreshItems(0, len(self.strings))

	def RemoveSelected(self):
		item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

		if (item > 0):
			self.strings.pop(item)

	def SetStringItem(self, index, col, data):
		if (col == 1):
			self.strings[index] = data

		wx.ListCtrl.SetStringItem(self, index, col, data)

	def OpenEditor(self, col, row):
		if (col == 1):
			listmix.TextEditMixin.OpenEditor(self, col, row)

class StringListPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.vbox = wx.BoxSizer(wx.VERTICAL)

		text = wx.StaticText(self, -1, "String descriptors", (20, 10))
		self.vbox.Add(text, 0, wx.ALIGN_LEFT)

		self.listCtrl = StringListCtrl(self, wx.NewId(), style = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
		self.vbox.Add(self.listCtrl, 1, wx.EXPAND)


		self.hbox = wx.BoxSizer(wx.HORIZONTAL)

		addButton = wx.Button(self, 10, "Add", (20, 20))
		addButton.SetSize(addButton.GetBestSize())
		addButton.Bind(wx.EVT_BUTTON, self.addClicked, addButton)

		removeButton = wx.Button(self, 10, "Remove", (20, 20))
		removeButton.SetSize(removeButton.GetBestSize())
		removeButton.Bind(wx.EVT_BUTTON, self.removeClicked, removeButton)

		self.hbox.Add(addButton, 0, wx.ALL, 10)
		self.hbox.Add(removeButton, 0, wx.ALL, 10)
		self.vbox.Add(self.hbox)

		self.SetSizer(self.vbox)
		self.SetAutoLayout(True)

	def addClicked(self, event):
		self.listCtrl.strings.append("")
		self.listCtrl.ReloadStrings()

	def removeClicked(self, event):
		self.listCtrl.RemoveSelected()
		self.listCtrl.ReloadStrings()

