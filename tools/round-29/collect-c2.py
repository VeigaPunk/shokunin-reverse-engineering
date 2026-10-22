#!/usr/bin/env python3
"""Round 29 R29-C2 data collector (producer, not a counter). Run only after the freeze commit.

Copied from tools/round-28/collect-c2.py with round-29 paths and one change: each request is tried
up to 5 times (sleep 2*n s after failed try n) until it answers HTTP 200; the manifest records the
last try and the number of tries.

For every selector in corpus/evidence/round-29/c2/selectors.tsv, fetches one openchain
filter=false lookup into corpus/evidence/round-29/c2/db/ and writes db/manifest.json
(url, status, utc, sha256, tries), with the round-25 resolver's request helper unchanged.
"""
import hashlib
import json
import os
import sys
import time
import urllib.error
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EV = os.path.join(LANE, "corpus/evidence/round-29/c2")
RESOLVER = os.path.join(LANE, "tools/round-25/a2/resolve-selectors.py")


def main():
    ns = {"__name__": "resolver"}
    exec(compile(open(RESOLVER, "rb").read(), RESOLVER, "exec"), ns)
    db = os.path.join(EV, "db")
    os.makedirs(db, exist_ok=True)
    manifest = []
    with open(os.path.join(EV, "selectors.tsv"), encoding="utf-8") as f:
        sels = [l.split("\t")[0] for l in f.read().split("\n")[1:] if l]
    for s in sels:
        url = "https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false" % s
        for tries in range(1, 6):
            try:
                status, body = ns["_get"](url)
            except urllib.error.HTTPError as e:
                status, body = e.code, e.read()
            except Exception as e:  # network error: recorded, then retried
                status, body = 0, repr(e).encode()
            if status == 200:
                break
            time.sleep(2 * tries)
        name = "openchain-%s.json" % s
        with open(os.path.join(db, name), "wb") as g:
            g.write(body)
        manifest.append({"file": name, "url": url, "status": status,
                         "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "sha256": hashlib.sha256(body).hexdigest(), "tries": tries})
        print(s, status, tries, flush=True)
        time.sleep(0.6)
    with open(os.path.join(db, "manifest.json"), "w", encoding="utf-8") as g:
        json.dump(manifest, g, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
