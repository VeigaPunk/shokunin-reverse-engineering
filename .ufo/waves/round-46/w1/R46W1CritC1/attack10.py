#!/usr/bin/env python3
"""Round 10: the pin's circularity — a committed patched counter whose own hash the
SKILL.md pin records, scored at freeze==rev."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["HYAKU_SCRATCH"]
PINDIR = sys.argv[1]
REV = sys.argv[2]
OUT = {}
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)


def show(p):
    r = subprocess.run(["git", "-C", LANE, "show", "%s:%s" % (REV, p)],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def cli(root, prog, freeze, rev, battery=False):
    args = [sys.executable, "-I", "-B", prog, "--root", root, "--freeze", freeze,
            "--rev", rev]
    if not battery:
        args.append("--no-battery")
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        d = {"raw": r.stdout[:200]}
    return r.returncode, d, r.stdout


def fixture(name, skill, tool_text):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "c@r46"), ("user.name", "critic")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    assert subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True).stdout.strip() == d
    files = {"SKILL.md": skill, "plans/round-46-claims.md": show("plans/round-46-claims.md"),
             "corpus/lessons/round-45.md": show("corpus/lessons/round-45.md"),
             "corpus/lessons/round-46.md": show("corpus/lessons/round-46.md"),
             "tools/round-46/attest.py": tool_text,
             "tools/round-46/gate.py": show("tools/round-46/gate.py")}
    for p, body in files.items():
        if body is None:
            continue
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w").write(body)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fx"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


skill = show("SKILL.md")
tool = show("tools/round-46/attest.py")
sys.path.insert(0, PINDIR)
import importlib.util
gs = importlib.util.spec_from_file_location("gate", os.path.join(PINDIR, "gate.py"))
gate = importlib.util.module_from_spec(gs); sys.modules["gate"] = gate; gs.loader.exec_module(gate)
a_s = importlib.util.spec_from_file_location("attest", os.path.join(PINDIR, "attest.py"))
attest = importlib.util.module_from_spec(a_s); sys.modules["attest"] = attest
a_s.loader.exec_module(attest)
block = [b for b in attest.craft_blocks(skill) if attest.SPECS["r46"]["marker"] in b][0]
realpin = attest.PIN.search(block).group(1)

# 1) baseline: genuine tool + genuine pin, freeze == rev, committed.
d, rev = fixture("base", skill, tool)
rc, r, raw = cli(d, os.path.join(d, "tools/round-46/attest.py"), rev, rev, battery=True)
OUT["1_baseline_committed"] = {"exit": rc, "met": r.get("met_target"),
                              "fail": r.get("failing"), "pin": r.get("pin"),
                              "bat": (r.get("battery") or {}).get("forgeries_total")}

# 2) patched tool committed + pin recomputed to that tool's own hash.
patched = tool.replace('    failing = []\n',
                       '    receipt["met_target"] = True\n    return 0, receipt\n'
                       '    failing = []\n', 1)
assert patched != tool
newpin = hashlib.sha256(patched.encode()).hexdigest()
skill2 = skill.replace("sha256:" + realpin, "sha256:" + newpin, 1)
d2, rev2 = fixture("patched", skill2, patched)
rc, r, raw = cli(d2, os.path.join(d2, "tools/round-46/attest.py"), rev2, rev2, battery=True)
OUT["2_patched_pin_recomputed"] = {"exit": rc, "met": r.get("met_target"),
                                  "fail": r.get("failing"), "pin": r.get("pin"),
                                  "pin_expected": r.get("pin_expected"),
                                  "newpin": newpin, "realpin": realpin}
print("2 patched+recomputed pin:", rc, json.dumps(OUT["2_patched_pin_recomputed"])[:300])

# 3) same patched tool but pin left at the genuine value, freeze==rev.
d3, rev3 = fixture("patched-oldpin", skill, patched)
rc, r, raw = cli(d3, os.path.join(d3, "tools/round-46/attest.py"), rev3, rev3, battery=True)
OUT["3_patched_pin_stale"] = {"exit": rc, "met": r.get("met_target"),
                              "fail": r.get("failing")}
print("3 patched+stale pin:", rc, json.dumps(OUT["3_patched_pin_stale"])[:300])

# 4) can the forger delete the pin clause instead of matching it? (no pin at all)
skill4 = skill.replace("sha256:" + realpin, "sha256:" + "0" * 64, 1)
d4, rev4 = fixture("zeropin", skill4, tool)
rc, r, raw = cli(d4, os.path.join(d4, "tools/round-46/attest.py"), rev4, rev4, battery=False)
OUT["4_zero_pin_genuine_tool"] = {"exit": rc, "fail": r.get("failing")}
print("4 zero pin:", rc, json.dumps(OUT["4_zero_pin_genuine_tool"])[:200])

OUT["realpin"] = realpin
OUT["patched_sha256"] = newpin
json.dump(OUT, open(os.path.join(S, "attacks10.json"), "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in OUT.items() if k in ("realpin", "patched_sha256")}, indent=1))
