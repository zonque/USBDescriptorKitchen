import wx
import string
import os
import sys

import wx.gizmos
import wx.lib.mixins.listctrl  as  listmix
from wx.lib.mixins import treemixin
import Descriptor

class DescriptorDetailsList(treemixin.VirtualTree,
			    treemixin.ExpansionState,
			    wx.gizmos.TreeListCtrl):

	def __init__(self, *args, **kwargs):
		kwargs['style'] = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT

		super(DescriptorDetailsList, self).__init__(*args, **kwargs)

		self.AddColumn("Name", width=150)
		self.AddColumn("Value", width=80, edit=True)
		self.AddColumn("Type", width=100)
		self.AddColumn("Comment", width=200)
		self.AddColumn("Size")

		self.editedElement = None

		self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
		self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)

	def OnBeginLabelEdit(self, event):
		indices = self.GetIndexOfItem(event.GetItem())
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2:
			e = e.bitmap[indices[1]]

		if (e.elementType == e.ELEMENT_TYPE_VARIABLE or
		    e.elementType == e.ELEMENT_TYPE_STRING):
			self.editedElement = e
			return

		if (e.elementType == e.ELEMENT_TYPE_ENUM):
			menu = wx.Menu()

			idx = 0
			for (k, v) in e.enum.items():
				if (v != k):
					title = "%s (%s)" % (k, e.dumpValueNoComma(e.convertToInt(v)))
				else:
					title = k

				item = wx.MenuItem(menu, idx + 1, title)
				menu.AppendItem(item)
				idx += 1

			self.editedElement = e
			menu.Bind(wx.EVT_MENU, self.OnEnumSelected)
			self.PopupMenu(menu)

		event.Veto()

	def OnEndLabelEdit(self, event):
		e = self.editedElement
		e.setValue(event.GetLabel())
		self.descriptor.handleAutoFields()
		self.RefreshItems()
		self.descriptorList.UpdateSummaryNames()

	def OnGetItemText(self, indices, column=0):
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2 and e.elementType == e.ELEMENT_TYPE_BITMAP:
			e = e.bitmap[indices[1]]

		if column == 0:
			return e.name

		if column == 1:
			return e.prettyPrint()

		if column == 2:
			etype = "UNKNOWN"

			if e.elementType == e.ELEMENT_TYPE_AUTO:
				etype = "automatic"
			if e.elementType == e.ELEMENT_TYPE_LINK:
				etype = "link"
			if e.elementType == e.ELEMENT_TYPE_CONSTANT:
				etype = "constant"
			if e.elementType == e.ELEMENT_TYPE_VARIABLE:
				etype = "variable"
			if e.elementType == e.ELEMENT_TYPE_ENUM:
				etype = "enumerated"
			if e.elementType == e.ELEMENT_TYPE_BITMAP:
				etype = "bitmap"
			if e.elementType == e.ELEMENT_TYPE_STRING:
				etype = "string"

			return etype

		if column == 3:
			return e.comment

		if column == 4:
			unit = "byte"
			if len(indices) == 2:
				unit = "bit"

			multiple = ""
			if (e.size != 1):
				multiple = "s"

			return "%d %s%s" % (e.size, unit, multiple)

		return ""

	def OnGetChildrenCount(self, indices):
		if len(indices) == 0:
			return len(self.descriptor.elements)

		index = indices[0]
		e = self.descriptor.elements[index]

		if len(indices) == 1 and e.elementType == e.ELEMENT_TYPE_BITMAP:
			return len(e.bitmap)

		return 0

	def OnGetItemTextColour(self, indices):
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2 and e.elementType == e.ELEMENT_TYPE_BITMAP:
			e = e.bitmap[indices[1]]

		if e.elementType == e.ELEMENT_TYPE_VARIABLE:
			return wx.RED

		if (e.elementType == e.ELEMENT_TYPE_ENUM) or \
		   (e.elementType == e.ELEMENT_TYPE_LINK):
			return wx.BLUE

		return wx.BLACK

	def OnEnumSelected(self, event):
		selected = event.GetId() - 1
		e = self.editedElement
		if not e:
			return;

		e.setValue(e.enum.values()[selected])
		self.editedElement = None

		event.Skip()
		self.RefreshItems()
		self.descriptorList.UpdateSummaryNames()

	def SetDescriptor(self, descriptor):
		self.descriptor = descriptor

		if descriptor:
			self.RefreshItems()
		else:
			self.DeleteAllItems()

	def setDescriptorList(self, l):
		self.descriptorList = l

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

	def RefreshItems(self):
		self.detailsList.RefreshItems()

	def setDescriptorList(self, l):
		self.detailsList.setDescriptorList(l)

