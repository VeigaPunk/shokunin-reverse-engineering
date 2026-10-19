import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
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
    projected_subject = (
        None
        if subject is None
        else {key: subject.get(key) for key in ("digest", "format", "architecture")}
    )
    return {
        "subject": projected_subject,
        **{key: evidence.get(key) for key in FIELDS},
    }


def digest(evidence):
    canonical = json.dumps(
        projection(evidence),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return "ev_" + hashlib.sha256(canonical.encode()).hexdigest()


def load(name):
    return json.loads((ROOT / name).read_text())["data"]


records = {
    name: load(name)
    for name in (
        "inspect-artifact-base-1.json",
        "inspect-artifact-base-2.json",
        "inspect-artifact-copy.json",
        "inspect-artifact-same-name-other-path.json",
    )
}
for name, evidence in records.items():
    computed = digest(evidence)
    print(
        f"{name}: reported={evidence['evidence_id']} recomputed={computed} "
        f"match={computed == evidence['evidence_id']} "
        f"name={evidence['subject']['name']} "
        f"path={evidence['subject']['local_path']} "
        f"sha256={evidence['subject']['digest']['sha256']}"
    )

base = copy.deepcopy(records["inspect-artifact-base-1.json"])
base["subject"]["name"] = "different-name"
base["subject"]["local_path"] = "/different/display/path"
print(
    "outer-display-fields-mutated: id_unchanged="
    f"{digest(base) == records['inspect-artifact-base-1.json']['evidence_id']}"
)

nested = copy.deepcopy(records["inspect-artifact-base-1.json"])
inner = nested["normalized_result"]["substeps"][0]["evidence"]["subject"]
inner["local_path"] = "/different/semantic-result/path/jq"
print(
    "nested-inventory-local-path-only-mutated: id_changed="
    f"{digest(nested) != records['inspect-artifact-base-1.json']['evidence_id']}"
)
print(
    "same-path-repeat-id="
    f"{records['inspect-artifact-base-1.json']['evidence_id'] == records['inspect-artifact-base-2.json']['evidence_id']}"
)
print(
    "different-path-same-name-same-bytes-id="
    f"{records['inspect-artifact-base-1.json']['evidence_id'] != records['inspect-artifact-same-name-other-path.json']['evidence_id']}"
)
print(
    "different-path-different-name-same-bytes-id="
    f"{records['inspect-artifact-base-1.json']['evidence_id'] != records['inspect-artifact-copy.json']['evidence_id']}"
)
