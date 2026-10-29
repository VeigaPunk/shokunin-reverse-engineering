#!/usr/bin/env python3
"""Receipt runner for ScribeProvinceBinding (kaidoku round 50, attempt 2, wave 3).

Runs a fixed list of READ-ONLY commands (lane `git` reads, greps, sha256 sums and
the seat's own offline binding check), and writes one receipt per command with the
exact argv, the UTC start/end, the exit code, the stdout sha256 and the stdout
(trimmed).  Nothing is written outside the seat's own directory.

Usage: python3 -I -B run-receipts.py <lane-root> <seat-dir>
"""
import hashlib
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = None
SEAT = None

CMDS = [
    ('head', ['git', '-C', '{lane}', 'rev-parse', 'HEAD']),
    ('status', ['git', '-C', '{lane}', 'status', '--porcelain']),
    ('frozen-counter-blob',
     ['git', '-C', '{lane}', 'show',
      '435d41fd4ad9211d1579fc447936fb33d2b74467:tools/round-50/c1-counter.py']),
    ('working-counter',
     ['sha256sum', '{lane}/tools/round-50/c1-counter.py']),
    ('counter-constants',
     ['grep', '-n', '-e', '^ENTRY', '-e', '^STEM', '-e', '^CORE_HEADING',
      '-e', '^FRONTIER_MARK', '-e', '^HANDLER_RE', '-e', '^AVM_MARKER_RE',
      '-e', '^LE_AVM_RE', '{lane}/tools/round-50/c1-counter.py']),
    ('attempt2-stem',
     ['grep', '-n', 'r50-le-avm-hsqs-core', '{lane}/plans/round-50-attempt2-claims.md']),
    ('frozen-stem-sites',
     ['grep', '-rn', 'r50-avm-le-squashfs-core', '{lane}/tools/round-50/']),
    ('sources-s24-rows',
     ['grep', '-n', '^| S24', '{lane}/corpus/SOURCES.md']),
    ('sources-row-count',
     ['grep', '-c', '^| S', '{lane}/corpus/SOURCES.md']),
    ('gap-rule',
     ['cat', '{lane}/tools/round-50/gap-rule.json']),
    ('oracle-kind-counts',
     ['bash', '-lc',
      "for f in {lane}/tools/round-50/oracle/*.nonregular.tsv; do "
      "echo \"--- $f\"; awk -F'\\t' '{c[$2]++} END{for(k in c) print k, c[k]}' \"$f\"; done"]),
    ('oracle-file-counts',
     ['bash', '-lc',
      "for f in {lane}/tools/round-50/oracle/*.oracle.tsv; do "
      "echo -n \"$f \"; wc -l < \"$f\"; done"]),
    ('frontier-le-avm-sites',
     ['grep', '-n', '-o', 'LE AVM members (`hsqs`)', '{lane}/PROVINCE.md']),
    ('binding-check',
     ['python3', '-I', '-B', '{seat}/check-bindings.py', '{seat}/province.md', '{lane}']),
    ('disk-guard',
     ['bash', '{fleet}/scripts/hyaku/disk-guard.sh', 'status']),
]


def main(argv):
    global LANE, SEAT
    LANE, SEAT = argv[1], argv[2]
    fleet = '/home/vgpnk/Projects/shokunin'
    rows = []
    for name, argv0 in CMDS:
        cmd = [a.replace('{lane}', LANE).replace('{seat}', SEAT).replace('{fleet}', fleet)
               for a in argv0]
        start = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=300)
            out, err, rc = p.stdout, p.stderr, p.returncode
        except Exception as e:                      # noqa: BLE001 - receipt of a failure
            out, err, rc = b'', str(e).encode(), 127
        end = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        rows.append((name, ' '.join(cmd), rc, start, end,
                     hashlib.sha256(out).hexdigest(), len(out), out, err))
    lines = ['# Receipts — ScribeProvinceBinding (kaidoku round 50, attempt 2, wave 3)',
             '',
             'Every command is read-only (lane `git` reads, greps, sha256 sums, the seat\'s',
             'own offline binding check). No REA, no network fetch, no write outside this',
             'seat directory.', '',
             '| # | receipt | command | exit | UTC start | UTC end | stdout sha256 | stdout bytes |',
             '|---|---|---|---|---|---|---|---|']
    for i, (name, cmd, rc, s, e, sha, n, out, err) in enumerate(rows, 1):
        lines.append('| %d | %s | `%s` | %d | %s | %s | `%s` | %d |'
                     % (i, name, cmd.replace('|', '\\|'), rc, s, e, sha, n))
    lines += ['', '## stdout of each receipt', '']
    for (name, cmd, rc, s, e, sha, n, out, err) in rows:
        lines.append('### %d. %s (exit %d)' % (rows.index((name, cmd, rc, s, e, sha, n, out, err)) + 1, name, rc))
        lines.append('```')
        txt = out.decode('utf-8', 'replace')
        lines.append(txt[:4000])
        if err:
            lines.append('--- stderr ---')
            lines.append(err.decode('utf-8', 'replace')[:2000])
        lines.append('```')
        lines.append('')
    with open(os.path.join(SEAT, 'receipts.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    print('\n'.join(l for l in lines if l.startswith('| ')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
