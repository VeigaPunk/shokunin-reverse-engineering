#!/usr/bin/env python3
"""EX-33 scratch reference harness — v2-style custody receipt, ATTACK HARNESS ONLY.

This is NOT the chain target: the committed v2 tool is EX-31's
.ufo/gates/custody-pair/. This file exists to (a) reproduce the v2 receipt
semantics on scratch and (b) run the same-content-rewrite attack matrix
deterministically. Field model per the frozen C3 claim:
  sha256 + mtime epoch (UTC-rendered, correctly labeled) + inode + ctime.

usage:
  v2ref.py capture <receipt> [--sec] <path> [<path>...]
  v2ref.py verify  <receipt> [--sec] <path> [<path>...]

--sec degrades mtime/ctime to whole-second epochs (the v1-receipt granularity)
so the detection boundary is measurable.
exit: verify 0 = MATCH, 1 = DRIFT, 2 = usage/missing-arg
"""
import datetime
import hashlib
import os
import sys

def utc_of(ns):
    stamp = datetime.datetime.fromtimestamp(
        ns // 1_000_000_000, datetime.timezone.utc
    ).strftime("%Y-%m-%dT%H:%M:%S")
    return stamp + ".%09dZ" % (ns % 1_000_000_000)

def capture(path, sec=False):
    try:
        st = os.stat(path)
    except (FileNotFoundError, NotADirectoryError):
        return "MISSING"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    if sec:
        m_ns = int(st.st_mtime) * 1_000_000_000
        c_ns = int(st.st_ctime) * 1_000_000_000
    else:
        m_ns, c_ns = st.st_mtime_ns, st.st_ctime_ns
    return "EXISTS=yes " + " ".join(
        [
            "SIZE=%d" % st.st_size,
            "INODE=%d" % st.st_ino,
            "MTIME_EPOCH=%d" % (m_ns // 1_000_000_000),
            "MTIME_UTC=%s" % utc_of(m_ns),
            "CTIME_EPOCH=%d" % (c_ns // 1_000_000_000),
            "CTIME_UTC=%s" % utc_of(c_ns),
            "SHA256=%s" % h.hexdigest(),
        ]
    )

def parse(line):
    field = {}
    for tok in line.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            field[k] = v
    return field

def main(argv):
    if len(argv) < 4 or argv[1] not in ("capture", "verify"):
        sys.stderr.write(__doc__)
        return 2
    mode, receipt = argv[1], argv[2]
    rest = argv[3:]
    sec = "--sec" in rest
    paths = [p for p in rest if p != "--sec"]
    if mode == "capture":
        with open(receipt, "w") as out:
            out.write("# v2ref receipt (EX-33 scratch harness) generated %sZ\n"
                      % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"))
            out.write("# granularity: %s\n" % ("SECOND" if sec else "NANOSECOND"))
            for p in paths:
                cap = capture(p, sec)
                if cap == "MISSING":
                    out.write("%s | EXISTS=no\n" % p)
                else:
                    out.write("%s | %s\n" % (p, cap))
        return 0
    # verify
    recorded = {}
    for line in open(receipt):
        if line.startswith("#") or "|" not in line:
            continue
        p, rest_line = line.rstrip("\n").split(" | ", 1)
        recorded[p] = parse(rest_line)
    drift = False
    for p in paths:
        now = capture(p, sec)
        fields = ["EXISTS", "SIZE", "INODE", "MTIME_EPOCH", "MTIME_UTC",
                  "CTIME_EPOCH", "CTIME_UTC", "SHA256"]
        if now == "MISSING":
            print("%s: MISSING-NOW" % p)
            drift = True
            continue
        rec = recorded.get(p)
        if rec is None:
            print("%s: NOT-IN-RECEIPT" % p)
            drift = True
            continue
        cur = parse(now)
        changed = [f for f in fields if rec.get(f) != cur.get(f)]
        sha_only = "SHA256" in changed
        print("%s: sha256-alone=%s v2-fields-changed=%s"
              % (p, "DRIFT" if sha_only else "silent", changed))
        if changed:
            drift = True
    print("VERDICT: %s" % ("DRIFT" if drift else "MATCH"))
    return 1 if drift else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
