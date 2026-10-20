#!/usr/bin/env python3
"""Freeze first-failure predictions for the Go 1.24.6 carrier set.

Only reads carrier bytes. It never executes a carrier or invokes REA.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

W20 = os.path.dirname(os.path.abspath(__file__))
W17 = os.path.join(os.path.dirname(W20), "round-17")
PRED = os.path.join(W20, "predictions")
CARRIERS = os.path.join(PRED, "carriers.tsv")
BUILDINFO = os.path.join(W17, "tools/buildinfo-probe.py")
DEFAULT_EMULATOR = os.path.join(W20, "tools/swiss-misread-v2.py")
PY = [sys.executable, "-I", "-B"]
COLUMNS = ["label", "path", "class", "sha256"]
LABEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(argv):
    return subprocess.run(argv, capture_output=True, text=True)


def load_carriers():
    with open(CARRIERS, newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != COLUMNS:
            raise SystemExit("carriers.tsv must have columns: " + "\t".join(COLUMNS))
        carriers = []
        seen = set()
        for line, row in enumerate(reader, 2):
            label, path, carrier_class, digest = (row.get(key, "") for key in COLUMNS)
            if not label or not LABEL_RE.fullmatch(label) or label in seen:
                raise SystemExit("carriers.tsv:%d: invalid or duplicate label" % line)
            if not path or not carrier_class or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise SystemExit("carriers.tsv:%d: incomplete carrier record" % line)
            seen.add(label)
            carriers.append({"label": label, "path": path,
                             "class": carrier_class, "sha256": digest})
    return carriers


def write_json(path, value):
    with open(path, "w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")


def write_checksums():
    entries = []
    for root, dirs, files in os.walk(PRED):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(root, name)
            relative = os.path.relpath(path, PRED).replace(os.sep, "/")
            if relative != "SHA256SUMS":
                entries.append((relative, sha(path)))
    with open(os.path.join(PRED, "SHA256SUMS"), "w", encoding="utf-8",
              newline="\n") as stream:
        for relative, digest in sorted(entries):
            stream.write("%s  predictions/%s\n" % (digest, relative))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read held-out Go carriers and freeze H1 first-failure predictions.")
    parser.add_argument("--emulator", default=DEFAULT_EMULATOR,
                        help="path to swiss-misread-v2.py (defaults to W20/tools)")
    parser.add_argument("--snapshot-dir",
                        help="optional Go type-snapshot directory forwarded to the emulator")
    args = parser.parse_args(argv)
    emulator = os.path.abspath(args.emulator)
    if not os.path.isfile(BUILDINFO):
        raise SystemExit("buildinfo probe is missing: " + BUILDINFO)
    if not os.path.isfile(emulator):
        raise SystemExit("Swiss EmulatorV2 is missing; pass --emulator PATH: " + emulator)

    carriers = load_carriers()
    os.makedirs(os.path.join(PRED, "swiss-misread-v2"), exist_ok=True)
    excluded, table = [], []
    for carrier in carriers:
        label, path = carrier["label"], carrier["path"]
        try:
            current_sha = sha(path)
        except OSError as exc:
            raise SystemExit("%s: carrier is unreadable: %s" % (label, exc))
        if current_sha != carrier["sha256"]:
            raise SystemExit("%s: carrier sha256 differs from carriers.tsv" % label)

        probe = run(PY + [BUILDINFO, path])
        if probe.returncode != 0:
            raise SystemExit("%s: buildinfo probe exited %d: %s" %
                             (label, probe.returncode, probe.stderr.strip()))
        try:
            buildinfo = json.loads(probe.stdout)
        except json.JSONDecodeError as exc:
            raise SystemExit("%s: buildinfo probe returned invalid JSON: %s" % (label, exc))
        if buildinfo.get("sha256") != current_sha:
            raise SystemExit("%s: carrier changed while probing build info" % label)
        if not buildinfo.get("found") or not buildinfo.get("go_version"):
            excluded.append({
                "label": label, "path": path, "class": carrier["class"],
                "sha256": current_sha, "cause": "no Go build info",
                "probe_found": bool(buildinfo.get("found")),
                "probe_go_version": buildinfo.get("go_version"),
                "probe_limitations": buildinfo.get("limitations", []),
            })
            continue

        command = PY + [emulator, "--carrier", path, "--label", label]
        if args.snapshot_dir:
            command += ["--snapshot-dir", args.snapshot_dir]
        result = run(command)
        if result.returncode == 2:
            excluded.append({
                "label": label, "path": path, "class": carrier["class"],
                "sha256": current_sha,
                "cause": "emulator could not evaluate (exit 2); excluded before any analyze, as round-19 link",
                "emulator_output": (result.stdout or result.stderr).strip()[:400],
            })
            continue
        if result.returncode != 0:
            raise SystemExit("%s: emulator exited %d: %s" %
                             (label, result.returncode,
                              (result.stderr or result.stdout).strip()))
        try:
            prediction_result = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise SystemExit("%s: emulator returned invalid JSON: %s" % (label, exc))
        first_failure = prediction_result.get("first_failure")
        if not isinstance(first_failure, dict) or "h1" not in first_failure or "h0" not in first_failure:
            raise SystemExit("%s: emulator result lacks first_failure.h1/h0" % label)
        for hypothesis in ("h1", "h0"):
            if first_failure[hypothesis] is not None and not isinstance(first_failure[hypothesis], dict):
                raise SystemExit("%s: first_failure.%s must be an object or null" %
                                 (label, hypothesis))

        raw_path = os.path.join(PRED, "swiss-misread-v2", label + ".json")
        write_json(raw_path, prediction_result)
        frozen = {
            "label": label,
            "carrier": {"path": path, "class": carrier["class"], "sha256": current_sha},
            "first_failure": first_failure["h1"],
            "extra_expectations": [],
        }
        write_json(os.path.join(PRED, label + ".prediction.json"), frozen)
        h1, h0 = first_failure["h1"], first_failure["h0"]
        table.append({"label": label, "go_version": buildinfo["go_version"],
                      "h1": h1, "h0": h0, "d": h1 is not None and h0 is None})

    diagnostic = [row["label"] for row in table if row["d"]]
    decision = {
        "frozen_by": "KaidokuR20 before any round-20 REA analyze",
        "emulator": {"path": emulator, "sha256": sha(emulator)},
        "excluded": excluded,
        "D": diagnostic,
        "D_definition": "labels whose first_failure.h1 is non-null and first_failure.h0 is null",
        "compare_rule": "compare-first-failure",
        "binding_gate": "a label counts only if receipt-validate.py --require-mid-maps exits 0 on its receipt, the bound log's carrier sha256 equals the prediction's, and the prediction blob is unchanged from the freeze commit",
        "extra_expectations": "none",
        "table": table,
    }
    write_json(os.path.join(PRED, "decision-rule.json"), decision)
    write_checksums()
    print(json.dumps({"excluded": excluded, "D": diagnostic,
                      "predicted": [row["label"] for row in table]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
