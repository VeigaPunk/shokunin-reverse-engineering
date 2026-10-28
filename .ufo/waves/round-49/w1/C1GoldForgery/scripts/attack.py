#!/usr/bin/env python3
"""Gold-forgery attack driver for R49-C1 (scratch only). Builds counterfactual trees in
shared clones of the dev freeze, scores each with the frozen draft counter, records
exit codes and sha256s. Never runs c1-run.sh --data-run; never writes into the lane."""
import copy, hashlib, json, os, re, subprocess, sys, base64
from concurrent.futures import ThreadPoolExecutor

S = '/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery'
CLONE = S + '/clone'
BASE = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
XPIN = 'tools/round-27/xpin-attribute.mjs'
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
STEM = '2026-10-28-r49-squashfs-v1v2-core'
OUTDIR_OK = '/fast/scratch/hyaku/kaidoku-r49/C1GoldForgery/never-created/%s/rea-out'
IDS = ['v1le', 'v1be', 'v2le', 'v2be']
R44 = 'corpus/evidence/round-44/c1/%s/after.json'
R49 = 'corpus/evidence/round-49/c1/%s/after.json'
os.environ['TMPDIR'] = S
os.environ['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
os.makedirs(S + '/v', exist_ok=True)


def sh(args, cwd=None, check=True, inp=None):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, input=inp)
    if check and r.returncode != 0:
        raise SystemExit('FAIL %r rc=%s %s' % (args[:3], r.returncode, r.stderr[-400:]))
    return r


def lane_show(rev, path):
    r = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (rev, path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest()


def variant(name, files, deletes=()):
    """Shared clone of the dev freeze with `files` (path -> bytes) planted in one commit."""
    D = '%s/v/%s' % (S, name)
    sh(['rm', '-rf', D])
    sh(['git', 'clone', '-q', '--shared', CLONE, D])
    top = sh(['git', '-C', D, 'rev-parse', '--show-toplevel']).stdout.strip()
    assert top == D, (top, D)
    sh(['git', '-C', D, 'config', 'user.name', 'r49-attack'])
    sh(['git', '-C', D, 'config', 'user.email', 'r49-attack@dev.invalid'])
    freeze = sh(['git', '-C', CLONE, 'rev-parse', 'HEAD']).stdout.strip()
    sh(['git', '-C', D, 'checkout', '-q', '--detach', freeze])
    for p, b in files.items():
        full = os.path.join(D, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(b)
    if files:
        sh(['git', '-C', D, 'add', '-A'])
        sh(['git', '-C', D, 'commit', '-q', '-m', 'attack ' + name])
    rev = sh(['git', '-C', D, 'rev-parse', 'HEAD']).stdout.strip()
    return D, freeze, rev


def score(name, D, freeze, rev):
    W = '%s/work-%s' % (S, name)
    sh(['rm', '-rf', W]); os.makedirs(W)
    out = W + '/out.json'
    r = subprocess.run(['python3', '-I', '-B', 'tools/round-49/c1-counter.py', '--root', D,
                        '--rev', rev, '--freeze', freeze, '--pkg65', PKG, '--work', W,
                        '--json-out', out], cwd=D, capture_output=True, text=True, timeout=1500)
    so = r.stdout.encode()
    open(W + '/stdout.txt', 'wb').write(so)
    summ = {'name': name, 'rev': rev, 'exit': r.returncode, 'stdout_sha256': sha(so),
            'stderr_tail': r.stderr[-300:]}
    if os.path.exists(out):
        d = json.load(open(out))
        summ['matched'] = d.get('carriers_matched')
        summ['met'] = d.get('met_target')
        summ['bindings_false'] = sorted(k for k, v in d.get('bindings', {}).items() if v is not True)
        summ['per_carrier_failing'] = {k: sorted(x for x in (
            'carrier_present carrier_pin_ok carrier_size_ok carrier_fresh_ok layout_ok carve_ok '
            'oracle_ok tree_ok receipt_present receipt_fresh evidence_envelope_ok subject_pin_ok '
            'operation_ok handler_ok chunks_ok oracle_hits_ok gaps_ok nonregular_unpublished_ok '
            'path_shape_ok run_provenance_ok evidence_id_ok projection_ok').split()
            if v.get(x) is not True) for k, v in d.get('carriers', {}).items()}
        summ['projection_diff'] = {k: v.get('projection_diff') for k, v in d.get('carriers', {}).items()
                                   if v.get('projection_diff')}
        summ['projection_error'] = {k: str(v.get('projection_error'))[:200] for k, v in d.get('carriers', {}).items()
                                    if v.get('projection_error')}
        summ['gaps_note'] = {k: v.get('gaps_note') for k, v in d.get('carriers', {}).items() if v.get('gaps_note')}
        summ['frozen_path_changed'] = d.get('frozen_path_changed')
    else:
        summ['no_json'] = True
    summ['score_stdout_head'] = so[:300].decode(errors='replace')
    return summ


def mint(envs):
    """Re-mint evidence ids with the frozen xpin tool under the package's own digest code."""
    paths = []
    for k, env in envs.items():
        p = '%s/mint-%s.json' % (S, k.replace('/', '_'))
        open(p, 'w').write(json.dumps({'data': env}))
        paths.append(p)
    r = sh(['node', LANE + '/' + XPIN, '--pkg65', PKG, '--pkg67', PKG] + paths, cwd=LANE)
    lines = [l for l in r.stdout.splitlines() if l]
    out = {}
    for k, line in zip(envs, lines):
        f = line.split('\t')
        out[k] = f[2]
    return out, r.stdout


def docs_files(hollow=True):
    """Hollow landing text: makes all five documentation bindings true (no content)."""
    files = {}
    prov = lane_show(BASE, 'PROVINCE.md').decode()
    prov += ('\n## Round-49 additions to Core\n\n'
             '| `squashfs_v1` and `squashfs_v2` (SquashFS v1/v2) | hollow attack row | '
             '`%s` |\n\n'
             'Round-49 frontier note, 2026-10-28: `%s`: SquashFS v1/v2 moved (hollow).\n'
             % (ENTRY, STEM))
    files['PROVINCE.md'] = prov.encode()
    files[ENTRY] = ('---\nsource: S138\nsource: S139\n---\n# hollow\n').encode()
    readme = lane_show(BASE, 'corpus/README.md').decode().splitlines(True)
    out, inside, done = [], False, False
    for line in readme:
        out.append(line)
        if line.startswith('## Coverage map'):
            inside = True
        elif inside and not done and line.startswith('|---'):
            out.append('| %s | hollow | attack |\n' % STEM)
            done = True
    files['corpus/README.md'] = ''.join(out).encode()
    src = lane_show(BASE, 'corpus/SOURCES.md').decode().splitlines(True)
    newsrc = []
    for line in src:
        m = re.match(r'^\s*\|\s*(S138|S139)\s*\|', line)
        if m:
            c = [x.strip() for x in line.strip().strip('|').split('|')]
            assert len(c) == 11, (m.group(1), len(c))
            c[8] = '2026-10-28'
            c[10] = (ENTRY + ', ' + c[10])
            line = '| ' + ' | '.join(c) + ' |\n'
        newsrc.append(line)
    files['corpus/SOURCES.md'] = ''.join(newsrc).encode()
    return files


def carriers():
    return json.load(open(LANE + '/.ufo/waves/round-49/draft/tools/round-49/carriers.json'))['carriers']


def r44_env(cid):
    return json.loads(lane_show(BASE, R44 % cid))


def rewrite_outdir(env, od):
    env = copy.deepcopy(env)
    env.setdefault('parameters', {})['output_directory'] = od
    env.setdefault('normalized_result', {})['output_directory'] = od
    return env


def oracle_env(c, od):
    """Envelope fabricated from committed oracle + committed unblob tree bytes. NO REA run.
    Structure taken from the committed round-44 envelope of the same carrier (shape only);
    every value is computed from committed bytes."""
    tmpl = r44_env(c['id'])
    env = copy.deepcopy(tmpl)
    members = c['oracle']['members']
    troot = c['output_tree']
    root = 'firmware.bin_extract'
    fdir = os.path.join(LANE, troot)
    files, reports, edges_files = [], [], []
    total = 0
    for m in sorted(members, key=lambda m: m['path']):
        rel = m['path'].split('/', 1)[1] if m['path'].startswith('squashfs-root/') else m['path']
        body = open(os.path.join(fdir, rel), 'rb').read()
        assert sha(body) == m['sha256'] and len(body) == m['size']
        mime = subprocess.run(['file', '-b', '--mime-type', os.path.join(fdir, rel)],
                              capture_output=True, text=True).stdout.strip()
        rp = root + '/' + rel
        total += len(body)
        files.append({'analysis_depth': 1, 'mime_type': mime, 'original_file_range': None,
                      'path': od + '/' + rp, 'relative_path': rp, 'reported_sha256': m['sha256'],
                      'runtime_address': None, 'sha256': m['sha256'], 'size': len(body)})
        reports.append({'reports': [
            {'__typename__': 'StatReport', 'is_dir': False, 'is_file': True, 'is_link': False,
             'link_target': None, 'path': '/fake/extracted/' + rp, 'size': len(body)},
            {'__typename__': 'FileMagicReport', 'magic': 'ASCII text', 'mime_type': mime},
            {'__typename__': 'HashReport', 'md5': hashlib.md5(body).hexdigest(),
             'sha1': hashlib.sha1(body).hexdigest(), 'sha256': m['sha256']}],
            'subtasks': [], 'task': {'blob_id': '0:1', 'depth': 1, 'is_multi_file': False,
                                     'path': '/fake/extracted/' + rp}})
        edges_files.append({'child_path': '$output/' + rp, 'handler': None,
                            'parent_file_range': None, 'parent_path': '$output/' + root,
                            'provider_blob_id': '0:1'})
    nr = env['normalized_result']
    nr['files'] = files
    nr['published_bytes'] = total
    nr['derivations'] = edges_files + [{'child_path': '$output/' + root, 'handler': c['handler'],
                                        'parent_file_range': {'length': 4096, 'offset': 0},
                                        'parent_path': '$input', 'provider_blob_id': '0:1'}]
    nr['chunks'] = [{'encrypted': False, 'extraction_failed': False, 'handler': c['handler'],
                     'input_path': '$input', 'provider_id': '0:1',
                     'range': {'length': 4096, 'offset': 0},
                     'root_file_range': {'length': 4096, 'offset': 0}}]
    nr['engine'] = dict(nr['engine'], name='unblob', version='26.6.4')
    nr['coverage'] = 'complete'
    nr['extraction_gaps'] = []
    nr['unpublished_entries'] = []
    nr['diagnostics'] = []
    nr['depth_limited_paths'] = []
    env['raw_result'] = dict(env['raw_result'], report=reports)
    env['subject']['digest']['sha256'] = c['sha256']
    env['parameters']['output_directory'] = od
    env['parameters']['path'] = os.path.join(LANE, c['path'])
    env['subject']['local_path'] = os.path.join(LANE, c['path'])
    env['normalized_result'] = nr
    return env


def plant(envs_by_id, doc=False):
    files = {}
    for cid, env in envs_by_id.items():
        files[R49 % cid] = (json.dumps(env, indent=1, sort_keys=True) + '\n').encode()
    if doc:
        files.update(docs_files())
    return files


def remint_all(envs_by_id):
    ids, _ = mint(envs_by_id)
    out = {}
    for cid, env in envs_by_id.items():
        e = copy.deepcopy(env)
        e['evidence_id'] = ids[cid]
        out[cid] = e
    return out


def main(which):
    results = {}
    builds = {}
    r44 = {c: r44_env(c) for c in IDS}
    crs = {c['id']: c for c in carriers()}
    # A1 docs only
    builds['A1-docs-only'] = variant('A1-docs-only', docs_files())
    # A2 round-44 verbatim copy onto round-49 path (no docs)
    builds['A2-r44-verbatim'] = variant('A2-r44-verbatim', plant(r44))
    # A3 rewritten output_directory, stale evidence id
    envs3 = {c: rewrite_outdir(r44[c], OUTDIR_OK % c) for c in IDS}
    builds['A3-rewrite-stale-id'] = variant('A3-rewrite-stale-id', plant(envs3))
    # A4 rewritten + re-minted id (package's own digest code), no docs
    envs4 = remint_all(envs3)
    builds['A4-rewrite-reminted'] = variant('A4-rewrite-reminted', plant(envs4))
    # A5 A4 + hollow docs  (copied receipts + hollow text)
    builds['A5-copy-plus-hollow-docs'] = variant('A5-copy-plus-hollow-docs', plant(envs4, doc=True))
    # A6 oracle-only fabrication (no REA), re-minted, + hollow docs
    envs6 = {c: oracle_env(crs[c], OUTDIR_OK % c) for c in IDS}
    envs6 = remint_all(envs6)
    builds['A6-oracle-only-reminted-docs'] = variant('A6-oracle-only-reminted-docs', plant(envs6, doc=True))
    # A7 A6 but hash reports removed (raw report stripped) -> expect projection red
    envs7 = copy.deepcopy(envs6)
    for c in IDS:
        envs7[c]['raw_result']['report'] = []
    envs7 = remint_all(envs7)
    builds['A7-oracle-no-hashes'] = variant('A7-oracle-no-hashes', plant(envs7, doc=True))
    # A8 A6 with published_bytes +1 -> expect projection red (attribution)
    envs8 = copy.deepcopy(envs6)
    for c in IDS:
        envs8[c]['normalized_result']['published_bytes'] += 1
    envs8 = remint_all(envs8)
    builds['A8-oracle-bytes-plus1'] = variant('A8-oracle-bytes-plus1', plant(envs8, doc=True))
    # A9 A4 with output_directory outside the segment (kaidoku-r44-like) -> provenance red
    envs9 = {c: rewrite_outdir(r44[c], '/fast/scratch/hyaku/kaidoku-r44/x/rea-out') for c in IDS}
    envs9 = remint_all(envs9)
    builds['A9-outdir-outside-segment'] = variant('A9-outdir-outside-segment', plant(envs9, doc=True))
    # A10 oracle-only but NOT re-minted (stale id) -> evidence_id red
    envs10 = {c: oracle_env(crs[c], OUTDIR_OK % c) for c in IDS}
    builds['A10-oracle-stale-id'] = variant('A10-oracle-stale-id', plant(envs10, doc=True))
    # save the minted-evidence pairs for the report
    json.dump({'A4_ids': {c: envs4[c]['evidence_id'] for c in IDS},
               'A6_ids': {c: envs6[c]['evidence_id'] for c in IDS}},
              open(S + '/minted.json', 'w'), indent=1)
    names = [w for w in builds if (not which or w in which)]
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {n: ex.submit(score, n, builds[n][0], builds[n][1], builds[n][2]) for n in names}
        for n in names:
            results[n] = futs[n].result()
            print(json.dumps(results[n], indent=1, sort_keys=True), flush=True)
    json.dump(results, open(S + '/results-%s.json' % ('all' if not which else '-'.join(which)), 'w'),
              indent=1, sort_keys=True)


if __name__ == '__main__':
    main(sys.argv[1:])
