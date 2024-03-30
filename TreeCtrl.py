import wx
import copy
import wx.lib.agw.customtreectrl as CT
import DescriptorDetailsPanel

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

		if newdescriptor.dependsOnDescriptor:
			found = False

			for d in parent:
				if d.descriptorType == newdescriptor.dependsOnDescriptor:
					found = True

			if not found:
				s = "Descriptor of type \"%s\" depends on \"%s\" which is non-existant." % \
					(newdescriptor.descriptorType, newdescriptor.dependsOnDescriptor)

				dlg = wx.MessageDialog(self, s, "Error adding descriptor", wx.OK | wx.ICON_ERROR)
				dlg.ShowModal()
				dlg.Destroy()
				return False

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
		newdescriptor.parentDescriptor = selectedDescriptor

		item = self.AppendItem(root, newdescriptor.getSummaryName())
		self.SetPyData(item, newdescriptor)
		self.SetItemTextColour(item, wx.BLACK)
		self.Expand(root)
		self.Expand(item)

		for c in newdescriptor.children:
			self.AddDescriptor(c, item)

		if not newdescriptor in parent:
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
			if d.descriptorType == "String":
				s = d.getValue("bString")
				l[s] = idx
				idx += 1

		return l

	def resolveStringDescriptor(self, strid):
		if strid == 0:
			return None

		for d in self.descriptors:
			if d.descriptorType != "String":
				continue

			strid -= 1
			if strid == 0:
				return d.getValue("bString")

	def findDescriptorsWithFieldRecursive(self, desc, fields, typeConstraint, descriptorList):
		matched = False

		if desc.descriptorType[:len(typeConstraint)] == typeConstraint:
			for field in fields:
				if desc.hasField(field):
					value = desc.getValue(field)
					matched = True

		if matched:
			#print("matched: %s v %d" % (desc.descriptorType, value))
			descriptorList.append((desc, value))

		for c in desc.children:
			self.findDescriptorsWithFieldRecursive(c, fields, typeConstraint, descriptorList)

		return descriptorList

	def findDescriptorsWithFields(self, fields, typeConstraint = ""):
		descriptorList = []

		for d in self.descriptors:
			self.findDescriptorsWithFieldRecursive(d, fields, typeConstraint, descriptorList)

		resultList = {}

		for (desc, value) in descriptorList:
			s = None

			if desc.descriptiveString:
				s = self.resolveStringDescriptor(desc.getValue(desc.descriptiveString))
				if s:
					s += " (%d)" % value

			if not s:
				s = str(value)

			resultList[s] = value

		return resultList

	def suggestValues(self, descriptor, element):
		resultList = {}
		valueList = []
		descriptorList = []

		# traverse up to the configuration descriptor
		configDescriptor = descriptor.iterateUp("Configuration")
		if not configDescriptor:
			print("Oops - no config descriptor?")
			return {}

		if element.suggestionType == "EndpointAddress":
			# first add all possible values
			for i in range(1, 16):
				valueList.append(i)
				valueList.append(i | 0x80)

			# and then subtract those which are already taken
			for desc in configDescriptor.children:
				self.findDescriptorsWithFieldRecursive(desc, ["bEndpointAddress"], "Endpoint", descriptorList)

		if element.suggestionType == "UAC2Unit":
			# first add all possible values
			for i in range(255):
				valueList.append(i)

			# and then subtract those which are already taken
			for desc in configDescriptor.children:
				self.findDescriptorsWithFieldRecursive(desc, ["bUnitID", "bTerminalID"], "UAC2", descriptorList)

		if element.suggestionType == "UAC2Clock":
			# first add all possible values
			for i in range(255):
				valueList.append(i)

			# and then subtract those which are already taken
			for desc in configDescriptor.children:
				self.findDescriptorsWithFieldRecursive(desc, ["bClockID"], "UAC2", descriptorList)

		if element.suggestionType == "MIDIJack":
			# first add all possible values
			for i in range(255):
				valueList.append(i)

			# and then subtract those which are already taken
			for desc in configDescriptor.children:
				self.findDescriptorsWithFieldRecursive(desc, ["bJackID"], "MIDI", descriptorList)

		for (desc, value) in descriptorList:
			if value in valueList:
				valueList.remove(value)

		for i in valueList:
			resultList[str(i)] = i

		return resultList

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
		item = self.item
		destination = event.GetItem()
		parent = item.GetParent()

		descriptor = self.GetPyData(item)
		destinationDescriptor = self.GetPyData(destination)
		parentDescriptor = self.GetPyData(parent)

		if destinationDescriptor:
			destinationType = destinationDescriptor.descriptorType
		else:
			destinationType = "Root"

		if parentDescriptor:
			parentList = parentDescriptor.children
		else:
			parentList = self.descriptors

		if destinationType in descriptor.allowedParents:
			foo = copy.deepcopy(descriptor)
			foo.debugDump()

			self.Delete(item)
			#self.item = None
			parentList.remove(descriptor)

			self.AddDescriptor(foo, destination)

		else:
			idx = 0
			for c in parentList:
				if c == destinationDescriptor:
					break
				idx += 1

			parentList.remove(descriptor)
			parentList.insert(idx, descriptor)

			self.Delete(item)
			item = self.InsertItemByIndex(parent, idx, descriptor.getSummaryName())
			self.SetPyData(item, descriptor)

			self.item = item

		event.Skip()
		return

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
