#!/usr/bin/env python3
"""Fixture-root behavioral detector for tools/round-68/packed-elf.py.

Loads a tool copy as a module and substitutes a deterministic MODELLED
environment (fake upx/readelf/REA, fixture carriers with real sha256 pins), then
runs the tool's own score() and returns its verdict.  The tool's arithmetic -
section_count, counts_from, carrier_arms, fold, every arm expression, the exit
code - is the real code under test.

Usage: harness.py <tool.py> <scenario> <scratch-root> <json-out>
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import sys

A = {"proc": 200, "seg": 30, "string": 190}
B = {"proc": 120, "seg": 22, "string": 140}
STUB_PROC = {"a": {"proc": 3, "seg": 4, "string": 9},
             "b": {"proc": 3, "seg": 3, "string": 11}}


def counts(d):
    return {"procedure_count": d["proc"], "segment_count": d["seg"],
            "string_count": d["string"]}


def carrier_of(name):
    for cid in ("a", "b"):
        if name.endswith("-bin-" + cid):
            return cid
    return None


def scenarios(fixdir):
    src = {"a": os.path.join(fixdir, "bin-a"), "b": os.path.join(fixdir, "bin-b")}
    raw = {}
    for cid in ("a", "b"):
        with open(src[cid], "rb") as fh:
            raw[cid] = fh.read()
    base = {
        "orig_counts": {"a": counts(A), "b": counts(B)},
        "packed_counts": {"a": counts(STUB_PROC["a"]), "b": counts(STUB_PROC["b"])},
        "unpacked_counts": {"a": counts(A), "b": counts(B)},
        "unpacked_bytes": {"a": raw["a"], "b": raw["b"]},
        "readelf_text": "There are no sections in this file.\n",
        "ctrl_list_rc": 1,
        "ctrl_decomp_rc": 2,
        "refusal": {"packed_rc": 7, "packed_error": "address_unmapped",
                    "symbols": {"a": "FUN_00001000", "b": None}},
    }
    sc = {"S0_green": dict(base)}
    s = copy.deepcopy(base)
    s["unpacked_bytes"] = {"a": b"WRONG-" + raw["a"], "b": b"WRONG-" + raw["b"]}
    sc["S1_identity_broken"] = s
    s = copy.deepcopy(base)
    s["unpacked_counts"] = {"a": counts({"proc": 190, "seg": 30, "string": 190}),
                            "b": counts({"proc": 110, "seg": 22, "string": 140})}
    sc["S2_recovery_broken"] = s
    s = copy.deepcopy(base)
    s["readelf_text"] = ("  [ 1] .interp PROGBITS 0000000000000318 000318 00001c 00 A 0 0 1\n"
                         "  [ 2] .note.gnu.build-id NOTE 0 0 0 0 A 0 0 8\n")
    sc["S3_sections_present"] = s
    s = copy.deepcopy(base)
    s["packed_counts"] = {"a": counts({"proc": 150, "seg": 40, "string": 60}),
                          "b": counts({"proc": 150, "seg": 40, "string": 60})}
    sc["S4_before_above_floor"] = s
    s = copy.deepcopy(base)
    s["ctrl_list_rc"] = 0
    sc["S5_control_hot"] = s
    return sc, src


def build_env(pe, scen, fixdir, src):
    def rec(argv, rc, stdout="", stderr=""):
        return {"argv": argv, "rc": rc, "stdout": stdout,
                "stdout_bytes": len(stdout), "stderr": stderr[-4000:]}

    def fake_run(argv, timeout=900):
        cmd = os.path.basename(argv[0])
        args = argv[1:]
        if cmd == os.path.basename(pe.UPX):
            if "--version" in args:
                return rec(argv, 0, "upx 5.2.0\nUCL data compression library 1.03\n")
            if "-l" in args:
                name = os.path.basename(args[-1])
                if name.startswith("orig-"):
                    rc = scen["ctrl_list_rc"]
                    return rec(argv, rc, "" if rc else "packed\n",
                               "" if rc else "NotPackedException\n")
                return rec(argv, 0, "packed\n")
            if "--best" in args:
                out = args[args.index("-o") + 1]
                with open(out, "wb") as fh:
                    fh.write(b"PACKED-" + carrier_of(os.path.basename(out)).encode())
                return rec(argv, 0, "")
            if "-d" in args:
                out = args[args.index("-o") + 1]
                if os.path.basename(args[-1]).startswith("orig-"):
                    return rec(argv, scen["ctrl_decomp_rc"])
                with open(out, "wb") as fh:
                    fh.write(scen["unpacked_bytes"][carrier_of(os.path.basename(out))])
                return rec(argv, 0, "")
            return rec(argv, 0, "")
        if cmd == "readelf":
            return rec(argv, 0, scen["readelf_text"], "")
        return rec(argv, 0, "")

    def fake_analyze(pkg, path, receipt_path):
        name = os.path.basename(path)
        cid = carrier_of(name)
        if name.startswith("orig-"):
            c = scen["orig_counts"][cid]
        elif name.startswith("packed-"):
            c = scen["packed_counts"][cid]
        else:
            c = scen["unpacked_counts"][cid]
        env = {"normalized_result": dict(c)}
        rr = rec(["node", "rea.mjs", "analyze", "--format", "json", path], 0,
                 json.dumps(env))
        with open(receipt_path, "w", encoding="utf-8") as fh:
            json.dump({"run": rr, "envelope": env}, fh, indent=1, sort_keys=True)
        return env, rr

    def fake_decompile(pkg, path, address):
        name = os.path.basename(path)
        cid = carrier_of(name)
        if name.startswith("packed-"):
            return {"run": rec(["node", "rea.mjs", "decompile", path, address],
                               scen["refusal"]["packed_rc"], "", ""),
                    "code": None, "error_code": scen["refusal"]["packed_error"]}
        sym = scen["refusal"]["symbols"][cid]
        code = (sym or "") + ": " + "x" * 300
        return {"run": rec(["node", "rea.mjs", "decompile", path, address], 0,
                           json.dumps({"normalized_result": code}), ""),
                "code": code, "error_code": None}

    pins = {cid: hashlib.sha256(open(src[cid], "rb").read()).hexdigest() for cid in ("a", "b")}
    carriers = [
        {"id": "fa", "source": src["a"], "sha256": pins["a"],
         "min_orig_procedures": 100, "address": "0x1000",
         "address_symbol": "FUN_00001000"},
        {"id": "fb", "source": src["b"], "sha256": pins["b"],
         "min_orig_procedures": 50, "address": None, "address_symbol": None},
    ]
    pe.run = fake_run
    pe.analyze = fake_analyze
    pe.decompile = fake_decompile
    pe.CARRIERS = carriers
    pe.UPX = os.path.join(fixdir, "upx-stub")
    return carriers


def load_tool(path):
    spec = importlib.util.spec_from_file_location("pe_under_test", path)
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    return pe


def main(argv):
    tool, scen_name, scratch, out = argv[1], argv[2], argv[3], argv[4]
    fixdir = os.path.join(scratch, "fix")
    sc, src = scenarios(fixdir)
    pe = load_tool(tool)
    build_env(pe, sc[scen_name], fixdir, src)
    work = os.path.join(scratch, "work", scen_name)
    os.makedirs(work, exist_ok=True)
    buf = io.StringIO()
    rc = None
    try:
        with contextlib.redirect_stdout(buf):
            rc = pe.score(os.path.join(fixdir, "repo"), "deadbeef",
                          "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents",
                          work, None, False)
        err = None
    except Exception as exc:  # Unevaluable or crash
        err = f"{type(exc).__name__}: {exc}"
    payload = None
    try:
        payload = json.loads(buf.getvalue())
    except json.JSONDecodeError:
        payload = None
    result = {
        "tool": tool,
        "tool_sha256": hashlib.sha256(open(tool, "rb").read()).hexdigest(),
        "scenario": scen_name,
        "rc": rc,
        "error": err,
        "met_target": None if payload is None else payload.get("met_target"),
        "control_ok": None if payload is None else payload.get("control_ok"),
        "failing": None if payload is None else payload.get("failing"),
        "before_procedures": None if payload is None else payload.get("before_procedures"),
        "arms": None if payload is None else {
            c["id"]: {**c["arms"], "ok": c["ok"],
                      "packed_sha256": c["packed_sha256"]}
            for c in payload.get("carriers", [])},
        "counts": None if payload is None else {
            c["id"]: {"orig": c["orig_counts"], "packed": c["packed_counts"],
                      "unpacked": c["unpacked_counts"],
                      "section_count": c["section_count"]}
            for c in payload.get("carriers", [])},
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
    print(json.dumps({k: result[k] for k in ("scenario", "rc", "met_target",
                                             "control_ok", "failing", "error")},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
