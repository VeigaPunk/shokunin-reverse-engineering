#!/usr/bin/env python3
"""Prospective R25 instrument-custody CLI ruler; never imports candidate helpers.

Reads committed cases and candidate bytes from one full measured commit. Executes
only the selected candidate CLI, never any audited instrument or fixture. Missing
candidate is measured unavailable (0 exact cases, exit 2), never a clean result.
Output is stdout JSON with full subprocess records; caller retains those bytes.
0 all declared exit/finding pairs exact; 1 evaluated mismatch; 2 cannot evaluate.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

CANDIDATE = 'tools/round-25/instrument-custody.py'
ORACLE = 'corpus/evidence/round-25/oracle/cases.json'


def clean_environment():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1',
               GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_COUNT='2',
               GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
               GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null')
    env['GIT_OPTIONAL_LOCKS'] = '0'
    return env


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError('duplicate_json_member')
        obj[key] = value
    return obj


def git(root, env, *args):
    p = subprocess.run(['git', '-C', str(root), *args], env=env,
                       capture_output=True, check=False)
    if p.returncode:
        raise ValueError('git_read_failed:' + args[0])
    return p.stdout


def root_state(root, env):
    entries = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(name for name in dirs if name not in ('.git', '.jj'))
        for name in sorted(files + [name for name in dirs if (Path(directory) / name).is_symlink()]):
            path = Path(directory) / name
            if path.relative_to(root).as_posix() in ('.git', '.jj'):
                continue
            info = path.lstat()
            entries[path.relative_to(root).as_posix()] = [
                info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns]
    index = Path(git(root, env, 'rev-parse', '--git-path', 'index').decode().strip())
    if not index.is_absolute():
        index = root / index
    refs = subprocess.run(['git', '-C', str(root), 'show-ref', '--head'],
                          env=env, capture_output=True, check=False)
    if refs.returncode not in (0, 1):
        raise ValueError('git_refs_unavailable')
    state = {'worktree_lstat': entries,
             'index_sha256': hashlib.sha256(index.read_bytes()).hexdigest() if index.exists() else None,
             'refs_hex': refs.stdout.hex(),
             'status_hex': git(root, env, 'status', '--porcelain=v1', '-z', '--untracked-files=all').hex()}
    encoded = json.dumps(state, sort_keys=True).encode()
    return {'at_utc': datetime.now(timezone.utc).isoformat(),
            'sha256': hashlib.sha256(encoded).hexdigest(), 'state': state}


def text_output(value):
    return value.decode('utf-8', 'replace') if isinstance(value, bytes) else value or ''


def measure(args):
    if not all(re.fullmatch(r'[0-9a-f]{40}', rev) for rev in (args.rev, args.oracle_rev)):
        raise ValueError('full_commit_required')
    if not re.fullmatch(r'[0-9a-f]{64}', args.oracle_sha256):
        raise ValueError('oracle_digest_required')
    root = args.root.resolve(strict=True)
    work = args.work_parent.resolve(strict=True)
    if not work.is_dir() or str(work).startswith(('/tmp', '/dev/shm')):
        raise ValueError('owned_fast_work_parent_required')
    if work == root or root in work.parents:
        raise ValueError('work_parent_must_be_outside_measured_root')
    env = clean_environment()
    if git(root, env, 'rev-parse', '--show-toplevel').decode().strip() != str(root):
        raise ValueError('root_not_repository_top')
    rev = git(root, env, 'rev-parse', '--verify', args.rev + '^{commit}').decode().strip()
    oracle_raw = git(root, env, 'show', args.oracle_rev + ':' + ORACLE)
    digest = hashlib.sha256(oracle_raw).hexdigest()
    if digest != args.oracle_sha256:
        raise ValueError('snapshot_tampered:oracle')
    oracle = json.loads(oracle_raw, object_pairs_hook=unique_object)
    cases = oracle['cases']
    if not isinstance(cases, list) or not cases:
        raise ValueError('oracle_cases_invalid')
    ids = [c['id'] for c in cases]
    if len(set(ids)) != len(ids):
        raise ValueError('oracle_case_duplicate')
    result = {'schema': 'kaidoku-r25-ruler-v1', 'rev': rev,
              'executed': 0,
              'oracle_rev': args.oracle_rev, 'oracle_sha256': digest,
              'candidate_path': CANDIDATE, 'total': len(cases), 'exact': 0,
              'limit': 'Finite declared exit/primary-finding pairs; no historical admission, discovery completeness, authenticity or behavioral-equivalence certificate.'}
    present = subprocess.run(['git', '-C', str(root), 'cat-file', '-e', rev + ':' + CANDIDATE],
                             env=env, capture_output=True, check=False)
    if present.returncode:
        result.update(finding='candidate_unavailable', candidate_sha256=None,
                      cases=[{'id': case['id'], 'expected': case['expected'],
                              'observed': None, 'exact': False, 'status': 'not_observed'}
                             for case in cases])
        return result, 2
    candidate = git(root, env, 'show', rev + ':' + CANDIDATE)
    result['candidate_sha256'] = hashlib.sha256(candidate).hexdigest()
    records = []
    unsettled = None
    with tempfile.TemporaryDirectory(prefix='r25-ruler-', dir=work) as scratch:
        executable = Path(scratch) / 'instrument-custody.py'
        executable.write_bytes(candidate)
        baseline_state = root_state(root, env)
        result['root_baseline'] = baseline_state
        result['root_guard_limit'] = 'Named instants only: file lstat mode/size/mtime/ctime, index digest, refs and porcelain status. No continuity, all-content, object-store, enforcement or universal-filesystem proof; no automatic restoration.'
        for case in cases:
            request = case.get('raw_request')
            if request is None:
                request = json.dumps(case['request'], sort_keys=True)
            argv = [sys.executable, '-I', '-B', str(executable), '--root', str(root),
                    '--request-json', request]
            record = {'id': case['id'], 'expected': case['expected'], 'observed': None,
                      'exact': False, 'status': 'not_observed', 'argv': argv}
            records.append(record)
            try:
                before = root_state(root, env)
                record['root_before'] = {key: before[key] for key in ('at_utc', 'sha256')}
                if before['sha256'] != baseline_state['sha256']:
                    record['root_changed_state'] = before
                    unsettled = 'measured_root_changed_before'
                    break
                try:
                    proc = subprocess.run(argv, cwd=scratch, env=env, text=True,
                                          capture_output=True, check=False, timeout=60)
                    record.update(stdout=proc.stdout, stderr=proc.stderr, status='observed')
                    try:
                        observed = json.loads(proc.stdout, object_pairs_hook=unique_object)
                        finding = observed['finding']
                    except (ValueError, KeyError, TypeError):
                        finding = 'invalid_candidate_output'
                    actual = {'exit': proc.returncode, 'finding': finding}
                    record.update(observed=actual, exact=actual == case['expected'])
                except (subprocess.TimeoutExpired, OSError) as error:
                    record.update(status='unsettled', error_type=type(error).__name__,
                                  error=str(error), stdout=text_output(getattr(error, 'stdout', None)),
                                  stderr=text_output(getattr(error, 'stderr', None)))
                    unsettled = 'candidate_execution_unevaluable'
                finally:
                    after = root_state(root, env)
                    record['root_after'] = {key: after[key] for key in ('at_utc', 'sha256')}
                    if after['sha256'] != before['sha256']:
                        record['root_changed_state'] = after
                        unsettled = 'measured_root_changed_after'
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                record.update(status='unsettled', error_type=type(error).__name__, error=str(error))
                unsettled = 'root_state_unevaluable'
            if unsettled:
                break
    if unsettled:
        records.extend({'id': case['id'], 'expected': case['expected'], 'observed': None,
                        'exact': False, 'status': 'not_observed'}
                       for case in cases[len(records):])
    result['cases'] = records
    result['exact'] = sum(record['exact'] for record in records)
    result['executed'] = sum(record['status'] in ('observed', 'unsettled') and 'stdout' in record
                             for record in records)
    if unsettled:
        result['finding'] = unsettled
        return result, 2
    result['finding'] = 'all_declared_pairs_exact' if result['exact'] == len(cases) else 'declared_pairs_mismatch'
    return result, 0 if result['exact'] == len(cases) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--rev', required=True)
    parser.add_argument('--oracle-rev', required=True)
    parser.add_argument('--oracle-sha256', required=True)
    parser.add_argument('--work-parent', type=Path, required=True)
    args = parser.parse_args()
    try:
        result, code = measure(args)
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, subprocess.SubprocessError) as error:
        result, code = {'schema': 'kaidoku-r25-ruler-v1', 'finding': 'could_not_evaluate',
                        'error': str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
