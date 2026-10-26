#!/usr/bin/env python3
"""R39-C2 counter <-> REAL triage interpreter / generator / table interface check.

Fixture git repo whose freeze commit carries the REAL `sqfs-triage.py`
(R39C2Triage), the REAL `heldout-gen.py` (R39C2HeldoutGen), the REAL
`tools/round-37/gen-squashfs.py`, and a craft-section triage block supplied by
`--table`.  Claim data = 16 real carriers generated from the freeze hash, each
paired with a synthetic envelope carrying the REA feature signature of its
recipe class, so the real interpreter must reproduce the generator's label for
every carrier.  No REA run, no held-out seed.  Expects counter exit 0.

Usage: python3 -I -B real-triage-check.py --lane LANE --gen GEN --triage TRIAGE \
         --table TABLE_BLOCK.md --counter COUNTER --json-out RECEIPT
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

HEADER = ['label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
          'symlink removed', 'published files', 'cause -> action', 'source']


def git(d, *args, check=True):
    r = subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', *args],
                       capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('git %s failed: %s' % (' '.join(args), r.stderr))
    return r


def write(d, rel, data):
    fp = os.path.join(d, rel)
    os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
    with open(fp, 'wb') as f:
        f.write(data if isinstance(data, bytes) else data.encode())


def commit(d, tree, msg):
    for rel, data in tree.items():
        write(d, rel, data)
    git(d, 'add', '-A')
    git(d, 'commit', '-qm', msg, '--allow-empty')
    return git(d, 'rev-parse', 'HEAD').stdout.strip()


def skill_doc(block):
    s = '# K\n\n## Queue-drain craft (x)\n\n- **rule**\n\n'
    if block:
        s += block.strip('\n') + '\n\n'
    return s + '## Next\n\n- x\n'


def feature_envelope(cls, sha):
    """An envelope whose REA features are the signature of the recipe class."""
    env = {'subject': {'name': 'carrier.sqsh', 'digest': {'sha256': sha}, 'format': 'file',
                       'architecture': None, 'local_path': '/fast/scratch/x'},
           'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
           'normalized_result': {'chunks': [], 'extraction_gaps': [], 'files': [],
                                 'diagnostics': []},
           'raw_result': {}}
    nr = env['normalized_result']
    cmd = 'sasquatch-v4be -no-exit-code -f -d /tmp/x /tmp/y'
    if cls in ('clean-be', 'dep-missing-be', 'avm-marker-be-dropped', 'body-extractor-failure',
               'escaping-symlink-removed', 'in-tree-symlink-metadata'):
        nr['chunks'] = [{'handler': 'squashfs_v4_be', 'range': {'offset': 0, 'length': 1024}}]
    elif cls == 'clean-le':
        nr['chunks'] = [{'handler': 'squashfs_v4_le', 'range': {'offset': 0, 'length': 1024}}]
    elif cls == 'dep-missing-le':
        nr['chunks'] = [{'handler': 'squashfs_v4_le', 'range': {'offset': 0, 'length': 1024}}]
    nr['files'] = [{'path': 'a'}, {'path': 'b'}]
    if cls in ('dep-missing-be', 'dep-missing-le'):
        dep = 'squashfs-v4be' if cls == 'dep-missing-be' else 'squashfs'
        dep = 'sasquatch-v4be' if cls == 'dep-missing-be' else 'sasquatch'
        h = 'squashfs_v4_be' if cls == 'dep-missing-be' else 'squashfs_v4_le'
        nr['extraction_gaps'] = [{'kind': 'missing-extractor-dependency', 'handler': h,
                                  'dependencies': [dep]}]
        nr['files'] = []
    elif cls == 'in-tree-symlink-metadata':
        nr['extraction_gaps'] = [{'kind': 'unpublished-entry', 'handler': 'squashfs_v4_be'}]
    elif cls == 'body-extractor-failure':
        nr['extraction_gaps'] = [{'kind': 'extractor-failure', 'handler': 'squashfs_v4_be'}]
        nr['diagnostics'] = [{'report': {'__typename__': 'ExtractCommandFailedReport',
                                         'command': cmd.replace(' -no-exit-code', ' -be -no-exit-code')}}]
    elif cls == 'avm-marker-be-dropped':
        nr['extraction_gaps'] = [{'kind': 'extractor-failure', 'handler': 'squashfs_v4_be'}]
        nr['diagnostics'] = [{'report': {'__typename__': 'ExtractCommandFailedReport',
                                         'command': cmd}}]
    elif cls == 'escaping-symlink-removed':
        nr['diagnostics'] = [{'report': {'__typename__': 'MaliciousSymlinkRemoved'}}]
    return env


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--gen', required=True)
    ap.add_argument('--triage', required=True)
    ap.add_argument('--table')
    ap.add_argument('--skill-doc')
    ap.add_argument('--expect-exit', type=int, default=0)
    ap.add_argument('--counter', required=True)
    ap.add_argument('--json-out', required=True)
    a = ap.parse_args()
    base = os.environ.get('HYAKU_SCRATCH') or os.path.join(tempfile.gettempdir(), 'hyaku')
    sroot = os.path.join(base, 'kaidoku-r39')
    os.makedirs(sroot, exist_ok=True)
    d = tempfile.mkdtemp(prefix='c2-triage.', dir=sroot)
    ev = {'fixture': d, 'note': 'real interpreter + real generator + supplied table'}
    try:
        git(d, 'init', '-q')
        if os.path.realpath(git(d, 'rev-parse', '--show-toplevel').stdout.strip()) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        if a.skill_doc:
            doc = open(a.skill_doc).read()
        else:
            block = open(a.table).read().strip('\n')
            doc = skill_doc(block)
        commit(d, {'SKILL.md': '# K\n\n## Queue-drain craft (x)\n\n- **rule**\n\n## Next\n'}, 'base')
        gen_bytes = open(a.gen, 'rb').read()
        triage_bytes = open(a.triage, 'rb').read()
        counter_bytes = open(a.counter, 'rb').read()
        writer = os.path.join(a.lane, 'tools', 'round-37', 'gen-squashfs.py')
        writer_bytes = open(writer, 'rb').read()
        freeze = commit(d, {
            'SKILL.md': doc,
            'tools/round-39/sqfs-triage.py': triage_bytes,
            'tools/round-39/heldout-gen.py': gen_bytes,
            'tools/round-39/c2-counter.py': counter_bytes,
            'plans/round-39-claims.md': '# claims\n',
            'tools/round-37/gen-squashfs.py': writer_bytes,
        }, 'freeze')
        ev['freeze'] = freeze
        ev['skill_sha256'] = hashlib.sha256(doc.encode()).hexdigest()
        env = dict(os.environ, KAIDOKU_GEN_SQUASHFS=writer)
        out = tempfile.mkdtemp(prefix='gen.', dir=sroot)
        p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, 'tools/round-39/heldout-gen.py'),
                            '--seed', freeze, '--out', out], capture_output=True, text=True,
                           env=env, cwd=a.lane)
        if p.returncode:
            raise SystemExit('generation failed: ' + p.stderr[-1500:])
        man = json.load(open(os.path.join(out, 'manifest.json')))
        claim = {}
        for c in man['carriers']:
            cid = c['id']
            claim['corpus/evidence/round-39/c2/heldout/%s/carrier.sqsh' % cid] = \
                open(os.path.join(out, c['carrier']), 'rb').read()
            envd = feature_envelope(c['class'], c['sha256'])
            claim['corpus/evidence/round-39/c2/heldout/%s/envelope.json' % cid] = \
                json.dumps(envd, indent=1, sort_keys=True)
            c['envelope'] = cid + '/envelope.json'
        claim['corpus/evidence/round-39/c2/heldout/manifest.json'] = \
            json.dumps(man, indent=2, sort_keys=True) + '\n'
        rev = commit(d, claim, 'claim data')
        ev['rev'] = rev
        ev['classes'] = man['classes']
        ev['n'] = len(man['carriers'])
        p = subprocess.run([sys.executable, '-I', '-B', a.counter, '--root', d, '--rev', rev,
                            '--freeze', freeze, '--json-out', a.json_out],
                           capture_output=True, text=True, cwd=sroot)
        ev['counter_exit'] = p.returncode
        ev['counter_stdout'] = p.stdout.strip()
        ev['counter_stderr_tail'] = p.stderr[-1200:]
        rec = json.load(open(a.json_out))
        ev['matched'] = rec.get('matched')
        ev['bindings_false'] = rec.get('bindings_false')
        ev['met_target'] = rec.get('met_target')
        ev['met_target_consistent'] = rec.get('met_target_consistent')
        ev['unevaluable'] = rec.get('unevaluable')
        ev['interpreter_exit'] = rec.get('interpreter_exit')
        ev['interpreter_stderr_tail'] = rec.get('interpreter_stderr_tail')
        ev['per_carrier'] = [{'id': r.get('id'), 'class': r.get('class'),
                              'expected': r.get('expected_label'), 'label': r.get('label'),
                              'match': r.get('class_match')}
                             for r in rec.get('carriers', [])]
        ev['expect_exit'] = a.expect_exit
        if a.expect_exit == 0:
            ok = p.returncode == 0 and rec.get('met_target') is True \
                and rec.get('matched') == len(man['carriers'])
        else:
            ok = p.returncode == a.expect_exit and rec.get('met_target') is not True
        ev['result'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(ev, indent=1, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)
        for name in os.listdir(sroot):
            if name.startswith('gen.') and os.path.isdir(os.path.join(sroot, name)):
                shutil.rmtree(os.path.join(sroot, name), ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
