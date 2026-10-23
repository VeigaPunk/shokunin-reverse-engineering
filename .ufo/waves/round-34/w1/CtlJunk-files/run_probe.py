#!/usr/bin/env python3
"""Record one explicitly assigned control-reader probe, never the production reader."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/CtlJunk')
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
OUT = ROOT / '.ufo/waves/round-34/w1/CtlJunk-files'
COUNTER = ROOT / 'tools/round-34/version-needs-counter.py'
READER = OUT / 'control_reader.py'
PIN = 'd7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    phase = sys.argv[1]
    if phase not in {'pristine', 'mutated', 'restored'}:
        raise ValueError('unknown phase')
    prefix = OUT / phase
    if prefix.with_suffix('.receipt.json').exists():
        raise ValueError('refusing to overwrite an exercised receipt')
    counter_bytes = COUNTER.read_bytes()
    if sha(counter_bytes) != PIN:
        raise ValueError('frozen counter digest differs')
    before = READER.read_bytes()
    prefix.with_suffix('.reader.py').write_bytes(before)
    frozen_inputs = {
        'version-needs-counter.py': counter_bytes,
        'claims.json': (ROOT / '.ufo/waves/round-34/claims.json').read_bytes(),
        'expected.json': (ROOT / '.ufo/waves/round-34/expected.json').read_bytes(),
    }
    inputs = OUT / 'inputs'
    inputs.mkdir(exist_ok=True)
    for name, data in frozen_inputs.items():
        archive = inputs / name
        if archive.exists() and archive.read_bytes() != data:
            raise ValueError('input bytes changed: ' + name)
        if not archive.exists():
            archive.write_bytes(data)
    limits = {
        'RLIMIT_AS': 536870912,
        'RLIMIT_CPU': 90,
        'RLIMIT_NPROC': 4096,
        'RLIMIT_NOFILE': 128,
        'RLIMIT_FSIZE': 16777216,
        'RLIMIT_CORE': 0,
    }
    for name, value in limits.items():
        key = getattr(resource, name)
        hard = resource.getrlimit(key)[1]
        cap = value if hard == resource.RLIM_INFINITY else min(value, hard)
        resource.setrlimit(key, (cap, cap))
        limits[name] = cap
    environment = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
    environment.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'LC_ALL': 'C'})
    counter_argv = [sys.executable, '-I', '-B', str(COUNTER), '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE, '--control-reader', str(READER)]
    detector_argv = ['/usr/bin/timeout', '--signal=TERM', '--kill-after=5s', '150s', *counter_argv]
    launch_argv = ['env', '-u', 'GIT_DIR', '-u', 'GIT_WORK_TREE', '-u', 'GIT_INDEX_FILE', 'timeout', '--signal=TERM', '--kill-after=5s', '180s', 'python3', '-I', '-B', str(Path(__file__).resolve()), phase]
    started = utc()
    clock = time.monotonic()
    process = subprocess.Popen(detector_argv, cwd=ROOT, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=160)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate()
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
            remaining_group_killed = True
        except ProcessLookupError:
            remaining_group_killed = False
    ended = utc()
    prefix.with_suffix('.stdout.json').write_bytes(stdout)
    prefix.with_suffix('.stderr.txt').write_bytes(stderr)
    try:
        result = json.loads(stdout)
        summary = {k: result.get(k) for k in ('predicate', 'mode', 'finding', 'matched', 'target', 'met_target', 'documents_ok', 'measured_revision', 'freeze_revision', 'reader_sha256')}
        summary['attempts'] = sum(len(row['attempts']) for row in result.get('rows', []))
        summary['matched_attempts'] = sum(attempt['matched'] for row in result.get('rows', []) for attempt in row['attempts'])
        summary['matched_carriers'] = [row['id'] for row in result.get('rows', []) if row['matched']]
    except (ValueError, TypeError, KeyError) as error:
        summary = {'parse_error': str(error)}
    receipt = {
        'phase': phase,
        'launch_argv': launch_argv,
        'python_orig_argv': sys.orig_argv,
        'detector_argv': detector_argv,
        'counter_argv': counter_argv,
        'cwd': str(ROOT),
        'started_utc': started,
        'ended_utc': ended,
        'elapsed_seconds': time.monotonic() - clock,
        'exit': process.returncode,
        'driver_timeout': timed_out,
        'remaining_process_group_killed': remaining_group_killed,
        'resource_limits': limits,
        'git_environment': {k: v for k, v in environment.items() if k.startswith('GIT_')},
        'reader_sha256_before': sha(before),
        'reader_sha256_after': sha(READER.read_bytes()),
        'counter_sha256_before': sha(counter_bytes),
        'counter_sha256_after': sha(COUNTER.read_bytes()),
        'frozen_input_sha256': {name: sha(data) for name, data in frozen_inputs.items()},
        'stdout_sha256': sha(stdout),
        'stderr_sha256': sha(stderr),
        'stdout_bytes': len(stdout),
        'stderr_bytes': len(stderr),
        'summary': summary,
        'python_version': sys.version,
    }
    prefix.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
