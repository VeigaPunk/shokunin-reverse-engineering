#!/usr/bin/env python3
"""round-51 seat ScribeSources — build the two SOURCES rows and prove the block.

Builds a scratch mirror of the lane's corpus/SOURCES.md with the two new rows
appended (ascending id order) plus the search-log bullet, then runs the fleet
census against the mirror. Also asserts the registry grammar: 11 cells, no
'|' inside any cell, id uniqueness, kind/tier/status enums, cell lengths.

Exit 0 = the block is clean and the census validates at exit 0.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
_HERE = os.path.dirname(os.path.abspath(__file__))
S = (_HERE if os.path.isdir(os.path.join(_HERE, 'body')) else
     '/fast/scratch/hyaku/kaidoku-r51/w1-ScribeSources')
CENSUS = '/home/vgpnk/Projects/shokunin/scripts/sources-census.sh'
MIRROR = os.path.join(S, 'mirror')

ENTRY = 'corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md'
ENTRY_STEM = '2026-10-30-r51-avm-le-squashfs-core'

# ---------------------------------------------------------------- the rows --
S250 = (
    'S250',
    'squashfs-tools 4.7.5 `unsquashfs.c` device-node creation path -- '
    'https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c',
    'code',
    'A',
    'the upstream extractor\'s char/block device-node creation path and its privilege '
    'refusal: the node is created only under `root_process`, and an unprivileged run '
    'reports "not superuser" instead of creating it, while fifo and socket nodes are '
    'attempted unconditionally and only report ERROR on failure; not REA\'s gap schema, '
    'not the sasquatch fork\'s tree, not any carrier\'s census',
    'tag `4.7.5` = commit `708c59ae80853b0845017c33b42e56061cc546cd`; sha256 '
    '`6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341` (116,844 B); '
    '`:1296` the `mknod` call; `:1313`-`:1315` the "not superuser" refusal; `:1328`/'
    '`:1349` the fifo and socket `mknod` calls; `:4459` `root_process = geteuid() == 0;`; '
    '`unsquashfs_error.h` sha256 `6433564edbd528d12d4db9ae20a45594fdc8065884c3dcf7774858'
    'e30e44bc4a` `:44`-`:50` `EXIT_UNSQUASH_STRICT` degrades to a non-fatal `ERROR` unless '
    '`-strict-errors`; the sasquatch fork that actually ran has the same structure at '
    '`:1247`/`:1256`/`:1273`-`:1275`/`:1288`/`:1306` (sha256 '
    '`ece42b66f37ba67707c2c51b47b643c027232153705f59d238da79958a54cb40`)',
    'A device node in a SquashFS image is absent from an unprivileged extraction by '
    'construction, not by reader failure: the extractor creates it only as root and '
    'refuses by name otherwise, so a char-device oracle entry is expected to carry no '
    'published counterpart.',
    'queued',
    '2026-10-30',
    'on-release',
    ENTRY,
)

S251 = (
    'S251',
    'squashfs-tools `mksquashfs.c` and `mksquashfs_help.c` padding option -- '
    'https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c',
    'code',
    'A',
    'the producer-side option that suppresses 4K padding of the produced filesystem, its '
    'upstream spelling and the padding logic it gates; the upstream spelling is `-nopad` '
    'with no hyphen at every upstream tag checked, and the option belongs to the writer, '
    'not to the reader; not any carrier\'s bytes, not a reader\'s behaviour, not REA\'s '
    'publication',
    'tag `4.7.5` = commit `708c59ae80853b0845017c33b42e56061cc546cd`; `mksquashfs.c` '
    'sha256 `509241bb1aaa1a4fd144d3c7ddc96e628a9d34033573b04836672352fb4f17e2` (257,215 B) '
    '`:7113` the `-nopad` parse, `:596`/`:7491`/`:8946` the padding write it gates, '
    '`:5964` the superblock offset it chooses; `mksquashfs_help.c` sha256 '
    '`9136f6e6ac57859cb45df633128f68e615b412dc8b6abfa4da8374373f981ac2` `:467` the help '
    'line; the v3-era producer at tag `3.1` carries the same option name and help text '
    '(`mksquashfs.c` `:1914`, `:1973`, `:2248`)',
    'A SquashFS body named "no-pad" is the producer\'s `-nopad` option: the filesystem is '
    'left at its unaligned length instead of being padded to a 4K multiple, and in '
    'streaming mode the superblock is placed at the unaligned write position rather than '
    'the next 4K boundary.',
    'queued',
    '2026-10-30',
    'on-release',
    ENTRY + ', SKILL.md',
)

ROWS = [S250, S251]

SEARCH_LOG = (
    '- 2026-10-30 round 51 wave 1 (C1/C2 source opens) — Question: what upstream '
    'squashfs-tools source grounds the round-51 device-accounting law and the `-no-pad` '
    'padding claim? Where searched: the two named master raw files '
    '(`unsquashfs.c`, `mksquashfs.c`) re-fetched today, the same two files at the tagged '
    'release matching the host oracle (`4.7.5`), the same files at the current master '
    'HEAD commit, the companion `mksquashfs_help.c`/`mksquashfs_help.h`/`squashfs_fs.h`/'
    '`unsquashfs_error.h` at both refs, the upstream tags `3.1`/`4.4`/`4.5.1`/`4.6.1`/'
    '`4.7`/`4.7.4` `mksquashfs.c`, the sasquatch fork `mksquashfs.c` at tag '
    '`sasquatch-v4.5.1-6`, and `git ls-remote --tags` for the upstream tag list; every '
    'body was digested and every located quote re-checked against the served bytes '
    '(receipts under `.ufo/waves/round-51/w1/ScribeSources/`). Identified 2, screened 2, '
    'included 2 (S250, S251), excluded 0; the upstream spelling of the padding option is '
    '`-nopad` with no hyphen, so the lane\'s "no-pad" prose is not an upstream option '
    'name. Stop: both rows are located and anchored at a named upstream tag; no further '
    'source family was opened.'
)


def cell_safe(text):
    return '|' not in text


def render_row(row):
    return '| ' + ' | '.join(row) + ' |'


def main():
    # ---- grammar assertions ------------------------------------------------
    problems = []
    for row in ROWS:
        rid = row[0]
        if len(row) != 11:
            problems.append('%s: %d cells (must be 11)' % (rid, len(row)))
        if not re.match(r'^S[0-9]{3,}$', rid):
            problems.append('%s: bad id' % rid)
        for i, c in enumerate(row):
            if not cell_safe(c):
                problems.append('%s: cell %d contains a pipe' % (rid, i))
        if row[2] not in ('spec', 'docs', 'paper', 'code', 'tool', 'dataset', 'talk',
                          'book', 'community', 'own-work'):
            problems.append('%s: bad kind %r' % (rid, row[2]))
        if row[3] not in ('A', 'B', 'C'):
            problems.append('%s: bad tier %r' % (rid, row[3]))
        if row[7] not in ('queued', 'mined', 'rejected'):
            problems.append('%s: bad status %r' % (rid, row[7]))
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', row[8]):
            problems.append('%s: bad opened %r' % (rid, row[8]))
        if not (re.match(r'^\d+[d]$', row[9]) or re.match(r'^[A-Za-z][A-Za-z0-9 _-]*$', row[9])):
            problems.append('%s: bad recheck %r' % (rid, row[9]))
        if row[3] == 'A' and row[2] == 'community':
            problems.append('%s: community at tier A' % rid)
        lens = [len(c) for c in row]
        print('%-6s cells=%d max_cell=%d %s' % (rid, len(row), max(lens),
                                                'MAXCELL=%d' % max(lens)))
    if problems:
        for p in problems:
            print('PROBLEM %s' % p)
        return 1

    base = open(os.path.join(LANE, 'corpus/SOURCES.md'), encoding='utf-8').read()

    # ---- id uniqueness against the live registry ---------------------------
    for row in ROWS:
        n = len(re.findall(r'^\|\s*%s\s*\|' % row[0], base, re.M))
        print('id %s present in base registry: %d' % (row[0], n))
        if n:
            print('PROBLEM id %s already exists' % row[0])
            return 1

    # ---- build the mirror --------------------------------------------------
    if os.path.isdir(MIRROR):
        shutil.rmtree(MIRROR)
    os.makedirs(os.path.join(MIRROR, 'corpus'))
    shutil.copy(os.path.join(LANE, 'corpus/SOURCES.md'),
                os.path.join(MIRROR, 'corpus/SOURCES.md'))
    # copy the real corpus tree so E11 resolves the lane's used-by paths
    shutil.copytree(os.path.join(LANE, 'corpus'), os.path.join(MIRROR, 'corpus'),
                    symlinks=True, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('SOURCES.md'))
    # symlink the lane's top-level paths that rows use as used-by targets
    # (the census resolves used-by relative to the registry's grandparent dir)
    for name in ('SKILL.md', 'PROVINCE.md', 'SCORECARD.md', 'LOG.md', 'CORPUS.md',
                 'README.md', 'MINT.md', 'AGENTS.md'):
        src = os.path.join(LANE, name)
        if os.path.exists(src):
            os.symlink(src, os.path.join(MIRROR, name))
    for name in ('tools',):
        src = os.path.join(LANE, name)
        if os.path.exists(src):
            os.symlink(src, os.path.join(MIRROR, name))
    # mirror-only placeholder for the not-yet-landed entry
    with open(os.path.join(MIRROR, 'corpus/knowledge', os.path.basename(ENTRY)),
              'w', encoding='utf-8') as fh:
        fh.write('mirror-only placeholder\n')

    patched = base
    # insert the rows in ascending id order, right after the last existing row
    lines = patched.split('\n')
    last_row = max(i for i, l in enumerate(lines)
                    if re.match(r'^\|\s*S[0-9]{3,}\s*\|', l))
    new_lines = lines[:last_row + 1] + [render_row(r) for r in ROWS] + lines[last_row + 1:]
    # append the search-log bullet as the LAST bullet of the ## Search log section
    # (insert right after the last '- ' bullet inside that section, so the section's
    #  shape — blank line before the next '## ' heading — is unchanged)
    out = []
    in_log = False
    last_bullet = None
    for i, l in enumerate(new_lines):
        if re.match(r'^##\s+Search log', l):
            in_log = True
        elif re.match(r'^##\s+', l) and in_log:
            in_log = False
        if in_log and l.startswith('- '):
            last_bullet = i
    if last_bullet is None:
        print('PROBLEM could not find the ## Search log section')
        return 1
    new_lines = (new_lines[:last_bullet + 1] + [SEARCH_LOG]
                 + new_lines[last_bullet + 1:])
    patched = '\n'.join(new_lines)

    with open(os.path.join(MIRROR, 'corpus/SOURCES.md'), 'w', encoding='utf-8') as fh:
        fh.write(patched)
    print('mirror SOURCES.md written, sha256 %s'
          % hashlib.sha256(patched.encode()).hexdigest())

    # ---- census on the mirror ---------------------------------------------
    mf = os.path.join(MIRROR, 'corpus/SOURCES.md')
    p = subprocess.run([CENSUS, 'validate', '--file', mf],
                       capture_output=True, text=True)
    out = p.stdout
    print('census exit=%d' % p.returncode)
    findings = [l for l in out.split('\n')
                if re.search(r'\t[EW][0-9]{2}\t', l)]
    for l in findings:
        print('CENSUS %s' % l)
    w04 = [l for l in findings if '\tW04\t' in l]
    e = [l for l in findings if '\tE' in l]
    print('census: W04=%d E=%d exit=%d' % (len(w04), len(e), p.returncode))

    # ---- census WITHOUT the entry placeholder (the E11 negative control) ---
    ph = os.path.join(MIRROR, 'corpus/knowledge', os.path.basename(ENTRY))
    os.remove(ph)
    p2 = subprocess.run([CENSUS, 'validate', '--file', mf],
                        capture_output=True, text=True)
    e2 = [l for l in p2.stdout.split('\n') if '\tE' in l]
    print('census without the entry placeholder: exit=%d E-lines=%d'
          % (p2.returncode, len(e2)))
    for l in e2:
        print('E11 %s' % l)
    with open(ph, 'w', encoding='utf-8') as fh:
        fh.write('mirror-only placeholder\n')

    # ---- baseline census on the untouched lane registry --------------------
    p3 = subprocess.run([CENSUS, 'validate', '--lane', 'kaidoku']
                        if False else [CENSUS, 'validate', LANE],
                        capture_output=True, text=True)
    base_findings = [l for l in p3.stdout.split('\n') if re.search(r'\t[EW][0-9]{2}\t', l)]
    print('baseline lane census: exit=%d findings=%d W04=%d'
          % (p3.returncode, len(base_findings),
             len([l for l in base_findings if '\tW04\t' in l])))
    with open(os.path.join(_HERE, 'receipts/census-mirror.txt'), 'w', encoding='utf-8') as fh:
        fh.write(out)
        fh.write('\n--- without entry placeholder: exit=%d ---\n' % p2.returncode)
        fh.write(p2.stdout)
        fh.write('\n--- baseline lane: exit=%d ---\n' % p3.returncode)
        fh.write(p3.stdout)

    # ---- diff size ---------------------------------------------------------
    diff = subprocess.run(['diff', os.path.join(LANE, 'corpus/SOURCES.md'), mf],
                          capture_output=True, text=True)
    added = sum(1 for l in diff.stdout.split('\n') if l.startswith('>'))
    removed = sum(1 for l in diff.stdout.split('\n') if l.startswith('<'))
    print('diff vs base: added=%d removed=%d' % (added, removed))

    # ---- the `mined` variant (what QUALITY row 45 wants at landing) -------
    # rows with status `mined` must have their used-by path on disk, so S250's
    # used-by (the not-yet-landed entry) is the E11 risk. Measure it.
    mined_rows = [tuple(list(r[:7]) + ['mined'] + list(r[8:])) for r in ROWS]
    lines2 = patched.split('\n')
    out2 = []
    for l in lines2:
        for mr in mined_rows:
            if l.startswith('| %s |' % mr[0]):
                l = render_row(mr)
        out2.append(l)
    mined_path = os.path.join(MIRROR, 'corpus/SOURCES.mined.md')
    with open(mined_path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out2))
    p4 = subprocess.run([CENSUS, 'validate', '--file', mined_path],
                        capture_output=True, text=True)
    e4 = [l for l in p4.stdout.split('\n') if '\tE' in l]
    w4 = [l for l in p4.stdout.split('\n') if '\tW04\t' in l]
    print('mined-status variant: exit=%d E=%d W04=%d' % (p4.returncode, len(e4), len(w4)))
    for l in e4:
        print('MINED-E %s' % l)
    # and with the entry placeholder removed, the mined variant must go red on
    # S250 only (the row whose used-by is the not-yet-landed entry)
    ph2 = os.path.join(MIRROR, 'corpus/knowledge', os.path.basename(ENTRY))
    os.remove(ph2)
    p5 = subprocess.run([CENSUS, 'validate', '--file', mined_path],
                        capture_output=True, text=True)
    e5 = [l for l in p5.stdout.split('\n') if '\tE' in l]
    print('mined variant without the entry placeholder: exit=%d E=%d'
          % (p5.returncode, len(e5)))
    for l in e5:
        print('MINED-E11 %s' % l)
    with open(ph2, 'w', encoding='utf-8') as fh:
        fh.write('mirror-only placeholder\n')
    with open(os.path.join(_HERE, 'receipts/census-mined-variant.txt'), 'w',
              encoding='utf-8') as fh:
        fh.write('mined variant, entry placeholder present: exit=%d\n' % p4.returncode)
        fh.write(p4.stdout)
        fh.write('\n--- mined variant, entry placeholder REMOVED: exit=%d ---\n'
                 % p5.returncode)
        fh.write(p5.stdout)

    ok = (p.returncode == 0 and not e and removed == 0 and added == 3)
    print('BUILD %s' % ('OK' if ok else 'PROBLEM'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
