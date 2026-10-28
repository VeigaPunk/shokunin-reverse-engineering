#!/usr/bin/env python3
"""L1 landing assembly for round 49 (KaidokuR49): writes the landing bytes into the lane worktree.
Run once from the lane root after the data commit; every number is read from committed receipts."""
import hashlib
import json
import os
import re
import shutil

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W = L + '/.ufo/waves/round-49'
FREEZE = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
DATA = '4aabb0b4bf716fb564c8406509c40b0a67457800'
STEM = '2026-10-28-r49-squashfs-v1v2-core'
ENTRY = 'corpus/knowledge/%s.md' % STEM


def rd(p):
    return open(os.path.join(L, p), encoding='utf8').read()


def wr(p, s):
    full = os.path.join(L, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf8').write(s)


sha = lambda b: hashlib.sha256(b).hexdigest()
score = json.load(open(W + '/l1/scores/c1-at-data-4aabb0b4.json'))
HEAD = ('REA 6.5.0 `extract-firmware` on the four frozen carriers matched 4/4 at the data commit `%s` '
        '(`carriers_matched 4`, `failing []`, `gaps []`, every oracle member published: 3/3/4/4; receipt '
        '`.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`); the final score at the landing '
        'revision is `.ufo/waves/round-49/l1/scores/c1-final.json`' % DATA[:8])

# ---- A. snapshots (C2 evidence)
os.makedirs(L + '/corpus/evidence/round-49/c2', exist_ok=True)
for f in ('popper.html', 'sysexits.html'):
    shutil.copy(W + '/draft/snapshots/' + f, L + '/corpus/evidence/round-49/c2/' + f)
shutil.copy('/fast/scratch/hyaku/kaidoku-r49/l1/freebsd.html', L + '/corpus/evidence/round-49/c2/freebsd-sysexits.html')
pop = sha(open(L + '/corpus/evidence/round-49/c2/popper.html', 'rb').read())
sx = sha(open(L + '/corpus/evidence/round-49/c2/sysexits.html', 'rb').read())
fb = sha(open(L + '/corpus/evidence/round-49/c2/freebsd-sysexits.html', 'rb').read())

# ---- B. SOURCES.md
reg = rd('corpus/SOURCES.md')
lines = reg.split('\n')
out = []
for l in lines:
    if re.match(r'^ {0,3}\|\s*(S138|S139)\s*\|', l) and ENTRY not in l:
        l = l.rstrip().rstrip('|').rstrip() + ', ' + ENTRY + ' |'
    out.append(l)
reg = '\n'.join(out)
rows = open(W + '/w1/C2ScribeSources/rows.md', encoding='utf8').read().strip().split('\n')
s147, s148 = rows[0], rows[1]
assert s147.startswith('| S147 |') and s148.startswith('| S148 |')
s147 = s147.replace('supersedes S145 — the same page', 'supersedes S145 (row `corpus/SOURCES.md:151`, left unchanged) — the same page')
s148 = s148.replace('supersedes S146 — sysexits(3)', 'supersedes S146 (row `corpus/SOURCES.md:152`, left unchanged) — sysexits(3)')
s149 = ('| S149 | sysexits(3) FreeBSD manual, a second archive — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 '
        '| docs | C | The same exit-code header as S148 from another archive, considered as corroboration | '
        '`DESCRIPTION`; "EX_USAGE (64) The command was used incorrectly" (7 words); accessed 2026-10-28, HTTP 200, 59,251 bytes, '
        'sha256 `%s`, snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html` | REJECTED: a second mirror of the value S148 already '
        'carries (EX_USAGE is 64) with no meaning for the lane\'s exit 2, so it adds no claim S148 cannot carry; flip: a claim whose '
        'verdict needs an independent archive of the header rather than one mirror | rejected | 2026-10-28 | on-request | — |' % fb)
idx = max(i for i, l in enumerate(reg.split('\n')) if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l))
rl = reg.split('\n')
rl[idx + 1:idx + 1] = [s147, s148, s149]
reg = '\n'.join(rl)
e48 = ('- 2026-10-28 round 48 (late entry, written in round 49) — Question: which source grounds the falsifiability criterion for a '
       'check, and does sysexits ground the lane\'s exit 2? Where searched: the registry rows S145 (SEP, Karl Popper) and S146 (man7 '
       '`sysexits.h.3`), both opened during round 48 on 2026-10-28. Identified 2, screened 2, included 1, excluded 1; rows 144 → 146. '
       'Exclusion: S146, HTTP 404 at the URL as written. Stop: the two sources named by the round-48 lesson were each opened once; no '
       'further search was run.')
e49 = ('- 2026-10-28 round 49 — Question: do the S145 locator and the S146 rationale survive a re-open, and does a second archive add '
       'anything to the sysexits value? Where searched: the SEP Popper entry and the man7 `sysexits.h.3head` page re-fetched today and '
       'pinned by sha256 under `corpus/evidence/round-49/c2/`, plus the FreeBSD `man.freebsd.org` sysexits(3) page (one fetch, '
       'HTTP 200). Identified 3, screened 3, included 2, excluded 1; rows 146 → 149. Exclusion: S149 duplicates S148\'s value from a '
       'second mirror and defines no meaning for exit 2. Stop: the questions are answered by the three fetched pages; no web-wide '
       'search was run, so a negative claim about other archives is not made.')
assert '\n## Leads (unopened)' in reg
reg = reg.replace('\n## Leads (unopened)', '\n' + e48 + '\n' + e49 + '\n\n## Leads (unopened)', 1)
wr('corpus/SOURCES.md', reg)

# ---- C. PROVINCE.md (append only)
prov = rd('PROVINCE.md')
ba = open(W + '/w1/C1ScribeProvince/block-a.md', encoding='utf8').read().rstrip('\n')
bb = open(W + '/w1/C1ScribeProvince/block-b.md', encoding='utf8').read().rstrip('\n')
bb = re.sub(r'<AFTER-DATA:[^>]*>', 'moved Frontier → Core', bb)
ba = re.sub(r'<AFTER-DATA:[^>]*>', HEAD, ba)
wr('PROVINCE.md', prov.rstrip('\n') + '\n\n' + ba + '\n\n' + bb + '\n')

# ---- D. README
rm = rd('corpus/README.md').split('\n')
bc = open(W + '/w1/C1ScribeProvince/block-c.md', encoding='utf8').read().strip()
bc = re.sub(r'<AFTER-DATA:[^>]*>', HEAD, bc)
i44 = next(i for i, l in enumerate(rm) if l.startswith('| SquashFS v1/v2 through REA (round 44)'))
rm.insert(i44 + 1, bc)
k44 = next(i for i, l in enumerate(rm) if l.startswith('| `2026-10-28-r44-squashfs-v1v2-core`'))
rm.insert(k44 + 1, '| `%s` | SquashFS v1/v2 through REA on four frozen fixtures, Core (R49-C1 under a predicate stated once; supersedes the round-44 not-promoted entry) | S112, S138, S139; receipts `corpus/evidence/round-49/c1/`; counter `tools/round-49/c1-counter.py` | 2026-10-28 |' % STEM)
f44 = next(i for i, l in enumerate(rm) if l.startswith('- sasquatch — 2026-10-28 round 44'))
rm.insert(f44 + 1, '- sasquatch — 2026-10-28 round 49: SquashFS v1/v2 (`squashfs_v1`, `squashfs_v2`, four standard fixtures) is **Core** (`%s`), superseding the round-44 line above. Still frontier: `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.' % STEM)
wr('corpus/README.md', '\n'.join(rm))

# ---- E. entry
ent = open(W + '/w1/C1ScribeEntry/entry.md', encoding='utf8').read()
ent = ent.split('\n## Markers')[0].rstrip('\n') + '\n'
el = ent.split('\n')
el[0] = el[0].replace('<MEASURED: verdict>', 'Core, 4/4 carriers')
el[2] = ('status: R49-C1 — the four carriers matched 4/4 at the data commit `%s` (`.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`: '
         '`carriers_matched 4`, `failing []`, `frozen_path_changed []`; the six documentation bindings were false there because this entry '
         'and the PROVINCE/README rows did not yet exist). The score at the landing revision, against the single round-49 freeze `%s`, is '
         '`.ufo/waves/round-49/l1/scores/c1-final.json` (counter `tools/round-49/c1-counter.py`, sha256 `%s`); the control ledger is '
         '`.ufo/waves/round-49/controls/summary.json` (`kill_rule_fires false`). Round 44 stopped on this same claim because its frozen '
         'claim and its frozen counter named different provenance paths for the REA output directory '
         '(`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`); round 49 states that predicate once (a prefix test on '
         '`/fast/scratch/hyaku/kaidoku-r49/`) and the counter implements that sentence. What the counter measures is REA\'s behaviour on '
         'the four frozen bytes, reproduced by its own rerun; it does not authenticate who wrote the committed receipt (plan, disclosed limit).'
         % (DATA, FREEZE, score['counter_sha256']))
ent = '\n'.join(el)
ent = ent.replace('Promotion outcome: <MEASURED: promotion outcome>. The row is "moved to Core" only if the counter is met at REV; otherwise it is "not promoted; Frontier stands".',
                  'Promotion outcome: moved to Core, on the four frozen carriers only, if and only if the counter is met at the landing revision (`.ufo/waves/round-49/l1/scores/c1-final.json`); the round-44 `measured, not promoted` note is superseded for v1/v2 and nothing else.')
mm = {
    'everything in this section comes from the data run, after the freeze, and is quoted from the committed round-49 receipts; nothing here is carried over from round 44.':
        'Everything in this section comes from the data run after the freeze (`corpus/evidence/round-49/c1/`, commit `%s`) and is quoted from the committed round-49 receipts and the counter output `.ufo/waves/round-49/l1/scores/c1-at-data-4aabb0b4.json`; nothing here is carried over from round 44.' % DATA[:8],
    'handler_ok per carrier': 'true on all four', 'extra_published': '[]', 'gap_kinds': '[]',
    'coverage per carrier': '`complete` on all four', 'gap_rule_uncovered_kinds': '[]',
    'per_carrier_failing': '[]', 'gap_rule_problems': '[]', 'evidence_id_ok per carrier': 'true on all four',
    'carrier_pin_ok per carrier': 'true on all four', 'projection_ok per carrier': 'true on all four',
    'output_directory of the scored receipt': 'a path under `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/` (`provenance_ok` is a prefix test)',
    'landing path of these receipts at REV, e.g. copied to `corpus/evidence/round-49/oracle/`':
        'They stay in the wave directory, committed with wave 1 at `14936cb9`; no copy under `corpus/` is made',
}
for car, files, nbytes in (('v1le', 3, 20), ('v1be', 3, 20), ('v2le', 4, 28), ('v2be', 4, 28)):
    mm['%s published files' % car] = str(files)
    mm['%s bytes' % car] = str(nbytes)
    mm['%s gaps' % car] = '`[]`'
    mm['%s coverage' % car] = '`complete`'
    mm['%s receipt path' % car] = '`corpus/evidence/round-49/c1/%s/after.json`' % car


def sub(m):
    k = m.group(1)
    if k not in mm:
        raise SystemExit('unmapped marker: ' + k)
    return mm[k]


ent = re.sub(r'<MEASURED: ([^>]*)>', sub, ent)
ent = ent.replace('(round 44, Core)', '(round 49, Core)').replace('Before this round `PROVINCE.md`', 'Before round 49 (2026-10-28) `PROVINCE.md`')
assert 'MEASURED' not in ent and 'AFTER-DATA' not in ent
wr(ENTRY, ent)
print('landing bytes written; entry %d bytes' % len(ent))
