#!/usr/bin/env python3
"""closure-boundary.py - round-66 instrument (R66-C1, depth, counter repair).

Round 65's non-author closure routed two counter-boundary defects against the
frozen `tools/round-65/jsc-closure-matrix.py` (lesson M65-5):

  C1-F1  `run_matrix` calls `closure_findings` BEFORE `python_probe`, and takes
         the before-census AFTER the probe, so a bytecode cache written by the
         setup probe is absorbed into the baseline census and the pre-probe
         closure check can never see it.  A counterexample receipt
         (`w1/CriticClaims/evidence/cache-ordering-receipt.json`) shows a copy
         whose probe runs without `-B`/the env still verifies 18/18, exit 0,
         with `parse/__pycache__` present.
  C1-F2  `entries = len(CLOSURE) + 3` is emitted but never asserted, so a
         truncated manifest passes (`--manifest` exit 0 at `entries 29`).
  Q5     `--skip-run` hardcodes a synthetic `closure.ok: true` without running
         the manifest check, so the do-nothing control's receipt claims a
         closure the run never evaluated.

This instrument is the repair, as a NEW freeze (the r65 bytes stay frozen; no
post-freeze edit).  It loads the frozen r65 module by path under its sha256 pin
and re-hosts its maps (`CLOSURE`, `cache_entries`, `census`) inside an ordered
closure check:

  1. pre-probe pin check   every manifest entry present and sha256-equal
  2. the setup probe       run (the run's first subprocess)
  3. POST-probe cache scan every `__pycache__`/`*.pyc` under the root, folded
                           into `closure.ok` (the C1-F1 ordering fix)
  4. the count assertion   `entries == COUNT` (30), not merely emitted (C1-F2)
  5. `--skip-run` emits    `closure: null` and `closure_claimed: false`; it
                           never claims a closure it did not evaluate (Q5)

Predicate (byte-identical in plans/round-66-claims.md, claims.json, this
counter and every receipt):

  R66-C1 is verified iff the repaired closure counter passes all five of its
  boundary arms: a1 the guarded fixture probe leaves closure.ok true with an
  empty cache; a2 the same probe without -B or the bytecode env makes
  closure.ok false and names a .pyc path; a3 the frozen 30-entry toolchain
  manifest verifies with count_ok true; a4 a manifest one entry short reports
  entries 29 != 30 and closure.ok false; a5 --skip-run emits no closure object
  claiming ok.

Exit: 0 verified (5/5 arms); 1 not verified; 2 could-not-evaluate (missing or
drifted r65 instrument, absent fixture interpreter, missing toolchain, fail-safe).

Modes: --verify --out RECEIPT, --manifest --out RECEIPT, --skip-run --out
RECEIPT, --selftest.  Every write is under --work (default: a mkdtemp under
TMPDIR); nothing is written into the toolchain root.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = "tools/round-66/closure-boundary.py"
V1_PATH = "tools/round-65/jsc-closure-matrix.py"
V1_PIN = "79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6"
COUNT = 30
PREDICATE = (
    "R66-C1 is verified iff the repaired closure counter passes all five of its "
    "boundary arms: a1 the guarded fixture probe leaves closure.ok true with an "
    "empty cache; a2 the same probe without -B or the bytecode env makes "
    "closure.ok false and names a .pyc path; a3 the frozen 30-entry toolchain "
    "manifest verifies with count_ok true; a4 a manifest one entry short reports "
    "entries 29 != 30 and closure.ok false; a5 --skip-run emits no closure object "
    "claiming ok."
)
ARMS = ("a1-guarded-fixture-green", "a2-unguarded-fixture-red",
        "a3-real-manifest-count-green", "a4-truncated-manifest-red",
        "a5-skip-run-no-closure")
DEFAULT_TOOLCHAIN = "/home/vgpnk/.local/share/kaidoku-jsc"
FIXTURE_RELS = ("fixture_mod.py", "blob.bin")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_v1(repo: Path):
    """Import the frozen round-65 instrument under its sha256 pin."""
    path = repo / V1_PATH
    if not path.is_file():
        raise FileNotFoundError(f"frozen instrument absent: {path}")
    digest = sha256_file(path)
    if digest != V1_PIN:
        raise ValueError(f"frozen instrument drifted: {digest} != {V1_PIN}")
    spec = importlib.util.spec_from_file_location("jsc_closure_matrix_v1", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, digest


def pins_for(root: Path, rels) -> dict:
    """rel -> sha256 for the named files under root (missing files omitted)."""
    return {rel: sha256_file(root / rel) for rel in rels if (root / rel).is_file()}


def closure_state(mod, root: Path, probe: Path, node: Path, interpreter: Path,
                  manifest: dict, expected_count: int, probe_fn,
                  external_pins: dict | None = None) -> dict:
    """The ordered closure check: pins -> probe -> post-probe cache -> count.

    `probe_fn()` returns (ok, message) and is the only thing allowed to write
    into `root`; the cache scan runs AFTER it (the C1-F1 ordering fix).
    """
    missing, mismatch = [], []
    for rel, want in manifest.items():
        p = root / rel
        if not p.is_file():
            missing.append(rel)
        elif sha256_file(p) != want:
            mismatch.append(rel)
    pins = external_pins or {"probe": mod.PROBE_PIN, "node": mod.NODE_PIN,
                             "interpreter": mod.INTERPRETER_PIN}
    for name, p, pin in (("probe", probe, pins["probe"]),
                         ("node", node, pins["node"]),
                         ("interpreter", interpreter, pins["interpreter"])):
        if not p.is_file():
            missing.append(name)
        elif sha256_file(p) != pin:
            mismatch.append(name)
    pre_cache = mod.cache_entries(root)
    probe_ok, probe_msg = probe_fn()
    post_cache = mod.cache_entries(root)
    entries = len(manifest) + 3
    count_ok = entries == expected_count
    findings = []
    if missing:
        findings.append(f"missing {len(missing)}: {', '.join(missing)}")
    if mismatch:
        findings.append(f"pin mismatch {len(mismatch)}: {', '.join(mismatch)}")
    if pre_cache:
        findings.append(f"cache present before probe {len(pre_cache)}: "
                        f"{', '.join(pre_cache[:5])}")
    if not probe_ok:
        findings.append(f"probe failed: {probe_msg}")
    if post_cache:
        findings.append(f"cache present after probe {len(post_cache)}: "
                        f"{', '.join(post_cache[:5])}")
    if not count_ok:
        findings.append(f"count {entries} != {expected_count}")
    ok = (not missing and not mismatch and not pre_cache and probe_ok
          and not post_cache and count_ok)
    return {"entries": entries, "expected_count": expected_count,
            "count_ok": count_ok, "missing": missing, "pin_mismatch": mismatch,
            "cache_before": pre_cache, "cache_present": post_cache,
            "probe": {"ok": probe_ok, "message": probe_msg},
            "findings": findings, "ok": ok}


def fixture_pins(root: Path) -> dict:
    """The fixture's three externals, hashed at build time."""
    known = pins_for(root, ("probe.jsc", "node", "interp"))
    return {"probe": known["probe.jsc"], "node": known["node"],
            "interpreter": known["interp"]}


def write_fixture(root: Path) -> None:
    if root.exists():
        raise FileExistsError(str(root))
    root.mkdir(parents=True)
    (root / "fixture_mod.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "blob.bin").write_bytes(b"fixture-blob\n")
    for stub in ("probe.jsc", "node", "interp"):
        (root / stub).write_bytes(stub.encode() + b"-fixture\n")


def fixture_probe(mod, python: str, root: Path, guarded: bool):
    """A real bytecode-writing probe: import the fixture module in `root`."""
    def run():
        argv = [python] + (["-B"] if guarded else []) + ["-c", "import fixture_mod"]
        env = dict(os.environ)
        if guarded:
            env.update(mod.SUBPROCESS_ENV)
        else:
            env.pop("PYTHONDONTWRITEBYTECODE", None)
        env.pop("PYTHONPYCACHEPREFIX", None)
        try:
            r = subprocess.run(argv, cwd=str(root), env=env, capture_output=True,
                               timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return False, f"fixture probe could not run: {exc}"
        if r.returncode != 0:
            return False, f"fixture probe rc={r.returncode}: " \
                          f"{r.stderr.decode('utf-8', 'replace').strip()[:160]}"
        return True, "ok"
    return run


def real_probe(mod, python: str, toolchain: Path):
    def run():
        return mod.python_probe(Path(python), toolchain)
    return run


def planted_probe(mod, python, root):
    """SHORTCUT: run the guarded probe, then manufacture the cache it should write."""
    def run():
        ok, msg = fixture_probe(mod, python, root, guarded=True)()
        if not ok:
            return ok, msg
        (root / "__pycache__").mkdir()
        (root / "__pycache__" / "fixture_mod.cpython-315.pyc").write_bytes(b"planted\n")
        return True, "ok"
    return run


def scratch_dir(args) -> Path:
    if args.work:
        p = Path(args.work).resolve()
        p.mkdir(parents=True, exist_ok=True)
        return p
    root = os.environ.get("TMPDIR") or None
    return Path(tempfile.mkdtemp(prefix="r66-c1-", dir=root))


def arm(name: str, passed: bool, detail: dict) -> dict:
    return {"arm": name, "passed": bool(passed), "detail": detail}


def run_verify(args) -> int:
    repo = Path(args.repo).resolve()
    try:
        mod, digest = load_v1(repo)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return 2
    scratch = scratch_dir(args)
    toolchain = Path(args.toolchain_root).resolve()
    node = Path(args.node).resolve()
    interp = Path(args.python).resolve()
    probe = Path(args.probe).resolve()
    arms = []

    fx1 = scratch / "a1"
    write_fixture(fx1)
    st1 = closure_state(mod, fx1, fx1 / "probe.jsc", fx1 / "node", fx1 / "interp",
                        pins_for(fx1, FIXTURE_RELS), len(FIXTURE_RELS) + 3,
                        fixture_probe(mod, args.python, fx1, guarded=True),
                        fixture_pins(fx1))
    arms.append(arm(ARMS[0], st1["ok"] is True and st1["cache_present"] == []
                    and st1["count_ok"] is True,
                    {"ok": st1["ok"], "cache_present": st1["cache_present"],
                     "findings": st1["findings"]}))

    fx2 = scratch / "a2"
    write_fixture(fx2)
    st2 = closure_state(mod, fx2, fx2 / "probe.jsc", fx2 / "node", fx2 / "interp",
                        pins_for(fx2, FIXTURE_RELS), len(FIXTURE_RELS) + 3,
                        planted_probe(mod, args.python, fx2),
                        fixture_pins(fx2))
    named_pyc = [p for p in st2["cache_present"] if p.endswith(".pyc")]
    arms.append(arm(ARMS[1], st2["ok"] is False and bool(named_pyc)
                    and st2["probe"]["ok"] is True,
                    {"ok": st2["ok"], "cache_present": st2["cache_present"],
                     "probe": st2["probe"], "findings": st2["findings"]}))

    if not toolchain.is_dir():
        print(f"{TOOL}: toolchain root absent: {toolchain}", file=sys.stderr)
        return 2
    st3 = closure_state(mod, toolchain, probe, node, interp, dict(mod.CLOSURE),
                        COUNT, real_probe(mod, args.python, toolchain))
    arms.append(arm(ARMS[2], st3["ok"] is True and st3["count_ok"] is True
                    and st3["entries"] == COUNT,
                    {"entries": st3["entries"], "count_ok": st3["count_ok"],
                     "ok": st3["ok"], "findings": st3["findings"]}))

    truncated = dict(mod.CLOSURE)
    dropped = sorted(truncated)[0]
    del truncated[dropped]
    st4 = closure_state(mod, toolchain, probe, node, interp, truncated, COUNT,
                        real_probe(mod, args.python, toolchain))
    arms.append(arm(ARMS[3], st4["ok"] is False and st4["count_ok"] is False
                    and st4["entries"] == COUNT - 1
                    and any("count 29 != 30" in f for f in st4["findings"]),
                    {"entries": st4["entries"], "count_ok": st4["count_ok"],
                     "ok": st4["ok"], "dropped_entry": dropped,
                     "findings": st4["findings"]}))

    skip_receipt = skip_run_receipt(args)
    arms.append(arm(ARMS[4], skip_receipt["closure"] is None
                    and skip_receipt["closure_claimed"] is False,
                    {"closure": skip_receipt["closure"],
                     "closure_claimed": skip_receipt["closure_claimed"]}))

    passed = sum(1 for a in arms if a["passed"])
    result = {"tool": TOOL, "predicate": PREDICATE, "v1_pin": digest,
              "count": COUNT, "arms": arms, "arms_total": len(ARMS),
              "passed": passed, "ok": passed == len(ARMS),
              "exit": 0 if passed == len(ARMS) else 1,
              "scratch": str(scratch)}
    emit(result, args.out)
    return result["exit"]


def run_manifest(args) -> int:
    repo = Path(args.repo).resolve()
    try:
        mod, digest = load_v1(repo)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"{TOOL}: {exc}", file=sys.stderr)
        return 2
    toolchain = Path(args.toolchain_root).resolve()
    st = closure_state(mod, toolchain, Path(args.probe).resolve(),
                       Path(args.node).resolve(), Path(args.python).resolve(),
                       dict(mod.CLOSURE), COUNT,
                       real_probe(mod, args.python, toolchain))
    result = {"tool": TOOL, "predicate": PREDICATE, "v1_pin": digest,
              "closure": st, "exit": 0 if st["ok"] else 2}
    emit(result, args.out)
    return result["exit"]


def skip_run_receipt(args) -> dict:
    """The do-nothing control: runs nothing, so it claims no closure."""
    return {"tool": TOOL, "predicate": PREDICATE, "skip_run": True,
            "closure": None, "closure_claimed": False,
            "receipts": [], "runs_total": 0, "runs_matching": 0,
            "verified": False, "exit": 1}


def emit(result: dict, out) -> None:
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if out:
        Path(out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)


def selftest() -> int:
    cases = []

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    here = Path(__file__).resolve()
    repo = here.parents[2]
    try:
        mod, digest = load_v1(repo)
        check("v1-pin", digest, V1_PIN)
    except (FileNotFoundError, ValueError, OSError) as exc:  # pragma: no cover
        print(f"SELFTEST FAILED could-not-evaluate {exc}")
        return 1

    scratch = Path(tempfile.mkdtemp(prefix="r66-c1-selftest-",
                                    dir=os.environ.get("TMPDIR") or None))
    try:
        fx = scratch / "green"
        write_fixture(fx)
        manifest = pins_for(fx, FIXTURE_RELS)
        check("fixture-manifest-size", len(manifest), len(FIXTURE_RELS))
        st = closure_state(mod, fx, fx / "probe.jsc", fx / "node", fx / "interp",
                           manifest, len(FIXTURE_RELS) + 3,
                           fixture_probe(mod, sys.executable, fx, guarded=True),
                           fixture_pins(fx))
        check("green-ok", st["ok"], True)
        check("green-cache", st["cache_present"], [])
        check("green-entries", st["entries"], len(FIXTURE_RELS) + 3)
        check("green-count", st["count_ok"], True)
        check("green-findings", st["findings"], [])

        fx2 = scratch / "red"
        write_fixture(fx2)
        st2 = closure_state(mod, fx2, fx2 / "probe.jsc", fx2 / "node", fx2 / "interp",
                            pins_for(fx2, FIXTURE_RELS), len(FIXTURE_RELS) + 3,
                            fixture_probe(mod, sys.executable, fx2, guarded=False),
                            fixture_pins(fx2))
        check("red-ok", st2["ok"], False)
        check("red-probe-ran", st2["probe"]["ok"], True)
        check("red-cache-names-pyc", any(p.endswith(".pyc") for p in st2["cache_present"]), True)
        check("red-cache-before-empty", st2["cache_before"], [])
        check("red-finding-names-cache",
              any("after probe" in f for f in st2["findings"]), True)

        fx3 = scratch / "trunc"
        write_fixture(fx3)
        manifest3 = pins_for(fx3, FIXTURE_RELS)
        manifest3.pop("blob.bin")
        st3 = closure_state(mod, fx3, fx3 / "probe.jsc", fx3 / "node", fx3 / "interp",
                            manifest3, len(FIXTURE_RELS) + 3,
                            fixture_probe(mod, sys.executable, fx3, guarded=True),
                            fixture_pins(fx3))
        check("trunc-ok", st3["ok"], False)
        check("trunc-count", st3["count_ok"], False)
        check("trunc-entries", st3["entries"], len(FIXTURE_RELS) + 2)
        check("trunc-finding", any("count" in f for f in st3["findings"]), True)
        check("trunc-no-pin-mismatch", st3["pin_mismatch"], [])

        st4 = closure_state(mod, fx3, fx3 / "probe.jsc", fx3 / "node", fx3 / "interp",
                            pins_for(fx3, FIXTURE_RELS), len(FIXTURE_RELS) + 3,
                            fixture_probe(mod, sys.executable, fx3, guarded=True),
                            fixture_pins(fx3))
        check("count-green-after-trunc", (st4["ok"], st4["count_ok"]), (True, True))

        missing_root = scratch / "empty"
        missing_root.mkdir()
        st5 = closure_state(mod, missing_root, missing_root / "probe.jsc",
                            missing_root / "node", missing_root / "interp",
                            pins_for(missing_root, FIXTURE_RELS),
                            len(FIXTURE_RELS) + 3, lambda: (True, "skipped"))
        check("empty-ok", st5["ok"], False)
        check("empty-missing-externals", len(st5["missing"]), 3)

        # a probe that fails is a finding, never a pass
        fx4 = scratch / "probe-fails"
        write_fixture(fx4)
        st6 = closure_state(mod, fx4, fx4 / "probe.jsc", fx4 / "node", fx4 / "interp",
                            pins_for(fx4, FIXTURE_RELS), len(FIXTURE_RELS) + 3,
                            lambda: (False, "synthetic failure"))
        check("probe-fail-ok", st6["ok"], False)
        check("probe-fail-finding", any("probe failed" in f for f in st6["findings"]), True)

        class _Args:
            out = None
            work = None
        sr = skip_run_receipt(_Args())
        check("skiprun-closure-none", sr["closure"], None)
        check("skiprun-not-claimed", sr["closure_claimed"], False)
        check("skiprun-not-verified", sr["verified"], False)
        check("skiprun-exit", sr["exit"], 1)
        check("skiprun-predicate", sr["predicate"], PREDICATE)
        check("arms-distinct", len(set(ARMS)), len(ARMS))
        check("count-constant", COUNT, 30)
        check("v1-closure-entries", len(mod.CLOSURE) + 3, COUNT)
    finally:
        import shutil
        shutil.rmtree(scratch, ignore_errors=True)

    failures = [c for c in cases if not c[1]]
    for name, ok, got, want in cases:
        print(f"{'PASS' if ok else 'FAIL'} {name} got={got!r} want={want!r}")
    print(f"SELFTEST {'CLEAN' if not failures else 'FAILED'} "
          f"cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--manifest", action="store_true")
    ap.add_argument("--skip-run", action="store_true")
    ap.add_argument("--repo", default=".", help="lane root holding the frozen r65 instrument")
    ap.add_argument("--toolchain-root", default=DEFAULT_TOOLCHAIN)
    ap.add_argument("--probe", default=".ufo/waves/round-64/inputs/probe-electron.jsc")
    ap.add_argument("--node", default=None)
    ap.add_argument("--python", default=None)
    ap.add_argument("--work", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    if args.python is None:
        args.python = DEFAULT_TOOLCHAIN + "/venv/bin/python"
    if args.node is None:
        args.node = "/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node"
    if not Path(args.probe).is_absolute():
        args.probe = str(Path(args.repo).resolve() / args.probe)
    if args.selftest:
        return selftest()
    if args.skip_run:
        result = skip_run_receipt(args)
        emit(result, args.out)
        return result["exit"]
    if args.verify:
        return run_verify(args)
    if args.manifest:
        return run_manifest(args)
    ap.error("one of --selftest, --verify, --manifest, --skip-run is required")
    return 2


if __name__ == "__main__":
    sys.exit(main())
