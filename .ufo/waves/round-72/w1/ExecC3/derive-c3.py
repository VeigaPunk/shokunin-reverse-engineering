#!/usr/bin/env python3
"""Independent R72-C3 cutter and receipt-reader experiment; no audit imports."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

LANE = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = LANE / '.ufo/waves/round-72/w1/ExecC3'
S = Path('/fast/scratch/hyaku/kaidoku-r72/ExecC3')
OLDREV = 'b827a8b5d54f2885ec9be7786389f356c59226ce'
NEWREV = '6316c1053f927a1a1cdc3e0960b70acab5f56381'


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def run(name, args):
    proc = subprocess.run(args, cwd=LANE, capture_output=True, text=True, timeout=45)
    row = {'argv': [str(a) for a in args], 'cwd': str(LANE), 'rc': proc.returncode,
           'stdout': proc.stdout, 'stderr': proc.stderr}
    try:
        row['result'] = json.loads(proc.stdout)
    except json.JSONDecodeError:
        row['result'] = None
    save(OUT / (name + '.json'), row)
    return row


def encode(rows):
    return b''.join((json.dumps(row, sort_keys=True) + '\n').encode() for row in rows)


def main():
    S.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        shutil.copy2('/usr/bin/upx', S / 'upx-pinned-copy')
        source = LANE / '.ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl'
        audit_path = LANE / '.ufo/waves/round-71/l1/scores/c1-env-audit.json'
        data = source.read_bytes()
        rows = [json.loads(line) for line in data.splitlines() if line.strip()]
        summary = json.loads(audit_path.read_text())
        root = Path(summary['original_run_root'])
        allow = {'HOME', 'LANG', 'PATH', 'TMPDIR'}
        facts = []
        for n, row in enumerate(rows, 1):
            env = row['env']
            facts.append({'record': n, 'keys': sorted(env), 'exact_key_set': set(env) == allow,
                          'canary_present': 'KAIDOKU_ENV_CANARY' in env,
                          'home_under_run': Path(os.path.abspath(env['HOME'])).is_relative_to(root),
                          'tmpdir_under_run': Path(os.path.abspath(env['TMPDIR'])).is_relative_to(root),
                          'child': Path(row['argv'][0]).name})
        derived = {'records': len(rows), 'log_sha256': hashlib.sha256(data).hexdigest(),
                   'exact_key_sets': all(r['exact_key_set'] for r in facts),
                   'canary_absent': not any(r['canary_present'] for r in facts),
                   'home_under_run': all(r['home_under_run'] for r in facts),
                   'tmpdir_under_run': all(r['tmpdir_under_run'] for r in facts),
                   'children': dict(Counter(r['child'] for r in facts))}
        comparisons = {key: value == summary[key] for key, value in derived.items()}
        save(OUT / 'independent-derivation.json', {'derived': derived, 'summary': summary,
             'matches': comparisons, 'per_record': facts,
             'axes': ['raw-byte fidelity', 'clause discrimination', 'reader differential'],
             'imports_capsule_audit': False})
        shutil.copy2(source, OUT / 'genuine.jsonl')
        shutil.copy2(audit_path, OUT / 'genuine-summary.json')
        variants = {'digest': (data + b'\n', 'log_sha256'),
                    'record-count': (encode(rows[:-1]), 'records')}
        for name, key, value, clause in [
            ('extra-key', 'EXECC3_EXTRA', 'synthetic', 'keys'),
            ('canary-key', 'KAIDOKU_ENV_CANARY', 'synthetic', 'canary'),
            ('home-escape', 'HOME', str(root) + '-outside/home', 'home_under_run'),
            ('tmpdir-escape', 'TMPDIR', str(root) + '-outside/tmp', 'tmpdir_under_run')]:
            mutant = copy.deepcopy(rows)
            mutant[0]['env'][key] = value
            variants[name] = (encode(mutant), clause)
        mutant = copy.deepcopy(rows)
        mutant[0]['argv'][0] = '/usr/bin/exec-c3-other-child'
        variants['child-class'] = (encode(mutant), 'children')
        calls = [('genuine', source, None)]
        for name, (payload, clause) in variants.items():
            path = S / (name + '.jsonl')
            path.write_bytes(payload)
            shutil.copy2(path, OUT / path.name)
            calls.append((name, path, clause))

        def adjudicate(call):
            name, path, clause = call
            result = run('audit-' + name, [sys.executable, '-I', '-B',
                         str(LANE / 'tools/round-72/capsule-audit.py'),
                         '--capsule', str(path), '--audit', str(audit_path)])
            failures = (result['result'] or {}).get('failures', [])
            return {'shape': name, 'declared_clause': clause, 'rc': result['rc'],
                    'failures': failures, 'clause_named': clause in failures if clause else None,
                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

        with ThreadPoolExecutor(max_workers=8) as pool:
            battery = list(pool.map(adjudicate, calls))
        save(OUT / 'audit-results.json', battery)
        oldtool = S / 'round71-packed-elf.py'
        blob = subprocess.run(['git', 'show', OLDREV + ':tools/round-71/packed-elf.py'],
                              cwd=LANE, capture_output=True, check=True).stdout
        oldtool.write_bytes(blob)
        shutil.copy2(oldtool, OUT / oldtool.name)
        oldreceipt = json.loads((LANE / '.ufo/waves/round-71/w1/ExecC1/c1-route.json').read_text())
        oldreceipt['child_env_observed']['log'] = str(OUT / 'canary-key.jsonl')
        save(OUT / 'receipt-r71-lying.json', oldreceipt)
        oldargs = [sys.executable, '-I', '-B', str(oldtool), '--root', str(LANE), '--rev', OLDREV,
                   '--nonce-commitment', oldreceipt['nonce_commitment'], '--check-receipt',
                   str(OUT / 'receipt-r71-lying.json')]
        unsupported = run('reader-r71-explicit-capsule', oldargs + ['--capsule', str(OUT / 'canary-key.jsonl')])
        oldresult = run('reader-r71-supported-interface', oldargs)
        newreceipt = json.loads((LANE / '.ufo/waves/round-72/l1/pre/route-at-declaration.json').read_text())
        newsource = LANE / '.ufo/waves/round-72/l1/pre/env-at-declaration.jsonl'
        newrows = [json.loads(line) for line in newsource.read_bytes().splitlines() if line.strip()]
        newrows[0]['env']['KAIDOKU_ENV_CANARY'] = 'synthetic'
        polluted = S / 'r72-polluted.jsonl'
        polluted.write_bytes(encode(newrows))
        shutil.copy2(polluted, OUT / polluted.name)
        newreceipt['child_env_observed']['log'] = str(OUT / polluted.name)
        save(OUT / 'receipt-r72-lying.json', newreceipt)
        newargs = [sys.executable, '-I', '-B', str(LANE / 'tools/round-72/packed-elf.py'),
                   '--root', str(LANE), '--rev', NEWREV, '--work', str(S),
                   '--nonce-commitment', newreceipt['nonce_commitment'], '--check-receipt',
                   str(OUT / 'receipt-r72-lying.json'), '--capsule', str(polluted)]
        newresult = run('reader-r72-explicit-capsule', newargs)
        result = {'summary_matches': all(comparisons.values()), 'genuine_accepted': battery[0]['rc'] == 0,
                  'seven_rejected_named': all(r['rc'] == 1 and r['clause_named'] for r in battery[1:]),
                  'r71_accepts_lie': oldresult['rc'] == 0,
                  'r71_explicit_capsule_rc': unsupported['rc'],
                  'r72_rejects_lie': newresult['rc'] == 1,
                  'r72_receipt_capsule_named': 'receipt_capsule' in newresult['stdout'],
                  'old_checker_sha256': hashlib.sha256(blob).hexdigest(),
                  'upx_sha256': hashlib.sha256((S / 'upx-pinned-copy').read_bytes()).hexdigest(),
                  'scratch_removed_on_exit': True}
        save(OUT / 'results.json', result)
        print(json.dumps(result, indent=2))
    finally:
        shutil.rmtree(S)


if __name__ == '__main__':
    main()
