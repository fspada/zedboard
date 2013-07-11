set_directive_interface -mode ap_none test_48 a
set_directive_interface -mode ap_none test_48 b
set_directive_interface -mode ap_ctrl_hs -register test_48 return
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_48 a
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_48 b
set_directive_resource -core AXI4LiteS -metadata "-bus_bundle slv0" test_48 return
