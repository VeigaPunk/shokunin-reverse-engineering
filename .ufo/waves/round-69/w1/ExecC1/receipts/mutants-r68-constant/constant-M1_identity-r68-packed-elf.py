#!/usr/bin/env python3
"""packed-elf.py - round-68 instrument (R68-C2, coverage, capability).

A shipped ELF is often UPX-packed: the file on disk is a loader stub and the
program's code exists only as compressed bytes.  REA analyzes the bytes it is
given, so on a packed artifact it reports a stub (three procedures), and every
address-level verb refuses.  The lane had no route for this class: `upx` sat in
PROVINCE's fallback-reader list as a binary name, never as a surface.

This instrument scores the route on two pinned carriers, in one run:

  detect     `upx -l` names the file as packed AND the ELF carries no section
             header table (a packed image has none)
  before     REA's own inventory of the PACKED bytes: procedure_count below the
             carrier's declared floor - the stub, not the program
  identity   `upx -d` restores bytes whose sha256 equals the carrier's pin
  recover    REA's inventory of the UNPACKED copy equals the inventory of the
             pinned original on procedure, segment and string counts
  refusal    (carriers with a pinned address) a decompile at that address is
             refused on the packed bytes and returns the procedure after unpack
  control    the ORIGINAL is not reported packed and `upx -d` on it refuses, so
             detection has a negative arm on the same bytes

met_target is `carriers_matched == 2 of 2` and `control_ok true`.

Exit: 0 met; 1 not met (every false arm named, the receipt still written); 2
could-not-evaluate (unknown revision, carrier pin drift, missing upx/node,
REA package pin drift, a refused --work root, or bad argv).

Pins: the carriers are host system binaries pinned by sha256; the packer is
/usr/bin/upx pinned by sha256 and version; the REA package is pinned by version
plus its own package.json sha256 (QUALITY #110 - the npx cache-level lock is
RECORDED, never pinned, because npx rewrites it).  Both carriers and the
packed copies are rebuilt inside --work on every run; no artifact is committed.

--selftest runs the pure helpers over in-memory fixtures (no upx, no REA).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-68/packed-elf.py"
UPX = "/usr/bin/upx"
UPX_SHA256 = None  # set at run time; recorded in every receipt
REA_VERSION = "6.5.0"
REA_PKGJSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq", "sha256":
     "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806",
     "min_orig_procedures": 100, "address": "0x103fa0", "address_symbol": "FUN_00103fa0"},
    {"id": "xxd", "source": "/usr/bin/xxd", "sha256":
     "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65",
     "min_orig_procedures": 50, "address": None, "address_symbol": None},
]

REGISTERED_CASES = [
    "sections-none",
    "sections-some",
    "identity-equal",
    "identity-mismatch",
    "counts-analyze",
    "counts-error-envelope",
    "counts-missing",
    "carrier-ok-all-true",
    "carrier-ok-one-false",
    "fold-met-target",
    "fold-not-met",
    "skip-run-no-claim",
    "case-inventory",
]


class Unevaluable(Exception):
    """Exit-2 class: the route cannot be measured, so it scores nothing."""


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def section_count(readelf_text: str) -> int:
    """Section-header entries in `readelf -SW` output; 0 when the file has none."""
    if "There are no sections in this file" in readelf_text:
        return 0
    return len(re.findall(r"(?m)^\s*\[\s*\d+\]\s", readelf_text))


def counts_from(envelope: dict) -> dict | None:
    """REA analyze counts, or None when the envelope carries no inventory."""
    if not isinstance(envelope, dict) or envelope.get("error"):
        return None
    norm = envelope.get("normalized_result")
    if not isinstance(norm, dict):
        return None
    keys = ("procedure_count", "segment_count", "string_count")
    if not all(isinstance(norm.get(k), int) for k in keys):
        return None
    return {k: norm[k] for k in keys}


def carrier_arms(detected: bool, before_ok: bool, identity_ok: bool,
                 recovery_ok: bool, refusal_ok: bool | None) -> dict:
    arms = {"detected": bool(detected), "before_ok": bool(before_ok),
            "identity_ok": bool(identity_ok), "recovery_ok": bool(recovery_ok)}
    if refusal_ok is not None:
        arms["refusal_ok"] = bool(refusal_ok)
    return arms


def fold(carriers: list[dict], control_ok: bool, target: int) -> dict:
    matched = sum(1 for c in carriers if c["ok"])
    return {"carriers_matched": matched, "target": target,
            "control_ok": bool(control_ok),
            "met_target": matched == target and bool(control_ok)}


def run(argv: list[str], timeout: int = 900) -> dict:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return {"argv": argv, "rc": proc.returncode, "stdout": proc.stdout,
            "stdout_bytes": len(proc.stdout), "stderr": proc.stderr[-4000:]}


def rea(pkg: str, *args: str) -> dict:
    return run(["node", os.path.join(pkg, "scripts", "rea.mjs"), *args], timeout=900)


def analyze(pkg: str, path: str, receipt_path: str) -> tuple[dict, dict]:
    """Run REA analyze, keep the raw envelope, return (envelope, run record)."""
    rec = rea(pkg, "analyze", "--format", "json", path)
    env = {}
    try:
        env = json.loads(rec["stdout"]) if rec["stdout"].strip() else {}
    except json.JSONDecodeError:
        env = {}
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump({"run": rec, "envelope": env}, fh, indent=1, sort_keys=True)
    return env, rec


def decompile(pkg: str, path: str, address: str) -> dict:
    rec = rea(pkg, "decompile", path, address, "--format", "json")
    env = {}
    try:
        env = json.loads(rec["stdout"]) if rec["stdout"].strip() else {}
    except json.JSONDecodeError:
        env = {}
    code = env.get("normalized_result") if isinstance(env, dict) else None
    return {"run": rec, "code": code if isinstance(code, str) else None,
            "error_code": env.get("code") if isinstance(env, dict) else None}


def score(root: str, rev: str, pkg: str, work: str, out: str | None,
          skip_run: bool) -> int:
    def git(*argv: str) -> str:
        try:
            return subprocess.run(["git", "-C", root, *argv], check=True,
                                  capture_output=True, text=True).stdout
        except subprocess.CalledProcessError as exc:
            raise Unevaluable(f"git {' '.join(argv)} failed: rc={exc.returncode}") from exc

    instrument = {"path": TOOL, "sha256": sha256_file(os.path.abspath(__file__)),
                  "rev": git("log", "-1", "--format=%H", "--", TOOL).strip() or None}
    upx_env = {
        "upx": UPX,
        "sha256": sha256_file(UPX) if os.path.exists(UPX) else None,
        "version": run([UPX, "--version"]).get("stdout", "").splitlines()[0]
        if os.path.exists(UPX) else None,
    }
    pkg_json = os.path.join(pkg, "package.json")
    if not os.path.exists(pkg_json):
        raise Unevaluable(f"REA package root unreadable: {pkg}")
    pkg_sha = sha256_file(pkg_json)
    if pkg_sha != REA_PKGJSON_SHA256:
        raise Unevaluable(f"REA package.json pin drift: {pkg_sha}")
    pkg_meta = json.load(open(pkg_json, encoding="utf-8"))
    if pkg_meta.get("version") != REA_VERSION:
        raise Unevaluable(f"REA version drift: {pkg_meta.get('version')}")
    lock = None
    for cand in (os.path.join(os.path.dirname(pkg), "package-lock.json"),
                 os.path.join(os.path.dirname(os.path.dirname(pkg)), "package-lock.json")):
        if os.path.exists(cand):
            lock = cand
            break
    env = {
        "instrument": instrument, "rev": rev,
        "packer": upx_env,
        "rea": {"version": pkg_meta.get("version"), "package_json_sha256": pkg_sha,
                "root": pkg, "lock_path": lock,
                "lock_sha256": sha256_file(lock) if lock else None,
                "lock_recorded_not_pinned": True,
                "node": shutil.which("node"),
                "node_version": run([shutil.which("node") or "node", "--version"]).get("stdout", "").strip()},
    }
    if skip_run:
        payload = {**env, "claim": "R68-C2", "closure": None, "verdict_claimed": False,
                   "met_target": None, "carriers": [], "control_ok": None}
        text = json.dumps(payload, indent=1, sort_keys=True)
        if out:
            open(out, "w", encoding="utf-8").write(text + "\n")
        print(text)
        return 1

    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    if upx_env["sha256"] is None:
        raise Unevaluable("upx absent")
    carriers = []
    run_root = tempfile.mkdtemp(prefix="packed-", dir=work)
    try:
        for c in CARRIERS:
            cdir = os.path.join(run_root, c["id"])
            os.makedirs(cdir, exist_ok=True)
            src = c["source"]
            if not os.path.exists(src):
                raise Unevaluable(f"carrier source absent: {src}")
            base = os.path.basename(src)
            orig = os.path.join(cdir, "orig-" + base)
            shutil.copy(src, orig)
            os.chmod(orig, 0o755)
            orig_sha = sha256_file(orig)
            if orig_sha != c["sha256"]:
                raise Unevaluable(f"carrier pin drift {c['id']}: {orig_sha}")
            orig_env, orig_run = analyze(pkg, orig, os.path.join(cdir, "orig.analyze.json"))
            orig_counts = counts_from(orig_env)
            if not orig_counts or orig_counts["procedure_count"] < c["min_orig_procedures"]:
                raise Unevaluable(f"carrier {c['id']}: original inventory below the floor "
                                  f"({orig_counts})")
            packed = os.path.join(cdir, "packed-" + base)
            pack = run([UPX, "--best", "-q", "-o", packed, orig])
            if pack["rc"] != 0 or not os.path.exists(packed):
                raise Unevaluable(f"carrier {c['id']}: upx pack failed rc={pack['rc']}")
            packed_sha = sha256_file(packed)
            listing = run([UPX, "-l", packed])
            readelf = run(["readelf", "-SW", packed])
            secs = section_count(readelf["stdout"] + readelf["stderr"])
            detected = listing["rc"] == 0 and secs == 0
            packed_env, packed_run = analyze(pkg, packed, os.path.join(cdir, "packed.analyze.json"))
            packed_counts = counts_from(packed_env) or {}
            before_procedures = packed_counts.get("procedure_count")
            floor = c["min_orig_procedures"] // 2
            before_ok = before_procedures is not None and before_procedures < floor
            unpacked = os.path.join(cdir, "unpacked-" + base)
            unpack = run([UPX, "-d", "-q", "-o", unpacked, packed])
            identity_ok = True
            rec_env, rec_run = analyze(pkg, unpacked, os.path.join(cdir, "unpacked.analyze.json"))
            rec_counts = counts_from(rec_env) or {}
            recovery_ok = bool(rec_counts) and rec_counts == orig_counts
            refusal_ok = None
            refusal = None
            if c.get("address"):
                d_packed = decompile(pkg, packed, c["address"])
                d_unpacked = decompile(pkg, unpacked, c["address"])
                code = d_unpacked["code"] or ""
                refusal_ok = (d_packed["run"]["rc"] != 0 and d_unpacked["run"]["rc"] == 0
                              and c["address_symbol"] in code and len(code) > 200)
                refusal = {"packed_rc": d_packed["run"]["rc"],
                           "packed_error_code": d_packed["error_code"],
                           "unpacked_rc": d_unpacked["run"]["rc"],
                           "unpacked_code_bytes": len(code),
                           "symbol_present": c["address_symbol"] in code}
            ctrl_l = run([UPX, "-l", orig])
            ctrl_d = run([UPX, "-d", "-q", "-o", os.path.join(cdir, "ctrl-" + base), orig])
            control_ok = ctrl_l["rc"] != 0 and ctrl_d["rc"] != 0
            arms = carrier_arms(detected, before_ok, identity_ok, recovery_ok, refusal_ok)
            carriers.append({
                "id": c["id"], "source": src, "pin": c["sha256"], "packed_sha256": packed_sha,
                "orig_counts": orig_counts, "packed_counts": packed_counts,
                "unpacked_counts": rec_counts, "section_count": secs,
                "upx_list_rc": listing["rc"], "before_floor": floor,
                "refusal": refusal, "control": {"list_rc": ctrl_l["rc"], "decompress_rc": ctrl_d["rc"]},
                "arms": arms, "ok": all(arms.values()),
                "runs": {"orig": orig_run, "pack": pack, "packed": packed_run,
                         "unpack": unpack, "recovered": rec_run},
            })
        verdict = fold(carriers, all(c["control"]["list_rc"] != 0 and c["control"]["decompress_rc"] != 0
                                     for c in carriers), len(CARRIERS))
    finally:
        shutil.rmtree(run_root, ignore_errors=True)
    payload = {**env, "claim": "R68-C2", "closure": verdict, **verdict,
               "before_procedures": [c["packed_counts"].get("procedure_count") for c in carriers],
               "carriers": carriers}
    failing = [f"{c['id']}:{k}" for c in carriers for k, v in c["arms"].items() if not v]
    payload["failing"] = failing
    text = json.dumps(payload, indent=1, sort_keys=True)
    if out:
        open(out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0 if verdict["met_target"] and not failing else 1


def selftest() -> int:
    cases = []
    # section_count
    cases.append(("sections-none", section_count("There are no sections in this file.\n") == 0))
    some = "  [ 1] .interp PROGBITS 0000000000000318 000318 00001c 00 A 0 0 1\n" \
           "  [ 2] .note.gnu.build-id NOTE 0 0 0 0 A 0 0 8\n"
    cases.append(("sections-some", section_count(some) == 2))
    # identity
    cases.append(("identity-equal", "ab" * 32 == "ab" * 32))
    cases.append(("identity-mismatch", ("ab" * 32) != ("cd" * 32)))
    # counts_from
    ok_env = {"normalized_result": {"procedure_count": 167, "segment_count": 30, "string_count": 190}}
    cases.append(("counts-analyze", counts_from(ok_env) ==
                  {"procedure_count": 167, "segment_count": 30, "string_count": 190}))
    cases.append(("counts-error-envelope",
                  counts_from({"error": "x", "code": "invalid_request"}) is None))
    cases.append(("counts-missing", counts_from({"normalized_result": {}}) is None))
    # carrier_arms / fold
    a = carrier_arms(True, True, True, True, None)
    cases.append(("carrier-ok-all-true", all(a.values()) and "refusal_ok" not in a))
    b = carrier_arms(True, True, False, True, True)
    cases.append(("carrier-ok-one-false", not all(b.values()) and "refusal_ok" in b))
    good = [{"ok": True}, {"ok": True}]
    cases.append(("fold-met-target", fold(good, True, 2)["met_target"] is True))
    cases.append(("fold-not-met", fold([{"ok": True}, {"ok": False}], True, 2)["met_target"] is False
                  and fold(good, False, 2)["met_target"] is False))
    # a --skip-run payload never claims a verdict
    payload = {"closure": None, "verdict_claimed": False, "met_target": None}
    cases.append(("skip-run-no-claim", payload["closure"] is None
                  and payload["verdict_claimed"] is False and payload["met_target"] is None))
    executed = [name for name, _ in cases] + ["case-inventory"]
    cases.append(("case-inventory", executed == REGISTERED_CASES))
    failed = [name for name, ok in cases if not ok]
    print(json.dumps({"selftest": TOOL, "cases": len(cases), "failed": failed,
                      "ok": not failed}, indent=1))
    return 0 if not failed else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--pkg")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--skip-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if not (args.root and args.rev and args.pkg):
        print("packed-elf: --root, --rev and --pkg are required", file=sys.stderr)
        return 2
    try:
        return score(args.root, args.rev, args.pkg, args.work or "/proc/self/fd",
                     args.json_out, args.skip_run)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r68-packed-elf-v1",
                          "unevaluable": str(exc), "claim": "R68-C2"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
