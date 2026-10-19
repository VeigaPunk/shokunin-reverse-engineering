#!/usr/bin/env python3
"""RV-7 residual probe — one tool revision, three residual legs, one report.

Seat RV-7 (chain c3, reviewer), wave arc3-loop1-round4, 2026-10-19.

Legs (the c3 frozen claim's (a)(b)(c)):
  A  sidecar path not scope-checked   -> `--out X --paths X.sha256`
  B  mkdir outside the guarded try    -> `--out <regular-file>/sub/r.txt`
  C  coverage gate counts stanzas     -> 5x duplicate stanza, `--require-paths 5`

Each leg reports a mechanical BEFORE/AFTER fingerprint (exit code + one boolean),
so the same driver can be run on the base revision, the revised revision, and
each single-fix-reverted mutant; the mutation driver diffs the three columns.

READ-ONLY over every custody path; all fixtures under the given scratch root.
usage: probe.py <tool.py> <scratch-root> <label>
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

TOOL = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
LABEL = sys.argv[3] if len(sys.argv) > 3 else "run"


def sha256(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError as exc:
        return "ERR:%s" % type(exc).__name__


def run(argv, cwd):
    p = subprocess.run([sys.executable, str(TOOL)] + argv, cwd=str(cwd),
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def box(name):
    b = ROOT / LABEL / name
    shutil.rmtree(b, ignore_errors=True)
    b.mkdir(parents=True)
    return b


def leg_a():
    """(a) `--out vic --paths vic.sha256`: the derived sidecar is vic.sha256 —
    the file being measured. Fixed behavior: refusal (exit 2), vic.sha256 intact."""
    b = box("a")
    (b / "vic.sha256").write_bytes(b"MEASURED-FIXTURE-BYTES\n")
    pre = sha256(b / "vic.sha256")
    rc, so, se = run(["capture", "--out", "vic", "--paths", "vic.sha256", "--label", "rv7-a"], b)
    post = sha256(b / "vic.sha256")
    return {
        "exit": rc,
        "measured_file_intact": pre == post,
        "refusal_line": ("USAGE" in se.strip().splitlines()[-1]) if se.strip() else False,
        "traceback": "Traceback" in se,
        "stdout_tail": so.strip().splitlines()[-1] if so.strip() else "",
    }


def leg_a2():
    """(a) literal claim spelling `--out X.sha256 --paths X`: the sidecar is
    X.sha256.sha256, so the receipt itself lands on the measured file's NEIGHBOUR.
    With an existing bystander there, the neighbour is overwritten."""
    b = box("a2")
    (b / "vic").write_bytes(b"MEASURED-FILE-X\n")
    (b / "vic.sha256").write_bytes(b"BYSTANDER-NEIGHBOUR-BYTES\n")
    pre = sha256(b / "vic")
    pre_n = sha256(b / "vic.sha256")
    rc, so, se = run(["capture", "--out", "vic.sha256", "--paths", "vic", "--label", "rv7-a2"], b)
    return {
        "exit": rc,
        "measured_intact": pre == sha256(b / "vic"),
        "bystander_intact": pre_n == sha256(b / "vic.sha256"),
        "stderr_tail": se.strip().splitlines()[-1] if se.strip() else "",
        "traceback": "Traceback" in se,
    }


def leg_b():
    """(b) `--out <existing-regular-file>/sub/r.txt`: mkdir under a non-directory.
    Fixed behavior: declared USAGE exit 2 with a message, no raw traceback."""
    b = box("b")
    (b / "plainfile").write_bytes(b"PLAIN\n")
    (b / "meas.conf").write_bytes(b"MEASURED\n")
    rc, so, se = run(["capture", "--out", str(b / "plainfile" / "sub" / "r.txt"),
                      "--paths", str(b / "meas.conf"), "--label", "rv7-b"], b)
    return {
        "exit": rc,
        "traceback": "Traceback" in se,
        "usage_line": "USAGE" in se,
        "stderr_tail": se.strip().splitlines()[-1] if se.strip() else "",
    }


def leg_b2():
    """(b) second spelling of the same class: `--out ""` (empty target).
    Base: declared USAGE exit 2 (`Is a directory: '.'`). A fix that computes the
    sidecar name eagerly outside the try turns this into a ValueError traceback."""
    b = box("b2")
    (b / "meas.conf").write_bytes(b"MEASURED\n")
    rc, so, se = run(["capture", "--out", "", "--paths", str(b / "meas.conf"), "--label", "rv7-b2"], b)
    return {
        "exit": rc,
        "traceback": "Traceback" in se,
        "usage_line": "USAGE" in se,
        "stderr_tail": se.strip().splitlines()[-1] if se.strip() else "",
    }


def leg_c():
    """(c) coverage gate counts stanzas: 5x the same path's stanza vs `--require-paths 5`.
    Fixed behavior: refusal (exit 2) + a REFERENCE-COVERAGE line with the distinct count."""
    b = box("c")
    (b / "one.conf").write_bytes(b"ONE-PATH-FIXTURE\n")
    rc0, so0, se0 = run(["capture", "--out", str(b / "ref1.txt"), "--paths", str(b / "one.conf"),
                         "--label", "rv7-c0"], b)
    if rc0 != 0:
        return {"setup_error": "capture exit %d: %s" % (rc0, se0.strip()[:200])}
    text = (b / "ref1.txt").read_text()
    head, first = text.split("\n\nPATH: ", 1)
    block = "PATH: " + first.rstrip("\n")
    dup = head + "\n\n" + "\n\n".join([block] * 5) + "\n"
    (b / "ref5-dupe.txt").write_text(dup)
    n_stanzas = dup.count("\nPATH: ") + (1 if dup.startswith("PATH: ") else 0)
    rc, so, se = run(["verify", str(b / "ref5-dupe.txt"), "--live", "--require-paths", "5"], b)
    cov = [ln for ln in so.splitlines() if ln.startswith("REFERENCE-COVERAGE")]
    return {
        "exit": rc,
        "stanzas": n_stanzas,
        "coverage_line": cov[0] if cov else "(none)",
        "reported_distinct": cov[0].split("/")[0].split(":")[1].strip() if cov else None,
    }


def control_legit():
    """Control: the legitimate write path must keep working on every revision."""
    b = box("control")
    (b / "vic.sha256").write_bytes(b"MEASURED\n")
    rc, so, se = run(["capture", "--out", "fresh.txt", "--paths", "vic.sha256", "--label", "rv7-ctl"], b)
    sidecar_pins = None
    if (b / "fresh.txt.sha256").is_file():
        sidecar_pins = (b / "fresh.txt.sha256").read_text().split()[0] == sha256(b / "fresh.txt")
    vrc, vso, vse = run(["verify", "fresh.txt", "--live", "--require-paths", "1"], b) if (b / "fresh.txt").is_file() else (None, "", "")
    return {"exit": rc, "receipt": (b / "fresh.txt").is_file(),
            "sidecar_pins": sidecar_pins, "verify_exit": vrc}


def selftest():
    b = ROOT / LABEL / "selftest"
    shutil.rmtree(b, ignore_errors=True)
    b.mkdir(parents=True)
    p = subprocess.run([sys.executable, str(TOOL), "selftest", "--scratch", str(b)],
                       capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("CUSTODY_PAIR_SELFTEST")]
    fails = [ln for ln in p.stdout.splitlines() if ln.startswith("case ") and "FAIL" in ln]
    return {"exit": p.returncode, "summary": line[0] if line else "(none)", "failed_cases": fails}


def main():
    report = {
        "label": LABEL,
        "tool": str(TOOL),
        "tool_sha256": sha256(TOOL),
        "tool_bytes": TOOL.stat().st_size,
        "A_sidecar": leg_a(),
        "A2_sidecar_neighbour": leg_a2(),
        "B_mkdir": leg_b(),
        "B2_empty_out": leg_b2(),
        "C_coverage": leg_c(),
        "control_legit": control_legit(),
        "selftest": selftest(),
    }
    print(json.dumps(report, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
