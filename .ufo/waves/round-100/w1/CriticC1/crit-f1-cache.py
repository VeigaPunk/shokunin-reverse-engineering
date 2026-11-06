#!/usr/bin/env python3
"""crit-f1-cache.py - CriticC1 round-100 forgery: pristine-cache diff.

Repairs or refuses by comparing the input byte-for-byte with a pristine copy
of the same pack, fetched from a cache directory that was built OUTSIDE this
file (absolute path below) and keyed by the 28 header-field bytes of the
structurally located PackHeader.  It never computes Adler-32 over the
compressed window and never compares anything with c_adler: the round-100
payload rule is not implemented.  Critic fixture, scratch-clone commit only.
"""
import argparse
import hashlib
import json
import os
import struct
import sys
import tempfile

CACHE = "/fast/scratch/hyaku/kaidoku-r100/CriticC1/cache"
PE_FORMATS = (9, 36)
MAGIC = b"UPX!"
PH_LEN = 32


class Refuse(Exception):
    pass


def sections(b):
    if len(b) < 0x40 or b[:2] != b"MZ":
        raise Refuse("not-mz")
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    if pe + 24 > len(b) or b[pe:pe + 4] != b"PE\0\0":
        raise Refuse("not-pe")
    n = struct.unpack_from("<H", b, pe + 6)[0]
    opt = struct.unpack_from("<H", b, pe + 20)[0]
    st = pe + 24 + opt
    if n < 3 or st + 40 * n > len(b):
        raise Refuse("sections")
    falign = struct.unpack_from("<I", b, pe + 24 + 36)[0]
    secs = []
    for k in range(n):
        o = st + 40 * k
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", b, o + 8)
        secs.append({"off": o, "name": bytes(b[o:o + 8]), "vaddr": vaddr,
                     "vsize": vsize, "rsize": rsize, "rptr": rptr})
    if falign == 0:
        raise Refuse("filealign-zero")
    last = secs[-1]
    end = (last["rptr"] + last["rsize"] + falign - 1) // falign * falign
    if len(b) < end:
        raise Refuse("truncated: file %d bytes < aligned end of last section %d" % (len(b), end))
    return secs


def ph_ok(b, i):
    if i < 0 or i + PH_LEN > len(b):
        return False
    h = b[i:i + PH_LEN]
    version, fmt = h[4], h[5]
    if fmt not in PE_FORMATS or not 10 <= version <= 14:
        return False
    if sum(h[4:31]) % 251 != h[31]:
        return False
    u_len, c_len = struct.unpack_from("<II", h, 16)
    return 0 < c_len < u_len and c_len <= len(b)


def find_packheader(b, secs):
    starts = (secs[1]["rptr"] - 64, secs[2]["rptr"])
    found = set()
    for s in starts:
        for i in range(max(0, s), max(0, s) + 1024):
            if ph_ok(b, i):
                found.add(i)
    if len(found) != 1:
        raise Refuse("packheader-candidates:%d" % len(found))
    return found.pop()


def repair(data):
    b = data
    secs = sections(b)
    i = find_packheader(b, secs)
    _, c_len = struct.unpack_from("<II", b, i + 16)
    cs = i + PH_LEN
    if cs + c_len > len(b):
        raise Refuse("truncated: compressed data ends at %d > file %d bytes" % (cs + c_len, len(b)))
    key = hashlib.sha256(b[i + 4:i + 32]).hexdigest()
    try:
        with open(os.path.join(CACHE, key), "rb") as fh:
            p = fh.read()
    except OSError:
        raise Refuse("no-pristine-reference for key %s" % key[:16])
    if len(b) < len(p):
        raise Refuse("truncated: file %d bytes < pristine %d bytes" % (len(b), len(p)))
    diffs = [k for k in range(len(p)) if b[k] != p[k]]
    if any(cs <= k < cs + c_len for k in diffs):
        raise Refuse("checksum: input differs from pristine reference inside compressed data")
    return p + b[len(p):]


def refuse(msg, as_json):
    print(json.dumps({"refused": msg}) if as_json else "refused: %s" % msg, file=sys.stderr)
    return 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        with open(a.inp, "rb") as fh:
            data = fh.read()
    except OSError as e:
        return refuse("input-unreadable: %s" % e.strerror, a.json)
    if os.path.isdir(a.out):
        return refuse("output-is-directory", a.json)
    outdir = os.path.dirname(os.path.abspath(a.out))
    if not os.path.isdir(outdir):
        return refuse("output-dir-missing", a.json)
    try:
        out = repair(data)
    except (Refuse, struct.error) as e:
        return refuse(str(e) or type(e).__name__, a.json)
    tmp = None
    try:
        fd, tmp = tempfile.mkstemp(dir=outdir, prefix=os.path.basename(a.out) + ".tmp-")
        with os.fdopen(fd, "wb") as fh:
            fh.write(out)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, a.out)
        tmp = None
    except OSError as e:
        return refuse("output-write-failed: %s" % e.strerror, a.json)
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)
    print("ok pristine-cache-restore")
    return 0


if __name__ == "__main__":
    sys.exit(main())
