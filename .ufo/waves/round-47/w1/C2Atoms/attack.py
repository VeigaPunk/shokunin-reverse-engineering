#!/usr/bin/env python3
"""C2Atoms attack harness for tools/round-47/record.py (R47-C2).

Scores forged SCORECARD.md cards with a PINNED COPY of the counter (never the lane
worktree copy, which is moving) inside a one-branch fixture clone.

usage: attack.py --counter-rev <rev> [--only S3]
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r47/C2Atoms"
BASE = "e856beb552080c03ede6000b96f1b58bde44c421"      # round-47 landing
FIXTURE = os.path.join(SCRATCH, "fixture")


def sh(*args, cwd=None, check=False):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=check)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def materialize(rev):
    """Counter + gate at `rev` into scratch; never touch the lane worktree copy."""
    root = os.path.join(SCRATCH, "counter", rev)
    for rel in ("tools/round-47/record.py", "tools/round-46/gate.py"):
        dst = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        body = sh("git", "-C", LANE, "show", f"{rev}:{rel}")
        if body.returncode != 0:
            sys.exit(f"cannot read {rel} at {rev}: {body.stderr}")
        open(dst, "w").write(body.stdout)
    counter = os.path.join(root, "tools/round-47/record.py")
    return counter, sha(open(counter).read())


def fixture(base_rev):
    if os.path.isdir(FIXTURE):
        shutil.rmtree(FIXTURE)
    os.makedirs(FIXTURE)
    sh("git", "clone", "-q", "--no-hardlinks", LANE, FIXTURE, check=True)
    top = sh("git", "-C", FIXTURE, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(FIXTURE), (top, FIXTURE)
    sh("git", "-C", FIXTURE, "config", "user.email", "c2atoms@fixture.invalid")
    sh("git", "-C", FIXTURE, "config", "user.name", "C2Atoms")
    sh("git", "-C", FIXTURE, "checkout", "-q", "--detach", base_rev, check=True)
    return FIXTURE


CARD_BASE = [BASE]


def run_card(counter, name, card_text):
    path = os.path.join(FIXTURE, "SCORECARD.md")
    open(path, "w").write(card_text)
    top = sh("git", "-C", FIXTURE, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(FIXTURE), top
    sh("git", "-C", FIXTURE, "add", "SCORECARD.md", check=True)
    if sh("git", "-C", FIXTURE, "status", "--porcelain").stdout.strip():
        sh("git", "-C", FIXTURE, "commit", "-qm", f"attack {name}", check=True)
    rev = sh("git", "-C", FIXTURE, "rev-parse", "HEAD").stdout.strip()
    env = dict(os.environ, HYAKU_SCRATCH=SCRATCH, TMPDIR=SCRATCH)
    r = subprocess.run([sys.executable, "-I", "-B", counter, "--root", FIXTURE,
                        "--rev", rev], capture_output=True, text=True, env=env)
    try:
        rec = json.loads(r.stdout)
    except ValueError:
        rec = {"stdout": r.stdout, "stderr": r.stderr}
    out = {"name": name, "commit": rev, "card_sha256": sha(card_text),
           "stdout_sha256": sha(r.stdout), "exit": r.returncode,
           "failing": rec.get("failing"), "mismatches": [
               {"class": m["class"], "key": m["key"]} for m in rec.get("mismatches", [])],
           "exempted": [{"class": e["class"], "key": e["key"]}
                        for e in rec.get("exempted", [])],
           "corrections": rec.get("corrections"),
           "corrections_bad": rec.get("corrections_bad"),
           "atoms": rec.get("atoms"), "verified": rec.get("verified"),
           "battery": rec.get("battery"), "met_target": rec.get("met_target")}
    sh("git", "-C", FIXTURE, "reset", "-q", "--hard", CARD_BASE[0], check=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter-rev", required=True)
    ap.add_argument("--only")
    ap.add_argument("--card-rev", default=BASE)
    args = ap.parse_args()
    counter, counter_sha = materialize(args.counter_rev)
    fixture(args.card_rev)
    CARD_BASE[0] = args.card_rev
    base = sh("git", "-C", FIXTURE, "show", f"{args.card_rev}:SCORECARD.md").stdout
    corr_head = "## Record corrections — round 47"
    wline = ("- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 "
             "plans/round-46-claims.md")
    scenarios = {}

    scenarios["S0-control-landing-unchanged"] = base

    scenarios["S1-axes-correction-false"] = base.replace(
        "- corrects axes coverage: 138/138", "- corrects axes coverage: 999/999")

    scenarios["S2-no-corrections-section"] = base.split(corr_head)[0]

    scenarios["S3-window-laundered-unrelated-path"] = base.replace(
        wline,
        "- corrects window round-46: empty in 13a9e9e1..e856beb5 -- corpus/knowledge")

    scenarios["S3b-window-correction-false-window"] = base.replace(
        wline,
        "- corrects window round-46: empty in 0425224..332f4884 -- tools/round-46 "
        "plans/round-46-claims.md")

    scenarios["S4-window-correction-ends-at-rev"] = None  # built in run() with rev

    synth = (
        "\n## Round 47 — synthetic scope\n\n"
        "Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. Freeze `5017e1f7`. "
        "Dispatch `.ufo/waves/round-47/w1-dispatch.json`.\n\n"
        "Wave 1: 75 seats; wave 2: 0 seats.\n\n"
        "`git log 13a9e9e1..e856beb5 -- corpus/knowledge` is empty at every measurement "
        "above.\n\n"
        "## Round 48 — placeholder\n\nNo atoms.\n")
    scenarios["S5-scope-rollforward-no-corrections"] = base.split(corr_head)[0] + synth
    scenarios["S6-historical-corrections-only"] = base + synth
    scenarios["S6b-historical-seats-total-wrong"] = (base + synth).replace(
        "- corrects seats round-45: 2 waves, 76 seats total",
        "- corrects seats round-45: 2 waves, 77 seats total")
    scenarios["S7-contentless-path-correction"] = base + (
        "\n- corrects path .ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json: "
        "nothing is re-derived here\n")

    # the round appends its own section AFTER the corrections section (natural order)
    scenarios["S8-round-section-appended-after-corrections"] = base + synth.split(
        "## Round 48")[0]

    # a *false* "is empty" claim made green by a pathspec that names nothing
    scenarios["S11-window-atom-bogus-pathspec"] = base.replace(
        "0425224..<tip> -- tools/round-46 plans/round-46-claims.md",
        "0425224..13a9e9e1 -- corpuss/round-46")

    results = {"counter_rev": args.counter_rev, "counter_sha256": counter_sha,
               "card_rev": args.card_rev, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                         time.gmtime()),
               "scenarios": []}
    for name, text in scenarios.items():
        if args.only and args.only not in name:
            continue
        if name.startswith("S4"):
            rev_before = sh("git", "-C", FIXTURE, "rev-parse", "HEAD").stdout.strip()
            text = base.replace("332f4884..58eb04b6", f"332f4884..{rev_before}")
            res = run_card(counter, name, text)
        else:
            res = run_card(counter, name, text)
        results["scenarios"].append(res)
        print(f"{name}: exit={res['exit']} failing={res['failing']} "
              f"corrections={res['corrections']} exempted={len(res['exempted'] or [])} "
              f"mismatches={len(res['mismatches'] or [])} "
              f"battery={res['battery'] and (res['battery']['correction_forgeries'], res['battery']['forgeries_green'])}")
    json.dump(results, open(os.path.join(SCRATCH, "attacks.json"), "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
