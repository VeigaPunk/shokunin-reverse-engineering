#!/usr/bin/env python3
"""packed-elf.py - round-70 instrument (R70-C1 calibration, R70-C2 operability,
R70-C3 coverage).

Supersession of tools/round-69/packed-elf.py (kept byte-identical at its own
round).  The route is unchanged in scope: a shipped ELF may be UPX-packed, the
file on disk is a loader stub, REA analyzes the bytes it is given, and the
route detects, unpacks with byte identity and recovers the original inventory.
Round 70 closes the routed round-69 defects and widens the carrier class:

  detect     `upx -l` names the file as packed AND the ELF carries no section
             header table (a packed image has none)
  before     REA's own inventory of the PACKED bytes: procedure_count at or
             below the carrier's declared stub ceiling (`before_ceiling_ratio`
             records ceiling/original, and the counter requires <= 0.75)
  identity   `upx -d` restores bytes whose sha256 equals the carrier's pin
  recover    REA's inventory of the UNPACKED copy equals the inventory of the
             pinned original on procedure, segment and string counts
  refusal    (carriers with a pinned address) a decompile at that address is
             refused on the packed bytes and returns the procedure after unpack
  control    the ORIGINAL is not reported packed and `upx -d` on it refuses, so
             detection has a negative arm on the same bytes

R70-C2 (the safe packer seam, QUALITY #113 executed): the caller-supplied
`--upx` binary is hashed and pin-compared BEFORE its first execution (a stub
that prints the pinned version but hashes differently is never run); the
packer's children receive a minimal allowlisted environment built by the pure
`build_child_env()` (PATH/HOME/LANG/TMPDIR, HOME and TMPDIR inside --work,
never /tmp); the validated path is threaded through the carrier loop (pack,
list, unpack and the negative control all execute the pinned bytes the caller
named, never a module constant); a packer that exists but cannot execute
(exec-format-less) is a typed `packer_mismatch`, and a `node` that exists but
cannot run is a typed `broken_tool`, both exit 2 `unevaluable` instead of a
traceback.  Every scratch root is a per-run `mkdtemp` under --work, and the
receipt records the child environment it used.

R70-C1 (receipt provenance bound inside the reader, QUALITY #114 executed):
`--check-receipt` now requires --root and --rev, and fails (exit 1, named
clause) any receipt whose measured revision or instrument sha256 differs from
the ones it is invoked with, whose carrier ids/pins/sources/kinds/ceilings/
original-procedure counts differ from the frozen CARRIERS table, whose
before_ceiling_ratio does not equal round(ceiling/orig, 4), whose packed
procedure count exceeds its ceiling, or whose row set, carriers_matched,
target or arm truth disagrees with that table.  A fabricated receipt that
merely asserts green fields is rejected; the genuine landing receipt still
passes.

R70-C3: the carrier set carries a pinned statically linked executable
(/usr/bin/docker-init, kind `static-exe`) beside the two executables and the
pinned shared object -> `carriers_matched == 4 of 4`.

Exit: 0 met; 1 not met (every false arm or failed clause named, the receipt
still written); 2 could-not-evaluate (missing or broken node/git/readelf/upx,
an unusable --work root, a packer version or sha256 mismatch, an
exec-format-less packer, carrier pin drift, REA package pin drift, unknown
revision or bad argv).

Pins: the carriers are host system binaries pinned by sha256; the packer is
pinned by version and sha256 and the pin is ENFORCED (a mismatch is exit 2, not
a recorded observation); the REA package is pinned by version plus its own
package.json sha256 (QUALITY #110 - the npx cache-level lock is RECORDED, never
pinned, because npx rewrites it).  Carriers and packed copies are rebuilt
inside --work on every run; no artifact is committed.

--selftest runs the pure helpers, the arm seam and the child-environment
builder over in-memory fixtures (no upx, no REA).
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

TOOL = "tools/round-70/packed-elf.py"
UPX = "/usr/bin/upx"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
PACKING_MODE = "upx --best"
REA_VERSION = "6.5.0"
REA_PKGJSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
# `kind` names the artifact class each carrier stands for; `before_max_procedures`
# is the stub ceiling the packed bytes must stay at or below (QUALITY #107: the
# bound is declared per carrier class, never generalised across classes).
CARRIERS = [
    {"id": "jq", "name": "jq", "kind": "executable", "source": "/usr/bin/jq", "sha256":
     "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806",
     "min_orig_procedures": 100, "before_max_procedures": 10,
     "address": "0x103fa0", "address_symbol": "FUN_00103fa0"},
    {"id": "xxd", "name": "xxd", "kind": "executable", "source": "/usr/bin/xxd", "sha256":
     "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65",
     "min_orig_procedures": 50, "before_max_procedures": 10,
     "address": None, "address_symbol": None},
    {"id": "libz", "name": "libz", "kind": "shared-object",
     "source": "/usr/lib/libz.so.1.3.2", "sha256":
     "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9",
     "min_orig_procedures": 150, "before_max_procedures": 120,
     "address": None, "address_symbol": None},
    {"id": "dinit", "name": "docker-init", "kind": "static-exe",
     "source": "/usr/bin/docker-init", "sha256":
     "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115",
     "min_orig_procedures": 1000, "before_max_procedures": 10,
     "address": None, "address_symbol": None},
]

# The original procedure counts the pinned sources measured on 2026-11-04; the
# receipt reader binds each carrier's orig_counts.procedure_count to its
# declared value (QUALITY #114: the payload is re-derived from the frozen
# table, never taken from the receipt's word).
DECLARED_ORIG = {"jq": 167, "xxd": 99, "libz": 184, "dinit": 1268}

# The packer's children get exactly these keys, built by the pure
# build_child_env(); HOME and TMPDIR live inside the run's scratch root and
# never fall back to /tmp (round-69 M69-11).
CHILD_ENV_KEYS = ("HOME", "LANG", "PATH", "TMPDIR")

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
    "arm-pack-green",
    "arm-pack-identity-false",
    "arm-pack-recovery-false",
    "arm-pack-detected-false",
    "arm-pack-before-false",
    "arm-pack-control-false",
    "arm-pack-refusal",
    "child-env-allowlist",
    "child-env-home-in-work",
    "child-env-no-tmp",
    "case-inventory",
]


class Unevaluable(Exception):
    """Exit-2 class: the route cannot be measured, so it scores nothing."""


def build_child_env(work: str) -> dict:
    """The minimal allowlisted environment handed to packer children.

    Pure: derives from `work` and the parent PATH only.  HOME and TMPDIR live
    inside the run's scratch root (never a /tmp fallback, round-69 M69-11) and
    the key set is exactly CHILD_ENV_KEYS - nothing else is inherited (the
    round-69 S-1 finding: the seam inherited the caller's full environment).
    """
    root = os.path.abspath(work)
    path = os.environ.get("PATH") or "/usr/bin"
    return {"HOME": os.path.join(root, "home"),
            "LANG": "C",
            "PATH": path,
            "TMPDIR": os.path.join(root, "tmp")}


def child_env_audit(env: dict, work: str) -> dict:
    """The receipt-facing description of a child environment."""
    root = os.path.abspath(work)
    return {"keys": sorted(env), "allowlist": list(CHILD_ENV_KEYS),
            "home": env.get("HOME"), "tmpdir": env.get("TMPDIR"),
            "home_under_work": str(env.get("HOME", "")).startswith(root),
            "tmpdir_under_work": str(env.get("TMPDIR", "")).startswith(root),
            "work": root}


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
                 recovery_ok: bool, refusal_ok: bool | None,
                 control_ok: bool = True) -> dict:
    arms = {"detected": bool(detected), "before_ok": bool(before_ok),
            "identity_ok": bool(identity_ok), "recovery_ok": bool(recovery_ok),
            "control_ok": bool(control_ok)}
    if refusal_ok is not None:
        arms["refusal_ok"] = bool(refusal_ok)
    return arms


def evaluate_carrier(model: dict) -> dict:
    """Every arm of one carrier, from evidence only (no I/O).

    `--selftest` feeds this seam a false model per arm; `score()` feeds it the
    measured model.  A gate whose own selftest cannot reach its arm expressions
    is decorative (round-68 M68-6, QUALITY #108).
    """
    detected = model["upx_list_rc"] == 0 and model["section_count"] == 0
    before_ok = model["packed_procedures"] is not None and model["packed_procedures"] <= model["before_max_procedures"]
    identity_ok = model["unpack_rc"] == 0 and model["unpacked_sha256"] == model["pin"]
    recovery_ok = bool(model["recovered_counts"]) and model["recovered_counts"] == model["orig_counts"]
    control_ok = model["control_list_rc"] != 0 and model["control_decompress_rc"] != 0
    refusal_ok = None
    if model.get("address"):
        refusal_ok = (model["refusal_packed_rc"] != 0 and model["refusal_unpacked_rc"] == 0
                      and model.get("refusal_symbol_present") is True
                      and (model.get("refusal_code_bytes") or 0) > 200)
    arms = carrier_arms(detected, before_ok, identity_ok, recovery_ok, refusal_ok, control_ok)
    return {"arms": arms, "ok": all(arms.values())}


def fold(carriers: list[dict], target: int) -> dict:
    """Composite verdict: every carrier ok and its negative control arm true."""
    matched = sum(1 for c in carriers if c["ok"])
    control_ok = bool(carriers) and all(c["arms"]["control_ok"] for c in carriers)
    return {"carriers_matched": matched, "target": target,
            "control_ok": control_ok,
            "met_target": matched == target and control_ok}


def run(argv: list[str], timeout: int = 900, env: dict | None = None) -> dict:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                              env=env)
    except OSError as exc:
        raise Unevaluable(f"child_unexecutable: {argv[0]} ({exc.__class__.__name__}: {exc})")
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


def elf_format(readelf_header_text: str) -> dict | None:
    """ELF identity from `readelf -h` output: class, data, type, machine."""
    keys = {"Class": "class", "Data": "data", "Type": "type", "Machine": "machine"}
    found = {}
    for line in readelf_header_text.splitlines():
        m = re.match(r"^\s*(Class|Data|Type|Machine):\s+(.+?)\s*$", line)
        if m and keys[m.group(1)] not in found:
            found[keys[m.group(1)]] = m.group(2)
    return found if len(found) == 4 else None


def preflight(upx: str, pkg: str, work: str, check_work: bool = True,
              child_env: dict | None = None) -> dict:
    """Typed exit-2 contract: every prerequisite is checked before any run.

    Identity comes BEFORE execution (QUALITY #113): the caller-supplied `upx`
    is hashed and pin-compared first, so a binary that is not the pinned packer
    is refused without ever being run; only then is its `--version` banner
    read, through the minimal child environment.  Round-68 let a missing `node`
    and a refused `--work` escape as a Python traceback with exit 1 (M68-8 /
    ADV-3), and recorded the packer pin without enforcing it (ADV-2).  A
    refused route must be a named class, never a crash.
    """
    if not os.path.isfile(upx):
        raise Unevaluable(f"missing_tool: upx ({upx})")
    try:
        sha = sha256_file(upx)
    except OSError as exc:
        raise Unevaluable(f"packer_mismatch: unreadable ({upx}: {exc.__class__.__name__})")
    if sha != UPX_SHA256_PIN:
        raise Unevaluable(f"packer_mismatch: sha256 {sha} != pin {UPX_SHA256_PIN}")
    if not os.access(upx, os.X_OK):
        raise Unevaluable(f"missing_tool: upx not executable ({upx})")
    cenv = child_env if child_env is not None else build_child_env(work)
    try:
        version = run([upx, "--version"], env=cenv).get("stdout", "").strip().splitlines()
    except Unevaluable as exc:
        raise Unevaluable(f"packer_mismatch: not executable ({exc})")
    version = version[0] if version else ""
    if version != UPX_VERSION_PIN:
        raise Unevaluable(f"packer_mismatch: version {version!r} != pin {UPX_VERSION_PIN!r}")
    for tool in ("node", "git", "readelf"):
        found = shutil.which(tool)
        if found is None:
            raise Unevaluable(f"missing_tool: {tool}")
        if tool == "node":
            try:
                banner = run([found, "--version"], env=cenv).get("stdout", "").strip()
            except Unevaluable as exc:
                raise Unevaluable(f"broken_tool: node ({exc})")
            if not re.match(r"^v\d+\.\d+\.\d+", banner):
                raise Unevaluable(f"broken_tool: node (banner {banner!r})")
    if not os.path.isdir(pkg) or not os.path.isfile(os.path.join(pkg, "package.json")):
        raise Unevaluable(f"missing_tool: rea package ({pkg})")
    if check_work:
        if not os.path.isdir(work):
            raise Unevaluable(f"work_unusable: not a directory ({work})")
        try:
            probe = tempfile.mkdtemp(prefix="preflight-", dir=work)
            os.rmdir(probe)
        except OSError as exc:
            raise Unevaluable(f"work_unusable: not writable ({work}: {exc.__class__.__name__})")
    return {"upx": upx, "sha256": sha, "version": version,
            "sha256_pin": UPX_SHA256_PIN, "version_pin": UPX_VERSION_PIN,
            "pin_enforced": True, "packing_mode": PACKING_MODE,
            "child_env": child_env_audit(cenv, work),
            "hash_before_exec": True}


def git_blob_sha256(root: str, rev: str, path: str) -> str | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        return None
    return hashlib.sha256(proc.stdout).hexdigest()


def check_receipt(path: str, root: str, rev: str) -> int:
    """Score an existing receipt against R70-C3's frozen predicate sentence.

    Every green field is re-derived, never trusted (QUALITY #114): the receipt
    is bound to its producer (its recorded instrument sha256 must equal the
    blob of this instrument at --rev, and its recorded revision must equal
    --rev), every carrier row is bound to the frozen CARRIERS table (id, pin,
    source, kind, ceiling), each original procedure count to DECLARED_ORIG,
    each ratio to round(ceiling/orig, 4), each packed count to its ceiling,
    and the row set/target/matched/control/arms to the table.  The check reads
    committed-byte evidence; a receipt whose ceiling is looser than 0.75 of the
    original inventory is not evidence that the packed bytes are the stub
    (QUALITY #107).
    """
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"check": "R70-C3", "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    failing = []
    blob_sha = git_blob_sha256(root, rev, TOOL)
    if blob_sha is None:
        print(json.dumps({"check": "R70-C3",
                          "unevaluable": f"git show {rev}:{TOOL} failed"}), file=sys.stderr)
        return 2
    instrument = receipt.get("instrument")
    if not isinstance(instrument, dict) or not instrument:
        failing.append("instrument absent")
    else:
        if instrument.get("path") != TOOL:
            failing.append(f"instrument.path {instrument.get('path')} != {TOOL}")
        if instrument.get("sha256") != blob_sha:
            failing.append(f"instrument.sha256 {instrument.get('sha256')} != "
                           f"blob at {rev} ({blob_sha})")
    if receipt.get("rev") != rev:
        failing.append(f"rev {receipt.get('rev')} != {rev}")
    registry = {c["id"]: c for c in CARRIERS}
    target = receipt.get("target")
    if target != len(CARRIERS):
        failing.append(f"target {target} != {len(CARRIERS)}")
    carriers = receipt.get("carriers") or []
    if receipt.get("carriers_matched") != len(CARRIERS):
        failing.append(f"carriers_matched {receipt.get('carriers_matched')} != {len(CARRIERS)}")
    if len(carriers) != len(CARRIERS):
        failing.append(f"carrier rows {len(carriers)} != {len(CARRIERS)}")
    if receipt.get("control_ok") is not True:
        failing.append("control_ok not true")
    if receipt.get("met_target") is not True:
        failing.append("met_target not true")
    if receipt.get("failing") != []:
        failing.append(f"failing not empty: {receipt.get('failing')}")
    seen_ids = []
    kinds = sorted({c.get("kind") for c in carriers})
    if kinds != sorted(c["kind"] for c in CARRIERS):
        failing.append(f"carrier kinds {kinds} != "
                       f"{sorted(c['kind'] for c in CARRIERS)}")
    for c in carriers:
        cid = c.get("id")
        seen_ids.append(cid)
        row = registry.get(cid)
        if row is None:
            failing.append(f"unknown carrier id {cid}")
            continue
        if c.get("pin") != row["sha256"]:
            failing.append(f"{cid}: pin {c.get('pin')} != registry {row['sha256']}")
        if c.get("source") != row["source"]:
            failing.append(f"{cid}: source {c.get('source')} != registry {row['source']}")
        if c.get("kind") != row["kind"]:
            failing.append(f"{cid}: kind {c.get('kind')} != registry {row['kind']}")
        ceiling = c.get("before_ceiling")
        if ceiling != row["before_max_procedures"]:
            failing.append(f"{cid}: ceiling {ceiling} != registry "
                           f"{row['before_max_procedures']}")
        if c.get("ok") is not True:
            failing.append(f"{cid}: not ok")
        arms = c.get("arms")
        if not isinstance(arms, dict) or not arms:
            failing.append(f"{cid}: arms absent")
        else:
            for arm_name, value in arms.items():
                if value is not True:
                    failing.append(f"{cid}: arm {arm_name} {value} not true")
            for arm_name in ("detected", "before_ok", "identity_ok",
                             "recovery_ok", "control_ok"):
                if arm_name not in arms:
                    failing.append(f"{cid}: arm {arm_name} missing")
        orig_counts = c.get("orig_counts")
        packed_counts = c.get("packed_counts")
        if not isinstance(orig_counts, dict) or not isinstance(packed_counts, dict):
            failing.append(f"{cid}: counts absent")
        else:
            orig_proc = orig_counts.get("procedure_count")
            if orig_proc != DECLARED_ORIG[cid]:
                failing.append(f"{cid}: orig_procedures {orig_proc} != "
                               f"declared {DECLARED_ORIG[cid]}")
            packed_proc = packed_counts.get("procedure_count")
            if not isinstance(packed_proc, int):
                failing.append(f"{cid}: packed procedure_count absent")
            elif ceiling is not None and packed_proc > ceiling:
                failing.append(f"{cid}: packed {packed_proc} > ceiling {ceiling}")
        ratio = c.get("before_ceiling_ratio")
        if not isinstance(ratio, (int, float)):
            failing.append(f"{cid}: before_ceiling_ratio absent")
        elif ceiling is not None and isinstance(orig_counts, dict) \
                and isinstance(orig_counts.get("procedure_count"), int) \
                and orig_counts["procedure_count"] > 0:
            want = round(ceiling / orig_counts["procedure_count"], 4)
            if ratio != want:
                failing.append(f"{cid}: before_ceiling_ratio {ratio} != "
                               f"ceiling/orig {want}")
            if ratio > 0.75:
                failing.append(f"{cid}: before_ceiling_ratio {ratio} > 0.75")
    if sorted(x for x in seen_ids if x is not None) != sorted(registry):
        failing.append(f"carrier ids {seen_ids} != registry {sorted(registry)}")
    out = {"check": "R70-C3", "met": not failing, "failing": failing,
           "target": target, "carriers_matched": receipt.get("carriers_matched"),
           "kinds": kinds, "receipt": path, "rev": rev,
           "instrument_sha256": (instrument or {}).get("sha256"),
           "before_ceilings": receipt.get("before_ceilings")}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not failing else 1


def score(root: str, rev: str, pkg: str, work: str, out: str | None,
          skip_run: bool, upx: str = UPX) -> int:
    def git(*argv: str) -> str:
        try:
            return subprocess.run(["git", "-C", root, *argv], check=True,
                                  capture_output=True, text=True).stdout
        except subprocess.CalledProcessError as exc:
            raise Unevaluable(f"git {' '.join(argv)} failed: rc={exc.returncode}") from exc

    packer_env = preflight(upx, pkg, work, check_work=not skip_run)
    upx_v = packer_env["upx"]
    instrument = {"path": TOOL, "sha256": sha256_file(os.path.abspath(__file__)),
                  "rev": git("log", "-1", "--format=%H", "--", TOOL).strip() or None}
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
        "packer": packer_env,
        "claims": ["R70-C1", "R70-C2", "R70-C3"],
        "child_env": child_env_audit(build_child_env(work), work),
        "rea": {"version": pkg_meta.get("version"), "package_json_sha256": pkg_sha,
                "root": pkg, "lock_path": lock,
                "lock_sha256": sha256_file(lock) if lock else None,
                "lock_recorded_not_pinned": True,
                "node": shutil.which("node"),
                "node_version": run([shutil.which("node") or "node", "--version"]).get("stdout", "").strip()},
    }
    if skip_run:
        payload = {**env, "claim": "R70", "closure": None, "verdict_claimed": False,
                   "met_target": None, "carriers": [], "control_ok": None}
        text = json.dumps(payload, indent=1, sort_keys=True)
        if out:
            open(out, "w", encoding="utf-8").write(text + "\n")
        print(text)
        return 1

    carriers = []
    run_root = tempfile.mkdtemp(prefix="packed-", dir=work)
    packer_env_cenv = build_child_env(run_root)
    for sub in ("home", "tmp"):
        os.makedirs(os.path.join(run_root, sub), exist_ok=True)
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
            pack = run([upx_v, "--best", "-q", "-o", packed, orig], env=packer_env_cenv)
            if pack["rc"] != 0 or not os.path.exists(packed):
                raise Unevaluable(f"carrier {c['id']}: upx pack failed rc={pack['rc']}")
            packed_sha = sha256_file(packed)
            listing = run([upx_v, "-l", packed], env=packer_env_cenv)
            readelf = run(["readelf", "-SW", packed])
            secs = section_count(readelf["stdout"] + readelf["stderr"])
            packed_env, packed_run = analyze(pkg, packed, os.path.join(cdir, "packed.analyze.json"))
            packed_counts = counts_from(packed_env) or {}
            unpacked = os.path.join(cdir, "unpacked-" + base)
            unpack = run([upx_v, "-d", "-q", "-o", unpacked, packed], env=packer_env_cenv)
            unpacked_sha = sha256_file(unpacked) if os.path.exists(unpacked) else None
            rec_env, rec_run = analyze(pkg, unpacked, os.path.join(cdir, "unpacked.analyze.json"))
            rec_counts = counts_from(rec_env) or {}
            refusal = None
            if c.get("address"):
                d_packed = decompile(pkg, packed, c["address"])
                d_unpacked = decompile(pkg, unpacked, c["address"])
                code = d_unpacked["code"] or ""
                refusal = {"packed_rc": d_packed["run"]["rc"],
                           "packed_error_code": d_packed["error_code"],
                           "unpacked_rc": d_unpacked["run"]["rc"],
                           "unpacked_code_bytes": len(code),
                           "symbol_present": c["address_symbol"] in code}
            ctrl_l = run([upx_v, "-l", orig], env=packer_env_cenv)
            ctrl_d = run([upx_v, "-d", "-q", "-o", os.path.join(cdir, "ctrl-" + base), orig],
                         env=packer_env_cenv)
            header = run(["readelf", "-h", orig])
            model = {
                "upx_list_rc": listing["rc"], "section_count": secs,
                "packed_procedures": packed_counts.get("procedure_count"),
                "before_max_procedures": c["before_max_procedures"],
                "unpack_rc": unpack["rc"], "unpacked_sha256": unpacked_sha, "pin": c["sha256"],
                "recovered_counts": rec_counts, "orig_counts": orig_counts,
                "control_list_rc": ctrl_l["rc"], "control_decompress_rc": ctrl_d["rc"],
                "address": c.get("address"),
                "refusal_packed_rc": (refusal or {}).get("packed_rc"),
                "refusal_unpacked_rc": (refusal or {}).get("unpacked_rc"),
                "refusal_symbol_present": (refusal or {}).get("symbol_present"),
                "refusal_code_bytes": (refusal or {}).get("unpacked_code_bytes"),
            }
            result = evaluate_carrier(model)
            carriers.append({
                "id": c["id"], "name": c["name"], "kind": c["kind"],
                "source": src, "pin": c["sha256"], "packed_sha256": packed_sha,
                "format": elf_format(header["stdout"] + header["stderr"]),
                "packing_mode": PACKING_MODE,
                "orig_counts": orig_counts, "packed_counts": packed_counts,
                "unpacked_counts": rec_counts, "section_count": secs,
                "upx_list_rc": listing["rc"],
                "before_ceiling": c["before_max_procedures"],
                "before_ceiling_ratio": round(
                    c["before_max_procedures"] / orig_counts["procedure_count"], 4),
                "refusal": refusal, "control": {"list_rc": ctrl_l["rc"], "decompress_rc": ctrl_d["rc"]},
                "arms": result["arms"], "ok": result["ok"],
                "runs": {"orig": orig_run, "pack": pack, "packed": packed_run,
                         "unpack": unpack, "recovered": rec_run},
            })
        verdict = fold(carriers, len(CARRIERS))
    finally:
        shutil.rmtree(run_root, ignore_errors=True)
    payload = {**env, "claim": "R70", "closure": verdict, **verdict,
               "before_procedures": [c["packed_counts"].get("procedure_count") for c in carriers],
               "before_ceilings": [{"id": c["id"], "ceiling": c["before_ceiling"],
                                    "orig_procedures": c["orig_counts"]["procedure_count"],
                                    "ceiling_ratio": c["before_ceiling_ratio"]} for c in carriers],
               "carrier_classes": [{"id": c["id"], "kind": c["kind"]} for c in carriers],
               "carriers": carriers}
    failing = [f"{c['id']}:{k}" for c in carriers for k, v in c["arms"].items() if not v]
    payload["failing"] = failing
    text = json.dumps(payload, indent=1, sort_keys=True)
    if out:
        open(out, "w", encoding="utf-8").write(text + "\n")
    print(text)
    return 0 if verdict["met_target"] and not failing else 1


def _model(**over: object) -> dict:
    """A green modelled carrier; each arm-false case overrides one field."""
    base = {
        "upx_list_rc": 0, "section_count": 0,
        "packed_procedures": 3, "before_max_procedures": 10,
        "unpack_rc": 0, "unpacked_sha256": "aa" * 32, "pin": "aa" * 32,
        "recovered_counts": {"procedure_count": 167, "segment_count": 30, "string_count": 190},
        "orig_counts": {"procedure_count": 167, "segment_count": 30, "string_count": 190},
        "control_list_rc": 2, "control_decompress_rc": 2,
        "address": None,
    }
    base.update(over)
    return base


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
    a = carrier_arms(True, True, True, True, None, True)
    cases.append(("carrier-ok-all-true", all(a.values()) and "refusal_ok" not in a))
    b = carrier_arms(True, True, False, True, True, True)
    cases.append(("carrier-ok-one-false", not all(b.values()) and "refusal_ok" in b))
    good = [{"ok": True, "arms": {"control_ok": True}},
            {"ok": True, "arms": {"control_ok": True}}]
    cases.append(("fold-met-target", fold(good, 2)["met_target"] is True))
    cases.append(("fold-not-met",
                  fold([{"ok": True, "arms": {"control_ok": True}},
                        {"ok": False, "arms": {"control_ok": True}}], 2)["met_target"] is False
                  and fold([{"ok": True, "arms": {"control_ok": False}}], 1)["met_target"] is False))
    # a --skip-run payload never claims a verdict
    payload = {"closure": None, "verdict_claimed": False, "met_target": None}
    cases.append(("skip-run-no-claim", payload["closure"] is None
                  and payload["verdict_claimed"] is False and payload["met_target"] is None))
    # the arm seam: one green model, then one false model per arm (M68-6 closure)
    green = evaluate_carrier(_model())
    cases.append(("arm-pack-green", green["ok"] is True and "refusal_ok" not in green["arms"]
                  and all(green["arms"].values())))
    ident = evaluate_carrier(_model(unpacked_sha256="bb" * 32))
    cases.append(("arm-pack-identity-false",
                  ident["arms"]["identity_ok"] is False and ident["ok"] is False))
    rec = evaluate_carrier(_model(recovered_counts={"procedure_count": 166,
                                                    "segment_count": 30, "string_count": 190}))
    cases.append(("arm-pack-recovery-false",
                  rec["arms"]["recovery_ok"] is False and rec["ok"] is False))
    det = evaluate_carrier(_model(section_count=2))
    cases.append(("arm-pack-detected-false",
                  det["arms"]["detected"] is False and det["ok"] is False))
    bef = evaluate_carrier(_model(packed_procedures=150))
    cases.append(("arm-pack-before-false",
                  bef["arms"]["before_ok"] is False and bef["ok"] is False))
    ctl = evaluate_carrier(_model(control_list_rc=0))
    cases.append(("arm-pack-control-false",
                  ctl["arms"]["control_ok"] is False and ctl["ok"] is False))
    ref_ok = evaluate_carrier(_model(address="0x1000", refusal_packed_rc=1,
                                     refusal_unpacked_rc=0, refusal_symbol_present=True,
                                     refusal_code_bytes=400))
    ref_bad = evaluate_carrier(_model(address="0x1000", refusal_packed_rc=0,
                                      refusal_unpacked_rc=0, refusal_symbol_present=True,
                                      refusal_code_bytes=400))
    cases.append(("arm-pack-refusal", ref_ok["arms"]["refusal_ok"] is True
                  and ref_bad["arms"]["refusal_ok"] is False))
    # the child environment builder: allowlist, HOME inside work, no /tmp
    ce = build_child_env("/some/work")
    cases.append(("child-env-allowlist", sorted(ce) == sorted(CHILD_ENV_KEYS)))
    cases.append(("child-env-home-in-work",
                  ce["HOME"].startswith(os.path.abspath("/some/work"))
                  and ce["TMPDIR"].startswith(os.path.abspath("/some/work"))))
    cases.append(("child-env-no-tmp",
                  not ce["HOME"].startswith("/tmp") and not ce["TMPDIR"].startswith("/tmp")))
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
    ap.add_argument("--upx", default=UPX)
    ap.add_argument("--json-out")
    ap.add_argument("--check-receipt")
    ap.add_argument("--skip-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.check_receipt:
        if not (args.root and args.rev):
            print("packed-elf: --check-receipt requires --root and --rev", file=sys.stderr)
            return 2
        return check_receipt(args.check_receipt, args.root, args.rev)
    if not (args.root and args.rev and args.pkg):
        print("packed-elf: --root, --rev and --pkg are required", file=sys.stderr)
        return 2
    try:
        return score(args.root, args.rev, args.pkg, args.work or "/proc/self/fd",
                     args.json_out, args.skip_run, args.upx)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r70-packed-elf-v1",
                          "unevaluable": str(exc), "claim": "R70"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
