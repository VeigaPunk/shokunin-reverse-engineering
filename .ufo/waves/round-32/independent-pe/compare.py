#!/usr/bin/env python3
"""Compare an independent PE structural decode with frozen labels and two witnesses.

Inputs (all produced by A2PEIndependent, no lane module imported):
  * indep.json            -- decode of pe_indep.py (the independent instrument)
  * oracle.stdout.jsonl   -- stdout of the frozen lane oracle CLI, one JSON object per carrier
  * readobj-<id>.txt      -- llvm-readobj --file-headers --sections --coff-exports output
  * carriers.tsv          -- frozen carrier labels (path, sha256, bytes, native/EC counts)

The labels are the frozen build-spec columns; the oracle and llvm-readobj are witnesses only.
Every check is recorded as id -> {pass, observed, expected}; nothing is repaired on mismatch.
"""

import json
import re
import subprocess
import sys

TSV = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-32/c1/carriers.tsv"
BASE = "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2PEIndependent"


def read_tsv(path):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            row = dict(zip(header, line.split("\t")))
            rows[row["id"]] = row
    return rows


def load_oracle(path):
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            out[rec["path"].rsplit("/", 1)[-1].split(".")[0]] = rec
    return out


def parse_readobj(path):
    text = open(path, encoding="utf-8").read()
    parts = text.split("HybridObject {", 1)
    prim, hyb = parts[0], ("HybridObject {" + parts[1]) if len(parts) > 1 else ""
    rec = {"format": None, "machine": None, "image_base": None, "section_count": None,
           "sections": [], "exports": [], "hybrid": {"present": bool(hyb), "format": None,
           "machine": None, "export_table_rva": None, "section_count": None, "exports": []}}
    m = re.search(r"^Format: (\S+)$", prim, re.M)
    rec["format"] = m.group(1) if m else None
    m = re.search(r"^  Machine: (\S+) \((0x[0-9A-Fa-f]+)\)$", prim, re.M)
    rec["machine"] = m.group(2) if m else None
    m = re.search(r"^  ImageBase: (0x[0-9a-fA-F]+)$", prim, re.M)
    rec["image_base"] = m.group(1) if m else None
    m = re.search(r"^  SectionCount: (\d+)$", prim, re.M)
    rec["section_count"] = int(m.group(1)) if m else None
    for nm in re.finditer(r"^    Name: (\S+) \([0-9A-F ]+\)$", prim, re.M):
        rec["sections"].append(nm.group(1))
    for blk in re.finditer(r"^Export \{\n  Ordinal: (\d+)\n  Name: (\S+)\n  RVA: (0x[0-9a-fA-F]+)\n\}$",
                           prim, re.M):
        rec["exports"].append({"ordinal": int(blk.group(1)), "name": blk.group(2),
                               "rva": blk.group(3)})
    if hyb:
        m = re.search(r"^  Format: (\S+)$", hyb, re.M)
        rec["hybrid"]["format"] = m.group(1) if m else None
        m = re.search(r"^    Machine: (\S+) \((0x[0-9A-Fa-f]+)\)$", hyb, re.M)
        rec["hybrid"]["machine"] = m.group(2) if m else None
        m = re.search(r"^    SectionCount: (\d+)$", hyb, re.M)
        rec["hybrid"]["section_count"] = int(m.group(1)) if m else None
        m = re.search(r"^      ExportTableRVA: (0x[0-9a-fA-F]+)$", hyb, re.M)
        rec["hybrid"]["export_table_rva"] = m.group(1) if m else None
        for blk in re.finditer(
                r"^  Export \{\n    Ordinal: (\d+)\n    Name: (\S+)\n    RVA: (0x[0-9a-fA-F]+)\n  \}$",
                hyb, re.M):
            rec["hybrid"]["exports"].append({"ordinal": int(blk.group(1)),
                                             "name": blk.group(2), "rva": blk.group(3)})
    return rec


def main():
    labels = read_tsv(TSV)
    indep = {r["label"]: r for r in json.load(open(BASE + "/indep.json"))["results"]}
    oracle = load_oracle(BASE + "/oracle.stdout.jsonl")
    checks = {}
    summary = {}

    def put(carrier, cid, ok, observed, expected):
        checks.setdefault(carrier, {})[cid] = {"pass": bool(ok), "observed": observed,
                                               "expected": expected}

    for cid in sorted(labels):
        lab = labels[cid]
        rec = indep[cid]
        orc = oracle[cid]
        rob = parse_readobj("%s/readobj-%s.txt" % (BASE, cid))
        car = rec["carrier"]
        prim_exports = rec["exports"]["names"]
        prim_names = [n["name"] for n in prim_exports]
        secondary = [x for x in rec["embedded_export_directories"]
                     if x["rva"] != rec["exports"]["directory_rva"]]
        sec_names = secondary[0]["names"] if len(secondary) == 1 else []
        sec_name_list = [n["name"] for n in sec_names]

        # --- frozen labels -------------------------------------------------
        put(cid, "label_sha256", rec["sha256"] == lab["sha256"], rec["sha256"], lab["sha256"])
        put(cid, "label_bytes", str(rec["bytes"]) == lab["bytes"], rec["bytes"], lab["bytes"])
        put(cid, "label_native_exports", rec["exports"]["name_count"] == int(lab["native_exports"]),
            rec["exports"]["name_count"], int(lab["native_exports"]))
        put(cid, "label_ec_exports", len(sec_names) == int(lab["ec_exports"]),
            {"secondary_directories": len(secondary), "names": sec_name_list},
            int(lab["ec_exports"]))
        put(cid, "label_ec_via_hexpthk",
            rec["hexpthk"]["slot_count"] == int(lab["ec_exports"]),
            rec["hexpthk"]["slot_count"], int(lab["ec_exports"]))
        meta = rec["chpe"]["metadata"] or {}
        put(cid, "label_ec_via_entry_point_count",
            meta.get("code_ranges_to_entry_points_count") == int(lab["ec_exports"]),
            meta.get("code_ranges_to_entry_points_count"), int(lab["ec_exports"]))
        put(cid, "label_ec_via_redirection_count",
            meta.get("redirection_metadata_count") == int(lab["ec_exports"]),
            meta.get("redirection_metadata_count"), int(lab["ec_exports"]))
        kinds = set(rec["chpe"]["range_kinds"])
        put(cid, "machine_0xaa64", rec["coff"]["machine"] == "0xaa64",
            rec["coff"]["machine"], "0xaa64")
        put(cid, "classify_arm64x", rec["classify"]["arm64x"] is True,
            rec["classify"], {"arm64x": True})
        put(cid, "code_map_arm64_and_arm64ec", {"ARM64", "ARM64EC"} <= kinds,
            sorted(kinds), ["ARM64", "ARM64EC"])
        put(cid, "hexpthk_slots_are_x64_thunks",
            rec["hexpthk"]["present"] and set(rec["hexpthk"]["slot_prefixes"]) <= {"488bc4"},
            sorted(set(rec["hexpthk"]["slot_prefixes"])), ["488bc4"])

        # --- oracle witness -------------------------------------------------
        o_exp = orc["expected"]
        my_cm = [(r["type"], r["start"], r["length"]) for r in rec["chpe"]["code_map"]]
        o_cm = [(r["type"], r["start"], r["length"]) for r in orc["class"]["code_map"]]
        put(cid, "oracle_sha256", orc["sha256"] == rec["sha256"], orc["sha256"], rec["sha256"])
        put(cid, "oracle_machine", orc["class"]["machine"] == rec["coff"]["machine"],
            orc["class"]["machine"], rec["coff"]["machine"])
        put(cid, "oracle_arm64x_flag", bool(orc["class"]["arm64x"]) == rec["classify"]["arm64x"],
            orc["class"]["arm64x"], rec["classify"]["arm64x"])
        put(cid, "oracle_code_map", o_cm == my_cm, o_cm, my_cm)
        put(cid, "oracle_image_base", o_exp["image_base"] == rec["optional"]["image_base"],
            o_exp["image_base"], rec["optional"]["image_base"])
        put(cid, "oracle_segment_count", o_exp["segment_count"] == rec["segment_count"],
            o_exp["segment_count"], rec["segment_count"])
        put(cid, "oracle_procedure_count", o_exp["procedure_count"] == rec["procedure_count"],
            o_exp["procedure_count"], rec["procedure_count"])
        my_segs = [{"name": s["name"], "start": hex(s["start"]), "end": hex(s["end"]),
                    "length": s["length"], "image_base": hex(s["image_base"]),
                    "address_space": s["address_space"]} for s in rec["segments"]]
        put(cid, "oracle_segments", o_exp["segments"] == my_segs, o_exp["segments"], my_segs)
        put(cid, "oracle_document",
            o_exp["document"] == "target-%s.dll" % rec["sha256"][:12],
            o_exp["document"], "target-%s.dll" % rec["sha256"][:12])
        put(cid, "oracle_format_arch",
            (o_exp["format"], o_exp["architecture"]) == ("pe", "arm64"),
            (o_exp["format"], o_exp["architecture"]), ("pe", "arm64"))
        put(cid, "oracle_native_export_names", orc["native_exports"] == prim_names,
            orc["native_exports"], prim_names)

        # --- llvm-readobj witness ------------------------------------------
        put(cid, "readobj_format", rob["format"] == "COFF-ARM64X", rob["format"], "COFF-ARM64X")
        put(cid, "readobj_image_base", rob["image_base"] == rec["optional"]["image_base"],
            rob["image_base"], rec["optional"]["image_base"])
        put(cid, "readobj_section_count", rob["section_count"] == rec["coff"]["section_count"],
            rob["section_count"], rec["coff"]["section_count"])
        put(cid, "readobj_section_names",
            rob["sections"] == [s["name"] for s in rec["sections"]],
            rob["sections"], [s["name"] for s in rec["sections"]])
        put(cid, "readobj_primary_export_names", [e["name"] for e in rob["exports"]] == prim_names,
            [e["name"] for e in rob["exports"]], prim_names)
        put(cid, "readobj_hybrid_export_names",
            [e["name"] for e in rob["hybrid"]["exports"]] == sec_name_list,
            [e["name"] for e in rob["hybrid"]["exports"]], sec_name_list)
        put(cid, "readobj_hybrid_export_table_rva",
            rob["hybrid"]["export_table_rva"] is not None
            and int(rob["hybrid"]["export_table_rva"], 16)
            == (secondary[0]["rva"] if len(secondary) == 1 else None),
            rob["hybrid"]["export_table_rva"],
            hex(secondary[0]["rva"]) if len(secondary) == 1 else None)
        put(cid, "readobj_hybrid_format", rob["hybrid"]["format"] == "COFF-ARM64EC",
            rob["hybrid"]["format"], "COFF-ARM64EC")
        # Raw COFF machine vs llvm-readobj's synthesized top-level machine label.
        put(cid, "readobj_machine_is_synthesized",
            rob["machine"] == "0xA64E" and rec["coff"]["machine"] == "0xaa64",
            {"readobj": rob["machine"], "raw_coff": rec["coff"]["machine"]},
            {"readobj": "0xA64E", "raw_coff": "0xaa64"})

        summary[cid] = {"native_exports": rec["exports"]["name_count"],
                        "secondary_directory_rva": hex(secondary[0]["rva"]) if len(secondary) == 1 else None,
                        "secondary_export_names": sec_name_list,
                        "image_base": rec["optional"]["image_base"],
                        "segment_count": rec["segment_count"],
                        "section_names": [s["name"] for s in rec["sections"]]}

    # aggregate
    total = sum(len(v) for v in checks.values())
    failed = [(cid, cid2, rec["observed"], rec["expected"])
              for cid, per in checks.items() for cid2, rec in per.items() if not rec["pass"]]
    by_check = {}
    for cid, per in checks.items():
        for cid2, rec in per.items():
            agg = by_check.setdefault(cid2, {"pass": 0, "fail": 0})
            agg["pass" if rec["pass"] else "fail"] += 1
    version_lines = subprocess.run(["llvm-readobj", "--version"], capture_output=True,
                                   text=True).stdout.splitlines()
    payload = {"schema": "a2pe-compare-v1",
               "carriers": len(labels),
               "checks_total": total,
               "checks_passed": total - len(failed),
               "checks_failed": len(failed),
               "failed": failed,
               "by_check": by_check,
               "per_carrier": checks,
               "summary": summary,
               "oracle_path": BASE + "/oracle.stdout.jsonl",
               "readobj_tool": version_lines[1].strip() if len(version_lines) > 1 else "unknown"}
    with open(BASE + "/compare.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("carriers=%d checks=%d passed=%d failed=%d" % (len(labels), total,
                                                         total - len(failed), len(failed)))
    for cid2 in sorted(by_check):
        print("  %-42s pass=%2d fail=%d" % (cid2, by_check[cid2]["pass"], by_check[cid2]["fail"]))
    for f in failed:
        print("FAIL", f)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
