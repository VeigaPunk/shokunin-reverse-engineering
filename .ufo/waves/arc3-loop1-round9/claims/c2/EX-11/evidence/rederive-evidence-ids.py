import copy
import hashlib
import json
from pathlib import Path

root = Path(__file__).parent
files = ["go-base-1.json", "go-base-2.json", "go-copy.json"]
fields = [
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
]
records = [(root / name).read_bytes() for name in files]
envelopes = [json.loads(data) for data in records]
assert records[0] == records[1]

def projection(envelope):
    value = {field: envelope[field] for field in fields}
    subject = envelope["subject"]
    value["subject"] = {
        "digest": subject["digest"],
        "format": subject["format"],
        "architecture": subject["architecture"],
    }
    return value

def recompute(envelope):
    encoded = json.dumps(
        projection(envelope),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(encoded).hexdigest()

def redact_request_paths(envelope):
    value = copy.deepcopy(projection(envelope))
    value["parameters"]["path"] = "<path>"
    value["normalized_result"]["artifact"]["path"] = "<path>"
    artifact_paths = [location for location in value["locations"] if location["kind"] == "artifact-path"]
    assert len(artifact_paths) == 1
    artifact_paths[0]["path"] = "<path>"
    return value

rows = []
for name, envelope in zip(files, envelopes):
    computed = recompute(envelope)
    assert computed == envelope["evidence_id"]
    rows.append({
        "file": name,
        "evidence_id_recorded": envelope["evidence_id"],
        "evidence_id_recomputed": computed,
        "matches": computed == envelope["evidence_id"],
        "request_path": envelope["parameters"]["path"],
        "subject_sha256": envelope["subject"]["digest"]["sha256"],
        "artifact_bytes": envelope["normalized_result"]["artifact"]["bytes"],
        "artifact_path": envelope["normalized_result"]["artifact"]["path"],
        "subject_name": envelope["subject"]["name"],
    })

assert rows[0]["evidence_id_recorded"] == rows[1]["evidence_id_recorded"]
assert rows[0]["evidence_id_recorded"] != rows[2]["evidence_id_recorded"]
assert len({row["subject_sha256"] for row in rows}) == 1
assert len({row["artifact_bytes"] for row in rows}) == 1
assert redact_request_paths(envelopes[0]) == redact_request_paths(envelopes[2])
print(json.dumps({
    "same_path_envelopes_byte_identical": records[0] == records[1],
    "same_bytes_across_all_paths": len({row["subject_sha256"] for row in rows}) == 1,
    "projection_equal_after_redacting_three_path_fields": redact_request_paths(envelopes[0]) == redact_request_paths(envelopes[2]),
    "results": rows,
}, sort_keys=True, indent=2))
