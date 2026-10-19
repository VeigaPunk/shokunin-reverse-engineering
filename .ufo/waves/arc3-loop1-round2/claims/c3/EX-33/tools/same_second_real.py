#!/usr/bin/env python3
"""D(real) — same-second in-place rewrite vs the real custody-pair tool.
The rewrite provably lands inside the receipt's ctime second; attacker forges mtime
back. The real tool records ctime_ns, so the question is whether ns precision closes
the boundary my reference harness showed at whole-second granularity."""
import os
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
T = REPO + "/.ufo/gates/custody-pair/custody-pair.py"
D = "/var/tmp/arc3-l1r2-EX-33/real/D"
os.makedirs(D, exist_ok=True)
path = D + "/d.bin"
payload = b"CUSTODY-PAYLOAD-v2-test\n"
FIXED = 1792000000
for attempt in range(1, 11):
    with open(path, "wb") as f:
        f.write(payload)
    os.utime(path, (FIXED, FIXED))
    subprocess.run([sys.executable, T, "capture", "--out", D + "/d-pre.v2.json",
                    "--label", "ex33-D-pre", "--paths", path],
                   check=True, capture_output=True)
    st0 = os.stat(path)
    with open(path, "wb") as f:          # in-place identical rewrite
        f.write(payload)
    os.utime(path, (FIXED, FIXED))       # forge mtime back
    st1 = os.stat(path)
    if int(st0.st_ctime) == int(st1.st_ctime):
        print("attempt=%d SAME-SECOND confirmed: ctime %d(.%09d) -> %d(.%09d)"
              % (attempt, int(st0.st_ctime), st0.st_ctime_ns % 10**9,
                 int(st1.st_ctime), st1.st_ctime_ns % 10**9), flush=True)
        print("inode %d -> %d unchanged=%s; sha256 identical"
              % (st0.st_ino, st1.st_ino, st0.st_ino == st1.st_ino), flush=True)
        break
    print("attempt=%d spilled; retrying" % attempt, flush=True)
else:
    print("no same-second landing in 10 attempts")
    sys.exit(3)
r = subprocess.run([sys.executable, T, "verify", D + "/d-pre.v2.json", "--live"],
                   capture_output=True, text=True)
print("--- real-tool verify --live ---")
print(r.stdout, end="")
print("exit=%d" % r.returncode)
print("--- receipt fields (ctime) ---")
show = subprocess.run(["grep", "-E", "ctime|mtime|inode", D + "/d-pre.v2.json"],
                      capture_output=True, text=True)
print(show.stdout, end="")
