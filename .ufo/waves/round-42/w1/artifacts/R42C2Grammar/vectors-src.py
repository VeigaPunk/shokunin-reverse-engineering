#!/usr/bin/env python3
"""vectors-src.py - hand-written A1 feature-tuple vectors for R42-C2 (grammar seat).

Each vector's expected (label, action) pair and deciding step are derived BY
HAND from plans/round-42-claims.md `## R42-C2` amendment A1 steps 1-15. The
script validates every vector against ref-eval-v4draft.classify (an independent
encoding of the same text) and emits vectors-v4draft.json. A mismatch means a
transcription slip in one of the two encodings - fix by hand, never by copying.

Handler shorthand (real unblob 26.6.4 names, handlers/filesystem/squashfs.py):
  L  squashfs_v3            Ld squashfs_v3_ddwrt     L1 squashfs_v1
  B  squashfs_v4_be         E  squashfs_v4_le        W  squashfs_v4_broadcom
  T  trx_v1 (container)     X  cpio (non-SquashFS chunk)
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import importlib.util as _ilu  # noqa: E402

_spec = _ilu.spec_from_file_location('ref_eval_v4draft',
                                     os.path.join(HERE, 'ref-eval-v4draft.py'))
_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
classify = _mod.classify

L, LD, L1 = 'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v1'
B, E, W = 'squashfs_v4_be', 'squashfs_v4_le', 'squashfs_v4_broadcom'
T, X = 'trx_v1', 'cpio'

KNOWN = {L, LD, L1, 'squashfs_v2', 'squashfs_v2_nonstandard',
         'squashfs_v3_broadcom', 'squashfs_v3_nonstandard', B, E, W, T, X}


def v(vid, decides, tag, note, reached=None, **kw):
    feat = {'OP': 'extract_firmware', 'PR': 'unblob', 'H': [], 'HF': [],
            'G': [], 'D': [], 'BE': 'n/a', 'SR': 'no', 'P': 0}
    feat.update(kw)
    feat['H'] = sorted(feat['H'])
    feat['HF'] = sorted(feat['HF'])
    feat['G'] = sorted(feat['G'])
    feat['D'] = sorted(feat['D'])
    label, action, step = classify(feat)
    out = {'id': vid, 'decides': decides, 'tag': tag, 'note': note,
           'features': feat,
           'expected': {'label': label, 'action': action}}
    if reached is not None:
        out['reached'] = reached
    return out


VECTORS = [
    # ---- step 1: domain guard ------------------------------------------------
    v('V01', 1, 'domain-guard', 'wrong operation; everything else in-domain',
      OP='extract_image', H=[B], P=1),
    v('V02', 1, 'domain-guard', 'wrong provider id', PR='binwalk', H=[B], P=1),
    v('V03', 1, 'domain-guard', 'wrong OP with a maximal tuple: step 1 precedes all',
      OP='extract_image', H=[L, B], HF=[L], BE='no', SR='yes', P=3,
      G=['missing-extractor-dependency', 'extractor-failure', 'depth-limited',
         'unpublished-entry', 'unknown-chunk-handler'], D=['sasquatch']),
    # ---- step 2: container (F empty + depth) ---------------------------------
    v('V04', 2, 'container', 'A1 container class: SquashFS image inside a TRX at --max-depth 1',
      H=[T], G=['depth-limited']),
    v('V05', 2, 'container', 'container with no chunk carved at all', H=[], G=['depth-limited']),
    v('V06', 2, 'container', 'SR=yes rides along: step 2 precedes the SR rows',
      H=[T], G=['depth-limited'], SR='yes'),
    v('V07', 2, 'container', 'dependency gap rides along: step 2 precedes step 4',
      H=[T], G=['depth-limited', 'missing-extractor-dependency'], D=['sasquatch']),
    v('V08', 2, 'container', 'residue rides along on a container: step 2 precedes step 9',
      H=[T], G=['depth-limited', 'unknown-chunk-handler']),
    # ---- step 3: no-squashfs-chunk -------------------------------------------
    v('V09', 3, 'no-chunk', 'bare envelope, no chunks', H=[]),
    v('V10', 3, 'no-chunk', 'only a non-SquashFS chunk: F is prefix-scoped to squashfs_',
      H=[X], P=2),
    v('V11', 3, 'no-chunk', 'dependency gap with F empty: step 3 precedes step 4',
      H=[X], G=['missing-extractor-dependency'], D=['sasquatch']),
    v('V12', 3, 'no-chunk', 'residue gap with F empty and no depth gap: step 3 precedes step 9',
      H=[X], G=['unknown-chunk-handler'], P=1),
    v('V13', 3, 'no-chunk', 'SR=yes with F empty and no gaps: step 3 precedes step 12',
      H=[X], SR='yes'),
    v('V14', 3, 'no-chunk', 'container chunk WITHOUT a depth gap falls to step 3 (the 2/3 boundary)',
      H=[T], G=['unknown-chunk-handler'], P=1),
    # ---- step 4: dependency by membership ------------------------------------
    v('V15', 4, 'dep', 'v4 BE chunk resolves sasquatch-v4be', H=[B], G=['missing-extractor-dependency'],
      D=['sasquatch-v4be']),
    v('V16', 4, 'dep', 'legacy chunk resolves plain sasquatch (confirmed on real envelopes)',
      H=[L], G=['missing-extractor-dependency'], D=['sasquatch']),
    v('V17', 4, 'dep', 'v4 LE chunk also resolves plain sasquatch', H=[E], G=['missing-extractor-dependency'],
      D=['sasquatch']),
    v('V18', 4, 'dep', 'D naming both: membership + be-arm-first (one-column exact-set table diverges)',
      H=[B], G=['missing-extractor-dependency'], D=['sasquatch', 'sasquatch-v4be']),
    v('V19', 15, 'dep', 'dependency gap naming neither: else-continue falls to step 15', reached=4,
      H=[E], G=['missing-extractor-dependency'], D=['unsquashfs'], P=4),
    v('V20', 4, 'dep', 'dep + partial failure: step 4 precedes step 5',
      H=[L], HF=[L], G=['missing-extractor-dependency', 'extractor-failure'], D=['sasquatch'], P=5),
    v('V21', 4, 'dep', 'dep + zero-file failure: step 4 precedes step 6',
      H=[B], HF=[B], G=['missing-extractor-dependency', 'extractor-failure'], D=['sasquatch-v4be']),
    v('V22', 10, 'dep', 'dep else-continue reaches step 10 (depth)', reached=4,
      H=[E], G=['missing-extractor-dependency', 'depth-limited'], D=['unsquashfs'], P=1),
    v('V23', 11, 'dep', 'dep else-continue reaches step 11 (SR rows)', reached=4,
      H=[E], G=['missing-extractor-dependency', 'unpublished-entry'], SR='yes'),
    # ---- step 5: partial ------------------------------------------------------
    v('V24', 5, 'partial', 'partial with depth + link gaps + removal: step 5 absorbs them all',
      H=[B], HF=[B], G=['extractor-failure', 'depth-limited', 'unpublished-entry'],
      BE='yes', SR='yes', P=7),
    v('V25', 5, 'partial', 'partial on a FAILING legacy chunk: P>0 beats step 7',
      H=[L], HF=[L], G=['extractor-failure'], BE='no', P=3),
    v('V26', 5, 'partial', 'partial + residue: step 5 precedes step 9',
      H=[E], HF=[E], G=['extractor-failure', 'unknown-chunk-handler'], BE='no', P=1),
    # ---- step 6: avm ----------------------------------------------------------
    v('V27', 6, 'avm', 'A1 avm class: failing v4_be, BE argv recorded without -be',
      H=[B], HF=[B], G=['extractor-failure'], BE='no'),
    v('V28', 8, 'avm', 'BE=n/a (timeout, no argv): step 6 needs BE=no, falls to step 8', reached=6,
      H=[B], HF=[B], G=['extractor-failure']),
    v('V29', 8, 'avm', 'BE=yes envelope-level (a legacy sibling ran -be) blocks step 6; HF={v4_be} not legacy -> step 8', reached=6,
      H=[B, L], HF=[B], G=['extractor-failure'], BE='yes'),
    v('V30', 6, 'avm', 'both v4_be and legacy failing: membership fires step 6 before step 7',
      H=[L, B], HF=[L, B], G=['extractor-failure'], BE='no'),
    # ---- step 7: legacy-body-failure -----------------------------------------
    v('V31', 7, 'legacy', 'A1 legacy class: failing v3 chunk, BE=no', H=[L], HF=[L],
      G=['extractor-failure'], BE='no'),
    v('V32', 7, 'legacy', 'BE=yes: step 7 has NO BE condition (a BE v3 chunk runs sasquatch -be)',
      H=[L], HF=[L], G=['extractor-failure'], BE='yes'),
    v('V33', 7, 'legacy', 'BE=n/a (legacy timeout): still step 7, not step 8',
      H=[L], HF=[L], G=['extractor-failure']),
    v('V34', 7, 'legacy', 'ddwrt variant is in L', H=[LD], HF=[LD], G=['extractor-failure'], BE='no'),
    v('V35', 7, 'legacy', 'v1 handler is in L', H=[L1], HF=[L1], G=['extractor-failure'], BE='no'),
    v('V36', 7, 'legacy', 'MIXED: legacy failing beside a CLEAN v4_be chunk (one-column table fires avm)',
      H=[L, B], HF=[L], G=['extractor-failure'], BE='no'),
    v('V37', 7, 'legacy', 'MIXED: legacy failing beside a clean v4_le chunk (both encodings agree)',
      H=[L, E], HF=[L], G=['extractor-failure'], BE='no'),
    v('V38', 7, 'legacy', 'MIXED: legacy and v4_le both failing -> step 7',
      H=[L, E], HF=[L, E], G=['extractor-failure'], BE='no'),
    # ---- step 8: body residual ------------------------------------------------
    v('V39', 8, 'body', 'failing v4_le chunk, single chunk', H=[E], HF=[E],
      G=['extractor-failure'], BE='no'),
    v('V40', 8, 'body', 'MIXED: v4_le failing beside a CLEAN legacy chunk (one-column table fires legacy)',
      H=[E, L], HF=[E], G=['extractor-failure'], BE='no'),
    v('V41', 8, 'body', 'MIXED: v4_le failing beside a CLEAN v4_be chunk (one-column table fires avm)',
      H=[E, B], HF=[E], G=['extractor-failure'], BE='no'),
    v('V42', 8, 'body', 'v4_broadcom failing: in F, not in L, not v4_be',
      H=[W], HF=[W], G=['extractor-failure'], BE='no'),
    v('V43', 8, 'body', 'MIXED: v4_broadcom failing beside a clean legacy chunk',
      H=[W, L], HF=[W], G=['extractor-failure'], BE='no'),
    v('V44', 8, 'body', 'MIXED: v4_broadcom failing beside a clean v4_be chunk',
      H=[W, B], HF=[W], G=['extractor-failure'], BE='no'),
    v('V45', 6, 'avm', 'HF fallback to F (no failing gap handler recorded): F={v3,v4_be} -> step 6 membership',
      H=[L, B], G=['extractor-failure'], BE='no'),
    v('V46', 7, 'legacy', 'HF fallback to F={v3,v4_le}: no v4_be, legacy present -> step 7',
      H=[L, E], G=['extractor-failure'], BE='no'),
    v('V47', 8, 'body', 'failing handler is the NON-SquashFS chunk: HF={cpio} decides, not F',
      H=[E, X], HF=[X], G=['extractor-failure'], BE='no'),
    # ---- step 9: residue -------------------------------------------------------
    v('V48', 9, 'residue', 'A1 residue class: unclaimed bytes beside a SquashFS chunk',
      H=[E], G=['unknown-chunk-handler'], P=3),
    v('V49', 9, 'residue', 'residue + depth: step 9 precedes step 10 (L1-named boundary)',
      H=[E], G=['unknown-chunk-handler', 'depth-limited'], P=2),
    v('V50', 9, 'residue', 'residue + SR: step 9 precedes steps 11/12',
      H=[B], G=['unknown-chunk-handler'], SR='yes'),
    v('V51', 4, 'residue', 'dep + residue: step 4 precedes step 9',
      H=[L], G=['missing-extractor-dependency', 'unknown-chunk-handler'], D=['sasquatch']),
    v('V52', 8, 'residue', 'zero-file failure + residue: step 8 precedes step 9',
      H=[E], HF=[E], G=['extractor-failure', 'unknown-chunk-handler'], BE='no'),
    # ---- step 10: depth ---------------------------------------------------------
    v('V53', 10, 'depth', 'depth gap on a SquashFS chunk', H=[E], G=['depth-limited'], P=6),
    v('V54', 10, 'depth', 'depth + in-tree links + removal: step 10 precedes step 11',
      H=[B], G=['depth-limited', 'unpublished-entry'], SR='yes', P=2),
    v('V67', 10, 'depth', 'container chunk AND a separate top-level SquashFS chunk: F nonempty -> step 10, not 2',
      H=[T, L], G=['depth-limited'], P=1),
    # ---- step 11: mixed ---------------------------------------------------------
    v('V55', 11, 'mixed', 'SR + in-tree links', H=[E], G=['unpublished-entry'], SR='yes', P=4),
    v('V56', 11, 'mixed', 'mixed on a legacy chunk: grammar-reachable, fixtures cannot build it (no v3 writer)',
      H=[L], G=['unpublished-entry'], SR='yes'),
    # ---- step 12: escaping -------------------------------------------------------
    v('V57', 12, 'escaping', 'removal report, empty gap set', H=[B], SR='yes', P=2),
    v('V58', 12, 'escaping', 'escaping on a legacy chunk with P=0', H=[L], SR='yes'),
    # ---- step 13: in-tree ----------------------------------------------------------
    v('V59', 13, 'in-tree', 'exact singleton gap set', H=[E], G=['unpublished-entry'], P=1),
    v('V60', 13, 'in-tree', 'in-tree on a legacy chunk', H=[L], G=['unpublished-entry']),
    # ---- step 14: clean / clean-empty ------------------------------------------------
    v('V61', 14, 'clean', 'clean legacy chunk (the R41-CL4 fix, positive arm)', H=[L], P=5),
    v('V62', 14, 'clean', 'clean-empty on a v1 chunk', H=[L1]),
    v('V63', 14, 'clean', 'clean v4 chunk', H=[B], P=1),
    v('V64', 14, 'clean', 'clean with a non-SquashFS sibling chunk: sibling does not matter',
      H=[T, E], P=2),
    # ---- step 15: unclassified ---------------------------------------------------------
    v('V65', 15, 'unclassified', 'unpublished-entry beside an unknown gap kind: not the exact singleton',
      H=[E], G=['unpublished-entry', 'encrypted-chunk'], P=2),
    v('V66', 15, 'unclassified', 'SR=yes beside an unrelated gap: step 11 needs unpublished-entry',
      H=[B], G=['encrypted-chunk'], SR='yes'),
    # ---- cross-boundary: failure rows beat depth/residue --------------------------------
    v('V68', 7, 'legacy', 'container chunk + failing legacy chunk: failure rows precede depth/residue',
      H=[T, L], HF=[L], G=['depth-limited', 'extractor-failure'], BE='no'),
]


def main():
    problems = []
    seen = set()
    for vec in VECTORS:
        if vec['id'] in seen:
            problems.append('duplicate id %s' % vec['id'])
        seen.add(vec['id'])
        f = vec['features']
        if not set(f['H']) <= KNOWN:
            problems.append('%s: unknown handler in H %s' % (vec['id'], f['H']))
        if not set(f['HF']) <= set(f['H']):
            problems.append('%s: HF not a subset of H' % vec['id'])
        if f['D'] and 'missing-extractor-dependency' not in f['G']:
            problems.append('%s: D nonempty without a dependency gap' % vec['id'])
        if f['HF'] and 'extractor-failure' not in f['G']:
            problems.append('%s: HF nonempty without an extractor-failure gap' % vec['id'])
        if f['BE'] not in ('yes', 'no', 'n/a'):
            problems.append('%s: bad BE' % vec['id'])
        if f['SR'] not in ('yes', 'no'):
            problems.append('%s: bad SR' % vec['id'])
        if vec['decides'] < 1 or vec['decides'] > 15:
            problems.append('%s: bad step' % vec['id'])
    # cross-check the hand-derived pairs against the reference implementation
    for vec in VECTORS:
        label, action, step = classify(vec['features'])
        if (label, action) != (vec['expected']['label'], vec['expected']['action']):
            problems.append('%s: hand pair %s != reference %s (step %d)'
                            % (vec['id'], (vec['expected']['label'],
                                          vec['expected']['action']),
                               (label, action), step))
        elif step != vec['decides']:
            problems.append('%s: hand step %d != reference step %d'
                            % (vec['id'], vec['decides'], step))
    if problems:
        for p in problems:
            print('PROBLEM %s' % p, file=sys.stderr)
        return 1
    doc = {
        '_readme': [
            'R42-C2 (amendment A1) feature-tuple vectors, grammar seat R42C2Grammar.',
            'features -> expected (label, action) + decides = the A1 step whose guard',
            'fired (mechanically checkable); reached = a step whose guard was',
            'evaluated and failed (else-continue / BE guard), absent when equal.',
            'Expected pairs are hand-derived from plans/round-42-claims.md ## R42-C2',
            'steps 1-15 and cross-checked against ref-eval-v4draft.py classify().',
            'Feature semantics are the A1 feature paragraph verbatim: H = chunk',
            'handlers union gap handlers; F = squashfs_-prefixed subset of H;',
            'L = F members matching squashfs_v1*/v2*/v3*; HF = handlers on',
            'extractor-failure gaps, falling back to F when none carries one;',
            'D = union of gap dependencies; BE in yes|no|n/a; SR yes|no; P int.',
            'HF=[] means "no failing gap carries a handler" (the A1 fallback) or',
            '"no extractor-failure gap" - steps 6/7 are unreachable in the latter.',
            'build-envelope.py realizes a vector as a synthetic REA envelope',
            'readable by both frozen round-41 tools.',
        ],
        '_pinned': {
            'source': 'plans/round-42-claims.md ## R42-C2 amendment A1 steps 1-15',
            'step3_membership': 'D holds = membership, be-arm tested first',
            'step6_membership': 'squashfs_v4_be in HF (membership, not equality)',
            'step7_no_be_guard': 'step 7 has no BE condition',
            'hf_fallback': 'HF = F when no extractor-failure gap carries a handler',
            'legacy_glob': 'squashfs_v[123]* == union of squashfs_v1*/v2*/v3*',
            'handler_inventory': sorted(KNOWN),
        },
        'vectors': VECTORS,
    }
    out = os.path.join(HERE, 'vectors-v4draft.json')
    with open(out, 'w', encoding='utf-8') as handle:
        json.dump(doc, handle, indent=1, sort_keys=False)
    steps = sorted({vec['decides'] for vec in VECTORS})
    print('vectors-v4draft.json: %d vectors, steps covered %s' % (len(VECTORS), steps))
    missing = [s for s in range(1, 16) if s not in steps]
    if missing:
        print('steps with no deciding vector: %s' % missing, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
