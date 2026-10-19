#!/usr/bin/env python3
"""RV-5 late-join independent mutation matrix (re-derived, not copied).

Reverts each landed closure site (and each arm of the guard) in a scratch copy
of the landed tool and runs the landed selftest against the mutant, recording
which cases go DIRTY. Also diagnoses the single-line scratch-guard revert that
RV-5's earlier sabotage run recorded as CLEAN.

usage: mutate.py <tool> <scratch-root> <outdir>
"""
import pathlib, subprocess, sys

tool, scratch, outdir = (pathlib.Path(a) for a in sys.argv[1:4])
src = tool.read_text()
scratch.mkdir(parents=True, exist_ok=True)
outdir.mkdir(parents=True, exist_ok=True)

ISDIR = "    if not base.is_dir():"
MKDIR = (
    "    try:\n"
    "        root = Path(tempfile.mkdtemp(prefix=\"custody-pair-selftest-\", dir=str(base)))\n"
    "    except OSError as exc:\n"
    "        print(\"USAGE: cannot create a fixture root under %s (%s)\" % (base, exc), file=sys.stderr)\n"
    "        return EXIT_USAGE\n"
)
BARE = "    root = Path(tempfile.mkdtemp(prefix=\"custody-pair-selftest-\", dir=str(base)))\n"

MUT = [
    ("M1-unevaluable-branch",
     [("    if ref_uneval or cand_uneval:", "    if False and (ref_uneval or cand_uneval):")],
     ["unreadable-path-is-unevaluable", "unevaluable-never-matches",
      "parsed-unevaluable-reference-never-matches"]),
    ("M1b-parser-error-keys",
     [('"stat_error", "read_error"):', "):")],
     ["parsed-unevaluable-reference-never-matches"]),
    ("M2-guard-scope-both-arms",
     [("guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths",
       "guarded = [Path(p).expanduser() for p in CUSTODY_PATHS]")],
     ["refuses-to-write-over-scoped-path", "refuses-write-through-hardlink-alias"]),
    ("M2b-guard-inode-arm-only",
     [("or any(_same_file(out, g) for g in guarded)", "or False")],
     ["refuses-write-through-hardlink-alias"]),
    ("M3-scratch-isdir-line-only",
     [(ISDIR, "    if False:")],
     ["selftest-missing-scratch-usage-exit"]),
    ("M3b-scratch-both-layers",
     [(ISDIR, "    if False:"), (MKDIR, BARE)],
     ["selftest-missing-scratch-usage-exit"]),
    ("M4-require-paths",
     [("    if require:  # falsy (None/0) = no gate — the declared default; opt-in by design",
       "    if False:")],
     ["partial-reference-require-paths-gate"]),
]

lines = ["# RV-5 independent mutation matrix — tool sha256 under test:"]
lines.append("# " + subprocess.run(["sha256sum", str(tool)], capture_output=True, text=True).stdout.strip())
for name, subs, expect in MUT:
    text = src
    missing_needle = []
    for needle, repl in subs:
        if text.count(needle) != 1:
            missing_needle.append("%r x%d" % (needle[:60], text.count(needle)))
        text = text.replace(needle, repl, 1)
    if missing_needle:
        lines.append("%-32s NEEDLE-PROBLEM %s" % (name, missing_needle))
        continue
    sab = scratch / (name + ".py")
    sab.write_text(text)
    p = subprocess.run([sys.executable, str(sab), "selftest", "--scratch", str(scratch)],
                       capture_output=True, text=True)
    fails = [l.split()[1] for l in p.stdout.splitlines()
             if l.startswith("case ") and " FAIL" in l]
    state = "DIRTY" if "DIRTY" in p.stdout else "CLEAN"
    lines.append("%-32s %-6s exit=%s failed_cases=%s" % (name, state, p.returncode, fails))
    lines.append("      expected-failing=%s  not-fired=%s" % (list(expect), [c for c in expect if c not in fails]))

# S3 diagnosis: what does each arm actually emit under the single-line revert?
lines.append("")
lines.append("== S3 diagnosis: single-line is_dir revert, per-arm stderr ==")
sab = scratch / "M3-scratch-isdir-line-only.py"
scr = scratch / "diag"
scr.mkdir(exist_ok=True)
for label, target in (("missing", str(scr / "does-not-exist")),
                      ("file", str(scr / "a-file")),
                      ("tmp", "/tmp/rv5-late-must-not")):
    if label == "file":
        pathlib.Path(target).write_text("x")
    p = subprocess.run([sys.executable, str(sab), "selftest", "--scratch", target],
                       capture_output=True, text=True)
    first_err = (p.stderr.strip().splitlines() or [""])[0]
    lines.append("  arm=%-8s rc=%s traceback=%s stderr1=%s" % (
        label, p.returncode, "Traceback" in p.stderr, first_err))
lines.append("")
lines.append("== landed tool, same three arms (for the message contrast) ==")
for label, target in (("missing", str(scr / "does-not-exist")),
                      ("file", str(scr / "a-file")),
                      ("tmp", "/tmp/rv5-late-must-not")):
    p = subprocess.run([sys.executable, str(tool), "selftest", "--scratch", target],
                       capture_output=True, text=True)
    first_err = (p.stderr.strip().splitlines() or [""])[0]
    lines.append("  arm=%-8s rc=%s traceback=%s stderr1=%s" % (
        label, p.returncode, "Traceback" in p.stderr, first_err))

(outdir / "mutation-matrix.log").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
