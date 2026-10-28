import importlib.util, json, hashlib, sys
DRAFT='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py'
spec_=importlib.util.spec_from_file_location('c1c', DRAFT); c1=importlib.util.module_from_spec(spec_); spec_.loader.exec_module(c1)
sha=lambda b: hashlib.sha256(b).hexdigest()
pin=sha(b'carrier'); rows=[('apple.txt', sha(b'fa'), 6), ('banana.txt', sha(b'fb'), 7)]
env=c1.mk_receipt(pin, rows, 'squashfs_v1', '/fast/scratch/hyaku/kaidoku-r49/probe/v1le')
model,_=c1.gap_rule_model(c1.GAP_RULE)
carrier={'handler':'squashfs_v1','endian':'le','s_major':1,'s_minor':0,'compression':'gzip','sha256':pin}
def clauses(e):
    d=c1.evaluate_carrier(e, carrier, rows, [], model, pin, 'plus-extractor', None)
    return {k:d[k] for k in ('handler_ok','chunks_ok','oracle_hits_ok','gaps_ok','nonregular_unpublished_ok','path_shape_ok','run_provenance_ok','subject_pin_ok','operation_ok')}
base=clauses(env)
print('green-shape receipt clauses:', json.dumps(base))
e2=json.loads(json.dumps(env))
e2['normalized_result']['unpublished_entries']=[{'path':'/x/firmware.bin_extract/bin/link','kind':'symlink','target':'/etc/passwd','reason':'probe'}]
print('with unpublished_entries (plan: must be []):', json.dumps(clauses(e2)))
print('gaps', c1.gaps(e2), 'unpublished_entries', e2['normalized_result']['unpublished_entries'][:1])
