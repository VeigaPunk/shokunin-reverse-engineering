import json, os, sys, hashlib, subprocess, tempfile, shutil, textwrap

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
TOOLS = os.path.join(LANE, 'tools/round-41')
sys.path.insert(0, TOOLS)
import importlib.util
_spec = importlib.util.spec_from_file_location('c1_counter', os.path.join(TOOLS, 'c1-counter.py'))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
S = os.environ.get('S_SCRATCH', '/fast/scratch/hyaku/kaidoku-r41/R41W2C1PathRule')
os.environ['HYAKU_SCRATCH'] = S
OUT = os.path.join(S, 'out'); os.makedirs(OUT, exist_ok=True)

sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda i: sha(('f%s' % i).encode())
H1, H2 = fsha(1), fsha(2)
HX = fsha(99)

# carriers: V3 gzip, V4 xz(4), L3 gzip, L4 xz(2)
carriers = {
    'V3': C.sb_carrier(C.GZIP_ID, b'V3-avm'),
    'V4': C.sb_carrier(4, b'V4-avm'),
    'L3': C.sb_carrier(C.GZIP_ID, b'L3-avm'),
    'L4': C.sb_carrier(2, b'L4-avm'),
}
pins = {k: sha(v) for k, v in carriers.items()}

AFTERDIR = 'corpus/evidence/round-41/c1'
ORACLE = [('var/info.txt', H1, 40)]
NONREG = [('bin/link', 'symlink', '../usr/bin/x')]

def rule_text():
    return json.dumps({
        'claim': 'R41-C1',
        'allowed': {'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': False},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive', 'silent': {}},
        'structural': {'depth-limited': 1}}, indent=1)

def oracle_tsv(rows=ORACLE):
    return ''.join(f'{r}\t{h}\t{sz}\n' for r, h, sz in rows).encode()

def nonreg_tsv(rows=NONREG):
    return ''.join(f'{r}\t{k}\t{d}\n' if d is not None else f'{r}\t{k}\n'
                   for r, k, d in rows).encode()

def spec_text(**over):
    cs = []
    for k in ('V3','V4','L3','L4'):
        c = {'id': k, 'sha256': pins[k], 'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
             'nonregular': f'{AFTERDIR}/{k}/nonregular.tsv',
             'path': f'{AFTERDIR}/{k}/carrier.sqsh'}
        cs.append(c)
    if 'oracle_root' in over:
        by_id = {c['id']: c for c in cs}
        for cid, root in over.pop('oracle_root').items():
            by_id[cid]['oracle_root'] = root
    doc = {'claim': 'R41-C1', 'target': 4, 'carriers': cs}
    doc.update(over)
    return json.dumps(doc, indent=1)

def base_env(k, files=None, gaps=None, unpub=None, diags=None, chunk_dir='firmware.bin_extract',
             derivations=None, outdir=None):
    if outdir is None:
        outdir = '/fast/scratch/hyaku/kaidoku-r41/fx/%s-after' % k
    return C.mk_env('carrier.sqsh', pins[k],
                    files=files if files is not None else ORACLE,
                    gaps=gaps if gaps is not None else [('unpublished-entry', 'bin/link', [])],
                    unpub=unpub if unpub is not None else [('bin/link', 'symlink', '../usr/bin/x')],
                    diags=diags if diags is not None else [],
                    outdir=outdir, chunk_dir=chunk_dir,
                    derivations=derivations)

def green_envs():
    return {k: base_env(k) for k in carriers}

def frozen_files(envs):
    f = {
        C.XPIN: open(os.path.join(LANE, 'tools/round-27/xpin-attribute.mjs'), 'rb').read(),
        C.CARRIERS: spec_text().encode(),
        C.GAPRULE: rule_text().encode(),
        'plans/round-41-claims.md': b'# plan\n',
        'tools/round-41/c1-counter.py': open(os.path.join(TOOLS, 'c1-counter.py'), 'rb').read(),
        'PROVINCE.md': C._province().encode(),
        C.ENTRY: C._entry().encode(),
        'corpus/SOURCES.md': C._registry().encode(),
        'corpus/README.md': C._readme().encode(),
    }
    for k in carriers:
        f[f'{AFTERDIR}/{k}/carrier.sqsh'] = carriers[k]
        f[f'{AFTERDIR}/{k}/oracle.tsv'] = oracle_tsv()
        f[f'{AFTERDIR}/{k}/nonregular.tsv'] = nonreg_tsv()
    return f

def receipts(envs):
    return {f'{AFTERDIR}/{k}/after.json': json.dumps(envs[k])
            for k in envs}

def mint(work, envs):
    ids = C.mint_many(work, os.path.join(work, 'xpin.mjs'), PKG65,
                      {k: envs[k] for k in envs})
    for k in envs:
        envs[k]['evidence_id'] = ids[k]
    return envs

def same_runner(envs):
    def run(carrier_bytes, cid, params=None):
        e = json.loads(json.dumps(envs[cid]))
        e['subject']['digest']['sha256'] = sha(carrier_bytes)
        e['normalized_result']['selection']['sha256'] = sha(carrier_bytes)
        return 'ok', C.rehost(e, 'fx-same-' + cid)
    return run

def run_scenario(name, mutate, hint=None, want='see'):
    work = tempfile.mkdtemp(prefix='fx-work.', dir=S)
    d = tempfile.mkdtemp(prefix='fx-repo.', dir=S)
    try:
        # initialize isolated fixture repo
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise RuntimeError('fixture toplevel mismatch: ' + top)
        # xpin at freeze
        shutil.copy(os.path.join(LANE, 'tools/round-27/xpin-attribute.mjs'),
                    os.path.join(work, 'xpin.mjs'))
        envs = green_envs()
        mutate(envs)
        mint(work, envs)
        recs = receipts(envs)
        fz = frozen_files(envs)
        if hint is not None:
            fz[C.CARRIERS] = spec_text(oracle_root={'V4': hint}).encode()
        steps = [fz, recs]
        revs = []
        for i, files in enumerate(steps):
            for p, content in files.items():
                full = os.path.join(d, p)
                os.makedirs(os.path.dirname(full) or d, exist_ok=True)
                data = content if isinstance(content, bytes) else content.encode()
                with open(full, 'wb') as fh:
                    fh.write(data)
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                            'commit', '-qm', 'step%d' % i, '--allow-empty'], check=True)
            revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                                       capture_output=True, text=True).stdout.strip())
        fz_rev, rv_rev = revs[0], revs[-1]
        res = C.measure(d, rv_rev, fz_rev, PKG65, rerun=same_runner(envs))
        failing = set()
        for k, v in res.get('carriers', {}).items():
            failing |= {x for x in C.CLAUSES if v.get(x) is not True}
        failing |= {'b:' + x for x in C.BINDINGS if res.get('bindings', {}).get(x) is not True}
        v4 = res.get('carriers', {}).get('V4', {})
        summary = {
            'scenario': name,
            'met_target': res.get('met_target'),
            'carriers_matched': res.get('carriers_matched'),
            'exit_code': 0 if res.get('met_target') else 1,
            'failing': sorted(failing),
            'V4_extract_root': v4.get('extract_root'),
            'V4_extract_root_source': v4.get('extract_root_source'),
            'V4_oracle_hits': v4.get('oracle_hits'),
            'V4_oracle_files': v4.get('oracle_files'),
            'V4_gaps_ok': v4.get('gaps_ok'),
            'V4_gaps_note': v4.get('gaps_note'),
            'V4_nonregular_unpublished_ok': v4.get('nonregular_unpublished_ok'),
            'V4_nonregular_published': v4.get('nonregular_published'),
            'V4_projection_ok': v4.get('projection_ok'),
            'V4_evidence_id_ok': v4.get('evidence_id_ok'),
            'V4_published_files': v4.get('published_files'),
        }
        with open(os.path.join(OUT, name + '.json'), 'w') as fh:
            json.dump(res, fh, indent=1, sort_keys=True)
        return summary
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(d, ignore_errors=True)

scenarios = []

# ---- baseline
def _base(envs):
    pass
scenarios.append(run_scenario('00-baseline-green', _base))

# ---- (a) two squashfs_v4 derivations
INNER = 'firmware.bin_extract/core.sqsh_extract'
def _two_roots(envs):
    e = envs['V4']
    e['normalized_result']['derivations'].append({
        'parent_path': '$output/firmware.bin_extract',
        'child_path': '$output/' + INNER,
        'handler': C.HANDLER, 'provider_blob_id': 'fx:2',
        'parent_file_range': {'offset': 4096, 'length': 2048}})
    for f in e['normalized_result']['files']:
        f['relative_path'] = INNER + '/' + f['relative_path'].split('/', 1)[1]
        f['path'] = '/x/' + f['relative_path']
    for g in e['normalized_result']['extraction_gaps']:
        if g.get('relative_path'):
            g['relative_path'] = INNER + '/' + g['relative_path'].split('/', 1)[1]
            g['input_path'] = '$output/' + g['relative_path']
    for u in e['normalized_result']['unpublished_entries']:
        u['relative_path'] = INNER + '/' + u['relative_path'].split('/', 1)[1]
scenarios.append(run_scenario('01a-two-roots-no-hint', _two_roots))
scenarios.append(run_scenario('01b-two-roots-correct-hint', _two_roots, hint=INNER))
scenarios.append(run_scenario('01c-two-roots-wrong-hint', _two_roots, hint='firmware.bin_extract'))

# ---- (b) carve at nonzero offset
PORTION = 'firmware.bin_extract/4096-6513.squashfs_v4_be_extract'
def _carve(envs, deep=True):
    e = envs['V4']
    e['normalized_result']['derivations'] = [{
        'parent_path': '$input', 'child_path': '$output/' + PORTION,
        'handler': C.HANDLER, 'provider_blob_id': 'fx:c',
        'parent_file_range': {'offset': 4096, 'length': 2517}}]
    e['normalized_result']['chunks'] = [{
        'input_path': '$input', 'provider_id': 'fx:c',
        'range': {'offset': 4096, 'length': 2517}, 'handler': C.HANDLER,
        'encrypted': False, 'root_file_range': {'offset': 4096, 'length': 2517},
        'extraction_failed': False}]
    pre = PORTION if deep else 'firmware.bin_extract'
    for f in e['normalized_result']['files']:
        f['relative_path'] = pre + '/' + f['relative_path'].split('/', 1)[1]
        f['path'] = '/x/' + f['relative_path']
    for g in e['normalized_result']['extraction_gaps']:
        if g.get('relative_path'):
            g['relative_path'] = pre + '/' + g['relative_path'].split('/', 1)[1]
            g['input_path'] = '$output/' + g['relative_path']
    for u in e['normalized_result']['unpublished_entries']:
        u['relative_path'] = pre + '/' + u['relative_path'].split('/', 1)[1]
scenarios.append(run_scenario('02a-carve-nonzero-offset-deep', lambda envs: _carve(envs, True)))
scenarios.append(run_scenario('02b-carve-shallow-publish', lambda envs: _carve(envs, False)))

# ---- (c) path equals CR exactly
def _root_equal_file(envs):
    e = envs['V4']
    e['normalized_result']['files'].append({
        'relative_path': 'firmware.bin_extract', 'path': '/x/firmware.bin_extract',
        'size': 7, 'sha256': HX})
scenarios.append(run_scenario('03a-path-equals-CR-file', _root_equal_file))

def _root_equal_gap(envs):
    e = envs['V4']
    e['normalized_result']['extraction_gaps'].append({
        'kind': 'unpublished-entry', 'handler': C.HANDLER,
        'relative_path': 'firmware.bin_extract', 'dependencies': []})
scenarios.append(run_scenario('03b-path-equals-CR-gap', _root_equal_gap))

# ---- (d) $output/ twice
def _double_prefix_child(envs):
    e = envs['V4']
    e['normalized_result']['derivations'][0]['child_path'] = '$output/$output/firmware.bin_extract'
scenarios.append(run_scenario('04a-double-dollaroutput-child', _double_prefix_child))

def _double_prefix_file(envs):
    e = envs['V4']
    for f in e['normalized_result']['files']:
        f['relative_path'] = '$output/$output/' + f['relative_path']
        f['path'] = '/x/' + f['relative_path']
    for g in e['normalized_result']['extraction_gaps']:
        if g.get('relative_path'):
            g['relative_path'] = '$output/$output/' + g['relative_path']
            g['input_path'] = '$output/$output/' + g['relative_path']
    for u in e['normalized_result']['unpublished_entries']:
        u['relative_path'] = '$output/$output/' + u['relative_path']
scenarios.append(run_scenario('04b-double-dollaroutput-file', _double_prefix_file))

# ---- (e) removal diagnostic outside CR
def _removal_outside(envs):
    e = envs['V4']
    e['normalized_result']['extraction_gaps'] = []
    e['normalized_result']['unpublished_entries'] = []
    e['normalized_result']['diagnostics'] = [{
        'input_path': '$output/firmware.bin_extract',
        'report': {'__typename__': 'MaliciousSymlinkRemoved', 'severity': 'WARNING',
                   'link': '/x/outside/never-under-root', 'target': '/etc/shadow'}}]
scenarios.append(run_scenario('05a-removal-outside-no-root-run', _removal_outside))

def _removal_decoy(envs):
    e = envs['V4']
    e['normalized_result']['extraction_gaps'] = []
    e['normalized_result']['unpublished_entries'] = [
        {'relative_path': 'firmware.bin_extract/bin/link', 'kind': 'symlink',
         'link_target': '../x'}]
    # The actual run output directory is /fast/scratch/hyaku/kaidoku-r41/fx/V4-after.
    # The diagnostic points to a different directory that contains a decoy CR suffix.
    e['normalized_result']['diagnostics'] = [{
        'input_path': '$output/firmware.bin_extract',
        'report': {'__typename__': 'MaliciousSymlinkRemoved', 'severity': 'WARNING',
                   'link': '/fast/scratch/hyaku/kaidoku-r41/decoy/firmware.bin_extract/bin/link',
                   'target': '/etc/shadow'}}]
scenarios.append(run_scenario('05b-removal-decoy-segment-run', _removal_decoy))

# ---- (f) trailing slash / ./
def _trailing_file(envs):
    e = envs['V4']
    for f in e['normalized_result']['files']:
        f['relative_path'] = f['relative_path'] + '/'
        f['path'] = '/x/' + f['relative_path']
scenarios.append(run_scenario('06a-file-trailing-slash', _trailing_file))

def _dotdot_file(envs):
    e = envs['V4']
    for f in e['normalized_result']['files']:
        f['relative_path'] = './' + f['relative_path']
        f['path'] = '/x/' + f['relative_path']
scenarios.append(run_scenario('06b-file-leading-dotslash', _dotdot_file))

def _interior_dot_file(envs):
    e = envs['V4']
    for f in e['normalized_result']['files']:
        f['relative_path'] = f['relative_path'].replace('info.txt', './info.txt')
scenarios.append(run_scenario('06c-file-interior-dot', _interior_dot_file))

def _dir_as_file(envs):
    e = envs['V4']
    e['normalized_result']['files'].append({
        'relative_path': 'firmware.bin_extract/bin/link/',
        'path': '/x/bin/link/', 'size': 3, 'sha256': HX})
scenarios.append(run_scenario('06d-dir-as-file-trailing-slash', _dir_as_file))

def _gap_trailing(envs):
    e = envs['V4']
    for g in e['normalized_result']['extraction_gaps']:
        if g.get('relative_path'):
            g['relative_path'] = g['relative_path'] + '/'
            g['input_path'] = '$output/' + g['relative_path']
scenarios.append(run_scenario('06e-gap-trailing-slash', _gap_trailing))

# ---- probes (pure functions)
R = 'firmware.bin_extract'
probes = [
    ('P1 root eq: extract_rel(root, root) == ""',
     C.extract_rel(R, R) == ''),
    ('P2 root-eq path does not satisfy a non-empty row',
     C.same_rel(R, 'var/info.txt', R) is False),
    ('P3 double slash inside candidate normalizes',
     C.same_rel(R + '//var/info.txt', 'var/info.txt', R) is True),
    ('P4 ./ inside candidate normalizes',
     C.same_rel(R + '/./var/info.txt', 'var/info.txt', R) is True),
    ('P5 trailing slash on candidate matches row',
     C.same_rel(R + '/var/info.txt/', 'var/info.txt', R) is True),
    ('P6 trailing slash on table row does NOT match plain candidate',
     C.same_rel(R + '/var/info.txt', 'var/info.txt/', R) is False),
    ('P7 table row ./ prefix strips',
     C.same_rel(R + '/var/info.txt', './var/info.txt', R) is True),
    ('P8 table row leading / strips',
     C.same_rel(R + '/var/info.txt', '/var/info.txt', R) is True),
    ('P9 suffix is never a match',
     C.same_rel(R + '/usr/bin/busy', 'bin/busy', R) is False),
    ('P10 prefix-segment mismatch is not a match',
     C.same_rel(R + '_extra/x', 'x', R) is False),
    ('P11 deeper file is not a match',
     C.same_rel(R + '/x/usr/bin/busy', 'usr/bin/busy', R) is False),
    ('P12 materialised symlink at its own path matches',
     C.same_rel(R + '/bin/busy', 'bin/busy', R) is True),
]
decoy1 = C.diagnostic_rel({'report': {'link': '/x/decoy/firmware.bin_extract/bin/evil'}}, R)
probes.append(('P13 decoy removal resolves to rel inside CR: %r' % decoy1,
               decoy1 == 'bin/evil'))
probes.append(('P14 removal link with no root run is None',
               C.diagnostic_rel({'report': {'link': '/x/outside/x'}}, R) is None))
probes.append(('P15 trailing-slash candidate equals root -> ""',
               C.extract_rel(R + '/', R) == ''))

summary = {'scenarios': scenarios, 'probes': probes,
           'probe_fail': [p for p, ok in probes if not ok]}
print(json.dumps(summary, indent=1))
with open(os.path.join(OUT, 'summary.json'), 'w') as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
