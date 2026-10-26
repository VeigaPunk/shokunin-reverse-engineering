#!/usr/bin/env python3
"""Counter-sensitivity probes for round-38 command_a on a sandbox clone.

Each case starts from the clone HEAD tree, applies one mutation, commits with
fixture identity, and calls the imported command_a at that commit (base = the
round-40 base, fa6a8a3f...). Nothing outside the sandbox is written.
"""
import importlib.util, json, os, re, subprocess, sys

ROOT = sys.argv[1]
BASE = 'fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f'
C38 = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py'
spec = importlib.util.spec_from_file_location('c2r38', C38)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert subprocess.run(['git', '-C', ROOT, 'rev-parse', '--show-toplevel'],
                      capture_output=True, text=True).stdout.strip() == ROOT, 'sandbox toplevel mismatch'
HEAD0 = subprocess.run(['git', '-C', ROOT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()


def commit(msg):
    subprocess.run(['git', '-C', ROOT, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', ROOT, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                    'commit', '-q', '-m', msg, '--allow-empty'], check=True)
    return subprocess.run(['git', '-C', ROOT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()


def reset():
    subprocess.run(['git', '-C', ROOT, 'read-tree', '--reset', '-u', HEAD0], check=True)


def edit(path, fn):
    p = os.path.join(ROOT, path)
    t = open(p).read()
    n = fn(t)
    assert n != t, f'mutation was a no-op on {path}'
    open(p, 'w').write(n)


def measured(rev, label):
    a = mod.command_a(ROOT, rev)
    print(json.dumps({'case': label, 'rev': rev[:8], **a}, sort_keys=True))
    return a


cases = []
# T0 control
cases.append(('T0 control clone HEAD', None))
res = {}
res['T0'] = measured(HEAD0, 'T0 control clone HEAD')

# T1 drop one stem from the coverage-map section only
def t1():
    reset()

    def f(t):
        head, rest = t.split('## Coverage map\n', 1)
        sec, tail = rest.split('\n## ', 1)
        sec2 = re.sub(r'(?m)^\| SquashFS `extract-firmware` outcome triage v2 \(round 40\).*\n', '', sec)
        assert sec2 != sec
        return head + '## Coverage map\n' + sec2 + '\n## ' + tail
    edit('corpus/README.md', f)
    return commit('fx: remove v2 map row')
res['T1'] = measured(t1(), 'T1 coverage-map row removed')

# T2 block 19 precise ranges -> bare filenames
def t2():
    reset()

    def f(t):
        def sub(m):
            return m.group(1).rstrip(':0123456789-')
        n = re.sub(r'(corpus/knowledge/2026-10-26-r40-sqfs-triage-v2\.md):\d+-\d+', sub, t)
        assert n != t
        return n
    edit('SKILL.md', f)
    return commit('fx: bare citations in block 19')
res['T2'] = measured(t2(), 'T2 block19 precise ranges -> bare filenames')

# T3 out-of-file range on block 19 (entry has 56 lines)
def t3():
    reset()

    def f(t):
        n = t.replace('corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:46-56',
                      'corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:46-57')
        assert n != t
        return n
    edit('SKILL.md', f)
    return commit('fx: range past EOF')
res['T3'] = measured(t3(), 'T3 block19 range past EOF (46-57 of 56)')

# T4 new citation-free rule block
def t4():
    reset()
    edit('SKILL.md', lambda t: t.replace(
        '## Config custody for live-probe rounds (SOP)',
        '- **Empty rule (fx).** No citation at all.\n\n## Config custody for live-probe rounds (SOP)', 1))
    return commit('fx: citation-free block')
res['T4'] = measured(t4(), 'T4 citation-free rule block appended')

# T5 block 19 cites a nonexistent knowledge file
def t5():
    reset()

    def f(t):
        n = t.replace('corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:11-18',
                      'corpus/knowledge/2026-10-26-r40-nonexistent-entry.md:11-18')
        assert n != t
        return n
    edit('SKILL.md', f)
    return commit('fx: missing entry cite')
res['T5'] = measured(t5(), 'T5 block19 cites missing knowledge file')
reset()

json.dump({'head0': HEAD0, 'base': BASE, 'results': res}, open(os.environ['OUT'], 'w'), indent=1, sort_keys=True)
