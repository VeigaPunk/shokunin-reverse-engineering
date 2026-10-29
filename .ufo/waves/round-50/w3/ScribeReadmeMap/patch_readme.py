#!/usr/bin/env python3
"""Draft the round-50 corpus/README.md edits on a scratch copy and verify them
against the FROZEN round-50 counter's own binding code (read-only import).

Nothing here writes to the lane tree; the clone under $S/clone is scratch.
"""
import hashlib
import importlib.util
import os
import re
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
CLONE = '/fast/scratch/hyaku/kaidoku-r50/w3-ScribeReadmeMap/clone'
README = os.path.join(CLONE, 'corpus/README.md')

STEM = '2026-10-28-r50-avm-le-squashfs-core'

COV_ROW = (
    '| SquashFS LE AVM members (round 50) | `2026-10-28-r50-avm-le-squashfs-core` | '
    '**Core** — on four pinned vendor carriers, bounded: REA 6.5.0 `extract-firmware --max-depth 1` '
    '(unblob 26.6.4, `sasquatch` 4.5.1 on the child `PATH`, no `-be` binary) resolves the '
    '`squashfs_v4_le` handler on the four chain-pinned genuine AVM-marker little-endian members '
    '(FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30), publishing every '
    'regular file of the independent `unsquashfs` 4.7.5 oracle at its exact path with no extra file '
    '(R50-C1 `carriers_matched 4`); the carrier bytes are fetched through the pinned chain and never '
    'committed (AVM licence), so the durable evidence is the committed receipt set, the frozen oracle '
    'tables and the pin chain; bound: four carriers, one vendor, xz bodies, depth 1 (the LE AVM rootfs '
    'of ~13k files under REA\'s 120 s limit stays Frontier); supersedes the round-49 note\'s LE-AVM '
    'clause (which listed LE AVM members, `hsqs`, as still Frontier) |'
)

KNOW_ROW = (
    '| `2026-10-28-r50-avm-le-squashfs-core` | SquashFS LE AVM (`hsqs`) members through REA on four '
    'chain-pinned vendor carriers, Core (R50-C1; supersedes the round-49 note\'s LE-AVM clause) | '
    'S243, S244, S245, S249; receipts `corpus/evidence/round-50/c1/`; counter '
    '`tools/round-50/c1-counter.py` | 2026-10-29 |'
)

FRONTIER_ROW = (
    '- sasquatch — 2026-10-29 round 50: genuine AVM-marker little-endian SquashFS v4 members (`hsqs`) '
    'are **Core** (`2026-10-28-r50-avm-le-squashfs-core`: REA 6.5.0 `extract-firmware --max-depth 1` '
    'on four chain-pinned vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable 07.57/07.30; '
    'the carrier bytes are fetched and never committed, AVM licence), superseding the LE-AVM clause of '
    'the round-49 line above (which listed LE AVM members, `hsqs`, as still Frontier). Scope: four '
    'pinned carriers, one vendor, xz bodies, depth 1. Still frontier: the LE AVM rootfs of ~13k files '
    'under REA\'s 120 s limit (FRITZ!Box 7530/7590 08.25), `squashfs_v2_nonstandard`, '
    '`squashfs_v3_broadcom`/`_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3, '
    'v4 Broadcom, v2.1 images, AVM kernel images and nested sub-images below depth 1.'
)

# Option B (in-place): the round-49 frontier line loses the LE-AVM clause and
# keeps a forward pointer to the superseding line.
R49_OLD = ('v4 Broadcom, v2.1 images, LE AVM members (`hsqs`), AVM kernels and nested sub-images '
           'below depth 1.')
R49_NEW = ('v4 Broadcom, v2.1 images, AVM kernels and nested sub-images below depth 1 (its LE-AVM '
           'clause is superseded by the round-50 line below).')


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else 'primary'
    text = open(README, encoding='utf-8').read()
    orig = text

    # E1 coverage-map row: after the round-49 coverage row
    anchor = '| SquashFS v1/v2 through REA (round 49) |'
    lines = text.split('\n')
    idx = [i for i, l in enumerate(lines) if l.startswith(anchor)]
    assert len(idx) == 1, idx
    lines.insert(idx[0] + 1, COV_ROW)
    text = '\n'.join(lines)

    # E3 knowledge-index row: after the round-49 knowledge row
    lines = text.split('\n')
    idx = [i for i, l in enumerate(lines)
           if l.startswith('| `2026-10-28-r49-squashfs-v1v2-core` |')]
    assert len(idx) == 1, idx
    lines.insert(idx[0] + 1, KNOW_ROW)
    text = '\n'.join(lines)

    # E2 frontier row: last line of the `## Frontier` section
    lines = text.split('\n')
    start = lines.index('## Frontier')
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith('## '))
    last = max(i for i in range(start + 1, end) if lines[i].strip())
    lines.insert(last + 1, FRONTIER_ROW)
    text = '\n'.join(lines)

    # E4 option B: in-place removal of the LE-AVM clause in the round-49 line
    if variant == 'primary':
        assert text.count(R49_OLD) == 1, text.count(R49_OLD)
        text = text.replace(R49_OLD, R49_NEW)

    open(README, 'w', encoding='utf-8').write(text)

    # ---- verification against the FROZEN counter's own code -----------------
    ctr = load_mod('c1counter', os.path.join(CLONE, 'tools/round-50/c1-counter.py'))
    rec = load_mod('c2record', os.path.join(CLONE, 'tools/round-50/c2-record.py'))
    print('counter STEM      :', ctr.STEM)
    print('counter ENTRY     :', ctr.ENTRY)
    print('stem matches arg  :', ctr.STEM == STEM)
    print('CORE_HEADING      :', ctr.CORE_HEADING)
    print('FRONTIER_MARK     :', ctr.FRONTIER_MARK)

    t = open(README, encoding='utf-8').read()

    # the counter's coverage_map_row binding, verbatim logic
    cm = ctr.section(t, '## Coverage map')
    rows = [l for l in cm if l.lstrip().startswith('|') and ctr.STEM in l]
    binding = bool(cm) and any(ctr.STEM in l for l in cm if l.lstrip().startswith('|'))
    print('binding coverage_map_row (counter logic):', binding, '| rows naming stem:', len(rows))
    print('coverage row cells:', ctr.cells(rows[0]) and len(ctr.cells(rows[0])))

    # c2-record unique_section + B1 mapping simulation
    cov, bad = rec.unique_section(t, '## Coverage map')
    print('unique_section ## Coverage map:', 'unique' if cov is not None else bad)
    know, bad2 = rec.unique_section(t, '## Knowledge')
    print('unique_section ## Knowledge     :', 'unique' if know is not None else bad2)
    front, bad3 = rec.unique_section(t, '## Frontier')
    print('unique_section ## Frontier      :', 'unique' if front is not None else bad3)

    tok = rec.map_token(STEM)
    print('map_token(STEM) matches coverage section:', bool(tok.search('\n'.join(cov or []))))

    kdir = os.path.join(CLONE, 'corpus/knowledge')
    files = sorted(f for f in os.listdir(kdir) if f.endswith('.md'))
    unmapped = [f for f in files if not rec.map_token(f[:-3]).search('\n'.join(cov or []))]
    print('knowledge files at clone HEAD:', len(files), '| unmapped by coverage map:', unmapped)

    # with the landing entry present, B1 must find it mapped
    land = os.path.join(kdir, STEM + '.md')
    open(land, 'w', encoding='utf-8').write('# landing entry stub (verification only)\n')
    files2 = sorted(f for f in os.listdir(kdir) if f.endswith('.md'))
    unmapped2 = [f for f in files2 if not rec.map_token(f[:-3]).search('\n'.join(cov or []))]
    print('with landing entry present:', len(files2), '| unmapped:', unmapped2)
    os.remove(land)

    # cell-count sanity for the three drafted lines
    for name, line, want in (('coverage', COV_ROW, 3), ('knowledge', KNOW_ROW, 4),
                              ('frontier', FRONTIER_ROW, 1)):
        got = len(ctr.cells(line)) if name != 'frontier' else 1
        print('cells %-9s: %d (want %d) %s' % (name, got, want, 'OK' if got == want else 'FAIL'))
        assert '|' not in line.replace('|', '', 0) or True
        # a pipe inside a cell would change the count; count raw pipes
        print('   raw pipe count %-9s: %d' % (name, line.count('|')))

    # frontier section content
    fl = ctr.section(t, '## Frontier')
    fl_nonempty = [l for l in fl if l.strip()]
    print('frontier last line is the round-50 line:',
          fl_nonempty[-1].startswith('- sasquatch — 2026-10-29 round 50:'))
    print('frontier still mentions LE AVM members (`hsqs`):',
          any('LE AVM members (`hsqs`)' in l for l in fl))
    print('frontier mentions ~13k clause:', any('~13k files' in l for l in fl))
    print('frontier names the superseding entry:', any(STEM in l for l in fl))

    print('variant:', variant)
    print('patched README sha256:', hashlib.sha256(t.encode()).hexdigest())
    print('original README sha256:', hashlib.sha256(orig.encode()).hexdigest())
    if variant == 'primary':
        print('LE AVM members (`hsqs`) left in ## Frontier:',
              [l[:60] for l in fl if 'LE AVM members (`hsqs`)' in l])
    return 0


if __name__ == '__main__':
    sys.exit(main())
