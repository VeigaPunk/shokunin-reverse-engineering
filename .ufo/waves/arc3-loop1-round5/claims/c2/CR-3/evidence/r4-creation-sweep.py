import json
from pathlib import Path

root = Path('.ufo/waves/arc3-loop1-round4/claims/c1')
paths = sorted(path for path in root.rglob('*.json') if 'creation' in path.name.lower())
for path in paths:
    envelope = json.loads(path.read_text())
    normalized = envelope.get('normalized_result')
    raw = envelope.get('raw_result')
    if not isinstance(normalized, dict) or not isinstance(normalized.get('functions'), list):
        raise SystemExit(f'{path}: missing normalized_result.functions')
    if not isinstance(raw, dict) or not isinstance(raw.get('functions'), list):
        raise SystemExit(f'{path}: missing raw_result.functions')
    normalized_count = len(normalized['functions'])
    raw_count = len(raw['functions'])
    print(f'{path}: normalized={normalized_count} raw={raw_count}')
    if normalized_count or raw_count:
        raise SystemExit(f'{path}: expected parsed-and-empty creation result')
print(f'TOTAL files={len(paths)} all_zero={bool(paths)}')
