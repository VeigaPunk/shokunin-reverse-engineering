#!/usr/bin/env python3
"""CriticC1 attack harness (scratch). Builds receipt fixtures from the honest v6 receipt at
the clone HEAD, scores them in-process with the v6 verify_receipt and through the round-95
c1-agreement-v2 CLI, and runs kill-rule-v2 mutant/probe attacks on scratch copies."""
import copy
import hashlib
import importlib.util
import io
import json
import os
import py_compile
import shutil
import subprocess
import sys
import contextlib

S = os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku/kaidoku-r96/CriticC1")
LANE = os.path.join(S, "lane")
ATK = os.path.join(S, "attacks")
OUT = os.path.join(S, "harness-out")
os.makedirs(OUT, exist_ok=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


base = json.load(open(os.path.join(ATK, "base", "honest-at-head.json")))
HEAD = base["head"]
OLD = "e4d1f7de9deae83e6d5f78d2d7f0157196002af0"
FROZEN = base["expect"]
V6 = os.path.join(LANE, "tools/round-96/stop-boundary-repair-battery-v6.py")
V3 = os.path.join(LANE, "tools/round-93/stop-boundary-repair-battery-v3.py")
UPX = os.path.join(LANE, "tools/round-92/upx-stop-boundary-search-repair.py")
PINS = {"counter": sha(V6), "verdict": sha(V3), "repair": sha(UPX)}
v6 = load(V6, "r96_v6_attack")

# ---------------------------------------------------------------- attack fixtures
INTENDED = {
    "counts-bool": "counts-type:repaired",
    "counts-extra-key": None,            # gap if accepted
    "counts-unbound-silent": None,       # gap if accepted
    "head-39hex": "head-not-bound",
    "met-string-true": None,             # gap if accepted (met must be a bool)
    "met-null": None,                    # gap if accepted
    "expect-empty-met-lying": "met-not-recomputed",
    "label-no-counts": "counts-missing-key",   # intended: a schema refusal
    "repair-cmd-swapped": None,          # gap if accepted (repair_cmd unbound)
    "head-rev-old-caller-old": None,     # head == revision == OLD; caller world OLD
    "public-met-lying": None,            # gap if accepted (public_met unbound)
    "imported-pins-zeroed": None,        # gap if accepted (imported_* unbound)
    "revision-symbolic-HEAD": "revision-not-bound",
    "committed-honest-pos-dirty": None,  # the landed honest receipt itself
}


def mk(name):
    r = copy.deepcopy(base)
    if name == "counts-bool":
        r["counts"]["repaired"] = True
    elif name == "counts-extra-key":
        r["counts"]["forged_extra"] = 7
    elif name == "counts-unbound-silent":
        r["counts"]["silent"] = 9
    elif name == "head-39hex":
        r["revision"] = HEAD[:39]
        r["head"] = HEAD[:39]
    elif name == "met-string-true":
        r["met_target"] = "true"
    elif name == "met-null":
        r["met_target"] = None
    elif name == "expect-empty-met-lying":
        r["met_target"] = False
        r["exit"] = 1
    elif name == "label-no-counts":
        del r["counts"]
    elif name == "repair-cmd-swapped":
        r["repair_cmd"] = ".ufo/waves/round-93/controls/identity_noop.py"
    elif name == "head-rev-old-caller-old":
        r["revision"] = OLD
        r["head"] = OLD
    elif name == "public-met-lying":
        r["public_met"] = False
        r["public_label"] = "repaired 0 of 0; wrong 0; unsafe 0; intact 0 of 0; far-refused 0 of 0"
    elif name == "imported-pins-zeroed":
        r["imported_r92_battery_sha256"] = "0" * 64
        r["imported_v2_sha256"] = "0" * 64
    elif name == "revision-symbolic-HEAD":
        r["revision"] = "HEAD"
        r["head"] = HEAD
    elif name == "committed-honest-pos-dirty":
        r = json.load(open(os.path.join(LANE, ".ufo/waves/round-96/l1/scores/honest-pos.json")))
    elif name == "honest-control":
        pass
    else:
        raise KeyError(name)
    return r


NAMES = list(INTENDED) + ["honest-control"]
rows = []
os.makedirs(os.path.join(ATK, "fixtures"), exist_ok=True)
os.makedirs(os.path.join(ATK, "agreement"), exist_ok=True)
for name in NAMES:
    rec = mk(name)
    p = os.path.join(ATK, "fixtures", "atk-%s.json" % name)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    # agreement triple (stdout/rc derived from the receipt the way a producer prints it)
    label = rec.get("label") if isinstance(rec.get("label"), str) else "(no label)"
    met = rec.get("met_target")
    met_txt = "True" if met in (True, "true") else ("False" if met in (False, None) else "False")
    ex = rec.get("exit", 1)
    ex = ex if isinstance(ex, int) and not isinstance(ex, bool) else 1
    ad = os.path.join(ATK, "agreement", name)
    os.makedirs(ad, exist_ok=True)
    shutil.copyfile(p, os.path.join(ad, "atk-pos.json"))
    with open(os.path.join(ad, "atk-pos.stdout"), "w") as fh:
        fh.write("%s met %s exit %d\n" % (label, met_txt, ex))
    with open(os.path.join(ad, "atk-pos.rc"), "w") as fh:
        fh.write("%d\n" % ex)

# ---------------------------------------------------------------- in-process verify
for name in NAMES:
    rec = json.load(open(os.path.join(ATK, "fixtures", "atk-%s.json" % name)))
    p = os.path.join(ATK, "fixtures", "atk-%s.json" % name)
    expect = FROZEN
    caller = HEAD  # honest caller: the world is the lane HEAD
    res_head = v6.verify_receipt(p, expect, caller, 6, PINS)
    # kill-rule style: rev_full taken from the receipt's own revision (K-forgeries)
    kr_style = v6.verify_receipt(p, expect, rec.get("revision"), 6, PINS)
    res_old = None
    if name in ("head-rev-old-caller-old", "committed-honest-pos-dirty"):
        res_old = v6.verify_receipt(p, expect, OLD, 6, PINS)
    extra = None
    if name == "expect-empty-met-lying":
        extra = v6.verify_receipt(p, "", HEAD, 6, PINS)
    rows.append({"name": name, "intended": INTENDED.get(name, "n/a"),
                 "verify_head_world": res_head, "verify_kill_rule_style": kr_style,
                 "verify_old_world": res_old, "verify_expect_empty": extra})

with open(os.path.join(OUT, "inprocess.json"), "w") as fh:
    json.dump(rows, fh, indent=1, sort_keys=True)
for r in rows:
    print("%-30s head-world=%s | kr-style=%s%s%s" % (
        r["name"], r["verify_head_world"]["reasons"] if not r["verify_head_world"]["ok"] else "ACCEPT",
        r["verify_kill_rule_style"]["reasons"] if not r["verify_kill_rule_style"]["ok"] else "ACCEPT",
        (" | old-world=" + str(r["verify_old_world"]["reasons"] if not r["verify_old_world"]["ok"] else "ACCEPT")) if r["verify_old_world"] else "",
        (" | expect-empty=" + str(r["verify_expect_empty"]["reasons"] if not r["verify_expect_empty"]["ok"] else "ACCEPT")) if r["verify_expect_empty"] else ""))

# ---------------------------------------------------------------- agreement CLI
agr_rows = {}
for name in NAMES:
    rev = HEAD
    cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-95/c1-agreement-v2.py"),
           "--root", LANE, "--dir", os.path.join(ATK, "agreement", name), "--prefix", "atk",
           "--names", "pos", "--expect", FROZEN, "--rev", rev, "--intact-total", "6"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try:
        payload = json.loads(p.stdout)
        reasons = [r["reasons"] for r in payload.get("rows", []) if r.get("run") == "pos"]
    except ValueError:
        reasons = ["UNPARSED:" + p.stdout[-200:] + p.stderr[-300:]]
    agr_rows[name] = {"rc": p.returncode, "reasons": reasons}
# Old-world agreement for the two OLD-revision attacks and the committed honest receipt
for name in ("head-rev-old-caller-old", "committed-honest-pos-dirty"):
    cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-95/c1-agreement-v2.py"),
           "--root", LANE, "--dir", os.path.join(ATK, "agreement", name), "--prefix", "atk",
           "--names", "pos", "--expect", FROZEN, "--rev", OLD, "--intact-total", "6"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try:
        payload = json.loads(p.stdout)
        reasons = [r["reasons"] for r in payload.get("rows", []) if r.get("run") == "pos"]
    except ValueError:
        reasons = ["UNPARSED:" + p.stdout[-200:] + p.stderr[-300:]]
    agr_rows[name + "@OLD"] = {"rc": p.returncode, "reasons": reasons}
with open(os.path.join(OUT, "agreement.json"), "w") as fh:
    json.dump(agr_rows, fh, indent=1, sort_keys=True)
for k, v in agr_rows.items():
    print("agreement %-34s rc=%s %s" % (k, v["rc"], v["reasons"]))

# the committed honest receipt at its own revision via the honest-pos triple
hp = os.path.join(LANE, ".ufo/waves/round-96/l1/scores")
cmd = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-95/c1-agreement-v2.py"),
       "--root", LANE, "--dir", hp, "--prefix", "honest", "--names", "pos",
       "--expect", FROZEN, "--rev", OLD, "--intact-total", "6"]
p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print("agreement committed honest-pos @OLD rc=%s %s" % (p.returncode, p.stdout[-400:]))
cmd[cmd.index("--rev") + 1] = HEAD
p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
print("agreement committed honest-pos @HEAD rc=%s %s" % (p.returncode, p.stdout[-400:]))
