#!/usr/bin/env python3
"""upx-field-battery.py - round-89 counter (R89-C1, coverage, capability).

Population: four pinned carriers (jq, xxd, libz.so, docker-init), each packed by
the pinned packer (`upx 5.2.0`, sha256 `cf2f6e7c…`) and then tampered in class
`T4-chain-szcpr-wrong`: block 0's `b_info.sz_cpr` is overwritten with an
in-range but WRONG value (`stored - 8`, or `stored + 8` when `stored <= 8`).
Every bound the packer applies to the field passes, so the precondition arm
requires `upx -t` to fail on the tampered file anyway (`compressed data
violation`): a tamper the packer tolerates is not this class.

A case is RECOVERED iff all five arms hold:
  repair_rc0   the repair exits 0 and writes an output
  field_only   every differing byte lies inside block 0's 4-byte `sz_cpr` window
  test_ok      `upx -t` accepts the repaired file
  identity     `upx -d` of the repaired file hashes to the pinned carrier
  rea_recover  REA's procedure count of the unpacked file equals the declared one

Controls in every run (all must hold for met):
  N1-refuse-plain      the repair exits non-zero on each pinned ORIGINAL: 4/4
  N2-corrupt-payload   the class tamper plus one flipped byte at len//2 is not
                       recovered (any arm false on each carrier)
  N3-intact-idempotent the untampered packed file: repair exits 0 and the
                       output is byte-identical to the input

Answer isolation (round-88 M88-8 / QUALITY 158): every repair invocation runs in
its own private directory that holds the single input file and nothing else; the
receipt records the directory listing each invocation saw, and the `isolation`
control requires it to be exactly one path.

met_target: recovered == --expect-recovered (a required argument, QUALITY 157),
all three controls, the isolation control and the round-88 class regression arm
(the frozen round-88 counter, same repair, `recovered 4 of 4`).
Exit: 0 met; 1 not met (every false arm named; receipt written); 2 unevaluable.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile

TOOL = "tools/round-89/upx-field-battery.py"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
REA_VERSION = "6.5.0"
REA_PKGJSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
CLASS = "T4-chain-szcpr-wrong"
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
ARMS = ("repair_rc0", "field_only", "test_ok", "identity", "rea_recover")
BUILTINS = ("identity", "naive-global", "r87-anchor", "r88-repair")
R87_REPAIR = "tools/round-87/upx-magic-repair.py"
R88_REPAIR = "tools/round-88/upx-chain-repair.py"
R88_COUNTER = "tools/round-88/upx-chain-battery.py"


class Unevaluable(Exception):
    pass


class _Refused(Exception):
    def __init__(self, rc, tail):
        super().__init__(f"refused rc={rc} {tail}")
        self.rc, self.tail = rc, tail


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def child_env(work: str) -> dict:
    return {"HOME": os.path.join(work, "home"), "LANG": "C",
            "PATH": os.environ.get("PATH") or "/usr/bin",
            "TMPDIR": os.path.join(work, "tmp")}


def run(argv: list, env: dict, timeout: int = 900) -> dict:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=env,
                           timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"argv": argv, "rc": None,
                "error": f"{exc.__class__.__name__}: {exc}"}
    tail = (p.stdout + p.stderr).strip().splitlines()
    return {"argv": argv, "rc": p.returncode, "tail": tail[-2:],
            "stdout": p.stdout}


def first_block(packed: bytes, rep) -> int:
    ph_off, ph = rep.find_packheader(packed)
    m, _s, _w = rep.find_linfo(packed, ph_off, ph)
    return m + 20


def tamper_field(packed: bytes, b0: int) -> tuple[bytes, dict]:
    """Class T4: an in-range but wrong `sz_cpr` (never the true value)."""
    sz_unc, sz_cpr = struct.unpack_from("<II", packed, b0)
    if sz_cpr == 0 or sz_cpr > sz_unc:
        raise Unevaluable(f"packer produced a non-plain block0 at {b0}")
    wrong = sz_cpr - 8 if sz_cpr > 8 else sz_cpr + 8
    if not (0 < wrong <= sz_unc) or wrong == sz_cpr:
        raise Unevaluable(f"no in-range wrong value for sz_cpr {sz_cpr}")
    out = bytearray(packed)
    out[b0 + 4:b0 + 8] = struct.pack("<I", wrong)
    return bytes(out), {"true_sz_cpr": sz_cpr, "wrong_sz_cpr": wrong,
                        "delta": wrong - sz_cpr}


def field_only(tampered: bytes, out: bytes, b0: int) -> tuple[bool, str]:
    """Every differing byte lies inside block 0's 4-byte sz_cpr window."""
    if len(tampered) != len(out):
        return False, f"length {len(out)} != {len(tampered)}"
    lo, hi = b0 + 4, b0 + 8
    for i, (a, b) in enumerate(zip(tampered, out)):
        if a != b and not (lo <= i < hi):
            return False, f"byte {i} changed outside the sz_cpr window {lo}-{hi}"
    return True, ""


def builtin_repair(name: str, data: bytes, root: str) -> bytes:
    if name == "identity":
        return data
    if name == "naive-global":
        if len(data) < 36:
            return data
        word = data[-36:-32]
        return data.replace(word, b"UPX!") if word else data
    if name in ("r87-anchor", "r88-repair"):
        with tempfile.TemporaryDirectory() as td:
            src, dst = os.path.join(td, "in"), os.path.join(td, "out")
            with open(src, "wb") as fh:
                fh.write(data)
            tool = R87_REPAIR if name == "r87-anchor" else R88_REPAIR
            r = run([sys.executable, "-I", "-B",
                     os.path.join(os.path.abspath(root), tool), "--in", src,
                     "--out", dst], child_env(td), timeout=300)
            if r["rc"] != 0 or not os.path.isfile(dst):
                raise _Refused(r["rc"], r.get("tail"))
            with open(dst, "rb") as fh:
                return fh.read()
    raise ValueError(name)


def apply_repair(cmd: str, data: bytes, env: dict, root: str,
                 private_root: str) -> dict:
    """Run the repair in a private directory that holds the input alone."""
    box = tempfile.mkdtemp(prefix="inv-", dir=private_root)
    src, dst = os.path.join(box, "in"), os.path.join(box, "out")
    with open(src, "wb") as fh:
        fh.write(data)
    before = sorted(os.listdir(box))
    if cmd in BUILTINS:
        try:
            out = builtin_repair(cmd, data, root)
        except _Refused as exc:
            return {"argv": ["<builtin>", cmd], "rc": exc.rc, "tail": exc.tail,
                    "box": before, "output": None}
        with open(dst, "wb") as fh:
            fh.write(out)
        rec = {"argv": ["<builtin>", cmd], "rc": 0}
    else:
        rec = run([sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst],
                  env, timeout=300)
    out = None
    if rec["rc"] == 0 and os.path.isfile(dst):
        with open(dst, "rb") as fh:
            out = fh.read()
    rec.update({"box": before, "output": out})
    return rec


def rea_procedures(pkg: str, path: str, env: dict, out_json: str) -> tuple[int | None, dict]:
    rec = run(["node", os.path.join(pkg, "scripts", "rea.mjs"), "analyze",
               "--format", "json", path], env)
    try:
        envl = json.loads(rec.get("stdout") or "{}")
    except json.JSONDecodeError:
        envl = {}
    norm = envl.get("normalized_result") if isinstance(envl, dict) else None
    counts = None
    if isinstance(norm, dict):
        counts = {k: norm.get(k) for k in ("procedure_count", "segment_count",
                                           "string_count")}
    with open(out_json, "w", encoding="utf-8") as fh:
        json.dump({"argv": rec["argv"], "rc": rec["rc"], "counts": counts,
                   "evidence_id": envl.get("evidence_id")
                   if isinstance(envl, dict) else None},
                  fh, indent=1, sort_keys=True)
    pc = counts.get("procedure_count") if counts else None
    return (pc if isinstance(pc, int) else None), {"rc": rec["rc"], "counts": counts}


def preflight(upx: str, pkg: str, env: dict, repair: str, rea_on: bool,
              root: str) -> dict:
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
    for rel in (R87_REPAIR, R88_REPAIR, R88_COUNTER):
        if not os.path.isfile(os.path.join(os.path.abspath(root), rel)):
            raise Unevaluable(f"missing_module: {rel}")
    return {"upx": upx, "sha256": sha, "version": ver[0],
            "rea_pkg": pkg if rea_on else None,
            "r87_module_sha256": sha256_file(os.path.join(os.path.abspath(root), R87_REPAIR)),
            "r88_module_sha256": sha256_file(os.path.join(os.path.abspath(root), R88_REPAIR)),
            "r88_counter_sha256": sha256_file(os.path.join(os.path.abspath(root), R88_COUNTER))}


def score(args) -> tuple[int, dict]:
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: {work}")
    run_root = tempfile.mkdtemp(prefix="r89-battery-", dir=work)
    env = child_env(run_root)
    os.makedirs(env["HOME"])
    os.makedirs(env["TMPDIR"])
    private_root = os.path.join(run_root, "invocations")
    os.makedirs(private_root)
    rea_on = not args.no_rea
    repair = args.repair_cmd if args.repair_cmd in BUILTINS \
        else os.path.abspath(args.repair_cmd)
    root = os.path.abspath(args.root)
    try:
        pre = preflight(args.upx, args.pkg, env, repair, rea_on, root)
        rep = load_module(os.path.join(root, R87_REPAIR), "r87repair")
        repair_sha = None if repair in BUILTINS else sha256_file(repair)
        cases, controls = [], {"N1-refuse-plain": [], "N2-corrupt-payload": [],
                               "N3-intact-idempotent": [], "isolation": []}
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
            b0 = first_block(pbytes, rep)
            n1 = apply_repair(repair, open(orig, "rb").read(), env, root, private_root)
            controls["N1-refuse-plain"].append({"carrier": c["id"], "rc": n1["rc"],
                                                "refused": n1["rc"] != 0})
            controls["isolation"].append({"carrier": c["id"], "n1_box": n1["box"]})
            n3 = apply_repair(repair, pbytes, env, root, private_root)
            same = n3["rc"] == 0 and n3["output"] is not None \
                and sha256_bytes(n3["output"]) == sha256_bytes(pbytes)
            controls["N3-intact-idempotent"].append({"carrier": c["id"], "rc": n3["rc"],
                                                     "identical": same})
            tb, tinfo = tamper_field(pbytes, b0)
            tp = os.path.join(d, "field.tampered")
            with open(tp, "wb") as fh:
                fh.write(tb)
            pre_t = run([args.upx, "-t", "-q", tp], env)
            if pre_t["rc"] == 0:
                raise Unevaluable(f"tamper_ineffective: {c['id']} (packer tolerated the wrong value)")
            case = {"carrier": c["id"], "class": CLASS, "block0": b0,
                    "packed_sha256": sha256_bytes(pbytes),
                    "tampered_sha256": sha256_bytes(tb), "tamper": tinfo,
                    "precondition": {"upx_t_rc": pre_t["rc"],
                                     "tail": pre_t.get("tail")}}
            rr = apply_repair(repair, tb, env, root, private_root)
            case["invocation_box"] = rr["box"]
            arms = dict.fromkeys(ARMS, False)
            why = {}
            arms["repair_rc0"] = rr["rc"] == 0 and rr["output"] is not None
            if not arms["repair_rc0"]:
                why["repair_rc0"] = f"rc {rr['rc']} {rr.get('tail')}"
            else:
                ob = rr["output"]
                case["repaired_sha256"] = sha256_bytes(ob)
                case["repaired_equals_packed"] = ob == pbytes
                arms["field_only"], w = field_only(tb, ob, b0)
                if w:
                    why["field_only"] = w
                outp = os.path.join(d, "field.repaired")
                with open(outp, "wb") as fh:
                    fh.write(ob)
                t = run([args.upx, "-t", "-q", outp], env)
                arms["test_ok"] = t["rc"] == 0
                if not arms["test_ok"]:
                    why["test_ok"] = f"rc {t['rc']} {t.get('tail')}"
                un = os.path.join(d, "field.unpacked")
                u = run([args.upx, "-d", "-q", "-o", un, outp], env)
                usha = sha256_file(un) if u["rc"] == 0 and os.path.isfile(un) else None
                case["unpacked_sha256"] = usha
                arms["identity"] = usha == c["sha256"]
                if not arms["identity"]:
                    why["identity"] = f"rc {u['rc']} sha {usha}"
                if arms["identity"] and rea_on:
                    rj = os.path.join(args.evidence_dir, f"rea-{c['id']}-{CLASS}.json") \
                        if args.evidence_dir else os.path.join(d, "field.rea.json")
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
            t2 = bytearray(tb)
            mid = len(t2) // 2
            t2[mid] ^= 0xFF
            n2 = apply_repair(repair, bytes(t2), env, root, private_root)
            rec2 = False
            if n2["rc"] == 0 and n2["output"] is not None:
                n2p = os.path.join(d, "n2.out")
                with open(n2p, "wb") as fh:
                    fh.write(n2["output"])
                tt = run([args.upx, "-t", "-q", n2p], env)
                un2 = os.path.join(d, "n2.unpacked")
                u2 = run([args.upx, "-d", "-q", "-o", un2, n2p], env)
                rec2 = (tt["rc"] == 0 and u2["rc"] == 0 and os.path.isfile(un2)
                        and sha256_file(un2) == c["sha256"])
            controls["N2-corrupt-payload"].append({"carrier": c["id"],
                                                   "flipped_offset": mid,
                                                   "repair_rc": n2["rc"],
                                                   "recovered": rec2})
        recovered = sum(1 for k in cases if k["recovered"])
        iso_ok = all(x["n1_box"] == ["in"] for x in controls["isolation"])
        ctl_ok = {
            "N1-refuse-plain": all(x["refused"] for x in controls["N1-refuse-plain"]),
            "N2-corrupt-payload": not any(x["recovered"] for x in controls["N2-corrupt-payload"]),
            "N3-intact-idempotent": all(x["identical"] for x in controls["N3-intact-idempotent"]),
            "isolation": iso_ok,
        }
        reg_json = os.path.join(run_root, "r88-regression.json")
        reg = run([sys.executable, "-I", "-B",
                   os.path.join(root, R88_COUNTER), "--root", root,
                   "--repair-cmd", repair, "--upx", args.upx, "--pkg", args.pkg,
                   "--work", run_root, "--json-out", reg_json]
                  + (["--no-rea"] if not rea_on else []), env)
        regression = {"rc": reg["rc"], "tail": reg.get("tail"), "met": False}
        if os.path.isfile(reg_json):
            with open(reg_json, encoding="utf-8") as fh:
                r88 = json.load(fh)
            regression.update({"recovered": r88.get("recovered"),
                               "target": r88.get("target"),
                               "controls_ok": r88.get("controls_ok"),
                               "met": bool(r88.get("met_target"))
                               and r88.get("recovered") == r88.get("target")})
        met = (recovered == args.expect_recovered and all(ctl_ok.values())
               and regression["met"])
        receipt = {"tool": TOOL, "tool_sha256": sha256_file(os.path.abspath(__file__)),
                   "repair_cmd": args.repair_cmd if repair in BUILTINS
                   else os.path.relpath(repair, root),
                   "repair_sha256": repair_sha, "preflight": pre,
                   "rea_enabled": rea_on, "class": CLASS,
                   "target": args.expect_recovered, "population": len(CARRIERS),
                   "recovered": recovered,
                   "label": f"recovered {recovered} of {len(CARRIERS)}",
                   "controls": controls, "controls_ok": ctl_ok,
                   "regression": regression, "met_target": met, "cases": cases}
        return (0 if met else 1), receipt
    finally:
        shutil.rmtree(run_root, ignore_errors=True)


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    t = bytearray(b"0123456789abcdefghij")
    t[4:8] = struct.pack("<I", 3)
    ok = bytearray(t)
    ok[4:8] = struct.pack("<I", 7)
    check("field-only-accepts-window", field_only(bytes(t), bytes(ok), 0)[0])
    bad = bytearray(ok)
    bad[9] ^= 1
    check("field-only-refuses-outside", not field_only(bytes(t), bytes(bad), 0)[0])
    check("field-only-refuses-length", not field_only(bytes(t), bytes(ok) + b"x", 0)[0])
    check("identity-builtin-noop", builtin_repair("identity", bytes(t), ".") == bytes(t))
    check("class-name", CLASS == "T4-chain-szcpr-wrong")
    check("arms-five", len(ARMS) == 5)
    # tamper_field on a synthetic block: struct <II at offset 0 of the window
    synth = bytearray(64)
    struct.pack_into("<II", synth, 0, 400, 200)
    tb, ti = tamper_field(bytes(synth), 0)
    check("tamper-wrong-value", ti["wrong_sz_cpr"] == 192 and ti["delta"] == -8)
    check("tamper-in-range", 0 < ti["wrong_sz_cpr"] <= 400)
    check("tamper-changes-window-only",
          tb[:4] == bytes(synth[:4]) and tb[8:] == bytes(synth[8:]))
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
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
    ap.add_argument("--expect-recovered", type=int)
    ap.add_argument("--no-rea", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    missing = [k for k in ("repair_cmd", "work", "json_out", "expect_recovered")
               if getattr(a, k) in (None, "")]
    if missing:
        print(f"could-not-evaluate: --{', --'.join(m.replace('_', '-') for m in missing)} "
              "are required", file=sys.stderr)
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
    print(f"{receipt.get('label', receipt.get('unevaluable'))} "
          f"controls_ok={receipt.get('controls_ok')} met={receipt['met_target']} exit={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
