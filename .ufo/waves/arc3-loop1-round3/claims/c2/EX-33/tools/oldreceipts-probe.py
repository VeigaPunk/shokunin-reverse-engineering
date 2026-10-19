#!/usr/bin/env python3
"""EX-33 leg O — old-tool receipts through the (revised) tool's verify.

For each probe: run `<tool> verify <A> [<B>|--live]`, capture stdout+stderr+exit,
and classify against the DECLARED exit map {0,10,11,12,13,2,3}.  A receipt is
"processable" iff verify terminates with a declared class and prints a verdict
line — a traceback / exit 1 is a FAIL.

Usage:
  oldreceipts-probe.py --tool <tool.py> --out <log> [--capture-json <receipt-or-'-'>]
                       --probe "tag|A|B|--live" ...
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

DECLARED = {0, 2, 3, 10, 11, 12, 13, 14}  # 14 = UNEVALUABLE, added by the EX-21 revision
VERDICT_RE = re.compile(r"^VERDICT: (\S+)", re.M)


def run(tool: Path, argv) -> tuple:
    p = subprocess.run([sys.executable, str(tool)] + argv,
                       capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--probe", action="append", default=[])
    ap.add_argument("--capture-json", default=None,
                    help="capture a receipt (5 custody paths, read-only) into this path first")
    ap.add_argument("--label", default="")
    a = ap.parse_args()

    tool = Path(a.tool)
    log_lines = []
    nl = log_lines.append

    nl("LEG-O old-receipt processability probe  label=%s" % (a.label or "(none)"))
    nl("tool=%s  tool-sha=%s" % (tool, __import__("hashlib").sha256(tool.read_bytes()).hexdigest()))

    if a.capture_json:
        rc, out, err = run(tool, ["capture", "--out", a.capture_json, "--label", "ex33-legO"])
        nl("\n$ %s capture --out %s --label ex33-legO\n[exit %d]\n%s%s" %
           (tool, a.capture_json, rc, out, err))
        if rc not in DECLARED:
            nl("  !! capture exit %d OUTSIDE declared map" % rc)

    failures = 0
    for spec in a.probe:
        tag, ref, cand, mode = spec.split("|")
        argv = ["verify", ref] + (["--live"] if mode == "--live" else [cand])
        rc, out, err = run(tool, argv)
        verdict = VERDICT_RE.search(out)
        declared = rc in DECLARED
        has_verdict = bool(verdict)
        ok = declared and has_verdict
        failures += 0 if ok else 1
        nl("\n$ %s %s\n[exit %d] %s" % (tool, " ".join(argv), rc,
                                        "DECLARED" if declared else "OUTSIDE-DECLARED-MAP"))
        for line in out.splitlines():
            if line.startswith(("A format", "PATH ", "SHA256-CONTRACT", "VERDICT:", "CUSTODY_PAIR_VERIFY")):
                nl("  " + line)
        if err.strip():
            for line in err.strip().splitlines()[-6:]:
                nl("  stderr: " + line)
        nl("  class-check: exit=%d declared=%s verdict-line=%s traceback=%s"
           % (rc, declared, has_verdict, "Traceback" in err or "Traceback" in out))

    nl("\nLEG-O RESULT: probes=%d processable=%d unprocessable=%d"
       % (len(a.probe), len(a.probe) - failures, failures))
    Path(a.out).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    sys.stdout.write("\n".join(log_lines) + "\n")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())