#!/usr/bin/env python3
"""Mutation driver for tools/round-46/registry.py --selftest.

For each mutant: fresh copy of the pristine pair (registry.py, gate.py), one exact
text substitution (asserted to apply exactly once), then the same bounded detector
the frozen instrument provides: `--selftest`.  A mutant is KILLED when at least one
selftest case whose expectation is 1 (or 0) flips, i.e. failures>0; SURVIVED when
`failures=0` still prints, i.e. the selftest cannot see the defect.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC2Checks"
BASE = os.environ.get("BASE", os.path.join(S, "pristine"))
LABEL = os.environ.get("LABEL", "head")
OUT = os.environ.get("OUT", os.path.join(
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-46/w1",
    "R46W1MutC2Checks", "mutants.json"))
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "31820472784284727546808acc31b3ea1e73919b"
REV = "1e32827bd05328ee3b1e439d116008f40f078049"
ARGS = ["--root", L, "--freeze", FREEZE, "--rev", REV, "--selftest"]

MUTANTS = [
    ("m1-cell-substring-search",
     "cell 0 matched by re.search instead of exact backtick equality (R45-CL14 b)",
     """            key = row[0].strip()
            if key.startswith("`") and key.endswith("`") and len(key) > 2:
                by_path.setdefault(key[1:-1], row)""",
     """            m = PATHCELL.search(row[0])
            if m:
                by_path.setdefault(m.group(1), row)"""),
    ("m2-fence-blind-parse",
     "rows_in_section loses fence and HTML-comment awareness (R45-CL14 a/c)",
     '''    """Fence-aware and HTML-comment-aware parse of the bound section."""
    out, fence, comment = [], False, False
    for line in mid.splitlines():
        s = line.strip()
        if s.startswith("```") or s.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if comment:
            if "-->" in s:
                comment = False
            continue
        if s.startswith("<!--"):
            if "-->" not in s:
                comment = True
            continue
        if not s.startswith("|"):
            continue
        out.append([c.strip() for c in s.strip("|").split("|")])
    return out''',
     '''    """MUTANT m2: fence- and comment-blind parse of the bound section."""
    return [[c.strip() for c in line.strip().strip("|").split("|")]
            for line in mid.splitlines() if line.strip().startswith("|")]'''),
    ("m3-drop-header-check",
     "house-schema header equality dropped (R45-CL14 d)",
     '    if hard and spec["strict_header"]:',
     '    if False and spec["strict_header"]:'),
    ("m4-drop-absent-at-rev",
     "presence arm dropped: a registered path need not exist at --rev (R45-CL2)",
     '    if hard and spec["presence"]:',
     '    if False and spec["presence"]:'),
    ("m5-exitmap-digit-only",
     "EXITMAP reverted to \\\\b[012]\\\\b: any cell mentioning the digits binds them",
     'EXITMAP = re.compile(r"\\b([012])\\s*[=:]")',
     'EXITMAP = re.compile(r"\\b([012])\\b")'),
    ("m6-rows-outside-section",
     "section bounds dropped: fence-aware rows from the whole SKILL.md register",
     "        cells = rows_in_section(mid)",
     "        cells = rows_in_section(skill)"),
    ("m7-close-before-open-allowed",
     "split_section accepts a close marker that precedes the open marker",
     """    if j < i:
        return None, "close marker precedes open marker"
""",
     ""),
    ("m8-last-row-wins",
     "first-wins shadowing replaced by last-wins (duplicate cell 0)",
     "                by_path.setdefault(key[1:-1], row)",
     "                by_path[key[1:-1]] = row"),
    ("m9-battery-v2-green-requirement",
     "battery acceptance changed from v2_green==0 to v2_green==7",
     '''        for key, want in (("forgeries_total", 7), ("v1_green", 7), ("v2_green", 0),
                          ("genuine_green", 1)):''',
     '''        for key, want in (("forgeries_total", 7), ("v1_green", 7), ("v2_green", 7),
                          ("genuine_green", 1)):'''),
    ("m10-duplicate-markers-allowed",
     "marker uniqueness relaxed to at-least-one, so two opens register",
     '    if skill.count(head) != 1 or skill.count(tail) != 1:',
     '    if skill.count(head) < 1 or skill.count(tail) < 1:'),
    ("m9b-battery-check-neutered",
     "battery acceptance loop emptied: a battery that accepts all forgeries still scores green",
     '''        for key, want in (("forgeries_total", 7), ("v1_green", 7), ("v2_green", 0),
                          ("genuine_green", 1)):''',
     "        for key, want in ():"),
    ("m12-frozen-arm-ignored",
     "the exit-2 frozen-touch verdict is dropped, so a tampered freeze is scored as met",
     """    flat, fs = gate.freeze_state(root, freeze, rev, SPECS[spec_name]["claims"])
    if flat == 2:""",
     """    flat, fs = gate.freeze_state(root, freeze, rev, SPECS[spec_name]["claims"])
    if False:"""),
    ("m11-empty-scope-accepted",
     "load_scope accepts an empty path list, so a census naming nothing scores green",
     "    if not isinstance(paths, list) or not paths:",
     "    if not isinstance(paths, list):"),
]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def cases_of(out):
    try:
        j = json.loads(out[out.index("{"):])
    except (ValueError, IndexError):
        return None
    return {c["case"]: {"expect": c["expect"], "got": c["got"], "ok": c["ok"],
                        "failing": c.get("failing")} for c in j["cases"]}


def main():
    base = BASE
    b_rc, b_out, b_err = run([sys.executable, "-I", "-B", "registry.py"] + ARGS, base)
    baseline = cases_of(b_out)
    assert baseline, b_err
    receipts = []
    for name, defect, old, new in MUTANTS:
        d = os.path.join(S, "mut-%s-%s" % (LABEL, name))
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(base, d)
        src = open(os.path.join(d, "registry.py")).read()
        n = src.count(old)
        if n != 1:
            receipts.append({"name": name, "defect": defect,
                             "applied": False, "error": f"anchor count {n}"})
            continue
        mpath = os.path.join(d, "registry.py")
        with open(mpath, "w") as fh:
            fh.write(src.replace(old, new, 1))
        cmd = [sys.executable, "-I", "-B", "registry.py"] + ARGS
        t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        rc, out, err = run(cmd, d)
        got = cases_of(out)
        flipped = {}
        if got:
            for k, v in got.items():
                if k in baseline and (v["got"] != baseline[k]["got"] or not v["ok"]):
                    flipped[k] = {"baseline_got": baseline[k]["got"], "got": v["got"],
                                  "expect": v["expect"]}
        verdict = ("KILLED" if rc != 0 else "SURVIVED")
        receipts.append({
            "name": name, "defect": defect, "applied": True,
            "mutant_sha256": sha(mpath), "registry_sha256_before": sha(
                os.path.join(base, "registry.py")),
            "anchor_old": old, "anchor_new": new,
            "cmd": "python3 -I -B registry.py " + " ".join(ARGS), "cwd": d,
            "utc": t0, "exit": rc,
            "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
            "stdout_head": out.splitlines()[0] if out.splitlines() else "",
            "stderr_head": err.splitlines()[0] if err.splitlines() else "",
            "selftest_cases": len(got) if got else None,
            "flipped_cases": flipped, "verdict": verdict,
            "surviving_case_hits": sorted(k for k, v in (got or {}).items() if v["ok"]),
        })
        print(f"{name:34s} exit={rc} {receipts[-1]['stdout_head'][:46]:46s} "
              f"flipped={sorted(flipped)} verdict={verdict}")
    outdir = os.path.dirname(OUT)
    os.makedirs(outdir, exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump({"label": LABEL, "base": base,
                   "baseline": {"exit": b_rc,
                                "stdout_head": b_out.splitlines()[0],
                                "stdout_sha256": hashlib.sha256(b_out.encode()).hexdigest(),
                                "cmd": "python3 -I -B registry.py " + " ".join(ARGS),
                                "registry_sha256": sha(os.path.join(base, "registry.py")),
                                "gate_sha256": sha(os.path.join(base, "gate.py")),
                                "cases": baseline},
                   "mutants": receipts}, fh, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
