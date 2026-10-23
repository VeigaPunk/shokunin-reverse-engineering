#!/usr/bin/env python3
"""Private text-only outer-CLI counter mutation probe; never imports a reader."""
import argparse
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys

ROOT = Path('/fast/scratch/hyaku/kaidoku-r34/w1/MutCounterPins')
BASE = ROOT / '.ufo/waves/round-34/w1/MutCounterPins-files'
FREEZE = '54a87a51a865ab931fd355e767303337b05cccf4'
COUNTER = ROOT / 'tools/round-34/version-needs-counter.py'
PREDICATE = 'P34-version-needs: twelve public ELF carriers yield exactly their independently frozen GNU version-needs records on opaque paths, including randomized same-length string-table naming wherever requirements are present, and the pinned source-backed decision table is present.'
MAX_WRITE = 2 * 1024 * 1024
READER = b'''import json, sys
from pathlib import Path
raw = Path(sys.argv[1]).read_bytes()
if not raw.startswith(b"TEXT\\n"):
    raise SystemExit(3)
print(json.dumps(json.loads(raw[5:]), sort_keys=True))
'''
NAMED = {'schema': 1, 'needed': [
    {'file': 'libA', 'versions': [
        {'name': 'VER_1', 'flags': 0, 'other': 2, 'hash': 1},
        {'name': 'VER_2', 'flags': 0, 'other': 2, 'hash': 2},
    ]},
    {'file': 'libB', 'versions': []},
]}
EMPTY = {'schema': 1, 'needed': []}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()


def bounded_write(path, data):
    if len(data) > MAX_WRITE:
        raise RuntimeError('fixture_write_limit')
    if not path.is_relative_to(BASE):
        raise RuntimeError('fixture_write_scope')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def clean_env():
    result = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
    result.update({'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull})
    return result


def limits():
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_NPROC, (4096, 4096))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_WRITE, MAX_WRITE))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def command(argv, timeout):
    started = utc()
    proc = subprocess.Popen(argv, cwd=ROOT, env=clean_env(), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True, preexec_fn=limits)
    timed_out = False
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, stderr = proc.communicate()
    finally:
        # The assigned fake reader never spawns; remove any remaining members of our own tree.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    return {'argv': argv, 'cwd': str(ROOT), 'started_utc': started, 'finished_utc': utc(),
            'exit': proc.returncode, 'timeout': timed_out,
            'stdout': stdout.decode('utf-8', errors='replace'),
            'stderr': stderr.decode('utf-8', errors='replace'),
            'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
            'stdout_bytes': len(stdout), 'stderr_bytes': len(stderr)}


def baseline_files():
    data_a = b'TEXT\n' + encoded(NAMED)
    data_b = b'TEXT\n' + encoded(EMPTY)
    rows = [
        {'id': 'text-a', 'path': 'carrier-a.txt', 'size': len(data_a), 'sha256': sha(data_a), 'expected': NAMED},
        {'id': 'text-b', 'path': 'carrier-b.txt', 'size': len(data_b), 'sha256': sha(data_b), 'expected': EMPTY},
    ]
    spec = {'target': 2, 'documents_ok': True, 'manifest': {'schema': 1, 'carriers': rows}}
    return spec, {'spec.json': encoded(spec), 'reader.py': READER, 'carrier-a.txt': data_a, 'carrier-b.txt': data_b}


def make_cases(spec, files):
    cases = []
    row = ('manifest', 'carriers', 0)
    expected = row + ('expected',)
    record = expected + ('needed', 0)
    version = record + ('versions', 0)

    def change(name, path, value, finding, rule):
        cases.append({'name': name, 'action': 'set', 'path': list(path), 'value': value,
                      'expected_exit': 2, 'expected_finding': finding, 'source_rule': rule})

    change('wrong-declared-digest', row + ('sha256',), '0' * 64, 'carrier_pin:text-a', 'score:114-116')
    change('wrong-declared-size', row + ('size',), len(files['carrier-a.txt']) + 1, 'carrier_pin:text-a', 'score:114-116')
    for name, replacement in (
        ('same-size-carrier-byte', files['carrier-a.txt'].replace(b'TEXT', b'TEXU', 1)),
        ('shortened-carrier-byte', files['carrier-a.txt'][:-1]),
    ):
        cases.append({'name': name, 'action': 'file', 'file': 'carrier-a.txt', 'value': replacement.decode(),
                      'expected_exit': 2, 'expected_finding': 'carrier_pin:text-a', 'source_rule': 'score:114-116'})
    for name, value in [('zero-size', 0), ('oversized-size', 16777217), ('boolean-size', True), ('float-size', 1.0)]:
        change(name, row + ('size',), value, 'manifest_row_schema', 'validate_manifest:153-154')
    change('duplicate-id', ('manifest', 'carriers', 1, 'id'), 'text-a', 'manifest_duplicate', 'validate_manifest:149-150')
    change('duplicate-digest', ('manifest', 'carriers', 1, 'sha256'), spec['manifest']['carriers'][0]['sha256'], 'manifest_duplicate', 'validate_manifest:149-150')
    for name, value in [
        ('empty-path', ''), ('absolute-path', '/not-opened/MutCounterPins.txt'),
        ('parent-path', '../not-opened.txt'), ('embedded-parent-path', 'sub/../carrier-a.txt'),
        ('colon-path', 'head:carrier-a.txt'), ('nul-path', 'carrier-a.txt\x00suffix'),
    ]:
        change(name, row + ('path',), value, 'unsafe_path', 'safe_path:57-61; validate_manifest:148')
    for name, path, value, rule in [
        ('expected-not-object', expected, [], 'canonical:35-36'),
        ('expected-extra-field', expected + ('extra',), 1, 'canonical:35-36'),
        ('expected-boolean-schema', expected + ('schema',), True, 'canonical:35-36'),
        ('expected-string-schema', expected + ('schema',), '1', 'canonical:35-36'),
        ('expected-unknown-schema', expected + ('schema',), 2, 'canonical:35-36'),
        ('needed-not-list', expected + ('needed',), {}, 'canonical:37-38'),
        ('needed-record-not-object', expected + ('needed', 0), [], 'canonical:41-42'),
        ('needed-record-extra-field', record + ('extra',), 1, 'canonical:41-42'),
        ('needed-file-empty', record + ('file',), '', 'canonical:41-42'),
        ('needed-file-not-string', record + ('file',), 7, 'canonical:41-42'),
        ('versions-not-list', record + ('versions',), {}, 'canonical:41-42'),
        ('version-not-object', record + ('versions', 0), [], 'canonical:46-47'),
        ('version-extra-field', version + ('extra',), 1, 'canonical:46-47'),
        ('version-name-empty', version + ('name',), '', 'canonical:46-47'),
        ('version-name-not-string', version + ('name',), False, 'canonical:46-47'),
        ('versions-unsorted', record + ('versions',), list(reversed(NAMED['needed'][0]['versions'])), 'canonical:52-54'),
        ('versions-duplicate-name-other', record + ('versions', 1, 'name'), 'VER_1', 'canonical:52-54'),
        ('needed-files-unsorted', expected + ('needed',), list(reversed(NAMED['needed'])), 'canonical:55'),
        ('needed-files-duplicate', expected + ('needed', 1, 'file'), 'libA', 'canonical:55'),
    ]:
        change(name, path, value, 'manifest_row_schema', rule + '; validate_manifest:153-154')
    for field, maximum in [('flags', 65535), ('other', 65535), ('hash', 4294967295)]:
        for suffix, value, rule in [('boolean', True, 'canonical:48-49'), ('negative', -1, 'canonical:48-49'), ('overflow', maximum + 1, 'canonical:50-51')]:
            change(field + '-' + suffix, version + (field,), value, 'manifest_row_schema', rule + '; validate_manifest:153-154')
    for name, path, rule in [
        ('expected-missing-schema', expected + ('schema',), 'canonical:35-36'),
        ('expected-missing-needed', expected + ('needed',), 'canonical:35-36'),
        ('needed-missing-file', record + ('file',), 'canonical:41-42'),
        ('version-missing-hash', version + ('hash',), 'canonical:46-47'),
    ]:
        cases.append({'name': name, 'action': 'delete', 'path': list(path), 'expected_exit': 2,
                      'expected_finding': 'manifest_row_schema', 'source_rule': rule + '; validate_manifest:153-154'})
    return cases


def mutate(spec, files, case):
    changed = dict(files)
    if case['action'] == 'file':
        changed[case['file']] = case['value'].encode()
    else:
        value = copy.deepcopy(spec)
        node = value
        for key in case['path'][:-1]:
            node = node[key]
        if case['action'] == 'delete':
            del node[case['path'][-1]]
        else:
            node[case['path'][-1]] = case['value']
        changed['spec.json'] = encoded(value)
    if sum(changed[name] != files[name] for name in files) != 1:
        raise RuntimeError('not_one_fixture_file_mutated')
    return changed


def hash_files(files):
    return {name: sha((BASE / name).read_bytes()) for name in files}


def run_detector():
    argv = ['/usr/bin/timeout', '--signal=TERM', '--kill-after=1s', '15s', '/usr/bin/python3', '-I', '-B',
            str(COUNTER), '--root', str(ROOT), '--rev', FREEZE, '--freeze', FREEZE,
            '--fixture-spec', str(BASE / 'spec.json'), '--fixture-reader', str(BASE / 'reader.py')]
    result = command(argv, 18)
    try:
        result['decoded'] = json.loads(result['stdout'])
    except (ValueError, TypeError):
        result['decoded'] = None
    return result


def matches(result, code, finding, met):
    value = result['decoded']
    return (not result['timeout'] and result['exit'] == code and isinstance(value, dict)
            and value.get('finding') == finding and value.get('met_target') is met)


def probe_case(spec, originals, case):
    for name, data in originals.items():
        if (BASE / name).read_bytes() != data:
            raise RuntimeError('nonpristine_fixture:' + name)
    receipt = {'case': case, 'pristine_hashes': hash_files(originals), 'pristine': run_detector()}
    changed = mutate(spec, originals, case)
    changed_name = next(name for name in originals if originals[name] != changed[name])
    receipt['mutated_file'] = changed_name
    receipt['exact_mutated_utf8'] = changed[changed_name].decode()
    try:
        bounded_write(BASE / changed_name, changed[changed_name])
        receipt['mutated_hashes'] = hash_files(originals)
        receipt['mutated'] = run_detector()
    finally:
        bounded_write(BASE / changed_name, originals[changed_name])
        receipt['restored_hashes'] = hash_files(originals)
        receipt['exact_restoration'] = all((BASE / name).read_bytes() == data for name, data in originals.items())
        receipt['restored'] = run_detector()
    green = matches(receipt['pristine'], 0, 'version_needs_match', True) and matches(receipt['restored'], 0, 'version_needs_match', True)
    red = matches(receipt['mutated'], case['expected_exit'], case['expected_finding'], False)
    if not green or not receipt['exact_restoration']:
        verdict = 'inconclusive'
    elif red:
        verdict = 'killed'
    elif receipt['mutated']['decoded'] and receipt['mutated']['decoded'].get('met_target') is True:
        verdict = 'survived'
    else:
        verdict = 'inconclusive'
    receipt['verdict'] = verdict
    receipt['expected_detector_matched'] = red
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, required=True)
    args = parser.parse_args()
    if args.batch not in range(4):
        raise SystemExit('batch must be 0..3')
    spec, originals = baseline_files()
    cases = make_cases(spec, originals)
    plan = {'predicate_verbatim': PREDICATE, 'production_score': False, 'freeze': FREEZE,
            'axes': ['carrier byte/size pin enforcement', 'carrier ID/digest uniqueness',
                     'unsafe path rejection', 'canonical expected-record shape', 'exact restoration'],
            'source': 'tools/round-34/version-needs-counter.py', 'cases': cases,
            'original_files_utf8': {name: data.decode() for name, data in originals.items()}}
    if args.batch == 0:
        for name, data in originals.items():
            bounded_write(BASE / name, data)
        bounded_write(BASE / 'plan.json', encoded(plan))
        bounded_write(BASE / 'counter-under-test.py.txt', COUNTER.read_bytes())
        bounded_write(BASE / 'claims-at-freeze.json', (ROOT / '.ufo/waves/round-34/claims.json').read_bytes())
    elif (BASE / 'plan.json').read_bytes() != encoded(plan):
        raise RuntimeError('plan_changed')
    revision = command(['/usr/bin/git', '--no-replace-objects', '-c', 'core.fsmonitor=false', '-C', str(ROOT), 'rev-parse', 'HEAD', '--show-toplevel', '--abbrev-ref', 'HEAD'], 10)
    expected_identity = [FREEZE, str(ROOT), 'seat-r34-MutCounterPins']
    if revision['exit'] != 0 or revision['stdout'].splitlines() != expected_identity:
        raise RuntimeError('unexpected_sandbox_identity:' + revision['stdout'])
    instrument_paths = ['tools/round-34/version-needs-counter.py', 'tools/round-34/elf-version-needs.py',
                        'tools/round-34/freeze-integrity.py', '.ufo/waves/round-34/prep/R34Expected-files/author_expected.py',
                        '.ufo/waves/round-34/claims.json', '.ufo/waves/round-34/expected.json']
    pins_before = {name: sha((ROOT / name).read_bytes()) for name in instrument_paths}
    size = (len(cases) + 3) // 4
    selected = cases[args.batch * size:(args.batch + 1) * size]
    result = {'started_utc': utc(), 'batch': args.batch, 'measured_revision': FREEZE,
              'freeze_revision': FREEZE, 'sandbox_identity': revision,
              'counter_sha256': pins_before['tools/round-34/version-needs-counter.py'],
              'limits': {'address_space_bytes': 512 * 1024 * 1024, 'cpu_seconds': 30, 'processes_per_uid': 4096,
                         'per_file_bytes': MAX_WRITE, 'detector_wall_seconds': 15, 'outer_wall_seconds': 120,
                         'one_child_tree_at_a_time': True},
              'instruments_before': pins_before, 'case_count_total': len(cases), 'cases': []}
    try:
        for case in selected:
            receipt = probe_case(spec, originals, case)
            result['cases'].append(receipt)
            print(json.dumps({'case': case['name'], 'expected': case['expected_finding'],
                              'actual': receipt['mutated']['decoded'], 'verdict': receipt['verdict'],
                              'restored': receipt['exact_restoration']}, sort_keys=True), flush=True)
            bounded_write(BASE / ('batch-' + str(args.batch) + '.json'), encoded(result))
    finally:
        for name, data in originals.items():
            bounded_write(BASE / name, data)
        result['final_fixture_hashes'] = hash_files(originals)
        result['instruments_after'] = {name: sha((ROOT / name).read_bytes()) for name in instrument_paths}
        result['instruments_unchanged'] = result['instruments_before'] == result['instruments_after']
        result['exact_final_restoration'] = all((BASE / name).read_bytes() == data for name, data in originals.items())
        result['finished_utc'] = utc()
        result['counts'] = {verdict: sum(r['verdict'] == verdict for r in result['cases']) for verdict in ['killed', 'survived', 'inconclusive']}
        bounded_write(BASE / ('batch-' + str(args.batch) + '.json'), encoded(result))
    print(json.dumps({'batch': args.batch, 'counts': result['counts'], 'instruments_unchanged': result['instruments_unchanged'],
                      'exact_final_restoration': result['exact_final_restoration']}, sort_keys=True), flush=True)
    return 0 if result['counts']['inconclusive'] == result['counts']['survived'] == 0 and result['instruments_unchanged'] and result['exact_final_restoration'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
