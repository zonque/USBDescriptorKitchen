import wx
import string
import os
import wx.lib.colourselect as csel
import wx.lib.customtreectrl as CT
import DescriptorDetailsPanel
import Template

class CustomTreeCtrl(CT.CustomTreeCtrl):

	def __init__(self, parent, descriptorDetailPanel,
			 id=wx.ID_ANY, pos=wx.DefaultPosition,
			 size=wx.DefaultSize,
			 style=wx.SUNKEN_BORDER | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | wx.WANTS_CHARS,
			 log=None):

		CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style)

		alldata = dir(CT)

		treestyles = []
		events = []
		for data in alldata:
			if data.startswith("TR_"):
				treestyles.append(data)
			elif data.startswith("EVT_"):
				events.append(data)

		self.events = events
		self.styles = treestyles
		self.item = None
		self.descriptorDetailPanel = descriptorDetailPanel
		self.descriptors = []
		self.selectedDescriptor = None

		self.count = 0
		self.log = log

		self.BuildTree()

		self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)

	def AddDescriptor(self, newdescriptor, root=None):

		if not root:
			if self.item:
				root = self.item
			else:
				root = self.root

			if self.selectedDescriptor:
				parent = self.selectedDescriptor.children
			else:
				parent = self.descriptors

		name = newdescriptor.descriptorType
		if (newdescriptor.comment):
			name += " (%s)" % newdescriptor.comment

		item = self.AppendItem(root, name)
		self.SetPyData(item, newdescriptor)
		self.SetItemTextColour(item, wx.BLACK)
		self.Expand(root)
		self.Expand(item)

		for c in newdescriptor.children:
			self.AddDescriptor(c, item)

		parent.append(newdescriptor)

		if self.selectedDescriptor:
			self.selectedDescriptor.handleAutoFields()
			self.descriptorDetailPanel.RefreshItems()

	def BuildTree(self):
		self.DeleteAllItems()
		self.root = self.AddRoot("Root")
		self.SetItemTextColour(self.root, wx.BLACK)

		for d in self.descriptors:
			self.AddDescriptor(d, self.root)

		self.Expand(self.root)

	def BindEvents(self, choice, recreate=False):

		value = choice.GetValue()
		text = choice.GetLabel()

		evt = "CT." + text
		binder = self.eventdict[text]

		if value == 1:
			if evt == "CT.EVT_TREE_BEGIN_RDRAG":
				self.Bind(wx.EVT_RIGHT_DOWN, None)
				self.Bind(wx.EVT_RIGHT_UP, None)
			self.Bind(eval(evt), binder)
		else:
			self.Bind(eval(evt), None)
			if evt == "CT.EVT_TREE_BEGIN_RDRAG":
				self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
				self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

	def OnItemFont(self, event):

		data = wx.FontData()
		font = self.itemdict["font"]

		if font is None:
			font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

		data.SetInitialFont(font)

		dlg = wx.FontDialog(self, data)

		if dlg.ShowModal() == wx.ID_OK:
			data = dlg.GetFontData()
			font = data.GetChosenFont()
			self.SetItemFont(self.current, font)

		dlg.Destroy()


	def OnItemHyperText(self, event):

		self.SetItemHyperText(self.current, not self.itemdict["ishtml"])


	def OnEnableWindow(self, event):

		enable = self.GetItemWindowEnabled(self.current)
		self.SetItemWindowEnabled(self.current, not enable)


	def OnDisableItem(self, event):

		self.EnableItem(self.current, False)

	def OnItemInfo(self, event):

		itemtext = self.itemdict["text"]
		numchildren = str(self.itemdict["children"])
		itemtype = self.itemdict["itemtype"]
		pydata = repr(type(self.itemdict["pydata"]))

		if itemtype == 0:
			itemtype = "Normal"
		elif itemtype == 1:
			itemtype = "CheckBox"
		else:
			itemtype = "RadioButton"

		strs = "Information On Selected Item:\n\n" + "Text: " + itemtext + "\n" \
			   "Number Of Children: " + numchildren + "\n" \
			   "Item Type: " + itemtype + "\n" \
			   "Item Data Type: " + pydata + "\n"

		dlg = wx.MessageDialog(self, strs, "CustomTreeCtrlDemo Info", wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		dlg.Destroy()



	def OnItemDelete(self, event):

		strs = "Are You Sure You Want To Delete Item " + self.GetItemText(self.current) + "?"
		dlg = wx.MessageDialog(None, strs, 'Deleting Item', wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_QUESTION)

		if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
			dlg.Destroy()
			return

		dlg.Destroy()

		self.DeleteChildren(self.current)
		self.Delete(self.current)
		self.current = None



	def OnItemPrepend(self, event):

		dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

		if dlg.ShowModal() == wx.ID_OK:
			newname = dlg.GetValue()
			newitem = self.PrependItem(self.current, newname)
			self.EnsureVisible(newitem)

		dlg.Destroy()


	def OnItemAppend(self, event):

		dlg = wx.TextEntryDialog(self, "Please Enter The New Item Name", 'Item Naming', 'Python')

		if dlg.ShowModal() == wx.ID_OK:
			newname = dlg.GetValue()
			newitem = self.AppendItem(self.current, newname)
			self.EnsureVisible(newitem)

		dlg.Destroy()


	def OnBeginEdit(self, event):

		self.log.write("OnBeginEdit" + "\n")
		# show how to prevent edit...
		item = event.GetItem()
		if item and self.GetItemText(item) == "The Root Item":
			wx.Bell()
			self.log.write("You can't edit this one..." + "\n")

			# Lets just see what's visible of its children
			cookie = 0
			root = event.GetItem()
			(child, cookie) = self.GetFirstChild(root)

			while child:
				self.log.write("Child [%s] visible = %d" % (self.GetItemText(child), self.IsVisible(child)) + "\n")
				(child, cookie) = self.GetNextChild(root, cookie)

			event.Veto()


	def OnEndEdit(self, event):

		self.log.write("OnEndEdit: %s %s" %(event.IsEditCancelled(), event.GetLabel()))
		# show how to reject edit, we'll not allow any digits
		for x in event.GetLabel():
			if x in string.digits:
				self.log.write(", You can't enter digits..." + "\n")
				event.Veto()
				return

		self.log.write("\n")


	def OnLeftDClick(self, event):

		pt = event.GetPosition()
		item, flags = self.HitTest(pt)
		if item and (flags & CT.TREE_HITTEST_ONITEMLABEL):
			if self.GetTreeStyle() & CT.TR_EDIT_LABELS:
				self.log.write("OnLeftDClick: %s (manually starting label edit)"% self.GetItemText(item) + "\n")
				self.EditLabel(item)
			else:
				self.log.write("OnLeftDClick: Cannot Start Manual Editing, Missing Style TR_EDIT_LABELS\n")

		event.Skip()


	def OnSelChanged(self, event):

		for d in self.descriptors:
			d.handleAutoFields()

		self.item = event.GetItem()
		d = self.GetPyData(self.item)
		self.descriptorDetailPanel.SetDescriptor(d)

		self.selectedDescriptor = d

		event.Skip()


	def OnBeginDrag(self, event):

		self.item = event.GetItem()
		if self.item:
			self.log.write("Beginning Drag..." + "\n")

			event.Allow()


	def OnBeginRDrag(self, event):

		self.item = event.GetItem()
		if self.item:
			self.log.write("Beginning Right Drag..." + "\n")

			event.Allow()


	def OnEndDrag(self, event):

		self.item = event.GetItem()
		if self.item:
			self.log.write("Ending Drag!" + "\n")

		event.Skip()


	def OnDeleteItem(self, event):

		item = event.GetItem()

		if not item:
			return

		self.log.write("Deleting Item: %s" % self.GetItemText(item) + "\n")
		event.Skip()


	def OnItemCheck(self, event):

		item = event.GetItem()
		self.log.write("Item " + self.GetItemText(item) + " Has Been Checked!\n")
		event.Skip()


	def OnItemChecking(self, event):

		item = event.GetItem()
		self.log.write("Item " + self.GetItemText(item) + " Is Being Checked...\n")
		event.Skip()


	def OnToolTip(self, event):

		item = event.GetItem()
		if item:
			event.SetToolTip(wx.ToolTip(self.GetItemText(item)))


	def OnItemMenu(self, event):

		item = event.GetItem()
		if item:
			self.log.write("OnItemMenu: %s" % self.GetItemText(item) + "\n")

		event.Skip()

	def RemoveSelectedDescriptor(self):
		print "bla"

