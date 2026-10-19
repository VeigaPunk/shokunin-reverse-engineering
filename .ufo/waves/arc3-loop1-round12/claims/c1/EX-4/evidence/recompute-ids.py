import copy
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent
names = ("base1", "base2", "copyA", "copyB")
fields = (
    "subject", "provider", "analysis_profile", "predicate_type", "operation",
    "parameters", "raw_result", "normalized_result", "confidence", "authority",
    "environment", "limitations", "relationship_coverage", "locations", "evidence_links",
)


def projection(envelope):
    evidence = envelope["data"]
    subject = evidence["subject"]
    selected = {key: evidence[key] for key in fields if key != "subject"}
    selected["subject"] = None if subject is None else {
        "digest": subject["digest"],
        "format": subject["format"],
        "architecture": subject["architecture"],
    }
    return selected


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return "ev_" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def paths_to_marker(value):
    result = copy.deepcopy(value)
    result["parameters"]["path"] = "<PATH>"
    result["normalized_result"]["artifact"]["path"] = "<PATH>"
    result["locations"][0]["path"] = "<PATH>"
    return result


def has_non_ascii(value):
    if isinstance(value, str):
        return any(ord(character) > 127 for character in value)
    if isinstance(value, list):
        return any(has_non_ascii(item) for item in value)
    if isinstance(value, dict):
        return any(has_non_ascii(key) or has_non_ascii(item) for key, item in value.items())
    return False


envelopes = {name: json.loads((root / "probes" / f"{name}.json").read_text()) for name in names}
projections = {name: projection(envelope) for name, envelope in envelopes.items()}
ids = {name: envelope["data"]["evidence_id"] for name, envelope in envelopes.items()}
recomputed = {name: digest(value) for name, value in projections.items()}
base = copy.deepcopy(envelopes["base1"])
base_projection = projection(base)
base["data"]["subject"]["name"] = "changed display name"
base["data"]["subject"]["local_path"] = "/not/a/semantic/path"
display_only_id = digest(projection(base))
path_variant = copy.deepcopy(envelopes["base1"])
copy_path = envelopes["copyA"]["data"]["parameters"]["path"]
path_variant["data"]["parameters"]["path"] = copy_path
path_variant["data"]["normalized_result"]["artifact"]["path"] = copy_path
path_variant["data"]["locations"][0]["path"] = copy_path
path_mutation_id = digest(projection(path_variant))
normalized = {name: paths_to_marker(value) for name, value in projections.items()}
results = {
    "evidence_ids": ids,
    "recomputed_ids": recomputed,
    "all_ids_recompute_exactly": ids == recomputed,
    "same_path_repeat_stable": ids["base1"] == ids["base2"],
    "distinct_copy_paths_distinct_ids": ids["copyA"] != ids["copyB"],
    "copy_ids_differ_from_original": ids["base1"] != ids["copyA"] and ids["base1"] != ids["copyB"],
    "semantic_projection_equal_after_masking_three_path_fields": all(value == normalized["base1"] for value in normalized.values()),
    "display_subject_fields_excluded": display_only_id == ids["base1"],
    "three_path_fields_alone_reproduce_copyA_id": path_mutation_id == ids["copyA"],
    "projection_contains_non_ascii": has_non_ascii(base_projection),
    "changed_projection_fields": ["parameters.path", "normalized_result.artifact.path", "locations[0].path"],
}
print(json.dumps(results, sort_keys=True, indent=2))
if not all((
    results["all_ids_recompute_exactly"],
    results["same_path_repeat_stable"],
    results["distinct_copy_paths_distinct_ids"],
    results["copy_ids_differ_from_original"],
    results["semantic_projection_equal_after_masking_three_path_fields"],
    results["display_subject_fields_excluded"],
    results["three_path_fields_alone_reproduce_copyA_id"],
    not results["projection_contains_non_ascii"],
)):
    raise SystemExit(1)
