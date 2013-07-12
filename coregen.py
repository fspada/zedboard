from tclgen import *
import xml.etree.ElementTree as Xml
import os

xmlPath = "./xml/final_0.xml"

doc = Xml.parse(xmlPath)

blackListImpl = ["BUS"]

mapping_task = filter(lambda x: x.attrib["component"] not in blackListImpl,doc.findall(".//mapping"))

taskHW = filter(lambda x: x.find("component").attrib["type"]=="HW", 
			map(lambda x: doc.find(".//implementation[@id='" + x.attrib["impl"] +"']"),mapping_task))

blackListFunc = ["COMMUNICATION","END"]
funcHW = filter(lambda x: x.find('specs').attrib['value'] not in blackListFunc,
			map(lambda x: doc.find(".//partition/task[@id='" + x.find('task').attrib["id"] +"']"),taskHW))

clock_period = doc.find("./architecture/system/system/specs[@name='clock']").attrib['value']
fileCode = doc.find(".//application/files/file").attrib['name']
core = list(set(map(lambda x: x.find('specs').attrib['value'],funcHW)))

fileCodeTEST = "test.c"
coreTEST = map(lambda x: "test_"+x, core)

for c in coreTEST:
	gen_tcl_core(fileCodeTEST,c,clock_period)
	os.chdir("./cores/hls")
	os.system("vivado_hls -f core_"+c+"/solution1/script.tcl") #trovi il core in ./core_prj/solution1/impl/ip
	os.chdir("../..")

