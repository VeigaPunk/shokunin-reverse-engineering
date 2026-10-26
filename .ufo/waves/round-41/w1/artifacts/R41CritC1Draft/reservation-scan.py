#!/usr/bin/env python3
"""Reservation audit prototype for round 41's four reserved AVM images.

The wave context reserves FRITZ!Box 3490 07.31, 5490 07.31, 5491 07.31 and 7560
07.30 (plus the lane-built L3/L4 carriers) against every REA/unblob run, and lets
exactly one seat per vendor carrier read the image (`R41C1VendorV3`,
`R41C1VendorV4`) with a reader (`sqfs-list.py`, `sasquatch-v4be`, tar/HTTP).

Nothing in the draft C1 predicate or the counter asks for evidence of that. This
script is the cheapest checkable form of it: scan one wave tree for the reserved
tokens, classify every line that names one, and go red on any REA (`extract-
firmware`) or unblob invocation, or on a reader invocation by a non-owner seat.

Usage:
  reservation-scan.py --wave DIR [--reserved FILE] [--out FILE] [--selftest]

Exit 0 green, 1 red, 2 usage. Only reads; writes only --out. Honours TMPDIR.
"""
import argparse
import json
import os
import re
import sys
import tempfile

# The four reserved images (task context, wave-1 dispatch context). The 3490 and
# 7560 image sha256 are not published anywhere this lane holds: they are matched
# by URL prefix only and reported as `identity_by_url` [INFERENCE on the exact
# 7560 file name]. 5490/5491 carry the sha256 the seats pinned.
RESERVED = [
    {'id': '3490-07.31', 'url_prefix': 'https://download.avm.de/fritzbox/fritzbox-3490/',
     'image_sha256': None, 'member_sha256': None},
    {'id': '5490-07.31', 'url_prefix': 'https://download.avm.de/fritzbox/fritzbox-5490/',
     'image_sha256': '770efb4e368a58104bf362c990114db8b70a5060932ce8bcec7ef1bc75045ab7',
     'member_sha256': '87cc5d6b3ad105221114a86f6a4d4d868f731b868ff875979e7f0cb47bcea0f8'},
    {'id': '5491-07.31', 'url_prefix': 'https://download.avm.de/fritzbox/fritzbox-5491/',
     'image_sha256': 'a5a3a763a615c2dab226d15463bc05fbc74e844736687fa5cc87a91d2f35f661',
     'member_sha256': '4cfc3016d84cccf4982d6a4c50935f1771ad350994f569496e91e42be3d92f6c'},
    {'id': '7560-07.30', 'url_prefix': 'https://download.avm.de/fritzbox/fritzbox-7560/',
     'image_sha256': None, 'member_sha256': None},
]
OWNERS = {'R41C1VendorV3': {'5490-07.31'}, 'R41C1VendorV4': {'5491-07.31'}}

REA_RE = re.compile(r'extract-firmware|rea-agents')
UNBLOB_CMD_RE = re.compile(r'(^|[\s;|&(])unblob(\s|$)')
READER_RE = re.compile(r'sqfs-list\.py|sasquatch-v4be|sasquatch\b')
NET_READ_RE = re.compile(r'\bcurl\b|\bwget\b|\btar\b|tarfile|Range:')
SHA_RE = re.compile(r'[0-9a-f]{64}')
MAX_BYTES = 1 << 20


def reserved_hits(line, reserved):
    ids = set()
    for r in reserved:
        if r['url_prefix'] and r['url_prefix'] in line:
            ids.add(r['id'])
        if r['image_sha256'] and r['image_sha256'] in line:
            ids.add(r['id'])
        if r['member_sha256'] and r['member_sha256'] in line:
            ids.add(r['id'])
    return ids


def seat_of(path, wave):
    rel = os.path.relpath(path, wave)
    parts = rel.split(os.sep)
    if parts[0] == 'artifacts' and len(parts) >= 2:
        return parts[1]
    if parts[0] == 'artifacts':
        return '<artifacts-root>'
    return os.path.splitext(parts[0])[0] if parts else '<wave>'


def classify(line, seat):
    """(action, red, why) for one line that names a reserved image."""
    if REA_RE.search(line):
        return 'rea', True, 'REA invocation naming a reserved image'
    if UNBLOB_CMD_RE.search(line):
        return 'unblob', True, 'unblob invocation naming a reserved image'
    if READER_RE.search(line):
        ok = seat in OWNERS
        return 'reader', not ok, ('owner read' if ok else 'non-owner reader')
    if NET_READ_RE.search(line):
        return 'identity-read', False, 'HTTP/tar identity read'
    return 'mention', False, 'reserved name mentioned, no invocation'


def scan(wave, reserved=RESERVED):
    rows = []
    for root, dirs, files in os.walk(wave):
        dirs[:] = [d for d in dirs if d not in ('.git',)]
        for name in files:
            p = os.path.join(root, name)
            try:
                if os.path.getsize(p) > MAX_BYTES:
                    continue
                raw = open(p, 'rb').read()
                if b'\0' in raw[:4096]:
                    continue
                text = raw.decode('utf-8', 'replace')
            except OSError:
                continue
            if not any(tok for r in reserved
                       for tok in (r['url_prefix'], r['image_sha256'],
                                   r['member_sha256']) if tok and tok in text):
                continue
            seat = seat_of(p, wave)
            for ln, line in enumerate(text.splitlines(), 1):
                ids = reserved_hits(line, reserved)
                if not ids:
                    continue
                action, red, why = classify(line, seat)
                rows.append({'file': os.path.relpath(p, wave), 'line': ln,
                             'seat': seat, 'reserved': sorted(ids),
                             'action': action, 'red': red, 'why': why,
                             'text': line.strip()[:240]})
    reds = [r for r in rows if r['red']]
    return {'wave': wave, 'rows': len(rows), 'red': len(reds),
            'by_action': {a: sum(1 for r in rows if r['action'] == a)
                          for a in sorted({r['action'] for r in rows})},
            'findings': rows, 'verdict': 'red' if reds else 'green'}


def selftest():
    with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as d:
        os.makedirs(os.path.join(d, 'artifacts/R41C1VendorV3'))
        os.makedirs(os.path.join(d, 'artifacts/R41C1Scout'))
        url = RESERVED[1]['url_prefix'] + 'FRITZ.Box_5490-07.31.image'
        open(os.path.join(d, 'artifacts/R41C1VendorV3/oracle-run.json'), 'w').write(
            '{"cmd": "sasquatch-v4be -f -d out %s"}\n' % url)
        open(os.path.join(d, 'artifacts/R41C1Scout/run.log'), 'w').write(
            'curl -o 5490.image %s\n' % url)
        green = scan(d)
        assert green['verdict'] == 'green', green
        planted = os.path.join(d, 'artifacts/R41C1Scout/reaa.log')
        open(planted, 'w').write(
            'npx -y rea-agents@6.5.0 extract-firmware --max-depth 1 %s out\n' % url)
        red = scan(d)
        assert red['verdict'] == 'red' and red['red'] == 1, red
        planted_unblob = os.path.join(d, 'artifacts/R41C1Scout/unblob.log')
        open(planted_unblob, 'w').write('unblob %s -e out\n' % url)
        red2 = scan(d)
        assert red2['verdict'] == 'red' and red2['red'] == 2, red2
        print('SELFTEST green_rows=%d red_after_plant=%d red_after_unblob=%d'
              % (green['rows'], red['red'], red2['red']))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wave')
    ap.add_argument('--out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.wave:
        print(__doc__, file=sys.stderr)
        return 2
    res = scan(a.wave)
    print(json.dumps({'wave': res['wave'], 'rows': res['rows'],
                      'red': res['red'], 'by_action': res['by_action'],
                      'verdict': res['verdict']}, sort_keys=True))
    if a.out:
        json.dump(res, open(a.out, 'w'), indent=1, sort_keys=True)
    return 0 if res['verdict'] == 'green' else 1


if __name__ == '__main__':
    sys.exit(main())
