#!/usr/bin/env python3
"""Consolidated clause-8 matrix, pinned to one lane revision.

Every fixture is rebuilt from the lane's blob at PIN for the files the counter needs, so
each receipt names the exact bytes it graded. The counter under test is the frozen
tools/round-47/exact.py at PIN (byte-identical to the freeze blob).
"""
import hashlib
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs")
import drive  # noqa: E402

S = drive.S
LANE = drive.LANE
PIN = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
drive.FILES = drive.FILES  # unchanged


def blob(p):
    return subprocess.run(["git", "-C", LANE, "show", f"{PIN}:{p}"],
                          capture_output=True, text=True).stdout


def bfiles():
    return {p: blob(p) for p in drive.FILES}


BASE = bfiles()
SKILL = BASE["SKILL.md"]
SKILL_SHA = hashlib.sha256(SKILL.encode()).hexdigest()
R46 = BASE["corpus/lessons/round-46.md"]
R45 = BASE["corpus/lessons/round-45.md"]
KN = blob("corpus/knowledge/2026-10-13-crash-evidence.md")

# the three interpreters: the frozen counter, a clause-8-lax copy, a clause-8-literal copy
EX = BASE["tools/round-47/exact.py"]
G = BASE["tools/round-46/gate.py"]
for d in ("lax", "strict", "round-46"):
    os.makedirs(os.path.join(S, d), exist_ok=True)
open(os.path.join(S, "round-46/gate.py"), "w").write(G)
old = "def check_refs(block, files, hard):\n    bad, cited = [], set()"
assert old in EX and EX.count("    return bad, cited\n") == 1
LAX = (EX.replace(old, old).replace("    return bad, cited\n", "    return [], cited\n")
          .replace('"""Round-47 C1 counter', '"""Round-47 C1 counter (LAX)', 1))
EXEMPT = ('        if name == SELF:\n'
          '            continue  # identified by its own sha256 pin, not by a line selector\n')
assert EXEMPT in EX
STRICT = EX.replace(EXEMPT, "").replace('"""Round-47 C1 counter',
                                        '"""Round-47 C1 counter (STRICT)', 1)
open(os.path.join(S, "lax/exact.py"), "w").write(LAX)
open(os.path.join(S, "strict/exact.py"), "w").write(STRICT)
LAX_SHA = hashlib.sha256(LAX.encode()).hexdigest()
rows = []


def rec(name, fx, rev, interp, battery, note):
    cmd = ["python3", "-I", "-B", interp, "--root", fx, "--freeze", rev, "--rev", rev]
    if not battery:
        cmd.append("--no-battery")
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S)
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
                    ("failing", "met_target", "refs", "cited", "unresolved_citations",
                     "reason", "interpreter_sha256", "interpreter_sha256_expected")})
        out["battery"] = {k: v for k, v in (d.get("battery") or {}).items()
                          if k != "fixtures"}
        out["battery_fixtures"] = (d.get("battery") or {}).get("fixtures")
    except Exception:
        out["stdout_head"] = r.stdout[:300]
        out["stderr_head"] = r.stderr[:300]
    path = os.path.join(S, "receipts", name + ".json")
    open(path, "w").write(json.dumps(out, indent=1, sort_keys=True) + "\n")
    rows.append(out)
    print(f"{name:28s} exit={out['exit']} refs={out.get('refs')} "
          f"battery={'(skipped)' if not battery else out.get('battery', {}).get('v3_green')} "
          f"failing={out.get('failing')} reason={out.get('reason')}")
    return out


def fixture(name, refs, extra=None, mutate=None):
    return drive.make_repo(name, drive.swap_refs(SKILL, refs, mutate), extra)


def real(fx):
    return os.path.join(fx, "tools/round-47/exact.py")


# ---- baseline -------------------------------------------------------------------
fx, rev = fixture("c0_landed", None)
rec("c0_landed_battery", fx, rev, real(fx), True, "landed block, unchanged")

# ---- 1. citations that resolve but are off-topic --------------------------------
fx, rev = fixture("c1_offtopic",
                  "`corpus/lessons/round-46.md:1-1`, `plans/round-47-claims.md:1-1`, "
                  "`tools/round-47/exact.py:1-1`")
rec("c1_offtopic_battery", fx, rev, real(fx), True, "three resolving but contentless anchors")

fx, rev = fixture("c1b_wronground",
                  "`corpus/lessons/round-45.md:1-5`, `corpus/lessons/round-45.md:6-9`, "
                  "`corpus/lessons/round-46.md:1-1`")
rec("c1b_wronground_battery", fx, rev, real(fx), True,
    "round-45 lines cited for round-46 defects (round-45.md is in the battery dict)")

fx, rev = fixture("c1c_samefile",
                  "`corpus/lessons/round-46.md:5`, `corpus/lessons/round-46.md:5`, "
                  "`corpus/lessons/round-46.md:5`")
rec("c1c_samefile3x_battery", fx, rev, real(fx), True, "one line cited three times = refs 3")

# ---- 2. path prefix of the allowlist -------------------------------------------
fx, rev = fixture("c2_prefix",
                  "`corpus/lessons-evil/round-46.md:1-5`, "
                  "`corpus/lessons-evil/round-46.md:6`, `corpus/lessons/round-46.md:1-1`",
                  {"corpus/lessons-evil/round-46.md": R46})
rec("c2_prefix_evil_nobat", fx, rev, real(fx), False, "corpus/lessons-evil/ cited, file exists")

fx, rev = fixture("c2b_bak",
                  "`corpus/lessons/round-46.md.bak:1-5`, `corpus/lessons/round-46.md.bak:6`, "
                  "`corpus/lessons/round-46.md:1-1`",
                  {"corpus/lessons/round-46.md.bak": R46})
rec("c2b_sibling_bak_nobat", fx, rev, real(fx), False, "byte copy under an allowed prefix")
rec("c2b_sibling_bak_battery", fx, rev, real(fx), True, "same, with the battery")

# ---- 3. ranges that end at the last line ---------------------------------------
fx, rev = fixture("c3_lastline",
                  "`corpus/lessons/round-46.md:1-102`, `corpus/lessons/round-46.md:102`, "
                  "`corpus/lessons/round-46.md:102-102`")
rec("c3_lastline_battery", fx, rev, real(fx), True,
    "whole file, last line, last line as a range (file has 102 lines)")

fx, rev = fixture("c3b_pasteof",
                  "`corpus/lessons/round-46.md:103`, `corpus/lessons/round-46.md:1-102`, "
                  "`plans/round-47-claims.md:1-1`")
rec("c3b_pasteof_nobat", fx, rev, real(fx), False, "one line past EOF")

# ---- 4. pins over a copy of the counter ----------------------------------------
fx, rev = fixture("c4_prefix_for_lax",
                  "`corpus/lessons-evil/round-46.md:1-5`, "
                  "`corpus/lessons-evil/round-46.md:6`, `corpus/lessons/round-46.md:1-1`",
                  {"corpus/lessons-evil/round-46.md": R46})
rec("c4_real_nobat", fx, rev, real(fx), False, "frozen counter, hostile citation")
rec("c4_lax_copy_nobat", fx, rev, os.path.join(S, "lax/exact.py"), False,
    "same fixture bytes, out-of-tree lax copy executed")

fx, rev = fixture("c4b_pin_over_lax",
                  "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:45-113`, "
                  "`plans/round-47-claims.md:141-176`",
                  mutate=lambda b: __import__("re").sub(
                      r"interpreter_sha256:[0-9a-f]{64}",
                      "interpreter_sha256:" + LAX_SHA, b, count=1))
rec("c4b_pin_over_lax_nobat", fx, rev, real(fx), False,
    "block pins the lax copy's digest instead of the counter's")

# ---- 5. clause 8 read literally (SELF exemption removed) -----------------------
fx, rev = fixture("c5_landed", None)
rec("c5_landed_real_nobat", fx, rev, real(fx), False, "landed block, frozen counter")
rec("c5_landed_strict_nobat", fx, rev, os.path.join(S, "strict/exact.py"), False,
    "landed block, clause 8 without the SELF exemption")

# ---- 6. the allowlist is not the battery's file set ----------------------------
fx, rev = fixture("c6_knowledge",
                  "`corpus/knowledge/2026-10-13-crash-evidence.md:1-3`, "
                  "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:45-113`",
                  {"corpus/knowledge/2026-10-13-crash-evidence.md": KN})
rec("c6_knowledge_nobat", fx, rev, real(fx), False, "a legitimate knowledge citation")
rec("c6_knowledge_battery", fx, rev, real(fx), True, "same, with the battery")

fx, rev = fixture("c6b_dir",
                  "`tools/round-47/:1-2`, `plans/:1-2`, `corpus/lessons/round-46.md:1-1`")
rec("c6b_dir_nobat", fx, rev, real(fx), False, "two directory citations, one real selector")
rec("c6b_dir_battery", fx, rev, real(fx), True, "same, with the battery")

# ---- 7. the dirty guard --------------------------------------------------------
fx, rev = fixture("c7_dirty", None)
open(real(fx), "a").write("\n# tampered\n")
rec("c7_dirty_worktree_nobat", fx, rev, real(fx), False,
    "worktree copy of the counter edited after the commit")

fx, rev = fixture("c7b_ignored", None)
open(os.path.join(fx, ".gitignore"), "w").write(blob(".gitignore"))
os.makedirs(os.path.join(fx, "tools/round-47/__pycache__"), exist_ok=True)
open(os.path.join(fx, "tools/round-47/__pycache__/forged.pyc"), "wb").write(b"\x00")
subprocess.run(["git", "-C", fx, "add", "-A"], check=True)
subprocess.run(["git", "-C", fx, "commit", "-q", "-m", "ignored"], check=True)
rev = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()
rec("c7b_ignored_artefact_nobat", fx, rev, real(fx), False,
    "gitignored byte under tools/round-47/ (the lane has __pycache__/ there)")

json.dump({"lane_pin": PIN, "freeze": FREEZE, "base_skill_sha256": SKILL_SHA,
           "lax_sha256": LAX_SHA,
           "strict_sha256": hashlib.sha256(STRICT.encode()).hexdigest(),
           "rows": rows},
          open(os.path.join(S, "receipts", "matrix_final.json"), "w"), indent=1)
print("\nPINS", PIN, SKILL_SHA, LAX_SHA)
