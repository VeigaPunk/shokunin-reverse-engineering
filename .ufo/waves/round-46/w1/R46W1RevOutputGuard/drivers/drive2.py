#!/usr/bin/env python3
"""Clean C-series + ordering defect re-run on a FRESH clone (lane2)."""
import hashlib, json, os, shutil, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevOutputGuard"
LANE = os.path.join(S, "lane2")
RCPT = os.path.join(S, "receipts2")
os.makedirs(RCPT, exist_ok=True)
ATT = os.path.join(LANE, "tools/round-46/attest.py")
REG = os.path.join(LANE, "tools/round-46/registry.py")
REV = "781e19ae674225b6be0b5de56ee8574679bac0b6"
FRZ = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
HEAD_REV = "49e6cac4f6604986b1a7e9cfcbd9d46704dff390"
HEAD_FRZ = "04252247"  # newest declared freeze; resolved below
WATCH = ["SKILL.md", "LOG.md", "SCORECARD.md", "SHONEN.md", "PROVINCE.md",
         "plans/round-46-claims.md", "corpus/SOURCES.md",
         "tools/round-46/attest.py", "tools/round-46/gate.py",
         "tools/round-46/registry.py", ".git/config", ".git/hooks/pre-commit"]


def sha(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return "<dir>"


def snap():
    return {w: sha(os.path.join(LANE, w)) for w in WATCH}


def run(case, target, script=ATT, cwd=None, freeze=FRZ, rev=REV, root=None,
        note="", extra=()):
    cwd = cwd or LANE
    root = root or LANE
    before = snap()
    cmd = [sys.executable, "-I", "-B", script, "--root", root, "--freeze", freeze,
           "--rev", rev, "--no-battery", *extra]
    if target is not None:
        cmd += ["--json-out", target]
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    after = snap()
    changed = {k: [before[k], after[k]] for k in WATCH if before[k] != after[k]}
    rec = {"case": case, "note": note, "argv": cmd, "cwd": cwd, "target": target,
           "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
           "stdout_head": p.stdout[:300],
           "stderr_tail": p.stderr[-300:],
           "changed": changed,
           "target_abs": os.path.realpath(os.path.join(cwd, target)) if target else None,
           "target_written": bool(target) and os.path.exists(
               os.path.realpath(os.path.join(cwd, target))),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    json.dump(rec, open(os.path.join(RCPT, case + ".json"), "w"), indent=1, sort_keys=True)
    print("%-26s exit=%d changed=%s written=%s" % (
        case, p.returncode, sorted(changed) or "-", rec["target_written"]))
    return rec


seat = os.path.join(LANE, ".ufo/waves/round-46/w1/R46W1RevOutputGuard")
os.makedirs(seat, exist_ok=True)
os.makedirs(os.path.join(seat, "plans"), exist_ok=True)
os.makedirs(os.path.join(LANE, ".ufo/state"), exist_ok=True)
shutil.copyfile(os.path.join(LANE, "SKILL.md"), os.path.join(S, "SKILL2.pristine"))

run("D1-dir-target", ".ufo/waves", note="existing directory as --json-out")
run("D2-missing-dir", ".ufo/nope/x.json", note="absent parent directory")
run("D3-normal-ok", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/ok2.json",
    note="allowed receipt path, verdict 0")
run("D4-cwd-shift", "plans/round-46-claims.md", cwd=seat,
    note="same argv text, cwd moved into the seat dir")
run("D5-root-subdir-escape", os.path.join(LANE, "SKILL.md"),
    root=os.path.join(LANE, ".ufo"), note="--root narrowed to .ufo, absolute graded target")
run("D6-root-subdir-rel", "SKILL.md", root=os.path.join(LANE, ".ufo"),
    note="--root narrowed to .ufo, relative target")
run("D7-registry-graded", "tools/round-46/gate.py", script=REG,
    note="shared guard on the registry.py side")
# newest HEAD pair: same crash class must reproduce after the lane advanced
run("D8-head-dir-target", ".ufo/waves", freeze=HEAD_FRZ, rev=HEAD_REV,
    note="dir target at the lane's current HEAD")
run("D9-head-normal", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/head.json",
    freeze=HEAD_FRZ, rev=HEAD_REV, note="allowed path at the lane's current HEAD")
# hardlink bypass
hard = os.path.join(seat, "hardlink2.json")
if os.path.exists(hard):
    os.unlink(hard)
os.link(os.path.join(LANE, "SKILL.md"), hard)
run("D10-hardlink-SKILL", ".ufo/waves/round-46/w1/R46W1RevOutputGuard/hardlink2.json",
    note="hard link to SKILL.md")
shutil.copyfile(os.path.join(S, "SKILL2.pristine"), os.path.join(LANE, "SKILL.md"))
print("   repaired SKILL.md:", sha(os.path.join(LANE, "SKILL.md")))
run("D11-git-hook", ".git/hooks/pre-commit", note="write into .git/hooks")
run("D12-ufo-state", ".ufo/state/probe2.json", note="write under .ufo/state")
run("D13-git-config", ".git/config", note="write into .git/config (last, poisons git)")
g = subprocess.run(["git", "-C", LANE, "rev-parse", "HEAD"], capture_output=True, text=True)
json.dump({"case": "D14-post-config-git", "argv": ["git", "-C", LANE, "rev-parse", "HEAD"],
           "exit": g.returncode, "stdout": g.stdout[:120], "stderr": g.stderr[:200]},
          open(os.path.join(RCPT, "D14-post-config-git.json"), "w"), indent=1)
print("D14-post-config-git exit=%d %s" % (g.returncode, g.stderr.strip()[:80]))
