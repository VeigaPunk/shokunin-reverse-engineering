import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
EVIDENCE = ROOT / ".ufo/waves"
RECORDS = {
    "evm-base": ("arc3-loop1-round7/claims/c2/EX-3/evidence/probes/67-base1.json", False),
    "evm-copy": ("arc3-loop1-round7/claims/c2/EX-3/evidence/probes/67-copyA.json", False),
    "rust-base": ("arc3-loop1-round10/claims/c1/EX-4/evidence/probe-base1.json", True),
    "rust-copy": ("arc3-loop1-round10/claims/c1/EX-4/evidence/probe-copyA.json", True),
    "artifact-base": ("arc3-loop1-round11/claims/c1/CR-2/evidence/inspect-artifact-base-1.json", True),
    "artifact-same-name-copy": ("arc3-loop1-round11/claims/c1/CR-2/evidence/inspect-artifact-same-name-other-path.json", True),
}
FIELDS = (
    "provider", "analysis_profile", "predicate_type", "operation", "parameters",
    "raw_result", "normalized_result", "confidence", "authority", "environment",
    "limitations", "relationship_coverage", "locations", "evidence_links",
)


def load_record(name):
    relative_path, wrapped = RECORDS[name]
    value = json.loads((EVIDENCE / relative_path).read_text())
    return value["data"] if wrapped else value


def projection(record):
    subject = record["subject"]
    projected = {
        "subject": None if subject is None else {
            key: subject[key] for key in ("digest", "format", "architecture")
        }
    }
    projected.update({key: record[key] for key in FIELDS if key in record})
    return projected


def evidence_id(record):
    canonical = json.dumps(
        projection(record), ensure_ascii=False, allow_nan=False,
        sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(canonical).hexdigest()


def diff_paths(left, right, prefix=""):
    if isinstance(left, dict) and isinstance(right, dict):
        changes = []
        for key in sorted(set(left) | set(right)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                changes.append(path)
            else:
                changes.extend(diff_paths(left[key], right[key], path))
        return changes
    if isinstance(left, list) and isinstance(right, list):
        changes = []
        for index, (a, b) in enumerate(zip(left, right)):
            changes.extend(diff_paths(a, b, f"{prefix}[{index}]"))
        if len(left) != len(right):
            changes.append(prefix + ".length")
        return changes
    return [] if left == right else [prefix]


pairs = (
    ("inspect-evm-interface", "evm-base", "evm-copy"),
    ("inspect_rust_binary", "rust-base", "rust-copy"),
    ("inspect_artifact", "artifact-base", "artifact-same-name-copy"),
)
records = {name: load_record(name) for name in RECORDS}
for family, base_name, copy_name in pairs:
    base, copied = records[base_name], records[copy_name]
    print(
        f"{family}: recompute_base_matches={evidence_id(base) == base['evidence_id']}; "
        f"recompute_copy_matches={evidence_id(copied) == copied['evidence_id']}; "
        f"same_subject_digest={base['subject']['digest'] == copied['subject']['digest']}; "
        f"observed_ids_differ={base['evidence_id'] != copied['evidence_id']}; "
        f"projection_deltas={diff_paths(projection(base), projection(copied))}"
    )

rust = copy.deepcopy(records["rust-base"])
rust["subject"]["name"] += ".changed"
rust["subject"]["local_path"] += ".changed"
rust_display_stable = evidence_id(rust) == records["rust-base"]["evidence_id"]

artifact = copy.deepcopy(records["artifact-base"])
artifact["subject"]["name"] += ".changed"
artifact["subject"]["local_path"] += ".changed"
artifact_display_stable = evidence_id(artifact) == records["artifact-base"]["evidence_id"]

artifact = copy.deepcopy(records["artifact-base"])
artifact["normalized_result"]["substeps"][0]["evidence"]["subject"]["local_path"] += ".changed"
artifact_nested_path_sensitive = evidence_id(artifact) != records["artifact-base"]["evidence_id"]

print(f"inspect_rust_binary: top_level_display_mutation_preserves_id={rust_display_stable}")
print(
    f"inspect_artifact: top_level_display_mutation_preserves_id={artifact_display_stable}; "
    f"nested_inventory_path_mutation_changes_id={artifact_nested_path_sensitive}"
)
