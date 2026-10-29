#!/usr/bin/env python3
"""Receipts: re-run each load-bearing read-only command, capture exit, stdout sha256, UTC."""
import subprocess, hashlib, json, datetime, os

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SCRATCH = '/fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry'
OUT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w3/RevB9Registry/receipts.json'

COMMANDS = [
 ('census-r49-r50-at-base',
  "git ls-tree -r --name-only f890bbead20ca2c549487167f56876ae47f1e1a4 -- tools/round-49 tools/round-50 | grep -E '\\.(py|sh)$' | grep -v control-fixtures | sort"),
 ('rowcount-per-commit',
  r"for c in 845e0586 11ccdb72 f890bbea; do n=$(git show $c:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -c '^| `tools/'); echo \"$c rows=$n\"; done"),
 ('rows-added-at-attempt1-landing',
  r"diff <(git show 845e0586:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -o '^| `[^`]*`' | sort) <(git show 11ccdb72:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -o '^| `[^`]*`' | sort)"),
 ('rows-f890-vs-11cc',
  r"diff <(git show 11ccdb72:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -o '^| `[^`]*`' | sort) <(git show f890bbea:SKILL.md | sed -n '/<!-- instrument-registry v2 -->/,/<!-- \/instrument-registry -->/p' | grep -o '^| `[^`]*`' | sort) && echo IDENTICAL"),
 ('b9-hand-replica',
  "python3 /fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/b9-replica.py"),
 ('drift-scan',
  "python3 /fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/drift-scan.py"),
 ('attempt1-cell-dump',
  "python3 /fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/attempt1-cells.py"),
 ('header-separator-bytes',
  "git show f890bbea:SKILL.md | sed -n '1715,1718p' | cat -A"),
 ('skillmd-blob-f890-vs-head',
  "git rev-parse f890bbead20ca2c549487167f56876ae47f1e1a4:SKILL.md 6f4aba635fc47b5823ed42afe9c8b5dc3e28127f:SKILL.md"),
 ('c2record-blob-f890-vs-freeze',
  "git rev-parse f890bbead20ca2c549487167f56876ae47f1e1a4:tools/round-50/c2-record.py 435d41fd4ad9211d1579fc447936fb33d2b74467:tools/round-50/c2-record.py"),
 ('tools49-unchanged-counterbase-to-base',
  "git diff --name-only 7c678ae6d97aedb969fd253b52b3d2882ef1e186 f890bbead20ca2c549487167f56876ae47f1e1a4 -- tools/round-49"),
 ('registry-marker-span',
  "git show f890bbea:SKILL.md | grep -n 'instrument-registry v2\\|/instrument-registry'"),
]

receipts = []
for name, cmd in COMMANDS:
    t0 = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    if cmd.startswith('python3'):
        full = cmd
        p = subprocess.run(['bash', '-c', full], capture_output=True, cwd=SCRATCH)
    else:
        full = 'cd %s && %s' % (LANE, cmd)
        p = subprocess.run(['bash', '-c', full], capture_output=True)
    out = p.stdout
    receipts.append({
        'name': name,
        'command': cmd,
        'exit_code': p.returncode,
        'stdout_sha256': hashlib.sha256(out).hexdigest(),
        'stdout_bytes': len(out),
        'utc': t0,
    })
    print(name, 'exit=', p.returncode, 'sha256=', receipts[-1]['stdout_sha256'][:16])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(receipts, open(OUT, 'w'), indent=1)
print('wrote', OUT)
