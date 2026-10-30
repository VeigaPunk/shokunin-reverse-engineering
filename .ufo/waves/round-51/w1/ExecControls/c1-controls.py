#!/usr/bin/env python3
"""Offline R51-C1 controls over committed R50 receipts; no extraction or REA calls.

Run with --counter pointing to the integrated R51 v2 counter. The counter's
--controls interface scores receipts against a supplied rule and reports
carriers_matched. Every invocation is captured as an independent JSON receipt.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

IDS = ('c6430', 'c6490', 'g7581', 'g7582')
KINDS = ('symlink', 'char-device', 'block-device', 'fifo', 'socket', 'dir')
DETAILS_13 = ('247:0', *(f'136:{i}' for i in range(8)), '230:0', '3:0', '3:1', '3:2')


def load(path):
    return json.loads(Path(path).read_text())


def rule_fixtures(old_path):
    """Named, syntactically valid rule variants, leaving input rules unmodified."""
    old = load(old_path)
    variants = {'old': old}
    new = json.loads(json.dumps(old))
    new['claim'] = 'R51-C1'
    # Silent nonregular entries are producer-omitted, not extraction gaps.
    new['required']['char-device'] = False
    new['removed']['silent']['char-device'] = list(DETAILS_13)
    variants['new'] = new
    junk = json.loads(json.dumps(new))
    junk['allowed'] = {k: ['__impossible_control_allowance__'] for k in KINDS}
    junk['required'] = {k: True for k in KINDS}
    junk['removed']['silent'] = {}
    variants['junk'] = junk
    require = json.loads(json.dumps(new))
    require['required']['char-device'] = True
    variants['require-char-device'] = require
    only_247 = json.loads(json.dumps(new))
    only_247['removed']['silent']['char-device'] = ['247:0']
    variants['only-247-0'] = only_247
    for n in range(1, len(DETAILS_13)):
        subset = json.loads(json.dumps(new))
        subset['removed']['silent']['char-device'] = list(DETAILS_13[:n])
        variants[f'strict-subset-{n:02d}'] = subset
    return variants


def observed_count(proc):
    try:
        doc = json.loads(proc.stdout)
        return doc.get('carriers_matched')
    except (json.JSONDecodeError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True, help='lane checkout')
    ap.add_argument('--counter', required=True, help='integrated R51 counter path')
    ap.add_argument('--old-gap-rule', required=True)
    ap.add_argument('--receipts', required=True, help='committed R50 c1 receipts directory')
    ap.add_argument('--out', required=True, help='directory for generated rule fixtures and receipts')
    a = ap.parse_args()
    root = Path(a.root).resolve()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    rules_dir = out / 'rules'
    rules_dir.mkdir(exist_ok=True)
    rules = rule_fixtures(a.old_gap_rule)
    for name, doc in rules.items():
        (rules_dir / f'{name}.json').write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
    # Controls have fixed semantic expectations. Empty receipts are an intentional
    # absent-path probe; counter's exit 1 or 2 is acceptable and 0 is never acceptable.
    controls = [
        ('CTL-OLD', rules_dir / 'old.json', a.receipts, 2, 1),
        ('CTL-NEW', rules_dir / 'new.json', a.receipts, 4, 0),
        ('CTL-DN', rules_dir / 'new.json', str(out / 'absent-receipts'), None, (1, 2)),
        ('CTL-JUNK', rules_dir / 'junk.json', a.receipts, 0, 1),
        ('MUT-REQUIRE-CHAR-DEVICE', rules_dir / 'require-char-device.json', a.receipts, None, (1, 2)),
        ('MUT-ONLY-247-0', rules_dir / 'only-247-0.json', a.receipts, None, (1, 2)),
    ]
    for n in range(1, len(DETAILS_13)):
        controls.append((f'MUT-STRICT-SUBSET-{n:02d}', rules_dir / f'strict-subset-{n:02d}.json', a.receipts, None, (1, 2)))
    failed = False
    for name, rule, receipts, expected_count, expected_rc in controls:
        argv = [sys.executable, '-I', '-B', str(Path(a.counter).resolve()), '--root', str(root),
                '--controls', '--gap-rule', str(rule), '--receipts', str(receipts)]
        proc = subprocess.run(argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        count = observed_count(proc)
        rc_ok = proc.returncode in expected_rc if isinstance(expected_rc, tuple) else proc.returncode == expected_rc
        count_ok = expected_count is None or count == expected_count
        ok = rc_ok and count_ok
        failed |= not ok
        receipt = {'control': name, 'command': argv, 'exit_code': proc.returncode,
                   'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
                   'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                   'expected': {'carriers_matched': expected_count, 'exit_code': list(expected_rc) if isinstance(expected_rc, tuple) else expected_rc},
                   'observed': {'carriers_matched': count, 'exit_code': proc.returncode},
                   'verdict': 'expected' if ok else 'misbehaved'}
        (out / f'{name}.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
        print(json.dumps(receipt, sort_keys=True))
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
