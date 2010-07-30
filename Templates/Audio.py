from Descriptor import *

# USB AUDIO CLASS 2

def createUACbmControls(name, offset):
	bitmap = DescriptorElementClass(elementType = "enum", size = 1, name = name)
	bitmap.offset = offset
	bitmap.size = 2
	bitmap.enum = { "Off": 0, "read-only": 1, "read/write": 3 }
	return bitmap

UAC2SpatialLocations = {
				"Front Left - FL": 0,
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
				"Raw Data - RD": 31
			}

def createUAC2SpatialLocations(name):
	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = name)

	for (k, v) in UAC2SpatialLocations.items():
		bitmap = DescriptorElementClass(elementType = "enum", size = 1, name = k)
		bitmap.size = 1
		bitmap.offset = v
		bitmap.enum = { "Off": 0, "On": 1 }
		elem.appendBitmap(bitmap)

	return elem


def createUAC2InterfaceHeaderDescriptor():
	desc = DescriptorClass("UAC2InterfaceHeader")
	desc.allowedParents.append("Interface")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 2, name = "bcdADC")
	elem.value = 0x200
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bCategory")
	elem.enum = {
			"FUNCTION_SUBCLASS_UNDEFINED": 0,
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
	elem.autoMethod = "descriptorSizeAllChildren"
	elem.comment = "Total number of bytes returned for the class-specific AudioControl interface descriptor."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Latency Control", 0))
	desc.addElement(elem)

	return desc

def createUAC2InputTerminalDescriptor():
	desc = DescriptorClass("UAC2InputTerminal")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0x2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bTerminalID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 2, name = "wTerminalType")
	elem.enum = {
			"USB Undefined": 0x0100,
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

def createUAC2OutputTerminalDescriptor():
	desc = DescriptorClass("UAC2OutputTerminal")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0x3
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bTerminalID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 2, name = "wTerminalType")
	elem.enum = {
			"USB Undefined": 0x0100,
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

def createUAC2MixerUnitDescriptor():
	print "implement me"

def createUAC2SelectorUnitDescriptor():
	desc = DescriptorClass("UAC2SelectorUnit")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 5
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bUnitID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrInPins")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bNrInPins")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bNrInPins"
	member = DescriptorElementArrayMemberClass(memberType = "link", size = 1, name = "baSourceID")
	member.linkType = "UAC2Unit"
	arr.appendMember(member)
	desc.addElementArray(arr)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Selector Control", 0))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iSelector")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iSelector"

	return desc

def createUAC2FeatureUnitDescriptor():
	desc = DescriptorClass("UAC2FeatureUnit")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 6
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bUnitID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "bSourceID")
	elem.linkType = "UAC2Unit"
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bSourceID")
	arr.arrayLength = "dynamic"
	member = DescriptorElementArrayMemberClass(memberType = "bitmap", size = 4, name = "bmaControls")
	member.appendBitmap(createUACbmControls("Mute Control", 0))
	member.appendBitmap(createUACbmControls("Volume Control", 2))
	member.appendBitmap(createUACbmControls("Bass Control", 4))
	member.appendBitmap(createUACbmControls("Mid Control", 6))
	member.appendBitmap(createUACbmControls("Treble Control", 8))
	member.appendBitmap(createUACbmControls("Graphic Equalizer Control", 10))
	member.appendBitmap(createUACbmControls("Automatic Gain Control", 12))
	member.appendBitmap(createUACbmControls("Delay Control", 14))
	member.appendBitmap(createUACbmControls("Bass Boost Control", 16))
	member.appendBitmap(createUACbmControls("Loudness Control", 18))
	member.appendBitmap(createUACbmControls("Input Gain Control", 20))
	member.appendBitmap(createUACbmControls("Input Gain Pad Control", 22))
	member.appendBitmap(createUACbmControls("Phase Inverter Control", 24))
	member.appendBitmap(createUACbmControls("Underflow Control", 26))
	member.appendBitmap(createUACbmControls("Overfow Control", 28))
	arr.appendMember(member)
	desc.addElementArray(arr)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iFeature")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iFeature"

	return desc

def createUAC2ClockSourceDescriptor():
	desc = DescriptorClass("UAC2ClockSource")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xa
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	elem.suggestionType = "UAC2Clock"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "bitmap", size = 1, name = "bmAttributes")
	bitmap = DescriptorElementClass(elementType = "enum", size = 2, name = "Clock type")
	bitmap.enum = {
			"External Clock": 0,
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

def createUAC2ClockSelectorUnitDescriptor():
	desc = DescriptorClass("UAC2ClockSelectorUnit")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xb
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	elem.suggestionType = "UAC2Clock"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrInPins")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bNrInPins")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bNrInPins"
	member = DescriptorElementArrayMemberClass(memberType = "link", size = 1, name = "baCSourceID")
	member.linkType = "UAC2Clock"
	print "memberType %s" % member.memberType
	arr.appendMember(member)
	desc.addElementArray(arr)

	elem = DescriptorElementClass(elementType = "bitmap", size = 4, name = "bmControls")
	elem.appendBitmap(createUACbmControls("Selector Control", 0))
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iClockSelector")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iClockSelector"

	return desc

def createUAC2ClockMultiplierDescriptor():
	desc = DescriptorClass("UAC2ClockMultiplier")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xc
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	elem.suggestionType = "UAC2Clock"
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

def createUAC2SamplingRateConverterUnitDescriptor():
	desc = DescriptorClass("UAC2SamplingRateConverterUnit")
	desc.allowedParents.append("UAC2InterfaceHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0xd
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bClockID")
	elem.suggestionType = "UAC2Clock"
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

def createAudioControlHeaderDescriptor():
	desc = DescriptorClass("AudioControlHeader")
	desc.allowedParents.append("Interface")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 2, name = "bcdMSC")
	elem.value = 0x100
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "wTotalLength")
	elem.autoMethod = "descriptorSizeAllChildren"
	elem.comment = "Total number of bytes returned for the class-specific AudioControl interface descriptor."
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bInCollection")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bInCollection")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bInCollection"

	member = DescriptorElementArrayMemberClass(memberType = "variable", size = 1, name = "baInterfaceNr")
	arr.appendMember(member)
	desc.addElementArray(arr)

	return desc

def createMIDIStreamingHeaderDescriptor():
	desc = DescriptorClass("MIDIStreamingHeader")
	desc.allowedParents.append("AudioControlHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 1
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 2, name = "bcdMSC")
	elem.value = 0x100

	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "auto", size = 1, name = "wTotalLength")
	elem.autoMethod = "descriptorSize"
	elem.comment = "Total number of bytes returned for the class-specific AudioControl interface descriptor."
	desc.addElement(elem)

	return desc

def createMIDIInJackDescriptor():
	desc = DescriptorClass("MIDIInJack")
	desc.allowedParents.append("AudioControlHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bDescriptorSubtype")
	elem.enum = { "MIDI_IN_JACK": 0x02, "MIDI_OUT_JACK": 0x03 }
	elem.value = 2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bJackType")
	elem.enum = { "EMBEDDED": 0x01, "EXTERNAL": 0x02 }
	elem.value = 0x01
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bJackID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iJack")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iJack"

	return desc

def createMIDIOutJackDescriptor():
	desc = DescriptorClass("MIDIOutJack")
	desc.allowedParents.append("AudioControlHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x24
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bDescriptorSubtype")
	elem.enum = { "MIDI_IN_JACK": 0x02, "MIDI_OUT_JACK": 0x03 }
	elem.value = 2
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "enum", size = 1, name = "bJackType")
	elem.enum = { "EMBEDDED": 0x01, "EXTERNAL": 0x02 }
	elem.value = 0x01
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bJackID")
	elem.suggestionType = "UAC2Unit"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNrInputPins")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bNrInputPins")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bNrInputPins"
	member = DescriptorElementArrayMemberClass(memberType = "link", size = 1, name = "BaSourceID")
	member.linkType = "MIDIID"
	arr.appendMember(member)
	desc.addElementArray(arr)

	elem = DescriptorElementClass(elementType = "link", size = 1, name = "iJack")
	elem.linkType = "stringIndex"
	desc.addElement(elem)

	desc.descriptiveString = "iJack"

	return desc

def createMIDIEndpointDescriptor():
	desc = DescriptorClass("MIDIEndpoint")
	desc.allowedParents.append("AudioControlHeader")

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorType")
	elem.value = 0x25
	elem.comment = "CS_ENDPOINT"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "constant", size = 1, name = "bDescriptorSubtype")
	elem.value = 0x01
	elem.comment = "MS_GENERAL"
	desc.addElement(elem)

	elem = DescriptorElementClass(elementType = "variable", size = 1, name = "bNumEmbMIDIJack")
	desc.addElement(elem)

	arr = DescriptorElementArrayClass("bNumEmbMIDIJack")
	arr.arrayLength = "given"
	arr.arrayLengthField = "bNumEmbMIDIJack"
	member = DescriptorElementArrayMemberClass(memberType = "link", size = 1, name = "baAssocJackID")
	member.linkType = "MIDIID"
	arr.appendMember(member)
	desc.addElementArray(arr)

	return desc

