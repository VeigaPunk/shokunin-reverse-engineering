#!/usr/bin/env python3
"""ScribeRowsSources — build the four SOURCES append rows for round-50 attempt 2,
plus the search-log entry, and prove the block on a scratch registry copy.

Read-only on the lane tree: reads /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md,
writes only under the seat dir and the seat scratch.

Entry path is the frozen counter's ENTRY constant (tools/round-50/c1-counter.py:377-378):
    corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md
"""
import hashlib
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SEAT = LANE + '/.ufo/waves/round-50/w3/ScribeRowsSources'
S = os.environ.get('S', '/fast/scratch/hyaku/kaidoku-r50/w3-ScribeRowsSources')
REG = LANE + '/corpus/SOURCES.md'
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'
OPENED = '2026-10-28'          # first opened (attempt 1); re-open 2026-10-29 in the Gate
CENSUS = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'

# ---------------------------------------------------------------- the four rows
ROWS = [
    # id, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used-by
    ('S243',
     'Freetz patch 101, `AVM_LE`/`AVM_BE` symbols — '
     'https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/'
     '101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch',
     'code', 'B',
     'the AVM LE/BE symbol definitions and the byte order they select; not an LE layout, '
     'not a marker definition, not AVM-authored text',
     '`:7` `+#define AVM_LE 2`; `:17-18` the LE condition selects `__LITTLE_ENDIAN`; '
     'sha256 `e28b3341…4c707` (1,153 B), byte-identical at Freetz-NG `9a723692`; HTTP 200 2026-10-29',
     'Read the LE AVM claim as a symbol definition, not a format spec: this patch adds the '
     '`AVM_LE` symbol and the byte order only, so the marker on the LE carriers is an '
     'observation of their bytes',
     'mined', OPENED, '180d', ENTRY),
    ('S244',
     'AVM FRITZ!OS download index — https://download.avm.de/fritzbox/ (root listing) and the four '
     'carrier model `fritz.os/` directories; HTTP 200 2026-10-29',
     'dataset', 'A',
     'which firmware images AVM publishes per model directory and their listed sizes and dates; '
     'not image contents, not tar members, not the licence',
     '`fritzbox-{7581/other,7582/other,6490-cable/deutschland,6430-cable/deutschland}/fritz.os/`; '
     'listing rows 19-Aug-2024 32010240 B, 19-Aug-2024 32256000 B, 04-Sep-2023 39741440 B, '
     '05-Sep-2023 35911680 B',
     'Bind a carrier to the publisher\'s own listed file, size and date, so the chain pin is the '
     'vendor\'s row and not a re-measurement',
     'mined', OPENED, '90d', ENTRY),
    ('S245',
     'unblob SquashFS v4 little-endian handler at tag 26.6.4 — '
     'https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py',
     'code', 'A',
     'the little-endian v4 handler and its sasquatch `-le` argv; not the BE AVM branch '
     '(S108, S112), not the extractor, not other versions',
     '`:53-54` `case Endian.LITTLE, _:` then `commands_args.append("-le")`; `:455` '
     '`NAME = "squashfs_v4_le"`; tag 26.6.4 = `1fcc7a0a`, sha256 `2d7b901b…599287` (19,842 B); '
     'HTTP 200 2026-10-29',
     'Name the LE path exactly: every little-endian member gets plain `sasquatch -le`, so an '
     'AVM-marker LE member and a standard LE member take one handler and one argv',
     'mined', OPENED, '180d', ENTRY),
    ('S249',
     'AVM FRITZ!OS firmware licence, publisher info_en.txt — '
     'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt',
     'docs', 'A',
     'the AVM firmware licence restricts redistribution of the package; not a SquashFS layout, '
     'extraction or carrier claim',
     '`:850` "The licensee may create only one copy of the software, which may be used exclusively '
     'for backup use." (18 words); sha256 `6c601b34…070a7` (67,591 B); HTTP 200 2026-10-29',
     'Ground the chain-pinned custody in the publisher\'s own licence: one personal backup copy '
     'only, so carrier bytes are fetched and pinned, never committed',
     'mined', OPENED, '90d', ENTRY),
]

SEARCH_LOG = (
    '- 2026-10-29 round 50 attempt 2 (C1 source re-open) — Question: do the four C1 source rows '
    'survive a re-open, and can they be registered now that the C1 entry cites them? Where searched: '
    'the four canonical URLs re-fetched today — the Freetz `squashfs4-host-be` patch 101 raw file, '
    'the AVM download index root and the four carrier `fritz.os/` model directories, the unblob '
    '26.6.4 `squashfs.py` raw file, and the 6490-cable `info_en.txt`; every body was digested and '
    'every located quote re-checked against the served bytes (receipts under '
    '`.ufo/waves/round-50/w3/ScribeRowsSources/`). Identified 4, screened 4, included 4 '
    '(S243, S244, S245, S249), excluded 0; the 2026-10-28 round-50 entry\'s separate 3/3/3/0 '
    'count covers the three C2 correction rows already landed as S246-S248, and this entry '
    'counts only the four C1 rows. The re-open is byte-identical to the attempt-1 fetch of '
    '2026-10-28 (root index `75e886e2…`, 7581 `c1dd76d6…`, 7582 `18ccf345…`, 6490 `4de20237…`, '
    '6430 `ab4da28c…`, patch 101 `e28b3341…`, unblob `2d7b901b…`, licence `6c601b34…`), so the '
    'attempt-1 quotes still locate and the digests are unchanged. Excluded: none — S114 (the '
    'AVM-BE format note) is unchanged and stays as it is, and the attempt-1 Gate rows for these '
    'four sources stay in the lesson as the record of the earlier honest stop. Stop: the four '
    'sources are unchanged, the four claims the C1 entry needs are covered by them, and no further '
    'source family was opened, so the search ends at the C1 source set.'
)

GATE_ROWS = [
    ('S243',
     'https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/'
     '101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch (1,153 B, sha256 `e28b3341…4c707`)',
     '2026-10-28, HTTP 200; re-opened 2026-10-29, HTTP 200, same digest',
     '`:7` "+#define AVM_LE 2" (4 words); `:17-18` the byte-order condition naming `SQUASHFS4_LE` '
     'or `AVM_LE` selects `__LITTLE_ENDIAN`',
     '**admit** (tier B, `mined`): the patch defines the `AVM_LE` symbol and the byte order only; '
     'it adds no marker and no LE layout text, so the LE marker remains an observation of the '
     'carriers\' bytes (`w1/C1SrcFreetz.md` F1-F5). Attempt-1 held the row back under the honest '
     'stop; the C1 entry now cites it.'),
    ('S244',
     'https://download.avm.de/fritzbox/ and the four carrier `fritz.os/` model dirs '
     '(7581/other, 7582/other, 6490-cable/deutschland, 6430-cable/deutschland) '
     '(8,990 B root; 574, 574, 604, 604 B listings)',
     '2026-10-28, HTTP 200; re-opened 2026-10-29, HTTP 200, same digests',
     'listing row `FRITZ.Box_7581-07.18.image` `19-Aug-2024 12:33` `32010240` (a listing row, '
     '6 fields)',
     '**admit** (tier A, `mined`): the publisher\'s own listing gives each carrier\'s image file, '
     'size and date, so the chain pin is the vendor\'s row. Attempt-1 held the row back under the '
     'honest stop; the C1 entry now cites it.'),
    ('S245',
     'https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/'
     'squashfs.py (19,842 B, sha256 `2d7b901b…599287`)',
     '2026-10-28, HTTP 200; re-opened 2026-10-29, HTTP 200, same digest',
     '`:455` `NAME = "squashfs_v4_le"` (4 words); `:53-54` `case Endian.LITTLE, _:` then '
     '`commands_args.append("-le")`',
     '**admit** (tier A, `mined`): a same-URL, different-scope row against S108/S112 (the BE '
     'branch, opened 2026-10-26); the census emits the expected `W04` duplicate-URL warning and '
     'no error. Attempt-1 held the row back under the honest stop; the C1 entry now cites it.'),
    ('S249',
     'https://download.avm.de/fritzbox/fritzbox-6490-cable/deutschland/fritz.os/info_en.txt '
     '(67,591 B, sha256 `6c601b34…070a7`)',
     '2026-10-28, HTTP 200; re-opened 2026-10-29, HTTP 200, same digest',
     '`:850` "The licensee may create only one copy of the software, which may be used exclusively '
     'for backup use." (18 words)',
     '**admit** (tier A, `mined`): the licence wording is why the carriers are chain-pinned and '
     'never committed. Attempt-1 held the row back under the honest stop; the C1 entry now cites it.'),
]


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def check_row(r):
    rid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby = r
    assert len(r) == 11, (rid, len(r))
    for i, c in enumerate(r):
        assert '|' not in c, (rid, i, 'pipe in cell')
    assert re.fullmatch(r'S\d{3,}', rid), rid
    assert kind in ('spec', 'docs', 'paper', 'code', 'tool', 'dataset', 'talk', 'book',
                     'community', 'own-work'), (rid, kind)
    assert tier in 'ABC' and len(tier) == 1, (rid, tier)
    assert status in ('queued', 'mined', 'rejected'), (rid, status)
    assert re.fullmatch(r'\d{4}-\d{2}-\d{2}', opened), (rid, opened)
    assert re.fullmatch(r'(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)', recheck), (rid, recheck)
    assert usedby == ENTRY, (rid, usedby)


def render(r):
    return '| ' + ' | '.join(r) + ' |'


for r in ROWS:
    check_row(r)

maxlen = max((len(c), r[0], i) for r in ROWS for i, c in enumerate(r))
print('max cell length:', maxlen[0], 'in row', maxlen[1], 'cell', maxlen[2])
for r in ROWS:
    for i, c in enumerate(r):
        if len(c) > 200:
            print('OVER-200 cell:', r[0], 'cell', i, len(c))

# ---------------------------------------------------------------- the draft file
rows_md = []
rows_md.append('# SOURCES append rows — round 50 attempt 2 (seat ScribeRowsSources)\n')
rows_md.append(
    'Draft for the L1 to land into `corpus/SOURCES.md`. **Not applied to the lane tree.**\n')
rows_md.append(
    'Entry path in every `used-by` cell: `%s`\n' % ENTRY)
rows_md.append(
    'This is the frozen counter\'s `ENTRY` constant (`tools/round-50/c1-counter.py:377-378`), '
    'pinned by the attempt-2 claims correction commit `6f4aba63`. The w3 dispatch text named a '
    'stale stem (`2026-10-29-r50-le-avm-hsqs-core`); the counter is the rule, so the rows cite '
    '`%s`. The counter\'s `sourced` binding (`c1-counter.py:2468-2476`) wants rows whose id is '
    'cited by the entry\'s `source:` lines, whose `opened` is 2026-10-28 or 2026-10-29, and whose '
    '`used-by` names this entry path or stem — all four rows satisfy it.\n' % STEM)
rows_md.append(
    'Rows are placed in ascending id order (S243, S244, S245 after the S149 row; S249 after '
    'S248), the same placement the lane\'s own landing script uses for the round-50 correction '
    'rows; the registry stays append-only (no existing row is edited).\n')
rows_md.append('## The four rows\n')
rows_md.append('```markdown')
for r in ROWS:
    rows_md.append(render(r))
rows_md.append('```\n')
rows_md.append(
    'Cell lengths: max %d chars (row %s, cell %d) — under the 200-char guide. Eleven columns '
    'per row, no `|` inside any cell, ids `S243`/`S244`/`S245`/`S249` are free in the registry '
    '(it ends at S248; S150-S242 stay skipped as earlier lessons record). `opened` is 2026-10-28 '
    '(first opened in attempt 1); the attempt-2 re-open of 2026-10-29 is recorded in the round '
    'lesson\'s `## Gate` (below) and in the receipts.\n' % (maxlen[0], maxlen[1], maxlen[2]))
rows_md.append('## Search-log entry\n')
rows_md.append('Append as the last bullet of the `## Search log` section '
               '(before `## Leads (unopened)`):\n')
rows_md.append('```markdown')
rows_md.append(SEARCH_LOG)
rows_md.append('```\n')
rows_md.append('## Round-lesson `## Gate` rows (the L1 integrates these into '
               '`corpus/lessons/round-50.md`)\n')
rows_md.append('```markdown')
rows_md.append('| row | source | accessed | located quote (≤25 words) | decision |')
rows_md.append('|---|---|---|---|---|')
for g in GATE_ROWS:
    rows_md.append('| ' + ' | '.join(g) + ' |')
rows_md.append('```\n')
rows_md.append(
    'The attempt-1 Gate rows for these four sources (the `## Honest stop` section of '
    '`corpus/lessons/round-50.md`) said "not registered (honest stop)". This attempt registers '
    'them because the C1 entry lands in the same round and cites all four; the attempt-1 rows '
    'stay in the lesson as the record of the earlier stop, and the Gate above records the '
    'attempt-2 re-open (2026-10-29, same digests).\n')
rows_md.append('## Landing constraints the L1 must honour\n')
rows_md.append(
    '1. **The entry file and these four rows must land in the same commit.** The census '
    '`E11` check resolves every `mined` row\'s `used-by` path on disk. Measured on the scratch '
    'registry copy: with the entry path present, `sources-census.sh validate --file <copy>` '
    'exits **0**; with it absent, the same command exits **1** with exactly four `E11` lines '
    '(one per new row) and no other finding. The entry `corpus/knowledge/'
    '2026-10-28-r50-avm-le-squashfs-core.md` does not exist in the lane at the base revision, '
    'so a rows-only landing would make the registry red.\n')
rows_md.append(
    '2. **The counter\'s `sourced` binding needs these rows, not just the entry.** '
    '`tools/round-50/c1-counter.py:2468-2476` reads the registry at the measured revision and '
    'requires, for the binding to be true, a row whose id is among the `S###` tokens the '
    'entry\'s `source:` lines cite, whose `opened` is 2026-10-28 or 2026-10-29 '
    '(`OPENED_DATES`, `c1-counter.py:393`), and whose `used-by` names the entry path or its '
    'stem. All four rows satisfy the last two conditions today (checked: `opened=2026-10-28`, '
    '`used_by_ok=True` for each). The first condition is the entry draft\'s to satisfy — the '
    'entry must cite S243, S244, S245 and S249 in its `source:` lines, or the binding stays '
    'red for a reason no registry row can fix.\n')
rows_md.append(
    '3. **`W04` is expected and is the only new census finding.** S245 carries the same URL as '
    'S108 and S112 with a different scope, so the census emits '
    '`file\\tW04\\tS245 duplicate url raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/'
    'unblob/handlers/filesystem/squashfs.py across scopes`. The W04 count goes from 18 to 19; '
    'no E-code appears, and the baseline registry (the same file without these four rows) also '
    'validates at exit 0. S245\'s scope deliberately excludes the BE branch that S108/S112 '
    'cover, which is what keeps this a warning and not the `E04` duplicate-within-scope error.\n')
rows_md.append(
    '4. **Ids.** S243, S244, S245 and S249 are free in the registry (it ends at S248). '
    'S150-S242 stay skipped: earlier lessons cite them as refused staged rows that were never '
    'registered, so reusing one would repoint those citations (`w1/C1SrcFreetz.md` F6). The '
    'registry is append-only, so no existing row is edited by this block.\n')
rows_md.append(
    '5. **The L1\'s landing scripts must be brought onto this stem before they run.** '
    '`.ufo/waves/round-50/l1/land_sources.py:11-12` and `land_c1.py:17-18` still set '
    '`STEM = \'2026-10-28-r50-le-avm-members-core\'` (the attempt-1 stem), and '
    '`land_sources.py:130` filters the four rows away (`S = {k: S[k] for k in '
    '(\'S246\',\'S247\',\'S248\')}`). Run as they stand, they write the entry under the wrong path '
    'and land none of these four rows, leaving `entry_present`, `province_core_row`, '
    '`frontier_note`, `coverage_map_row` and `sourced` red. Bring both scripts onto '
    '`2026-10-28-r50-avm-le-squashfs-core` and drop the filter.\n')
rows_md.append(
    '6. **The `used-by` cells above are plain paths, no backticks** — the census `E11` rule '
    'resolves the path literally, so a backticked cell would not resolve. Apply them as printed.\n')
open(SEAT + '/rows.md', 'w', encoding='utf8').write('\n'.join(rows_md))
print('wrote', SEAT + '/rows.md')

# ---------------------------------------------------------------- scratch registry copy
MIRROR = S + '/mirror'
os.makedirs(MIRROR + '/corpus', exist_ok=True)
os.makedirs(MIRROR + '/tools/round-27', exist_ok=True)
reg = open(REG, encoding='utf8').read()
lines = reg.split('\n')


def row_index(rid):
    hits = [n for n, l in enumerate(lines) if re.match(r'^ {0,3}\|\s*' + rid + r'\s*\|', l)]
    assert len(hits) == 1, (rid, hits)
    return hits[0]


# S243, S244, S245 after S149; S249 after S248
i = row_index('S149')
lines[i + 1:i + 1] = [render(r) for r in ROWS[:3]]
j = row_index('S248')
lines[j + 1:j + 1] = [render(ROWS[3])]
reg2 = '\n'.join(lines)
assert reg2.count('\n| S243 |') == 1 and reg2.count('\n| S249 |') == 1

# search-log entry: last bullet of the Search log section, before "## Leads (unopened)"
slog_at = reg2.rindex('\n## Leads (unopened)')
reg2 = reg2[:slog_at] + '\n' + SEARCH_LOG + reg2[slog_at:]
open(MIRROR + '/corpus/SOURCES.md', 'w', encoding='utf8').write(reg2)

# mirror the used-by targets so E11 resolves: symlink each existing file, and add the
# not-yet-landed entry path as a mirror-only placeholder (the entry lands with the rows).
kn = LANE + '/corpus/knowledge'
os.makedirs(MIRROR + '/corpus/knowledge', exist_ok=True)
for n in sorted(os.listdir(kn)):
    dst = MIRROR + '/corpus/knowledge/' + n
    if not os.path.lexists(dst):
        os.symlink(kn + '/' + n, dst)
placeholder = MIRROR + '/corpus/knowledge/' + os.path.basename(ENTRY)
open(placeholder, 'w', encoding='utf8').write(
    '# MIRROR-ONLY PLACEHOLDER for the scratch census.\n'
    '# The real entry ' + ENTRY + ' does not exist in the lane yet;\n'
    '# the L1 lands it in the same commit as these rows. The lane tree is untouched.\n')
ls = LANE + '/corpus/lessons'
os.makedirs(MIRROR + '/corpus/lessons', exist_ok=True)
for n in sorted(os.listdir(ls)):
    dst = MIRROR + '/corpus/lessons/' + n
    if not os.path.lexists(dst):
        os.symlink(ls + '/' + n, dst)
for rel in ('corpus/QUALITY.md', 'SKILL.md', 'tools/round-27/xpin-attribute.mjs'):
    src = LANE + '/' + rel
    dst = MIRROR + '/' + rel
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.lexists(dst):
        os.symlink(src, dst)

# ---------------------------------------------------------------- census proof
proc = subprocess.run([CENSUS, 'validate', '--file', MIRROR + '/corpus/SOURCES.md'],
                      capture_output=True, text=True)
out = proc.stdout + proc.stderr
open(SEAT + '/census-validate.txt', 'w', encoding='utf8').write(out)
print('census exit:', proc.returncode)
for line in out.splitlines():
    if re.search(r'\t(S243|S244|S245|S249)\t', line) or 'W04' in line and 'squashfs.py' in line \
            or line.endswith('ok\t' + MIRROR + '/corpus/SOURCES.md'):
        print('CENSUS:', line)

# also: the baseline (rows removed) must be equally clean, so the block adds no new error
base = open(REG, encoding='utf8').read()
open(MIRROR + '/corpus/SOURCES.base.md', 'w', encoding='utf8').write(base)
proc2 = subprocess.run([CENSUS, 'validate', '--file', MIRROR + '/corpus/SOURCES.base.md'],
                       capture_output=True, text=True)
print('baseline census exit:', proc2.returncode)
print('W04 count with block:', out.count('W04'), 'baseline:', proc2.stdout.count('W04'))

# ---------------------------------------------------------------- counter binding check
c = subprocess.run([sys.executable, '-I', '-B', '-c',
                    'import re,sys\n'
                    'reg=open(sys.argv[1],encoding="utf8").read()\n'
                    'ENTRY=sys.argv[2]\n'
                    'for l in reg.splitlines():\n'
                    '    if not re.match(r"^ {0,3}\\|\\s*S\\d{3,}\\s*\\|", l): continue\n'
                    '    c=[x.strip() for x in l.strip().strip("|").split("|")]\n'
                    '    if len(c)!=11: continue\n'
                    '    if c[0] in ("S243","S244","S245","S249"):\n'
                    '        print(c[0], "opened="+c[8], "used_by_ok=", ENTRY in c[10])\n',
                    MIRROR + '/corpus/SOURCES.md', ENTRY], capture_output=True, text=True)
print(c.stdout.strip())
print('rows.md sha256:', sha(SEAT + '/rows.md'))
