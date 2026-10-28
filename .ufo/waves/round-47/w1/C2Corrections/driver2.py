#!/usr/bin/env python3
"""C2Corrections probe set 2: exemption vacuity, padding, false-claim exposure."""
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
D = os.path.join(S, "repo")
COUNTER = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47/record.py"
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
LAND = "e856beb552080c03ede6000b96f1b58bde44c421"
CORR = "## Record corrections — round 47"


def g(*a):
    r = subprocess.run(["git", "-C", D, *a], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("git %s: %s" % (a, r.stderr))
    return r


def show(rev, p):
    return subprocess.run(["git", "-C", D, "show", "%s:%s" % (rev, p)],
                          capture_output=True, text=True).stdout


def fixture(label, base, card):
    g("checkout", "-q", "-f", "-B", "p2-" + label, base)
    open(os.path.join(D, "SCORECARD.md"), "w").write(card)
    g("add", "-A")
    g("commit", "-q", "-m", "probe " + label)
    return g("rev-parse", "HEAD").stdout.strip()


def score(label, rev):
    out = os.path.join(D, ".ufo/waves/round-47/w1/fx2", label + ".json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-B", COUNTER, "--root", D,
                        "--rev", rev, "--json-out", out], capture_output=True,
                       text=True, env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = json.load(open(out)) if os.path.exists(out) else {"reason": "no receipt"}
    return {"label": label, "exit": r.returncode, "failing": rec.get("failing"),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "mismatches": [(m["class"], m["key"], m.get("derived")) for m in rec.get("mismatches", [])],
            "exempted": [e["atom"][:60] for e in rec.get("exempted", [])],
            "forgeries_green": (rec.get("battery") or {}).get("forgeries_green")}


SEATS = "- corrects seats round-45: 2 waves, 76 seats total"


def main():
    assert g("rev-parse", "--show-toplevel").stdout.strip() == D
    base = show(BASE, "SCORECARD.md")
    out = []
    fixed_rows = base.replace("| coverage | 9.72 → 10.0 | ", "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
                     .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)

    # Q1 padding: everything repaired in place, two corrections that exempt nothing
    c = base.replace("wave 2: 32 seats", "wave 2: 36 seats")
    c = c.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                  "58eb04b6..13a9e9e1 -- tools/round-46 plans/round-46-claims.md` is empty")
    c = c.replace("| coverage | 9.72 → 10.0 | ", "| coverage | 9.72 → 10.0 | 138/138 | ", 1) \
         .replace("| depth | 10 → 10 | ", "| depth | 10 → 10 | 23/23 | ", 1)
    c += "\n" + CORR + "\n\n" + SEATS + "\n" + \
         "- corrects path .ufo/waves/round-46/w1-dispatch.json: exists\n"
    out.append(score("q1-padding-with-real-path-token", fixture("q1", BASE, c)))

    # Q2 a window correction about unrelated paths exempts the round-46 placeholder
    c = fixed_rows.replace("wave 2: 32 seats", "wave 2: 36 seats")
    c += "\n" + CORR + "\n" + SEATS + "\n" + \
         "- corrects window round-46: empty in 332f4884..58eb04b6 -- corpus/lessons/round-46.md\n"
    out.append(score("q2-unrelated-pathspec-exempts-placeholder", fixture("q2", BASE, c)))

    # Q3 the record's original placeholder replaced by the section's own measured rev
    c = fixed_rows.replace("wave 2: 32 seats", "wave 2: 36 seats") \
        .replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                 "0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` is empty")
    c += "\n" + CORR + "\n" + SEATS + "\n" + \
         "- corrects window round-46: empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md\n"
    out.append(score("q3-original-window-is-false", fixture("q3", BASE, c)))

    # Q4 empty-in-both-ends: the landed section's window re-stated as the round-47 base..tip
    c = fixed_rows.replace("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty",
                           "58eb04b6..13a9e9e1 -- tools/round-46 plans/round-46-claims.md` is empty")
    c = c.replace("wave 2: 32 seats", "wave 2: 36 seats")
    c += "\n" + CORR + "\n" + SEATS + "\n" + \
         "- corrects window round-46: empty in 58eb04b6..13a9e9e1 -- tools/round-46 plans/round-46-claims.md\n"
    out.append(score("q4-landed-window-repair-green", fixture("q4", BASE, c)))

    # Q5 wrong-but-grammatical seats total
    c = fixed_rows + "\n" + CORR + "\n" + "- corrects seats round-45: 2 waves, 75 seats total\n" + \
        "- corrects window round-46: empty in 58eb04b6..13a9e9e1 -- tools/round-46 plans/round-46-claims.md\n"
    c = c.replace("wave 2: 32 seats", "wave 2: 36 seats")
    out.append(score("q5-seats-total-75", fixture("q5", BASE, c)))

    # Q6 landed card + a *false* window correction appended (grammar ok, window non-empty)
    land = show(LAND, "SCORECARD.md")
    c = land + "\n- corrects window round-46: empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md\n"
    out.append(score("q6-extra-false-window-line", fixture("q6", LAND, c)))

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
