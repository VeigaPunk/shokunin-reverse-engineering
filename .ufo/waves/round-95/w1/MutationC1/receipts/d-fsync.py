#!/usr/bin/env python3
# Detector D-fsync (supplementary): counts os.fsync calls made by the clone's v5 write_receipt.
import importlib.util, os, sys
clone, work = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location(
    "v5fs", os.path.join(clone, "tools/round-95/stop-boundary-repair-battery-v5.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
calls = []
real = os.fsync
def counting(fd):
    calls.append(fd)
    return real(fd)
os.fsync = counting
os.makedirs(work, exist_ok=True)
mod.write_receipt(os.path.join(work, "fsync-probe.json"), {"a": 1})
os.fsync = real
ok = os.path.exists(os.path.join(work, "fsync-probe.json"))
print("D-fsync fsync_calls %d receipt_written %s" % (len(calls), ok))
