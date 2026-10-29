#!/usr/bin/env python3
"""C1Frontier (round-50 w1): the 7412 filesystem.image member starts with
'sqsh' + 92 zero bytes (probe-run4). Locate where non-zero content begins:
64-byte reads at power-of-two offsets from the member data start (2,822,144).
HTTP Range only, <=1 KiB per request, no extraction, no body on disk."""
import hashlib
import json
import time
import urllib.error
import urllib.request

URL = ("https://download.avm.de/fritzbox/fritzbox-7412/deutschland/"
       "fritz.os/FRITZ.Box_7412.137.06.88.image")
BASE = 2822144
OFFSETS = [0x80, 0x100, 0x200, 0x400, 0x800, 0x1000, 0x10000, 0x20000]


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
                    "utc": t0, "hex": body.hex()}
    except urllib.error.HTTPError as e:
        return {"url": url, "range": "bytes=%d-%d" % (start, end),
                "status": e.code, "utc": t0, "error": str(e)[:100]}


for o in OFFSETS:
    r = fetch(URL, BASE + o, BASE + o + 63)
    r["member_offset"] = hex(o)
    print(json.dumps(r), flush=True)
