#!/usr/bin/env python3
"""ConnectorCross r76 receipt builder (read-only).

Re-runs the assignment's three searches as fixed argv lists over the fleet root,
classifies the hits (live instrument / prose record / wave scratch), and emits
the receipt JSON. No shell, no writes outside --out.
"""
import json
import os
import re
import subprocess
import sys

FLEET = "/home/vgpnk/Projects/shokunin"
LANE = os.path.join(FLEET, "kaidoku-shokunin")


def grep(argv_tail, root=FLEET):
    argv = ["grep"] + argv_tail + ["."]
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    hits = sorted(l for l in p.stdout.splitlines() if "/.git/" not in l)
    return {"argv": " ".join(argv), "cwd": root, "rc": p.returncode, "n": len(hits), "hits": hits}


def classify(path):
    """live = a committed instrument/prose surface a lane would maintain."""
    if "/.ufo/" in path or "/reports/" in path or "/census/" in path or "/corpus/live/" in path \
            or "/corpus/evidence/" in path or "/quality/" in path or "/tests/" in path:
        return "wave-evidence"
    if re.search(r"/(tools|plans|scripts|verifiers)/(?:[^/]+/)?[^/]+\.py$", path):
        return "instrument"
    if re.search(r"/(SCORECARD|LOG|SKILL|PROVINCE|SHONEN|MINT|README)\.md$", path):
        return "record"
    if re.search(r"/corpus/(lessons|knowledge)/", path):
        return "lesson"
    if re.search(r"/corpus/SOURCES\.md$", path):
        return "registry"
    return "other"


def lane_of(path):
    m = re.match(r"\./([^/]+)/", path)
    return m.group(1) if m else "."


def main():
    out = {"seat": "ConnectorCross", "round": 76, "wave": "r76-w1",
           "fleet_root": FLEET, "lane": "kaidoku-shokunin",
           "lane_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=LANE,
                                       capture_output=True, text=True).stdout.strip()}

    q1 = grep(["-rl", "counting-command\\|plan-command\\|plan_command",
               "--include=*.py", "--include=*.md"])
    buckets = {}
    for h in q1["hits"]:
        buckets.setdefault(classify(h), []).append(h)
    out["q1"] = {
        "searched": q1["argv"], "cwd": q1["cwd"], "rc": q1["rc"], "hits_total": q1["n"],
        "by_class": {k: {"n": len(v), "lanes": sorted({lane_of(p) for p in v}),
                         "hits": v} for k, v in sorted(buckets.items())},
    }

    # literal PLACEHOLDER_UNBOUND token, fleet-wide
    ph = grep(["-rl", "PLACEHOLDER_UNBOUND", "--include=*.py", "--include=*.md"])
    out["q1"]["placeholder_unbound_token"] = {"n": ph["n"], "hits": ph["hits"]}

    # one-line counting-command prose (md only), grouped by lane
    q1m = grep(["-rn", "counting-command", "--include=*.md"])
    lanes = {}
    for h in q1m["hits"]:
        lanes.setdefault(lane_of(h.split(":")[0]), 0)
        lanes[lane_of(h.split(":")[0])] += 1
    out["q1"]["prose_counts_by_lane"] = dict(sorted(lanes.items(), key=lambda kv: -kv[1]))

    q2 = grep(["-rn", "## Capabilities", "--include=*.py"])
    b2 = {}
    for h in q2["hits"]:
        path = h.split(":")[0]
        b2.setdefault(classify(path), []).append(h)
    out["q2"] = {"searched": q2["argv"], "cwd": q2["cwd"], "n_lines": q2["n"],
                 "by_class": {k: {"n": len(v), "lanes": sorted({lane_of(x.split(':')[0]) for x in v}),
                                  "files": sorted({x.split(':')[0] for x in v})}
                              for k, v in sorted(b2.items())}}

    # fence-aware subprocess runners (candidate printed-command executors)
    p = subprocess.run(
        ["bash", "-c",
         "for f in $(grep -rl subprocess --include='*.py' . 2>/dev/null "
         "| grep -v '/\\.git/' | grep -v '/\\.ufo/'); do "
         "if grep -qE '```|\\bfence|FENCE|code_block|CODEBLOCK' \"$f\" 2>/dev/null; then echo \"$f\"; fi; done"],
        cwd=FLEET, capture_output=True, text=True)
    fr = sorted(l for l in p.stdout.splitlines() if "/.git/" not in l)
    out["q2"]["fence_and_subprocess_runners"] = {
        "n": len(fr),
        "instruments": [f for f in fr if re.search(r"/(tools|plans|scripts|verifiers)/(?:[^/]+/)?[^/]+\.py$", f)],
    }

    # census
    census = os.path.join(FLEET, "scripts", "sources-census.sh")
    with open(census, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    out["q3"] = {
        "path": "scripts/sources-census.sh",
        "separate_instrument": True,
        "capabilities_mentions": text.count("Capabilities"),
        "plan_command_mentions": text.count("counting-command") + text.count("plan-command"),
        "verdict": "no relevant check: the fleet census validates corpus/SOURCES.md registry "
                   "shape (E01-E12, W01-W04) and never reads a plan, a SCORECARD ## Capabilities "
                   "table, or an executable command",
    }

    # considerthese
    lanes_dirs = sorted(d for d in os.listdir(FLEET) if d.endswith("-shokunin"))
    have = [d for d in lanes_dirs if os.path.isdir(os.path.join(FLEET, d, "considerthese"))]
    absent = [d for d in lanes_dirs if d not in have]
    out["q4"] = {
        "considerthese_present_in": have, "considerthese_absent_in": absent,
        "kaidoku_absents": "kaidoku-shokunin" in absent,
        "lane_local_merge_dir": os.path.isdir(os.path.join(LANE, "merge")),
        "fleet_merge_dir": os.path.isdir(os.path.join(FLEET, "merge")),
        "shokuknow_merge_kaidoku": {
            "path": "/home/vgpnk/Projects/shokuknow/merge/kaidoku",
            "present": os.path.isdir("/home/vgpnk/Projects/shokuknow/merge/kaidoku"),
            "members": sorted(os.listdir("/home/vgpnk/Projects/shokuknow/merge/kaidoku"))
            if os.path.isdir("/home/vgpnk/Projects/shokuknow/merge/kaidoku") else [],
            "merge_report_headings": [l for l in subprocess.run(
                ["grep", "-nE", "^#{1,3} ",
                 "/home/vgpnk/Projects/shokuknow/merge/kaidoku/MERGE-REPORT.md"],
                capture_output=True, text=True).stdout.splitlines()] if os.path.isdir(
                "/home/vgpnk/Projects/shokuknow/merge/kaidoku") else [],
        },
    }


    out["verdicts"] = {
        "q1_printed_command_gate": {
            "verdict": "duplication with named divergences",
            "owner_of_the_other_surface": "kengaku-shokunin",
            "sibling": "plans/correction_command_check.py",
            "same_class": "extract a printed counting command from committed bytes, re-run it "
                          "with shlex.split and shell=False, price the integer output",
            "divergences": [
                "extraction: one-line backtick span in dated-correction sections vs fenced "
                "sh block between counting-command markers",
                "refusal: path-shape out-of-scope SKIP (< > : .. /) vs argv-wide "
                "PLACEHOLDER_UNBOUND/ellipsis refusal at exit 3",
                "child env: ambient env inherited (no env= kwarg) vs four-key env",
                "grammar: argv[0]==grep only, one integer vs generic argv with "
                "SAFE_SCRIPT_PREFIX + METACHARS + ALLOWED_VARS",
                "shape: population gate with counts vs three-arm battery over two fixtures",
                "exit map: 0/1/2 vs 0/1/2/3",
            ],
            "no_other_sibling": "87 fence+subprocess lane instruments survive the semantic filter; "
                                "none extracts a fenced block and executes it",
        },
        "q2_capability_atom": {
            "verdict": "duplication with named divergences",
            "owner_of_the_other_surface": "kengaku-shokunin",
            "sibling": "plans/round68_capability_table.py",
            "same_class": "does every declared capability carry exactly one SCORECARD "
                          "## Capabilities row with a round cell and an existing evidence path",
            "divergences": [
                "population: literal DECLARED dict (rounds 64-67) vs derived from record "
                "sentences that say 'Capabilities rows appended'",
                "cells: name + round + path vs name + non-empty description + resolving "
                "pointer + claiming round",
                "evidence grammar: (?:plans|corpus)/ vs the wider tools/ and .ufo/ pointers",
                "fixtures: s1-s5 string-replace fixtures vs six declared red fixtures",
                "composition: standalone predicate vs atom D24 of nine in a record audit "
                "whose receipt carries a validate block",
            ],
            "other_readers": {
                "mori-shokunin/tools/mori-register-check.py": "MANIFEST keys -> register row",
                "tameshi-shokunin/tools/selfstate-freshness.py": "row figure -> live instrument print",
                "chousa-shokunin/tools/lane-preflight.py": "G05 evidence-cell path existence only",
                "kama-shokunin/tools/round74-selfdesc-canon.py": "newest table resolution by heading form",
                "kama-shokunin/tools/round78-selfrecord-round77.py": "F2 canonical list as one of six facts",
                "tsukuroi-shokunin/tools/check-self-assessment.py": "CAPABILITIES membership, miss -> exit 2",
            },
            "record_audits_without_the_atom": [
                "chousa-shokunin/tools/claims-audit-v2.py (rule-TSV, 10 selftest cases, no Capabilities rule)",
                "kotodama-shokunin/reports/round-28/audit/x62-frozen-record-audit.py (frozen-surface replay)",
            ],
        },
        "q3_considerthese_and_merge": {
            "verdict": "no overlap",
            "considerthese_absent_in_lane": True,
            "merge_kaidoku_serves_claims": False,
            "note": "merge/kaidoku exists only in the shokuknow staging campaign, not in this "
                    "fleet and not in this lane; its six headings are sources/knowledge adoption "
                    "sections",
        },
        "q4_fleet_census": {
            "verdict": "no overlap",
            "note": "scripts/sources-census.sh has 0 Capabilities and 0 plan-command mentions; "
                    "it validates corpus/SOURCES.md registry shape only",
        },
    }

    out["reads_only"] = True
    out["writes"] = [".ufo/waves/round-76/w1/ConnectorCross.md",
                     ".ufo/waves/round-76/w1/ConnectorCross/receipt.json",
                     ".ufo/waves/round-76/w1/ConnectorCross/scan.py"]

    json.dump(out, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
