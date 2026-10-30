#!/usr/bin/env python3
"""Collect the R51-C1 knowledge-entry's receipt ledger (ScribeEntryC1, wave 1).

Every receipt is (id, UTC, exit code, stdout sha256, exact command). All commands
run read-only inside the lane checkout; none of them runs REA, downloads vendor
bytes, or mutates the lane tree. The ledger is written to the seat directory and
copied into the entry's "Commands and receipts" table.

Usage: python3 -I -B receipts-collect.py --lane <LANE> --out <FILE>
Exit: 0 the ledger was written, 1 a usage/IO error.
"""
import argparse
import datetime
import hashlib
import os
import subprocess
import sys

# (id, shell command) — every command is read-only against the lane.
COMMANDS = [
    ('census-char-devices',
     'for f in c6430 c6490 g7581 g7582; do '
     'n=$(awk -F\'\\t\' \'$2=="char-device"\' tools/round-50/oracle/$f.nonregular.tsv | wc -l); '
     'echo "$f char-device=$n"; done'),
    ('census-kinds',
     'for f in c6430 c6490 g7581 g7582; do echo "== $f"; '
     'awk -F\'\\t\' \'{c[$2]++}END{for(k in c)printf "  %s=%d\\n",k,c[k]}\' '
     'tools/round-50/oracle/$f.nonregular.tsv; done'),
    ('census-fritzbox-twelve',
     'for f in g7581 g7582; do '
     'n=$(awk -F\'\\t\' \'$2=="char-device" && $1!="dev/led"\' '
     'tools/round-50/oracle/$f.nonregular.tsv | wc -l); '
     'echo "$f other-char-device=$n"; done'),
    ('census-g7581-devices',
     'awk -F\'\\t\' \'$2=="char-device"{print $1"\\t"$3}\' '
     'tools/round-50/oracle/g7581.nonregular.tsv'),
    ('oracle-tables-sha',
     'sha256sum tools/round-50/oracle/*.nonregular.tsv tools/round-50/oracle/*.oracle.tsv'),
    ('gap-rule-r50',
     'cat tools/round-50/gap-rule.json'),
    ('gap-rule-r50-silent',
     'python3 -c "import json;d=json.load(open(\'tools/round-50/gap-rule.json\'));'
     'print(\'required\',d[\'required\']);print(\'silent\',d[\'removed\'][\'silent\'])"'),
    ('r50-miss-receipt',
     'python3 -c "import json;d=json.load(open(\'.ufo/waves/round-50/l1/scores/'
     'c1-after-attempt2.json\'));print(\'carriers_matched\',d[\'carriers_matched\']);'
     'print(\'exit_code\',d[\'exit_code\']);print(\'target\',d[\'target\']);'
     'print(\'gaps_ok\',{k:v.get(\'gaps_ok\') for k,v in d[\'carriers\'].items()})"'),
    ('r50-miss-carriers',
     'python3 -c "import json;d=json.load(open(\'.ufo/waves/round-50/l1/scores/'
     'c1-after-attempt2.json\'));'
     '[print(k,\'gaps_ok\',v.get(\'gaps_ok\'),\'projection_ok\',v.get(\'projection_ok\'),'
     '\'nonregular_unpublished_ok\',v.get(\'nonregular_unpublished_ok\')) '
     'for k,v in sorted(d[\'carriers\'].items())]"'),
    ('r50-unpublished-kinds',
     'for id in c6430 c6490 g7581 g7582; do python3 -c "import json;'
     'from collections import Counter;d=json.load(open(\'corpus/evidence/round-50/c1/'
     '$id/after.json\'));n=d[\'normalized_result\'];'
     'print(\'$id\',len(n[\'files\']),dict(Counter(x[\'kind\'] '
     'for x in n[\'unpublished_entries\'])))"; done'),
    ('law-device-disposition',
     'python3 .ufo/waves/round-51/w1/ScribeEntryC1/law-device-disposition.py --lane .'),
    ('rule-scope-offline',
     'python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/rule-scope-offline.py '
     '--lane . --rule OLD=tools/round-50/gap-rule.json '
     '--rule NEW=.ufo/waves/round-51/w1/ExecRuleDerive/gap-rule-v2.json'),
    ('rule-shape-variants-offline',
     'python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/rule-variants-offline.py --lane .'),
    ('failclosed-probe',
     'python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/failclosed-probe.py --lane .'),
    ('entry-binding-check',
     'python3 -I -B .ufo/waves/round-51/w1/ScribeEntryC1/entry-binding-check.py --lane . '
     '--entry .ufo/waves/round-51/w1/ScribeEntryC1/entry.md '
     '--entry-path corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md '
     '--opened-date 2026-10-30'),
    ('knowledge-file-count',
     'git ls-tree -r --name-only HEAD corpus/knowledge | grep -c \'\\.md$\''),
    ('sources-row-count',
     'grep -c "^| S[0-9][0-9][0-9] |" corpus/SOURCES.md'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    rows = []
    for cid, cmd in COMMANDS:
        t0 = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        p = subprocess.run(cmd, shell=True, cwd=args.lane, capture_output=True)
        digest = hashlib.sha256(p.stdout).hexdigest()
        rows.append((cid, t0, p.returncode, digest, cmd))
        sys.stderr.write('%s exit=%d sha256=%s\n' % (cid, p.returncode, digest[:16]))
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write('id\tutc\texit\tstdout_sha256\tcommand\n')
        for r in rows:
            fh.write('%s\t%s\t%d\t%s\t%s\n' % r)
    return 0


if __name__ == '__main__':
    sys.exit(main())
