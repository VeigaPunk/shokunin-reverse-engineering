#!/usr/bin/env python3
"""R47-C2 correction attacks — v3: clean insertion, bogus-pathspec case, hashed receipts."""
import hashlib, json, os, subprocess, sys, datetime

D = "/fast/scratch/hyaku/kaidoku-r47/RevHistory/fix-clone"
COUNTER = os.path.join(D, "tools", "round-47", "record.py")
CARD = os.path.join(D, "SCORECARD.md")
OUT = os.path.join(D, ".receipts")
BASE = "a631bba0"
WINDOW_LINE = "- corrects window round-46:"
WINDOW_OLD = "332f4884..58eb04b6"


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def check(r, what):
    assert r.returncode == 0, f"{what}: rc={r.returncode} err={r.stderr[:400]}"
    return r


top = sh("git", "-C", D, "rev-parse", "--show-toplevel").stdout.strip()
assert top == D, top


def reset():
    os.makedirs(OUT, exist_ok=True)
    excl = os.path.join(D, ".git", "info", "exclude")
    if ".receipts/" not in open(excl).read():
        open(excl, "a").write(".receipts/\n")
    check(sh("git", "-C", D, "checkout", "-q", "-f", "-B", "revhist", BASE), "reset")
    d = sh("git", "-C", D, "status", "--porcelain").stdout.strip()
    assert d == "", f"dirty after reset: {d[:200]}"


def patch(old, new):
    text = open(CARD).read()
    n = text.count(old)
    assert n == 1, f"{old[:60]!r} occurs {n}x"
    open(CARD, "w").write(text.replace(old, new, 1))


def commit(msg):
    check(sh("git", "-C", D, "-c", "user.name=RevHistory",
             "-c", "user.email=revhist@fixture", "commit", "-q", "-a", "-m", msg), "commit")
    return sh("git", "-C", D, "rev-parse", "HEAD").stdout.strip()


def run(name):
    dest = os.path.join(OUT, f"{name}.json")
    cmd = [sys.executable, "-I", "-B", COUNTER, "--root", D, "--rev", "HEAD",
           "--json-out", dest, "--no-battery"]
    t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    r = subprocess.run(cmd, capture_output=True, text=True)
    rec = json.load(open(dest)) if os.path.exists(dest) else {"reason": r.stdout[:300]}
    return {"name": name,
            "command": "python3 -I -B tools/round-47/record.py --root <FIXTURE> --rev HEAD "
                       "--json-out <FIXTURE>/.receipts/%s.json --no-battery" % name,
            "rev": sh("git", "-C", D, "rev-parse", "HEAD").stdout.strip()[:10],
            "utc": t0,
            "exit": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "stdout": r.stdout.strip()[:200],
            "failing": rec.get("failing"),
            "mismatches": len(rec.get("mismatches", [])),
            "corrections": rec.get("corrections"),
            "corrections_bad": rec.get("corrections_bad"),
            "exempted": [e["atom"][:44] for e in rec.get("exempted", [])]}


steps = []


def step(name, mutator):
    reset()
    mutator()
    dirty = bool(sh("git", "-C", D, "status", "--porcelain").stdout.strip())
    commit(name) if dirty else None
    steps.append(run(name))


step("control-a5-baseline", lambda: None)
step("A-degenerate-window", lambda: patch(WINDOW_OLD, "58eb04b6..58eb04b6"))
step("B-real-span", lambda: patch(WINDOW_OLD, "0425224..58eb04b6"))
step("F-degenerate-window-bogus-path",
     lambda: patch(WINDOW_OLD + " -- tools/round-46 plans/round-46-claims.md",
                   "58eb04b6..58eb04b6 -- does/not/exist"))
step("C-truthful-seats-46",
     lambda: patch(WINDOW_LINE, "- corrects seats round-46: 1 wave, 40 seats total\n" + WINDOW_LINE))
step("D-plan-seats-46",
     lambda: patch(WINDOW_LINE, "- corrects seats round-46: 2 waves, 80 seats total\n" + WINDOW_LINE))
step("I-truth-parsed-shape",
     lambda: patch("Waves: 40 + 40 = 80 seats.",
                   "Wave 1: 40 seats; wave 2: 0 seats (planned, never dispatched)."))
step("J-truth-unparsed-prose",
     lambda: patch("Waves: 40 + 40 = 80 seats.",
                   "One dispatched wave of 40; the second wave was planned and never dispatched."))
step("G-false-axes-coverage",
     lambda: patch("- corrects axes coverage: 138/138", "- corrects axes coverage: 137/138"))
step("H-false-axes-depth",
     lambda: patch("- corrects axes depth: 24/24", "- corrects axes depth: 23/24"))

reset()
print(json.dumps({"toplevel": top, "base": BASE, "steps": steps}, indent=1))
