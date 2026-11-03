#!/usr/bin/env python3
"""jsc-closure-matrix.py - round-65 instrument (R65-C1, depth, capability acquisition).

Round 64 stopped R64-C1 honestly: the 18/18 label matrix reproduced, but the
frozen predicate's clause "every input and binary sha256 equal to its pin" could
not be certified (round-64 non-author review F1: D2/D3 snapshot_blob.bin,
icudtl.dat variants and the transitive View8 tree unpinned; F2: the View8 run
wrote __pycache__ into the frozen toolchain).  Round 65 repairs the closure and
re-runs the same matrix under it.

Closure (every file the matrix run reads, plus every executable it spawns):

  d8 builds      d8-14.8.178.14, d8-14.8.178.1, d8-14.7.173, each pinned on
                 d8 + snapshot_blob.bin + icudtl.dat (9 files)
  View8 tree     the 12 files under jsc2js-src/View8 (the whole import closure:
                 view8.py, Parser/, Simplify/, Translate/, Bin/, README.md)
  venv identity  the interpreter symlink target's real binary (sha256 of the
                 resolved path), parse/__init__.py, parse/__init__.pyi,
                 parse-1.22.4.dist-info/METADATA, parse-1.22.4.dist-info/RECORD,
                 venv/pyvenv.cfg
  artifacts      the Typora code cache (inside the toolchain root) and the
                 Electron probe cache (repo path)
  harness        the node binary that runs `node --check` (real path + sha256)

The manifest check also refuses a toolchain that still holds Python bytecode
cache (`__pycache__` directories or `*.pyc` files): a run that starts from a
contaminated tree cannot demonstrate that the run itself wrote nothing.

The no-writes clause is a census: every regular file under the toolchain root
(except `jsc2js-src/.git/`, git metadata that is not a run input and that a
read-only `git` call may refresh) is hashed before the first run and after the
last one; the two maps must be equal.  A file added, removed or changed during
the run is a finding.  mtime is not compared: a byte-identical rewrite is a
limit, stated, never claimed covered.

Predicate (the same sentence appears in plans/round-65-claims.md, claims.json
and the receipts):

  R65-C1 is verified iff (i) the frozen closure manifest matches every one of
  its entries (count and sha256) with no Python bytecode cache present before
  the first run, (ii) all 18 runs reproduce the frozen predicted label of their
  cell (dump|view8|check), and (iii) the after-run toolchain census equals the
  before-run census.

Every subprocess runs with PYTHONDONTWRITEBYTECODE=1 in its environment and
`-B` in its argv (the round-64 F2 repair).

Exit: 0 verified; 1 claim not verified (any label mismatch, including the
--skip-run do-nothing control, or an unequal census); 2 could-not-evaluate
(missing root or input, closure finding, cache present, missing tool).

Modes: --selftest, --manifest (closure check only), --census OUT, --compare A B,
--skip-run (do-nothing control), or a full run (the default after validation).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

TOOL = "tools/round-65/jsc-closure-matrix.py"
PREDICATE = (
    "R65-C1 is verified iff (i) the frozen closure manifest matches every one of its "
    "entries (count and sha256) with no Python bytecode cache present before the first "
    "run, (ii) all 18 runs reproduce the frozen predicted label of their cell "
    "(dump|view8|check), and (iii) the after-run toolchain census equals the before-run census."
)
REPS = 3
DEFAULT_ROOT = "/home/vgpnk/.local/share/kaidoku-jsc"
DEFAULT_PYTHON = DEFAULT_ROOT + "/venv/bin/python"
CENSUS_EXCLUDE = ("jsc2js-src/.git/",)

# toolchain-root-relative path -> sha256.  Frozen before the operative freeze;
# every entry was opened and hashed in this round (round-65 prep receipt).
CLOSURE = {
    "d8-14.8.178.14/d8": "bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331",
    "d8-14.8.178.14/snapshot_blob.bin": "b5c418dc0c6006d8dc6f4ac9981182eecf783cd892ae4c4b4ba16977c17bf2bb",
    "d8-14.8.178.14/icudtl.dat": "c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6",
    "d8-14.8.178.1/d8": "4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8",
    "d8-14.8.178.1/snapshot_blob.bin": "601efdc639d9f439cca3d1274e0917ab28ee09d6870787d6052d8949fa73e24d",
    "d8-14.8.178.1/icudtl.dat": "c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6",
    "d8-14.7.173/d8": "c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2",
    "d8-14.7.173/snapshot_blob.bin": "80590f459ddbac237de5f282196b2c551e24982f31150cb8998a3b4898ea2720",
    "d8-14.7.173/icudtl.dat": "c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6",
    "jsc2js-src/View8/view8.py": "b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c",
    "jsc2js-src/View8/README.md": "557d14a20a622d42f620547b19c41d2f7224bc264f6fc22f64bedb4164efcf50",
    "jsc2js-src/View8/Bin/VersionDetector.exe": "61347ee8eddcbe2c77229bc3f8ee8ccc9437e31710afbfc33b5ace886747c95e",
    "jsc2js-src/View8/Parser/parse_v8cache.py": "98ffc4b5b638f955f45fb219b1934a03a03a921fc4c18fcea6f08d495dcc3bc5",
    "jsc2js-src/View8/Parser/sfi_file_parser.py": "7ce34163cace6e818f405d0177400c0d24fab36e35644c893e8437dccae444a1",
    "jsc2js-src/View8/Parser/shared_function_info.py": "b5c79cdd27fdc2a2480a7b34a5142bd83b92ddda9f563f99d34a5f987d1aae2e",
    "jsc2js-src/View8/Simplify/function_context_stack.py": "51b6f4f50c45741626ad3a9ad4ddc199ff0288d51c662d18001fd2d2f4f9a810",
    "jsc2js-src/View8/Simplify/global_scope_replace.py": "0f217057142f07503780265d1d13488bfa26ac24ee97a4a1438565017d2fe16e",
    "jsc2js-src/View8/Simplify/simplify.py": "9603ff0fc837720cbb39cc3b27ba1a7e707dba76d3f05203bfb623f746402cf7",
    "jsc2js-src/View8/Translate/jump_blocks.py": "ab0acbff954a1424f3c0804b0942ad84372c5d510b8ae299ae0621cdbf33f044",
    "jsc2js-src/View8/Translate/translate.py": "0e07589374ad38541c2edaf9867e7dc8ad4636eb6dff3532ea62503a01ff9f78",
    "jsc2js-src/View8/Translate/translate_table.py": "717e2a67c3792b09160082efa50f0553f35ef197293e625bf653dedb382cf4a3",
    "venv/lib/python3.15/site-packages/parse/__init__.py": "27ddec2fdfc9a5a97d8086eb4c073f3f9a3c7a8e5086c13adc198114ac6ba8c0",
    "venv/lib/python3.15/site-packages/parse/__init__.pyi": "0ada9b911ad08edcbb9d8e06fc57033fdc2eb93bd4e978ffae53af928c0d4f00",
    "venv/lib/python3.15/site-packages/parse-1.22.4.dist-info/METADATA": "e4179e24374e7084ebe589092e44bf2c8aa03cfec9756a56fcaa98a056bb232c",
    "venv/lib/python3.15/site-packages/parse-1.22.4.dist-info/RECORD": "58aa77c758d4c307da016a6e4db5011d7069bfa1053c836235cce94e7b2bd8c6",
    "venv/pyvenv.cfg": "87a6b46ee1f9261cabbe8efb4b60639c50dfc14d77157fd670390e411152f335",
    "inputs/atom.compiled.dist.jsc": "6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9",
}
PROBE_PIN = "a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710"
NODE_PIN = "7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c"
NODE_PATH = "/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin/node"
INTERPRETER_PIN = "aac3ade3f7d90fbf63e3ea0c46120a0cfbd159e1e503dde04721979507a1548b"
INTERPRETER_PATH = "/home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15"

# The frozen predictions, unchanged from round 64 (written before the r64 matrix
# run).  A cell whose label differs from its prediction is a finding; it is
# never re-predicted.
PREDICTED = {
    ("probe", "D1"): "dump-ok|view8-ok|node-fail",
    ("probe", "D2"): "dump-ok|view8-ok|node-fail",
    ("probe", "D3"): "dump-exit-139|view8-skipped|node-skipped",
    ("typora", "D1"): "dump-exit-134|view8-skipped|node-skipped",
    ("typora", "D2"): "dump-exit-134|view8-skipped|node-skipped",
    ("typora", "D3"): "dump-exit-134|view8-skipped|node-skipped",
}

SFI_RE = re.compile(rb"\[SharedFunctionInfo\]")
SUBPROCESS_ENV = {"PYTHONDONTWRITEBYTECODE": "1"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_rc(rc: int) -> int:
    """Python reports a signal death as -signo; a POSIX shell reports 128+signo."""
    return 128 - rc if rc < 0 else rc


def classify_dump(rc, stdout: bytes) -> str:
    if rc == "timeout":
        return "dump-timeout"
    code = norm_rc(rc)
    if code != 0:
        return f"dump-exit-{code}"
    if not SFI_RE.search(stdout):
        return "dump-empty"
    return "dump-ok"


def classify_view8(rc: int, out_size: int | None) -> str:
    code = norm_rc(rc)
    if code != 0:
        return f"view8-exit-{code}"
    if not out_size:
        return "view8-empty"
    return "view8-ok"


def classify_check(rc: int) -> str:
    return "node-pass" if norm_rc(rc) == 0 else "node-fail"


def compose(dump: str, view8: str | None, check: str | None) -> str:
    v = view8 if view8 is not None else "view8-skipped"
    c = check if check is not None else "node-skipped"
    return f"{dump}|{v}|{c}"


def verdict(labels: dict) -> tuple[int, dict]:
    """labels: {(artifact, build, rep): label}. Returns (exit, summary)."""
    total = len(PREDICTED) * REPS
    matches = 0
    mismatches = []
    for (artifact, build), predicted in PREDICTED.items():
        for rep in range(1, REPS + 1):
            got = labels.get((artifact, build, rep), "not-run")
            if got == predicted:
                matches += 1
            else:
                mismatches.append({"cell": [artifact, build], "rep": rep,
                                   "predicted": predicted, "observed": got})
    ok = matches == total
    return (0 if ok else 1), {"runs_total": total, "runs_matching": matches,
                              "mismatches": mismatches, "verified": ok}


def cache_entries(root: Path) -> list[str]:
    """Every __pycache__ directory and every *.pyc file under root."""
    out = []
    if not root.is_dir():
        return out
    for p in sorted(root.rglob("*")):
        if p.is_dir() and p.name == "__pycache__":
            out.append(str(p.relative_to(root)))
        elif p.is_file() and p.suffix == ".pyc":
            out.append(str(p.relative_to(root)))
    return out


def census(root: Path) -> dict:
    """relpath -> sha256 for every regular file under root, excluding CENSUS_EXCLUDE."""
    if not root.is_dir():
        raise FileNotFoundError(str(root))
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_symlink() or not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(rel == e.rstrip("/") or rel.startswith(e) for e in CENSUS_EXCLUDE):
            continue
        out[rel] = sha256_file(p)
    return out


def compare_censuses(before: dict, after: dict) -> dict:
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    return {"equal": not (added or removed or changed),
            "added": added, "removed": removed, "changed": changed}


def closure_findings(root: Path, probe: Path, node: Path, interpreter: Path) -> dict:
    """Closure check: every pinned entry present and equal, cache-free tree."""
    missing, mismatch = [], []
    for rel, want in CLOSURE.items():
        p = root / rel
        if not p.is_file():
            missing.append(rel)
        elif sha256_file(p) != want:
            mismatch.append(rel)
    for name, p, want in (("probe", probe, PROBE_PIN), ("node", node, NODE_PIN),
                          ("interpreter", interpreter, INTERPRETER_PIN)):
        if not p.is_file():
            missing.append(name)
        elif sha256_file(p) != want:
            mismatch.append(name)
    cache = cache_entries(root)
    findings = []
    if missing:
        findings.append(f"missing {len(missing)}: {', '.join(missing)}")
    if mismatch:
        findings.append(f"pin mismatch {len(mismatch)}: {', '.join(mismatch)}")
    if cache:
        findings.append(f"cache present {len(cache)}: {', '.join(cache[:5])}")
    return {"entries": len(CLOSURE) + 3, "missing": missing, "pin_mismatch": mismatch,
            "cache_present": cache, "findings": findings,
            "ok": not missing and not mismatch and not cache}


def python_probe(python: Path, root: Path) -> tuple[bool, str]:
    """The view8 interpreter must be able to import its pinned dependency."""
    env = dict(os.environ)
    env.update(SUBPROCESS_ENV)
    try:
        r = subprocess.run([str(python), "-B", "-c", "from parse import parse"],
                           capture_output=True, timeout=60, env=env,
                           cwd=str(root / "jsc2js-src/View8"))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"view8 interpreter probe failed: {exc}"
    if r.returncode != 0:
        return False, (f"view8 interpreter cannot import parse (rc={r.returncode}): "
                       f"{r.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return True, "ok"


def run_cell(d8: Path, artifact: Path, cell: Path, timeout: int):
    try:
        r = subprocess.run([str(d8), "-e", f"loadjsc('{artifact}')"],
                           cwd=str(cell), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "timeout", b"", b""
    return r.returncode, r.stdout, r.stderr


def run_matrix(args) -> int:
    root = Path(args.toolchain_root).resolve()
    probe = Path(args.probe).resolve()
    node = Path(args.node).resolve()
    interpreter = Path(args.python).resolve()
    closure = closure_findings(root, probe, node, interpreter)
    if not closure["ok"]:
        print(f"{TOOL}: closure check failed: {closure['findings']}", file=sys.stderr)
        return 2
    builds = {b: root / d for b, d in (("D1", "d8-14.8.178.14"),
                                       ("D2", "d8-14.8.178.1"),
                                       ("D3", "d8-14.7.173"))}
    if not all((builds[b] / "d8").is_file() for b in builds):
        print(f"{TOOL}: missing d8 build under {root}", file=sys.stderr)
        return 2
    inputs = {"probe": probe, "typora": root / "inputs/atom.compiled.dist.jsc"}
    view8_dir = root / "jsc2js-src/View8"
    work_root = Path(args.work).resolve()
    py_ok, py_msg = python_probe(Path(args.python), root)
    if not py_ok:
        print(f"{TOOL}: {py_msg}", file=sys.stderr)
        return 2
    work_root.mkdir(parents=True, exist_ok=True)
    before = census(root)
    env = dict(os.environ)
    env.update(SUBPROCESS_ENV)
    labels: dict = {}
    receipts = []
    for (artifact, build) in PREDICTED:
        for rep in range(1, REPS + 1):
            cell = work_root / f"{artifact}-{build}-r{rep}"
            cell.mkdir(parents=True, exist_ok=True)
            rc, out, err = run_cell(builds[build] / "d8", inputs[artifact], cell,
                                    args.timeout)
            (cell / "dump.txt").write_bytes(out)
            (cell / "dump.err").write_bytes(err)
            dump = classify_dump(rc, out)
            view8 = check = None
            out_size = None
            if dump == "dump-ok":
                out_js = cell / "reconstruction.js"
                r = subprocess.run(
                    [args.python, "-B", "view8.py", "--disassembled",
                     str(cell / "dump.txt"), str(out_js)],
                    cwd=str(view8_dir), capture_output=True, timeout=600, env=env)
                out_size = out_js.stat().st_size if out_js.exists() else None
                view8 = classify_view8(r.returncode, out_size)
                if view8 == "view8-ok":
                    c = subprocess.run([str(node), "--check", str(out_js)],
                                       capture_output=True, timeout=120, env=env)
                    check = classify_check(c.returncode)
            label = compose(dump, view8, check)
            labels[(artifact, build, rep)] = label
            receipts.append({"artifact": artifact, "build": build, "rep": rep,
                             "dump_rc": rc if isinstance(rc, str) else norm_rc(rc),
                             "dump_bytes": len(out), "view8_out_bytes": out_size,
                             "label": label})
    after = census(root)
    delta = compare_censuses(before, after)
    return emit(labels, receipts, False, args, closure, delta)


def emit(labels: dict, receipts: list, skip_run: bool, args, closure: dict,
         delta: dict) -> int:
    _, summary = verdict(labels)
    verified = bool(summary["verified"] and closure["ok"] and delta["equal"]) and not skip_run
    if not closure["ok"]:
        exit_code = 2
    elif verified:
        exit_code = 0
    else:
        exit_code = 1
    result = {"tool": TOOL, "predicate": PREDICATE, "skip_run": skip_run,
              "predicted": {f"{a}|{b}": v for (a, b), v in PREDICTED.items()},
              "closure": closure, "census": delta, "receipts": receipts,
              **summary, "verified": verified, "exit": exit_code}
    text = json.dumps(result, indent=1, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return exit_code


def selftest() -> int:
    cases = []

    def check(name, got, want):
        cases.append((name, got == want, got, want))

    dump_ok = b"Start SharedFunctionInfo\n0x1: [SharedFunctionInfo] in OldSpace\n"
    check("dump-ok", classify_dump(0, dump_ok), "dump-ok")
    check("dump-empty-rc0", classify_dump(0, b""), "dump-empty")
    check("dump-sigabrt", classify_dump(-6, b""), "dump-exit-134")
    check("dump-sigsegv", classify_dump(-11, b""), "dump-exit-139")
    check("dump-exit-1", classify_dump(1, dump_ok), "dump-exit-1")
    check("dump-timeout", classify_dump("timeout", b""), "dump-timeout")
    check("view8-ok", classify_view8(0, 213), "view8-ok")
    check("view8-empty", classify_view8(0, 0), "view8-empty")
    check("view8-exit", classify_view8(1, 213), "view8-exit-1")
    check("check-pass", classify_check(0), "node-pass")
    check("check-fail", classify_check(1), "node-fail")
    check("compose-full", compose("dump-ok", "view8-ok", "node-fail"),
          "dump-ok|view8-ok|node-fail")
    check("compose-skipped", compose("dump-exit-134", None, None),
          "dump-exit-134|view8-skipped|node-skipped")
    full = {(a, b, r): v for (a, b), v in PREDICTED.items() for r in range(1, REPS + 1)}
    check("verdict-all-match", verdict(full)[0], 0)
    check("verdict-do-nothing-exit", verdict({})[0], 1)
    check("verdict-do-nothing-count", verdict({})[1]["runs_matching"], 0)
    one_off = dict(full)
    one_off[("typora", "D2", 2)] = "dump-ok|view8-ok|node-pass"
    check("verdict-one-mismatch-exit", verdict(one_off)[0], 1)
    check("verdict-one-mismatch-count", verdict(one_off)[1]["runs_matching"], 17)
    fake_green = {k: "dump-ok|view8-ok|node-pass" for k in full}
    check("verdict-fake-green-count", verdict(fake_green)[1]["runs_matching"], 0)

    # closure map integrity: 64-hex digests, unique paths, non-empty
    check("closure-nonempty", len(CLOSURE) >= 20, True)
    check("closure-digests-hex",
          all(re.fullmatch(r"[0-9a-f]{64}", v) for v in CLOSURE.values()), True)
    check("closure-paths-relative", all(not k.startswith("/") for k in CLOSURE), True)

    import tempfile

    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR") or None) as scratch:
        s = Path(scratch)
        root = s / "toolchain"
        (root / "sub").mkdir(parents=True)
        (root / "a.bin").write_bytes(b"alpha")
        (root / "sub/b.bin").write_bytes(b"beta")
        c1 = census(root)
        check("census-paths", sorted(c1), ["a.bin", "sub/b.bin"])
        check("census-equal", compare_censuses(c1, dict(c1))["equal"], True)
        (root / "new.pyc").write_bytes(b"x")
        c2 = census(root)
        check("census-added", compare_censuses(c1, c2)["added"], ["new.pyc"])
        (root / "a.bin").write_bytes(b"ALPHA")
        c3 = census(root)
        check("census-changed", compare_censuses(c1, c3)["changed"], ["a.bin"])
        (root / "sub/b.bin").unlink()
        c4 = census(root)
        check("census-removed", compare_censuses(c1, c4)["removed"], ["sub/b.bin"])
        check("cache-detects-pyc", cache_entries(root) != [], True)
        (root / "new.pyc").unlink()
        check("cache-clean-after-unlink", cache_entries(root), [])
        (root / "sub/__pycache__").mkdir()
        check("cache-detects-dir", cache_entries(root), ["sub/__pycache__"])
        (root / "sub/__pycache__").rmdir()
        # census exclusion of git metadata
        (root / "jsc2js-src/.git").mkdir(parents=True)
        (root / "jsc2js-src/.git/index").write_bytes(b"git")
        c5 = census(root)
        check("census-excludes-git", any(".git" in k for k in c5), False)
        # closure refusal classes on an empty root
        empty = s / "empty"
        empty.mkdir()
        f = closure_findings(empty, empty / "probe", empty / "node", empty / "interp")
        check("closure-missing-count", len(f["missing"]), len(CLOSURE) + 3)
        check("closure-missing-ok", f["ok"], False)
        # a mismatched path names itself
        bad = s / "bad"
        bad.mkdir()
        for rel, want in list(CLOSURE.items())[:1]:
            p = bad / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"wrong")
        f2 = closure_findings(bad, bad / "probe", bad / "node", bad / "interp")
        check("closure-mismatch-names", f2["pin_mismatch"], [list(CLOSURE)[0]])

    failures = [c for c in cases if not c[1]]
    for name, ok, got, want in cases:
        print(f"{'PASS' if ok else 'FAIL'} {name} got={got!r} want={want!r}")
    print(f"SELFTEST {'CLEAN' if not failures else 'FAILED'} "
          f"cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--manifest", action="store_true",
                    help="closure check only (no run)")
    ap.add_argument("--census", metavar="OUT", help="write the toolchain census JSON")
    ap.add_argument("--compare", nargs=2, metavar=("A", "B"),
                    help="compare two census JSON files")
    ap.add_argument("--skip-run", action="store_true",
                    help="do-nothing control: every cell recorded as not-run")
    ap.add_argument("--toolchain-root", dest="toolchain_root", default=DEFAULT_ROOT)
    ap.add_argument("--probe")
    ap.add_argument("--python", default=DEFAULT_PYTHON)
    ap.add_argument("--node", default=NODE_PATH)
    ap.add_argument("--work", help="explicit scratch root for the run cells")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--out")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.compare:
        a = json.loads(Path(args.compare[0]).read_text())
        b = json.loads(Path(args.compare[1]).read_text())
        delta = compare_censuses(a, b)
        print(json.dumps(delta, indent=1, sort_keys=True))
        return 0 if delta["equal"] else 1
    if args.census:
        root = Path(args.toolchain_root)
        if not root.is_dir():
            print(f"{TOOL}: missing toolchain root {root}", file=sys.stderr)
            return 2
        data = census(root)
        Path(args.census).write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps({"entries": len(data), "out": args.census}))
        return 0
    if args.manifest:
        root = Path(args.toolchain_root)
        probe = Path(args.probe or (root / "inputs/atom.compiled.dist.jsc"))
        result = closure_findings(root, probe, Path(args.node),
                                  Path(args.python).resolve())
        print(json.dumps(result, indent=1, sort_keys=True))
        return 0 if result["ok"] else 2
    if args.skip_run:
        closure = {"entries": len(CLOSURE) + 3, "missing": [], "pin_mismatch": [],
                   "cache_present": [], "findings": [], "ok": True}
        return emit({}, [], True, args, closure, {"equal": True, "added": [],
                                                  "removed": [], "changed": []})
    required = ("probe", "work")
    missing = [k for k in required if not getattr(args, k)]
    if missing:
        ap.error("missing: " + ", ".join("--" + m.replace("_", "-") for m in missing))
    return run_matrix(args)


if __name__ == "__main__":
    sys.exit(main())
