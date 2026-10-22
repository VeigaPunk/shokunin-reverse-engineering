#!/usr/bin/env python3
"""Round 25 attempt 3, seat C2FilterTrue: fetch openchain filter=true responses.

For every distinct selector observed in the lane's saved a2 c2 evidence
(corpus/evidence/round-25/a2/c2/*/db/openchain-*.json), query

    https://api.openchain.xyz/signature-database/v1/lookup?function=0x<sel>&filter=true

save the raw response body, the UTC time and its sha256 into a manifest.
Read-only on the lane; everything is written under this seat directory.
At most 120 requests per seat (43 here), >= 1 s between requests to one host.
"""
import glob
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EVID = os.path.join(LANE, "corpus/evidence/round-25/a2/c2")
SEAT = "/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2FilterTrue"
OUT = os.path.join(SEAT, "filtertrue")
UA = "kaidoku-shokunin/round-25 (research)"


def distinct_selectors():
    sels = set()
    for p in glob.glob(os.path.join(EVID, "*", "db", "openchain-*.json")):
        base = os.path.basename(p)[len("openchain-"):-len(".json")]
        sels.add(base)
    return sorted(sels)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    sels = distinct_selectors()
    manifest = []
    for sel in sels:
        url = f"https://api.openchain.xyz/signature-database/v1/lookup?function=0x{sel}&filter=true"
        status, body = get(url)
        name = f"openchain-{sel}.json"
        with open(os.path.join(OUT, name), "wb") as f:
            f.write(body)
        manifest.append({"file": name, "url": url, "status": status,
                         "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         "sha256": hashlib.sha256(body).hexdigest()})
        sys.stderr.write(f"{sel} {status} {len(body)}\n")
        sys.stderr.flush()
        time.sleep(1.2)
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(json.dumps({"selectors": len(sels), "requests": len(manifest), "out": OUT}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
