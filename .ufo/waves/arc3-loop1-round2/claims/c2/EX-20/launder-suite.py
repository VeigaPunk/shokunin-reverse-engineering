#!/usr/bin/env python3
"""EX-20 (c2, arc3-loop1-round2) laundering suite — the r4 CR3 class.

Runs, against ONE census instrument revision (never the repo target; a scratch
copy in every case), the injection families a launderer would use to turn a
stale-locus FAIL into a silent PASS:

  W = weakened regex (detection needles / marker assertions narrowed in the
      instrument)
      W-blind    PIN+VER+PTR all dead      (CR-5's census-blind fixture shape)
      W-gate     REA_GATE dead             (nothing is collected at all)
      W-pin      PIN dead only, on the 6.3.0 plant (VER still sees the value)
      W-pin7     PIN dead only, on the 7.3.0 plant (PIN is its ONLY needle:
                 the surgical partial-blindness form)
      W-pinv     PIN+VER dead, on the 6.3.0 plant
      W-marker   last DATED row's marker regex weakened to r"." on a tree whose
                 marker TEXT has been stripped (G15 defeater)
  O = open-ended / overshooting bound (r4 CR3/P3/R3: the scope bound relaxed so
      appended text is sheltered as "historical (dated scope)")
      O-open       last DATED row end 855 -> 1000000000   (> EOF)
      O-overshoot  last DATED row end 855 -> 9999          (> EOF)
      O-addrow     new DATED row 856-1000000000, marker in the tail (> EOF)
      O-ineof      last DATED row end 855 -> EOF exactly  (<= EOF: escapes the
                   r9 rows-beyond-EOF check by construction)
      O-tailrow    new DATED row 856-EOF exactly, marker in the tail (<= EOF)

Trees (scratch roots over byte copies of the three scoped files):
  clean        unmodified copies
  noSKILL      SKILL.md removed (H1 landing-identity marker)
  P6           clean + appended tail carrying `rea-agents@6.3.0` (round-1
               CR-5 t5-dated-shelter / widen-swallow plant shape)
  P7           clean + appended tail carrying `rea-agents@7.3.0`
  P6M          P6 with the planted line carrying INLINE_MARKER words (H2)
  P6S          P6 with the `arc2-loop1-round3` marker token stripped at :769

Phase 2 re-runs the round-1 creep audit (CR-5 scope-diff.py) on each variant
against the base tool: what the external certificate sees, per variant.

Usage: python3 launder-suite.py --tool <census-copy.py> [--label before]
Outputs one row per run; exit 0 always (this is a measuring harness).
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

BASE = "/dev/shm/ex20r2"
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCOPED = ["PROVINCE.md", "SCORECARD.md", "SKILL.md"]
SCOPE_DIFF = (REPO + "/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py")

PIN_OLD = 'PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)'
PIN_DEAD = 'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)'
VER_OLD = 'VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")'
VER_DEAD = 'VER = re.compile(r"(?<![\\d.])Z6\\.\\d+\\.\\d+")'
PTR_OLD = 'PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")'
PTR_DEAD = 'PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml))Z:(\\d+)")'
GATE_OLD = ('REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|'
            'mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)')
GATE_DEAD = 'REA_GATE = re.compile(r"ZZZ_laundered_away|qxj_never_matches", re.I)'
BOUND_OLD = '    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),'
BOUND_MARK_WEAK = '    ("SCORECARD.md", 769, 855, "DATED", 769, r"."),'
BOUND_OPEN = '    ("SCORECARD.md", 769, 1000000000, "DATED", 769, r"arc2-loop1-round3"),'
BOUND_OVER = '    ("SCORECARD.md", 769, 9999, "DATED", 769, r"arc2-loop1-round3"),'

VARIANTS = {
    "ctl": {},
    "W-blind": {PIN_OLD: PIN_DEAD, VER_OLD: VER_DEAD, PTR_OLD: PTR_DEAD},
    "W-gate": {GATE_OLD: GATE_DEAD},
    "W-pin": {PIN_OLD: PIN_DEAD},
    "W-pin7": {PIN_OLD: PIN_DEAD},
    "W-pinv": {PIN_OLD: PIN_DEAD, VER_OLD: VER_DEAD},
    "W-marker": {BOUND_OLD: BOUND_MARK_WEAK},
    "O-open": {BOUND_OLD: BOUND_OPEN},
    "O-overshoot": {BOUND_OLD: BOUND_OVER},
    "O-ineof": None,     # end filled from the planted tree's line count
    "O-addrow": None,    # new row, open end
    "O-tailrow": None,   # new row, end = EOF
}
COMBOS = [("ctl", "clean"), ("ctl", "noSKILL"), ("ctl", "P6"), ("ctl", "P7"),
          ("ctl", "P6M"), ("ctl", "P6S"),
          ("W-blind", "clean"), ("W-blind", "P6"), ("W-gate", "P6"),
          ("W-pin", "P6"), ("W-pin7", "P7"), ("W-pinv", "P6"),
          ("W-marker", "P6S"),
          ("O-open", "P6"), ("O-overshoot", "P6"), ("O-addrow", "P6"),
          ("O-ineof", "P6"), ("O-tailrow", "P6")]


def plant_lines(value, flavored=False):
    note = ("Baseline capsule note (historical): the deployed kimi pin reads "
            "rea-agents@%s." % value) if flavored else \
           ("Capsule note: the deployed kimi pin reads rea-agents@%s." % value)
    return ["", "## planted tail section (2026-10-19)", "", note,
            "Records appended 2026-10-19; lane receipt attached."]


def tree(kind):
    """Build and return a scratch root. Deterministic; rebuilt each run."""
    root = os.path.join(BASE, "root-" + kind)
    os.makedirs(root, exist_ok=True)
    for f in SCOPED:
        src, dst = os.path.join(REPO, f), os.path.join(root, f)
        if kind == "noSKILL" and f == "SKILL.md":
            if os.path.exists(dst):
                os.remove(dst)
            continue
        if kind in ("P6", "P7", "P6M", "P6S") and f == "SCORECARD.md":
            value = "7.3.0" if kind == "P7" else "6.3.0"
            lines = open(src, encoding="utf-8").read().splitlines() + \
                plant_lines(value, flavored=(kind == "P6M"))
            if kind == "P6S":
                lines = [ln.replace("arc2-loop1-round3", "arc2-loop1-rXXX")
                         for ln in lines]
            open(dst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        else:
            open(dst, "wb").write(open(src, "rb").read())
    return root


def marker_line(root, needle):
    lines = open(os.path.join(root, "SCORECARD.md"), encoding="utf-8").read().splitlines()
    return next((i for i, ln in enumerate(lines, 1) if needle in ln), None)


def apply_variant(text, variant, planted):
    reps = VARIANTS[variant]
    n = len(open(os.path.join(planted, "SCORECARD.md"), encoding="utf-8").read().splitlines())
    if variant == "O-ineof":
        reps = {BOUND_OLD: '    ("SCORECARD.md", 769, %d, "DATED", 769, '
                           'r"arc2-loop1-round3"),' % n}
    elif variant == "O-tailrow":
        ml = marker_line(planted, "Records appended 2026-10-19")
        reps = {BOUND_OLD: BOUND_OLD + "\n" + (
            '    ("SCORECARD.md", 856, %d, "DATED", %d, r"2026-10-19"),' % (n, ml))}
    elif variant == "O-addrow":
        ml = marker_line(planted, "Records appended 2026-10-19")
        reps = {BOUND_OLD: BOUND_OLD + "\n" + (
            '    ("SCORECARD.md", 856, 1000000000, "DATED", %d, r"2026-10-19"),' % ml)}
    for old, new in reps.items():
        if old not in text:
            return None
        text = text.replace(old, new, 1)
    return text


def run(tool, root):
    p = subprocess.run([sys.executable, tool, "--root", root],
                       capture_output=True, text=True, timeout=120)
    out = p.stdout

    def grab(pat, default="-"):
        m = re.search(pat, out)
        return m.group(0) if m else default
    return p.returncode, out, {
        "verdict": grab(r"VERDICT: (?:PASS|FAIL)  \(stale=\d+ ambiguous=\d+ undeclared=\d+ unresolved=\d+\)"),
        "g2": grab(r"G2 positive-assertion guard: \w+"),
        "undecl": grab(r"UNDECLARED \((\d+)\)", "UNDECLARED (0)"),
        "unread": grab(r"UNREADABLE \(could-not-evaluate\): \[[^\]]*\]",
                       "UNREADABLE line: absent"),
        "scopeerr": grab(r"SCOPE-ERRORS \(marker assertions\): \[\]",
                         "SCOPE-ERRORS non-empty"),
    }


def audit(base, var):
    p = subprocess.run([sys.executable, SCOPE_DIFF, base, var],
                       capture_output=True, text=True, timeout=60)
    m = re.search(r"CREEP FLAGS: (\[.*\])", p.stdout)
    return (m.group(1) if m else "<no flags line>"), p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--label", default="run")
    args = ap.parse_args()
    tool_sha = hashlib.sha256(open(args.tool, "rb").read()).hexdigest()
    src = open(args.tool, encoding="utf-8").read()
    trees = {k: tree(k) for k in ("clean", "noSKILL", "P6", "P7", "P6M", "P6S")}
    print("# launder-suite label=%s tool=%s sha256=%s" % (args.label, args.tool, tool_sha))
    vdir = os.path.join(BASE, "variants", args.label)
    os.makedirs(vdir, exist_ok=True)
    print("## phase 1 — instrument behaviour")
    for (v, tk) in COMBOS:
        text = apply_variant(src, v, trees["P6"])
        if text is None:
            print("%-12s %-8s SUITE-ERROR: attack anchor absent from this instrument" % (v, tk))
            continue
        path = os.path.join(vdir, "%s.py" % v)
        open(path, "w", encoding="utf-8").write(text)
        rc, out, k = run(path, trees[tk])
        open(os.path.join(vdir, "%s-%s.out" % (v, tk)), "w", encoding="utf-8").write(out)
        state = "PASS" if k["verdict"].startswith("VERDICT: PASS") else "FAIL"
        print("%-12s %-8s exit=%s %-4s %s | %s | %s | %s" %
              (v, tk, rc, state, k["verdict"].split("  ")[-1], k["g2"],
               k["undecl"], k["scopeerr"]))
        print("%-12s %-8s          out-sha256=%s" %
              ("", "", hashlib.sha256(out.encode()).hexdigest()[:16]))
        print("%-12s %-8s          unreadable=%s" % ("", "", k["unread"]))
    print("## phase 2 — external certificate (CR-5 scope-diff creep audit)")
    for v in list(VARIANTS):
        path = os.path.join(vdir, "%s.py" % v)
        if not os.path.exists(path):
            continue
        flags, rc = audit(args.tool, path)
        print("%-12s scope-diff exit=%s flags=%s" % (v, rc, flags))
    return 0


if __name__ == "__main__":
    sys.exit(main())
