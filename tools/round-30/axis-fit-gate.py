#!/usr/bin/env python3
"""Round-30 axis-fit gate: the fix for mistake M30-1 (an axis-misfit claim).

M30-1 (from the round-29 outside rejection): a round froze a claim under the
axis `coverage` (or `depth`) whose frozen text named no surface and no command
that would move when the surface moved, so the label could not be checked; and
the wave's pre-data controls were not committed before its data.

This gate reads Git objects only (never the worktree) and, per round at a
revision, checks:

  surface    every claim whose axis begins with `coverage` or `depth` (the
             round-29 axes read `coverage (learning claim: ...)`) carries a
             nonempty `surface` string and a nonempty `unmoved_command` string.
  controls   when at least one such claim exists, the round holds a committed
             `.ufo/waves/round-<N>/controls/receipts.tsv` at the revision
             (header `claim<TAB>control<TAB>counter_exit<TAB>met_target`)
             whose first adding commit is strictly earlier (committer
             timestamp) than the first commit adding any path under
             `corpus/evidence/round-<N>/<claim-dir>/envelopes/`; every listed
             row has met_target `no`; and every control named in the claims
             file's `controls_required_before_data` is present in the receipts
             for each such claim. A receipt control cell satisfies a frozen
             name when the two are equal, or when the cell equals the frozen
             name's text before the first ` (` (its short id) and that head
             names exactly one frozen control.

Exit 0 when every requirement holds, 1 when one fails (every finding is
printed), 2 when the input cannot be evaluated (claims file absent or
unparsable, git failure, --root not a repository top, receipts present but its
adding commit not in the walked history).

Usage:
  axis-fit-gate.py --root <lane> --round <N> [--rev <rev>]     (default rev HEAD)
  axis-fit-gate.py --selftest

--selftest builds red and green fixture repositories under TMPDIR (fixed
committer dates, so the ordering is deterministic) and runs this file against
each as a subprocess; it prints one line per case and exits 0 only when every
case matches its expected exit code and findings.

Limits: commit timestamps and authorship are not authenticated; the ordering
check uses committer timestamps and additionally reports whether the receipts
commit is an ancestor of the first envelope commit; a control named only in
prose outside the claims file is not seen; the receipts file is checked for its
shape and the clauses above, not for the truth of the control it records; the
envelope pattern is exactly one directory segment between `round-<N>/` and
`envelopes/`.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

AXIS = re.compile(r'^(coverage|depth)\b')
RECEIPTS_HEADER = ['claim', 'control', 'counter_exit', 'met_target']
ROUND_RE = re.compile(r'(?:round-)?(\d+)')
T0 = '2026-01-01T00:00:00 +0000'
T1 = '2026-01-01T00:01:00 +0000'


def scrub_git_env():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ.update(GIT_NO_REPLACE_OBJECTS='1', GIT_CONFIG_NOSYSTEM='1',
                      GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_COUNT='2',
                      GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
                      GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null')


def git(root, *args, ok=(0,)):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
    if p.returncode not in ok:
        raise ValueError('git_failed: ' + ' '.join(args[:3]))
    return p


def show(root, rev, path):
    """Blob text at rev:path, or None when the path is not a blob there."""
    if git(root, 'cat-file', '-e', f'{rev}:{path}', ok=(0, 1, 128)).returncode:
        return None
    if git(root, 'cat-file', '-t', f'{rev}:{path}').stdout.strip() != b'blob':
        return None
    return git(root, 'show', f'{rev}:{path}').stdout.decode('utf-8', 'replace')


def first_add(root, rev, path):
    """(commit, committer_ct) of the first commit in rev's history that added path."""
    lines = [l for l in git(root, 'log', '--format=%H %ct', '--diff-filter=A', rev,
                            '--', path).stdout.decode().splitlines() if l.strip()]
    if not lines:
        return None
    commit, ct = lines[-1].split()
    return commit, int(ct)


def first_envelope_add(root, rev, round_no):
    """(commit, committer_ct, path) of the first commit in rev's history that added
    any path under corpus/evidence/round-<N>/<one segment>/envelopes/."""
    prefix = 'corpus/evidence/round-%d/' % round_no
    out = git(root, 'log', '--format=%x00%H %ct', '--name-only', '--diff-filter=A',
              rev).stdout.decode('utf-8', 'replace')
    head = None
    found = None
    for line in out.splitlines():
        if line.startswith('\x00'):
            cells = line[1:].split()
            head = (cells[0], int(cells[1])) if len(cells) == 2 else None
            continue
        path = line.strip()
        if not head or not path.startswith(prefix):
            continue
        rest = path[len(prefix):].split('/')
        if len(rest) >= 3 and rest[1] == 'envelopes':
            # walk order is newest-first: keep overwriting so the oldest adding
            # commit wins, and inside one commit keep its first path in diff order
            if found is None or found[0] != head[0]:
                found = (head[0], head[1], path)
    return found


def field_state(claim, key):
    if key not in claim or not isinstance(claim[key], str):
        return 'missing'
    return 'ok' if claim[key].strip() else 'empty'


def control_head(name):
    return name.split(' (', 1)[0].strip()


def parse_receipts(text):
    """(rows, findings) for the receipts table text."""
    lines = text.splitlines()
    if not lines or lines[0].split('\t') != RECEIPTS_HEADER:
        return [], [{'finding': 'RECEIPTS_HEADER_INVALID',
                     'header': lines[0][:120] if lines else ''}]
    rows, findings = [], []
    for n, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        cells = line.split('\t')
        if len(cells) != 4 or not cells[0].strip() or not cells[1].strip():
            findings.append({'finding': 'RECEIPTS_ROW_INVALID', 'line': n, 'text': line[:120]})
            continue
        claim, control, counter_exit, met_target = (c.strip() for c in cells)
        try:
            exit_code = int(counter_exit)
        except ValueError:
            findings.append({'finding': 'RECEIPTS_ROW_INVALID', 'line': n,
                             'why': 'counter_exit not an integer', 'text': line[:120]})
            continue
        rows.append({'line': n, 'claim': claim, 'control': control,
                     'counter_exit': exit_code, 'met_target': met_target})
        if met_target.lower() != 'no':
            findings.append({'finding': 'MET_TARGET_YES' if met_target.lower() == 'yes'
                             else 'MET_TARGET_INVALID',
                             'line': n, 'claim': claim, 'control': control,
                             'met_target': met_target})
    return rows, findings


def controls_for(required, rows, claim_id):
    """frozen control name -> 'exact' | 'head' | None for one claim."""
    cells = {(r['claim'], r['control']) for r in rows}
    heads = {}
    for name in required:
        heads.setdefault(control_head(name), []).append(name)
    present = {}
    for name in required:
        head = control_head(name)
        if (claim_id, name) in cells:
            present[name] = 'exact'
        elif len(heads[head]) == 1 and (claim_id, head) in cells:
            present[name] = 'head'
        else:
            present[name] = None
    return present


def round_number(value):
    m = ROUND_RE.fullmatch(str(value).strip())
    if not m:
        raise ValueError('round_invalid: ' + str(value))
    return int(m.group(1))


def audit(root, round_no, rev):
    if git(root, 'rev-parse', '--show-prefix').stdout.strip():
        raise ValueError('root_not_repository_top')
    measured = git(root, 'rev-parse', '--verify', '--end-of-options',
                   rev + '^{commit}').stdout.decode().strip()
    claims_path = '.ufo/waves/round-%d/claims.json' % round_no
    text = show(root, measured, claims_path)
    if text is None:
        raise ValueError('claims_absent: ' + claims_path)
    try:
        doc = json.loads(text)
    except ValueError as error:
        raise ValueError('claims_invalid: %s' % error)
    if not isinstance(doc, dict) or not isinstance(doc.get('claims'), list):
        raise ValueError('claims_invalid: no claims list')
    findings, notes, axis_entries = [], [], []
    for i, claim in enumerate(doc['claims']):
        if not isinstance(claim, dict):
            findings.append({'finding': 'CLAIM_INVALID', 'index': i})
            continue
        axis = claim.get('axis')
        if not isinstance(axis, str) or not AXIS.match(axis.strip()):
            continue
        cid = claim.get('id') if isinstance(claim.get('id'), str) and claim['id'].strip() \
            else 'claim[%d]' % i
        entry = {'claim': cid, 'axis': axis.strip(),
                 'surface': field_state(claim, 'surface'),
                 'unmoved_command': field_state(claim, 'unmoved_command')}
        axis_entries.append(entry)
        for key, code in (('surface', 'SURFACE'), ('unmoved_command', 'UNMOVED_COMMAND')):
            if entry[key] != 'ok':
                findings.append({'finding': '%s_%s' % (code, entry[key].upper()),
                                 'claim': cid})
    required = doc.get('controls_required_before_data')
    controls = []
    if required is None:
        notes.append('controls_required_before_data absent: no control is named')
    elif not isinstance(required, list) or \
            not all(isinstance(x, str) and x.strip() for x in required):
        findings.append({'finding': 'CONTROLS_LIST_INVALID'})
    else:
        controls = [x.strip() for x in required]
    receipts_path = '.ufo/waves/round-%d/controls/receipts.tsv' % round_no
    receipts = {'path': receipts_path, 'present': False}
    if axis_entries:
        rtext = show(root, measured, receipts_path)
        if rtext is None:
            findings.append({'finding': 'RECEIPTS_ABSENT', 'path': receipts_path})
        else:
            receipts['present'] = True
            rows, rfindings = parse_receipts(rtext)
            findings += rfindings
            receipts['rows'] = len(rows)
            r_add = first_add(root, measured, receipts_path)
            if r_add is None:
                raise ValueError('receipts_add_unknown: ' + receipts_path)
            receipts['first_add'] = {'commit': r_add[0], 'committer_ct': r_add[1]}
            e_add = first_envelope_add(root, measured, round_no)
            if e_add is None:
                receipts['ordering'] = 'no-envelopes'
                receipts['first_envelope_add'] = None
                notes.append('no envelope path is committed yet: the ordering clause is vacuous')
            else:
                receipts['first_envelope_add'] = {'commit': e_add[0], 'committer_ct': e_add[1],
                                                  'path': e_add[2]}
                ancestor = git(root, 'merge-base', '--is-ancestor', r_add[0], e_add[0],
                               ok=(0, 1)).returncode == 0
                receipts['ancestor_of_first_envelope'] = ancestor
                if r_add[1] < e_add[1]:
                    receipts['ordering'] = 'earlier'
                    if not ancestor and r_add[0] != e_add[0]:
                        notes.append('receipts commit is not an ancestor of the first envelope '
                                     'commit; ordered by committer timestamp only')
                else:
                    receipts['ordering'] = 'not-earlier'
                    findings.append({'finding': 'RECEIPTS_NOT_BEFORE_ENVELOPES',
                                     'receipts': {'commit': r_add[0], 'committer_ct': r_add[1]},
                                     'envelopes': {'commit': e_add[0], 'committer_ct': e_add[1],
                                                   'path': e_add[2]}})
            seen = {}
            for row in rows:
                key = (row['claim'], row['control'])
                seen[key] = seen.get(key, 0) + 1
                if row['counter_exit'] == 0 and row['met_target'].lower() == 'no':
                    notes.append('row %d: counter_exit 0 with met_target no' % row['line'])
            if any(v > 1 for v in seen.values()):
                notes.append('duplicate claim/control rows: %d' % sum(1 for v in seen.values() if v > 1))
            known = {e['claim'] for e in axis_entries}
            extra = sorted({r['claim'] for r in rows} - known)
            if extra:
                notes.append('receipt rows for claims not on coverage/depth: %s' % ','.join(extra))
            for entry in axis_entries:
                present = controls_for(controls, rows, entry['claim'])
                entry['controls_present'] = present
                for name, how in present.items():
                    if how is None:
                        findings.append({'finding': 'CONTROL_MISSING', 'claim': entry['claim'],
                                         'control': name})
    result = {'claim': 'R30-axis-fit-gate', 'round': round_no, 'rev': measured,
              'claims_file': claims_path, 'axis_claims': axis_entries,
              'required_controls': controls, 'receipts': receipts,
              'findings': findings, 'notes': notes,
              'verdict': 'PASS' if not findings else 'FAIL'}
    return result, (0 if not findings else 1)


def _g(root, *args, env=None):
    base = dict(os.environ)
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE'):
        base.pop(key, None)
    base.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    if env:
        base.update(env)
    p = subprocess.run(['git', '-C', str(root), '-c', 'user.name=ctl',
                        '-c', 'user.email=ctl@sandbox', *args], capture_output=True,
                       env=base, check=False)
    if p.returncode:
        raise RuntimeError('fixture git failed: %s: %s'
                           % (' '.join(args[:2]), p.stderr.decode()[:200]))
    return p


def _commit(repo, when, message, files):
    for rel, text in files.items():
        full = os.path.join(repo, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w') as handle:
            handle.write(text)
    _g(repo, 'add', '-A')
    _g(repo, 'commit', '-q', '-m', message,
       env={'GIT_AUTHOR_DATE': when, 'GIT_COMMITTER_DATE': when})


def _claims(claims, controls=None):
    doc = {'round': 99, 'claims': claims}
    if controls is not None:
        doc['controls_required_before_data'] = controls
    return json.dumps(doc, indent=1) + '\n'


def _claim(cid, axis, **kw):
    claim = {'id': cid, 'axis': axis}
    claim.update(kw)
    return claim


GOOD = _claim('R99-C1', 'coverage', surface='PROVINCE gains x',
              unmoved_command='git show <REV>:PROVINCE.md | grep -c x')
GOOD2 = _claim('R99-C2', 'depth (learning claim: y)', surface='SKILL gains z',
               unmoved_command='git show <REV>:SKILL.md | grep -c z')
CONTROLS = ['do-nothing', 'junk-row (entry without envelopes)']
RECEIPTS_OK = ('claim\tcontrol\tcounter_exit\tmet_target\n'
               'R99-C1\tdo-nothing\t2\tno\n'
               'R99-C1\tjunk-row\t1\tno\n'
               'R99-C2\tdo-nothing\t2\tno\n'
               'R99-C2\tjunk-row (entry without envelopes)\t1\tno\n')
ENVELOPE = 'corpus/evidence/round-99/c1/envelopes/e1.json'


def _receipts(rows):
    return ('claim\tcontrol\tcounter_exit\tmet_target\n'
            + ''.join('\t'.join(str(c) for c in r) + '\n' for r in rows))


def _case(base, name, commits, want_exit, want_findings, want_error=None, plain=False):
    repo = os.path.join(base, name)
    os.makedirs(repo)
    if not plain:
        _g(repo, 'init', '-q', '-b', 'main')
    for i, (when, files) in enumerate(commits):
        _commit(repo, when, 'c%d' % i, files)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.abspath(__file__),
                        '--root', repo, '--round', '99', '--rev', 'main'],
                       capture_output=True, check=False)
    stdout = p.stdout.decode()
    codes = []
    try:
        got = json.loads(stdout)
        codes = sorted({f['finding'] for f in got.get('findings', [])
                        if isinstance(f, dict) and 'finding' in f})
    except ValueError:
        pass
    if want_error is not None:
        ok = p.returncode == want_exit and want_error in stdout
    else:
        ok = p.returncode == want_exit and sorted(want_findings) == codes
    print('%s %s exit=%d findings=%s%s' % ('ok' if ok else 'FAIL', name, p.returncode,
                                           ','.join(codes) or '-',
                                           '' if ok else ' want_exit=%d want=%s'
                                           % (want_exit, want_error or ','.join(want_findings) or '-')))
    if not ok:
        print('  stdout: ' + stdout.strip()[:400])
    return ok


def selftest():
    base = tempfile.mkdtemp(prefix='axis-fit-gate-selftest-')
    green = _claims([GOOD, GOOD2], CONTROLS)
    cases = [
        ('green-basic', [(T0, {'.ufo/waves/round-99/claims.json': green,
                               '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK}),
                         (T1, {ENVELOPE: '{}\n'})], 0, [], None),
        ('green-pre-data-no-envelopes', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                               '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK})],
         0, [], None),
        ('green-other-axis-only', [(T0, {'.ufo/waves/round-99/claims.json':
                                         _claims([_claim('R99-C3', 'calibration', statement='x')])})],
         0, [], None),
        ('red-surface-missing', [(T0, {'.ufo/waves/round-99/claims.json':
                                       _claims([_claim('R99-C1', 'coverage',
                                                       unmoved_command='grep -c x'), GOOD2], CONTROLS),
                                       '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK}),
                                 (T1, {ENVELOPE: '{}\n'})], 1, ['SURFACE_MISSING'], None),
        ('red-surface-blank', [(T0, {'.ufo/waves/round-99/claims.json':
                                     _claims([_claim('R99-C1', 'coverage', surface='   ',
                                                     unmoved_command='grep -c x'), GOOD2], CONTROLS),
                                     '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK})],
         1, ['SURFACE_EMPTY'], None),
        ('red-unmoved-missing', [(T0, {'.ufo/waves/round-99/claims.json':
                                       _claims([_claim('R99-C1', 'coverage', surface='PROVINCE x'),
                                                GOOD2], CONTROLS),
                                       '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK})],
         1, ['UNMOVED_COMMAND_MISSING'], None),
        ('red-receipts-absent', [(T0, {'.ufo/waves/round-99/claims.json': green}),
                                 (T1, {ENVELOPE: '{}\n'})], 1, ['RECEIPTS_ABSENT'], None),
        ('red-receipts-after-envelopes', [(T0, {ENVELOPE: '{}\n'}),
                                          (T1, {'.ufo/waves/round-99/claims.json': green,
                                                '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK})],
         1, ['RECEIPTS_NOT_BEFORE_ENVELOPES'], None),
        ('red-receipts-same-commit', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                            '.ufo/waves/round-99/controls/receipts.tsv': RECEIPTS_OK,
                                            ENVELOPE: '{}\n'})],
         1, ['RECEIPTS_NOT_BEFORE_ENVELOPES'], None),
        ('red-met-target-yes', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                      '.ufo/waves/round-99/controls/receipts.tsv':
                                      _receipts([['R99-C1', 'do-nothing', 2, 'no'],
                                                 ['R99-C1', 'junk-row', 0, 'yes'],
                                                 ['R99-C2', 'do-nothing', 2, 'no'],
                                                 ['R99-C2', 'junk-row (entry without envelopes)', 1, 'no']])})],
         1, ['MET_TARGET_YES'], None),
        ('red-control-missing', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                       '.ufo/waves/round-99/controls/receipts.tsv':
                                       _receipts([['R99-C1', 'do-nothing', 2, 'no'],
                                                  ['R99-C1', 'junk-row', 1, 'no'],
                                                  ['R99-C2', 'do-nothing', 2, 'no']])})],
         1, ['CONTROL_MISSING'], None),
        ('red-control-head-ambiguous', [(T0, {'.ufo/waves/round-99/claims.json':
                                              _claims([GOOD], ['dup (a)', 'dup (b)']),
                                              '.ufo/waves/round-99/controls/receipts.tsv':
                                              _receipts([['R99-C1', 'dup', 1, 'no']])})],
         1, ['CONTROL_MISSING'], None),
        ('red-header-invalid', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                      '.ufo/waves/round-99/controls/receipts.tsv':
                                      'claim\tcontrol\texit\tmet_target\n'})],
         1, ['RECEIPTS_HEADER_INVALID', 'CONTROL_MISSING'], None),
        ('red-row-invalid', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                   '.ufo/waves/round-99/controls/receipts.tsv':
                                   RECEIPTS_OK + 'R99-C1\tdo-nothing\t2\n'})],
         1, ['RECEIPTS_ROW_INVALID'], None),
        ('red-counter-exit-not-int', [(T0, {'.ufo/waves/round-99/claims.json': green,
                                            '.ufo/waves/round-99/controls/receipts.tsv':
                                            RECEIPTS_OK + 'R99-C1\tdo-nothing\tx\tno\n'})],
         1, ['RECEIPTS_ROW_INVALID'], None),
        ('red-claims-absent', [(T0, {'README': 'nothing here\n'})], 2, [], 'claims_absent'),
        ('red-claims-invalid-json', [(T0, {'.ufo/waves/round-99/claims.json': '{"claims": ['})],
         2, [], 'claims_invalid'),
        ('red-not-a-repo', [], 2, [], 'git_failed', True),
    ]
    failures = 0
    for case in cases:
        name, commits, want_exit, want_findings, want_error = case[:5]
        plain = len(case) > 5 and case[5]
        failures += not _case(base, name, commits, want_exit, want_findings, want_error, plain)
    print('selftest cases=%d failures=%d' % (len(cases), failures))
    return 0 if failures == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', type=Path)
    ap.add_argument('--round', dest='round_no')
    ap.add_argument('--rev', default='HEAD')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    scrub_git_env()
    if a.selftest:
        return selftest()
    if a.root is None or a.round_no is None:
        ap.error('--root and --round are required')
    try:
        result, code = audit(a.root.resolve(), round_number(a.round_no), a.rev)
    except (OSError, ValueError, UnicodeError, KeyError, RecursionError, AttributeError) as error:
        result, code = {'claim': 'R30-axis-fit-gate', 'round': str(a.round_no),
                        'finding': 'unevaluable', 'error': str(error)}, 2
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
