#!/usr/bin/env python3
"""ScribeRowsSources — locate-check every quote the four draft rows anchor on,
against the bodies re-fetched on 2026-10-29.

Exit 0 when every quote is located at the stated line; exit 1 otherwise.
Reads only the seat scratch; writes only its stdout receipt.
"""
import os
import re
import sys

S = os.environ.get('S', '/fast/scratch/hyaku/kaidoku-r50/w3-ScribeRowsSources')
SRC = S + '/src'

# (id, file, line, expected substring on that line)
CHECKS = [
    ('S243', 'S243-freetz-101.patch', 7, '+#define AVM_LE 2'),
    ('S243', 'S243-freetz-101.patch', 8, '+#define AVM_BE 3'),
    ('S243', 'S243-freetz-101.patch', 17, 'TARGET_FORMAT == SQUASHFS4_LE || TARGET_FORMAT == AVM_LE'),
    ('S243', 'S243-freetz-101.patch', 18, '#define TARGET_FORMAT_BYTE_ORDER __LITTLE_ENDIAN'),
    ('S245', 'S245-unblob-squashfs.py', 53, 'case Endian.LITTLE, _:'),
    ('S245', 'S245-unblob-squashfs.py', 54, 'commands_args.append("-le")'),
    ('S245', 'S245-unblob-squashfs.py', 455, 'NAME = "squashfs_v4_le"'),
    ('S245', 'S245-unblob-squashfs.py', 48, 'is_avm = header.bytes_used == header.mkfs_time'),
    ('S245', 'S245-unblob-squashfs.py', 40, 'case Endian.BIG, 4:'),
    ('S249', 'S249-info_en.txt', 850,
     'The licensee may create only one copy of the software, which may be used exclusively for backup use.'),
]

# listing rows the S244 anchor names, checked against the four index bodies
LISTING = [
    ('S244', 'S244-7581-index.html', 'FRITZ.Box_7581-07.18.image', '19-Aug-2024 12:33', '32010240'),
    ('S244', 'S244-7582-index.html', 'FRITZ.Box_7582-07.18.image', '19-Aug-2024 12:36', '32256000'),
    ('S244', 'S244-6490-index.html', 'FRITZ.Box_6490_Cable-07.57.image', '04-Sep-2023 17:07', '39741440'),
    ('S244', 'S244-6430-index.html', 'FRITZ.Box_6430_Cable-07.30.image', '05-Sep-2023 09:10', '35911680'),
]

located = 0
missing = 0
for rid, fn, lineno, want in CHECKS:
    path = os.path.join(SRC, fn)
    if not os.path.exists(path):
        print('MISSING FILE %s %s' % (rid, fn))
        missing += 1
        continue
    with open(path, encoding='utf8', errors='replace') as fh:
        lines = fh.read().split('\n')
    if lineno > len(lines):
        print('MISSING LINE %s %s:%d (file has %d lines)' % (rid, fn, lineno, len(lines)))
        missing += 1
        continue
    line = lines[lineno - 1]
    if want in line:
        located += 1
        print('LOCATED   %s %s:%d  %s' % (rid, fn, lineno, want[:64]))
    else:
        missing += 1
        print('MISSING   %s %s:%d  want=%r got=%r' % (rid, fn, lineno, want[:60], line[:80]))

for rid, fn, name, date, size in LISTING:
    path = os.path.join(SRC, fn)
    with open(path, encoding='utf8', errors='replace') as fh:
        body = fh.read()
    # the AVM index is an Apache-style HTML listing: the file name sits inside an
    # <a> tag, the date and size follow as whitespace-separated columns.
    flat = re.sub(r'<[^>]*>', '', body)
    flat = re.sub(r'\s+', ' ', flat)
    want = '%s %s %s' % (name, date, size)
    if want in flat:
        located += 1
        print('LOCATED   %s %s  listing row %s' % (rid, fn, want))
    else:
        missing += 1
        print('MISSING   %s %s  listing row %s' % (rid, fn, want))

# the root index must list the four model dirs (the S244 source cell names them)
root = re.sub(r'\s+', ' ', open(os.path.join(SRC, 'S244-root-index.html'), encoding='utf8',
                                errors='replace').read())
for d in ('fritzbox-7581/', 'fritzbox-7582/', 'fritzbox-6490-cable/', 'fritzbox-6430-cable/'):
    if d in root:
        located += 1
        print('LOCATED   S244 S244-root-index.html  dir %s' % d)
    else:
        missing += 1
        print('MISSING   S244 S244-root-index.html  dir %s' % d)

print('QUOTE_CHECK located=%d missing=%d' % (located, missing))
sys.exit(0 if missing == 0 else 1)
