#!/usr/bin/env python3
"""Frozen-bytes experiment: was R47-C2's target unreachable at freeze 5017e1f (A1's claim)?

frozen  = tools/round-47/record.py @ 5017e1f (sha256 af666ce2…)
current = the lane worktree record.py (post A1..A5)
"""
import json, os, subprocess, sys, hashlib

S = os.path.dirname(os.path.abspath(__file__))
FX0 = os.path.join(S, "fx0")
FROZEN = os.path.join(S, "frozen/tools/round-47/record.py")
CURRENT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py"
CORR = "## Record corrections — round 47"
HIDE_45 = ("## Round 45 — the freeze rule becomes an instrument with four red arms; "
           "the registry names the six claim-carrying instruments")
PATH_ATOM = ".ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json"


def sh(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED %s: %s %s" % (" ".join(a), r.stdout, r.stderr))
    return r


def fresh(name):
    d = os.path.join(S, "fx-" + name)
    if os.path.exists(d):
        subprocess.run(["rm", "-rf", d], check=True)
    sh("git", "clone", "-q", FX0, d)
    sh("git", "-C", d, "config", "user.email", "st@r47")
    sh("git", "-C", d, "config", "user.name", "r47 fixture")
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d
    return d


def write_commit(d, text):
    p = os.path.join(d, "SCORECARD.md")
    assert text != open(p, encoding="utf-8").read()
    open(p, "w", encoding="utf-8").write(text)
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", "mutate")
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def run(script, d, rev):
    out = os.path.join(d, "r.json")
    r = subprocess.run(["python3", "-I", "-B", script, "--root", d, "--rev", rev,
                        "--json-out", out], capture_output=True, text=True, cwd=S,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if os.path.exists(out):
        os.unlink(out)
    return {"exit": r.returncode, "mismatches": len(rec.get("mismatches") or []),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["class"] + "/" + str(e["key"]) for e in rec.get("exempted") or []],
            "failing": rec.get("failing")}


def axes_fix(t):
    t = t.replace("| coverage | 9.72 → 10.0 | 133/133", "| coverage | 9.72 → 10.0 | 138/138")
    return t.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")


TWO = ("\n%s\n\n" % CORR +
       "- corrects seats round-45: 2 waves, 76 seats total\n"
       "- corrects path %s: landed\n" % PATH_ATOM)

CASES = {}

# (a) the honest repair the frozen clause allowed: state a concrete, true, empty window in place
CASES["f1_rewrite_window_in_place"] = lambda t: axes_fix(t).replace(
    "0425224..<tip> -- tools/round-46 plans/round-46-claims.md",
    "f762b72..c011299 -- tools/round-47/") + TWO
# (b) keep the placeholder and exempt it with an unrelated true window
CASES["f2_keep_placeholder_exempt"] = lambda t: axes_fix(t) + TWO + (
    "- corrects window round-46: empty in 22fd0d6..22fd0d6 -- "
    "corpus/lessons/round-46-verifier-spotcheck.md\n")
# (c) the c10 forgery: fenced heading hides the round-45 body, false seats sentence retained
CASES["f3_fence_hides_round45"] = lambda t: axes_fix(t).replace(
    HIDE_45, HIDE_45 + "\n```\n## note: everything below is background\n```\n", 1) + (
    "\n%s\n\n" % CORR +
    "- corrects seats round-46: 2 waves, 80 seats total\n"
    "- corrects window round-46: empty in 22fd0d6..22fd0d6 -- "
    "corpus/lessons/round-46-verifier-spotcheck.md\n")


def main():
    rows = []
    for name, mut in CASES.items():
        d = fresh(name)
        tip = write_commit(d, mut(open(os.path.join(d, "SCORECARD.md"),
                                       encoding="utf-8").read()))
        raw = open(os.path.join(d, "SCORECARD.md"), encoding="utf-8").read()
        rows.append({"case": name, "fixture": d, "tip": tip,
                     "false_sentence_present": "wave 2: 32 seats" in raw,
                     "frozen_5017e1f": run(FROZEN, d, tip),
                     "current_worktree": run(CURRENT, d, tip)})
        print(json.dumps(rows[-1], indent=1))
        print("-" * 70)
    json.dump(rows, open(os.path.join(S, "frozen-experiment.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
