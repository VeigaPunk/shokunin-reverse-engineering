#!/usr/bin/env python3
"""W2C1Forge fixture driver. Builds scratch commits on top of the landing
revision (read-only against the lane; all writes go to scratch clones) and
scores them with the FROZEN counter copy (sha256 checked against FREEZE blob)."""
import json, os, subprocess, sys, shutil, hashlib

S = '/fast/scratch/hyaku/kaidoku-r49/W2C1Forge'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
FREEZE = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
PRE = '14936cb9df3897f89f8bc1eef3fe269f7d7df313'  # decc5697^ (pre-freeze)
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
NPXCACHE_SRC = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6'
IDS = ['v1le', 'v1be', 'v2le', 'v2be']
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'carrier_size_ok', 'carrier_fresh_ok',
           'layout_ok', 'carve_ok', 'oracle_ok', 'tree_ok', 'receipt_present',
           'receipt_fresh', 'evidence_envelope_ok', 'subject_pin_ok', 'operation_ok',
           'handler_ok', 'chunks_ok', 'oracle_hits_ok', 'gaps_ok',
           'nonregular_unpublished_ok', 'path_shape_ok', 'run_provenance_ok',
           'evidence_id_ok', 'projection_ok')
BASE_ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku',
                GIT_NO_REPLACE_OBJECTS='1')
EVD = 'corpus/evidence/round-49/c1'


def git(*a, cwd=None, env=None, inp=None, check=True):
    r = subprocess.run(['git', *a], cwd=cwd, capture_output=True,
                       env=env or BASE_ENV, input=inp)
    if check and r.returncode:
        raise SystemExit('git %s failed: %s' % (a, r.stderr.decode(errors='replace')))
    return r.stdout


def show(path, rev=REV):
    return git('-C', LANE, 'show', '%s:%s' % (rev, path))


def jload(raw):
    return json.loads(raw)


def jdump(obj):
    return (json.dumps(obj, indent=1, ensure_ascii=False) + '\n').encode()


os.makedirs(S + '/mint', exist_ok=True)
XPIN = S + '/xpin-attribute.mjs'


def mint(env, tag='x'):
    """Re-mint evidence id with the frozen 6.5.0 rule (xpin tool, same as counter)."""
    p = '%s/mint/%s.wrapped.json' % (S, tag)
    with open(p, 'w') as fh:
        json.dump({'data': env}, fh)
    r = subprocess.run(['node', XPIN, '--pkg65', PKG, '--pkg67', PKG, p],
                       capture_output=True, text=True, env=BASE_ENV)
    if r.returncode:
        raise SystemExit('xpin failed: ' + r.stderr)
    f = r.stdout.strip().split('\t')
    return f[2], f[1]  # (recomputed under 6.5.0, stored)


def newcommit(name, changes, parent=REV, base_tree_rev=None, date=None, parents=None):
    """changes: list of (op, path, payload). op in write|link|rm. Returns commit sha."""
    D = '%s/fx/%s' % (S, name)
    shutil.rmtree(D, ignore_errors=True)
    os.makedirs(os.path.dirname(D), exist_ok=True)
    git('clone', '-q', '--shared', '--no-checkout', LANE, D)
    top = git('-C', D, 'rev-parse', '--show-toplevel').decode().strip()
    assert top == D, (top, D)
    git('-C', D, 'config', 'user.name', 'W2C1Forge fixture')
    git('-C', D, 'config', 'user.email', 'fixture@invalid')
    idx = {'GIT_INDEX_FILE': '%s/.git/tmpidx' % D}
    env = dict(BASE_ENV, **idx)
    git('-C', D, 'read-tree', base_tree_rev or parent, env=env)
    for op, path, payload in changes:
        if op == 'rm':
            git('-C', D, 'update-index', '--force-remove', path, env=env)
            continue
        if op == 'blobsha':  # payload = (mode, sha) of an existing blob
            mode, sha = payload
            git('-C', D, 'update-index', '--add', '--cacheinfo',
                '%s,%s,%s' % (mode, sha, path), env=env)
            continue
        mode = '120000' if op == 'link' else '100644'
        data = payload.encode() if isinstance(payload, str) else payload
        blob = git('-C', D, 'hash-object', '-w', '--stdin', inp=data).decode().strip()
        git('-C', D, 'update-index', '--add', '--cacheinfo',
            '%s,%s,%s' % (mode, blob, path), env=env)
    tree = git('-C', D, 'write-tree', env=env).decode().strip()
    cenv = dict(env)
    if date:
        cenv['GIT_AUTHOR_DATE'] = date
        cenv['GIT_COMMITTER_DATE'] = date
    plist = []
    for p in (parents or [parent]):
        plist += ['-p', p]
    commit = git('-C', D, 'commit-tree', tree, *plist, '-m', name, env=cenv).decode().strip()
    return D, commit


def rec_bytes(id_):
    return show('%s/%s/after.json' % (EVD, id_))


def relabel_changes():
    ch = []
    for i in IDS:
        e = jload(show('corpus/evidence/round-44/c1/%s/after.json' % i))
        od = '/fast/scratch/hyaku/kaidoku-r49/relabel/%s/rea-out' % i
        e['parameters']['output_directory'] = od
        if isinstance(e.get('normalized_result'), dict) and 'output_directory' in e['normalized_result']:
            e['normalized_result']['output_directory'] = od
        new_id, _ = mint(e, 'rel-' + i)
        e['evidence_id'] = new_id
        ch.append(('write', '%s/%s/after.json' % (EVD, i), jdump(e)))
    return ch


def oracle_members(i):
    c = jload(show('tools/round-49/carriers.json'))
    for x in c['carriers']:
        if x['id'] == i:
            return x['oracle']
    raise SystemExit('no carrier ' + i)


def fab_changes():
    ch = []
    for i in IDS:
        tmpl = jload(show('corpus/evidence/round-44/c1/%s/after.json' % i))
        od = '/fast/scratch/hyaku/kaidoku-r49/fab/%s/rea-out' % i
        tmpl['parameters']['output_directory'] = od
        tmpl['normalized_result']['output_directory'] = od
        orc = oracle_members(i)
        rows = []
        for m in orc.get('members', []):
            if m.get('type', 'regular') != 'regular':
                continue
            rel = m['path']
            rows.append({'path': od + '/firmware.bin_extract/' + rel,
                         'relative_path': 'firmware.bin_extract/' + rel,
                         'sha256': m['sha256'], 'reported_sha256': m['sha256'],
                         'size': m['size'], 'mime_type': 'text/plain',
                         'analysis_depth': 1, 'original_file_range': None,
                         'runtime_address': None})
        rows.sort(key=lambda r: r['relative_path'])
        tmpl['normalized_result']['files'] = rows
        tmpl['normalized_result']['published_bytes'] = sum(r['size'] for r in rows)
        new_id, _ = mint(tmpl, 'fab-' + i)
        tmpl['evidence_id'] = new_id
        ch.append(('write', '%s/%s/after.json' % (EVD, i), jdump(tmpl)))
    return ch


def r49(i):
    return jload(rec_bytes(i))


def remint_write(env, i, tag):
    nid, _ = mint(env, tag + '-' + i)
    env['evidence_id'] = nid
    return ('write', '%s/%s/after.json' % (EVD, i), jdump(env))


def build(name):
    if name == 'rel':
        return newcommit('rel', relabel_changes())
    if name == 'fab':
        return newcommit('fab', fab_changes())
    if name == 'und1':  # provider.version not checked (plan names unblob 26.6.4)
        e = r49('v1le'); e['provider']['version'] = '26.6.3'
        return newcommit('und1', [remint_write(e, 'v1le', 'und1')])
    if name == 'und2':  # depth_limited_paths / extraction_continuations not projected
        e = r49('v2le')
        e['normalized_result']['depth_limited_paths'] = ['firmware.bin_extract/apple1.txt']
        e['normalized_result']['extraction_continuations'] = [
            {'kind': 'continuation', 'relative_path': 'firmware.bin_extract/apple2.txt'}]
        return newcommit('und2', [remint_write(e, 'v2le', 'und2')])
    if name == 'und3':  # committed evidence tree / logs not read
        return newcommit('und3', [
            ('link', EVD + '/v1le/firmware.bin_extract/apple.txt', '/etc/hostname'),
            ('write', EVD + '/v2le/firmware.bin_extract/evil.txt', 'X\n'),
            ('write', EVD + '/v1be/extract-tree.tsv', 'junk\n'),
        ])
    if name in ('und4f', 'und4o'):  # pre-freeze side branch adds the receipts
        date = '2031-01-01T00:00:00Z' if name == 'und4f' else '2000-01-01T00:00:00Z'
        ch = []
        for i in IDS:
            ch.append(('blobsha', '%s/%s/after.json' % (EVD, i),
                       ('100644', git('-C', LANE, 'rev-parse', '%s:%s/%s/after.json' % (REV, EVD, i)).decode().strip())))
        # side commit: parent PRE (pre-freeze, not a descendant of FREEZE)
        D, side = newcommit(name + '-side', ch, parent=PRE, date=date)
        cenv = dict(BASE_ENV, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date,
                    GIT_INDEX_FILE='%s/.git/tmpidx2' % D)
        # merge commit: tree identical to REV's tree (side added identical blobs)
        tree = git('-C', LANE, 'rev-parse', '%s^{tree}' % REV).decode().strip()
        D2 = D
        merge = git('-C', D2, 'commit-tree', tree, '-p', REV, '-p', side, '-m', name + '-merge').decode().strip()
        return D2, merge
    if name == 'und5':
        return LANE, REV  # rerun-binding attack is environmental (npm cache), no commit
    if name == 'ctlsubj':  # subject digest changed on a copied receipt (cross-carrier)
        e = jload(show('%s/v2be/after.json' % EVD))
        e['subject']['digest']['sha256'] = jload(show('tools/round-49/carriers.json'))['carriers'][2]['sha256']
        e['parameters']['path'] = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-42/c2/fixtures/v2-le--squashfs_v2.0_le.bin'
        return newcommit('ctlsubj', [remint_write(e, 'v2le', 'ctlsubj')])
    if name == 'ctlh':  # wrong handler on a v2 carrier
        e = r49('v2le')
        for c in e['normalized_result']['chunks']:
            c['handler'] = 'squashfs_v1'
        for d in e['normalized_result']['derivations']:
            if d.get('handler') == 'squashfs_v2':
                d['handler'] = 'squashfs_v1'
        return newcommit('ctlh', [remint_write(e, 'v2le', 'ctlh')])
    if name == 'ctlg':  # unpublished entry present
        e = r49('v2le')
        e['normalized_result']['unpublished_entries'] = [
            {'kind': 'symlink', 'relative_path': 'firmware.bin_extract/apple1.txt'}]
        return newcommit('ctlg', [remint_write(e, 'v2le', 'ctlg')])
    if name == 'ctls':  # subject digest changed only
        e = r49('v2le')
        e['subject']['digest']['sha256'] = jload(show('tools/round-49/carriers.json'))['carriers'][0]['sha256']
        return newcommit('ctls', [remint_write(e, 'v2le', 'ctls')])
    raise SystemExit('unknown scenario ' + name)


def summarize(d):
    out = {'carriers_matched': d.get('carriers_matched'), 'met_target': d.get('met_target'),
           'bindings_false': d.get('bindings_false'), 'frozen_path_changed': d.get('frozen_path_changed'),
           'failing': d.get('failing'), 'carriers': {}}
    for k, v in (d.get('carriers') or {}).items():
        out['carriers'][k] = {'matched': v.get('matched'),
                              'false_clauses': [c for c in CLAUSES if v.get(c) is not True],
                              'gaps_note': v.get('gaps_note'), 'projection_diff': v.get('projection_diff'),
                              'projection_error': v.get('projection_error')}
    return out


def score(name, root, rev, extra_env=None, pkg=PKG, tag=None):
    tag = tag or name
    os.makedirs(S + '/scores', exist_ok=True)
    out = '%s/scores/%s.json' % (S, tag)
    so = '%s/scores/%s.stdout' % (S, tag)
    env = dict(BASE_ENV, **(extra_env or {}))
    r = subprocess.run(['python3', '-I', '-B', S + '/c1-counter.py', '--root', root, '--rev', rev,
                        '--freeze', FREEZE, '--pkg65', pkg, '--work', '%s/work/%s' % (S, tag),
                        '--json-out', out], capture_output=True, text=True, env=env)
    with open(so, 'w') as fh:
        fh.write(r.stdout)
    d = json.load(open(out)) if os.path.exists(out) else {}
    summ = summarize(d)
    sha = hashlib.sha256(r.stdout.encode()).hexdigest()
    with open('%s/scores/%s.exit' % (S, tag), 'w') as fh:
        fh.write(str(r.returncode) + '\n')
    print(json.dumps({'scenario': tag, 'root': root, 'rev': rev, 'exit': r.returncode,
                      'stdout_sha256': sha, 'counter_sha256': d.get('counter_sha256'),
                      'summary': summ, 'stderr_tail': r.stderr[-300:]}, indent=1, sort_keys=True))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'build':
        for n in sys.argv[2:]:
            D, c = build(n)
            print(n, D, c)
    elif cmd == 'score':
        n, root, rev = sys.argv[2], sys.argv[3], sys.argv[4]
        score(n, root, rev)
    elif cmd == 'mintcheck':
        for i in IDS:
            e = r49(i)
            print(i, 'stored', e['evidence_id'], 'recomputed', mint(e, 'chk-' + i)[0])
    else:
        raise SystemExit('usage')
