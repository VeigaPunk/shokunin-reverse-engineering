#!/usr/bin/env python3
"""EX-25 (c3, arc3-loop1-round4) coverage-gate matrix.

Runs one labelled matrix against a given tool revision copy and writes
<phase>/matrix.out + <phase>/checks.json.  Every leg is a single command whose
exit code, stdout and stderr are captured verbatim.

Usage: run-matrix.py <phase>            # phase = before | after | candidate
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/var/tmp/ex25-r4")
FIX = ROOT / "fixtures"
CUSTODY_FIVE = (
    "~/.config/devin/mcp_config.json",
    "~/.omp/agent/mcp.json",
    "~/.kimi-code/config.toml",
    "~/.bashrc",
    "~/.profile",
)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    phase = sys.argv[1]
    tool = ROOT / "tools" / phase / "custody-pair.py"
    outdir = ROOT / "out" / phase
    outdir.mkdir(parents=True, exist_ok=True)
    scratch = outdir / "selftest-scratch"
    scratch.mkdir(exist_ok=True)
    tool_sha = sha256_file(tool)

    legs: list[tuple[str, list[str]]] = []

    def leg(name, *args):
        legs.append((name, [str(a) for a in args]))

    # --- the seat's claim -------------------------------------------------
    leg("V1-dupe5-onepath-req5", "verify", FIX / "dupe5-one-path-pre.txt", "--live", "--require-paths", 5)
    leg("V2-custody5-distinct-req5", "verify", FIX / "custody5-distinct-pre.txt", "--live", "--require-paths", 5)
    # --- padding variants -------------------------------------------------
    leg("V3-dupe4plus1-req5", "verify", FIX / "dupe4plus1-pre.txt", "--live", "--require-paths", 5)
    leg("V4-symlink-alias-5stanzas-req5", "verify", FIX / "symlink-alias-5stanzas-pre.txt", "--live", "--require-paths", 5)
    leg("V5-v1-dupe5-onepath-req5", "verify", FIX / "v1-dupe5-one-path-pre.txt", "--live", "--require-paths", 5)
    # --- controls ---------------------------------------------------------
    leg("V6-one-path-req5", "verify", FIX / "one-pre.txt", "--live", "--require-paths", 5)
    leg("V7-one-path-req1", "verify", FIX / "one-pre.txt", "--live", "--require-paths", 1)
    leg("V8-dupe5-onepath-req1", "verify", FIX / "dupe5-one-path-pre.txt", "--live", "--require-paths", 1)
    leg("V9-scratch5-distinct-req5", "verify", FIX / "scratch5-distinct-pre.txt", "--live", "--require-paths", 5)
    leg("V10-v1-distinct5-req5", "verify", FIX / "v1-distinct5-pre.txt", "--live", "--require-paths", 5)
    leg("V11-custody5-distinct-req6", "verify", FIX / "custody5-distinct-pre.txt", "--live", "--require-paths", 6)
    # --- declared opt-in (must be unchanged) ------------------------------
    leg("V12-dupe5-onepath-noflag", "verify", FIX / "dupe5-one-path-pre.txt", "--live")
    leg("V13-custody5-distinct-noflag", "verify", FIX / "custody5-distinct-pre.txt", "--live")
    # --- the r3 real receipt pair (no-regression on real artifacts) -------
    r3 = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c2/receipts")
    pre = r3 / "config-pre-pair-v2r3-revised.txt"
    post = r3 / "config-post-pair-v2r3.txt"
    if pre.exists() and post.exists():
        leg("V14-r3-pair-req5", "verify", pre, post, "--require-paths", 5)
        leg("V15-r3-pair-noflag", "verify", pre, post)
    # --- selftest ---------------------------------------------------------
    leg("V16-selftest", "selftest", "--scratch", scratch)
    leg("V17-paths", "paths")

    results = []
    lines = ["# EX-25 coverage-gate matrix — phase=%s  tool=%s  sha256=%s"
             % (phase, tool, tool_sha), "# date-utc: %s" % subprocess.run(
                 ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"], capture_output=True, text=True).stdout.strip(), ""]
    for name, args in legs:
        cmd = ["python3", str(tool)] + args
        proc = subprocess.run(cmd, capture_output=True, text=True)
        body = proc.stdout + (("\n[stderr]\n" + proc.stderr) if proc.stderr else "")
        lines.append("=" * 78)
        lines.append("LEG %s  exit=%d" % (name, proc.returncode))
        lines.append("CMD %s" % " ".join(cmd))
        lines.append(body.rstrip("\n"))
        lines.append("")
        results.append({
            "leg": name,
            "exit": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        })
    (outdir / "matrix.out").write_text("\n".join(lines), encoding="utf-8")

    # ---- checks: the seat's own criteria --------------------------------
    def res(leg_name):
        for r in results:
            if r["leg"] == leg_name:
                return r
        return None

    def text(leg_name):
        r = res(leg_name)
        return (r["stdout"] + r["stderr"]) if r else ""

    checks = []

    def chk(cid, desc, ok, evidence):
        checks.append({"id": cid, "desc": desc, "pass": bool(ok), "evidence": evidence})

    r = res("V1-dupe5-onepath-req5")
    chk("C1", "duplicate-stanza 5-path reference is caught by --require-paths 5 (exit 2)",
        r and r["exit"] == 2,
        "exit=%s out=%r" % (r["exit"], text("V1-dupe5-onepath-req5").strip().splitlines()[:2] if r else None))

    r = res("V2-custody5-distinct-req5")
    chk("C2", "single-stanza-per-path 5-path control still passes (exit 0, MATCH 5/5)",
        r and r["exit"] == 0 and "MATCH" in r["stdout"],
        "exit=%s out=%r" % (r["exit"], r["stdout"].strip().splitlines()[-1] if r else None))

    r = res("V3-dupe4plus1-req5")
    chk("C3", "4-distinct-plus-padding is caught (exit 2)", r and r["exit"] == 2,
        "exit=%s" % (r["exit"] if r else None))

    r = res("V4-symlink-alias-5stanzas-req5")
    chk("C4", "symlink-alias boundary: 5 stanzas/4 resolved paths is caught (exit 2)",
        r and r["exit"] == 2, "exit=%s" % (r["exit"] if r else None))

    r = res("V5-v1-dupe5-onepath-req5")
    chk("C5", "v1 sums shape: 5 rows/1 distinct path is caught (exit 2)",
        r and r["exit"] == 2, "exit=%s" % (r["exit"] if r else None))

    r = res("V6-one-path-req5")
    chk("C6", "1-of-5 reference under the gate is still USAGE exit 2 (r3 behaviour held)",
        r and r["exit"] == 2 and "REFERENCE-COVERAGE: 1/5" in text("V6-one-path-req5"),
        "exit=%s" % (r["exit"] if r else None))

    r = res("V7-one-path-req1")
    chk("C7", "threshold semantics: --require-paths 1 on a 1-path reference exits 0",
        r and r["exit"] == 0, "exit=%s" % (r["exit"] if r else None))

    r = res("V12-dupe5-onepath-noflag")
    chk("C8", "declared opt-in unchanged: padded reference without the flag exits 0",
        r and r["exit"] == 0, "exit=%s" % (r["exit"] if r else None))

    r = res("V13-custody5-distinct-noflag")
    chk("C9", "declared opt-in unchanged: canonical 5-path reference without the flag exits 0",
        r and r["exit"] == 0, "exit=%s" % (r["exit"] if r else None))

    r = res("V10-v1-distinct5-req5")
    chk("C10", "v1 distinct-5 control passes the gate (exit 0)", r and r["exit"] == 0,
        "exit=%s" % (r["exit"] if r else None))

    r = res("V14-r3-pair-req5")
    chk("C11", "r3 real receipt pair under the gate is unchanged (MATCH 5/5 exit 0)",
        r and r["exit"] == 0 and "MATCH" in r["stdout"], "exit=%s" % (r["exit"] if r else None))

    r = res("V16-selftest")
    chk("C12", "selftest runs (exit 0, CLEAN)", r and r["exit"] == 0 and "CLEAN" in r["stdout"],
        "exit=%s last=%r" % (r["exit"], r["stdout"].strip().splitlines()[-1] if r else None))

    r = res("V9-scratch5-distinct-req5")
    chk("C13", "declared count-vs-identity residual R3 (5 unrelated paths pass) — recorded, not failed",
        r is not None, "exit=%s (a 0 here is the declared R3 shape, not a regression)"
        % (r["exit"] if r else None))

    summary = {
        "phase": phase,
        "tool": str(tool),
        "tool_sha256": tool_sha,
        "legs": {r["leg"]: r["exit"] for r in results},
        "checks": checks,
        "passed": sum(1 for c in checks if c["pass"]),
        "failed": sum(1 for c in checks if not c["pass"]),
    }
    (outdir / "checks.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"phase": phase, "tool_sha256": tool_sha,
                      "legs": summary["legs"], "passed": summary["passed"],
                      "failed": summary["failed"]}, indent=2))
    for c in checks:
        print("%-4s %-4s %s" % (c["id"], "PASS" if c["pass"] else "FAIL", c["desc"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
