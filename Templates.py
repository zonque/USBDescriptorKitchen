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
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 1
	elem.comment = "DEVICE Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 2, name = "bcdUSB")
	elem.enum = { "1.1": 0x0101, "2.0": 0x0200 }
	elem.value = 0x0200
	elem.comment = "USB Specification Release Number in Binary-Coded Decimal"
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	elem.comment = "Class code (assigned by the USB-IF)."
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bDeviceSubClass")
	elem.enum = { "Defined at interface level": 0x00, "Vendor specific": 0xff }
	elem.comment = "Subclass code (assigned by the USB-IF)."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bDeviceProtocol")
	elem.comment = "Protocol code (assigned by the USB-IF)."
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bMaxPacketSize0")
	elem.enum = { "8": 8, "16": 16, "32": 32, "64": 64 }
	elem.value = 64
	elem.comment = "Maximum packet size for endpoint zero"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "idVendor")
	elem.displayFormat = "hex"
	elem.comment = "Vendor ID (assigned by the USB-IF)"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "idProduct")
	elem.displayFormat = "hex"
	elem.comment = "Product ID (assigned by the manufacturer)"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 2, name = "bcdDevice")
	elem.displayFormat = "hex"
	elem.comment = "Device release number in binary-coded decimal"
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
	elem.autoMethod = "countDescriptorsOfType"
	elem.autoMethodDetail = "ConfigurationDescriptor"
	elem.comment = "Number of possible configurations"
	desc.addElement(elem)

	return desc

def createConfigDescriptorTemplate():
	desc = DescriptorClass("ConfigurationDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 2
	elem.comment = "CONFIGURATION Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 2, name = "wTotalLength")
	elem.autoMethod = "descriptorSizeAllChildren"
	elem.comment = "Total length of data returned for this configuration"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumInterfaces")
	elem.autoMethod = "countChildrenOfType"
	elem.autoMethodDetail = "InterfaceDescriptor"
	elem.comment = "Number of interfaces supported by this configuration"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bConfigurationValue")
	elem.autoMethod = "indexOfDescriptor"
	elem.base = 1
	elem.comment = "Value to use as an argument to the SetConfiguration() request to select this configuration"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iConfiguration")
	elem.linkType = "stringIndex"
	elem.comment = "Index of string descriptor describing this configuration"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass("enum", size = 1, name = "Remote Wakeup")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 5
	elem.comment = "Configuration characteristics"
	elem.appendBitmap(bitmap)

	bitmap = DescriptorElementClass("enum", size = 1, name = "Self-powered")
	bitmap.enum = { "No": 0, "Yes": 1 };
	bitmap.offset = 6
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bMaxPower")
	elem.comment = ""
	elem.comment = "Maximum power consumption of the USB, device. Expressed in 2 mA units"
	desc.addElement(elem)

	return desc

def createStringDescriptorTemplate():
	desc = DescriptorClass("StringDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 3
	elem.comment = "STRING Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "string", name = "bString")
	desc.addElement(elem)

	return desc

def createInterfaceDescriptorTemplate():
	desc = DescriptorClass("InterfaceDescriptor")
	desc.allowedParents.append("ConfigurationDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 4
	elem.comment = "INTERFACE Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bInterfaceNumber")
	elem.autoMethod = "indexOfDescriptor"
	elem.comment = "Number of this interface. Zero-based value."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bAlternateSetting")
	elem.comment = "Value used to select this alternate setting"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumEndpoints")
	elem.autoMethod = "countChildrenOfType"
	elem.autoMethodDetail = "EndpointDescriptor"
	elem.comment = "Number of endpoints used by this interface"
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bInterfaceClass")
	elem.comment = "Class code (assigned by the USB-IF)."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceSubClass")
	elem.comment = "Subclass code (assigned by the USB-IF)."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceProtocol")
	elem.comment = "Protocol code (assigned by the USB)."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iInterface")
	elem.linkType = "stringIndex"
	elem.comment = "Index of string descriptor describing this interface"
	desc.addElement(elem)

	return desc

def createEndpointDescriptorTemplate():
	desc = DescriptorClass("EndpointDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
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
	desc.allowedParents.append("ConfigurationDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 6
	elem.comment = "Device Qualifier Type"
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 2, name = "bcdUSB")
	elem.enum = { "1.1": 0x0101, "2.0": 0x0200 }
	elem.value = 0x0200
	elem.comment = "USB specification version number"
	desc.addElement(elem)

	elem = createInterfaceClassCodes("bDeviceClass")
	elem.comment = "Class Code"
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bDeviceSubClass")
	elem.enum = { "Defined at interface level": 0x00, "Vendor specific": 0xff }
	elem.comment = "Subclass Code"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bDeviceProtocol")
	elem.comment = "Protocol Code"
	desc.addElement(elem)

	elem = DescriptorElementClass("enum", size = 1, name = "bMaxPacketSize0")
	elem.enum = { "8": 8, "16": 16, "32": 32, "64": 64 }
	elem.value = 64
	elem.comment = "Maximum packet size for other speed"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bNumConfigurations")
	elem.autoMethod = "countChildrenOfType:ConfigurationDescriptor"
	elem.comment = "Number of Other-speed Configurations"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bReserved")
	elem.comment = "Reserved for future use, must be zero"
	desc.addElement(elem)

	return desc

def createOtherSpeedConfigurationDescriptorTemplate():
	desc = createConfigDescriptorTemplate()
	desc.descriptorType = "OtherSpeedConfigurationDescriptor"

	for e in desc.elements:
		if e.name == "bDescriptorType":
			e.value = 7

	return desc

def createInterfaceAssociationDescriptorTemplate():
	desc = DescriptorClass("InterfaceAssociationDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
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
	elem.comment = "Size of this descriptor in bytes"
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
	templates.append(createOtherSpeedConfigurationDescriptorTemplate())
	templates.append(createInterfaceAssociationDescriptorTemplate())
	templates.append(createDFUFunctionDescriptorTemplate())

	return templates

