import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMON = (
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
    "locations",
    "evidence_links",
)


def projection(record):
    subject = record["subject"]
    value = {
        "subject": None
        if subject is None
        else {
            "digest": subject["digest"],
            "format": subject["format"],
            "architecture": subject["architecture"],
        }
    }
    value.update({key: record[key] for key in COMMON})
    if "relationship_coverage" in record:
        value["relationship_coverage"] = record["relationship_coverage"]
    return value


def evidence_id(record):
    encoded = json.dumps(
        projection(record),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return "ev_" + hashlib.sha256(encoded).hexdigest()


records = {}
for path in sorted((ROOT / "probes").glob("*.json")):
    record = json.loads(path.read_text())
    derived = evidence_id(record)
    display_only = copy.deepcopy(record)
    display_only["subject"]["name"] += ".renamed"
    display_only["subject"]["local_path"] += ".renamed"
    print(
        f"{path.stem} claimed={record['evidence_id']} derived={derived} "
        f"match={derived == record['evidence_id']} "
        f"display_only_same_id={evidence_id(display_only) == record['evidence_id']}"
    )
    records[path.stem] = record

for left, right in (
    ("67-base1", "67-base2"),
    ("67-base1", "67-copyA"),
    ("67-copyA", "67-copyB"),
    ("64-base", "64-copyA"),
):
    a, b = records[left], records[right]
    an, bn = a["normalized_result"], b["normalized_result"]
    same_bytecode = an["bytecode"]["sha256"] == bn["bytecode"]["sha256"]
    same_functions = an["functions"] == bn["functions"]
    print(
        f"pair={left}/{right} id_equal={a['evidence_id'] == b['evidence_id']} "
        f"parameter_path_equal={a['parameters']['path'] == b['parameters']['path']} "
        f"carrier_sha_equal={a['subject']['digest']['sha256'] == b['subject']['digest']['sha256']} "
        f"decoded_bytecode_equal={same_bytecode} function_payload_equal={same_functions}"
    )
