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

	desc.descriptiveString = "iProduct"

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

	desc.descriptiveString = "iConfiguration"

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

	desc.descriptiveString = "iInterface"

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

	desc.descriptiveString = "iFunction"

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


# USB AUDIO CLASS 2

def createUACbmControls(name, offset):
	bitmap = DescriptorElementClass(elementType = "enum", size = 1, name = name)
	bitmap.offset = offset
	bitmap.size = 2
	bitmap.enum = { "Off": 0, "read-only": 1, "read/write": 3 }
	return bitmap

UAC2SpatialLocations = { 	"Front Left - FL": 0,
				"Front Right - FR": 1,
				"Front Center - FC": 2,
				"Low Frequency Effects- LFE": 3,
				"Back Left - BL": 4,
				"Back Right - BR": 5,
				"Front Left of Center - FLC": 6,
				"Front Right of Center - FRC": 7,
				"Back Center - BC": 8,
				"Side Left - SL": 9,
				"Side Right - SR": 10,
				"Top Center - TC": 11,
				"Top Front Left - TFL": 12,
				"Top Front Center - TFC": 13,
				"Top Front Right - TFR": 14,
				"Top Back Left - TBL": 15,
				"Top Back Center - TBC": 16,
				"Top Back Right - TBR": 17,
				"Top Front Left of Center - TFLC": 18,
				"Top Front Right of Center - TFRC": 19,
				"Left Low Frequency Effects - LLFE": 20,
				"Right Low Frequency Effects - RLFE": 21,
				"Top Side Left - TSL": 22,
				"Top Side Right - TSR": 23,
				"Bottom Center - BC": 24,
				"Back Left of Center - BLC": 25,
				"Back Right of Center - BRC": 26,
				"Raw Data - RD": 31 }

def createUAC2SpatialLocations(name):
	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = name)

	for (k, v) in UAC2SpatialLocations.items():
		bitmap = DescriptorElementClass(elementType = "enum", size = 1, name = k)
		bitmap.size = 1
		bitmap.offset = v
		bitmap.enum = { "Off": 0, "On": 1 }
		elem.appendBitmap(bitmap)

	return elem


def createUAC2InterfaceHeaderDescriptorTemplate():
	desc = DescriptorClass("UAC2InterfaceHeaderDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bcdADC")
	elem.value = 0x200
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bCategory")
	elem.enum = { 	"FUNCTION_SUBCLASS_UNDEFINED": 0,
			"DESKTOP_SPEAKER": 1,
			"HOME_THEATER": 2,
			"MICROPHONE": 3,
			"HEADSET": 4,
			"TELEPHONE": 5,
			"CONVERTER": 6,
			"VOICE/SOUND_RECORDER": 7,
			"I/O_BOX": 8,
			"MUSICAL_INSTRUMENT": 9,
			"PRO-AUDIO": 0xa,
			"AUDIO/VIDEO": 0xb,
			"CONTROL_PANEL": 0xc,
			"OTHER": 0xff }
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "wTotalLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Total number of bytes returned for the class-specific AudioControl interface descriptor."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Latency Control", 0))
	desc.addElement(elem)

	return desc

def createUAC2InputTerminalDescriptorTemplate():
	desc = DescriptorClass("UAC2InputTerminalDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0x2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bTerminalID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 2, name = "wTerminalType")
	elem.enum = { 	"USB Undefined": 0x0100,
			"USB streaming": 0x0101,
			"USB vendor specific": 0x01ff,
			"Input Undefined": 0x0200,
			"Microphone": 0x0201,
			"Desktop microphone": 0x0202,
			"Personal microphone": 0x0203,
			"Omni-directional microphone": 0x0204,
			"Microphone array": 0x0205,
			"Processing microphone array": 0x0206 }
	elem.value = 0x0100
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bAssocTerminal")
	elem.linkType = "UAC2Terminal"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bCSourceID")
	elem.linkType = "UAC2Clock"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrChannels")
	desc.addElement(elem)

	elem = createUAC2SpatialLocations("bmChannelConfig")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iChannelNames")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Copy Protect Control", 0))
	elem.appendBitmap(createUACbmControls("Connector Control", 2))
	elem.appendBitmap(createUACbmControls("Overload Control", 4))
	elem.appendBitmap(createUACbmControls("Cluster Control", 6))
	elem.appendBitmap(createUACbmControls("Underflow Control", 8))
	elem.appendBitmap(createUACbmControls("Overflow Control", 10))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iTerminal")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iTerminal"

	return desc

def createUAC2OutputTerminalDescriptorTemplate():
	desc = DescriptorClass("UAC2OutputTerminalDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0x3
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bTerminalID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 2, name = "wTerminalType")
	elem.enum = { 	"USB Undefined": 0x0100,
			"USB streaming": 0x0101,
			"USB vendor specific": 0x01ff,
			"Output Undefined": 0x0300,
			"Speaker": 0x0301,
			"Headphones": 0x0302,
			"Head Mounted Display Audio": 0x0303,
			"Desktop speaker": 0x0304,
			"Room speaker": 0x0305,
			"Communication speaker": 0x0306,
			"Low frequency effects speaker": 0x0307 }
	elem.value = 0x0100
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bAssocTerminal")
	elem.linkType = "UAC2Terminal"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bCSourceID")
	elem.linkType = "UAC2Clock"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Copy Protect Control", 0))
	elem.appendBitmap(createUACbmControls("Connector Control", 2))
	elem.appendBitmap(createUACbmControls("Overload Control", 4))
	elem.appendBitmap(createUACbmControls("Cluster Control", 6))
	elem.appendBitmap(createUACbmControls("Underflow Control", 8))
	elem.appendBitmap(createUACbmControls("Overflow Control", 10))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iTerminal")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iTerminal"

	return desc

def createUAC2MixerUnitDescriptorTemplate():
	print "implement me"

def createUAC2SelectorUnitDescriptorTemplate():
	desc = DescriptorClass("UAC2SelectorUnitDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 5
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bUnitID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrInPins")
	desc.addElement(elem)

	elem = DescriptorElementArrayClass("baSourceID", "bNrInPins")
	elem.arrayLength = "given"
	elem.arrayLengthField = "bNrInPins"
	elem.arrayMemberType = "variable"
	elem.arrayMemberSize = 1
	desc.addElementArray(elem)


	#elem = DescriptorElementArrayClass("blaaaaa", "bUnitID")
	#elem.arrayLength = "dynamic"
	#elem.arrayMemberType = "variable"
	#elem.arrayMemberSize = 1
	#desc.addElementArray(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Selector Control", 0))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iSelector")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iSelector"

	return desc

def createUAC2FeatureUnitDescriptorTemplate():
	desc = DescriptorClass("UAC2FeatureUnitDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 6
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bUnitID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bSourceID")
	elem.linkType = "UAC2Unit"
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bmaControls", "bSourceID")
	arr.arrayLength = "dynamic"
	arr.arrayMemberType = "bitmap"
	arr.arrayMemberSize = 4
	arr.appendBitmap(createUACbmControls("Mute Control", 0))
	arr.appendBitmap(createUACbmControls("Volume Control", 2))
	arr.appendBitmap(createUACbmControls("Bass Control", 4))
	arr.appendBitmap(createUACbmControls("Mid Control", 6))
	arr.appendBitmap(createUACbmControls("Treble Control", 8))
	arr.appendBitmap(createUACbmControls("Graphic Equalizer Control", 10))
	arr.appendBitmap(createUACbmControls("Automatic Gain Control", 12))
	arr.appendBitmap(createUACbmControls("Delay Control", 14))
	arr.appendBitmap(createUACbmControls("Bass Boost Control", 16))
	arr.appendBitmap(createUACbmControls("Loudness Control", 18))
	arr.appendBitmap(createUACbmControls("Input Gain Control", 20))
	arr.appendBitmap(createUACbmControls("Input Gain Pad Control", 22))
	arr.appendBitmap(createUACbmControls("Phase Inverter Control", 24))
	arr.appendBitmap(createUACbmControls("Underflow Control", 26))
	arr.appendBitmap(createUACbmControls("Overfow Control", 28))
	desc.addElementArray(arr)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iFeature")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iFeature"

	return desc

def createUAC2ClockSourceDescriptorTemplate():
	desc = DescriptorClass("UAC2ClockSourceDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xa
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass(elementType = "enum", size = 2, name = "Clock type")
	bitmap.enum = { "External Clock": 0,
			"Internal fixed Clock": 1,
			"Internal variable Clock": 2,
			"Internal programmable Clock": 3 }
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass(elementType = "enum", size = 2, name = "Clock synchronized to SOF")
	bitmap.enum = { "No": 0, "Yes": 1 }
	elem.appendBitmap(bitmap)
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Clock Frequency Control", 0))
	elem.appendBitmap(createUACbmControls("Clock Validity Control", 2))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bAssocTerminal")
	elem.linkType = "UAC2Terminal"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iClockSource")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iClockSource"

	return desc

def createUAC2ClockSelectorUnitDescriptorTemplate():
	desc = DescriptorClass("UAC2ClockSelectorUnitDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xb
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrInPins")
	desc.addElement(elem)

	elem = DescriptorElementArrayClass("baCSourceID", "bNrInPins")
	elem.arrayLength = "given"
	elem.arrayLengthField = "bNrInPins"
	elem.arrayMemberType = "link"
	elem.arrayMemberLinkType = "UAC2Clock"
	elem.arrayMemberSize = 1
	desc.addElementArray(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Selector Control", 0))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iClockSelector")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iClockSelector"

	return desc

def createUAC2ClockMultiplierDescriptorTemplate():
	desc = DescriptorClass("UAC2ClockMultiplierDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xc
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bCSourceID")
	elem.linkType = "UAC2Clock"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Clock Numerator Control", 0))
	elem.appendBitmap(createUACbmControls("Clock Denominator Control", 2))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iClockMultiplier")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iClockMultiplier"

	return desc

def createUAC2SamplingRateConverterUnitDescriptorTemplate():
	desc = DescriptorClass("UAC2SamplingRateConverterUnitDescriptor")
	desc.allowedParents.append("InterfaceDescriptor")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "bLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Size of this descriptor in bytes"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xd
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bUnitID")
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bSourceID")
	elem.linkType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bSourceInID")
	elem.linkType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bSourceOutID")
	elem.linkType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iSRC")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iSRC"

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

	templates.append(createUAC2InterfaceHeaderDescriptorTemplate())
	templates.append(createUAC2InputTerminalDescriptorTemplate())
	templates.append(createUAC2OutputTerminalDescriptorTemplate())
	templates.append(createUAC2SelectorUnitDescriptorTemplate())
	templates.append(createUAC2FeatureUnitDescriptorTemplate())
	templates.append(createUAC2ClockSourceDescriptorTemplate())
	templates.append(createUAC2ClockSelectorUnitDescriptorTemplate())
	templates.append(createUAC2ClockMultiplierDescriptorTemplate())
	templates.append(createUAC2SamplingRateConverterUnitDescriptorTemplate())

	return templates

