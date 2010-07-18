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
			 style=wx.SUNKEN_BORDER | wx.WANTS_CHARS,
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


	def OnEndDrag(self, event):

		self.item = event.GetItem()
		if self.item:
			self.log.write("Ending Drag!" + "\n")

		event.Skip()

	def RemoveSelectedDescriptor(self):
		if not self.selectedDescriptor:
			return

		p = self.item.GetParent()
		pd = self.GetPyData(p)

		if pd:
			parent = pd.children
		else:
			parent = self.descriptors

		parent.remove(self.selectedDescriptor)
		self.Delete(self.item)
		self.selectedDescriptor = None
		self.item = None
		self.descriptorDetailPanel.SetDescriptor(None)

