#!/usr/bin/env python3
"""Section-scoping attack harness for the frozen R47-C2 counter (record.py at the freeze).

Byte-frozen counter: tools/round-47/record.py from commit 5017e1f
(sha256 af666ce26c72e209e165779958489ed53182a1e68270aa9353da32ca2c8abe9d).
Each variant is one commit in a throwaway fixture repo under HYAKU_SCRATCH.
"""
import hashlib
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
COUNT = os.path.join(S, "frozen", "tools", "round-47", "record.py")
D = sys.argv[1]
OUT = os.path.join(S, "runs")
os.makedirs(OUT, exist_ok=True)
RUNS = []


def g(*args):
    r = subprocess.run(["git", "-C", D, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("git failed: %s :: %s" % (" ".join(args), r.stderr))
    return r.stdout.strip()


def w(path, body):
    full = os.path.join(D, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(body)


def commit(msg):
    g("add", "-A")
    g("commit", "-q", "-m", msg)
    return g("rev-parse", "HEAD")


def run(name, rev, expect):
    path = os.path.join(D, "receipts", name + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cmd = [sys.executable, "-I", "-B", COUNT, "--root", D, "--rev", rev,
           "--json-out", path]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    try:
        rec = json.loads(r.stdout)
    except ValueError:
        rec = {"raw": r.stdout[:400], "stderr": r.stderr[-400:]}
    row = {"variant": name, "rev": rev, "expect_exit": expect, "exit": r.returncode,
           "cmd": " ".join(cmd), "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "sections": rec.get("sections"), "atoms": rec.get("atoms"),
           "atoms_by_class": rec.get("atoms_by_class"),
           "mismatches": [m.get("atom") for m in rec.get("mismatches", [])],
           "mismatch_detail": rec.get("mismatches"),
           "exempted": [e.get("atom") for e in rec.get("exempted", [])],
           "corrections": rec.get("corrections"),
           "corrections_bad": rec.get("corrections_bad"),
           "failing": rec.get("failing"), "reason": rec.get("reason"),
           "receipt": path}
    RUNS.append(row)
    print(json.dumps({k: row[k] for k in ("variant", "exit", "expect_exit", "sections",
                                          "atoms", "mismatches", "exempted",
                                          "corrections", "failing")}, indent=1))
    return row


# ---------------------------------------------------------------- seed
os.makedirs(D, exist_ok=True)
subprocess.run(["git", "-C", D, "init", "-q"], check=True)
assert os.path.realpath(g("rev-parse", "--show-toplevel")) == os.path.realpath(D), \
    "fixture toplevel mismatch"
g("config", "user.email", "r47@fixture.invalid")
g("config", "user.name", "r47 fixture")

w("corpus/knowledge/2026-10-01-x.md", "# x\n\ntext\n")
w("corpus/README.md", "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n## Gaps\n\ntail\n")
w("tools/x/keep.md", "keep\n")
w("SKILL.md", "# skill\n\n## Queue-drain craft \n\n"
  "- **1. first rule** cites `tools/x/keep.md:1`.\n\n"
  "- **2. second rule** cites `tools/x/keep.md:1`.\n\n"
  "## Elsewhere\n\ntail\n")
for rnd, (a, b) in ((45, (40, 36)), (46, (40, 40)), (47, (3, 3)), (48, (2, 2))):
    for i, n in ((1, a), (2, b)):
        w(".ufo/waves/round-%d/w%d-dispatch.json" % (rnd, i),
          json.dumps({"counts": {"spawn": n, "resume": 0, "total": n}}))
        w(".ufo/waves/round-%d/w%d.ready.dispatched" % (rnd, i), "ok\n")
c1 = commit("fixture infra")
w("tools/y/marker.md", "measured revision marker\n")
c2 = commit("fixture measured-revision marker")

PRE = """
# Self-assessment

## Owned axes

| Axis | Baseline → current score, 0–10 | Observable | Evidence | Round |
|---|---|---|---|---|
| coverage | 10 → 10 | {cov} knowledge files mapped | command A | r45 |
| depth | 10 → 10 | 2/2 craft rule blocks resolved | command A | r45 |
"""

R45_TRUE = """
## Round 45 — the freeze rule becomes an instrument

Base `{c1}`; measured revision `{c2}`. See `.ufo/waves/round-45/w1-dispatch.json`.
`git log {c1}..{c1} -- tools/x/` is empty.
Wave 1: 40 seats; wave 2: 36 seats (counts from the dispatch files).
"""

R45_FALSE = R45_TRUE.replace("wave 2: 36 seats", "wave 2: 32 seats")
R45_NOWIN = """
## Round 45 — the freeze rule becomes an instrument

Base `{c1}`; measured revision `{c2}`. See `.ufo/waves/round-45/w1-dispatch.json`.
Wave 1: 40 seats; wave 2: 36 seats (counts from the dispatch files).
"""

R46 = """
## Round 46 — the freeze-integrity matrix and its discriminating counter

Waves: 40 + 40 = 80 seats. See `.ufo/waves/round-46/w1-dispatch.json`.
`git log {c1}..{c1} -- SCORECARD.md` is empty. Measured at `{c2}`.
"""

R46_TIP = """
## Round 46 — the freeze-integrity matrix and its discriminating counter

Waves: 40 + 40 = 80 seats. See `.ufo/waves/round-46/w1-dispatch.json`.
`git log 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every
measurement above. Measured at `{c2}`.
"""

CORR = "\n## Record corrections — round 47\n\n"
CORR_46 = ("- corrects seats round-46: 2 waves, 80 seats total\n"
           "- corrects path .ufo/waves/round-46/w1-dispatch.json: landed\n")
CORR_47 = ("- corrects seats round-47: 2 waves, 6 seats total\n"
           "- corrects path .ufo/waves/round-47/w1-dispatch.json: landed\n")
CORR_45_SEATS = "- corrects seats round-45: 2 waves, 76 seats total\n"
WIN46 = lambda: "- corrects window round-46: empty in %s..%s -- SCORECARD.md\n" % (c1, c1)
WIN47 = lambda: "- corrects window round-47: empty in %s..%s -- SCORECARD.md\n" % (c2, c2)
C46 = lambda: WIN46() + CORR_46
C47 = lambda: WIN47() + CORR_47


def card(rounds, corr, cov="1/1"):
    return PRE.format(cov=cov) + rounds + (CORR + corr if corr is not None else "")


def put(name, body, msg, expect):
    w("SCORECARD.md", body)
    rev = commit(msg)
    return run(name, rev, expect)


T = dict(c1=c1, c2=c2)

# V1 — the false round-45 seats atom is in scope and red
put("V1-false-atom-in-scope", card(R45_FALSE.format(**T) + R46.format(**T), C46()),
    "V1: rounds 45+46 in scope", 1)

# V2 — append an EMPTY ## Round 47 after the corrections: round 45 leaves scope
V2 = card(R45_FALSE.format(**T) + R46.format(**T) + CORR + C46(),
          None) + "\n## Round 47\n\nLanding under way; no self-assessment atoms yet.\n"
put("V2-empty-appended-section", V2, "V2: append an empty ## Round 47", 0)

# V2b — same, corrections section last instead of the round section
V2B = (PRE.format(cov="1/1") + R45_FALSE.format(**T) + R46.format(**T) +
       "\n## Round 47\n\nLanding under way; no self-assessment atoms yet.\n" +
       CORR + C46())
put("V2b-empty-appended-section-corr-last", V2B, "V2b: round 47 above corrections", 0)

# V3 — keep the round-45 correction after round 45 left scope
put("V3-correction-out-of-scope",
    PRE.format(cov="1/1") + R45_FALSE.format(**T) + R46.format(**T) + CORR +
    CORR_45_SEATS + C46() + "\n## Round 47\n\nLanding under way.\n",
    "V3: keep the round-45 seats correction", 1)

# V4 — an embedded ## subheading truncates the round section before the false atom
R45_CUT = ("""
## Round 45 — the freeze rule becomes an instrument

Base `{c1}`; measured revision `{c2}`. See `.ufo/waves/round-45/w1-dispatch.json`.
`git log {c1}..{c1} -- tools/x/` is empty.

## Learning trends

Wave 1: 40 seats; wave 2: 32 seats (counts from the dispatch files).
""")
put("V4-embedded-heading-truncation",
    card(R45_CUT.format(**T) + R46.format(**T), C46()),
    "V4: ## subheading inside the round section", 0)

# V5 — duplicate ## Round 45 heading appended with a true atom
put("V5-duplicate-heading",
    PRE.format(cov="1/1") + R45_FALSE.format(**T) + R46.format(**T) +
    "\n## Round 45 — the freeze rule becomes an instrument (re-stated)\n\n"
    "Wave 1: 40 seats; wave 2: 36 seats. See `.ufo/waves/round-45/w1-dispatch.json`.\n" +
    CORR + C46(),
    "V5: duplicate ## Round 45 appended", 0)

# V6 — two appended rounds push the whole audited range out of scope
R47 = """
## Round 47 — calibration

Waves: 3 + 3 = 6 seats. See `.ufo/waves/round-47/w1-dispatch.json`.
`git log {c2}..{c2} -- SCORECARD.md` is empty. Measured at `{c2}`.
"""
R48 = """
## Round 48 — depth

Waves: 2 + 2 = 4 seats. See `.ufo/waves/round-48/w1-dispatch.json`.
`git log {c2}..{c2} -- SCORECARD.md` is empty. Measured at `{c2}`.
"""
put("V6-two-appended-rounds",
    PRE.format(cov="1/1") + R45_FALSE.format(**T) + R46_TIP.format(**T) +
    R47.format(**T) + R48.format(**T) + CORR + C47(),
    "V6: two appended rounds", 0)

# V7 — real-card shape: the only window atom is a <tip> placeholder
put("V7-placeholder-window-correction",
    card(R45_NOWIN.format(**T) + R46_TIP.format(**T),
         WIN46() + CORR_46),
    "V7: placeholder window + concrete-window correction", 1)

# V8 — a concrete window atom elsewhere makes the same correction pass, exempting the placeholder
W45_LINE = "`git log %s..%s -- tools/x/` is empty.\n" % (c1, c1)
put("V8-misdirected-window-exemption",
    card(R45_TRUE.format(**T) + R46_TIP.format(**T),
         "- corrects window round-45: empty in %s..%s -- tools/x/\n" % (c1, c1) + CORR_46),
    "V8: correction names round-45's window, exempts round-46's", 0)

# V9 — the axes class has no correction grammar at all
w("corpus/knowledge/2026-10-02-y.md", "# y\n\ntext (never mapped)\n")
put("V9-axes-correction-ignored",
    card(R45_TRUE.format(**T) + R46.format(**T),
         "- corrects axes coverage: 1/2\n" + C46()),
    "V9: an axes correction line cannot be read", 1)

json.dump({"fixture": D, "counter": COUNT, "c1": c1, "c2": c2, "runs": RUNS},
          open(os.path.join(OUT, "runs.json"), "w"), indent=1)
print("\nRUNS saved:", os.path.join(OUT, "runs.json"))
