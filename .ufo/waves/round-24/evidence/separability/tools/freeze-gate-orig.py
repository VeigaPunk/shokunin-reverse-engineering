#!/usr/bin/env python3
"""R24-C2 claim-freeze instrument gate (frozen before the claim).

For every retained `.ufo/waves/round-*/claims.json` at MEASURED (default: the
given --rev), the gate reads Git objects only and reports, per claim freeze:

  freeze      first commit that added the claims file (its freeze commit)
  instruments lane-relative script paths named inside each claim's strings
              (*.py, *.sh, *.mjs, *.js under .ufo/ or corpus/ or tools/)
  findings    INSTRUMENT_NONE      no instrument path named by any claim
              INSTRUMENT_ABSENT    a named instrument is not a blob at freeze
              INSTRUMENT_UNPINNED  claims file records no sha256 for it
              INSTRUMENT_PIN_MISMATCH  recorded sha256 != blob at freeze
              INSTRUMENT_REVISED   commits in freeze..MEASURED changed it and
                                   the claims file at MEASURED does not list
                                   each of them under instrument_supersessions
  verdict     CLEAN (no findings) or FLAGGED

A claims file pins instruments with a top-level object
`"instruments": {"<path>": "<sha256>"}`; a later revision is disclosed with
`"instrument_supersessions": [{"path", "commit", "reason"}]` appended to the
same file. Optional --disclosures <lane path> reads a TSV ledger at MEASURED
(header `round<TAB>verdict<TAB>findings<TAB>pointer`; findings are the sorted
unique finding codes joined by commas, `-` when CLEAN); a freeze counts as
disclosed only when its row's verdict and code set equal the gate's.
Exit: 0 when every --require-clean freeze exists and is CLEAN and, when
--disclosures is given, every audited freeze is disclosed exactly with no
stray rows; 1 otherwise; 2 when the input cannot be evaluated. The audit
always prints every verdict.
Limits: commit timestamps and authorship are not authenticated; a path named
only in prose outside claims.json is not seen; the ledger is author-written
and checked for agreement, not for completeness of its prose pointer.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

CLAIMS = re.compile(r'^\.ufo/waves/(round-[0-9]+)/claims\.json$')
SCRIPT = re.compile(r'(?<![A-Za-z0-9_./-])((?:\.ufo|corpus|tools)/[A-Za-z0-9._/-]+\.(?:py|sh|mjs|js))(?![A-Za-z0-9_-])')


def git(root, *args, ok=(0,)):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if p.returncode not in ok:
        raise ValueError('git_failed: ' + ' '.join(args[:3]))
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


def audit_one(root, measured, claims_path):
    added = git(root, 'log', '--format=%H', '--diff-filter=A', measured, '--', claims_path).stdout.split()
    if not added:
        raise ValueError('freeze_commit_unknown: ' + claims_path)
    freeze = added[-1].decode()
    frozen = json.loads(git(root, 'show', f'{freeze}:{claims_path}').stdout.decode('utf-8'))
    current = json.loads(git(root, 'show', f'{measured}:{claims_path}').stdout.decode('utf-8'))
    claims = frozen.get('claims') if isinstance(frozen, dict) else None
    if not isinstance(claims, list):
        claims = [frozen]
    pins = frozen.get('instruments') if isinstance(frozen, dict) else None
    pins = pins if isinstance(pins, dict) else {}
    disclosed = current.get('instrument_supersessions') if isinstance(current, dict) else None
    disclosed = {(d.get('path'), d.get('commit')) for d in disclosed
                 if isinstance(d, dict) and d.get('reason')} if isinstance(disclosed, list) else set()
    paths = sorted({m.group(1) for claim in claims for s in strings(claim) for m in SCRIPT.finditer(s)})
    findings = []
    if not paths:
        findings.append({'finding': 'INSTRUMENT_NONE'})
    for path in paths:
        digest = blob_sha256(root, freeze, path)
        if digest is None:
            findings.append({'finding': 'INSTRUMENT_ABSENT', 'path': path})
        elif path not in pins:
            findings.append({'finding': 'INSTRUMENT_UNPINNED', 'path': path})
        elif pins[path] != digest:
            findings.append({'finding': 'INSTRUMENT_PIN_MISMATCH', 'path': path,
                             'pinned': pins[path], 'at_freeze': digest})
        revs = git(root, 'rev-list', '--reverse', f'{freeze}..{measured}', '--', path).stdout.decode().split()
        undisclosed = [r for r in revs if (path, r) not in disclosed]
        if undisclosed:
            findings.append({'finding': 'INSTRUMENT_REVISED', 'path': path,
                             'commits': undisclosed, 'disclosed': len(revs) - len(undisclosed)})
    return {'claims_file': claims_path, 'freeze': freeze, 'instruments': paths,
            'findings': findings, 'verdict': 'FLAGGED' if findings else 'CLEAN'}


def read_disclosures(root, measured, path):
    p = git(root, 'cat-file', '-e', f'{measured}:{path}', ok=(0, 1, 128))
    if p.returncode:
        return None
    lines = git(root, 'show', f'{measured}:{path}').stdout.decode('utf-8').splitlines()
    if not lines or lines[0].split('\t') != ['round', 'verdict', 'findings', 'pointer']:
        raise ValueError('disclosures_header_invalid')
    rows = {}
    for line in lines[1:]:
        cells = line.split('\t')
        if len(cells) != 4 or cells[0] in rows or not cells[3].strip():
            raise ValueError('disclosures_row_invalid: ' + line[:60])
        rows[cells[0]] = (cells[1], cells[2])
    return rows


def audit(root, rev, require_clean, disclosures):
    if git(root, 'rev-parse', '--show-prefix').stdout.strip():
        raise ValueError('root_not_repository_top')
    measured = git(root, 'rev-parse', '--verify', '--end-of-options', rev + '^{commit}').stdout.decode().strip()
    files = git(root, 'ls-tree', '-r', '--name-only', '--full-tree', measured, '--', '.ufo/waves/').stdout.decode().splitlines()
    claims_files = sorted((f for f in files if CLAIMS.match(f)),
                          key=lambda f: int(CLAIMS.match(f).group(1).split('-')[1]))
    results = [audit_one(root, measured, f) for f in claims_files]
    by_round = {CLAIMS.match(r['claims_file']).group(1): r for r in results}
    failed = [r for r in require_clean if r not in by_round or by_round[r]['verdict'] != 'CLEAN']
    summary = {f: sum(1 for r in results for x in r['findings'] if x['finding'] == f)
               for f in ('INSTRUMENT_NONE', 'INSTRUMENT_ABSENT', 'INSTRUMENT_UNPINNED',
                         'INSTRUMENT_PIN_MISMATCH', 'INSTRUMENT_REVISED')}
    result = {'claim': 'R24-C2', 'rev': measured, 'audited': len(results),
              'clean': sum(r['verdict'] == 'CLEAN' for r in results),
              'flagged': [rnd for rnd, r in by_round.items() if r['verdict'] != 'CLEAN'],
              'summary': summary, 'required_clean': list(require_clean), 'required_failed': failed,
              'freezes': results}
    code = 1 if failed else 0
    if disclosures:
        rows = read_disclosures(root, measured, disclosures)
        expected = {rnd: (r['verdict'], ','.join(sorted({x['finding'] for x in r['findings']})) or '-')
                    for rnd, r in by_round.items()}
        rows = rows or {}
        exact = sorted(rnd for rnd, want in expected.items() if rows.get(rnd) == want)
        mismatched = sorted(rnd for rnd in expected if rnd in rows and rows[rnd] != expected[rnd])
        result['disclosures'] = {'path': disclosures, 'present': bool(rows), 'exact': len(exact),
                                 'of': len(expected), 'missing': sorted(set(expected) - set(rows)),
                                 'mismatched': mismatched, 'stray': sorted(set(rows) - set(expected))}
        if len(exact) != len(expected) or result['disclosures']['stray']:
            code = 1
    return result, code


def main():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1',
                      GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_COUNT='2',
                      GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
                      GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--require-clean', action='append', default=[], metavar='round-N')
    p.add_argument('--disclosures', metavar='LANE_PATH')
    a = p.parse_args()
    try:
        result, code = audit(a.root.resolve(), a.rev, a.require_clean, a.disclosures)
    except (OSError, ValueError, UnicodeError, KeyError, RecursionError, AttributeError) as error:
        result, code = {'claim': 'R24-C2', 'finding': 'unevaluable', 'error': str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
