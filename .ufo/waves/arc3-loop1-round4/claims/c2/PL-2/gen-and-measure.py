#!/usr/bin/env python3
"""PL-2 r4 — PROVINCE staleness-census repair generator + measurement harness.

Chain c2, seat PL-2 (planner), wave arc3-loop1-round4.  Reads the real
PROVINCE.md READ-ONLY, emits the candidate repair patch text, builds a scratch
tree with the repairs applied, and measures: line count, census verdict,
locus differ vs baseline, residual-literal sweep.  The real tree is never
written; scratch lives under /var/tmp (never /tmp — standing EDQUOT rule).

Usage:  python3 gen-and-measure.py [--emit]
        (without --emit only the measurement runs; the patch text is rewritten
         either way, from the same hunk table)
"""
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WORK = "/var/tmp/pl2-r4"
SELFDIR = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c2/PL-2")
CENSUS = os.path.join(REPO, ".ufo/gates/c1-census-v10.py")
DIFFER = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c2/RV-4/census-diff.py")
VZ2 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round4/claims/c2/VZ-2/evidence/"
                   "province-staleness-census.py")

# (hunk, 1-based line, pattern, replacement, why)  — patterns are ASCII-only and
# must match exactly once on their line; unicode inside the line is bridged
# with .*? so no non-ASCII literal is typed here.
HUNKS = [
    # --- Frontier (73-93): in the frozen claim's letter -------------------
    ("F1b", 83,
     r"Reserve: 91MB Godot ARM64 template, ARM64X hybrids\.",
     "The 91MB reserve is consumed; scale wall closed (arc2-r7/r8). ARM64X hybrids untested.",
     "corpus/README.md:175 '>90MB PE scale - CLOSED, not frontier'; arc2-r7 entry; r8 control"),
    ("F2a", 84,
     r"all 3 organic cores",
     "the r1-scan organic",
     "coredumpctl today holds 72 non-godot rows (incl. the 2026-10-18 quota-era SIGXFSZ "
     "kills); the r1 scan's '3' (godot, waybar, localsearch) is no longer the census"),
    ("F2b", 85,
     r"exceed the cap \(waybar 434MB\)\. Needs a cap-raising knob or partial-core",
     "cores exceed the cap (waybar 434MB); a 2026-10-19 crashpad-handler core",
     "coredumpctl dump 1857 -> 17,608,704 B < 33,554,432 cap (2026-10-19 00:35:13 -03)"),
    ("F2c", 86,
     r"intake .*?exists\. Retention decays oldest-first\.",
     "dumped sub-cap (17.6 MB); neither a cap knob nor partial-core intake exists. "
     "Retention decays oldest-first.",
     "r2-crash-inspect-probe.md:22 (no flag); waybar dumps now read 'missing' (decay observed)"),
    ("F3b", 88,
     r"JEB \(unprobed\)\. Engine installs are operator-owned\.",
     "JEB (client probed: typed refusal, no engine). Engine installs are operator-owned.",
     "r2-provider-capability-matrix.md:99 (inspect-jeb-client -> capability_unavailable)"),
    ("F5a", 91,
     r"selectors held on synthetic dispatcher",
     "synthetic-dispatcher selectors held (Core,",
     "re-wrap only; r3-07 Core marker kept"),
    ("F5b", 92,
     r"\(Core, r3-07\); real solc/vyper-compiled bytecode untested; selectors stay",
     "r3-07); on-host solc-compiled carriers recovered K/K (arc3-r1/r3, RESULT-",
     "arc3-r1-evm-real-solc.md (K/K on 0.8.37); arc3-r3 (optimizer shapes); no Core promotion claimed"),
    ("F5c", 93,
     r"bare hashes \(no signature DB",
     "class); the Vyper leg is this round's C1 claim; bare hashes (no signature DB",
     "C1's vyper leg is measured in the wave tree (EX-04); corpus entry not yet admitted"),
    # --- Frontier (133-162) ----------------------------------------------
    ("R2a", 139,
     r"PE hits REA's ~900s internal",
     "PE hit REA's ~900s internal",
     "record tense; r4-12 is a past run"),
    ("R2b", 140,
     r"GhidraClient\.js:607\), still progressing",
     "GhidraClient.js:607) at kill (r4-12)",
     "same; no token introduced"),
    ("R2c", 141,
     r"at kill \(r4-12\) \[r5-audit C1: r4-12 cite added\]\. Not OOM \(RSS ~2\.36GB vs",
     "[r5-audit C1: r4-12 cite added]; not OOM (RSS ~2.36GB vs -Xmx2G headroom).",
     "r4-12 entry: provider_timeout, not OOM"),
    ("R2d", 142,
     r"-Xmx2G headroom exists\)\. Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS` to",
     "Closed since: the validated analyzer-disable recipe produced a mitigated",
     "corpus/README.md:175; arc2-r7-pe-wall.md (mitigated hold)"),
    ("R2e", 143,
     r"~3\.6Ms \+ `GHIDRA_HEADLESS_MAXMEM=6-8G` on an idle host, or bisect with a",
     "hold (arc2-r7), and the no-disable control OOM-killed at 9G (arc2-r8); no",
     "arc2-r8 control: no natural hold at this cap"),
    ("R2f", 144,
     r"2-5MB PE\.",
     "natural hold at this cap; rerun id-stability STABLE (arc2-r10).",
     "arc2-r10 erratum: rerun id-stability is STABLE at the 91.6MB point (byte-identical envelope); "
     "r8 control: no natural hold at this cap"),
    ("X1a", 157,
     r"still$",
     "is exercised",
     "r12-02: L203 discharged on both input classes"),
    ("X1b", 158,
     r"probe-refused since r2; multi-version pacman pairs beyond expac unexercised",
     "now (r12-02; the runtime-reconciliation input class stays untested) and",
     "r12-02 (JS + managed success legs)"),
    ("X1c", 159,
     r"\[r5-audit C1: merged from the pruned Frontier bullet .*?its",
     "multi-version pacman pairs are exercised (`op` 2.34.1->2.40.0, r4-10)",
     "r4-10: 1password-cli op 2.34.1->2.40.0, a cached pacman pair; PROVINCE Core row 52 already records it"),
    ("X1d", 160,
     r"`compare_javascript_export_shapes` item is now held \(Core, r4-09\)\]\.",
     "[r5-audit C1: merged from the pruned Frontier bullet; export-shape held (Core, r4-09)].",
     "citation kept; wording compressed to hold the line count"),
    # --- Core sweep (seat line; outside the frozen claim's letter) --------
    ("C46", 46,
     r"35 features incl\. PyGhidra/BSim",
     "34 features incl. PyGhidra/BSim",
     "live `ls Ghidra/Features | wc -l` = 34; the r1 corpus entry lists exactly 34 names "
     "while its claim text says 35 — COUPLED: needs a corpus erratum in the same commit"),
    ("C50", 50,
     r"corpus 1556 signed archives",
     "corpus 1556 signed archives at the 2026-10-13 scan (1350 today)",
     "live `ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l` = 1350 (cache churns)"),
    ("C62", 62,
     r"absent: `7z`, `cabextract`, `xxd`, radare2/rizin, strace/ltrace, upx, pacman-contrib",
     "absent at the scan: `cabextract`, rizin, `ltrace`, `pacman-contrib`; "
     "`7z`/`xxd`/`radare2`/`strace`/`upx` present now",
     "pacman -Qo: 7z=7zip 26.03-1, xxd=tinyxxd 1.3.16-1, radare2 6.2.0-1, strace 7.0-1, "
     "upx 5.2.0-1 — all installed 2026-10-13 13:52, after the r1 scan"),
]

# Optional same-line refresh for the stamp-scoped pointer (adjudication-eligible).
S5_HUNK = ("S5", 18,
           r"\(`~/\.kimi-code/config\.toml:3298` at the 17:55:49Z receipt; "
           r"value unchanged through 2026-10-18's rewrites .*? earlier pointers",
           "(`~/.kimi-code/config.toml:3546` at the round-3 custody receipt; "
           "the 17:55:49Z receipt's :3298 pointer is historical; earlier pointers",
           "live file bc66d543 (3570 lines): pin at :3546, stanza [mcp_servers.rea] at :3544; "
           "the 17:55:49Z pointer :3298 now holds max_context_size")

# Coupled variant: if C1's vyper entry lands in the same commit, line 93's clause
# may name the leg instead of deferring to it. Same line, same count.
COUPLED_HUNK = ("F5c-coupled", 93,
                r"the Vyper leg is this round's C1 claim; bare hashes \(no signature DB",
                "the Vyper leg landed same-commit (arc3-r4); bare hashes (no signature DB",
                "coupling variant: only true once corpus/knowledge/ holds the arc3-r4 vyper entry")
CORPUS_ERRATUM = """# PL-2 r4 — coupled corpus erratum for the Ghidra feature count (patch text)

Target: `corpus/knowledge/2026-10-13-ghidra-install.md` (seats never write corpus;
this is text for the parent). Append at EOF, append-only convention.

Why it is coupled: `PROVINCE.md:46`'s repair (`35 features` -> `34 features`)
would otherwise leave the lane asserting 34 while the corpus entry the row's
sibling facts come from still says 35 in its claim line — and that entry's own
enumerated list holds 34 names (re-derived 2026-10-19: list vs live directory,
zero differences in both directions). Land both or neither.

Literal text to append:

```markdown
## Erratum (arc3-loop1-round4, append-only)

- The Candidate line above reads "35 feature modules"; its own enumerated list
  holds 34 names, and the live directory matches that list exactly (34 dirs,
  0 non-dir entries; `ls -1 Ghidra/Features | wc -l` = 34, re-derived
  2026-10-19). The count is 34; the list was right. PROVINCE.md:46 carried the
  same miscount and was repaired to 34 in the same commit.
```
"""

RESIDUALS = [
    "Reserve: 91MB Godot ARM64 template",
    "all 3 organic cores",
    "JEB (unprobed)",
    "real solc/vyper-compiled bytecode untested",
    "Next: raise `REA_GHIDRA_STARTUP_TIMEOUT_MS`",
    "probe-refused since r2",
    "pacman pairs beyond expac unexercised",
    "absent: `7z`",
    "35 features incl. PyGhidra/BSim",
]

TOKEN_PATTERNS = [
    ("pin", re.compile(r"rea-agents@\d+\.\d+\.\d+", re.I)),
    ("bare-version", re.compile(r"(?<![\d.])6\.\d+\.\d+")),
    ("pointer", re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")),
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def apply_hunks(lines, hunks):
    out = list(lines)
    applied = []
    for name, ln, pat, repl, why in hunks:
        idx = ln - 1
        old = out[idx]
        new, n = re.subn(pat, lambda m: repl, old)
        if n != 1:
            raise SystemExit("hunk %s: pattern matched %d times on line %d: %r"
                             % (name, n, ln, old[:90]))
        out[idx] = new
        applied.append((name, ln, old, new, why))
    if len(out) != len(lines):
        raise SystemExit("line count changed: %d -> %d" % (len(lines), len(out)))
    return out, applied


def emit_patch(applied, path, title, extra_note):
    body = ["# %s" % title, "",
            "Generated by `gen-and-measure.py` from the real `PROVINCE.md` (read-only);",
            "hunks are byte-exact and content-anchored (line numbers informational).",
            extra_note, ""]
    for name, ln, old, new, why in applied:
        body.append("`PROVINCE.md` — hunk %s (line %d): %s" % (name, ln, why))
        body.append("")
        body.append("```diff")
        body.append("--- a/PROVINCE.md")
        body.append("+++ b/PROVINCE.md")
        body.append("@@ line %d @@" % ln)
        body.append("-" + old)
        body.append("+" + new)
        body.append("```")
        body.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(body) + "\n")


def build_tree(tag, new_lines, files=("PROVINCE.md", "SKILL.md", "SCORECARD.md")):
    tree = os.path.join(WORK, "tree-" + tag)
    shutil.rmtree(tree, ignore_errors=True)
    os.makedirs(tree)
    for f in files:
        src = os.path.join(REPO, f)
        dst = os.path.join(tree, f)
        if f == "PROVINCE.md":
            with open(dst, "w", encoding="utf-8") as fh:
                fh.write("\n".join(new_lines))
                if read(src).endswith("\n"):
                    fh.write("\n")
        else:
            shutil.copy2(src, dst)
    return tree


def census(tree, tag):
    jout = os.path.join(WORK, "census-%s.json" % tag)
    tout = os.path.join(WORK, "census-%s.txt" % tag)
    with open(jout, "w") as fh:
        p = subprocess.run([sys.executable, CENSUS, "--root", tree, "--json"],
                           capture_output=True, text=True)
        fh.write(p.stdout)
        rc = p.returncode
    with open(tout, "w") as fh:
        p2 = subprocess.run([sys.executable, CENSUS, "--root", tree, "--quiet"],
                            capture_output=True, text=True)
        fh.write(p2.stdout)
    verdict = [l for l in open(tout) if l.startswith("VERDICT")]
    return jout, tout, rc, (verdict[-1].strip() if verdict else "?")


def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(SELFDIR, exist_ok=True)
    orig = read(os.path.join(REPO, "PROVINCE.md")).split("\n")
    if orig and orig[-1] == "":
        orig = orig[:-1]
    print("real PROVINCE.md lines=%d" % len(orig))

    cand_lines, cand_applied = apply_hunks(orig, HUNKS)
    s5_lines, s5_applied = apply_hunks(orig, HUNKS + [S5_HUNK])
    cpl_lines, cpl_applied = apply_hunks(orig, HUNKS + [COUPLED_HUNK])

    emit_patch(cand_applied, os.path.join(SELFDIR, "candidate-repairs.patch.md"),
               "PL-2 r4 — PROVINCE staleness repairs (21 hunks, line-neutral, token-free)",
               "Scope: 18 Frontier hunks (73-93 and 133-162; the frozen claim's letter) "
               "+ 3 Core-sweep hunks (seat-line scope; C46 is landing-coupled to a corpus erratum).")
    emit_patch(s5_applied, os.path.join(SELFDIR, "candidate-with-s5.patch.md"),
               "PL-2 r4 — same 21 hunks + the optional S5 pointer refresh (22 hunks)",
               "S5 is adjudication-eligible: the pointer is stamp-scoped, so the refresh is "
               "optional; it is measured here so the parent can take either voice.")
    emit_patch(cpl_applied, os.path.join(SELFDIR, "candidate-coupled-vyper.patch.md"),
               "PL-2 r4 — 21 hunks + the Vyper-naming coupling variant (22 hunks)",
               "The extra hunk names the arc3-r4 vyper leg on line 93. TRUE ONLY if C1's "
               "corpus entry lands in the same commit; otherwise take candidate-repairs.patch.md.")
    with open(os.path.join(SELFDIR, "corpus-erratum-coupled.patch.md"), "w",
              encoding="utf-8") as fh:
        fh.write(CORPUS_ERRATUM)

    trees = {}
    trees["candidate"] = build_tree("candidate", cand_lines)
    trees["candidate-s5"] = build_tree("candidate-s5", s5_lines)
    trees["candidate-coupled"] = build_tree("candidate-coupled", cpl_lines)
    trees["baseline"] = build_tree("baseline", orig)

    results = {}
    for tag in ("baseline", "candidate", "candidate-s5", "candidate-coupled"):
        jout, tout, rc, verdict = census(trees[tag], tag)
        nlines = len(read(os.path.join(trees[tag], "PROVINCE.md")).split("\n")) - 1
        results[tag] = {"json": jout, "txt": tout, "rc": rc, "verdict": verdict,
                        "lines": nlines}
        print("%-18s lines=%d  census rc=%d  %s" % (tag, nlines, rc, verdict))

    # differ vs baseline
    for tag in ("candidate", "candidate-s5", "candidate-coupled"):
        p = subprocess.run([sys.executable, DIFFER, results["baseline"]["json"],
                            results[tag]["json"]], capture_output=True, text=True)
        out = os.path.join(WORK, "differ-%s.txt" % tag)
        with open(out, "w") as fh:
            fh.write(p.stdout + "\n--exit=%d\n" % p.returncode)
        last = [l for l in p.stdout.splitlines() if l.startswith("RESULT")]
        print("differ %-14s exit=%d  %s" % (tag, p.returncode,
                                            last[-1] if last else "?"))

    # VZ-2's own instrument on the patched tree (independent cross-check)
    if os.path.exists(VZ2):
        for tag in ("candidate", "candidate-s5", "candidate-coupled"):
            p = subprocess.run([sys.executable, VZ2, "--province",
                                os.path.join(trees[tag], "PROVINCE.md"),
                                "--corpus", os.path.join(REPO, "corpus")],
                               capture_output=True, text=True)
            out = os.path.join(WORK, "vz2-on-%s.txt" % tag)
            with open(out, "w") as fh:
                fh.write(p.stdout + p.stderr + "\n--exit=%d\n" % p.returncode)
            tail = [l for l in p.stdout.splitlines() if l.startswith(("SUMMARY", "STALE"))]
            print("vz2 %-14s exit=%d  %s" % (tag, p.returncode, " | ".join(tail)))

    # residual sweep + token sweep on the patched text
    patched = "\n".join(cand_lines)
    with open(os.path.join(WORK, "residual-check.txt"), "w") as fh:
        fh.write("== residual literals (must be ABSENT from the patched text) ==\n")
        for r in RESIDUALS:
            fh.write("  %-55s %s\n" % (r[:55], "PRESENT" if r in patched else "gone"))
        fh.write("\n== token sweep on the hunks' new text (must be empty) ==\n")
        for name, ln, old, new, why in cand_applied:
            for kind, rx in TOKEN_PATTERNS:
                for m in rx.finditer(new):
                    fh.write("  hunk %s line %d: %s token %r\n" % (name, ln, kind, m.group(0)))
        fh.write("  (no line above = token-free)\n")
    print("residual/token sweep ->", os.path.join(WORK, "residual-check.txt"))

    # control: the same repair with a planted pin must FAIL undeclared=1
    ctrl = list(cand_lines)
    ctrl[91] = ctrl[91] + " rea-agents@6.5.0"
    tree = build_tree("control-pin", ctrl)
    jout, tout, rc, verdict = census(tree, "control-pin")
    print("control-pin    census rc=%d  %s" % (rc, verdict))

    with open(os.path.join(WORK, "summary.json"), "w") as fh:
        json.dump({"hunks": [h[0] for h in cand_applied],
                   "results": results, "control_pin": verdict}, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
