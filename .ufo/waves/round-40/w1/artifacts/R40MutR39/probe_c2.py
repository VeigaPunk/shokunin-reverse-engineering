#!/usr/bin/env python3
"""Differential fixtures for surviving c2-counter mutants (replicates the counter's
own selftest build(); pristine vs mutant measure() on the same fixture repo)."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
os.makedirs(os.path.join(S, 'hyaku'), exist_ok=True)

spec = importlib.util.spec_from_file_location('c2p', os.path.join(S, 'c2-counter.py'))
P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)

SKILL, GEN, MANIFEST, HEADER = P.SKILL, P.GEN, P.MANIFEST, P.HEADER
STUB_GEN, STUB_INTERP = P.STUB_GEN, P.STUB_INTERP
sroot = os.path.join(S, 'hyaku')


def row(label, pat):
    return ['`%s`' % label, '`%s`' % pat, '`*`', '`*`', '`*`', '`*`', '`*`', 'reason', '`corpus/k.md:1-1`']


GREEN_TABLE = [row('clean', 'clean'), row('dep-missing-be', 'dep-missing-be')]


def table_text(rows, trail_last=False):
    sep = '|' + '---|' * len(HEADER)
    lines = ['| ' + ' | '.join(HEADER) + ' |', sep]
    lines += ['| ' + ' | '.join(r) + ' |' for r in rows]
    if trail_last:
        lines[-1] = lines[-1] + ' '
    return '\n'.join(lines)


def skill_doc(rows):
    s = '# K\n\n## Queue-drain craft (x)\n\n- **rule** text\n\n'
    if rows is not None:
        s += '<!-- sqfs-triage-table v1 -->\n\n' + table_text(rows) + '\n\n'
    return s + '## Next\n\n- other\n'


def write_tree(d, tree):
    for p, c in tree.items():
        fp = os.path.join(d, p)
        os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
        with open(fp, 'wb') as f:
            f.write(c if isinstance(c, bytes) else c.encode())


def commit(d, tree, msg='x'):
    write_tree(d, tree)
    subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                    'commit', '-qm', msg, '--allow-empty'], check=True)
    return subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()


def build(params):
    """Replica of the counter's selftest build() with extra hooks:
    seed_override, trail_space, op_sub, carrier_diverge, label_drift."""
    d = tempfile.mkdtemp(prefix='c2-probe.', dir=sroot)
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d)
    commit(d, {'SKILL.md': skill_doc(None)}, 'base')
    tool_tree = {SKILL: skill_doc(GREEN_TABLE), 'tools/round-39/sqfs-triage.py': STUB_INTERP,
                 'tools/round-39/heldout-gen.py': STUB_GEN,
                 'tools/round-39/c2-counter.py': '# counter\n',
                 'plans/round-39-claims.md': '# claims\n'}
    freeze = commit(d, tool_tree, 'freeze')
    gdir = tempfile.mkdtemp(prefix='gen.', dir=sroot)
    gen_path = os.path.join(d, GEN)
    pr = subprocess.run([sys.executable, '-I', '-B', gen_path, '--seed', freeze, '--out', gdir],
                        capture_output=True, text=True)
    assert pr.returncode == 0, pr.stderr
    rman = json.load(open(os.path.join(gdir, 'manifest.json')))
    man = {'seed': (params['seed_override'](freeze) if callable(params.get('seed_override'))
                    else params.get('seed_override') or freeze),
           'generator': GEN, 'classes': rman['classes'], 'carriers': []}
    claim_files = {}
    for c in rman['carriers']:
        cid = c['id']
        body = open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb').read()
        if params.get('carrier_diverge') and cid == 'H01':
            body = body + b'X'
        base = 'corpus/evidence/round-39/c2/heldout/' + cid
        op = 'xextract_firmwarey' if (params.get('op_sub') and cid == 'H03') else 'extract_firmware'
        env = {'subject': {'name': 'carrier.sqsh', 'digest': {'sha256': hashlib.sha256(body).hexdigest()},
                           'format': 'file', 'architecture': None, 'local_path': '/fast/scratch/x'},
               'operation': op, 'provider': {'id': 'unblob'},
               'normalized_result': {'extraction_gaps': [], 'files': [], 'chunks': [],
                                     'diagnostics': []},
               'stub_class': c.get('label', c['class'])}
        if params.get('label_drift') and cid == 'H05':
            env['stub_class'] = 'clean'
        claim_files[base + '/carrier.sqsh'] = body
        claim_files[base + '/envelope.json'] = json.dumps(env, indent=1, sort_keys=True)
        entry = dict(c)
        if params.get('label_drift') and cid == 'H05':
            entry['label'] = 'clean'
        if params.get('carrier_diverge') and cid == 'H01':
            entry['sha256'] = hashlib.sha256(body).hexdigest()
        man['carriers'].append(entry)
    man_text = json.dumps(man, indent=1, sort_keys=True)
    post = {}
    if params.get('trail_space'):
        post[SKILL] = skill_doc(GREEN_TABLE)  # placeholder, replaced below
    tree = dict(claim_files)
    tree[MANIFEST] = man_text
    if params.get('trail_space'):
        # rebuild SKILL.md at rev with a trailing space on the LAST table row line
        s = '# K\n\n## Queue-drain craft (x)\n\n- **rule** text\n\n<!-- sqfs-triage-table v1 -->\n\n'
        s += table_text(GREEN_TABLE, trail_last=True) + '\n\n## Next\n\n- other\n'
        post[SKILL] = s
    tree.update(post)
    rev = commit(d, tree, 'claim data')
    return d, freeze, rev


def load_mutant(mid):
    import mutate
    for m_id, tool, old, new, clause, prov in mutate.MUTANTS:
        if m_id == mid:
            path = os.path.join(S, 'mut-%s.py' % mid)
            shutil.copy(os.path.join(S, tool), path)
            src = open(path, encoding='utf-8').read()
            assert src.count(old) == 1, (mid, src.count(old))
            open(path, 'w', encoding='utf-8').write(src.replace(old, new))
            sp = importlib.util.spec_from_file_location('c2m' + mid, path)
            mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
            return mod
    raise SystemExit('unknown mutant ' + mid)


def run_case(name, params, mids):
    d, freeze, rev = build(params)
    out = {}
    try:
        for tag, mod in [('pristine', P)] + [(m, load_mutant(m)) for m in mids]:
            try:
                r = mod.measure(d, rev, freeze)
                out[tag] = {'exit': 0 if r['met_target'] else 1, 'met': r['met_target'],
                            'matched': r['matched'],
                            'false': r['bindings_false']}
            except mod.Unevaluable as e:
                out[tag] = {'exit': 2, 'reason': e.reason}
        print('%s\t%s' % (name, json.dumps(out, sort_keys=True)))
        return out
    finally:
        shutil.rmtree(d, ignore_errors=True)


results = {}
results['P-N-M1'] = run_case('P-N-M1 seed 8-prefix',
                             dict(seed_override=lambda fz: fz[:8] + 'a' * 32), ['N-M1'])
results['P-N-M2'] = run_case('P-N-M2 table trailing-space', dict(trail_space=True), ['N-M2'])
results['P-N-M5'] = run_case('P-N-M5 operation substring', dict(op_sub=True), ['N-M5'])
results['P-M06-M29'] = run_case('P-M06+M29 committed-diverges-from-regen',
                                dict(carrier_diverge=True), ['M06', 'M29'])
results['P-M04'] = run_case('P-M04 regen label drift', dict(label_drift=True), ['M04'])

json.dump(results, open(os.path.join(S, 'probe-c2-results.json'), 'w'), indent=1)
print('wrote probe-c2-results.json')
