import Descriptor
from xml.dom.minidom import parse, parseString


def getText(nodelist):
	rc = []
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc.append(node.data)
	return ''.join(rc)

def parseTemplateFromFile(filename):
	try:
		datasource = open(filename)
	except:
		print "unable to open %s" % filename
		return

	dom = parse(datasource)

	descriptor = dom.getElementsByTagName("descriptor")[0]
	newDescriptor = Descriptor.DescriptorClass()

	attrs = descriptor.attributes
	for i in range(attrs.length):
		a = attrs.item(i)
		if (a.name == "type"):
			newDescriptor.descriptorType = a.nodeValue

	for e in descriptor.getElementsByTagName("element"):
		newElement = Descriptor.DescriptorElementClass()
		attrs = e.attributes

		for i in range(attrs.length):
			a = attrs.item(i)
			if (a.name == "type"):
				if (a.nodeValue == "variable"):
					newElement.elementType = newElement.ELEMENT_TYPE_VARIABLE
				if (a.nodeValue == "constant"):
					newElement.elementType = newElement.ELEMENT_TYPE_CONSTANT
				if (a.nodeValue == "enum"):
					newElement.elementType = newElement.ELEMENT_TYPE_ENUM
				if (a.nodeValue == "auto"):
					newElement.elementType = newElement.ELEMENT_TYPE_AUTO
				if (a.nodeValue == "link"):
					newElement.elementType = newElement.ELEMENT_TYPE_LINK
				if (a.nodeValue == "bitmap"):
					newElement.elementType = newElement.ELEMENT_TYPE_BITMAP

			if (a.name == "name"):
				newElement.name = a.nodeValue
			if (a.name == "size"):
				newElement.size = int(a.nodeValue)
			if (a.name == "base"):
				newElement.base = int(a.nodeValue)
			if (a.name == "value"):
				newElement.value = newElement.convertToInt(a.nodeValue)
			if (a.name == "format"):
				newElement.displayFormat = a.nodeValue
			if (a.name == "method"):
				(method, colon, detail) = a.nodeValue.partition(":")
				newElement.autoMethod = method
				newElement.autoMethodDetail = detail

		if (newElement.elementType == newElement.ELEMENT_TYPE_ENUM):
			for v in e.getElementsByTagName("item"):
				val = getText(v.childNodes)
				key = v.getAttribute("name")
				if (key == ""):
					key = val

				newElement.enumVals.append(val)
				newElement.enumKeys.append(key)

		if (newElement.elementType == newElement.ELEMENT_TYPE_BITMAP):
			for v in e.getElementsByTagName("bitmap"):

				bitmap = Descriptor.DescriptorElementClass()

				bitmap.name = v.attributes["name"].nodeValue
				bitmap.offset = int(v.attributes["offset"].nodeValue)
				bitmap.size = int(v.attributes["size"].nodeValue)

				bitmapType = v.attributes["type"].nodeValue

				if (bitmapType == "variable"):
					bitmap.elementType = newElement.ELEMENT_TYPE_VARIABLE
				if (bitmapType == "constant"):
					bitmap.elementType = newElement.ELEMENT_TYPE_CONSTANT
				if (bitmapType == "enum"):
					bitmap.elementType = newElement.ELEMENT_TYPE_ENUM

				newElement.bitmap.append(bitmap)

		newDescriptor.addElement(newElement)

	return newDescriptor

