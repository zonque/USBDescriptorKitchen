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

		self.count = 0
		self.log = log

		# NOTE:  For some reason tree items have to have a data object in
		#		order to be sorted.  Since our compare just uses the labels
		#		we don't need any real data, so we'll just use None below for
		#		the item data.

		self.BuildTree()

#
#		if not(self.GetTreeStyle() & CT.TR_HIDE_ROOT):
#			self.SetPyData(self.root, None)
#			self.SetItemImage(self.root, 24, CT.TreeItemIcon_Normal)
#			self.SetItemImage(self.root, 13, CT.TreeItemIcon_Expanded)
#
#		textctrl = wx.TextCtrl(self, -1, "I Am A Simple\nMultiline wx.TexCtrl", style=wx.TE_MULTILINE)
#		self.gauge = wx.Gauge(self, -1, 50, style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
#		self.gauge.SetValue(0)
#		combobox = wx.ComboBox(self, -1, choices=["That", "Was", "A", "Nice", "Holyday!"], style=wx.CB_READONLY|wx.CB_DROPDOWN)
#
#		textctrl.Bind(wx.EVT_CHAR, self.OnTextCtrl)
#		combobox.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
#
#		for x in range(15):
#			if x == 1:
#				child = self.AppendItem(self.root, "Item %d" % x + "\nHello World\nHappy wxPython-ing!")
#				self.SetItemBold(child, True)
#			else:
#				child = self.AppendItem(self.root, "Item %d" % x)G
#			self.SetPyData(child, None)
#			self.SetItemImage(child, 24, CT.TreeItemIcon_Normal)
#			self.SetItemImage(child, 13, CT.TreeItemIcon_Expanded)
#			self.SetItemTextColour(child, wx.BLACK)
#
#			for y in range(5):
#				if y == 0 and x == 1:
#					last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2, wnd=self.gauge)
#				elif y == 1 and x == 2:
#					last = self.AppendItem(child, "Item %d-%s" % (x, chr(ord("a")+y)), ct_type=1, wnd=textctrl)
#				elif 2 < y < 4:
#					last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
#				elif y == 4 and x == 1:
#					last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), wnd=combobox)
#				else:
#					last = self.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)), ct_type=2)
#
#				self.SetPyData(last, None)
#				self.SetItemImage(last, 24, CT.TreeItemIcon_Normal)
#				self.SetItemImage(last, 13, CT.TreeItemIcon_Expanded)
#
#				for z in range(5):
#					if z > 2:
#						item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=1)
#					elif 0 < z <= 2:
#						item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z), ct_type=2)
#					elif z == 0:
#						item = self.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
#						self.SetItemHyperText(item, True)
#					self.SetPyData(item, None)
#
#		self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
#
#		self.eventdict = {'EVT_TREE_BEGIN_DRAG': self.OnBeginDrag, 'EVT_TREE_BEGIN_LABEL_EDIT': self.OnBeginEdit,
#						  'EVT_TREE_BEGIN_RDRAG': self.OnBeginRDrag, 'EVT_TREE_DELETE_ITEM': self.OnDeleteItem,
#						  'EVT_TREE_END_DRAG': self.OnEndDrag, 'EVT_TREE_END_LABEL_EDIT': self.OnEndEdit,
#						  'EVT_TREE_ITEM_ACTIVATED': self.OnActivate, 'EVT_TREE_ITEM_CHECKED': self.OnItemCheck,
#						  'EVT_TREE_ITEM_CHECKING': self.OnItemChecking, 'EVT_TREE_ITEM_COLLAPSED': self.OnItemCollapsed,
#						  'EVT_TREE_ITEM_COLLAPSING': self.OnItemCollapsing, 'EVT_TREE_ITEM_EXPANDED': self.OnItemExpanded,
#						  'EVT_TREE_ITEM_EXPANDING': self.OnItemExpanding, 'EVT_TREE_ITEM_GETTOOLTIP': self.OnToolTip,
#						  'EVT_TREE_ITEM_MENU': self.OnItemMenu, 'EVT_TREE_ITEM_RIGHT_CLICK': self.OnRightDown,
#						  'EVT_TREE_KEY_DOWN': self.OnKey, 'EVT_TREE_SEL_CHANGED': self.OnSelChanged,
#						  'EVT_TREE_SEL_CHANGING': self.OnSelChanging, "EVT_TREE_ITEM_HYPERLINK": self.OnHyperLink}
#
#		mainframe = wx.GetTopLevelParent(self)
#
#		if not hasattr(mainframe, "leftpanel"):

#		self.Bind(CT.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
#		self.Bind(CT.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
		self.Bind(CT.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
#		self.Bind(CT.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
#		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
#		self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


#		else:
#			for combos in mainframe.treeevents:
#				self.BindEvents(combos)

#
#		if hasattr(mainframe, "leftpanel"):
#			self.ChangeStyle(mainframe.treestyles)
#
#		if not(self.GetTreeStyle() & CT.TR_HIDE_ROOT):
#			self.SelectItem(self.root)
#			self.Expand(self.root)
#

	def AddDescriptor(self, root, descriptor):
		name = descriptor.descriptorType
		if (descriptor.comment):
			name += " (%s)" % descriptor.comment

		item = self.AppendItem(root, name)
		self.SetPyData(item, descriptor)
		self.SetItemTextColour(item, wx.BLACK)
		self.Expand(root)
		self.Expand(item)

		for c in descriptor.children:
			self.AddDescriptor(item, c)

	def BuildTree(self):
		self.DeleteAllItems()
		self.root = self.AddRoot("Root")
		self.SetItemTextColour(self.root, wx.BLACK)

		for d in self.descriptors:
			self.AddDescriptor(self.root, d)

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


	def OnCompareItems(self, item1, item2):

		t1 = self.GetItemText(item1)
		t2 = self.GetItemText(item2)

		self.log.write('compare: ' + t1 + ' <> ' + t2 + "\n")

		if t1 < t2:
			return -1
		if t1 == t2:
			return 0

		return 1


	def OnRightDown(self, event):

		pt = event.GetPosition()
		item, flags = self.HitTest(pt)

		if item:
			self.item = item
			self.log.write("OnRightClick: %s, %s, %s" % (self.GetItemText(item), type(item), item.__class__) + "\n")
			self.SelectItem(item)


	def OnRightUp(self, event):

		item = self.item

		if not item:
			event.Skip()
			return

		if not self.IsItemEnabled(item):
			event.Skip()
			return

		# Item Text Appearance
		ishtml = self.IsItemHyperText(item)
		back = self.GetItemBackgroundColour(item)
		fore = self.GetItemTextColour(item)
		isbold = self.IsBold(item)
		font = self.GetItemFont(item)

		# Icons On Item
		normal = self.GetItemImage(item, CT.TreeItemIcon_Normal)
		selected = self.GetItemImage(item, CT.TreeItemIcon_Selected)
		expanded = self.GetItemImage(item, CT.TreeItemIcon_Expanded)
		selexp = self.GetItemImage(item, CT.TreeItemIcon_SelectedExpanded)

		# Enabling/Disabling Windows Associated To An Item
		haswin = self.GetItemWindow(item)

		# Enabling/Disabling Items
		enabled = self.IsItemEnabled(item)

		# Generic Item's Info
		children = self.GetChildrenCount(item)
		itemtype = self.GetItemType(item)
		text = self.GetItemText(item)
		pydata = self.GetPyData(item)

		self.current = item
		self.itemdict = {"ishtml": ishtml, "back": back, "fore": fore, "isbold": isbold,
						 "font": font, "normal": normal, "selected": selected, "expanded": expanded,
						 "selexp": selexp, "haswin": haswin, "children": children,
						 "itemtype": itemtype, "text": text, "pydata": pydata, "enabled": enabled}

		menu = wx.Menu()

		item1 = menu.Append(wx.ID_ANY, "Change Item Background Colour")
		item2 = menu.Append(wx.ID_ANY, "Modify Item Text Colour")
		menu.AppendSeparator()
		if isbold:
			strs = "Make Item Text Not Bold"
		else:
			strs = "Make Item Text Bold"
		item3 = menu.Append(wx.ID_ANY, strs)
		item4 = menu.Append(wx.ID_ANY, "Change Item Font")
		menu.AppendSeparator()
		if ishtml:
			strs = "Set Item As Non-Hyperlink"
		else:
			strs = "Set Item As Hyperlink"
		item5 = menu.Append(wx.ID_ANY, strs)
		menu.AppendSeparator()
		if haswin:
			enabled = self.GetItemWindowEnabled(item)
			if enabled:
				strs = "Disable Associated Widget"
			else:
				strs = "Enable Associated Widget"
		else:
			strs = "Enable Associated Widget"
		item6 = menu.Append(wx.ID_ANY, strs)

		if not haswin:
			item6.Enable(False)

		item7 = menu.Append(wx.ID_ANY, "Disable Item")

		menu.AppendSeparator()
		item8 = menu.Append(wx.ID_ANY, "Change Item Icons")
		menu.AppendSeparator()
		item9 = menu.Append(wx.ID_ANY, "Get Other Information For This Item")
		menu.AppendSeparator()

		item10 = menu.Append(wx.ID_ANY, "Delete Item")
		if item == self.GetRootItem():
			item10.Enable(False)
		item11 = menu.Append(wx.ID_ANY, "Prepend An Item")
		item12 = menu.Append(wx.ID_ANY, "Append An Item")

		self.Bind(wx.EVT_MENU, self.OnItemBackground, item1)
		self.Bind(wx.EVT_MENU, self.OnItemForeground, item2)
		self.Bind(wx.EVT_MENU, self.OnItemBold, item3)
		self.Bind(wx.EVT_MENU, self.OnItemFont, item4)
		self.Bind(wx.EVT_MENU, self.OnItemHyperText, item5)
		self.Bind(wx.EVT_MENU, self.OnEnableWindow, item6)
		self.Bind(wx.EVT_MENU, self.OnDisableItem, item7)
		self.Bind(wx.EVT_MENU, self.OnItemIcons, item8)
		self.Bind(wx.EVT_MENU, self.OnItemInfo, item9)
		self.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
		self.Bind(wx.EVT_MENU, self.OnItemPrepend, item11)
		self.Bind(wx.EVT_MENU, self.OnItemAppend, item12)

		self.PopupMenu(menu)
		menu.Destroy()


	def OnItemBold(self, event):

		self.SetItemBold(self.current, not self.itemdict["isbold"])


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


	def OnKey(self, event):

		keycode = event.GetKeyCode()
		keyname = keyMap.get(keycode, None)

		if keycode == wx.WXK_BACK:
			self.log.write("OnKeyDown: HAHAHAHA! I Vetoed Your Backspace! HAHAHAHA\n")
			return

		if keyname is None:
			if "unicode" in wx.PlatformInfo:
				keycode = event.GetUnicodeKey()
				if keycode <= 127:
					keycode = event.GetKeyCode()
				keyname = "\"" + unichr(event.GetUnicodeKey()) + "\""
				if keycode < 27:
					keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)

			elif keycode < 256:
				if keycode == 0:
					keyname = "NUL"
				elif keycode < 27:
					keyname = "Ctrl-%s" % chr(ord('A') + keycode-1)
				else:
					keyname = "\"%s\"" % chr(keycode)
			else:
				keyname = "unknown (%s)" % keycode

		self.log.write("OnKeyDown: You Pressed '" + keyname + "'\n")

		event.Skip()


	def OnActivate(self, event):

		if self.item:
			self.log.write("OnActivate: %s" % self.GetItemText(self.item) + "\n")

		event.Skip()


	def OnHyperLink(self, event):

		item = event.GetItem()
		if item:
			self.log.write("OnHyperLink: %s" % self.GetItemText(self.item) + "\n")


	def OnTextCtrl(self, event):

		char = chr(event.GetKeyCode())
		self.log.write("EDITING THE TEXTCTRL: You Wrote '" + char + \
					   "' (KeyCode = " + str(event.GetKeyCode()) + ")\n")
		event.Skip()


	def OnComboBox(self, event):

		selection = event.GetEventObject().GetValue()
		self.log.write("CHOICE FROM COMBOBOX: You Chose '" + selection + "'\n")
		event.Skip()

class DescriptorView(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

		self.descriptorDetailPanel = DescriptorDetailsPanel.DescriptorDetailsPanel(splitter)
		self.descriptorTree = CustomTreeCtrl(splitter, self.descriptorDetailPanel)

		"""
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(self.descriptorTree, 1, wx.EXPAND)

		hbox = wx.BoxSizer(wx.HORIZONTAL)

		addButton = wx.Button(self, 10, "Add", (20, 20))
		addButton.SetSize(addButton.GetBestSize())
	#	addButton.Bind(wx.EVT_BUTTON, self.addClicked, addButton)

		removeButton = wx.Button(self, 10, "Remove", (20, 20))
		removeButton.SetSize(removeButton.GetBestSize())
	#	removeButton.Bind(wx.EVT_BUTTON, self.removeClicked, removeButton)

		hbox.Add(addButton, 0, wx.ALL, 10)
		hbox.Add(removeButton, 0, wx.ALL, 10)
		#vbox.Add(hbox, 1, wx.EXPAND)

	#	panel = wx.Panel(splitter)
	#	panel.SetSizer(vbox)
	#	panel.SetAutoLayout(True)

		panel = self.descriptorTree

		"""

		splitter.SplitVertically(self.descriptorTree, self.descriptorDetailPanel, 300)
		splitter.SetMinimumPaneSize(300)

		sizer = wx.BoxSizer()
		sizer.Add(splitter, 1, wx.EXPAND)
		self.SetSizer(sizer)


		tree = self.descriptorTree


		deviceDescriptor = Template.parseTemplateFromFile("templates/device.xml")
		tree.descriptors.append(deviceDescriptor)


		configDescriptor = Template.parseTemplateFromFile("templates/configuration.xml")
		i = Template.parseTemplateFromFile("templates/interface.xml")
		ep = Template.parseTemplateFromFile("templates/endpoint.xml")

		assoc = Template.parseTemplateFromFile("templates/interfaceassociation.xml")
		i.addChild(assoc)

		i.addChild(ep)
		i.addChild(ep)
		configDescriptor.addChild(i)
		configDescriptor.addChild(i)
		tree.descriptors.append(configDescriptor)


		configDescriptor = Template.parseTemplateFromFile("templates/configuration.xml")
		tree.descriptors.append(configDescriptor)

		qual = Template.parseTemplateFromFile("templates/devicequalifier.xml")
		tree.descriptors.append(qual)

		typecount = {}

		for d in tree.descriptors:
			t = d.descriptorType;
			try:
				typecount[t] += 1
			except:
				typecount[t] = 1

			n = typecount[t]

			print "static const char %s_%d[] = {" % (t, n)
			d.dumpC()
			print "};\n"


		tree.BuildTree()

