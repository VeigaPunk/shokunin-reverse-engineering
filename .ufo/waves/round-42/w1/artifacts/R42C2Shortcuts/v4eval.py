#!/usr/bin/env python3
"""v4eval.py -- R42-C2 independent-evaluator TRANSCRIPTION (A1) for shortcut
analysis.

NOT the frozen evaluator: this is a working model written ONLY from the
round-42 draft's precedence text as amended by A1 (plans/round-42-claims.md
`## R42-C2`, steps 1-15), used to derive expected (label, action) pairs for
the tuple universe of the shortcut attack.  A1 status: amended 2026-10-26
~22:20Z; this file implements the amended text.

Feature tuple vocabulary (round 41 + F, L, HF):
  OP  operation
  PR  provider id
  H   handler set (all chunk/gap handlers)
  HF  failing-chunk handler set (handlers carried by extractor-failure gaps;
       when none carries a handler, HF = F)
  F   {name in H | name.startswith('squashfs_')}
  L   {name in F | name matches squashfs_v1*/v2*/v3*}
  G   gap-kind set
  D   dependency-name set (exact names)
  BE  '-be' in a recorded child argv: yes | no | n/a
  SR  symlink removed: yes | no
  P   published regular file count

Steps, first match wins (quoted from the amended draft):
  1. OP != extract_firmware or PR != unblob -> (unclassified, none).
  2. F = {} and depth-limited in G -> (container-depth-limited, raise-depth).
  3. F = {} -> (no-squashfs-chunk, inspect-input).
  4. missing-extractor-dependency in G: D holds sasquatch-v4be ->
     (dep-missing-be, install-extractor-be); else D holds sasquatch ->
     (dep-missing-le, install-extractor-le); else continue.
  5. extractor-failure in G and P > 0 -> (partial-body-failure, salvage-partial).
  6. extractor-failure in G, P = 0, BE = no, squashfs_v4_be in HF ->
     (avm-marker-be-dropped, wrap-extractor-be).
  7. extractor-failure in G, P = 0, HF intersect L != {} ->
     (legacy-body-failure, cross-read-legacy).
  8. extractor-failure in G, P = 0 -> (body-extractor-failure, preserve-failure).
  9. unknown-chunk-handler in G -> (unknown-residue, isolate-residue).
 10. depth-limited in G -> (depth-limited, raise-depth).
 11. SR = yes and unpublished-entry in G -> (mixed-symlinks, audit-symlinks).
 12. SR = yes and G = {} -> (escaping-symlink-removed, expect-link-absent).
 13. G = {unpublished-entry} -> (in-tree-symlink-metadata, count-gap).
 14. G = {}: P > 0 -> (clean, none); P = 0 -> (clean-empty, confirm-empty).
 15. anything else -> (unclassified, none).
"""

SQUASHFS_PREFIX = "squashfs_"
BE_DEPENDENCY = "sasquatch-v4be"
LE_DEPENDENCY = "sasquatch"
AVM_HANDLER = "squashfs_v4_be"
LEGACY_PREFIXES = ("squashfs_v1", "squashfs_v2", "squashfs_v3")

ACTION_BY_LABEL = {
    "container-depth-limited": "raise-depth",
    "no-squashfs-chunk": "inspect-input",
    "dep-missing-be": "install-extractor-be",
    "dep-missing-le": "install-extractor-le",
    "partial-body-failure": "salvage-partial",
    "avm-marker-be-dropped": "wrap-extractor-be",
    "legacy-body-failure": "cross-read-legacy",
    "body-extractor-failure": "preserve-failure",
    "unknown-residue": "isolate-residue",
    "depth-limited": "raise-depth",
    "mixed-symlinks": "audit-symlinks",
    "escaping-symlink-removed": "expect-link-absent",
    "in-tree-symlink-metadata": "count-gap",
    "clean": "none",
    "clean-empty": "confirm-empty",
    "unclassified": "none",
}

NOMATCH_PAIR = ("unclassified", "none")


def is_legacy_handler(name):
    return any(name.startswith(p) for p in LEGACY_PREFIXES)


def classify(feats):
    """Return ((label, action), step) per the amended precedence."""
    op = feats.get("OP")
    pr = feats.get("PR")
    h = set(feats.get("H") or [])
    hf = set(feats.get("HF") or [])
    g = set(feats.get("G") or [])
    d = set(feats.get("D") or [])
    be = feats.get("BE")
    sr = (feats.get("SR") == "yes") or feats.get("SR") is True
    p = feats.get("P") or 0

    f = {name for name in h if name.startswith(SQUASHFS_PREFIX)}
    l = {name for name in f if is_legacy_handler(name)}
    hf_eff = (hf or f) or set()

    # 1
    if op != "extract_firmware" or pr != "unblob":
        return NOMATCH_PAIR, 1
    # 2
    if not f and "depth-limited" in g:
        return ("container-depth-limited", "raise-depth"), 2
    # 3
    if not f:
        return ("no-squashfs-chunk", "inspect-input"), 3
    # 4
    if "missing-extractor-dependency" in g:
        if BE_DEPENDENCY in d:
            return ("dep-missing-be", "install-extractor-be"), 4
        if LE_DEPENDENCY in d:
            return ("dep-missing-le", "install-extractor-le"), 4
    # 5
    if "extractor-failure" in g and p > 0:
        return ("partial-body-failure", "salvage-partial"), 5
    # 6
    if "extractor-failure" in g and p == 0 and be == "no" \
            and AVM_HANDLER in hf_eff:
        return ("avm-marker-be-dropped", "wrap-extractor-be"), 6
    # 7
    if "extractor-failure" in g and p == 0 and (hf_eff & l):
        return ("legacy-body-failure", "cross-read-legacy"), 7
    # 8
    if "extractor-failure" in g and p == 0:
        return ("body-extractor-failure", "preserve-failure"), 8
    # 9
    if "unknown-chunk-handler" in g:
        return ("unknown-residue", "isolate-residue"), 9
    # 10
    if "depth-limited" in g:
        return ("depth-limited", "raise-depth"), 10
    # 11
    if sr and "unpublished-entry" in g:
        return ("mixed-symlinks", "audit-symlinks"), 11
    # 12
    if sr and not g:
        return ("escaping-symlink-removed", "expect-link-absent"), 12
    # 13
    if g == {"unpublished-entry"}:
        return ("in-tree-symlink-metadata", "count-gap"), 13
    # 14
    if not g:
        return ("clean" if p > 0 else "clean-empty",
                "none" if p > 0 else "confirm-empty"), 14
    # 15
    return NOMATCH_PAIR, 15


def pair_of(feats):
    pair, step = classify(feats)
    return pair
