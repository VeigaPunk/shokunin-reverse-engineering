#!/usr/bin/env python3
"""Read-only reproduction of ExecConj's frozen C1 population counterexample."""
import copy
import hashlib
import json
import subprocess

ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '2d63e1a7d04d4dcff45c3908bb51be787a2f22e1'
PATH = 'tools/round-82/conjunction-gate.py'

def get(path):
    return subprocess.check_output(['git', '--no-optional-locks', '-C', ROOT, 'show', f'{REV}:{path}'])

source = get(PATH)
assert hashlib.sha256(source).hexdigest() == '6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af'
namespace = {'__name__': 'frozen_execconj_probe', '__file__': PATH}
exec(compile(source, PATH, 'exec'), namespace)
landing = json.loads(get(namespace['LANDING']))
for summary in ([1, 0], [12, 0]):
    receipt = copy.deepcopy(landing)
    receipt['pristine']['summary'] = summary
    ok, defects = namespace['conjunction'](receipt)
    print(json.dumps({'revision': REV, 'summary': summary, 'case_count': len(receipt['pristine']['cases']), 'accepted': ok, 'defects': defects}))
receipt = copy.deepcopy(landing)
receipt['pristine']['cases'][0]['case'] = 'replacement-original-case'
ok, defects = namespace['conjunction'](receipt)
print(json.dumps({'revision': REV, 'mutation': 'replace first original name, retain population', 'accepted': ok, 'defects': defects}))
