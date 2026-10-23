#!/usr/bin/env python3
"""Round-30 pre-freeze gate: round-29 routed defect 3 (M29-3) as an exit-code check.

Routed defect 3 of corpus/lessons/round-29-verifier-spotcheck.md: the round-29 freeze file
names tools/round-28/c1-heldout-naming.py in a claim's own text but pins no sha256 for it,
and the run-before-freeze step was a procedure rather than a check.  This gate turns both
into exit codes for one round, reading Git objects only (no working-tree read, no write):

  python3 -I -B tools/round-30/prefreeze-gate.py --root <LANE> --round <N> [--rev <REV>]

For round <N>:
  freeze  the first commit (reachable from --rev, default HEAD) that adds
          .ufo/waves/round-<N>/claims.json.
  pins    every path recorded under `instruments`, `frozen_inputs` (round-30 shape) and
          `loaded_by_counter`, `producers_not_counters` (round-29 shape) in the claims
          file at the freeze commit: a string value is a sha256 pin and the path must be
          a blob at the freeze commit with that digest; a list value records paths with
          no digest and each must at least be a blob at the freeze commit.
  data    no path under corpus/evidence/round-<N>/ that lies in an `envelopes/`
          directory or is named `runs.tsv` may have been added at or before the freeze
          commit (run-before-freeze).
  tools   every `tools/*.py|sh|mjs|js` path named in a claim's own strings must be
          digest-pinned in the claims file at the freeze commit or listed under
          `instrument_supersessions` (path and reason) in the claims file at --rev.

Findings (printed as `FINDING <code> <path> ...`, sorted by code then path):
  PIN_ABSENT          a pinned/list-recorded path is not a blob at the freeze commit
  PIN_MISMATCH        recorded sha256 != blob sha256 at the freeze commit
  DATA_BEFORE_FREEZE  an envelopes/ or runs.tsv path was added at or before the freeze
  TOOL_UNPINNED       a tools/ path named in claim text has no pin and no supersession
Exit: 0 clean; 1 any finding; 2 cannot evaluate (root not a repository top, no freeze
commit, unreadable claims file, bad --round).
`--selftest` builds throwaway Git fixture repositories in a temp dir and runs the same
audit on them; it prints `selftest cases=<N> failures=<M>` and exits 0/1.
Limits: commit timestamps and authorship are not authenticated; paths named only in prose
outside the claims file are not seen; a path recorded only in a list is checked for
presence, not digest; an `instrument_supersessions` entry is honoured on path+reason, its
commit and sha256 fields are not verified.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

PIN_KEYS = ('instruments', 'frozen_inputs', 'loaded_by_counter', 'producers_not_counters')
TOOL = re.compile(r'(?<![A-Za-z0-9_./-])(tools/[A-Za-z0-9._/-]+\.(?:py|sh|mjs|js))(?![A-Za-z0-9_-])')
ROUND = re.compile(r'^(?:round-)?([0-9]+)$')
HEX40 = re.compile(r'^[0-9a-f]{40}$')


def harden_env():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1',
                      GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_COUNT='2',
                      GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
                      GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null',
                      GIT_OPTIONAL_LOCKS='0')


def git(root, *args, ok=(0,)):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if p.returncode not in ok:
        raise ValueError('git_failed: ' + ' '.join(args[:4]))
    return p


def strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, list):
        for item in node:
            yield from strings(item)
    elif isinstance(node, dict):
        for item in node.values():
            yield from strings(item)


def blob_sha256(root, rev, path):
    p = git(root, 'cat-file', '-e', f'{rev}:{path}', ok=(0, 1, 128))
    if p.returncode:
        return None
    if git(root, 'cat-file', '-t', f'{rev}:{path}').stdout.strip() != b'blob':
        return None
    return hashlib.sha256(git(root, 'show', f'{rev}:{path}').stdout).hexdigest()


def extract_pins(obj):
    """path -> recorded sha256, or None when the claims file records the path in a list
    (round-30 loaded_by_counter shape) and pins no digest for it."""
    pins = {}
    if not isinstance(obj, dict):
        return pins
    for key in PIN_KEYS:
        node = obj.get(key)
        if isinstance(node, dict):
            for path, value in node.items():
                if not isinstance(path, str):
                    continue
                if isinstance(value, str):
                    pins[path] = value
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, str) and item not in pins:
                            pins[item] = None
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str):
                    pins.setdefault(item, None)
    return pins


def is_data_path(path, round_dir):
    if not path.startswith(round_dir + '/'):
        return False
    parts = path[len(round_dir) + 1:].split('/')
    return 'envelopes' in parts[:-1] or parts[-1] == 'runs.tsv'


def data_before_freeze(root, freeze, round_dir):
    p = git(root, 'log', '--no-renames', '--diff-filter=A', '--name-only',
            '--format=%H', freeze, '--', round_dir)
    found = []
    commit = None
    for line in p.stdout.decode('utf-8', 'replace').splitlines():
        line = line.strip()
        if not line:
            continue
        if HEX40.match(line):
            commit = line
        elif is_data_path(line, round_dir):
            found.append({'path': line, 'commit': commit})
    return found


def supersession_paths(root, rev, freeze, claims_path):
    found = set()
    for r in (freeze, rev):
        p = git(root, 'show', f'{r}:{claims_path}', ok=(0, 1, 128))
        if p.returncode:
            continue
        try:
            obj = json.loads(p.stdout.decode('utf-8'))
        except (UnicodeError, ValueError):
            continue
        node = obj.get('instrument_supersessions') if isinstance(obj, dict) else None
        if isinstance(node, list):
            for entry in node:
                if (isinstance(entry, dict) and isinstance(entry.get('path'), str)
                        and str(entry.get('reason') or '').strip()):
                    found.add(entry['path'])
    return found


def audit(root, round_arg, rev):
    m = ROUND.match(str(round_arg))
    if not m:
        raise ValueError('round_invalid: ' + str(round_arg))
    n = int(m.group(1))
    claims_path = f'.ufo/waves/round-{n}/claims.json'
    round_dir = f'corpus/evidence/round-{n}'
    if git(root, 'rev-parse', '--show-prefix').stdout.strip():
        raise ValueError('root_not_repository_top')
    measured = git(root, 'rev-parse', '--verify', '--end-of-options',
                   rev + '^{commit}').stdout.decode().strip()
    added = git(root, 'log', '--no-renames', '--format=%H', '--diff-filter=A',
                measured, '--', claims_path).stdout.split()
    if not added:
        raise ValueError('freeze_commit_unknown: no commit adds ' + claims_path)
    freeze = added[-1].decode()
    try:
        frozen = json.loads(git(root, 'show', f'{freeze}:{claims_path}').stdout.decode('utf-8'))
    except (UnicodeError, ValueError) as error:
        raise ValueError('claims_unreadable: ' + str(error))
    if not isinstance(frozen, dict):
        raise ValueError('claims_not_an_object')
    claims = frozen.get('claims')
    if not isinstance(claims, list):
        claims = [frozen]
    pins = extract_pins(frozen)
    findings = []
    present = 0
    unhashed = 0
    for path in sorted(pins):
        digest = pins[path]
        at_freeze = blob_sha256(root, freeze, path)
        if at_freeze is None:
            findings.append({'finding': 'PIN_ABSENT', 'path': path})
        elif digest is None:
            unhashed += 1
            present += 1
        elif digest != at_freeze:
            findings.append({'finding': 'PIN_MISMATCH', 'path': path,
                             'pinned': digest, 'at_freeze': at_freeze})
        else:
            present += 1
    data = data_before_freeze(root, freeze, round_dir)
    for row in data:
        findings.append({'finding': 'DATA_BEFORE_FREEZE', 'path': row['path'],
                         'commit': row['commit']})
    texts = [s for claim in claims for s in strings(claim)]
    named = sorted({mm.group(1) for s in texts for mm in TOOL.finditer(s)})
    superseded = supersession_paths(root, measured, freeze, claims_path)
    pinned = {path for path, digest in pins.items() if digest is not None}
    unpinned = [path for path in named if path not in pinned and path not in superseded]
    for path in unpinned:
        findings.append({'finding': 'TOOL_UNPINNED', 'path': path})
    findings.sort(key=lambda f: (f['finding'], f['path']))
    result = {'gate': 'prefreeze', 'round': f'round-{n}', 'claims_file': claims_path,
              'freeze': freeze, 'rev': measured, 'pins': len(pins), 'pins_present': present,
              'pins_unhashed': unhashed,
              'pins_mismatch': sum(1 for f in findings if f['finding'] == 'PIN_MISMATCH'),
              'data_before_freeze': len(data), 'tools_named': len(named),
              'tools_unpinned': len(unpinned), 'findings': findings,
              'verdict': 'FLAGGED' if findings else 'CLEAN'}
    return result, 1 if findings else 0


def report(result):
    print('prefreeze round=%s freeze=%s rev=%s claims=%s'
          % (result['round'], result['freeze'], result['rev'], result['claims_file']))
    for f in result['findings']:
        extra = ''
        if f['finding'] == 'PIN_MISMATCH':
            extra = ' pinned=%s at_freeze=%s' % (f['pinned'], f['at_freeze'])
        elif f['finding'] == 'DATA_BEFORE_FREEZE':
            extra = ' commit=%s' % f['commit']
        print('FINDING %s %s%s' % (f['finding'], f['path'], extra))
    print('pins=%d present=%d unhashed=%d mismatch=%d data_before_freeze=%d '
          'tools_named=%d tools_unpinned=%d findings=%d'
          % (result['pins'], result['pins_present'], result['pins_unhashed'],
             result['pins_mismatch'], result['data_before_freeze'], result['tools_named'],
             result['tools_unpinned'], len(result['findings'])))
    print('verdict=%s' % result['verdict'])


def _git(repo, *args):
    p = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=False)
    if p.returncode != 0:
        raise RuntimeError('fixture git failed: git %s: %s'
                           % (' '.join(args), p.stderr.decode('utf-8', 'replace')))
    return p


def _new_repo(tmp, name):
    repo = Path(tmp) / name
    repo.mkdir(parents=True)
    _git(repo, 'init', '-q', '-b', 'main')
    return repo


def _commit(repo, message, files):
    for rel, data in files.items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data.encode() if isinstance(data, str) else data)
    _git(repo, 'add', '-A')
    _git(repo, '-c', 'user.name=prefreeze-selftest', '-c', 'user.email=selftest@local',
         'commit', '-q', '-m', message)
    return _git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()


def _claims(pins=None, claims=None, **extra):
    obj = dict(pins or {})
    obj['claims'] = claims if claims is not None else []
    obj.update(extra)
    return json.dumps(obj, sort_keys=True, indent=1) + '\n'


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def selftest():
    harden_env()
    tmp = tempfile.mkdtemp(prefix='prefreeze-selftest-')
    cases = []
    fails = 0

    def check(name, repo, want_code, want_codes, want_paths=(), round_arg='97',
              want_data_commit=None):
        nonlocal fails
        try:
            result, code = audit(repo, round_arg, 'HEAD')
        except (OSError, ValueError, UnicodeError, KeyError, RecursionError,
                AttributeError) as error:
            result, code = {'findings': [], 'error': str(error)}, 2
        codes = sorted({f['finding'] for f in result['findings']})
        paths = sorted({f['path'] for f in result['findings']})
        ok = (code == want_code
              and (want_codes is None or codes == sorted(want_codes))
              and all(p in paths for p in want_paths))
        if want_data_commit is not None:
            ok = ok and all(f.get('commit') == want_data_commit
                            for f in result['findings']
                            if f['finding'] == 'DATA_BEFORE_FREEZE')
        why = 'code=%s codes=%s' % (code, codes)
        cases.append((name, ok, why))
        if not ok:
            fails += 1

    try:
        counter = 'print("counter")\n'
        repo = _new_repo(tmp, 'clean')
        _commit(repo, 'freeze', {
            'tools/round-97/counter.py': counter,
            '.ufo/waves/round-97/claims.json': _claims(
                {'instruments': {'tools/round-97/counter.py': _sha(counter)}},
                [{'id': 'R97-C1', 'counter': 'python3 -I -B tools/round-97/counter.py'}])})
        check('clean', repo, 0, [], [])
        check('round_arg_form', repo, 0, [], [], round_arg='round-97')
        check('round_invalid', repo, 2, None, [], round_arg='abc')

        repo = _new_repo(tmp, 'pin_absent')
        _commit(repo, 'freeze', {'.ufo/waves/round-97/claims.json': _claims(
            {'instruments': {'tools/round-97/gone.py': '0' * 64}}, [])})
        check('pin_absent', repo, 1, ['PIN_ABSENT'], ['tools/round-97/gone.py'])

        repo = _new_repo(tmp, 'pin_mismatch')
        _commit(repo, 'freeze', {
            'tools/round-97/counter.py': 'print("v2")\n',
            '.ufo/waves/round-97/claims.json': _claims(
                {'instruments': {'tools/round-97/counter.py': _sha('print("v1")\n')}}, [])})
        check('pin_mismatch', repo, 1, ['PIN_MISMATCH'], ['tools/round-97/counter.py'])

        repo = _new_repo(tmp, 'r29_keys')
        helper = 'print("helper")\n'
        _commit(repo, 'freeze', {
            'tools/round-25/helper.py': helper,
            '.ufo/waves/round-97/claims.json': _claims({
                'loaded_by_counter': {'tools/round-25/helper.py': _sha(helper),
                                      'corpus/evidence/round-97/c1/x.tsv': _sha('x\n')},
                'producers_not_counters': {'tools/round-97/prod.py': _sha('prod\n')}}, [])})
        check('r29_keys', repo, 1, ['PIN_ABSENT'],
              ['corpus/evidence/round-97/c1/x.tsv', 'tools/round-97/prod.py'])

        repo = _new_repo(tmp, 'r30_list')
        _commit(repo, 'freeze', {
            'tools/round-97/counter.py': counter,
            'corpus/evidence/round-97/c1/carriers.tsv': 'id\n',
            '.ufo/waves/round-97/claims.json': _claims({
                'instruments': {'tools/round-97/counter.py': _sha(counter)},
                'loaded_by_counter': {'c1': ['tools/round-97/counter.py',
                                             'corpus/evidence/round-97/c1/carriers.tsv']}},
                [{'id': 'R97-C1', 'counter': 'tools/round-97/counter.py'}])})
        check('r30_list', repo, 0, [], [])

        repo = _new_repo(tmp, 'r30_list_absent')
        _commit(repo, 'freeze', {'.ufo/waves/round-97/claims.json': _claims(
            {'loaded_by_counter': {'c1': ['tools/round-97/missing.py']}}, [])})
        check('r30_list_absent', repo, 1, ['PIN_ABSENT'], ['tools/round-97/missing.py'])

        repo = _new_repo(tmp, 'envelope_at_freeze')
        _commit(repo, 'freeze', {
            'corpus/evidence/round-97/c1/envelopes/a.json': '{}\n',
            '.ufo/waves/round-97/claims.json': _claims()})
        check('envelope_at_freeze', repo, 1, ['DATA_BEFORE_FREEZE'],
              ['corpus/evidence/round-97/c1/envelopes/a.json'])

        repo = _new_repo(tmp, 'runs_before_freeze')
        first = _commit(repo, 'inputs', {
            'corpus/evidence/round-97/c1/runs.tsv': 'id\n',
            'corpus/evidence/round-97/c2/deep/envelopes/x.json': '{}\n'})
        _commit(repo, 'freeze', {'.ufo/waves/round-97/claims.json': _claims()})
        check('runs_before_freeze', repo, 1, ['DATA_BEFORE_FREEZE'],
              ['corpus/evidence/round-97/c1/runs.tsv',
               'corpus/evidence/round-97/c2/deep/envelopes/x.json'],
              want_data_commit=first)

        repo = _new_repo(tmp, 'data_after_freeze')
        _commit(repo, 'freeze', {'.ufo/waves/round-97/claims.json': _claims()})
        _commit(repo, 'data', {'corpus/evidence/round-97/c1/runs.tsv': 'id\n',
                               'corpus/evidence/round-97/c1/envelopes/a.json': '{}\n'})
        check('data_after_freeze', repo, 0, [], [])

        repo = _new_repo(tmp, 'other_round_data')
        _commit(repo, 'freeze', {'corpus/evidence/round-96/c1/runs.tsv': 'id\n',
                                 '.ufo/waves/round-97/claims.json': _claims()})
        check('other_round_data', repo, 0, [], [])

        repo = _new_repo(tmp, 'tool_unpinned')
        _commit(repo, 'freeze', {
            'tools/round-98/other.py': 'print("o")\n',
            '.ufo/waves/round-97/claims.json': _claims(
                {}, [{'id': 'R97-C1', 'counter': 'python3 -I -B tools/round-98/other.py'}])})
        check('tool_unpinned', repo, 1, ['TOOL_UNPINNED'], ['tools/round-98/other.py'])

        repo = _new_repo(tmp, 'tool_pinned')
        other = 'print("o")\n'
        _commit(repo, 'freeze', {
            'tools/round-98/other.py': other,
            '.ufo/waves/round-97/claims.json': _claims(
                {'instruments': {'tools/round-98/other.py': _sha(other)}},
                [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}])})
        check('tool_pinned', repo, 0, [], [])

        repo = _new_repo(tmp, 'tool_superseded')
        freeze = _commit(repo, 'freeze', {
            'tools/round-98/other.py': other,
            '.ufo/waves/round-97/claims.json': _claims(
                {}, [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}])})
        _commit(repo, 'supersede', {'.ufo/waves/round-97/claims.json': _claims(
            {}, [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}],
            instrument_supersessions=[{'path': 'tools/round-98/other.py', 'commit': freeze,
                                       'reason': 'pin note'}])})
        check('tool_superseded', repo, 0, [], [])

        repo = _new_repo(tmp, 'tool_supersession_no_reason')
        freeze = _commit(repo, 'freeze', {
            'tools/round-98/other.py': other,
            '.ufo/waves/round-97/claims.json': _claims(
                {}, [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}])})
        _commit(repo, 'supersede', {'.ufo/waves/round-97/claims.json': _claims(
            {}, [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}],
            instrument_supersessions=[{'path': 'tools/round-98/other.py', 'commit': freeze,
                                       'reason': ''}])})
        check('tool_supersession_no_reason', repo, 1, ['TOOL_UNPINNED'],
              ['tools/round-98/other.py'])

        repo = _new_repo(tmp, 'late_pin_not_counted')
        _commit(repo, 'freeze', {
            'tools/round-98/other.py': other,
            '.ufo/waves/round-97/claims.json': _claims(
                {}, [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}])})
        _commit(repo, 'late pin', {'.ufo/waves/round-97/claims.json': _claims(
            {'instruments': {'tools/round-98/other.py': _sha(other)}},
            [{'id': 'R97-C1', 'counter': 'tools/round-98/other.py'}])})
        check('late_pin_not_counted', repo, 1, ['TOOL_UNPINNED'], ['tools/round-98/other.py'])

        repo = _new_repo(tmp, 'no_claims')
        _commit(repo, 'empty', {'README': 'x\n'})
        check('no_claims', repo, 2, None, [])

        repo = _new_repo(tmp, 'bad_json')
        _commit(repo, 'freeze', {'.ufo/waves/round-97/claims.json': '{not json\n'})
        check('bad_json', repo, 2, None, [])

        not_repo = Path(tmp) / 'not_repo'
        not_repo.mkdir()
        check('not_repo', not_repo, 2, None, [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for name, ok, why in cases:
        print('%s %s got=%s' % ('ok' if ok else 'FAIL', name, why))
    print('selftest cases=%d failures=%d' % (len(cases), fails))
    return 1 if fails else 0


def main():
    harden_env()
    ap = argparse.ArgumentParser(description='pre-freeze gate (round-29 routed defect 3, M29-3)')
    ap.add_argument('--root', type=Path)
    ap.add_argument('--round', metavar='N')
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.root is None or a.round is None:
        ap.error('--root and --round are required unless --selftest is given')
    try:
        result, code = audit(a.root.resolve(), a.round, a.rev)
    except (OSError, ValueError, UnicodeError, KeyError, RecursionError, AttributeError) as error:
        print('prefreeze round=%s unevaluable: %s' % (a.round, error), file=sys.stderr)
        return 2
    report(result)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
