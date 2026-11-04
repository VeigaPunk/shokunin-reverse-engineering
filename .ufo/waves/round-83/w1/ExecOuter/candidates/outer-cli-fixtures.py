#!/usr/bin/env python3
"""Reusable outer-CLI fixtures for the round-83 attribution claim (R83-C1).

Drives the frozen counter ``tools/round-83/attribution-audit.py`` from a
committed revision:

* ``audit-legacy-red``    — legacy target ``tools/round-82/printed-command.py``
  at BASE with the same FREEZE (the plan's Before command); expected rc 1 with
  finding ``real-withdrawn``.
* ``audit-candidate-green`` — new target ``tools/round-83/source-bind.py`` at
  ``--rev``; expected rc 0 with no mismatches.
* ``cli-positive-S286`` / ``cli-negative-S299`` — subject CLI contract
  ``--entry FILE --sid SNNN --json-out FILE`` against the BASE knowledge entry
  bytes; expected rc 0 (attributed) and rc 1 (not_attributed).

Mirrors ``tools/round-82/cli-fixtures.py``: one ``--shared --no-checkout``
clone, detached checkout, clean child env, per-case receipts, scratch removed
in ``finally``. The candidate is read from the committed revision, never
fabricated; arms report the actual exit honestly when it is absent, so the
driver stays executable for L1 to run after integration.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# Mirror the constants of tools/round-83/attribution-audit.py (single source
# of truth remains the frozen counter; repeated here for arm construction).
BASE = '650344bc37ca303fb9487c1174192057af499b9b'
ENTRY = 'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md'
OLD = 'tools/round-82/printed-command.py'
COUNTER = 'tools/round-83/attribution-audit.py'
CANDIDATE = 'tools/round-83/source-bind.py'
POSITIVE_SID = 'S286'
NEGATIVE_SID = 'S299'
CLI_EXITS = {0: 'attributed', 1: 'not_attributed', 2: 'unavailable'}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', required=True, help='lane git repository, read-only baseline')
    ap.add_argument('--rev', required=True, help='committed revision holding counter and candidate')
    ap.add_argument('--freeze', required=True, help='revision holding frozen attribution-cases.json')
    ap.add_argument('--work', required=True, help='scratch directory for the private clone')
    ap.add_argument('--json-out', required=True)
    a = ap.parse_args()
    a.root = str(Path(a.root).resolve())
    a.work = str(Path(a.work).resolve())
    Path(a.work).mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix='outer-cli-', dir=a.work))
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': str(scratch),
           'TMPDIR': str(scratch), 'LANG': 'C.UTF-8'}
    rows = []

    def git(repo, *args):
        return subprocess.run(['git', '-C', str(repo), *args], env=env,
                              capture_output=True, text=True, check=True).stdout

    def case(name, argv, expected_exit, expected_id=None, kind='audit'):
        out = scratch / (name + '.json')
        try:
            p = subprocess.run(argv, cwd=scratch / 'repo', env=env,
                               capture_output=True, text=True, timeout=300)
            rc, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, so, se = 'timeout', '', str(e)
        receipt = {}
        if out.exists():
            try:
                receipt = json.loads(out.read_text())
            except ValueError:
                receipt = {'unparsable': out.read_text(errors='replace')[:2000]}
        if not isinstance(receipt, dict):
            receipt = {'invalid_receipt': receipt}
        mismatches = receipt.get('mismatches')
        if rc != expected_exit:
            finding = CLI_EXITS.get(rc, 'unexpected') if kind == 'cli' else 'unexpected'
        elif kind == 'cli':
            finding = CLI_EXITS.get(rc, 'unexpected')
        elif expected_id is None:
            finding = 'clean' if mismatches == [] else 'unexpected'
        elif isinstance(mismatches, list) and expected_id in mismatches:
            finding = expected_id
        else:
            finding = 'missing:' + json.dumps(mismatches)
        expected_finding = (CLI_EXITS[expected_exit] if kind == 'cli'
                            else expected_id or 'clean')
        fields_match = True
        if kind == 'cli':
            expected_fields = {'schema': 'kaidoku-r83-source-bind-v1',
                               'sid': POSITIVE_SID if expected_exit == 0 else NEGATIVE_SID,
                               'cites': expected_exit == 0,
                               'status': 'attributed' if expected_exit == 0 else 'not-attributed'}
            fields_match = all(type(receipt.get(key)) is type(value)
                               and receipt.get(key) == value
                               for key, value in expected_fields.items())
        rows.append({'case': name, 'kind': kind, 'argv': argv,
                     'exit': rc, 'expected_exit': expected_exit,
                     'finding': finding, 'expected_finding': expected_finding,
                     'mismatch_count': receipt.get('mismatch_count'),
                     'output': receipt,
                     'fields_match': fields_match,
                     'stdout': so[-2000:], 'stderr': se[-2000:],
                     'pass': rc == expected_exit and finding == expected_finding and fields_match})

    try:
        repo = scratch / 'repo'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', a.root, str(repo)],
                       env=env, capture_output=True, check=True, timeout=300)
        assert Path(git(repo, 'rev-parse', '--show-toplevel').strip()) == repo.resolve()
        git(repo, 'checkout', '--detach', a.rev)

        def py(rel):
            return [sys.executable, '-I', '-B', str(repo / rel)]

        # 1) legacy red: BASE substituted for REV, same FREEZE (plan Before command).
        case('audit-legacy-red',
             py(COUNTER) + ['--root', str(repo), '--rev', BASE, '--freeze', a.freeze,
                            '--target', OLD, '--json-out', str(scratch / 'audit-legacy-red.json')],
             expected_exit=1, expected_id='real-withdrawn')
        # 2) candidate green at the committed revision.
        case('audit-candidate-green',
             py(COUNTER) + ['--root', str(repo), '--rev', a.rev, '--freeze', a.freeze,
                            '--target', CANDIDATE, '--json-out', str(scratch / 'audit-candidate-green.json')],
             expected_exit=0, expected_id=None)
        # 3/4) subject CLI positive/negative fields on the BASE entry bytes.
        entry = scratch / 'entry-base.md'
        entry.write_bytes(subprocess.run(['git', '-C', str(repo), 'show', BASE + ':' + ENTRY],
                                         env=env, capture_output=True, check=True,
                                         timeout=300).stdout)
        for name, sid, expected in [('cli-positive-' + POSITIVE_SID, POSITIVE_SID, 0),
                                    ('cli-negative-' + NEGATIVE_SID, NEGATIVE_SID, 1)]:
            case(name, py(CANDIDATE) + ['--entry', str(entry), '--sid', sid,
                                        '--json-out', str(scratch / (name + '.json'))],
                 expected_exit=expected, expected_id=None, kind='cli')
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    try:
        instrument = str(Path(__file__).resolve().relative_to(Path(a.root).resolve()))
    except ValueError:
        instrument = str(Path(__file__).resolve())
    result = {'schema': 'kaidoku-r83-outer-cli-fixtures-v1',
              'root': a.root, 'rev': a.rev, 'freeze': a.freeze, 'base': BASE,
              'instrument': {'path': instrument,
                             'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
              'cases': rows,
              'failures': [r['case'] for r in rows if not r['pass']],
              'cleanup': True}
    out = Path(a.json_out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps(result, sort_keys=True))
    return 1 if result['failures'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
