#!/usr/bin/env python3
"""RV-5 sabotage matrix: revert each landed fix in a scratch copy and confirm the
new selftest case (and only it, plus its siblings) goes DIRTY. Proves the cases
are load-bearing, not vacuous. Usage: sabotage.py <tool> <scratch-root> <outdir>"""
import pathlib, re, shutil, subprocess, sys

tool, scratch, outdir = (pathlib.Path(a) for a in sys.argv[1:4])
src = tool.read_text()
scratch.mkdir(parents=True, exist_ok=True)
outdir.mkdir(parents=True, exist_ok=True)

SAB = {
    "S1-unevaluable-branch-reverted": (
        "    if ref_uneval or cand_uneval:",
        "    if False and (ref_uneval or cand_uneval):",
        ("unreadable-path-is-unevaluable", "unevaluable-never-matches",
         "parsed-unevaluable-reference-never-matches")),
    "S2-guard-scope-reverted": (
        "guarded = [Path(p).expanduser() for p in CUSTODY_PATHS] + paths",
        "guarded = [Path(p).expanduser() for p in CUSTODY_PATHS]",
        ("refuses-to-write-over-scoped-path", "refuses-write-through-hardlink-alias")),
    "S3-scratch-guard-reverted": (
        "    if not base.is_dir():",
        "    if False:",
        ("selftest-missing-scratch-usage-exit",)),
    "S4-require-paths-reverted": (
        "    if require:  # falsy (None/0) = no gate — the declared default; opt-in by design",
        "    if False:",
        ("partial-reference-require-paths-gate",)),
}

report = []
for name, (needle, repl, expect_fail) in SAB.items():
    if needle not in src:
        report.append((name, "NEEDLE-MISSING", [], -1))
        continue
    sab = scratch / (name + ".py")
    sab.write_text(src.replace(needle, repl, 1))
    p = subprocess.run([sys.executable, str(sab), "selftest", "--scratch", str(scratch)],
                       capture_output=True, text=True)
    fails = [l.split()[1] for l in p.stdout.splitlines()
             if l.startswith("case ") and " FAIL" in l]
    dirty = "DIRTY" in p.stdout
    report.append((name, "DIRTY" if dirty else "CLEAN", fails, p.returncode))

lines = []
for name, state, fails, rc in report:
    lines.append("%-36s %-6s exit=%s failed_cases=%s" % (name, state, rc, fails))
    _, _, expect = SAB[name]
    missing = [c for c in expect if c not in fails]
    lines.append("      expected-failing=%s  missing=%s" % (list(expect), missing))
text = "\n".join(lines) + "\n"
(outdir / "sabotage.log").write_text(text)
print(text, end="")