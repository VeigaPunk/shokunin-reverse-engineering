#!/usr/bin/env python3
"""RV-7 extra attack set for the citation-drift frozen-run guard.

Cases the sibling seats' harnesses do not cover: byte-level false positives,
the unpinned-expected path, strict-vs-drift separation, consistent re-pin,
CWD independence, and the exactly-one-finding preflight property.

Read-only over the real repo; scratch under this seat's artifact dir.
Usage: python3 verify-extra.py --phase pre|post
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
WORK = os.path.join(HERE, "tmp", "extra")
PY = sys.executable


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(args, cwd=REPO):
    env = dict(os.environ, TMPDIR=os.path.join(HERE, "tmp"))
    p = subprocess.run([PY, PROBE] + args, capture_output=True, text=True,
                       cwd=cwd, env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def show(label, rc, out, note=""):
    lines = out.splitlines()
    verdict = [l for l in lines if l.startswith("CITATION_DRIFT_VERDICT")]
    findings = [l for l in lines if l.startswith("CITATION_DRIFT:")]
    ids = sorted({l.split()[1] for l in findings if len(l.split()) > 1})
    print("[%s] rc=%d findings=%d ids=%s" % (label, rc, len(findings), ids))
    print("      %s%s" % (verdict[-1] if verdict else "<NO VERDICT LINE>",
                          (" | " + note) if note else ""))
    return rc, len(findings), ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK, exist_ok=True)
    print("=== RV-7 extra attacks phase=%s HEAD=%s" % (
        a.phase, subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()))
    exp = json.load(open(EXP))
    # Peers proposed three pin shapes (PL-2 `pointer_table.sha256`, EX-21
    # `table_sha256`, EX-23 `frozen_run.table_sha256`), so discover the pin by
    # value rather than by name.
    def hex_paths(node, path=()):
        out = []
        if isinstance(node, dict):
            for k, v in node.items():
                out += hex_paths(v, path + (k,))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                out += hex_paths(v, path + (i,))
        elif isinstance(node, str) and len(node) == 64 and \
                all(c in "0123456789abcdef" for c in node):
            out.append((path, node))
        return out

    def find_pin(root_obj, want):
        for path, val in hex_paths(root_obj):
            if val == want:
                return path, val
        return None, None

    def set_pin(root_obj, digest):
        """Write `digest` into whichever key path holds the current table pin."""
        for path, _ in hex_paths(root_obj):
            if any("table" in str(p).lower() for p in path):
                node = root_obj
                for p in path[:-1]:
                    node = node[p]
                node[path[-1]] = digest
                return True
        return False

    def deep_unpin(node):
        """Remove any table-pin key, wherever it nests."""
        if isinstance(node, dict):
            for k in [k for k in node if "table" in str(k).lower()]:
                del node[k]
            for v in node.values():
                deep_unpin(v)
        elif isinstance(node, list):
            for v in node:
                deep_unpin(v)

    pin_path, pin = find_pin(exp, sha(TABLE))
    print("expected.json pin path = %s value=%s" % (pin_path or "<ABSENT>", pin or "<none>"))
    print("actual worktree table sha256 = %s" % sha(TABLE))
    head_bytes = subprocess.run(["git", "-C", REPO, "show",
                                 "HEAD:.ufo/gates/citation-drift/pointer-table.json"],
                                capture_output=True).stdout
    print("HEAD git-object table sha256 = %s" % hashlib.sha256(head_bytes).hexdigest())

    # X1 reformat-only (semantically identical bytes differ)
    d = json.load(open(TABLE))
    reformat = os.path.join(WORK, "table-reformatted.json")
    json.dump(d, open(reformat, "w"), indent=4, sort_keys=True)
    assert json.load(open(reformat)) == d
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", reformat, "--expected", EXP])
    show("X1-reformat-only-table", rc, out, "byte-level pin vs semantic identity")

    # X2/X3 unpinned expected.json (every table-pin key removed, wherever nested)
    unpinned_obj = json.load(open(EXP))
    deep_unpin(unpinned_obj)
    unpinned = os.path.join(WORK, "expected-unpinned.json")
    json.dump(unpinned_obj, open(unpinned, "w"))
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", TABLE, "--expected", unpinned])
    show("X2-unpinned-expected-real-table", rc, out)
    emptied = os.path.join(WORK, "table-emptied.json")
    json.dump({"_doc": "x", "entries": [], "quoted": []}, open(emptied, "w"))
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", emptied, "--expected", unpinned])
    show("X3-unpinned-expected-tampered-table", rc, out,
         "silent-clean here = residual hole, not a guard failure")

    # X4/X5 strict separation: drift must stay 1, never 2
    old = "6645585873c4e66372b15687c47000abf8d91978"
    if subprocess.run(["git", "-C", REPO, "cat-file", "-e", old + "^{commit}"],
                      capture_output=True).returncode == 0:
        for lbl, extra in (("X4-oldrev-probe", []), ("X4-oldrev-strict", ["--strict"])):
            rc, out = run(["--root", REPO, "--rev", old] + extra)
            show(lbl, rc, out, "drift must not be swallowed into the guard's 2")

    # X6 consistent re-pin: tampered table + matching pin reads clean
    repin = json.load(open(EXP))
    repinned = set_pin(repin, sha(emptied))
    print("[X6] re-pin written into the discovered pin path: %s" % repinned)
    rp = os.path.join(WORK, "expected-repinned.json")
    json.dump(repin, open(rp, "w"))
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", emptied, "--expected", rp])
    show("X6-consistent-repin", rc, out, "scope boundary: pin guards drift, not an author re-pin")

    # X11 the recorded r10 experiment shape: custom table + COMMITTED expected
    # (RV-8's S2 consumer shape; a different-but-honest table, not a tamper)
    honest = json.load(open(TABLE))
    honest["entries"] = honest["entries"][:-1]          # a legitimately narrower table
    honest_tbl = os.path.join(WORK, "table-honest-narrowed.json")
    json.dump(honest, open(honest_tbl, "w"))
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", honest_tbl, "--expected", EXP])
    show("X11-honest-custom-table-vs-committed-expected", rc, out,
         "exit 2 here = r10-style experiment recipes now need their own expected file")

    # X7 CWD independence (default paths, foreign cwd)
    rc, out = run(["--root", REPO, "--rev", "HEAD"], cwd=WORK)
    show("X7-foreign-cwd-default-paths", rc, out)

    # X8 exactly-one-finding preflight property on a tamper
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", emptied, "--expected", EXP])
    n = len([l for l in out.splitlines() if l.startswith("CITATION_DRIFT:")])
    print("[X8-preflight-single-finding] rc=%d finding_lines=%d (1 = entries not evaluated)"
          % (rc, n))

    # X9 symlinked table follows the target's bytes
    link = os.path.join(WORK, "table-link.json")
    if not os.path.islink(link):
        os.symlink(TABLE, link)
    rc, out = run(["--root", REPO, "--rev", "HEAD", "--table", link, "--expected", EXP])
    show("X9-symlinked-table", rc, out)

    # X10 both pin sources must agree (expected.json pin vs the table the entry run uses)
    print("[X10] pin==worktree: %s | pin==HEAD-object: %s" % (
        pin == sha(TABLE) if pin else "n/a",
        pin == hashlib.sha256(head_bytes).hexdigest() if pin else "n/a"))
    print("=== RV-7 extra attacks phase=%s done" % a.phase)


if __name__ == "__main__":
    main()
