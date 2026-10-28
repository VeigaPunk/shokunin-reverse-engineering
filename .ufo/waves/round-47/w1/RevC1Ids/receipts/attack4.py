#!/usr/bin/env python3
"""Round-47 C1 clause-4 attack: build one-commit fixture repos from the landed
SKILL.md and score each with tools/round-47/exact.py (frozen at 62e33f7d).

Every fixture is `git init`'d inside HYAKU_SCRATCH, its toplevel asserted, and the
counter invoked as a subprocess so the exit code is the counter's own.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EXACT = os.path.join(LANE, "tools/round-47/exact.py")
S = os.environ["HYAKU_SCRATCH"]
REV = "HEAD"
FILES = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
         "tools/round-46/gate.py", "corpus/lessons/round-46.md",
         "corpus/lessons/round-45.md"]
HEADER = "| trigger | v2 hole | v3 arm | exit |"
SEP = "|---|---|---|---|"

BASE = [
    ("R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test",
     "containment over a lowercased cell, so any superstring passes", "`symbol`", "1"),
    ("R46-CL3 a row claims a routed id another row already addresses",
     "the id check asks whether the id appears in *some* row", "`once`", "1"),
    ("R46-CL4 deleting a mutation changes the denominator the claim is judged on",
     "`forgeries_total` is compared with a number the code computes, and nothing pins the list",
     "`digest`", "1"),
    ("R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice and blinds the arm",
     "the argument order is a convention no clause reads", "`order`", "1"),
]


def rows_of(spec):
    return ["| " + " | ".join(r) + " |" for r in spec]


def cases():
    b = [list(r) for r in BASE]
    out = []

    def add(name, spec, expect, why):
        out.append({"name": name, "rows": spec, "expect": expect, "why": why})

    add("c4-0-genuine", b, 0, "the landed table, untouched (control)")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL2 and R46-CL3 the substring arm test"
    add("c4-1-two-ids", r, 1, "one trigger cell names two routed ids")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL2 R46-CL3 the substring arm test"
    r[1][0] = "the once-hole, no id named here"
    add("c4-2-two-ids-plus-empty", r, 1,
        "two ids in one cell, none in another: the 4-id multiset is exact, per-row is not")

    r = [list(x) for x in b]
    r[1][0] = "the once-hole, no id named here"
    add("c4-3-no-id", r, 1, "one trigger cell names no routed id")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL7 the substring arm test"
    add("c4-4-id-outside-frozen-set", r, 1, "an id outside {CL2,CL3,CL4,CL6} in place of CL2")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL7 R46-CL2 the substring arm test"
    add("c4-5-extra-id-beside-real", r, 1, "a real id plus a non-frozen id in one cell")

    r = [list(x) for x in b]
    r[1][0] = "R46-CL2 a row claiming an id row 1 already addresses"
    add("c4-6-same-id-two-rows", r, 1, "R46-CL2 twice across two rows, R46-CL3 nowhere")

    r = [list(x) for x in b]
    r[0][0] = "the substring arm test"
    r[0][1] = "R46-CL2 containment over a lowercased cell, so any superstring passes"
    add("c4-7-id-in-v2-hole-cell", r, 1, "the id sits in the v2-hole cell, trigger cell names none")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL2x the substring arm test"
    add("c4-8-id-with-suffix", r, 0, "HOLE: `R46-CL2x` is no routed id but ID.findall matches R46-CL2")

    r = [list(x) for x in b]
    r[0][0] = "no R46-CL2 defect is addressed by this row"
    add("c4-9-id-in-a-negation", r, 0, "HOLE: naming is not addressing; a negated id passes")

    r = [list(x) for x in b]
    r[0][2], r[1][2], r[2][2], r[3][2] = "`order`", "`digest`", "`once`", "`symbol`"
    add("c4-10-arm-permutation", r, 0,
        "HOLE: arm cells are checked as a vocabulary set, never bound to their row's id")

    r = [list(x) for x in b]
    r[0][0] = "R46-CL2 R46-CL2 the substring arm test"
    add("c4-11-id-twice-one-cell", r, 1, "one cell names the same id twice")

    r = [list(x) for x in b]
    for i, row in enumerate(r):
        row[1] = row[1] + " (also routed as " + ["R46-CL2", "R46-CL3", "R46-CL4", "R46-CL6"][i] + ")"
    add("c4-12-ids-also-in-hole-cells", r, 0,
        "control: ids repeated in non-trigger cells are not counted again (not a defect)")
    return out


def build(skill_base, rows):
    lines = skill_base.splitlines()
    i = lines.index(HEADER)
    if lines[i + 1].strip() != SEP:
        raise SystemExit("unexpected separator line: %r" % lines[i + 1])
    new = lines[:i] + [HEADER, SEP] + rows + lines[i + 6:]
    return "\n".join(new) + ("\n" if skill_base.endswith("\n") else "")


def run(cmd, env):
    p = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout


def main():
    env = dict(os.environ)
    env["HYAKU_SCRATCH"] = S
    env["TMPDIR"] = S
    skill_base = subprocess.run(
        ["git", "-C", LANE, "show", REV + ":SKILL.md"],
        capture_output=True, text=True, check=True).stdout
    bodies = {}
    for p in FILES[1:]:
        bodies[p] = subprocess.run(["git", "-C", LANE, "show", REV + ":" + p],
                                   capture_output=True, text=True, check=True).stdout
    results = []
    for c in cases():
        d = subprocess.run(["mktemp", "-d", "-p", S, "fx-" + c["name"] + "-XXXX"],
                           capture_output=True, text=True, check=True).stdout.strip()
        subprocess.run(["git", "-C", d, "init", "-q"], check=True)
        for k, v in (("user.email", "fx@round47"), ("user.name", "clause4 fixture")):
            subprocess.run(["git", "-C", d, "config", k, v], check=True)
        top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit("toplevel mismatch %s != %s" % (top, d))
        files = dict(bodies)
        files["SKILL.md"] = build(skill_base, rows_of(c["rows"]))
        for p, text in files.items():
            full = os.path.join(d, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as fh:
                fh.write(text)
        key = hashlib.sha256(files["SKILL.md"].encode()).hexdigest()
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture " + c["name"]],
                       check=True)
        frev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                              capture_output=True, text=True, check=True).stdout.strip()
        cmd = [sys.executable, "-I", "-B", EXACT, "--root", d, "--freeze", frev,
               "--rev", frev, "--no-battery"]
        v3, out3 = run(cmd, env)
        v2, out2 = run(cmd + ["--profile", "v2"], env)
        rec = {"name": c["name"], "why": c["why"], "expect": c["expect"],
               "fixture": d, "rev": frev, "skill_sha256": key,
               "command": " ".join(cmd), "v3_exit": v3, "v2_exit": v2,
               "v3_stdout_sha256": hashlib.sha256(out3.encode()).hexdigest(),
               "v2_stdout_sha256": hashlib.sha256(out2.encode()).hexdigest()}
        try:
            rec["v3_failing"] = json.loads(out3).get("failing")
            rec["v3_routed_counts"] = json.loads(out3).get("routed_counts")
            rec["v3_arm_tokens"] = json.loads(out3).get("arm_tokens")
            rec["v2_failing"] = json.loads(out2).get("failing")
        except Exception:
            rec["v3_raw"] = out3[:400]
        rec["verdict"] = ("AS-EXPECTED" if v3 == c["expect"] else "MISMATCH")
        results.append(rec)
        print("%-28s v3=%d v2=%d expect=%d %s" % (c["name"], v3, v2, c["expect"],
                                                  rec["verdict"]))
    with open(os.path.join(S, "c4-results.json"), "w") as fh:
        json.dump(results, fh, indent=1)
    holes = [r for r in results if r["v3_exit"] == 0 and r["expect"] == 1] + \
            [r for r in results if r["verdict"] == "MISMATCH"]
    print("\nHOLES:", [r["name"] for r in holes] or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main())
