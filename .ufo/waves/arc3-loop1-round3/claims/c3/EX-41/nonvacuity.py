#!/usr/bin/env python3
"""EX-41 non-vacuity battery: every newly added entry must be able to redden.

Two mutations per new entry:
  (a) needle -> unique unmatchable token (must_match replaced)
  (b) pointer -> for `extracted` entries only, the citing line is re-pointed at
      a line of the same file that carries no resolvable token (pattern absent)
Expectation: exactly one finding, on that entry's id, class citation_dead.
This proves each entry grades (it is not a vacuous green row).
"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PROBE = os.path.join(ROOT, ".ufo/gates/citation-drift/citation-drift-probe.py")
CAND = "/var/tmp/ex41/pointer-table.ext.json"
NEW_IDS = [e["id"] for e in json.load(open(CAND))["entries"][31:]]


def run(table_path, exp_path):
    p = subprocess.run([sys.executable, PROBE, "--root", ROOT, "--strict",
                        "--table", table_path, "--expected", exp_path],
                       capture_output=True, text=True, cwd=ROOT)
    lines = [l for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT:")]
    verdict = [l for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT_VERDICT")]
    return p.returncode, lines, (verdict[0] if verdict else "")


def mutate(mode, idx, workdir):
    t = json.load(open(CAND))
    entry = t["entries"][31 + idx]
    if mode == "needle":
        entry["must_match"] = "ZZZ_EX41_NEUTER_%s_NO_MATCH_4f2a" % entry["id"]
    else:
        entry["line"] = 1 if entry.get("line") != 1 else 2
    tbl = os.path.join(workdir, "table.json")
    open(tbl, "w").write(json.dumps(t, indent=2, ensure_ascii=False) + "\n")
    import hashlib
    exp = json.load(open(os.path.join(ROOT, ".ufo/gates/citation-drift/expected.json")))
    exp["pointer_table"]["sha256"] = hashlib.sha256(open(tbl, "rb").read()).hexdigest()
    expf = os.path.join(workdir, "expected.json")
    open(expf, "w").write(json.dumps(exp, ensure_ascii=False) + "\n")
    return tbl, expf


def main():
    workdir = tempfile.mkdtemp(prefix="ex41-neuter-", dir="/var/tmp")
    ok = bad = 0
    for idx, eid in enumerate(NEW_IDS):
        for mode in ("needle", "pointer"):
            if mode == "pointer" and json.load(open(CAND))["entries"][31 + idx]["kind"] != "extracted":
                continue
            tbl, expf = mutate(mode, idx, workdir)
            rc, lines, verdict = run(tbl, expf)
            hit = [l for l in lines if "entry=%s " % eid in l + " "]
            good = (rc == 1 and len(lines) == 1 and hit
                    and "citation_dead" in hit[0])
            ok += bool(good)
            bad += (not good)
            print("%s %-40s %-8s rc=%d findings=%d %s"
                  % ("OK  " if good else "FAIL", eid, mode, rc, len(lines),
                     hit[0][:120] if hit else (lines[0][:120] if lines else verdict)))
    total = ok + bad
    print("NONVACUITY: %s controls=%d passed=%d failed=%d"
          % ("CLEAN" if bad == 0 else "FAILED", total, ok, bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())