import hashlib, importlib.util, json, mimetypes, os, subprocess, sys

S = '/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1PosArm'
SB = S + '/sandbox'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

ctl = load(SB + '/tools/round-44/c1-controls.py', 'c1ctl')
ctr = load(SB + '/tools/round-44/c1-counter.py', 'c1ctr')

spec = json.load(open(SB + '/tools/round-44/carriers.json'))
byid = {c['id']: c for c in spec['carriers']}

def members(cid):
    orc = byid[cid]['oracle']
    return [m for m in orc['members'] if m.get('type') == 'regular' and m.get('path')]

def hull(cid, outdir, strengthen):
    car = byid[cid]
    rows = [(m['path'], m['sha256'], int(m['size'])) for m in members(cid)]
    env = ctl.envelope(car, outdir, files=rows)
    nr = env['normalized_result']
    nr['coverage'] = 'complete'
    nr['published_bytes'] = sum(r[2] for r in rows)
    if strengthen:
        odir = S + '/oracle/' + cid
        report = []
        deriv = env['normalized_result']['derivations']  # keeps the chunk edge
        for rel, sha, size in rows:
            body = open(os.path.join(odir, rel), 'rb').read()
            md5 = hashlib.md5(body).hexdigest()
            sha1 = hashlib.sha1(body).hexdigest()
            mime = mimetypes.guess_type(rel)[0] or 'application/octet-stream'
            for f in nr['files']:
                if f['relative_path'] == 'firmware.bin_extract/' + rel:
                    f['mime_type'] = mime
                    f['reported_sha256'] = sha
                    f['analysis_depth'] = 1
            taskpath = '$output/firmware.bin_extract/' + rel
            report.append({
                'task': {'blob_id': '1:1', 'depth': 1, 'is_multi_file': False,
                         'path': taskpath},
                'reports': [{'__typename__': 'HashReport', 'md5': md5,
                             'sha1': sha1, 'sha256': sha}],
                'subtasks': []})
            deriv.append({'parent_path': '$output/firmware.bin_extract',
                          'child_path': taskpath, 'provider_blob_id': '1:1',
                          'handler': None, 'parent_file_range': None})
        env['raw_result']['report'] = report
    return env

outdirs = {'v1le': S + '/rea-out/v1le',
           'v1be': S + '/rea-out/v1be'}
envs = {'v1le': hull('v1le', outdirs['v1le'], False),
        'v1be': hull('v1be', outdirs['v1be'], True)}
minted = ctl.mint_evidence_ids(S + '/work', PKG, envs)
for cid, env in envs.items():
    env['evidence_id'] = minted[cid]
    real = json.load(open('%s/corpus/evidence/round-44/c1/%s/after.json' % (SB, cid)))
    a = ctr.projection(env, 'plus-extractor', byid[cid]['handler'])
    b = ctr.projection(real, 'plus-extractor', byid[cid]['handler'])
    eq, keys, detail = ctr.projection_diff(a, b, 'plus-extractor')
    print(cid, 'strengthened=%s' % (cid == 'v1be'), 'projection_equal_to_real=%s' % eq,
          'diff_keys=%s' % keys)
    if not eq:
        print('  detail:', json.dumps(detail)[:600])
    rel = 'corpus/evidence/round-44/c1/%s/after.json' % cid
    open(SB + '/' + rel, 'w').write(json.dumps(env, indent=1, sort_keys=True) + '\n')
    print('  wrote', rel, 'evidence_id', env['evidence_id'])
