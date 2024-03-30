import copy

class DescriptorElementArrayMemberClass:
	def __init__(self, memberType, size, name):
		self.bitmap = []
		self.enum = []
		self.name = name
		self.memberType = memberType
		self.size = size
		self.linkType = ""
		self.value = 0
		self.comment = ""

	def appendBitmap(self, bitmap):
		self.bitmap.append(bitmap)

class DescriptorElementArrayClass:
	def __init__(self, after):
		self.after = after
		self.numEntries = 1
		self.members = []

	def appendMember(self, member):
		self.members.append(member)

class DescriptorElementClass:
	def __init__(self, elementType = "UNKNOWN", size = 0, name = ""):
		self.elementType = elementType
		self.size = size
		self.name = name
		self.displayFormat = "dec"
		self.comment = ""
		self.value = 0
		self.strValue = ""
		self.base = 0
		self.offset = 0
		self.enum = {}
		self.bitmap = []
		self.autoMethod = ""
		self.suggestionType = False
		self.createdByArray = False
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

		key = None

		for (k, v) in self.enum.items():
			if self.convertToInt(self.value) == self.convertToInt(v):
				key = k

		if not key:
			print("Ooops ... val %d not in enum %s" % (val, self.name))

		return key

	def getValue(self):
		if self.elementType == "string":
			return self.strValue
		else:
			return self.value

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
		out = indent
		dump = self.dumpHex(indent)
		padding = ' ' * (30 - len(indent) - len(dump))
		out += "%s%s/* %s" % (dump, padding, self.name)

		if self.comment != "":
			out += " (%s)" % self.comment

		if self.elementType == "enum":
			out += " (\"%s\")" % self.getEnumKey()

		if self.elementType == "bitmap":
			out += " ("
			first = 1
			for b in self.bitmap:
				if not first:
					out += ", "
				first = 0
				out += "'%s' = %d" % (b.name, b.value)
			out += ")"

		if self.size > 1:
			out += " (%d)" % self.value

		out += " */\n"
		return out

	def updateSize(self):
		if self.elementType == "string":
			try:
				self.size = len(self.strValue) * 2 # UNICODE
			except:
				self.size = 0

	def appendBitmap(self, bitmap):
		bitmap.parentElement = self
		self.bitmap.append(bitmap)

	def updateBitmap(self):
		for b in self.bitmap:
			b.value = (self.value >> b.offset) & ((1 << b.size) - 1)

class DescriptorClass:
	def __init__(self, descriptorType = "", comment = ""):
		self.elements = []
		self.children = []
		self.arrays = []
		self.descriptorType = descriptorType
		self.comment = comment
		self.allowedParents = []
		self.descriptiveString = None
		self.parentDescriptor = None
		self.parentList = None
		self.dependsOnDescriptor = None

		elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
		elem.autoMethod = "descriptorSize"
		elem.comment = "Size of this descriptor in bytes"
		self.addElement(elem)

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
		if element.elementType == "bitmap":
			for b in element.bitmap:
				if b.elementType == "constant":
					element.value &= ~(((1 << b.size) - 1) << b.offset)
					element.value |= b.value << b.offset

		self.elements.append(element)

	def addChild(self, child):
		self.children.append(child)

	def addElementArray(self, array):
		self.arrays.append(array)

	def hasField(self, field):
		for e in self.elements:
			if e.name == field:
				return 1

		return 0

	def countChildrenOfType(self, cType):
		count = 0

		for c in self.children:
			if c.descriptorType == cType:
				count += 1

		return count

	def countDescriptorsOfType(self, cType):
		count = 0

		for d in self.parentList:
			if d.descriptorType == cType:
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

	def addArrayField(self, elem):
		if not elem.createdByArray:
			return

		for a in self.arrays:
			if a.arrayLength != "dynamic":
				continue

			for member in a.members:
				if elem.name[:len(member.name)] == member.name:
					a.numEntries += 1

		self.handleAutoFields()

	def removeArrayField(self, elem):
		if not elem.createdByArray:
			return

		for a in self.arrays:
			if a.arrayLength != "dynamic":
				continue

			if a.numEntries < 2:
				continue

			if elem.name[:len(a.name)] == a.name:
				a.numEntries -= 1

		self.handleAutoFields()

	def handleArrays(self):
		# create elements from arrays
		for a in self.arrays:
			savedValues = []

			# remove all elements that have been created dynamically
			elements = self.elements[:]

			for e in elements:
				for member in a.members:
					if e.createdByArray and e.name[:len(member.name)] == member.name:
						savedValues.append(e.value)
						self.elements.remove(e)

			if a.arrayLength == "given":
				num = self.getValue(a.arrayLengthField)

			if a.arrayLength == "dynamic":
				num = a.numEntries

			idx = 0
			# find element to create new things after
			elements = self.elements[:]
			for e in elements:
				if e.name == a.after:
					for i in range(num):
						for member in a.members:
							name = "%s(%d)" % (member.name, i)
							elem = DescriptorElementClass(elementType = member.memberType, size = member.size, name = name)
							elem.createdByArray = True
							elem.linkType = member.linkType
							elem.enum = member.enum
							elem.comment = member.comment

							for b in member.bitmap:
								bitmap = copy.deepcopy(b)
								bitmap.parentElement = self
								elem.appendBitmap(bitmap)

							# try to restore former values
							try:
								elem.value = savedValues.pop(0)
							except:
								#raise
								elem.value = member.value

							self.elements.insert(idx  + 1, elem)
							idx += 1

					break

				idx += 1

	def handleAutoFields(self):
		self.handleArrays()

		idx = 0
		for c in self.children:
			c.handleAutoFields()
			idx += 1

		for e in self.elements:
			e.updateBitmap()

			if e.elementType != "auto":
				continue

			if e.autoMethod == "descriptorSize":
				e.value = self.countSize()

			if e.autoMethod == "descriptorSizeAllChildren":
				e.value = self.countAllSize()

			if e.autoMethod == "countChildrenOfType":
				e.value = self.countChildrenOfType(e.autoMethodDetail)

			if e.autoMethod == "countDescriptorsOfType":
				e.value = self.countDescriptorsOfType(e.autoMethodDetail)

			if e.autoMethod == "indexOfDescriptor":
				e.value = self.getIndexFromParentList() + e.base

	def getValue(self, field):
		for e in self.elements:
			if e.name == field:
				return e.getValue()
		return -1

	def iterateUp(self, descriptorType):
		desc = self

		while desc and desc.descriptorType != descriptorType:
			desc = desc.parentDescriptor

		return desc

	def getSummaryName(self):
		name = self.descriptorType

		if name == "Configuration":
			for e in self.elements:
				if e.name == "bConfigurationValue":
					val = e.value
			name += " (#%d)" % val

		if name == "Interface":
			for e in self.elements:
				if e.name == "bInterfaceNumber":
					idx = e.value
				if e.name == "bAlternateSetting":
					alt = e.value
			name += " (#%d, alt %d)" % (idx, alt)

		if name == "Endpoint":
			for e in self.elements:
				if e.name == "bEndpointAddress":
					addr = e.value
			name += " (0x%02x)" % addr

		if name == "String":
			for e in self.elements:
				if e.name == "bString":
					v = e.strValue

			name += " (%s)" % v

		return name

	def dumpC(self, indent = ""):
		self.handleAutoFields()

		indent += "  "

		out = indent
		out += "/* %s" % self.descriptorType
		if self.comment != "":
			out += " (%s)" % self.comment
		out += "*/\n"

		for e in self.elements:
			out += e.dumpC(indent)

		for c in self.children:
			out += c.dumpC(indent)

		return out

	def debugDump(self, indent=""):
		print(indent + self)
		print(indent + self.descriptorType)

		for e in self.elements:
			print(indent + "element %s" % e.name)
			print(indent + "value %d" % e.value)

		indent += "  "
		for c in self.children:
			c.debugDump(indent)
