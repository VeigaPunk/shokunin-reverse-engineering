#!/usr/bin/env python3
"""Secondary (EC-view) export directory: placement and reference evidence.

Reads the retained independent decode (indep.json) and re-opens each carrier read-only to
test three bounded questions per file:
  1. does the secondary directory start exactly where the primary export bloc ends?
  2. is its RVA named by any data-directory entry?
  3. where does a 4-byte/8-byte value equal to its RVA occur, and in which section?
Writes secondary-evidence.json; imports only hashlib/struct/json (stdlib).
"""

import json
import struct

BASE = "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2PEIndependent"


def r2o(sections, rva):
    for s in sections:
        span = max(s["virtual_size"], s["raw_size"])
        if s["virtual_address"] <= rva < s["virtual_address"] + span:
            return s["raw_ptr"] + rva - s["virtual_address"]
    return None


def o2sec(sections, off):
    for s in sections:
        if s["raw_ptr"] <= off < s["raw_ptr"] + s["raw_size"]:
            return s["name"]
    return None


def main():
    indep = json.load(open(BASE + "/indep.json"))["results"]
    out = []
    for rec in indep:
        b = open(rec["carrier"]["path"], "rb").read()
        secs = rec["sections"]
        e = rec["exports"]
        sec = [x for x in rec["embedded_export_directories"]
               if x["rva"] != e["directory_rva"]]
        rec_out = {"label": rec["label"], "secondary_directories": len(sec)}
        if len(sec) != 1:
            rec_out["error"] = "expected exactly one secondary directory"
            out.append(rec_out)
            continue
        s = sec[0]
        # 1. adjacency to the end of the primary export bloc
        ends = [e["directory_rva"] + 40,
                e["address_of_functions"] + 4 * e["function_count"],
                e["address_of_names"] + 4 * e["name_count"],
                e["address_of_name_ordinals"] + 2 * e["name_count"]]
        d0 = r2o(secs, e["directory_rva"])
        name_rva = struct.unpack_from("<I", b, d0 + 12)[0]
        ends.append(name_rva + len(e["dll_name"]) + 1)
        no = r2o(secs, e["address_of_names"])
        for i in range(e["name_count"]):
            nrva = struct.unpack_from("<I", b, no + 4 * i)[0]
            nm = e["names"][i]["name"]
            ends.append(nrva + len(nm) + 1)
        bloc_end = max(ends)
        # 2. named by a data directory?
        dd_rvas = [d["rva"] for d in rec["data_directories"]]
        # 3. references to the secondary RVA
        pat32 = struct.pack("<I", s["rva"])
        pat64 = struct.pack("<Q", int(rec["optional"]["image_base"], 16) + s["rva"])
        hits32 = [i for i in range(len(b) - 3) if b.startswith(pat32, i)]
        hits64 = [i for i in range(len(b) - 7) if b.startswith(pat64, i)]
        rec_out.update({
            "secondary_rva": s["rva"],
            "primary_bloc_end_rva": bloc_end,
            "adjacent": s["rva"] == bloc_end,
            "named_by_data_directory": s["rva"] in dd_rvas,
            "u32_occurrences": [{"offset": hex(o), "section": o2sec(secs, o)} for o in hits32],
            "u64_va_occurrences": [{"offset": hex(o), "section": o2sec(secs, o)} for o in hits64],
            "secondary_export_names": [n["name"] for n in s["names"]],
            "secondary_export_rvas": [hex(n["rva"]) for n in s["names"]],
        })
        out.append(rec_out)
    json.dump(out, open(BASE + "/secondary-evidence.json", "w"), indent=1, sort_keys=True)
    for r in out:
        print(r["label"], "adjacent=%s named_by_dd=%s u32=%s u64=%s" % (
            r.get("adjacent"), r.get("named_by_data_directory"),
            [(h["offset"], h["section"]) for h in r.get("u32_occurrences", [])],
            [(h["offset"], h["section"]) for h in r.get("u64_va_occurrences", [])]))


if __name__ == "__main__":
    main()
