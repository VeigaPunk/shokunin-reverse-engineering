#!/usr/bin/env python3
"""Describe the exact committed L1 Dart envelope/run pair; no producer replay.

Probe:0 report produced (inspect discrepancy fields),2 could-not-evaluate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

PREFIX = '.ufo/waves/round-23/evidence/c1/'

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
        r = subprocess.run(['git', '-C', str(a.root), *args], capture_output=True, check=False)
        if r.returncode:
            raise ValueError('git_input_unreadable')
        return r.stdout
    try:
        rev = git('rev-parse', '--verify', '--end-of-options', a.rev+'^{commit}').decode().strip()
        raw = git('show', rev+':'+PREFIX+'inspect-dart-legacy-saber.envelope.json')
        envelope = json.loads(raw)
        run = json.loads(git('show', rev+':'+PREFIX+'inspect-dart-legacy-saber.run.json'))
        fetch = json.loads(git('show', rev+':'+PREFIX+'legacy-saber-download.json'))
        data = envelope['data']
        n = data['normalized_result']
        print(json.dumps({'rev': rev, 'ok': envelope.get('ok'), 'exit': run['exit'],
                          'original_stderr': run['stderr'], 'overall_coverage': n['coverage'],
                          'envelope_sha256': hashlib.sha256(raw).hexdigest(),
                          'stdout_byte_equal': raw == run['stdout'].encode(),
                          'argv': run['argv'], 'env_overrides': run['env_overrides'],
                          'evidence_id': data['evidence_id'], 'operation': data['operation'],
                          'subject': data['subject'], 'abi': n['abi'], 'libapp': n['libapp'],
                          'string_pool_coverage': n['string_pool']['coverage'],
                          'package_uri_count_at_least': n['string_pool'].get('package_uri_count_at_least'),
                          'dart_uri_count_at_least': n['string_pool'].get('dart_uri_count_at_least'),
                          'limitations': data['limitations'],
                          'argv_target_matches_subject': run['argv'][4] == data['subject']['local_path'],
                          'subject_digest_matches_fetch': data['subject']['digest']['sha256'] == fetch['sha256'],
                          'command_matches': run['argv'][3] == envelope['meta']['command'] == 'inspect-dart-aot',
                          'limit': 'retained consistency, not source authenticity or SDK/source recovery'}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'finding': 'unevaluable', 'error': str(error)}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
