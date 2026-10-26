#!/usr/bin/env python3
"""run-controls.py — format-validate every R40-C2 control and score it.

For each table file in this directory, under both available interpreters
(`sqfs-triage-v2-min.py`, this seat's minimal validator, and `../R40C2Interp/
sqfs-triage-v2.py` when the interpreter seat's artifact exists):

  1. `--skill FILE --table-only` -> exit code + first stderr line;
  2. when the file parses, classify the 26 synthetic class envelopes (envelopes/) and the
     17 committed round-39 envelopes, comparing (label, action) against the expectation.

Writes control-matrix.tsv (control x envelope, decisions of the PRIMARY interpreter, which
is the seat interpreter when present), control-summary.tsv and interp-agreement.tsv.
Exit 0 iff every control that is supposed to parse parses under every interpreter,
CTL-C2-0 exits 2 everywhere, the two interpreters agree on every scored cell, and the
candidate table (best-table.md) matches every expectation.
"""

import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ENV = os.path.join(HERE, 'envelopes')
REAL_INTERP = os.path.join(HERE, '..', 'R40C2Interp', 'sqfs-triage-v2.py')

INTERPS = [('min', os.path.join(HERE, 'sqfs-triage-v2-min.py'))]
if os.path.isfile(REAL_INTERP):
    INTERPS.append(('seat', os.path.abspath(REAL_INTERP)))

CONTROLS = ['CTL-C2-0.md', 'CTL-C2-1.md', 'CTL-C2-2.md', 'CTL-C2-3.md', 'CTL-C2-4.md',
            'CTL-C2-5.md', 'CTL-C2-6.md', 'best-table.md', 'probe-shadow.md']
MUST_PARSE = 'CTL-C2-0.md'      # the base SKILL must NOT parse: exit 2

REAL_EXPECT = {
    'round-39/c1/K1/after.json': ('escaping-symlink-removed', 'verify-link-absence'),
    'round-39/c1/K2/after.json': ('in-tree-symlink-metadata', 'count-metadata-gaps'),
    'round-39/c1/K3/after.json': ('clean', 'match-oracle'),
    'round-39/c1/K4/after.json': ('clean', 'match-oracle'),
    'round-39/c1/K5/after.json': ('mixed-symlinks', 'split-mixed-links'),
    'round-39/c1/K6/after.json': ('mixed-symlinks', 'split-mixed-links'),
    'R39C2AxisFit/env-avm.json': ('avm-marker-be-dropped', 'rerun-with-be'),
    'R39C2AxisFit/env-bodyflip.json': ('clean', 'match-oracle'),
    'R39C2AxisFit/env-bytesused.json': ('no-squashfs-chunk', 'probe-superblock'),
    'R39C2AxisFit/env-clean.json': ('clean', 'match-oracle'),
    'R39C2AxisFit/env-depbe.json': ('dep-missing-be', 'install-sasquatch-v4be'),
    'R39C2AxisFit/env-inodeptr.json': ('body-extractor-failure', 'preserve-failing-arm'),
    'R39C2AxisFit/env-magic.json': ('no-squashfs-chunk', 'probe-superblock'),
    'R39C2AxisFit/env-rootino.json': ('body-extractor-failure', 'preserve-failing-arm'),
    'R39C2AxisFit/env-sym.json': ('mixed-symlinks', 'split-mixed-links'),
    'R39C2AxisFit/env-trunc.json': ('no-squashfs-chunk', 'probe-superblock'),
    'R39C2AxisFit/env-zeroed.json': ('clean', 'match-oracle'),
}


def synth_cases():
    cases = []
    with open(os.path.join(ENV, 'expected.tsv'), 'r', encoding='utf-8') as handle:
        next(handle)
        for line in handle:
            cls, rep, rel, label, action = line.rstrip('\n').split('\t')
            cases.append({'corpus': 'synthetic', 'class': cls, 'rep': rep,
                          'path': os.path.join(HERE, rel), 'name': '%s/%s' % (cls, rep),
                          'label': label, 'action': action})
    return cases


def real_cases():
    cases = []
    for rel, (label, action) in REAL_EXPECT.items():
        if rel.startswith('round-39/'):
            path = os.path.join(LANE, 'corpus/evidence', rel)
        else:
            path = os.path.join(LANE, '.ufo/waves/round-39/w1/artifacts', rel)
        group = ('real:round-39-core' if rel.startswith('round-39/')
                 else 'real:dev-envelope')
        cases.append({'corpus': 'real', 'class': group, 'rep': '-',
                      'path': path, 'name': rel, 'label': label, 'action': action})
    return cases


def table_only(tool, skill):
    res = subprocess.run([sys.executable, '-I', '-B', tool, '--skill', skill,
                          '--table-only'], capture_output=True, text=True)
    first = (res.stderr.strip().splitlines() or [''])[0]
    return res.returncode, first


def classify(tool, skill, paths):
    res = subprocess.run([sys.executable, '-I', '-B', tool, '--skill', skill, '--json',
                          *paths], capture_output=True, text=True)
    if res.returncode != 0:
        return None, (res.stderr.strip().splitlines() or [''])[0]
    payload = json.loads(res.stdout)
    return {(r['label'], r['action']) for r in payload['results']}, None


def decisions(tool, skill, paths):
    res = subprocess.run([sys.executable, '-I', '-B', tool, '--skill', skill, '--json',
                          *paths], capture_output=True, text=True)
    if res.returncode != 0:
        return None, (res.stderr.strip().splitlines() or [''])[0]
    payload = json.loads(res.stdout)
    return [(r['label'], r['action']) for r in payload['results']], None


def main():
    cases = synth_cases() + real_cases()
    paths = [c['path'] for c in cases]
    primary_name, primary_tool = INTERPS[-1]
    matrix = []
    agreement = []
    summary = []
    failures = []
    for name in CONTROLS:
        skill = os.path.join(HERE, name)
        entry = {'control': name}
        per_interp = {}
        for label, tool in INTERPS:
            code, err = table_only(tool, skill)
            per_interp[label] = {'exit': code, 'stderr': err}
            if code != 0 and name != MUST_PARSE:
                failures.append('%s under %s: expected exit 0, got %d (%s)'
                                % (name, label, code, err))
            if code == 0 and name == MUST_PARSE:
                failures.append('%s under %s: expected exit 2, got 0' % (name, label))
            if code == 0:
                got, cerr = decisions(tool, skill, paths)
                if got is None:
                    failures.append('%s under %s: classify failed (%s)'
                                    % (name, label, cerr))
            else:
                got = None
            per_interp[label]['decisions'] = got
        entry['exits'] = '|'.join('%s=%d' % (label, per_interp[label]['exit'])
                                 for label, _ in INTERPS)
        entry['stderr'] = ' | '.join(
            '%s: %s' % (label, per_interp[label]['stderr'].split(': ', 1)[-1])
            for label, _ in INTERPS if per_interp[label]['stderr']) or '-'
        if len(INTERPS) == 2:
            a = per_interp['min']['decisions']
            b = per_interp['seat']['decisions']
            if a is not None and b is not None:
                for case, da, db in zip(cases, a, b):
                    agreement.append({'control': name, 'case': case['name'],
                                      'min': '%s/%s' % da, 'seat': '%s/%s' % db,
                                      'agree': da == db})
            elif a is not None or b is not None:
                agreement.append({'control': name, 'case': '(table unparseable)',
                                  'min': a is not None, 'seat': b is not None,
                                  'agree': False})
        got = per_interp[primary_name]['decisions']
        if got is None:
            entry['envelopes'] = 'not scored'
            entry['wrong_classes'] = 'all (table unparseable)'
            entry['wrong_count'] = len(cases)
        else:
            wrong = []
            for case, decision in zip(cases, got):
                ok = decision == (case['label'], case['action'])
                matrix.append({'control': name, 'corpus': case['corpus'],
                               'case': case['name'],
                               'expected': '%s/%s' % (case['label'], case['action']),
                               'got': '%s/%s' % decision,
                               'ok': 'ok' if ok else 'WRONG'})
                if not ok:
                    wrong.append(case)
            entry['envelopes'] = '%d/%d' % (len(cases) - len(wrong), len(cases))
            classes = []
            for case in wrong:
                if case['class'] not in classes:
                    classes.append(case['class'])
            entry['wrong_classes'] = ','.join(classes) if classes else '-'
            entry['wrong_count'] = len(wrong)
            if name == 'best-table.md' and wrong:
                failures.append('best-table.md: %d wrong envelopes (%s)'
                                % (len(wrong), entry['wrong_classes']))
        summary.append(entry)
    for row in agreement:
        if not row['agree']:
            failures.append('interpreters disagree: %s on %s (%s vs %s)'
                            % (row['control'], row['case'], row['min'], row['seat']))
    with open(os.path.join(HERE, 'control-matrix.tsv'), 'w', encoding='utf-8') as handle:
        handle.write('control\tcorpus\tcase\texpected\tgot\tverdict\n')
        for row in matrix:
            handle.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (row['control'], row['corpus'],
                                                       row['case'], row['expected'],
                                                       row['got'], row['ok']))
    with open(os.path.join(HERE, 'interp-agreement.tsv'), 'w',
              encoding='utf-8') as handle:
        handle.write('control\tcase\tmin\tseat\tagree\n')
        for row in agreement:
            handle.write('%s\t%s\t%s\t%s\t%s\n'
                         % (row['control'], row['case'], row['min'], row['seat'],
                            'yes' if row['agree'] else 'NO'))
    with open(os.path.join(HERE, 'control-summary.tsv'), 'w', encoding='utf-8') as handle:
        handle.write('control\ttable_only_exit\tenvelopes_ok\twrong_classes\t'
                     'wrong_count\tstderr\n')
        for row in summary:
            handle.write('%s\t%s\t%s\t%s\t%s\t%s\n'
                         % (row['control'], row['exits'], row['envelopes'],
                            row['wrong_classes'], row['wrong_count'], row['stderr']))
    print('primary interpreter: %s (%s)' % (primary_name, primary_tool))
    for row in summary:
        print('%-16s exit=%-11s envelopes_ok=%-8s wrong=%-2s %s'
              % (row['control'], row['exits'], row['envelopes'], row['wrong_count'],
                 row['wrong_classes']))
    if failures:
        print('FAILURES:')
        for line in failures:
            print('  ' + line)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
