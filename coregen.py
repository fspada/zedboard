from tclgen import *
import xml.etree.ElementTree as Xml
import os

xmlPath = "./xml/final_0.xml"

doc = Xml.parse(xmlPath)

blackListImpl = ["BUS"]

mapping_task = filter(lambda x: x.attrib["component"] not in blackListImpl,doc.findall(".//mapping"))

implHW = filter(lambda x: x.find("component").attrib["type"]=="HW", 
			map(lambda x: doc.find(".//implementation[@id='" + x.attrib["impl"] +"']"),mapping_task))

taskHW = map(lambda x: doc.find(".//partition/task[@id='" + x.find('task').attrib["id"] +"']"),implHW)

blackListFunc = ["COMMUNICATION","END"]
funcHW = filter(lambda x: x.find('specs').attrib['value'] not in blackListFunc,taskHW)

ip_hw_name = map(lambda x: x.attrib['component'],filter(lambda x: x.attrib['task'] in map(lambda x: x.attrib['id'],taskHW), mapping_task))
print ip_hw_name,'\n'

axiLite_interface = doc.find("./architecture/system/communication_elements/communication_element[@id='axiLite']/interface").attrib['name']
#print axiLite_interface,'\n'

virtual_link = map(lambda x: (x.attrib['master'],x.attrib['slave']), doc.findall("./architecture/system/system/communication_elements/communication_element/virtual/link"))
#print virtual_link,'\n'

master_v_link = map(lambda x: x[0], virtual_link)
slave_v_link = map(lambda x: x[1], virtual_link)

link_ip_hw = map(lambda x: map(lambda y: (x, y.attrib['name'], 'M' if y.attrib['name'] in master_v_link else 'S', y.attrib['type']), 
							doc.findall("./architecture/system/system/processing_elements/processing_element[@id='"+x+"']/interface")),ip_hw_name)
print link_ip_hw,'\n'


#id_task_HW = map(lambda x: x.attrib['id'], taskHW)
value_funcHW = map(lambda x: x.find('specs').attrib['value'],funcHW)
vfunc_ipname = zip(value_funcHW, ip_hw_name)
print vfunc_ipname,'\n'


ip_master = []
pe = doc.findall("./architecture/system/system/processing_elements/processing_element")
for m in master_v_link:
	pe_with_m = filter(lambda x: m in map(lambda y: y.attrib['name'], x.findall("./interface")), pe)
	if pe_with_m:
		ip_master.append((pe_with_m[0].attrib['id'], m))
	else:
		ip_master.append(('BUS',axiLite_interface))
#print ip_master
ip_slave = []
for s in slave_v_link:
	pe_with_s = filter(lambda x: s in map(lambda y: y.attrib['name'], x.findall("./interface")), pe)
	if pe_with_s:
		ip_slave.append((pe_with_s[0].attrib['id'], s))
	else:
		ip_slave.append(('BUS',axiLite_interface))
#print ip_slave
ip_connections = zip(ip_master,ip_slave)
print ip_connections,'\n'



clock_period = doc.find("./architecture/system/system/specs[@name='clock_period']").attrib['value']
fileCode = doc.find(".//application/files/file").attrib['name']
core = list(set(value_funcHW))

fileCodeTEST = "test.c"
#coreTEST = map(lambda x: "test_"+x, core)

for (f,ip) in vfunc_ipname:
	#print ("test_"+str(f),ip)
	ip_interfaces = filter(lambda x: x[0][0]==ip if x else False, link_ip_hw)
	if ip_interfaces:
		ip_interfaces = ip_interfaces[0]
	ip_master_conn = filter(lambda x: x[0][0]==ip and x[1][0] in ip_hw_name, ip_connections)
	if ip_master_conn:
		to_int = ip_master_conn[0][1][0]
	else:
		to_int = 'BUS'
	ip_slave_conn = filter(lambda x: x[1][0]==ip and x[0][0] in ip_hw_name, ip_connections)
	from_int = {}
	if ip_slave_conn:
		for i in ip_slave_conn:
			from_int[i[1]] = i[0][0]
	else:
		from_int = 'BUS'
	print from_int
	gen_tcl_core(fileCodeTEST,"test_"+str(f),clock_period,ip_interfaces, from_int, to_int)
	os.chdir("./cores/hls")
	os.system("vivado_hls -f core_"+"test_"+str(f)+"/solution1/script.tcl") #trovi il core in ./core_prj/solution1/impl/ip
	os.chdir("../..")

# gen_tcl_sys(coreTEST)
# os.chdir("./zedboard_prj")
# os.system("vivado -mode tcl -source script_sys.tcl")
# os.chdir("..")