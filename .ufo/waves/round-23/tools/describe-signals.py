#!/usr/bin/env python3
"""Describe committed original signal envelopes and their producing records.

Probe, not admission gate. 0=report produced (inspect discrepancy fields),
2=could-not-evaluate. Does not replay tools or authenticate observations.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

PREFIX = '.ufo/waves/round-23/evidence/c1/'
NAMES = ('inventory', 'uart-help', 'decode-uart-hi', 'decode-official-uart', 'decode-invalid-decoder')

def main():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    a = p.parse_args()
    def git(*args):
        proc = subprocess.run(['git', '-C', str(a.root), *args], capture_output=True, check=False)
        if proc.returncode:
            raise ValueError('git_input_unreadable')
        return proc.stdout
    try:
        rev = git('rev-parse', '--verify', '--end-of-options', a.rev+'^{commit}').decode().strip()
        rows = []
        for name in NAMES:
            raw = git('show', rev+':'+PREFIX+name+'.envelope.json')
            envelope = json.loads(raw)
            run = json.loads(git('show', rev+':'+PREFIX+name+'.run.json'))
            data = envelope.get('data', {})
            normalized = data.get('normalized_result', {})
            annotations = normalized.get('annotations_text', '')
            meta_command = envelope.get('meta', {}).get('command')
            row = {'name': name, 'envelope_sha256': hashlib.sha256(raw).hexdigest(),
                   'stdout_byte_equal': run['stdout'].encode('utf-8') == raw,
                   'argv': run['argv'], 'env_overrides': run.get('env_overrides'),
                   'exit': run['exit'], 'ok': envelope.get('ok'),
                   'command': meta_command, 'operation': data.get('operation'),
                   'evidence_id': data.get('evidence_id'), 'subject': data.get('subject'),
                   'artifact': normalized.get('artifact'), 'selection': normalized.get('selection'),
                   'output_window': normalized.get('output_window'),
                   'decoder_count': len(normalized.get('decoders', [])),
                   'diagnostics': normalized.get('diagnostics'),
                   'error': envelope.get('error'),
                   'annotation_line_count': len(annotations.splitlines()),
                   'first_annotation_lines': annotations.splitlines()[:22],
                   'contains_literal_Hello_World': 'Hello World!' in annotations,
                   'synthetic_exact': annotations == '300-1100 uart-1: 48\n1300-2100 uart-1: 69\n' if name == 'decode-uart-hi' else None}
            if name.startswith('decode-') and data.get('subject'):
                carrier = PREFIX+('hello_world_8n1_9600.sr' if name=='decode-official-uart' else 'uart-hi.bin')
                blob = git('show', rev+':'+carrier)
                row['carrier_sha256'] = hashlib.sha256(blob).hexdigest()
                row['subject_digest_matches_carrier'] = data['subject']['digest']['sha256'] == row['carrier_sha256']
                row['argv_target_matches_subject'] = run['argv'][4] == data['subject']['local_path']
            if meta_command:
                row['argv_command_matches_meta'] = run['argv'][3] == meta_command
            rows.append(row)
        print(json.dumps({'rev': rev, 'producer': 'describe-signals.py', 'records': rows,
                          'limit': 'local retained consistency; no source authenticity, continuous custody or producer replay'}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'finding': 'unevaluable', 'error': str(error)}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
