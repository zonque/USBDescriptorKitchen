from Descriptor import *

langids = {
	"Afrikaans": 0x0436,
	"Albanian": 0x041c,
	"Arabic (Saudi Arabia)": 0x0401,
	"Arabic (Iraq)": 0x0801,
	"Arabic (Egypt)": 0x0c01,
	"Arabic (Libya)": 0x1001,
	"Arabic (Algeria)": 0x1401,
	"Arabic (Morocco)": 0x1801,
	"Arabic (Tunisia)": 0x1c01,
	"Arabic (Oman)": 0x2001,
	"Arabic (Yemen)": 0x2401,
	"Arabic (Syria)": 0x2801,
	"Arabic (Jordan)": 0x2c01,
	"Arabic (Lebanon)": 0x3001,
	"Arabic (Kuwait)": 0x3401,
	"Arabic (U.A.E.)": 0x3801,
	"Arabic (Bahrain)": 0x3c01,
	"Arabic (Qatar)": 0x4001,
	"Armenian.": 0x042b,
	"Assamese.": 0x044d,
	"Azeri (Latin)": 0x042c,
	"Azeri (Cyrillic)": 0x082c,
	"Basque": 0x042d,
	"Belarussian": 0x0423,
	"Bengali.": 0x0445,
	"Bulgarian": 0x0402,
	"Burmese": 0x0455,
	"Catalan": 0x0403,
	"Chinese (Taiwan)": 0x0404,
	"Chinese (PRC)": 0x0804,
	"Chinese (Hong Kong SAR, PRC)": 0x0c04,
	"Chinese (Singapore)": 0x1004,
	"Chinese (Macau SAR)": 0x1404,
	"Croatian": 0x041a,
	"Czech": 0x0405,
	"Danish": 0x0406,
	"Dutch (Netherlands)": 0x0413,
	"Dutch (Belgium)": 0x0813,
	"English (United States)": 0x0409,
	"English (United Kingdom)": 0x0809,
	"English (Australian)": 0x0c09,
	"English (Canadian)": 0x1009,
	"English (New Zealand)": 0x1409,
	"English (Ireland)": 0x1809,
	"English (South Africa)": 0x1c09,
	"English (Jamaica)": 0x2009,
	"English (Caribbean)": 0x2409,
	"English (Belize)": 0x2809,
	"English (Trinidad)": 0x2c09,
	"English (Zimbabwe)": 0x3009,
	"English (Philippines)": 0x3409,
	"Estonian": 0x0425,
	"Faeroese": 0x0438,
	"Farsi": 0x0429,
	"Finnish": 0x040b,
	"French (Standard)": 0x040c,
	"French (Belgian)": 0x080c,
	"French (Canadian)": 0x0c0c,
	"French (Switzerland)": 0x100c,
	"French (Luxembourg)": 0x140c,
	"French (Monaco)": 0x180c,
	"Georgian.": 0x0437,
	"German (Standard)": 0x0407,
	"German (Switzerland)": 0x0807,
	"German (Austria)": 0x0c07,
	"German (Luxembourg)": 0x1007,
	"German (Liechtenstein)": 0x1407,
	"Greek": 0x0408,
	"Gujarati.": 0x0447,
	"Hebrew": 0x040d,
	"Hindi.": 0x0439,
	"Hungarian": 0x040e,
	"Icelandic": 0x040f,
	"Indonesian": 0x0421,
	"Italian (Standard)": 0x0410,
	"Italian (Switzerland)": 0x0810,
	"Japanese": 0x0411,
	"Kannada.": 0x044b,
	"Kashmiri (India)": 0x0860,
	"Kazakh": 0x043f,
	"Konkani.": 0x0457,
	"Korean": 0x0412,
	"Korean (Johab)": 0x0812,
	"Latvian": 0x0426,
	"Lithuanian": 0x0427,
	"Lithuanian (Classic)": 0x0827,
	"Macedonian": 0x042f,
	"Malay (Malaysian)": 0x043e,
	"Malay (Brunei Darussalam)": 0x083e,
	"Malayalam.": 0x044c,
	"Manipuri": 0x0458,
	"Marathi.": 0x044e,
	"Nepali (India).": 0x0861,
	"Norwegian (Bokmal)": 0x0414,
	"Norwegian (Nynorsk)": 0x0814,
	"Oriya.": 0x0448,
	"Polish": 0x0415,
	"Portuguese (Brazil)": 0x0416,
	"Portuguese (Standard)": 0x0816,
	"Punjabi.": 0x0446,
	"Romanian": 0x0418,
	"Russian": 0x0419,
	"Sanskrit.": 0x044f,
	"Serbian (Cyrillic)": 0x0c1a,
	"Serbian (Latin)": 0x081a,
	"Sindhi": 0x0459,
	"Slovak": 0x041b,
	"Slovenian": 0x0424,
	"Spanish (Traditional Sort)": 0x040a,
	"Spanish (Mexican)": 0x080a,
	"Spanish (Modern Sort)": 0x0c0a,
	"Spanish (Guatemala)": 0x100a,
	"Spanish (Costa Rica)": 0x140a,
	"Spanish (Panama)": 0x180a,
	"Spanish (Dominican Republic)": 0x1c0a,
	"Spanish (Venezuela)": 0x200a,
	"Spanish (Colombia)": 0x240a,
	"Spanish (Peru)": 0x280a,
	"Spanish (Argentina)": 0x2c0a,
	"Spanish (Ecuador)": 0x300a,
	"Spanish (Chile)": 0x340a,
	"Spanish (Uruguay)": 0x380a,
	"Spanish (Paraguay)": 0x3c0a,
	"Spanish (Bolivia)": 0x400a,
	"Spanish (El Salvador)": 0x440a,
	"Spanish (Honduras)": 0x480a,
	"Spanish (Nicaragua)": 0x4c0a,
	"Spanish (Puerto Rico)": 0x500a,
	"Sutu": 0x0430,
	"Swahili (Kenya)": 0x0441,
	"Swedish": 0x041d,
	"Swedish (Finland)": 0x081d,
	"Tamil.": 0x0449,
	"Tatar (Tatarstan)": 0x0444,
	"Telugu.": 0x044a,
	"Thai": 0x041e,
	"Turkish": 0x041f,
	"Ukrainian": 0x0422,
	"Urdu (Pakistan)": 0x0420,
	"Urdu (India)": 0x0820,
	"Uzbek (Latin)": 0x0443,
	"Uzbek (Cyrillic)": 0x0843,
	"Vietnamese": 0x042a,
	"HID (Usage Data Descriptor)": 0x04ff,
	"HID (Vendor Defined 1)": 0xf0ff,
	"HID (Vendor Defined 2)": 0xf4ff,
	"HID (Vendor Defined 3)": 0xf8ff,
	"HID (Vendor Defined 4)": 0xfcff,
}

def createInterfaceClassCodes(name):
	elem = DescriptorElementClass("enum", size = 1, name = name)
	elem.enum = {
			"Defined at interface level": 0,
			"Audio": 1, "Conn": 2, "HID": 3, "Pysical": 4, "Still Image": 5, "Printer": 6,
			"Mass Storage": 7, "HUB": 8, "CDC Data": 9, "CSCID": 0xa, "Content Sec": 0xb,
			"Video": 0xd, "Misc": 0xe, "Wireless Controller": 0xe0,
			"App Specific": 0xef, "Vendor specific": 0xff
			}
	return elem

def createDeviceDescriptor():
	desc = DescriptorClass("Device")
	desc.allowedParents.append("Root")

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

	elem = DescriptorElementClass("variable", size = 1, name = "bDeviceSubClass")
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
	elem.autoMethodDetail = "Configuration"
	elem.comment = "Number of possible configurations"
	desc.addElement(elem)

	desc.descriptiveString = "iProduct"

	return desc

def createConfigDescriptor():
	desc = DescriptorClass("Configuration")
	desc.allowedParents.append("Root")

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
	elem.autoMethodDetail = "Interface"
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

def createStringDescriptor():
	desc = DescriptorClass("String")
	desc.allowedParents.append("Root")
	desc.dependsOnDescriptor = "StringZero"

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 3
	elem.comment = "STRING Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "string", name = "bString")
	desc.addElement(elem)

	return desc

def createStringDescriptorZero():
	desc = DescriptorClass("StringZero")
	desc.allowedParents.append("Root")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 3
	elem.comment = "STRING Descriptor Type"
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bDescriptorType")
	arr.arrayLength = "dynamic"
	member = DescriptorElementArrayMemberClass(memberType = "enum", size = 2, name = "wLANGID")
	member.enum = langids
	member.value = 0x407
	arr.appendMember(member)
	desc.addElementArray(arr)

	return desc

def createInterfaceDescriptor():
	desc = DescriptorClass("Interface")
	desc.allowedParents.append("Configuration")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 4
	elem.comment = "INTERFACE Descriptor Type"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterfaceNumber")
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

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bInterfaceSubClass")
	elem.comment = "Subclass code (assigned by the USB-IF)."
	elem.enum = {	"0": 0, "1": 1, "2": 2,
			"AUDIOCONTROL": 0x01, "MIDISTREAMING": 0x03
		}
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

def createEndpointDescriptor():
	desc = DescriptorClass("Endpoint")
	desc.allowedParents.append("Interface")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 5
	elem.comment = "ENDPOINT descriptor"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bEndpointAddress")
	bitmap = DescriptorElementClass("enum", size = 4, name = "Endpoint Number")
	for i in range(1, 16):
		bitmap.enum[str(i)] = i
	bitmap.offset = 0
	elem.appendBitmap(bitmap)
	bitmap = DescriptorElementClass("enum", size = 1, name = "Direction")
	bitmap.enum = { "OUT": 0, "IN": 1 };
	bitmap.offset = 7
	elem.appendBitmap(bitmap)
	elem.suggestionType = "EndpointAddress"
	elem.value = 1
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
	elem.comment = "Maximum packet size this endpoint is capable of sending or receiving when this configuration is selected."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInterval")
	elem.comment = "Interval for polling endpoint for data transfers. Expressed in frames or microframes depending on the device operating speed (i.e., either 1 millisecond or 125 us units)"
	desc.addElement(elem)

	return desc

def createDeviceQualifier():
	desc = DescriptorClass("DeviceQualifier")
	desc.allowedParents.append("Configuration")

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

	elem = DescriptorElementClass("variable", size = 1, name = "bDeviceSubClass")
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

def createOtherSpeedConfigurationDescriptor():
	desc = createConfigDescriptor()
	desc.descriptorType = "OtherSpeedConfigurationDescriptor"

	for e in desc.elements:
		if e.name == "bDescriptorType":
			e.value = 7

	return desc

def createInterfaceAssociationDescriptor():
	desc = DescriptorClass("InterfaceAssociation")
	desc.allowedParents.append("Configuration")

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

def createDFUFunctionDescriptor():
	desc = DescriptorClass("DFUFunctional")
	desc.allowedParents.append("Interface")

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

