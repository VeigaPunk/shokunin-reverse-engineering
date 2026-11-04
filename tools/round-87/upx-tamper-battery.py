#!/usr/bin/env python3
"""upx-tamper-battery.py - round-87 counter (R87-C1, coverage, capability).

The packed-ELF route (rounds 68-73) recovers UPX-packed carriers, but only
while the packer's own markers are intact.  A common anti-unpack trick
overwrites the `UPX!` magic words: the packed program still runs (its stub
never needs them) while `upx -d` and `upx -l` answer `NotPackedException`.
PROVINCE.md kept that class on the Frontier ("an anti-UPX stub whose magic or
entry is altered").  This counter scores a repair command against it.

Population (frozen): the four round-70 carriers (jq, xxd, libz, docker-init;
sha256-pinned) packed with the pinned packer (`upx --best`, UPX 5.2.0) and
tampered in two classes:

  T1-zero     every `UPX!` word of the packed file replaced by 00 00 00 00
  T2-foreign  every `UPX!` word replaced by `KDK!` (absent from the packed
              file before tampering; checked, otherwise exit 2)

Precondition per case: `upx -t` on the tampered file exits non-zero (the
tamper is effective); a case where it does not is could-not-evaluate (exit 2).

A case is RECOVERED iff all five arms hold:
  repair_rc0    the repair command exits 0 and writes the output file
  windows_only  the output has the tampered file's length and every byte that
                differs lies inside a 4-byte window that now reads `UPX!`
  test_ok       `upx -t` on the output exits 0
  identity      `upx -d` of the output restores bytes whose sha256 is the
                carrier pin
  rea_recover   REA 6.5.0 `analyze` of the restored bytes reports the
                carrier's declared original procedure count (round-70
                DECLARED_ORIG) - skipped (false) unless identity holds

Controls in every run (all must hold for met):
  N1-refuse-plain      the repair command exits non-zero on each pinned
                       ORIGINAL (not packed): 4 of 4 refused
  N2-corrupt-payload   T1 tamper plus one flipped byte at len//2 (inside the
                       compressed payload): recovered 0 of 4
  N3-intact-idempotent the untampered packed file: repair exits 0 and the
                       output is byte-identical: 4 of 4

met_target: recovered == 8 of 8 and all three controls hold.
Exit: 0 met; 1 not met (every false arm named; receipt written);
2 could-not-evaluate (packer/carrier/REA pin drift, missing tool, ineffective
tamper, bad argv, refused --work).

--repair-cmd takes a path to a Python repair script, invoked as
`python3 -I -B <script> --in <tampered> --out <output>` under a four-key child
environment, or one of two built-in controls that skip the claimed work:
  identity      copies input to output (the do-nothing control)
  naive-global  reads the 4 bytes at len-36 and replaces every occurrence of
                them in the file with `UPX!` (the cheap rule)
Named limit: a repair that reads the original carrier and re-packs it would
produce the same correct bytes; the counter scores bytes, not provenance.

--selftest runs the pure helpers on in-memory fixtures (no upx, no REA).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-87/upx-tamper-battery.py"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
REA_VERSION = "6.5.0"
REA_PKGJSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
MAGIC = b"UPX!"
TAMPERS = {"T1-zero": b"\x00\x00\x00\x00", "T2-foreign": b"KDK!"}
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq",
     "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"},
    {"id": "xxd", "source": "/usr/bin/xxd",
     "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2",
     "sha256": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"},
    {"id": "dinit", "source": "/usr/bin/docker-init",
     "sha256": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"},
]
DECLARED_ORIG = {"jq": 167, "xxd": 99, "libz": 184, "dinit": 1268}
TARGET = len(CARRIERS) * len(TAMPERS)
ARMS = ("repair_rc0", "windows_only", "test_ok", "identity", "rea_recover")
BUILTINS = ("identity", "naive-global")


class Unevaluable(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def child_env(work: str) -> dict:
    return {"HOME": os.path.join(work, "home"), "LANG": "C",
            "PATH": os.environ.get("PATH") or "/usr/bin",
            "TMPDIR": os.path.join(work, "tmp")}


def run(argv: list, env: dict, timeout: int = 900) -> dict:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=env,
                           timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"argv": argv, "rc": None, "error": f"{exc.__class__.__name__}: {exc}"}
    tail = (p.stdout + p.stderr).strip().splitlines()
    return {"argv": argv, "rc": p.returncode, "tail": tail[-2:], "stdout": p.stdout}


def tamper(packed: bytes, value: bytes) -> bytes:
    return packed.replace(MAGIC, value)


def windows_only(tampered: bytes, out: bytes) -> tuple[bool, str]:
    """Every differing byte lies inside a 4-byte window that now reads UPX!."""
    if len(tampered) != len(out):
        return False, f"length {len(out)} != {len(tampered)}"
    covered = bytearray(len(out))
    start = out.find(MAGIC)
    while start != -1:
        for k in range(start, start + 4):
            covered[k] = 1
        start = out.find(MAGIC, start + 1)
    for i, (a, b) in enumerate(zip(tampered, out)):
        if a != b and not covered[i]:
            return False, f"byte {i} changed outside a UPX! window"
    return True, ""


def builtin_repair(name: str, data: bytes) -> bytes:
    if name == "identity":
        return data
    if name == "naive-global":
        if len(data) < 36:
            return data
        word = data[-36:-32]
        return data.replace(word, MAGIC) if word else data
    raise ValueError(name)


def apply_repair(cmd: str, src: str, dst: str, env: dict) -> dict:
    if cmd in BUILTINS:
        with open(src, "rb") as fh:
            data = fh.read()
        with open(dst, "wb") as fh:
            fh.write(builtin_repair(cmd, data))
        return {"argv": ["<builtin>", cmd], "rc": 0}
    return run([sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst], env,
               timeout=300)


def rea_procedures(pkg: str, path: str, env: dict, out_json: str) -> tuple[int | None, dict]:
    rec = run(["node", os.path.join(pkg, "scripts", "rea.mjs"), "analyze",
               "--format", "json", path], env)
    envl = {}
    try:
        envl = json.loads(rec.get("stdout") or "{}")
    except json.JSONDecodeError:
        envl = {}
    norm = envl.get("normalized_result") if isinstance(envl, dict) else None
    counts = None
    if isinstance(norm, dict):
        counts = {k: norm.get(k) for k in ("procedure_count", "segment_count", "string_count")}
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump({"argv": rec["argv"], "rc": rec["rc"], "counts": counts,
                   "evidence_id": envl.get("evidence_id") if isinstance(envl, dict) else None},
                  fh, indent=1, sort_keys=True)
    rec.pop("stdout", None)
    pc = counts.get("procedure_count") if counts else None
    return (pc if isinstance(pc, int) else None), {"rc": rec["rc"], "counts": counts}


def preflight(upx: str, pkg: str, work: str, env: dict, repair: str, rea_on: bool) -> dict:
    if not os.path.isfile(upx):
        raise Unevaluable(f"missing_tool: upx ({upx})")
    sha = sha256_file(upx)
    if sha != UPX_SHA256_PIN:
        raise Unevaluable(f"packer_mismatch: sha256 {sha}")
    ver = run([upx, "--version"], env).get("stdout", "").strip().splitlines()
    if not ver or ver[0] != UPX_VERSION_PIN:
        raise Unevaluable(f"packer_mismatch: version {ver[:1]}")
    if rea_on:
        pj = os.path.join(pkg, "package.json")
        if not os.path.isfile(pj) or sha256_file(pj) != REA_PKGJSON_SHA256:
            raise Unevaluable(f"rea_pin: {pj}")
        if shutil.which("node") is None:
            raise Unevaluable("missing_tool: node")
    if repair not in BUILTINS and not os.path.isfile(repair):
        raise Unevaluable(f"missing_repair: {repair}")
    for c in CARRIERS:
        if not os.path.isfile(c["source"]) or sha256_file(c["source"]) != c["sha256"]:
            raise Unevaluable(f"carrier_pin: {c['id']}")
    return {"upx": upx, "sha256": sha, "version": ver[0], "rea_pkg": pkg if rea_on else None}


def score(args) -> tuple[int, dict]:
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: {work}")
    run_root = tempfile.mkdtemp(prefix="r87-battery-", dir=work)
    env = child_env(run_root)
    os.makedirs(env["HOME"]); os.makedirs(env["TMPDIR"])
    rea_on = not args.no_rea
    repair = args.repair_cmd if args.repair_cmd in BUILTINS else os.path.abspath(args.repair_cmd)
    try:
        pre = preflight(args.upx, args.pkg, work, env, repair, rea_on)
        repair_sha = None if repair in BUILTINS else sha256_file(repair)
        cases, controls = [], {"N1-refuse-plain": [], "N2-corrupt-payload": [],
                               "N3-intact-idempotent": []}
        for c in CARRIERS:
            d = os.path.join(run_root, c["id"])
            os.makedirs(d)
            orig = os.path.join(d, "orig")
            shutil.copy2(c["source"], orig)
            packed = os.path.join(d, "packed")
            r = run([args.upx, "--best", "-q", "-o", packed, orig], env)
            if r["rc"] != 0:
                raise Unevaluable(f"pack_failed: {c['id']} {r.get('tail')}")
            with open(packed, "rb") as fh:
                pbytes = fh.read()
            if pbytes.count(MAGIC) == 0:
                raise Unevaluable(f"no_magic: {c['id']}")
            # N1: refuse the plain original
            n1 = apply_repair(repair, orig, os.path.join(d, "n1.out"), env)
            controls["N1-refuse-plain"].append({"carrier": c["id"], "rc": n1["rc"],
                                                "refused": n1["rc"] != 0})
            # N3: intact packed file is left byte-identical
            n3o = os.path.join(d, "n3.out")
            n3 = apply_repair(repair, packed, n3o, env)
            same = n3["rc"] == 0 and os.path.isfile(n3o) and sha256_file(n3o) == sha256_bytes(pbytes)
            controls["N3-intact-idempotent"].append({"carrier": c["id"], "rc": n3["rc"],
                                                     "identical": same})
            for tname, value in TAMPERS.items():
                case = {"carrier": c["id"], "tamper": tname,
                        "packed_sha256": sha256_bytes(pbytes),
                        "magic_words": pbytes.count(MAGIC)}
                if value != b"\x00\x00\x00\x00" and value in pbytes:
                    raise Unevaluable(f"tamper_value_present: {c['id']} {tname}")
                tb = tamper(pbytes, value)
                tp = os.path.join(d, f"{tname}.tampered")
                with open(tp, "wb") as fh:
                    fh.write(tb)
                pre_t = run([args.upx, "-t", "-q", tp], env)
                if pre_t["rc"] == 0:
                    raise Unevaluable(f"tamper_ineffective: {c['id']} {tname}")
                case["precondition"] = {"upx_t_rc": pre_t["rc"], "tail": pre_t.get("tail")}
                case["tampered_sha256"] = sha256_bytes(tb)
                outp = os.path.join(d, f"{tname}.repaired")
                rr = apply_repair(repair, tp, outp, env)
                arms = dict.fromkeys(ARMS, False)
                why = {}
                arms["repair_rc0"] = rr["rc"] == 0 and os.path.isfile(outp)
                if not arms["repair_rc0"]:
                    why["repair_rc0"] = f"rc {rr['rc']} {rr.get('tail')}"
                else:
                    with open(outp, "rb") as fh:
                        ob = fh.read()
                    case["repaired_sha256"] = sha256_bytes(ob)
                    case["repaired_equals_packed"] = ob == pbytes
                    arms["windows_only"], w = windows_only(tb, ob)
                    if w:
                        why["windows_only"] = w
                    t = run([args.upx, "-t", "-q", outp], env)
                    arms["test_ok"] = t["rc"] == 0
                    if not arms["test_ok"]:
                        why["test_ok"] = f"rc {t['rc']} {t.get('tail')}"
                    un = os.path.join(d, f"{tname}.unpacked")
                    u = run([args.upx, "-d", "-q", "-o", un, outp], env)
                    usha = sha256_file(un) if u["rc"] == 0 and os.path.isfile(un) else None
                    case["unpacked_sha256"] = usha
                    arms["identity"] = usha == c["sha256"]
                    if not arms["identity"]:
                        why["identity"] = f"rc {u['rc']} sha {usha}"
                    if arms["identity"] and rea_on:
                        rj = os.path.join(args.evidence_dir, f"rea-{c['id']}-{tname}.json") \
                            if args.evidence_dir else os.path.join(d, f"{tname}.rea.json")
                        pc, rinfo = rea_procedures(args.pkg, un, env, rj)
                        case["rea"] = rinfo
                        arms["rea_recover"] = pc == DECLARED_ORIG[c["id"]]
                        if not arms["rea_recover"]:
                            why["rea_recover"] = f"procedure_count {pc} != {DECLARED_ORIG[c['id']]}"
                    elif not rea_on:
                        why["rea_recover"] = "REA disabled (--no-rea)"
                    else:
                        why["rea_recover"] = "skipped: identity false"
                case["arms"] = arms
                case["false_arms"] = why
                case["recovered"] = all(arms.values())
                cases.append(case)
            # N2: payload corruption must not be recovered
            tb = bytearray(tamper(pbytes, TAMPERS["T1-zero"]))
            mid = len(tb) // 2
            tb[mid] ^= 0xFF
            n2p = os.path.join(d, "n2.tampered")
            with open(n2p, "wb") as fh:
                fh.write(tb)
            n2o = os.path.join(d, "n2.out")
            n2 = apply_repair(repair, n2p, n2o, env)
            rec2 = False
            if n2["rc"] == 0 and os.path.isfile(n2o):
                t2 = run([args.upx, "-t", "-q", n2o], env)
                un2 = os.path.join(d, "n2.unpacked")
                u2 = run([args.upx, "-d", "-q", "-o", un2, n2o], env)
                rec2 = (t2["rc"] == 0 and u2["rc"] == 0 and os.path.isfile(un2)
                        and sha256_file(un2) == c["sha256"])
            controls["N2-corrupt-payload"].append({"carrier": c["id"], "flipped_offset": mid,
                                                   "repair_rc": n2["rc"], "recovered": rec2})
        recovered = sum(1 for k in cases if k["recovered"])
        ctl_ok = {
            "N1-refuse-plain": all(x["refused"] for x in controls["N1-refuse-plain"]),
            "N2-corrupt-payload": not any(x["recovered"] for x in controls["N2-corrupt-payload"]),
            "N3-intact-idempotent": all(x["identical"] for x in controls["N3-intact-idempotent"]),
        }
        met = recovered == TARGET and all(ctl_ok.values())
        receipt = {"tool": TOOL, "tool_sha256": sha256_file(os.path.abspath(__file__)),
                   "repair_cmd": args.repair_cmd if repair in BUILTINS else os.path.relpath(repair, args.root),
                   "repair_sha256": repair_sha, "preflight": pre, "rea_enabled": rea_on,
                   "target": TARGET, "recovered": recovered,
                   "label": f"recovered {recovered} of {TARGET}",
                   "controls": controls, "controls_ok": ctl_ok, "met_target": met,
                   "cases": cases}
        return (0 if met else 1), receipt
    finally:
        shutil.rmtree(run_root, ignore_errors=True)


def selftest() -> int:
    fails = []

    def check(name, cond):
        if not cond:
            fails.append(name)
    p = b"\x7fELF" + b"A" * 20 + MAGIC + b"B" * 20 + MAGIC + b"C" * 32 + MAGIC + b"D" * 32
    t1 = tamper(p, TAMPERS["T1-zero"])
    check("tamper-removes-all-magic", MAGIC not in t1 and len(t1) == len(p))
    check("windows-only-accepts-restore", windows_only(t1, p)[0])
    bad = bytearray(p); bad[2] ^= 1
    check("windows-only-refuses-outside-byte", not windows_only(t1, bytes(bad))[0])
    check("windows-only-refuses-length", not windows_only(t1, p + b"x")[0])
    check("identity-builtin-noop", builtin_repair("identity", t1) == t1)
    t2 = tamper(p, TAMPERS["T2-foreign"])
    check("naive-global-fixes-foreign", builtin_repair("naive-global", t2) == p)
    check("naive-global-breaks-zero", builtin_repair("naive-global", t1 + b"\0" * 4) != p + b"\0" * 4)
    check("target-is-eight", TARGET == 8)
    print(f"SELFTEST cases=8 failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd")
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--pkg", default="")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--evidence-dir", default="")
    ap.add_argument("--no-rea", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.repair_cmd or not a.work or not a.json_out:
        print("could-not-evaluate: --repair-cmd, --work and --json-out are required", file=sys.stderr)
        return 2
    if a.evidence_dir:
        os.makedirs(a.evidence_dir, exist_ok=True)
    try:
        rc, receipt = score(a)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
        rc = 2
    receipt["exit"] = rc
    with open(a.json_out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
    print(f"{receipt.get('label', receipt.get('unevaluable'))} controls_ok={receipt.get('controls_ok')} "
          f"met={receipt['met_target']} exit={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
