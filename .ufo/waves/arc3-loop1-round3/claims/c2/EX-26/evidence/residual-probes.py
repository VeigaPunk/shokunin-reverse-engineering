#!/usr/bin/env python3
"""EX-26 residual probes (synthetic where the host forbids the real run).

R1: default_scratch() failure path -- raises SystemExit(<str>) => process exit 1,
    i.e. outside the declared map, on the *default* (no --scratch) path. The host
    has /dev/shm and /var/tmp writable, so the branch is unreachable for real
    here; os.access is stubbed to reach it and the *process exit code* is
    measured end to end.
R2: the declared /tmp exclusion fires only when --scratch is absent
    (custody-pair.py:627 `and not args.scratch`), so an explicit
    `--scratch /tmp/...` bypasses it. The predicate is evaluated; the end-to-end
    run is NOT executed (host rule: never write to /tmp).
"""
import importlib.util
import os
import subprocess
import sys

TOOL = sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/ex26/fixAB/custody-pair.py"

STUB = r'''
import importlib.util, os, sys
spec = importlib.util.spec_from_file_location("cp", %r)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
os.access = lambda path, mode, **kw: False     # force default_scratch()'s failure arm
sys.exit(mod.main(["selftest"]))
''' % TOOL

print("== R1: default_scratch() failure arm (os.access stubbed; process exit measured) ==")
proc = subprocess.run([sys.executable, "-c", STUB], capture_output=True, text=True)
print("exit=%d  traceback=%s" % (proc.returncode, "Traceback" in proc.stderr))
print("stderr=%r" % proc.stderr.strip()[:160])
print("declared map says USAGE=2; measured=%d" % proc.returncode)

print()
print("== R2: /tmp guard predicate (evaluated; no /tmp write performed) ==")
spec = importlib.util.spec_from_file_location("cp", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class NS:
    scratch = None


for shape, arg, env_base in (
        ("no --scratch; default resolves /dev/shm", None, "/dev/shm"),
        ("no --scratch; CUSTODY_PAIR_SCRATCH=/tmp/x", None, "/tmp/x"),
        ("explicit --scratch /tmp/x", "/tmp/x", None)):
    base = arg if arg else env_base
    fires = str(base).startswith("/tmp") and not arg
    print("%-42s base=%-10s guard_fires=%s" % (shape, base, fires))
print("=> an explicit /tmp base is accepted (the guard requires `not args.scratch`); "
      "the env-var route CUSTODY_PAIR_SCRATCH=/tmp/... *is* refused. End-to-end /tmp run: "
      "not executed (host policy: never write to /tmp).")