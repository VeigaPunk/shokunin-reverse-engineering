#!/usr/bin/env python3
"""EX-25 probe: write-guard scope attack, `--paths X --out X` (and variants).

Usage: guard-probe.py <tool.py> <label> <outfile> [<tool-canon.py>]

Every --paths/--out argument used by a case lives under the scratch root
(/var/tmp/ex25/probe). No real custody path is ever named as an --out target:
the canonical-out regression case (D) uses a second tool copy whose
CUSTODY_PATHS tuple has been re-pointed at scratch decoys, so the "canonical
path" branch is exercised on decoys only.

Per case: fresh victim dir, plant X (and Y), stat/sha before, run the tool,
stat/sha after. CLOBBERED = the attacked file's sha256/size/inode/mtime_ns/
ctime_ns moved. REFUSED = exit 2 (USAGE) and nothing moved.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path("/var/tmp/ex25/probe")
DECOY_DIR = ROOT / "host"


def sha(p: Path):
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError as exc:
        return "ERR:%s" % exc


def stattuple(p: Path):
    try:
        st = p.lstat()
        return {
            "sha256": sha(p) if p.is_file() else None,
            "size": st.st_size,
            "inode": st.st_ino,
            "mtime_ns": st.st_mtime_ns,
            "ctime_ns": st.st_ctime_ns,
            "mode": oct(st.st_mode & 0o7777),
            "exists": True,
        }
    except OSError:
        return {"exists": False, "sha256": None, "size": None, "inode": None,
                "mtime_ns": None, "ctime_ns": None, "mode": None}


def diff_fields(b, a):
    return [f for f in ("sha256", "size", "inode", "mtime_ns", "ctime_ns")
            if b.get(f) != a.get(f)]


def classify(rc, moved_list):
    any_moved = any(moved_list)
    if rc == 2:
        return "REFUSED" if not any_moved else "REFUSED-BUT-MOVED"
    if any_moved:
        return "CLOBBERED"
    return "INTACT"


def run_case(name, tool, args, victims, note="", cwd=None):
    case = ROOT / name
    if case.exists():
        shutil.rmtree(case)
    case.mkdir(parents=True)
    for v in victims:
        vp = case / v
        vp.parent.mkdir(parents=True, exist_ok=True)
        vp.write_bytes(("VICTIM-%s-%s\n" % (name, v)).encode() * 24)
    before = {v: stattuple(case / v) for v in victims}
    argv = [sys.executable, str(tool)] + [a.replace("@CASE@", str(case)) for a in args]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          cwd=str(cwd or "/var/tmp/ex25"))
    after = {v: stattuple(case / v) for v in victims}
    moved = {v: diff_fields(before[v], after[v]) for v in victims}
    return {
        "case": name, "note": note, "argv": " ".join(argv), "exit": proc.returncode,
        "stdout": proc.stdout, "stderr": proc.stderr, "before": before, "after": after,
        "fields_moved": moved,
        "sidecars": sorted(p.name for p in case.rglob("*.sha256")),
        "verdict": classify(proc.returncode, list(moved.values())),
    }


def main():
    tool = Path(sys.argv[1]).resolve()
    label = sys.argv[2]
    outfile = Path(sys.argv[3])
    tool_canon = Path(sys.argv[4]).resolve() if len(sys.argv) > 4 else None
    results = []

    # A. the seat-line attack, absolute spellings: --paths X --out X
    results.append(run_case("A-paths-X-out-X", tool,
                            ["capture", "--paths", "@CASE@/X", "--out", "@CASE@/X"],
                            ["X"], "seat-line attack: measured file == receipt target"))
    # A2. same attack with relative spellings (cwd = case dir)
    results.append(run_case("A2-relative", tool,
                            ["capture", "--paths", "X", "--out", "./X"],
                            ["X"], "relative spellings of the same aim", cwd=ROOT / "A2-relative"))
    # B. multi-path: --paths X Y --out Y
    results.append(run_case("B-paths-XY-out-Y", tool,
                            ["capture", "--paths", "@CASE@/X", "@CASE@/Y", "--out", "@CASE@/Y"],
                            ["X", "Y"], "out is one of several measured paths"))
    # C. control: distinct receipt target must not touch X
    results.append(run_case("C-paths-X-out-R", tool,
                            ["capture", "--paths", "@CASE@/X", "--out", "@CASE@/R"],
                            ["X"], "control: distinct out, X must be untouched"))
    # D. canonical-set path as --out (decoy-armed tool copy; never a real path)
    if tool_canon:
        results.append(run_case("D-out-canonical-decoy", tool_canon,
                                ["capture", "--paths", "@CASE@/X", "--out",
                                 str(DECOY_DIR / ".bashrc")],
                                ["X"], "regression: canonical-set out stays refused (decoy set)"))
    # E. nonexistent measured path used as --out (boundary: create vs clobber)
    e = ROOT / "E-missing-paths-X-out-X"
    if e.exists():
        shutil.rmtree(e)
    e.mkdir(parents=True)
    argv_e = [sys.executable, str(tool), "capture", "--paths", str(e / "M"), "--out", str(e / "M")]
    proc_e = subprocess.run(argv_e, capture_output=True, text=True, cwd="/var/tmp/ex25")
    results.append({
        "case": "E-missing-paths-X-out-X", "note": "measured path does not exist yet",
        "argv": " ".join(argv_e), "exit": proc_e.returncode, "stdout": proc_e.stdout,
        "stderr": proc_e.stderr, "before": {"M": {"exists": False}},
        "after": {"M": stattuple(e / "M")}, "fields_moved": {"M": []},
        "sidecars": sorted(p.name for p in e.rglob("*.sha256")),
        "verdict": "REFUSED" if proc_e.returncode == 2 else
                   ("CREATED" if (e / "M").exists() else "OTHER"),
    })
    # F. hardlink alias of the measured file used as --out (D7 class)
    f = ROOT / "F-hardlink-out"
    if f.exists():
        shutil.rmtree(f)
    f.mkdir(parents=True)
    (f / "X").write_bytes(b"VICTIM-F-hardlink\n" * 24)
    os.link(f / "X", f / "ALIAS")
    b_f = stattuple(f / "X")
    argv_f = [sys.executable, str(tool), "capture", "--paths", str(f / "X"),
              "--out", str(f / "ALIAS")]
    proc_f = subprocess.run(argv_f, capture_output=True, text=True, cwd="/var/tmp/ex25")
    a_f = stattuple(f / "X")
    moved_f = diff_fields(b_f, a_f)
    results.append({
        "case": "F-hardlink-out", "note": "D7 class: --out is a hardlink alias of measured X",
        "argv": " ".join(argv_f), "exit": proc_f.returncode, "stdout": proc_f.stdout,
        "stderr": proc_f.stderr, "before": {"X": b_f}, "after": {"X": a_f},
        "fields_moved": {"X": moved_f},
        "sidecars": sorted(p.name for p in f.rglob("*.sha256")),
        "verdict": "REFUSED" if proc_f.returncode == 2 and not moved_f else
                   ("CLOBBERED" if moved_f else
                    ("INTACT" if proc_f.returncode == 0 else "OTHER")),
    })
    # G. symlink alias of the measured file used as --out
    g = ROOT / "G-symlink-out"
    if g.exists():
        shutil.rmtree(g)
    g.mkdir(parents=True)
    (g / "X").write_bytes(b"VICTIM-G-symlink\n" * 24)
    os.symlink(g / "X", g / "LINK")
    b_g = stattuple(g / "X")
    argv_g = [sys.executable, str(tool), "capture", "--paths", str(g / "X"),
              "--out", str(g / "LINK")]
    proc_g = subprocess.run(argv_g, capture_output=True, text=True, cwd="/var/tmp/ex25")
    a_g = stattuple(g / "X")
    moved_g = diff_fields(b_g, a_g)
    results.append({
        "case": "G-symlink-out", "note": "--out is a symlink to measured X (resolve-covered)",
        "argv": " ".join(argv_g), "exit": proc_g.returncode, "stdout": proc_g.stdout,
        "stderr": proc_g.stderr, "before": {"X": b_g}, "after": {"X": a_g},
        "fields_moved": {"X": moved_g},
        "sidecars": sorted(p.name for p in g.rglob("*.sha256")),
        "verdict": "REFUSED" if proc_g.returncode == 2 and not moved_g else
                   ("CLOBBERED" if moved_g else
                    ("INTACT" if proc_g.returncode == 0 else "OTHER")),
    })

    # H. sidecar aliasing: --paths R.sha256 --out R makes the receipt's sidecar
    #    (out.name + ".sha256") land on a measured path.
    h = ROOT / "H-sidecar-alias"
    if h.exists():
        shutil.rmtree(h)
    h.mkdir(parents=True)
    (h / "R.sha256").write_bytes(b"VICTIM-H-sidecar\n" * 24)
    b_h = stattuple(h / "R.sha256")
    argv_h = [sys.executable, str(tool), "capture", "--paths", str(h / "R.sha256"),
              "--out", str(h / "R")]
    proc_h = subprocess.run(argv_h, capture_output=True, text=True, cwd="/var/tmp/ex25")
    a_h = stattuple(h / "R.sha256")
    moved_h = diff_fields(b_h, a_h)
    results.append({
        "case": "H-sidecar-alias", "note": "--out sidecar (out.name+'.sha256') == measured path",
        "argv": " ".join(argv_h), "exit": proc_h.returncode, "stdout": proc_h.stdout,
        "stderr": proc_h.stderr, "before": {"R.sha256": b_h}, "after": {"R.sha256": a_h},
        "fields_moved": {"R.sha256": moved_h},
        "sidecars": sorted(p.name for p in h.rglob("*.sha256")),
        "verdict": "REFUSED" if proc_h.returncode == 2 and not moved_h else
                   ("CLOBBERED" if moved_h else
                    ("INTACT" if proc_h.returncode == 0 else "OTHER")),
    })

    # I. symlink whose target is a canonical-set path (indirect canonical aim)
    if tool_canon:
        i = ROOT / "I-symlink-canonical"
        if i.exists():
            shutil.rmtree(i)
        i.mkdir(parents=True)
        (i / "X").write_bytes(b"VICTIM-I-indirect\n" * 24)
        os.symlink(DECOY_DIR / ".profile", i / "AIM")
        b_i = stattuple(DECOY_DIR / ".profile")
        argv_i = [sys.executable, str(tool_canon), "capture", "--paths", str(i / "X"),
                  "--out", str(i / "AIM")]
        proc_i = subprocess.run(argv_i, capture_output=True, text=True, cwd="/var/tmp/ex25")
        a_i = stattuple(DECOY_DIR / ".profile")
        moved_i = diff_fields(b_i, a_i)
        results.append({
            "case": "I-symlink-canonical", "note": "out is a symlink to a canonical-set path (decoy)",
            "argv": " ".join(argv_i), "exit": proc_i.returncode, "stdout": proc_i.stdout,
            "stderr": proc_i.stderr, "before": {".profile": b_i}, "after": {".profile": a_i},
            "fields_moved": {".profile": moved_i},
            "sidecars": sorted(p.name for p in i.rglob("*.sha256")),
            "verdict": "REFUSED" if proc_i.returncode == 2 and not moved_i else
                       ("CLOBBERED" if moved_i else
                        ("INTACT" if proc_i.returncode == 0 else "OTHER")),
        })

    payload = {"label": label, "tool": str(tool), "tool_sha256": sha(tool),
               "tool_canon_sha256": sha(tool_canon) if tool_canon else None,
               "results": results}
    outfile.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    for r in results:
        print("%-26s exit=%-3s verdict=%-10s moved=%s sidecars=%s"
              % (r["case"], r["exit"], r["verdict"], r["fields_moved"], r["sidecars"]))
    print("WROTE %s sha256=%s" % (outfile, sha(outfile)))


if __name__ == "__main__":
    main()