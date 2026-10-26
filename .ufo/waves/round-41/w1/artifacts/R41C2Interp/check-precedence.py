#!/usr/bin/env python3
"""check-precedence.py - does the drafted v3 table agree with the claims' precedence text?

The oracle in this file is written from ONE surface: the numbered ``**Label precedence**``
list of ``plans/round-41-claims.md`` (steps 1-12), read as prose.  It never reads the
drafted table's rows, never reads an interpreter constant, and never reads the round-40
independent evaluator.  It maps a feature tuple

    OP operation, PR provider, H handler set, G gap-kind set, D dependency set,
    BE -be in a recorded child argv (yes/no/n/a), SR symlink removed (yes/no),
    P published regular files

to ``(label, action, step)``.  The precedence text fixes the LABELS and the ordering; it
says nothing about actions, so the action of each label is taken from the committed
round-40 label map (``corpus/evidence/round-40/c2/heldout/manifest.json``
``label_actions``) plus the action the round-41 claims name for the new label
(``depth-limited-nested`` -> ``raise-depth``).  Those twelve-plus-one pairs are the only
non-precedence input, and each one is printed with the run so a reader can audit it.

The comparison drives the real interpreter: one REA envelope is written per feature tuple
(it encodes exactly the tuple's features and nothing else), ``sqfs-triage-v3.py --skill
<table> --json`` labels a batch of them, and every ``(label, action)`` is compared with
the oracle's.  Divergences are printed and matched against the two grammar limits the
draft already documents; any OTHER divergence exits 1.

Usage
  python3 -I -B check-precedence.py [--table T.md] [--interp I.py] [--work DIR]
                                    [--ledger OUT.tsv] [--batch 400] [--examples 3]
                                    [--reachable]
"""

import argparse
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TABLE = os.path.join(HERE, 'sqfs-triage-v3-table.md')
DEFAULT_INTERP = os.path.join(HERE, 'sqfs-triage-v3.py')

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
ROUND40_MANIFEST = LANE + '/corpus/evidence/round-40/c2/heldout/manifest.json'

UNCLASSIFIED = 'unclassified'
NO_ACTION = 'none'

# ---------------------------------------------------------------------------- the domains

OPS = ('extract_firmware', 'inspect_firmware_regions')
PVS = ('unblob', 'binwalk')
HS = ((), ('squashfs_v4_le',), ('squashfs_v4_be',), ('squashfs_v3',),
      ('squashfs_v4_le', 'squashfs_v4_be'))
GS = ((), ('extractor-failure',), ('unpublished-entry',), ('depth-limited',),
      ('missing-extractor-dependency',),
      ('extractor-failure', 'unpublished-entry'),
      ('depth-limited', 'unpublished-entry'),
      ('depth-limited', 'extractor-failure'),
      ('missing-extractor-dependency', 'extractor-failure'),
      ('missing-extractor-dependency', 'depth-limited'),
      ('mystery-gap',), ('unpublished-entry', 'mystery-gap'))
DS = ((), ('sasquatch',), ('sasquatch-v4be',), ('sasquatch', 'sasquatch-v4be'))
BES = ('yes', 'no', 'n/a')
SRS = ('yes', 'no')
PS = (0, 3)

# the only non-precedence input: label -> action, from the committed round-40 map plus the
# round-41 claim's named new action for depth-limited-nested.
LABEL_ACTIONS = {
    'clean': 'none',
    'clean-empty': 'confirm-empty',
    'escaping-symlink-removed': 'expect-link-absent',
    'in-tree-symlink-metadata': 'count-gap',
    'mixed-symlinks': 'audit-symlinks',
    'dep-missing-be': 'install-extractor-be',
    'dep-missing-le': 'install-extractor-le',
    'avm-marker-be-dropped': 'wrap-extractor-be',
    'body-extractor-failure': 'preserve-failure',
    'partial-body-failure': 'salvage-partial',
    'no-squashfs-chunk': 'inspect-input',
    'depth-limited-nested': 'raise-depth',
    UNCLASSIFIED: NO_ACTION,
}


def oracle(op, pv, handlers, gaps, deps, be, sr, published):
    """The **Label precedence** list of plans/round-41-claims.md, step by step.

    Returns (label, action, step).  Step 3's text has no else branch: when the gap kind is
    present but no dependency names either sasquatch binary, evaluation continues at step 4
    (recorded as the one ambiguity of the text; the alternative - a dep-missing label with no
    binary to install - would be unactionable).
    """
    if op != 'extract_firmware' or pv != 'unblob':
        return UNCLASSIFIED, NO_ACTION, 1
    if not any(handler.startswith('squashfs_v4_') for handler in handlers):
        return 'no-squashfs-chunk', LABEL_ACTIONS['no-squashfs-chunk'], 2
    if 'missing-extractor-dependency' in gaps:
        if 'sasquatch-v4be' in deps:
            return 'dep-missing-be', LABEL_ACTIONS['dep-missing-be'], 3
        if 'sasquatch' in deps:
            return 'dep-missing-le', LABEL_ACTIONS['dep-missing-le'], 3
    if 'extractor-failure' in gaps and published > 0:
        return 'partial-body-failure', LABEL_ACTIONS['partial-body-failure'], 4
    if ('extractor-failure' in gaps and published == 0 and be == 'no'
            and 'squashfs_v4_be' in handlers):
        return ('avm-marker-be-dropped', LABEL_ACTIONS['avm-marker-be-dropped'], 5)
    if 'extractor-failure' in gaps and published == 0:
        return 'body-extractor-failure', LABEL_ACTIONS['body-extractor-failure'], 6
    if 'depth-limited' in gaps:
        return 'depth-limited-nested', LABEL_ACTIONS['depth-limited-nested'], 7
    if sr == 'yes' and 'unpublished-entry' in gaps:
        return 'mixed-symlinks', LABEL_ACTIONS['mixed-symlinks'], 8
    if sr == 'yes' and not gaps:
        return 'escaping-symlink-removed', LABEL_ACTIONS['escaping-symlink-removed'], 9
    if gaps == frozenset({'unpublished-entry'}) or gaps == ('unpublished-entry',):
        return 'in-tree-symlink-metadata', LABEL_ACTIONS['in-tree-symlink-metadata'], 10
    if not gaps and published > 0:
        return 'clean', LABEL_ACTIONS['clean'], 11
    if not gaps and published == 0:
        return 'clean-empty', LABEL_ACTIONS['clean-empty'], 11
    return UNCLASSIFIED, NO_ACTION, 12


# ------------------------------------------------------------------------- features -> wire

def envelope(op, pv, handlers, gaps, deps, be, sr, published):
    """One REA ``data`` object whose extracted features are exactly the tuple."""
    chunks = [{'handler': handler, 'depth': 0} for handler in handlers]
    gaps_out = []
    for index, kind in enumerate(gaps):
        gaps_out.append({'kind': kind,
                         'dependencies': list(deps) if index == 0 else []})
    if not gaps and deps:
        gaps_out.append({'dependencies': list(deps)})
    diagnostics = []
    if be != 'n/a':
        argv = ['/usr/local/bin/sasquatch-v4be']
        if be == 'yes':
            argv.append('-be')
        argv.extend(['-d', '/out', '/in'])
        diagnostics.append({'report': {'command': argv, '__typename__':
                                       'CommandReport'}})
    data = {
        'operation': op,
        'provider': {'id': pv, 'name': pv, 'version': '0.0'},
        'normalized_result': {
            'chunks': chunks,
            'extraction_gaps': gaps_out,
            'diagnostics': diagnostics,
            'files': [{'relative_path': 'f/%03d.bin' % n, 'size': 1}
                      for n in range(published)],
        },
    }
    if sr == 'yes':
        data['raw_result'] = {'report': [{'reports': [{'__typename__':
                                                       'MaliciousSymlinkRemoved',
                                                       'severity': 'WARNING'}]}]}
    return data


def tuples(reachable=False):
    for op, pv, hs, gs, ds, be, sr, p in itertools.product(OPS, PVS, HS, GS, DS, BES, SRS,
                                                           PS):
        if reachable and ds and 'missing-extractor-dependency' not in gs:
            # unblob records dependencies ON a gap, so a dependency with no dependency gap
            # cannot come out of a real envelope; skip it in the reachable domain.
            continue
        yield {'OP': op, 'PV': pv, 'H': hs, 'G': gs, 'D': ds, 'BE': be, 'SR': sr,
               'P': p}


# ------------------------------------------------------------------------------- divergence

KNOWN = (
    ('K1-non-v4-handler',
     'H holds a squashfs handler that is not squashfs_v4_* (e.g. squashfs_v3): precedence '
     'step 2 labels it no-squashfs-chunk, but a handler cell can only say "no squashfs '
     'handler at all" (none) or match a pattern, so the draft table returns unclassified. '
     'Outside the held-out envelope domain.'),
    ('K2-dependency-names-both',
     'the missing-extractor-dependency gap names BOTH sasquatch and sasquatch-v4be: '
     'precedence step 3 tests sasquatch-v4be first and labels dep-missing-be, but the '
     'dependencies cell keeps the v2 exact-set form (the seat brief extends CONTAINS to gap '
     'kinds only), so no dependency row matches and the table falls through to whichever '
     'later row the other gaps match - unclassified when the dependency gap is alone, '
     'partial-body-failure / body-extractor-failure / depth-limited-nested when it carries '
     'one of those kinds. Outside the held-out envelope domain (the generator puts one '
     'dependency name on a gap).'),
)


def known_divergence(tup, oracle_label, table_label):
    if oracle_label == table_label:
        return None
    if (tup['OP'] == 'extract_firmware' and tup['PV'] == 'unblob'
            and tup['H'] and not any(h.startswith('squashfs_v4_') for h in tup['H'])
            and oracle_label == 'no-squashfs-chunk' and table_label == UNCLASSIFIED):
        return 'K1-non-v4-handler'
    if ('missing-extractor-dependency' in tup['G']
            and {'sasquatch', 'sasquatch-v4be'} <= set(tup['D'])
            and oracle_label == 'dep-missing-be'):
        return 'K2-dependency-names-both'
    return None


# ------------------------------------------------------------------------------------- cli

def _fmt_set(values):
    return '{}' .format('|'.join(values)) if values else '{}'


def _tuple_id(index):
    return 't%05d' % index


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='check-precedence.py',
        description='Compare the drafted v3 table with the claims precedence text over '
                    'every synthetic feature tuple.')
    parser.add_argument('--table', default=DEFAULT_TABLE)
    parser.add_argument('--interp', default=DEFAULT_INTERP)
    parser.add_argument('--work', default=None,
                        help='scratch directory (default: a fresh dir under $TMPDIR)')
    parser.add_argument('--ledger', default=None,
                        help='write one TSV line per tuple to this path')
    parser.add_argument('--batch', type=int, default=400)
    parser.add_argument('--reachable', action='store_true',
                        help='only tuples a real envelope can produce (dependencies appear '
                             'only on a missing-extractor-dependency gap)')
    parser.add_argument('--examples', type=int, default=3,
                        help='examples printed per divergence class')
    ns = parser.parse_args(argv)

    work = ns.work or tempfile.mkdtemp(dir=os.environ.get('TMPDIR') or None,
                                       prefix='precedence-check.')
    os.makedirs(work, exist_ok=True)
    problems = []
    rows = []
    try:
        # 1. the table must parse, and its vocabulary must cover the oracle's actions.
        res = subprocess.run([sys.executable, '-I', '-B', ns.interp, '--skill', ns.table,
                              '--table-only'], capture_output=True, text=True)
        if res.returncode != 0:
            print('TABLE UNEVALUABLE: exit %d\n%s' % (res.returncode, res.stderr))
            return 2
        actions_line = [line for line in res.stdout.splitlines()
                        if line.startswith('actions: ')]
        vocabulary = actions_line[0][len('actions: '):].split() if actions_line else []
        missing = sorted(set(LABEL_ACTIONS.values()) - set(vocabulary))
        if missing:
            # not a defect by itself: a table that never emits an action need not declare it
            print('note: the table vocabulary lacks these oracle actions: %r' % missing)

        # 2. write one envelope per tuple.
        items = list(tuples(reachable=ns.reachable))
        paths = []
        for index, tup in enumerate(items):
            directory = os.path.join(work, _tuple_id(index))
            os.makedirs(directory, exist_ok=True)
            path = os.path.join(directory, 'envelope.json')
            with open(path, 'w', encoding='utf-8') as handle:
                json.dump(envelope(tup['OP'], tup['PV'], tup['H'], tup['G'], tup['D'],
                                   tup['BE'], tup['SR'], tup['P']), handle)
            paths.append(path)

        # 3. label them in batches through the real interpreter.
        decisions = []
        for start in range(0, len(paths), ns.batch):
            chunk = paths[start:start + ns.batch]
            res = subprocess.run([sys.executable, '-I', '-B', ns.interp, '--skill',
                                  ns.table, '--json', *chunk],
                                 capture_output=True, text=True)
            if res.returncode != 0:
                print('INTERPRETER FAILED on batch %d: exit %d\n%s'
                      % (start, res.returncode, res.stderr[:2000]))
                return 2
            payload = json.loads(res.stdout)
            results = payload['results']
            if len(results) != len(chunk):
                print('SHORT BATCH at %d: %d results for %d envelopes'
                      % (start, len(results), len(chunk)))
                return 2
            for result in results:
                decisions.append((result['label'], result['action'],
                                  result['features']))

        # 4. compare.
        step_examples = {}
        divergences = {}
        for index, (tup, (label, action, features)) in enumerate(zip(items, decisions)):
            want_label, want_action, step = oracle(tup['OP'], tup['PV'], tup['H'],
                                                   tup['G'], tup['D'], tup['BE'],
                                                   tup['SR'], tup['P'])
            # the interpreter's own feature extraction must reproduce the tuple
            feats = (features['OP'], tuple(sorted(features['H'])),
                     tuple(sorted(features['G'])), tuple(sorted(features['D'])),
                     features['BE'], features['SR'], features['P'])
            expect = (tup['OP'], tuple(sorted(tup['H'])), tuple(sorted(tup['G'])),
                      tuple(sorted(tup['D'])), tup['BE'], tup['SR'], tup['P'])
            if feats != expect:
                problems.append('tuple %s extracted as %r, not %r'
                                % (_tuple_id(index), feats, expect))
            agree = (label, action) == (want_label, want_action)
            step_examples.setdefault(step, (index, tup, want_label, want_action,
                                            label, action, agree))
            if not agree:
                reason = known_divergence(tup, want_label, label)
                if reason is None:
                    problems.append('tuple %s %r: oracle %r/%r, table %r/%r'
                                    % (_tuple_id(index), tup, want_label, want_action,
                                       label, action))
                else:
                    divergences.setdefault(reason, []).append(
                        (index, tup, want_label, want_action, label, action))
            rows.append((
                _tuple_id(index), tup['OP'], tup['PV'], _fmt_set(tup['H']),
                _fmt_set(tup['G']), _fmt_set(tup['D']), tup['BE'], tup['SR'],
                str(tup['P']), str(step), want_label, want_action, label, action,
                'yes' if agree else 'no',
                known_divergence(tup, want_label, label) or ''))

        # 5. report.
        print('table: %s' % ns.table)
        print('interpreter: %s' % ns.interp)
        print('tuples: %d' % len(items))
        print('oracle label->action pairs (round-40 committed map + the claimed new action):')
        for label in sorted(LABEL_ACTIONS):
            print('  %-26s %s' % (label, LABEL_ACTIONS[label]))
        print('precedence steps exercised:')
        for step in sorted(step_examples):
            index, tup, want_label, want_action, label, action, agree = step_examples[step]
            print('  step %-2d %s  %s/%s  table %s/%s  %s'
                  % (step, _tuple_id(index), want_label, want_action, label, action,
                     'agree' if agree else 'DIVERGE'))
            print('          tuple OP=%s PV=%s H=%r G=%r D=%r BE=%s SR=%s P=%d'
                  % (tup['OP'], tup['PV'], tup['H'], tup['G'], tup['D'], tup['BE'],
                     tup['SR'], tup['P']))
        matched = sum(1 for row in rows if row[14] == 'yes')
        print('agreement: %d/%d tuples match on (label, action)' % (matched, len(rows)))
        for reason, _text in KNOWN:
            examples = divergences.get(reason, [])
            print('known divergence %s: %d tuples' % (reason, len(examples)))
            for index, tup, want_label, want_action, label, action in \
                    examples[:ns.examples]:
                print('  %s OP=%s PV=%s H=%r G=%r D=%r BE=%s SR=%s P=%d  oracle %s/%s  '
                      'table %s/%s'
                      % (_tuple_id(index), tup['OP'], tup['PV'], tup['H'], tup['G'],
                         tup['D'], tup['BE'], tup['SR'], tup['P'], want_label,
                         want_action, label, action))
        unexpected = [reason for reason in divergences if reason not in
                      {known for known, _t in KNOWN}]
        if unexpected:
            problems.append('unexpected divergence classes %r' % unexpected)

        if ns.ledger:
            header = ('tuple\tOP\tPV\tH\tG\tD\tBE\tSR\tP\tstep\toracle_label\t'
                      'oracle_action\ttable_label\ttable_action\tagree\tknown_divergence')
            with open(ns.ledger, 'w', encoding='utf-8') as handle:
                handle.write(header + '\n')
                for row in rows:
                    handle.write('\t'.join(row) + '\n')
            print('ledger: %s (%d lines)' % (ns.ledger, len(rows)))
        if problems:
            print('PROBLEMS:')
            for problem in problems[:40]:
                print('  ' + problem)
            return 1
        print('RESULT: agree on every tuple outside the two documented grammar limits')
        return 0
    finally:
        if ns.work is None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
