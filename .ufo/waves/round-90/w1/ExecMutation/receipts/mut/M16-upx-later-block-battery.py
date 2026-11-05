#!/usr/bin/env python3
"""upx-later-block-battery.py - round-90 counter (R90-C1, coverage, capability).

Scores a repair command on three populations built from the four pinned
carriers (UPX 5.2.0 `--best`, little-endian ELF x86-64):

  P1-later-block   an *interior* first-segment block's `sz_cpr` overwritten with
                   a different in-range value, both directions (stored - 7 and
                   stored + 7), on the carriers whose chain accounts the full
                   `u_len` (jq, xxd, docker-init) -> 6 cells
  P2-first-block   block 0's `sz_cpr` overwritten (round-89 class), 4 carriers
  P3-zeroed        block 0's `sz_cpr` zeroed (round-88 class), 4 carriers

A cell is `recovered` only when all of: the repair exits 0, every differing byte
lies inside the tampered 4-byte window, `upx -t` answers rc 0, `upx -d` produces
bytes whose sha256 equals the carrier pin, and REA 6.5.0 reports the original's
own procedure/segment/string counts for the unpacked bytes.

Controls, all required for `met`:
  N1-refuse-plain      a plain ELF input is refused (rc != 0)
  N2-corrupt-payload   a flipped payload byte is never reported recovered
  N3-intact-idempotent an intact packed carrier comes back byte-identical
  isolation            each invocation's directory is listed *after* the child
                       exits and holds exactly ["in"] (QUALITY 170)
  carrier_blind        the six P1 cells are re-scored inside a bwrap sandbox in
                       which every pinned carrier path holds decoy bytes and the
                       counter's run root is a tmpfs, and the probe proves the
                       blinding took effect (QUALITY 168)
  no-work              the unchanged round-89 repair on P1 (do-nothing control)
  cheat-repack         the provenance cheat: live unblinded (must reproduce the
                       intact packed bytes) and killed blinded

`met` = P1 6 of 6, P2 4 of 4, P3 4 of 4, every control true, and `--expect`
matching the label.  The PackHeader `u_len` is enforced as a *filter* inside the
repair for this class, not as a rank key (QUALITY 171).
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

TOOL = "tools/round-90/upx-later-block-battery.py"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
REA_PKGJSON_SHA256 = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
CLASS = "T5-chain-szcpr-wrong-later"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq",
     "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806",
     "p1": True},
    {"id": "xxd", "source": "/usr/bin/xxd",
     "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65",
     "p1": True},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2",
     "sha256": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9",
     "p1": False},
    {"id": "dinit", "source": "/usr/bin/docker-init",
     "sha256": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115",
     "p1": True},
]
DECLARED_ORIG = {"jq": 167, "xxd": 99, "libz": 184, "dinit": 1268}
R87_REPAIR = "tools/round-87/upx-magic-repair.py"
R88_REPAIR = "tools/round-88/upx-chain-repair.py"
R89_REPAIR = "tools/round-89/upx-field-value-repair.py"
CHEAT = "tools/round-90/control-cheat-repack.py"
BUILTINS = ("r89-repair",)
DIRECTIONS = (-7, 7)


class Unevaluable(Exception):
    pass


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
        return {"argv": argv, "rc": None, "error": f"{exc.__class__.__name__}: {exc}"}
    tail = (p.stdout + p.stderr).strip().splitlines()
    return {"argv": argv, "rc": p.returncode, "tail": tail[-2:], "stdout": p.stdout}


def layout(packed: bytes, rep, r88) -> tuple[int, list]:
    """(b0, first-segment blocks) for the packed bytes."""
    ph_off, ph = rep.find_packheader(packed)
    best = (None, [])
    for m in r88.l_info_candidates(packed, ph_off, ph):
        b0 = m + 20
        sz_unc0, _ = struct.unpack_from("<II", packed, b0)
        if sz_unc0 == 0:
            continue
        method = packed[b0 + 8]
        q, blocks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", packed, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off \
                    or packed[q + 8] not in (method, ph["method"]):
                break
            blocks.append({"block": q, "sz_unc": su, "sz_cpr": sc})
            q += 12 + sc
        if len(blocks) > len(best[1]):
            best = (b0, blocks)
    return best


def tamper(packed: bytes, block: dict, value: int) -> bytes:
    out = bytearray(packed)
    struct.pack_into("<I", out, block["block"] + 4, value)
    return bytes(out)


def window_only(tampered: bytes, out: bytes, block: dict) -> tuple[bool, str]:
    """Every differing byte lies inside the tampered block's sz_cpr window."""
    if len(tampered) != len(out):
        return False, f"length {len(out)} != {len(tampered)}"
    lo, hi = block["block"] + 4, block["block"] + 12
    for i, (a, b) in enumerate(zip(tampered, out)):
        if a != b and not (lo <= i < hi):
            return False, f"byte {i} changed outside {lo}-{hi}"
    return True, ""


def rea_counts(pkg: str, path: str, env: dict, out_json: str) -> dict:
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
                   if isinstance(envl, dict) else None}, fh, indent=1, sort_keys=True)
    return {"rc": rec["rc"], "counts": counts}


def invoke(cmd: str, data: bytes, env: dict, boxes: str, blind=None) -> dict:
    """Run the repair on `data` in a private box that holds the input alone."""
    box = tempfile.mkdtemp(prefix="inv-", dir=boxes)
    src, dst = os.path.join(box, "in"), os.path.join(box, "out")
    with open(src, "wb") as fh:
        fh.write(data)
    if blind is not None:
        argv = ["bwrap", "--dev-bind", "/", "/", "--tmpfs", blind["hide"]]
        for path in blind["paths"]:
            argv += ["--bind", blind["decoy"], path]
        argv += ["--", sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst]
    else:
        argv = [sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst]
    rec = run(argv, env, timeout=600)
    after = sorted(os.listdir(box))           # QUALITY 170: list after the child
    out = None
    if rec["rc"] == 0 and os.path.isfile(dst):
        with open(dst, "rb") as fh:
            out = fh.read()
    rec.update({"box_after": after, "output": out, "blinded": blind is not None})
    return rec


def score_case(cmd, tampered, intact_packed, block, orig_sha, env, boxes, pkg,
               rea_on, blind=None, orig_path=None, orig_counts=None) -> dict:
    rec = invoke(cmd, tampered, env, boxes, blind)
    out = rec.get("output")
    arms = {"repair_rc0": rec["rc"] == 0 and out is not None,
            "field_only": False, "test_ok": False, "identity": False,
            "unpack_pin": False, "rea_recover": None}
    row = {"tampered_block": block["block"], "stored_sz_cpr": block["sz_cpr"],
           "rc": rec["rc"], "box_after": rec.get("box_after"),
           "blinded": rec.get("blinded")}
    if arms["repair_rc0"]:
        ok, why = window_only(tampered, out, block)
        arms["field_only"] = ok
        arms["identity"] = sha256_bytes(out) == sha256_bytes(intact_packed)
        rp = tempfile.mkstemp(prefix="cand-", dir=boxes)[1]
        with open(rp, "wb") as fh:
            fh.write(out)
        arms["test_ok"] = run(["/usr/bin/upx", "-t", "-q", rp], env)["rc"] == 0
        up = rp + ".unpacked"
        r = run(["/usr/bin/upx", "-d", "-q", "-o", up, rp], env)
        if r["rc"] == 0 and os.path.isfile(up):
            arms["unpack_pin"] = sha256_file(up) == orig_sha
            if rea_on and arms["unpack_pin"] and orig_counts is not None:
                got = rea_counts(pkg, up, env, up + ".rea.json")
                arms["rea_recover"] = (got["counts"] is not None
                                       and got["counts"] == orig_counts)
        row["detail"] = why
    row["arms"] = arms
    row["recovered"] = all(v is True for v in arms.values() if v is not None) and \
        (arms["rea_recover"] in (True, None))
    return row


def preflight(args, root: str, env: dict) -> dict:
    if not os.path.isfile(args.upx) or sha256_file(args.upx) != UPX_SHA256_PIN:
        raise Unevaluable("packer_mismatch: upx pin")
    ver = run([args.upx, "--version"], env).get("stdout", "").strip().splitlines()
    if not ver or ver[0] != UPX_VERSION_PIN:
        raise Unevaluable(f"packer_mismatch: version {ver[:1]}")
    if not args.no_rea:
        pj = os.path.join(args.pkg, "package.json")
        if not os.path.isfile(pj) or sha256_file(pj) != REA_PKGJSON_SHA256:
            raise Unevaluable(f"rea_pin: {pj}")
        if shutil.which("node") is None:
            raise Unevaluable("missing_tool: node")
    if not args.no_rea and not os.path.isdir(args.pkg):
        raise Unevaluable(f"rea_pkg_missing: {args.pkg}")
    for c in CARRIERS:
        if not os.path.isfile(c["source"]) or sha256_file(c["source"]) != c["sha256"]:
            raise Unevaluable(f"carrier_pin: {c['id']}")
    if shutil.which("bwrap") is None:
        raise Unevaluable("missing_tool: bwrap (carrier-blind arm)")
    for rel in (R87_REPAIR, R88_REPAIR, R89_REPAIR, CHEAT):
        if not os.path.isfile(os.path.join(root, rel)):
            raise Unevaluable(f"missing_module: {rel}")
    return {"upx": args.upx, "upx_sha256": sha256_file(args.upx),
            "upx_version": ver[0], "rea_pkg": None if args.no_rea else args.pkg,
            "modules": {rel: sha256_file(os.path.join(root, rel))
                        for rel in (R87_REPAIR, R88_REPAIR, R89_REPAIR, CHEAT)},
            "bwrap": shutil.which("bwrap")}


def score(args) -> tuple[int, dict]:
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: {work}")
    root = os.path.abspath(args.root)
    run_root = tempfile.mkdtemp(prefix="r90-battery-", dir=work)
    boxes = tempfile.mkdtemp(prefix="r90-boxes-", dir=work)   # outside run_root
    env = child_env(run_root)
    os.makedirs(env["HOME"])
    os.makedirs(env["TMPDIR"])
    rea_on = not args.no_rea
    repair = args.repair_cmd
    if repair in BUILTINS:
        repair = os.path.join(root, R89_REPAIR)
    elif not os.path.isfile(repair):
        raise Unevaluable(f"missing_repair: {repair}")
    cheat = os.path.join(root, CHEAT)
    pins = preflight(args, root, env)
    rep = load_module(os.path.join(root, R87_REPAIR), "r87repair")
    r88 = load_module(os.path.join(root, R88_REPAIR), "r88repair")
    decoy = os.path.join(boxes, "decoy")
    with open(decoy, "wb") as fh:
        fh.write(b"decoy-not-a-carrier\n" * 64)
    # bwrap refuses a bind whose destination is a symlink, so a carrier that is
    # one is blinded through its resolved target (the symlink then resolves to
    # the decoy inside the sandbox).
    blind_paths = []
    for c in CARRIERS:
        real = os.path.realpath(c["source"])
        if real not in blind_paths:
            blind_paths.append(real)
    blind = {"decoy": decoy, "hide": run_root, "paths": blind_paths}
    controls = {"N1-refuse-plain": [], "N2-corrupt-payload": [],
                "N3-intact-idempotent": [], "isolation": [],
                "carrier_blind": {"blind_ok": None, "probe": None, "cases": []},
                "no_work": {"cases": [], "recovered": None},
                "cheat_repack": {"unblinded": None, "blinded": None}}
    cases = {"P1-later-block": [], "P2-first-block": [], "P3-zeroed": []}
    try:
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
            orig_sha = sha256_file(orig)
            orig_counts = (rea_counts(args.pkg, orig, env,
                                      os.path.join(boxes, f"rea-orig-{c['id']}.json")
                                      )["counts"] if rea_on else None)
            _b0, blocks = layout(pbytes, rep, r88)
            if len(blocks) < 3:
                raise Unevaluable(f"too_few_blocks: {c['id']} {len(blocks)}")
            n3 = invoke(repair, pbytes, env, boxes)
            controls["N3-intact-idempotent"].append(
                {"carrier": c["id"], "rc": n3["rc"],
                 "identical": n3.get("output") == pbytes})
            n1 = invoke(repair, open(orig, "rb").read(), env, boxes)
            controls["N1-refuse-plain"].append({"carrier": c["id"], "rc": n1["rc"],
                                                "refused": n1["rc"] not in (0, None)})
            # N2: flip a byte inside block 1's compressed payload
            corrupt = bytearray(pbytes)
            at = blocks[1]["block"] + 12 + blocks[1]["sz_cpr"] // 2
            corrupt[at] ^= 0xFF
            n2 = invoke(repair, bytes(corrupt), env, boxes)
            clean = None
            if n2["rc"] == 0 and n2.get("output") is not None:
                rp = os.path.join(boxes, "n2.out")
                with open(rp, "wb") as fh:
                    fh.write(n2["output"])
                clean = run([args.upx, "-t", "-q", rp], env)["rc"] == 0
            controls["N2-corrupt-payload"].append(
                {"carrier": c["id"], "rc": n2["rc"], "packer_clean": clean,
                 "not_recovered": not (n2["rc"] == 0 and clean)})
            for rec in (n1, n2, n3):
                # QUALITY 170: the listing is taken after the child exits; the
                # only entries allowed are the input and the repair's own output.
                after = rec.get("box_after") or []
                controls["isolation"].append(
                    {"carrier": c["id"], "box_after": after,
                     "ok": sorted(after) in (["in"], ["in", "out"])})
            # P1 on the carriers whose chain accounts the full u_len
            if c["p1"]:
                blk = blocks[1]
                for delta in DIRECTIONS:
                    value = blk["sz_cpr"] + delta
                    if not (0 < value <= blk["sz_unc"]):
                        continue
                    t = tamper(pbytes, blk, value)
                    row = score_case(repair, t, pbytes, {**blk, "sz_cpr": value},
                                     orig_sha, env, boxes, args.pkg, rea_on,
                                     orig_path=orig, orig_counts=orig_counts)
                    row["carrier"] = c["id"]
                    row["direction"] = delta
                    cases["P1-later-block"].append(row)
                    nw = score_case(os.path.join(root, R89_REPAIR), t, pbytes,
                                    {**blk, "sz_cpr": value}, orig_sha, env, boxes,
                                    args.pkg, False)
                    controls["no_work"]["cases"].append(
                        {"carrier": c["id"], "direction": delta,
                         "recovered": nw["recovered"], "rc": nw["rc"]})
            # P2: block 0 wrong (round-89 class); P3: block 0 zeroed (round-88 class)
            b0blk = blocks[0]
            for label, value in (("P2-first-block", b0blk["sz_cpr"] - 7),
                                 ("P3-zeroed", 0)):
                if label == "P2-first-block" and not (0 < value <= b0blk["sz_unc"]):
                    continue
                t = tamper(pbytes, b0blk, value)
                row = score_case(repair, t, pbytes, {**b0blk, "sz_cpr": value},
                                 orig_sha, env, boxes, args.pkg, rea_on,
                                 orig_path=orig, orig_counts=orig_counts)
                row["carrier"] = c["id"]
                cases[label].append(row)
        # carrier-blind arm: prove the blinding, then re-score P1
        pr = run(["bwrap", "--dev-bind", "/", "/", "--tmpfs", run_root]
                 + sum([["--bind", decoy, p] for p in blind["paths"]], [])
                 + ["--", sys.executable, "-c",
                    "import hashlib,sys\n"
                    "print(' '.join(hashlib.sha256(open(p,'rb').read()).hexdigest()"
                    " for p in sys.argv[1:]))"] + blind["paths"], env)
        want = sha256_file(decoy)
        seen = (pr.get("stdout") or "").split()
        controls["carrier_blind"]["probe"] = {"rc": pr["rc"], "seen": seen,
                                              "decoy_sha256": want,
                                              "tail": pr.get("tail")}
        controls["carrier_blind"]["blind_ok"] = pr["rc"] == 0 and seen == [want] * len(
            blind["paths"])
        if controls["carrier_blind"]["blind_ok"]:
            for c in CARRIERS:
                if not c["p1"]:
                    continue
                d = os.path.join(run_root, c["id"])
                pbytes = open(os.path.join(d, "packed"), "rb").read()
                _b0, blocks = layout(pbytes, rep, r88)
                blk = blocks[1]
                for delta in DIRECTIONS:
                    value = blk["sz_cpr"] + delta
                    if not (0 < value <= blk["sz_unc"]):
                        continue
                    t = tamper(pbytes, blk, value)
                    row = score_case(repair, t, pbytes, {**blk, "sz_cpr": value},
                                     sha256_file(os.path.join(d, "orig")), env, boxes,
                                     args.pkg, False, blind)
                    row["carrier"] = c["id"]
                    row["direction"] = delta
                    controls["carrier_blind"]["cases"].append(row)
        # the cheat: live unblinded on the first P1 cell, then killed blinded
        c0 = CARRIERS[0]
        d0 = os.path.join(run_root, c0["id"])
        p0 = open(os.path.join(d0, "packed"), "rb").read()
        _b, blocks0 = layout(p0, rep, r88)
        blk0 = blocks0[1]
        t0 = tamper(p0, blk0, blk0["sz_cpr"] - 7)
        live = score_case(cheat, t0, p0, {**blk0, "sz_cpr": blk0["sz_cpr"] - 7},
                          sha256_file(os.path.join(d0, "orig")), env, boxes,
                          args.pkg, False)
        killed = score_case(cheat, t0, p0, {**blk0, "sz_cpr": blk0["sz_cpr"] - 7},
                            sha256_file(os.path.join(d0, "orig")), env, boxes,
                            args.pkg, False, blind)
        controls["cheat_repack"]["unblinded"] = live["recovered"]
        controls["cheat_repack"]["blinded"] = killed["recovered"]
    except Unevaluable:
        raise
    p1 = cases["P1-later-block"]
    p2 = cases["P2-first-block"]
    p3 = cases["P3-zeroed"]
    controls["no_work"]["recovered"] = sum(1 for x in controls["no_work"]["cases"]
                                           if x["recovered"])
    arms_ok = {
        "N1": all(x["refused"] for x in controls["N1-refuse-plain"]),
        "N2": all(x["not_recovered"] for x in controls["N2-corrupt-payload"]),
        "N3": all(x["identical"] for x in controls["N3-intact-idempotent"]),
        "isolation": all(x["ok"] for x in controls["isolation"]),
        "carrier_blind": bool(controls["carrier_blind"]["blind_ok"]) and
        all(x["recovered"] for x in controls["carrier_blind"]["cases"]) and
        len(controls["carrier_blind"]["cases"]) == len(p1),
        "no_work": controls["no_work"]["recovered"] == 0,
        "cheat_live": controls["cheat_repack"]["unblinded"] is True,
        "cheat_killed": controls["cheat_repack"]["blinded"] is False,
    }
    recovered = {"P1": sum(1 for x in p1 if x["recovered"]), "P2": sum(1 for x in p2 if x["recovered"]),
                 "P3": sum(1 for x in p3 if x["recovered"])}
    label = (f"P1 {recovered['P1']} of {len(p1)}; P2 {recovered['P2']} of {len(p2)}; "
             f"P3 {recovered['P3']} of {len(p3)}")
    met = (recovered["P1"] == len(p1) == 6 and recovered["P2"] == len(p2) == 4
           and recovered["P3"] == len(p3) == 4 and all(arms_ok.values()))
    if args.expect:
        met = met and label == args.expect
    receipt = {"tool": TOOL, "class": CLASS, "revision": args.rev, "label": label,
               "met_target": met, "exit": 0 if met else 1,
               "recovered": recovered, "controls_ok": arms_ok,
               "cases": cases, "controls": controls, "pins": pins,
               "repair": {"cmd": args.repair_cmd,
                          "sha256": sha256_file(repair) if os.path.isfile(repair) else None},
               "work_root": run_root, "expect": args.expect}
    return (0 if met else 1), receipt


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    rep = load_module(os.path.join(root, R87_REPAIR), "r87repair")
    r88 = load_module(os.path.join(root, R88_REPAIR), "r88repair")
    r90 = load_module(os.path.join(root, "tools/round-90/upx-break-repair.py"), "r90")
    clean = r90._fixture()
    b0, blocks = layout(clean, rep, r88)
    check("layout-three-blocks", len(blocks) == 3 and b0 == blocks[0]["block"])
    blk = blocks[1]
    t = tamper(clean, blk, blk["sz_cpr"] - 7)
    ok, why = window_only(t, clean, blk)
    check("window-only-accepts-field-repair", ok)
    other = bytearray(clean)
    other[blocks[2]["block"] + 4] ^= 0x01
    ok, why = window_only(t, bytes(other), blk)
    check("window-only-refuses-foreign-byte", not ok)
    check("window-only-refuses-length", not window_only(t, clean[:-1], blk)[0])
    # a zeroed block 0 is the round-88 class: the tampered window is block 0's
    ok, _ = window_only(tamper(clean, blocks[0], 0), clean, blocks[0])
    check("window-only-accepts-block0", ok)
    check("declared-orig-table", DECLARED_ORIG["jq"] == 167)
    check("p1-carrier-set", [c["id"] for c in CARRIERS if c["p1"]] == ["jq", "xxd", "dinit"])
    check("p1-cells", len([c for c in CARRIERS if c["p1"]]) * len(DIRECTIONS) == 6)
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--repair-cmd", default="tools/round-90/upx-break-repair.py")
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--pkg", default=os.path.expanduser(
        "~/.local/share/rea-agents/6.5.0"))
    ap.add_argument("--work", default=os.environ.get("TMPDIR") or "/tmp")
    ap.add_argument("--expect", default=None)
    ap.add_argument("--no-rea", action="store_true")
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    try:
        rc, receipt = score(args)
    except Unevaluable as exc:
        print(json.dumps({"tool": TOOL, "unevaluable": str(exc)}))
        return 2
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(json.dumps({"label": receipt["label"], "met_target": receipt["met_target"],
                      "exit": receipt["exit"], "controls_ok": receipt["controls_ok"],
                      "recovered": receipt["recovered"]}, sort_keys=True))
    return receipt["exit"]


if __name__ == "__main__":
    sys.exit(main())
