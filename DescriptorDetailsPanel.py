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
		index = self.GetIndexOfItem(event.GetItem())[0]

		e = self.descriptor.elements[index]
		#item = self.GetItem(row, col).GetId()
		#print "item %d, col %d row %d" % (item, col, row)

		if (e.elementType == e.ELEMENT_TYPE_VARIABLE):
			self.editedElement = e
			return

		if (e.elementType == e.ELEMENT_TYPE_ENUM):
			menu = wx.Menu()

			print e

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

		event.Veto()

	def OnEndLabelEdit(self, event):
		e = self.editedElement

		if e:
			mask = (1 << (e.size * 8)) - 1
			e.value = e.convertToInt(event.GetLabel()) & mask

		self.RefreshItems()

	def OnGetItemText(self, indices, column=0):
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2 and e.elementType == e.ELEMENT_TYPE_BITMAP:
			e = e.bitmap[indices[1]]

		if column == 0:
			return e.name

		if column == 1:
			value = e.prettyPrint()

			if (e.elementType == e.ELEMENT_TYPE_ENUM):
				idx = 0
				for v in e.enumVals:
					if (e.convertToInt(e.value) == e.convertToInt(v)):
						value = e.enumKeys[idx]

					idx += 1
			return value

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
		return wx.BLACK

	def OnEnumSelected(self, event):
		selected = event.GetId()
		e = self.editedElement
		self.editedElement = None

		e.value = e.enumVals[selected]
		event.Skip()
		self.RefreshItems()

	def SetDescriptor(self, descriptor):
		self.descriptor = descriptor
		self.RefreshItems()

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
