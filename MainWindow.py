#!/usr/bin/python

import wx
import os
import string

import StringListPanel
import Descriptor
import TreeCtrl

class MainWindow(wx.Panel):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent)

		splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)

		self.stringListPanel = StringListPanel.StringListPanel(splitter)
		self.descriptorTree = TreeCtrl.DescriptorView(splitter)

		splitter.SplitVertically(self.stringListPanel, self.descriptorTree, 300)
		splitter.SetMinimumPaneSize(220)

		sizer = wx.BoxSizer()
		sizer.Add(splitter, 1, wx.EXPAND)
		self.SetSizer(sizer)

class MainFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "USB Descriptor Kitchen", size=(1200, 400))

		self.CenterOnScreen()

		# Prepare the menu bar
		menuBar = wx.MenuBar()

		# 1st menu from left
		menu1 = wx.Menu()
		menu1.Append(101, "&Open", "")
		menu1.Append(102, "&Save", "")
		menu1.Append(103, "Save &as", "")
		menu1.AppendSeparator()
		menu1.Append(104, "&Quit", "")
		# Add menu to the menu bar
		menuBar.Append(menu1, "&File")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.OnOpen, id=101)
		self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=104)

	def OnCloseWindow(self, event):
		self.Close()

	def OnOpen(self, event):
		Template.parseTemplateFromFile("templates/device.xml")

if __name__ == '__main__':
	import sys,os

	app = wx.App(False)
	frame = MainFrame(None)
	MainWindow(frame)
	frame.Show(True)
	app.MainLoop()

