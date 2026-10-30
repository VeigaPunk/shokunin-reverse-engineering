#!/usr/bin/env python3
"""ScribeScorecard (kaidoku round 51, wave 1) — BEFORE-column fact derivation.

Read-only over the lane tree. Re-derives, from committed bytes only:
  B1  C1 before-arm: round-50 after-attempt2 receipt -> carriers_matched / exit_code /
      failing carriers / bindings_false / measured revision / freeze.
  B2  C1 before-arm at the round-50 freeze (the other committed receipt).
  B3  C2 committed before-state: v5 labels of the FAILED no-pad ddwrt body
      `dmg_Z3_v3ddwrt_inode_table` from .ufo/waves/round-50/c3/c3-after.json.
  B4  C2 census drift: registered paths inside the `<!-- instrument-registry v2 -->`
      markers of SKILL.md minus the paths of tools/round-48/census2.json.
  B5  coverage head at the round base: knowledge .md files and mapped count
      (command A shape) at HEAD.
  B6  base identity: the diff between the claims file's declared base
      (1aa27369...) and the dispatch base (f04b51dd...).

Every figure is printed as JSON on stdout. The caller records the exact command,
the exit code, the stdout sha256 and the UTC time.

Usage:  python3 -I -B derive-before.py --root <LANE>
Exit:   0 = all derivations ran (a missing optional artefact is reported as
             "absent", not as a failure); 1 = a required derivation failed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

REGISTRY_MARKER = "<!-- instrument-registry v2 -->"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args],
                          capture_output=True, text=True)


def show(root, rev, path):
    p = git(root, "show", f"{rev}:{path}")
    if p.returncode != 0:
        return None
    return p.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", default="HEAD")
    args = ap.parse_args()
    root = args.root
    out = {"root": root, "rev": args.rev}
    problems = []

    # B1 -- C1 after-arm receipt (the committed round-50 miss).
    p = os.path.join(root, ".ufo/waves/round-50/l1/scores/c1-after-attempt2.json")
    try:
        d = json.load(open(p))
        out["B1_c1_after_attempt2"] = {
            "receipt": ".ufo/waves/round-50/l1/scores/c1-after-attempt2.json",
            "carriers_matched": d.get("carriers_matched"),
            "target": d.get("target"),
            "exit_code": d.get("exit_code"),
            "met_target": d.get("met_target"),
            "failing": d.get("failing"),
            "bindings_false": d.get("bindings_false"),
            "revision": d.get("revision"),
            "freeze": d.get("freeze"),
            "counter_sha256": d.get("counter_sha256"),
            "gaps_ok_by_carrier": {k: v.get("gaps_ok")
                                   for k, v in (d.get("carriers") or {}).items()},
        }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B1 {exc}")

    # B2 -- C1 before-arm at the round-50 freeze.
    p = os.path.join(root, ".ufo/waves/round-50/l1/scores/c1-before-attempt2.json")
    try:
        d = json.load(open(p))
        out["B2_c1_before_attempt2"] = {
            "receipt": ".ufo/waves/round-50/l1/scores/c1-before-attempt2.json",
            "carriers_matched": d.get("carriers_matched"),
            "exit_code": d.get("exit_code"),
            "revision": d.get("revision"),
            "freeze": d.get("freeze"),
        }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B2 {exc}")

    # B3 -- the v5 label of the FAILED no-pad ddwrt body.
    p = os.path.join(root, ".ufo/waves/round-50/c3/c3-after.json")
    try:
        d = json.load(open(p))
        hit = None
        for e in d.get("envelopes", []):
            if e.get("envelope") == "dmg_Z3_v3ddwrt_inode_table":
                hit = e
                break
        if hit is None:
            problems.append("B3 envelope not found")
        else:
            out["B3_c2_v5_ddwrt_failed_body"] = {
                "receipt": ".ufo/waves/round-50/c3/c3-after.json",
                "envelope": hit.get("envelope"),
                "table_label": hit.get("table_label"),
                "table_action": hit.get("table_action"),
                "evaluator_label": hit.get("evaluator_label"),
                "evaluator_action": hit.get("evaluator_action"),
                "features_F": (hit.get("features") or {}).get("F"),
                "features_G": (hit.get("features") or {}).get("G"),
                "match": hit.get("match"),
                "n_envelopes": d.get("n_envelopes"),
                "pair_mismatch_count": d.get("pair_mismatch_count"),
            }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B3 {exc}")

    # B4 -- registry/census drift, from SKILL.md markers and census2.json.
    try:
        skill = show(root, args.rev, "SKILL.md")
        if skill is None:
            problems.append("B4 SKILL.md unreadable")
        else:
            i = skill.find(REGISTRY_MARKER)
            if i < 0:
                problems.append("B4 registry marker absent")
            else:
                region = skill[i:]
                rows = sorted(set(re.findall(r"^\|\s*`(tools/[^`]+)`\s*\|",
                                             region, re.M)))
                census = json.load(open(os.path.join(
                    root, "tools/round-48/census2.json")))
                paths = set(census["paths"])
                outside = [p for p in rows if p not in paths]
                out["B4_census_drift"] = {
                    "registry_marker": REGISTRY_MARKER,
                    "registered_paths_in_marker_region": len(rows),
                    "census2_paths": len(paths),
                    "census_outside": len(outside),
                    "census_outside_paths": outside,
                    "census2_rule": census.get("rule"),
                }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B4 {exc}")

    # B5 -- coverage head (command A shape) at the measured revision.
    try:
        paths = git(root, "ls-tree", "-r", "--name-only", args.rev,
                    "--", "corpus/knowledge").stdout.splitlines()
        files = {os.path.basename(p)[:-3] for p in paths if p.endswith(".md")}
        readme = show(root, args.rev, "corpus/README.md") or ""
        sec = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
        mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", sec))
        out["B5_coverage_head"] = {
            "knowledge_files": len(files),
            "mapped": len(files & mapped),
            "missing": sorted(files - mapped),
            "dangling": sorted(mapped - files),
        }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B5 {exc}")

    # B6 -- the two candidate bases.
    try:
        diff = git(root, "diff", "--name-only",
                   "1aa273694f4409d3432fbcd73e83a33bee0dd8e9",
                   "f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab").stdout.split()
        skill_diff = git(root, "diff", "--name-only",
                         "1aa273694f4409d3432fbcd73e83a33bee0dd8e9",
                         "f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab",
                         "--", "SKILL.md").stdout.split()
        out["B6_bases"] = {
            "claims_file_declared_base": "1aa273694f4409d3432fbcd73e83a33bee0dd8e9",
            "dispatch_base": "f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab",
            "paths_differing": diff,
            "skill_md_differs": bool(skill_diff),
        }
    except Exception as exc:  # noqa: BLE001
        problems.append(f"B6 {exc}")

    out["problems"] = problems
    print(json.dumps(out, indent=1, sort_keys=True))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
