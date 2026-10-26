#!/usr/bin/env python3
"""Sandbox discrimination battery: run the frozen c2-counter against mutant SKILL tables."""
import json, os, shutil, subprocess, sys

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '42c10a58cb2cae3a4a0122af35a0cf95ac718043'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'
CTL = os.path.join(L, '.ufo/waves/round-40/controls/c2')
S = os.environ['S']
CLONE = open(os.path.join(S, 'clonedir.txt')).read().strip() + '/lane'
OUT = os.path.join(S, 'mutants')
os.makedirs(OUT, exist_ok=True)

top = subprocess.run(['git', '-C', CLONE, 'rev-parse', '--show-toplevel'],
                     capture_output=True, text=True).stdout.strip()
assert os.path.realpath(top) == os.path.realpath(CLONE), top

MARK = '<!-- sqfs-triage-table v2 -->'


def show(rev, path):
    p = subprocess.run(['git', '-C', CLONE, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    return p.stdout.decode()


def block_of(text, mark=MARK):
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == mark)
    end = start
    for i in range(start + 1, len(lines)):
        if lines[i].lstrip().startswith('|'):
            end = i
        elif end > start:
            break
    return start, end, '\n'.join(lines[start:end + 1])


rev_skill = show(REV, 'SKILL.md')
rs, re_, adopted_block = block_of(rev_skill)
print('adopted block lines %d..%d' % (rs + 1, re_ + 1))


def rows_of(block):
    return [l for l in block.splitlines() if l.lstrip().startswith('|')]


def mutate(fn):
    rows = rows_of(adopted_block)
    body = fn(rows)
    head = [l for l in adopted_block.splitlines() if not l.lstrip().startswith('|')]
    return '\n'.join(head + body)


def cells(line):
    return line.strip().strip('|').split('|')


def join(cs):
    return '| ' + ' | '.join(c.strip() for c in cs) + ' |'


def row_by_label(rows, label):
    for i, l in enumerate(rows):
        cs = cells(l)
        if cs and cs[0].strip().strip('`') == label:
            return i, cs
    raise SystemExit('no row %r' % label)


def m_clean_empty_action(rows):
    i, cs = row_by_label(rows, 'clean-empty')
    cs[9] = ' `count-gap` '
    rows[i] = join(cs)
    return rows


def m_swap_files(rows):
    i1, c1 = row_by_label(rows, 'clean')
    i2, c2 = row_by_label(rows, 'clean-empty')
    c1[8], c2[8] = c2[8], c1[8]
    rows[i1], rows[i2] = join(c1), join(c2)
    return rows


def m_avm_be_cell(rows):
    i, cs = row_by_label(rows, 'avm-marker-be-dropped')
    cs[6] = ' `yes` '
    rows[i] = join(cs)
    return rows


def m_merge_failure_rows(rows):
    i, cs = row_by_label(rows, 'partial-body-failure')
    cs[8] = ' `*` '
    rows[i] = join(cs)
    return rows


def m_swap_two_actions(rows):
    i1, c1 = row_by_label(rows, 'avm-marker-be-dropped')
    i2, c2 = row_by_label(rows, 'body-extractor-failure')
    c1[9], c2[9] = c2[9], c1[9]
    rows[i1], rows[i2] = join(c1), join(c2)
    return rows


CASES = []
for name in ('CTL-C2-1', 'CTL-C2-2', 'CTL-C2-3', 'CTL-C2-4', 'CTL-C2-5', 'CTL-C2-6'):
    text = open(os.path.join(CTL, name + '.md')).read()
    _, _, blk = block_of(text)
    CASES.append((name, blk))
CASES += [
    ('MUT-clean-empty-action', mutate(m_clean_empty_action)),
    ('MUT-swap-clean-files', mutate(m_swap_files)),
    ('MUT-avm-be-cell', mutate(m_avm_be_cell)),
    ('MUT-merge-failure-rows', mutate(m_merge_failure_rows)),
    ('MUT-swap-two-actions', mutate(m_swap_two_actions)),
]

results = []
for name, blk in CASES:
    subprocess.run(['git', '-C', CLONE, 'checkout', '-q', '--detach', REV], check=True)
    subprocess.run(['git', '-C', CLONE, 'clean', '-qfd'], check=True)
    new = rev_skill.replace(adopted_block, blk)
    if new == rev_skill:
        raise SystemExit('%s: block substitution was a no-op' % name)
    with open(os.path.join(CLONE, 'SKILL.md'), 'w') as fh:
        fh.write(new)
    subprocess.run(['git', '-C', CLONE, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                    'commit', '-qam', 'mutant %s' % name], check=True)
    commit = subprocess.run(['git', '-C', CLONE, 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip()
    jout = os.path.join(OUT, name + '.json')
    p = subprocess.run([sys.executable, '-I', '-B',
                        os.path.join(L, 'tools/round-40/c2-counter.py'),
                        '--root', CLONE, '--rev', commit, '--freeze', FREEZE,
                        '--json-out', jout], capture_output=True, text=True)
    rec = json.load(open(jout)) if os.path.exists(jout) else {}
    row = {'case': name, 'commit': commit, 'exit': p.returncode,
           'matched': rec.get('matched'), 'n': rec.get('n'),
           'met_target': rec.get('met_target'),
           'bindings_false': rec.get('bindings_false'),
           'distinct_decisions': rec.get('distinct_decisions')}
    wrong = [c['class'] for c in rec.get('carriers', []) if not c.get('pair_match')]
    row['missed_classes'] = sorted(set(wrong))
    results.append(row)
    print(json.dumps(row, sort_keys=True))

with open(os.path.join(OUT, 'battery.json'), 'w') as fh:
    json.dump(results, fh, indent=1, sort_keys=True)
print('wrote', os.path.join(OUT, 'battery.json'))
