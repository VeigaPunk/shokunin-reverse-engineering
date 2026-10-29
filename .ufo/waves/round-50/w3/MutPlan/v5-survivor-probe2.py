#!/usr/bin/env python3
"""Decisive characterisation of the two surviving v5-draft mutants.

S1 `clean-unverified-row-files-cell-widened` (published files '>0' -> '*'):
    the TABLE now labels a no-reader family with ZERO published files and no
    gaps `clean-unverified`/`record-unverified`, while the draft's EVALUATOR
    still says `clean-empty`/`confirm-empty`.  That is a TABLE-vs-EVALUATOR
    disagreement - the very thing the C3 predicate (`table_labels ==
    evaluator_labels` on every envelope) forbids - but it is invisible to the
    selftest because no fixture and no committed envelope has a no-reader
    family with zero published files and no gaps.

S2 `clean-unverified-row-symlink-cell-widened` (symlink removed 'no' -> '*'):
    the TABLE's clean-unverified row now also fires on a run that removed a
    symlink.  The v4 `escaping-symlink-removed` row (gaps none, sr yes) sits
    ABOVE clean-unverified, so the pair may be unaffected; measure it.

For each mutant: run the draft's table and evaluator over purpose-built probe
shapes AND over the 126 committed round-42 envelopes, and report the pair
mismatches the C3 predicate would see.
"""
import importlib.util
import json
import os
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
BASE = os.path.join(S, 'v5-mut')
PRISTINE = os.path.join(S, 'v5-draft.py')
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
CORPUS = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')

MUTANTS = {
    'pristine': PRISTINE,
    'files-cell-widened': os.path.join(
        BASE, 'clean-unverified-row-files-cell-widened', 'sqfs-triage-v5.py'),
    'symlink-cell-widened': os.path.join(
        BASE, 'clean-unverified-row-symlink-cell-widened', 'sqfs-triage-v5.py'),
}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def table_rules(mod):
    header = ['label', 'operation', 'provider', 'handler', 'failing handler',
              'gap kinds', 'dependencies', '-be in child argv',
              'symlink removed', 'published files', 'action', 'cause', 'source']
    lines = ['| ' + ' | '.join(header) + ' |',
             '| ' + ' | '.join(['---'] * len(header)) + ' |']
    for row in mod.V5_ROWS:
        lines.append('| ' + ' | '.join(str(c) for c in row) + ' |')
    return mod.parse_table(lines, 0, mod.V5_ACTIONS.split())


def probe_set(mod):
    out = {}
    out['v2ns-zero-files-no-gaps'] = mod._env(
        handler='squashfs_v2_nonstandard', gaps=[], files=0)
    out['v3bc-zero-files-no-gaps'] = mod._env(
        handler='squashfs_v3_broadcom', gaps=[], files=0)
    out['v3ns-zero-files-no-gaps'] = mod._env(
        handler='squashfs_v3_nonstandard', gaps=[], files=0)
    out['v2ns-symlink-removed'] = mod._env(
        handler='squashfs_v2_nonstandard', gaps=[], files=2, be='-le', sr=True)
    out['v2ns-symlink-removed-unpublished'] = mod._env(
        handler='squashfs_v2_nonstandard', gaps=['unpublished-entry'], files=2,
        be='-le', sr=True)
    return out


def main():
    out = {}
    for tag, path in MUTANTS.items():
        if not os.path.isfile(path):
            continue
        m = load(path, 'v5p_' + tag)
        rules = table_rules(m)
        rec = {}
        for pname, env in probe_set(m).items():
            feat = m.features(env)
            rule = m.classify(rules, feat)
            tlab, tact = m.decision(rule)
            elab, eact, _step = m.evaluate(feat)
            rec[pname] = {'table': [tlab, tact], 'evaluator': [elab, eact],
                          'agree': [tlab, tact] == [elab, eact],
                          'P': feat['P'], 'G': feat['G'], 'SR': feat['SR'],
                          'F': feat['F']}
        mism = 0
        total = 0
        for d in sorted(os.listdir(CORPUS)):
            p = os.path.join(CORPUS, d, 'envelope.json')
            if not os.path.isfile(p):
                continue
            total += 1
            feat = m.load_envelope(p)
            rule = m.classify(rules, feat)
            tlab, tact = m.decision(rule)
            elab, eact, _ = m.evaluate(feat)
            if [tlab, tact] != [elab, eact]:
                mism += 1
        rec['corpus_envelopes'] = total
        rec['corpus_table_evaluator_mismatches'] = mism
        out[tag] = rec
    p = os.path.join(S, 'v5-survivor-probe-2.json')
    json.dump(out, open(p, 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
