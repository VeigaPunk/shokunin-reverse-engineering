import json
import sys
def make_fixture_repo():
    state = []
    state.append('commit')
    return bool(state)
clean = make_fixture_repo()
spec = {'extra': True}
if not clean and spec.get('crash'):
    raise RuntimeError('isolated fixture crash')
count = spec.get('pristine_count', 11) if clean else 11
failures = spec.get('pristine_failures', 0) if clean else 1
case = 'record-fixture-committed-clean'
if not clean and spec.get('wrong'):
    case = 'unrelated-case'
if clean or not spec.get('absent'):
    print(json.dumps({'case': case, 'pass': clean}))
if not clean and spec.get('duplicate'):
    print(json.dumps({'case': case, 'pass': False}))
if not clean and spec.get('extra'):
    print(json.dumps({'case': 'unrelated-case', 'pass': False}))
    failures = 2
if clean or spec.get('summary', True):
    print(f'SELFTEST cases={count} failures={failures}')
sys.exit(0 if clean else 1)
