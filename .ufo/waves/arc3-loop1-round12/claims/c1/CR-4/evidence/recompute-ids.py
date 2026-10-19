import copy
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
files = {name: json.loads((root / f"{name}.json").read_text()) for name in ("base-1", "base-2", "copy-a", "copy-b")}
keys = (
    "subject", "provider", "analysis_profile", "predicate_type", "operation",
    "parameters", "raw_result", "normalized_result", "confidence", "authority",
    "environment", "limitations", "relationship_coverage", "locations", "evidence_links",
)

def projection(envelope):
    evidence = envelope["data"]
    subject = evidence["subject"]
    return {
        "subject": None if subject is None else {
            "digest": subject["digest"],
            "format": subject["format"],
            "architecture": subject["architecture"],
        },
        **{key: evidence[key] for key in keys[1:]},
    }

def digest(value):
    encoded = json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return "ev_" + hashlib.sha256(encoded).hexdigest()

def differences(left, right, path=""):
    out = []
    if isinstance(left, dict) and isinstance(right, dict):
        for key in sorted(set(left) | set(right)):
            child = f"{path}.{key}" if path else key
            if key not in left or key not in right:
                out.append(child)
            else:
                out.extend(differences(left[key], right[key], child))
    elif isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            out.append(path + ".length")
        else:
            for i, (a, b) in enumerate(zip(left, right)):
                out.extend(differences(a, b, f"{path}[{i}]"))
    elif left != right:
        out.append(path)
    return out

for name, envelope in files.items():
    actual = envelope["data"]["evidence_id"]
    calculated = digest(projection(envelope))
    print(f"{name}: reported={actual} recomputed={calculated} match={actual == calculated}")
    assert actual == calculated

base = files["base-1"]
copy_a = files["copy-a"]
copy_b = files["copy-b"]
base_projection = projection(base)
copy_a_projection = projection(copy_a)
changed = differences(base_projection, copy_a_projection)
print("base-to-copy-a projection differences=" + json.dumps(changed, separators=(",", ":")))
assert changed == [
    "locations[0].path",
    "normalized_result.artifact.path",
    "parameters.path",
]

renamed_display = copy.deepcopy(base)
renamed_display["data"]["subject"]["name"] = "display-only-change"
renamed_display["data"]["subject"]["local_path"] = "/display-only/path"
print("display-only mutation id=" + digest(projection(renamed_display)))
assert digest(projection(renamed_display)) == base["data"]["evidence_id"]

path_mutated = copy.deepcopy(base)
new_path = copy_a["data"]["parameters"]["path"]
path_mutated["data"]["parameters"]["path"] = new_path
path_mutated["data"]["normalized_result"]["artifact"]["path"] = new_path
path_mutated["data"]["locations"][0]["path"] = new_path
print("base-with-copy-a-semantic-paths id=" + digest(projection(path_mutated)))
assert digest(projection(path_mutated)) == copy_a["data"]["evidence_id"]
assert base["data"]["subject"]["digest"] == copy_a["data"]["subject"]["digest"] == copy_b["data"]["subject"]["digest"]
assert base["data"]["normalized_result"]["artifact"]["sha256"] == copy_a["data"]["normalized_result"]["artifact"]["sha256"] == copy_b["data"]["normalized_result"]["artifact"]["sha256"]
assert copy_a["data"]["evidence_id"] != copy_b["data"]["evidence_id"]
print("same-byte-copy IDs differ; identity digests match=" + base["data"]["subject"]["digest"]["sha256"])
