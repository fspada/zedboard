import xml.etree.ElementTree as Xml

xmlPath = "./xml/final_0.xml"
# xmlFile = os.open(xmlPath, "r")

doc = Xml.parse(xmlPath)

# for elem in doc.findall(".//memory_element"):
# 	print elem._children

blackListImpl = ["BUS"]

mapping_task = filter(lambda x: x.attrib["component"] not in blackListImpl,doc.findall(".//mapping"))

taskHW = filter(lambda x: x.find("component").attrib["type"]=="HW", 
			map(lambda x: doc.find(".//implementation[@id='" + x.attrib["impl"] +"']"),mapping_task))

blackListFunc = ["COMMUNICATION","END"]
funcHW = filter(lambda x: x.find('specs').attrib['value'] not in blackListFunc,
			map(lambda x: doc.find(".//partition/task[@id='" + x.find('task').attrib["id"] +"']"),taskHW))

for f in funcHW:
	print f[0].attrib['value']

for t in taskHW:
	print t.find('task').attrib["id"]

# xmlFile.close()