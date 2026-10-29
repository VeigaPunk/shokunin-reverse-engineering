#!/usr/bin/env python3
"""Independent spot-check of the frozen c6430 oracle tables (R50-C1).

Compares two independent readers of the carved carrier bytes
  A) /usr/bin/unsquashfs -lls  (listing: path, kind, size, link target)
  B) tools/round-41/sqfs-list.py --layout auto (path, sha256, size | path, kind, detail)
against the frozen tables
  tools/round-50/oracle/c6430.oracle.tsv        (rel, sha256, size)
  tools/round-50/oracle/c6430.nonregular.tsv    (rel, kind[, detail])

Exit 0 = all comparisons agree; 1 = disagreement; 2 = could not evaluate.
"""
import hashlib
import json
import os
import re
import sys

LLS_RE = re.compile(
    r'^(?P<mode>[bcdlps-][rwxsStT-]{9})\s+\S+\s+(?P<size>\d+(?:,\s*\d+)?)\s+'
    r'(?P<date>\S+)\s+(?P<time>\S+)\s+(?P<name>.*)$')

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(LANE, 'tools/round-50/oracle/c6430.oracle.tsv')
NONREG = os.path.join(LANE, 'tools/round-50/oracle/c6430.nonregular.tsv')
CARRIER = os.path.join(SCRATCH, 'carrier.bin')
LLS = os.path.join(SCRATCH, 'lls.txt')
SQLS_FILES = os.path.join(SCRATCH, 'sqfs.files.tsv')
SQLS_NONREG = os.path.join(SCRATCH, 'sqfs.nonreg.tsv')
OUT = os.path.join(SCRATCH, 'compare.json')

report = {'carrier': CARRIER, 'checks': {}, 'disagreements': []}


def fail(msg):
    report['disagreements'].append(msg)
    print('DISAGREE: ' + msg)


# ---------------------------------------------------------------- frozen tables
def read_tsv(path):
    rows = []
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if not line.strip():
                continue
            rows.append([c.rstrip('\r') for c in line.rstrip('\n').split('\t')])
    return rows


oracle_rows = read_tsv(ORACLE)
oracle = {}
for r in oracle_rows:
    if len(r) != 3:
        fail('oracle row has %d fields: %r' % (len(r), r))
        continue
    oracle[r[0].strip()] = (r[1].strip().lower(), int(r[2].strip()))

nonreg_rows = read_tsv(NONREG)
nonreg = {}
for r in nonreg_rows:
    if len(r) < 2:
        fail('nonregular row has %d fields: %r' % (len(r), r))
        continue
    if (r[0].strip(), r[1].strip().lower()) == ('relative_path', 'kind'):
        continue
    nonreg[r[0].strip()] = (r[1].strip().lower(),
                             r[2].strip() if len(r) > 2 else None)

report['frozen'] = {'oracle_rows': len(oracle), 'nonregular_rows': len(nonreg),
                    'nonregular_kinds': sorted({k for k, _ in nonreg.values()})}

# ---------------------------------------------------------------- reader A: unsquashfs -lls
lls_entries = {}
lls_kinds = {}
with open(LLS, 'r', encoding='utf-8', errors='replace') as fh:
    for line in fh:
        line = line.rstrip('\n')
        if not line.strip():
            continue
        m = LLS_RE.match(line)
        if not m:
            fail('unparsed -lls line: %r' % line)
            continue
        mode = m.group('mode')
        raw_size = m.group('size')
        size = int(raw_size.split(',')[0].strip())
        name = m.group('name').strip()
        target = None
        if ' -> ' in name:
            name, target = name.split(' -> ', 1)
        name = name.strip()
        if name == 'squashfs-root':
            continue
        rel = name[len('squashfs-root/'):] if name.startswith('squashfs-root/') else name
        kind = {'d': 'dir', 'l': 'symlink', 'c': 'char-device',
                'b': 'block-device', 'p': 'fifo', 's': 'socket'}.get(mode[0], 'file')
        lls_entries[rel] = {'kind': kind, 'size': size, 'target': target}
        lls_kinds[kind] = lls_kinds.get(kind, 0) + 1

report['lls'] = {'entries': len(lls_entries), 'kinds': lls_kinds}

# ---------------------------------------------------------------- reader B: sqfs-list.py
sqfs_files = {}
for r in read_tsv(SQLS_FILES):
    if len(r) != 3:
        fail('sqfs-list files row has %d fields: %r' % (len(r), r))
        continue
    sqfs_files[r[0].strip()] = (r[1].strip().lower(), int(r[2].strip()))

sqfs_nonreg = {}
for r in read_tsv(SQLS_NONREG):
    if len(r) < 2:
        fail('sqfs-list nonregular row has %d fields: %r' % (len(r), r))
        continue
    sqfs_nonreg[r[0].strip()] = (r[1].strip().lower(),
                                 r[2].strip() if len(r) > 2 else None)

report['sqfs_list'] = {'files': len(sqfs_files), 'nonregular': len(sqfs_nonreg),
                        'nonregular_kinds': sorted({k for k, _ in sqfs_nonreg.values()})}

# ---------------------------------------------------------------- checks
# C1: unsquashfs -lls regular-file row count == frozen oracle row count
lls_regular = {k: v for k, v in lls_entries.items() if v['kind'] == 'file'}
report['checks']['C1_lls_regular_count'] = {
    'lls_regular': len(lls_regular), 'oracle': len(oracle),
    'equal': len(lls_regular) == len(oracle)}
if len(lls_regular) != len(oracle):
    fail('unsquashfs -lls regular-file count %d != frozen oracle %d'
         % (len(lls_regular), len(oracle)))

# C2: unsquashfs -lls non-regular count == frozen nonregular row count
lls_nonreg = {k: v for k, v in lls_entries.items() if v['kind'] != 'file'}
report['checks']['C2_lls_nonregular_count'] = {
    'lls_nonregular': len(lls_nonreg), 'frozen_nonregular': len(nonreg),
    'equal': len(lls_nonreg) == len(nonreg)}
if len(lls_nonreg) != len(nonreg):
    fail('unsquashfs -lls non-regular count %d != frozen nonregular %d'
         % (len(lls_nonreg), len(nonreg)))

# C3: sqfs-list.py regular-file count == frozen oracle row count
report['checks']['C3_sqfsls_files_count'] = {
    'sqfs_list_files': len(sqfs_files), 'oracle': len(oracle),
    'equal': len(sqfs_files) == len(oracle)}
if len(sqfs_files) != len(oracle):
    fail('sqfs-list.py file count %d != frozen oracle %d'
         % (len(sqfs_files), len(oracle)))

# C4: sqfs-list.py non-regular count == frozen nonregular row count
report['checks']['C4_sqfsls_nonregular_count'] = {
    'sqfs_list_nonregular': len(sqfs_nonreg), 'frozen_nonregular': len(nonreg),
    'equal': len(sqfs_nonreg) == len(nonreg)}
if len(sqfs_nonreg) != len(nonreg):
    fail('sqfs-list.py non-regular count %d != frozen nonregular %d'
         % (len(sqfs_nonreg), len(nonreg)))

# C5: path sets, all three views
oracle_paths = set(oracle)
for label, paths in (('lls_regular', set(lls_regular)),
                     ('sqfs_list_files', set(sqfs_files))):
    report['checks']['C5_paths_' + label] = {
        'only_in_reader': sorted(paths - oracle_paths)[:10],
        'only_in_oracle': sorted(oracle_paths - paths)[:10],
        'equal': paths == oracle_paths}
    if paths != oracle_paths:
        fail('%s path set != oracle path set (reader-only %d, oracle-only %d)'
             % (label, len(paths - oracle_paths), len(oracle_paths - paths)))

nonreg_paths = set(nonreg)
for label, paths in (('lls_nonregular', set(lls_nonreg)),
                     ('sqfs_list_nonregular', set(sqfs_nonreg))):
    report['checks']['C5_paths_' + label] = {
        'only_in_reader': sorted(paths - nonreg_paths)[:10],
        'only_in_frozen': sorted(nonreg_paths - paths)[:10],
        'equal': paths == nonreg_paths}
    if paths != nonreg_paths:
        fail('%s path set != frozen nonregular path set (reader-only %d, frozen-only %d)'
             % (label, len(paths - nonreg_paths), len(nonreg_paths - paths)))

# C6: kinds agree for every non-regular path (path+kind, not link target)
kind_mismatch = []
for label, src in (('lls', {k: v['kind'] for k, v in lls_nonreg.items()}),
                   ('sqfs_list', {k: v[0] for k, v in sqfs_nonreg.items()})):
    for rel, kind in src.items():
        if rel in nonreg and nonreg[rel][0] != kind:
            kind_mismatch.append((label, rel, kind, nonreg[rel][0]))
report['checks']['C6_nonregular_kinds'] = {
    'mismatches': kind_mismatch[:10], 'n_mismatches': len(kind_mismatch),
    'equal': not kind_mismatch}
if kind_mismatch:
    fail('non-regular kind mismatches: %r' % kind_mismatch[:5])

# C7: sqfs-list.py sha256 + size == frozen oracle, FULL set (both directions)
mism = [p for p in (set(sqfs_files) & oracle_paths)
        if sqfs_files[p] != oracle[p]]
report['checks']['C7_sqfsls_full_sha256'] = {
    'compared': len(set(sqfs_files) & oracle_paths),
    'mismatches': mism[:10], 'n_mismatches': len(mism), 'equal': not mism}
if mism:
    fail('sqfs-list.py sha256/size mismatch on %d rows: %r' % (len(mism), mism[:5]))

# C8: unsquashfs -lls size == frozen oracle size, FULL set (both directions)
size_mism = [p for p in (set(lls_regular) & oracle_paths)
             if lls_regular[p]['size'] != oracle[p][1]]
report['checks']['C8_lls_full_size'] = {
    'compared': len(set(lls_regular) & oracle_paths),
    'mismatches': size_mism[:10], 'n_mismatches': len(size_mism), 'equal': not size_mism}
if size_mism:
    fail('unsquashfs -lls size mismatch on %d rows: %r' % (len(size_mism), size_mism[:5]))

# ---------------------------------------------------------------- required sample of 25
paths_sorted = sorted(oracle_paths)
first10 = paths_sorted[:10]
last10 = paths_sorted[-10:]
mid = paths_sorted[10:-10] if len(paths_sorted) > 20 else []
# 5 hash-random rows: deterministic on the path string
hashed = sorted(mid, key=lambda p: hashlib.sha256(p.encode()).hexdigest())
rand5 = hashed[:5]
sample = first10 + last10 + rand5
sample = sorted(set(sample))
report['sample'] = {'n': len(sample), 'first10': first10, 'last10': last10,
                    'hash_random5': rand5, 'sample': sample}
sample_rows = []
for p in sample:
    row = {'path': p, 'frozen_sha256': oracle[p][0], 'frozen_size': oracle[p][1],
           'sqfs_list_sha256': sqfs_files.get(p, (None, None))[0],
           'sqfs_list_size': sqfs_files.get(p, (None, None))[1],
           'lls_size': lls_regular.get(p, {}).get('size')}
    row['equal'] = (row['sqfs_list_sha256'] == row['frozen_sha256']
                    and row['sqfs_list_size'] == row['frozen_size']
                    and row['lls_size'] == row['frozen_size'])
    if not row['equal']:
        fail('sample row disagrees: %r' % row)
    sample_rows.append(row)
report['checks']['C9_sample25'] = {'n': len(sample_rows),
                                   'all_equal': all(r['equal'] for r in sample_rows),
                                   'rows': sample_rows}

# ---------------------------------------------------------------- all non-regular rows
nr_rows = []
nr_mism = 0
for rel in sorted(nonreg_paths):
    kind, detail = nonreg[rel]
    lls_e = lls_nonreg.get(rel)
    sq_e = sqfs_nonreg.get(rel)
    row = {'path': rel, 'frozen_kind': kind, 'frozen_detail': detail,
           'lls_kind': lls_e['kind'] if lls_e else None,
           'lls_target': lls_e['target'] if lls_e else None,
           'sqfs_kind': sq_e[0] if sq_e else None,
           'sqfs_detail': sq_e[1] if sq_e else None}
    ok = (lls_e is not None and sq_e is not None
          and lls_e['kind'] == kind and sq_e[0] == kind)
    row['equal_kind'] = ok
    if not ok:
        nr_mism += 1
    nr_rows.append(row)
report['checks']['C10_all_nonregular'] = {'n': len(nr_rows), 'n_kind_mismatch': nr_mism,
                                          'equal': nr_mism == 0,
                                          'rows': nr_rows}

report['verdict'] = 'PASS' if not report['disagreements'] else 'FAIL'
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(report, fh, indent=1, sort_keys=True)
print('verdict=%s disagreements=%d -> %s' % (report['verdict'],
                                             len(report['disagreements']), OUT))
sys.exit(0 if not report['disagreements'] else 1)
