import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "probes"


def load(name):
    return json.loads((ROOT / f"{name}.json").read_text())


for left, right in (("67-base1", "67-copyA"), ("67-copyA", "67-copyB"), ("64-base", "64-copyA")):
    a, b = load(left), load(right)
    changed = [key for key in a if key not in ("evidence_id", "subject") and a[key] != b[key]]
    an, bn = a["normalized_result"], b["normalized_result"]
    print(
        f"{left}/{right}: ids_differ={a['evidence_id'] != b['evidence_id']} "
        f"changed_record_fields={changed} "
        f"same_carrier_sha={a['subject']['digest']['sha256'] == b['subject']['digest']['sha256']} "
        f"same_decoded_sha={an['bytecode']['sha256'] == bn['bytecode']['sha256']} "
        f"same_functions={an['functions'] == bn['functions']} "
        f"same_subject_basename={a['subject']['name'] == b['subject']['name']}"
    )
    print(f"  parameters.path: {a['parameters']['path']} -> {b['parameters']['path']}")
    print(f"  normalized_result.artifact.path: {an['artifact']['path']} -> {bn['artifact']['path']}")
    print(f"  locations[0].path: {a['locations'][0]['path']} -> {b['locations'][0]['path']}")
