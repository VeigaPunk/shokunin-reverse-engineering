#!/usr/bin/env python3
"""RV-7 independent verification harness — citation-drift frozen-run guard.

Read-only over the real repo. Every mutated input is written under /tmp/rv7.
Usage: python3 verify.py --phase pre|post
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
# Defaults to the real target; RV7_GATE_DIR points the same harness at a
# scratch reconstruction so the two readings are directly comparable.
G = os.environ.get("RV7_GATE_DIR") or os.path.join(REPO, ".ufo/gates/citation-drift")
PROBE = os.path.join(G, "citation-drift-probe.py")
EXP = os.path.join(G, "expected.json")
TABLE = os.path.join(G, "pointer-table.json")
HERE = os.path.dirname(os.path.abspath(__file__))
# /tmp is user-quota-blocked this wave (Errno 122, RV-6 recorded the same wall),
# so scratch lives in this seat's artifact dir and is removed at the end.
WORK = os.path.join(HERE, "tmp", "work")
PY = sys.executable


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def run(args, cwd=REPO):
    env = dict(os.environ, TMPDIR=os.path.join(HERE, "tmp"))
    p = subprocess.run([PY, PROBE] + args, capture_output=True, text=True,
                       cwd=cwd, env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def summarize(out):
    lines = out.splitlines()
    verdict = [l for l in lines if l.startswith("CITATION_DRIFT_VERDICT")]
    findings = [l for l in lines if l.startswith("CITATION_DRIFT:")]
    ids = sorted({l.split()[1] for l in findings if len(l.split()) > 1})
    return (verdict[-1] if verdict else "<NO VERDICT LINE>"), len(findings), ids


def case(label, args, expect=None):
    rc, out = run(args)
    v, n, ids = summarize(out)
    silent = rc == 0 and n == 0
    print("[%s] rc=%d findings=%d ids=%s" % (label, rc, n, ids))
    print("      %s" % v)
    print("      silent_clean=%s" % ("YES" if silent else "no"))
    if expect is not None:
        print("      expect_rc=%s -> %s" % (expect, "MATCH" if rc == expect else "MISMATCH"))
    return rc, n, ids, v


def find_pin(exp_obj, digest):
    """Locate any pinned pointer-table digest inside expected.json."""
    hits = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + [str(i)])
        elif isinstance(node, str):
            if node == digest:
                hits.append(".".join(path))
            if digest[:16] in node:
                hits.append(".".join(path) + " (prefix-hit)")
    walk(exp_obj, [])
    return hits


def selftest(expected_path, tag):
    rc, out = run(["--selftest", "--expected", expected_path])
    tail = [l for l in out.splitlines() if l.startswith("CITATION_DRIFT_SELFTEST")]
    print("[%s] rc=%d | %s" % (tag, rc, tail[-1] if tail else "<no summary>"))
    return rc, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    args = ap.parse_args()

    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    print("=== RV-7 verify phase=%s repo_HEAD=%s" % (
        args.phase,
        subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"],
                       capture_output=True, text=True).stdout.strip()))

    exp_obj = json.load(open(EXP))
    table_digest = sha(TABLE)
    print("gate file digests:")
    for name in sorted(os.listdir(G)):
        p = os.path.join(G, name)
        if os.path.isfile(p):
            print("  %s  %s" % (sha(p), name))
    print("expected.json top-level keys: %s" % sorted(exp_obj.keys()))
    print("selftest cases: %s" % [c["case"] for c in exp_obj.get("selftest", [])])
    print("pin-for-table-digest in expected.json: %s" % (find_pin(exp_obj, table_digest) or "NONE"))
    print("snapshots keys: %s" % sorted((exp_obj.get("snapshots") or {}).keys()))

    # ---- C0: the four named checks ----
    print("\n--- C0 named checks ---")
    case("C0-probe-HEAD-default", ["--root", REPO, "--rev", "HEAD"], 0)
    case("C0-probe-HEAD-strict", ["--root", REPO, "--rev", "HEAD", "--strict"], 0)
    case("C0-rev-deadbeef", ["--root", REPO, "--rev", "deadbeef"], 2)
    case("C0-rev-deadbeef-strict", ["--root", REPO, "--rev", "deadbeef", "--strict"], 2)

    # ---- C1..C5: table mutations, real expected.json ----
    print("\n--- C1-C5 table mutations vs the real expected.json ---")
    absent = os.path.join(WORK, "does-not-exist.json")
    empty = os.path.join(WORK, "table-empty.json")
    json.dump({"_doc": "x", "entries": [], "quoted": []}, open(empty, "w"))
    weak = os.path.join(WORK, "table-weakened.json")
    d = json.load(open(TABLE))
    for e in d.get("entries", []) + d.get("quoted", []):
        e["must_match"] = ".*"
    json.dump(d, open(weak, "w"))
    copy = os.path.join(WORK, "table-identical-copy.json")
    shutil.copyfile(TABLE, copy)
    flip = os.path.join(WORK, "table-onebyte.json")
    raw = open(TABLE, "rb").read()
    i = raw.find(b"SCORECARD.md")
    assert i > 0, "anchor string not found in table"
    open(flip, "wb").write(raw[:i] + b"SCORECARD.md".replace(b"S", b"Z") + raw[i + 12:])
    json.load(open(flip))  # must stay valid JSON

    for label, tbl in (("C1-table-absent", absent), ("C2-table-emptied", empty),
                       ("C3-table-weakened", weak), ("C4-table-identical-copy", copy),
                       ("C5-table-onebyte", flip)):
        for strict in (False, True):
            a = ["--root", REPO, "--rev", "HEAD", "--table", tbl, "--expected", EXP]
            if strict:
                a.append("--strict")
            case(label + ("-strict" if strict else ""), a)

    # ---- C6: whole-dir copy with a tampered table, default paths ----
    print("\n--- C6 whole-dir copy, tampered table at the copied default path ---")
    gcopy = os.path.join(WORK, "gate-copy")
    shutil.copytree(G, gcopy)
    json.dump({"_doc": "x", "entries": [], "quoted": []},
              open(os.path.join(gcopy, "pointer-table.json"), "w"))
    rc, out = run(["--root", REPO, "--rev", "HEAD",
                   "--table", os.path.join(gcopy, "pointer-table.json"),
                   "--expected", os.path.join(gcopy, "expected.json")])
    v, n, ids = summarize(out)
    print("[C6-copied-dir-tampered] rc=%d findings=%d ids=%s" % (rc, n, ids))
    print("      %s" % v)
    print("      silent_clean=%s" % ("YES" if rc == 0 and n == 0 else "no"))

    # ---- C8: the guard must not mask real drift ----
    print("\n--- C8 drift preservation at an old rev ---")
    for rev in ("6645585873c4e66372b15687c47000abf8d91978", "HEAD~10"):
        ok = subprocess.run(["git", "-C", REPO, "cat-file", "-e", rev + "^{commit}"],
                            capture_output=True).returncode == 0
        if not ok:
            print("[C8-%s] rev not present, skipped" % rev)
            continue
        rc, out = run(["--root", REPO, "--rev", rev])
        v, n, ids = summarize(out)
        print("[C8-%s] rc=%d findings=%d ids=%s" % (rev[:12], rc, n, ids[:4]))
        print("      %s" % v)

    # ---- C9: pin self-consistency ----
    print("\n--- C9 pin self-consistency ---")
    head_table = subprocess.run(["git", "-C", REPO, "show", "HEAD:.ufo/gates/citation-drift/pointer-table.json"],
                                capture_output=True).stdout
    print("worktree table sha256 : %s" % table_digest)
    print("HEAD-object table     : %s" % sha_bytes(head_table))
    print("worktree==HEAD-object : %s" % (table_digest == sha_bytes(head_table)))
    print("pinned digest match   : %s" % (find_pin(exp_obj, table_digest) or "NO PIN FOUND"))

    # ---- C10: selftest ----
    print("\n--- C10 selftest ---")
    rc, _ = selftest(EXP, "C10-selftest")

    # ---- C11/C12: mutation-sensitivity sweep (anti-tautology) ----
    print("\n--- C11/C12 selftest case-table sensitivity sweep ---")
    if rc != 0:
        print("selftest already red at this phase; sweep still runs to show which assertions bite")
    cases = exp_obj.get("selftest", [])
    for field, mk in (("exit_code", lambda c: {"0": 1, "1": 2, "2": 0}[str(c["exit_code"])]),
                      ("finding", lambda c: "zzz-nonexistent-id")):
        for idx, c in enumerate(cases):
            m = json.load(open(EXP))
            m["selftest"][idx][field] = mk(c)
            p = os.path.join(WORK, "exp-mut-%s-%d.json" % (field, idx))
            json.dump(m, open(p, "w"))
            mrc, out = run(["--selftest", "--expected", p])
            tail = [l for l in out.splitlines() if l.startswith("CITATION_DRIFT_SELFTEST")]
            print("  [sweep-%s case=%s] mutated->rc=%d %s" % (
                field, c["case"], mrc, tail[-1] if tail else "<no summary>"))

    print("\n=== RV-7 verify phase=%s done" % args.phase)


if __name__ == "__main__":
    main()
