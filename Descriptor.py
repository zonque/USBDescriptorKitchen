class DescriptorLink:
	descriptorType = 0
	descriptorField = ""

class DescriptorElementClass:
	ELEMENT_TYPE_UNKNOWN = 0
	ELEMENT_TYPE_CONSTANT = 1
	ELEMENT_TYPE_VARIABLE = 2
	ELEMENT_TYPE_ENUM = 3
	ELEMENT_TYPE_AUTO = 4
	ELEMENT_TYPE_LINK = 5
	ELEMENT_TYPE_BITMAP = 6
	ELEMENT_TYPE_STRING = 7

	def __init__(self):
		self.elementType = self.ELEMENT_TYPE_UNKNOWN
		self.displayFormat = "dec"
		self.name = ""
		self.comment = ""
		self.size = 0
		self.value = 0
		self.strValue = ""
		self.displayValue = ""
		self.base = 0
		self.enumVals = []
		self.enumKeys = []
		self.bitmap = []
		self.possibleLinkedDescriptors = []
		self.autoMethod = ""
		self.autoMethodDetail = 0
		self.parentElement = None

	def convertToInt(self, data):
		if (type(data) is int):
			return data

		if (data[:2] == "0x"):
			try:
				return int(data, 16)
			except:
				return 0

		try:
			return int(data, 10)
		except:
			return 0

	def checkIntegrity(self):
		if (self.name == ""):
			print "DEBUG: self.name is not set."
			return

		if (self.elementType == self.ELEMENT_TYPE_UNKNOWN):
			print "DEBUG: %s: elementType is not set." % self.name

		if (self.elementType == self.ELEMENT_TYPE_AUTO and
		    self.autoMethod == ""):
			print "DEBUG %s: AUTO type requested but non set." % self.name

		if (self.elementType == self.ELEMENT_TYPE_ENUM and
		    len(self.enumVals) == 0):
			print "DEBUG %s: no ENUMs given." % self.name

	def prettyPrint(self, value = None):
		if not value:
			value = self.value

		if (self.elementType == self.ELEMENT_TYPE_STRING):
			return self.strValue

		if (self.elementType == self.ELEMENT_TYPE_BITMAP):
			self.displayFormat = "hex"

		if (self.displayFormat == "hex"):
			if (self.size == 1):
				s = "0x%02x" % value
			if (self.size == 2):
				s = "0x%04x" % value
			if (self.size == 3):
				s = "0x%06x" % value
			if (self.size == 4):
				s = "0x%08x" % value
		else:
			s = "%d" % self.convertToInt(str(value))

		return s

	def dumpValueNoComma(self, value = None):
		if not value:
			value = self.value

		s = ""
		first = 1
		for i in range(self.size):
			if (first == 0):
				s += ", "
			s += "0x%02x" % ((value >> (i * 8)) & 0xff)
			first = 0

		return s

	def dumpHex(self):
		s = ""
		if self.elementType == self.ELEMENT_TYPE_STRING:
			for i in range(len(self.strValue)):
				# FIXME: this works for ASCII only
				s += "0x%02x, " % ord(self.strValue[i])
				s += "0x00, "
		else:
			for i in range(self.size):
				s += "0x%02x, " % ((self.value >> (i * 8)) & 0xff)

		return s

	def dumpC(self, indent = ""):
		print indent ,
		dump = self.dumpHex()
		padding = ' ' * (30 - len(indent) - len(dump))
		print "%s%s/* %s" % (dump, padding, self.name) ,

		if (self.comment != ""):
			print "\t(%s)" % self.comment ,

		print "*/"

	def updateSize(self):
		if self.elementType == self.ELEMENT_TYPE_STRING:
			try:
				self.size = len(self.strValue) * 2 # UNICODE
			except:
				self.size = 0
	def setValue(self, value):
		p = self.parentElement

		if self.elementType == self.ELEMENT_TYPE_STRING:
			self.strValue = value
			self.comment = "\"%s\"" % e.strValue
			return

		if p:
			# handle bitmap elements
			if p.elementType == self.ELEMENT_TYPE_BITMAP:
				mask = (1 << self.size) - 1
				self.value = self.convertToInt(value)
				v = p.value
				v &= ~(mask << self.offset)
				v |= self.value << self.offset
				p.value = v
		else:
			mask = (1 << (self.size * 8)) - 1
			self.value = self.convertToInt(value) & mask


class DescriptorClass:
	comment = ""
	descriptorType = ""

	def __init__(self):
		self.elements = []
		self.children = []
		self.indexOfDescriptor = 0

	def countSize(self):
		size = 0

		for e in self.elements:
			e.updateSize()
			e.checkIntegrity()
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
			if (c.descriptorType == cType):
				count += 1

		return count

	def handleAutoFields(self):
		idx = 0
		for c in self.children:
			c.indexOfDescriptor = idx
			c.handleAutoFields()
			idx += 1

		for e in self.elements:
			if (e.elementType != e.ELEMENT_TYPE_AUTO):
				continue

			if (e.autoMethod == "descriptorSize"):
				e.value = self.countSize()

			if (e.autoMethod == "descriptorSizeAllChildren"):
				e.value = self.countAllSize()

			if (e.autoMethod == "countChildrenOfType"):
				e.value = self.countChildrenOfType(e.autoMethodDetail)

			if (e.autoMethod == "indexOfDescriptor"):
				e.value = self.indexOfDescriptor + e.base

	def getValue(self, field):
		for e in self.elements:
			if (e.name == field):
				return e.value
		return -1

	def dumpC(self, indent = ""):
		self.handleAutoFields()

		indent += "  "

		print indent ,
		print "/* %s" % self.descriptorType ,
		if (self.comment != ""):
			print " (%s)" % self.comment,
		print "*/"

		for e in self.elements:
			e.dumpC(indent)

		print ""

		for c in self.children:
			c.dumpC(indent)

	def findDescriptorLinks(self, possibleDescriptors):
		a = []

		for p in possibleDescriptors:
			for c in self.children:
				if (c.descriptorType == p.descriptorType):
					a.append({'descriptorID': c.getValue(p.descriptorField),
						  'descriptorName': c.comment,
						  'descriptorType': c.descriptorType})

		return a

