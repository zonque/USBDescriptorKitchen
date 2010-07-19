import wx
import copy
import wx.lib.customtreectrl as CT
import DescriptorDetailsPanel
import Template

class CustomTreeCtrl(CT.CustomTreeCtrl):
	def __init__(self, parent, descriptorDetailPanel, templates,
			 id=wx.ID_ANY, pos=wx.DefaultPosition,
			 size=wx.DefaultSize,
			 style=wx.SUNKEN_BORDER | CT.TR_HAS_BUTTONS | CT.TR_HAS_VARIABLE_ROW_HEIGHT | wx.WANTS_CHARS):

		CT.CustomTreeCtrl.__init__(self, parent, id, pos, size, style)

		self.item = None
		self.descriptorDetailPanel = descriptorDetailPanel
		self.descriptors = []
		self.templates = templates

		self.BuildTree()

		self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
		self.Bind(CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
		self.Bind(CT.EVT_TREE_END_DRAG, self.OnEndDrag)
		self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemMenu)

		descriptorDetailPanel.setDescriptorList(self)

	def OnItemMenu(self, event):
		# ignore right click other than on selection
		if self.GetSelection() != event.GetItem():
			return

		desc = self.GetPyData(event.GetItem())
		if desc:
			parentType = desc.descriptorType
		else:
			parentType = "Root"

		submenu = wx.Menu()
		menuid = 1000

		for t in self.templates:
			if parentType in t.allowedParents:
				submenu.Append(menuid, t.descriptorType)
				self.Bind(wx.EVT_MENU, self.OnAddDescriptor, id=menuid)

			menuid += 1

		menu = wx.Menu()

		if submenu.GetMenuItemCount():
			menu.AppendMenu(100, "&Add", submenu)

		menu.AppendItem(wx.MenuItem(menu, 101, "&Remove"))
		menu.Bind(wx.EVT_MENU, self.OnRemoveDescriptor, id=101)

		self.PopupMenu(menu)

	def OnAddDescriptor(self, event):
		idx = event.GetId() - 1000
		desc = copy.deepcopy(self.templates[idx])
		self.AddDescriptor(desc)

	def OnRemoveDescriptor(self, event):
		self.RemoveSelectedDescriptor()

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
		idx = 1
		for d in self.descriptors:
			if d.descriptorType == "StringDescriptor":
				s = d.getValue("bString")
				l[s] = idx
				idx += 1

		return l

	def resolveStringDescriptor(self, strid):
		if strid == 0:
			return None

		for d in self.descriptors:
			if d.descriptorType != "StringDescriptor":
				continue

			strid -= 1
			if strid == 0:
				return d.getValue("bString")

	def findDescriptorsWithField(self, field, typeConstraint = ""):
		l = {}
		for d in self.descriptors:
			if d.descriptorType[:len(typeConstraint)] == typeConstraint and d.hasField(field):
				n = d.getValue(field)
				s = None

				if d.descriptiveString:
					s = self.resolveStringDescriptor(d.getValue(d.descriptiveString))
					if s:
						s += " (%d)" % n

				if not s:
					s = str(n)

				l[s] = n

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

				if desc.descriptiveString:
					descriptive = self.resolveStringDescriptor(desc.getValue(desc.descriptiveString))
					if descriptive:
						name += " (%s)" % descriptive

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

	def RemoveAllDescriptors(self):
		self.descriptors = []
		self.BuildTree()
		self.item = None
		self.descriptorDetailPanel.SetDescriptor(None)

