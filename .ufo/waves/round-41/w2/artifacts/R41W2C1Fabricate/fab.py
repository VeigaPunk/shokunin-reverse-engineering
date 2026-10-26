import json, os, sys, hashlib, subprocess, shutil

S = '/fast/scratch/hyaku/kaidoku-r41/R41W2C1Fabricate'
D = os.environ['D']
LANE = os.path.join(D, 'lane')
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
XPIN = os.path.join(LANE, 'tools/round-27/xpin-attribute.mjs')

sys.path.insert(0, os.path.join(LANE, 'tools/round-41'))
import importlib.util
_spec = importlib.util.spec_from_file_location('c1counter', os.path.join(LANE, 'tools/round-41/c1-counter.py'))
cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cc)

SPEC = json.load(open(os.path.join(LANE, '.ufo/waves/round-41/c1/carriers.json')))
CARRIERS = {c['id']: c for c in SPEC['carriers']}

def read_tsv(rel):
    rows = []
    for line in open(os.path.join(LANE, rel)):
        f = line.rstrip('\n').split('\t')
        if f[0] == 'relative_path' or not f[0]:
            continue
        rows.append(f)
    return rows

def oracle_rows(cid):
    c = CARRIERS[cid]
    return [(f[0], f[1], int(f[2])) for f in read_tsv(c['oracle'])]

def nonreg_rows(cid):
    c = CARRIERS[cid]
    return [(f[0], f[1], f[2] if len(f) > 2 else ('' if len(f) == 3 else None)) for f in read_tsv(c['nonregular'])]

def length_of(cid):
    c = CARRIERS[cid]
    if c.get('external'):
        return c['external']['length']
    return os.path.getsize(os.path.join(LANE, c['path']))

def pin_of(cid):
    return CARRIERS[cid]['sha256']

def base_env(cid, scen):
    pin = pin_of(cid); L = length_of(cid)
    c = CARRIERS[cid]
    if c.get('external'):
        src = f'/fast/scratch/hyaku/kaidoku-r41/cache/{pin}.bin'
        name = f'{pin}.bin'
    else:
        src = os.path.join(LANE, c['path'])
        name = c['path'].split('/')[-1]
    outdir = f'/fast/scratch/hyaku/kaidoku-r41/{scen}-{cid}/extract'
    env = {
        'analysis_profile': None,
        'authority': 'shipped-artifact',
        'confidence': 'observed',
        'environment': None,
        'evidence_id': 'ev_' + '0'*62,
        'evidence_links': [],
        'limitations': ["Fabricated envelope (seat R41W2C1Fabricate)."],
        'locations': [{'end': L, 'kind': 'file-offset-range', 'start': 0}],
        'operation': 'extract_firmware',
        'parameters': {'max_depth': 1, 'max_output_bytes': 268435456,
                       'max_output_files': 10000, 'output_directory': outdir,
                       'path': src},
        'predicate_type': 'rea.analysis',
        'provider': {'id': 'unblob', 'name': 'Unblob', 'version': '26.6.4'},
        'raw_result': {'execution': {'args': ['npx', '-y', 'rea-agents@6.5.0',
                       'extract-firmware', '--format', 'json', '--full-output',
                       '--max-depth', '1'], 'command': 'npx', 'exit_code': 0,
                       'resource_limiter': None, 'signal': None,
                       'stderr': {'bytes': 0, 'observedBytes': 0},
                       'stdout': {'bytes': 0, 'observedBytes': 0}},
                       'report': [],
                       'version_execution': {'args': ['--version'], 'command': src,
                       'exit_code': 0, 'resource_limiter': None, 'signal': None,
                       'stderr': {'bytes': 0, 'observedBytes': 0},
                       'stdout': {'bytes': 0, 'observedBytes': 0}}},
        'relationship_coverage': None,
        'subject': {'architecture': None, 'digest': {'sha256': pin},
                    'format': 'file', 'local_path': src, 'name': name},
    }
    return env, outdir, L, pin

def nr_skeleton(cid, env, outdir, L, pin):
    files = []
    for rel, sha, size in oracle_rows(cid):
        files.append({'analysis_depth': None, 'mime_type': None,
                      'original_file_range': None,
                      'path': outdir + '/firmware.bin_extract/' + rel,
                      'relative_path': 'firmware.bin_extract/' + rel,
                      'reported_sha256': None, 'runtime_address': None,
                      'sha256': sha, 'size': size})
    symlinks = [(r, k, d) for r, k, d in nonreg_rows(cid) if k == 'symlink']
    nr = {
        'chunks': [{'encrypted': False, 'extraction_failed': False,
                     'handler': 'squashfs_v4_be', 'input_path': '$input',
                     'provider_id': 'FAB:1',
                     'range': {'length': L, 'offset': 0},
                     'root_file_range': {'length': L, 'offset': 0}}],
        'coverage': 'partial',
        'depth_limited_paths': ['$output/firmware.bin_extract'],
        'derivations': [{'child_path': '$output/firmware.bin_extract',
                         'handler': 'squashfs_v4_be',
                         'parent_file_range': {'length': L, 'offset': 0},
                         'parent_path': '$input', 'provider_blob_id': 'FAB:1'}],
        'diagnostics': [],
        'engine': {'executable_path': '/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob',
                   'executable_sha256': '0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09',
                   'name': 'unblob', 'source_revision': None,
                   'version': '26.6.4', 'worker_count': 1},
        'extraction_continuations': [{'id': '3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab',
                                      'instruction': 'Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this image.'}],
        'extraction_gaps': [{'continuation_id': '3b54e297653ef5bd5afa64e607b809946398c269f862657ab0544192b7b442ab',
                             'dependencies': [], 'handler': None,
                             'input_path': '$output/firmware.bin_extract',
                             'kind': 'depth-limited', 'provider_id': None,
                             'range': None, 'relative_path': None,
                             'root_file_range': None}],
        'files': files,
        'output_directory': outdir,
        'published_bytes': sum(f['size'] for f in files),
        'selection': {'length': L, 'offset': 0, 'sha256': pin},
        'unpublished_entries': [],
    }
    return nr, symlinks

def gap_for(rel):
    return {'continuation_id': '602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca',
            'dependencies': [], 'handler': None,
            'input_path': '$output/firmware.bin_extract/' + rel,
            'kind': 'unpublished-entry', 'provider_id': None,
            'range': None, 'relative_path': 'firmware.bin_extract/' + rel,
            'root_file_range': None}

def unpub_for(rel, target):
    return {'kind': 'symlink', 'link_target': target,
            'relative_path': 'firmware.bin_extract/' + rel}

def diag_for(rel, outdir):
    return {'input_path': '$input',
            'report': {'__typename__': 'MaliciousSymlinkRemoved',
                       'link': outdir + '/firmware.bin_extract/' + rel,
                       'severity': 'WARNING',
                       'target': '/x'}}

def fab_oracle(cid, scen, removals=()):
    env, outdir, L, pin = base_env(cid, scen)
    nr, symlinks = nr_skeleton(cid, env, outdir, L, pin)
    rem = set(removals)
    for rel, kind, target in symlinks:
        if rel in rem:
            nr['diagnostics'].append(diag_for(rel, outdir))
        else:
            nr['extraction_gaps'].append(gap_for(rel))
            nr['unpublished_entries'].append(unpub_for(rel, target))
    env['normalized_result'] = nr
    return env

def mint(env):
    p = os.path.join(S, 'wrapped.json')
    with open(p, 'w') as fh:
        json.dump({'data': env}, fh)
    r = subprocess.run(['node', XPIN, '--pkg65', PKG, '--pkg67', PKG, p],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('xpin: ' + r.stderr)
    f = r.stdout.splitlines()[0].split('\t')
    return f[1], f[2]

def finalize(env, tag):
    stored, id65 = mint(env)
    if id65.startswith('ev_'):
        env['evidence_id'] = id65
    else:
        env['evidence_id'] = stored
    stored2, id652 = mint(env)
    assert id652 == env['evidence_id'], (id652, env['evidence_id'])
    assert stored2 == id652
    return env

def write_fab(scen, cid, env):
    out = os.path.join(S, 'fab', scen, cid, 'after.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as fh:
        json.dump(env, fh, indent=1)
    return out

def proj_of(path):
    env = json.load(open(path))
    return cc.projection(env, 'plus-extractor')

def cmp_real_fab(cid, fabpath):
    real = os.path.join(LANE, f'corpus/evidence/round-41/c1/{cid}/after.json')
    a = proj_of(real); b = proj_of(fabpath)
    eq, keys, detail = cc.projection_diff(a, b, 'plus-extractor')
    return eq, keys, detail

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 's1':
        # oracle-only, all four. V4 variant b removes 4 chosen absolute-target symlinks.
        v4_removals = []
        for r, k, d in nonreg_rows('V4'):
            if k == 'symlink' and d.startswith('/') and len(v4_removals) < 4:
                v4_removals.append(r)
        for cid in ['V3', 'V4', 'L3', 'L4']:
            rem = v4_removals if cid == 'V4' else ()
            env = fab_oracle(cid, 'fab-oracle', rem)
            finalize(env, 's1')
            path = write_fab('s1', cid, env)
            eq, keys, detail = cmp_real_fab(cid, path)
            print('s1', cid, 'projection_equal_to_real:', eq, 'diff_keys:', keys)
            if detail:
                for k, v in detail.items():
                    if isinstance(v, dict):
                        print('   ', k, v.get('counts'), v.get('committed_only'), v.get('fresh_only'))
                    else:
                        print('   ', k, v)
    elif which == 's2':
        r40 = {'V3': 'V1', 'V4': 'V2', 'L3': 'L1', 'L4': 'L2'}
        for cid, r40id in r40.items():
            src = os.path.join(LANE, f'corpus/evidence/round-40/c1/{r40id}/after.json')
            env = json.load(open(src))
            out = os.path.join(S, 'fab', 's2', cid, 'after.json')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            json.dump(env, open(out, 'w'), indent=1)
            eq, keys, detail = cmp_real_fab(cid, out)
            print('s2', cid, '(from', r40id + ') projection_equal_to_real:', eq, 'diff_keys:', keys)
    elif which == 's3':
        cid = 'L3'
        src = os.path.join(LANE, f'corpus/evidence/round-41/c1/{cid}/after.json')
        env = json.load(open(src))
        nr = env['normalized_result']
        # drop the bin/busy gap + unpublished entry (uncovered symlink)
        before = len(nr['extraction_gaps'])
        nr['extraction_gaps'] = [g for g in nr['extraction_gaps']
                                 if not (g.get('kind') == 'unpublished-entry'
                                         and g.get('relative_path') == 'firmware.bin_extract/bin/busy')]
        nr['unpublished_entries'] = [u for u in nr['unpublished_entries']
                                     if u.get('relative_path') != 'firmware.bin_extract/bin/busy']
        # add one fake published regular file
        nr['files'].append({'analysis_depth': None, 'mime_type': None,
                            'original_file_range': None,
                            'path': env['parameters']['output_directory'] + '/firmware.bin_extract/usr/bin/fake',
                            'relative_path': 'firmware.bin_extract/usr/bin/fake',
                            'reported_sha256': None, 'runtime_address': None,
                            'sha256': 'aa'*32, 'size': 123})
        nr['published_bytes'] = sum(f['size'] for f in nr['files'])
        finalize(env, 's3')
        path = write_fab('s3', cid, env)
        eq, keys, detail = cmp_real_fab(cid, path)
        print('s3 L3 projection_equal_to_real:', eq, 'diff_keys:', keys)
        print('   gaps', before, '->', len(nr['extraction_gaps']), 'files', len(nr['files']))
    elif which == 's4':
        cid = 'V4'
        src = os.path.join(LANE, f'corpus/evidence/round-41/c1/{cid}/after.json')
        env = json.load(open(src))
        nr = env['normalized_result']
        # find removal rels
        rem = [cc.diagnostic_rel(d, 'firmware.bin_extract') for d in nr['diagnostics']]
        rem = [r for r in rem if r]
        # pick a gapped symlink to swap with the first removal
        gapped = [g['relative_path'][len('firmware.bin_extract/'):]
                  for g in nr['extraction_gaps'] if g.get('kind') == 'unpublished-entry']
        B = gapped[0]
        A = rem[0]
        # remove B's gap + unpub; add A's gap + unpub
        nr['extraction_gaps'] = [g for g in nr['extraction_gaps']
                                 if not (g.get('kind') == 'unpublished-entry'
                                         and g.get('relative_path') == 'firmware.bin_extract/' + B)]
        nr['unpublished_entries'] = [u for u in nr['unpublished_entries']
                                     if u.get('relative_path') != 'firmware.bin_extract/' + B]
        nr['extraction_gaps'].append(gap_for(A))
        nr['unpublished_entries'].append(unpub_for(A, '/x'))
        # point the first removal diagnostic at B
        nr['diagnostics'][0]['report']['link'] = (nr['diagnostics'][0]['report']['link']
            .replace('/firmware.bin_extract/' + A, '/firmware.bin_extract/' + B))
        finalize(env, 's4')
        path = write_fab('s4', cid, env)
        eq, keys, detail = cmp_real_fab(cid, path)
        print('s4 V4 (swap gap<->removal) projection_equal_to_real:', eq, 'diff_keys:', keys)
        for k, v in detail.items():
            if isinstance(v, dict):
                print('   ', k, v.get('counts'), v.get('committed_only'), v.get('fresh_only'))
