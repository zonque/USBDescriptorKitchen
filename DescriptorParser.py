import re
import copy
import string
import Descriptor

def commentRemover(text):
	def replacer(match):
		s = match.group(0)
		if s.startswith('/'):
			return ""
		else:
			return s

	pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
	return re.sub(pattern, replacer, text)

def reconstructFields(desc, array):
	idx = 0

	# now copy over all non-constant elements
	for e in desc.elements:	
		if e.elementType == "constant" or \
		   e.elementType == "auto":
			idx += e.size
			continue

		e.value = 0
		e.strValue = ""

		if e.name == "bString":
			for i in range(len(array) - idx):
				# only copy over every second byte (unicode)
				if not (i % 2):
					e.strValue += "%c" % array[idx + i]
		else:
			for n in range(e.size):
				e.value |= array[idx + n] << (n * 8)
				#print "element %s val %d" % (e.name, e.value)

		idx += e.size

def reconstructDescriptor(array, descriptorTemplates, state, parentList):
	desc = None

	for t in descriptorTemplates:
		off = 0
		matched = True

		# test if all constant elements in the template descriptor match
		for e in t.elements:
			if (off + e.size > len(array)):
				matched = False
				off += e.size
				break

			v = 0
			for n in range(e.size):
				v |= array[off + n] << (n * 8)

			if e.elementType == "constant" and e.value != v:
				matched = False

			if e.elementType == "enum":
				enumvals = []
				for (name, enumval) in e.enum.items():
					enumvals.append(int(enumval))

				#print enumvals

				if not v in enumvals:
					matched = False

			off += e.size

		if not matched:
			continue

		desc = copy.deepcopy(t)
		desc.setParentList(parentList)

		# quirks for string descriptors - a StringDescriptorZero must always come first
		if desc.descriptorType.descriptorType == "StringZero":
			if "stringDescriptorZeroSeen" in state:
				desc.descriptorType == "String"
			else:
				state.append("stringDescriptorZeroSeen")

		# reconstruct fields once
		reconstructFields(desc, array)
		desc.handleAutoFields()

		# reconstruct fields again after the auto fields have been set
		reconstructFields(desc, array)

		return desc

	return None


def reconstructDescriptors(array, descriptorTemplates, state, parentList):
	idx = 0
	l = []

	while idx < len(array):
		length = int(array[idx], 16)

		if length == 0:
			print "bogus descriptors"
			return []

		subarray = []
		for b in array[idx:idx+length]:
			subarray.append(int(b, 16))

		idx += length

		d = reconstructDescriptor(subarray, descriptorTemplates, state, parentList)
		if d:
			l.append(d)
		else:
			print "Unable to parse descriptor(s) from array: "
			print subarray

	return l

def parseDescriptorFromFile(filename, descriptorTemplates):
	f = open(filename, "r")
	s = f.read()

	s = commentRemover(s)

	strings = re.split("\n", s)

	desc = None
	array = []
	runningindent = -1
	rootList = []
	parentList = rootList
	stack = []
	state = []

	for s in strings:

		# skip empty lines
		if re.match("^[ \t]*$", s):
			continue

		# determine the indentation level
		indent = 0
		while indent < len(s) and s[indent] == " ":
			indent += 1

		if runningindent == -1:
			runningindent = indent

		if indent != runningindent:
			if len(array):
				descList = reconstructDescriptors(array, descriptorTemplates, state, parentList)

				if len(descList) == 0:
					continue

				array = []

				if (indent < runningindent):
					if len(stack):
						while len(stack):
							st = stack.pop()
							if st["indent"] == indent:
								break
					else:
						parentList = rootList

				for d in descList:
					parentList.append(d)
					desc = d

				if (indent > runningindent):
					stack.append({ "list": parentList, "indent": runningindent})
					parentList = desc.children

		runningindent = indent

		array += re.findall("(0x[0-9a-fA-F][0-9a-fA-F])", s)

	f.close()

	return rootList
