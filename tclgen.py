import os

def gen_tcl_core(file_source,func_name,clock_period):
	os.system("cp -r src/ cores/")
	os.system("mkdir -p cores/hls/core_"+func_name+"/solution1/")

	tcl_directives = open("cores/hls/core_"+func_name+"/solution1/directives.tcl","w")

	tcl_directives.write("set_directive_interface -mode ap_none "+ func_name + " a\n" +
						 "set_directive_interface -mode ap_none "+ func_name + " b\n" +
						 "set_directive_interface -mode ap_ctrl_hs -register "+ func_name + " return\n" +
						 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' a\n' +
						 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' b\n' +
						 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' return\n')

	tcl_directives.close()

	tcl_script = open("cores/hls/core_"+func_name+"/solution1/script.tcl","w")

	tcl_script.write("open_project core_"+func_name+"\n" +
					 "set_top "+func_name+"\n" +
					 "add_files ../src/"+file_source+"\n" +
					 "open_solution solution1\n" +
					 "set_part {xc7z020clg484-1}\n" +
					 "create_clock -period "+clock_period+"\n" +
					 'source "core_'+func_name+'/solution1/directives.tcl"\n' +
					 "csynth_design\n" +
					 "export_design\n" +
					 "exit\n")

	tcl_script.close()

def gen_tcl_sys():
	print "Unimplemented method"

