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

def reconstructDescriptor(array, descriptorTemplates):
	length = array[0]
	dtype = array[1]

	idx = 0

	for t in descriptorTemplates:
		if dtype == t.elements[1].value:
			d = copy.deepcopy(t)

			for e in t.elements:
				for n in range(e.size):
					e.value = array[idx]
					idx += 1


	return 

def parseDescriptorFromFile(filename, descriptorTemplates):
	f = open(filename, "r")
	s = f.read()

	s = commentRemover(s)
	s = re.sub("/^[ \t]*$/", "", s)
	blocks = re.split("}", s)

	for block in blocks:
		desc = re.findall("(0x[0-9a-fA-F][0-9a-fA-F])", block)
		reconstructDescriptor(desc, descriptorTemplates)

	f.close()

