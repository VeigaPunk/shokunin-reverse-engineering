#!/usr/bin/env python3
"""Correction-grammar fixture driver for seat C2CorrGrammar (round 47).

Each case rewrites SCORECARD.md in a clone of the lane at the freeze revision, commits it
(the clone is the fixture repo; the lane is never written), then scores the same card with
two counter states:

  frz  = tools/round-47/record.py as committed at the freeze 5017e1f7 (the frozen rule)
  a1   = the lane working tree's record.py (carries uncommitted amendment A1)

Receipt per run: exact command, exit code, stdout sha256, UTC time.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/kaidoku-r47/C2CorrGrammar"
R = os.path.join(S, "rec")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
H8 = "5017e1f7"
TIP8 = "3186f69b"
CORR_HEAD = "## Record corrections — round 47"
FRZ = os.path.join(R, "tools/round-47/record-frz.py")
A1 = os.path.join(LANE, "tools/round-47/record.py")

BASE = subprocess.run(["git", "-C", R, "show", FREEZE + ":SCORECARD.md"],
                      capture_output=True, text=True, check=True).stdout

OLD_WIN = ("0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at "
           "every measurement above.")
AXES_COV = "| coverage | 9.72 → 10.0 | 133/133 "
AXES_DEPTH = "| depth | 10 → 10 | 20/20 "


def sub(card, old, new, why):
    if old not in card:
        raise SystemExit(f"anchor missing ({why}): {old[:80]!r}")
    return card.replace(old, new, 1)


def corr(lines):
    return "\n\n" + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def win(card, pair, paths, extra=""):
    return sub(card, OLD_WIN,
               f"{pair} -- {paths}` is empty at every measurement above.{extra}",
               "window sentence")


def axes(card, cov, depth):
    card = sub(card, AXES_COV, f"| coverage | 9.72 → 10.0 | {cov} ", "coverage row")
    return sub(card, AXES_DEPTH, f"| depth | 10 → 10 | {depth} ", "depth row")


def git(*a):
    return subprocess.run(["git", "-C", R, *a], capture_output=True, text=True)


def commit(card, name):
    with open(os.path.join(R, "SCORECARD.md"), "w") as fh:
        fh.write(card)
    git("add", "SCORECARD.md")
    c = git("commit", "-q", "--allow-empty", "-m", "case " + name)
    if c.returncode != 0:
        raise SystemExit("commit failed: " + c.stderr)
    return git("rev-parse", "HEAD").stdout.strip()


def run(counter, label, case, rev, outdir):
    out = os.path.join(outdir, f"{case}.{label}.json")
    cmd = [sys.executable, "-I", "-B", counter, "--root", R, "--rev", rev,
           "--json-out", out]
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    p = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = {}
    if os.path.exists(out):
        with open(out) as fh:
            rec = json.load(fh)
    return {"case": case, "counter": label, "counter_sha256":
            hashlib.sha256(open(counter, "rb").read()).hexdigest(),
            "cmd": " ".join(cmd), "exit": p.returncode,
            "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
            "utc": t0, "stderr_head": p.stderr.strip().splitlines()[:2],
            "failing": rec.get("failing"),
            "mismatches": [{"class": m["class"], "key": m["key"]}
                           for m in rec.get("mismatches", [])],
            "corrections": rec.get("corrections"),
            "corrections_bad": [d.get("detail") for d in rec.get("corrections_bad", [])],
            "exempted": len(rec.get("exempted", [])),
            "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                        if k in ("correction_forgeries", "forgeries_green")} or None,
            "met_target": rec.get("met_target")}


SEATS = "- corrects seats round-45: 2 waves, 76 seats total"


def main():
    if git("rev-parse", "--show-toplevel").stdout.strip() != R:
        raise SystemExit("fixture toplevel mismatch")
    git("checkout", "-q", "-B", "grammar", FREEZE)
    # a side commit that resolves but is not an ancestor of the graded branch
    git("checkout", "-q", "-B", "side", FREEZE)
    open(os.path.join(R, "side-note.txt"), "w").write("off-branch measurement\n")
    git("add", "side-note.txt")
    git("commit", "-q", "-m", "side measurement")
    side = git("rev-parse", "HEAD").stdout.strip()[:8]
    git("checkout", "-q", "grammar")
    git("branch", "-f", "grammar", FREEZE)
    if os.path.exists(os.path.join(R, "side-note.txt")):
        os.remove(os.path.join(R, "side-note.txt"))

    outdir = os.path.join(R, "receipts")
    os.makedirs(outdir, exist_ok=True)
    ledger = os.path.join(S, "bin", "ledger.jsonl")
    open(ledger, "w").close()

    cases = {}

    # c01 — do-nothing card
    cases["c01-baseline"] = BASE

    # c02 — the round-45/46 appendix wording pasted as a corrections section
    cases["c02-foreign-wording"] = BASE + corr([
        "- corrects seats round-45: Wave 1: 40 seats; wave 2: 36 seats (counts from "
        "`.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)",
        "- corrects window round-46: `git log 0425224..<tip> -- tools/round-46 "
        "plans/round-46-claims.md` is empty at every measurement above",
        "- corrects axes coverage: 138/138",
    ])

    # c03 — prose that happens to embed the magic substrings
    cases["c03-prose-with-magic-phrase"] = BASE + corr([
        "- corrects seats round-45: wave 2 was not dispatched as written; the true "
        "arithmetic is 2 waves, 76 seats total",
        "- corrects window round-46: the placeholder is superseded; empty in "
        "5017e1f7..5017e1f7 -- tools/round-46",
    ])

    # c04 — the minimal correct lines, rows untouched
    cases["c04-minimal-freeze"] = BASE + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- tools/round-46",
    ])

    # c05 — c04 plus the axes correction lines the claims file says are expressible
    cases["c05-axes-correction-line"] = BASE + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- tools/round-46",
        "- corrects axes coverage: 138/138",
        "- corrects axes depth: 23/23",
    ])

    # c06 — axes rows edited, seats corrected, and an honest window correction:
    #       a real range over the frozen tools path, empty because nothing changed there
    c06 = axes(win(BASE, "5017e1f7..3186f69b", "tools/round-47/"), "138/138", "23/23")
    cases["c06-row-edit-honest-window"] = c06 + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..3186f69b -- tools/round-47/",
    ])

    # c07 — axes rows edited, seats corrected, window claim left as the <tip> placeholder
    cases["c07-row-edit-placeholder-window"] = axes(BASE, "138/138", "23/23") + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- tools/round-46",
    ])

    # c08 — axes rows edited, window sentence rewritten to X..X, correction restating it
    c08 = axes(win(BASE, "5017e1f7..5017e1f7", "SCORECARD.md"), "138/138", "23/23")
    cases["c08-rewrite-vacuous-window"] = c08 + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- SCORECARD.md",
    ])

    # c09 — a false window claim (0425224..1e32827b over .ufo/waves/round-46/ is not
    #       empty) exempted by a correction naming a path that does not exist; the
    #       battery's mutation anchor is the harmless X..X line, listed first
    c09 = axes(win(BASE, "0425224..1e32827b", ".ufo/waves/round-46/",
                   "\n\nA second window, `5017e1f7..5017e1f7 -- SCORECARD.md`, "
                   "is empty."),
               "138/138", "23/23")
    cases["c09-pathspec-substitution"] = c09 + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- SCORECARD.md",
        "- corrects window round-46: empty in 0425224..1e32827b -- no/such/path.md",
    ])

    # c12 — the same two window corrections, vacuous line first: the battery's single
    #       mutation now lands on the vacuous line and the forgery survives
    cases["c12-vacuous-first"] = c09 + corr([
        SEATS,
        "- corrects window round-46: empty in 0425224..1e32827b -- no/such/path.md",
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- SCORECARD.md",
    ])

    # c13 — a false window claim written on the same physical line as a true one: only
    #       the first pair on a line becomes an atom
    c13 = axes(sub(BASE, OLD_WIN,
                   "5017e1f7..5017e1f7 -- SCORECARD.md` is empty at every measurement "
                   "above, and `0425224..1e32827b -- .ufo/waves/round-46/` is empty too.",
                   "c13 two windows"), "138/138", "23/23")
    cases["c13-line-blind-window"] = c13 + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..5017e1f7 -- SCORECARD.md",
    ])

    # c14 — a correction for a round older than the last two: no atom required
    c14 = axes(win(BASE, "5017e1f7..3186f69b", "tools/round-47/"), "138/138", "23/23")
    cases["c14-historical-correction"] = c14 + corr([
        SEATS,
        "- corrects window round-46: empty in 5017e1f7..3186f69b -- tools/round-47/",
        "- corrects window round-44: empty in 5017e1f7..5017e1f7 -- SCORECARD.md",
    ])

    # c15 — the heading with an ASCII hyphen instead of the em dash: every line in the
    #       section is invisible to the counter
    c15 = axes(win(BASE, "5017e1f7..3186f69b", "tools/round-47/"), "138/138", "23/23")
    cases["c15-heading-hyphen"] = c15 + ("\n\n## Record corrections - round 47\n\n"
        "- corrects seats round-45: 2 waves, 76 seats total\n"
        "- corrects window round-46: empty in 5017e1f7..3186f69b -- tools/round-47/\n")

    # c10 — a path atom whose file does not exist, "corrected" by a line that says so
    c10 = axes(BASE, "138/138", "23/23")
    c10 = sub(c10, "` is empty at every measurement above.",
              "` is empty at every measurement above. The superseded dispatch "
              "`.ufo/waves/round-46/gone-dispatch.json` was retired.", "c10 path atom")
    cases["c10-path-inert"] = c10 + corr([
        SEATS,
        "- corrects path .ufo/waves/round-46/gone-dispatch.json: retired, not re-derived",
    ])

    # c11 — a commit that resolves but is off the graded branch, waived with no content
    c11 = axes(BASE, "138/138", "23/23")
    c11 = sub(c11, "` is empty at every measurement above.",
              f"` is empty at every measurement above. Measured at `{side}`.", "c11 rev")
    cases["c11-rev-vacuous"] = c11 + corr([
        SEATS,
        f"- corrects rev {side}: off-branch side measurement, kept for provenance",
    ])

    for name in cases:
        rev = commit(cases[name], name)
        row = {"case": name, "rev": rev, "seed": FREEZE}
        for label, counter in (("frz", FRZ), ("a1", A1)):
            r = run(counter, label, name, rev, outdir)
            row[label] = {k: r[k] for k in ("exit", "stdout_sha256", "utc", "failing",
                                            "mismatches", "corrections",
                                            "corrections_bad", "exempted", "battery",
                                            "met_target", "cmd", "counter_sha256",
                                            "stderr_head")}
        with open(ledger, "a") as fh:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
        print(name, "| frz", row["frz"]["exit"], row["frz"]["failing"],
              "| a1", row["a1"]["exit"], row["a1"]["failing"])
    print("SIDE", side)


if __name__ == "__main__":
    main()
