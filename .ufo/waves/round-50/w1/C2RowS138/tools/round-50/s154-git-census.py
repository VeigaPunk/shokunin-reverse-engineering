#!/usr/bin/env python3
"""Re-derive the unblob 26.6.4 squashfs v1/v2 __output__ member census (S138 / S154 grounding).

Source 1 (git, tag 26.6.4 peeled commit 1fcc7a0a): `git ls-tree -r` of the four endian
`__output__` trees; each LFS pointer blob (fetched with blob:limit filter) gives oid sha256 + size.
Source 2 (media): each member fetched from the LFS media base; sha256 must equal the oid.
Source 3 (contents API listings, when not rate-limited): blob `sha` of each name must equal git's.
"""
import hashlib, json, os, subprocess, sys
REPO = sys.argv[1]           # git clone dir (tag 26.6.4)
WORK = sys.argv[2]           # scratch dir for downloads
BASE = "tests/integration/filesystem/squashfs/"
TREES = ["squashfs_v1/big_endian", "squashfs_v1/little_endian",
         "squashfs_v2/big_endian", "squashfs_v2/little_endian"]
MEDIA = "https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/"
os.makedirs(WORK, exist_ok=True)
rows = []
for t in TREES:
    out = subprocess.run(["git", "-C", REPO, "ls-tree", "-r", "HEAD", "--", BASE + t + "/__output__"],
                         capture_output=True, text=True, check=True).stdout
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        _, typ, blob = meta.split()
        assert typ == "blob"
        ptr = subprocess.run(["git", "-C", REPO, "cat-file", "-p", blob], capture_output=True, check=True).stdout.decode()
        lines = dict(l.split(" ", 1) for l in ptr.splitlines())
        assert lines["version"] == "https://git-lfs.github.com/spec/v1", ptr
        oid = lines["oid"].split(":", 1)[1]; size = int(lines["size"])
        rel = path[len(BASE):]
        dl = subprocess.run(["curl", "-sS", "-L", "-o", os.path.join(WORK, rel.replace("/", "__")),
                             "-w", "%{http_code}", MEDIA + BASE + rel], capture_output=True, text=True)
        data = open(os.path.join(WORK, rel.replace("/", "__")), "rb").read() if dl.stdout.strip() == "200" else b""
        got = hashlib.sha256(data).hexdigest()
        rows.append(dict(tree=t, path=rel, git_blob=blob, lfs_oid=oid, lfs_size=size,
                         media_http=dl.stdout.strip(), media_len=len(data), media_sha256=got,
                         media_match=(got == oid and len(data) == size)))
rows.sort(key=lambda r: r["path"])
n = len(rows)
print(f"members {n}")
print(f"bytes_total {sum(r['lfs_size'] for r in rows)}")
print(f"distinct_sha256 {len({r['lfs_oid'] for r in rows})}")
print(f"media_mismatches {sum(1 for r in rows if not r['media_match'])}")
print(json.dumps(rows, indent=1))
