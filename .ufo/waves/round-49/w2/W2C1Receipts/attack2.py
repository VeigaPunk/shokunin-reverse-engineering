import json, hashlib, subprocess, os, re
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
C1 = 'corpus/evidence/round-49/c1'
ids = ['v1le', 'v1be', 'v2le', 'v2be']
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1')
def blob(path, rev=REV):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None
def sha(b): return hashlib.sha256(b).hexdigest()
car = json.loads(blob('tools/round-49/carriers.json'))
C = {c['id']: c for c in car['carriers']}
tree = json.load(open('tree.json'))['tree']
res = {}
for i in ids:
    base = f'{C1}/{i}'
    c = C[i]
    print('=====', i, c['file'], c['handler'], c['endian'])
    # fixture pin
    fx = blob(c['path'])
    print(' fixture sha ok:', sha(fx) == c['sha256'], 'size', len(fx), c['size'], 'expected_regular', c['expected_regular'])
    # oracle image sha in carriers oracle block
    print(' oracle.image.sha ok:', c['oracle']['image']['sha256'] == c['sha256'])
    # superblock
    mag = fx[0:4]; major = int.from_bytes(fx[28:30], 'big' if c['endian']=='be' else 'little'); minor = int.from_bytes(fx[30:32],'big' if c['endian']=='be' else 'little')
    print(' magic', mag, 'major', major, 'minor', minor, 'carriers s_major/minor', c['s_major'], c['s_minor'])
    # oracle members
    om = c['oracle']['members']
    ot = c['oracle']['output_tree']['members']
    print(' oracle members == output_tree members:', om == ot, 'n=', len(om), 'nonregular', c['oracle']['nonregular'])
    # recompute output tree digest from members
    dig = sha(''.join('%s\t%s\n' % (m['path'], m['sha256']) for m in sorted(om, key=lambda m: m['path'].encode())).encode())
    print(' oracle digest recompute ok:', dig == c['oracle']['output_tree_digest'], dig, c['oracle']['output_tree_digest'])
    # census vs members
    cen = [r for r in c['oracle']['census'] if r['type']=='regular']
    print(' census regular rows vs members:', sorted((r['rel'], r['size']) for r in cen) == sorted((m['path'], m['size']) for m in om), 'census rows', len(c['oracle']['census']), 'types', sorted({r['type'] for r in c['oracle']['census']}))
    # tsv
    tsv_raw = blob(f'{base}/extract-tree.tsv').decode()
    tlines = tsv_raw.splitlines()
    print(' tsv header:', repr(tlines[0]), 'rows', len(tlines)-1, 'trailing newline', tsv_raw.endswith('\n'))
    rows = []
    for ln in tlines[1:]:
        rel, kind, size, h = ln.split('\t')
        rows.append((rel, kind, int(size), h))
    # committed extract files
    ext = sorted(p for p in tree if p.startswith(base + '/firmware.bin_extract/'))
    actual = {}
    for p in ext:
        b = blob(p)
        actual[p[len(base)+1:]] = (len(b), sha(b))
    tsvmap = {r[0]: (r[2], r[3]) for r in rows}
    print(' tsv vs committed extract files equal:', tsvmap == actual, 'tsv names', sorted(tsvmap), 'files', sorted(actual))
    print(' tsv kinds', sorted({r[1] for r in rows}), 'dup rows', len(rows)!=len(tsvmap))
    # oracle vs committed
    orc = {m['path']: (m['size'], m['sha256']) for m in om}
    orc_full = {'firmware.bin_extract/'+k: v for k,v in orc.items()}
    print(' oracle vs committed extract equal:', orc_full == actual)
    # after.json
    aj_raw = blob(f'{base}/after.json')
    aj = json.loads(aj_raw)
    files = aj['normalized_result']['files']
    afmap = {f['relative_path']: (f['size'], f['sha256']) for f in files}
    print(' after.files rel-set == committed:', afmap == actual, 'n', len(files), 'reported==sha', all(f['reported_sha256']==f['sha256'] for f in files))
    print(' after.files path prefix', sorted({os.path.dirname(f['path']).rsplit('/',1)[0] for f in files}))
    print(' after: handler chunks', [(ch['handler'], ch['extraction_failed']) for ch in aj['normalized_result']['chunks']], 'coverage', aj['normalized_result']['coverage'])
    print(' after: gaps', aj['normalized_result']['extraction_gaps'], 'unpub', aj['normalized_result']['unpublished_entries'], 'diag', aj['normalized_result']['diagnostics'], 'cont', aj['normalized_result']['extraction_continuations'], 'depthlim', aj['normalized_result']['depth_limited_paths'])
    print(' after.subject', aj.get('subject'))
    print(' after.parameters', aj.get('parameters'))
    print(' after.operation', aj.get('operation'), 'provider', aj.get('provider'), 'env', aj.get('environment'), 'predicate', aj.get('predicate_type'))
    print(' after.evidence_id', aj.get('evidence_id'), 'published_bytes', aj['normalized_result'].get('published_bytes'), 'selection', aj['normalized_result'].get('selection'))
    print(' after.engine', aj['normalized_result']['engine'])
    print(' after.keys', sorted(aj.keys()))
    res[i] = dict(aj=aj, actual=actual, tsvrows=rows, aj_raw=aj_raw)
json.dump({k: {'aj_sha': sha(v['aj_raw']), 'tsv': v['tsvrows']} for k,v in res.items()}, open('afterdigests.json','w'), indent=1)
