#!/usr/bin/env python3
"""Consolidate the three mutation receipts and the probe transcripts into the
one acceptance receipt: targets / mutants / survivors / inconclusive.
"""

from __future__ import annotations

import glob
import json
import os
import pathlib
import sys

EVID = pathlib.Path(__file__).resolve().parent


def load(name: str) -> dict:
    return json.loads((EVID / name).read_text(encoding="utf-8"))


def probe_rows(name: str) -> dict:
    rows = {}
    path = EVID / name
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("{"):
            entry = json.loads(line)
            rows[entry["mutant"]] = entry
    return rows


def hunk_index() -> dict:
    index = {}
    path = EVID / "diffs" / "hunks.txt"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            key, *rest = line.split()
            fields = dict(item.split("=", 1) for item in rest)
            index[os.path.basename(key)] = {k: int(v) for k, v in fields.items()}
    return index


SUPERSEDED = [
    {"target": "binder", "id": "b11-evidence-extra-accepted",
     "reason": "anchor absent: the candidate removed its evidence-length check between "
               "observed revisions d46806d9 and b01e7b49; re-cut as "
               "b11-drop-evidence-token-match against the stable bytes"},
    {"target": "prov", "id": "p4-bad-digest-not-skipped",
     "reason": "anchor absent: the candidate renamed RE_HEX64 to RE_HEX64_ANY between "
               "observed revisions e6576187 and b07ee0c0; re-cut against the stable bytes"},
]

OBSERVED_CHURN = {
    "binder": ["d46806d9f9496eddf9321f4cae9dfffc3a04be86853ffac61c7d2bea85290581",
               "b01e7b494acd88caed037a473824ab0b0cb524b520659114c4d46234a1ff8f8a"],
    "prov": ["e6576187ce43f9127de7511b870816ec599a8d3f224fc0288e0625d8cea18768",
             "b07ee0c028d1f1623eb3173ba81551e4c69c27cf6d1299b0ddb3a732242c4001"],
    "guard": ["b25eace205a531a83f3f48075c0afc431380cab7a2b2eb1df255f9428b24e0a7",
              "2ba488896da50eb44ec6251d1aaef41be28d8bac6315dab7a14f3a34bdbd104e",
              "45efcb2a9190e5b17690627d2dff4c8d2977e8a028b5b2f159e31801376a2e4c",
              "d97fcc6063f8587d76522e178b1b89ec550754c9c7614640f70b4eccec059c50"],
}


def main() -> int:
    receipts = [load("receipt-round79.json"), load("receipt-binder-prov.json"),
                load("receipt-binder-extra.json"), load("receipt-guard.json")]
    probes = {}
    probes.update(probe_rows("survivor-probes-round79.txt"))
    probes.update(probe_rows("survivor-probes-binder.txt"))
    probes.update(probe_rows("survivor-probes-prov.txt"))
    probes.update(probe_rows("survivor-probes-guard.txt"))
    hunks = hunk_index()

    targets, mutants, survivors = [], [], []
    for receipt in receipts:
        for target in receipt["targets"]:
            tally = {"killed": 0, "survived": 0, "inconclusive": 0}
            for mutant in receipt["mutants"]:
                if mutant.get("target") != target["name"]:
                    continue
                tally[mutant["verdict"]] = tally.get(mutant["verdict"], 0) + 1
            entry = {
                "name": target["name"], "path": target["path"],
                "sha256": target["sha256"], "bytes": target.get("bytes"),
                "pristine": target["pristine"],
                "mutants_total": sum(tally.values()),
                "killed": tally["killed"], "survived": tally["survived"],
                "inconclusive": tally["inconclusive"],
            }
            live = pathlib.Path(target["path"])
            if live.is_file():
                import hashlib
                now = hashlib.sha256(live.read_bytes()).hexdigest()
                entry["sha256_at_consolidation"] = now
                entry["unchanged_since_run"] = now == target["sha256"]
            if target["name"] in OBSERVED_CHURN:
                entry["observed_revisions"] = OBSERVED_CHURN[target["name"]]
                entry["tested_revision_note"] = (
                    "results below are the tested sha256; earlier revisions were observed "
                    "mid-write and not scored")
            targets.append(entry)

        for mutant in receipt["mutants"]:
            row = {"target": mutant["target"], "id": mutant["id"],
                   "edit": mutant["edit"],
                   "anchor_occurrences": mutant.get("anchor_occurrences"),
                   "mutant_sha256": mutant.get("mutant_sha256"),
                   "exit": mutant.get("exit"), "cases": mutant.get("cases"),
                   "failures": mutant.get("failures"),
                   "killed_by": mutant.get("killed_by") or [],
                   "sole_detector": mutant.get("sole_detector") is True,
                   "survived": mutant.get("verdict") == "survived",
                   "verdict": mutant.get("verdict"),
                   "reason": mutant.get("reason"),
                   "diff_hunks": hunks.get(mutant["id"], {}).get("hunks")}
            mutants.append(row)

        for survivor in receipt["survivors"]:
            proof = probes.get(survivor["id"], {})
            survivors.append({
                "target": survivor["target"], "id": survivor["id"],
                "edit": survivor["edit"],
                "case_that_would_kill": survivor.get("case_that_would_kill"),
                "proof": {"pristine_asserts_correct": proof.get("pristine_asserts_correct"),
                          "mutant_asserts_correct": proof.get("mutant_asserts_correct"),
                          "proved": proof.get("proved")},
                "equivalent_mutant": proof.get("equivalent_mutant", False),
            })

    out = {
        "schema": "mutinstruments-r80-receipt-v1",
        "round": 80,
        "seat": "MutInstruments",
        "base": "16dfa009bf143080dfcdfc5f9ec34bd359536d90",
        "frozen": {
            "claims_guard": "84d68e90f8a1ea3a3a7f94a208695c21023c0472",
            "strictness_sha256": "40f99456aff65f5b8b1ee7098820b2086499ae0c62b372d575f5f09d34510feb",
        },
        "environment": {
            "python": sys.version.split()[0],
            "child_env_keys": ["PATH", "HOME", "TMPDIR", "LANG"],
            "scratch": "/fast/scratch/hyaku/kaidoku-r80/MutInstruments",
            "installs": [],
        },
        "targets": targets,
        "mutants": mutants,
        "survivors": survivors,
        "inconclusive": [m for m in mutants if m["verdict"] == "inconclusive"],
        "superseded_attempts": SUPERSEDED,
        "totals": {
            "targets": len(targets),
            "mutants": len(mutants),
            "killed": sum(1 for m in mutants if m["verdict"] == "killed"),
            "survived": sum(1 for m in mutants if m["verdict"] == "survived"),
            "inconclusive": sum(1 for m in mutants if m["verdict"] == "inconclusive"),
            "survivors_with_proof": sum(
                1 for s in survivors if s["proof"]["proved"] is True),
            "equivalent_survivors": sum(
                1 for s in survivors if s["equivalent_mutant"]),
            "one_hunk_mutants": sum(1 for m in mutants if m["diff_hunks"] == 1),
        },
    }
    (EVID / "receipt.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8")
    print(json.dumps(out["totals"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
