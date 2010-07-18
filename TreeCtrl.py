import wx
import copy
import wx.lib.customtreectrl as CT
import DescriptorDetailsPanel
import Template

class CustomTreeCtrl(CT.CustomTreeCtrl):
	def __init__(self, parent, descriptorDetailPanel,
			 id=wx.ID_ANY, pos=wx.DefaultPosition,
			 size=wx.DefaultSize,
			 style=wx.SUNKEN_BORDER | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | wx.WANTS_CHARS):

		CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style)

		self.item = None
		self.descriptorDetailPanel = descriptorDetailPanel
		self.descriptors = []

		self.BuildTree()

		self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
		self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
		self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)

		descriptorDetailPanel.setDescriptorList(self)

	def AddDescriptor(self, newdescriptor, root=None):
		if not root:
			if self.item:
				root = self.item
			else:
				root = self.root

		selectedDescriptor = self.GetPyData(root)

		if selectedDescriptor:
			parent = selectedDescriptor.children
			parentType = selectedDescriptor.descriptorType
		else:
			parent = self.descriptors
			parentType = "Root"

		if not parentType in newdescriptor.allowedParents:
			s = "Illegal parent \"%s\" for descriptor of type \"%s\". " % (parentType, newdescriptor.descriptorType)
			s += "Allowed parent types are:\n\n"
			for a in newdescriptor.allowedParents:
				s += "\"" + a + "\"\n"

			dlg = wx.MessageDialog(self, s, "Error adding descriptor", wx.OK | wx.ICON_ERROR)
			dlg.ShowModal()
			dlg.Destroy()
			return False

		newdescriptor.setParentList(parent)
		item = self.AppendItem(root, newdescriptor.getSummaryName())
		self.SetPyData(item, newdescriptor)
		self.SetItemTextColour(item, wx.BLACK)
		self.Expand(root)
		self.Expand(item)

		for c in newdescriptor.children:
			print "child ..."
			self.AddDescriptor(c, item)

		parent.append(newdescriptor)

		if selectedDescriptor:
			selectedDescriptor.handleAutoFields()
			self.descriptorDetailPanel.RefreshItems()

		self.UpdateSummaryNames()
		return True

	def getStringDescriptors(self):
		l = {}
		idx = 0
		for d in self.descriptors:
			if d.descriptorType == "StringDescriptor":
				s = d.getValue("bString")
				l[s] = idx
				idx += 1

		return l

	def BuildTree(self):
		self.DeleteAllItems()
		self.root = self.AddRoot("Root")
		self.SetItemTextColour(self.root, wx.BLACK)

		for d in self.descriptors:
			self.AddDescriptor(d, self.root)

		self.Expand(self.root)

	def UpdateSummaryNames(self):
		item = self.GetRootItem()

		while item:
			desc = self.GetPyData(item)

			if desc:
				desc.handleAutoFields()
				name = desc.getSummaryName()
				self.SetItemText(item, name)

			item = self.GetNext(item)

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

		event.Skip()


	def OnBeginDrag(self, event):
		self.item = event.GetItem()
		if self.item:
			event.Allow()

	def OnEndDrag(self, event):
		newroot = event.GetItem()

		descriptor = self.GetPyData(self.item)

		oldParent = self.item.GetParent()
		oldParentDescriptor = self.GetPyData(oldParent)

		newParentDescriptor = self.GetPyData(newroot)

		if self.AddDescriptor(copy.deepcopy(descriptor), newroot):
			if oldParentDescriptor:
				oldParentDescriptor.children.remove(descriptor)
			else:
				self.descriptors.remove(descriptor)

			self.Delete(self.item)
			self.item = None

		event.Skip()

	def RemoveSelectedDescriptor(self):
		if not self.item:
			return

		selectedDescriptor = self.GetPyData(self.item)

		p = self.item.GetParent()
		pd = self.GetPyData(p)

		if pd:
			parent = pd.children
		else:
			parent = self.descriptors

		parent.remove(selectedDescriptor)
		self.Delete(self.item)
		self.item = None
		self.descriptorDetailPanel.SetDescriptor(None)

