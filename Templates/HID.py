from Descriptor import *

def createHIDDescriptor():
	desc = DescriptorClass("HID")
	desc.allowedParents.append("Interface")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x21
	elem.comment = "HID"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 2, name = "bcdHID")
	elem.value = 0x101
	elem.comment = "1.1"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bCountryCode")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNumDescriptors")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bNumDescriptors")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bNumDescriptors"

	member = DescriptorElementArrayMemberClass(memberType = "constant", size = 1, name = "bDescriptorType")
	member.value = 0x22
	arr.appendMember(member)

	member = DescriptorElementArrayMemberClass(memberType = "variable", size = 2, name = "wDescriptorLength")
	arr.appendMember(member)
	desc.addElementArray(arr)

	return desc

