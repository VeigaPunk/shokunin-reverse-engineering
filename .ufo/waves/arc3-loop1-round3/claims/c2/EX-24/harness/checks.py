#!/usr/bin/env python3
"""EX-24 after-state acceptance checker (design-agnostic).

Reads the matrix output dir produced by run-matrix.sh and evaluates the seat's
acceptance criteria. Emits PASS/FAIL/UNKNOWN per criterion with quoted evidence.

Usage: checks.py <phase-dir>   (e.g. /var/tmp/ex24-after/before)
"""
import json
import re
import sys
from pathlib import Path

PHASE = Path(sys.argv[1])
D = PHASE

CUSTODY = [
    "/home/vgpnk/.config/devin/mcp_config.json",
    "/home/vgpnk/.omp/agent/mcp.json",
    "/home/vgpnk/.kimi-code/config.toml",
    "/home/vgpnk/.bashrc",
    "/home/vgpnk/.profile",
]
UNACCOUNTED4 = CUSTODY[1:]


def read(name):
    p = D / name
    return p.read_text(errors="replace") if p.exists() else None


def exit_of(text):
    m = re.findall(r"^EXIT=(-?\d+)$", text or "", re.M)
    return int(m[-1]) if m else None


def verdict_line(text):
    m = re.findall(r"^VERDICT: (\S+)\s+paths=(\d+)\s+(.*?)exit=(\d+)$", text or "", re.M)
    return m[-1] if m else None


def final_line(text):
    m = re.findall(r"^CUSTODY_PAIR_VERIFY: (\S+) paths=(\S+) drift=(\d+) exit=(\d+)$",
                   text or "", re.M)
    return m[-1] if m else None


results = []


def check(cid, desc, ok, evidence):
    results.append({"id": cid, "desc": desc, "verdict": ok, "evidence": evidence})


# --- C1: the 1-of-5 v1 leg must not read as a clean verified pass ---
t = read("M1-v1-1of5-live.out")
if t is None:
    check("C1", "v1 1-of-5 leg present", "UNKNOWN", "file missing")
else:
    ex = exit_of(t)
    fl = final_line(t)
    vl = verdict_line(t)
    declared_nonmatch = ex not in (0,) and fl is not None
    check("C1", "v1 1-of-5 --live: default mode yields a declared non-MATCH class",
          declared_nonmatch, "exit=%s final=%s verdict=%s" % (ex, fl, vl))

# --- C2: the 1-of-5 v2 leg (tool-produced receipt) ---
t = read("M3b-v2-1of5-live.out")
if t is None:
    check("C2", "v2 1-of-5 leg present", "UNKNOWN", "file missing")
else:
    ex = exit_of(t)
    fl = final_line(t)
    vl = verdict_line(t)
    check("C2", "v2 1-of-5 --live: default mode yields a declared non-MATCH class",
          ex not in (0,) and fl is not None, "exit=%s final=%s verdict=%s" % (ex, fl, vl))

# --- C3: --require-paths 5 on the 1-of-5 legs (if the flag landed) ---
for cid, name in (("C3", "M2-v1-1of5-reqpaths5.out"), ("C4", "M3c-v2-1of5-reqpaths5.out")):
    t = read(name)
    if t is None:
        check(cid, name + " present", "UNKNOWN", "file missing")
        continue
    ex = exit_of(t)
    landed = "unrecognized arguments" not in (t or "")
    cov = re.findall(r"^.*(REFERENCE-COVERAGE|COVERAGE|unaccounted).*$", t or "", re.M)
    check(cid, "%s: flag landed and refuses with a coverage declaration" % name,
          landed and ex is not None and ex != 0 and bool(cov),
          "exit=%s landed=%s coverage_lines=%s" % (ex, landed, cov[:3]))

# --- C5: no unaccounted path may be classified MATCH / verified in 1-of-5 output ---
scan = read("M6-unaccounted-scan.out")
if scan is None:
    check("C5", "unaccounted-path scan present", "UNKNOWN", "file missing")
else:
    bad = []
    for line in scan.splitlines():
        if line.startswith("MENTIONED"):
            p, rest = line.split(" in ", 1)
            path = p.split(" ", 1)[1]
            fname, payload = rest.split(":", 1)
            if re.search(r":\s*(MATCH|MATCH-V1-PARTIAL)\b", payload):
                bad.append(line)
    check("C5", "no unaccounted custody path classified MATCH in any 1-of-5 output",
          not bad, "MATCH-classified unaccounted mentions=%d %s" % (len(bad), bad[:3]))

# --- C6: canonical 5/5 pair must still verify MATCH exit 0 ---
t = read("M4c-canonical-pair.out")
ex = exit_of(t)
fl = final_line(t)
check("C6", "canonical 5/5 pair still MATCH 5/5 exit 0 (no false positive)",
      ex == 0 and fl is not None and fl[0] == "MATCH" and fl[1] == "5/5",
      "exit=%s final=%s" % (ex, fl))

# --- C7: --require-paths 5 must pass a genuine 5-path receipt ---
t = read("M8b-v2-5of5-noncanonical-reqpaths5.out")
ex = exit_of(t)
check("C7", "5-path receipt under --require-paths 5 not refused (threshold, not blanket)",
      ex == 0, "exit=%s line=%s" % (ex, final_line(t)))

# --- C8: --require-paths 1 on a 1-path receipt passes (threshold semantics) ---
t = read("M10-v1-1of5-reqpaths1.out")
ex = exit_of(t)
landed = t is not None and "unrecognized arguments" not in t
check("C8", "1-path receipt under --require-paths 1 passes (threshold semantics)",
      landed and ex == 0, "exit=%s landed=%s" % (ex, landed))

# --- C9: 4-path receipt under --require-paths 5 must be refused ---
t = read("M9b-v2-4of5-reqpaths5.out")
ex = exit_of(t)
check("C9", "4-path receipt under --require-paths 5 refused",
      ex is not None and ex != 0, "exit=%s line=%s" % (ex, final_line(t)))

# --- C10: selftest count and cleanliness ---
t = read("M7a-selftest-default.out")
m = re.search(r"CUSTODY_PAIR_SELFTEST: (\S+) cases=(\d+) passed=(\d+) failed=(\d+) exit=(\d+)", t or "")
if not m:
    check("C10", "selftest summary present", "UNKNOWN", "no summary line")
else:
    status, cases, passed, failed, ex = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
    check("C10", "selftest CLEAN and cases>=17 (r3 C2 target)",
          status == "CLEAN" and failed == 0 and cases >= 17,
          "status=%s cases=%d passed=%d failed=%d exit=%d" % (status, cases, passed, failed, ex))

# --- C11: D6 scratch guard ---
t = read("M7c-selftest-missing.out")
ex = exit_of(t)
trace = "Traceback" in (t or "")
check("C11", "selftest --scratch <missing> declared class, no traceback",
      ex == 2 and not trace, "exit=%s traceback=%s first=%r" % (ex, trace, (t or "").splitlines()[:1]))

print(json.dumps(results, indent=2))
n_pass = sum(1 for r in results if r["verdict"] is True)
n_fail = sum(1 for r in results if r["verdict"] is False)
n_unk = sum(1 for r in results if r["verdict"] == "UNKNOWN")
print("\nSUMMARY phase=%s pass=%d fail=%d unknown=%d" % (D.name, n_pass, n_fail, n_unk))
sys.exit(0 if n_fail == 0 else 1)