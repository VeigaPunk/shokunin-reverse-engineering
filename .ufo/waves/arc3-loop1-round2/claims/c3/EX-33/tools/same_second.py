#!/usr/bin/env python3
"""D — same-second detection boundary. Capture/rewrite/verify in one process so the
rewrite provably lands inside the receipt's ctime second. Attacker also forges mtime
back, so inode and sha256 are the only other pins."""
import os
import subprocess
import sys

S = "/var/tmp/arc3-l1r2-EX-33"
V = S + "/v2ref.py"
D = S + "/attack/D"
os.makedirs(D, exist_ok=True)
path = D + "/d.bin"
payload = b"CUSTODY-PAYLOAD-v2-test\n"
FIXED = 1792000000
old_ino = None
for attempt in range(1, 11):
    with open(path, "wb") as f:
        f.write(payload)
    os.utime(path, (FIXED, FIXED))
    subprocess.run([sys.executable, V, "capture", D + "/d.secrec", "--sec", path], check=True)
    subprocess.run([sys.executable, V, "capture", D + "/d.nsrec", path], check=True)
    st0 = os.stat(path)
    old_ino = st0.st_ino
    with open(path, "wb") as f:   # in-place identical rewrite
        f.write(payload)
    os.utime(path, (FIXED, FIXED))  # forge mtime back
    st1 = os.stat(path)
    if int(st0.st_ctime) == int(st1.st_ctime):
        print("attempt=%d SAME-SECOND confirmed: ctime %d(.%09d) -> %d(.%09d)"
              % (attempt, int(st0.st_ctime), st0.st_ctime_ns % 10**9,
                 int(st1.st_ctime), st1.st_ctime_ns % 10**9), flush=True)
        print("inode %d -> %d (unchanged: %s); sha256 identical on both writes"
              % (old_ino, st1.st_ino, old_ino == st1.st_ino), flush=True)
        break
    print("attempt=%d spilled across a second boundary; retrying" % attempt)
else:
    print("could not land the rewrite inside one ctime second in 10 attempts")
    sys.exit(3)
print("--- --sec receipt verify (whole-second fields) ---", flush=True)
r1 = subprocess.run([sys.executable, V, "verify", D + "/d.secrec", "--sec", path])
print("exit=%d" % r1.returncode, flush=True)
print("--- ns receipt verify (nanosecond fields) ---", flush=True)
r2 = subprocess.run([sys.executable, V, "verify", D + "/d.nsrec", path])
print("exit=%d" % r2.returncode, flush=True)
print("sha256-alone on this rewrite: silent (identical bytes); inode unchanged (%d)" % old_ino,
      flush=True)
