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
					e.strValue += "%c" % int(array[idx + i], 16)
		else:
			for n in range(e.size):
				e.value |= int(array[idx], 16) << (n * 8)
				#print "element %s val %d" % (e.name, e.value)
				idx += 1

def reconstructDescriptor(array, descriptorTemplates, state, parentList):
	idx = 0
	l = []

	while idx < len(array):
		length = int(array[idx], 16)
		print "len %d" % length

		for t in descriptorTemplates:
			off = 0
			matched = True

			# test if all constant elements in the template descriptor match
			for e in t.elements:
				if (off >= len(array)) or \
				   (e.elementType == "constant" and e.value != int(array[idx+off], 16)):
					matched = False

				off += e.size

			if not matched:
				continue

			# quirks for string descriptors - a StringDescriptorZero must always come first
			if t.descriptorType == "StringDescriptorZero":
				if "stringDescriptorZeroSeen" in state:
					continue

				state.append("stringDescriptorZeroSeen")

			desc = copy.deepcopy(t)
			desc.setParentList(parentList)
			print "desc type: %s" % desc.descriptorType

			# reconstruct fields once
			reconstructFields(desc, array[idx:])
			desc.handleAutoFields()

			# reconstruct fields again after the auto fields have been set
			reconstructFields(desc, array[idx:])

			l.append(desc)
			break

		idx += length

	return l

def parseDescriptorFromFile(filename, descriptorTemplates):
	f = open(filename, "r")
	s = f.read()

	s = commentRemover(s)
	
	strings = re.split("\n", s)
	
	desc = None
	bytearray = []
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
			if len(bytearray):
				descList = reconstructDescriptor(bytearray, descriptorTemplates, state, parentList)
				
				if not descList:
					print "Unable to parse descriptor(s) from array: "
					print bytearray
					bytearray = []
					continue

				bytearray = []

				if (indent < runningindent):
					if len(stack):
						while len(stack):
							st = stack.pop()
							if st["indent"] == indent:
								break
					else:
						print "ROOT"
						parentList = rootList

				for desc in descList:
					parentList.append(desc)

				if (indent > runningindent):
					stack.append({ "list": parentList, "indent": runningindent})
					parentList = desc.children

		runningindent = indent

		bytearray += re.findall("(0x[0-9a-fA-F][0-9a-fA-F])", s)

	f.close()

	return rootList
