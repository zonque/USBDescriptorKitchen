#!/usr/bin/python

import wx
import os
import string

import StringListPanel
import Descriptor
import TreeCtrl
import DescriptorDetailsPanel
import Template

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

		string = Template.parseTemplateFromFile("templates/string.xml")
		tree.descriptors.append(string)

		tree.BuildTree()

		parent.setTree(tree)

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "USB Descriptor Kitchen", size=(900, 400))

		self.CenterOnScreen()

		# Prepare the menu bar
		menuBar = wx.MenuBar()

		menu1 = wx.Menu()
		menu1.Append(101, "&Open", "")
		menu1.Append(102, "&Save", "")
		menu1.Append(103, "Save &as", "")
		menu1.AppendSeparator()
		menu1.Append(104, "&Quit", "")
		menuBar.Append(menu1, "&File")

		menu2 = wx.Menu()
		menu2.Append(201, "&Dump", "")
		menuBar.Append(menu2, "&Descriptor set")

		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnOpen, id=101)
		self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=104)

		self.Bind(wx.EVT_MENU, self.OnDump, id=201)

	def OnCloseWindow(self, event):
		self.Close()

	def OnOpen(self, event):
		Template.parseTemplateFromFile("templates/device.xml")

	def OnDump(self, event):
		typecount = {}

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

	def setTree(self, tree):
		self.tree = tree


if __name__ == '__main__':
	import sys,os

	app = wx.App(False)
	frame = MainFrame(None)
	MainWindow(frame)
	frame.Show(True)
	app.MainLoop()

