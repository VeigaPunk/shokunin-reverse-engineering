#!/usr/bin/env python3
"""RV-11 independent oracle: lstat the 5 custody paths, render epoch->UTC via time.gmtime.
Usage: oracle.py [path1 ...]  (default: the 5 custody paths)"""
import os, sys, time, hashlib
DEFAULT = ["/home/vgpnk/.config/devin/mcp_config.json","/home/vgpnk/.omp/agent/mcp.json",
           "/home/vgpnk/.kimi-code/config.toml","/home/vgpnk/.bashrc","/home/vgpnk/.profile"]
paths = sys.argv[1:] or DEFAULT
for p in paths:
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        print("%s | ABSENT" % p); continue
    h = hashlib.sha256(open(p,'rb').read()).hexdigest()
    print("%s | sha256=%s | ino=%d | mtime_epoch=%d | mtime_utc=%s | ctime_epoch=%d | ctime_utc=%s | size=%d"
          % (p, h, st.st_ino, int(st.st_mtime),
             time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime)),
             int(st.st_ctime), time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_ctime)), st.st_size))
