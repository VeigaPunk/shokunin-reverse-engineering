#!/usr/bin/env python3
"""Build plans/round-50-claims.md from plan-template.md by copying the predicate paragraphs
byte-for-byte out of the counters' docstrings; `--check` re-extracts and compares.

  mkplan.py            write <lane>/plans/round-50-claims.md
  mkplan.py --check    exit 0 when every predicate paragraph in the plan equals the counter's
                       docstring paragraph (read from tools/round-50/ in the working tree, or
                       from `--rev REV` git objects), exit 1 otherwise
"""
import argparse
import os
import re
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
HERE = os.path.dirname(os.path.abspath(__file__))
C1 = 'tools/round-50/c1-counter.py'
C2 = 'tools/round-50/c2-record.py'
PLAN = 'plans/round-50-claims.md'


def read(lane, rev, path):
    if rev:
        p = subprocess.run(['git', '-C', lane, 'show', '%s:%s' % (rev, path)], capture_output=True)
        if p.returncode != 0:
            raise SystemExit('cannot read %s at %s' % (path, rev))
        return p.stdout.decode()
    return open(os.path.join(lane, path), encoding='utf8').read()


def p_c1(src):
    m = re.search(r'^(  At the measured revision REV, for each frozen carrier,.*?freeze\.)\n', src, re.S | re.M)
    if not m:
        raise SystemExit('C1 predicate paragraph not found')
    return m.group(1)


def p_c2(src):
    m = re.search(r'^(Predicate \(the same sentence as the plan\):.*?)\n\nFreeze integrity:', src, re.S | re.M)
    if not m:
        raise SystemExit('C2 predicate paragraph not found')
    return m.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', default=LANE)
    ap.add_argument('--rev')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    c1 = p_c1(read(a.lane, a.rev, C1))
    c2 = p_c2(read(a.lane, a.rev, C2))
    if a.check:
        plan = read(a.lane, a.rev, PLAN)
        ok = c1 in plan and c2 in plan
        print('C1 paragraph in plan: %s; C2 paragraph in plan: %s' % (c1 in plan, c2 in plan))
        return 0 if ok else 1
    tpl = open(os.path.join(HERE, 'plan-template.md'), encoding='utf8').read()
    out = tpl.replace('{{P50C1}}', c1).replace('{{P50C2}}', c2)
    assert '{{' not in out
    os.makedirs(os.path.join(a.lane, 'plans'), exist_ok=True)
    with open(os.path.join(a.lane, PLAN), 'w', encoding='utf8') as f:
        f.write(out)
    print('wrote', os.path.join(a.lane, PLAN), len(out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
