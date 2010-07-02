import wx
import string
import os
import sys

import wx.lib.mixins.listctrl  as  listmix
import Descriptor

class DescriptorDetailsList(wx.ListCtrl,
			    listmix.ListCtrlAutoWidthMixin,
			    listmix.TextEditMixin):

	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

		listmix.ListCtrlAutoWidthMixin.__init__(self)

		self.InsertColumn(0, "Name")
		self.InsertColumn(1, "Value")
		self.InsertColumn(2, "Type")
		self.InsertColumn(3, "Comment")
		self.InsertColumn(4, "Size")

		self.SetColumnWidth(0, 100)
		self.SetColumnWidth(1, 80)
		self.SetColumnWidth(2, 100)
		self.SetColumnWidth(3, 200)
		self.SetColumnWidth(4, wx.LIST_AUTOSIZE)

		listmix.TextEditMixin.__init__(self)
		self.editedElement = None

		#self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.OnItemActivated)

	def OnComboBoxLostFocus(self, event):
		if (self.comboBox != None):
			self.comboBox.Hide()
		event.Skip()

	def OnEnumSelected(self, event):
		selected = event.GetId()
		e = self.editedElement
		self.editedElement = None

		e.value = e.enumVals[selected]
		event.Skip()
		self.UpdatePanel()

	def SetStringItem(self, index, col, data):
		e = self.editedElement

		if (e and col == 1):
			mask = (1 << (e.size * 8)) - 1
			e.val = self.editedElement.convertToInt(data) & mask
			data = str(e.val)

		wx.ListCtrl.SetStringItem(self, index, col, data)

	def OpenEditor(self, col, row):
		e = self.descriptor.elements[row]
		item = self.GetItem(row, col).GetId()
		print "item %d, col %d row %d" % (item, col, row)

		# only the "value" column is editable
		if (col != 1):
			return;

		if (e.elementType == e.ELEMENT_TYPE_VARIABLE):
			listmix.TextEditMixin.OpenEditor(self, col, row)
			self.editedElement = e

		if (e.elementType == e.ELEMENT_TYPE_ENUM):
			menu = wx.Menu()

			idx = 0
			for k in e.enumKeys:
				v = e.enumVals[idx]
				if (v != k):
					title = "%s (%s)" % (k, e.dumpValueNoComma(e.convertToInt(v)))
				else:
					title = k

				item = wx.MenuItem(menu, idx, title)
				menu.AppendItem(item)
				idx += 1

			self.editedElement = e
			menu.Bind(wx.EVT_MENU, self.OnEnumSelected)
			self.PopupMenu(menu)

	def SetDescriptor(self, descriptor):
		self.descriptor = descriptor
		self.UpdatePanel()

	def UpdatePanel(self):
		self.DeleteAllItems()

		descriptor = self.descriptor

		for e in descriptor.elements:
			etype = "UNKNOWN"
			value = e.prettyPrint()

			if (e.elementType == e.ELEMENT_TYPE_CONSTANT):
				etype = "constant"
			if (e.elementType == e.ELEMENT_TYPE_VARIABLE):
				etype = "variable"
			if (e.elementType == e.ELEMENT_TYPE_ENUM):
				etype = "enumerated"
				idx = 0
				for v in e.enumVals:
					if (e.convertToInt(e.value) == e.convertToInt(v)):
						value = e.enumKeys[idx]

					idx += 1

			if (e.elementType == e.ELEMENT_TYPE_AUTO):
				etype = "automatic"
			if (e.elementType == e.ELEMENT_TYPE_LINK):
				etype = "link"

			index = self.InsertStringItem(sys.maxint, "")
			self.SetStringItem(index, 0, e.name)
			self.SetStringItem(index, 1, value)
			self.SetStringItem(index, 2, etype)
			self.SetStringItem(index, 3, e.comment)
			self.SetStringItem(index, 4, "%d" % e.size)

		self.RefreshItems(0, len(descriptor.elements))

class DescriptorDetailsPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		self.vbox = wx.BoxSizer(wx.VERTICAL)

		text = wx.StaticText(self, -1, "Descriptor details", (20, 10))
		self.vbox.Add(text, 0, wx.ALIGN_LEFT)

		self.detailsList = DescriptorDetailsList(self, wx.NewId(), style = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING)
		self.vbox.Add(self.detailsList, 1, wx.EXPAND)

		self.SetSizer(self.vbox)
		self.SetAutoLayout(True)

	def addClicked(self, event):
		self.listCtrl.strings.append("")
		self.listCtrl.ReloadStrings()

	def removeClicked(self, event):
		self.listCtrl.RemoveSelected()
		self.listCtrl.ReloadStrings()

	def SetDescriptor(self, descriptor):
		self.detailsList.SetDescriptor(descriptor)

