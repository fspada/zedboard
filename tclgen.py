import os

def gen_tcl_core(file_source, func_name, clock_period, ip_interfaces, from_int, to_int):
	os.system("cp -r src/ cores/")
	os.system("mkdir -p cores/hls/core_"+func_name+"/solution1/")

	tcl_directives = open("cores/hls/core_"+func_name+"/solution1/directives.tcl","w")

	if not ip_interfaces:
		tcl_directives.write("set_directive_interface -mode ap_none "+ func_name + " a\n" +
							 "set_directive_interface -mode ap_ctrl_hs -register "+ func_name + " return\n" +
							 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' a\n' +
							 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" '+ func_name +' return\n')
	else:
		for (ip,interf,m_s,ty) in ip_interfaces:
			if ty=='AXIStream':
				interface = 'ap_fifo'
				resource = 'AXI4Stream'
			else:
				interface = 'ap_none'
				resource = 'AXI4LiteS'
			if m_s == 'S':
				if from_int == 'BUS':
					tcl_directives.write("set_directive_interface -mode ap_none "+ func_name + " "+interf+"\n" +
										 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle '+interf+'" '+ func_name +' '+interf+'\n')				
				else:
					tcl_directives.write("set_directive_interface -mode "+ interface +" "+ func_name + " "+interf+"\n" +
										 'set_directive_resource -core '+resource+' -metadata "-bus_bundle '+interf+'" '+ func_name +' '+interf+'\n')
			else:
				if to_int == 'BUS':
					tcl_directives.write("set_directive_interface -mode ap_ctrl_hs -register "+ func_name + " return\n" +
										 'set_directive_resource -core AXI4LiteS -metadata "-bus_bundle '+interf+'" '+ func_name +' return\n')
				else:
					tcl_directives.write("set_directive_interface -mode ap_fifo "+ func_name + " "+interf+"\n" +
										 'set_directive_resource -core AXI4Stream -metadata "-bus_bundle '+interf+'" '+ func_name +' '+interf+'\n')

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

def gen_tcl_sys(cores):
	os.system("mkdir -p zedboard_prj/")
	tcl_sys_script = open("zedboard_prj/script_sys.tcl","w")

	tcl_sys_script.write("create_project vivado_prj ./vivado_prj -part xc7z020clg484-1 -force\n" +
						 "set_property board em.avnet.com:zynq:zed:d [current_project]\n" +
						 'create_bd_design "zynq_bd"\n' +
						 "startgroup\n" +
						 "create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.2 processing_system7_1\n" +
						 "endgroup\n" +
						 'apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 -config {make_external "FIXED_IO, DDR" }  [get_bd_cells /processing_system7_1]\n' +
						 "startgroup\n"+
						 "set_property -dict [list CONFIG.PCW_USE_FABRIC_INTERRUPT {1}] [get_bd_cells /processing_system7_1]\n" +
						 "endgroup\n" +
						 "startgroup\n" +
						 "set_property -dict [list CONFIG.PCW_IRQ_F2P_INTR {1}] [get_bd_cells /processing_system7_1]\n" +
						 "endgroup\n"+
						 "startgroup\n" +
						 "create_bd_cell -type ip -vlnv xilinx.com:ip:xlconcat:1.0 xlconcat_1\n" +
						 "endgroup\n" +
						 "set_property -dict [list CONFIG.NUM_PORTS {"+ str(len(cores)) +"}] [get_bd_cells /xlconcat_1]\n" +
						 "connect_bd_net [get_bd_pins /processing_system7_1/IRQ_F2P] [get_bd_pins /xlconcat_1/dout]\n" +
						 "set_property ip_repo_paths  {"+ ' '.join(map(lambda c: "../cores/hls/core_"+ c +"/solution1/impl/ip",cores)) +"} [current_fileset]\n" + 
						 "update_ip_catalog\n")
	i = 0
	for c in cores:
		tcl_sys_script.write("startgroup\n"+
							 "create_bd_cell -type ip -vlnv xilinx.com:hls:"+ c +":1.0 "+ c +"_1\n" +
							 "endgroup\n" +
							 'apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/processing_system7_1/M_AXI_GP0" }  [get_bd_intf_pins /'+c+'_1/S_AXI_SLV0]\n' +
							 "connect_bd_net [get_bd_pins /"+c+"_1/interrupt] [get_bd_pins /xlconcat_1/In"+str(i)+"]\n")
		i += 1
	tcl_sys_script.write("save_bd_design\n" +
						 "validate_bd_design\n" +
						 "generate_target {synthesis simulation implementation} [get_files  ./vivado_prj/vivado_prj.srcs/sources_1/bd/zynq_bd/zynq_bd.bd]\n" +
						 "make_wrapper -files [get_files ./vivado_prj/vivado_prj.srcs/sources_1/bd/zynq_bd/zynq_bd.bd] -top\n" +
						 "import_files -force -norecurse ./vivado_prj/vivado_prj.srcs/sources_1/bd/zynq_bd/hdl/zynq_bd_wrapper.v\n" +
						 "update_compile_order -fileset sources_1\n" +
						 "update_compile_order -fileset sim_1\n" +
						 "#synth_design\n" +
						 "launch_runs synth_1\n" +
						 "wait_on_run synth_1\n" +
						 "#launch_runs impl_1\n" +
						 "#wait_on_run impl_1\n" +
						 "launch_runs impl_1 -to_step write_bitstream\n" +
						 "wait_on_run impl_1\n" +
						 "exit\n")
	tcl_sys_script.close()

