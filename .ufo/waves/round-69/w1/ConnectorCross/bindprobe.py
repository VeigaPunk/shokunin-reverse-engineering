#!/usr/bin/env python3
"""Scratch: demonstrate what the two frozen receipt readers bind and do not bind.

Read-only w.r.t. the lane: imports the frozen modules, writes only inside this
scratch dir, copies nothing from the lane. Never executes a carrier.
"""
import importlib.util
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


probe = load("r69probe", os.path.join(LANE, "tools/round-69/contract-probe.py"))
controls = load("r69controls", os.path.join(LANE, "tools/round-69/controls.py"))

bogus = {"path": "tools/does-not-exist.py",
         "sha256": "00" * 32,
         "rev": "deadbeef" * 5}

# --- A: C3 checker over a synthetic met receipt with a fabricated instrument ---
r = controls.synthetic_receipt(False)
r["instrument"] = bogus
p_a = os.path.join(S, "a-c3-synthetic-bogus-instrument.json")
with open(p_a, "w", encoding="utf-8") as fh:
    json.dump(r, fh, indent=1, sort_keys=True)
a = subprocess.run([sys.executable, "-I", "-B",
                    os.path.join(LANE, "tools/round-69/packed-elf.py"),
                    "--check-receipt", p_a],
                   capture_output=True, text=True)

# --- B: A5/A6 over a receipt shaped as the readers require, fabricated instrument ---
carriers = []
for cid, kind, source in (("jq", "executable", "/usr/bin/jq"),
                          ("xxd", "executable", "/usr/bin/xxd"),
                          ("libz", "shared-object", "/usr/lib/libz.so.1.3.2")):
    fmt = probe.elf_format(subprocess.run(
        ["readelf", "-h", source], capture_output=True, text=True).stdout)
    carriers.append({
        "id": cid, "name": cid, "kind": kind,
        "source": source, "pin": probe.sha256_file(source),
        "format": fmt, "packing_mode": probe.PACKING_MODE,
        "ok": True,
        "arms": {"detected": True, "before_ok": True, "identity_ok": True,
                 "recovery_ok": True, "control_ok": True},
        "runs": {"pack": {"argv": ["/usr/bin/upx", "--best", "-q",
                                   "-o", "packed", "orig"]}},
        "orig_counts": {"procedure_count": 167},
        "packed_counts": {"procedure_count": 3},
    })
upx_sha = probe.sha256_file("/usr/bin/upx")
upx_ver = subprocess.run(["/usr/bin/upx", "--version"], capture_output=True,
                         text=True).stdout.strip().splitlines()[0]
receipt_b = {
    "instrument": bogus,
    "rev": "deadbeef" * 5,
    "carriers": carriers,
    "packer": {"upx": "/usr/bin/upx", "sha256": upx_sha, "version": upx_ver,
               "sha256_pin": upx_sha, "version_pin": upx_ver,
               "pin_enforced": True},
}
p_b = os.path.join(S, "b-ab-synthetic-bogus-instrument.json")
with open(p_b, "w", encoding="utf-8") as fh:
    json.dump(receipt_b, fh, indent=1, sort_keys=True)
arms = probe.arms_from_receipt(p_b)
# swap in a genuine route hash to show the field is never compared
frozen_sha = "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc"
print(json.dumps({
    "A": {"argv": ["packed-elf.py", "--check-receipt", p_a],
          "rc": a.returncode,
          "met": (json.loads(a.stdout).get("met") if a.stdout.strip() else None),
          "instrument_in_receipt": bogus,
          "receipt": p_a},
    "B": {"arms": [{"id": x["id"], "ok": x["ok"],
                    "failures": x["observed"].get("failures")} for x in arms],
          "instrument_in_receipt": bogus,
          "frozen_route_sha_unused": frozen_sha,
          "receipt": p_b},
}, indent=1, sort_keys=True))
