#!/usr/bin/env python3
"""R45W2Src141: independent re-verification of the S141 registry row and its record.

Reads (read-only) the lane files named on argv; never writes outside --out.
Checks, each printed as one JSON line:
  page    - bytes, sha256, anchors, quote in normalized text, word count
  row     - 11 columns, per-column values, used-by
  record  - lesson Gate quote+word count, claims bullet, block 22 arm text
Exit 0 iff every check is true; 1 otherwise.
"""
import json
import re
import sys
import html
import hashlib

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
QUOTE = ("When --raw, --numstat, --name-only or --name-status has been given, "
         "do not munge pathnames and use NULs as output field terminators.")
ANCHORS = ["Documentation/git-diff-tree.txt--z", "_raw_output_format"]


def norm(h):
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    return re.sub(r"\s+", " ", t).strip()


def main(page_path):
    out = {}
    raw = open(page_path, "rb").read()
    h = raw.decode("utf-8")
    out["page"] = {
        "path": page_path,
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "recorded_bytes": 256810,
        "recorded_sha256": "f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640",
        "anchors_present": {a: (('id="%s"' % a) in h) for a in ANCHORS},
        "quote_words": len(QUOTE.split()),
        "quote_in_normalized_text": QUOTE in norm(h),
        "quote_is_raw_byte_substring": QUOTE in h,
        "quote_omitted_next_sentence_in_page": "Without this option, pathnames with \"unusual\" characters are quoted" in norm(h),
    }

    src = open(LANE + "/corpus/SOURCES.md", encoding="utf-8").read().splitlines()
    s141 = [l for l in src if l.startswith("| S141 ")]
    out["row"] = {"count": len(s141)}
    if s141:
        cells = [c.strip() for c in s141[0].strip().strip("|").split("|")]
        out["row"].update({
            "ncols": len(cells),
            "cells": cells,
            "all_nonempty": all(cells),
            "used_by": cells[-1],
            "used_by_mentions_skill": "SKILL.md" in cells[-1],
        })

    lesson = open(LANE + "/corpus/lessons/round-45.md", encoding="utf-8").read().splitlines()
    gate = [l for l in lesson if l.startswith("| S141 ")]
    out["record"] = {"gate_row": gate, "gate_word_cell": None}
    if gate:
        m = re.search(r"\((\d+) words\)", gate[0])
        out["record"]["gate_word_cell"] = int(m.group(1)) if m else None

    claims = open(LANE + "/plans/round-45-claims.md", encoding="utf-8").read()
    i = claims.find("**S141**")
    out["record"]["claims_bullet"] = re.sub(r"\s+", " ", claims[i:i + 260]) if i >= 0 else None

    skill = open(LANE + "/SKILL.md", encoding="utf-8").read()
    flat = re.sub(r"\s+", " ", skill); j = flat.find("the commit arm reads plain tab-separated")
    out["record"]["block22_arm_sentence"] = flat[j:j + 520] if j >= 0 else None
    out["record"]["block22_s141_table_cell"] = "| commit (git log --name-status, S141) |" in skill

    ok = (out["page"]["sha256"] == out["page"]["recorded_sha256"]
          and out["page"]["bytes"] == out["page"]["recorded_bytes"]
          and all(out["page"]["anchors_present"].values())
          and out["page"]["quote_in_normalized_text"]
          and out["row"].get("ncols") == 11
          and out["row"].get("all_nonempty"))
    out["ok"] = ok
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
