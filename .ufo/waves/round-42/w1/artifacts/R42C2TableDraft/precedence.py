#!/usr/bin/env python3
"""precedence.py — the drafted round-42 label precedence, amendment A1, steps 1-15.

Written ONLY from the numbered steps in `plans/round-42-claims.md` § R42-C2 (A1, 2026-10-26),
for wave-1 self-checking of `block21.md`.  It is not the frozen independent evaluator
(`tools/round-42/indep-eval-v4.py`, another seat) and must never be cited as one.

Features used: OP, PR, H, F, L, HF, G, D, BE, SR, P — exactly the A1 definitions.
`HF` is the handler set of the `extractor-failure` gaps, or `F` when none carries one.

Input: a feature dict as produced by `v4-refparse.features()`.
Output: (label, action, step).
"""
from __future__ import annotations

LEGACY_PREFIXES = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3')


def legacy(fam):
    return {h for h in fam if h.startswith(LEGACY_PREFIXES)}


def decide(feat):
    op = feat['OP']
    pr = feat['PR']
    fam = set(feat['F'])
    low = legacy(fam)
    hf = set(feat.get('HF') or ()) or fam
    gaps = set(feat['G'])
    deps = set(feat['D'])
    be = feat['BE']
    sr = feat['SR']
    published = feat['P']

    # 1. domain
    if op != 'extract_firmware' or pr != 'unblob':
        return 'unclassified', 'none', 1
    # 2. no SquashFS handler at this depth, and the depth budget explains it
    if not fam and 'depth-limited' in gaps:
        return 'container-depth-limited', 'raise-depth', 2
    # 3. no SquashFS handler
    if not fam:
        return 'no-squashfs-chunk', 'inspect-input', 3
    # 4. dependency gap, membership in D
    if 'missing-extractor-dependency' in gaps:
        if 'sasquatch-v4be' in deps:
            return 'dep-missing-be', 'install-extractor-be', 4
        if 'sasquatch' in deps:
            return 'dep-missing-le', 'install-extractor-le', 4
        # names neither -> continue at 5
    # 5. extractor failure with published files
    if 'extractor-failure' in gaps and published > 0:
        return 'partial-body-failure', 'salvage-partial', 5
    # 6. BE v4 handler failed, no -be recorded
    if ('extractor-failure' in gaps and published == 0 and be == 'no'
            and 'squashfs_v4_be' in hf):
        return 'avm-marker-be-dropped', 'wrap-extractor-be', 6
    # 7. a v1-v3 handler failed
    if 'extractor-failure' in gaps and published == 0 and (hf & low):
        return 'legacy-body-failure', 'cross-read-legacy', 7
    # 8. any other zero-file extractor failure
    if 'extractor-failure' in gaps and published == 0:
        return 'body-extractor-failure', 'preserve-failure', 8
    # 9. unclaimed bytes beside the filesystem
    if 'unknown-chunk-handler' in gaps:
        return 'unknown-residue', 'isolate-residue', 9
    # 10. depth ceiling over a SquashFS chunk
    if 'depth-limited' in gaps:
        return 'depth-limited', 'raise-depth', 10
    # 11. removed link beside kept metadata
    if sr == 'yes' and 'unpublished-entry' in gaps:
        return 'mixed-symlinks', 'audit-symlinks', 11
    # 12. removed link, no gap
    if sr == 'yes' and not gaps:
        return 'escaping-symlink-removed', 'expect-link-absent', 12
    # 13. exactly one kept-metadata gap kind
    if gaps == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'count-gap', 13
    # 14. no gap
    if not gaps:
        if published > 0:
            return 'clean', 'none', 14
        return 'clean-empty', 'confirm-empty', 14
    # 15. anything else
    return 'unclassified', 'none', 15
