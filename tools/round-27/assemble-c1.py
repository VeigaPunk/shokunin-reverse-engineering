#!/usr/bin/env python3
"""Assemble R27-C1 seat outputs into corpus/evidence/round-27/c1/ (L1 integration step).

Copies each seat's envelopes byte-exact, concatenates the seats' runs.tsv lines under the
frozen header, and writes table.tsv from the copied envelopes. It never edits an envelope.
The table verdicts it writes are checked again by tools/round-27/c1-rename-identity.py.

Usage: assemble-c1.py SEATS_DIR LANE
"""

import hashlib
import json
import os
import shutil
import sys

HEADER = ["seat", "carrier", "verb", "run", "path", "argv", "exit", "utc_start", "utc_end",
          "envelope_sha256", "evidence_id", "subject_sha256", "pkg_version", "pkg_json_sha256"]
SEATS = ["RunJqA", "RunJqB", "RunJqC", "RunJqD", "RunTxA", "RunTxB", "RunTxC", "RunTxD"]
VERBS = ["analyze", "inspect", "decompile", "xrefs", "read-bytes", "function", "instructions", "inspect-binary-layout"]
CARRIERS = {"jq": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806",
            "tinyxxd": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"}


def main(seats_dir, lane):
    out = os.path.join(lane, "corpus/evidence/round-27/c1")
    os.makedirs(os.path.join(out, "envelopes"), exist_ok=True)
    lines = []
    for seat in SEATS:
        runs = os.path.join(seats_dir, seat, "runs.tsv")
        rows = [l for l in open(runs, encoding="utf-8").read().split("\n") if l]
        if rows[0].split("\t") != HEADER:
            sys.exit("%s: header differs: %r" % (runs, rows[0]))
        for line in rows[1:]:
            cells = line.split("\t")
            row = dict(zip(HEADER, cells))
            name = "%s-%s-%s.json" % (row["carrier"], row["verb"], row["run"])
            src = os.path.join(seats_dir, seat, "envelopes", name)
            raw = open(src, "rb").read()
            if hashlib.sha256(raw).hexdigest() != row["envelope_sha256"]:
                sys.exit("%s: sha256 differs from the seat's runs.tsv" % src)
            shutil.copyfile(src, os.path.join(out, "envelopes", name))
            lines.append(line)
    with open(os.path.join(out, "runs.tsv"), "w", encoding="utf-8") as handle:
        handle.write("\t".join(HEADER) + "\n" + "\n".join(lines) + "\n")
    table = ["\t".join(["carrier", "verb", "verdict", "base_id", "repeat_id", "renamed_id", "subject_sha256"])]
    for carrier, sha in CARRIERS.items():
        for verb in VERBS:
            ids = {}
            for run in ("base", "repeat", "renamed"):
                env = json.load(open(os.path.join(out, "envelopes", "%s-%s-%s.json" % (carrier, verb, run))))
                ids[run] = env["data"]["evidence_id"]
            if ids["base"] != ids["repeat"]:
                verdict = "unstable"
            elif ids["renamed"] == ids["base"]:
                verdict = "content-keyed"
            else:
                verdict = "rename-sensitive"
            table.append("\t".join([carrier, verb, verdict, ids["base"], ids["repeat"], ids["renamed"], sha]))
    with open(os.path.join(out, "table.tsv"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(table) + "\n")
    print("\n".join(table))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
