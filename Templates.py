from Descriptor import *

def createInterfaceClassCodes(name):
	elem = DescriptorElementClass("enum", size = 1, name = name)
	elem.enum = { "Defined at interface level": 0,
			"Audio": 1, "Conn": 2, "HID": 3, "Pysical": 4, "Still Image": 5, "Printer": 6,
			"Mass Storage": 7, "HUB": 8, "CDC Data": 9, "CSCID": 0xa, "Content Sec": 0xb,
			"Video": 0xd, "Misc": 0xe, "App Specific": 0xef, "Vendor specific": 0xff }
	return elem

def createDeviceDescriptorTemplate():
	desc = DescriptorClass("DeviceDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bcdUSB")
	elem.enum = { "1.1": 0x0101, "2.0": 0x0200 }
	elem.value = 0x0200
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bDeviceSubClass")
	elem.enum = { "Defined at interface level": 0x00, "Vendor specific": 0xff }
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bMaxPacketSize0")
	elem.enum = { "8": 8, "16": 16, "32": 32, "64": 64 }
	elem.value = 64
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "idVendor")
	elem.displayFormat = "hex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "idProduct")
	elem.displayFormat = "hex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iManufacturer")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iProduct")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iSerialNumber")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumConfigurations")
	elem.autoMethod = "countChildrenOfType:ConfigurationDescriptor"
	desc.addElement(elem)

	return desc

def createConfigDescriptorTemplate():
	desc = DescriptorClass("ConfigurationDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 2, name = "wTotalLength")
	elem.autoMethod = "descriptorSizeAllChildren"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumInterfaces")
	elem.autoMethod = "countChildrenOfType:InterfaceDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bConfigurationValue")
	elem.autoMethod = "indexOfDescriptor"
	elem.base = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iConfiguration")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass("enum", size = 1, name = "Remote Wakeup")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 5
	elem.appendBitmap(bitmap)

	bitmap = DescriptorElementClass("enum", size = 1, name = "Self-powered")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 6
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bMaxPower")
	desc.addElement(elem)

	return desc

def createStringDescriptorTemplate():
	desc = DescriptorClass("StringDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 3
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "string", name = "bString")
	desc.addElement(elem)

	return desc

def createInterfaceDescriptorTemplate():
	desc = DescriptorClass("InterfaceDescriptor")
	desc.allowedParents.append("ConfigurationDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 4
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bInterfaceNumber")
	elem.autoMethod = "indexOfDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bAlternateSetting")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumEndpoints")
	elem.autoMethod = "countChildrenOfType:EndpointDescriptor"
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bInterfaceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceSubClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iInterface")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	return desc

def createEndpointDescriptorTemplate():
	desc = DescriptorClass("EndpointDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 5
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bEndpointAddress")
	bitmap = DescriptorElementClass("variable", size = 4, name = "Endpoint Number")
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 1, name = "Direction")
	bitmap.enum = { "OUT": 0, "IN": 1 };
	bitmap.offset = 7
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bEndpointAttributes")
	bitmap = DescriptorElementClass("enum", size = 2, name = "Transfer Type")
	bitmap.enum = { "Control": 0, "Isochronous": 1, "Bulk": 2, "Interrupt": 3 };
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 2, name = "Synchronization Type")
	bitmap.enum = { "No Synchronization": 0, "Asynchronous": 1, "Adaptive": 2, "Syncronous": 3 };
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 2, name = "Usage Type")
	bitmap.enum = { "Data Endpoint": 0, "Feedback Endpoint": 1, "Implcit Feedback Data Endpoint": 3 };
	bitmap.offset = 2
	elem.appendBitmap(bitmap)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "wMaxPacketSize")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterval")
	desc.addElement(elem)

	return desc

def createDeviceQualifierTemplate():
	desc = DescriptorClass("DeviceQualifier")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 6
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bcdUSB")
	elem.enum = { "1.1": 0x0101, "2.0": 0x0200 }
	elem.value = 0x0200
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bDeviceSubClass")
	elem.enum = { "Defined at interface level": 0x00, "Vendor specific": 0xff }
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bMaxPacketSize0")
	elem.enum = { "8": 8, "16": 16, "32": 32, "64": 64 }
	elem.value = 64
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumConfigurations")
	elem.autoMethod = "countChildrenOfType:ConfigurationDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bReserved")
	desc.addElement(elem)

	return desc

def createInterfaceAssociationDescriptorTemplate():
	desc = DescriptorClass("InterfaceAssociationDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 8
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bFirstInterface")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceCount")
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bFunctionClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceSubClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iFunction")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	return desc

def createDFUFunctionDescriptorTemplate():
	desc = DescriptorClass("DFUFunctionalDescriptor")
	desc.allowedParents.append("ConfigurationDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x21
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass("enum", size = 1, name = "bitWillDetach")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 3
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 1, name = "bitManifestationTolerant")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 2
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 1, name = "bitCanUpload")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 1
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 1, name = "bitCanDnload")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "wDetachTimeOut")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "wTransferSize")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "bcdDFUVersion")
	desc.addElement(elem)

	return desc

def createTemplates():
	templates = []

	templates.append(createDeviceDescriptorTemplate())
	templates.append(createConfigDescriptorTemplate())
	templates.append(createStringDescriptorTemplate())
	templates.append(createInterfaceDescriptorTemplate())
	templates.append(createEndpointDescriptorTemplate())
	templates.append(createDeviceQualifierTemplate())
	templates.append(createInterfaceAssociationDescriptorTemplate())
	templates.append(createDFUFunctionDescriptorTemplate())

	return templates

