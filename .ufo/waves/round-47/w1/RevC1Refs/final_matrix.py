#!/usr/bin/env python3
"""Final clause-8 matrix on full-tree fixtures pinned to one lane revision.

Fixtures are `git archive <PIN> | tar -x` copies of the lane, so every citation in the
landed block resolves exactly as it does in the lane. Only the marked block's Refs line
(or the interpreter) is varied.
"""
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import time

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs"
os.makedirs(os.path.join(S, "receipts"), exist_ok=True)
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FROZEN_FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
PIN = os.environ.get("R47_PIN") or subprocess.run(
    ["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
MARKER = "<!-- exactness-table v3 -->"


def blob(p, rev=PIN):
    return subprocess.run(["git", "-C", LANE, "show", f"{rev}:{p}"],
                          capture_output=True, text=True).stdout


SKILL = blob("SKILL.md")
SKILL_SHA = hashlib.sha256(SKILL.encode()).hexdigest()
EX = blob("tools/round-47/exact.py")
G = blob("tools/round-46/gate.py")
PIN_IN_BLOCK = re.search(r"interpreter_sha256:([0-9a-f]{64})", SKILL).group(1)
EX_SHA = hashlib.sha256(EX.encode()).hexdigest()

# interpreters ---------------------------------------------------------------------
os.makedirs(os.path.join(S, "round-46"), exist_ok=True)
open(os.path.join(S, "round-46/gate.py"), "w").write(G)
HEAD8 = "def check_refs(block, files, hard):\n    bad, cited = [], set()"
assert HEAD8 in EX and EX.count("    return bad, cited\n") == 1
LAX = (EX.replace("    return bad, cited\n", "    return [], cited\n")
         .replace('"""Round-47 C1 counter', '"""Round-47 C1 counter (LAX)', 1))
EXEMPT = ('        if name == SELF:\n'
          '            continue  # identified by its own sha256 pin, not by a line selector\n')
assert EXEMPT in EX
STRICT = EX.replace(EXEMPT, "").replace('"""Round-47 C1 counter',
                                        '"""Round-47 C1 counter (STRICT)', 1)
os.makedirs(os.path.join(S, "lax"), exist_ok=True)
os.makedirs(os.path.join(S, "strict"), exist_ok=True)
open(os.path.join(S, "lax/exact.py"), "w").write(LAX)
open(os.path.join(S, "strict/exact.py"), "w").write(STRICT)
LAX_SHA = hashlib.sha256(LAX.encode()).hexdigest()
STRICT_SHA = hashlib.sha256(STRICT.encode()).hexdigest()

rows = []


def archive_fixture(name, skill_text):
    """Extract the lane tree at PIN, overwrite SKILL.md, commit one revision."""
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    tar = subprocess.run(["git", "-C", LANE, "archive", PIN], capture_output=True)
    assert tar.returncode == 0, tar.stderr[:300]
    with tarfile.open(fileobj=io.BytesIO(tar.stdout)) as tf:
        tf.extractall(d, filter=lambda m, p: None if (m.issym() or m.islnk()) else m)
    open(os.path.join(d, "SKILL.md"), "w").write(skill_text)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def swap(skill, refs):
    i = skill.index(MARKER)
    start = skill.rindex("- **", 0, i)
    end = skill.index("\n## ", i)
    block = skill[start:end]
    out = ["  Refs: " + refs if line.strip().startswith("Refs:") else line
           for line in block.splitlines()]
    return skill[:start] + "\n".join(out) + skill[end:]


def repin(skill, digest):
    return re.sub(r"interpreter_sha256:[0-9a-f]{64}",
                  "interpreter_sha256:" + digest, skill, count=1)


def measure(name, skill, interp, battery, note):
    fx, rev = archive_fixture(name, skill)
    interp = os.path.join(fx, "tools/round-47/exact.py") if interp == "SELF" else interp
    cmd = ["python3", "-I", "-B", interp, "--root", fx, "--freeze", rev, "--rev", rev]
    if not battery:
        cmd.append("--no-battery")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S), cwd=S)
    out = {"variant": name, "lane_pin": PIN, "base_skill_sha256": SKILL_SHA,
           "fixture": fx, "fixture_rev": rev, "cmd": " ".join(cmd), "note": note,
           "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "interpreter": interp,
           "interpreter_sha256": hashlib.sha256(open(interp, "rb").read()).hexdigest()}
    try:
        d = json.loads(r.stdout)
        out.update({k: d.get(k) for k in
                    ("failing", "met_target", "refs", "unresolved_citations", "reason",
                     "interpreter_sha256", "interpreter_sha256_expected")})
        out["battery"] = {k: v for k, v in (d.get("battery") or {}).items()
                          if k != "fixtures"}
        out["battery_fixtures"] = (d.get("battery") or {}).get("fixtures")
    except Exception:
        out["stdout_head"] = r.stdout[:400]
        out["stderr_head"] = r.stderr[:400]
    open(os.path.join(S, "receipts", name + ".json"), "w").write(
        json.dumps(out, indent=1, sort_keys=True) + "\n")
    rows.append(out)
    b = out.get("battery") or {}
    print(f"{name:30s} exit={out['exit']} refs={out.get('refs')} "
          f"v3_green={b.get('v3_green')} genuine={b.get('genuine_green')} "
          f"failing={out.get('failing')} reason={out.get('reason')}")
    return out


def fx_interp(name):
    return os.path.join(S, "fx-" + name, "tools/round-47/exact.py")


FRESH = repin(SKILL, EX_SHA)  # the landed block with the pin refreshed to the bytes at PIN

# L: the lane's own bytes, no fixture: declared freeze vs the measured rev
lane_cmd = ["python3", "-I", "-B", os.path.join(LANE, "tools/round-47/exact.py"),
            "--root", LANE, "--freeze", FROZEN_FREEZE, "--rev", PIN, "--no-battery"]
r = subprocess.run(lane_cmd, capture_output=True, text=True,
                   env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S), cwd=S)
out = {"variant": "L_lane_declared_freeze", "lane_pin": PIN, "cmd": " ".join(lane_cmd),
       "exit": r.returncode,
       "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
       "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
try:
    d = json.loads(r.stdout)
    out.update({k: d.get(k) for k in ("reason", "frozen_path_changed", "failing")})
except Exception:
    out["stdout_head"] = r.stdout[:300]
rows.append(out)
print(f"{out['variant']:30s} exit={out['exit']} reason={out.get('reason')} "
      f"changed={out.get('frozen_path_changed')}")

# 0. the landed block, as committed, then with the pin refreshed
measure("f0_landed_ascommitted", SKILL, "SELF", False,
        "landed block at PIN, its committed interpreter pin")
measure("f0b_landed_pin_refreshed", FRESH, "SELF", True,
        "landed block, interpreter pin refreshed to the bytes at PIN")

# 1. citations that resolve but are off-topic
measure("f1_offtopic", swap(FRESH,
        "`corpus/lessons/round-46.md:1-1`, `plans/round-47-claims.md:1-1`, "
        "`tools/round-47/exact.py:1-1`"), "SELF", True,
        "three resolving but contentless anchors (headers only)")
measure("f1b_wronground", swap(FRESH,
        "`corpus/lessons/round-45.md:1-5`, `corpus/lessons/round-45.md:6-9`, "
        "`corpus/lessons/round-46.md:1-1`"), "SELF", True,
        "round-45 lines cited for the round-46 defects")
measure("f1c_samefile3x", swap(FRESH,
        "`corpus/lessons/round-46.md:5`, `corpus/lessons/round-46.md:5`, "
        "`corpus/lessons/round-46.md:5`"), "SELF", True, "one line cited three times")
measure("f1d_bare_self", swap(FRESH,
        "`tools/round-47/exact.py`, `tools/round-47/exact.py`, "
        "`corpus/lessons/round-46.md:1-1`"), "SELF", True,
        "two selector-less self references + one real selector")

# 2. prefix of the allowlist
measure("f2_prefix_evil", swap(FRESH,
        "`corpus/lessons-evil/round-46.md:1-5`, `corpus/lessons-evil/round-46.md:6`, "
        "`corpus/lessons/round-46.md:1-1`"), "SELF", False,
        "corpus/lessons-evil/ is NOT inside corpus/lessons/ (file also absent)")
measure("f2b_sibling_bak", swap(FRESH,
        "`corpus/lessons/round-46-verifier-spotcheck.md:1-5`, "
        "`corpus/lessons/round-46-verifier-spotcheck.md:6-9`, "
        "`corpus/lessons/round-46.md:1-1`"), "SELF", True,
        "a different real file under the allowed prefix, irrelevant to the matrix")

# 3. ranges that end at the last line
measure("f3_lastline", swap(FRESH,
        "`corpus/lessons/round-46.md:1-102`, `corpus/lessons/round-46.md:102`, "
        "`corpus/lessons/round-46.md:102-102`"), "SELF", True,
        "whole file, last line, last line as a range")
measure("f3b_pasteof", swap(FRESH,
        "`corpus/lessons/round-46.md:103`, `corpus/lessons/round-46.md:1-102`, "
        "`plans/round-47-claims.md:1-1`"), "SELF", False, "one past EOF")

# 4. pins over a copy of the counter
measure("f4_real_interp", swap(FRESH,
        "`corpus/lessons-evil/round-46.md:1-5`, `corpus/lessons-evil/round-46.md:6`, "
        "`corpus/lessons/round-46.md:1-1`"), "SELF", False,
        "the frozen counter scores a citation outside the path set")
measure("f4_lax_copy", swap(FRESH,
        "`corpus/lessons-evil/round-46.md:1-5`, `corpus/lessons-evil/round-46.md:6`, "
        "`corpus/lessons/round-46.md:1-1`"), os.path.join(S, "lax/exact.py"), False,
        "same fixture bytes, an out-of-tree lax copy executed")
measure("f4b_pin_over_lax", repin(swap(FRESH,
        "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:45-113`, "
        "`plans/round-47-claims.md:141-176`"), LAX_SHA), "SELF", False,
        "block pins the lax copy's digest instead of the counter's")

# 5. clause 8 read literally
measure("f5_strict_interp", FRESH, os.path.join(S, "strict/exact.py"), False,
        "landed block, clause 8 without the SELF exemption")

# 6. the allowlist vs the battery's file set
measure("f6_knowledge", swap(FRESH,
        "`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, "
        "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:45-113`"), "SELF", True,
        "a knowledge citation the landed block now carries")
measure("f6b_dir", swap(FRESH,
        "`tools/round-47/:1-2`, `plans/:1-2`, `corpus/lessons/round-46.md:1-1`"), "SELF", False,
        "two directory citations")
measure("f6c_dir_battery", swap(FRESH,
        "`tools/round-47/:1-2`, `plans/:1-2`, `corpus/lessons/round-46.md:1-1`"), "SELF", True,
        "same, with the battery")

# 7. the dirty guard
measure("f7_dirty_worktree", FRESH, "SELF", False, "control: untouched worktree")
open(os.path.join(S, "fx-f7_dirty_worktree/tools/round-47/exact.py"), "a").write("\n# x\n")
measure("f7b_dirty_after_edit", FRESH, os.path.join(S, "fx-f7_dirty_worktree/tools/round-47/exact.py"),
        False, "worktree copy of the counter edited after the commit")

json.dump({"lane_pin": PIN, "base_skill_sha256": SKILL_SHA, "counter_sha256": EX_SHA,
           "pin_in_block": PIN_IN_BLOCK, "lax": LAX_SHA, "strict": STRICT_SHA,
           "frozen_freeze": FROZEN_FREEZE, "rows": rows},
          open(os.path.join(S, "receipts", "final_matrix.json"), "w"), indent=1)
print("\nPINS", PIN, EX_SHA, "blockpin", PIN_IN_BLOCK)
