#!/usr/bin/env python3
"""Round-18 L1 prediction freezer (C3). For every row of predictions/carriers.tsv:
read the carrier's build-info version (round-17 buildinfo-probe.py), predict the
snapshot route (round-17 predict.py), predict the post-bootstrap symbol-markup
outcome under H1 (Ghidra binds OldMapType for Swiss descriptors) and H0 (true
layout) with tools/swiss-misread.py, and write <label>.prediction.json carrying
the route expectation plus the H1 outcome as compare.py extra_expectations.
Also writes predictions/swiss-misread/<label>.json (full emulator output),
decision-rule.json and SHA256SUMS. Never executes a carrier, never runs REA.
Run once before any round-18 carrier analysis; the outputs are committed first.
"""
import hashlib
import json
import os
import subprocess
import sys

W18 = os.path.dirname(os.path.abspath(__file__))
W17 = os.path.join(os.path.dirname(W18), "round-17")
GODATA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
PY = [sys.executable, "-I", "-B"]
PRED = os.path.join(W18, "predictions")


def run_json(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit("failed (%d): %s\n%s" % (p.returncode, " ".join(argv), p.stderr))
    return json.loads(p.stdout)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(PRED, "carriers.tsv")) if l.strip()]
    os.makedirs(os.path.join(PRED, "swiss-misread"), exist_ok=True)
    table = []
    for row in rows:
        label, path = row[0], row[1]
        bi = run_json(PY + [os.path.join(W17, "tools/buildinfo-probe.py"), path])
        ver = bi.get("go_version")
        route = run_json(PY + [os.path.join(W17, "tools/predict.py"), "--go-version", ver,
                               "--golang-root", GODATA])
        sm = run_json(PY + [os.path.join(W18, "tools/swiss-misread.py"), "--carrier", path,
                            "--golang-root", GODATA])
        with open(os.path.join(PRED, "swiss-misread", label + ".json"), "w") as f:
            json.dump(sm, f, sort_keys=True, indent=2)
        kind = sm["predicted_failure_kind_h1"]
        if kind == "unknown":
            raise SystemExit("%s: H1 outcome unknown; not frozen" % label)
        extra = {"eof_reads": sm["predicted_eof_reads_h1"],
                 "invalid_index_reads": sm["predicted_invalid_index_reads_h1"]}
        if kind == "none":
            extra["analyzer_errors_empty"] = True
        else:
            extra["analyzer_errors_contain"] = "Go analysis failure"
        pred = dict(route)
        pred["extra_expectations"] = extra
        pred["carrier"] = {"path": path, "sha256": sha(path)}
        pred["c3"] = {"hypothesis_frozen": "H1",
                      "h1_kind": kind, "h0_kind": sm["predicted_failure_kind_h0"],
                      "diagnostic": sm["diagnostic"],
                      "uncommon_map_types": sm["uncommon_map_types"],
                      "misread_map_types": sm["misread_map_types"],
                      "true_kind": sm["layout"]["true_kind"],
                      "emulator": "tools/swiss-misread.py",
                      "emulator_sha256": sha(os.path.join(W18, "tools/swiss-misread.py"))}
        with open(os.path.join(PRED, label + ".prediction.json"), "w") as f:
            json.dump(pred, f, sort_keys=True, indent=2)
        table.append({"label": label, "go_version": ver, "route": route["expected"]["snapshot_route"],
                      "fallback_to": route["expected"]["fallback_to"], "h1": kind,
                      "h0": sm["predicted_failure_kind_h0"], "diagnostic": sm["diagnostic"],
                      "eof_reads_h1": extra["eof_reads"], "invalid_index_reads_h1": extra["invalid_index_reads"]})
    diag = [t["label"] for t in table if t["diagnostic"]]
    rule = {
        "frozen_by": "L1 KaidokuR18 before any round-18 REA run",
        "calibration_only": ["calib-aether", "calib-notesmd-cli"],
        "diagnostic_set_D": diag,
        "held_out_D": [d for d in diag if not d.startswith("calib-")],
        "binding_gate": "a label counts only if receipt-validate.py --require-mid-maps exits 0 on its receipt, the bound log's carrier sha256 equals the prediction's, and the prediction blob is unchanged from the freeze commit",
        "confirmed": "every held-out D label shows its exact H1 outcome (analyzer_errors contain 'Go analysis failure' and eof_reads/invalid_index_reads equal the frozen lists) AND every noswiss sibling of a D label shows no Go analysis failure AND no non-D synthetic label shows a failure",
        "refuted": "any held-out D label shows the H0 outcome (no Go analysis failure), OR any noswiss synthetic label fails, OR a Swiss label fails with a read not predicted under H1",
        "unresolved": "anything else (e.g. route mismatch, unbound log, timeout, a D label failing with a different read)",
        "route_fields": "compared separately by compare.py; a route mismatch is reported, not a mechanism verdict",
        "count_rule": "the C3 count is labels with a bound retained log and a compare.json carrying extra.eof_reads; match or not is reported per label",
        "table": table,
    }
    with open(os.path.join(PRED, "decision-rule.json"), "w") as f:
        json.dump(rule, f, sort_keys=True, indent=2)
    names = sorted(n for n in os.listdir(PRED) if n != "SHA256SUMS" and os.path.isfile(os.path.join(PRED, n)))
    names += sorted("swiss-misread/" + n for n in os.listdir(os.path.join(PRED, "swiss-misread")))
    with open(os.path.join(PRED, "SHA256SUMS"), "w") as f:
        for n in names:
            f.write("%s  predictions/%s\n" % (sha(os.path.join(PRED, n)), n))
    for t in table:
        print(json.dumps(t, sort_keys=True))


if __name__ == "__main__":
    main()
