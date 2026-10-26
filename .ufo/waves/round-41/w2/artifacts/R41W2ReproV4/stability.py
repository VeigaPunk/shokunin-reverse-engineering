#!/usr/bin/env python3
"""Projection stability across V4 after-receipts.

Reuses cmp.py's exact-path projection and prints, per receipt, a digest of the
scored projection (files rel+sha256+size, unpublished rel+kind+target, gap
(kind, rel), removal rel+target) plus the removal set, so identical receipts
are visible without diffing pairwise.
"""
import hashlib
import json
import sys

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r41/R41W2ReproV4")
import cmp  # noqa: E402


def projection(proj):
    body = {
        "files": proj["files"],
        "unpublished": proj["unpublished"],
        "gaps": sorted((g["kind"], str(g["rel"]), str(g["handler"]),
                        list(g["dependencies"])) for g in proj["gaps"]),
        "removals": proj["removals"],
        "subject": proj["subject_sha256"],
        "handlers": proj["handlers"],
    }
    raw = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest(), body


def main():
    rows = []
    for p in sys.argv[1:]:
        proj = cmp.project(cmp.load(p))
        dig, body = projection(proj)
        rows.append({
            "receipt": p,
            "projection_sha256": dig,
            "n_files": len(body["files"]),
            "n_unpublished": len(body["unpublished"]),
            "n_diagnostics_gaps": len(body["gaps"]),
            "n_removals": len(body["removals"]),
            "removal_paths": sorted(body["removals"]),
            "removal_targets": sorted(set(body["removals"].values())),
            "evidence_id": proj["evidence_id"],
            "output_directory": (proj["parameters"] or {}).get("output_directory"),
        })
    digs = {r["projection_sha256"] for r in rows}
    print(json.dumps({"receipts": rows, "distinct_projections": len(digs),
                      "stable": len(digs) == 1,
                      "removal_sets": sorted({json.dumps(r["removal_paths"]) for r in rows})},
                     indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
