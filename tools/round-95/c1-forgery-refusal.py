#!/usr/bin/env python3
"""c1-forgery-refusal.py - round-95 frozen counting command for R95-C1 (calibration).

Scores the four committed forged receipt triples in `--fixtures` twice:

  before  the frozen round-94 instrument `--old-counter` (pinned) runs over the
          fixtures with `--old-prefix`. The do-nothing premise: the unchanged
          round-94 instrument ADMITS all four forgeries (valid 4, agree 4,
          predicted 4, met true, exit 0). If it refuses any, the claim's premise
          (a strengthened instrument is needed) is false and the battery exits 1.

  after   the strengthened instrument `c1-agreement-v2.py` scores each forgery as a
          single case against the fixture world revision `--world-rev`. Each forgery
          violates exactly one binding and must carry exactly its intended typed
          reason: pos -> label-not-frozen, F1 -> label-not-recomputed,
          F2 -> revision-not-bound, F3 -> pins-not-bound.

It then scores the honest positive triple (`--honest-dir`/`--honest-prefix`/`pos`,
produced by the real v5 public run at `--instrument-rev`) with the strengthened
instrument: every atom and binding green, met true, exit 0. A blanket-refusal
"instrument" is excluded by this positive control.

Exit 0 iff: before met true; all four forgeries refused with exactly their intended
reason; the honest triple accepted. The receipt records the fixture digests, the
instrument digests and both revisions.

    python3 -I -B tools/round-95/c1-forgery-refusal.py --root . \
      --fixtures .ufo/waves/round-95/forgery --old-prefix forge \
      --old-counter tools/round-94/c1-receipt-agreement.py \
      --honest-dir .ufo/waves/round-95/l1/scores --honest-prefix honest \
      --world-rev <base-full> --instrument-rev <decl-full> \
      --expect '<FROZEN_LABEL>' --json-out <receipt>

`--selftest <dir>` runs the same three legs over a hermetic mini world authored in
<dir> (the real old counter is generic enough to score the mini fixtures).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-95/c1-forgery-refusal.py"
V2 = os.path.join(HERE, "c1-agreement-v2.py")
FORGERY_REASONS = {"pos": "label-not-frozen", "F1": "label-not-recomputed",
                   "F2": "revision-not-bound", "F3": "pins-not-bound"}
NAMES = ("pos", "F1", "F2", "F3")
FROZEN_LABEL = ("repaired 2 of 2; wrong 0; unsafe 0; intact 1 of 1; "
                "far-refused 1 of 1; fresh-roundtrip 1 of 1")


def _sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _run(cmd: list, timeout: int = 120):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def _run_leg(root: str, fixtures: str, prefix: str, names, expect: str,
             rev: str, json_out, intact_total: int = 6) -> dict:
    cmd = [sys.executable, "-I", "-B", V2, "--root", root, "--dir", fixtures,
           "--prefix", prefix, "--names", ",".join(names), "--expect", expect,
           "--rev", rev, "--intact-total", str(intact_total)]
    if json_out:
        cmd += ["--json-out", json_out]
    rc, out, err = _run(cmd)
    try:
        payload = json.loads(out)
    except ValueError:
        payload = {"parse_error": out[-400:], "stderr": err[-400:]}
    return {"exit": rc, "payload": payload}


def _mini_world(dirpath: str, rev: str, verdict_sha: str, counter_sha: str) -> str:
    """Author the hermetic mini fixture world; returns the mini frozen label."""
    os.makedirs(dirpath, exist_ok=True)
    counts = {"repaired": 2, "scored": 2, "wrong": 0, "unsafe": 0, "intact": 1,
              "far": 1, "far_refused": 1, "fresh_roundtrip": 1, "fresh_scored": 1,
              "refused": 0, "silent": 0}
    label = FROZEN_LABEL
    common = {"class": "mini",
              "counts": counts, "revision": rev,
              "tool": "tools/round-93/stop-boundary-repair-battery-v3.py",
              "verdict_sha256": verdict_sha,
              "counter_sha256": counter_sha}
    # pos: consistent label rewrite, met true
    other = ("repaired 2 of 2; wrong 0; unsafe 0; intact 1 of 1; "
             "far-refused 0 of 1; fresh-roundtrip 1 of 1")
    c_other = dict(counts, far_refused=0)
    _mini_triple(dirpath, "mini-pos", {**common, "label": other,
                                       "public_label": other, "met_target": True,
                                       "exit": 0, "counts": c_other}, other, True, 0)
    # F1: label not recomputed (label says fresh-roundtrip 1 of 1, counts say 0)
    _mini_triple(dirpath, "mini-F1", {**common, "label": label,
                                      "public_label": label,
                                      "met_target": False, "exit": 1,
                                      "counts": dict(counts, fresh_roundtrip=0)},
                 label, False, 1)
    # F2: short revision
    _mini_triple(dirpath, "mini-F2", {**common, "label": label,
                                      "public_label": label, "met_target": False,
                                      "exit": 1, "revision": rev[:9]},
                 label, False, 1)
    # F3: fabricated pins
    _mini_triple(dirpath, "mini-F3", {**common, "label": label,
                                      "public_label": label, "met_target": False,
                                      "exit": 1, "verdict_sha256": "0" * 64,
                                      "counter_sha256": "f" * 64},
                 label, False, 1)
    # honest: green world bound to the real pins
    _mini_triple(dirpath, "honest-pos", {**common, "label": label,
                                         "public_label": label,
                                         "met_target": True, "exit": 0},
                 label, True, 0)
    return label


def _mini_triple(dirpath: str, stem: str, rec: dict, label: str, met: bool,
                 exit_code: int) -> None:
    base = os.path.join(dirpath, stem)
    with open(base + ".json", "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    with open(base + ".stdout", "w", encoding="utf-8") as fh:
        fh.write("%s met %s exit %d\n" % (label, met, exit_code))
    with open(base + ".rc", "w", encoding="utf-8") as fh:
        fh.write("%d\n" % exit_code)


def _selftest(work: str) -> int:
    """Hermetic mini world authored in the scratch dir. The live repo revision and
    the real pinned byte digests (v3 verdict, v2 instrument) are resolved with
    read-only `git` calls so the strengthened instrument's main-mode bindings can
    resolve; no live-tree write and no network."""
    mini = os.path.join(work, "mini")
    rc, rev, _ = _run(["git", "rev-parse", "HEAD"])
    if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}", rev.strip()):
        print("selftest precondition: cannot resolve HEAD", file=sys.stderr)
        return 1
    rev = rev.strip()

    def _pin(relpath: str) -> str:
        p = subprocess.run(["git", "show", "%s:%s" % (rev, relpath)],
                           capture_output=True, timeout=30)
        if p.returncode != 0:
            print("selftest precondition: git show %s failed" % relpath, file=sys.stderr)
            raise SystemExit(1)
        return hashlib.sha256(p.stdout).hexdigest()

    verdict_sha = _pin("tools/round-93/stop-boundary-repair-battery-v3.py")
    counter_sha = _pin("tools/round-93/stop-boundary-repair-battery-v3.py")
    label = _mini_world(mini, rev, verdict_sha, counter_sha)
    results = []

    def case(name: str, cond: bool) -> None:
        results.append(cond)
        print(f"selftest {name}: {'ok' if cond else 'FAIL'}")

    old_counter = os.path.abspath(os.path.join(
        HERE, "..", "round-94", "c1-receipt-agreement.py"))
    rc, out, _ = _run([sys.executable, "-I", "-B", old_counter,
                       "--dir", mini, "--prefix", "mini"])
    before = json.loads(out) if rc in (0, 1) else {}
    case("mini-before-admits", rc == 0 and before.get("met") is True)
    after = _run_leg(os.getcwd(), mini, "mini", NAMES, label, rev, None,
                     intact_total=1)
    reasons = {r["run"]: r["reasons"] for r in after["payload"].get("rows", [])}
    case("mini-forgeries-refused",
         after["exit"] == 1
         and reasons.get("pos") == ["label-not-frozen"]
         and reasons.get("F1") == ["label-not-recomputed"]
         and reasons.get("F2") == ["revision-not-bound"]
         and reasons.get("F3") == ["pins-not-bound"])
    honest = _run_leg(os.getcwd(), mini, "honest", ("pos",), label, rev, None,
                      intact_total=1)
    case("mini-honest-accepted", honest["exit"] == 0
         and honest["payload"].get("met") is True)
    print(f"SELFTEST cases=3 failures={sum(1 for c in results if not c)}")
    return 0 if all(results) else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--fixtures")
    ap.add_argument("--old-prefix")
    ap.add_argument("--old-counter", default="tools/round-94/c1-receipt-agreement.py")
    ap.add_argument("--honest-dir")
    ap.add_argument("--honest-prefix")
    ap.add_argument("--world-rev")
    ap.add_argument("--instrument-rev")
    ap.add_argument("--expect")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest")
    args = ap.parse_args(argv)
    if args.selftest:
        return _selftest(args.selftest)
    missing = [a for a, v in (("--fixtures", args.fixtures),
                              ("--old-prefix", args.old_prefix),
                              ("--honest-dir", args.honest_dir),
                              ("--honest-prefix", args.honest_prefix),
                              ("--world-rev", args.world_rev),
                              ("--instrument-rev", args.instrument_rev),
                              ("--expect", args.expect)) if v is None]
    if missing:
        print("usage: missing %s" % ", ".join(missing), file=sys.stderr)
        return 2
    root = os.path.abspath(args.root)

    # before: the frozen round-94 instrument over the forged fixtures
    old_path = os.path.join(root, args.old_counter)
    rc_before, out_before, _ = _run([sys.executable, "-I", "-B", old_path,
                                     "--dir", args.fixtures,
                                     "--prefix", args.old_prefix])
    try:
        before = json.loads(out_before)
    except ValueError:
        before = {"parse_error": out_before[-400:]}
    before_ok = (rc_before == 0 and before.get("met") is True)

    # after: the strengthened instrument, one case per forgery
    forgeries = []
    for name in NAMES:
        leg = _run_leg(root, args.fixtures, args.old_prefix, (name,),
                       args.expect, args.world_rev, None)
        rows = leg["payload"].get("rows", [])
        reasons = rows[0]["reasons"] if rows else ["instrument-error"]
        forgeries.append({"name": name, "exit": leg["exit"], "reasons": reasons,
                          "expected_reason": FORGERY_REASONS[name],
                          "refused": leg["exit"] == 1
                          and reasons == [FORGERY_REASONS[name]]})

    # positive control: the honest v5 triple
    honest = _run_leg(root, args.honest_dir, args.honest_prefix, ("pos",),
                      args.expect, args.instrument_rev, None)
    honest_ok = honest["exit"] == 0 and honest["payload"].get("met") is True

    ok = before_ok and all(f["refused"] for f in forgeries) and honest_ok
    receipt = {
        "class": "R95-C1 forgery refusal",
        "counter": TOOL,
        "counter_sha256": _sha256_file(os.path.abspath(__file__)),
        "strengthened_instrument": "tools/round-95/c1-agreement-v2.py",
        "frozen_before_instrument": args.old_counter,
        "expect": args.expect,
        "world_revision": args.world_rev,
        "instrument_revision": args.instrument_rev,
        "before": {"exit": rc_before, "counts": before.get("counts_of_4"),
                   "met": before.get("met"), "admits": before_ok},
        "forgeries": forgeries,
        "honest": {"exit": honest["exit"], "met": honest["payload"].get("met"),
                   "rows": honest["payload"].get("rows", [])},
        "fixture_sha256": {n: {ext: _sha256_file(os.path.join(args.fixtures,
                          "%s-%s.%s" % (args.old_prefix, n, ext)))
                          for ext in ("json", "stdout", "rc")} for n in NAMES},
        "met": ok,
    }
    rendered = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(rendered + "\n")
    print(rendered)
    refused_n = sum(1 for f in forgeries if f["refused"])
    print("forgeries refused %d of 4; before admits %s; honest accepted %s"
          % (refused_n, before_ok, honest_ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
