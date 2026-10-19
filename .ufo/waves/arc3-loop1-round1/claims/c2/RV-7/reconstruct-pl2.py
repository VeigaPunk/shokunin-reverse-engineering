#!/usr/bin/env python3
"""RV-7 — reconstruct PL-2's frozen-run-guard patch text on scratch copies.

Purpose: EX-16 had not landed when this seat ran. This reconstructs the
authoritative spec (PL-2's patch text, the artifact EX-16 is instructed to apply
verbatim) in a scratch tree, so (a) the patch text's own fidelity is checkable
and (b) the four named checks plus the RV-7 attack set have a labelled reference
reading. This is NOT the landed artifact and must never be reported as one.

Read-only over the repo. Usage: python3 reconstruct-pl2.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
G = os.path.join(REPO, ".ufo/gates/citation-drift")
HERE = os.path.dirname(os.path.abspath(__file__))
PL2 = os.path.join(REPO, ".ufo/waves/arc3-loop1-round1/claims/c2/PL-2")
WORK = os.path.join(HERE, "tmp", "pl2")
PY = sys.executable

PIN = "738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f"
PL2_PROBE_SHA = "e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a"


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(args, cwd=None):
    env = dict(os.environ, TMPDIR=os.path.join(HERE, "tmp"))
    p = subprocess.run([PY] + args, capture_output=True, text=True, cwd=cwd, env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def verdict_of(out):
    v = [l for l in out.splitlines() if l.startswith("CITATION_DRIFT_VERDICT")]
    return v[-1] if v else "<none>"


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    root = os.path.join(WORK, "tree")
    gdir = os.path.join(root, ".ufo/gates/citation-drift")
    os.makedirs(gdir)
    for name in ("citation-drift-probe.py", "expected.json", "pointer-table.json"):
        shutil.copyfile(os.path.join(G, name), os.path.join(gdir, name))
    shutil.copyfile(os.path.join(REPO, "SKILL.md"), os.path.join(root, "SKILL.md"))
    print("=== RV-7 PL-2 reconstruction (NOT the landed artifact)")
    print("base probe sha256   : %s" % sha(os.path.join(gdir, "citation-drift-probe.py")))
    print("base expected sha256: %s" % sha(os.path.join(gdir, "expected.json")))

    # ---- extract patch 1 (the ```diff fence) from PL-2's patch text ----
    text = open(os.path.join(PL2, "frozen-run-guard.patch.md")).read()
    blocks = []
    cur = None
    for line in text.splitlines():
        if line.startswith("```diff"):
            cur = []
            continue
        if cur is not None and line.startswith("```"):
            blocks.append("\n".join(cur) + "\n")
            cur = None
            continue
        if cur is not None:
            cur.append(line)
    assert blocks, "no ```diff block found in PL-2 patch text"
    diff_path = os.path.join(WORK, "patch1.diff")
    open(diff_path, "w").write(blocks[0])
    print("extracted patch1: %d lines" % len(blocks[0].splitlines()))

    env = dict(os.environ, TMPDIR=os.path.join(HERE, "tmp"))
    p = subprocess.run(["patch", "-p1", "--dry-run", "-i", diff_path],
                       cwd=root, capture_output=True, text=True, env=env)
    print("patch --dry-run rc=%d %s" % (p.returncode, (p.stdout + p.stderr).strip().replace("\n", " | ")))
    p = subprocess.run(["patch", "-p1", "-i", diff_path],
                       cwd=root, capture_output=True, text=True, env=env)
    print("patch apply   rc=%d %s" % (p.returncode, (p.stdout + p.stderr).strip().replace("\n", " | ")))
    got = sha(os.path.join(gdir, "citation-drift-probe.py"))
    print("patched probe sha256: %s" % got)
    print("PL-2 claimed proto  : %s -> %s" % (PL2_PROBE_SHA, "MATCH" if got == PL2_PROBE_SHA else "DIFFERENT"))

    # ---- patch 2: the three expected.json text edits ----
    exp_path = os.path.join(gdir, "expected.json")
    t = open(exp_path).read()
    old_doc = ("the frozen-run baseline pins the digest of every snapshot input "
               "file, and")
    new_doc = ("the frozen-run baseline pins the digest of every snapshot input "
               "file AND of the pointer table itself (a tampered or absent table "
               "is could-not-evaluate, never silent findings), and")
    assert old_doc in t, "_doc anchor missing"
    t = t.replace(old_doc, new_doc, 1)
    snippet = ('"pointer_table": {"sha256": "%s", "note": "frozen-run guard (R6 debt, '
               'arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte '
               'difference is pointer_table_tampered, an absent table is pointer_table_unreadable, '
               'an unpinned baseline is pointer_table_unpinned -- all exit 2"}, ' % PIN)
    assert '"snapshots": {' in t, "snapshots anchor missing"
    t = t.replace('"snapshots": {', snippet + '"snapshots": {', 1)
    old_row = ('{"case": "rev_unresolvable", "exit_code": 2, "finding": '
               '"revision_unresolvable"}]')
    new_row = (old_row[:-1] + ', {"case": "table_tampered", "exit_code": 2, "finding": '
               '"pointer_table_tampered"}, {"case": "table_absent", "exit_code": 2, '
               '"finding": "pointer_table_unreadable"}]')
    assert old_row in t, "selftest row anchor missing"
    t = t.replace(old_row, new_row, 1)
    open(exp_path, "w").write(t)
    parsed = json.load(open(exp_path))
    print("patched expected sha256: %s" % sha(exp_path))
    print("cases=%d pin=%s" % (len(parsed["selftest"]),
                               (parsed.get("pointer_table") or {}).get("sha256")))

    # ---- the four named checks, against the reconstruction ----
    probe = os.path.join(gdir, "citation-drift-probe.py")
    print("\n--- four named checks on the reconstruction ---")
    rc, out = run([probe, "--selftest", "--expected", exp_path])
    tail = [l for l in out.splitlines() if l.startswith("CITATION_DRIFT_SELFTEST")]
    print("[N1-selftest] rc=%d | %s" % (rc, tail[-1] if tail else "<none>"))
    for lbl, extra in (("N2-rev-HEAD", []), ("N3-rev-deadbeef", ["--rev", "deadbeef"])):
        args = [probe, "--root", REPO, "--table", os.path.join(gdir, "pointer-table.json"),
                "--expected", exp_path]
        if not extra:
            args += ["--rev", "HEAD"]
        else:
            args += extra
        rc, out = run(args)
        n = len([l for l in out.splitlines() if l.startswith("CITATION_DRIFT:")])
        print("[%s] rc=%d findings=%d | %s" % (lbl, rc, n, verdict_of(out)))

    # ---- guard behaviour on the reconstruction ----
    print("\n--- guard behaviour (reconstruction) ---")
    empty = os.path.join(WORK, "table-empty.json")
    json.dump({"_doc": "x", "entries": [], "quoted": []}, open(empty, "w"))
    unpinned_obj = json.load(open(exp_path))
    del unpinned_obj["pointer_table"]
    unpinned = os.path.join(WORK, "expected-unpinned.json")
    json.dump(unpinned_obj, open(unpinned, "w"))
    tbl = os.path.join(gdir, "pointer-table.json")
    for lbl, args in (
            ("G1-real-table", [probe, "--root", REPO, "--rev", "HEAD", "--table", tbl, "--expected", exp_path]),
            ("G2-emptied-table", [probe, "--root", REPO, "--rev", "HEAD", "--table", empty, "--expected", exp_path]),
            ("G3-emptied-strict", [probe, "--root", REPO, "--rev", "HEAD", "--table", empty, "--expected", exp_path, "--strict"]),
            ("G4-absent-table", [probe, "--root", REPO, "--rev", "HEAD", "--table", os.path.join(WORK, "nope.json"), "--expected", exp_path]),
            ("G5-unpinned-expected-real-table", [probe, "--root", REPO, "--rev", "HEAD", "--table", tbl, "--expected", unpinned]),
            ("G6-unpinned-expected-emptied-table", [probe, "--root", REPO, "--rev", "HEAD", "--table", empty, "--expected", unpinned]),
            ("G7-byte-identical-copy", [probe, "--root", REPO, "--rev", "HEAD", "--table", os.path.join(WORK, "copy.json"), "--expected", exp_path]),
    ):
        if lbl == "G7-byte-identical-copy":
            shutil.copyfile(tbl, os.path.join(WORK, "copy.json"))
        rc, out = run(args)
        n = len([l for l in out.splitlines() if l.startswith("CITATION_DRIFT:")])
        ids = sorted({l.split()[1] for l in out.splitlines()
                      if l.startswith("CITATION_DRIFT:") and len(l.split()) > 1})
        print("[%s] rc=%d findings=%d ids=%s | %s" % (lbl, rc, n, ids, verdict_of(out)))

    print("\n=== reconstruction done (scratch at %s)" % WORK)


if __name__ == "__main__":
    main()
