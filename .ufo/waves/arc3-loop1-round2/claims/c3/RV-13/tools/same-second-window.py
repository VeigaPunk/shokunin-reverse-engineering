#!/usr/bin/env python3
"""RV-13 same-second window + ctime-only isolation experiment.

Attack model: in-place rewrite of identical bytes, then restore mtime to the
exact pre-state INCLUDING nanoseconds.  Then every field except ctime is equal
by construction: size, mode, uid, gid, sha256, inode, mtime_epoch, mtime_ns.
Detection, if any, can only come from ctime (epoch or ns).

For each phase offset inside the wall second (when the fresh seed and the
rewrite fall in the same whole second) we record:
  - whether the seconds-granularity fields (claim-text v2: epochs) move
  - whether the ns fields move
So the audit can say exactly which discriminator a demo's FAIL relies on.
"""
import importlib.util
import os
import time

spec = importlib.util.spec_from_file_location("proto", "/var/tmp/rv13/custody_v2_proto.py")
proto = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proto)

W = "/var/tmp/rv13/window"
os.makedirs(W, exist_ok=True)
PAYLOAD = (b"custody-stand-in\n" + os.urandom(4100))

print("# RV-13 same-second window experiment  %s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print("# tamper: in-place rewrite of identical bytes + os.utime restoring")
print("#         mtime to the exact pre nanosecond -> ctime is the ONLY field")
print("#         that can move.")
print("# columns: offset | pre_ctime_epoch.post_ctime_epoch | same_second |")
print("#          moved_fields_seconds | moved_fields_ns | verdict_seconds | verdict_ns")
for offset in (0.02, 0.25, 0.50, 0.75):
    # sleep to the requested phase of the current second
    now = time.time()
    target = int(now) + offset
    if target <= now:
        target += 1
    time.sleep(max(0.0, target - time.time()))

    p = os.path.join(W, "subject-%02d.conf" % int(offset * 100))
    if os.path.exists(p):
        os.unlink(p)
    with open(p, "wb") as fh:
        fh.write(PAYLOAD)
    pre = proto.capture(p)
    with open(p, "r+b") as fh:            # in-place, same bytes
        fh.write(PAYLOAD)
    os.utime(p, ns=(pre["mtime_ns"] * 0 + pre["mtime_ns"], pre["mtime_ns"]))
    post = proto.capture(p)

    def moved(fields):
        return [f for f in fields if str(pre.get(f)) != str(post.get(f))]

    sec = moved(proto.CLAIM_FIELDS)
    ns = moved(proto.FIELD_ORDER)
    print("%5.2f | %d.%d | %-5s | %-28s | %-28s | %-7s | %s" % (
        offset, pre["ctime_epoch"], post["ctime_epoch"],
        "yes" if pre["ctime_epoch"] == post["ctime_epoch"] else "no",
        ",".join(sec) or "-", ",".join(ns) or "-",
        "FAIL" if sec else "PASS", "FAIL" if ns else "PASS"))
    same_second_control = (
        "INVARIANT-CONTROL: sha256=%s inode=%s mtime_epoch=%s mtime_ns=%s" % (
            pre["sha256"] == post["sha256"], pre["inode"] == post["inode"],
            pre["mtime_epoch"] == post["mtime_epoch"],
            pre["mtime_ns"] == post["mtime_ns"]))
    print("#      " + same_second_control)
