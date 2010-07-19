import wx
import string

import wx.gizmos
from wx.lib.mixins import treemixin
import Descriptor

class DescriptorDetailsList(treemixin.VirtualTree,
			    treemixin.ExpansionState,
			    wx.gizmos.TreeListCtrl):

	def __init__(self, *args, **kwargs):
		kwargs['style'] = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT

		super(DescriptorDetailsList, self).__init__(*args, **kwargs)

		self.AddColumn("Name", width=150)
		self.AddColumn("Value", width=150, edit=True)
		self.AddColumn("Type", width=50)
		self.AddColumn("Comment", width=200)
		self.AddColumn("Size", width=50)

		self.editedElement = None

		self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
		self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)

	def getPossibleLinks(self, element):
		if element.linkType == "stringIndex":
			return self.descriptorList.getStringDescriptors()

	def OnBeginLabelEdit(self, event):
		indices = self.GetIndexOfItem(event.GetItem())
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2:
			e = e.bitmap[indices[1]]

		if (e.elementType == "variable" or
		    e.elementType == "string"):
			self.editedElement = e
			return

		if e.elementType == "enum":
			items = sorted(e.enum.iteritems(), key=lambda(k,v): (v,k))

		if e.elementType == "link":
			items = self.getPossibleLinks(e).items()

		if items:
			menu = wx.Menu()

			for (k, v) in items:
				if v != k:
					title = "%s (%s)" % (k, e.dumpValueNoComma(e.convertToInt(v)))
				else:
					title = k

				# "+1" for OS X where zero values are not allowed
				item = wx.MenuItem(menu, v + 1, title)
				menu.AppendItem(item)

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

		if len(indices) == 2 and e.elementType == "bitmap":
			e = e.bitmap[indices[1]]

		if column == 0:
			return e.name

		if column == 1:
			return e.prettyPrint()

		if column == 2:
			return e.elementType

		if column == 3:
			return e.comment

		if column == 4:
			unit = "byte"
			if len(indices) == 2:
				unit = "bit"

			multiple = ""
			if e.size != 1:
				multiple = "s"

			return "%d %s%s" % (e.size, unit, multiple)

		return ""

	def OnGetChildrenCount(self, indices):
		if len(indices) == 0:
			return len(self.descriptor.elements)

		index = indices[0]
		e = self.descriptor.elements[index]

		if len(indices) == 1 and e.elementType == "bitmap":
			return len(e.bitmap)

		return 0

	def OnGetItemTextColour(self, indices):
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2 and e.elementType == "bitmap":
			e = e.bitmap[indices[1]]

		if e.elementType == "variable":
			return wx.RED

		if (e.elementType == "enum" or
		    e.elementType == "link"):
			return wx.BLUE

		return wx.BLACK

	def OnEnumSelected(self, event):
		selected = event.GetId() - 1
		e = self.editedElement
		if not e:
			return;

		e.setValue(selected)
		self.editedElement = None

		event.Skip()
		self.RefreshItems()
		self.descriptorList.UpdateSummaryNames()

	def OnAddField(self, event):
		item = self.GetSelection()
		indices = self.GetIndexOfItem(item)
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2:
			e = e.bitmap[indices[1]]

		self.descriptor.addArrayField(e)
		self.RefreshItems()

	def OnRemoveField(self, event):
		item = self.GetSelection()
		indices = self.GetIndexOfItem(item)
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2:
			e = e.bitmap[indices[1]]

		self.descriptor.removeArrayField(e)
		self.RefreshItems()

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

