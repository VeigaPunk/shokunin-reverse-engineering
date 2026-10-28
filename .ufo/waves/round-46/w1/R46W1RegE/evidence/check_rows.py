"""Row-format check for seat R46W1RegE, scored by the FROZEN round-46 registry.py.

No lane writes: the frozen tools are copied into scratch and imported; every fixture
tree is in memory (registry.score takes a `files` callable, not a repo).
"""
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FREEZE = '31820472784284727546808acc31b3ea1e73919b'
S = '/fast/scratch/hyaku/kaidoku-r46/R46W1RegE'
REG = os.path.join(S, 'reg')
ROWS = os.path.join(LANE, '.ufo/waves/round-46/w1/R46W1RegE/rows.md')

os.makedirs(REG, exist_ok=True)
for f in ('tools/round-46/registry.py', 'tools/round-46/gate.py'):
    b = subprocess.run(['git', '-C', LANE, 'show', '%s:%s' % (FREEZE, f)],
                       capture_output=True, check=True).stdout
    open(os.path.join(REG, os.path.basename(f)), 'wb').write(b)
sys.path.insert(0, REG)
import registry  # noqa: E402

HEAD = ('| tool | gate or probe - purpose | verdict map (exit codes) | '
        'self-test command | pinned-value path | write scope | owner |')
SEP = '|' + '---|' * 7


def doc(rows):
    return ('# K\n\n## x\n\n<!-- instrument-registry v2 -->\n\n' + HEAD + '\n' + SEP
            + '\n' + '\n'.join(rows) + '\n\n<!-- /instrument-registry -->\n\n## y\n')


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


rows = [l for l in open(ROWS).read().splitlines() if l.strip()]
print('rows:', len(rows))

# ---- clause 0 sanity: shape of each row -------------------------------------
bad = []
for r in rows:
    c = cells(r)
    key = c[0]
    ticks = r.count('`')
    if len(c) != 7:
        bad.append('cells %d != 7: %s' % (len(c), key))
    if not (key.startswith('`') and key.endswith('`') and len(key) > 2):
        bad.append('cell 0 not one backticked path: %r' % key)
    if ticks != 2:
        bad.append('backticks %d != 2 (only cell 0 may be backticked): %s' % (ticks, key))
    if any('`' in x for x in c[1:]):
        bad.append('backtick outside cell 0: %s' % key)
print('shape_violations:', json.dumps(bad))

mine = [cells(r)[0][1:-1] for r in rows]
print('my_paths:', json.dumps(mine))


def files_fn(paths):
    census = json.dumps({'rule': 'probe', 'paths': paths}).encode()

    def files(p):
        if p == registry.CENSUS:
            return census
        return b'' if p in paths else None
    return files


def score(rowtext, paths, label):
    rc, rec = registry.score(doc(rowtext), files_fn(paths), 'r46', 'v2', 'REV',
                             battery=None)
    print('\n=== %s' % label)
    print(json.dumps({'exit': rc, 'scope_size': rec['scope_size'],
                      'registry_rows': rec['registry_rows'],
                      'header_ok': rec['header'] == registry.HOUSE,
                      'registered': rec['registered'], 'unregistered': rec['unregistered'],
                      'thin': rec['thin'], 'absent_at_rev': rec['absent_at_rev'],
                      'met_target': rec['met_target'], 'failing': rec['failing']},
                     indent=1, sort_keys=True))
    return rc, rec


# A: my three rows alone.
score(rows, mine, 'A my three rows')

# B: the landed round-45 rows, verbatim, under the same house header.
skill = subprocess.run(['git', '-C', LANE, 'show', '%s:SKILL.md' % FREEZE],
                       capture_output=True, check=True, text=True).stdout
lines = skill.splitlines()
start = next(i for i, l in enumerate(lines)
             if l.strip() == '### Round-44/45 instrument registry')
end = next((i for i in range(start + 1, len(lines))
            if lines[i].startswith('## ')), len(lines))
sect = [l for l in lines[start + 1:end] if l.strip().startswith('|')]
landed_cells = [[c.strip() for c in l.strip().strip('|').split('|')] for l in sect]
landed_cells = [c for c in landed_cells if not registry.is_sep(c)][1:]  # drop header
landed = ['| ' + ' | '.join(c) + ' |' for c in landed_cells]
landed_paths = [c[0].strip('`') for c in landed_cells]
print('\nlanded rows:', len(landed), json.dumps(landed_paths))
score(rows + landed, mine + landed_paths, 'B my rows plus the six landed round-45 rows')

# B2: the six landed rows alone, under the house header.
score(landed, landed_paths, 'B2 the six landed round-45 rows alone')

# B3: the six landed rows under their own landed header.
landed_head = [l for l in lines[start + 1:end] if l.strip().startswith('|')][0].strip()
def doc_head(rows, head):
    return ('# K\n\n## x\n\n<!-- instrument-registry v2 -->\n\n' + head + '\n'
            + '|' + '---|' * len([c for c in head.strip('|').split('|')]) + '\n'
            + '\n'.join(rows) + '\n\n<!-- /instrument-registry -->\n\n## y\n')
rc, rec = registry.score(doc_head(landed, landed_head), files_fn(landed_paths),
                         'r46', 'v2', 'REV', battery=None)
print('\n=== B3 landed rows under the landed header')
print(json.dumps({'exit': rc, 'landed_header': landed_head,
                  'house_header': '| ' + ' | '.join(registry.HOUSE) + ' |',
                  'header_ok': rec['header'] == registry.HOUSE,
                  'failing': rec['failing']}, indent=1, sort_keys=True))

# C: negative control, my row 1 worded the way the landed rows word theirs.
thin_row = '| ' + ' | '.join([cells(rows[0])[0],
                              cells(rows[0])[1],
                              '`0` met; `1` not met; `2` could-not-evaluate',
                              cells(rows[0])[3], cells(rows[0])[4],
                              cells(rows[0])[5], cells(rows[0])[6]]) + ' |'
score([thin_row], [mine[0]], 'C control: backticked digits and no = in the verdict cell')

# D: negative control, substring in cell 0 instead of the exact path.
sub_row = '| ' + ' | '.join(['see `%s` (wrapper)' % mine[0]] + cells(rows[0])[1:]) + ' |'
score([sub_row], [mine[0]], 'D control: cell 0 names the path as a substring')
