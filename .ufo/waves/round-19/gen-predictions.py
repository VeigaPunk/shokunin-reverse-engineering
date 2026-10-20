#!/usr/bin/env python3
"""Round-19 L1 prediction freezer (C3). Same method as round 18's gen-predictions.py
(round-17 buildinfo-probe.py + predict.py for the snapshot route, the UNCHANGED round-18
tools/swiss-misread.py for the H1/H0 symbol-markup outcome) over the official go1.25.0
toolchain binaries in /home/vgpnk/.local/opt/go-1.25.0 (held-out artifacts: never in the
round-17/18 calibration or prediction sets). Two deliberate differences, both decided before
any round-19 REA run:
- D (diagnostic set) is formed from the map-path booleans (predicted_failure_h1 true and
  predicted_failure_h0 false), not from swiss-misread's `diagnostic` field: that field
  compares kinds that also absorb the full-walk failure (w1 H0H1Semantics.md), so it reads
  false for vet although only H1 fails on the map path.
- Carriers with no Go build info (link) are excluded and recorded, not predicted.
Writes predictions/<label>.prediction.json, predictions/swiss-misread/<label>.json,
carriers.tsv, decision-rule.json, SHA256SUMS. Never executes a carrier, never runs REA.
"""
import hashlib
import json
import os
import subprocess
import sys

W19 = os.path.dirname(os.path.abspath(__file__))
W17 = os.path.join(os.path.dirname(W19), "round-17")
W18 = os.path.join(os.path.dirname(W19), "round-18")
GODATA = "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
GO = "/home/vgpnk/.local/opt/go-1.25.0"
NAMES = [("go", "bin/go"), ("gofmt", "bin/gofmt")] + [
    (n, "pkg/tool/linux_amd64/" + n) for n in ("asm", "cgo", "compile", "cover", "link", "preprofile", "vet")]
PY = [sys.executable, "-I", "-B"]
PRED = os.path.join(W19, "predictions")
SM = os.path.join(W18, "tools/swiss-misread.py")


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    os.makedirs(os.path.join(PRED, "swiss-misread"), exist_ok=True)
    table, excluded, tsv = [], [], []
    for name, rel in NAMES:
        label, path = "t1250-" + name, os.path.join(GO, rel)
        rc, out, err = run(PY + [SM, "--carrier", path, "--golang-root", GODATA])
        sm = json.loads(out) if out.strip() else {"status": "no-output", "stderr": err}
        with open(os.path.join(PRED, "swiss-misread", label + ".json"), "w") as f:
            json.dump(sm, f, sort_keys=True, indent=2)
        if rc != 0 or sm.get("status") == "unparseable" or "predicted_failure_kind_h1" not in sm:
            excluded.append({"label": label, "path": path, "sha256": sha(path), "emulator_exit": rc,
                             "cause": sm.get("error") or sm.get("status")})
            continue
        rc, out, err = run(PY + [os.path.join(W17, "tools/buildinfo-probe.py"), path])
        if rc != 0:
            raise SystemExit("%s: buildinfo-probe failed: %s" % (label, err))
        ver = json.loads(out).get("go_version")
        rc, out, err = run(PY + [os.path.join(W17, "tools/predict.py"), "--go-version", ver,
                                 "--golang-root", GODATA])
        if rc != 0:
            raise SystemExit("%s: predict.py failed: %s" % (label, err))
        route = json.loads(out)
        kind = sm["predicted_failure_kind_h1"]
        if kind == "unknown":
            raise SystemExit("%s: H1 outcome unknown; not frozen" % label)
        extra = {"eof_reads": sm["predicted_eof_reads_h1"],
                 "invalid_index_reads": sm["predicted_invalid_index_reads_h1"]}
        if kind == "none":
            extra["analyzer_errors_empty"] = True
        else:
            extra["analyzer_errors_contain"] = "Go analysis failure"
        d = bool(sm["predicted_failure_h1"]) and not bool(sm["predicted_failure_h0"])
        pred = dict(route)
        pred["extra_expectations"] = extra
        pred["carrier"] = {"path": path, "sha256": sha(path)}
        pred["c3"] = {"hypothesis_frozen": "H1", "h1_kind": kind,
                      "h1_map_path_failure": sm["predicted_failure_h1"],
                      "h0_map_path_failure": sm["predicted_failure_h0"],
                      "h0_reads_including_walk": {"eof": sm["predicted_eof_reads_h0"],
                                                  "invalid_index": sm["predicted_invalid_index_reads_h0"]},
                      "diagnostic_r19": d, "emulator_diagnostic_field": sm["diagnostic"],
                      "uncommon_map_types": sm.get("uncommon_map_types"),
                      "misread_map_types": sm["misread_map_types"],
                      "true_kind": sm["layout"]["true_kind"],
                      "emulator": "round-18/tools/swiss-misread.py", "emulator_sha256": sha(SM)}
        with open(os.path.join(PRED, label + ".prediction.json"), "w") as f:
            json.dump(pred, f, sort_keys=True, indent=2)
        tsv.append("\t".join([label, path, "held-out-toolchain", sha(path)]))
        table.append({"label": label, "go_version": ver, "route": route["expected"]["snapshot_route"],
                      "fallback_to": route["expected"]["fallback_to"], "h1": kind, "d": d,
                      "invalid_index_reads_h1": extra["invalid_index_reads"],
                      "invalid_index_reads_h0_incl_walk": sm["predicted_invalid_index_reads_h0"],
                      "eof_reads_h1": extra["eof_reads"]})
    with open(os.path.join(PRED, "carriers.tsv"), "w") as f:
        f.write("\n".join(tsv) + "\n")
    diag = [t["label"] for t in table if t["d"]]
    h1_only = {t["label"]: sorted(set(t["invalid_index_reads_h1"]) - set(t["invalid_index_reads_h0_incl_walk"]))
               for t in table if t["d"]}
    walk = {t["label"]: sorted(set(t["invalid_index_reads_h0_incl_walk"])) for t in table if t["d"]}
    rule = {
        "frozen_by": "L1 KaidokuR19 before any round-19 REA analyze",
        "held_out": "official go1.25.0 linux-amd64 toolchain binaries (archive sha256 2852af0c...b613 per go.dev JSON); none was in the round-17/18 calibration or prediction sets",
        "excluded": excluded,
        "diagnostic_set_D": diag,
        "D_definition": "map-path booleans: predicted_failure_h1 true and predicted_failure_h0 false (round-18 used the emulator's `diagnostic` field, which absorbs the full-walk failure; w1 H0H1Semantics.md)",
        "h1_only_invalid_indexes": h1_only,
        "walk_invalid_indexes_both_hypotheses": walk,
        "binding_gate": "a label counts only if receipt-validate.py --require-mid-maps exits 0 on its receipt, the bound log's carrier sha256 equals the prediction's, and the prediction blob is unchanged from the freeze commit",
        "confirmed": "every D label's bound ghidra.log reports a Go analysis failure whose Invalid index value(s) include at least one h1_only_invalid_indexes value and no index outside the frozen H1 list, AND every non-D label shows no Go analysis failure",
        "h0_consistent": "a D label's only reported Invalid index values are walk_invalid_indexes_both_hypotheses values (the failure does not discriminate H1 from H0 for that label)",
        "refuted": "a D label shows no Go analysis failure, OR a non-D label fails, OR a D label fails with an index or EOF read predicted under neither hypothesis",
        "unresolved": "anything else (route mismatch, unbound log, timeout)",
        "compare_note": "compare.py checks the frozen extra_expectations (full H1 lists, as in round 18); its exit is reported per label; the mechanism verdict above is decided from the bound log",
        "count_rule": "the C3 count is held-out labels with a bound retained log and a compare.json; match or not is reported per label",
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
    print(json.dumps({"excluded": excluded, "D": diag, "h1_only": h1_only}))


if __name__ == "__main__":
    main()
