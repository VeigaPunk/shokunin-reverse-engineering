#!/usr/bin/env python3
"""Doc-binding attack harness (C1DocBindings). Builds variant commits on top of the
POS sandbox HEAD (real REA receipts + draft landing) in a scratch clone, then scores each
with the DRAFT counter against the DEV freeze. Only documentation bytes change per variant."""
import json, os, re, subprocess, sys, hashlib, time
from concurrent.futures import ThreadPoolExecutor

S = os.environ['TMPDIR']
LANE_BASE_SOURCES = subprocess.run(['git', '-C', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin', 'show', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9:corpus/SOURCES.md'], capture_output=True).stdout
POS = sys.argv[1]            # sandbox-pos path
DEV = sys.argv[2]            # dev freeze hash
CLONE = os.path.join(S, 'var')
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
STEM = '2026-10-28-r49-squashfs-v1v2-core'
ART = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts/R49C1Doc'
ENTRY_TEXT = open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts/R49EntryDraft/' + ENTRY, 'rb').read()

def git(*a, inp=None, check=True):
    p = subprocess.run(['git', '-C', CLONE, *a], capture_output=True, input=inp)
    if check and p.returncode:
        raise SystemExit('git %s: %s' % (a, p.stderr.decode()))
    return p.stdout

def show(path, rev):
    return subprocess.run(['git', '-C', POS, 'show', '%s:%s' % (rev, path)], capture_output=True).stdout

if os.path.isdir(CLONE):
    subprocess.run(['rm', '-rf', CLONE])
subprocess.run(['git', 'clone', '-q', '--shared', POS, CLONE], check=True)
assert subprocess.run(['git', '-C', CLONE, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip() == CLONE
git('config', 'user.name', 'r49-c1-docbindings-attack'); git('config', 'user.email', 'attack@r49.invalid')
POS_REV = git('rev-parse', 'HEAD').decode().strip()

BASE = {p: show(p, POS_REV) for p in ['PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', ENTRY]}

def line_with(text, needle, start=None):
    idx = [i for i, l in enumerate(text.split('\n')) if (l.startswith(start) if start else needle in l)]
    assert len(idx) == 1, (needle, start, idx)
    return idx[0]

def replace_line(blob, idxfn, new):
    lines = blob.decode().split('\n')
    i = idxfn(lines)
    lines[i] = new
    return '\n'.join(lines).encode()

def prov_row_idx(lines):
    return [i for i, l in enumerate(lines) if l.startswith('| `squashfs_v1` and `squashfs_v2`')][-1]

def prov_note_idx(lines):
    return [i for i, l in enumerate(lines) if l.startswith('Round-49 frontier note')][0]

def readme_r49_idx(lines):
    return [i for i, l in enumerate(lines) if 'SquashFS v1/v2 through REA (round 44)' in l and STEM in l][0]

def src_row_idx(sid):
    def f(lines):
        return [i for i, l in enumerate(lines) if l.startswith('| %s |' % sid)][0]
    return f

ROW_BASE = BASE['PROVINCE.md'].decode().split('\n')[prov_row_idx(BASE['PROVINCE.md'].decode().split('\n'))]
NOTE_BASE = BASE['PROVINCE.md'].decode().split('\n')[prov_note_idx(BASE['PROVINCE.md'].decode().split('\n'))]
README_BASE = BASE['corpus/README.md'].decode().split('\n')[readme_r49_idx(BASE['corpus/README.md'].decode().split('\n'))]
ROW_ART = open(ART + '/block-a-province-round-49-core-row.md').read().strip()
NOTE_ART = open(ART + '/block-b-province-frontier-note.md').read().strip()
README_ART_RAW = open(ART + '/block-c-readme-coverage-map-row.md').read().strip()

def set_prov(row=None, note=None, fence=False):
    t = BASE['PROVINCE.md'].decode()
    lines = t.split('\n')
    if row is not None:
        lines[prov_row_idx(lines)] = row
    if note is not None:
        lines[prov_note_idx(lines)] = note
    if fence:
        h = lines.index('## Round-49 additions to Core')
        r = prov_row_idx(lines)
        lines.insert(r + 1, '```')
        lines.insert(h, '```')
    return '\n'.join(lines).encode()

def set_readme(row):
    lines = BASE['corpus/README.md'].decode().split('\n')
    lines[readme_r49_idx(lines)] = row
    return '\n'.join(lines).encode()

def set_src(sid_fn):
    lines = BASE['corpus/SOURCES.md'].decode().split('\n')
    return sid_fn(lines)

def sources_used_append(lines):
    # the POS landing: append ENTRY to S138/S139 used-by (exactly as the draft landing does)
    out = []
    for l in lines:
        if re.match(r'^ {0,3}\|\s*(S138|S139)\s*\|', l) and ENTRY not in l:
            l = l.rstrip().rstrip('|').rstrip() + ', ' + ENTRY + ' |'
        out.append(l)
    return out

def base_sources():
    return sources_used_append(BASE['corpus/SOURCES.md'].decode().split('\n'))

def s_bytes(lines):
    return '\n'.join(lines).encode()

V = {}
# 0 control: the POS landing unchanged
V['00_pos_baseline'] = {}
# 1 control: entry deleted
V['01_entry_missing'] = {ENTRY: None}
# 2 hollow row: negates the promotion, still names both handlers, the family, and the entry path
V['02_row_negated'] = {'PROVINCE.md': set_prov(row='| `squashfs_v1` and `squashfs_v2` (SquashFS v1/v2): **not promoted**, both stay Frontier; see `%s` | none | none | `%s` |' % (ENTRY, ENTRY))}
# 3 control: row without the entry path
V['03_row_no_entry_path'] = {'PROVINCE.md': set_prov(row='| `squashfs_v1` and `squashfs_v2` (SquashFS v1/v2) | x | y | the round-44 entry |')}
# 4 hollow section: the whole Core section sits inside a fenced code block (renders as literal text)
V['04_section_fenced'] = {'PROVINCE.md': set_prov(fence=True)}
# 5 hollow note: negated, placed where it is read as a claim
V['05_note_negated'] = {'PROVINCE.md': set_prov(note='- Round-49 frontier note, 2026-10-28: `%s` is an empty placeholder; SquashFS v1/v2 remain Frontier and supersede nothing.' % STEM)}
# 6 control: note without the SquashFS v1/v2 token
V['06_note_no_token'] = {'PROVINCE.md': set_prov(note='- Round-49 frontier note, 2026-10-28: `%s` supersedes the frontier clause for the handler family.' % STEM)}
# 7 hollow entry: two source lines naming S138/S139 and no content at all
V['07_entry_hollow_sources_only'] = {ENTRY: b'# E\n\nsource: S138\nsource: S139\n'}
# 8 entry present but zero bytes (entry_present is existence only)
V['08_entry_zero_bytes'] = {ENTRY: b''}
# 9 sourced satisfied by tokens in a non-citation sentence
V['09_source_tokens_not_citations'] = {ENTRY: b'# E\n\nsource: none for this entry; S138 and S139 are named here only so the registry binding can read them.\n'}
# 10 sourced: the registry rows keep 'mined' and carry a forged duplicate row appended
def dup_rows(lines):
    out = sources_used_append(lines)
    extra = []
    for sid in ('S138', 'S139'):
        r = [l for l in out if l.startswith('| %s |' % sid)][0]
        extra.append(r.replace('| mined |', '| rejected |'))
    return out + extra
V['10_sources_dup_row_forged'] = {'corpus/SOURCES.md': s_bytes(dup_rows(BASE['corpus/SOURCES.md'].decode().split('\n')))}
# 11 sourced: registry status column says rejected; counter reads only id/opened/used-by
def rejected(lines):
    out = sources_used_append(lines)
    return [l.replace('| mined |', '| rejected |') if re.match(r'^\| S13[89] \|', l) else l for l in out]
V['11_sources_status_rejected'] = {'corpus/SOURCES.md': s_bytes(rejected(BASE['corpus/SOURCES.md'].decode().split('\n')))}
# 12 control: registry left at base (no used-by append) -> sourced must go false
V['12_sources_not_appended'] = {'corpus/SOURCES.md': LANE_BASE_SOURCES}
# 13 hollow readme row: negated, still carries the stem in the coverage map
V['13_readme_negated'] = {'corpus/README.md': set_readme('| SquashFS v1/v2 through REA (round 49) | `%s` | **Frontier** — not promoted; the stem is a placeholder | none |' % STEM)}
# 14 control: readme row without the stem
V['14_readme_no_stem'] = {'corpus/README.md': set_readme('| SquashFS v1/v2 through REA (round 49) | `see the lesson` | **Core** | none |')}
# 15 placeholder left in the coverage row (AFTER-DATA marker never replaced)
V['15_readme_marker_left'] = {'corpus/README.md': set_readme(README_ART_RAW)}
# 16 ALL HOLLOW: every documentation binding satisfied by text that states nothing true
hollow_entry = b'# E\n\nsource: S138 (see registry)\nsource: S139 (see registry)\n'
V['16_all_documentation_hollow'] = {
    'PROVINCE.md': set_prov(row='| `squashfs_v1` and `squashfs_v2` (SquashFS v1/v2): **not promoted** | none | none | `%s` |' % ENTRY,
                            note='- Round-49 frontier note, 2026-10-28: `%s` is a placeholder; SquashFS v1/v2 remain Frontier.' % STEM, fence=True),
    'corpus/README.md': set_readme('| SquashFS v1/v2 through REA (round 49) | `%s` | **Frontier** | none |' % STEM),
    'corpus/SOURCES.md': s_bytes(rejected(BASE['corpus/SOURCES.md'].decode().split('\n'))),
    ENTRY: hollow_entry,
}
# 17 copy-last-round: the round-44 entry bytes at the round-49 path, registry appended, round-44 row kept
V['17_copy_r44_entry_as_r49'] = {ENTRY: subprocess.run(['git', '-C', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin', 'show', 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9:corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md'], capture_output=True).stdout}
# 18 copy-last-round with the round-44 row and stem text: positive as to all six bindings
V['18_copy_r44_entry_and_row_text'] = {ENTRY: V['17_copy_r44_entry_as_r49'][ENTRY], 'corpus/README.md': set_readme(README_BASE.replace('r44', 'r49'))}

def make_commit(name, edits):
    git('checkout', '-q', '--detach', POS_REV)
    for path, blob in edits.items():
        full = os.path.join(CLONE, path)
        if blob is None:
            if os.path.exists(full):
                os.remove(full)
            git('add', '-A', '--', path, check=False)
            continue
        os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
        open(full, 'wb').write(blob)
    # every other documentation file keeps the POS bytes; the sources, row, note and README
    # that a variant does not name are reset to POS so each variant changes only what it names
    for path in ['PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', ENTRY]:
        if path not in edits:
            full = os.path.join(CLONE, path)
            if BASE[path] is None:
                continue
            open(full, 'wb').write(BASE[path])
    git('add', '-A', '--', 'PROVINCE.md', 'corpus/README.md', 'corpus/SOURCES.md', 'corpus/knowledge')
    if not git('diff', '--cached', '--name-only').strip():
        return POS_REV
    git('commit', '-q', '-m', 'attack ' + name)
    return git('rev-parse', 'HEAD').decode().strip()

def score(name, rev):
    w = os.path.join(S, 'w', name); os.makedirs(w, exist_ok=True)
    out = os.path.join(w, 'counter.json')
    t0 = time.time()
    p = subprocess.run(['python3', '-I', '-B', os.path.join(CLONE, 'tools/round-49/c1-counter.py'),
                        '--root', CLONE, '--rev', rev, '--freeze', DEV, '--pkg65', PKG,
                        '--work', w, '--json-out', out], capture_output=True, cwd=w)
    res = {'variant': name, 'rev': rev, 'exit': p.returncode,
           'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(), 'wall_s': round(time.time() - t0, 1)}
    try:
        d = json.load(open(out))
        b = d.get('bindings', {})
        res['met_target'] = d.get('met_target')
        res['carriers_matched'] = d.get('carriers_matched')
        res['failing'] = d.get('failing')
        res['docs'] = {k: b.get(k) for k in ['province_core_section', 'province_core_row', 'frontier_note',
                                             'entry_present', 'sourced', 'coverage_map_row']}
        res['counter_sha256'] = d.get('counter_sha256')
    except Exception as e:
        res['error'] = repr(e) + ' stderr=' + p.stderr.decode()[-300:]
    return res

# build commits sequentially (single clone), score in parallel from immutable commits
revs = {}
for name, edits in V.items():
    revs[name] = make_commit(name, edits)
    print('commit', name, revs[name], flush=True)
# NB: the counter reads bytes from git objects, so scoring a rev never needs the checkout
with ThreadPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(lambda kv: score(*kv), revs.items()))
json.dump(results, open(os.path.join(S, 'att', 'results.json'), 'w'), indent=1)
for r in results:
    print(json.dumps(r, sort_keys=True))
