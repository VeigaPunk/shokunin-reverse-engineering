import subprocess, json, os, shutil, sys, hashlib
CL = open('clone-path.txt').read().strip()
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
FRZ = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
W = '/fast/scratch/hyaku/kaidoku-r49/W2C1Receipts'
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=W, HYAKU_SCRATCH='/fast/scratch/hyaku')
C1 = os.path.join(CL, 'corpus/evidence/round-49/c1')
def g(*a):
    r = subprocess.run(['git', '-C', CL, *a], capture_output=True, env=env)
    if r.returncode: raise SystemExit(('git', a, r.stderr[:300]))
    return r.stdout
def reset():
    g('reset', '-q', '--hard', REV); g('clean', '-qfdx')
def commit(msg):
    g('add', '-A'); g('commit', '-q', '-m', msg); return g('rev-parse', 'HEAD').decode().strip()
def counter(rev, tag):
    out = os.path.join(W, f'scen-{tag}.json'); wk = os.path.join(W, f'scen-work-{tag}')
    os.makedirs(wk, exist_ok=True)
    r = subprocess.run(['python3', '-I', '-B', os.path.join(W, 'c1-counter.py'), '--root', CL, '--rev', rev,
                        '--freeze', FRZ, '--pkg65', '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents',
                        '--work', wk, '--json-out', out], capture_output=True, env=env, text=True)
    d = json.load(open(out)) if os.path.exists(out) else {}
    per = {k: [c for c, v in (x.items()) if v is False] for k, x in (d.get('carriers') or {}).items()}
    return dict(tag=tag, rc=r.returncode, carriers_matched=d.get('carriers_matched'), frozen=d.get('frozen_path_changed'),
                bindings_false=d.get('bindings_false'), failing_per_carrier=per, stderr=r.stderr[-300:])
def rd(p): return open(os.path.join(C1, p), 'rb').read()
def wr(p, b):
    fp = os.path.join(C1, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'wb').write(b)
def js(p): return json.loads(rd(p))
def wjs(p, o): wr(p, (json.dumps(o, indent=2) + '\n').encode())
scen = {}
def S(name, fn):
    scen[name] = fn
S('S1_tamper_extracted_apple_bytes', lambda: wr('v1le/firmware.bin_extract/apple.txt', b'XXXXXX\n'))
S('S2_delete_extracted_cherry', lambda: os.remove(os.path.join(C1, 'v1le/firmware.bin_extract/cherry.txt')))
S('S3_add_extra_extracted_file', lambda: wr('v1le/firmware.bin_extract/evil.txt', b'evil\n'))
S('S4_rewrite_extract_tree_tsv', lambda: wr('v2be/extract-tree.tsv', b'# relpath\tkind\tsize\tsha256\nfirmware.bin_extract/apple1.txt\tfile\t7\t' + b'0'*64 + b'\n'))
S('S5_run_json_exit_code_1', lambda: wjs('v1be/run.json', dict(js('v1be/run.json'), exit_code=1)))
S('S6_stdout_log_garbage', lambda: wr('v2le/stdout.log', b'{}\n'))
S('S7_extract_env_sasquatch_sha_zero', lambda: wjs('v1le/extract-env.json', dict(js('v1le/extract-env.json'), sasquatch=dict(js('v1le/extract-env.json')['sasquatch'], sha256='0'*64))))
S('S8_symlink_in_extract_tree', lambda: (os.symlink('apple.txt', os.path.join(C1, 'v2le/firmware.bin_extract/apple1_link.txt'))))
S('S9_after_file_sha_mutated', lambda: (lambda a: (a['normalized_result']['files'][0].update(sha256='1'*64, reported_sha256='1'*64), wjs('v1le/after.json', a)))(js('v1le/after.json')))
S('S10_after_outdir_tmp', lambda: (lambda a: (a['parameters'].update(output_directory='/tmp/x-rea-out'), wjs('v1le/after.json', a)))(js('v1le/after.json')))
S('S11_after_subject_digest_changed', lambda: (lambda a: (a['subject']['digest'].update(sha256='2'*64), wjs('v2be/after.json', a)))(js('v2be/after.json')))
S('S12_unblob_log_replaced', lambda: wr('v2le/unblob.log', b'nothing\n'))
S('S13_provenance_files_99', lambda: wjs('v1be/provenance.json', dict(js('v1be/provenance.json'), produced_tree=dict(js('v1be/provenance.json')['produced_tree'], files=99))))
S('S14_after_removes_one_file_row', lambda: (lambda a: (a['normalized_result'].update(files=a['normalized_result']['files'][:2]), wjs('v2be/after.json', a)))(js('v2be/after.json')))
S('S15_relabel_v1le_after_into_v1be', lambda: wr('v1be/after.json', rd('v1le/after.json')))
S('S16_manifest_rev_at_run_forged', lambda: wjs('manifest.json', dict(js('manifest.json'), rev_at_run='0'*40)))
S('S17_after_unpublished_row_added', lambda: (lambda a: (a['normalized_result'].update(unpublished_entries=[{'relative_path':'firmware.bin_extract/zz','kind':'symlink','link_target':'x'}]), wjs('v1le/after.json', a)))(js('v1le/after.json')))
S('S18_after_gaps_added_structural', lambda: (lambda a: (a['normalized_result'].update(extraction_gaps=[{'kind':'depth-limited','relative_path':None,'dependencies':[]}]), wjs('v2le/after.json', a)))(js('v2le/after.json')))

S('S19_raw_report_injected_symlink_stat', lambda: (lambda a: (a['raw_result']['report'][0]['reports'].append({'__typename__':'StatReport','is_dir':False,'is_file':False,'is_link':True,'link_target':'/etc/passwd','path':'/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.v1le.1044367/rea-firmware-8CX3Ku/extracted/firmware.bin_extract/evil','size':0}), wjs('v1le/after.json', a)))(js('v1le/after.json')))
S('S20_raw_execution_exit_code_1', lambda: (lambda a: (a['raw_result']['execution'][0].update(exit_code=1) if isinstance(a['raw_result']['execution'], list) else a['raw_result']['execution'].update(exit_code=1), wjs('v1be/after.json', a)))(js('v1be/after.json')))
S('S22_authority_and_confidence_changed', lambda: (lambda a: (a.update(authority='vendor-attested', confidence='verified'), wjs('v2le/after.json', a)))(js('v2le/after.json')))
S('S24_coverage_partial', lambda: (lambda a: (a['normalized_result'].update(coverage='partial'), wjs('v2be/after.json', a)))(js('v2be/after.json')))
S('S25_depth_limited_paths_nonempty', lambda: (lambda a: (a['normalized_result'].update(depth_limited_paths=['firmware.bin_extract']), wjs('v1be/after.json', a)))(js('v1be/after.json')))
S('S27_continuations_nonempty', lambda: (lambda a: (a['normalized_result'].update(extraction_continuations=[{'continuation_id':'x','handler':'squashfs_v2'}]), wjs('v2le/after.json', a)))(js('v2le/after.json')))
S('S28_chunk_extraction_failed', lambda: (lambda a: (a['normalized_result']['chunks'][0].update(extraction_failed=True), wjs('v1le/after.json', a)))(js('v1le/after.json')))
which = sys.argv[1:] or list(scen)
res = []
for name in which:
    reset()
    scen[name]()
    if name == 'S8_symlink_in_extract_tree':
        pass
    h = commit(name)
    r = counter(h, name); r['commit'] = h
    res.append(r); print(json.dumps(r), flush=True)
reset()
json.dump(res, open(os.path.join(W, 'scen-results-%s.json' % ('all' if len(which)==len(scen) else 'part')), 'w'), indent=1)
print('DONE', flush=True)
