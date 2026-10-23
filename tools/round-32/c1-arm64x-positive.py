#!/usr/bin/env python3
"""R32-C1 counter (coverage): REA 6.5.0 `inspect` on 12 ARM64X hybrid PE DLLs, against an
independent pure-Python PE oracle (tools/round-32/arm64x_oracle.py).

Predicate label `P1-pass` (frozen in .ufo/waves/round-32/claims.json): a carrier passes when
the oracle classifies its pinned bytes as ARM64X (COFF machine 0xAA64, a CHPE code map with
at least one ARM64 and one ARM64EC range); its live REA 6.5.0 `inspect` run exits 0 with an
ok envelope whose operation is binary_overview and whose subject sha256 equals the frozen
sha256; the envelope's format, architecture, document, image_base, segments (name, start,
end, length, image_base, address_space, in order), segment_count and procedure_count equal
the oracle's expected report, and procedure_count also equals the frozen prediction in
predictions.tsv (the native-view export count); and its committed envelope, first added
after the freeze commit, equals the live envelope in every field except meta, and the
round-32 entry names that evidence_id.  Doc gates: entry_ok (the entry cites S099) and
province_ok (a PROVINCE.md table row naming ARM64X and the entry whose nearest preceding
heading names Core and not Frontier/Adjacent/exclusion).

Measure mode prints `carriers=N pass=P target=12 entry_ok=E (..) province_ok=V (..)` and
exits 0 only on target.  Write mode (--write-evidence) stores the live envelopes and never
prints that line (round-31 routed defect 6 / M31-3): it prints `WRITE-MODE ... not a receipt`
and exits 3 whatever the verdicts.
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
CLAIM_ROW = "S099"
ENTRY = "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
CARRIERS = "corpus/evidence/round-32/c1/carriers.tsv"
PREDICTIONS = "corpus/evidence/round-32/c1/predictions.tsv"
CLAIMS = ".ufo/waves/round-32/claims.json"
ENV_DIR = "corpus/evidence/round-32/c1/envelopes"
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "P1-pass"
OPERATION = "binary_overview"


def load_oracle():
    spec = importlib.util.spec_from_file_location("arm64x_oracle", os.path.join(HERE, "arm64x_oracle.py"))
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


def judge(env, code, carrier_sha, expected, predicted_procs, is_arm64x, comparable):
    if not is_arm64x:
        return "P1-fail", "oracle does not classify the carrier as ARM64X"
    if not isinstance(env, dict):
        return "P1-fail", "no JSON envelope (exit %s)" % code
    if code != 0 or env.get("ok") is not True:
        return "P1-fail", "exit %s ok %r" % (code, env.get("ok"))
    data = env.get("data") or {}
    if data.get("operation") != OPERATION:
        return "P1-fail", "operation %r" % data.get("operation")
    if ((data.get("subject") or {}).get("digest") or {}).get("sha256") != carrier_sha:
        return "P1-fail", "subject sha256 differs from the frozen carrier"
    got = comparable(data)
    if got != expected:
        diff = sorted(k for k in set(got) | set(expected) if got.get(k) != expected.get(k))
        return "P1-fail", "report differs from the oracle: %s" % ",".join(diff)
    if got.get("procedure_count") != predicted_procs:
        return "P1-fail", "procedure_count %r differs from the frozen prediction %r" % (got.get("procedure_count"), predicted_procs)
    return LABEL, "segments=%d procedure_count=%d" % (got["segment_count"], got["procedure_count"])


def clean_env():
    env = {k: v for k, v in os.environ.items() if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
    return env


def run_rea(path):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    argv = REA + ["inspect", path, "--format", "json", "--full-output"]
    p = subprocess.run(argv, capture_output=True, timeout=600, cwd="/tmp", env=clean_env())
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
    """A table row naming ARM64X and the entry whose governing heading names Core."""
    if not text:
        return False, "PROVINCE absent"
    heading = ""
    for ln in text.splitlines():
        if re.match(r"#{1,6} ", ln):
            heading = ln
            continue
        if ln.startswith("|") and "ARM64X" in ln and ENTRY in ln:
            if "Core" in heading and not re.search(r"Frontier|Adjacent|exclusion", heading):
                return True, "ok"
            return False, "row sits under %r, not a Core heading" % heading[:60]
    return False, "no PROVINCE table row names ARM64X and the entry"


def pinned_inputs(root, rev):
    out = {}
    for rel in (CARRIERS, PREDICTIONS):
        frozen = show(root, rev, rel)
        if frozen is None:
            return None, "PIN pinned input absent: %s at %s" % (rel, rev)
        disk = os.path.join(root, rel)
        if not os.path.isfile(disk) or open(disk).read() != frozen:
            return None, "PIN %s in the tree differs from %s" % (rel, rev)
        out[rel] = list(csv.DictReader(frozen.splitlines(), delimiter="\t"))
    return out, None


def measure(root, rev, write):
    pins, why = pinned_inputs(root, rev)
    if pins is None:
        print(why)
        return 2
    rows, preds = pins[CARRIERS], {r["id"]: r for r in pins[PREDICTIONS]}
    if len(rows) != TARGET or sorted(preds) != sorted(r["id"] for r in rows):
        print("PIN carrier list has %d rows (frozen %d) or predictions do not cover it" % (len(rows), TARGET))
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
        expected = oracle.expected(r["path"])
        is_x = oracle.classify(r["path"])["arm64x"]
        argv, code, out, err, start, end = run_rea(r["path"])
        try:
            env = json.loads(out)
        except ValueError:
            env = None
        verdict, reason = judge(env, code, r["sha256"], expected, int(preds[r["id"]]["procedure_count"]), is_x, oracle.comparable)
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
            f.write("id\tutc_start\tutc_end\texit\targv\tpkg_version\tpkg_json_sha256\tverdict_without_committed_clause\treason\n")
            for row in runs:
                f.write("\t".join(str(x) for x in row) + "\n")
        print("WRITE-MODE carriers=%d written=%d at %s (not a receipt; no target line)" % (
            len(rows), len(runs), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")))
        return 3
    e_ok, e_why = entry_ok(entry_text)
    p_ok, p_why = province_ok(show(root, rev, "PROVINCE.md"))
    print("carriers=%d pass=%d target=%d entry_ok=%d (%s) province_ok=%d (%s)" % (
        len(rows), passed, TARGET, e_ok, e_why, p_ok, p_why))
    return 0 if passed == TARGET and e_ok and p_ok else 1


def selftest():
    fails = 0
    exp = {"format": "pe", "architecture": "arm64", "document": "target-aaaaaaaaaaaa.dll", "image_base": "0x180000000",
           "segments": [{"name": "Headers"}], "segment_count": 1, "procedure_count": 2}
    data = {"operation": OPERATION, "subject": {"digest": {"sha256": "a"}, "format": "pe", "architecture": "arm64"},
            "normalized_result": {"document": "target-aaaaaaaaaaaa.dll", "image_base": "0x180000000",
                                  "segments": [{"name": "Headers"}], "segment_count": 1, "procedure_count": 2}}
    env = {"ok": True, "data": data}
    o = load_oracle()

    def mod(path, value):
        e = json.loads(json.dumps(env))
        cur = e
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return e
    cases = [
        ("exact", env, 0, "a", 2, True, LABEL),
        ("exit 1", env, 1, "a", 2, True, "P1-fail"),
        ("wrong sha", env, 0, "b", 2, True, "P1-fail"),
        ("not ARM64X by oracle", env, 0, "a", 2, False, "P1-fail"),
        ("procedure_count = EC export count", mod(["data", "normalized_result", "procedure_count"], 3), 0, "a", 2, True, "P1-fail"),
        ("oracle and envelope agree, frozen prediction differs", env, 0, "a", 3, True, "P1-fail"),
        ("segment differs", mod(["data", "normalized_result", "segments"], [{"name": ".text"}]), 0, "a", 2, True, "P1-fail"),
        ("architecture x86-64 (EC view)", mod(["data", "subject", "architecture"], "x86-64"), 0, "a", 2, True, "P1-fail"),
        ("wrong operation", mod(["data", "operation"], "inspect_artifact"), 0, "a", 2, True, "P1-fail"),
        ("refusal", {"ok": False, "error": {}}, 1, "a", 2, True, "P1-fail"),
        ("no envelope", None, 0, "a", 2, True, "P1-fail"),
    ]
    for name, e, code, sha, pred, isx, want in cases:
        got, why = judge(e, code, sha, exp, pred, isx, o.comparable)
        ok = got == want
        fails += not ok
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, why))
    row = "| ARM64X hybrid PE (`inspect`) | x | `%s` |" % ENTRY
    prov = [
        ("row under Core heading", "## Core\n" + row, True),
        ("row under round Core-addition heading", "## Round-32 additions to Core (verified 2026-10-23)\n" + row, True),
        ("row under Frontier", "## Frontier\n" + row, False),
        ("row under Adjacent exclusion", "## Adjacent — Core exclusion\n" + row, False),
        ("prose, not a table row", "## Core\nARM64X %s" % ENTRY, False),
        ("ARM64X without entry", "## Core\n| ARM64X |", False),
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
    if a.selftest:
        sys.exit(selftest())
    sys.exit(measure(os.path.abspath(a.root), a.rev, a.write_evidence))


if __name__ == "__main__":
    main()
