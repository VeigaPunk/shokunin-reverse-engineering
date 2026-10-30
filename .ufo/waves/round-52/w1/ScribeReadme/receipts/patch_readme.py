#!/usr/bin/env python3
"""Offline verification driver for the R52-C1 corpus/README.md drafts.

Read-only against the lane tree; writes only into its own output directory.
Runs the three variants:
  A  append-only   (new coverage row, new Knowledge row, new frontier bullet, new trailing note)
  B  supersede + in-place removal of the LE-AVM-members clause from the historical lines

Every check prints PASS/FAIL and the script exits 0 only if all checks in every variant pass.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
BASE_REV = 'c525de54a53eb3c4fee28ede2721da4527cf8ece'
CLAIMS_REV = 'ab0eafedc41402b43b41a4362084119578dfe7ce'
STEM = '2026-10-30-r52-avm-le-squashfs-core'
ENTRY = 'corpus/knowledge/%s.md' % STEM
MARK = 'Round-52 frontier note'
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT.mkdir(parents=True, exist_ok=True)

fails = []


def check(name, cond, detail=''):
    print('%-72s %s %s' % (name, 'PASS' if cond else 'FAIL', detail))
    if not cond:
        fails.append(name)
    return cond


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(LANE), *args])


readme = git('show', '%s:corpus/README.md' % BASE_REV).decode()
readme_claims = git('show', '%s:corpus/README.md' % CLAIMS_REV).decode()
readme_head = git('show', 'HEAD:corpus/README.md').decode()

# ---- base measurements (recorded, not asserted by the drafts)
print('== base measurements ==')
print('README blob identical at base / claims draft / HEAD:',
      git('rev-parse', '%s:corpus/README.md' % BASE_REV).strip() ==
      git('rev-parse', '%s:corpus/README.md' % CLAIMS_REV).strip() ==
      git('rev-parse', 'HEAD:corpus/README.md').strip())
print('README sha256:', sha(readme.encode()))

# the frozen counter's helpers, verbatim from tools/round-50/c1-counter.py
def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def map_token(stem):
    return re.compile(r'`(?:corpus/)?(?:knowledge/)?%s(?:\.md)?`' % re.escape(stem))


def unique_section(text, heading):
    """Same idea as tools/round-50/c2-record.py:unique_section - one section only."""
    return text.count(heading + '\n') == 1


# ---- the drafts
COVERAGE_ROW = (
    '| SquashFS LE AVM members (round 52) | `%s` | **Core** — REA 6.5.0 `extract-firmware '
    '--max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`) resolves the '
    '`squashfs_v4_le` handler on the four chain-pinned genuine AVM-marker little-endian members '
    '(FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30) and publishes every '
    'regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path on all four, under '
    'the re-frozen device-accounting law (an unprivileged extraction creates no device nodes, fifos '
    'or sockets and emits no gap record for them, so a non-regular oracle entry carries no '
    'disposition at all) scored by `tools/round-52/c1-counter.py` (receipts '
    '`corpus/evidence/round-52/c1/`); the law\'s width is the four measured carriers — no fifo, '
    'socket or block-device row exists in any measured carrier — and the carrier bytes are fetched '
    'through the pinned vendor chain and never committed (AVM licence) (S243, S244, S245, S249, '
    'S250, S251, S252) |' % STEM
)

FALLBACK_ROW = (
    '| SquashFS LE AVM members (round 52) | `%s` | measured, not promoted — the re-frozen '
    'device-accounting law did not reach 4 of 4 carriers under the frozen counter (R52-C1 miss: '
    '`carriers_matched` < 4), so LE AVM members (`hsqs`) stay Frontier and the entry records the '
    'measurement (S243, S244, S245, S249, S250, S251, S252) |' % STEM
)

KNOWLEDGE_ROW = (
    '| `%s` | genuine AVM-marker LE SquashFS v4 (`hsqs`) through REA on the four pinned vendor '
    'members — Core (R52-C1 under the re-frozen device-accounting law: 4 of 4 carriers, every '
    'oracle regular file published at its exact path) | S243, S244, S245, S249, S250, S251, S252; '
    'receipts `corpus/evidence/round-52/c1/`; counter `tools/round-52/c1-counter.py` | 2026-10-30 |'
    % STEM
)

FRONTIER_BULLET = (
    '- sasquatch — 2026-10-30 round 52 (Round-52 frontier note): LE AVM members (`hsqs`) moved '
    'Frontier → Core (`%s`; REA 6.5.0 `extract-firmware --max-depth 1` publishes every regular '
    'file of the independent `unsquashfs` 4.7.5 oracle at its exact path on all four chain-pinned '
    'vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable 07.57/07.30 — and R52-C1 '
    're-froze the gap accounting from the per-carrier-class derivation, the device-accounting law: '
    'an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap record '
    'for them, so a non-regular oracle entry carries no disposition at all). This supersedes the '
    'LE-AVM clause of the round-40/41/44/49 lines above and of the round-50 frontier note below, '
    'and nothing else. Still frontier: LE AVM rootfs of ~13k files under REA\'s 120 s limit '
    '(observed, not claimed), AVM kernels, nested sub-images below depth 1, '
    '`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, '
    'v4 Broadcom.' % STEM
)

FRONTIER_NOTE = (
    'Round-52 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core (`%s`; REA '
    'published every oracle regular file on all four chain-pinned vendor carriers, and R52-C1 '
    're-froze the gap accounting from the per-carrier-class derivation — the device-accounting '
    'law: an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap '
    'record for them, so a non-regular oracle entry carries no disposition at all — so the counter '
    'matched 4 of 4 under the law-derived rule). This note supersedes the LE-AVM clause of the '
    'round-50 frontier note above (2 of 4 under the round-50 detail whitelist, which generalised '
    '`247:0` from the Cable-carrier class) and of the round-40/41/44/49 `## Frontier` lines, and '
    'nothing else. Still Frontier: LE AVM rootfs of ~13k files under REA\'s 120 s limit (observed, '
    'not claimed), AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, '
    '`squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom.' % STEM
)

# option B in-place edits: (old, new) - each old string is unique in the file.
# The pointer wording deliberately avoids the literal token "LE AVM members" and the
# LE_AVM_RE tokens (LE[ _-]AVM / AVM[ _-]LE), so a still-frontier enumeration that
# names the class cannot be mistaken for one that lists it.
INPLACE = [
    ('Still frontier: AVM-BE promotion, LE AVM members, nested `filesystem_core` images below depth 1, other vendor-mangled images.',
     'Still frontier: AVM-BE promotion, nested `filesystem_core` images below depth 1, other vendor-mangled images (the little-endian AVM members left this list on 2026-10-30 — see the Round-52 frontier note).'),
    ('Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.',
     'Still frontier: AVM kernel images, nested sub-images below depth 1, other vendor-mangled images (the little-endian AVM members left this list on 2026-10-30 — see the Round-52 frontier note).'),
    ('gzip v3, v4 Broadcom, LE AVM members, AVM kernels and nested sub-images below depth 1.',
     'gzip v3, v4 Broadcom, AVM kernels and nested sub-images below depth 1 (the little-endian AVM members left this list on 2026-10-30 — see the Round-52 frontier note).'),
    ('gzip v3, v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.',
     'gzip v3, v4 Broadcom, v2.1 images, AVM kernels and nested sub-images below depth 1 (the little-endian AVM members left this list on 2026-10-30 — see the Round-52 frontier note).'),
    ('Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA\'s 120 s limit,',
     'Still Frontier (as of 2026-10-29; the little-endian AVM members left this list on 2026-10-30 — see the Round-52 frontier note below): LE AVM rootfs of ~13k files under REA\'s 120 s limit,'),
    ('; LE AVM members and AVM kernels stay Frontier |',
     '; LE AVM members and AVM kernels stay Frontier (the LE-AVM clause was superseded on 2026-10-30 — see the Round-52 frontier note) |'),
    ('; LE AVM members (`hsqs`) stay Frontier, and the entry records the measurement (S243, S244, S245, S249) |',
     '; LE AVM members (`hsqs`) stayed Frontier at this round (superseded on 2026-10-30 — see the Round-52 frontier note), and the entry records the measurement (S243, S244, S245, S249) |'),
]


def build(variant):
    lines = readme.split('\n')
    # coverage map row: after the round-51 coverage row
    i = [n for n, l in enumerate(lines)
         if l.startswith('| SquashFS device and padding boundaries (round 51) |')]
    assert len(i) == 1, i
    lines.insert(i[0] + 1, COVERAGE_ROW)
    # Knowledge index row: after the round-51 Knowledge row
    j = [n for n, l in enumerate(lines)
         if l.startswith('| `2026-10-30-r51-avm-le-squashfs-core` |')]
    assert len(j) == 1, j
    lines.insert(j[0] + 1, KNOWLEDGE_ROW)
    # frontier bullet: after the round-49 bullet (last bullet of ## Frontier)
    k = [n for n, l in enumerate(lines)
         if l.startswith('- sasquatch — 2026-10-28 round 49:')]
    assert len(k) == 1, k
    lines.insert(k[0] + 1, FRONTIER_BULLET)
    # trailing note: end of file
    lines.insert(len(lines), '')
    lines.insert(len(lines), FRONTIER_NOTE)
    text = '\n'.join(lines)
    if variant == 'B':
        for old, new in INPLACE:
            assert text.count(old) == 1, ('not unique', old, text.count(old))
            text = text.replace(old, new)
    return text


def verify(variant, text):
    print('\n== variant %s ==' % variant)
    # 1. coverage row shape
    cm = section(text, '## Coverage map')
    check('%s: ## Coverage map section found' % variant, cm is not None)
    rows = [l for l in cm if l.lstrip().startswith('|')]
    bad = [l for l in rows if len(cells(l)) != 3]
    check('%s: every coverage-map row is 3 cells (%d rows, %d bad)' % (variant, len(rows), len(bad)),
          not bad, bad[:2])
    check('%s: coverage row cells == 3' % variant, len(cells(COVERAGE_ROW)) == 3,
          len(cells(COVERAGE_ROW)))
    check('%s: no pipe inside any coverage-row cell' % variant,
          not any('|' in c for c in cells(COVERAGE_ROW)))
    # 2. the counter's own coverage_map_row expression
    ok = any(STEM in l for l in cm if l.lstrip().startswith('|'))
    check('%s: coverage_map_row binding (c1-counter.py:2479-2482)' % variant, ok)
    # 3. map_token / B1 mapping
    ct = '\n'.join(cm)
    check('%s: map_token matches the row' % variant, bool(map_token(STEM).search(ct)))
    # 4. unique sections
    for h in ('## Coverage map', '## Knowledge', '## Frontier'):
        check('%s: unique section %s' % (variant, h), unique_section(text, h))
    # 5. Knowledge row is 4 cells
    kn = section(text, '## Knowledge')
    krow = [l for l in kn if l.startswith('| `%s` |' % STEM)]
    check('%s: exactly one Knowledge row for the stem' % variant, len(krow) == 1)
    check('%s: Knowledge row is 4 cells' % variant, len(cells(krow[0])) == 4, len(cells(krow[0])))
    # 6. frontier-note binding shape: mark + stem + LE-AVM token (stem removed)
    LE_AVM_RE = re.compile(r'\bLE[ _-]AVM\b|\bAVM[ _-]LE\b', re.IGNORECASE)
    hits = [l for l in text.splitlines()
            if MARK in l and STEM in l and LE_AVM_RE.search(l.replace(STEM, ''))]
    check('%s: frontier-note shape (mark + stem + LE-AVM token) on %d line(s)' % (variant, len(hits)),
          len(hits) >= 1)
    check('%s: neither new frontier line carries a pipe' % variant,
          '|' not in FRONTIER_BULLET and '|' not in FRONTIER_NOTE)
    # 7. the new bullet is the last bullet of ## Frontier and drops the clause
    fr = section(text, '## Frontier')
    bullets = [l for l in fr if l.startswith('- ')]
    check('%s: new bullet is the last ## Frontier bullet' % variant,
          bullets[-1] == FRONTIER_BULLET)
    check('%s: new bullet drops the LE-AVM-members clause' % variant,
          'LE AVM members (`hsqs`)' not in bullets[-1].split('Still frontier:')[-1])
    check('%s: new bullet keeps the ~13k-file rootfs clause' % variant,
          '~13k files' in bullets[-1])
    check('%s: new bullet keeps AVM kernels / nested sub-images' % variant,
          'AVM kernels' in bullets[-1] and 'nested sub-images below depth 1' in bullets[-1])
    # 8. the trailing note is the last non-blank line
    last = max(i for i, l in enumerate(text.splitlines(), 1) if l.strip())
    check('%s: trailing note is the last non-blank line' % variant,
          text.splitlines()[last - 1] == FRONTIER_NOTE)
    # 9. option B: no still-frontier ENUMERATION lists LE AVM members any more
    if variant == 'B':
        still = [l for l in fr if re.search(r'Still frontier[^.]*LE AVM members', l)]
        check('%s: no ## Frontier enumeration lists LE AVM members as still-frontier' % variant,
              not still, still[:1])
        tail = [l for l in text.splitlines()
                if re.search(r'Still Frontier[^.]*LE AVM members', l)]
        check('%s: no trailing note enumeration lists LE AVM members as still-frontier' % variant,
              not tail, tail[:1])
        check('%s: the ~13k-file clause survives the in-place edits (base 1 + 2 new lines)'
              % variant,
              text.count('~13k files') == readme.count('~13k files') + 2,
              (readme.count('~13k files'), text.count('~13k files')))
        # residual: dated descriptive sentences that still name the class (history)
        resid = [l for l in text.splitlines()
                 if 'LE AVM members' in l and 'left this list' not in l
                 and 'moved Frontier' not in l]
        print('   [option B] residual dated sentences naming the class (history, not an '
              'enumeration): %d' % len(resid))
        for l in resid:
            print('     -', l[:150])
    else:
        still = [l for l in fr if re.search(r'Still frontier[^.]*LE AVM members', l)]
        print('   [option A] historical still-frontier enumerations naming LE AVM members: %d '
              '(expected; option B removes them)' % len(still))
        for l in still:
            print('     -', l[:150])
    # 10. the patch touches nothing else: write the patched copy and a unified diff
    patched = OUT / ('README.patched.%s.md' % variant)
    patched.write_text(text)
    base_copy = OUT / ('README.base.%s.md' % variant)
    base_copy.write_text(readme)
    diff = subprocess.run(
        ['diff', '-u', '--label', 'corpus/README.md (base %s)' % BASE_REV[:8],
         '--label', 'corpus/README.md (patched %s)' % variant,
         str(base_copy), str(patched)], capture_output=True)
    (OUT / ('README.%s.patch' % variant)).write_bytes(diff.stdout)
    base_copy.unlink()
    print('   patch %s: %d diff lines, patched sha256 %s'
          % (variant, len(diff.stdout.decode().splitlines()), sha(text.encode())))
    return text


for variant in ('A', 'B'):
    text = build(variant)
    verify(variant, text)

# ---- command A on the patched clone (simulated): files 141 + the new entry
print('\n== command A simulation on the patched tree ==')
base_files = subprocess.check_output(
    ['git', '-C', str(LANE), 'ls-tree', '-r', '--name-only', BASE_REV, '--', 'corpus/knowledge'],
    text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in base_files if p.endswith('.md')}
check('base knowledge .md files == 141', len(files) == 141, len(files))
for variant in ('A', 'B'):
    text = (OUT / ('README.patched.%s.md' % variant)).read_text()
    cm = section(text, '## Coverage map')
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', '\n'.join(cm)))
    landed = files | {STEM}
    check('%s: command A mapped == knowledge_files == 142' % variant,
          len(landed & mapped) == 142 and len(landed) == 142,
          (len(landed & mapped), len(landed)))
    check('%s: command A missing == []' % variant, not (landed - mapped), landed - mapped)
    check('%s: command A dangling == []' % variant, not (mapped - landed), mapped - landed)
    check('%s: coverage_score == 10.0 at 142/142' % variant,
          round(10 * len(landed & mapped) / len(landed), 2) == 10.0)
    # the entry stem must be a real token match, not a prefix of another stem
    check('%s: the new stem is in the mapped set' % variant, STEM in mapped)
    check('%s: the r51 stem is still mapped (no regression)' % variant,
          '2026-10-30-r51-avm-le-squashfs-core' in mapped)

print('\n== fallbacks / negative controls ==')
# the fallback row must also be 3 cells and must NOT assert Core
check('fallback row is 3 cells', len(cells(FALLBACK_ROW)) == 3)
check('fallback row says measured, not promoted', 'measured, not promoted' in FALLBACK_ROW)
check('fallback row keeps LE AVM members Frontier', 'stay Frontier' in FALLBACK_ROW)
check('core row asserts Core', '**Core**' in COVERAGE_ROW)
# S252 does not exist yet at the base revision - a false citation if landed alone
sources = git('show', '%s:corpus/SOURCES.md' % BASE_REV).decode()
ids = [m.group(1) for m in re.finditer(r'^\| (S\d+)', sources, re.M)]
print('SOURCES rows at base: %d, highest id: %s, S252 present: %s'
      % (len(ids), max(ids, key=lambda s: int(s[1:])), 'S252' in ids))
check('S252 is NOT yet in the registry (the row must not cite it before it lands)',
      'S252' not in ids)

print('\nfailures: %d' % len(fails))
for f in fails:
    print('  FAIL', f)
print('utc: %s' % time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
sys.exit(1 if fails else 0)
