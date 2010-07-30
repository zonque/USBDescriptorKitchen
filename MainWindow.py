#!/usr/bin/python

import wx
import os
import copy
import string
import re

import Descriptor
import DescriptorParser
import TreeCtrl
import DescriptorDetailsPanel
import Templates.Templates

def getVersion():
	return "0.2"

wildcard = 	"Header Files (*.h)|*h|" \
		"All files (*)|*"

class MainWindow(wx.Panel):

	def __init__(self, parent, templates):
		wx.Panel.__init__(self, parent)

		splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

		self.descriptorDetailPanel = DescriptorDetailsPanel.DescriptorDetailsPanel(splitter)
		self.descriptorTree = TreeCtrl.CustomTreeCtrl(splitter, self.descriptorDetailPanel, templates)

		splitter.SplitVertically(self.descriptorTree, self.descriptorDetailPanel, 300)
		splitter.SetMinimumPaneSize(300)

		sizer = wx.BoxSizer()
		sizer.Add(splitter, 1, wx.EXPAND)
		self.SetSizer(sizer)

		tree = self.descriptorTree

		parent.setTree(tree)

class MainFrame(wx.Frame):

	def __init__(self, parent, templates):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "USB Descriptor Kitchen", size=(1000, 400))

		self.CenterOnScreen()

		menuBar = wx.MenuBar()
		menu1 = wx.Menu()
		menu1.Append(101, "&Load", "")
		menu1.Append(102, "&Save", "")
		menu1.Append(103, "Save &as ...", "")
		menu1.AppendSeparator()
		menu1.Append(104, "&Check", "")
		menu1.Append(105, "&Dump to stdout", "")
		menu1.Append(106, "&Clear", "")
		menu1.AppendSeparator()
		menu1.Append(107, "&Quit", "")
		menuBar.Append(menu1, "&Descriptor set")

		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnFileOpen, id=101)
		self.Bind(wx.EVT_MENU, self.OnFileSave, id=102)
		self.Bind(wx.EVT_MENU, self.OnFileSaveAs, id=103)
		self.Bind(wx.EVT_MENU, self.OnDump, id=105)
		self.Bind(wx.EVT_MENU, self.OnClearDescriptors, id=106)
		self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=107)

		self.templates = templates
		self.filename = None

	def OnCloseWindow(self, event):
		self.Close()

	def doDump(self):
		typecount = {}

		out = "\n"
		out += "/***************************************************************************\n"
		out += "   AUTOMATICALLY GENERATED by USBDescriptorKitchen (%s)\n" % getVersion()
		out += "   When editing, make sure you keep the indentation right\n"
		out += "   and use an editor that doesn't mess around with the linefeeds.\n"
		out += "\n"
		out += "   See http://github.com/zonque/USBDescriptorKitchen/\n"
		out += "   for more information about the tool that was used to generate this file\n"
		out += " ***************************************************************************/"
		out += "\n"

		for d in self.tree.descriptors:
			t = d.descriptorType;
			try:
				typecount[t] += 1
			except:
				typecount[t] = 1

			n = typecount[t]

			out += "static const char %s_%d[] = {\n" % (t, n)
			out += d.dumpC()
			out += "};\n\n"

		for key in typecount:
			val = typecount[key]

			out += "static const char *%ss[] = {\n" % key

			for n in range(val):
				out += "\t%s_%d,\n" % (key, n + 1)

			out += "};\n\n"

		return out

	def OnDump(self, event):
		print self.doDump()

	def OnFileOpen(self, event):
		dlg = wx.FileDialog(self, message="Choose a file",
				    defaultDir=os.getcwd(), 
				    defaultFile="",
				    wildcard=wildcard,
				    style=wx.OPEN | wx.CHANGE_DIR)

		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			self.filename = paths[0]

			self.tree.RemoveAllDescriptors()
			for d in DescriptorParser.parseDescriptorFromFile(paths[0], self.templates):
				#print d
				self.tree.AddDescriptor(d)


	def OnFileSaveAs(self, event):
		dlg = wx.FileDialog(self, message="Save descriptors to ...",
				    defaultDir=os.getcwd(), 
				    defaultFile="",
				    wildcard=wildcard,
				    style=wx.SAVE | wx.CHANGE_DIR)

		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			self.filename = paths[0]
			fp = file(paths[0], 'w')
			fp.write(self.doDump())
			fp.close

	def OnFileSave(self, event):
		if not self.filename:
			self.OnFileSaveAs(event)
			return

		fp = file(self.filename, 'w')
		fp.write(self.doDump())
		fp.close

	def OnClearDescriptors(self, event):
		self.tree.RemoveAllDescriptors()

	def setTree(self, tree):
		self.tree = tree

if __name__ == '__main__':
	import sys,os

	templates = Templates.Templates.createTemplates()

	app = wx.App(False)
	frame = MainFrame(None, templates)
	MainWindow(frame, templates)
	frame.Show(True)
	app.MainLoop()

