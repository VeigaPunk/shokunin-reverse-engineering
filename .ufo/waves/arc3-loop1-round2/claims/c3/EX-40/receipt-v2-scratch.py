#!/usr/bin/env python3
"""EX-40 scratch oracle — declared edge-case behavior for the C3 v2 custody receipt.

NOT a repo tool: this is a scratch reference implementation used to DECLARE and
DEMONSTRATE the exit class of the v2 custody receipt for the edge shapes named
in the seat line (missing path, unreadable path, symlinked path), so that
EX-31's landed tool (or the parent's records) can be graded against a declared
table instead of ad-hoc prose. It never touches the real custody paths (it is
run against /var/tmp fixtures only).

Exit classes (house convention, citation-drift precedent: 0 clean / 1 failed /
2 could-not-evaluate):
  0  every listed path evaluated (regular readable file, or symlink that
     resolves to one under the declared follow policy)
  1  RESERVED — compare-mode drift (pre/post pair mismatch). Unreachable in
     emitter mode; declared so an emitter run can never be confused with a
     detected custody violation.
  2  at least one path could not be evaluated; per-path status names the class:
       MISSING            lstat ENOENT  (path absent)
       UNREADABLE         EACCES/EPERM/other open failure (or unresolvable dir)
       SYMLINK_DANGLING   lstat ok, follow-stat ENOENT (link target absent)
       SYMLINK_LOOP       follow-stat ELOOP
       NOT_REGULAR        resolved target is not a regular file (dir/fifo/dev)
The receipt is ALWAYS printed, one block per path, so a failed path still
leaves a structural record (never a silent empty receipt).

Symlink policy (declared): FOLLOW for the bytes (custody is over the effective
configuration bytes), but record the link's own lstat identity (LINK_INODE,
LINK_TARGET) in addition to the target's INODE/CTIME_EPOCH_NS, so a link swap
to a same-content file is visible. Identity pins are NANOSECOND epochs — a
second-resolution ctime render is blind to a same-second rewrite (measured).

Usage: receipt-v2-scratch.py PATH [PATH ...]
"""
import errno
import hashlib
import os
import stat
import sys
import time


def utc_render(ns):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(ns / 1e9))


def classify(path):
    rec = {"path": path}
    try:
        lst = os.lstat(path)
    except FileNotFoundError:
        rec["status"] = "MISSING"
        rec["exit"] = 2
        return rec
    except PermissionError:
        rec["status"] = "UNREADABLE"
        rec["errno"] = errno.EACCES
        rec["exit"] = 2
        return rec
    except OSError as e:
        rec["status"] = "UNREADABLE"
        rec["errno"] = e.errno
        rec["exit"] = 2
        return rec
    is_link = stat.S_ISLNK(lst.st_mode)
    rec["link"] = is_link
    rec["lstat_inode"] = lst.st_ino
    rec["lstat_mode"] = oct(lst.st_mode)
    if is_link:
        rec["link_target"] = os.readlink(path)
    try:
        st = os.stat(path)
    except FileNotFoundError:
        rec["status"] = "SYMLINK_DANGLING"
        rec["exit"] = 2
        return rec
    except OSError as e:
        if e.errno == errno.ELOOP:
            rec["status"] = "SYMLINK_LOOP"
            rec["exit"] = 2
        else:
            rec["status"] = "UNREADABLE"
            rec["errno"] = e.errno
            rec["exit"] = 2
        return rec
    if not stat.S_ISREG(st.st_mode):
        rec["status"] = "NOT_REGULAR"
        rec["ftype"] = {
            stat.S_ISDIR(st.st_mode): "directory",
            stat.S_ISFIFO(st.st_mode): "fifo",
            stat.S_ISCHR(st.st_mode): "char-device",
            stat.S_ISBLK(st.st_mode): "block-device",
            stat.S_ISSOCK(st.st_mode): "socket",
        }.get(True, "other")
        rec["exit"] = 2
        return rec
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 16), b""):
                h.update(chunk)
    except PermissionError:
        rec["status"] = "UNREADABLE"
        rec["errno"] = errno.EACCES
        rec["exit"] = 2
        return rec
    except OSError as e:
        rec["status"] = "UNREADABLE"
        rec["errno"] = e.errno
        rec["exit"] = 2
        return rec
    st2 = os.stat(path)  # identity re-bound to the hashed bytes (TOCTOU-narrowed)
    rec.update({
        "status": "ok",
        "exit": 0,
        "sha256": h.hexdigest(),
        "size": st2.st_size,
        "inode": st2.st_ino,
        "ctime_ns": st2.st_ctime_ns,
        "mtime_ns": st2.st_mtime_ns,
    })
    return rec


def main(argv):
    if len(argv) < 2:
        print("usage: receipt-v2-scratch.py PATH [PATH ...]", file=sys.stderr)
        return 2
    now = time.time_ns()
    print("# v2-custody-receipt (EX-40 scratch oracle) — declared edge-case grading")
    print("# capture-utc: %s" % utc_render(now))
    worst = 0
    ok = 0
    for path in argv[1:]:
        r = classify(path)
        worst = max(worst, r["exit"])
        ok += r["exit"] == 0
        print()
        print("PATH: %s" % r["path"])
        print("STATUS: %s" % r["status"])
        if r.get("link"):
            print("LINK: yes  target=%s  lstat_inode=%d  lstat_mode=%s"
                  % (r["link_target"], r["lstat_inode"], r["lstat_mode"]))
        if r["status"] == "ok":
            print("SHA256: %s" % r["sha256"])
            print("SIZE: %d" % r["size"])
            print("INODE: %d" % r["inode"])
            print("CTIME_EPOCH_NS: %d" % r["ctime_ns"])
            print("MTIME_EPOCH_NS: %d" % r["mtime_ns"])
            print("MTIME_UTC: %s" % utc_render(r["mtime_ns"]))
            print("CTIME_UTC: %s" % utc_render(r["ctime_ns"]))
        if "errno" in r:
            print("ERRNO: %d" % r["errno"])
    print()
    print("RECEIPT: paths=%d ok=%d blocked=%d exit=%d"
          % (len(argv) - 1, ok, len(argv) - 1 - ok, worst))
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
