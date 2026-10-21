#!/usr/bin/env python3
"""Round-24 red/green controls for the frozen C1/C2 instruments.

Usage: selftest.py --root <LANE> --rev <REV>

Clones REV into throwaway directories, applies one mutation per case,
commits it there, and runs the instrument blobs taken from REV itself (never
the worktree copy) against the clone. Prints one JSON line per case and a
summary; exit 0 only if every case matches its expectation, 1 otherwise,
2 on setup failure. Never writes to the lane.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

C1 = '.ufo/waves/round-24/tools/count-c1.py'
C2 = '.ufo/waves/round-24/tools/freeze-gate.py'
EV = '.ufo/waves/round-24/evidence/c1/'
ENTRY = 'corpus/knowledge/2026-10-21-r24-pcap-family-envelopes.md'
OLD_ENTRY = 'corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md'
R22_REFUSAL = '.ufo/waves/round-22/evidence/c2/inspect-packet-fields.json'
GATE_ARGS = ['--require-clean', 'round-24', '--disclosures', 'corpus/claim-freezes.tsv']


def run(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)


def git(repo, *args):
    p = run(['git', '-C', str(repo), *args])
    if p.returncode:
        raise RuntimeError('git ' + ' '.join(args[:2]) + ': ' + p.stderr.strip()[:200])
    return p.stdout


def commit(repo, message):
    git(repo, 'add', '-A')
    git(repo, '-c', 'user.name=selftest', '-c', 'user.email=selftest@invalid',
        '-c', 'commit.gpgsign=false', 'commit', '-q', '--allow-empty', '-m', message)
    return git(repo, 'rev-parse', 'HEAD').strip()


def edit_json(path, fn):
    data = json.loads(path.read_text())
    fn(data)
    path.write_text(json.dumps(data, indent=1, sort_keys=True) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--work-parent', default='/fast/scratch',
                   help='parent for throwaway clones (not /tmp: it shares the nearly full root disk)')
    a = p.parse_args()
    root = a.root.resolve()
    work = Path(tempfile.mkdtemp(prefix='kaidoku-r24-selftest-', dir=a.work_parent))
    try:
        rev = git(root, 'rev-parse', '--verify', a.rev + '^{commit}').strip()
        tools = work / 'tools'
        tools.mkdir()
        for rel in (C1, C2):
            (tools / Path(rel).name).write_bytes(subprocess.run(
                ['git', '-C', str(root), 'show', f'{rev}:{rel}'], capture_output=True, check=True).stdout)
        digests = {rel: hashlib.sha256((tools / Path(rel).name).read_bytes()).hexdigest() for rel in (C1, C2)}

        def clone(name):
            repo = work / name
            git(work, 'clone', '-q', '--shared', str(root), str(repo))
            git(repo, 'checkout', '-q', '--detach', rev)
            return repo

        def c1(repo, at='HEAD'):
            r = run(['python3', '-I', '-B', str(tools / 'count-c1.py'), '--root', str(repo), '--rev', at])
            out = json.loads(r.stdout) if r.stdout.strip() else {}
            return r.returncode, out.get('t2_held_count'), out.get('error')

        def c2(repo, extra=GATE_ARGS, at='HEAD'):
            r = run(['python3', '-I', '-B', str(tools / 'freeze-gate.py'), '--root', str(repo), '--rev', at, *extra])
            return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else {})

        results = []

        def case(name, observed, expected):
            ok = observed == expected
            results.append(ok)
            print(json.dumps({'case': name, 'expected': expected, 'observed': observed, 'pass': ok}))

        base = clone('base')
        case('c1_positive_at_rev', c1(base)[:2], (0, 4))

        r = clone('stdout')
        edit_json(r / EV / 'l1-pcap-client.run.json', lambda d: d.__setitem__('stdout', d['stdout'] + ' '))
        commit(r, 'stdout differs')
        case('c1_stdout_mismatch', c1(r)[:2], (1, 3))

        r = clone('exit')
        edit_json(r / EV / 'l1-packet-capture-http.run.json', lambda d: d.__setitem__('exit', 1))
        commit(r, 'nonzero exit')
        case('c1_nonzero_exit', c1(r)[:2], (1, 3))

        r = clone('norun')
        (r / EV / 'l1-pcap-capture-dns.run.json').unlink()
        (r / EV / 'l1-pcap-capture-tls.run.json').unlink()
        commit(r, 'run records removed')
        case('c1_run_record_missing', c1(r)[:2], (1, 3))

        r = clone('refusal')
        refusal = (r / R22_REFUSAL).read_bytes()
        (r / EV / 'l1-packet-fields-dns.envelope.json').write_bytes(refusal)
        edit_json(r / EV / 'l1-packet-fields-dns.run.json', lambda d: d.__setitem__('stdout', refusal.decode()))
        commit(r, 'refusal envelope')
        case('c1_refusal_not_counted', c1(r)[:2], (1, 3))

        r = clone('source')
        text = (r / ENTRY).read_text().split('\n', 1)
        (r / ENTRY).write_text('source: S063 only\n' + text[1])
        commit(r, 'ineligible source')
        case('c1_ineligible_source', c1(r)[:2], (1, 0))

        r = clone('mention')
        (r / ENTRY).write_text(re.sub(re.escape(EV) + r'[A-Za-z0-9._/-]+', 'ENVELOPE', (r / ENTRY).read_text()))
        commit(r, 'mention only')
        case('c1_mention_only', c1(r)[:2], (1, 0))

        r = clone('history')
        (r / OLD_ENTRY).write_text((r / OLD_ENTRY).read_text() + '\nedited\n')
        commit(r, 'historical knowledge edited')
        code, _, err = c1(r)
        case('c1_historical_knowledge_guard', (code, err), (2, 'historical_knowledge_changed'))

        code, out = c2(base)
        case('c2_clean_at_rev', (code, out.get('disclosures', {}).get('exact'), out.get('required_failed')), (0, 11, []))

        r = clone('absent')
        d = r / '.ufo/waves/round-99'
        d.mkdir(parents=True)
        (d / 'claims.json').write_text(json.dumps({'claims': [{'counting_command': 'python3 .ufo/waves/round-99/tools/missing.py'}]}))
        commit(r, 'freeze with absent instrument')
        code, out = c2(r, ['--require-clean', 'round-99'])
        f = next(x for x in out['freezes'] if 'round-99' in x['claims_file'])
        case('c2_absent_flagged', (code, sorted({x['finding'] for x in f['findings']})), (1, ['INSTRUMENT_ABSENT']))

        r = clone('pins')
        d = r / '.ufo/waves/round-98'
        (d / 'tools').mkdir(parents=True)
        (d / 'tools' / 'm.py').write_text('print(1)\n')
        commit(r, 'instrument first')
        good = hashlib.sha256(b'print(1)\n').hexdigest()
        (d / 'claims.json').write_text(json.dumps({'instruments': {'.ufo/waves/round-98/tools/m.py': '0' * 64},
                                                   'claims': [{'counting_command': 'python3 .ufo/waves/round-98/tools/m.py'}]}))
        commit(r, 'freeze with wrong pin')
        code, out = c2(r, ['--require-clean', 'round-98'])
        f = next(x for x in out['freezes'] if 'round-98' in x['claims_file'])
        case('c2_pin_mismatch', (code, sorted({x['finding'] for x in f['findings']})), (1, ['INSTRUMENT_PIN_MISMATCH']))

        r = clone('revised')
        d = r / '.ufo/waves/round-97'
        (d / 'tools').mkdir(parents=True)
        (d / 'tools' / 'm.py').write_text('print(1)\n')
        commit(r, 'instrument first')
        (d / 'claims.json').write_text(json.dumps({'instruments': {'.ufo/waves/round-97/tools/m.py': good},
                                                   'claims': [{'counting_command': 'python3 .ufo/waves/round-97/tools/m.py'}]}))
        commit(r, 'clean freeze')
        code, out = c2(r, ['--require-clean', 'round-97'])
        case('c2_clean_pinned_freeze', code, 0)
        (d / 'tools' / 'm.py').write_text('print(2)\n')
        changed = commit(r, 'undisclosed revision')
        code, out = c2(r, ['--require-clean', 'round-97'])
        f = next(x for x in out['freezes'] if 'round-97' in x['claims_file'])
        case('c2_undisclosed_revision', (code, sorted({x['finding'] for x in f['findings']})), (1, ['INSTRUMENT_REVISED']))
        edit_json(d / 'claims.json', lambda c: c.__setitem__('instrument_supersessions', [
            {'path': '.ufo/waves/round-97/tools/m.py', 'commit': changed, 'reason': 'selftest disclosure'}]))
        commit(r, 'disclose revision')
        code, out = c2(r, ['--require-clean', 'round-97'])
        case('c2_disclosed_revision_clean', code, 0)

        r = clone('bare')
        d = r / '.ufo/waves/round-96'
        d.mkdir(parents=True)
        (d / 'claims.json').write_text(json.dumps({'claims': [{'cmd': 'run check.py --root LANE'}]}))
        commit(r, 'bare name')
        code, out = c2(r, ['--require-clean', 'round-96'])
        f = next(x for x in out['freezes'] if 'round-96' in x['claims_file'])
        case('c2_bare_name_unresolved', (code, sorted({x['finding'] for x in f['findings']})), (1, ['INSTRUMENT_UNRESOLVED']))

        r = clone('ledger')
        led = r / 'corpus/claim-freezes.tsv'
        led.write_text(led.read_text().replace('round-23\tFLAGGED\tINSTRUMENT_ABSENT,INSTRUMENT_REVISED',
                                               'round-23\tFLAGGED\tINSTRUMENT_REVISED'))
        commit(r, 'ledger disagrees')
        code, out = c2(r)
        case('c2_ledger_mismatch', (code, out.get('disclosures', {}).get('mismatched')), (1, ['round-23']))

        r = clone('stray')
        led = r / 'corpus/claim-freezes.tsv'
        led.write_text(led.read_text() + 'round-95\tCLEAN\t-\tno such freeze\n')
        commit(r, 'stray row')
        code, out = c2(r)
        case('c2_stray_row', (code, out.get('disclosures', {}).get('stray')), (1, ['round-95']))

        print(json.dumps({'rev': rev, 'instrument_sha256': digests, 'cases': len(results),
                          'passed': sum(results), 'exit': 0 if all(results) else 1}))
        return 0 if all(results) else 1
    except (RuntimeError, OSError, ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        print(json.dumps({'finding': 'selftest_setup_failed', 'error': str(error)}))
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
