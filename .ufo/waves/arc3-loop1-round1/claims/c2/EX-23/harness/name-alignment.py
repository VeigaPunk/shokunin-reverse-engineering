#!/usr/bin/env python3
"""EX-23 name-alignment check: re-run the census's key rows under PL-2's
planned naming (pin key `pointer_table.sha256`, unpinned id
`pointer_table_unpinned`, tampered `pointer_table_tampered`), so the census
rows hold for the shape EX-16 is most likely to land.

Measured rows: H1 (honest re-key), C0 (clean), C1 (coupled re-pin), C3 (absent
table), C5 (no pin), C7 (malformed pin)."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SRC = os.path.join(BASE, "head-citation-drift-probe.py")
TABLE = os.path.join(BASE, "head-pointer-table.json")
EXPECTED = os.path.join(BASE, "head-expected.json")

GUARD = '''    try:
        table_bytes = open(table_path, "rb").read()
    except OSError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path),
                     str(exc))
        return findings
    pin_block = expected.get("pointer_table")
    pinned_table = pin_block.get("sha256") if isinstance(pin_block, dict) else None
    if not isinstance(pinned_table, str) or len(pinned_table) != 64:
        findings.add("pointer_table_unpinned", os.path.basename(table_path),
                     "no usable table digest pinned in expected.json")
        return findings
    if sha256_bytes(table_bytes) != pinned_table:
        findings.add("pointer_table_tampered", os.path.basename(table_path),
                     "sha256 %s != pinned %s" % (sha256_bytes(table_bytes),
                                                 pinned_table))
        return findings
    tree = Tree(root, rev, snapshot_dir, expected, findings)
'''
ANCHOR = "    tree = Tree(root, rev, snapshot_dir, expected, findings)\n"
CNE_OLD = ('        if any(f in ("snapshot_tampered", "snapshot_missing",\n'
           '                     "pointer_table_unreadable", "unpinned_legacy",\n')
CNE_NEW = ('        if any(f in ("snapshot_tampered", "snapshot_missing",\n'
           '                     "pointer_table_unreadable", "pointer_table_tampered",\n'
           '                     "pointer_table_unpinned", "unpinned_legacy",\n')


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    src = open(SRC, encoding="utf-8").read()
    assert ANCHOR in src and CNE_OLD in src
    out = src.replace(ANCHOR, GUARD, 1).replace(CNE_OLD, CNE_NEW, 1)
    probe = os.path.join(BASE, "guardP.py")
    open(probe, "w", encoding="utf-8").write(out)

    pristine = open(TABLE, "rb").read()
    base_exp = json.loads(open(EXPECTED, encoding="utf-8").read())

    def table_with(edit):
        obj = json.loads(pristine)
        edit(obj)
        return (json.dumps(obj, indent=2) + "\n").encode()

    def entry(obj, eid):
        return next(x for x in obj["entries"] if x["id"] == eid)

    cases = {
        "H1-rekey": (table_with(lambda o: entry(o, "sc59-stanza-key-anchor")
                                .update(line=60)), "pin"),
        "C0-clean": (pristine, "pin"),
        "C1-repin": (table_with(lambda o: entry(o, "sc270-dated-record")
                                .update(note="reworded")), "repin"),
        "C3-absent": (None, "pin"),
        "C5-nopin": (pristine, "drop"),
        "C7-malformed": (pristine, "junk"),
    }
    for name, (tb, mode) in cases.items():
        d = tempfile.mkdtemp(dir=BASE, prefix="namecheck-")
        tp = os.path.join(d, "pointer-table.json")
        ep = os.path.join(d, "expected.json")
        if tb is not None:
            open(tp, "wb").write(tb)
        exp = json.loads(json.dumps(base_exp))
        if mode == "pin":
            exp["pointer_table"] = {"sha256": sha256_bytes(pristine)}
        elif mode == "repin":
            exp["pointer_table"] = {"sha256": sha256_bytes(tb)}
        elif mode == "junk":
            exp["pointer_table"] = {"sha256": "deadbeef"}
        json.dump(exp, open(ep, "w"))
        line = []
        for sem in (False, True):
            args = [sys.executable, probe, "--root", REPO, "--rev", "HEAD",
                    "--table", tp, "--expected", ep]
            if sem:
                args.append("--strict")
            p = subprocess.run(args, capture_output=True, text=True, timeout=120)
            fid = [l.split()[1] for l in p.stdout.splitlines()
                   if l.startswith("CITATION_DRIFT: ")]
            line.append("%s=%d%s" % ("strict" if sem else "probe",
                                     p.returncode, ("[" + ",".join(fid) + "]") if fid else ""))
        print("%-12s %s" % (name, "  ".join(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
