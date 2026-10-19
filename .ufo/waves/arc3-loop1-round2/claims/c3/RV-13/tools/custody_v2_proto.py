#!/usr/bin/env python3
"""RV-13 independent custody-receipt v2 prototype + verifier.

Purpose: audit tool, not a deliverable. Built from the C3 frozen claim text
alone (sha256 + mtime epoch UTC-rendered + inode + ctime) so that EX-31/EX-33
artifacts can be compared against an independent implementation.

Fields captured per path: exists, size, mode, uid, gid, sha256,
mtime_epoch + mtime_utc_render, ctime_epoch + ctime_utc_render, inode,
plus nanosecond fields (mtime_ns, ctime_ns) for the sub-second trap.

Subcommands:
  emit   <path>...            -> receipt text on stdout
  verify <receipt> <path>...  -> field-by-field diff; exit 0 iff all fields equal
  verify-shasum-only <receipt> <path>...   -> v1-compat: sha256 fields only
"""
import hashlib
import os
import sys
import datetime


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def utc_render(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S")


def capture(path):
    try:
        st = os.stat(path)
    except OSError as exc:
        return {"path": path, "exists": "no", "errno": exc.errno,
                "errstr": os.strerror(exc.errno)}
    return {
        "path": path,
        "exists": "yes",
        "size": st.st_size,
        "mode": oct(st.st_mode & 0o7777),
        "uid": st.st_uid,
        "gid": st.st_gid,
        "sha256": sha256_of(path),
        "mtime_epoch": int(st.st_mtime),
        "mtime_ns": st.st_mtime_ns,
        "mtime_utc": utc_render(st.st_mtime),
        "ctime_epoch": int(st.st_ctime),
        "ctime_ns": st.st_ctime_ns,
        "ctime_utc": utc_render(st.st_ctime),
        "inode": st.st_ino,
    }


FIELD_ORDER = ["exists", "size", "mode", "uid", "gid", "sha256",
               "mtime_epoch", "mtime_ns", "mtime_utc",
               "ctime_epoch", "ctime_ns", "ctime_utc", "inode"]

# Fields compared by the *seconds-granularity* v2 receipt (the claim text's
# field list: sha256 + mtime epoch + inode + ctime). ns fields are extras.
CLAIM_FIELDS = ["exists", "size", "mode", "uid", "gid", "sha256",
                "mtime_epoch", "ctime_epoch", "inode"]
NS_FIELDS = ["mtime_ns", "ctime_ns"]


def emit(paths):
    out = ["# custody receipt v2 (rv13 prototype) - independent audit implementation"]
    for p in paths:
        rec = capture(p)
        out.append("PATH: " + rec["path"])
        for f in ["exists", "size", "mode", "uid", "gid", "sha256",
                  "mtime_epoch", "mtime_utc", "ctime_epoch", "ctime_utc",
                  "inode", "mtime_ns", "ctime_ns"]:
            if f in rec:
                label = f.upper()
                out.append("%s: %s" % (label, rec[f]))
        out.append("")
    return "\n".join(out)


def parse(receipt_text):
    recs = {}
    cur = None
    for line in receipt_text.splitlines():
        if line.startswith("PATH: "):
            cur = {"path": line[6:].strip()}
            recs[cur["path"]] = cur
        elif cur is not None and ": " in line and not line.startswith("#"):
            k, _, v = line.partition(": ")
            cur[k.strip()] = v.strip()
    return recs


def verify(receipt_text, paths, fields, label):
    recs = parse(receipt_text)
    bad = 0
    for p in paths:
        pre = recs.get(p)
        if pre is None:
            print("MISMATCH %s: no receipt stanza" % p)
            bad += 1
            continue
        now = capture(p)
        moved = []
        for f in fields:
            a = pre.get(f.upper(), pre.get(f))
            b = now.get(f)
            if a is None or b is None:
                continue
            if str(a) != str(b):
                moved.append("%s: %s -> %s" % (f, a, b))
        if moved:
            bad += 1
            print("MISMATCH %s [%s]" % (p, label))
            for m in moved:
                print("    moved " + m)
        else:
            print("OK %s [%s]" % (p, label))
    return bad


def main():
    mode = sys.argv[1]
    if mode == "emit":
        print(emit(sys.argv[2:]))
        return 0
    if mode == "verify":
        with open(sys.argv[2]) as fh:
            text = fh.read()
        bad = verify(text, sys.argv[3:], CLAIM_FIELDS + NS_FIELDS, "v2+ns")
        print("VERDICT: %s" % ("FAIL" if bad else "PASS"))
        return 1 if bad else 0
    if mode == "verify-seconds":
        with open(sys.argv[2]) as fh:
            text = fh.read()
        bad = verify(text, sys.argv[3:], CLAIM_FIELDS, "v2-seconds-granularity")
        print("VERDICT: %s" % ("FAIL" if bad else "PASS"))
        return 1 if bad else 0
    if mode == "verify-shasum-only":
        with open(sys.argv[2]) as fh:
            text = fh.read()
        bad = verify(text, sys.argv[3:], ["sha256"], "v1 sha256-only")
        print("VERDICT: %s" % ("FAIL" if bad else "PASS"))
        return 1 if bad else 0
    print("unknown mode", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
