#!/usr/bin/env python3
"""ExecPremise probes for R93-C1 fresh-pack held-out arm (exploratory, unscored).

Usage: python3 -I -B probe.py {fresh|public|forgery|strict}
Each probe writes one receipt into the seat directory and exits 0 iff all its
premise assertions hold. Nothing here is a frozen counter: the v3 battery is
only imported and its functions called.
"""
import hashlib
import importlib.util
import json
import os
import struct
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r93/ExecPremise"
CLONE = os.path.join(S, "clone")
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SEAT = os.path.join(LANE, ".ufo/waves/round-93/w1/ExecPremise")
REPAIR = os.path.join(CLONE, "tools/round-92/upx-stop-boundary-search-repair.py")
FRESH_SRC = "/usr/bin/env"
FRESH_PIN = "a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301"
NONCE = "0123456789abcdef"  # fixed nonce for the forgery probe (reproducible)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def workdir(name):
    w = os.path.join(S, "work", name)
    os.makedirs(w, exist_ok=True)
    return w


def last_line(text):
    lines = [ln for ln in (text or "").strip().splitlines() if ln.strip()]
    return lines[-1] if lines else None


def cmd_line(argv):
    return " ".join(argv)


def write_receipt(name, rec):
    os.makedirs(SEAT, exist_ok=True)
    with open(os.path.join(SEAT, name), "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")


v3 = load(os.path.join(CLONE, "tools/round-93/stop-boundary-repair-battery-v3.py"), "v3probe")
v2 = v3.v2
rep = v2._load(os.path.join(CLONE, v2.R87), "r87")
r88 = v2._load(os.path.join(CLONE, v2.R88), "r88")


def fresh_packed(w, env, nonce):
    """Mutate the pinned fresh source with `nonce`, pack it twice, return pieces."""
    with open(FRESH_SRC, "rb") as fh:
        raw = fh.read()
    mut, minfo = v3.mutate_source(raw, nonce)
    src = os.path.join(w, "fresh-src.bin")
    with open(src, "wb") as fh:
        fh.write(mut)
    p1 = v2.pack(src, w, env)
    p2 = v2.pack(src, w, env)
    b0, blocks = v2.layout(p1, rep, r88)
    return {"raw": raw, "mut": mut, "minfo": minfo, "p1": p1, "p2": p2,
            "blocks": blocks, "b0": b0}


def probe_fresh():
    w = workdir("fresh-arm")
    env = v2.env_for(w)
    fresh = v3.fresh_arm(REPAIR, env, w, rep, r88, {"sentinel-deadbeef"}, CLONE)
    prov = fresh.get("provenance", {})
    near = [c for c in fresh.get("cells", []) if c.get("kind") == "near"]
    far = [c for c in fresh.get("cells", []) if c.get("kind") == "far"]
    intact = fresh.get("intact") or {}
    checks = {
        "no_unevaluable": fresh.get("unevaluable") is None,
        "deterministic_pack": prov.get("deterministic") is True,
        "marker_in_mutated": prov.get("marker_in_mutated") is True,
        "marker_absent_in_original": prov.get("marker_absent_in_original") is True,
        "no_collision_with_public": prov.get("collides_public_packed") is False,
        "walkable_chain": (prov.get("blocks") or 0) >= 1,
        "near_cells_two": len(near) == 2,
        "near_both_repaired_roundtrip": len(near) == 2 and all(
            c.get("class") == "repaired" and c.get("roundtrip") is True for c in near),
        "far_cells_two": len(far) == 2,
        "far_both_refused": len(far) == 2 and all(c.get("class") == "refused" for c in far),
        "intact_identity": intact.get("identity") is True,
    }
    ok = all(checks.values())

    def brief(c):
        return {k: c.get(k) for k in ("kind", "delta", "class", "rc", "roundtrip",
                                      "stored", "value", "block_index", "typed_strict",
                                      "tail", "detail")}
    rec = {"probe": "fresh-arm-premise", "exit": 0 if ok else 1,
           "command": cmd_line(["python3", "-I", "-B", "probe.py", "fresh"]),
           "tmpdir": env["TMPDIR"],
           "counter_imported_sha256": sha_file(os.path.join(CLONE, "tools/round-93/stop-boundary-repair-battery-v3.py")),
           "repair": REPAIR, "repair_sha256": sha_file(REPAIR),
           "public_shas_arg": ["sentinel-deadbeef"],
           "fresh_source": FRESH_SRC, "fresh_source_sha256": sha_file(FRESH_SRC),
           "checks": checks, "provenance": prov,
           "cells": [brief(c) for c in fresh.get("cells", [])],
           "intact": {k: intact.get(k) for k in ("rc", "identity", "box_after", "typed_strict")},
           "unevaluable": fresh.get("unevaluable")}
    write_receipt("fresh-arm-premise.json", rec)
    print("fresh-arm-premise", "PASS" if ok else "FAIL", json.dumps(checks, sort_keys=True))
    return 0 if ok else 1


def probe_public():
    w = workdir("public")
    env = v2.env_for(w)
    carriers = {}
    for cid, path, pin in v2.CARRIERS:
        raw_ok = sha_file(path) == pin
        if cid == "jq" or True:
            a = v2.pack(path, w, env)
            b = v2.pack(path, w, env)
        carriers[cid] = {"path": path, "raw_sha_pin_ok": raw_ok,
                         "pack1_sha256": sha_bytes(a), "pack2_sha256": sha_bytes(b),
                         "byte_equal": a == b, "packed_len": len(a)}
    jq = carriers["jq"]
    ok = jq["byte_equal"] is True and jq["raw_sha_pin_ok"] is True
    rec = {"probe": "public-determinism", "exit": 0 if ok else 1,
           "command": cmd_line(["python3", "-I", "-B", "probe.py", "public"]),
           "tmpdir": env["TMPDIR"], "upx": v2.UPX, "upx_sha256": sha_file(v2.UPX),
           "assertion": "jq packed twice via v2.pack byte-equal",
           "jq_byte_equal": jq["byte_equal"], "jq": jq,
           "informational_other_carriers": {k: {"byte_equal": v["byte_equal"],
                                                "raw_sha_pin_ok": v["raw_sha_pin_ok"]}
                                            for k, v in carriers.items() if k != "jq"}}
    write_receipt("public-determinism.json", rec)
    print("public-determinism", "PASS" if ok else "FAIL", "jq byte_equal", jq["byte_equal"])
    return 0 if ok else 1


def probe_forgery():
    w = workdir("forgery")
    env = v2.env_for(w)
    fp = fresh_packed(w, env, NONCE)
    packed, blocks = fp["p1"], fp["blocks"]
    if not blocks:
        print("forgery: no walkable blocks")
        return 1
    last = blocks[-1]
    cdir = os.path.join(w, "cells")
    odir = os.path.join(w, "out")
    os.makedirs(cdir, exist_ok=True)
    os.makedirs(odir, exist_ok=True)
    cells = {"intact": packed}
    cell_meta = {"intact": {"delta": None}}
    for d in (-7, 7, -40, 40):
        value = last["sz_cpr"] + d
        in_range = 0 < value <= last["sz_unc"]
        t = bytearray(packed)
        struct.pack_into("<I", t, last["block"] + 4, value)
        cells[f"d{d:+d}"] = bytes(t)
        cell_meta[f"d{d:+d}"] = {"delta": d, "stored": last["sz_cpr"], "value": value,
                                 "in_range": in_range, "block": last["block"]}
    cell_paths = {}
    for name, data in cells.items():
        p = os.path.join(cdir, f"{name}.bin")
        with open(p, "wb") as fh:
            fh.write(data)
        cell_paths[name] = p
    forgers = {
        "F1-table5-window": os.path.join(CLONE, ".ufo/waves/round-93/controls/table5-window.py"),
        "F2-carrierread5": os.path.join(CLONE, ".ufo/waves/round-93/controls/carrierread5.py"),
    }
    results = {}
    all_refused = True
    for fid, script in forgers.items():
        results[fid] = {"script": script, "script_sha256": sha_file(script), "cells": {}}
        for cname, cpath in cell_paths.items():
            outp = os.path.join(odir, f"{fid}-{cname}.bin")
            if os.path.exists(outp):
                os.remove(outp)
            argv = [sys.executable, "-I", "-B", script, "--in", cpath, "--out", outp]
            p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=900)
            exists = os.path.isfile(outp)
            out_sha = sha_file(outp) if exists else None
            lastl = last_line(p.stdout)
            parsed = None
            if lastl:
                try:
                    parsed = json.loads(lastl)
                except ValueError:
                    parsed = None
            results[fid]["cells"][cname] = {
                "command": cmd_line(argv), "rc": p.returncode, "stdout": p.stdout,
                "stderr_tail": (p.stderr or "").strip().splitlines()[-3:],
                "output_exists": exists, "output_sha256": out_sha,
                "output_equals_packed": (out_sha == sha_bytes(packed)) if exists else False,
                "last_stdout_json": parsed, "meta": cell_meta[cname],
            }
            if cname != "intact" and (p.returncode == 0 or exists):
                all_refused = False
    # Premise for this probe: both forgers refuse (no output) on every fresh cell.
    ok = all_refused
    rec = {"probe": "forgery-fresh-direct", "exit": 0 if ok else 1,
           "command": cmd_line(["python3", "-I", "-B", "probe.py", "forgery"]),
           "tmpdir": env["TMPDIR"], "nonce": NONCE,
           "fresh_source": FRESH_SRC, "fresh_source_sha256": sha_file(FRESH_SRC),
           "marker_offset": fp["minfo"]["marker_offset"],
           "fresh_packed_sha256": sha_bytes(packed), "blocks": len(blocks),
           "last_block": last, "lane_repair_imported_by_F2": os.path.join(LANE, "tools/round-92/upx-stop-boundary-search-repair.py"),
           "lane_repair_sha256_F2_imports": sha_file(os.path.join(LANE, "tools/round-92/upx-stop-boundary-search-repair.py")),
           "clone_repair_sha256": sha_file(REPAIR),
           "forgers": results,
           "note": "F1/F2 invoked directly (no battery). F2 hard-codes ROOT=lane path for its cand import; the lane file sha is recorded above."}
    # Receipts split per forger for the requested filenames.
    f1 = dict(rec, probe="f1-fresh-direct", forgers={"F1-table5-window": results["F1-table5-window"]})
    f2 = dict(rec, probe="f2-fresh-direct", forgers={"F2-carrierread5": results["F2-carrierread5"]})
    f1["exit"] = f2["exit"] = 0 if ok else 1
    write_receipt("f1-fresh-direct.json", f1)
    write_receipt("f2-fresh-direct.json", f2)
    summary = {fid: {c: (v["rc"], v["output_exists"]) for c, v in results[fid]["cells"].items()}
               for fid in results}
    print("forgery-fresh-direct", "PASS" if ok else "FAIL", json.dumps(summary, sort_keys=True))
    return 0 if ok else 1


def probe_strict():
    w = workdir("strict")
    env = v2.env_for(w)
    fp = fresh_packed(w, env, NONCE)
    packed, blocks = fp["p1"], fp["blocks"]
    last = blocks[-1]
    r91 = os.path.join(CLONE, "tools/round-91/upx-stop-boundary-repair.py")
    cells = {}
    for d in (-40, 40, -7, 7):
        value = last["sz_cpr"] + d
        t = bytearray(packed)
        struct.pack_into("<I", t, last["block"] + 4, value)
        cp = os.path.join(w, f"cell{d:+d}.bin")
        with open(cp, "wb") as fh:
            fh.write(bytes(t))
        outp = os.path.join(w, f"r91-out{d:+d}.bin")
        if os.path.exists(outp):
            os.remove(outp)
        argv = [sys.executable, "-I", "-B", r91, "--in", cp, "--out", outp]
        p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=900)
        rec_run = {"rc": p.returncode, "stdout": p.stdout}
        cells[f"{d:+d}"] = {"command": cmd_line(argv), "rc": p.returncode, "stdout": p.stdout,
                            "output_exists": os.path.isfile(outp),
                            "strict_typed": v3.strict_typed(rec_run)}
    far_refusal_strict = cells["-40"]["strict_typed"] and cells["+40"]["strict_typed"]
    synthetic_cases = {
        "refused_null_rc2": ({"rc": 2, "stdout": '{"tool": "x", "refused": null}\n'}, False),
        "refused_empty_rc2": ({"rc": 2, "stdout": '{"refused": ""}\n'}, False),
        "refused_int_rc2": ({"rc": 2, "stdout": '{"refused": 7}\n'}, False),
        "refused_string_rc2": ({"rc": 2, "stdout": '{"refused": "stop-boundary: x"}\n'}, True),
        "refused_string_rc1": ({"rc": 1, "stdout": '{"refused": "x"}\n'}, False),
        "no_refused_key_rc2": ({"rc": 2, "stdout": '{"error": "x"}\n'}, False),
        "non_json_last_rc2": ({"rc": 2, "stdout": "refused\n"}, False),
    }
    synth = {}
    synth_ok = True
    for name, (rec_in, expect) in synthetic_cases.items():
        got = v3.strict_typed(rec_in)
        synth[name] = {"input": rec_in, "expect": expect, "got": got, "ok": got is expect}
        synth_ok = synth_ok and got is expect
    ok = far_refusal_strict and synth_ok and cells["-40"]["rc"] == 2
    rec = {"probe": "strict-typed", "exit": 0 if ok else 1,
           "command": cmd_line(["python3", "-I", "-B", "probe.py", "strict"]),
           "tmpdir": env["TMPDIR"], "round91_tool": r91, "round91_sha256": sha_file(r91),
           "round91_on_fresh_cells": cells,
           "round91_far_strict_typed": far_refusal_strict,
           "synthetic": synth, "synthetic_all_ok": synth_ok,
           "assertion": "strict_typed True on round-91 far refusal stdout; False on refused:null"}
    write_receipt("strict-typed.json", rec)
    print("strict-typed", "PASS" if ok else "FAIL", "far strict", far_refusal_strict,
          "synthetic ok", synth_ok)
    return 0 if ok else 1


PROBES = {"fresh": probe_fresh, "public": probe_public,
          "forgery": probe_forgery, "strict": probe_strict}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in PROBES:
        print("usage: probe.py {fresh|public|forgery|strict}", file=sys.stderr)
        sys.exit(2)
    sys.exit(PROBES[sys.argv[1]]())
