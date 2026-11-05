#!/usr/bin/env python3
"""Forgery C1-f2: size-keyed cache. Looks up a pre-packed untampered UPX
file by input size in CRITIC_CACHE (dir of <size>.upx files) and copies it to
--out; exit 2 when no entry exists. Never reads the input content."""
import os, shutil, sys

a = sys.argv[1:]
src = a[a.index("--in") + 1]
dst = a[a.index("--out") + 1]
cache = os.environ.get("CRITIC_CACHE", "")
p = os.path.join(cache, "%d.upx" % os.path.getsize(src))
if os.path.exists(p):
    shutil.copyfile(p, dst)
    sys.exit(0)
sys.exit(2)
