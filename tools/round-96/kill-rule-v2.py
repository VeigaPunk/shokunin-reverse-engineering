#!/usr/bin/env python3
"""kill-rule-v2.py - round-96 frozen counting command for R96-C1 (calibration).

Round 95 froze a kill rule whose checks never called the counter's `main()` and never ran
the probe, so five of the ten round-95 mutants survived it (M95-h: the fsync removal M2,
the forced self-verify M3, the removed fail-closed exit M4, the removed revision binding
M6, and the probe's hard-coded verdict M10). kill-rule-v2 is the successor rule: it adds
the four named checks MutationC1 specified plus the no-json-out refusal, and scores the
ten round-96 mutants (the round-95 survivor set adapted to the v6 counter and the v2 probe)
over scratch copies - the lane tree is never mutated.

Check set (each must pass on the honest instrument, and at least one must fail on a killed
mutant):

  K-selftest   the counter's / agreement's `--selftest` exits 0 (v6 carries the
               wrong-revision case; v2 carries the pins/label cases).
  K-forgeries  `verify_receipt` of the counter refuses the six round-96 unbound-field
               forgeries with exactly their intended single reason, and refuses the four
               round-95 forgeries (regression, refusal-only there).
  K-agreement  the round-95 agreement instrument refuses its four forgeries with exactly
               their intended reasons and accepts the honest triple (exact, subprocess).
  K-dmain      the counter's `main()` with a faked verdict: the honest scenario exits 0;
               the short-rev, rewritten-label and not-recomputed scenarios exit non-zero
               (fail-closed, kills M3/M4/M6); a run without `--json-out` exits 2
               (self-verification is mandatory, kills the green-without-receipt gap).
  K-fsync      an instrumented count of `os.fsync` during `write_receipt` is at least 1
               (kills M2).
  K-probe      the probe's receipt is self-consistent - `verdict == "hardened"` if and
               only if `victim_intact and receipt_valid`, and `met` states the same
               (kills M10).

Legs:

  honest arm   every check above passes on the unmutated instrument set (no false kill);
               the round-95 frozen forgery battery re-run exits 0 (regression).
  mutant arm   each of the ten mutants is applied to a scratch copy of its file; killed
               when any applicable check fails.
  identity     a no-op "mutant" (M0) must NOT be killed (blanket-refusal guard).

Frozen label:
  `mutants killed 10 of 10; forgeries refused 10 of 10; negctl refused 3 of 3; probe consistent 1 of 1; honest accepted 1 of 1`
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys

TOOL = "tools/round-96/kill-rule-v2.py"
DEFAULT_COUNTER = "tools/round-96/stop-boundary-repair-battery-v6.py"
DEFAULT_V3 = "tools/round-93/stop-boundary-repair-battery-v3.py"
DEFAULT_AGREEMENT = "tools/round-95/c1-agreement-v2.py"
DEFAULT_PROBE = "tools/round-96/symlink-probe-v2.py"
DEFAULT_WRITER = "tools/round-94/stop-boundary-repair-battery-v4.py"
DEFAULT_NOOP = ".ufo/waves/round-93/controls/identity_noop.py"
DEFAULT_R95_BATTERY = "tools/round-95/c1-forgery-refusal.py"
FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
R95_REASONS = {"pos": "label-not-frozen", "F1": "label-not-recomputed",
               "F2": "revision-not-bound", "F3": "pins-not-bound"}
R95_WORLD_REV = "b5331db1fb0ce0bf93695ce1730cf831effef6a9"
R95_INSTRUMENT_REV = "4bda1d1dd3788973f10e61212b70df18b3b14ea0"
TOTAL_MUTANTS = 10
TOTAL_FORGERIES = 10


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(cmd: list, timeout: int = 600):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def write_receipt(path: str, receipt: dict) -> None:
    """Complete JSON or absent, immune to a planted symlink at `<path>.tmp`."""
    import tempfile
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(dir=d, prefix=os.path.basename(path) + ".",
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_head(root: str):
    rc, out, _ = run(["git", "-C", root, "rev-parse", "HEAD"], 30)
    full = out.strip() if rc == 0 else ""
    return full if re.fullmatch(r"[0-9a-f]{40}", full) else None


# ---------------------------------------------------------------- check set

def c_selftest(path: str, work: str) -> dict:
    d = os.path.join(work, "selftest-run")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    rc, out, err = run([sys.executable, "-I", "-B", path, "--selftest", d], 300)
    ok = rc == 0
    tail = (out or err).strip().splitlines()[-1:] if (out or err).strip() else []
    return {"ok": ok, "exit": rc, "tail": tail[0] if tail else ""}


def counter_pins(root: str, mod, repair_rel: str) -> dict:
    return {"counter": sha256_file(os.path.join(root, mod.TOOL)),
            "verdict": sha256_file(os.path.join(root, mod.V3_TOOL)),
            "repair": sha256_file(os.path.join(root, repair_rel))}


def c_verify_forgeries(mod, root: str, expect: str, repair_rel: str,
                       fixture_dirs: list) -> dict:
    """fixture_dirs: list of (path, prefix, exact: bool, intended: dict)."""
    pins = counter_pins(root, mod, repair_rel)
    rows = []
    for fdir, prefix, exact, intended in fixture_dirs:
        for name in sorted(intended.keys()):
            path = os.path.join(fdir, "%s-%s.json" % (prefix, name))
            try:
                with open(path, encoding="utf-8") as fh:
                    rec = json.load(fh)
                rev_full = rec.get("revision")
            except (OSError, ValueError):
                rev_full = None
            v = mod.verify_receipt(path, expect, rev_full, 6, pins)
            if exact:
                ok = (not v["ok"]) and v["reasons"] == [intended[name]]
            else:
                ok = (not v["ok"]) and len(v["reasons"]) >= 1
            rows.append({"fixture": "%s-%s" % (prefix, name), "ok": ok,
                         "reasons": v["reasons"], "exact": exact})
    refused = sum(1 for r in rows if r["ok"])
    return {"ok": refused == len(rows), "refused": refused, "total": len(rows),
            "rows": rows}


def c_agreement_exact(agreement_path: str, root: str, fixture_dir: str, prefix: str,
                      expect: str, work: str) -> dict:
    rows = []
    for name, intended in R95_REASONS.items():
        rc, out, err = run([sys.executable, "-I", "-B", agreement_path,
                            "--root", root, "--dir", fixture_dir, "--prefix", prefix,
                            "--names", name, "--expect", expect, "--rev",
                            _fixture_rev(fixture_dir, prefix, name), "--intact-total",
                            "6"], 120)
        try:
            payload = json.loads(out)
        except ValueError:
            payload = {}
        reasons = None
        for r in payload.get("rows", []):
            if r.get("run") == name:
                reasons = r.get("reasons")
        ok = rc == 1 and reasons == [intended]
        rows.append({"fixture": "%s-%s" % (prefix, name), "ok": ok, "exit": rc,
                     "reasons": reasons})
    rc, out, _ = run([sys.executable, "-I", "-B", agreement_path, "--root", root,
                      "--dir", os.path.join(root, ".ufo/waves/round-95/l1/scores"),
                      "--prefix", "honest", "--names", "pos", "--expect", expect,
                      "--rev", R95_INSTRUMENT_REV, "--intact-total", "6"], 120)
    honest_ok = rc == 0
    refused = sum(1 for r in rows if r["ok"])
    return {"ok": refused == 4 and honest_ok, "refused": refused, "total": 4,
            "honest_accepted": honest_ok, "rows": rows}


def _fixture_rev(fixture_dir: str, prefix: str, name: str) -> str:
    with open(os.path.join(fixture_dir, "%s-%s.json" % (prefix, name)),
              encoding="utf-8") as fh:
        return json.load(fh).get("revision") or "worktree"


def c_dmain(mod, root: str, head: str, expect: str, work: str) -> dict:
    base = {"repaired": 12, "scored": 12, "wrong": 0, "unsafe": 0, "intact": 6,
            "far": 12, "far_refused": 12, "fresh_roundtrip": 2, "fresh_scored": 2}
    other_counts = dict(base, far_refused=11)
    notre = dict(base, repaired=11)
    scenarios = [
        ("pos", head, expect, base, 0),
        ("shortrev", head[:9], expect, base, 1),
        ("rewrite", head, ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                           "far-refused 11 of 12; fresh-roundtrip 2 of 2"),
         other_counts, 1),
        ("notrecomp", head, expect, notre, 1),
    ]
    results = {}
    orig = mod.v3.score
    try:
        for name, rev, label, counts, want in scenarios:
            def fake(args, _l=label, _c=counts):
                return 0, {"class": "killrule", "label": _l, "met_target": True,
                           "exit": 0, "counts": _c, "revision": args.rev,
                           "fresh_cells": []}
            mod.v3.score = fake
            out = os.path.join(work, "dmain-%s.json" % name)
            shutil.rmtree(os.path.join(work, "w-" + name), ignore_errors=True)
            bo, be = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
                code = mod.main(["--root", root, "--work",
                                 os.path.join(work, "w-" + name), "--rev", rev,
                                 "--expect", expect, "--json-out", out])
            ok = code == 0 if want == 0 else code != 0
            results[name] = {"exit": code, "ok": ok}
        mod.v3.score = (lambda args: (
            0, {"class": "killrule", "label": expect, "met_target": True, "exit": 0,
                "counts": base, "revision": args.rev, "fresh_cells": []}))
        bo, be = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(bo), contextlib.redirect_stderr(be):
            code = mod.main(["--root", root, "--work",
                             os.path.join(work, "w-nojson"), "--rev", head,
                             "--expect", expect])
        results["nojson"] = {"exit": code, "ok": code == 2}
    finally:
        mod.v3.score = orig
    return results


def c_fsync(mod, work: str) -> dict:
    count = {"n": 0}
    orig = os.fsync

    def counting(fd, _o=orig, _c=count):
        _c["n"] += 1
        return _o(fd)

    os.fsync = counting
    try:
        mod.write_receipt(os.path.join(work, "fsync-receipt.json"), {"x": 1})
    finally:
        os.fsync = orig
    return {"ok": count["n"] >= 1, "fsync_calls": count["n"]}


def c_probe(root: str, probe_path: str, writer: str, noop: str, expect: str,
            head: str, work: str) -> dict:
    run_dir = os.path.join(work, "probe-run")
    shutil.rmtree(run_dir, ignore_errors=True)
    os.makedirs(run_dir, exist_ok=True)
    out = os.path.join(work, "probe-receipt.json")
    if os.path.lexists(out):
        os.remove(out)
    cmd = [sys.executable, "-I", "-B", probe_path, "--root", root,
           "--writer", writer, "--repair-cmd", noop, "--work", run_dir,
           "--rev", head, "--expect", expect, "--json-out", out]
    rc, so, se = run(cmd, 1800)
    rec = None
    try:
        with open(out, encoding="utf-8") as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    if not isinstance(rec, dict):
        return {"ok": False, "error": "probe receipt unreadable", "probe_rc": rc,
                "stderr_tail": se[-300:]}
    truth = bool(rec.get("victim_intact")) and bool(rec.get("receipt_valid"))
    verdict = rec.get("verdict")
    consistent = ((verdict == "hardened") == truth) and (rec.get("met") is truth)
    return {"ok": bool(consistent), "probe_rc": rc, "verdict": verdict,
            "met": rec.get("met"), "victim_intact": rec.get("victim_intact"),
            "receipt_valid": rec.get("receipt_valid")}


# ---------------------------------------------------------------- mutant arm

def build_copy(name: str, m: dict, root: str, work: str, deps: list) -> str:
    d = os.path.join(work, "mut-%s" % name)
    shutil.rmtree(d, ignore_errors=True)
    rel = m["file"]
    dst = os.path.join(d, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(os.path.join(root, rel), dst)
    with open(dst, encoding="utf-8") as fh:
        data = fh.read()
    n = data.count(m["find"])
    if n != 1:
        raise ValueError("mutant %s: find string occurs %d times in %s"
                         % (name, n, rel))
    data = data.replace(m["find"], m["replace"], 1)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(data)
    for dep in deps:
        dd = os.path.join(d, dep)
        os.makedirs(os.path.dirname(dd), exist_ok=True)
        shutil.copyfile(os.path.join(root, dep), dd)
    return d


def run_mutant(name: str, m: dict, root: str, expect: str, head: str, work: str,
               fixture_dirs: list, r95_fixture_dir: str, writer: str, noop: str,
               counter: str) -> dict:
    kind = m["kind"]
    checks = {}
    if kind in ("counter", "identity"):
        d = build_copy(name, m, root, work, [DEFAULT_V3])
        path = os.path.join(d, m["file"])
        checks["K-selftest"] = c_selftest(path, os.path.join(work, name, "st"))
        mod = load_module(path, "kr_%s" % name)
        checks["K-dmain"] = c_dmain(mod, root, head, expect,
                                    os.path.join(work, name, "dmain"))
        checks["K-fsync"] = c_fsync(mod, os.path.join(work, name, "fsync"))
        checks["K-forgeries"] = c_verify_forgeries(mod, root, expect, noop,
                                                   fixture_dirs)
    elif kind == "agreement":
        d = build_copy(name, m, root, work, [])
        path = os.path.join(d, m["file"])
        checks["K-selftest"] = c_selftest(path, os.path.join(work, name, "st"))
        checks["K-agreement"] = c_agreement_exact(path, root, r95_fixture_dir,
                                                  "forge", expect,
                                                  os.path.join(work, name, "agr"))
    elif kind == "probe":
        d = build_copy(name, m, root, work, [])
        path = os.path.join(d, m["file"])
        checks["K-probe"] = c_probe(root, path, writer, noop, expect, head,
                                    os.path.join(work, name, "probe"))
    else:
        raise ValueError("unknown mutant kind %r" % kind)
    killed = any(not c["ok"] for c in checks.values())
    return {"name": name, "kind": kind, "killed": killed, "checks": checks}


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--work")
    ap.add_argument("--mutants")
    ap.add_argument("--fixtures", help="round-96 forgery dir")
    ap.add_argument("--prefix", default="forge")
    ap.add_argument("--r95-fixtures", default=".ufo/waves/round-95/forgery")
    ap.add_argument("--r95-prefix", default="forge")
    ap.add_argument("--counter", default=DEFAULT_COUNTER)
    ap.add_argument("--agreement", default=DEFAULT_AGREEMENT)
    ap.add_argument("--probe", default=DEFAULT_PROBE)
    ap.add_argument("--writer", default=DEFAULT_WRITER)
    ap.add_argument("--noop", default=DEFAULT_NOOP)
    ap.add_argument("--expect", default=FROZEN_LABEL)
    ap.add_argument("--decl")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args)
    missing = [a for a, v in (("--work", args.work), ("--mutants", args.mutants),
                              ("--fixtures", args.fixtures)) if v is None]
    if missing:
        print("usage: missing %s" % ", ".join(missing), file=sys.stderr)
        return 2
    root = os.path.abspath(args.root)
    os.makedirs(os.path.abspath(args.work), exist_ok=True)
    head = resolve_head(root)
    if head is None:
        print("kill-rule: cannot resolve HEAD at %s" % root, file=sys.stderr)
        return 2
    with open(args.mutants, encoding="utf-8") as fh:
        mutants = json.load(fh)
    r95_fixture_dir = os.path.join(root, args.r95_fixtures)
    new_intended = json.loads(mutants["forgery_reasons"]) if \
        isinstance(mutants.get("forgery_reasons"), str) else \
        mutants.get("forgery_reasons")
    fixture_dirs = [(args.fixtures, args.prefix, True, new_intended),
                    (r95_fixture_dir, args.r95_prefix, False, R95_REASONS)]
    r95_fixtures_abs = r95_fixture_dir

    honest = {}
    counter_path = os.path.join(root, args.counter)
    agreement_path = os.path.join(root, args.agreement)
    probe_path = os.path.join(root, args.probe)
    honest["K-selftest-counter"] = c_selftest(counter_path,
                                              os.path.join(args.work, "honest-st-c"))
    honest["K-selftest-agreement"] = c_selftest(agreement_path,
                                                os.path.join(args.work, "honest-st-a"))
    cmod = load_module(counter_path, "kr_honest_counter")
    honest["K-forgeries"] = c_verify_forgeries(cmod, root, args.expect, args.noop,
                                               fixture_dirs)
    honest["K-agreement"] = c_agreement_exact(agreement_path, root, r95_fixtures_abs,
                                              args.r95_prefix, args.expect,
                                              os.path.join(args.work, "honest-agr"))
    honest["K-dmain"] = c_dmain(cmod, root, head, args.expect,
                                os.path.join(args.work, "honest-dmain"))
    honest["K-fsync"] = c_fsync(cmod, os.path.join(args.work, "honest-fsync"))
    honest["K-probe"] = c_probe(root, probe_path, args.writer, args.noop,
                                args.expect, head, os.path.join(args.work, "honest-probe"))
    rc95, o95, _ = run([sys.executable, "-I", "-B",
                        os.path.join(root, DEFAULT_R95_BATTERY),
                        "--root", root, "--fixtures", args.r95_fixtures,
                        "--old-prefix", args.r95_prefix,
                        "--old-counter", "tools/round-94/c1-receipt-agreement.py",
                        "--honest-dir", ".ufo/waves/round-95/l1/scores",
                        "--honest-prefix", "honest", "--world-rev", R95_WORLD_REV,
                        "--instrument-rev", R95_INSTRUMENT_REV,
                        "--expect", args.expect,
                        "--json-out", os.path.join(args.work, "a4-r95-battery.json")],
                       300)
    honest["r95-battery-regression"] = {"ok": rc95 == 0, "exit": rc95}

    negctl = sum(1 for s in ("shortrev", "rewrite", "notrecomp")
                 if honest["K-dmain"].get(s, {}).get("ok"))
    forgeries = (honest["K-forgeries"]["refused"] +
                 sum(1 for r in honest["K-agreement"]["rows"] if r["ok"]))
    probe_ok = 1 if honest["K-probe"]["ok"] else 0
    honest_checks = [honest["K-selftest-counter"], honest["K-selftest-agreement"],
                     honest["K-forgeries"], honest["K-agreement"], honest["K-dmain"],
                     honest["K-fsync"], honest["K-probe"],
                     honest["r95-battery-regression"]]
    honest_ok = 1 if all(c["ok"] for c in honest_checks) else 0

    mrows = []
    for m in mutants["mutants"]:
        mrows.append(run_mutant(m["name"], m, root, args.expect, head,
                                os.path.join(args.work, "mut"), fixture_dirs,
                                r95_fixtures_abs, args.writer, args.noop,
                                args.counter))
    real = [r for r in mrows if r["kind"] != "identity"]
    identity = [r for r in mrows if r["kind"] == "identity"]
    killed = sum(1 for r in real if r["killed"])
    identity_not_killed = all(not r["killed"] for r in identity)

    label = ("mutants killed %d of %d; forgeries refused %d of %d; negctl refused %d of 3; "
             "probe consistent %d of 1; honest accepted %d of 1"
             % (killed, TOTAL_MUTANTS, forgeries, TOTAL_FORGERIES, negctl,
                probe_ok, honest_ok))
    met = (killed == TOTAL_MUTANTS and forgeries == TOTAL_FORGERIES and negctl == 3
           and probe_ok == 1 and honest_ok == 1 and identity_not_killed)
    receipt = {
        "class": "R96-C1 kill rule v2",
        "counter": TOOL,
        "counter_sha256": sha256_file(os.path.abspath(__file__)),
        "target_counter": args.counter,
        "target_counter_sha256": sha256_file(counter_path),
        "agreement": args.agreement,
        "agreement_sha256": sha256_file(agreement_path),
        "probe": args.probe,
        "probe_sha256": sha256_file(probe_path),
        "mutants_file": args.mutants,
        "mutants_sha256": sha256_file(args.mutants),
        "decl": args.decl,
        "world_revision": head,
        "expect": args.expect,
        "honest": honest,
        "mutants": mrows,
        "identity_not_killed": identity_not_killed,
        "counts": {"mutants_killed": killed, "mutants": TOTAL_MUTANTS,
                   "forgeries_refused": forgeries, "forgeries": TOTAL_FORGERIES,
                   "negctl_refused": negctl, "negctl": 3,
                   "probe_consistent": probe_ok, "probe": 1,
                   "honest_accepted": honest_ok, "honest": 1},
        "label": label,
        "met_target": met,
        "exit": 0 if met else 1,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        write_receipt(args.json_out, receipt)
    print(rendered)
    print(label, "met", met, "exit", 0 if met else 1)
    return 0 if met else 1


def _selftest(args) -> int:
    """Hermetic: verifies the mutant application machinery and the consistency
    predicate on synthetic receipts; no lane write, no network."""
    results = []

    def case(name, ok):
        results.append(ok)
        print(f"selftest {name}: {'ok' if ok else 'FAIL'}")

    work = args.work or os.path.join(
        os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r96",
        "selftest-killrule")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    # mutant application: a one-line find/replace applies exactly once
    src = os.path.abspath(__file__)
    m = {"name": "T1", "kind": "agreement", "file": "x/probe.py",
         "find": "TARGET_LINE = 1\n", "replace": "TARGET_LINE = 2\n"}
    d = os.path.dirname(os.path.join(work, "copy", m["file"]))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(work, "copy", m["file"]), "w", encoding="utf-8") as fh:
        fh.write("TARGET_LINE = 1\n")
    fake_root = os.path.join(work, "root")
    os.makedirs(os.path.join(fake_root, "x"), exist_ok=True)
    shutil.copyfile(os.path.join(work, "copy", m["file"]),
                    os.path.join(fake_root, m["file"]))
    dep_free = build_copy("T1", m, fake_root, work, [])
    with open(os.path.join(dep_free, m["file"]), encoding="utf-8") as fh:
        case("apply-once", fh.read() == "TARGET_LINE = 2\n")

    # double occurrence is refused
    with open(os.path.join(fake_root, m["file"]), "w", encoding="utf-8") as fh:
        fh.write("TARGET_LINE = 1\nTARGET_LINE = 1\n")
    try:
        build_copy("T2", m, fake_root, work, [])
        case("double-find-refused", False)
    except ValueError:
        case("double-find-refused", True)

    # probe consistency predicate: a lying receipt is inconsistent
    lying = {"verdict": "hardened", "met": True, "victim_intact": False,
             "receipt_valid": True}
    truth = bool(lying["victim_intact"]) and bool(lying["receipt_valid"])
    consistent = ((lying["verdict"] == "hardened") == truth) and \
        (lying["met"] is truth)
    case("lying-probe-inconsistent", not consistent)

    # truthful negative probe is consistent
    honest_neg = {"verdict": "followed-symlink", "met": False,
                  "victim_intact": False, "receipt_valid": True}
    truth = bool(honest_neg["victim_intact"]) and bool(honest_neg["receipt_valid"])
    consistent = ((honest_neg["verdict"] == "hardened") == truth) and \
        (honest_neg["met"] is truth)
    case("truthful-negative-consistent", consistent)

    print(f"SELFTEST cases={len(results)} failures={sum(1 for c in results if not c)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
