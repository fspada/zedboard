set_directive_interface -mode ap_none test_25 a
set_directive_interface -mode ap_none test_25 b
set_directive_interface -mode ap_ctrl_hs -register test_25 return
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_25 a
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_25 b
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_25 return
