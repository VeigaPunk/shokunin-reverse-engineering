import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('input_dir', nargs='?', type=Path, default=ROOT)
INPUT_DIR = parser.parse_args().input_dir
FIELDS = (
    'subject', 'provider', 'analysis_profile', 'predicate_type', 'operation',
    'parameters', 'raw_result', 'normalized_result', 'confidence', 'authority',
    'environment', 'limitations', 'relationship_coverage', 'locations',
    'evidence_links',
)

def projection(evidence):
    result = {field: evidence[field] for field in FIELDS if field in evidence}
    subject = evidence.get('subject')
    result['subject'] = None if subject is None else {
        field: subject[field]
        for field in ('digest', 'format', 'architecture')
        if field in subject
    }
    return result

def canonical_json(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(',', ':'),
    ).encode('utf-8')

def walk_path_keys(value, pointer=''):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f'{pointer}/{key}'
            if 'path' in key.lower():
                found.append(child_pointer)
            found.extend(walk_path_keys(child, child_pointer))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(walk_path_keys(child, f'{pointer}/{index}'))
    return found

def walk_string_hits(value, needle, pointer=''):
    if isinstance(value, str):
        return [pointer] if needle in value else []
    if isinstance(value, dict):
        return [hit for key, child in value.items()
                for hit in walk_string_hits(child, needle, f'{pointer}/{key}')]
    if isinstance(value, list):
        return [hit for index, child in enumerate(value)
                for hit in walk_string_hits(child, needle, f'{pointer}/{index}')]
    return []

records = []
for filename in ('probe-base.json', 'probe-copy.json', 'probe-base-repeat.json'):
    wrapper = json.loads((INPUT_DIR / filename).read_text())
    assert wrapper['ok'] is True, filename
    evidence = wrapper['data']
    projected = projection(evidence)
    canonical = canonical_json(projected)
    computed = 'ev_' + hashlib.sha256(canonical).hexdigest()
    records.append((filename, evidence, projected, canonical, computed))
    assert computed == evidence['evidence_id'], filename
    path_hits = walk_string_hits(projected, evidence['subject']['local_path'])
    assert not path_hits, (filename, path_hits)
    print(f'{filename}: actual={evidence["evidence_id"]} recomputed={computed} MATCH')
    print(f'  target={evidence["subject"]["local_path"]!r} digest={evidence["subject"]["digest"]["sha256"]}')
    print(f'  operation={evidence["operation"]!r} parameters={json.dumps(evidence["parameters"], sort_keys=True)}')
    print(f'  path_keys_in_projection={walk_path_keys(projected)} target_path_string_hits={path_hits}')

assert records[0][3] == records[1][3] == records[2][3]
base = records[0][1]
mutated = json.loads(json.dumps(base))
mutated['subject']['local_path'] = '/an/alternate/display/path/probe'
mutated['subject']['name'] = 'probe'
mutated_projection = projection(mutated)
mutated_digest = 'ev_' + hashlib.sha256(canonical_json(mutated_projection)).hexdigest()
assert mutated_digest == base['evidence_id']
print(f'projection_equal_base_copy_repeat=True')
print(f'display-path-only-mutation={mutated_digest} MATCH')
print(f'projection_sha256={hashlib.sha256(records[0][3]).hexdigest()} canonical_bytes={len(records[0][3])}')
