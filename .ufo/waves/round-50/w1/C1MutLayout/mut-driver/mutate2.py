import concurrent.futures as cf, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate as m
M2 = [
 ('M36','receipt_fresh: freeze itself accepted as first add',"d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)","d['receipt_fresh'] = bool(add) and is_ancestor(root, freeze, add)"),
 ('M37','receipt_fresh: first_add without --diff-filter=A',"'log', '--diff-filter=A', '--format=%H'","'log', '--format=%H'"),
 ('M38','chunks_ok forced true',"d['chunks_ok'] = not chunk_failed(env)","d['chunks_ok'] = True"),
 ('M39','CLAUSES tuple drops layout_ok',"'carrier_fresh_ok', 'layout_ok',","'carrier_fresh_ok',"),
 ('M40','CLAUSES tuple drops projection_ok (rerun clause unconjoined)',"'evidence_id_ok',\n           'projection_ok')","'evidence_id_ok')"),
 ('M41','CLAUSES tuple drops evidence_id_ok',"'run_provenance_ok', 'evidence_id_ok',","'run_provenance_ok',"),
 ('M42','provenance: scratch segment test dropped',"    if PROV_SEGMENT not in output_directory:","    if False:"),
 ('M43','nonregular_unpublished_ok: root-known test dropped',"d['nonregular_unpublished_ok'] = (root_value is not None","d['nonregular_unpublished_ok'] = (True"),
 ('M44','oracle_hits equality loosened to one missing file',"d['oracle_hits'] == d['oracle_files'])","d['oracle_hits'] >= d['oracle_files'] - 1)"),
 ('M45','operation_ok: operation/provider test dropped',"d['operation_ok'] = (env.get('operation') == 'extract_firmware'","d['operation_ok'] = (True"),
 ('M46','layout_ok ORs the BE magic (loosened gate)',"d['layout_ok'] = bool(d['layout'].get('ok'))","d['layout_ok'] = bool(d['layout'].get('ok')) or bool(d['layout'].get('be_magic'))"),
 ('M47','layout probe: bytes_used sanity branch skipped',"    elif not d['bytes_used_sane']:","    elif False:"),
 ('M48','carrier_present forced true',"d['carrier_present'] = raw is not None","d['carrier_present'] = True"),
]
if __name__ == '__main__':
    res = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(lambda j: m.run(*j), M2):
            res.append(r)
    res.sort(key=lambda r: r['id'])
    json.dump(res, open(os.path.join(m.S, 'mutation-results-2.json'), 'w'), indent=1)
    for r in res:
        print(r['id'], r.get('status'), 'exit=%s' % r.get('exit'), 'cases=%s' % r.get('cases'),
              'fails=%s' % r.get('failures_n'), r.get('detail',''), r['clause'][:70])
