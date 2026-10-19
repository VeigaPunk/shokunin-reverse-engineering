import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
fields = (
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

def canonical_digest(value):
    def assert_ascii_keys(node):
        if isinstance(node, dict):
            for key, item in node.items():
                key.encode("ascii")
                assert_ascii_keys(item)
        elif isinstance(node, list):
            for item in node:
                assert_ascii_keys(item)
    assert_ascii_keys(value)
    canonical = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

def recompute(evidence):
    projection = {
        key: evidence[key] if key != "subject" or evidence["subject"] is None else {
            "digest": evidence["subject"]["digest"],
            "format": evidence["subject"]["format"],
            "architecture": evidence["subject"]["architecture"],
        }
        for key in fields
    }
    return "ev_" + canonical_digest(projection)

def changed_paths(left, right, path=""):
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(set(left) | set(right)):
            child = f"{path}.{key}" if path else key
            if key not in left or key not in right:
                yield child
            else:
                yield from changed_paths(left[key], right[key], child)
    elif isinstance(left, list) and isinstance(right, list):
        for index, (a, b) in enumerate(zip(left, right)):
            yield from changed_paths(a, b, f"{path}[{index}]")
        if len(left) != len(right):
            yield f"{path}.length"
    elif left != right:
        yield path

records = {}
for name, filename in (("base1", "probe-base1.json"), ("base2", "probe-base2.json"), ("copy", "probe-copy.json")):
    wrapped = json.loads((root / filename).read_text())
    evidence = wrapped["data"]
    nested = evidence["normalized_result"]["substeps"][0]["evidence"]
    records[name] = (evidence, nested)
    print(json.dumps({
        "run": name,
        "operation": evidence["operation"],
        "target_path": evidence["subject"]["local_path"],
        "target_sha256": evidence["subject"]["digest"]["sha256"],
        "reported_evidence_id": evidence["evidence_id"],
        "recomputed_evidence_id": recompute(evidence),
        "reported_nested_inventory_id": nested["evidence_id"],
        "recomputed_nested_inventory_id": recompute(nested),
        "inspection_id": evidence["normalized_result"]["inspection_id"],
        "manifest_id": evidence["normalized_result"]["subject"]["manifest_id"],
        "coverage": evidence["normalized_result"]["coverage"],
        "complete": evidence["normalized_result"]["substeps"][0]["evidence"]["normalized_result"]["coverage"],
        "ids_match": evidence["evidence_id"] == recompute(evidence) and nested["evidence_id"] == recompute(nested),
    }, sort_keys=True))

print("same_path_data_equal=" + str(records["base1"][0] == records["base2"][0]))
print("base1_to_copy_changed_fields=" + json.dumps(list(changed_paths(records["base1"][0], records["copy"][0]))))
print("nested_inventory_ids_equal_across_paths=" + str(records["base1"][1]["evidence_id"] == records["copy"][1]["evidence_id"]))
