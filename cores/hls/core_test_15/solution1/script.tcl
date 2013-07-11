open_project cores/hls/core_test_15
set_top test_15
add_files cores/src/test.c
open_solution cores/hls/core_test_15solution1
set_part {xc7z020clg484-1}
create_clock -period 10
source "cores/hls/core_test_15/solution1/directives.tcl"
csynth_design
export_design
exit
