#!/usr/bin/env python3
"""R31-C1 counter: REA 6.5.0 `inspect-sqlite-database --schema-scope database` on
12 published SQLite databases (5 PROJ proj.db from pyproj wheels, 2 Chinook release
databases, 5 GeoPackage fixtures from the pyogrio sdist), against an independent oracle.

Predicate P1-pass (frozen in .ufo/waves/round-31/claims.json): a carrier passes when its
live REA 6.5.0 run exits 0 with an ok envelope whose operation is inspect_sqlite_database
and whose subject sha256 equals the carrier's frozen sha256, and whose normalized_result,
without engine.version and limitations, equals the oracle's report field for field
(artifact, wal, engine name, database_encoding, and every table, index, view and trigger
with name, sql, root page, kind, without_rowid, strict, column count, column completeness
and all column fields; rows null); and its committed envelope, first added after the
freeze commit, equals the live envelope in every field except meta, and the round-31
entry names that evidence_id.  Doc gates: the entry cites S096 and PROVINCE.md holds a
table row naming inspect-sqlite-database and the entry under a heading that names Core
(placement, not co-occurrence; round-30 routed defect 6).

Prints `carriers=N pass=P target=12 entry_ok=E province_ok=V`; exit 0 only on target.
"""

import argparse
import csv
import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

TARGET = 12
REA = ["npx", "-y", "rea-agents@6.5.0"]
PKG_JSON = os.path.expanduser("~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json")
CLAIM_ROW = "S096"
ENTRY = "corpus/knowledge/2026-10-23-r31-sqlite-positive.md"
CARRIERS = "corpus/evidence/round-31/c1/carriers.tsv"
CLAIMS = ".ufo/waves/round-31/claims.json"
ENV_DIR = "corpus/evidence/round-31/c1/envelopes"
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "P1-pass"


def load_oracle():
    spec = importlib.util.spec_from_file_location("sqlite_oracle", os.path.join(HERE, "sqlite_oracle.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)


def show(root, rev, rel):
    p = git(root, "show", rev + ":" + rel)
    return p.stdout if p.returncode == 0 else None


def strip_meta(env):
    return {k: v for k, v in env.items() if k != "meta"} if isinstance(env, dict) else env


def judge(env, code, carrier_sha, expected, comparable):
    if not isinstance(env, dict):
        return "P1-fail", "no JSON envelope (exit %s)" % code
    if code != 0 or env.get("ok") is not True:
        return "P1-fail", "exit %s ok %r" % (code, env.get("ok"))
    data = env.get("data") or {}
    if data.get("operation") != "inspect_sqlite_database":
        return "P1-fail", "operation %r" % data.get("operation")
    if ((data.get("subject") or {}).get("digest") or {}).get("sha256") != carrier_sha:
        return "P1-fail", "subject sha256 differs from the frozen carrier"
    got = comparable(data.get("normalized_result") or {})
    if got != expected:
        diff = sorted(k for k in set(got) | set(expected) if got.get(k) != expected.get(k))
        if "schema" in diff:
            gs, es = got.get("schema") or {}, expected["schema"]
            diff += ["schema.%s" % k for k in es if gs.get(k) != es.get(k)]
        return "P1-fail", "report differs from the oracle: %s" % ",".join(diff)
    s = expected["schema"]
    return LABEL, "tables=%d indexes=%d views=%d triggers=%d columns=%d" % (
        len(s["tables"]), len(s["indexes"]), len(s["views"]), len(s["triggers"]),
        sum(len(t["columns"]) for t in s["tables"]))


def run_rea(path):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    argv = REA + ["inspect-sqlite-database", path, "--schema-scope", "database", "--format", "json", "--full-output"]
    p = subprocess.run(argv, capture_output=True, timeout=300, cwd="/tmp")
    end = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    return argv, p.returncode, p.stdout, p.stderr, start, end


def first_added(root, rel, rev):
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", rel)
    t = [int(x) for x in p.stdout.split()]
    return min(t) if t else None


def committed_check(root, rev, cid, live, freeze_ct, entry_text):
    rel = ENV_DIR + "/" + cid + ".json"
    text = show(root, rev, rel)
    if text is None:
        return False, "committed envelope absent"
    added = first_added(root, rel, rev)
    if freeze_ct is None or added is None or added <= freeze_ct:
        return False, "committed envelope not added after the freeze"
    try:
        committed = json.loads(text)
    except ValueError:
        return False, "committed envelope is not JSON"
    if strip_meta(committed) != strip_meta(live):
        return False, "committed envelope differs from the live envelope (full comparison)"
    eid = ((live or {}).get("data") or {}).get("evidence_id")
    if not eid or eid not in entry_text:
        return False, "entry does not name %s" % eid
    return True, "ok"


def entry_ok(text):
    if text is None:
        return False, "entry absent"
    if CLAIM_ROW not in text:
        return False, "entry does not cite %s" % CLAIM_ROW
    return True, "ok"


def province_ok(text):
    """A table row naming the verb and the entry whose governing heading names Core."""
    if not text:
        return False, "PROVINCE absent"
    heading = ""
    for ln in text.splitlines():
        if re.match(r"#{1,6} ", ln):
            heading = ln
            continue
        if ln.startswith("|") and "inspect-sqlite-database" in ln and ENTRY in ln:
            if "Core" in heading and not re.search(r"Frontier|Adjacent|exclusion", heading):
                return True, "ok"
            return False, "row sits under %r, not a Core heading" % heading[:60]
    return False, "no PROVINCE table row names the verb and the entry"


def measure(root, rev, write):
    frozen = show(root, rev, CARRIERS)
    if frozen is None:
        print("PIN pinned input absent: %s at %s" % (CARRIERS, rev))
        return 2
    if frozen != open(os.path.join(root, CARRIERS)).read():
        print("PIN carrier list in the tree differs from %s" % rev)
        return 2
    rows = list(csv.DictReader(frozen.splitlines(), delimiter="\t"))
    if len(rows) != TARGET:
        print("PIN carrier list has %d rows, frozen %d" % (len(rows), TARGET))
        return 2
    oracle = load_oracle()
    for r in rows:
        if not os.path.isfile(r["path"]) or oracle.sha256_file(r["path"]) != r["sha256"]:
            print("PIN carrier %s absent or altered at %s" % (r["id"], r["path"]))
            return 2
    if json.load(open(PKG_JSON))["version"] != "6.5.0":
        print("PIN package version")
        return 2
    pkg_sha = hashlib.sha256(open(PKG_JSON, "rb").read()).hexdigest()
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", CLAIMS)
    times = [int(x) for x in p.stdout.split()]
    freeze_ct = min(times) if times else None
    entry_text = show(root, rev, ENTRY)
    passed = 0
    runs = []
    for r in rows:
        expected = oracle.expected_report(r["path"])
        argv, code, out, err, start, end = run_rea(r["path"])
        try:
            env = json.loads(out)
        except ValueError:
            env = None
        verdict, reason = judge(env, code, r["sha256"], expected, oracle.comparable)
        if verdict == LABEL and not write:
            ok, why = committed_check(root, rev, r["id"], env, freeze_ct, entry_text or "")
            if not ok:
                verdict, reason = "P1-fail", why
        passed += verdict == LABEL
        print("%s\t%s\t%s" % (r["id"], verdict, reason))
        runs.append((r["id"], start, end, code, " ".join(argv), "6.5.0", pkg_sha, verdict, reason))
        if write:
            d = os.path.join(root, ENV_DIR)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, r["id"] + ".json"), "wb").write(out)
            open(os.path.join(d, r["id"] + ".stderr"), "wb").write(err)
    if write:
        with open(os.path.join(root, os.path.dirname(ENV_DIR), "runs.tsv"), "w") as f:
            f.write("id\tutc_start\tutc_end\texit\targv\tpkg_version\tpkg_json_sha256\tverdict\treason\n")
            for row in runs:
                f.write("\t".join(str(x) for x in row) + "\n")
    e_ok, e_why = entry_ok(entry_text)
    p_ok, p_why = province_ok(show(root, rev, "PROVINCE.md"))
    print("carriers=%d pass=%d target=%d entry_ok=%d (%s) province_ok=%d (%s)" % (
        len(rows), passed, TARGET, e_ok, e_why, p_ok, p_why))
    return 0 if passed == TARGET and e_ok and p_ok else 1


def selftest():
    fails = 0
    ident = lambda x: x
    exp = {"artifact": {"sha256": "a"}, "schema": {"tables": [], "indexes": [], "views": [], "triggers": []}}
    env = {"ok": True, "data": {"operation": "inspect_sqlite_database", "subject": {"digest": {"sha256": "a"}},
                                "normalized_result": exp}}
    other = json.loads(json.dumps(env))
    other["data"]["normalized_result"]["schema"]["views"] = [{"name": "v", "sql": None}]
    cases = [
        ("exact", env, 0, "a", LABEL),
        ("exit 1", env, 1, "a", "P1-fail"),
        ("wrong sha", env, 0, "b", "P1-fail"),
        ("schema differs", other, 0, "a", "P1-fail"),
        ("refusal", {"ok": False, "error": {}}, 1, "a", "P1-fail"),
        ("no envelope", None, 0, "a", "P1-fail"),
        ("wrong operation", json.loads(json.dumps(env).replace("inspect_sqlite_database", "inspect_artifact")), 0, "a", "P1-fail"),
    ]
    for name, e, code, sha, want in cases:
        got, why = judge(e, code, sha, exp, ident)
        ok = got == want
        fails += not ok
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, why))
    row = "| `inspect-sqlite-database` | x | y | `%s` |" % ENTRY
    prov = [
        ("row under Core heading", "## Core\n" + row, True),
        ("row under round Core-addition heading", "### Round-31 additions to Core\n" + row, True),
        ("row under Frontier", "## Frontier\n" + row, False),
        ("row under Adjacent exclusion", "## Adjacent — Core exclusion\n" + row, False),
        ("prose, not a table row", "## Core\ninspect-sqlite-database %s" % ENTRY, False),
        ("verb without entry", "## Core\n| `inspect-sqlite-database` |", False),
        ("absent", "", False),
    ]
    for name, text, want in prov:
        got, why = province_ok(text)
        ok = got == want
        fails += not ok
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, why))
    print("selftest cases=%d failures=%d" % (len(cases) + len(prov), fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--rev", default="main")
    ap.add_argument("--write-evidence", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        os.environ.pop(k, None)
    if a.selftest:
        sys.exit(selftest())
    sys.exit(measure(os.path.abspath(a.root), a.rev, a.write_evidence))


if __name__ == "__main__":
    main()
