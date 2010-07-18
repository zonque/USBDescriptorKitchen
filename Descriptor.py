class DescriptorLink:
	descriptorType = 0
	descriptorField = ""

class DescriptorElementClass:
	def __init__(self, elementType = "UNKNOWN", size = 0, name = ""):
		self.elementType = elementType
		self.size = size
		self.name = name
		self.displayFormat = "dec"
		self.comment = ""
		self.value = 0
		self.strValue = ""
		self.displayValue = ""
		self.base = 0
		self.enum = {}
		self.bitmap = []
		self.autoMethod = ""
		self.autoMethodDetail = 0
		self.parentElement = None

	def convertToInt(self, data):
		if type(data) is int:
			return data

		if data[:2] == "0x":
			try:
				return int(data, 16)
			except:
				return 0

		try:
			return int(data, 10)
		except:
			return 0

	def getEnumKey(self, val = None):
		if not val:
			val = self.value

		for (k, v) in self.enum.items():
			if self.convertToInt(self.value) == self.convertToInt(v):
				value = k

		return value

	def getValue(self):
		if self.elementType == "string":
			return self.strValue
		else:
			return self.value

	def prettyPrint(self, value = None):
		if not value:
			value = self.value

		if self.elementType == "string":
			return self.strValue

		if self.elementType == "enum":
			return self.getEnumKey(self.value)

		if self.elementType == "bitmap":
			self.displayFormat = "hex"

		if self.displayFormat == "hex":
			if self.size == 1:
				s = "0x%02x" % value
			if self.size == 2:
				s = "0x%04x" % value
			if self.size == 3:
				s = "0x%06x" % value
			if self.size == 4:
				s = "0x%08x" % value
		else:
			s = "%d" % self.convertToInt(str(value))

		return s

	def dumpValueNoComma(self, value = None):
		if not value:
			value = self.value

		s = ""
		first = 1
		size = self.size

		if self.parentElement and self.parentElement.elementType == "bitmap":
			size /= 8
			if self.size % 8:
				size += 1

		for i in range(size):
			if first == 0:
				s += ", "
			s += "0x%02x" % ((value >> (i * 8)) & 0xff)
			first = 0

		return s

	def dumpHex(self, indent=""):
		s = ""
		if self.elementType == "string":
			for i in range(len(self.strValue)):
				# FIXME: this works for ASCII only
				s += "0x%02x, 0x00, " % ord(self.strValue[i])
				if i % 8 == 7:
					s += "\n"
					s += indent + " "
		else:
			for i in range(self.size):
				s += "0x%02x, " % ((self.value >> (i * 8)) & 0xff)

		return s

	def dumpC(self, indent = ""):
		print indent ,
		dump = self.dumpHex(indent)
		padding = ' ' * (30 - len(indent) - len(dump))
		print "%s%s/* %s" % (dump, padding, self.name) ,

		if self.comment != "":
			print "(%s) " % self.comment ,

		if self.elementType == "enum":
			print "(\"%s\") " % self.getEnumKey() ,

		if self.elementType == "bitmap":
			print "(" ,
			first = 1
			for b in self.bitmap:
				if not first:
					print ", " ,
				first = 0
				print "'%s' = %d" % (b.name, b.value) ,
			print ")" ,

		if self.size > 1:
			print "(%d) " % self.value ,

		print "*/"

	def updateSize(self):
		if self.elementType == "string":
			try:
				self.size = len(self.strValue) * 2 # UNICODE
			except:
				self.size = 0

	def setValue(self, value):
		p = self.parentElement

		if self.elementType == "string":
			self.strValue = value
			self.comment = "\"%s\"" % self.strValue
			return

		if p:
			if p.elementType == "bitmap":
				mask = (1 << self.size) - 1
				self.value = self.convertToInt(value)
				v = p.value
				v &= ~(mask << self.offset)
				v |= self.value << self.offset
				p.value = v
		else:
			mask = (1 << (self.size * 8)) - 1
			self.value = self.convertToInt(value) & mask

	def appendBitmap(self, bitmap):
		bitmap.parentElement = self
		self.bitmap.append(bitmap)

class DescriptorClass:
	def __init__(self, descriptorType = "", comment = ""):
		self.elements = []
		self.children = []
		self.descriptorType = descriptorType
		self.comment = comment
		self.allowedParents = []

	def setParentList(self, pl):
		self.parentList = pl

	def countSize(self):
		size = 0

		for e in self.elements:
			e.updateSize()
			size += e.size

		return size

	def countAllSize(self):
		size = self.countSize()

		for c in self.children:
			size += c.countAllSize()

		return size

	def addElement(self, element):
		self.elements.append(element)

	def addChild(self, child):
		self.children.append(child)

	def countChildrenOfType(self, cType):
		count = 0

		for c in self.children:
			if c.descriptorType == cType:
				count += 1

		return count

	def getIndexFromParentList(self):
		idx = 0
		for d in self.parentList:
			if d.descriptorType != self.descriptorType:
				continue

			if d == self:
				return idx

			idx += 1

		return -1

	def handleAutoFields(self):
		idx = 0
		for c in self.children:
			c.handleAutoFields()
			idx += 1

		for e in self.elements:
			if e.elementType != "auto":
				continue

			if e.autoMethod == "descriptorSize":
				e.value = self.countSize()

			if e.autoMethod == "descriptorSizeAllChildren":
				e.value = self.countAllSize()

			if e.autoMethod == "countChildrenOfType":
				e.value = self.countChildrenOfType(e.autoMethodDetail)

			if e.autoMethod == "indexOfDescriptor":
				e.value = self.getIndexFromParentList() + e.base

	def getValue(self, field):
		for e in self.elements:
			if e.name == field:
				return e.getValue()
		return -1

	def getSummaryName(self):
		name = self.descriptorType

		if name == "ConfigurationDescriptor":
			for e in self.elements:
				if e.name == "bConfigurationValue":
					val = e.value
			name += " (#%d)" % val

		if name == "InterfaceDescriptor":
			for e in self.elements:
				if e.name == "bInterfaceNumber":
					idx = e.value
				if e.name == "bAlternateSetting":
					alt = e.value
			name += " (#%d, alt %d)" % (idx, alt)

		if name == "EndpointDescriptor":
			for e in self.elements:
				if e.name == "bEndpointAddress":
					addr = e.value
			name += " (0x%02x)" % addr

		if name == "StringDescriptor":
			for e in self.elements:
				if e.name == "bString":
					v = e.strValue

			name += " (%s)" % v

		return name

	def dumpC(self, indent = ""):
		self.handleAutoFields()

		indent += "  "

		print indent ,
		print "/* %s" % self.descriptorType ,
		if self.comment != "":
			print " (%s)" % self.comment,
		print "*/"

		for e in self.elements:
			e.dumpC(indent)

		for c in self.children:
			c.dumpC(indent)

