#!/usr/bin/env python3
"""packed-elf.py - round-71 instrument (R71-C1 coverage).

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

R71-C1 (the seam's runtime evidence class, PROVINCE/Core move of the round-70
Frontier line "runtime env-capture/concurrent-scratch coverage of the seam
arms"): every child of the route - packer, REA node, readelf, git - runs under
the SAME pure `build_child_env(run_root)` allowlist, and with
`--child-env-log <path>` the route records each child's OBSERVED environment
(the launcher writes its own `os.environ` - the block `execvp` passes to the
child - before exec) into a JSONL log and
summarises it in the receipt (`child_env_observed`: records, keys,
all_allowlisted, home_under_run, tmpdir_under_run, canary_present, children).
`--challenge <32-hex>` plus `--nonce-commitment <sha256>` bind the receipt to a
pre-committed run nonce: the receipt carries `run_nonce` and `run_binding =
sha256(nonce:instrument.sha256:packed_sha256...)`, and `--check-receipt
--nonce-commitment <c>` rejects a receipt whose nonce hash does not match the
commitment, whose binding does not re-derive, whose `run_root` is absent, or
whose observed-env summary contradicts the allowlist - a receipt transplanted
from another run fails beyond committed-field equality. `--carriers <id,...>`
runs a subset for probe evidence (target = subset size, `target_declared`
records 4); scoring evidence always uses all four carriers.

Round 72 closes the checker-mode gap the round-71 wave routed: `--check-receipt`
used to spawn `git` (the tool blob) and `readelf` (the carrier format) with no
`env=`, so both inherited the caller's whole environment.  Every checker-mode
child now runs under the same `build_child_env()` allowlist, is recorded into
`--child-env-log` when that path is given, and the checker's JSON carries a
re-derivable `clauses` object (the nonce/binding/run-root/child-env verdicts,
plus the capsule clause below) so a probe never re-derives a binding verdict
from the receipt's own fields.  `--capsule <log>` (or a receipt whose
`child_env_observed.log` resolves under `--root`) audits the raw witness with
`capsule_audit.py`: a lying summary over a polluted capsule fails the
`receipt_capsule` clause.

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capsule_audit  # noqa: E402

TOOL = "tools/round-72/packed-elf.py"
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

# UPX 5.2.0 --best packing is deterministic (same input bytes, same output:
# verified twice per carrier on 2026-11-04), so the packed stub's sha256 is a
# declared constant the receipt reader binds (supersession clause, round-70
# wave finding: a zeroed or fabricated packed_sha256 must fail).
DECLARED_PACKED = {
    "jq": "e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a",
    "xxd": "1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff",
    "libz": "a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b",
    "dinit": "b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7",
}

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
    "run-binding-derives",
    "nonce-hex-accept",
    "nonce-hex-reject",
    "observed-env-allowlist",
    "observed-env-canary",
    "observed-env-sibling-prefix",
    "nonce-clause-absent",
    "nonce-clause-mismatch",
    "nonce-clause-clean",
    "nonce-verdict-agrees",
    "checker-env-allowlist",
    "capsule-clause-names",
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
            "home_under_work": under(root, env.get("HOME", "")),
            "tmpdir_under_work": under(root, env.get("TMPDIR", "")),
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


# The observed-environment launcher: it records its own environ (the exact
# block the exec'ed child inherits) and then execs the real child.  It is the
# only way an arm can observe a real child environment instead of the
# builder's returned dict (round-70 M70-6).
LAUNCHER = r"""
import json, os, sys
# The launcher is an interpreter: PYTHONCOERCECLOCALE=0 was handed to it so the
# interpreter adds no LC_CTYPE of its own, and the marker key is removed before
# the observation.  Everything else the route passed is recorded verbatim and
# exec'ed unchanged (the declared launcher-artifact exclusion is this one key).
os.environ.pop("PYTHONCOERCECLOCALE", None)
with open(sys.argv[1], "a", encoding="utf-8") as fh:
    fh.write(json.dumps({"argv": sys.argv[2:], "env": dict(os.environ)},
                         sort_keys=True) + "\n")
os.execvp(sys.argv[2], sys.argv[2:])
"""

NONCE_RE = re.compile(r"^[0-9a-f]{64}$")


def under(root: str, path: str) -> bool:
    """True when path is root itself or a descendant (no sibling-prefix match)."""
    try:
        root_abs = os.path.abspath(root)
        return os.path.commonpath([root_abs, os.path.abspath(str(path))]) == root_abs
    except (TypeError, ValueError):
        return False


def run(argv: list[str], timeout: int = 900, env: dict | None = None,
        capture: str | None = None) -> dict:
    real = list(argv)
    child_env = env
    if capture:
        child_env = dict(env or {})
        child_env["PYTHONCOERCECLOCALE"] = "0"
        argv = [sys.executable, "-B", "-s", "-c", LAUNCHER, capture, *real]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                              env=child_env)
    except OSError as exc:
        raise Unevaluable(f"child_unexecutable: {real[0]} ({exc.__class__.__name__}: {exc})")
    return {"argv": real, "rc": proc.returncode, "stdout": proc.stdout,
            "stdout_bytes": len(proc.stdout), "stderr": proc.stderr[-4000:]}


def observed_env(log_path: str | None, run_root: str) -> dict | None:
    """Read the observed-child log and summarise it for the receipt."""
    if not log_path:
        return None
    root = os.path.abspath(run_root)
    records = []
    try:
        with open(log_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line)
                if isinstance(payload, dict):
                    records.append(payload)
    except (OSError, json.JSONDecodeError):
        records = []
    envs = [r.get("env") or {} for r in records]
    children = {}
    for r in records:
        argv = r.get("argv") or ["?"]
        name = os.path.basename(str(argv[0]))
        children[name] = children.get(name, 0) + 1
    return {"log": log_path, "run_root": root, "records": len(records),
            "log_sha256": sha256_file(log_path) if os.path.exists(log_path) else None,
            "keys": sorted({k for e in envs for k in e}),
            "all_allowlisted": bool(envs) and all(
                sorted(e) == sorted(CHILD_ENV_KEYS) for e in envs),
            "home_under_run": bool(envs) and all(
                under(root, e.get("HOME", "")) for e in envs),
            "tmpdir_under_run": bool(envs) and all(
                under(root, e.get("TMPDIR", "")) for e in envs),
            "canary_present": any("KAIDOKU_ENV_CANARY" in e for e in envs),
            "children": children}


def run_binding(nonce: str, instrument_sha: str | None, packed_shas) -> str:
    """The receipt's run binding: nonce + producer + the packed artifact pins."""
    payload = f"{nonce}:{instrument_sha}:{','.join(sorted(packed_shas))}"
    return hashlib.sha256(payload.encode()).hexdigest()


def nonce_clauses(receipt: dict, commitment: str) -> list[str]:
    """The R71-C1 receipt clauses beyond committed-field equality."""
    failing = []
    nonce = receipt.get("run_nonce")
    instrument = receipt.get("instrument") or {}
    carriers = receipt.get("carriers") or []
    if not isinstance(nonce, str) or not NONCE_RE.match(nonce):
        failing.append("run_nonce absent")
    elif hashlib.sha256(nonce.encode()).hexdigest() != commitment:
        failing.append(f"run_nonce hash != commitment {commitment}")
    else:
        shas = [c.get("packed_sha256") for c in carriers
                if isinstance(c.get("packed_sha256"), str)]
        want = run_binding(nonce, instrument.get("sha256"), shas)
        if receipt.get("run_binding") != want:
            failing.append("run_binding != derived")
    run_root = receipt.get("run_root")
    if not isinstance(run_root, str) or not run_root:
        failing.append("run_root absent")
    observed = receipt.get("child_env_observed")
    if not isinstance(observed, dict) or not observed:
        failing.append("child_env_observed absent")
    else:
        if sorted(observed.get("keys") or []) != sorted(CHILD_ENV_KEYS):
            failing.append(f"child_env_observed.keys {observed.get('keys')} "
                           f"!= allowlist")
        if not isinstance(observed.get("records"), int) or observed["records"] < 1:
            failing.append(f"child_env_observed.records {observed.get('records')} < 1")
        for flag in ("all_allowlisted", "home_under_run", "tmpdir_under_run"):
            if observed.get(flag) is not True:
                failing.append(f"child_env_observed.{flag} not true")
        if observed.get("canary_present") is not False:
            failing.append("child_env_observed.canary_present not false")
    return failing


def nonce_verdict(receipt: dict, commitment: str) -> dict:
    """The nonce/binding/run-root/child-env clauses as booleans (R72-C2).

    Mirrors `nonce_clauses` field for field; the seam probe's A10 reads these
    from the checker's JSON, never re-derives a binding verdict itself.
    """
    receipt = receipt if isinstance(receipt, dict) else {}
    nonce = receipt.get("run_nonce")
    instrument = receipt.get("instrument") or {}
    carriers = receipt.get("carriers") or []
    nonce_present = isinstance(nonce, str) and bool(NONCE_RE.match(nonce))
    nonce_ok = bool(nonce_present) and \
        hashlib.sha256(nonce.encode()).hexdigest() == commitment
    shas = [c.get("packed_sha256") for c in carriers
            if isinstance(c.get("packed_sha256"), str)]
    want = run_binding(nonce, instrument.get("sha256"), shas) if nonce_ok else None
    binding_ok = bool(nonce_ok) and receipt.get("run_binding") == want
    observed = receipt.get("child_env_observed")
    env_ok = (isinstance(observed, dict) and bool(observed)
              and sorted(observed.get("keys") or []) == sorted(CHILD_ENV_KEYS)
              and isinstance(observed.get("records"), int)
              and observed["records"] >= 1
              and all(observed.get(f) is True
                      for f in ("all_allowlisted", "home_under_run",
                                "tmpdir_under_run"))
              and observed.get("canary_present") is False)
    return {"nonce_present": bool(nonce_present), "nonce_ok": bool(nonce_ok),
            "binding_ok": bool(binding_ok),
            "run_root_ok": isinstance(receipt.get("run_root"), str)
            and bool(receipt.get("run_root")),
            "child_env_ok": bool(env_ok)}


def rea(pkg: str, env: dict, *args: str, capture: str | None = None) -> dict:
    return run(["node", os.path.join(pkg, "scripts", "rea.mjs"), *args],
               timeout=900, env=env, capture=capture)


def analyze(pkg: str, path: str, receipt_path: str, env: dict,
            capture: str | None = None) -> tuple[dict, dict]:
    """Run REA analyze, keep the raw envelope, return (envelope, run record)."""
    rec = rea(pkg, env, "analyze", "--format", "json", path, capture=capture)
    env = {}
    try:
        env = json.loads(rec["stdout"]) if rec["stdout"].strip() else {}
    except json.JSONDecodeError:
        env = {}
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump({"run": rec, "envelope": env}, fh, indent=1, sort_keys=True)
    return env, rec


def decompile(pkg: str, path: str, address: str, env: dict,
              capture: str | None = None) -> dict:
    rec = rea(pkg, env, "decompile", path, address, "--format", "json",
              capture=capture)
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
              child_env: dict | None = None, capture: str | None = None) -> dict:
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
        version = run([upx, "--version"], env=cenv,
                      capture=capture).get("stdout", "").strip().splitlines()
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
                banner = run([found, "--version"], env=cenv,
                             capture=capture).get("stdout", "").strip()
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


def git_blob_sha256(root: str, rev: str, path: str,
                    env: dict | None = None,
                    capture: str | None = None) -> str | None:
    """The tool blob at `rev`, read through the checker's own child environment.

    Round 72 (R72-C1): the checker's `git` used to inherit the caller's whole
    environment; it now runs under build_child_env() like every other child,
    and the capture launcher records it when a path is given.
    """
    try:
        proc = run(["git", "-C", root, "show", f"{rev}:{path}"], timeout=120,
                   env=env, capture=capture)
    except Unevaluable:
        return None
    if proc["rc"] != 0:
        return None
    return hashlib.sha256(proc["stdout"].encode("utf-8")).hexdigest()


def check_receipt(path: str, root: str, rev: str,
                  nonce_commitment: str | None = None,
                  work: str | None = None,
                  child_env_log: str | None = None,
                  capsule: str | None = None) -> int:
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

    Round 72: every checker-mode child (`git`, `readelf`) runs under
    build_child_env() and is captured into `child_env_log` when given
    (R72-C1); `capsule` (or the receipt's own resolvable `child_env_observed`
    log) is audited from its raw bytes by `capsule_audit.audit`, so a lying
    summary cannot pass (R72-C3).  The JSON carries the re-derivable `clauses`
    and `checker_child_env` blocks the probe reads.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"check": "R70-C3", "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    check_root = os.path.abspath(work) if work else tempfile.mkdtemp(prefix="kdk-check-")
    for sub in ("home", "tmp"):
        try:
            os.makedirs(os.path.join(check_root, sub), exist_ok=True)
        except OSError:
            pass
    cenv = build_child_env(check_root)
    capture = child_env_log
    if capture is not None and not os.path.isabs(capture):
        capture = os.path.join(check_root, capture)
    failing = []
    if not isinstance(receipt, dict):
        failing.append("receipt root is not an object")
        out = {"check": "R70-C3", "met": False, "failing": failing,
               "target": None, "carriers_matched": None, "kinds": [],
               "receipt": path, "rev": rev}
        print(json.dumps(out, indent=1, sort_keys=True))
        return 1
    blob_sha = git_blob_sha256(root, rev, TOOL, env=cenv, capture=capture)
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
    packer = receipt.get("packer") or {}
    if packer.get("sha256") != UPX_SHA256_PIN or packer.get("sha256_pin") != UPX_SHA256_PIN:
        failing.append(f"packer sha256 {packer.get('sha256')} / pin "
                       f"{packer.get('sha256_pin')} != {UPX_SHA256_PIN}")
    if packer.get("version") != UPX_VERSION_PIN or packer.get("version_pin") != UPX_VERSION_PIN:
        failing.append(f"packer version {packer.get('version')} / pin "
                       f"{packer.get('version_pin')} != {UPX_VERSION_PIN}")
    if packer.get("pin_enforced") is not True:
        failing.append("packer.pin_enforced not true")
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
    kinds = sorted(c.get("kind") for c in carriers)
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
        # Evidence fields the receipt must carry truthfully (round-70 wave
        # findings: the frozen first cut ignored these six and a lying receipt
        # passed).  Each is re-derived from the frozen table or the pinned
        # source bytes, never trusted from the receipt's word.
        if c.get("unpacked_counts") != c.get("orig_counts"):
            failing.append(f"{cid}: unpacked_counts {c.get('unpacked_counts')} "
                           f"!= orig_counts (the recovery arm is recover==orig)")
        if c.get("packed_sha256") != DECLARED_PACKED[cid]:
            failing.append(f"{cid}: packed_sha256 {c.get('packed_sha256')} != "
                           f"declared {DECLARED_PACKED[cid]}")
        if c.get("section_count") != 0:
            failing.append(f"{cid}: section_count {c.get('section_count')} != 0")
        if c.get("upx_list_rc") != 0:
            failing.append(f"{cid}: upx_list_rc {c.get('upx_list_rc')} != 0")
        control = c.get("control") or {}
        if control.get("list_rc", 1) == 0 or control.get("decompress_rc", 1) == 0:
            failing.append(f"{cid}: control rcs {control} not both nonzero")
        runs = c.get("runs")
        if not isinstance(runs, dict) or not runs:
            failing.append(f"{cid}: runs absent")
        else:
            for step, flag in (("pack", "--best"), ("unpack", "-d")):
                step_rec = runs.get(step) or {}
                argv = step_rec.get("argv")
                if not isinstance(argv, list) or not argv:
                    failing.append(f"{cid}: runs.{step}.argv absent")
                elif flag not in argv:
                    failing.append(f"{cid}: runs.{step}.argv {argv} lacks {flag}")
                if step_rec.get("rc") != 0:
                    failing.append(f"{cid}: runs.{step}.rc {step_rec.get('rc')} != 0")
        refusal = c.get("refusal")
        if row.get("address"):
            if not isinstance(refusal, dict):
                failing.append(f"{cid}: refusal absent for an addressed carrier")
            else:
                if refusal.get("packed_rc", 0) == 0:
                    failing.append(f"{cid}: refusal.packed_rc 0 (packed bytes must refuse)")
                if refusal.get("unpacked_rc") != 0:
                    failing.append(f"{cid}: refusal.unpacked_rc "
                                   f"{refusal.get('unpacked_rc')} != 0")
                if refusal.get("symbol_present") is not True:
                    failing.append(f"{cid}: refusal.symbol_present not true")
                if not isinstance(refusal.get("unpacked_code_bytes"), int) \
                        or refusal["unpacked_code_bytes"] <= 200:
                    failing.append(f"{cid}: refusal.unpacked_code_bytes "
                                   f"{refusal.get('unpacked_code_bytes')} <= 200")
        elif refusal is not None:
            failing.append(f"{cid}: refusal {refusal} present for an addressless carrier")
        derived_format = None
        if os.path.exists(row["source"]):
            rh = run(["readelf", "-h", row["source"]], env=cenv, capture=capture)
            derived_format = elf_format(rh["stdout"] + rh["stderr"])
        if c.get("format") != derived_format:
            failing.append(f"{cid}: format {c.get('format')} != readelf of the "
                           f"pinned source {derived_format}")
    ceilings = receipt.get("before_ceilings")
    if not isinstance(ceilings, list) or len(ceilings) != len(CARRIERS):
        failing.append(f"before_ceilings {type(ceilings).__name__}x"
                       f"{len(ceilings) if isinstance(ceilings, list) else 0} != "
                       f"{len(CARRIERS)} entries")
    else:
        for entry in ceilings:
            eid = entry.get("id")
            row = registry.get(eid)
            if row is None:
                failing.append(f"before_ceilings: unknown id {eid}")
                continue
            if entry.get("ceiling") != row["before_max_procedures"]:
                failing.append(f"before_ceilings {eid}: ceiling "
                               f"{entry.get('ceiling')} != registry")
            if entry.get("orig_procedures") != DECLARED_ORIG[eid]:
                failing.append(f"before_ceilings {eid}: orig_procedures "
                               f"{entry.get('orig_procedures')} != declared "
                               f"{DECLARED_ORIG[eid]}")
            if isinstance(entry.get("orig_procedures"), int) \
                    and entry["orig_procedures"] > 0 \
                    and entry.get("ceiling_ratio") != round(
                        row["before_max_procedures"] / entry["orig_procedures"], 4):
                failing.append(f"before_ceilings {eid}: ceiling_ratio "
                               f"{entry.get('ceiling_ratio')} != ceiling/orig")
    if sorted(x for x in seen_ids if x is not None) != sorted(registry):
        failing.append(f"carrier ids {seen_ids} != registry {sorted(registry)}")
    if nonce_commitment is not None:
        failing.extend(nonce_clauses(receipt, nonce_commitment))
    verdict = (nonce_verdict(receipt, nonce_commitment)
               if nonce_commitment is not None
               else {"nonce_ok": None, "binding_ok": None})
    observed = receipt.get("child_env_observed")
    capsule_path = capsule
    capsule_out = None
    capsule_absent = None
    if capsule_path is None and isinstance(observed, dict) \
            and isinstance(observed.get("log"), str):
        cand = observed["log"]
        if not os.path.isabs(cand):
            # A lane-relative capsule is filed evidence: its absence is a
            # named failure, never a silent pass (round-72 ReviewerGates).
            cand = os.path.join(os.path.abspath(root), cand)
            if os.path.exists(cand):
                capsule_path = cand
            else:
                capsule_absent = cand
        elif os.path.exists(cand):
            capsule_path = cand
        # An absolute pointer outside the lane is a run pointer (dead scratch),
        # recorded as not evaluated - it makes no committed-evidence claim.
    if capsule_absent is not None:
        failing.append(f"receipt_capsule: named capsule absent ({capsule_absent})")
    capsule_verdict = False if capsule_absent is not None else None
    if capsule_path is not None:
        capsule_out = capsule_audit.audit(capsule_path, observed or {},
                                          run_root=None)
        capsule_verdict = capsule_out.get("ok") is True
        failing.extend(f"receipt_capsule: {f}" for f in capsule_out.get("failures") or [])
    clauses = {"met": not failing,
               "run_nonce": verdict.get("nonce_ok"),
               "run_binding": verdict.get("binding_ok"),
               "run_root": verdict.get("run_root_ok"),
               "child_env_observed": verdict.get("child_env_ok"),
               "receipt_capsule": capsule_verdict}
    out = {"check": "R71-receipt", "met": not failing, "failing": failing,
           "target": target, "carriers_matched": receipt.get("carriers_matched"),
           "kinds": kinds, "receipt": path, "rev": rev,
           "instrument_sha256": (instrument if isinstance(instrument, dict)
                                 else {}).get("sha256"),
           "nonce_commitment": nonce_commitment,
           "clauses": clauses,
           "checker_child_env": observed_env(capture, check_root),
           "capsule": ({"path": capsule_path, "ok": capsule_verdict,
                        "failures": (capsule_out or {}).get("failures", [])}
                       if capsule_path is not None else None),
           "before_ceilings": receipt.get("before_ceilings")}
    print(json.dumps(out, indent=1, sort_keys=True))
    if work is None:
        shutil.rmtree(check_root, ignore_errors=True)
    return 0 if not failing else 1


def score(root: str, rev: str, pkg: str, work: str, out: str | None,
          skip_run: bool, upx: str = UPX, challenge: str | None = None,
          nonce_commitment: str | None = None,
          carrier_ids: list[str] | None = None,
          env_log: str | None = None) -> int:
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: not a directory ({work})")
    if challenge is not None:
        if not NONCE_RE.match(challenge or ""):
            raise Unevaluable(f"challenge is not 32 lowercase hex bytes: {challenge!r}")
        if not nonce_commitment or not NONCE_RE.match(nonce_commitment or ""):
            raise Unevaluable("--challenge requires a 32-hex --nonce-commitment")
        want = hashlib.sha256(challenge.encode()).hexdigest()
        if want != nonce_commitment:
            raise Unevaluable(f"commitment_mismatch: sha256(challenge) {want} != "
                              f"{nonce_commitment}")
    elif nonce_commitment is not None:
        raise Unevaluable("--nonce-commitment requires --challenge")
    selected = list(CARRIERS)
    if carrier_ids:
        known = {c["id"] for c in CARRIERS}
        unknown = [cid for cid in carrier_ids if cid not in known]
        if unknown:
            raise Unevaluable(f"unknown carrier ids: {unknown}")
        selected = [c for c in CARRIERS if c["id"] in carrier_ids]

    def git(*argv: str) -> str:
        try:
            return run(["git", "-C", root, *argv], timeout=120, env=cenv,
                       capture=capture)["stdout"]
        except Unevaluable as exc:
            raise Unevaluable(f"broken_tool: git ({exc})")

    run_root = tempfile.mkdtemp(prefix="packed-", dir=work)
    for sub in ("home", "tmp"):
        os.makedirs(os.path.join(run_root, sub), exist_ok=True)
    cenv = build_child_env(run_root)
    capture = env_log
    if capture is not None and not os.path.isabs(capture):
        capture = os.path.join(run_root, capture)
    try:
        packer_env = preflight(upx, pkg, work, check_work=not skip_run,
                               child_env=cenv, capture=capture)
    except Unevaluable:
        shutil.rmtree(run_root, ignore_errors=True)
        raise
    upx_v = packer_env["upx"]
    instrument = {"path": TOOL, "sha256": sha256_file(os.path.abspath(__file__)),
                  "rev": git("log", "-1", "--format=%H", "--", TOOL).strip() or None}
    instrument_sha = instrument["sha256"]
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
        "claims": ["R71-C1"],
        "child_env": child_env_audit(cenv, run_root),
        "run_root": run_root,
        "carrier_subset": [c["id"] for c in selected],
        "rea": {"version": pkg_meta.get("version"), "package_json_sha256": pkg_sha,
                "root": pkg, "lock_path": lock,
                "lock_sha256": sha256_file(lock) if lock else None,
                "lock_recorded_not_pinned": True,
                "node": shutil.which("node"),
                "node_version": run([shutil.which("node") or "node", "--version"],
                                    env=cenv, capture=capture).get("stdout", "").strip()},
    }
    if skip_run:
        binding = None
        if challenge:
            binding = run_binding(challenge, instrument_sha,
                                  [DECLARED_PACKED[c["id"]] for c in selected])
        payload = {**env, "claim": "R71", "closure": None, "verdict_claimed": False,
                   "met_target": None, "carriers": [], "control_ok": None,
                   "child_env_observed": observed_env(capture, run_root),
                   "run_nonce": challenge, "run_binding": binding,
                   "nonce_commitment": nonce_commitment,
                   "target_declared": len(CARRIERS)}
        text = json.dumps(payload, indent=1, sort_keys=True)
        if out:
            open(out, "w", encoding="utf-8").write(text + "\n")
        print(text)
        # A run-scoped env log (a relative --child-env-log) lives under the
        # run root; keep it for the caller that asked for it.  An absolute log
        # is the caller's artifact and survives on its own.
        if not (capture and capture.startswith(run_root)):
            shutil.rmtree(run_root, ignore_errors=True)
        return 1

    carriers = []
    try:
        for c in selected:
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
            orig_env, orig_run = analyze(pkg, orig,
                                         os.path.join(cdir, "orig.analyze.json"),
                                         cenv, capture)
            orig_counts = counts_from(orig_env)
            if not orig_counts or orig_counts["procedure_count"] < c["min_orig_procedures"]:
                raise Unevaluable(f"carrier {c['id']}: original inventory below the floor "
                                  f"({orig_counts})")
            packed = os.path.join(cdir, "packed-" + base)
            pack = run([upx_v, "--best", "-q", "-o", packed, orig],
                       env=cenv, capture=capture)
            if pack["rc"] != 0 or not os.path.exists(packed):
                raise Unevaluable(f"carrier {c['id']}: upx pack failed rc={pack['rc']}")
            packed_sha = sha256_file(packed)
            listing = run([upx_v, "-l", packed], env=cenv, capture=capture)
            readelf = run(["readelf", "-SW", packed], env=cenv, capture=capture)
            secs = section_count(readelf["stdout"] + readelf["stderr"])
            packed_env, packed_run = analyze(pkg, packed,
                                             os.path.join(cdir, "packed.analyze.json"),
                                             cenv, capture)
            packed_counts = counts_from(packed_env) or {}
            unpacked = os.path.join(cdir, "unpacked-" + base)
            unpack = run([upx_v, "-d", "-q", "-o", unpacked, packed],
                         env=cenv, capture=capture)
            unpacked_sha = sha256_file(unpacked) if os.path.exists(unpacked) else None
            rec_env, rec_run = analyze(pkg, unpacked,
                                       os.path.join(cdir, "unpacked.analyze.json"),
                                       cenv, capture)
            rec_counts = counts_from(rec_env) or {}
            refusal = None
            if c.get("address"):
                d_packed = decompile(pkg, packed, c["address"], cenv, capture)
                d_unpacked = decompile(pkg, unpacked, c["address"], cenv, capture)
                code = d_unpacked["code"] or ""
                refusal = {"packed_rc": d_packed["run"]["rc"],
                           "packed_error_code": d_packed["error_code"],
                           "unpacked_rc": d_unpacked["run"]["rc"],
                           "unpacked_code_bytes": len(code),
                           "symbol_present": c["address_symbol"] in code}
            ctrl_l = run([upx_v, "-l", orig], env=cenv, capture=capture)
            ctrl_d = run([upx_v, "-d", "-q", "-o", os.path.join(cdir, "ctrl-" + base), orig],
                         env=cenv, capture=capture)
            header = run(["readelf", "-h", orig], env=cenv, capture=capture)
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
        verdict = fold(carriers, len(selected))
    finally:
        shutil.rmtree(run_root, ignore_errors=True)
    packed_shas = [c["packed_sha256"] for c in carriers]
    binding = run_binding(challenge, instrument_sha, packed_shas) if challenge else None
    payload = {**env, "claim": "R71", "closure": verdict, **verdict,
               "child_env_observed": observed_env(capture, run_root),
               "run_nonce": challenge, "run_binding": binding,
               "nonce_commitment": nonce_commitment,
               "target_declared": len(CARRIERS),
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


def selftest(work: str | None = None) -> int:
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
    nonce = "ab" * 32
    cases.append(("run-binding-derives",
                  run_binding(nonce, "cc" * 32, ["dd" * 32, "bb" * 32])
                  == hashlib.sha256((nonce + ":" + "cc" * 32 + ":" +
                                     ",".join(sorted(["dd" * 32, "bb" * 32])))
                                    .encode()).hexdigest()))
    cases.append(("nonce-hex-accept", bool(NONCE_RE.match("ab" * 32))))
    cases.append(("nonce-hex-reject", not NONCE_RE.match("AB" * 32)
                  and not NONCE_RE.match("ab" * 31)))
    sel_scratch = tempfile.mkdtemp(prefix="packed-selftest-", dir=work)
    try:
        log = os.path.join(sel_scratch, "env.jsonl")
        allow = build_child_env(sel_scratch)
        with open(log, "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"argv": ["/usr/bin/upx", "--version"],
                                 "env": allow}) + "\n")
            fh.write(json.dumps({"argv": ["/usr/bin/node", "--version"],
                                 "env": allow}) + "\n")
        obs = observed_env(log, sel_scratch)
        cases.append(("observed-env-allowlist",
                      obs["records"] == 2 and obs["all_allowlisted"] is True
                      and obs["canary_present"] is False
                      and obs["home_under_run"] is True
                      and obs["children"] == {"upx": 1, "node": 1}))
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"argv": ["/usr/bin/upx", "-l"],
                                 "env": {**allow, "KAIDOKU_ENV_CANARY": "1"}}) + "\n")
        obs2 = observed_env(log, sel_scratch)
        cases.append(("observed-env-canary",
                      obs2["canary_present"] is True
                      and obs2["all_allowlisted"] is False))
        cases.append(("observed-env-sibling-prefix",
                      under(sel_scratch, sel_scratch + "-outside/home") is False
                      and under(sel_scratch, os.path.join(sel_scratch, "home")) is True))
    finally:
        shutil.rmtree(sel_scratch, ignore_errors=True)
    good_receipt = {"run_nonce": nonce,
                    "instrument": {"sha256": "cc" * 32},
                    "carriers": [{"packed_sha256": "dd" * 32}],
                    "run_root": "/some/run",
                    "child_env_observed": {"keys": list(CHILD_ENV_KEYS), "records": 1,
                                           "all_allowlisted": True,
                                           "home_under_run": True,
                                           "tmpdir_under_run": True,
                                           "canary_present": False}}
    good_receipt["run_binding"] = run_binding(nonce, "cc" * 32, ["dd" * 32])
    commitment = hashlib.sha256(nonce.encode()).hexdigest()
    cases.append(("nonce-clause-absent",
                  nonce_clauses({}, commitment) == ["run_nonce absent",
                                                    "run_root absent",
                                                    "child_env_observed absent"]))
    wrong = json.loads(json.dumps(good_receipt))
    wrong["run_nonce"] = "cd" * 32
    cases.append(("nonce-clause-mismatch",
                  nonce_clauses(wrong, commitment)[0].startswith(
                      "run_nonce hash != commitment")))
    cases.append(("nonce-clause-clean",
                  nonce_clauses(good_receipt, commitment) == []))
    verdict = nonce_verdict(good_receipt, commitment)
    cases.append(("nonce-verdict-agrees",
                  verdict["nonce_ok"] is True and verdict["binding_ok"] is True
                  and verdict["run_root_ok"] is True
                  and verdict["child_env_ok"] is True
                  and nonce_verdict(wrong, commitment)["nonce_ok"] is False
                  and nonce_verdict(
                      {**good_receipt, "run_binding": "00" * 32},
                      commitment)["binding_ok"] is False))
    check_env = build_child_env("/some/check")
    cases.append(("checker-env-allowlist",
                  sorted(check_env) == sorted(CHILD_ENV_KEYS)
                  and check_env["HOME"].startswith(os.path.abspath("/some/check"))
                  and check_env["TMPDIR"].startswith(os.path.abspath("/some/check"))))
    capsule = capsule_audit.audit(__file__, good_receipt["child_env_observed"],
                                  run_root="/some/run")
    cases.append(("capsule-clause-names",
                  capsule["ok"] is False
                  and "records" in capsule["failures"]
                  and capsule["clauses"]["log_sha256"] is None))
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
    ap.add_argument("--challenge")
    ap.add_argument("--nonce-commitment")
    ap.add_argument("--carriers")
    ap.add_argument("--child-env-log")
    ap.add_argument("--capsule")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest(args.work)
    if args.check_receipt:
        if not (args.root and args.rev):
            print("packed-elf: --check-receipt requires --root and --rev", file=sys.stderr)
            return 2
        return check_receipt(args.check_receipt, args.root, args.rev,
                             args.nonce_commitment, args.work,
                             args.child_env_log, args.capsule)
    if not (args.root and args.rev and args.pkg and args.work):
        print("packed-elf: --root, --rev, --pkg and --work are required",
              file=sys.stderr)
        return 2
    subset = [s.strip() for s in (args.carriers or "").split(",") if s.strip()]
    try:
        return score(args.root, args.rev, args.pkg, args.work, args.json_out,
                     args.skip_run, args.upx, args.challenge,
                     args.nonce_commitment, subset or None,
                     args.child_env_log)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r71-packed-elf-v1",
                          "unevaluable": str(exc), "claim": "R71"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
