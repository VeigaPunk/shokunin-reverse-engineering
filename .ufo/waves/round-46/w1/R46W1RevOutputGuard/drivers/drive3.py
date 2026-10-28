#!/usr/bin/env python3
"""E-series: escape/re-entry and repo-mutation cases on a third fresh clone."""
import hashlib, json, os, subprocess, sys, time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevOutputGuard"
LANE = os.path.join(S, "lane3")
R = os.path.join(S, "receipts3")
ATT = os.path.join(LANE, "tools/round-46/attest.py")
REV = "781e19ae674225b6be0b5de56ee8574679bac0b6"
FRZ = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
TOUCHED = "31820472784284727546808acc31b3ea1e73919b"
W = ["SKILL.md", "plans/round-46-claims.md", "tools/round-46/gate.py",
     "tools/round-46/attest.py", "corpus/SOURCES.md", ".git/refs/heads/main"]


def sha(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except (FileNotFoundError, IsADirectoryError):
        return None


def run(case, target, cwd=None, freeze=FRZ, note=""):
    cwd = cwd or LANE
    b = {w: sha(os.path.join(LANE, w)) for w in W}
    cmd = [sys.executable, "-I", "-B", ATT, "--root", LANE, "--freeze", freeze,
           "--rev", REV, "--no-battery", "--json-out", target]
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    a = {w: sha(os.path.join(LANE, w)) for w in W}
    ch = {k: [b[k], a[k]] for k in W if b[k] != a[k]}
    abs_t = os.path.realpath(os.path.join(cwd, target))
    rec = {"case": case, "note": note, "argv": cmd, "cwd": cwd, "target": target,
           "target_abs": abs_t, "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
           "stdout_head": p.stdout[:220], "stderr_tail": p.stderr[-200:],
           "changed": ch, "target_written": os.path.exists(abs_t),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    json.dump(rec, open(os.path.join(R, case + ".json"), "w"), indent=1, sort_keys=True)
    print("%-26s exit=%d changed=%s written=%s" % (case, p.returncode,
                                                   sorted(ch) or "-", rec["target_written"]))
    return rec


seat = os.path.join(LANE, ".ufo/waves/round-46/w1/R46W1RevOutputGuard")
os.makedirs(seat, exist_ok=True)
os.symlink(os.path.join(LANE, "tools"), os.path.join(LANE, ".ufo/waves/link-tools"))
os.symlink(os.path.join(LANE, "plans"), os.path.join(LANE, ".ufo/waves/link-plans"))
os.makedirs(os.path.join(LANE, ".ufo/state"), exist_ok=True)

run("E1-new-graded-file", "plans/new-file.md", note="a graded path that does not exist yet")
run("E2-graded-dir", "tools", note="a graded directory itself")
run("E4-symlink-dir-new", ".ufo/waves/link-tools/round-46/evil.py",
    note="dir symlink into tools/, new filename")
run("E5-escape-reenter", "../../../../../SKILL.md", cwd=seat,
    note="relative climb out of the seat and back onto SKILL.md")
run("E6-link-plans-new", ".ufo/waves/link-plans/new.md",
    note="dir symlink onto plans/, new filename")
run("E7-refusal-wins", "SKILL.md", freeze=TOUCHED,
    note="touched freeze AND a graded target: which check speaks")
run("E8-ref-overwrite", ".git/refs/heads/main",
    note="overwrite a branch ref through .git (silent corruption), last")
print(json.dumps({"receipts": R}, indent=1))
