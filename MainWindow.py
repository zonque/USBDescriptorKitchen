#!/usr/bin/python

import wx
import os
import copy
import string

import StringListPanel
import Descriptor
import TreeCtrl
import DescriptorDetailsPanel
import Templates

class MainWindow(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

		self.descriptorDetailPanel = DescriptorDetailsPanel.DescriptorDetailsPanel(splitter)
		self.descriptorTree = TreeCtrl.CustomTreeCtrl(splitter, self.descriptorDetailPanel)

		splitter.SplitVertically(self.descriptorTree, self.descriptorDetailPanel, 300)
		splitter.SetMinimumPaneSize(300)

		sizer = wx.BoxSizer()
		sizer.Add(splitter, 1, wx.EXPAND)
		self.SetSizer(sizer)

		tree = self.descriptorTree

		#tree.BuildTree()

		parent.setTree(tree)

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "USB Descriptor Kitchen", size=(900, 400))

		self.CenterOnScreen()

		self.templates = []

		# Prepare the menu bar
		menuBar = wx.MenuBar()

		menu1 = wx.Menu()
		menu1.Append(101, "&Open", "")
		menu1.Append(102, "&Save", "")
		menu1.Append(103, "Save &as", "")
		menu1.AppendSeparator()
		menu1.Append(104, "&Quit", "")
		menuBar.Append(menu1, "&File")

		submenu = wx.Menu()
		menuid = 1000

		self.templates = Templates.createTemplates()
		for t in self.templates:
			submenu.Append(menuid, t.descriptorType)
			self.Bind(wx.EVT_MENU, self.OnAddDescriptor, id=menuid)
			menuid += 1

		menu2 = wx.Menu()
		menu2.AppendMenu(201, "&Add", submenu)
		menu2.Append(202, "&Remove selected", "")
		menu2.AppendSeparator()
		menu2.Append(203, "&Dump", "")
		menuBar.Append(menu2, "&Descriptor set")

		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnOpen, id=101)
		self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=104)

		#self.Bind(wx.EVT_MENU, self.OnAddDescriptor)
		self.Bind(wx.EVT_MENU, self.OnRemoveDescriptor, id=202)
		self.Bind(wx.EVT_MENU, self.OnDump, id=203)

	def OnCloseWindow(self, event):
		self.Close()

	def OnOpen(self, event):
		print "open"

	def OnDump(self, event):
		typecount = {}

		print
		print "/*****************************************************************/"
		print "/* automatically generated. do not edit. */"
		print "/*****************************************************************/"
		print

		for d in self.tree.descriptors:
			t = d.descriptorType;
			try:
				typecount[t] += 1
			except:
				typecount[t] = 1

			n = typecount[t]

			print "static const char %s_%d[] = {" % (t, n)
			d.dumpC()
			print "};\n"

		for key in typecount:
			val = typecount[key]

			print "static const char *%ss[] = {" % key

			for n in range(val):
				print "\t%s_%d," % (key, n + 1)

			print "};\n"

	def OnAddDescriptor(self, event):
		idx = event.GetId() - 1000
		desc = copy.deepcopy(self.templates[idx])
		self.tree.AddDescriptor(desc)

	def OnRemoveDescriptor(self, event):
		self.tree.RemoveSelectedDescriptor()

	def setTree(self, tree):
		self.tree = tree


if __name__ == '__main__':
	import sys,os

	app = wx.App(False)
	frame = MainFrame(None)
	MainWindow(frame)
	frame.Show(True)
	app.MainLoop()

