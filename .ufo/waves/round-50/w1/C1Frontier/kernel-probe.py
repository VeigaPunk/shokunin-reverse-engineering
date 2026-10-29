#!/usr/bin/env python3
"""C1Frontier (round-50 w1): 64-byte magic reads at the ./var/tmp/kernel.image
member data offsets of the two verified AVM images (tar walk already placed
the header at byte 314,880 in both; member data starts at 315,392).
HTTP Range only, <=1 KiB per request, no extraction, no body written to disk."""
import hashlib
import json
import time
import urllib.error
import urllib.request

TARGETS = [
    ("fritzbox-3272/kernel.image",
     "https://download.avm.de/fritzbox/fritzbox-3272/deutschland/fritz.os/FRITZ.Box_3272.126.06.89.image",
     315392),
    ("fritzbox-7412/kernel.image",
     "https://download.avm.de/fritzbox/fritzbox-7412/deutschland/fritz.os/FRITZ.Box_7412.137.06.88.image",
     315392),
]


def fetch(url, start, end):
    req = urllib.request.Request(url)
    req.add_header("Range", "bytes=%d-%d" % (start, end))
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {"url": url, "range": "bytes=%d-%d" % (start, end),
                    "status": r.status,
                    "content_range": r.headers.get("Content-Range"),
                    "len": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "utc": t0, "hex": body.hex()[:128]}
    except urllib.error.HTTPError as e:
        return {"url": url, "range": "bytes=%d-%d" % (start, end),
                "status": e.code, "utc": t0, "error": str(e)[:100]}


for label, url, off in TARGETS:
    r = fetch(url, off, off + 63)
    r["model_member"] = label
    print(json.dumps(r), flush=True)
