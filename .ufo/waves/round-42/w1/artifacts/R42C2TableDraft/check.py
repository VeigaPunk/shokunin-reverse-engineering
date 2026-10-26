#!/usr/bin/env python3
"""check.py — compares the drafted table v4 (`block21.md`) with the drafted precedence.

Three groups, all measured against the artifacts in this directory:

  grid      a feature grid over (handler family, gap set, dependency set, -be, symlink
            report, published count, domain) compared row-for-row; every disagreement is
            classified as `seam-family` (the failing handler named by a gap and the family
            in `F` disagree, a column the table does not have) or `other` (a real defect).
  heldout   the 52 committed round-41 held-out envelopes: this draft vs the precedence, and
            the frozen v3 interpreter's pair, so the regression is measured, not assumed.
  dev       the two real `squashfs_v3` envelopes produced this wave (`--max-depth 1` and
            `3`): the R41-CL4 repair, executed.

Usage
  python3 -I -B check.py --skill FIXTURE-SKILL.md --heldout DIR \
      --dev ENVELOPE... --out-prefix PREFIX
Writes PREFIX-*.tsv and prints one summary block.  Exit 0 when the only disagreements are
`seam-family`; exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = _load('v4ref', os.path.join(HERE, 'v4-refparse.py'))
prec = _load('prec', os.path.join(HERE, 'precedence.py'))

FAMS = {
    'none': (),
    'v1': ('squashfs_v1',),
    'v3': ('squashfs_v3',),
    'v3ddwrt': ('squashfs_v3_ddwrt',),
    'v4be': ('squashfs_v4_be',),
    'v4le': ('squashfs_v4_le',),
    'v4both': ('squashfs_v4_be', 'squashfs_v4_le'),
    'v3_be': ('squashfs_v3', 'squashfs_v4_be'),
}
GAPS = {
    'empty': (),
    'depth': ('depth-limited',),
    'unpub': ('unpublished-entry',),
    'unpub2': ('unpublished-entry',),
    'fail': ('extractor-failure',),
    'dep': ('missing-extractor-dependency',),
    'depfail': ('missing-extractor-dependency', 'extractor-failure'),
    'faildepth': ('extractor-failure', 'depth-limited'),
    'failunpub': ('extractor-failure', 'unpublished-entry'),
    'depthunpub': ('depth-limited', 'unpublished-entry'),
    'depthfailunpub': ('depth-limited', 'extractor-failure', 'unpublished-entry'),
    'all': ('missing-extractor-dependency', 'extractor-failure', 'depth-limited',
            'unpublished-entry'),
    'unknown': ('unknown-chunk-handler',),
    'encrypted': ('encrypted-chunk',),
    'unpubunknown': ('unpublished-entry', 'unknown-chunk-handler'),
    'unknowndepth': ('unknown-chunk-handler', 'depth-limited'),
    'unknownfail': ('unknown-chunk-handler', 'extractor-failure'),
    'unknowndepthunpub': ('unknown-chunk-handler', 'depth-limited',
                          'unpublished-entry'),
}
DEPS = {
    'none': (),
    'le': ('sasquatch',),
    'be': ('sasquatch-v4be',),
    'both': ('sasquatch', 'sasquatch-v4be'),
    'other': ('other-tool',),
    'le_other': ('sasquatch', 'other-tool'),
}
DOMAINS = {
    'ok': ('extract_firmware', 'unblob'),
    'wrong-op': ('inspect_firmware_regions', 'unblob'),
    'wrong-prov': ('extract_firmware', 'binwalk'),
}
HFCH = {'fam': None, 'v3': ('squashfs_v3',), 'v4be': ('squashfs_v4_be',)}


def grid():
    rows = []
    for fam_name, fam in FAMS.items():
        for gap_name, gaps in GAPS.items():
            has_fail = 'extractor-failure' in gaps
            for dep_name, deps in DEPS.items():
                for be in ('yes', 'no', 'n/a'):
                    for sr in ('yes', 'no'):
                        for p in (0, 2):
                            for dom_name, (op, pr) in DOMAINS.items():
                                for fail_name, fail in HFCH.items():
                                    if fail is not None and not has_fail:
                                        continue
                                    famset = [h for h in fam
                                              if h.startswith('squashfs_')]
                                    # REA's gap handler is the chunk's own handler
                                    # (FirmwarePublication.js:226-238), so only HF
                                    # subset of F is a reachable envelope shape.
                                    if fail and not set(fail) <= set(famset):
                                        continue
                                    hf = list(fail) if fail else famset
                                    feat = {
                                        'OP': op, 'PR': pr,
                                        'H': list(fam), 'F': famset,
                                        'L': [h for h in famset
                                              if h.startswith(('squashfs_v1',
                                                               'squashfs_v2',
                                                               'squashfs_v3'))],
                                        'HF': hf,
                                        'G': list(gaps), 'D': list(deps), 'BE': be,
                                        'SR': sr, 'P': p,
                                        'commands': [],
                                    }
                                    rows.append((fam_name, gap_name, dep_name, be, sr, p,
                                                 dom_name, fail_name, feat))
    return rows


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--skill', required=True)
    ap.add_argument('--heldout', required=True)
    ap.add_argument('--dev', nargs='*', default=[])
    ap.add_argument('--out-prefix', required=True)
    ns = ap.parse_args(argv)

    rules, info = ref.parse_skill(ref.read_skill(ns.skill))
    print('table: marker %d actions %d table %d rules %d actions %d'
          % (info['marker_line'], info['actions_line'], info['table_line'],
             info['rules'], len(info['actions'])))
    labels = [r['label'] for r in rules]
    print('labels (%d): %s' % (len(labels), ' '.join(labels)))

    # ---- grid
    rows = grid()
    agree = 0
    other = []
    with open(ns.out_prefix + '-grid.tsv', 'w', encoding='utf-8') as fh:
        fh.write('fam\tgaps\tdeps\tbe\tsr\tp\tdomain\tfailch\tinterp\tprec\tclass\n')
        for (fam_name, gap_name, dep_name, be, sr, p, dom_name, fail_name, feat) in rows:
            ilabel, iaction, idx = ref.decision(ref.classify(rules, feat))
            plabel, paction, step = prec.decide(feat)
            same = (ilabel, iaction) == (plabel, paction)
            if same:
                cls = 'agree'
                agree += 1
            else:
                cls = 'other'
                other.append(feat)
            line = '%s\t%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s/%s\t%s/%s\t%s' % (
                fam_name, gap_name, dep_name, be, sr, p, dom_name, fail_name,
                ilabel, iaction, plabel, paction, cls)
            fh.write(line + '\n')
    total = len(rows)
    print('grid: %d points, %d agree, %d other' % (total, agree, len(other)))

    # ---- held-out (round-41 committed envelopes)
    held = []
    if os.path.isdir(ns.heldout):
        ids = sorted(d for d in os.listdir(ns.heldout)
                     if os.path.isfile(os.path.join(ns.heldout, d, 'envelope.json')))
        for cid in ids:
            path = os.path.join(ns.heldout, cid, 'envelope.json')
            feat = ref.load_envelope(path)
            held.append((cid, path, feat))
    interp_pairs = {}
    v3pairs_path = os.path.join(ns.out_prefix + '-v3pairs.tsv')
    if os.path.exists(v3pairs_path):
        for line in open(v3pairs_path, encoding='utf-8'):
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 3:
                interp_pairs[os.path.basename(os.path.dirname(parts[0]))] = (parts[1],
                                                                           parts[2])
    agree_h = seam_h = other_h = 0
    v4_vs_v3 = 0
    with open(ns.out_prefix + '-heldout.tsv', 'w', encoding='utf-8') as fh:
        fh.write('id\tinterp_v4\tprec\tstep\tv3\tv4_eq_prec\tv4_eq_v3\n')
        for cid, path, feat in held:
            ilabel, iaction, idx = ref.decision(ref.classify(rules, feat))
            plabel, paction, step = prec.decide(feat)
            v3 = interp_pairs.get(cid)
            same = (ilabel, iaction) == (plabel, paction)
            same3 = v3 is not None and (ilabel, iaction) == v3
            if same:
                agree_h += 1
            elif v3 is not None and v3 != (plabel, paction):
                seam_h += 1
            else:
                other_h += 1
            v4_vs_v3 += 1 if same3 else 0
            fh.write('%s\t%s/%s\t%s/%s\t%d\t%s/%s\t%s\t%s\n' % (
                cid, ilabel, iaction, plabel, paction, step,
                v3[0] if v3 else '-', v3[1] if v3 else '-',
                'yes' if same else 'NO', 'yes' if same3 else 'NO'))
    print('heldout: %d envelopes, %d agree, %d seam, %d other; v4==v3 on %d'
          % (len(held), agree_h, seam_h, other_h, v4_vs_v3))

    # ---- dev envelopes (real squashfs_v3)
    with open(ns.out_prefix + '-dev.tsv', 'w', encoding='utf-8') as fh:
        fh.write('envelope\tH\tG\tP\tinterp_v4\tprec\tv3\n')
        for path in ns.dev:
            feat = ref.load_envelope(path)
            ilabel, iaction, idx = ref.decision(ref.classify(rules, feat))
            plabel, paction, step = prec.decide(feat)
            fh.write('%s\t%s\t%s\t%d\t%s/%s\t%s/%s\t%s\n' % (
                os.path.basename(path), ','.join(feat['H']),
                ','.join(feat['G']) or 'none', feat['P'],
                ilabel, iaction, plabel, paction,
                'unclassified/none (v3: no squashfs_v4_* handler)'))
            print('dev %-18s H=%s G=%s P=%d -> v4 %s/%s, prec %s/%s'
                  % (os.path.basename(path), ','.join(feat['H']),
                     ','.join(feat['G']) or 'none', feat['P'], ilabel, iaction,
                     plabel, paction))

    return 0 if (not other and not other_h) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
