#!/usr/bin/env python3
"""Second matrix: battery-free isolation, lax interpreter, worktree dirt, knowledge citation."""
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC1Refs")
import drive  # noqa: E402

S = drive.S
base = drive.base_files()["SKILL.md"]
R46 = drive.blob("corpus/lessons/round-46.md")
KN = drive.blob("corpus/knowledge/2026-10-13-crash-evidence.md")
rows = []


def write(path, text):
    full = os.path.join(S, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(text)


def run_raw(name, fixture, rev, interpreter, battery=True, cwd=None):
    cmd = ["python3", "-I", "-B", interpreter, "--root", fixture, "--freeze", rev,
           "--rev", rev]
    if not battery:
        cmd.append("--no-battery")
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=cwd or S)
    rec = {"variant": name, "fixture": fixture, "rev": rev,
           "cmd": " ".join(cmd), "exit": r.returncode,
           "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "utc": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ",
                                              __import__("time").gmtime()),
           "interpreter": interpreter,
           "interpreter_sha256": hashlib.sha256(open(interpreter, "rb").read()).hexdigest()}
    try:
        body = json.loads(r.stdout)
        rec.update({k: body.get(k) for k in
                    ("failing", "met_target", "refs", "cited", "unresolved_citations",
                     "reason", "interpreter_sha256", "interpreter_sha256_expected")})
        rec["battery"] = {k: v for k, v in (body.get("battery") or {}).items()
                          if k != "fixtures"}
    except Exception:
        rec["stdout_head"] = r.stdout[:400]
        rec["stderr_head"] = r.stderr[:400]
    open(os.path.join(S, "receipts", name + ".json"), "w").write(
        json.dumps(rec, indent=1, sort_keys=True) + "\n")
    rows.append(rec)
    print(f"{name:22s} exit={rec['exit']} refs={rec.get('refs')} "
          f"failing={rec.get('failing')} reason={rec.get('reason')}")
    return rec


# --- b1: directory citations, battery off (outer clause 8 isolated) ---------------
fixture, rev = drive.make_repo("b1_dir_nobat", drive.swap_refs(
    base, "`tools/round-47/:1-2`, `plans/:1-2`, `corpus/lessons/round-46.md:1-1`"))
run_raw("b1_dir_nobattery", fixture, rev, os.path.join(fixture, "tools/round-47/exact.py"),
        battery=False)

# --- b2: sibling byte-copy of the lesson, battery off ----------------------------
fixture, rev = drive.make_repo("b2_bak_nobat", drive.swap_refs(
    base, "`corpus/lessons/round-46.md.bak:1-5`, `corpus/lessons/round-46.md.bak:6`, "
          "`corpus/lessons/round-46.md:1-1`"),
    {"corpus/lessons/round-46.md.bak": R46})
run_raw("b2_bak_nobattery", fixture, rev, os.path.join(fixture, "tools/round-47/exact.py"),
        battery=False)

# --- b3: the prefix-of-allowlist citation, lax interpreter outside the lane ------
fixture, rev = drive.make_repo("b3_prefix_lax", drive.swap_refs(
    base, "`corpus/lessons-evil/round-46.md:1-5`, `corpus/lessons-evil/round-46.md:6`, "
          "`corpus/lessons/round-46.md:1-1`"),
    {"corpus/lessons-evil/round-46.md": R46})
real = os.path.join(fixture, "tools/round-47/exact.py")
run_raw("b3_prefix_real_interp", fixture, rev, real, battery=False)
run_raw("b3_prefix_lax_interp", fixture, rev, os.path.join(S, "lax/exact.py"), battery=False)

# --- b4: worktree tamper under the frozen path (the dirty guard) -----------------
fixture, rev = drive.make_repo("b4_dirty", base)
p = os.path.join(fixture, "tools/round-47/exact.py")
open(p, "a").write("\n# tampered\n")
run_raw("b4_dirty_exact_worktree", fixture, rev, p, battery=False)

# --- b5: gitignored artefact under the frozen path ------------------------------
fixture, rev = drive.make_repo("b5_ignored", base)
write_gitignore = drive.blob(".gitignore")
open(os.path.join(fixture, ".gitignore"), "w").write(write_gitignore)
os.makedirs(os.path.join(fixture, "tools/round-47/__pycache__"), exist_ok=True)
open(os.path.join(fixture, "tools/round-47/__pycache__/forged.pyc"), "wb").write(b"\x00")
subprocess.run(["git", "-C", fixture, "add", "-A"], check=True)
subprocess.run(["git", "-C", fixture, "commit", "-q", "-m", "ignored artefact"],
               check=True)
rev2 = subprocess.run(["git", "-C", fixture, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()
run_raw("b5_ignored_worktree", fixture, rev2,
        os.path.join(fixture, "tools/round-47/exact.py"), battery=False)

# --- b6: a legitimate corpus/knowledge citation, battery on ---------------------
fixture, rev = drive.make_repo("b6_knowledge", drive.swap_refs(
    base, "`corpus/knowledge/2026-10-13-crash-evidence.md:1-3`, "
          "`corpus/lessons/round-46.md:57-66`, `plans/round-47-claims.md:45-113`"),
    {"corpus/knowledge/2026-10-13-crash-evidence.md": KN})
ex = os.path.join(fixture, "tools/round-47/exact.py")
run_raw("b6_knowledge_nobattery", fixture, rev, ex, battery=False)
run_raw("b6_knowledge_battery", fixture, rev, ex, battery=True)

json.dump(rows, open(os.path.join(S, "receipts", "matrix2.json"), "w"), indent=1)
