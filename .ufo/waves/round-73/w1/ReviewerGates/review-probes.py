#!/usr/bin/env python3
"""Focused reviewer counterexamples; no real environment values are captured."""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
sys.dont_write_bytecode = True
ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
WORK = Path(os.environ['TMPDIR'])
OUT = ROOT / '.ufo/waves/round-73/w1/ReviewerGates'
def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), ROOT / 'tools/round-73' / (name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
a = load('record-audit')
p = load('seam-probe')
m = load('mutation-check')
results = {}
blob = b'fixture target bytes'
sha = hashlib.sha256(blob).hexdigest()
wrong = '01234567'
card = (a.ROUND72_HEADING + '\ntarget sha `' + wrong + '`\n' + a.CORRECTION_MARK + '):** old token ' + wrong + ' remains correct.\nl1/pre/shared.json\n' + a.ROUND73_HEADING + '\nlowest-axis: coverage\nl1/pre/shared.json\n')
texts = {a.SCORECARD: card, a.FREEZES: 'round-72\nround-73\n', a.KNOWLEDGE_R72: 'source: only one field\n', a.KNOWLEDGE_R73: 'source: x\nsource: x\nsource: x\n'}
receipts = {a.RECEIPT_C2_BASE: {'target_sha256': sha, 'rev': 'fixture'}, a.R73_C2: {'target_pin': {'expect': sha, 'matched': True}, 'target_sha256': sha}, a.R73_GATE: {'disclosures': {'missing': [], 'stray': []}}, a.R73_C3_LYING: {'rc': 1, 'met': False}, '.ufo/waves/round-72/l1/pre/shared.json': {'rev': 'fixture'}}
def fake_show(root, rev, path):
    return texts.get(path)
def fake_json(root, rev, path):
    return receipts.get(path)
with patch.object(a, 'show', fake_show), patch.object(a, 'show_json', fake_json), patch.object(a.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, blob, b'')):
    result = a.audit(str(ROOT), 'fixture')
    results['audit_missing_population_missing_r73_before_bad_D1_and_bad_D5'] = result
    results['missing_required_inputs'] = [a.SPOTCHECK, '.ufo/waves/round-73/l1/pre/shared.json', a.GATE_BASE, a.RECEIPT_C3_LYING_BASE]
    results['correct_D1_digest_absent_from_correction'] = sha not in card
# Validators accept a census reduced to one arbitrary all-green row.
record = WORK / 'partial-record.json'
record.write_text(json.dumps({'atoms': [{'id': 'invented', 'ok': True, 'detail': 'fixture'}], 'mismatches': [], 'mismatch_count': 0, 'ok': True}))
mutation = WORK / 'partial-mutation.json'
mutation.write_text(json.dumps({'patch_set': 'r73', 'pristine_ok': True, 'target_sha256': sha, 'work_dir': str(WORK), 'mutants': [{'id': 'invented', 'rc': 1, 'failed': [], 'applied': True, 'verdict': 'killed'}], 'survivors': [], 'survivor_count': 99, 'ok': True}))
for label, mod, receipt in [('record_validator_partial', a, record), ('mutation_validator_partial_wrong_count', m, mutation)]:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.validate(str(receipt))
    results[label] = {'rc': rc, 'output': json.loads(buf.getvalue())}
clean = {'keys': list(p.CHILD_ENV_KEYS), 'canary_present': False}
dirty = {'keys': list(p.CHILD_ENV_KEYS) + ['KAIDOKU_ENV_CANARY'], 'canary_present': True}
genuine = {'rc': 0, 'kernel': {'git': clean, 'readelf': clean}}
forged = {'kernel': {'git': dirty, 'readelf': dirty}, 'shims': {'git': clean, 'readelf': clean}}
results['a12'] = {'positive': p.a12_verdict(genuine, forged, p.CHILD_ENV_KEYS), 'no_genuine_samples': p.a12_verdict({'rc': 0, 'kernel': {}}, forged, p.CHILD_ENV_KEYS), 'no_forged_samples': p.a12_verdict(genuine, {'kernel': {}, 'shims': forged['shims']}, p.CHILD_ENV_KEYS), 'one_forged_child_only': p.a12_verdict(genuine, {'kernel': {'git': dirty}, 'shims': {'git': clean}}, p.CHILD_ENV_KEYS)}
# The control's exact wrong target route is refused before reading or selftesting it.
no_case = WORK / 'route-no-case.py'
no_case.write_text('raise RuntimeError("SELFTEST_WAS_REACHED")\n')
proc = subprocess.run([sys.executable, '-I', '-B', str(ROOT / 'tools/round-73/mutation-check.py'), '--root', str(ROOT), '--rev', 'da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b', '--tool', str(no_case), '--patch-set', 'r73', '--work', str(WORK)], capture_output=True, text=True)
results['c3_no_case_never_selftests'] = {'rc': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr, 'control_met_predicate': proc.returncode == 2 and isinstance(json.loads(proc.stderr).get('unevaluable'), str)}
results['source_sha256'] = {name: hashlib.sha256((ROOT / 'tools/round-73' / (name + '.py')).read_bytes()).hexdigest() for name in ['record-audit', 'seam-probe', 'mutation-check', 'controls']}
results['scope'] = 'Synthetic function counterexamples plus one real battery CLI refusal. No live kernel probe, environment dump, git writes, or full controls run.'
(OUT / 'counterexamples.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps({'audit_mismatch_count': results['audit_missing_population_missing_r73_before_bad_D1_and_bad_D5']['mismatch_count'], 'record_validator_rc': results['record_validator_partial']['rc'], 'mutation_validator_rc': results['mutation_validator_partial_wrong_count']['rc'], 'c3_no_case_rc': proc.returncode, 'c3_no_case_control_met': results['c3_no_case_never_selftests']['control_met_predicate'], 'a12_empty_genuine_ok': results['a12']['no_genuine_samples']['ok'], 'a12_empty_forged_ok': results['a12']['no_forged_samples']['ok']}))
