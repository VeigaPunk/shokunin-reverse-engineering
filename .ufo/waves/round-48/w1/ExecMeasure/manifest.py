#!/usr/bin/env python3
"""Aggregate ExecMeasure receipts into manifest.json."""
import json
import os
import subprocess
import sys


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout.strip()


def main():
    out, rev, freeze, base, freeze_a1, freeze_a2 = sys.argv[1:7]
    lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
    recs = []
    for fn in sorted(os.listdir(os.path.join(out, "receipts"))):
        if not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(out, "receipts", fn)))
        recs.append({
            "invocation": d["invocation"],
            "receipt": f"receipts/{fn}",
            "exit_code": d["exit_code"],
            "utc": d["utc"],
            "stdout_sha256": d["stdout_sha256"],
            "met_target": d.get("met_target"),
            "failing": d.get("failing"),
            "reason": d.get("reason"),
            "meaning_rows_failed": d.get("meaning_rows_failed"),
            "quotes_bad": d.get("quotes_bad"),
            "battery": d.get("battery"),
        })
    manifest = {
        "seat": "ExecMeasure",
        "lane_root": lane,
        "round": 48,
        "wave": "w1",
        "base": base,
        "rev_graded": rev,
        "freeze_used": freeze,
        "freeze_declared_per_claims_file": freeze_a2,
        "freeze_literal_in_prompt_stale_a1": freeze_a1,
        "head": sh("git", "-C", lane, "rev-parse", "HEAD"),
        "head_subject": sh("git", "-C", lane, "log", "-1", "--format=%s"),
        "freeze_rederived": sh("git", "-C", lane, "log", "--format=%H", "-1",
                               "--", "plans/round-48-claims.md"),
        "frozen_paths_worktree_dirty": sh(
            "git", "-C", lane, "status", "--porcelain", "--",
            "tools/round-48", "plans/round-48-claims.md") or "(clean)",
        "landing_present": None,
        "invocations": recs,
    }
    for marker, card in (("verdict-meaning-table", "SKILL.md"),
                         ("## Round 48", "SCORECARD.md")):
        r = subprocess.run(["git", "-C", lane, "show", f"{rev}:{card}"],
                           capture_output=True, text=True)
        if marker in r.stdout:
            manifest["landing_present"] = True
    if manifest["landing_present"] is None:
        manifest["landing_present"] = False
    with open(os.path.join(out, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(manifest, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
