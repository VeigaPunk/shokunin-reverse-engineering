import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
FILES = ("probe-base1.json", "probe-base2.json", "probe-copy.json")
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


def projection(evidence):
    subject = evidence["subject"]
    return {
        "subject": None if subject is None else {
            "digest": subject["digest"],
            "format": subject["format"],
            "architecture": subject["architecture"],
        },
        **{field: evidence[field] for field in FIELDS},
    }


def evidence_id(evidence):
    value = projection(evidence)
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "ev_" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text())["data"]


base1 = load(FILES[0])
base2 = load(FILES[1])
copy_record = load(FILES[2])
records = {name: load(name) for name in FILES}
checks = {}
for name, record in records.items():
    reported = record["evidence_id"]
    recomputed = evidence_id(record)
    checks[name] = {"reported": reported, "recomputed": recomputed, "matches": reported == recomputed}
    nested = record["normalized_result"]["substeps"][0]["evidence"]
    checks[name]["nested_reported"] = nested["evidence_id"]
    checks[name]["nested_recomputed"] = evidence_id(nested)
    checks[name]["nested_matches"] = nested["evidence_id"] == evidence_id(nested)

display_mutation = copy.deepcopy(base1)
display_mutation["subject"]["name"] = "display-only-name"
display_mutation["subject"]["local_path"] = "/display-only/path.zip"
path_fields_restored = copy.deepcopy(copy_record)
path_fields_restored["subject"] = copy.deepcopy(base1["subject"])
path_fields_restored["normalized_result"]["inspection_id"] = base1["normalized_result"]["inspection_id"]
copy_nested = path_fields_restored["normalized_result"]["substeps"][0]["evidence"]
base_nested = base1["normalized_result"]["substeps"][0]["evidence"]
copy_nested["subject"] = copy.deepcopy(base_nested["subject"])

result = {
    "algorithm": "ev_ + SHA-256(UTF-8(compact JSON with sorted object keys) of the semantic projection)",
    "records": checks,
    "same_path_repeat_reproduces_outer_id": base1["evidence_id"] == base2["evidence_id"],
    "same_byte_copy_changes_outer_id": base1["subject"]["digest"] == copy_record["subject"]["digest"] and base1["evidence_id"] != copy_record["evidence_id"],
    "same_byte_copy_keeps_nested_inventory_id": base1["normalized_result"]["substeps"][0]["evidence"]["evidence_id"] == copy_record["normalized_result"]["substeps"][0]["evidence"]["evidence_id"],
    "top_level_display_only_mutation_preserves_id": evidence_id(display_mutation) == base1["evidence_id"],
    "restoring_copy_path_varying_output_fields_reproduces_base_id": evidence_id(path_fields_restored) == base1["evidence_id"],
    "path_varying_output_fields": [
        "normalized_result.inspection_id",
        "normalized_result.substeps[0].evidence.subject.name",
        "normalized_result.substeps[0].evidence.subject.local_path",
    ],
}
if not all(item["matches"] and item["nested_matches"] for item in checks.values()):
    raise SystemExit("reported Evidence ID did not match independent recomputation")
if not all(result[key] for key in (
    "same_path_repeat_reproduces_outer_id",
    "same_byte_copy_changes_outer_id",
    "same_byte_copy_keeps_nested_inventory_id",
    "top_level_display_only_mutation_preserves_id",
    "restoring_copy_path_varying_output_fields_reproduces_base_id",
)):
    raise SystemExit("an identity control did not reproduce")
print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
