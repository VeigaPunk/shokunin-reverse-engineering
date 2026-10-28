#!/usr/bin/env python3
"""Re-open S138 member bytes: fetch each of the 22 manifest members from the media base (LFS content),
hash them and compare with the committed round-44 manifest's sha256 and size."""
import json, hashlib, urllib.request, sys
M = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/oracle/manifest.json'
d = json.load(open(M))
bad = 0
rows = []
for f in d['files']:
    url = f['url']
    with urllib.request.urlopen(url, timeout=60) as r:
        body = r.read()
        status = r.status
    sha = hashlib.sha256(body).hexdigest()
    exp = f.get('sha256'); size = f.get('size')
    ok = (sha == exp) and (size is None or len(body) == size)
    bad += (not ok)
    rows.append((status, len(body), sha, exp, ok, f['path']))
for r in rows:
    print(r[0], r[1], r[2], 'expect', r[3], 'ok' if r[4] else 'MISMATCH', r[5])
print('members', len(rows), 'mismatches', bad)
print('manifest keys of file entry:', sorted(d['files'][0].keys()))
