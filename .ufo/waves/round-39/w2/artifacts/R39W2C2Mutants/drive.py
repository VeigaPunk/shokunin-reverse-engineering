#!/usr/bin/env python3
"""Differential driver: for each surviving mutant, build a fixture repo where
pristine and mutant DISAGREE, proving the survivor is non-equivalent (a real
missing test) rather than unkillable. Scratch-only; fixture repos are disposable."""
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile

S = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HYAKU_SCRATCH', '/fast/scratch/hyaku')
os.environ.setdefault('TMPDIR', S)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = load(os.path.join(S, 'pristine.py'), 'pristine')
GEN, INTERP = P.GEN, P.INTERP
MDIR = 'corpus/evidence/round-39/c2/heldout'


def git(cwd, *args):
    p = subprocess.run(['git', '-C', cwd, *args], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit('git %s failed: %s' % (args, p.stderr))
    return p.stdout.strip()


def commit(cwd, tree, msg, allow_empty=False):
    for path, content in tree.items():
        fp = os.path.join(cwd, path)
        os.makedirs(os.path.dirname(fp) or cwd, exist_ok=True)
        with open(fp, 'wb') as f:
            f.write(content if isinstance(content, bytes) else content.encode())
    git(cwd, 'add', '-A')
    git(cwd, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-qm', msg,
        *( ['--allow-empty'] if allow_empty else [] ))
    return git(cwd, 'rev-parse', 'HEAD')


def row(label, pat):
    return ['`%s`' % label, '`%s`' % pat, '`*`', '`*`', '`*`', '`*`', '`*`', 'reason', '`corpus/k.md:1-1`']


def skill_doc():
    rows = [row('clean', 'clean'), row('dep-missing-be', 'dep-missing-be')]
    sep = '|' + '---|' * len(P.HEADER)
    table = '\n'.join(['| ' + ' | '.join(P.HEADER) + ' |', sep] +
                      ['| ' + ' | '.join(r) + ' |' for r in rows])
    return ('# K\n\n## Queue-drain craft (x)\n\n- **rule** text\n\n'
            '<!-- sqfs-triage-table v1 -->\n\n' + table + '\n\n## Next\n\n- other\n')


def tool_tree():
    return {'SKILL.md': skill_doc(), INTERP: P.STUB_INTERP, GEN: P.STUB_GEN,
            'tools/round-39/c2-counter.py': '# counter\n', 'plans/round-39-claims.md': '# claims\n'}


def run_gen(d, seed):
    gdir = tempfile.mkdtemp(prefix='drv-gen.', dir=S)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(d, GEN),
                        '--seed', seed, '--out', gdir], capture_output=True, text=True)
    if p.returncode:
        raise SystemExit('stub gen failed: ' + p.stderr)
    return json.load(open(os.path.join(gdir, 'manifest.json'))), gdir


def envelope(sha, stub_class):
    return {'subject': {'name': 'carrier.sqsh', 'digest': {'sha256': sha},
                        'format': 'file', 'architecture': None, 'local_path': '/fast/scratch/x'},
            'operation': 'extract_firmware', 'provider': {'id': 'unblob'},
            'normalized_result': {'extraction_gaps': [], 'files': [], 'chunks': [],
                                  'diagnostics': []},
            'stub_class': stub_class}


def claim_data(d, seed, label_override=None, arm_override=None, body_suffix=None):
    """Returns (manifest_dict, files_dict) with all-green data by default."""
    rman, gdir = run_gen(d, seed)
    man = {'seed': seed, 'generator': GEN, 'classes': rman['classes'], 'carriers': []}
    files = {}
    for c in rman['carriers']:
        cid = c['id']
        body = open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb').read()
        sha = hashlib.sha256(body).hexdigest()
        if body_suffix and cid == 'H01':
            body = body + body_suffix
            sha = hashlib.sha256(body).hexdigest()
        base = MDIR + '/' + cid
        files[base + '/carrier.sqsh'] = body
        lab = (label_override or {}).get(cid, c['label'])
        arm = (arm_override or {}).get(cid, c['arm'])
        files[base + '/envelope.json'] = json.dumps(envelope(sha, lab), indent=1, sort_keys=True)
        man['carriers'].append({'id': cid, 'class': c['class'], 'label': lab, 'arm': arm,
                                'carrier': cid + '/carrier.sqsh', 'sha256': sha,
                                'envelope': cid + '/envelope.json'})
    shutil.rmtree(gdir, ignore_errors=True)
    return man, files


def measure(mod, d, rev, freeze):
    try:
        r = mod.measure(d, rev, freeze)
        return 0 if r['met_target'] else 1, r
    except mod.Unevaluable as e:
        return 2, e.receipt


def report(name, mutant, outcomes):
    p_exit, p_res = outcomes[0]
    m_exit, m_res = outcomes[1]
    flip = p_exit != m_exit
    print('%-4s pristine_exit=%d mutant_exit=%d %s' % (
        name, p_exit, m_exit, 'FLIPS -> non-equivalent survivor CONFIRMED' if flip
        else 'no flip (masked/equivalent)'))
    if flip:
        pk = sorted(k for k, v in p_res.get('bindings', {}).items() if v is not True)
        mk = sorted(k for k, v in m_res.get('bindings', {}).items() if v is not True)
        print('     pristine bindings_false=%s%s' % (pk, (' unevaluable=' + p_res.get('unevaluable', '')) if p_exit == 2 else ''))
        print('     mutant   bindings_false=%s%s' % (mk, (' unevaluable=' + m_res.get('unevaluable', '')) if m_exit == 2 else ''))


def scenario(name, mutant_file, builder):
    M = load(os.path.join(S, mutant_file), 'mut_' + name)
    d = tempfile.mkdtemp(prefix='drv-' + name + '.', dir=S)
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    top = git(d, 'rev-parse', '--show-toplevel')
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit('fixture toplevel mismatch')
    try:
        freeze, rev = builder(d)
        outcomes = [measure(P, d, rev, freeze), measure(M, d, rev, freeze)]
        report(name, mutant_file, outcomes)
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ---- scenario builders; each returns (freeze, rev) -------------------------
def b_upper_seed(d):
    """m01: manifest seed uppercase -> pristine met, m01 rejects (false negative)."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze)
    man['seed'] = freeze.upper()
    rev = commit(d, {**files, P.MANIFEST: json.dumps(man, indent=1, sort_keys=True)}, 'claim')
    return freeze, rev


def b_regen_label(d):
    """m04: regenerated label drifts from committed label; interpreter agrees with committed.
    H05 is a dep-missing-be carrier (regen label 'dep-missing-be'); committed label 'clean'."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze, label_override={'H05': 'clean'})
    rev = commit(d, {**files, P.MANIFEST: json.dumps(man, indent=1, sort_keys=True)}, 'claim')
    return freeze, rev


def b_regen_arm(d):
    """m05: regenerated arm drifts from committed arm."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze, arm_override={'H01': 'before'})
    rev = commit(d, {**files, P.MANIFEST: json.dumps(man, indent=1, sort_keys=True)}, 'claim')
    return freeze, rev


def b_regen_sha(d):
    """m06+m29: H01 committed body diverges from regeneration; manifest sha = committed."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze, body_suffix=b'X')
    rev = commit(d, {**files, P.MANIFEST: json.dumps(man, indent=1, sort_keys=True)}, 'claim')
    return freeze, rev


def b_mixed_order(d):
    """m13: H01 envelope committed before the manifest, H02 after -> any() passes."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze)
    pre = {k: v for k, v in files.items() if k.startswith(MDIR + '/H01/')}
    post = {k: v for k, v in files.items() if k.startswith(MDIR + '/H02/')}
    rest = {k: v for k, v in files.items() if k not in pre and k not in post}
    commit(d, pre, 'H01 before manifest')
    ma = commit(d, {P.MANIFEST: json.dumps(man, indent=1, sort_keys=True), **rest}, 'manifest')
    rev = commit(d, post, 'H02 after manifest')
    return freeze, rev


def b_readd(d):
    """m28: H01 files added, deleted, re-added -> first_add must pick the FIRST add."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze)
    h01 = {k: v for k, v in files.items() if k.startswith(MDIR + '/H01/')}
    rest = {k: v for k, v in files.items() if k not in h01}
    commit(d, h01, 'H01 v1')
    ma = commit(d, {P.MANIFEST: json.dumps(man, indent=1, sort_keys=True), **rest}, 'manifest')
    for k in h01:
        os.remove(os.path.join(d, k))
    git(d, 'add', '-A')
    git(d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-qm', 'drop H01')
    rev = commit(d, h01, 're-add H01')
    return freeze, rev


def b_side_branch(d):
    """m12: manifest first-added on a commit that is NOT a descendant of the freeze
    (sibling branch merged into rev). Needs plumbing."""
    base = commit(d, {}, 'base', allow_empty=True)
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze)
    # side commit off base containing SKILL + claim data (SKILL is not a frozen path)
    wt = tempfile.mkdtemp(prefix='drv-wt.', dir=S)
    subprocess.run(['git', '-C', d, 'worktree', 'add', '-q', '--detach', wt, base], check=True)
    try:
        side_tree = {'SKILL.md': tool_tree()['SKILL.md'],
                     P.MANIFEST: json.dumps(man, indent=1, sort_keys=True), **files}
        for path, content in side_tree.items():
            fp = os.path.join(wt, path)
            os.makedirs(os.path.dirname(fp) or wt, exist_ok=True)
            with open(fp, 'wb') as f:
                f.write(content if isinstance(content, bytes) else content.encode())
        subprocess.run(['git', '-C', wt, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', wt, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                        'commit', '-qm', 'claim data on side branch'], check=True)
        ma = git(wt, 'rev-parse', 'HEAD')
    finally:
        subprocess.run(['git', '-C', d, 'worktree', 'remove', '--force', wt], capture_output=True)
    tree = git(d, 'rev-parse', ma + '^{tree}')
    env = dict(os.environ, GIT_AUTHOR_NAME='fx', GIT_AUTHOR_EMAIL='fx@fx',
               GIT_COMMITTER_NAME='fx', GIT_COMMITTER_EMAIL='fx@fx')
    rev = subprocess.run(['git', '-C', d, 'commit-tree', tree, '-p', freeze, '-p', ma],
                         capture_output=True, text=True, env=env)
    if rev.returncode:
        raise SystemExit('commit-tree failed: ' + rev.stderr)
    return freeze, rev.stdout.strip()


def b_orphan(d):
    """m27: rev does not descend from the freeze -> pristine exit 2, m27 measures (exit 1)."""
    freeze = commit(d, tool_tree(), 'freeze')
    man, files = claim_data(d, freeze)
    subprocess.run(['git', '-C', d, 'checkout', '-q', '--orphan', 'side'], check=True)
    subprocess.run(['git', '-C', d, 'rm', '-rq', '--cached', '.'], check=True, capture_output=True)
    for path, content in {**files, P.MANIFEST: json.dumps(man, indent=1, sort_keys=True)}.items():
        fp = os.path.join(d, path)
        os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
        with open(fp, 'wb') as f:
            f.write(content if isinstance(content, bytes) else content.encode())
        # drop the frozen-path files from the orphan worktree so the frozen check stays clean
    for stale in ('SKILL.md', INTERP, GEN, 'tools/round-39/c2-counter.py', 'plans/round-39-claims.md'):
        fp = os.path.join(d, stale)
        if os.path.exists(fp):
            os.remove(fp)
    rev = commit(d, {}, 'orphan claim data')
    return freeze, rev


SCENARIOS = [
    ('m01', 'm01.py', b_upper_seed),
    ('m04', 'm04.py', b_regen_label),
    ('m05', 'm05.py', b_regen_arm),
    ('m06', 'm06.py', b_regen_sha),
    ('m29', 'm29.py', b_regen_sha),
    ('m12', 'm12.py', b_side_branch),
    ('m13', 'm13.py', b_mixed_order),
    ('m27', 'm27.py', b_orphan),
    ('m28', 'm28.py', b_readd),
]

for name, mf, builder in SCENARIOS:
    scenario(name, mf, builder)
print('driver done')
