#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

FIELDS = (
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


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def semantic_projection(evidence):
    subject = evidence["subject"]
    projected_subject = None if subject is None else {
        key: subject[key] for key in ("digest", "format", "architecture")
    }
    return {
        "subject": projected_subject,
        **{key: evidence[key] for key in FIELDS},
    }


evidence_dir = pathlib.Path(sys.argv[1])
records = []
projections = []
for name in ("base1.json", "base2.json", "copy.json"):
    envelope = json.loads((evidence_dir / name).read_text())
    assert envelope["ok"] is True, (name, envelope)
    evidence = envelope["data"]
    projection = semantic_projection(evidence)
    projection_bytes = canonical_json(projection).encode("utf-8")
    computed_id = "ev_" + hashlib.sha256(projection_bytes).hexdigest()
    assert computed_id == evidence["evidence_id"], (name, computed_id, evidence["evidence_id"])
    assert evidence["raw_result"] == evidence["normalized_result"], name
    projections.append(projection_bytes)
    records.append({
        "file": name,
        "reported_evidence_id": evidence["evidence_id"],
        "recomputed_evidence_id": computed_id,
        "subject_path": evidence["subject"]["local_path"],
        "subject_name": evidence["subject"]["name"],
        "subject_sha256": evidence["subject"]["digest"]["sha256"],
        "parameters": evidence["parameters"],
        "analysis_profile_digest": evidence["analysis_profile"]["digest"],
        "raw_equals_normalized": True,
    })

assert len(set(projections)) == 1, "semantic projections differ"
assert len({row["reported_evidence_id"] for row in records}) == 1
print(json.dumps({
    "operation": "search_bytes",
    "canonicalization": "JSON.stringify-compatible compact JSON with sorted ASCII keys; UTF-8 SHA-256",
    "semantic_projection_identical": True,
    "all_reported_ids_recomputed": True,
    "all_reported_ids_equal": True,
    "records": records,
}, sort_keys=True, indent=2))
