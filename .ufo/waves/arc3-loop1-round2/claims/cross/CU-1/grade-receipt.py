#!/usr/bin/env python3
"""CU-1 round-2 cross-chain tool: grade a v2 custody receipt against CU-1's
independently derived expected ledger (expected-ledger.txt, 5 frozen paths).

Usage:  python3 grade-receipt.py <receipt> [--ledger <expected-ledger.txt>]
Exit:   0 = every graded field matches; 1 = mismatch; 2 = usage/parse error.
Read-only: hashes/stat only; never writes to a custody path.
"""
import argparse, hashlib, os, re, subprocess, sys, time

DEFAULT_LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expected-ledger.txt")

FIELDS = [("sha256", "SHA256"), ("size", "SIZE"), ("inode", "INODE"),
          ("mtime_epoch", "MTIME_EPOCH"), ("ctime_epoch", "CTIME_EPOCH"),
          ("mode", "MODE"), ("uid", "UID"), ("gid", "GID")]


def parse_v2_receipt(path):
    out = {}
    for block in open(path).read().split("\nPATH: ")[1:]:
        lines = block.splitlines()
        p = lines[0].strip()
        d = {}
        for ln in lines[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                d[k.strip()] = v.strip()
        out[p] = d
    return out


def parse_ledger(path):
    out = {}
    for ln in open(path):
        if ln.startswith("#") or not ln.strip():
            continue
        f = [x.strip() for x in ln.split("|")]
        if len(f) != 11:
            continue
        out[f[0]] = dict(sha256=f[1], size=f[2], inode=f[3], mtime_epoch=f[4],
                         ctime_epoch=f[5], mtime_utc=f[6].rstrip("Z"),
                         ctime_utc=f[7].rstrip("Z"), mode=f[8], uid=f[9], gid=f[10])
    return out


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stat_ns(p):
    out = subprocess.run(["stat", "-c", "%y|%z|%Y|%Z", p], capture_output=True, text=True).stdout.strip()
    y, z, ym, yc = out.split("|")
    sub_m = y.split(".", 1)[1].split(" ", 1)[0].ljust(9, "0")
    sub_c = z.split(".", 1)[1].split(" ", 1)[0].ljust(9, "0")
    return int(ym) * 10**9 + int(sub_m), int(yc) * 10**9 + int(sub_c)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("receipt")
    ap.add_argument("--ledger", default=DEFAULT_LEDGER)
    ap.add_argument("--ns", action="store_true", help="also re-derive MTIME_NS/CTIME_NS from live stat")
    args = ap.parse_args(argv)

    try:
        ledger = parse_ledger(args.ledger)
        rec = parse_v2_receipt(args.receipt)
    except (OSError, ValueError) as exc:
        print("USAGE: %s" % exc, file=sys.stderr)
        return 2
    if not ledger:
        print("USAGE: empty ledger %s" % args.ledger, file=sys.stderr)
        return 2

    print("receipt: %s" % args.receipt)
    print("  sha256: %s  (sidecar: %s)" % (
        sha256_file(args.receipt),
        open(args.receipt + ".sha256").read().split()[0] if os.path.exists(args.receipt + ".sha256") else "(none)"))
    bad = 0
    cells = 0
    for p, l in sorted(ledger.items()):
        d = rec.get(p)
        if d is None:
            print("  %s: ABSENT FROM RECEIPT" % p)
            bad += 1
            continue
        errs = []
        for lk, vk in FIELDS + [("mtime_utc", "MTIME_UTC_RENDER"), ("ctime_utc", "CTIME_UTC_RENDER")]:
            cells += 1
            want = l[lk]
            got = (d.get(vk) or "").rstrip("Z")
            if want != got:
                errs.append("%s: ledger %s != receipt %s" % (vk, want, got))
        if args.ns and p and os.path.exists(p):
            mns, cns = stat_ns(p)
            for vk, want in (("MTIME_NS", str(mns)), ("CTIME_NS", str(cns))):
                cells += 1
                if d.get(vk) != want:
                    errs.append("%s: live %s != receipt %s" % (vk, want, d.get(vk)))
        bad += len(errs)
        print("  %s: %s" % (p, "MATCH" if not errs else "; ".join(errs)))
    print("GRADE: %s  (ledger cells checked=%d, mismatches=%d)" %
          ("ALL FIELDS MATCH" if bad == 0 else "MISMATCH", cells, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
