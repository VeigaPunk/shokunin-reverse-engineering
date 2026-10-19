import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = (
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


def projection(evidence):
    subject = evidence["subject"]
    projected_subject = None if subject is None else {
        "digest": subject["digest"],
        "format": subject["format"],
        "architecture": subject["architecture"],
    }
    return {"subject": projected_subject, **{key: evidence[key] for key in FIELDS[1:]}}


def digest(evidence):
    encoded = json.dumps(
        projection(evidence),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(encoded).hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text())["data"]


names = (
    "probe-base1.json",
    "probe-base2.json",
    "probe-same-name-copy.json",
    "probe-other-name-copy.json",
)
evidence = [load(name) for name in names]
ids = [digest(item) for item in evidence]
base_path = evidence[0]["parameters"]["path"]
copy_results = []
for name, item, recomputed in zip(names, evidence, ids):
    display_only = copy.deepcopy(item)
    display_only["subject"]["name"] = "display-name-sentinel"
    display_only["subject"]["local_path"] = "/display/path/sentinel"
    semantic_paths_rebound = copy.deepcopy(item)
    semantic_paths_rebound["parameters"]["path"] = base_path
    semantic_paths_rebound["normalized_result"]["artifact"]["path"] = base_path
    for location in semantic_paths_rebound["locations"]:
        if location["kind"] == "artifact-path":
            location["path"] = base_path
    copy_results.append({
        "file": name,
        "reported_id": item["evidence_id"],
        "recomputed_id": recomputed,
        "id_match": recomputed == item["evidence_id"],
        "subject_name": item["subject"]["name"],
        "subject_local_path": item["subject"]["local_path"],
        "parameters_path": item["parameters"]["path"],
        "normalized_artifact_path": item["normalized_result"]["artifact"]["path"],
        "artifact_location_path": next(
            location["path"] for location in item["locations"]
            if location["kind"] == "artifact-path"
        ),
        "display_only_mutation_preserves_id": digest(display_only) == recomputed,
        "semantic_path_rebind_id": digest(semantic_paths_rebound),
        "semantic_path_rebind_matches_base": digest(semantic_paths_rebound) == ids[0],
    })

print(json.dumps({
    "algorithm": "ev_ + lowercase SHA-256 of UTF-8 compact canonical JSON semantic projection",
    "projection_fields": list(FIELDS),
    "results": copy_results,
    "same_path_repeat_equal": ids[0] == ids[1],
    "same_bytes_same_basename_other_path_changes_id": ids[0] != ids[2],
    "same_bytes_different_basename_other_path_changes_id": ids[0] != ids[3],
    "all_reported_ids_recomputed": all(row["id_match"] for row in copy_results),
}, sort_keys=True, indent=2))
