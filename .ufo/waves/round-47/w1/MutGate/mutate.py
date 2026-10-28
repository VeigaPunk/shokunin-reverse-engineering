#!/usr/bin/env python3
"""MutGate — gate.py mutation probe for round 47, C1 clause 7.

Detectors (identical bounds on pristine / mutant / restored bytes):
  D1 structural  frozen tools/round-47/exact.py --profile v3 --no-battery,
                 --freeze <pinned clone HEAD> --rev <mutant commit>.
                 Clause 7 is the `failing` entry beginning "gate.py flag order".
  D2 behavioural gate.history_touched over a fixture whose only touch of
                 plans/merge-only.md is the merge commit's first-parent diff;
                 the fixture also carries a touched non-ASCII path (decode arm)
                 and a commit whose subject is exactly `M3` (format arm).
  D3 forgery     one commit inside freeze..tip rewrites a frozen path and a later
                 commit restores its bytes: net blob identical, so ONLY
                 history_touched can see the in-range tamper.
"""
import argparse
import hashlib
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
import time

GATE = "tools/round-46/gate.py"
EXACT = "tools/round-47/exact.py"
CLAIMS = "plans/round-47-claims.md"

MUTATIONS = [
    ("M01-flag-order", '"-m", "--diff-merges=first-parent", "--name-status", "-z",',
     '"--diff-merges=first-parent", "-m", "--name-status", "-z",'),
    ("M02-format-empty", '"--format=", f"{base}..{tip}"', '"--format=%s", f"{base}..{tip}"'),
    ("M03-drop-z", '"--name-status", "-z",', '"--name-status",'),
    ("M04-name-only", '"--name-status", "-z",', '"--name-only", "-z",'),
    ("M05-drop-m", '"-m", "--diff-merges=first-parent",', '"--diff-merges=first-parent",'),
    ("M06-drop-separator", 'f"{base}..{tip}", "--", *paths, binary=True',
     'f"{base}..{tip}", *paths, binary=True'),
    ("M07-pathspec-join", "*paths, binary=True", "*paths[:1], binary=True"),
    ("M08-status-regex", 'r"^[ACDMRTUXB][0-9]*$"', 'r"^[AD][0-9]*$"'),
    ("M09-decode", '"git log failed"\n    tokens = r.stdout.decode("utf-8", "surrogateescape")',
     '"git log failed"\n    tokens = r.stdout.decode("latin-1")'),
    ("M10-return", "return sorted(touched), None", "return [], None"),
    # clause-7 evasions: the graded literal survives verbatim, the behaviour does not
    ("M11-no-merges-appended",
     '"-m", "--diff-merges=first-parent", "--name-status"',
     '"-m", "--diff-merges=first-parent", "--no-merges", "--name-status"'),
    ("M12-rev-range-reversed", 'f"{base}..{tip}"', 'f"{tip}..{base}"'),
    ("M13-status-regex-dollar", 'r"^[ACDMRTUXB][0-9]*$"', 'r"^[ACDMRTUXB][0-9]*"'),
]

PATHS = ["plans/", "tools/", "corpus/"]
EXPECTED = ["corpus/na\u00efve.md", "corpus/plain.md", "plans/merge-only.md",
            "plans/x.md", "tools/y.md"]
FORGERY_PATHS = ["plans/round-47-claims.md", "tools/round-47/"]


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sha(b):
    return hashlib.sha256(b.encode() if isinstance(b, str) else b).hexdigest()


def g(root, *a, check=True):
    r = sh(["git", "-C", root, *a])
    if check:
        assert r.returncode == 0, (a, r.stderr)
    return r.stdout.strip()


def init_repo(root):
    os.makedirs(root, exist_ok=True)
    g(root, "init", "-q")
    g(root, "config", "user.email", "fx@round47")
    g(root, "config", "user.name", "round47 fixture")
    top = g(root, "rev-parse", "--show-toplevel")
    assert os.path.realpath(top) == os.path.realpath(root), (top, root)


def write(root, rel, text):
    full = os.path.join(root, rel)
    os.makedirs(os.path.dirname(full) or root, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def commit(root, msg, tracked_only=False):
    if not tracked_only:
        g(root, "add", "-A")
    args = ["commit", "-q"] + (["-a"] if tracked_only else []) + ["-m", msg]
    g(root, *args)
    return g(root, "rev-parse", "HEAD")


def build_history_fixture(root):
    init_repo(root)
    write(root, "plans/x.md", "A\n")
    write(root, "tools/y.md", "T\n")
    write(root, "corpus/plain.md", "P\n")
    write(root, "corpus/na\u00efve.md", "N\n")
    base = commit(root, "c1 base")
    g(root, "checkout", "-q", "-b", "side")
    write(root, "corpus/plain.md", "S\n")
    write(root, "corpus/na\u00efve.md", "N2\n")
    commit(root, "side edit")
    main = "master" if "master" in g(root, "branch", "--list") else "main"
    g(root, "checkout", "-q", main)
    write(root, "tools/y.md", "T2\n")
    commit(root, "M3")
    g(root, "merge", "--no-ff", "--no-commit", "side")
    write(root, "plans/merge-only.md", "merge resolution\n")
    write(root, "plans/x.md", "AB\n")
    tip = commit(root, "merge side")
    return base, tip


def build_dup_fixture(root):
    """Conflicting merge: calibrates R46-CL6's `-m` / order claim on raw bytes."""
    init_repo(root)
    write(root, "plans/x.md", "A\n")
    write(root, "tools/y.md", "T\n")
    base = commit(root, "c1 base")
    g(root, "checkout", "-q", "-b", "side")
    write(root, "plans/x.md", "B\n")
    commit(root, "side edit")
    main = "master" if "master" in g(root, "branch", "--list") else "main"
    g(root, "checkout", "-q", main)
    write(root, "plans/x.md", "M\n")
    commit(root, "main edit")
    r = sh(["git", "-C", root, "merge", "--no-ff", "-m", "merge side", "side"])
    assert r.returncode != 0, "merge should conflict"
    write(root, "plans/x.md", "AB\n")
    tip = commit(root, "merge side")
    return base, tip


def build_separator_fixture(root):
    """A ref literally named like a frozen file makes `--` load-bearing."""
    init_repo(root)
    write(root, CLAIMS, "claims\n")
    write(root, "tools/round-47/exact.py", "print(1)\n")
    base = commit(root, "c1")
    write(root, CLAIMS, "claims v2\n")
    write(root, "tools/round-47/exact.py", "print(2)\n")
    tip = commit(root, "touch both frozen paths")
    g(root, "update-ref", f"refs/heads/{CLAIMS}", tip)
    return base, tip


def load_gate(path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("gate_" + sha(path)[:10], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probe(text, tmpdir, tag, fixtures):
    write(tmpdir, f"g-{tag}.py", text)
    mod = load_gate(os.path.join(tmpdir, f"g-{tag}.py"))
    out = {}
    for name, (root, base, tip, paths) in fixtures.items():
        touched, err = mod.history_touched(root, base, tip, paths)
        out[name] = {"touched": touched, "error": err}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fx", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    fx, base, out = a.fx, a.base, a.out
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(dir=a.scratch, prefix="mut-")
    pristine = open(os.path.join(fx, GATE)).read()
    psha = sha(pristine)

    hroot = os.path.join(a.scratch, "fixture-history")
    shutil.rmtree(hroot, ignore_errors=True)
    hb, ht = build_history_fixture(hroot)
    droot = os.path.join(a.scratch, "fixture-dup")
    shutil.rmtree(droot, ignore_errors=True)
    db, dt = build_dup_fixture(droot)
    sroot = os.path.join(a.scratch, "fixture-separator")
    shutil.rmtree(sroot, ignore_errors=True)
    sb, st = build_separator_fixture(sroot)
    fixtures = {"history": (hroot, hb, ht, PATHS),
                "dup": (droot, db, dt, PATHS),
                "separator": (sroot, sb, st, FORGERY_PATHS)}

    variants = {}
    for tag, extra in (("both-canonical", ["-m", "--diff-merges=first-parent"]),
                       ("both-swapped", ["--diff-merges=first-parent", "-m"]),
                       ("first-parent-only", ["--diff-merges=first-parent"]),
                       ("m-only", ["-m"]),
                       ("no-merges", ["-m", "--diff-merges=first-parent", "--no-merges"])):
        r = sh(["git", "-C", droot, "log", *extra, "--name-status", "-z", "--format=",
                f"{db}..{dt}", "--", *PATHS])
        variants[tag] = {"rc": r.returncode, "bytes": len(r.stdout.encode()),
                         "sha256": sha(r.stdout),
                         "plans_x_occurrences": r.stdout.count("plans/x.md"),
                         "tokens": r.stdout.replace("\0", "|").strip()}

    rec = {"pristine_sha256": psha, "base": base, "rev_measured": base,
           "git": sh(["git", "--version"]).stdout.strip(),
           "expected_set": EXPECTED,
           "fixtures": {"history": [hb, ht], "dup": [db, dt],
                        "separator": [sb, st]},
           "flag_variants_raw": variants,
           "pristine": probe(pristine, tmp, "pristine", fixtures),
           "mutants": []}

    def counter(rev, tag):
        jout = os.path.join(fx, ".ufo", "scratch", f"{tag}.json")
        cmd = [sys.executable, "-I", "-B", os.path.join(fx, EXACT), "--root", fx,
               "--freeze", base, "--rev", rev, "--no-battery", "--json-out", jout]
        t0 = time.time()
        r = sh(cmd)
        try:
            d = json.load(open(jout))
        except Exception:  # noqa: BLE001
            d = {}
        failing = d.get("failing") or []
        return {"command": " ".join(cmd), "exit": r.returncode,
                "stdout_sha256": sha(r.stdout), "stderr": r.stderr.strip()[:300],
                "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "seconds": round(time.time() - t0, 2),
                "met_target": d.get("met_target"), "failing": failing,
                "reason": d.get("reason"),
                "gate_order_literal": d.get("gate_order_literal"),
                "gate_order_reversed": d.get("gate_order_reversed"),
                "frozen_path_changed": d.get("frozen_path_changed"),
                "clause7_red": any("flag order" in str(x) for x in failing)}

    for name, old, new in MUTATIONS:
        n = pristine.count(old)
        m = {"name": name, "target": old, "replacement": new, "occurrences": n}
        if n != 1:
            m.update(applied=False, reason=f"target occurrences {n} != 1")
            rec["mutants"].append(m)
            continue
        body = pristine.replace(old, new, 1)
        m["mutant_sha256"] = sha(body)
        mpath = os.path.join(tmp, f"{name}.py")
        write(tmp, f"{name}.py", body)
        try:
            py_compile.compile(mpath, cfile=mpath + "c", doraise=True)
            m["syntax"] = "ok"
        except Exception as exc:  # noqa: BLE001
            m["syntax"] = f"{type(exc).__name__}: {exc}"
        m["behaviour"] = probe(body, tmp, name, fixtures)
        write(fx, GATE, body)
        commit(fx, f"mut {name}", tracked_only=True)
        rev = g(fx, "rev-parse", "HEAD")
        m["rev"] = rev
        m["counter"] = counter(rev, name)
        m["clause7_red"] = m["counter"]["clause7_red"]
        m["behaviour_killed"] = m["behaviour"] != rec["pristine"]
        m["verdict"] = ("killed-clause7" if m["clause7_red"] else
                        "killed-behaviour" if m["behaviour_killed"] else
                        "survived" if m["counter"]["exit"] == 0 else
                        f"counter-exit-{m['counter']['exit']}")
        rec["mutants"].append(m)

    # ---- D3: in-range tamper of a frozen path, restored byte for byte ----------
    claims_base = sh(["git", "-C", fx, "show", f"{base}:{CLAIMS}"]).stdout
    rec["forgery"] = {}
    for tag, start in (
            ("pristine-gate", base),
            ("m10-return", next(m["rev"] for m in rec["mutants"] if m["name"] == "M10-return")),
            ("m12-rev-reversed", next(m["rev"] for m in rec["mutants"]
                                      if m["name"] == "M12-rev-range-reversed")),
            ("m11-no-merges", next(m["rev"] for m in rec["mutants"]
                                   if m["name"] == "M11-no-merges-appended"))):
        g(fx, "checkout", "-q", "-B", f"forgery-{tag}", start)
        write(fx, CLAIMS, claims_base + "\n<!-- in-range tamper -->\n")
        commit(fx, "tamper the frozen claims file", tracked_only=True)
        write(fx, CLAIMS, claims_base)
        commit(fx, "restore the frozen claims file byte for byte", tracked_only=True)
        tip = g(fx, "rev-parse", "HEAD")
        r = counter(tip, f"forgery-{tag}")
        r["tip"] = tip
        r["net_blob_identical"] = (g(fx, "rev-parse", f"HEAD:{CLAIMS}") ==
                                   g(fx, "rev-parse", f"{base}:{CLAIMS}"))
        rec["forgery"][tag] = r

    # ---- restore exact bytes ---------------------------------------------------
    g(fx, "checkout", "-q", base)
    write(fx, GATE, pristine)
    restored_probe = probe(pristine, tmp, "restored", fixtures)
    rc = counter(base, "restored")
    rec["restore"] = {
        "restored_sha256": sha(open(os.path.join(fx, GATE)).read()),
        "equals_pristine": sha(open(os.path.join(fx, GATE)).read()) == psha,
        "git_status_gate": g(fx, "status", "--porcelain", "--", GATE),
        "behaviour_matches_pristine": restored_probe == rec["pristine"],
        "counter": rc,
    }
    with open(os.path.join(out, "receipts.json"), "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    print(json.dumps({
        "base": base,
        "verdicts": {m["name"]: [m.get("verdict"),
                                 m.get("counter", {}).get("exit"),
                                 m.get("clause7_red"),
                                 (m.get("behaviour") or {}).get("history"),
                                 (m.get("behaviour") or {}).get("separator")]
                     for m in rec["mutants"]},
        "forgery": {k: [v["exit"], v["failing"], v["reason"],
                        v["frozen_path_changed"], v["net_blob_identical"]]
                    for k, v in rec["forgery"].items()},
        "restore": {k: rec["restore"][k] for k in
                    ("restored_sha256", "equals_pristine", "git_status_gate",
                     "behaviour_matches_pristine")},
        "restored_counter_exit": rec["restore"]["counter"]["exit"],
        "flags": {k: [v["bytes"], v["plans_x_occurrences"], v["tokens"]]
                  for k, v in variants.items()},
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
