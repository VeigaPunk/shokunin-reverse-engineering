#!/usr/bin/env python3
"""C2 attack harness, third batch: empty newest section, brace path token, SKILL.md coupling."""
import json, os, shutil, subprocess, sys, hashlib

S = os.path.dirname(os.path.abspath(__file__))
FX0 = os.path.join(S, "fx0")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
CORR = "## Record corrections — round 47"


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


def commit(d):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", "mutate")
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def run(d, rev, battery=True):
    out = os.path.join(d, "receipt.json")
    cmd = ["python3", "-I", "-B", COUNTER, "--root", d, "--rev", rev, "--json-out", out]
    if not battery:
        cmd.append("--no-battery")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=S,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if os.path.exists(out):
        os.unlink(out)
    return {"exit": r.returncode, "cmd": " ".join(cmd),
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "sections": rec.get("sections"), "atoms": rec.get("atoms"),
            "atoms_by_class": rec.get("atoms_by_class"),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["class"] + "/" + str(e["key"]) for e in rec.get("exempted") or []],
            "mismatches": [(m["class"], str(m["key"]), m["atom"][:90],
                            json.dumps(m.get("derived"))[:200])
                           for m in rec.get("mismatches") or []],
            "failing": rec.get("failing"),
            "battery": {k: v for k, v in (rec.get("battery") or {}).items() if k != "fixtures"}}


def axes_fix(t):
    t = t.replace("| coverage | 9.72 → 10.0 | 133/133", "| coverage | 9.72 → 10.0 | 138/138")
    return t.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")


def corr(win):
    return ("\n%s\n\n" % CORR +
            "- corrects seats round-46: 2 waves, 80 seats total\n"
            "- corrects window round-46: %s\n" % win)


def main():
    rows = []

    # c15: the newest section carries ZERO atoms; the record of the round says nothing
    d = fresh("c15_empty_newest_section_green")
    t = open(os.path.join(d, "SCORECARD.md"), encoding="utf-8").read()
    t = axes_fix(t) + "\n## Round 47 — nothing measured this round\n\nNo counter was run.\n"
    t += corr("empty in 22fd0d6..22fd0d6 -- corpus/lessons/round-46-verifier-spotcheck.md")
    open(os.path.join(d, "SCORECARD.md"), "w", encoding="utf-8").write(t)
    tip = commit(d)
    rows.append({"case": "c15_empty_newest_section_green", "tip": tip, "fixture": d,
                 "note": "the single newest ## Round 47 section has zero atoms",
                 "with_battery": run(d, tip), "no_battery": run(d, tip, False)})

    # c18: a brace-expanded citation to files that do not exist, graded on its directory prefix
    d = fresh("c18_brace_path_token")
    t = open(os.path.join(d, "SCORECARD.md"), encoding="utf-8").read()
    t = t.replace("## Round 46 —",
                  "Evidence: `.ufo/waves/round-46/{nope,nada}-results.json`.\n\n## Round 46 —", 1)
    open(os.path.join(d, "SCORECARD.md"), "w", encoding="utf-8").write(t)
    tip = commit(d)
    rows.append({"case": "c18_brace_path_token", "tip": tip, "fixture": d,
                 "note": "cites two nonexistent result files; only the directory prefix is graded",
                 "no_battery": run(d, tip, False)})

    # c19: SKILL.md block 24 changes the C2-derived depth fraction (causal coupling)
    d = fresh("c19_skill_coupling")
    sk = os.path.join(d, "SKILL.md")
    body = open(sk, encoding="utf-8").read()
    anchor = "## Queue-drain craft "
    head, rest = body.split(anchor, 1)
    craft, tail = rest.split("\n## ", 1)
    craft += ("\n- **24. Exactness matrix.** Four rows, one per routed defect; cites "
              "`plans/round-47-claims.md:1-5` and `corpus/lessons/round-46.md:28-33`.\n")
    open(sk, "w", encoding="utf-8").write(head + anchor + craft + "\n## " + tail)
    tip = commit(d)
    rows.append({"case": "c19_skill_coupling", "tip": tip, "fixture": d,
                 "note": "a craft block 24 is added; the C2 counter's depth derivation moves",
                 "no_battery": run(d, tip, False)})

    for r in rows:
        print(json.dumps(r, indent=1))
        print("-" * 70)
    json.dump(rows, open(os.path.join(S, "attack3-results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
