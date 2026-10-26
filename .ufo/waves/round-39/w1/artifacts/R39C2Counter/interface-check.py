#!/usr/bin/env python3
"""R39-C2 counter <-> real generator/writer interface check.

Builds a throwaway fixture git repo whose freeze commit carries the REAL
`heldout-gen.py` (the R39C2HeldoutGen seat artifact) and the REAL
`tools/round-37/gen-squashfs.py`, generates the claim data with 16 carriers
(8 recipe classes, 2 each) from the freeze hash, then runs the counter and
expects exit 0.  The triage interpreter in the fixture is a stub that labels
from a fixture-only `stub_class` envelope field; the real `sqfs-triage.py` is
not part of this check.

Usage: python3 -I -B interface-check.py --lane LANE --gen HELDOUT_GEN --counter C2_COUNTER
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

HEADER = ['label', 'handler', 'gap kinds', 'dependencies', '-be in child argv',
          'symlink removed', 'published files', 'cause -> action', 'source']
LABELS = ['clean', 'escaping-symlink-removed', 'in-tree-symlink-metadata', 'dep-missing-be',
          'dep-missing-le', 'avm-marker-be-dropped', 'body-extractor-failure']

STUB_INTERP = r'''#!/usr/bin/env python3
import argparse, fnmatch, json, sys
ap = argparse.ArgumentParser()
ap.add_argument('--skill')
ap.add_argument('--json', action='store_true')
ap.add_argument('--table-only', action='store_true')
ap.add_argument('envs', nargs='*')
a = ap.parse_args()
lines = open(a.skill).read().splitlines()
start = next((i for i, l in enumerate(lines) if l.startswith('## Queue-drain craft')), None)
if start is None:
    sys.exit(2)
end = len(lines)
for i in range(start + 1, len(lines)):
    if lines[i].startswith('## '):
        end = i
        break
sec = lines[start + 1:end]
mi = next((i for i, l in enumerate(sec) if '<!-- sqfs-triage-table v1 -->' in l), None)
if mi is None:
    sys.exit(2)
ti = next((i for i in range(mi + 1, len(sec)) if sec[i].lstrip().startswith('|')), None)
if ti is None:
    sys.exit(2)
rows = []
for l in sec[ti:]:
    if not l.lstrip().startswith('|'):
        break
    rows.append([c.strip().strip('`').strip() for c in l.strip().strip('|').split('|')])
rules = [(r[0], r[1]) for r in rows[2:]]
out = []
for p in a.envs:
    d = json.load(open(p))
    if isinstance(d, dict) and 'subject' not in d and isinstance(d.get('data'), dict):
        d = d['data']
    cls = d.get('stub_class')
    lab = 'unclassified'
    for label, pat in rules:
        if pat == '*' or (cls and fnmatch.fnmatchcase(cls, pat)):
            lab = label
            break
    out.append((p, lab))
for p, l in out:
    print('%s\t%s' % (p, l))
'''


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


def table_text():
    sep = '|' + '---|' * len(HEADER)
    rows = ['| ' + ' | '.join(['`%s`' % lab, '`%s`' % lab, '`*`', '`*`', '`*`', '`*`', '`*`',
                               'cause', '`corpus/k.md:1-1`']) + ' |' for lab in LABELS]
    return '\n'.join(['| ' + ' | '.join(HEADER) + ' |', sep] + rows)


def skill_doc(rows):
    s = '# K\n\n## Queue-drain craft (x)\n\n- **rule**\n\n'
    if rows:
        s += '<!-- sqfs-triage-table v1 -->\n\n' + rows + '\n\n'
    return s + '## Next\n\n- x\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--gen', required=True)
    ap.add_argument('--counter', required=True)
    ap.add_argument('--json-out', required=True)
    a = ap.parse_args()
    base = os.environ.get('HYAKU_SCRATCH') or os.path.join(tempfile.gettempdir(), 'hyaku')
    root = os.path.join(base, 'kaidoku-r39')
    os.makedirs(root, exist_ok=True)
    d = tempfile.mkdtemp(prefix='c2-iface.', dir=root)
    ev = {'fixture': d, 'note': 'stub triage interpreter; real generator + writer'}
    try:
        git(d, 'init', '-q')
        top = git(d, 'rev-parse', '--show-toplevel').stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        commit(d, {'SKILL.md': skill_doc(None)}, 'base')
        gen_bytes = open(a.gen, 'rb').read()
        counter_bytes = open(a.counter, 'rb').read()
        writer = os.path.join(a.lane, 'tools', 'round-37', 'gen-squashfs.py')
        writer_bytes = open(writer, 'rb').read()
        freeze = commit(d, {
            'SKILL.md': skill_doc(table_text()),
            'tools/round-39/sqfs-triage.py': STUB_INTERP,
            'tools/round-39/heldout-gen.py': gen_bytes,
            'tools/round-39/c2-counter.py': counter_bytes,
            'plans/round-39-claims.md': '# claims\n',
            'tools/round-37/gen-squashfs.py': writer_bytes,
        }, 'freeze')
        ev['freeze'] = freeze
        ev['generator_sha256'] = hashlib.sha256(gen_bytes).hexdigest()
        ev['writer_sha256'] = hashlib.sha256(writer_bytes).hexdigest()

        # two generations with the freeze hash must agree byte for byte
        runs = []
        for i in (1, 2):
            out = tempfile.mkdtemp(prefix='gen-%d.' % i, dir=root)
            env = dict(os.environ, KAIDOKU_GEN_SQUASHFS=writer)
            p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, 'tools/round-39/heldout-gen.py'),
                                '--seed', freeze, '--out', out], capture_output=True, text=True,
                               env=env, cwd=a.lane)
            if p.returncode:
                raise SystemExit('generation %d failed: %s' % (i, p.stderr[-1500:]))
            man = json.load(open(os.path.join(out, 'manifest.json')))
            runs.append({'out': out, 'manifest': man})
        m1, m2 = runs[0]['manifest'], runs[1]['manifest']
        ev['classes'] = m1['classes']
        ev['carriers'] = len(m1['carriers'])
        ev['deterministic_manifest'] = m1 == m2
        ev['deterministic_carriers'] = all(
            open(os.path.join(runs[0]['out'], c['carrier']), 'rb').read() ==
            open(os.path.join(runs[1]['out'], c['carrier']), 'rb').read() for c in m1['carriers'])
        ev['generator_field'] = m1['generator']
        ev['labels'] = sorted({c['label'] for c in m1['carriers']})
        if not (ev['deterministic_manifest'] and ev['deterministic_carriers']):
            raise SystemExit('generator is not deterministic at the freeze hash')

        # claim data: generator manifest verbatim + envelope paths, envelope stubs
        man = dict(m1)
        claim = {}
        for c in man['carriers']:
            cid = c['id']
            src = os.path.join(runs[0]['out'], c['carrier'])
            claim['corpus/evidence/round-39/c2/heldout/%s/carrier.sqsh' % cid] = open(src, 'rb').read()
            env = {'subject': {'name': 'carrier.sqsh',
                               'digest': {'sha256': c['sha256']}, 'format': 'file',
                               'architecture': None, 'local_path': '/fast/scratch/x'},
                   'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
                   'normalized_result': {'chunks': [], 'extraction_gaps': [], 'files': [],
                                         'diagnostics': []},
                   'stub_class': c['label']}
            claim['corpus/evidence/round-39/c2/heldout/%s/envelope.json' % cid] = \
                json.dumps(env, indent=1, sort_keys=True)
            c['envelope'] = cid + '/envelope.json'
        claim['corpus/evidence/round-39/c2/heldout/manifest.json'] = \
            json.dumps(man, indent=2, sort_keys=True) + '\n'
        rev = commit(d, claim, 'claim data')
        ev['rev'] = rev

        p = subprocess.run([sys.executable, '-I', '-B', a.counter, '--root', d, '--rev', rev,
                            '--freeze', freeze, '--json-out', a.json_out],
                           capture_output=True, text=True, cwd=root)
        ev['counter_exit'] = p.returncode
        ev['counter_stdout'] = p.stdout.strip()
        ev['counter_stderr_tail'] = p.stderr[-1000:]
        rec = json.load(open(a.json_out))
        ev['matched'] = rec.get('matched')
        ev['n'] = rec.get('n')
        ev['bindings_false'] = rec.get('bindings_false')
        ev['met_target'] = rec.get('met_target')
        ev['met_target_consistent'] = rec.get('met_target_consistent')
        ev['table'] = rec.get('table')
        ev['writer'] = rec.get('writer')
        ok = p.returncode == 0 and rec.get('met_target') is True
        ev['result'] = 'PASS' if ok else 'FAIL'
        print(json.dumps(ev, indent=1, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)
        for name in os.listdir(root):
            if name.startswith('gen-') and os.path.isdir(os.path.join(root, name)):
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
