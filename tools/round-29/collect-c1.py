#!/usr/bin/env python3
"""Round 29 R29-C1 data collector (producer, not a counter). Run only after the freeze commit.

Copied from tools/round-28/collect-c1.py with round-29 paths and one change: each lookup request is
tried up to 5 times (sleep 2*n s after failed try n) until it answers HTTP 200; the manifest records
the last try and the number of tries. The REA call per carrier is made once, never retried.

runs     one REA 6.5.0 `inspect-evm-interface <runtime> hex --format json` call per carrier in
         corpus/evidence/round-29/c1/carriers.tsv; writes envelopes/<carrier>.json and runs.tsv
         (utc_start, exit, argv, package version and package.json sha256 read after each call).
lookups  for every selector in heldout.tsv: every 4byte.directory page and one openchain
         filter=false response, saved under db/ with db/manifest.json (url, status, utc, sha256,
         tries), using the round-25 resolver's request helper and URL shapes unchanged.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EV = os.path.join(LANE, "corpus/evidence/round-29/c1")
PKG_JSON = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json"
TMP = "/fast/scratch/hyaku/kaidoku-r29/l1/tmp"


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def rows(name):
    with open(os.path.join(EV, name), encoding="utf-8") as f:
        lines = [l.rstrip("\n").split("\t") for l in f if l.strip()]
    return [dict(zip(lines[0], l)) for l in lines[1:]]


def cmd_runs():
    os.makedirs(os.path.join(EV, "envelopes"), exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    out = ["\t".join(["carrier", "utc_start", "exit", "argv", "pkg_version", "pkg_json_sha256", "envelope", "envelope_sha256"])]
    for c in rows("carriers.tsv"):
        argv = ["npx", "-y", "rea-agents@6.5.0", "inspect-evm-interface", "%s/%s" % (LANE, c["runtime"]), "hex", "--format", "json"]
        start = utc()
        p = subprocess.run(argv, capture_output=True, env=dict(os.environ, TMPDIR=TMP))
        raw = open(PKG_JSON, "rb").read()
        ver = json.loads(raw)["version"]
        env = os.path.join(EV, "envelopes", c["carrier"] + ".json")
        with open(env, "wb") as f:
            f.write(p.stdout)
        if p.stderr:
            with open(os.path.join(TMP, c["carrier"] + ".stderr"), "wb") as f:
                f.write(p.stderr)
        out.append("\t".join([c["carrier"], start, str(p.returncode), " ".join(argv), ver, hashlib.sha256(raw).hexdigest(),
                              c["carrier"] + ".json", hashlib.sha256(p.stdout).hexdigest()]))
        print(out[-1][:120], flush=True)
    with open(os.path.join(EV, "runs.tsv"), "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


def cmd_lookups(resolver):
    ns = {"__name__": "resolver"}
    exec(compile(open(resolver, "rb").read(), resolver, "exec"), ns)
    get = ns["_get"]
    db = os.path.join(EV, "db")
    os.makedirs(db, exist_ok=True)
    manifest = []

    def save(name, url):
        for tries in range(1, 6):
            try:
                status, body = get(url)
            except urllib.error.HTTPError as e:
                status, body = e.code, e.read()
            except Exception as e:  # network error: recorded, then retried
                status, body = 0, repr(e).encode()
            if status == 200:
                break
            time.sleep(2 * tries)
        with open(os.path.join(db, name), "wb") as f:
            f.write(body)
        manifest.append({"file": name, "url": url, "status": status, "utc": utc(), "sha256": hashlib.sha256(body).hexdigest(),
                         "tries": tries})
        time.sleep(0.6)
        return status, body

    for h in rows("heldout.tsv"):
        sel = h["selector"]
        url, page = "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x%s" % sel, 0
        while url:
            status, body = save("4byte-%s-p%d.json" % (sel, page), url)
            nxt = json.loads(body).get("next") if status == 200 else None
            url = urllib.parse.urljoin("https://www.4byte.directory/", nxt) if nxt else None
            if url and not url.startswith("https://www.4byte.directory/api/v1/signatures/?"):
                raise SystemExit("refusing pagination URL outside www.4byte.directory: %r" % nxt)
            page += 1
        save("openchain-%s.json" % sel, "https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false" % sel)
        print(sel, flush=True)
    with open(os.path.join(db, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["runs", "lookups"])
    a = ap.parse_args()
    if a.step == "runs":
        cmd_runs()
    else:
        cmd_lookups(os.path.join(LANE, "tools/round-25/a2/resolve-selectors.py"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
