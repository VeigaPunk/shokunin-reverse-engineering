#!/usr/bin/env python3
"""C2 attack harness: clone fx0, mutate SCORECARD.md, commit, run record.py at the tip."""
import json, os, re, shutil, subprocess, sys, time

S = os.path.dirname(os.path.abspath(__file__))
FX0 = os.path.join(S, "fx0")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"
CORR = "## Record corrections — round 47"


def sh(*args, cwd=None, check=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise SystemExit("FAILED %s: %s %s" % (" ".join(args), r.stdout, r.stderr))
    return r


def fresh(name):
    d = os.path.join(S, "fx-" + name)
    if os.path.exists(d):
        shutil.rmtree(d)
    sh("git", "clone", "-q", FX0, d)
    sh("git", "-C", d, "config", "user.email", "st@r47")
    sh("git", "-C", d, "config", "user.name", "r47 fixture")
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d
    return d


def commit(d, msg):
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", msg)
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def run(d, extra=()):
    out = os.path.join(d, "receipt.json")
    cmd = ["python3", "-I", "-B", COUNTER, "--root", d, "--rev", "HEAD",
           "--json-out", out, *extra]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       cwd=S, env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    os.unlink(out)
    return {"case": os.path.basename(d), "exit": r.returncode,
            "cmd": " ".join(cmd), "stdout_sha256": __import__("hashlib").sha256(
                r.stdout.encode()).hexdigest(),
            "sections": rec.get("sections"), "atoms": rec.get("atoms"),
            "atoms_by_class": rec.get("atoms_by_class"),
            "mismatches": [{"class": m["class"], "key": m["key"], "atom": m["atom"][:90]}
                           for m in rec.get("mismatches", [])],
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": rec.get("exempted"), "failing": rec.get("failing"),
            "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                        if k != "fixtures"},
            "battery_fixtures": (rec.get("battery") or {}).get("fixtures")}


def card(d):
    p = os.path.join(d, "SCORECARD.md")
    return p, open(p, encoding="utf-8").read()


def write(d, text):
    p = os.path.join(d, "SCORECARD.md")
    old = open(p, encoding="utf-8").read()
    if text == old:
        raise SystemExit("MUTATION WAS A NO-OP in %s" % d)
    open(p, "w", encoding="utf-8").write(text)
    return commit(d, "mutate card")


def fix_axes(text, cov="138/138", depth="23/23"):
    text = text.replace("| coverage | 9.72 → 10.0 | 133/133",
                        "| coverage | 9.72 → 10.0 | %s" % cov)
    text = text.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | %s" % depth)
    return text


CASES = {}


def case(fn):
    CASES[fn.__name__] = fn
    return fn


@case
def c0_base_replicate(d):
    return d, {}


@case
def c1_zero_atom_class(d):
    _, t = card(d)
    # drop the only window atom: remove the `is empty` phrasing
    t = t.replace("is empty at every measurement above", "was measured above")
    return write(d, t), {"mutation": "removed the only window sentence"}


@case
def c2a_empty_newest_section(d):
    _, t = card(d)
    t += "\n## Round 47 — no atoms, no work\n\nNothing was measured this round.\n"
    return write(d, t), {"mutation": "appended an atom-free ## Round 47 section"}


@case
def c2b_green_with_false_seats(d):
    _, t = card(d)
    t = fix_axes(t)
    t += ("\n## Round 47 — no atoms, no work\n\nNothing was measured this round.\n")
    tip = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    t += ("\n%s\n\n" % CORR +
          "- corrects window round-46: empty in %s..%s -- tools/round-46\n"
          % (tip[:7], tip[:7]) +
          "- corrects path .ufo/waves/round-45/w2-dispatch.json: landed\n")
    return write(d, t), {"mutation": "axes fixed + atom-free decoy section + "
                                    "tautological window correction + path correction",
                         "note": "the false `wave 2: 32 seats` sentence is still in the card"}


@case
def c3a_fenced_true_seats(d):
    _, t = card(d)
    t = t.replace("## Round 46 —", "```\nWaves: 1 + 1 = 2 seats\n```\n\n## Round 46 —", 1)
    return write(d, t), {"mutation": "fenced illustrative `Waves:` line in round-46 section"}


@case
def c3b_fenced_false_seats(d):
    _, t = card(d)
    t = t.replace("## Round 46 —", "```\nWaves: 9 + 9 = 99 seats\n```\n\n## Round 46 —", 1)
    return write(d, t), {"mutation": "fenced FALSE `Waves:` line (an example, not a claim)"}


@case
def c4_fenced_round_heading(d):
    _, t = card(d)
    t += "\n```\n## Round 99 — sample heading inside a code fence\n```\n"
    return write(d, t), {"mutation": "a `## Round 99` heading inside a fenced block"}


@case
def c5_fenced_heading_truncates(d):
    _, t = card(d)
    # a fenced `## note` line early in the round-45 section cuts the section body there
    t = t.replace("| claim | axis / surface | before | after |",
                  "```\n## note: the table below is illustrative\n```\n\n"
                  "| claim | axis / surface | before | after |", 1)
    return write(d, t), {"mutation": "a `## note` line inside a fence truncates the "
                                     "round-45 section body at that line"}


@case
def c6_axes_correction_unreachable(d):
    _, t = card(d)
    tip = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    t += ("\n%s\n\n" % CORR +
          "- corrects axes coverage: 138/138\n" +
          "- corrects window round-46: empty in %s..%s -- tools/round-46\n"
          % (tip[:7], tip[:7]) +
          "- corrects path .ufo/waves/round-45/w2-dispatch.json: landed\n")
    return write(d, t), {"mutation": "an `- corrects axes coverage:` line"}


@case
def c7_first_fraction(d):
    _, t = card(d)
    # put a TRUE fraction before the stale observable sentence in the same row
    t = t.replace("| coverage | 9.72 → 10.0 | 133/133",
                  "| coverage | 9.72 → 10.0 138/138 | 133/133")
    t = t.replace("| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")
    return write(d, t), {"mutation": "coverage row: a true 138/138 inserted in the score "
                                    "cell, the false `133/133 knowledge files mapped` left"}


@case
def c8_no_seats_correction(d):
    _, t = card(d)
    t = fix_axes(t)
    t += ("\n## Round 47 — no atoms, no work\n\nNothing was measured this round.\n")
    tip = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    t += ("\n%s\n\n" % CORR +
          "- corrects window round-46: empty in %s..%s -- tools/round-46\n"
          % (tip[:7], tip[:7]) +
          "- corrects path .ufo/waves/round-45/w2-dispatch.json: landed\n")
    return write(d, t), {"mutation": "same as c2b"}


@case
def c9_path_scope(d):
    _, t = card(d)
    t = t.replace("## Round 46 —",
                  "See `corpus/knowledge/2026-99-99-does-not-exist.md` for the proof.\n\n"
                  "## Round 46 —", 1)
    return write(d, t), {"mutation": "a false non-wave path claim inside a round section"}


def main(only):
    rows = []
    for name, fn in CASES.items():
        if only and name not in only:
            continue
        d = fresh(name)
        tip, meta = fn(d)
        rec = run(d, ("--no-battery",) if name == "c8_no_seats_correction" else ())
        if name in ("c0_base_replicate", "c2b_green_with_false_seats", "c8_no_seats_correction"):
            rec["with_battery"] = run(d)["battery"]
            rec["with_battery_exit"] = run(d)["exit"]
        rec.update(meta)
        rec["fixture"] = d
        rec["tip"] = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
        rows.append(rec)
        print(json.dumps(rec, indent=1)[:2200])
        print("-" * 70)
    open(os.path.join(S, "attack-results.json"), "w").write(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    main(sys.argv[1:])
