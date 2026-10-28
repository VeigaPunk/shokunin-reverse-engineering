#!/usr/bin/env python3
# CritFreeze scenario driver: builds manoeuvre commits in scratch clones of the dev-freeze base,
# then runs the freeze walk of BOTH counters (C1 frozen_drift via import of the frozen bytes;
# C2 CLI freeze_check) and records the verdicts. Scratch only. Every mutating git call names -C.
import json, os, subprocess, sys, hashlib, time, importlib.util, shutil

S = '/fast/scratch/hyaku/kaidoku-r49/CritFreeze'
F_OUT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/CritFreeze'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
BASE = S + '/base'
FREEZE = '34a25bac3921f74dd9137266703e4ee689de64b0'
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')


def g(d, *a, check=True, inp=None):
    p = subprocess.run(['git', '-C', d, *a], capture_output=True, input=inp, env=ENV)
    if check and p.returncode != 0:
        raise SystemExit('git %s failed in %s: %s' % (' '.join(a), d, p.stderr.decode()))
    return p


def mkrepo(name, src=BASE, at=FREEZE):
    d = os.path.join(S, 'sc', name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    subprocess.run(['git', 'clone', '-q', '--shared', src, d], check=True, env=ENV)
    top = g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip()
    assert top == d, (top, d)
    g(d, 'config', 'user.name', 'r49-crit'); g(d, 'config', 'user.email', 'r49-crit@dev.invalid')
    g(d, 'checkout', '-q', '--detach', at)
    return d


def commit(d, msg):
    g(d, 'commit', '-q', '--allow-empty', '-m', msg)
    return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()


def write(d, rel, text):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as fh:
        fh.write(text)


# ---------------------------------------------------------------- manoeuvres
def m_benign(d):
    write(d, 'notes/benign.txt', 'x\n'); g(d, 'add', '-A'); return commit(d, 'benign')


def touch_restore(rel):
    def f(d):
        with open(os.path.join(d, rel), 'a') as fh: fh.write('\n# probe\n')
        g(d, 'add', rel); commit(d, 'touch ' + rel)
        g(d, 'checkout', FREEZE, '--', rel); g(d, 'add', rel)
        return commit(d, 'restore ' + rel)
    return f


def m_new_file(rel):
    def f(d):
        write(d, rel, 'probe\n'); g(d, 'add', rel); return commit(d, 'new ' + rel)
    return f


def m_merge_edit_carriers(d):
    # side branch: unrelated commit; main: merge commit itself edits carriers.json
    g(d, 'checkout', '-q', '-b', 'side', FREEZE)
    write(d, 'notes/side.txt', 's\n'); g(d, 'add', '-A'); commit(d, 'side')
    g(d, 'checkout', '-q', '-b', 'main2', FREEZE)
    write(d, 'notes/main.txt', 'm\n'); g(d, 'add', '-A'); commit(d, 'main')
    g(d, 'merge', '-q', '--no-ff', '--no-commit', 'side')
    p = os.path.join(d, 'tools/round-49/carriers.json')
    s = open(p).read(); open(p, 'w').write(s.replace('{', '{ ', 1))
    g(d, 'add', 'tools/round-49/carriers.json')
    g(d, 'commit', '-q', '-m', 'merge edits carriers')
    return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()


def m_evil_merge_revert(d):
    # side branch edits carriers.json (b1); the merge resolves the file back to FREEZE bytes
    g(d, 'checkout', '-q', '-b', 'side', FREEZE)
    p = os.path.join(d, 'tools/round-49/carriers.json')
    open(p, 'a').write('\n'); g(d, 'add', 'tools/round-49/carriers.json'); commit(d, 'side edits carriers')
    g(d, 'checkout', '-q', '-b', 'main2', FREEZE)
    write(d, 'notes/main.txt', 'm\n'); g(d, 'add', '-A'); commit(d, 'main')
    g(d, 'merge', '-q', '--no-ff', '--no-commit', 'side')
    g(d, 'checkout', FREEZE, '--', 'tools/round-49/carriers.json')
    g(d, 'add', 'tools/round-49/carriers.json')
    g(d, 'commit', '-q', '-m', 'merge resolves carriers back to freeze')
    return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()


def m_side_new_file_merged(d):
    g(d, 'checkout', '-q', '-b', 'side', FREEZE)
    write(d, 'tools/round-49/side-new.py', 'x\n'); g(d, 'add', '-A'); commit(d, 'side new tool')
    g(d, 'checkout', '-q', '-b', 'main2', FREEZE)
    write(d, 'notes/main.txt', 'm\n'); g(d, 'add', '-A'); commit(d, 'main')
    g(d, 'merge', '-q', '--no-ff', '-m', 'merge side new tool', 'side')
    return g(d, 'rev-parse', 'HEAD').stdout.decode().strip()


def m_rename(src, dst):
    def f(d):
        os.makedirs(os.path.dirname(os.path.join(d, dst)), exist_ok=True)
        g(d, 'mv', src, dst); return commit(d, 'rename %s -> %s' % (src, dst))
    return f


def m_mode(rel):
    def f(d):
        os.chmod(os.path.join(d, rel), 0o644); g(d, 'add', rel); return commit(d, 'mode ' + rel)
    return f


def m_symlink(rel):
    def f(d):
        g(d, 'rm', '-q', rel); os.symlink('../../corpus/README.md', os.path.join(d, rel))
        g(d, 'add', rel); return commit(d, 'symlink ' + rel)
    return f


def m_delete(rel):
    def f(d):
        g(d, 'rm', '-q', rel); return commit(d, 'delete ' + rel)
    return f


# ---------------------------------------------------------------- walks
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(S, 'frozen', name + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def c1_walk(d, rev):
    m = load('c1-counter')
    spec = json.loads(g(d, 'show', FREEZE + ':tools/round-49/carriers.json').stdout)
    try:
        return {'touched': m.frozen_drift(d, FREEZE, rev, spec)}
    except Exception as e:
        return {'error': repr(e)}


def c2_walk(d, rev):
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(S, 'frozen', 'c2-mismatch.py'),
                        '--root', d, '--rev', rev, '--freeze', FREEZE], capture_output=True, env=ENV,
                       cwd=S)
    try:
        j = json.loads(p.stdout.decode())
    except Exception:
        j = {'raw': p.stdout.decode()[-300:], 'err': p.stderr.decode()[-300:]}
    return {'exit': p.returncode, 'reason': j.get('reason'), 'detail': j.get('detail'),
            'mismatches': j.get('mismatches'), 'freeze_check_passed': 'reason' not in j}


def c1_cli(d, rev):
    w = os.path.join(S, 'cli-work', os.path.basename(d)); shutil.rmtree(w, ignore_errors=True)
    os.makedirs(w)
    jo = os.path.join(w, 'out.json')
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, '-I', '-B', os.path.join(S, 'frozen', 'c1-counter.py'),
                            '--root', d, '--rev', rev, '--freeze', FREEZE, '--pkg65', PKG,
                            '--work', w, '--json-out', jo],
                           capture_output=True, env=ENV, cwd=S, timeout=240)
        rc = p.returncode; err = p.stderr.decode()[-200:]
    except subprocess.TimeoutExpired:
        rc, err = 'timeout240', ''
    j = json.load(open(jo)) if os.path.exists(jo) else {}
    return {'exit': rc, 'reason': j.get('reason'), 'frozen_path_changed': j.get('frozen_path_changed'),
            'secs': round(time.time() - t0, 1), 'stderr_tail': err}


SCEN = [
    ('S0_benign_nonfrozen', m_benign),
    ('S1a_touch_restore_c1counter', touch_restore('tools/round-49/c1-counter.py')),
    ('S1b_touch_restore_c2mismatch', touch_restore('tools/round-49/c2-mismatch.py')),
    ('S1c_touch_restore_c1controls', touch_restore('tools/round-49/c1-controls.py')),
    ('S1d_touch_restore_carriers', touch_restore('tools/round-49/carriers.json')),
    ('S1e_touch_restore_c1oracle', touch_restore('tools/round-49/c1-oracle.py')),
    ('S2a_new_file_tools', m_new_file('tools/round-49/probe-new.py')),
    ('S2b_new_file_nested', m_new_file('tools/round-49/control-fixtures/new/x.json')),
    ('S3a_merge_commit_edits_carriers', m_merge_edit_carriers),
    ('S3b_side_edit_reverted_in_merge', m_evil_merge_revert),
    ('S3c_side_new_tool_merged', m_side_new_file_merged),
    ('S4_rename_inside', m_rename('tools/round-49/c1-controls.py', 'tools/round-49/c1-ctl.py')),
    ('S5_rename_out', m_rename('tools/round-49/c2-mismatch.py', 'tools/round-49-moved/c2-mismatch.py')),
    ('S6_rename_in_nonfrozen', m_rename('corpus/README.md', 'tools/round-49/README.md')),
    ('S7_mode_change', m_mode('tools/round-49/c1-counter.py')),
    ('S8_symlink_swap', m_symlink('tools/round-49/c2-mismatch.py')),
    ('S9_delete_file', m_delete('tools/round-49/c1-oracle.py')),
]


def main():
    which = sys.argv[1:] or None
    # frozen counter bytes: extract from the FREEZE commit itself
    os.makedirs(os.path.join(S, 'frozen'), exist_ok=True)
    for n in ('c1-counter.py', 'c2-mismatch.py', 'c1-controls.py', 'carriers.json'):
        open(os.path.join(S, 'frozen', n), 'wb').write(
            g(BASE, 'show', FREEZE + ':tools/round-49/' + n).stdout)
    res = {}
    for name, fn in SCEN:
        if which and not any(name.startswith(w) for w in which):
            continue
        d = mkrepo(name)
        rev = fn(d)
        assert g(d, 'rev-parse', '--show-toplevel').stdout.decode().strip() == d
        rec = {'rev': rev, 'c1_walk': c1_walk(d, rev), 'c2_walk': c2_walk(d, rev)}
        res[name] = rec
        print(json.dumps({name: rec}, sort_keys=True), flush=True)
    os.makedirs(F_OUT, exist_ok=True)
    json.dump(res, open(os.path.join(S, 'results-walk.json'), 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
