open_project cores/hls/core_test_37
set_top test_37
add_files cores/src/test.c
open_solution cores/hls/core_test_37solution1
set_part {xc7z020clg484-1}
create_clock -period 10
source "cores/hls/core_test_37/solution1/directives.tcl"
csynth_design
export_design
exit
