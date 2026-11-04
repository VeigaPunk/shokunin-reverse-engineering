#!/usr/bin/env python3
"""c1-do-nothing.py - the do-nothing control for R66-C1 (phase-4 rule).

Cheapest control that SKIPS the claimed work: the round-65 counter's own
semantics — closure check taken BEFORE the setup probe, the entry count emitted
but never asserted, and `--skip-run` emitting a synthetic `closure.ok: true`.
Scored with the R66-C1 arm predicates (the frozen counter's own five
conditions). If this control met the target, the counter or the target would be
wrong.

Receipt: {"arms": 5, "passed": N, "ok": false, "target": 5}.

Run: TMPDIR=<scratch> python3 -I -B .ufo/waves/round-66/l1/controls/c1-do-nothing.py \
       --repo <lane> --out <receipt.json>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

V1_PATH = "tools/round-65/jsc-closure-matrix.py"
V1_PIN = "79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6"
COUNT = 30


def sha256_file(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def r65_order_state(v1, root: Path, manifest: dict, probe_fn) -> dict:
    """r65's order: pin + cache check BEFORE the probe; no post-probe scan; no count assert."""
    missing, mismatch = [], []
    for rel, want in manifest.items():
        p = root / rel
        if not p.is_file():
            missing.append(rel)
        elif sha256_file(p) != want:
            mismatch.append(rel)
    cache = v1.cache_entries(root)          # BEFORE the probe (the defect)
    probe_ok, probe_msg = probe_fn()
    entries = len(manifest) + 3             # emitted, never asserted (the defect)
    findings = []
    if missing:
        findings.append(f"missing {len(missing)}")
    if mismatch:
        findings.append(f"pin mismatch {len(mismatch)}")
    if cache:
        findings.append(f"cache present {len(cache)}")
    if not probe_ok:
        findings.append(f"probe failed: {probe_msg}")
    return {"entries": entries, "missing": missing, "pin_mismatch": mismatch,
            "cache_present": cache, "findings": findings,
            "ok": not missing and not mismatch and not cache and probe_ok}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=".")
    ap.add_argument("--toolchain-root", default="/home/vgpnk/.local/share/kaidoku-jsc")
    ap.add_argument("--python", default=None)
    ap.add_argument("--node", default="/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node")
    ap.add_argument("--probe", default=".ufo/waves/round-64/inputs/probe-electron.jsc")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    scratch = Path(tempfile.mkdtemp(prefix="r66-c1-ctl-",
                                    dir=os.environ.get("TMPDIR") or None))
    v1 = load(repo / V1_PATH, "v1")
    v2 = load(repo / "tools/round-66/closure-boundary.py", "v2")
    digest = sha256_file(repo / V1_PATH)
    tc = Path(args.toolchain_root)
    python = args.python or (str(tc / "venv/bin/python"))
    node = Path(args.node)
    probe = (repo / args.probe).resolve()
    interp = Path(python).resolve()

    def pins_fixture(root: Path) -> dict:
        known = v2.pins_for(root, v2.FIXTURE_RELS)
        return known

    def fixture_externals(root: Path) -> dict:
        known = v2.pins_for(root, ("probe.jsc", "node", "interp"))
        return {"probe": known["probe.jsc"], "node": known["node"],
                "interpreter": known["interp"]}

    arms = []

    def score(name: str, passed: bool, detail: dict):
        arms.append({"arm": name, "passed": bool(passed), "detail": detail})

    # --- a1/a2: r65 order on a fixture root; the unguarded probe writes a cache
    # AFTER r65's only cache scan, so the counter never sees it.
    for arm_name, guarded, want_pass in (
            ("a1-guarded-fixture-green", True, True),
            ("a2-unguarded-fixture-red", False, False)):
        # two SEPARATE fixtures: the r66 arms' fixture must not leave the cache
        # the r65-order fixture would then scan before its own probe.
        fx66 = scratch / f"arm66-{arm_name}"
        v2.write_fixture(fx66)
        st = v2.closure_state(v1, fx66, fx66 / "probe.jsc", fx66 / "node",
                              fx66 / "interp", pins_fixture(fx66),
                              len(v2.FIXTURE_RELS) + 3,
                              v2.fixture_probe(v1, python, fx66, guarded=guarded),
                              fixture_externals(fx66))
        fx = scratch / f"ctl-{arm_name}"
        v2.write_fixture(fx)
        st65 = r65_order_state(v1, fx, pins_fixture(fx),
                               v2.fixture_probe(v1, python, fx, guarded=guarded))
        post = v1.cache_entries(fx)
        met = (st65["ok"] is True) if guarded else (
            st65["ok"] is False and any(p.endswith(".pyc") for p in st65["cache_present"]))
        score(arm_name, met,
              {"r65_order_state": {"ok": st65["ok"],
                                   "cache_present": st65["cache_present"],
                                   "entries": st65["entries"]},
               "cache_on_disk_after_probe": post,
               "r66_arm_would_pass": want_pass,
               "control_meets_r66_arm": met})

    # --- a3/a4: the frozen 30-entry manifest, and a one-entry-short copy.
    real_probe = v2.real_probe(v1, python, tc)
    st3 = r65_order_state(v1, tc, dict(v1.CLOSURE), real_probe)
    score("a3-real-manifest-count-green",
          st3["ok"] is True and st3["entries"] == COUNT and "count_ok" in st3,
          {"r65_order_state": {"ok": st3["ok"], "entries": st3["entries"]},
           "count_ok_field_present": "count_ok" in st3,
           "control_meets_r66_arm": False,
           "reason": "r65 emits the count but asserts nothing, so the arm's count_ok clause has no line"})

    # a4: a scratch copy of the r65 instrument with one CLOSURE entry deleted,
    # run through its own --manifest CLI (the truncated-manifest defect).
    trunc_dir = scratch / "r65-trunc"
    trunc_dir.mkdir(parents=True)
    src = (repo / V1_PATH).read_text(encoding="utf-8")
    dropped = list(v1.CLOSURE)[0]
    marker = f'    "{dropped}":'
    lines = src.splitlines(keepends=True)
    kept, skipped = [], False
    for line in lines:
        if not skipped and line.startswith(marker):
            skipped = True
            continue
        kept.append(line)
    (trunc_dir / "jsc-closure-matrix.py").write_text("".join(kept), encoding="utf-8")
    r = subprocess.run([python, "-I", "-B", str(trunc_dir / "jsc-closure-matrix.py"),
                        "--manifest", "--probe", str(probe)],
                       capture_output=True, text=True, timeout=600)
    try:
        # v1 --manifest prints the closure dict to stdout and has no --out
        body = json.loads(r.stdout)
    except (ValueError, json.JSONDecodeError):
        body = {}
    score("a4-truncated-manifest-red",
          body.get("ok") is False and any("29" in str(f) for f in body.get("findings", [])),
          {"r65_exit": r.returncode, "r65_manifest": {k: body.get(k) for k in
                                                     ("entries", "ok", "findings")},
           "control_meets_r66_arm": False,
           "reason": "r65 --manifest exits 0 with a synthetic ok on a manifest one entry short"})

    # --- a5: r65 --skip-run claims a closure it never evaluated.
    out5 = scratch / "r65-skiprun.json"
    r5 = subprocess.run([python, "-I", "-B", str(repo / V1_PATH),
                         "--skip-run", "--probe", str(probe), "--out", str(out5)],
                        capture_output=True, text=True, timeout=300)
    try:
        body5 = json.loads(out5.read_text())
    except (OSError, json.JSONDecodeError):
        body5 = {}
    closure5 = body5.get("closure") or {}
    met5 = closure5 is None or closure5.get("ok") is not True
    score("a5-skip-run-no-closure", met5,
          {"r65_exit": r5.returncode, "r65_closure": body5.get("closure"),
           "control_meets_r66_arm": met5,
           "reason": "r65 --skip-run hardcodes closure.ok true"})

    passed = sum(1 for a in arms if a["passed"])
    result = {"tool": "c1-do-nothing control",
              "skips": "the probe-before-cache order, the count assertion and the skip-run closure claim",
              "v1_path": V1_PATH, "v1_pin": V1_PIN, "v1_sha256": digest,
              "arms": arms, "arms_total": len(arms), "passed": passed,
              "target": len(arms), "ok": passed == len(arms)}
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    sys.stdout.write(json.dumps({k: result[k] for k in ("passed", "arms_total", "ok")}) + "\n")
    shutil.rmtree(scratch, ignore_errors=True)
    return 0 if passed < len(arms) else 1


if __name__ == "__main__":
    sys.exit(main())
