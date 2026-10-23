#!/usr/bin/env python3
"""One bounded text-only freeze-map mutation matrix; never loads an ELF reader."""
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

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/MutFreezeSchema')
OUT = Path(__file__).resolve().parent
EVIDENCE = OUT / 'evidence'
FIXTURE = OUT / 'text-fixture'
CLAIMS = Path('.ufo/waves/round-99/claims.json')
BASE = '54a87a51a865ab931fd355e767303337b05cccf4'
GATE = ROOT / 'tools/round-34/freeze-integrity.py'
EXPECTED_GATE_SHA = 'fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138'
PREDICATE = 'P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.'
PAYLOAD = b'MutFreezeSchema inert text pin\n'
DIGEST = hashlib.sha256(PAYLOAD).hexdigest()
PRISTINE = ('{"instruments":{"a/b":"' + DIGEST + '"},"frozen_inputs":{}}\n').encode()
ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
ENV.update({
    'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null',
    'GIT_TERMINAL_PROMPT': '0', 'GIT_OPTIONAL_LOCKS': '0',
    'GIT_AUTHOR_NAME': 'MutFreezeSchema', 'GIT_COMMITTER_NAME': 'MutFreezeSchema',
    'GIT_AUTHOR_EMAIL': 'mut-freeze-schema@example.invalid',
    'GIT_COMMITTER_EMAIL': 'mut-freeze-schema@example.invalid',
    'GIT_AUTHOR_DATE': '2026-10-23T12:00:00Z', 'GIT_COMMITTER_DATE': '2026-10-23T12:00:00Z',
    'LC_ALL': 'C', 'TZ': 'UTC',
})
COMMANDS = []
RESULTS = []
START = datetime.datetime.now(datetime.timezone.utc).isoformat()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NOFILE, (128, 128))
    hard = resource.getrlimit(resource.RLIMIT_NPROC)[1]
    cap = 4096 if hard == resource.RLIM_INFINITY else min(4096, hard)
    resource.setrlimit(resource.RLIMIT_NPROC, (cap, cap))


def run(argv, *, cwd=ROOT, input_bytes=None, allow_failure=False, binary=False):
    bounded = ['/usr/bin/timeout', '--signal=TERM', '--kill-after=1s', '12s'] + [str(x) for x in argv]
    record = {'argv': bounded, 'cwd': str(cwd), 'utc_start': now(), 'stdin_utf8': None if input_bytes is None else input_bytes.decode()}
    start = time.monotonic()
    proc = subprocess.Popen(bounded, cwd=cwd, env=ENV, stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True, preexec_fn=limits)
    timed_out = False
    try:
        out, err = proc.communicate(input=input_bytes, timeout=15)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
    finally:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
            cleanup = 'group SIGKILL sent after collection'
        except ProcessLookupError:
            cleanup = 'process group absent after collection'
    record.update({'utc_end': now(), 'duration_s': round(time.monotonic() - start, 6), 'exit': proc.returncode,
                   'stdout': out.decode('utf-8', errors='replace'), 'stderr': err.decode('utf-8', errors='replace'),
                   'stdout_sha256': sha(out), 'timed_out': timed_out, 'process_group_cleanup': cleanup})
    COMMANDS.append(record)
    if not allow_failure and (proc.returncode != 0 or timed_out):
        raise RuntimeError('command failed: ' + json.dumps(record))
    return (out if binary else out.decode()), record


def git(*args, cwd=FIXTURE, input_bytes=None):
    return run(['/usr/bin/git', '-c', 'core.hooksPath=/nonexistent-mut-freeze-hooks',
                '-c', 'commit.gpgsign=false', '-C', str(cwd), *args], cwd=cwd, input_bytes=input_bytes)[0].strip()


def snapshot(data):
    (FIXTURE / CLAIMS).write_bytes(data)
    git('add', '--', str(CLAIMS), 'a/b')
    tree = git('write-tree')
    commit = git('commit-tree', tree, input_bytes=b'MutFreezeSchema text-only fixture snapshot\n')
    git('update-ref', 'refs/heads/probe', commit)
    return commit, tree


def detect(name, phase, data):
    commit, tree = snapshot(data)
    actual = (FIXTURE / CLAIMS).read_bytes()
    if actual != data:
        raise RuntimeError('fixture byte mismatch')
    _, record = run(['/usr/bin/python3', '-I', '-B', str(GATE), '--root', str(FIXTURE),
                     '--round', '99', '--rev', 'HEAD'], cwd=FIXTURE, allow_failure=True)
    return {'name': name, 'phase': phase, 'claims_sha256': sha(actual), 'claims_size': len(actual),
            'measured_revision': commit, 'freeze_revision': commit, 'tree': tree, 'detector': record}


def clean(stage):
    rec = stage['detector']
    return rec['exit'] == 0 and 'freeze-integrity: CLEAN pins=1 ' in rec['stdout'] and not rec['stderr'] and not rec['timed_out']


def doc(instruments, frozen='{}'):
    return ('{"instruments":' + instruments + ',"frozen_inputs":' + frozen + '}\n').encode()


def pin(path, value=DIGEST):
    return json.dumps(path) + ':' + json.dumps(value)


VALID_MAP = '{' + pin('a/b') + '}'
CASES = [
    ('duplicate_pin_bad_then_good', doc('{' + pin('a/b', 'not-a-sha256') + ',' + pin('a/b') + '}'),
     'Reject ambiguous duplicate JSON pin members before last-writer loss; no frozen duplicate-member code is promised.'),
    ('duplicate_pin_good_then_bad', doc('{' + pin('a/b') + ',' + pin('a/b', 'not-a-sha256') + '}'),
     'Exit 3 pin_digest_format when the last retained value is malformed; rejection alone is not duplicate detection.'),
    ('duplicate_top_instruments_drops_absent_pin',
     ('{"instruments":{' + pin('absent.txt') + '},"instruments":' + VALID_MAP + ',"frozen_inputs":{}}\n').encode(),
     'Reject duplicate top-level instruments before an earlier absent pin can be discarded; no such frozen code is promised.'),
    ('duplicate_frozen_inputs_erases_conflict',
     ('{"instruments":' + VALID_MAP + ',"frozen_inputs":' + VALID_MAP + ',"frozen_inputs":{}}\n').encode(),
     'Reject duplicate frozen_inputs before the earlier exact cross-map conflict can be discarded; no such frozen code is promised.'),
    ('escaped_duplicate_pin_bad_then_good',
     ('{"instruments":{' + pin('a/b', 'not-a-sha256') + ',"a/\\u0062":' + json.dumps(DIGEST) + '},"frozen_inputs":{}}\n').encode(),
     'Reject JSON members equal after escape decoding; no frozen duplicate-member code is promised.'),
    ('cross_map_exact_duplicate', doc(VALID_MAP, VALID_MAP),
     'Exit 3 pin_path_duplicate for the exact same retained key in both maps.'),
    ('cross_map_internal_dot_alias', doc(VALID_MAP, '{' + pin('a/./b') + '}'),
     'Reject aliased duplicate at schema or pin stage; distinguish actual schema detection from Git lookup failure.'),
    ('cross_map_leading_dot_alias', doc(VALID_MAP, '{' + pin('./a/b') + '}'),
     'Reject aliased duplicate at schema or pin stage; canonical alias rejection is not explicitly frozen.'),
    ('cross_map_repeated_separator_alias', doc(VALID_MAP, '{' + pin('a//b') + '}'),
     'Reject aliased duplicate at schema or pin stage; canonical alias rejection is not explicitly frozen.'),
    ('standalone_malformed_digest', doc('{' + pin('a/b', 'not-a-sha256') + '}'),
     'Exit 3 pin_digest_format, no ok rows and no CLEAN.'),
    ('standalone_uppercase_digest', doc('{' + pin('a/b', DIGEST.upper()) + '}'),
     'Exit 3 pin_digest_format, enforcing lowercase rather than merely 64 hexadecimal characters.'),
    ('standalone_newline_suffixed_digest', doc('{' + pin('a/b', DIGEST + '\n') + '}'),
     'Exit 3 pin_digest_format, enforcing full-string length even for a final newline.'),
]


def main():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CPU, (90, 90))
    resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    FIXTURE.mkdir(parents=True, exist_ok=False)
    (FIXTURE / CLAIMS).parent.mkdir(parents=True)
    (FIXTURE / 'a').mkdir()
    (FIXTURE / 'a/b').write_bytes(PAYLOAD)
    gate_before = GATE.read_bytes()
    (EVIDENCE / 'freeze-integrity.py').write_bytes(gate_before)
    (EVIDENCE / 'pristine-claims.json').write_bytes(PRISTINE)
    (EVIDENCE / 'payload.txt').write_bytes(PAYLOAD)
    meta = {'utc_start': START, 'model_visible': 'openai-codex/gpt-6.1-sol', 'predicate_verbatim': PREDICATE,
            'axes': ['depth: strict freeze-map discrimination', 'lexical precision', 'containment and exact-byte restoration'],
            'source_root': str(ROOT), 'fixture_root': str(FIXTURE), 'base_requested': BASE,
            'gate_sha256_before': sha(gate_before), 'payload_sha256_before': sha(PAYLOAD),
            'pristine_claims_sha256': sha(PRISTINE), 'cases': len(CASES),
            'bounds': {'outer_wall_s': 150, 'command_wall_s': 12, 'kill_after_s': 1,
                       'child_as_mib': 256, 'child_cpu_s': 10, 'child_fsize_mib': 1, 'child_nofile': 128,
                       'child_nproc_max': 4096, 'one_child_tree_at_a_time': True},
            'git_environment_dropped': ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'],
            'tool_installs': [], 'production_reader_executed': False, 'rea_executed': False,
            'contract_note': 'Survival of duplicate-member or alias controls is a lexical coverage finding, not amendment of the frozen predicate.'}
    error = None
    restoration = None
    try:
        meta['source_measured_revision'] = git('rev-parse', 'HEAD', cwd=ROOT)
        frozen, _ = run(['/usr/bin/git', '-C', str(ROOT), 'show', BASE + ':tools/round-34/freeze-integrity.py'], binary=True)
        meta['gate_sha256_at_base'] = sha(frozen)
        if meta['source_measured_revision'] != BASE or sha(gate_before) != EXPECTED_GATE_SHA or frozen != gate_before:
            raise RuntimeError('unexpected source revision or gate bytes')
        meta['python_version'] = run(['/usr/bin/python3', '--version'])[0].strip()
        meta['git_version'] = run(['/usr/bin/git', '--version'])[0].strip()
        git('init', '-q', '-b', 'probe')
        for name, data, expected in CASES:
            (EVIDENCE / (name + '.claims.json')).write_bytes(data)
            result = {'name': name, 'expected_detector': expected, 'mutant_sha256': sha(data)}
            RESULTS.append(result)
            result['pristine'] = detect(name, 'pristine', PRISTINE)
            try:
                result['mutated'] = detect(name, 'mutated', data)
                git('update-ref', 'refs/heads/' + name, result['mutated']['measured_revision'])
            finally:
                (FIXTURE / CLAIMS).write_bytes(PRISTINE)
                result['restored'] = detect(name, 'restored', PRISTINE)
            if not clean(result['pristine']) or not clean(result['restored']) or result['mutated']['detector']['timed_out']:
                result['verdict'] = 'inconclusive'
            elif result['mutated']['detector']['exit'] == 0 and 'freeze-integrity: CLEAN' in result['mutated']['detector']['stdout']:
                result['verdict'] = 'survived'
            else:
                result['verdict'] = 'killed'
            result['exact_claims_restoration'] = result['pristine']['claims_sha256'] == result['restored']['claims_sha256'] == sha(PRISTINE)
            print(json.dumps({'case': name, 'verdict': result['verdict'], 'mutant_exit': result['mutated']['detector']['exit'],
                              'stdout': result['mutated']['detector']['stdout'], 'stderr': result['mutated']['detector']['stderr'],
                              'restoration_exact': result['exact_claims_restoration']}, sort_keys=True), flush=True)
    except BaseException as exc:
        error = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        (FIXTURE / CLAIMS).write_bytes(PRISTINE)
        try:
            restored_revision, restored_tree = snapshot(PRISTINE)
            restoration = {'claims_sha256_after': sha((FIXTURE / CLAIMS).read_bytes()),
                           'claims_exact': (FIXTURE / CLAIMS).read_bytes() == PRISTINE,
                           'payload_sha256_after': sha((FIXTURE / 'a/b').read_bytes()),
                           'payload_exact': (FIXTURE / 'a/b').read_bytes() == PAYLOAD,
                           'gate_sha256_after': sha(GATE.read_bytes()), 'gate_exact': GATE.read_bytes() == gate_before,
                           'fixture_head_restored_revision': restored_revision, 'fixture_tree': restored_tree}
            git('bundle', 'create', str(EVIDENCE / 'text-fixture.bundle'), '--branches')
        except BaseException as exc:
            restoration = {'claims_sha256_after': sha((FIXTURE / CLAIMS).read_bytes()), 'claims_exact': (FIXTURE / CLAIMS).read_bytes() == PRISTINE,
                           'error': {'type': type(exc).__name__, 'message': str(exc)}}
        meta.update({'utc_end': now(), 'error': error, 'restoration': restoration,
                     'verdict_counts': {v: sum(r.get('verdict') == v for r in RESULTS) for v in ('killed', 'survived', 'inconclusive')},
                     'command_count': len(COMMANDS)})
        receipt = {'metadata': meta, 'results': RESULTS, 'commands': COMMANDS}
        (EVIDENCE / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({'summary': meta}, sort_keys=True), flush=True)
    return 1 if error or not restoration.get('claims_exact') or not restoration.get('gate_exact') else 0


if __name__ == '__main__':
    sys.exit(main())
