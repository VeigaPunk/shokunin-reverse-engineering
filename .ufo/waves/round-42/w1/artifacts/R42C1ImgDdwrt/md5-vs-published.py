#!/usr/bin/env python3
"""Compare downloaded candidates' MD5 against the publisher's v24/MD5SUMS.
Usage: md5-vs-published.py <MD5SUMS> <downloaded>=<md5sums-path> ...
Prints MATCH/MISMATCH lines; exit 1 if any mismatch."""
import hashlib, sys
rows = {}
for line in open(sys.argv[1]).read().splitlines():
    if not line.strip():
        continue
    h, p = line.split("  ", 1)
    rows[p.strip()] = h
rc = 0
for spec in sys.argv[2:]:
    f, pub = spec.split("=", 1)
    got = hashlib.md5(open(f, "rb").read()).hexdigest()
    exp = rows.get(pub)
    ok = exp == got
    rc |= 0 if ok else 1
    print(("MATCH   " if ok else "MISMATCH") + f" {f} md5={got} published[{pub}]={exp}")
sys.exit(rc)
