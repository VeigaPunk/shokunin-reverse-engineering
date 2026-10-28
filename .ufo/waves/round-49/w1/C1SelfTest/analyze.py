import json,sys
C=('carrier_present','carrier_pin_ok','carrier_size_ok','carrier_fresh_ok','layout_ok','carve_ok','oracle_ok','tree_ok','receipt_present','receipt_fresh','evidence_envelope_ok','subject_pin_ok','operation_ok','handler_ok','chunks_ok','oracle_hits_ok','gaps_ok','nonregular_unpublished_ok','path_shape_ok','run_provenance_ok','evidence_id_ok','projection_ok')
B=('province_core_section','province_core_row','frontier_note','entry_present','sourced','coverage_map_row','carriers_spec_ok','gap_rule_ok','endianness_coverage','family_coverage','frozen_tables_valid','oracle_tool_ok')
cov={x:[] for x in C+B}
for l in open(sys.argv[1]):
    if not l.startswith('DETAIL'):continue
    _,n,j=l.rstrip('\n').split('\t',2);d=json.loads(j)
    f=d.get('failing',[])
    print(d['exit'],n[:70],'|',(sorted(f) if len(f)<8 else str(len(f))+' failing'),'|',d.get('reason') or '','|',d.get('drift') or '', '|bind_false=',d.get('bindings_false'))
    if len(f)>=8: continue   # skip do-nothing/receipt-missing mass cases for coverage? keep separate
    for x in f:
        k=x[2:] if x.startswith('b:') else x.split(':',1)[1]
        cov[k].append(n[:40])
print()
for k in C+B: print(k,len(cov[k]),cov[k][:3] if cov[k] else '  <-- NONE (excluding mass-fail cases)')
