#!/usr/bin/env python3
"""Read-only inventory of the committed round-43 C1 heldout tree."""
import collections
import hashlib
import importlib.util
import json
import os
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
HELD = "corpus/evidence/round-43/c1/heldout"
EXPECTED = {"carrier.sqsh", "envelope.json", "rea-full.json", "run.json", "tree.json"}
sys.dont_write_bytecode = True

def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

spec = importlib.util.spec_from_file_location("c1counter", os.path.join(ROOT, "tools/round-43/c1-counter.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
home = os.path.join(ROOT, HELD)
manifest = json.load(open(os.path.join(home, "manifest.json")))
records = manifest["carriers"]
ids = [r["id"] for r in records]
class_counts = collections.Counter(r["class"] for r in records)
tc_obj = manifest["generator"]["tuple_check"]
tc = tc_obj["carriers"]
file_rows = []
file_mismatches = []
carrier_mismatches = []
subject_mismatches = []
tuple_mismatches = []
ood_ids = []
for record in records:
    cid = record["id"]
    folder = os.path.join(home, cid)
    names = set(os.listdir(folder))
    if names != EXPECTED:
        file_mismatches.append({"id": cid, "missing": sorted(EXPECTED - names), "extra": sorted(names - EXPECTED)})
    for name in sorted(names):
        path = os.path.join(folder, name)
        st = os.lstat(path)
        file_rows.append({"id": cid, "name": name, "regular": os.path.isfile(path) and not os.path.islink(path), "size_bytes": st.st_size, "sha256": sha(path)})
    carrier_path = os.path.join(folder, "carrier.sqsh")
    carrier_sha = sha(carrier_path)
    if record.get("sha256") != carrier_sha:
        carrier_mismatches.append(cid)
    envelope = json.load(open(os.path.join(folder, "envelope.json")))
    if mod.subject_sha(envelope) != carrier_sha:
        subject_mismatches.append(cid)
    observed = mod.observed_features(mod.envelope_data(envelope))
    observed_six = {key: observed.get(key) for key in tc_obj["fields"]}
    declaration = record.get("declared_features")
    row = tc.get(cid)
    if observed_six != declaration or not row or row.get("observed") != observed_six or row.get("declared") != declaration or row.get("equal") is not True:
        tuple_mismatches.append(cid)
    if record.get("class") == "out-of-domain":
        ood_ids.append(cid)
root_entries = sorted(os.listdir(home))
dirs = sorted(name for name in root_entries if os.path.isdir(os.path.join(home, name)))
summary = {
    "root_entries": len(root_entries), "carrier_dirs": len(dirs), "carrier_records": len(records),
    "unique_ids": len(set(ids)), "manifest_directory_sets_equal": set(ids) == set(dirs),
    "named_classes": len([name for name in manifest["classes"] if name != "combo"]),
    "class_counts": dict(sorted(class_counts.items())), "carrier_files": len(file_rows),
    "all_five_regular_files": len(file_rows) == 390 and all(row["regular"] for row in file_rows) and not file_mismatches,
    "file_mismatches": file_mismatches, "carrier_sha_mismatches": carrier_mismatches,
    "subject_sha_mismatches": subject_mismatches, "tuple_fields": tc_obj["fields"],
    "tuple_check_count": len(tc), "tuple_check_equal_true": sum(row.get("equal") is True for row in tc.values()),
    "tuple_check_all_equal": tc_obj.get("all_equal"), "tuple_check_measured": tc_obj.get("measured"),
    "tuple_check_ids_equal_manifest": set(tc) == set(ids), "observed_tuple_mismatches": tuple_mismatches,
    "ood_ids": sorted(ood_ids), "effective_n_if_ood_vacuous": len(records) - len(ood_ids),
    "seed": manifest.get("seed"),
}
print(json.dumps(summary, indent=2, sort_keys=True))
