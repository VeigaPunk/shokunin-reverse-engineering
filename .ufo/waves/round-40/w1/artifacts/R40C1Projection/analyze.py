#!/usr/bin/env python3
"""R40-C1 run-matrix analysis: projection invariance, receipt drift, field variance.

Reads the receipts written by run-matrix.sh plus the committed round-39 receipts,
and answers three questions:

  1. INVARIANCE   do three REA runs of one carrier in three scratch roots yield
                  one projection?  (core / plus-mime / plus-extractor profiles)
  2. DRIFT        does the committed round-39 receipt project to the same thing
                  as the fresh runs?
  3. VARIANCE     which leaf fields of the receipt document actually change
                  between runs, and which are run-identity (must be excluded)?

Usage: analyze.py --artifacts DIR --lane LANE [--json-out PATH] [--tsv-out PATH]
Pure stdlib.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import projection as P  # noqa: E402

CARRIERS = {
    "K1": "corpus/evidence/round-39/c1/K1/after.json",
    "K2": "corpus/evidence/round-39/c1/K2/after.json",
    "K4": "corpus/evidence/round-39/c1/K4/after.json",
    "K5": "corpus/evidence/round-39/c1/K5/after.json",
    "K6": "corpus/evidence/round-39/c1/K6/after.json",
}
RUNS = {
    "K1": ["r1", "r2", "r3"],
    "K2": ["r1", "r2", "r3"],
    "K4": ["r1", "r2", "r3"],
    "K5": ["r1", "r2", "r3", "r4"],
    "K6": ["r1", "r2", "r3"],
}
PROFILES = ("core", "plus-mime", "plus-content", "plus-extractor")


# --------------------------------------------------------------- flatten paths
def flatten(value, prefix="", out=None):
    """Map normalised leaf path -> leaf value.  List indices collapse to []."""
    if out is None:
        out = {}
    if isinstance(value, dict):
        for key in value:
            flatten(value[key], "%s.%s" % (prefix, key) if prefix else key, out)
    elif isinstance(value, list):
        for item in value:
            flatten(item, "%s[]" % prefix, out)
    else:
        out[prefix] = value
    return out


def classify(path, values):
    joined = " ".join("" if v is None else str(v) for v in values)
    if all(isinstance(v, str) and re.fullmatch(r"\d+:\d+", v) for v in values):
        # unblob ids are f"{os.getpid()}:{n}" -- a process id, never semantic
        return "run-identity:pid-blob-id"
    if "evidence_id" in path:
        return "run-identity:id"
    if path.endswith("output_directory") or path.endswith(".path") \
            or path.endswith("local_path") or path.endswith("subject.name"):
        return "run-identity:path-or-name"
    if path.endswith("provider_id") or path.endswith("blob_id") \
            or path.endswith("provider_blob_id") or path.endswith("continuation_id"):
        return "run-identity:provider-or-continuation-id"
    if re.search(r"/fast/scratch/|/tmp/|rea-firmware-", joined):
        return "run-identity:embedded-scratch-path"
    if path.endswith(".link") or path.endswith(".target"):
        if re.search(r"/fast/scratch/|/tmp/", joined):
            return "run-identity:embedded-scratch-path"
    if any(tok in path for tok in ("duration", "start_utc", "end_utc", "mtime", "timestamp")):
        return "run-identity:time"
    return "SEMANTIC"


def structural_diff(left, right, prefix="", out=None):
    """Exact leaf diff with real list indices: path -> (left, right)."""
    if out is None:
        out = {}
    if type(left) is not type(right):
        out[prefix] = (left, right)
        return out
    if isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            sub = "%s.%s" % (prefix, key) if prefix else key
            if key not in left:
                out[sub] = ("<absent>", right[key])
            elif key not in right:
                out[sub] = (left[key], "<absent>")
            else:
                structural_diff(left[key], right[key], sub, out)
    elif isinstance(left, list):
        for i in range(max(len(left), len(right))):
            sub = "%s[%d]" % (prefix, i)
            if i >= len(left):
                out[sub] = ("<absent>", right[i])
            elif i >= len(right):
                out[sub] = (left[i], "<absent>")
            else:
                structural_diff(left[i], right[i], sub, out)
    elif P.canonical(left) != P.canonical(right):
        out[prefix] = (left, right)
    return out


def samples(values, limit=2, width=110):
    seen, out = [], []
    for v in values:
        s = "" if v is None else str(v)
        if s in seen:
            continue
        seen.append(s)
        out.append(s[:width])
        if len(out) >= limit:
            break
    return out


# ------------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifacts", required=True)
    ap.add_argument("--lane", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--tsv-out", required=True)
    opts = ap.parse_args(argv or sys.argv[1:])

    art = os.path.abspath(opts.artifacts)
    lane = os.path.abspath(opts.lane)
    report = {"schema": "kaidoku-r40-rerun-analysis-v1", "carriers": {}}
    tsv_rows = []

    for carrier in sorted(CARRIERS):
        committed_path = os.path.join(lane, CARRIERS[carrier])
        committed = P.load_json(committed_path)
        fresh = {}
        for run in RUNS[carrier]:
            path = os.path.join(art, "receipts", "%s-%s.json" % (carrier, run))
            fresh[run] = P.load_json(path)

        entry = {"committed": committed_path, "runs": {}}
        for profile in PROFILES:
            base_proj = P.project(fresh[RUNS[carrier][0]], profile)
            run_equal = {}
            for run in RUNS[carrier][1:]:
                cmp_result = P.compare(base_proj, fresh[run], profile)
                run_equal[run] = {"equal": cmp_result["equal"],
                                  "fields": cmp_result["differing_fields"]}
            drift = P.compare(base_proj, committed, profile)
            entry[profile] = {
                "fresh_vs_fresh": run_equal,
                "fresh_vs_committed": {
                    "equal": drift["equal"],
                    "differing_fields": drift["differing_fields"],
                    "diff": drift["diff"],
                },
                "projection_sha256": base_proj["projection_sha256"],
            }

        # exact structural diff (real list indices) of run1 against each other run
        structural = {}
        for run in RUNS[carrier][1:] + ["committed"]:
            docs_pair = (fresh[RUNS[carrier][0]],
                         committed if run == "committed" else fresh[run])
            diffs = structural_diff(*docs_pair)
            structural[run] = {
                "n_differing_leaves": len(diffs),
                "semantic": sorted(p for p, vals in diffs.items()
                                   if classify(p, vals) == "SEMANTIC"),
                "paths": sorted(diffs),
            }
        entry["structural_diff_vs_run1"] = structural

        # variance over every run + the committed receipt
        docs = {("committed"): committed}
        docs.update(fresh)
        flat = {k: flatten(v) for k, v in docs.items()}
        paths = set()
        for f in flat.values():
            paths.update(f)
        varying = []
        for path in sorted(paths):
            values = [flat[k].get(path, "<absent>") for k in docs]
            if len(set(P.canonical(v) for v in values)) <= 1:
                continue
            kind = classify(path, values)
            varying.append({"path": path, "kind": kind,
                            "samples": samples(values)})
            tsv_rows.append((carrier, kind, path, samples(values, 2, 200)))
        invariant = sorted(paths - {v["path"] for v in varying})
        entry["invariant_leaf_paths"] = invariant
        entry["varying_leaf_paths"] = varying
        entry["variance_counts"] = {
            "total": len(varying),
            "semantic": sum(1 for v in varying if v["kind"] == "SEMANTIC"),
            "run_identity": sum(1 for v in varying if v["kind"] != "SEMANTIC"),
        }
        report["carriers"][carrier] = entry

    with open(opts.json_out, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
    with open(opts.tsv_out, "w", encoding="utf-8") as fh:
        fh.write("carrier\tkind\tpath\tsamples\n")
        for carrier, kind, path, sample in tsv_rows:
            fh.write("%s\t%s\t%s\t%s\n" % (carrier, kind, path, " | ".join(sample)))

    # console summary
    for carrier in sorted(report["carriers"]):
        entry = report["carriers"][carrier]
        print("== %s  projected=%s" % (carrier, entry["core"]["projection_sha256"][:16]))
        for profile in PROFILES:
            fvf = entry[profile]["fresh_vs_fresh"]
            bad = [r for r in fvf if not fvf[r]["equal"]]
            drift = entry[profile]["fresh_vs_committed"]
            print("   %-15s fresh-vs-fresh %s | vs committed equal=%s fields=%s" % (
                profile,
                "identical" if not bad else "DIFF " + ",".join(
                    "%s:%s" % (r, ",".join(fvf[r]["fields"])) for r in bad),
                drift["equal"], ",".join(drift["differing_fields"]) or "-"))
        vc = entry["variance_counts"]
        print("   varying leaf paths: %d (%d semantic, %d run-identity)" %
              (vc["total"], vc["semantic"], vc["run_identity"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
