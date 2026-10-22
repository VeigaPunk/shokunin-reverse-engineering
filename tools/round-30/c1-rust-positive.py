#!/usr/bin/env python3
"""R30-C1 counter: REA 6.5.0 `inspect-rust-binary` on the positive edge class.

Frozen predicate P1 (the same sentence is in .ufo/waves/round-30/claims.json):
  "A carrier passes when its live REA 6.5.0 inspect-rust-binary run exits 0 with
   an ok envelope whose operation is inspect_rust_binary and whose subject sha256
   equals the carrier's frozen sha256, and whose auditable_metadata package list
   equals, as a multiset of (name, version, source, kind, root, dependency
   (name, version) set) tuples, the non-empty list that the independent oracle
   decodes from the carrier's own .dep-v0 section, with REA's file_offset and
   compressed_bytes equal to the oracle's section offset and size; and its
   committed envelope, first added after the freeze commit, carries the same
   evidence_id and package multiset, and the round-30 entry names that
   evidence_id."

Every carrier is run live by this counter (a committed envelope is a record,
never the scored value; the committed envelope must agree with it). Exit 0 only
when pass == TARGET (16 of 16 frozen carriers), entry_ok and province_ok all
hold; exit 1 when measured but not met; exit 2 when a pinned input is absent or
altered. --write-evidence writes the envelopes and runs.tsv (data collection);
the committed-envelope clause is then checked on the next run.

Usage:
  c1-rust-positive.py --root <LANE> [--write-evidence] [--envelopes-dir DIR]
  c1-rust-positive.py --selftest
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

TARGET = 16
REA = ["npx", "-y", "rea-agents@6.5.0"]
PKG_JSON = os.path.expanduser("~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json")
CLAIM_ROW = "S089"
ENTRY = "corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md"
CARRIERS = "corpus/evidence/round-30/c1/carriers.tsv"
BASE = "d210fb8fa62d2af04d009cfa0c65a4e8137dc742"
HERE = os.path.dirname(os.path.abspath(__file__))
PASS_LABEL = "P1-pass"


def load_oracle():
    spec = importlib.util.spec_from_file_location("rust_dep_oracle", os.path.join(HERE, "rust_dep_oracle.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_metadata(node):
    """All distinct auditable_metadata values anywhere under node."""
    found = []
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == "auditable_metadata":
                    found.append(v)
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(node)
    uniq = []
    for v in found:
        if v not in uniq:
            uniq.append(v)
    return uniq


def rea_tuples(meta):
    pk = meta["packages"]
    out = []
    for p in pk:
        deps = tuple(sorted((pk[i]["name"], pk[i]["version"]) for i in p.get("dependencies", [])))
        out.append((p["name"], p["version"], p["source"], p.get("kind"), bool(p.get("root", False)), deps))
    return sorted(out, key=repr)


def judge(env, carrier_sha, oracle_sec, oracle_tuples, exit_code):
    """Return (verdict, reason). verdict is PASS_LABEL or 'P1-fail'."""
    if exit_code != 0:
        return "P1-fail", "exit %s" % exit_code
    if not isinstance(env, dict) or env.get("ok") is not True:
        return "P1-fail", "envelope not ok"
    data = env.get("data") or {}
    if data.get("operation") != "inspect_rust_binary":
        return "P1-fail", "operation %r" % data.get("operation")
    sub = ((data.get("subject") or {}).get("digest") or {}).get("sha256")
    if sub != carrier_sha:
        return "P1-fail", "subject sha256 %r" % sub
    metas = find_metadata(data)
    if len(metas) != 1 or not isinstance(metas[0], dict):
        return "P1-fail", "auditable_metadata count %d or null" % len(metas)
    meta = metas[0]
    if not oracle_tuples:
        return "P1-fail", "oracle list empty"
    try:
        got = rea_tuples(meta)
    except (KeyError, IndexError, TypeError) as e:
        return "P1-fail", "metadata shape %s" % e
    if got != oracle_tuples:
        return "P1-fail", "package multiset differs (rea %d, oracle %d)" % (len(got), len(oracle_tuples))
    if meta.get("file_offset") != oracle_sec["offset"]:
        return "P1-fail", "file_offset %r != %r" % (meta.get("file_offset"), oracle_sec["offset"])
    if meta.get("compressed_bytes") != oracle_sec["size"]:
        return "P1-fail", "compressed_bytes %r != %r" % (meta.get("compressed_bytes"), oracle_sec["size"])
    return PASS_LABEL, "packages=%d edges=%d" % (len(got), sum(len(t[5]) for t in got))


def run_rea(path):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    argv = REA + ["inspect-rust-binary", path, "--format", "json", "--full-output"]
    p = subprocess.run(argv, capture_output=True, timeout=300, cwd="/tmp")
    end = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    return argv, p.returncode, p.stdout, p.stderr, start, end


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)


def show(root, rev, rel):
    p = git(root, "show", rev + ":" + rel)
    return p.stdout if p.returncode == 0 else None


def entry_ok(root, rev):
    text = show(root, rev, ENTRY)
    if text is None:
        return False, "entry absent at rev"
    src = [l for l in text.splitlines() if l.startswith("source:")]
    if not src or CLAIM_ROW not in src[0]:
        return False, "entry source line lacks %s" % CLAIM_ROW
    sources = show(root, rev, "corpus/SOURCES.md") or ""
    if not re.search(r"^\| %s \|" % CLAIM_ROW, sources, re.M):
        return False, "%s not in SOURCES.md" % CLAIM_ROW
    base = show(root, BASE, "corpus/SOURCES.md") or ""
    if re.search(r"^\| %s \|" % CLAIM_ROW, base, re.M):
        return False, "%s already present at base" % CLAIM_ROW
    return True, "ok"


def province_ok(root, rev):
    text = show(root, rev, "PROVINCE.md") or ""
    base = show(root, BASE, "PROVINCE.md") or ""
    lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l]
    if not lines:
        return False, "no PROVINCE line names inspect-rust-binary with the entry"
    if any(l in base.splitlines() for l in lines):
        return False, "PROVINCE line already at base"
    return True, "ok"


def freeze_time(root, rev):
    """Committer time of the first commit that adds the round-30 claims file."""
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", ".ufo/waves/round-30/claims.json")
    times = [int(x) for x in p.stdout.split()]
    return min(times) if times else None


def added_time(root, rel, rev):
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", rel)
    times = [int(x) for x in p.stdout.split()]
    return min(times) if times else None


def committed_check(committed, live, tuples, entry_text, env_added, freeze_ct):
    """Second half of P1: the committed record agrees with the live run."""
    if freeze_ct is None:
        return False, "no freeze commit"
    if env_added is None or env_added <= freeze_ct:
        return False, "committed envelope absent or not added after the freeze"
    if not isinstance(committed, dict) or committed.get("ok") is not True:
        return False, "committed envelope not ok"
    cid = (committed.get("data") or {}).get("evidence_id")
    lid = ((live or {}).get("data") or {}).get("evidence_id")
    if not cid or cid != lid:
        return False, "committed evidence_id %r != live %r" % (cid, lid)
    metas = find_metadata(committed.get("data"))
    if len(metas) != 1 or not isinstance(metas[0], dict):
        return False, "committed metadata missing"
    try:
        if rea_tuples(metas[0]) != tuples:
            return False, "committed package multiset differs"
    except (KeyError, IndexError, TypeError):
        return False, "committed metadata shape"
    if cid not in entry_text:
        return False, "entry does not name %s" % cid
    return True, "ok"


def measure(root, write_evidence, env_dir, rev):
    oracle = load_oracle()
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
    for r in rows:
        if not os.path.exists(r["path"]) or sha256_file(r["path"]) != r["sha256"]:
            print("PIN carrier %s absent or altered at %s" % (r["id"], r["path"]))
            return 2
    pkg_sha = sha256_file(PKG_JSON)
    pkg_ver = json.load(open(PKG_JSON))["version"]
    if pkg_ver != "6.5.0":
        print("PIN package version %s" % pkg_ver)
        return 2
    runs = []
    passed = 0
    freeze_ct = freeze_time(root, rev)
    entry_text = show(root, rev, ENTRY) or ""
    for r in rows:
        sec, doc = oracle.read_file(r["path"])
        tuples = oracle.normalize(doc)
        argv, code, out, err, start, end = run_rea(r["path"])
        try:
            env = json.loads(out)
        except ValueError:
            env = None
        verdict, reason = judge(env, r["sha256"], sec, tuples, code)
        if verdict == PASS_LABEL and not write_evidence:
            rel = os.path.relpath(os.path.join(env_dir, r["id"] + ".json"), root)
            try:
                committed = json.loads(git(root, "show", rev + ":" + rel).stdout or "null")
            except ValueError:
                committed = None
            ok, why = committed_check(committed, env, tuples, entry_text, added_time(root, rel, rev), freeze_ct)
            if not ok:
                verdict, reason = "P1-fail", why
        passed += verdict == PASS_LABEL
        print("%s\t%s\t%s" % (r["id"], verdict, reason))
        runs.append((r["id"], start, end, code, " ".join(argv), pkg_ver, pkg_sha, verdict, reason))
        if write_evidence:
            os.makedirs(env_dir, exist_ok=True)
            open(os.path.join(env_dir, r["id"] + ".json"), "wb").write(out)
            open(os.path.join(env_dir, r["id"] + ".stderr"), "wb").write(err)
    if write_evidence:
        with open(os.path.join(os.path.dirname(env_dir), "runs.tsv"), "w") as f:
            f.write("id\tutc_start\tutc_end\texit\targv\tpkg_version\tpkg_json_sha256\tverdict\treason\n")
            for row in runs:
                f.write("\t".join(str(x) for x in row) + "\n")
    e_ok, e_why = entry_ok(root, rev)
    p_ok, p_why = province_ok(root, rev)
    print("carriers=%d pass=%d target=%d entry_ok=%d (%s) province_ok=%d (%s)" % (
        len(rows), passed, TARGET, e_ok, e_why, p_ok, p_why))
    return 0 if passed == TARGET and e_ok and p_ok else 1


def selftest():
    sec = {"offset": 100, "size": 50}
    pk = [{"name": "a", "version": "1", "source": "local", "dependencies": [1], "root": True},
          {"name": "b", "version": "2", "source": "crates.io", "kind": "build"}]
    oracle_t = sorted([("a", "1", "local", None, True, (("b", "2"),)),
                       ("b", "2", "crates.io", "build", False, ())], key=repr)
    def env(**kw):
        meta = {"packages": kw.get("packages", pk), "file_offset": kw.get("off", 100),
                "compressed_bytes": kw.get("size", 50)}
        return {"ok": kw.get("ok", True), "data": {"operation": kw.get("op", "inspect_rust_binary"),
                "subject": {"digest": {"sha256": kw.get("sha", "s")}},
                "normalized_result": {"auditable_metadata": kw.get("meta", meta)}}}
    reordered = [dict(pk[1]), dict(pk[0])]
    reordered[1]["dependencies"] = [0]
    cases = [
        ("green-exact", env(), 0, oracle_t, PASS_LABEL),
        ("green-reordered-indices", env(packages=reordered), 0, oracle_t, PASS_LABEL),
        ("red-do-nothing", None, 0, oracle_t, "P1-fail"),
        ("red-nonzero-exit", env(), 1, oracle_t, "P1-fail"),
        ("red-not-ok", env(ok=False), 0, oracle_t, "P1-fail"),
        ("red-other-operation", env(op="inspect_go_binary"), 0, oracle_t, "P1-fail"),
        ("red-subject-mismatch", env(sha="x"), 0, oracle_t, "P1-fail"),
        ("red-null-metadata", env(meta=None), 0, oracle_t, "P1-fail"),
        ("red-empty-packages", env(packages=[]), 0, oracle_t, "P1-fail"),
        ("red-empty-oracle", env(packages=[]), 0, [], "P1-fail"),
        ("red-version-differs", env(packages=[dict(pk[0]), dict(pk[1], version="3")]), 0, oracle_t, "P1-fail"),
        ("red-edge-dropped", env(packages=[dict(pk[0], dependencies=[]), dict(pk[1])]), 0, oracle_t, "P1-fail"),
        ("red-kind-dropped", env(packages=[dict(pk[0]), {k: v for k, v in pk[1].items() if k != "kind"}]), 0, oracle_t, "P1-fail"),
        ("red-root-dropped", env(packages=[{k: v for k, v in pk[0].items() if k != "root"}, dict(pk[1])]), 0, oracle_t, "P1-fail"),
        ("red-duplicate-package", env(packages=[dict(pk[0]), dict(pk[1]), dict(pk[1])]), 0, oracle_t, "P1-fail"),
        ("red-offset-differs", env(off=101), 0, oracle_t, "P1-fail"),
        ("red-size-differs", env(size=49), 0, oracle_t, "P1-fail"),
    ]
    fails = 0
    for name, e, code, ot, want in cases:
        got, why = judge(e, "s", sec, ot, code)
        ok = got == want
        fails += not ok
        print("%s %s got=%s (%s)" % ("ok" if ok else "FAIL", name, got, why))
    live = env()
    live["data"]["evidence_id"] = "ev_1"
    other = env()
    other["data"]["evidence_id"] = "ev_2"
    ccases = [
        ("green-committed-agrees", live, live, "entry ev_1", 200, 100, True),
        ("red-committed-absent", None, live, "entry ev_1", None, 100, False),
        ("red-committed-before-freeze", live, live, "entry ev_1", 90, 100, False),
        ("red-committed-same-commit-as-freeze", live, live, "entry ev_1", 100, 100, False),
        ("red-no-freeze-commit", live, live, "entry ev_1", 200, None, False),
        ("red-committed-id-differs", other, live, "entry ev_1 ev_2", 200, 100, False),
        ("red-committed-packages-differ", env(packages=[dict(pk[0])]), live, "entry ev_1", 200, 100, False),
        ("red-entry-lacks-id", live, live, "entry without ids", 200, 100, False),
    ]
    ccases[6][0]  # keep tuple layout explicit
    ccases[6][1]["data"]["evidence_id"] = "ev_1"
    for name, committed, lv, text, added, frz, want in ccases:
        got, why = committed_check(committed, lv, oracle_t, text, added, frz)
        ok = got == want
        fails += not ok
        print("%s %s got=%s (%s)" % ("ok" if ok else "FAIL", name, got, why))
    print("selftest cases=%d failures=%d" % (len(cases) + len(ccases), fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev", default="main")
    ap.add_argument("--write-evidence", action="store_true")
    ap.add_argument("--envelopes-dir")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.root:
        ap.error("--root required")
    env_dir = a.envelopes_dir or os.path.join(a.root, "corpus/evidence/round-30/c1/envelopes")
    sys.exit(measure(a.root, a.write_evidence, env_dir, a.rev))


if __name__ == "__main__":
    main()
