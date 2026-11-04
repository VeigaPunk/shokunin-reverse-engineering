"""Read-only bounded R83 claim review: no target/counter/fixture changes."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
OUT = Path(ROOT) / '.ufo/waves/round-83/w1/ReviewerClaim/receipts'
FREEZE = 'de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e'
BASE = '650344bc37ca303fb9487c1174192057af499b9b'
def blob(rev, path):
    return subprocess.check_output(['git', '-C', ROOT, 'show', rev + ':' + path])
raw = blob(FREEZE, 'tools/round-83/attribution-audit.py')
ns = {'__name__': 'review_only', '__file__': ROOT + '/tools/round-83/attribution-audit.py'}
exec(compile(raw, '<frozen-counter>', 'exec'), ns)
fixtures = blob(FREEZE, '.ufo/waves/round-83/attribution-cases.json')
cases = json.loads(fixtures)
actual = blob(BASE, ns['ENTRY']).decode()
legacy = ns['load_function'](blob(BASE, ns['OLD']))
# Deliberately inadequate implementation to exhibit finite-suite overfitting.
# This is a review control only, not a proposed or substituted target.
def overfit(text, sid):
    return sid == 'S286' or (sid == 'S299' and text.startswith(('source: S299 —', 'source: S286, S299 —')))
subjects = {'actual_legacy': legacy, 'refuse_everything': lambda text, sid: False, 'review_overfit_control': overfit}
result = {'counter_sha256': hashlib.sha256(raw).hexdigest(), 'fixture_sha256': hashlib.sha256(fixtures).hexdigest(), 'entry_sha256': hashlib.sha256(actual.encode()).hexdigest(), 'frozen_scores': {}}
for name, fn in subjects.items():
    rows = ns['score'](fn, cases, actual)
    result['frozen_scores'][name] = {'mismatches': [r['id'] for r in rows if not r['matched']], 'rows': rows}
extra = [
    ('new-valid-id', 'source: S300 — primary\n', 'S300', True),
    ('duplicate-header', 'source: S299 — primary\nsource: S300 — secondary\n', 'S299', False),
    ('absent-primary', '# no source header\n', 'S286', False),
    ('thirteenth-line', '\n' * 12 + 'source: S299 — primary\n', 'S299', False),
]
result['independent_overfit_counterexamples'] = [{'id': name, 'text': text, 'sid': sid, 'expected': expected, 'observed': overfit(text, sid)} for name, text, sid, expected in extra]
(OUT / 'bounded-probe.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'frozen_scores': {k: v['mismatches'] for k, v in result['frozen_scores'].items()}, 'counterexamples': result['independent_overfit_counterexamples'], 'hashes': {k: v for k, v in result.items() if k.endswith('sha256')}}, indent=2))
