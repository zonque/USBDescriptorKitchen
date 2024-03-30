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
		self.descriptor = None

		self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginLabelEdit)
		self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndLabelEdit)
		self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemMenu)

	def getElement(self, indices):
		e = self.descriptor.elements[indices[0]]

		if len(indices) == 2 and e.elementType == "bitmap":
			e = e.bitmap[indices[1]]

		return e	

	def createMenu(self, element, items):
		menu = wx.Menu()
		for (k, v) in sorted(items, key=lambda kv: (kv[0], kv[1])):

			if v != k:
				title = "%s (%s)" % (k, element.dumpValueNoComma(element.convertToInt(v)))
			else:
				title = k

			# "+1" for OS X where zero values are not allowed
			item = wx.MenuItem(menu, v + 1, title)
			menu.AppendItem(item)

		menu.Bind(wx.EVT_MENU, self.OnEnumSelected)
		return menu

	def OnItemMenu(self, event):
		# ignore right click other than on selection
		if self.GetSelection() != event.GetItem():
			return

		indices = self.GetIndexOfItem(event.GetItem())
		e = self.getElement(indices)

		if e.createdByArray:
			menu = wx.Menu()
			menu.AppendItem(wx.MenuItem(menu, 100, "&Add field"))
			menu.AppendItem(wx.MenuItem(menu, 101, "&Remove field"))

			menu.Bind(wx.EVT_MENU, self.OnAddField, id=100)
			menu.Bind(wx.EVT_MENU, self.OnRemoveField, id=101)

			self.PopupMenu(menu)

		if e.suggestionType:
			suggestions = self.getSuggestions(e)
			submenu = self.createMenu(e, suggestions.items())
			self.editedElement = e

			if submenu.GetMenuItemCount():
				menu = wx.Menu()
				menu.AppendMenu(100, "&Suggestions", submenu)
				self.PopupMenu(menu)

	def getPossibleLinks(self, element):
		if element.linkType == "stringIndex":
			return self.descriptorList.getStringDescriptors()

		if element.linkType == "UAC2Unit":
			return self.descriptorList.findDescriptorsWithFields(["bUnitID", "bTerminalID"], "UAC2")

		if element.linkType == "UAC2Clock":
			return self.descriptorList.findDescriptorsWithFields(["bClockID"], "UAC2")

		if element.linkType == "MIDIID":
			return self.descriptorList.findDescriptorsWithFields(["bJackID"], "MIDI")

		print("Missing implementation for link type %s" % element.linkType)

	def getSuggestions(self, element):
		return self.descriptorList.suggestValues(self.descriptor, element)

	def OnBeginLabelEdit(self, event):
		indices = self.GetIndexOfItem(event.GetItem())
		e = self.getElement(indices)

		if (e.elementType == "variable" or
		    e.elementType == "string"):
			self.editedElement = e
			return

		items = None

		if e.elementType == "enum":
			items = e.enum.iteritems()

		if e.elementType == "link":
			p = self.getPossibleLinks(e)

			if not p:
				print("No possible links for type %s" % e.linkType)
				event.Veto()
				return

			items = p.items()

		if items:
			menu = self.createMenu(e, items)
			self.editedElement = e
			self.PopupMenu(menu)

		event.Veto()

	def OnEndLabelEdit(self, event):
		e = self.editedElement
		e.setValue(event.GetLabel())
		self.descriptor.handleAutoFields()
		self.RefreshItems()
		self.descriptorList.UpdateSummaryNames()

	def OnGetItemText(self, indices, column=0):
		e = self.getElement(indices)

		if column == 0:
			return e.name

		if column == 1:
			return e.prettyPrint()

		if column == 2:
			t = e.elementType
			if e.createdByArray:
				t += "[]"
			return t

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
			if (self.descriptor):
				return len(self.descriptor.elements)
			else:
				return 0

		index = indices[0]
		e = self.descriptor.elements[index]

		if len(indices) == 1 and e.elementType == "bitmap":
			return len(e.bitmap)

		return 0

	def OnGetItemTextColour(self, indices):
		e = self.getElement(indices)

		if (e.elementType == "variable" or
		    e.elementType == "string"):
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
		e.updateBitmap()
		self.editedElement = None

		event.Skip()
		self.RefreshItems()
		self.descriptorList.UpdateSummaryNames()

	def OnAddField(self, event):
		item = self.GetSelection()
		indices = self.GetIndexOfItem(item)
		e = self.getElement(indices)
		self.descriptor.addArrayField(e)
		self.RefreshItems()

	def OnRemoveField(self, event):
		item = self.GetSelection()
		indices = self.GetIndexOfItem(item)
		e = self.getElement(indices)
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

