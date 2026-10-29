#!/usr/bin/env python3
"""Standalone checker for the C3 claim's "Counting command" bullet.

The frozen instrument (tools/round-50-c3/sqfs-triage-v5.py, sha256 ef4633c5...) carries
a selftest case that checks the claim's before-run revision and before-state size.  That
case reads the claims file as a WHOLE, so it still passes when the "Counting command"
BULLET itself is stale - the frozen-details bullets carry the right strings elsewhere
(reproduced: receipts/guard-defect-proof.txt section A).  The bullet-scoped fix is
patches/claim-counting-bullet-guard.patch, but the instrument is frozen for this round
and its receipts bind `instrument_sha256`, so changing it would stale every falsify
receipt.

This checker is the same assertion, STANDALONE: it changes no frozen byte and can be run
by the falsify wave against any claims file.

    python3 -I -B check-claim-counting-bullet.py [CLAIMS_FILE]

Exit codes: 0 the bullet names the declared base and the seat-measured before-state;
1 the bullet is stale, names the superseded base, or drops the ddwrt failed-body name;
2 the claims file could not be read, or carries no Counting command bullet.
"""
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DEFAULT = os.path.join(LANE, 'plans', 'round-50-attempt2-claims.md')
DECLARED_BASE = 'f890bbea'
SUPERSEDED_BASE = '8ccc05e6'
DDWRT_BODY = 'dmg_Z3_v3ddwrt_inode_table'
BEFORE_STATE = 'seat-measured **19**'


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except OSError as exc:
        sys.stderr.write('cannot read %r: %s\n' % (path, exc.strerror or exc))
        return 2
    flat = ' '.join(text.split())
    start = flat.find('- **Counting command**:')
    if start < 0:
        sys.stderr.write('the claim carries no Counting command bullet\n')
        return 2
    end = flat.find('- **', start + 10)
    bullet = flat[start:end if end > 0 else len(flat)]
    problems = []
    if DECLARED_BASE not in bullet:
        problems.append('the Counting command bullet does not name the declared base %s'
                        % DECLARED_BASE)
    if BEFORE_STATE not in bullet:
        problems.append('the Counting command bullet does not carry the %s before-state'
                        % BEFORE_STATE)
    if '19' not in bullet:
        problems.append('the Counting command bullet does not name the 19-row before-state')
    if SUPERSEDED_BASE in bullet:
        problems.append('the Counting command bullet still names the superseded base %s'
                        % SUPERSEDED_BASE)
    if DDWRT_BODY not in flat:
        problems.append('the claim does not name the ddwrt failed-body residue %s'
                        % DDWRT_BODY)
    if problems:
        for problem in problems:
            sys.stderr.write('%s\n' % problem)
        sys.stderr.write('the bullet reads: %s\n' % bullet[:200])
        return 1
    print('ok: the Counting command bullet names the declared base %s, the %s '
          'before-state and the ddwrt failed body' % (DECLARED_BASE, BEFORE_STATE))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
