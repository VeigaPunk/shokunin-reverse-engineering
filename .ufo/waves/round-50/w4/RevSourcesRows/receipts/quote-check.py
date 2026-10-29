#!/usr/bin/env python3
"""RevSourcesRows (w4) — independent re-locate check of the four landed SOURCES
rows' anchors against bodies fetched fresh on 2026-10-29T21:28Z.

Exit 0 when every anchored element locates byte-contiguously; exit 1 otherwise.
Writes only its stdout receipt.
"""
import re, sys

F = '/fast/scratch/hyaku/kaidoku-r50/w4-RevSourcesRows/fetch'

def lines(p):
    with open(p, encoding='utf8', errors='replace') as fh:
        return fh.read().split('\n')

located = missing = 0
def check(rid, path, lineno, want):
    global located, missing
    ls = lines(path)
    if lineno > len(ls):
        print('MISSING LINE %s :%d (file has %d lines)' % (rid, lineno, len(ls)))
        missing += 1; return
    got = ls[lineno - 1]
    if want in got:
        located += 1
        print('LOCATED   %s :%d  %s' % (rid, lineno, want[:70]))
    else:
        missing += 1
        print('MISSING   %s :%d  want=%r got=%r' % (rid, lineno, want[:60], got[:80]))

# S243 — Freetz patch 101: :7 symbol, :17-18 LE condition + __LITTLE_ENDIAN
check('S243', F + '/s243.patch', 7, '+#define AVM_LE 2')
check('S243', F + '/s243.patch', 17, 'TARGET_FORMAT == SQUASHFS4_LE || TARGET_FORMAT == AVM_LE')
check('S243', F + '/s243.patch', 18, '#define TARGET_FORMAT_BYTE_ORDER __LITTLE_ENDIAN')

# S245 — unblob 26.6.4 squashfs.py: :53-54 LE argv, :455 NAME, :48 is_avm in :40 BIG branch
check('S245', F + '/s245-squashfs.py', 53, 'case Endian.LITTLE, _:')
check('S245', F + '/s245-squashfs.py', 54, 'commands_args.append("-le")')
check('S245', F + '/s245-squashfs.py', 455, 'NAME = "squashfs_v4_le"')
check('S245', F + '/s245-squashfs.py', 48, 'is_avm = header.bytes_used == header.mkfs_time')
check('S245', F + '/s245-squashfs.py', 40, 'case Endian.BIG, 4:')
# knowledge-entry extras: LE pattern at :463
check('S245', F + '/s245-squashfs.py', 463, '68 73 71 73 [24] 04 00')

# S249 — AVM licence: :850 quote (18 words)
q850 = 'The licensee may create only one copy of the software, which may be used exclusively for backup use.'
check('S249', F + '/s249-info_en.txt', 850, q850)
print('INFO      S249 quote word count = %d (<=25 required)' % len(q850.split()))

# S244 — listing rows: filename + date + size contiguous per served body
LIST = [
    ('s244-7581.html', 'FRITZ.Box_7581-07.18.image', '19-Aug-2024 12:33', '32010240'),
    ('s244-7582.html', 'FRITZ.Box_7582-07.18.image', '19-Aug-2024 12:36', '32256000'),
    ('s244-6490.html', 'FRITZ.Box_6490_Cable-07.57.image', '04-Sep-2023 17:07', '39741440'),
    ('s244-6430.html', 'FRITZ.Box_6430_Cable-07.30.image', '05-Sep-2023 09:10', '35911680'),
]
for fn, name, date, size in LIST:
    body = open(F + '/' + fn, encoding='utf8', errors='replace').read()
    flat = re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', '', body))
    want = '%s %s %s' % (name, date, size)
    if want in flat:
        located += 1
        print('LOCATED   S244 %s  row %s' % (fn, want))
    else:
        missing += 1
        print('MISSING   S244 %s  row %s' % (fn, want))

# S244 — root index lists the four carrier dirs
root = open(F + '/s244-root.html', encoding='utf8', errors='replace').read()
for d in ('fritzbox-7581/', 'fritzbox-7582/', 'fritzbox-6490-cable/', 'fritzbox-6430-cable/'):
    if d in root:
        located += 1
        print('LOCATED   S244 root dir %s' % d)
    else:
        missing += 1
        print('MISSING   S244 root dir %s' % d)

print('QUOTE_CHECK located=%d missing=%d' % (located, missing))
sys.exit(0 if missing == 0 else 1)
