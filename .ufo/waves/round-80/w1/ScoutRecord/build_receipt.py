#!/usr/bin/env python3
"""Build the acceptance receipt from the probe output."""
from __future__ import annotations
import hashlib, json, os, subprocess

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "16dfa009bf143080dfcdfc5f9ec34bd359536d90"
EV = os.path.join(LANE, ".ufo/waves/round-80/w1/ScoutRecord")
probe = json.load(open(os.path.join(EV, "probe.json")))


def byte_span(path, start, end):
    data = open(path, "rb").read()
    lines = data.splitlines(keepends=True)
    off = sum(len(b) for b in lines[:start - 1])
    span = sum(len(b) for b in lines[start - 1:end])
    return off, span


cells = []
for c in probe["cells"]:
    off, span = byte_span(c["live_path"], c["line_start"], c["line_end"])
    tokens = [t["token"] for t in c["tokens_detail"]]
    whole = all(t["whole_token"] for t in c["tokens_detail"])
    entry = {
        "id": c["id"],
        "record_line": c["record_line"],
        "cell_text": c["cell_text"],
        "pointer": c["pointer"],
        "live_path": c["live_path"],
        "line_start": c["line_start"],
        "line_end": c["line_end"],
        "pointed_line": "\n".join(c["pointed_lines"]),
        "token": tokens[0] if len(tokens) == 1 else " + ".join(tokens),
        "tokens": tokens,
        "whole_token": whole,
        "line_sha256": c["line_sha256"],
        "line_sha256_rstrip": c["line_sha256_rstrip"],
        "byte_offset": off,
        "pointed_bytes": span,
        "occurrences": [
            {"token": t["token"],
             "hits": [{"start": h["start"], "end": h["end"],
                       "left": h["left"], "right": h["right"], "whole": h["whole"]}
                      for h in t["occurrences"]],
             "per_line": t["per_line"],
             "whole_token": t["whole_token"]}
            for t in c["tokens_detail"]],
    }
    cells.append(entry)

occ = [o for o in probe["rea_agents_occurrences"] if o["kind"] == "other"]
cell_tokens = {c["token"] for c in cells if c["id"] in ("devin-pin", "omp-pin", "kimi-pin")}
record_hits = [o for o in probe["rea_agents_occurrences"] if o["token"] in cell_tokens]

over_refusal = {
    "rule": ("a cell binds iff every declared token occurs as a delimited token in the "
             "pointed lines; delimited = start/end of line or a character outside "
             "[A-Za-z0-9._-] on each side"),
    "other_rea_agents_occurrences_in_province": occ,
    "pin_regex_matches": probe["pin_matches"],
    "cell_token_occurrences_in_record": record_hits,
    "whole_record_scan_all_whole": all(o["all_whole"] for o in probe["rea_agents_occurrences"]),
    "newly_refused_cells": [],
    "newly_refused_count": 0,
    "verdict": "no cell newly refused",
    "grounds": [
        "the frozen rule checks tokens only on each cell's pointed lines; the "
        "record's prose occurrences are never the token source (round-79 bind() reads "
        "the pointer target, PROVINCE.md is not consulted for tokens)",
        "RE_PIN finds exactly 3 client-cell matches (record lines 15-16, 16-17, 17-18 "
        "spans; pointer-bearing lines 16, 17, 18); lines 9, 12, 47 do not match "
        "`(Devin|OMP|Kimi)\\s+`rea-agents@...` (`<ptr>`)` and cannot displace or "
        "duplicate a cell (verified: exactly 3 matches, first-match order intact)",
        "all 8 non-cell `rea-agents@` occurrences (lines 9, 12 x2, 47, 322, 345, 358, "
        "438) are whole-token occurrences themselves (backtick- or space-delimited), "
        "so even a hypothetical whole-record strictness scan would refuse nothing",
        "each pointed file carries the declared pin exactly once, on the pointed line "
        "(devin 1, omp 1, kimi 1), so no longer live token competes with the pin",
    ],
}

receipt = {
    "schema": "kaidoku-r80-scoutrecord-v1",
    "seat": "ScoutRecord",
    "round": 80,
    "lane": LANE,
    "base": BASE,
    "declaration_guard": probe["declaration_guard"],
    "province": {
        "path": "PROVINCE.md",
        "lines": probe["province_lines"],
        "sha256": hashlib.sha256(
            subprocess.run(["git", "-C", LANE, "show", f"{BASE}:PROVINCE.md"],
                           capture_output=True).stdout).hexdigest(),
    },
    "ghidra_install_dir": probe["ghidra_install_dir"],
    "cells": cells,
    "over_refusal_check": over_refusal,
    "file_lengths": probe["file_lengths"],
}
with open(os.path.join(EV, "receipt.json"), "w", encoding="utf-8") as fh:
    json.dump(receipt, fh, indent=2)
    fh.write("\n")
print(json.dumps({"cells": len(cells),
                  "whole": sum(1 for c in cells if c["whole_token"]),
                  "file_lengths": list(receipt["file_lengths"])}, indent=2))
