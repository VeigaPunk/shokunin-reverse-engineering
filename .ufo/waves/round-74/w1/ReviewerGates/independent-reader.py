#!/usr/bin/env python3
"""Read-only round-74 review; emits exact command/outputs, never imports lane tools."""
import argparse
import collections
import concurrent.futures
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
FREEZE = '021914c0e638454e507087accfe41af1ab69f185'
DECLARATION = 'b3a7e28089582ce5fb002a1b88e5295caf696b9f'
WAVE = ROOT / '.ufo/waves/round-74'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def pins():
    claims = json.loads(git('show', FREEZE + ':.ufo/waves/round-74/claims.json'))
    rows = []
    for group in ('instruments', 'loaded_by_counter', 'producers_not_counters'):
        for path, expected in claims.get(group, {}).items():
            data = git('show', FREEZE + ':' + path)
            actual = hashlib.sha256(data).hexdigest()
            rows.append({'group': group, 'path': path, 'expected': expected,
                         'actual': actual, 'matched': expected == actual})
    declared = []
    for path, expected in claims['instruments'].items():
        actual = hashlib.sha256(git('show', DECLARATION + ':' + path)).hexdigest()
        declared.append({'path': path, 'expected': expected, 'actual': actual,
                         'matched': expected == actual})
    return {'rows': rows, 'pin_count': len(rows),
            'mismatches': [r for r in rows if not r['matched']],
            'declaration_rows': declared,
            'declaration_mismatches': [r for r in declared if not r['matched']]}

def contract():
    spec = json.loads((WAVE / 'r74-w1-spec.json').read_text())
    dispatch = json.loads((WAVE / 'r74-w1-dispatch.json').read_text())
    registry = json.loads((WAVE / 'w1/swarm-registry.json').read_text())
    rows = []
    tasks = {t['name']: t for t in dispatch['taskCall']['tasks']}
    for item in spec['items']:
        name = item['name']
        task = tasks.get(name, {})
        expected = '.ufo/waves/round-74/w1/' + name + '.md'
        trailers = re.findall(r'^Report: write your scoped findings to (.+)$', task.get('task', ''), re.M)
        rendered = (ROOT / trailers[0]).resolve() if len(trailers) == 1 else None
        rows.append({'name': name, 'role': item['role'], 'task_role': task.get('agent'),
                     'registry_role': registry['members'].get(name, {}).get('role'),
                     'expected_report': expected, 'actual_trailers': trailers,
                     'trailer_matched': trailers == [expected],
                     'path_contained': rendered is not None and rendered.is_relative_to(ROOT),
                     'report_present_at_snapshot': (ROOT / expected).is_file(),
                     'prompt_prefix_matches': task.get('task', '').startswith(item['prompt']),
                     'agentId': registry['members'].get(name, {}).get('agentId')})
    roles = dict(collections.Counter(i['role'] for i in spec['items']))
    return {'wave': spec['wave'], 'rows': rows, 'roles': roles,
            'spec_names': sorted(i['name'] for i in spec['items']),
            'dispatch_names': sorted(tasks), 'registry_names': sorted(registry['members']),
            'registry_matches_dispatch': registry['members'] == dispatch['registry']['members'],
            'report_dirs': [spec['reportDir'], dispatch['registry']['reportDir'], registry['reportDir']],
            'counts': dispatch['counts'], 'resumeSends': dispatch['resumeSends'],
            'saturation_claim': False, 'policy': dispatch['policy'],
            'tracked_changes_since_freeze': git('diff', '--name-only', FREEZE).decode().splitlines(),
            'observability': 'Contracts and lane diff do not establish process-wide writes, actual runtime launches, or same-identity execution; null agentId is not launch proof.'}

def ledger():
    path = ROOT / 'corpus/claim-freezes-v2.tsv'
    rows = [line for line in path.read_text().splitlines() if line.startswith(('round-73\t', 'round-74\t'))]
    frozen = git('show', FREEZE + ':corpus/claim-freezes-v2.tsv').decode()
    frozen_rows = [line for line in frozen.splitlines() if line.startswith(('round-73\t', 'round-74\t'))]
    return {'current_rows': rows, 'freeze_rows': frozen_rows,
            'r74_required_at_freeze': False, 'r74_required_at_record': True,
            'basis': 'freeze-gate.py:177-188 compares disclosures to every freeze at measured record revision when --disclosures is supplied; a freeze without disclosures does not require its own row.'}

def gate():
    command = ['python3', '-I', '-B', 'tools/round-29/freeze-gate.py', '--root', '.', '--rev', FREEZE, '--require-clean', 'round-74']
    p = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    parsed = json.loads(p.stdout)
    row = next(r for r in parsed['freezes'] if r['claims_file'] == '.ufo/waves/round-74/claims.json')
    claims = json.loads(git('show', FREEZE + ':.ufo/waves/round-74/claims.json'))
    named = sorted({c['instrument'] for c in claims['claims']})
    return {'command': command, 'rc': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
            'round74': row, 'claim_named': named,
            'reported_equals_claim_named': row['instruments'] == named,
            'reported_subset_declared': set(row['instruments']) <= set(claims['instruments'])}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('check', choices=['pins', 'contract', 'ledger', 'gate', 'all'])
    args = parser.parse_args()
    checks = {'pins': pins, 'contract': contract, 'ledger': ledger, 'gate': gate}
    if args.check == 'all':
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = {name: pool.submit(fn) for name, fn in checks.items()}
            result = {name: future.result() for name, future in futures.items()}
    else:
        result = checks[args.check]()
    print(json.dumps(result, indent=2, sort_keys=True))
