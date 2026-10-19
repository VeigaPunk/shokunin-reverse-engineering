#!/usr/bin/env python3
import copy
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
NAMES = ("base1", "base2", "copy-a", "copy-b")
PROJECTION_KEYS = (
    "subject",
    "provider",
    "analysis_profile",
    "predicate_type",
    "operation",
    "parameters",
    "raw_result",
    "normalized_result",
    "confidence",
    "authority",
    "environment",
    "limitations",
    "relationship_coverage",
    "locations",
    "evidence_links",
)
PATHS = (
    ("parameters", "path"),
    ("normalized_result", "artifact", "path"),
    ("locations", 0, "path"),
)


def evidence(name):
    envelope = json.loads((ROOT / f"{name}.json").read_text())
    assert envelope["ok"] is True
    return envelope["data"]


def projection(record):
    subject = record["subject"]
    projected_subject = None if subject is None else {
        "digest": subject["digest"],
        "format": subject["format"],
        "architecture": subject.get("architecture"),
    }
    result = {key: record[key] for key in PROJECTION_KEYS}
    result["subject"] = projected_subject
    return result


def digest(record):
    canonical = json.dumps(
        projection(record),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(canonical).hexdigest()


def normalized_projection(record):
    result = projection(copy.deepcopy(record))
    for path in PATHS:
        cursor = result
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = "<PATH>"
    return result


records = {name: evidence(name) for name in NAMES}
for name, record in records.items():
    claimed = record["evidence_id"]
    computed = digest(record)
    print(f"{name}: claimed={claimed} recomputed={computed} match={claimed == computed}")
    assert claimed == computed
    assert record["operation"] == "inspect_go_binary"
    assert record["subject"]["digest"]["sha256"] == "70f68a7702346cf4bb1a2568091cfee92216cc8498a627a488c4b212bc5f45c9"

assert records["base1"]["evidence_id"] == records["base2"]["evidence_id"]
print("same_path_repeat=PASS (base1 and base2 IDs equal)")
assert len({records[name]["evidence_id"] for name in ("copy-a", "copy-b")}) == 2
assert records["base1"]["evidence_id"] not in {
    records["copy-a"]["evidence_id"], records["copy-b"]["evidence_id"]
}
print("same_bytes_different_paths=PASS (base, copy-a, and copy-b IDs differ)")
assert normalized_projection(records["base1"]) == normalized_projection(records["copy-a"])
assert normalized_projection(records["base1"]) == normalized_projection(records["copy-b"])
print("projection_equal_after_path-normalizing_parameters_artifact_and_location=PASS")

for name in ("copy-a", "copy-b"):
    altered = copy.deepcopy(records["base1"])
    for path in PATHS:
        cursor = altered
        for key in path[:-1]:
            cursor = cursor[key]
        other = records[name]
        for key in path:
            other = other[key]
        cursor[path[-1]] = other
    rehashed = digest(altered)
    print(f"base1_path-fields-replaced-with-{name}: recomputed={rehashed} target={records[name]['evidence_id']} match={rehashed == records[name]['evidence_id']}")
    assert rehashed == records[name]["evidence_id"]

altered_subject = copy.deepcopy(records["base1"])
altered_subject["subject"]["name"] = "display-only-mutated"
altered_subject["subject"]["local_path"] = "/display-only/mutated"
rehashed_subject = digest(altered_subject)
print(f"subject_display-only-mutation: recomputed={rehashed_subject} base={records['base1']['evidence_id']} match={rehashed_subject == records['base1']['evidence_id']}")
assert rehashed_subject == records["base1"]["evidence_id"]
