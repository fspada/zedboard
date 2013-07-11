import os

def gen_tcl_core(file_source,func_name,clock_period):
	os.system("cp -r src/ cores/src/")
	os.system("mkdir -p cores/hls/core_"+func_name+"/solution1/")

	tcl_directives = open("cores/hls/core_"+func_name+"/solution1/directives.tcl","w")

	tcl_directives.write("set_directive_interface -mode ap_none "+ func_name + " a\n")
	tcl_directives.write("set_directive_interface -mode ap_none "+ func_name + " b\n")
	tcl_directives.write("set_directive_interface -mode ap_ctrl_hs -register "+ func_name + " return\n")

	tcl_directives.write('set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' a\n')
	tcl_directives.write('set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' b\n')
	tcl_directives.write('set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' return\n')

	tcl_directives.close()

	tcl_script = open("cores/hls/core_"+func_name+"/solution1/script.tcl","w")

	tcl_script.write("open_project cores/hls/core_"+func_name+"\n")
	tcl_script.write("set_top "+func_name+"\n")
	tcl_script.write("add_files cores/src/"+file_source+"\n")
	tcl_script.write("open_solution cores/hls/core_"+func_name+"solution1"+"\n")
	tcl_script.write("set_part {xc7z020clg484-1}\n")
	tcl_script.write("create_clock -period "+clock_period+"\n")

	tcl_script.write('source "cores/hls/core_'+func_name+'/solution1/directives.tcl"\n')
	tcl_script.write("csynth_design\n")
	tcl_script.write("export_design\n")
	tcl_script.write("exit\n")

	tcl_script.close()

def gen_tcl_sys():
	print "Unimplemented method"

