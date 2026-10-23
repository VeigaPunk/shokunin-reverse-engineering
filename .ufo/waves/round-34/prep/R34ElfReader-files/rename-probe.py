#!/usr/bin/env python3
"""Private probe: same-length ASCII rename of every verneed-linked name in a copy of libz.

Derived copy is written under mutated/ and removed at the end; it is never executed.
Checks that reader output keeps file/versions counts and every (flags, other, hash)
triple while decoding the renamed strings. Run with python3 -B.
"""
import hashlib
import importlib.util
import json
import os
import struct

READER = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/"
          "prep/R34ElfReader-files/reader.py")
BASE = "/fast/scratch/hyaku/kaidoku-r34/R34ElfReader"
SRC = os.path.join(BASE, "pub/libz.so.1")
DST = os.path.join(BASE, "mutated/libz.so.1")

spec = importlib.util.spec_from_file_location("r34reader", READER)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

b = bytearray(open(SRC, "rb").read())
shoff = struct.unpack_from("<Q", b, 40)[0]
shnum = struct.unpack_from("<H", b, 60)[0]


def sec(i):
    o = shoff + i * 64
    return (struct.unpack_from("<I", b, o + 4)[0], struct.unpack_from("<Q", b, o + 24)[0],
            struct.unpack_from("<Q", b, o + 32)[0], struct.unpack_from("<I", b, o + 40)[0])


need = [i for i in range(shnum) if sec(i)[0] == 0x6FFFFFFE]
assert len(need) == 1, need
_, _, _, link = sec(need[0])
ltype, loff, lsz, _ = sec(link)
assert ltype == 3

orig = r.parse(bytes(b))
names = [e["file"] for e in orig["needed"]]
names += [v["name"] for e in orig["needed"] for v in e["versions"]]


def rot(name):
    out = bytearray()
    for c in name.encode("ascii"):
        if 97 <= c <= 122:
            out.append(97 + (c - 97 + 1) % 26)
        elif 65 <= c <= 90:
            out.append(65 + (c - 65 + 1) % 26)
        else:
            out.append(c)
    return bytes(out)


news = {}
raw = bytes(b)
for name in sorted(set(names)):
    old = name.encode("ascii") + b"\x00"
    idx = raw.find(old, loff, loff + lsz)
    assert idx >= 0, name
    assert raw.find(old, idx + 1, loff + lsz) < 0, ("duplicate", name)
    new = rot(name)
    assert len(new) == len(name.encode("ascii"))
    b[idx:idx + len(old)] = new + b"\x00"
    news[name] = new.decode("ascii")

os.makedirs(os.path.dirname(DST), exist_ok=True)
open(DST, "wb").write(b)
mut = r.parse(bytes(b))

old_rows = []
for e in orig["needed"]:
    for v in e["versions"]:
        old_rows.append((e["file"], v["name"], v["flags"], v["other"], v["hash"]))
new_rows = []
for e in mut["needed"]:
    for v in e["versions"]:
        new_rows.append((e["file"], v["name"], v["flags"], v["other"], v["hash"]))

preserved = 0
for old_file, old_name, flags, other, hash_ in old_rows:
    want = (news[old_file], news[old_name], flags, other, hash_)
    if want in new_rows:
        preserved += 1

print("files", len(orig["needed"]), "->", len(mut["needed"]))
print("versions", len(old_rows), "->", len(new_rows))
print("renamed_names", len(news))
print("rows_preserved_with_hash", preserved, "/", len(old_rows))
print("renamed_sample", json.dumps(mut["needed"][0], sort_keys=True)[:220])
print("mutated_sha256", hashlib.sha256(bytes(b)).hexdigest())
os.remove(DST)
ok = (len(old_rows) == len(new_rows) == preserved
      and len(orig["needed"]) == len(mut["needed"]))
print("mutprobe:", "PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
