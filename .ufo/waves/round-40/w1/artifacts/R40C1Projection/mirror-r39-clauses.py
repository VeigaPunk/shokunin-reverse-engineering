#!/usr/bin/env python3
"""Does an oracle-only fabricated receipt pass every non-rerun R39-C1 clause?

The round-39 counter's per-carrier clauses other than the (round-40) rerun
binding are replicated here against a fabricated receipt, so the report can say
which single clause would have to refuse it.  The reimplementation mirrors
tools/round-39/c1-counter.py: subject_pin_ok, operation_ok, handler_ok,
chunks_ok, oracle_hits, gaps_ok, escaping_ok.  `evidence_id_ok` is checked
separately with the frozen xpin tool (see the report's command log).

Usage: mirror-r39-clauses.py --manifest carriers.json --lane-root LANE \
         --receipts DIR [--json-out PATH]
Pure stdlib.
"""
import argparse
import json
import os
import sys


def read_tsv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            rows.append(line.rstrip("\n").split("\t"))
    return rows


def same_rel(candidate, rel):
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith("/" + rel))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--lane-root", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--json-out")
    opts = ap.parse_args(argv or sys.argv[1:])
    lane = os.path.abspath(opts.lane_root)
    spec = json.load(open(opts.manifest, encoding="utf-8"))
    entries = spec["carriers"] if isinstance(spec, dict) else spec

    out = {}
    for entry in entries:
        cid = entry["id"]
        path = os.path.join(opts.receipts, cid + ".json")
        if not os.path.exists(path):
            continue
        env = json.load(open(path, encoding="utf-8"))
        nr = env.get("normalized_result") or {}
        oracle = read_tsv(os.path.join(lane, entry["oracle"]))
        links = read_tsv(os.path.join(lane, entry["symlinks"])) if entry.get("symlinks") else []
        in_tree = [r[0] for r in links if len(r) > 2 and r[2] == "in-tree"]
        escaping = [r[0] for r in links if len(r) > 2 and r[2] == "escaping"]

        files = [(f.get("relative_path") or "", f.get("sha256") or "")
                 for f in nr.get("files") or []]
        chunks = nr.get("chunks") or []
        gaps = nr.get("extraction_gaps") or []

        hits = sum(1 for row in oracle
                   if any(row[1] == sha and same_rel(fp, row[0]) for fp, sha in files))
        gap_paths = [g.get("relative_path") or "" for g in gaps]
        gaps_ok = (all(g.get("kind") == "unpublished-entry" for g in gaps)
                   and sorted({r for rp in gap_paths for r in in_tree if same_rel(rp, r)})
                   == sorted(in_tree)
                   and len(gap_paths) == len(in_tree))
        escaping_pub = [fp for fp, _s in files for e in escaping if same_rel(fp, e)]

        row = {
            "subject_pin_ok": ((env.get("subject") or {}).get("digest") or {}).get("sha256")
                               == entry["sha256"],
            "operation_ok": env.get("operation") == "extract_firmware"
                            and (env.get("provider") or {}).get("id") == "unblob",
            "handler_ok": any(c.get("handler") == "squashfs_v4_be" for c in chunks),
            "chunks_ok": not any(c.get("extraction_failed") for c in chunks),
            "oracle_hits": hits,
            "oracle_files": len(oracle),
            "oracle_ok": hits == len(oracle),
            "gaps_ok": gaps_ok,
            "escaping_ok": not escaping_pub,
            "escaping_published": escaping_pub,
        }
        row["all_non_rerun_clauses"] = all(
            row[k] for k in ("subject_pin_ok", "operation_ok", "handler_ok",
                             "chunks_ok", "oracle_ok", "gaps_ok", "escaping_ok"))
        out[cid] = row

    result = {"schema": "kaidoku-r40-mirror-r39-clauses-v1", "carriers": out}
    if opts.json_out:
        with open(opts.json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1)
    print("carrier  " + "  ".join("%-14s" % k for k in
                                  ("subject", "operation", "handler", "chunks",
                                   "oracle", "gaps", "escaping", "ALL")))
    for cid, row in out.items():
        print("%-7s  %-14s  %-14s  %-14s  %-14s  %-14s  %-14s  %-14s  %s" % (
            cid,
            "ok" if row["subject_pin_ok"] else "FAIL",
            "ok" if row["operation_ok"] else "FAIL",
            "ok" if row["handler_ok"] else "FAIL",
            "ok" if row["chunks_ok"] else "FAIL",
            "%d/%d" % (row["oracle_hits"], row["oracle_files"]),
            "ok" if row["gaps_ok"] else "FAIL",
            "ok" if row["escaping_ok"] else "FAIL",
            "PASS" if row["all_non_rerun_clauses"] else "FAIL"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
