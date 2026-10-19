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
GROUPS = {
    "inspect_evm_interface": ("evm-base-1", "evm-base-2", "evm-copy"),
    "inspect_rust_binary": ("rust-base-1", "rust-base-2", "rust-copy"),
    "inspect_artifact": ("artifact-base-1", "artifact-base-2", "artifact-copy"),
}


def evidence(label):
    return json.loads((ROOT / f"{label}.json").read_text())["data"]


def projection(record):
    subject = record.get("subject")
    result = {
        "subject": None
        if subject is None
        else {key: subject[key] for key in ("digest", "format", "architecture") if key in subject}
    }
    result.update({key: record[key] for key in FIELDS if key in record})
    return result


def recompute(record):
    canonical = json.dumps(
        projection(record),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(canonical).hexdigest()


def differences(left, right, path="$" ):
    if type(left) is not type(right):
        return [path]
    if isinstance(left, dict):
        changed = []
        for key in sorted(set(left) | set(right)):
            child = f"{path}.{key}"
            if key not in left or key not in right:
                changed.append(child)
            else:
                changed.extend(differences(left[key], right[key], child))
        return changed
    if isinstance(left, list):
        if len(left) != len(right):
            return [f"{path}.length"]
        changed = []
        for index, (a, b) in enumerate(zip(left, right)):
            changed.extend(differences(a, b, f"{path}[{index}]"))
        return changed
    return [] if left == right else [path]


for operation, (base_label, repeat_label, copy_label) in GROUPS.items():
    base, repeated, relocated = map(evidence, (base_label, repeat_label, copy_label))
    print(
        f"{operation}: base_match={recompute(base) == base['evidence_id']} "
        f"repeat_match={recompute(repeated) == repeated['evidence_id']} "
        f"copy_match={recompute(relocated) == relocated['evidence_id']} "
        f"same_path_repeat={base['evidence_id'] == repeated['evidence_id']} "
        f"relocated_id_changed={base['evidence_id'] != relocated['evidence_id']}"
    )
    print("  projection_diff=" + ",".join(differences(projection(base), projection(relocated))))
    display_only = copy.deepcopy(base)
    if isinstance(display_only.get("subject"), dict):
        display_only["subject"]["name"] = "display-only-changed"
        display_only["subject"]["local_path"] = "/display-only/changed"
    print(f"  top_subject_display_only_ignored={recompute(display_only) == base['evidence_id']}")
