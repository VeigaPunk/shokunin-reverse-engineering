#!/usr/bin/env python3
"""EX-23 false-positive census harness (scratch copy; /tmp quota-blocked,
relocated to ~/.cache/kaidoku-scratch/ex23 per the standing /tmp hazard).

Target: the DECLARED C2 frozen-run guard ("pins the sha256 of
pointer-table.json in expected.json; a tampered or absent table yields the
declared preflight could-not-evaluate class (exit 2), never silent findings").

Two guard variants are generated from the HEAD probe bytes:
  guardA  guard block, finding id `pointer_table_tampered` NOT registered in
          Findings.verdict()'s CNE tuple  (the "forgot the registry" variant)
  guardB  same block + the id registered in the CNE tuple

Scenarios mutate a scratch table and/or expected.json and run both variants
under probe semantics (default) and gate semantics (--strict); exit code,
finding lines, verdict line and traceback presence are recorded.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SRC = os.path.join(BASE, "head-citation-drift-probe.py")
CLEAN_TABLE = os.path.join(BASE, "head-pointer-table.json")
CLEAN_EXPECTED = os.path.join(BASE, "head-expected.json")
WORK = os.path.join(BASE, "work")

GUARD_BLOCK = '''    # Frozen-run guard: the table is the contract, so its bytes are pinned in
    # expected.json. The run cannot tell an honest in-flight re-key from a
    # tamper, so a digest mismatch is could-not-evaluate, never a finding set.
    try:
        table_bytes = open(table_path, "rb").read()
    except OSError as exc:
        findings.add("pointer_table_unreadable", os.path.basename(table_path),
                     str(exc))
        return findings
    pinned_table = (expected.get("frozen_run") or {}).get("table_sha256")
    if pinned_table is None:
        findings.add("unpinned_legacy", os.path.basename(table_path),
                     "no table digest pinned in expected.json")
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
           '                     "unpinned_legacy",\n')


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def make_variants():
    src = open(SRC, encoding="utf-8").read()
    assert ANCHOR in src and CNE_OLD in src
    a = src.replace(ANCHOR, GUARD_BLOCK, 1)
    b = a.replace(CNE_OLD, CNE_NEW, 1)
    paths = {}
    for name, text in (("guardA", a), ("guardB", b)):
        p = os.path.join(BASE, "%s.py" % name)
        open(p, "w", encoding="utf-8").write(text)
        paths[name] = p
    return paths


def tbl(edit):
    """Pristine table -> apply edit(obj) -> re-serialize (indent=2 + newline,
    the committed file's shape). Returns a bytes thunk."""
    def go():
        obj = json.loads(open(CLEAN_TABLE, encoding="utf-8").read())
        edit(obj)
        return (json.dumps(obj, indent=2) + "\n").encode()
    return go


def pristine():
    return open(CLEAN_TABLE, "rb").read()


def e(obj, eid):
    for x in obj["entries"]:
        if x["id"] == eid:
            return x
    raise KeyError(eid)


def pin_pristine(exp, actual):
    exp["frozen_run"]["table_sha256"] = sha256_bytes(pristine())


def pin_actual(exp, actual):
    if actual is not None:
        exp["frozen_run"]["table_sha256"] = actual


def drop_pin(exp, actual):
    exp["frozen_run"].pop("table_sha256", None)


SCENARIOS = [
    # ---- honest in-flight edits (the census proper) ----------------------
    ("H1-rekey-line", "honest",
     tbl(lambda o: e(o, "sc59-stanza-key-anchor").update(line=60)), pin_pristine,
     "probe-table re-key: SCORECARD.md:59 -> :60 after a legitimate shift "
     "(the r8 'census SCOPE re-key + probe re-pin coupled' class, 6bc4c29)"),
    ("H2-needle-fix", "honest",
     tbl(lambda o: e(o, "readme175-sc1217").update(must_match="id-stability debt")),
     pin_pristine,
     "in-round needle correction (02c45d5's readme175-sc1217 fix class)"),
    ("H3-entry-add", "honest",
     tbl(lambda o: o["entries"].append(
         {"id": "new-anchor", "kind": "anchor", "file": "PROVINCE.md",
          "must_match": "Core surface", "note": "r10-style extension"})),
     pin_pristine,
     "entry addition (dbae324's 13 -> 31 extension class)"),
    ("H4-entry-retire", "honest",
     tbl(lambda o: o["entries"].__delitem__(
         next(i for i, x in enumerate(o["entries"])
              if x["id"] == "sc698-sc2-refuted-record"))),
     pin_pristine,
     "entry retirement (dead pointer removed)"),
    ("H5-quoted-append", "honest",
     tbl(lambda o: o["quoted"].append(
         {"id": "log-new-quoted", "file": "LOG.md", "line": 1012,
          "must_match": "claim Kimi", "note": "append-only record"})),
     pin_pristine,
     "quoted-array append (085ca3c's LOG quoted-pin class)"),
    ("H6-note-only", "honest",
     tbl(lambda o: e(o, "sc270-dated-record").update(note="reworded note")),
     pin_pristine,
     "note-only edit: JSON semantics unchanged, bytes changed"),
    ("H7-exempt-add", "honest",
     tbl(lambda o: o["exempt"].append(
         {"token": "SCORECARD.md:999 `config.toml:N`", "cause": "dated record"})),
     pin_pristine,
     "exempt-list edit"),
    ("H8-reformat", "honest",
     lambda: (json.dumps(json.loads(open(CLEAN_TABLE, encoding='utf-8').read()),
                         indent=4) + "\n").encode(),
     pin_pristine,
     "pure reformat (indent 2 -> 4): zero semantic change, byte delta"),
    ("H9-receipt-anchor", "honest",
     tbl(lambda o: e(o, "sc59-receipt-stamp").update(
         must_match="2026-10-19T06:00:00Z custody receipt")),
     pin_pristine,
     "receipt-anchored update: re-anchor to a new round's receipt stamp"),
    ("H10-doc-note", "honest",
     tbl(lambda o: o.update(_doc=o["_doc"] + " Extended arc3-loop1-round1.")),
     pin_pristine,
     "table _doc extension note (the r10 table documents its own extension)"),
    ("H11-old-rev-table", "honest",
     lambda: subprocess.run(
         ["git", "-C", REPO, "show",
          "265e1aa:.ufo/gates/citation-drift/pointer-table.json"],
         capture_output=True, check=True).stdout,
     pin_pristine,
     "cross-revision replay: an OLD revision's table bytes run against the "
     "current expected.json pin (the lane's 're-derived from git archive "
     "trees at the cited commits' workflow)"),
    # ---- controls --------------------------------------------------------
    ("C0-clean", "control", pristine, pin_pristine,
     "control: pristine table, pin matches -> must be exit 0"),
    ("C1-coupled-repin", "control",
     tbl(lambda o: e(o, "sc270-dated-record").update(note="reworded note")),
     pin_actual,
     "control: honest edit + same-commit re-pin -> must be exit 0"),
    ("C2-tamper", "control",
     tbl(lambda o: e(o, "sc59-stanza-key-anchor").update(
         must_match="^totally wrong$")),
     pin_pristine,
     "control: semantic tamper, no re-pin -> indistinguishable from H1 at the "
     "digest level"),
    ("C3-absent-table", "control", None, pin_pristine,
     "control: table file deleted"),
    ("C4-unreadable-table", "control",
     lambda: b"{ not json", pin_pristine,
     "control: table bytes invalid JSON, pin is the pristine digest"),
    ("C5-legacy-no-pin", "control", pristine, drop_pin,
     "control: expected.json carries NO table pin (every pre-pin revision, "
     "including current HEAD, is this state)"),
    ("C6-expected-absent", "control", pristine, pin_pristine,
     "control: expected.json deleted"),
    ("C7-pin-malformed", "control", pristine,
     lambda exp, actual: exp["frozen_run"].update(table_sha256="deadbeef"),
     "control: pin present but malformed (short hex)"),
    ("C8-table-is-dir", "control", None, pin_pristine,
     "control: --table path is a directory"),
    ("C9-binary-table", "control",
     lambda: b"\xff\xfe\x00\x01binary", pin_pristine,
     "control: table bytes are not UTF-8"),
    ("C10-pin-matches-badjson", "control",
     lambda: b"{ not json", pin_actual,
     "control: pin matches, but the table bytes are invalid JSON -> the "
     "existing pointer_table_unreadable class must still fire"),
]


SPECIALS = {
    "C6-expected-absent": "expected_absent",
    "C8-table-is-dir": "table_is_dir",
}


def build_case(name, table_mut, expected_mut, special):
    d = tempfile.mkdtemp(dir=WORK, prefix=name + "-")
    table_path = os.path.join(d, "pointer-table.json")
    expected_path = os.path.join(d, "expected.json")
    actual = None
    if special == "table_is_dir":
        os.makedirs(table_path)
    elif table_mut is not None:
        tb = table_mut()
        if tb is not None:
            open(table_path, "wb").write(tb)
            actual = sha256_bytes(tb)
    exp = json.loads(open(CLEAN_EXPECTED, encoding="utf-8").read())
    exp.setdefault("frozen_run", {})["table_sha256"] = sha256_bytes(pristine())
    expected_mut(exp, actual)
    if special != "expected_absent":
        json.dump(exp, open(expected_path, "w"))
    return d, table_path, expected_path


def run_one(probe, table_path, expected_path, strict):
    args = [sys.executable, probe, "--root", REPO, "--rev", "HEAD",
            "--table", table_path, "--expected", expected_path]
    if strict:
        args.append("--strict")
    p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    findings = [l for l in p.stdout.splitlines() if l.startswith("CITATION_DRIFT: ")]
    verdict = [l for l in p.stdout.splitlines()
               if l.startswith("CITATION_DRIFT_VERDICT:")]
    return {
        "exit": p.returncode,
        "findings": findings,
        "verdict": verdict[0] if verdict else "<none>",
        "traceback": "Traceback" in p.stderr,
    }


def run_selftest(probe, expected_path):
    p = subprocess.run([sys.executable, probe, "--selftest",
                        "--expected", expected_path],
                       capture_output=True, text=True, timeout=300)
    lines = [l for l in p.stdout.splitlines() if l.startswith("SELFTEST_CASE:")]
    summary = [l for l in p.stdout.splitlines()
               if l.startswith("CITATION_DRIFT_SELFTEST:")]
    bad = [l for l in lines if " CLEAN " not in l]
    return {"exit": p.returncode,
            "summary": summary[0] if summary else "<none>",
            "failing_cases": bad,
            "traceback": "Traceback" in p.stderr}


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    probes = make_variants()
    rows = []
    for name, klass, tmut, emut, note in SCENARIOS:
        special = SPECIALS.get(name, "")
        d, tp, ep = build_case(name, tmut, emut, special)
        row = {"scenario": name, "class": klass, "note": note}
        for variant, probe in probes.items():
            for sem in ("probe", "strict"):
                row["%s/%s" % (variant, sem)] = run_one(
                    probe, tp, ep, strict=(sem == "strict"))
        rows.append(row)
        print("== %s (%s) ==" % (name, klass))
        for variant in probes:
            for sem in ("probe", "strict"):
                r = row["%s/%s" % (variant, sem)]
                first = r["findings"][0] if r["findings"] else ""
                print("   %-7s %-6s exit=%d tb=%s | %s | %s" %
                      (variant, sem, r["exit"], r["traceback"],
                       r["verdict"], first[:150]))
        shutil.rmtree(d, ignore_errors=True)

    # selftest interaction: the guard against the probe's own fixtures
    st = {}
    exp_with_pin = os.path.join(BASE, "expected-with-pin.json")
    exp = json.loads(open(CLEAN_EXPECTED, encoding="utf-8").read())
    exp.setdefault("frozen_run", {})["table_sha256"] = sha256_bytes(pristine())
    json.dump(exp, open(exp_with_pin, "w"))
    for variant, probe in probes.items():
        st[variant] = run_selftest(probe, exp_with_pin)
        print("== SELFTEST %s ==" % variant)
        print("   exit=%d tb=%s | %s" % (st[variant]["exit"],
                                         st[variant]["traceback"],
                                         st[variant]["summary"]))
        for l in st[variant]["failing_cases"][:14]:
            print("   " + l)
    st["_baseline"] = run_selftest(SRC, CLEAN_EXPECTED)
    print("== SELFTEST baseline (unguarded HEAD probe) ==")
    print("   exit=%d | %s" % (st["_baseline"]["exit"], st["_baseline"]["summary"]))

    out = os.path.join(BASE, "census-results.json")
    json.dump({"scenarios": rows, "selftest": st}, open(out, "w"), indent=2)
    print("\nresults -> %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
