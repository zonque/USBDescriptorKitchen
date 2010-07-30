from Descriptor import *
from Basic import *
from Audio import *
from HID import *

def createTemplates():
	templates = []

	templates.append(createDeviceDescriptor())
	templates.append(createConfigDescriptor())
	templates.append(createStringDescriptor())
	templates.append(createStringDescriptorZero())
	templates.append(createInterfaceDescriptor())
	templates.append(createEndpointDescriptor())
	templates.append(createDeviceQualifier())
	templates.append(createOtherSpeedConfigurationDescriptor())
	templates.append(createInterfaceAssociationDescriptor())
	templates.append(createDFUFunctionDescriptor())

	templates.append(createUAC2InterfaceHeaderDescriptor())
	templates.append(createUAC2InputTerminalDescriptor())
	templates.append(createUAC2OutputTerminalDescriptor())
	templates.append(createUAC2SelectorUnitDescriptor())
	templates.append(createUAC2FeatureUnitDescriptor())
	templates.append(createUAC2ClockSourceDescriptor())
	templates.append(createUAC2ClockSelectorUnitDescriptor())
	templates.append(createUAC2ClockMultiplierDescriptor())
	templates.append(createUAC2SamplingRateConverterUnitDescriptor())

	templates.append(createAudioControlHeaderDescriptor())
	templates.append(createMIDIStreamingHeaderDescriptor())
	templates.append(createMIDIInJackDescriptor())
	templates.append(createMIDIOutJackDescriptor())
	templates.append(createMIDIEndpointDescriptor())

	templates.append(createHIDDescriptor())

	return templates
