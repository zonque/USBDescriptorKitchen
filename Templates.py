from Descriptor import *

def createInterfaceClassCodes(name):
	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = name)
	elem.enumVals = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0xa, 0xb, 0xd, 0xe, 0xef, 0xfe, 0xff ]
	elem.enumKeys = [ "Defined at interface level", "Audio", "Conn", "HID", "Pysical", "Still Image", "Printer", \
			  "Mass Storage", "HUB", "CDC Data", "CSCID", "Content Sec", "Video", "Misc", "App Specific", "Vendor specific" ]
	return elem

def createDeviceDescriptorTemplate():
	desc = DescriptorClass("DeviceDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bcdUSB")
	elem.enumKeys = [ "1.1", "2.0" ]
	elem.enumVals = [ 0x0101, 0x0200 ]
	elem.value = 0x0200
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bDeviceSubClass")
	elem.enumKeys = [ "Defined at interface level", "Vendor specific" ]
	elem.enumVals = [ 0x00, 0xff ]
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bMaxPacketSize0")
	elem.enumKeys = [ "8", "16", "32", "64" ]
	elem.enumVals = [ 8, 16, 32, 64 ]
	elem.value = 64
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "idVendor")
	elem.displayFormat = "hex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "idProduct")
	elem.displayFormat = "hex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iManufacturer")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iProduct")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iSerialNumber")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bNumConfigurations")
	elem.autoMethod = "countChildrenOfType:ConfigurationDescriptor"
	desc.addElement(elem)

	return desc

def createConfigDescriptorTemplate():
	desc = DescriptorClass("ConfigurationDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 2, name = "wTotalLength")
	elem.autoMethod = "descriptorSizeAllChildren"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bNumInterfaces")
	elem.autoMethod = "countChildrenOfType:InterfaceDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bConfigurationValue")
	elem.autoMethod = "indexOfDescriptor"
	elem.base = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iConfiguration")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_BITMAP, size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "Remote Wakeup")
	bitmap.enumKeys = [ "No", "Yes" ];
	bitmap.enumVals = [ 0, 1 ];
	bitmap.offset = 5
	elem.appendBitmap(bitmap)

	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "Self-powered")
	bitmap.enumKeys = [ "No", "Yes" ];
	bitmap.enumVals = [ 0, 1 ];
	bitmap.offset = 6
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bMaxPower")
	desc.addElement(elem)

	return desc

def createStringDescriptorTemplate():
	desc = DescriptorClass("StringDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 3
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_STRING, name = "bString")
	desc.addElement(elem)

	return desc

def createInterfaceDescriptorTemplate():
	desc = DescriptorClass("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 4
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bInterfaceNumber")
	elem.autoMethod = "indexOfDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bAlternateSetting")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bNumEndpoints")
	elem.autoMethod = "countChildrenOfType:EndpointDescriptor"
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bInterfaceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterfaceSubClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterfaceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iInterface")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	return desc

def createEndpointDescriptorTemplate():
	desc = DescriptorClass("EndpointDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 5
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_BITMAP, size = 1, name = "bEndpointAddress")
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 4, name = "Endpoint Number")
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "Direction")
	bitmap.enumKeys = [ "OUT", "IN" ];
	bitmap.enumVals = [ 0, 1 ];
	bitmap.offset = 7
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_BITMAP, size = 1, name = "bEndpointAttributes")
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 2, name = "Transfer Type")
	bitmap.enumKeys = [ "Control", "Isochronous", "Bulk", "Interrupt" ];
	bitmap.enumVals = [ 0, 1, 2, 3 ];
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 2, name = "Synchronization Type")
	bitmap.enumKeys = [ "No Synchronization", "Asynchronous", "Adaptive", "Syncronous" ];
	bitmap.enumVals = [ 0, 1, 2, 3 ];
	bitmap.offset = 2
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 2, name = "Usage Type")
	bitmap.enumKeys = [ "Data Endpoint", "Feedback Endpoint", "Implcit Feedback Data Endpoint" ];
	bitmap.enumVals = [ 0, 1, 2, 3 ];
	bitmap.offset = 2
	elem.appendBitmap(bitmap)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "wMaxPacketSize")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterval")
	desc.addElement(elem)

	return desc

def createDeviceQualifierTemplate():
	desc = DescriptorClass("DeviceQualifier")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 6
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bcdUSB")
	elem.enumKeys = [ "1.1", "2.0" ]
	elem.enumVals = [ 0x0101, 0x0200 ]
	elem.value = 0x0200
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bDeviceSubClass")
	elem.enumKeys = [ "Defined at interface level", "Vendor specific" ]
	elem.enumVals = [ 0x00, 0xff ]
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bDeviceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(DescriptorElementClass.ELEMENT_TYPE_ENUM, size = 1, name = "bMaxPacketSize0")
	elem.enumKeys = [ "8", "16", "32", "64" ]
	elem.enumVals = [ 8, 16, 32, 64 ]
	elem.value = 64
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bNumConfigurations")
	elem.autoMethod = "countChildrenOfType:ConfigurationDescriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bReserved")
	desc.addElement(elem)

	return desc

def createInterfaceAssociationDescriptorTemplate():
	desc = DescriptorClass("InterfaceAssociationDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 8
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bFirstInterface")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterfaceCount")
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bFunctionClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterfaceSubClass")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bInterfaceProtocol")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_LINK, size = 1, name = "iFunction")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	return desc

def createDFUFunctionDescriptorTemplate():
	desc = DescriptorClass("DFUFunctionalDescriptor")

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_AUTO, size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_CONSTANT, size = 1, name = "bDescriptorType")
	elem.value = 0x21
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 1, name = "bmAttributes")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "wDetachTimeOut")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "wTransferSize")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = DescriptorElementClass.ELEMENT_TYPE_VARIABLE, size = 2, name = "bcdDFUVersion")
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

	return templates

