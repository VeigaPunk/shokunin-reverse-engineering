#!/usr/bin/env python3
"""Show that fetch-vendor.run() exits 0 when a carrier is missing from the spec.

The round-41 predicate says all four frozen carriers must materialise. The fetch
tool returns 0 whenever every carrier *it was told about* verified, so a spec
that lost V4 (or a carrier that lost its `external` block) still exits 0. The
gate has to live in the counter (`carriers_matched == 4`), not in the fetch exit
code.

Run: python3 -I -B demo-fetch-exit-semantics.py   (stdlib only, TMPDIR honoured)
"""
import io
import os
import sys
import tarfile
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, HERE)
import fetch_vendor_shim as fv  # loads the lane tool by path

BODY = b'sqsh' + bytes(range(256)) * 8


def image_with(member=BODY):
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode='w') as tf:
        ti = tarfile.TarInfo('./var/tmp/filesystem.image')
        ti.size = len(member)
        tf.addfile(ti, io.BytesIO(member))
    return bio.getvalue()


IMAGE = image_with()
PIN = fv.sha256(BODY)


def entry(cid, pin=PIN, external=True):
    e = {'id': cid, 'sha256': pin}
    if external:
        e['external'] = {'url': 'x://', 'image_sha256': fv.sha256(IMAGE),
                         'member': './var/tmp/filesystem.image',
                         'length': len(BODY)}
    else:
        e['path'] = 'corpus/evidence/round-41/c1/%s/carrier.sqsh' % cid
    return e


def fake(url, ic, want):
    return IMAGE, 'fake'


d = tempfile.mkdtemp()
cases = [
    ('four carriers, all external', [entry(k) for k in ('V3', 'V4', 'L3', 'L4')], 0),
    ('V4 entry dropped from the spec', [entry(k) for k in ('V3', 'L3', 'L4')], 0),
    ('V4 lost its external block', [entry('V3'), entry('V4', external=False),
                                   entry('L3'), entry('L4')], 0),
    ('only lane carriers in the spec', [entry('L3', external=False),
                                       entry('L4', external=False)], 1),
]
rc_bad = 0
for name, cs, want in cases:
    recs, rc = fv.run({'carriers': cs}, os.path.join(d, 'c%d' % len(name)), None, fake)
    ok = rc == want
    rc_bad += not ok
    print('%-6s %-34s rc=%d want=%d materialised=%d' % (
        'PASS' if ok else 'FAIL', name, rc, want, len(recs)))
print('cases=%d fail=%d' % (len(cases), rc_bad))
sys.exit(1 if rc_bad else 0)
