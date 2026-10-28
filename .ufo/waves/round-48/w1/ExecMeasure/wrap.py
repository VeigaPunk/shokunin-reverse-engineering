#!/usr/bin/env python3
"""Wrap one counter invocation into an ExecMeasure receipt."""
import json
import sys


def main():
    name, counter, rc, utc, sha, raw, stdout, dest = sys.argv[1:9]
    argv = sys.argv[10:]
    try:
        receipt = json.load(open(raw))
    except Exception:
        receipt = None
    fields = {}
    if isinstance(receipt, dict):
        for k in ("met_target", "failing", "meaning_rows_failed", "floor",
                  "quotes_bad", "battery", "freeze", "frozen_derived",
                  "frozen_path_changed", "touched", "restored", "reason",
                  "profile", "rev", "counter", "oracle", "axis_score_cells",
                  "axis_score_bad", "claim_ids", "corrections",
                  "corrections_bad", "quotes_checked", "sections",
                  "registry_rows", "census_paths", "census_rederived_equal",
                  "registry_duplicates", "registry_missing", "registry_extra",
                  "meaning_failures", "marker_occurrences", "block_present",
                  "routed_counts", "arm_by_id", "refs", "cited",
                  "unresolved_citations", "mutations_sha256",
                  "interpreter_sha256"):
            if k in receipt:
                fields[k] = receipt[k]
    wrapped = {
        "seat": "ExecMeasure",
        "invocation": name,
        "counter_tool": counter,
        "argv": ["python3"] + argv + ["--json-out", raw],
        "exit_code": int(rc),
        "utc": utc,
        "stdout_sha256": sha,
        "stdout_path": stdout,
        "counter_receipt_path": raw if receipt is not None else None,
        "counter_receipt_parseable": receipt is not None,
        **fields,
    }
    with open(dest, "w") as fh:
        json.dump(wrapped, fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    main()
