
def checkInterfaces(descriptorList, output):
	issues = 0

	lastInterface = -1
	expectedInterface = 0
	expectedAlt = 0

	for d in descriptorList:
		if d.descriptorType == "Interface":
			interfaceNumber = d.getValue("bInterfaceNumber")
			interfaceAlt = d.getValue("bAlternateSetting")

			if interfaceNumber != lastInterface:
				expectedAlt = 0
				expectedInterface += 1
			else:
				expectedAlt += 1

			if ((interfaceNumber != expectedInterface) or
			    (interfaceAlt != expectedAlt)):
				output.AppendText("ERROR: Interface bInterfaceNumber/bAlternateSetting: expected %d/%d, got %d/%d\n" %
					(expectedInterface, expectedAlt, interfaceNumber, interfaceAlt))
				issues += 1

	return issues

def doCheck(descriptorList, output):
	issues = 0

	for d in descriptorList:
		if d.descriptorType == "Configuration":
			issues += checkInterfaces(d.children, output)

	return issues
