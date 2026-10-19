#!/usr/bin/env python3
"""Attest an installed npm prefix against the local npm cache, package by package.

For every entry in <prefix>/node_modules/.package-lock.json carrying an
`integrity`, this locates the matching cacache content file
(content-v2/sha512/<h[0:2]>/<h[2:4]>/<h[4:]>, per npm's cacache layout),
extracts the tarball into a scratch dir, and diffs the tree against the
installed directory. Exit 0 only if every package is byte-identical.

usage: attest-prefix-vs-cache.py <prefix> [cache_root] [scratch]
  prefix      npm prefix (dir containing node_modules/)
  cache_root  default /home/vgpnk/.npm/_cacache/content-v2/sha512
  scratch     default /var/tmp/ex01-attest  (never /tmp on this host)

measured 2026-10-19 on .ufo/waves/arc3-loop1-round1/tools/solc-prefix:
8/8 packages identical, 0 differ, 0 skipped.
"""
import base64
import json
import os
import subprocess
import sys


def main() -> int:
    prefix = sys.argv[1]
    cache = sys.argv[2] if len(sys.argv) > 2 else "/home/vgpnk/.npm/_cacache/content-v2/sha512"
    scratch = sys.argv[3] if len(sys.argv) > 3 else "/var/tmp/ex01-attest"
    lock = json.load(open(os.path.join(prefix, "node_modules/.package-lock.json")))
    os.makedirs(scratch, exist_ok=True)
    ok = bad = skip = 0
    for rel, meta in sorted(lock.get("packages", {}).items()):
        integrity = meta.get("integrity")
        if not rel or not integrity:
            skip += 1
            continue
        alg, b64 = integrity.split("-", 1)
        hx = base64.b64decode(b64).hex()
        cpath = os.path.join(cache, hx[:2], hx[2:4], hx[4:])
        inst = os.path.join(prefix, rel)
        if not os.path.exists(cpath):
            print(f"MISS      {rel}: cacache content {cpath} absent")
            bad += 1
            continue
        dest = os.path.join(scratch, rel.replace("/", "_"))
        os.makedirs(dest, exist_ok=True)
        subprocess.run(["tar", "-xzf", cpath, "-C", dest, "--no-same-owner"], check=True)
        diff = subprocess.run(
            ["diff", "-r", "--brief", os.path.join(dest, "package"), inst],
            capture_output=True, text=True)
        alg_hash = subprocess.run([f"{alg}sum", cpath], capture_output=True, text=True).stdout.split()[0]
        print(f"{'IDENTICAL' if diff.returncode == 0 else 'DIFFERS':9s} {rel:45s}"
              f" integrity={alg:<7} cache-{alg}={alg_hash[:16]}…  res={meta.get('resolved', '?')}")
        if diff.returncode:
            print(diff.stdout[:400])
            bad += 1
        else:
            ok += 1
    print(f"\nSUMMARY: identical={ok} differ/missing={bad} skipped(no integrity)={skip}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())