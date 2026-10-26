#!/usr/bin/env python3
"""R40-C1 fabrication check: does the rerun projection refuse an oracle-only receipt?

For each carrier it compares (per projection profile)

  fabricated-min   oracle-only receipt, six-field-complete but no diagnostics
  fabricated-full2 full with an in-tree-only derivation tree (a forger who has
                   read RD39W2C1Fabricate)
  fabricated-full  oracle-only receipt in the R39 CTL-C1-3 shape (diagnostics
                   inferred from the escaping links, full derivation tree, engine
                   copied as a host constant, coverage/published_bytes derived,
                   extension-guessed mime, evidence id re-minted with the frozen
                   6.5.0 rule)

against the semantic projection of a *fresh* REA run of the same carrier.

Usage: fabrication-check.py --artifacts DIR [--json-out PATH]
Pure stdlib.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projection as P  # noqa: E402

CARRIERS = ("K1", "K2", "K4", "K5", "K6")
MODES = ("min", "full", "full2")
PROFILES = ("core", "plus-mime", "plus-content", "plus-extractor")


def compact(diff, width=120):
    out = {}
    for field, body in diff.items():
        detail = body.get("detail") or {}
        out[field] = {
            "left": P.canonical(body.get("left"))[:width],
            "right": P.canonical(body.get("right"))[:width],
            "detail": {k: P.canonical(v)[:width] for k, v in detail.items()
                       if v not in (None, [], {})},
        } if isinstance(detail, dict) and detail else {
            "left": P.canonical(body.get("left"))[:width],
            "right": P.canonical(body.get("right"))[:width],
        }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", required=True)
    ap.add_argument("--json-out", required=True)
    opts = ap.parse_args(argv or sys.argv[1:])
    art = os.path.abspath(opts.artifacts)

    report = {"schema": "kaidoku-r40-fabrication-check-v1", "carriers": {}}
    refused_all = True
    for carrier in CARRIERS:
        fresh = P.load_json(os.path.join(art, "receipts", "%s-r1.json" % carrier))
        entry = {}
        for mode in MODES:
            fab = P.load_json(os.path.join(art, "fabricated-%s" % mode, "%s.json" % carrier))
            per_profile = {}
            for profile in PROFILES:
                result = P.compare(fab, fresh, profile)
                per_profile[profile] = {
                    "refused": not result["equal"],
                    "differing_fields": result["differing_fields"],
                    "diff": compact(result["diff"]),
                }
                if profile == "core":
                    refused_core = not result["equal"]
            if not refused_core:
                refused_all = False
            entry[mode] = per_profile
        report["carriers"][carrier] = entry

    report["all_fabrications_refused_core"] = refused_all
    with open(opts.json_out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)

    print("carrier  mode  " + "  ".join("%-16s" % p for p in PROFILES))
    for carrier in CARRIERS:
        for mode in MODES:
            row = report["carriers"][carrier][mode]
            cells = []
            for profile in PROFILES:
                p = row[profile]
                cells.append("%-16s" % ("REFUSED " + ",".join(p["differing_fields"])
                                        if p["refused"] else "ACCEPTED"))
            print("%-7s  %-4s  %s" % (carrier, mode, "  ".join(cells)))
    print("\nall fabrications refused at profile=core: %s" % refused_all)
    return 0 if not refused_all else 1


if __name__ == "__main__":
    sys.exit(main())
