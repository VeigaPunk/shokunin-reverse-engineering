#!/usr/bin/env python3
"""R46-W1 gate.out_path attack matrix, run against a scratch CLONE of the lane."""
import hashlib, json, os, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevOutputGuard"
LANE = os.path.join(S, "lane")
RCPT = os.path.join(S, "receipts")
FREEZE_OK = "65678df0f1666e83cdeea7233bfb31ffe73ec709"      # L1-measured freeze (clean)
FREEZE_PROMPT = "31820472784284727546808acc31b3ea1e73919b"  # prompt/claims freeze (touched)
REV = "781e19ae674225b6be0b5de56ee8574679bac0b6"

WATCH = [
    "SKILL.md", "LOG.md", "SCORECARD.md", "PROVINCE.md", "SHONEN.md",
    "plans/round-46-claims.md", "corpus/SOURCES.md",
    "tools/round-46/attest.py", "tools/round-46/gate.py",
    "tools/round-46/registry.py", "tools/round-46/census.py",
    "tools/round-46/census.json",
    ".git/config", ".git/hooks/pre-commit",
]


def sha(p):
    try:
        with open(p, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return "<dir>"


def snap():
    return {w: sha(os.path.join(LANE, w)) for w in WATCH}


def run(case, target, extra=(), cwd=None, script="tools/round-46/attest.py",
        freeze=FREEZE_OK, note="", root=None, battery=False):
    cwd = cwd or LANE
    root = root or LANE
    before = snap()
    cmd = [sys.executable, "-I", "-B", script, "--root", root,
           "--freeze", freeze, "--rev", REV, *extra]
    if not battery and "--selftest" not in extra:
        cmd.append("--no-battery")
    if target is not None:
        cmd += ["--json-out", target]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    dt = round(time.time() - t0, 3)
    after = snap()
    changed = {k: [before[k], after[k]] for k in WATCH if before[k] != after[k]}
    out_sha = hashlib.sha256(p.stdout.encode()).hexdigest()
    target_abs = os.path.realpath(os.path.join(cwd, target)) if target else None
    target_exists = os.path.exists(target_abs) if target_abs else False
    target_sha = sha(target_abs) if target_abs and target_exists else None
    rec = {
        "case": case, "note": note,
        "cwd": cwd, "script": script,
        "argv": cmd,
        "target": target,
        "target_abs": target_abs,
        "exit": p.returncode,
        "stdout_sha256": out_sha,
        "stdout_head": p.stdout[:400],
        "stderr_head": p.stderr[:400],
        "graded_or_watched_changed": changed,
        "target_exists_after": target_exists,
        "target_sha_after": target_sha,
        "secs": dt,
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    with open(os.path.join(RCPT, case + ".json"), "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    print("%-34s exit=%d changed=%s exists=%s out=%s" % (
        case, p.returncode, sorted(changed) or "-", target_exists, out_sha[:12]))
    return rec


os.makedirs(RCPT, exist_ok=True)
os.makedirs(os.path.join(LANE, ".ufo", "waves", "round-46", "w1", "R46W1RevOutputGuard"),
            exist_ok=True)
# --- fixtures inside the clone -------------------------------------------------
seat = os.path.join(LANE, ".ufo/waves/round-46/w1/R46W1RevOutputGuard")
os.symlink(os.path.join(LANE, "SKILL.md"), os.path.join(seat, "link-skill.json"))
os.symlink(os.path.join(LANE, "plans/round-46-claims.md"), os.path.join(seat, "link-claims.json"))
os.symlink(os.path.join(LANE, "tools"), os.path.join(seat, "link-tools"))
os.makedirs(os.path.join(seat, "plans"), exist_ok=True)
os.makedirs(os.path.join(LANE, ".ufo", "waves", "plans"), exist_ok=True)
shutil.copyfile(os.path.join(LANE, "SKILL.md"), os.path.join(S, "SKILL.pristine"))

cases = []
# A. the seat's eight named targets, cwd = lane root (natural interpretation)
cases.append(run("A1-rel-SKILL", "SKILL.md",
                 note="relative graded file at lane root"))
cases.append(run("A2-rel-dotdot-SKILL", "../../SKILL.md",
                 note="relative escape out of the lane"))
cases.append(run("A3-rel-claims", "plans/round-46-claims.md",
                 note="relative frozen claims file"))
cases.append(run("A4-rel-corpus", "corpus/SOURCES.md",
                 note="relative graded corpus file"))
cases.append(run("A5-rel-gate", "tools/round-46/gate.py",
                 note="relative frozen instrument"))
cases.append(run("A6-abs-inside-graded", os.path.join(LANE, "SKILL.md"),
                 note="absolute path inside the lane on a graded file"))
cases.append(run("A6b-abs-inside-ok", os.path.join(seat, "abs-ok.json"),
                 note="absolute path inside the lane, non-graded"))
cases.append(run("A7-abs-outside", os.path.join(S, "outside.json"),
                 note="absolute path outside the lane root"))
cases.append(run("A8-symlink-file", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/link-skill.json",
                 note="lane-internal symlink whose target is SKILL.md"))
cases.append(run("A8b-symlink-claims", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/link-claims.json",
                 note="lane-internal symlink whose target is the frozen claims file"))
cases.append(run("A8c-symlink-dir", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/link-tools/round-46/gate.py",
                 note="lane-internal directory symlink into tools/"))
cases.append(run("A9-normal-ufo", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/ok.json",
                 note="normal allowed receipt path"))
cases.append(run("A10-normalize", "plans/../SKILL.md",
                 note="dot-dot normalization inside the argument"))
cases.append(run("A11-shadow-name", ".ufo/waves/plans/round-46-claims.md",
                 note="a graded basename living under .ufo (allowed?)"))
# B. ordering / crash class
cases.append(run("B1-dir-target", ".ufo/waves",
                 note="existing directory as --json-out"))
cases.append(run("B2-missing-dir", ".ufo/does-not-exist/x.json",
                 note="--json-out whose parent directory is absent"))
cases.append(run("B3-selftest-graded-out", "SKILL.md",
                 extra=("--selftest",),
                 note="--selftest short-circuits before out_path"))
cases.append(run("B4-refusal-before-verdict", os.path.join(LANE, "SKILL.md"),
                 note="verdict would be 0; refusal must precede evaluation"))
cases.append(run("B5-exit2-verdict-writes", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/frozen-touch.json",
                 freeze=FREEZE_PROMPT,
                 note="verdict exit 2 (frozen_path_changed) with an allowed json-out"))
# C. bypasses / contract gaps
hard = os.path.join(seat, "hardlink.json")
if os.path.exists(hard):
    os.unlink(hard)
os.link(os.path.join(LANE, "SKILL.md"), hard)
cases.append(run("C1-hardlink-SKILL", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/hardlink.json",
                 note="hard link to SKILL.md (realpath cannot see it)"))
# repair SKILL.md from the pristine copy, then prove the repair
shutil.copyfile(os.path.join(S, "SKILL.pristine"), os.path.join(LANE, "SKILL.md"))
print("  repaired SKILL.md sha =", sha(os.path.join(LANE, "SKILL.md")))
cases.append(run("C2-git-config", ".git/config",
                 note="write into .git/config (repository mutation)"))
cases.append(run("C3-git-hook", ".git/hooks/pre-commit",
                 note="write into .git/hooks (code execution on next commit)"))
os.makedirs(os.path.join(LANE, ".ufo", "state"), exist_ok=True)
cases.append(run("C4-ufo-state", ".ufo/state/probe.json",
                 note="write under .ufo/state (fleet-contract forbidden)"))
cases.append(run("C5-cwd-shift", "plans/round-46-claims.md", cwd=seat,
                 note="same argument, cwd moved into a seat directory"))
cases.append(run("C6-registry-graded", "tools/round-46/gate.py",
                 script="tools/round-46/registry.py",
                 note="shared guard, registry.py side"))
cases.append(run("C7-root-subdir-escape", os.path.join(LANE, "SKILL.md"),
                 root=os.path.join(LANE, ".ufo"),
                 note="--root narrowed to .ufo; absolute graded path outside that root"))
cases.append(run("C8-root-subdir-rel", "SKILL.md",
                 root=os.path.join(LANE, ".ufo"),
                 note="--root narrowed to .ufo; relative target resolves against cwd=lane"))
print(json.dumps({"cases": len(cases), "receipts": RCPT}, indent=1))
