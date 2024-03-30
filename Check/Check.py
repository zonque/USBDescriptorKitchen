import wx
from .Basic import *

class CheckFrame(wx.Frame):
	def __init__(self, parent, ID, title, pos=wx.DefaultPosition,
		size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

		wx.Frame.__init__(self, parent, ID, title, pos, size, style)
		panel = wx.Panel(self, -1)

		self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

		sizer = wx.BoxSizer()
		sizer.Add(self.text, 1, wx.EXPAND)

		self.SetSizer(sizer)

def doCheck(wxParent, descriptorList):
	win = CheckFrame(wxParent, -1, "Descriptor check results", size=(350, 200),
		style = wx.DEFAULT_FRAME_STYLE)
	win.Show(True)
	issues = 0

	issues += basicCheck(descriptorList, win.text)

	win.text.AppendText("------------------\n")
	
	s = ""
	if issues != 1:
		s = "s"

	win.text.AppendText("Check finished, %d issue%s\n" % (issues, s))


