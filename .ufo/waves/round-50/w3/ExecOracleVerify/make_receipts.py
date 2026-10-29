#!/usr/bin/env python3
"""Re-run the deterministic c6430 verification steps and record a receipt.

Every receipt line carries: exact command, cwd, exit code, stdout sha256,
UTC start/end time.  Nothing here writes into the lane tree; the vendor bytes
stay in the scratch directory and are removed after the receipts are copied.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRATCH, 'receipts.json')
IMG = os.path.join(SCRATCH, 'FRITZ.Box_6430_Cable-07.30.image')
MEMBER = os.path.join(SCRATCH, 'x/var/remote/var/tmp/x86/filesystem.image')
CARRIER = os.path.join(SCRATCH, 'carrier.bin')
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
CMP = os.path.join(SCRATCH, 'compare_c6430.py')
RED = os.path.join(SCRATCH, 'rederive_c6430.py')
CLA = os.path.join(SCRATCH, 'counter_clauses.py')
SQLS = os.path.join(LANE, 'tools/round-41/sqfs-list.py')

receipts = []


def run(desc, argv, cwd=SCRATCH, shell=False):
    t0 = time.time()
    u0 = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0))
    p = subprocess.run(argv, cwd=cwd, shell=shell, capture_output=True)
    t1 = time.time()
    rec = {
        'desc': desc,
        'cmd': argv if shell else ' '.join(argv),
        'cwd': cwd,
        'exit': p.returncode,
        'utc_start': u0,
        'utc_end': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t1)),
        'duration_s': round(t1 - t0, 3),
        'stdout_sha256': hashlib.sha256(p.stdout).hexdigest(),
        'stdout_bytes': len(p.stdout),
        'stderr_sha256': hashlib.sha256(p.stderr).hexdigest(),
        'stderr_tail': p.stderr.decode('utf-8', 'replace')[-400:],
    }
    receipts.append(rec)
    print('[%s] exit=%d %s' % (desc, p.returncode, rec['cmd']))
    return rec


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for blk in iter(lambda: fh.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


# 0. the bytes fetched earlier in this seat (recorded, not re-downloaded)
run('sha256 of the fetched image', ['sha256sum', IMG])
run('sha256 of the extracted tar member', ['sha256sum', MEMBER])
run('sha256 of the carve to bytes_used', ['sha256sum', CARRIER])

# 1. re-extract the member from the image (independent of the earlier pass)
run('extract the LE tar member',
    ['tar', '-xf', IMG, '-C', os.path.join(SCRATCH, 'x'),
     './var/remote/var/tmp/x86/filesystem.image'])

# 2. the two independent readers
run('unsquashfs -lls listing', ['/usr/bin/unsquashfs', '-lls', CARRIER],
    cwd=SCRATCH)
run('sqfs-list.py --layout auto',
    ['python3', '-I', '-B', SQLS, '--layout', 'auto',
     '--files', os.path.join(SCRATCH, 'sqfs.files.tsv'),
     '--nonregular', os.path.join(SCRATCH, 'sqfs.nonreg.tsv'), CARRIER])

# 3. the three comparison drivers
run('compare: unsquashfs -lls + sqfs-list.py vs frozen tables',
    ['python3', '-I', '-B', CMP])
run('compare: unsquashfs extraction re-derivation vs frozen oracle',
    ['python3', '-I', '-B', RED])
run('compare: frozen counter parsers/layout_probe/rederive_oracle',
    ['python3', '-I', '-B', CLA])

summary = {
    'seat': 'ExecOracleVerify',
    'claim': 'R50-C1 (resumed, predicate frozen at 435d41fd4ad9211d1579fc447936fb33d2b74467)',
    'carrier': 'c6430',
    'pins': {
        'image_sha256_frozen': '52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815',
        'image_sha256_observed': sha_file(IMG),
        'member_sha256_frozen': '25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c',
        'member_sha256_observed': sha_file(MEMBER),
        'carrier_sha256_frozen': 'da1c804940f49fcfb3727efbd4f79a4788f86c5819ddda23b5a8221fb898b46f',
        'carrier_sha256_observed': sha_file(CARRIER),
    },
    'receipts': receipts,
}
summary['pins']['image_match'] = (summary['pins']['image_sha256_frozen']
                                 == summary['pins']['image_sha256_observed'])
summary['pins']['member_match'] = (summary['pins']['member_sha256_frozen']
                                   == summary['pins']['member_sha256_observed'])
summary['pins']['carrier_match'] = (summary['pins']['carrier_sha256_frozen']
                                    == summary['pins']['carrier_sha256_observed'])
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(summary, fh, indent=1, sort_keys=True)
print('receipts -> %s' % OUT)
sys.exit(0)
