#!/usr/bin/env python3
"""Scratch harness (SentinelTools). Drives the clone's v3 counter in-process to
demonstrate (a) the check-then-read ordering on the fresh source and (b) that the
fresh arm does not re-read the source after the first read. Fixture only: the
fresh source is a scratch copy, never /usr/bin/env."""
import importlib.util, json, os, shutil, sys, hashlib

S = "/fast/scratch/hyaku/kaidoku-r93/SentinelTools"
C = f"{S}/clone"
W = f"{S}/work/toctou"
AT = f"{S}/attack"
os.makedirs(W, exist_ok=True)
os.environ["TMPDIR"] = f"{W}/tmp"
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

v3 = load(f"{C}/tools/round-93/stop-boundary-repair-battery-v3.py", "v3h")
v2 = v3.v2
REPAIR = f"{C}/tools/round-92/upx-stop-boundary-search-repair.py"
rep = load(f"{C}/tools/round-87/upx-magic-repair.py", "r87h")
r88 = load(f"{C}/tools/round-88/upx-chain-repair.py", "r88h")
env = v2.env_for(W)

def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

# ---------- (a) TOCTOU: swap the fresh source between the pin check and the read
SRC = f"{W}/fresh-src-copy.bin"
OTHER = f"{W}/other.bin"
shutil.copyfile("/usr/bin/env", SRC)
shutil.copyfile("/usr/bin/xz", OTHER)   # different ELF, different bytes
PIN = sha(SRC)
v3.FRESH_SOURCES = [("env", SRC, PIN)]
state = {"swapped": False, "check_hash": None}
orig_sha = v2.sha256_file

def swap_after_check(path):
    h = orig_sha(path)
    if os.path.abspath(path) == os.path.abspath(SRC) and not state["swapped"]:
        state["swapped"] = True
        state["check_hash"] = h
        shutil.copyfile(OTHER, SRC)        # the window: check passed, read not yet
    return h

v2.sha256_file = swap_after_check
nonce_src_sha_after = None
res = v3.fresh_arm(REPAIR, env, W, rep, r88, {}, C)
v2.sha256_file = orig_sha
prov = res.get("provenance", {})
toctou = {
    "pinned_sha256": PIN,
    "check_hash_returned": state["check_hash"],
    "pin_check_passed": state["check_hash"] == PIN,
    "source_bytes_sha256_at_end": sha(SRC),
    "provenance_source_sha256": prov.get("source_sha256"),
    "unevaluable": res.get("unevaluable"),
    "fresh_cells_classes": [(c.get("kind"), c.get("delta"), c.get("class"), c.get("roundtrip")) for c in res.get("cells", [])],
    "intact_identity": (res.get("intact") or {}).get("identity"),
}
print("TOCTOU", json.dumps(toctou, indent=1))
json.dump(toctou, open(f"{AT}/toctou-result.json", "w"), indent=1)

# ---------- (b) source made unreadable / removed after the first invoke of the arm
SRC2 = f"{W}/fresh-src-copy2.bin"
shutil.copyfile("/usr/bin/env", SRC2)
v3.FRESH_SOURCES = [("env", SRC2, sha(SRC2))]
orig_invoke = v2.invoke
calls = {"n": 0}

def kill_source_after_first(repair, data, env_, work):
    calls["n"] += 1
    rec = orig_invoke(repair, data, env_, work)
    if calls["n"] == 1:
        os.chmod(SRC2, 0)
        os.unlink(SRC2)
    return rec

v2.invoke = kill_source_after_first
res2 = v3.fresh_arm(REPAIR, env, W, rep, r88, {}, C)
v2.invoke = orig_invoke
cls2 = [(c.get("kind"), c.get("delta"), c.get("class"), c.get("roundtrip")) for c in res2.get("cells", [])]
unread = {"invokes_seen": calls["n"], "source_removed_after_first_invoke": not os.path.exists(SRC2),
          "unevaluable": res2.get("unevaluable"), "cells": cls2,
          "intact_identity": (res2.get("intact") or {}).get("identity"),
          "provenance_ok": bool(res2.get("provenance", {}).get("marker_in_mutated"))}
print("UNREADABLE", json.dumps(unread, indent=1))
json.dump(unread, open(f"{AT}/unreadable-mid-arm-result.json", "w"), indent=1)
