#!/usr/bin/env python3
"""R42-C2 held-out SquashFS carrier generator, table-v4 classes (round 42).

ROUND 42 (v4) adds, over the frozen round-41 v3 generator:
  * LEGACY classes built from PINNED unblob 26.6.4 test fixtures (MIT; commit
    ``1fcc7a0a584a70a96c31f5a276c20944d199a089``): ``legacy-clean``,
    ``legacy-dep-missing-be``, ``legacy-dep-missing-le``, ``legacy-body-failure``
    and ``legacy-partial``.  The carrier bytes are a pinned fixture (v1-v3
    families: ``squashfs_v1``, ``squashfs_v2``, ``squashfs_v2_nonstandard``,
    ``squashfs_v3``, ``squashfs_v3_ddwrt``, ``squashfs_v3_broadcom``,
    ``squashfs_v3_nonstandard``; the ``squashfs_v3_adaptive`` fixtures resolve to
    plain ``squashfs_v3``) optionally with a pinned 4-byte zero window that makes
    sasquatch fail.  The fixture choice is drawn from the seed (BE and LE strata
    separately, see ``fixture_for``), so a table that hard-codes one v3 handler
    loses.
  * ``combo`` widens from 12 to 24 carriers and gains a FAMILY factor
    (``v4`` / ``legacy`` / ``legacy+v4``): a generated v4 image, a pinned legacy
    fixture, or a legacy fixture padded to 4096 followed by a generated v4 image.
    The declared tuple is still computed from the factors; no named-class tuple
    is consulted.
  * R41-CL1 FIX: the binding tuple is written under EXACTLY ONE key,
    ``declared_features``, for every class including combos.  There is no
    ``declared`` key and ``class_expected`` carries no ``features`` key; the two
    facts outside the binding live in ``declared_extras``.  ``--verify`` reads
    ``declared_features`` (never a second spelling).
  * ``--verify`` regenerates: every carrier and every manifest byte is rebuilt
    from the seed into a fresh directory and compared, so "byte-identical
    regeneration" is a checked property, not a claim.
  * ACTION vocabulary ``draft42`` is the round-42 precedence text's own tokens
    (rule 1-13), including the new ``legacy-body-failure -> cross-read-legacy``.

ROUND 41 (v3) adds, over the frozen round-40 v2 generator:
  * five COMBINED classes: ``partial-in-tree`` (partial body failure + in-tree
    symlink), ``partial-mixed`` (partial failure + in-tree + escaping symlink),
    ``depth-limited-alone`` (a nested SquashFS image file inside the carrier,
    ``--max-depth 1``, no symlinks), ``depth-limited-in-tree`` and
    ``depth-limited-mixed``.  All five carry the precedence trap the v3 table
    must survive: some rule earlier in the precedence list owns the combined gap
    set, so a table that matches the symlink-only or the failure-only row loses.
  * per-class REA parameters: ``max_depth`` is recorded per class (3, REA's
    default, for the v2 classes; 1 for the three depth-limited classes) and is
    passed explicitly, so the envelope's ``parameters.max_depth`` is evidence
    rather than an accident of the CLI default.
  * ``class_expected``: the generator's own expectation (label, action AND the
    feature tuple the class is supposed to reach) is recorded per carrier.  It
    is a CROSS-CHECK, never the scored label: the scored labels come from the
    frozen independent evaluator, and ``--verify`` reports every disagreement.
  * R40-CL4: the partial-body recipe is pinned by the DAMAGED BLOCK'S COMPRESSED
    LENGTH (``MAX_DAMAGED_BLOCK``), not by the compressor.  MH-4 measured that a
    zeroed block of 26-136 B fails on gzip and xz, while a zeroed block of
    ~1.7 KiB is absorbed by the decompressor fallback and lands ``clean``; the
    damage report carries the damaged block list, its byte total and ``pin``, and
    the recipe skips every block above the ceiling instead of silently shipping a
    carrier whose only damaged block is absorbed.
The v2 body (image writer adapter, stdlib SquashFS reader, tree material,
envelope parsing) is unchanged where v3 does not need it, so the round-40
carrier bytes stay reproducible for the 13 v2 classes.

Every byte this script emits is a pure function of ``--seed`` (the freeze commit
hash).  Structure comes from ``random.Random(int(seed[:16], 16) ^ (class_index
* 1000 + k))``; file contents come from a SHA-256 counter stream keyed by
(seed, class, k, relative path), so images stay reproducible across Python and
liblzma point releases rather than only inside one interpreter build.  No clock,
no ``os.urandom``, no directory-listing order, no host-specific input.

Two replicates per class.  Within a class the replicates differ only in
non-decision features: ``k == 1`` is gzip and ``k == 2`` is xz, the tree differs
(different RNG stream), and for the classes whose table row is
``squashfs_v4_*`` the endianness also differs (``k == 1`` big-endian, ``k == 2``
little-endian).  A class whose row pins one endianness or the AVM marker keeps
its endianness in both replicates.  The manifest records the axes.

Expected (label, action) pairs are assigned here, from the class, BEFORE any
REA run; ``--run`` only fills envelopes.  The label is fixed by the class.  The
action token is selected from one of the wave-1 candidate vocabularies
(``--actions-set``) and can be validated against the frozen
``<!-- sqfs-triage-actions: ... -->`` line (``--actions-file``); carriers do not
depend on tokens, so a rebind changes manifest.json only.

Usage
    python3 -I -B heldout-gen-v3.py --seed HEX --out DIR [--classes a,b,...] [--run]
    python3 -I -B heldout-gen-v3.py --seed HEX --selftest
    python3 -I -B heldout-gen-v3.py --seed HEX --out DIR --run --verify   (dev proof)

``--run`` executes one REA 6.5.0 operation per carrier:
  * ``extract-firmware`` in the ``after`` arm (PATH unchanged);
  * ``extract-firmware`` in the ``before`` arm (``$HOME/.local/bin`` removed
    from the child PATH, so neither sasquatch binary resolves);
  * the ``out-of-domain`` class runs ``out_of_domain_run``, which invokes a
    non-extract-firmware operation (``--ood-op``, default
    ``inspect-firmware-regions``) on the same carrier.
Every ``extract-firmware`` argv carries an explicit ``--max-depth`` (3 for the
v2 classes, 1 for the three depth-limited classes); the value is in the manifest
and reappears as the envelope's ``parameters.max_depth``.

Layout
    DIR/manifest.json        {seed, generator, action_vocabulary, classes, rea, carriers:[...]}
    DIR/<id>/carrier.sqsh
    DIR/<id>/tree.json       oracle: directories, regular files (path, sha256, size), symlinks
    DIR/<id>/envelope.json   (--run) the `data` object of the CLI envelope
    DIR/<id>/rea-full.json   (--run) the whole {ok, data, meta} envelope
    DIR/<id>/run.json        (--run) arm/operation, exit code, digest binding, shape summary

With ``--gzip`` the two envelope files are written as ``.json.gz`` (mtime 0) so a
36-carrier delivery stays small; the JSON payload is unchanged.  ``--verify``
prints the per-class feature table (class | observed tuple | expected tuple |
match) and exits 1 if any envelope misses its own class's expectation.

The image writer is loaded by path (``--gen``, default tools/round-39/gen-squashfs.py).
Its block encoder is replaced as in round 39: the round-37 prototype writes bare
LZMA2 streams that sasquatch 4.5.1 rejects, and advertises comp id 2 (LZMA)
instead of 4 (xz).

Damage recipes (``bytes -> bytes``; the input image is never mutated).  The
reader below is a pure-stdlib SquashFS 4.0 parser; every offset comes from the
image itself, so a recipe works for both endiannesses and both compressors.
``corrupt_partial`` and ``empty_tree`` are the hooks the sibling recon seats
(R40C2ReconPartial, R40C2ReconEmpty) specified; the implementations here are
self-contained so a frozen carrier set never depends on a wave artifact.
"""
from __future__ import annotations

import argparse
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import lzma
import os
import posixpath
import random
import shutil
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zlib

# A run without -B must not drop tools/round-39/__pycache__ into the lane.
sys.dont_write_bytecode = True

VERSION = 'r42-c2-v4'
ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
CARRIERS_PER_CLASS = 2
REA_PACKAGE = 'rea-agents@6.5.0'
BLOCK_ENCODER = ('gzip=zlib level 9, comp_id 1; xz=.xz container/CRC32, '
                 'comp_id 4 (replaces stock raw-LZMA2 and comp_id 2)')
DEFAULT_OOD_OP = 'inspect-firmware-regions'
# REA's own default; the v2 classes keep it and the depth-limited classes cut to 1.
DEFAULT_MAX_DEPTH = 3
# R40-CL4 pin.  MH-4 measured (round-40 w2 R40W2MistakeHunt §3): a 0x00-filled
# block of 26-136 B makes gzip and xz fail (extractor-failure + published files),
# while a 0x00-filled block of ~1.7 KiB is ABSORBED by sasquatch's decompressor
# fallback chain and the run lands `clean` with a corrupt file on disk.  The
# determinant is the damaged block's compressed length, not the compressor, so
# the recipe refuses a target above this ceiling instead of shipping a carrier
# that silently reads clean.
MAX_DAMAGED_BLOCK = 136   # measured absorption edge: 140 B was absorbed (R42 dev arm H30)
PARTIAL_FILL = 0x00

# ---------------------------------------------------------------------------
# Action maps (closed vocabularies).  The (label, action) pair is scored against
# the frozen table, so the token must be the table's token, not a paraphrase.
# Wave 1 produced three candidate vocabularies for the same 11 labels.  The
# generator carries each verbatim; the freeze selects one with --actions-set, or
# validates the selected map against the frozen
# `<!-- sqfs-triage-actions: ... -->` line with --actions-file.  Carriers never
# depend on tokens: rebinding changes manifest.json only (no carrier bytes).
#   tabledraft    artifacts/R40C2TableDraft/block.md:30 (the table block's line)
#   interp        artifacts/R40C2Interp/v2-block.md:2 (interpreter prototype)
#   actionreview  artifacts/R40C2ActionReview/actions.md sections 1-2
# The 12th label `unclassified` is the domain guard / no-match answer in all
# three; the out-of-domain carrier's pair is (unclassified, none).
# ROUND 41: the 13th label `depth-limited` is new, so none of the wave-1
# vocabularies has a row for it.  The tokens below are the generator's wave-1
# PROPOSALS; the table author owns the real ones, and the freeze binds them with
# --actions-set/--actions-file (a mismatch is a loud exit, carriers unaffected).
# `partial-in-tree`/`partial-mixed` reuse the `partial-body-failure` row because
# the precedence text gives them that label (see EXPECTATIONS).
# ---------------------------------------------------------------------------
ACTION_SETS = {
    # ROUND 42: the round-42 precedence text's own (label, action) pairs, rule
    # 1-13, verbatim.  This is the DEFAULT for v4: the labels and tokens scored
    # against the frozen table must be the table's own, and the round-41 sets
    # below predate `legacy-body-failure` and cannot express it.
    # Precedence text: plans/round-42-claims.md `## R42-C2` step list.
    'draft42': {
        'unclassified': 'none',
        'container-depth-limited': 'raise-depth',
        'no-squashfs-chunk': 'inspect-input',
        'dep-missing-be': 'install-extractor-be',
        'dep-missing-le': 'install-extractor-le',
        'partial-body-failure': 'salvage-partial',
        'avm-marker-be-dropped': 'wrap-extractor-be',
        'legacy-body-failure': 'cross-read-legacy',
        'body-extractor-failure': 'preserve-failure',
        'unknown-residue': 'isolate-residue',
        'depth-limited': 'raise-depth',
        'mixed-symlinks': 'audit-symlinks',
        'escaping-symlink-removed': 'expect-link-absent',
        'in-tree-symlink-metadata': 'count-gap',
        'clean': 'none',
        'clean-empty': 'confirm-empty',
    },
    'tabledraft': {
        'clean': 'accept',
        'clean-empty': 'accept',
        'escaping-symlink-removed': 'expect-removed',
        'in-tree-symlink-metadata': 'resolve-unpublished',
        'mixed-symlinks': 'expect-removed-and-unpublished',
        'dep-missing-be': 'install-sasquatch-v4be',
        'dep-missing-le': 'install-sasquatch',
        'avm-marker-be-dropped': 'rerun-with-be-wrapper',
        'body-extractor-failure': 'keep-failure-evidence',
        'partial-body-failure': 'accept-partial-published',
        'depth-limited': 'descend-nested',
        'no-squashfs-chunk': 'check-superblock',
        'unclassified': 'none',
    },
    'interp': {
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
        'depth-limited': 'raise-depth',  # L1 freeze binding: SKILL v3 action line (round 41)
        'no-squashfs-chunk': 'inspect-input',
        'unclassified': 'none',
    },
    'actionreview': {
        'clean': 'match-oracle',
        'clean-empty': 'match-oracle',
        'escaping-symlink-removed': 'expect-absent',
        'in-tree-symlink-metadata': 'count-gaps',
        'mixed-symlinks': 'expect-absent-and-count-gaps',
        'dep-missing-be': 'install-dependency-rerun',
        'dep-missing-le': 'install-dependency-rerun',
        'avm-marker-be-dropped': 'wrapper-be-then-remove',
        'body-extractor-failure': 'keep-evidence-quarantine',
        'partial-body-failure': 'keep-evidence-match-published',
        'depth-limited': 'rerun-deeper-then-match',
        'no-squashfs-chunk': 'check-superblock',
        # R40C2ActionReview row 0 is a guard row: label unclassified, action
        # `not-comparable`; `none` stays the no-match default of its table.
        'unclassified': 'not-comparable',
    },
}
DEFAULT_ACTION_SET = 'draft42'  # L1 freeze binding: round-42 precedence text (rule 1-13)
NO_MATCH_TOKEN = 'none'
ACTIONS_LINE_TAG = '<!-- sqfs-triage-actions:'
ACTIONS = ACTION_SETS[DEFAULT_ACTION_SET]
ACTION_SET_NAME = DEFAULT_ACTION_SET
ACTION_SOURCE = None

# ---------------------------------------------------------------------------
# Recipe table.  ``label`` is the label the frozen interpreter must produce and
# the key into ACTIONS for the action half of the pair; the recipe key is the
# generator-side ``class``.
#
#   endian      le | be | avm | k   (k: k==1 be, k==2 le)
#               avm = BE magic with mkfs_time := bytes_used, the marker that
#               makes unblob drop ``-be`` (a marker-only standard-BE body, NOT
#               the genuine AVM layout -- that is R40-C1's ground)
#   arm         after | before  (PATH arm for the REA extract-firmware run)
#   comp        'k' (k==1 gzip, k==2 xz) or a fixed choice
#   tree        'random' | 'empty'
#   content     'stream' (incompressible SHA stream) | 'pattern' (compressible)
#   symlinks    kinds: 'escaping' -> relative target leaving the image root,
#               removed by unblob and reported MaliciousSymlinkRemoved with no
#               gap; 'in-tree' -> relative target resolving inside the root,
#               kept as metadata and reported as one unpublished-entry gap
#   corruption  key into CORRUPTIONS, applied to the finished image bytes
#   ood         True: run ``out_of_domain_run`` instead of extract-firmware
#   rea         {'max_depth': n} -- the extraction depth passed to REA.  Absent
#               means DEFAULT_MAX_DEPTH (3, REA's default); the three
#               depth-limited classes cut to 1 so the depth cap does the work.
#   nested      True: a nested SquashFS v4 image is written as a regular file
#               inside the carrier tree, so the depth cap is material (there is
#               a real chunk behind it) and the file is part of the oracle.
#   link_placement  'rng' (default) or 'root-first'.  'root-first' places every
#               link at the image root with a name starting '-', which sorts
#               before every ALPHABET name (ASCII 0x2d), so the link is
#               extracted BEFORE the damaged block fails and the combined
#               gap set {extractor-failure, unpublished-entry} is real rather
#               than an accident of directory order.
# ---------------------------------------------------------------------------
RECIPES = {
    'clean-be': dict(label='clean', endian='be',
                     arm='after', comp='k', tree='random', content='stream',
                     symlinks=(), corruption=None),
    'clean-le': dict(label='clean', endian='le',
                     arm='after', comp='k', tree='random', content='stream',
                     symlinks=(), corruption=None),
    # A clean image with zero regular files: P=0 with no gap.  Distinct from
    # both ``clean`` (the v1 row requires P>0) and ``no-squashfs-chunk``
    # (handler present here).  R39-CL3 D2.
    'clean-empty': dict(label='clean-empty',
                        endian='k', arm='after', comp='k', tree='empty',
                        content='stream', symlinks=(), corruption=None),
    'escaping-symlink-removed': dict(
        label='escaping-symlink-removed',
        endian='k', arm='after', comp='k', tree='random', content='stream',
        symlinks=('escaping',), corruption=None),
    'in-tree-symlink-metadata': dict(
        label='in-tree-symlink-metadata',
        endian='k', arm='after', comp='k', tree='random', content='stream',
        symlinks=('in-tree',), corruption=None),
    # Both link kinds in one image: the escaping link is removed (SR=yes) and
    # every in-tree link adds one unpublished-entry gap, so a table whose
    # escaping row matches on SR alone reports the wrong action.  R39-CL2.
    'mixed-symlinks': dict(label='mixed-symlinks',
                           endian='k',
                           arm='after', comp='k', tree='random',
                           content='stream', symlinks=('escaping', 'in-tree'),
                           corruption=None),
    'dep-missing-be': dict(label='dep-missing-be',
                           endian='be',
                           arm='before', comp='k', tree='random',
                           content='stream', symlinks=(), corruption=None),
    'dep-missing-le': dict(label='dep-missing-le',
                           endian='le',
                           arm='before', comp='k', tree='random',
                           content='stream', symlinks=(), corruption=None),
    'avm-marker-be-dropped': dict(label='avm-marker-be-dropped',
                                  endian='avm', arm='after', comp='k',
                                  tree='random', content='stream', symlinks=(),
                                  corruption=None),
    # The extractor ran with -be and failed before writing any file.
    'body-extractor-failure': dict(label='body-extractor-failure',
                                   endian='be', arm='after', comp='k',
                                   tree='random', content='pattern',
                                   symlinks=(), corruption='zero-id-table'),
    # The extractor ran with -be, wrote every file before the damaged one, then
    # failed: published files > 0.  R39-CL3 D1.
    # R41 (R40-CL4): the round-40 pin was the COMPRESSOR (gzip only) because a
    # zeroed single-block xz file had extracted clean in one dry run.  MH-4 then
    # measured the real determinant: the damaged block's COMPRESSED LENGTH (26-136
    # B fails on gzip and xz; ~1.7 KiB is absorbed by the fallback chain).  v3
    # restores comp='k' and pins the length in corruption_partial.
    'partial-body-failure': dict(label='partial-body-failure',
                                 endian='be', arm='after', comp='k',
                                 tree='random', content='pattern',
                                 symlinks=(), corruption='partial'),
    'no-squashfs-chunk': dict(label='no-squashfs-chunk',
                              endian='k',
                              arm='after', comp='k', tree='random',
                              content='stream', symlinks=(),
                              corruption='bad-major'),
    # A non-extract-firmware operation on a SquashFS carrier:
    # inspect_firmware_regions / provider binwalk.  The domain guard must
    # refuse it instead of reading it as a squashfs outcome.  R39-CL1.
    'out-of-domain': dict(label='unclassified',
                          endian='k', arm='after', comp='k', tree='random',
                          content='stream', symlinks=(), corruption=None,
                          ood=True),
    # -----------------------------------------------------------------------
    # ROUND 41 combined classes.  Each one reaches a gap set that TWO table rows
    # could match, so the label is decided by the precedence order alone:
    #   * partial + in-tree link: G = {extractor-failure, unpublished-entry},
    #     P > 0 -- rule 4 (partial body failure "whatever other gaps accompany
    #     it") wins over the symlink rows; a table that matches the
    #     unpublished-entry row loses.
    #   * partial + in-tree + escaping: same G plus SR=yes -- rule 4 wins over
    #     the mixed-symlinks row (rule 8).
    #   * depth-limited (+ links): G = {depth-limited[, unpublished-entry]},
    #     no extractor-failure, P > 0 -- rule 7 wins over the symlink rows and
    #     over rule 11.
    # The links are 'root-first' for the partial classes: the damaged block
    # failure must not be able to pre-empt the link's extraction.
    # -----------------------------------------------------------------------
    'partial-in-tree': dict(label='partial-body-failure',
                            endian='be', arm='after', comp='k',
                            tree='random', content='pattern',
                            symlinks=('in-tree',), corruption='partial',
                            link_placement='root-first'),
    'partial-mixed': dict(label='partial-body-failure',
                          endian='be', arm='after', comp='k',
                          tree='random', content='pattern',
                          symlinks=('in-tree', 'escaping'),
                          corruption='partial',
                          link_placement='root-first'),
    'depth-limited-alone': dict(label='depth-limited',
                                endian='k', arm='after', comp='k',
                                tree='random', content='stream',
                                symlinks=(), corruption=None,
                                nested=True, rea={'max_depth': 1}),
    'depth-limited-in-tree': dict(label='depth-limited',
                                  endian='k', arm='after', comp='k',
                                  tree='random', content='stream',
                                  symlinks=('in-tree',), corruption=None,
                                  nested=True, rea={'max_depth': 1}),
    'depth-limited-mixed': dict(label='depth-limited',
                                endian='k', arm='after', comp='k',
                                tree='random', content='stream',
                                symlinks=('in-tree', 'escaping'),
                                corruption=None,
                                nested=True, rea={'max_depth': 1}),
    # --- round-41 amendments (L1 binding, `## Amendments after wave-1 recon`) --
    # The same id-table damage as `body-extractor-failure`, on LITTLE-endian
    # bytes: unblob runs plain `sasquatch -le`, so BE = no with handler
    # squashfs_v4_le.  Rule 5 needs handler squashfs_v4_be, so a table that reads
    # "failed + P=0 + BE=no" without the handler column labels this
    # avm-marker-be-dropped instead of body-extractor-failure.
    'body-extractor-failure-le': dict(label='body-extractor-failure',
                                      endian='le', arm='after', comp='k',
                                      tree='random', content='pattern',
                                      symlinks=(), corruption='zero-id-table'),
    # Failure AND depth cut in one envelope, at --max-depth 1: a valid EMPTY
    # squashfs (its extraction dir is the depth ceiling, publishes nothing) is
    # followed at offset 4096 by a zero-id-table squashfs that fails.  Measured
    # tuple: G={extractor-failure, depth-limited}, P=1 (the carve of the second
    # chunk; the layout is in the manifest), BE=yes on BE / no on LE.  Rule 4
    # (extractor-failure with P>0) therefore owns the label even though the
    # depth row is also matchable -- the whole point of the class.
    'failure-depth-limited': dict(label='partial-body-failure',
                                  endian='k', arm='after', comp='k',
                                  tree=None, content='pattern',
                                  symlinks=(), corruption=None,
                                  layout='two-chunk', rea={'max_depth': 1}),
    # -----------------------------------------------------------------------
    # ROUND 42 legacy classes (v1-v3 handler family), built from the PINNED
    # unblob 26.6.4 fixtures in fixtures.json -- never from a generated image,
    # because no writer in the lane emits v1-v3 and a hand-built v3 image would
    # be a lane artifact rather than a third-party input.  `kind='legacy'`
    # switches build_carrier onto build_legacy_carrier; the fields below are the
    # ones that class needs, and `stratum` is the fixture pool its replicate
    # draws from ('le'/'be' or 'any').
    #
    # Labels are the round-42 precedence text's answers, not the class names:
    #   legacy-clean            G=0, P>0                       -> rule 12 clean
    #   legacy-dep-missing-be   BE chunk, sasquatch stripped   -> rule 3
    #   legacy-dep-missing-le   LE chunk, sasquatch stripped   -> rule 3
    #   legacy-body-failure     damaged legacy chunk, P=0      -> rule 6
    #   legacy-partial          clean legacy chunk + damaged   -> rule 4
    #                           legacy chunk, P>0
    # MEASURED (this wave, REA 6.5.0 + unblob 26.6.4 + sasquatch 4.5.1): a
    # v1-v3 BIG-ENDIAN chunk also runs plain `sasquatch -be`, and the failing
    # Command reports its OWN executable, so its dependency set is exactly
    # ['sasquatch'] -- rule 3 therefore answers (dep-missing-le,
    # install-extractor-le) for a big-endian legacy chunk too.  That is the
    # draft's own TBC; the class name names the CHUNK's endianness, and the
    # declared tuple (not the name) is what the counter binds.
    'legacy-clean': dict(label='clean', kind='legacy', stratum='any',
                         arm='after', damage=False, pair=False, tree='fixture',
                         content='fixture', symlinks=(), corruption=None),
    'legacy-dep-missing-be': dict(label='dep-missing-le', kind='legacy',
                                  stratum='be', arm='before', damage=False,
                                  pair=False, tree='fixture',
                                  content='fixture', symlinks=(),
                                  corruption=None),
    'legacy-dep-missing-le': dict(label='dep-missing-le', kind='legacy',
                                  stratum='le', arm='before', damage=False,
                                  pair=False, tree='fixture',
                                  content='fixture', symlinks=(),
                                  corruption=None),
    'legacy-body-failure': dict(label='legacy-body-failure', kind='legacy',
                                stratum='any', arm='after', damage=True,
                                pair=False, tree='fixture', content='fixture',
                                symlinks=(), corruption='fixture-damage'),
    'legacy-partial': dict(label='partial-body-failure', kind='legacy',
                           stratum='any', arm='after', damage=True, pair=True,
                           tree='fixture', content='fixture', symlinks=(),
                           corruption='fixture-damage'),
    # -----------------------------------------------------------------------
    # ROUND 42 amendment A1: the two decisions the v3 table gets wrong on real
    # REA envelopes.
    #   container-depth-limited  a SquashFS chunk that sits BELOW the depth
    #     budget inside a container (tar member).  At --max-depth 1 REA sees
    #     H={'tar'}, G={depth-limited}, F=0, P=1 (the member) -- v3 answers
    #     no-squashfs-chunk/inspect-input.  MEASURED at depth 1; at depth 3 the
    #     member is opened and the run is `clean`, which is why max_depth is
    #     pinned to 1 for this class.  k=1 wraps a generated v4 image, k=2 wraps
    #     a pinned legacy fixture (the handler INSIDE the tar is never visible at
    #     this depth, so the two replicates differ only in the wrapped body).
    #   unknown-residue  a SquashFS image followed by NON-PADDING bytes.  REA
    #     mints G={unknown-chunk-handler} for the tail chunk and publishes
    #     `<start>-<end>.unknown`, and the tail's own carve makes P > 0 --
    #     v3 answers unclassified.  MEASURED at depth 3 with a 64 B seeded tail
    #     after the 4 KiB section; P = image files + the .unknown carve.
    'container-depth-limited': dict(label='container-depth-limited',
                                    kind='container', stratum='any',
                                    arm='after', damage=False, pair=False,
                                    tree='random', content='stream',
                                    symlinks=(), corruption=None,
                                    rea={'max_depth': 1}),
    'unknown-residue': dict(label='unknown-residue', kind='residue',
                            stratum='any', arm='after', damage=False,
                            pair=False, tree='random', content='stream',
                            symlinks=(), corruption=None),
}

DEFAULT_CLASSES = tuple(RECIPES) + ('combo',)

# ---------------------------------------------------------------------------
# ROUND 42: pinned legacy fixtures (unblob 26.6.4, MIT)
#
# A v1-v3 carrier cannot be generated: the lane writer emits SquashFS 4.0 only,
# and a hand-built v3 image would be a lane artifact rather than a third-party
# input.  So the legacy classes are built from the unblob 26.6.4 integration
# fixtures, pinned by URL + sha256 in ``fixtures.json`` (committed beside this
# script; the L1 proposal is ``corpus/evidence/round-42/c2/fixtures/`` when the
# bytes are committed instead of fetched).
#
# Every pinned fixture is MIT-licensed and 320-4096 B.  Damage is NOT derived at
# run time: no probe is run during generation, because a carrier must be a pure
# function of (pins, seed) and must not depend on the sasquatch build in the
# environment.  ``damage_offset``/``damage_len`` are pre-verified 4-byte zero
# windows (wave-1 sweep + REA confirmation; see the wave-1 report §4) and
# ``--verify`` re-checks the resulting envelope, not the recipe.
# ---------------------------------------------------------------------------
FIXTURE_PINS_NAME = 'fixtures.json'
FIXTURE_PIN_PROJECT = 'onekey-sec/unblob'
FIXTURE_PIN_COMMIT = '1fcc7a0a584a70a96c31f5a276c20944d199a089'
FIXTURE_URL_BASE = ('https://media.githubusercontent.com/media/onekey-sec/unblob/'
                    '26.6.4/tests/integration/filesystem/squashfs')
FIXTURE_TWO_CHUNK_PAD = 4096


class FixturePinError(SystemExit):
    """A pinned-fixture problem: loud, before any carrier is built."""


def default_fixture_pins():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        FIXTURE_PINS_NAME)


# Set by main(): the pin file actually read, and the value the manifest reports
# (a lane-relative path when the file sits beside this script, so the manifest
# does not carry a host-local absolute path).
FIXTURE_PINS_PATH = None
FIXTURE_PINS_LOGICAL = FIXTURE_PINS_NAME


def load_fixture_pins(path):
    """Read the pin list and check the header the carrier bytes depend on."""
    with open(path, encoding='utf-8') as handle:
        pins = json.load(handle)
    meta = pins.get('pinned') or {}
    for key, want in (('project', FIXTURE_PIN_PROJECT),
                      ('commit', FIXTURE_PIN_COMMIT),
                      ('url_base', FIXTURE_URL_BASE)):
        if meta.get(key) != want:
            raise FixturePinError(
                f'{path}: pinned {key} is {meta.get(key)!r}; this generator is '
                f'written against {want!r}.  A different pin changes the carrier '
                f'bytes, so it must be a deliberate rebind, not a silent one.')
    fixtures = pins.get('fixtures') or []
    if len(fixtures) < 2:
        raise FixturePinError(f'{path}: {len(fixtures)} fixture(s) pinned, need >= 2')
    seen, digests = set(), set()
    for entry in fixtures:
        for field in ('id', 'handler', 'endian', 'path', 'file', 'sha256',
                      'size', 'compression', 'damage_offset', 'damage_len'):
            if field not in entry:
                raise FixturePinError(
                    f'{path}: fixture {entry.get("id")!r} lacks {field!r}')
        if entry['id'] in seen:
            raise FixturePinError(f'{path}: duplicate fixture id {entry["id"]!r}')
        if entry['sha256'] in digests:
            raise FixturePinError(
                f'{path}: fixture {entry["id"]!r} repeats sha256 '
                f'{entry["sha256"]}: one id per distinct image')
        seen.add(entry['id'])
        digests.add(entry['sha256'])
        if entry['endian'] not in ('be', 'le'):
            raise FixturePinError(
                f'{path}: fixture {entry["id"]!r} endian {entry["endian"]!r}')
        if not (0 <= entry['damage_offset']
                and entry['damage_offset'] + entry['damage_len'] <= entry['size']):
            raise FixturePinError(
                f'{path}: fixture {entry["id"]!r} damage window '
                f'{entry["damage_offset"]}+{entry["damage_len"]} outside {entry["size"]} B')
        if entry['size'] > FIXTURE_TWO_CHUNK_PAD:
            raise FixturePinError(
                f'{path}: fixture {entry["id"]!r} is {entry["size"]} B, above the '
                f'{FIXTURE_TWO_CHUNK_PAD} B two-chunk pad')
    by_endian = {side: [f for f in fixtures if f['endian'] == side]
                 for side in ('le', 'be')}
    for side, pool in by_endian.items():
        if not pool:
            raise FixturePinError(f'{path}: no {side.upper()} fixture pinned')
    return pins


def fixture_url(entry):
    return f'{FIXTURE_URL_BASE}/{entry["path"]}'


def fixture_bytes(entry, fixtures_dir, cache_dir, fetch):
    """Resolve one pinned fixture: committed copy, cache, or the pinned URL.

    Every candidate is sha256-checked against the pin.  The URL is only used
    with ``--fetch``; otherwise a missing fixture is a loud exit naming both the
    URL and the committed-copy directory the freeze should use.
    """
    # The committed copy is named `<id>--<file>` because two fixture ids share a
    # basename with DIFFERENT bytes (v2-be vs v2ns-be are both
    # `squashfs_v2.0_be.bin`), so the bare name is ambiguous on disk.  A bare
    # name is still accepted for a unique fixture.
    candidates = []
    if fixtures_dir:
        candidates.append(os.path.join(fixtures_dir,
                                       f'{entry["id"]}--{entry["file"]}'))
        candidates.append(os.path.join(fixtures_dir, entry['file']))
    candidates.append(os.path.join(cache_dir, f'{entry["id"]}--{entry["file"]}'))
    for path in candidates:
        if os.path.isfile(path):
            with open(path, 'rb') as handle:
                payload = handle.read()
            digest = hashlib.sha256(payload).hexdigest()
            if digest != entry['sha256']:
                raise FixturePinError(
                    f'{path}: sha256 {digest} != pinned {entry["sha256"]}; the '
                    f'fixture is a frozen input, so a mismatch cannot be carried')
            return payload, path
    url = fixture_url(entry)
    if not fetch:
        raise FixturePinError(
            f'fixture {entry["id"]!r} found in neither '
            f'{fixtures_dir or "(no --fixtures-dir)"} nor {cache_dir}.  '
            f'Pass --fetch to download {url} (sha256 {entry["sha256"]}), or commit '
            f'the pinned copies once and pass --fixtures-dir.')
    os.makedirs(cache_dir, exist_ok=True)
    dest = candidates[-1]
    request = urllib.request.Request(url, headers={'User-Agent': 'kaidoku-r42-c2'})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise FixturePinError(f'fetching {url} failed: {exc}') from None
    digest = hashlib.sha256(payload).hexdigest()
    if digest != entry['sha256']:
        raise FixturePinError(
            f'{url}: downloaded sha256 {digest} != pinned {entry["sha256"]}')
    with open(dest, 'wb') as handle:
        handle.write(payload)
    return payload, dest


def apply_fixture_damage(payload, entry):
    """Zero the pinned window: the damage recipe for every legacy class."""
    window = entry['damage_len']
    start = entry['damage_offset']
    out = bytearray(payload)
    out[start:start + window] = bytes(window)
    return bytes(out)


def fixture_pair(seed, name, k, pins, used=None):
    """The seeded fixture choice for one legacy replicate.

    ``stratum`` 'le'/'be' pins the pool; 'any' rotates with the replicate index
    (k == 1 -> LE, k == 2 -> BE) so both endianness strata are exercised whatever
    the seed draws.  A pair class (``legacy-partial``) draws its CLEAN fixture
    from that pool and its DAMAGED one from the complement, so the two chunks
    never carry identical bytes and the damaged chunk can have a different
    handler from the clean one.
    """
    recipe = RECIPES[name]
    stratum = recipe.get('stratum') or 'any'
    if stratum in ('le', 'be'):
        pool = [f for f in pins['fixtures'] if f['endian'] == stratum]
    else:
        want = 'le' if k == 1 else 'be'
        pool = [f for f in pins['fixtures'] if f['endian'] == want]
    if not pool:
        raise FixturePinError(f'{name}: no pinned fixture for stratum {stratum!r}')
    key = hashlib.sha256(f'{seed}:fixture:{name}:{k}'.encode()).hexdigest()[:16]
    rng = random.Random(int(key, 16))
    # Prefer a fixture this manifest has not used yet: two legacy carriers built
    # from the same pinned bytes with the same damage window would be byte- and
    # tuple-identical, which weakens the set without adding a decision.  The
    # exclusion is deterministic (classes are built in RECIPES order), and a
    # drained pool falls back to the full stratum instead of failing.
    # The exclusion key is (bytes, damage state): a DAMAGED carrier of the same
    # fixture is a different image, so only the same fixture in the same state
    # would be a byte- and tuple-identical duplicate.
    def key_of(entry, damaged):
        return f"{entry['sha256']}:{'damaged' if damaged else 'clean'}"

    primary_damaged = bool(recipe.get('damage')) and not recipe.get('pair')
    fresh = [f for f in pool
             if used is None or key_of(f, primary_damaged) not in used] or pool
    primary = fresh[rng.randrange(len(fresh))]
    secondary = None
    if recipe.get('pair'):
        rest = [f for f in pins['fixtures']
                if f['sha256'] != primary['sha256']
                and (used is None or key_of(f, True) not in used)]
        if not rest:
            rest = [f for f in pins['fixtures'] if f['sha256'] != primary['sha256']]
        secondary = rest[rng.randrange(len(rest))]
    if used is not None:
        used.add(key_of(primary, primary_damaged))
        if secondary is not None:
            used.add(key_of(secondary, True))
    return primary, secondary


def legacy_features(recipe, primary, secondary):
    """The binding tuple of one legacy carrier, from its class and its fixtures.

    Measured rules (this wave; REA 6.5.0 / unblob 26.6.4 / sasquatch 4.5.1):
      * a clean v1-v3 fixture lands G = 0 with P > 0 at --max-depth 3;
      * with $HOME/.local/bin off the child PATH the failing Command reports its
        OWN executable (``unblob/extractors/command.py:68-73``) and every v1-v3
        handler runs plain ``sasquatch``, so D = ['sasquatch'] and no argv is
        recorded (BE = 'n/a');
      * a damaged ROOT chunk fails with P = 0 and no carve, and the recorded
        argv is ``-be`` for BE / ``-le`` for LE (BE = 'yes'/'no');
      * a damaged NON-ROOT chunk (offset 4096) also fails but the chunk itself is
        carved and published, so P > 0.
    """
    if recipe.get('pair'):
        handlers = sorted({primary['handler'], secondary['handler']})
        damaged_endian = secondary['endian']
        published = 'nonzero'
        gaps = ('extractor-failure',)
        failed = True
    else:
        handlers = [primary['handler']]
        damaged_endian = primary['endian']
        if recipe.get('arm') == 'before':
            published = 'zero'
            gaps = ('missing-extractor-dependency',)
            failed = True
        elif recipe.get('damage'):
            published = 'zero'
            gaps = ('extractor-failure',)
            failed = True
        else:
            published = 'nonzero'
            gaps = ()
            failed = False
    if recipe.get('arm') == 'before':
        be = 'n/a'  # no child argv is recorded for a dependency failure
    elif not recipe.get('damage'):
        be = 'n/a'  # a successful run records no argv
    else:
        be = 'yes' if damaged_endian == 'be' else 'no'
    return {
        'handler_set': handlers,
        'gap_kinds': sorted(gaps),
        'gap_dependencies': (['sasquatch'] if recipe.get('arm') == 'before' else []),
        'be_argv': be,
        'symlink_removed': False,
        'published': published,
        'extraction_failed': failed,
        'max_depth': (recipe.get('rea') or {}).get('max_depth', DEFAULT_MAX_DEPTH),
    }


# ---------------------------------------------------------------------------
# ROUND 42 (A1): a seeded FACTORIAL family of 24 carriers in which EVERY carrier
# draws at least two DECISION factors.  An N-row lookup of the named class tuples
# can be tied by a table that hard-codes them, so the family draws its factors
# from the seed itself and its expected tuple is COMPUTED from those factors --
# `class_expected` is null because a combo has no class label; only the frozen
# evaluator gives a pair.
#
# Decision factors (each one changes the declared tuple, which is why the count
# of active ones is the calibration strength of the carrier):
#   legacy chunk      the squashfs body is a pinned v1-v3 fixture
#   second v4 chunk   a generated v4 image at offset 4096 next to the legacy one
#   links             in-tree and/or escaping symlink in the v4 tree
#   residue           seeded non-padding bytes after the last 4 KiB section
#   container wrap    the body inside a USTAR tar
#   damage            the body fails its extractor
#   dependency        sasquatch unreachable in the child PATH
#   max_depth 1       the extraction depth budget is 1
# ---------------------------------------------------------------------------
FAMILIES = {'combo': 24}
COMBO_FACTORS = ('base', 'second_v4', 'links', 'residue', 'wrap', 'damage',
                 'dep', 'max_depth', 'endian', 'comp', 'legacy_fixture')
COMBO_LINKS = ('none', 'in-tree', 'escaping', 'both')
COMBO_BASES = ('v4', 'legacy')
COMBO_ID_PREFIX = 'C'
COMBO_MIN_DECISIONS = 2
COMBO_MAX_REDRAWS = 64
V4_HANDLER = {'be': 'squashfs_v4_be', 'le': 'squashfs_v4_le'}


def combo_decisions(factors):
    """The OBSERVABLE decision factors of one draw, as names.

    "Observable" is the point: a container wrap at ``--max-depth 1`` stops the
    inner image from ever being carved, so a dependency or damage factor drawn
    alongside it leaves no trace in the envelope (R42C2ReconLegacy D8).  Counting
    those two as decisions would let a carrier claim two factors while exposing
    one, which is exactly the accounting hole ``combo_unseen_majority`` exists to
    close.  The wrap and the depth cut are themselves observable, so a capped draw
    still reaches the minimum.
    """
    capped = bool(factors['wrap']) and factors['max_depth'] == 1
    active = []
    if factors['wrap']:
        active.append('container wrap')
    if factors['max_depth'] == 1:
        active.append('max_depth 1')
    if factors['residue']:
        active.append('residue')
    if not capped:
        if factors['base'] == 'legacy':
            active.append('legacy chunk')
        if factors['second_v4']:
            active.append('second v4 chunk')
        if factors['links'] != 'none':
            active.append('links')
        if factors['damage']:
            active.append('damage')
        if factors['dep']:
            active.append('dependency')
    return active


def combo_factors(seed, k, pins, variant=0):
    """Draw the factor vector of combo ``k`` from the seed alone.

    One ``random.Random`` keyed by ``sha256('<seed>:combo:<k>')`` -- or
    ``...:r<variant>`` for a redraw -- draws every factor in a FIXED order, then
    the compatibility rules are applied.  The vector is a pure function of the
    seed, the replicate index and the redraw counter: no clock, no host input and
    no measurement.
    """
    key = f'{seed}:combo:{k}' + (f':r{variant}' if variant else '')
    rng = random.Random(int(hashlib.sha256(key.encode()).hexdigest()[:16], 16))
    base = rng.choice(list(COMBO_BASES))
    second = rng.choice([0, 1])
    links = rng.choice(list(COMBO_LINKS))
    residue = rng.choice([0, 1])
    wrap = rng.choice([0, 1])
    damage = rng.choice([0, 1])
    dep = rng.choice([0, 1])
    depth = rng.choice([1, 3])
    endian = rng.choice(['le', 'be'])
    comp = 'gzip' if damage else rng.choice(['gzip', 'xz'])
    fixture = pins['fixtures'][rng.randrange(len(pins['fixtures']))]
    # --- compatibility rules (each one is a MEASURED statement) --------------
    if base == 'v4':
        second = 0           # a second v4 chunk adds no decision the single one lacks
    if base == 'legacy' and not second:
        links = 'none'       # a pinned fixture carries no tree to link in
    if damage and dep:
        damage = 0           # the extractor never runs, so damage is unobservable
    if base == 'legacy' and not second:
        endian, comp = fixture['endian'], 'fixture'
    body_v4 = base == 'v4' or second
    damage_endian = endian if body_v4 else fixture['endian']
    return rng, {
        'base': base,
        'second_v4': second,
        'links': links,
        'residue': residue,
        'wrap': wrap,
        'damage': damage,
        'dep': dep,
        'max_depth': depth,
        'endian': endian,
        'comp': comp,
        'legacy_fixture': fixture['id'],
        'legacy_handler': fixture['handler'],
        'body_v4': body_v4,
        'two_chunk': base == 'legacy' and bool(second),
        'damage_endian': damage_endian,
    }


def combo_draw(seed, k, pins):
    """The first variant whose draw carries >= COMBO_MIN_DECISIONS decisions."""
    for variant in range(COMBO_MAX_REDRAWS):
        rng, factors = combo_factors(seed, k, pins, variant)
        if len(combo_decisions(factors)) >= COMBO_MIN_DECISIONS:
            factors['redraw'] = variant
            factors['decisions'] = combo_decisions(factors)
            return rng, factors
    raise SystemExit(
        f'combo {k}: no draw with >= {COMBO_MIN_DECISIONS} decision factors in '
        f'{COMBO_MAX_REDRAWS} variants -- the factor space is too thin')


def combo_declared(factors):
    """The feature tuple a combo's factor vector implies, per the A1 precedence.

    Every clause below is MEASURED in this wave (report §4) rather than inferred:

    * ``capped`` -- a wrapped body at ``--max-depth 1``: the tar is extracted and
      the member published, but the image inside is never opened, so F = 0,
      SR = no, no link gap, and no extractor argv exists.  Rules 2/4/5/6/7 never
      see it; rule 2 answers container-depth-limited.
    * ``reached`` -- ``depth-limited`` is minted only when an extraction actually
      got to the ceiling.  A clean chunk, a wrapped container, or a sibling chunk
      in a two-chunk carrier mints it; a FAILING single root chunk (damaged or
      dependency-missing) mints nothing.
    * ``residue`` -- the tail chunk has a null handler, so H keeps only the
      squashfs/tar names while G gains ``unknown-chunk-handler``; the tail is
      also carved and published (``<start>-<end>.unknown``), which is why a
      damaged image beside a residue is P > 0 and lands rule 5, not rule 7.
    * ``dep`` -- the failing Command reports its own executable and every v1-v3
      chunk runs plain ``sasquatch``, so D = ['sasquatch'] and BE = 'n/a'.
    """
    capped = bool(factors['wrap']) and factors['max_depth'] == 1
    dep_effective = bool(factors['dep']) and not capped
    damage_effective = bool(factors['damage']) and not dep_effective and not capped
    # A dependency failure means the extractor never ran, so no symlink was ever
    # inspected: SR stays no and no unpublished-entry gap exists (measured C10,
    # C12, C20 in the dev arm).
    links_active = ((not capped) and (not dep_effective)
                    and factors['links'] != 'none' and bool(factors['body_v4']))
    handlers = set()
    if factors['wrap']:
        handlers.add('tar')
    if not capped:
        if factors['base'] == 'legacy':
            handlers.add(factors['legacy_handler'])
        if factors['body_v4']:
            handlers.add(V4_HANDLER[factors['endian']])
    gaps = set()
    if dep_effective:
        gaps.add('missing-extractor-dependency')
    elif damage_effective:
        gaps.add('extractor-failure')
    if links_active and factors['links'] in ('in-tree', 'both'):
        gaps.add('unpublished-entry')
    if factors['max_depth'] == 1:
        if factors['wrap']:
            reached = True            # the tar itself is extracted at the ceiling
        elif dep_effective:
            reached = False           # nothing was ever written to descend into
        else:
            # A damaged chunk still reaches the ceiling when it is carved (a
            # residue or a sibling chunk makes it a non-root chunk), which is why
            # a damaged root chunk alone mints nothing but damage + residue does.
            reached = ((not damage_effective) or bool(factors['residue'])
                       or bool(factors['two_chunk']))
        if reached:
            gaps.add('depth-limited')
    if factors['residue']:
        gaps.add('unknown-chunk-handler')
    carved = (bool(factors['residue']) or bool(factors['wrap'])
              or bool(factors['two_chunk']))
    if not damage_effective and not dep_effective:
        published = 'nonzero'          # a clean chunk publishes its tree/files
    elif dep_effective:
        # A dependency failure writes nothing for a SINGLE root chunk (dev arm
        # C11, and round-41's dep classes); the carve / the sibling chunk / the
        # tar member still publish when one of those is present.
        published = 'nonzero' if carved else 'zero'
    elif carved:
        published = 'nonzero'          # the tail carve / the tar member / the sibling
    elif factors['body_v4']:
        # The v4 damage recipe zeroes a LATE data block, so every earlier file is
        # already published when it fails (round-41 measured; dev arm C09/C13).
        published = 'nonzero'
    else:
        # A pinned legacy fixture's damage lands in its metadata, before any file.
        published = 'zero'
    if dep_effective or not damage_effective:
        be = 'n/a'
    else:
        be = 'yes' if factors['damage_endian'] == 'be' else 'no'
    deps = set()
    if dep_effective:
        # MEASURED (R42C2ReconCombo CB5): a two-chunk carrier attempts every
        # chunk's extractor, so a legacy chunk adds plain `sasquatch` and a v4 BE
        # chunk adds `sasquatch-v4be`; the union is what rule 4 reads, and the
        # `sasquatch-v4be` membership wins the BE label.
        if factors['base'] == 'legacy':
            deps.add('sasquatch')
        if factors['body_v4']:
            deps.add('sasquatch-v4be' if factors['endian'] == 'be'
                     else 'sasquatch')
    return {
        'handler_set': sorted(handlers),
        'gap_kinds': sorted(gaps),
        'gap_dependencies': sorted(deps),
        'be_argv': be,
        'symlink_removed': bool(links_active and factors['links'] in ('escaping', 'both')),
        'published': published,
    }


# ---------------------------------------------------------------------------
# Expected feature tuples (the generator-side cross-check, never the scored
# label).  Derived from the plan's precedence text, written per class BEFORE any
# REA run, and compared to the measured envelope by --verify:
#   handler  'k' = the replicate's endianness (k==1 be -> squashfs_v4_be,
#            k==2 le -> squashfs_v4_le); 'be'/'avm' -> squashfs_v4_be
#   gaps     the exact gap-kind SET (order-free)
#   deps     the exact dependency SET
#   sr       symlink removed (MaliciousSymlinkRemoved diagnostic)
#   failed   any chunk with extraction_failed
#   files    'nonzero' (P > 0) or 'zero' (P == 0)
#   be       '-be' in a recorded child argv: 'yes' / 'no' / 'n/a' (no argv)
#   depth    the --max-depth this class must run at
# ---------------------------------------------------------------------------
EXPECTATIONS = {
    'clean-be': dict(handler='be', gaps=(), sr=False, failed=False,
                     files='nonzero', be='n/a'),
    'clean-le': dict(handler='le', gaps=(), sr=False, failed=False,
                     files='nonzero', be='n/a'),
    'clean-empty': dict(handler='k', gaps=(), sr=False, failed=False,
                        files='zero', be='n/a'),
    'escaping-symlink-removed': dict(handler='k', gaps=(), sr=True,
                                     failed=False, files='nonzero', be='n/a'),
    'in-tree-symlink-metadata': dict(handler='k', gaps=('unpublished-entry',),
                                     sr=False, failed=False, files='nonzero',
                                     be='n/a'),
    'mixed-symlinks': dict(handler='k', gaps=('unpublished-entry',), sr=True,
                           failed=False, files='nonzero', be='n/a'),
    # A chunk with a MISSING extractor dependency is marked extraction_failed
    # too (measured, and round-40's committed H13/H15 agree): unblob could not
    # run the extractor, so it records both the dependency gap and the chunk
    # failure.  The precedence text never reads 'failed' on the dependency
    # branch (rule 3 precedes 4-6), so the label is unaffected -- but a table
    # that matched a bare "failed" column before the gap kind would report
    # body-extractor-failure here.
    'dep-missing-be': dict(handler='be',
                           gaps=('missing-extractor-dependency',),
                           deps=('sasquatch-v4be',), sr=False, failed=True,
                           files='zero', be='n/a'),
    'dep-missing-le': dict(handler='le',
                           gaps=('missing-extractor-dependency',),
                           deps=('sasquatch',), sr=False, failed=True,
                           files='zero', be='n/a'),
    'avm-marker-be-dropped': dict(handler='be', gaps=('extractor-failure',),
                                  sr=False, failed=True, files='zero',
                                  be='no'),
    'body-extractor-failure': dict(handler='be', gaps=('extractor-failure',),
                                   sr=False, failed=True, files='zero',
                                   be='yes'),
    'partial-body-failure': dict(handler='be', gaps=('extractor-failure',),
                                 sr=False, failed=True, files='nonzero',
                                 be='yes'),
    'partial-in-tree': dict(handler='be',
                            gaps=('extractor-failure', 'unpublished-entry'),
                            sr=False, failed=True, files='nonzero', be='yes'),
    'partial-mixed': dict(handler='be',
                          gaps=('extractor-failure', 'unpublished-entry'),
                          sr=True, failed=True, files='nonzero', be='yes'),
    'depth-limited-alone': dict(handler='k', gaps=('depth-limited',),
                                sr=False, failed=False, files='nonzero',
                                be='n/a', depth=1),
    'depth-limited-in-tree': dict(handler='k',
                                  gaps=('depth-limited', 'unpublished-entry'),
                                  sr=False, failed=False, files='nonzero',
                                  be='n/a', depth=1),
    'depth-limited-mixed': dict(handler='k',
                                gaps=('depth-limited', 'unpublished-entry'),
                                sr=True, failed=False, files='nonzero',
                                be='n/a', depth=1),
    # round-41 amendments.  `be='k'` means: 'yes' on a BE replicate (-be is
    # appended for a standard big-endian body), 'no' on an LE replicate (unblob
    # runs `sasquatch -le`, which carries no -be token).
    'body-extractor-failure-le': dict(handler='le',
                                     gaps=('extractor-failure',),
                                     sr=False, failed=True, files='zero',
                                     be='no'),
    'failure-depth-limited': dict(handler='k',
                                 gaps=('extractor-failure', 'depth-limited'),
                                 sr=False, failed=True, files='nonzero',
                                 be='k', depth=1),
    'no-squashfs-chunk': dict(handler=None, gaps=(), sr=False, failed=False,
                              files='zero', be='n/a'),
    'out-of-domain': dict(handler=None, gaps=(), sr=False, failed=False,
                          files='zero', be='n/a', depth=None),
}


def rea_params(recipe):
    """The REA parameters this class must run with, recorded in the manifest.

    The out-of-domain class does not run ``extract-firmware`` at all, so its
    extraction depth is n/a (``None``) rather than REA's default -- a recorded 3
    there would claim a depth-limited extract-firmware run that never happened.
    """
    if recipe.get('ood'):
        return {'max_depth': None, 'operation': 'not_extract_firmware'}
    return {'max_depth': (recipe.get('rea') or {}).get('max_depth',
                                                        DEFAULT_MAX_DEPTH)}


def expected_features(name, endian, primary=None, secondary=None):
    """Resolve the class expectation into a concrete, JSON-able feature tuple.

    Legacy classes (``kind='legacy'``) have no static EXPECTATIONS row: their
    handler set and BE value come from the fixtures the seed drew, so they go
    through ``legacy_features`` instead.
    """
    recipe = RECIPES.get(name) or {}
    if recipe.get('kind') == 'legacy':
        return legacy_features(recipe, primary, secondary)
    spec = dict(EXPECTATIONS[name])
    handler = spec.get('handler')
    if handler is None:
        handler_set = []
    elif handler == 'k':
        handler_set = ['squashfs_v4_be' if endian in ('be', 'avm')
                       else 'squashfs_v4_le']
    else:
        handler_set = ['squashfs_v4_be' if handler == 'be'
                       else 'squashfs_v4_le']
    be = spec.get('be')
    if be == 'k':
        be = 'yes' if endian in ('be', 'avm') else 'no'
    return {
        'handler_set': handler_set,
        'gap_kinds': sorted(spec.get('gaps') or ()),
        'gap_dependencies': sorted(spec.get('deps') or ()),
        'symlink_removed': bool(spec.get('sr')),
        'extraction_failed': bool(spec.get('failed')),
        'published': spec.get('files'),
        'be_argv': be,
        'max_depth': spec.get('depth', DEFAULT_MAX_DEPTH),
    }


# The six fields the counter binds as `observed_features_match_declared`.
# R41-CL1: they are written under EXACTLY ONE manifest key, `declared_features`,
# for every class including combos.  There is no `declared` key and no
# `class_expected.features` key -- the round-41 generator wrote the same tuple a
# second time under `class_expected.features`, and a counter that read the other
# spelling could disagree with the manifest it was scoring.
# `extraction_failed` and `max_depth` are NOT part of that binding: they are
# extra facts this generator cross-checks, and they live in `declared_extras`.
DECLARED_FIELDS = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                   'symlink_removed', 'published')
DECLARED_KEY = 'declared_features'
DECLARED_EXTRAS_KEY = 'declared_extras'
EXTRA_FIELDS = ('extraction_failed', 'max_depth')


def declared_tuple(features):
    """The binding half of an expectation: (H, G, D, BE, SR, P-class)."""
    return {key: features[key] for key in DECLARED_FIELDS}


def declared_extras(features):
    """The two facts outside the binding, kept in their own key."""
    return {key: features[key] for key in EXTRA_FIELDS}


# ---------------------------------------------------------------------------
# image writer
# ---------------------------------------------------------------------------
WRITER_LOGICAL = os.path.join('tools', 'round-39', 'gen-squashfs.py')


def default_writer_path():
    """Locate gen-squashfs.py: tools/round-39 beside us, then any ancestor's tools/round-39."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [os.path.join(here, '..', 'round-39', 'gen-squashfs.py')]
    cursor = here
    for _ in range(8):
        candidates.append(os.path.join(cursor, 'tools', 'round-39', 'gen-squashfs.py'))
        parent = os.path.dirname(cursor)
        if parent == cursor:
            break
        cursor = parent
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.normpath(candidate)
    return os.path.normpath(candidates[0])


def writer_logical_path(resolved):
    """Stable manifest value: the lane-relative path when the writer lives under tools/round-39."""
    marker = WRITER_LOGICAL + os.sep
    if resolved.endswith(marker[:-1]):
        return WRITER_LOGICAL
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.relpath(resolved, here)


def load_writer(path):
    if not os.path.isfile(path):
        raise SystemExit(f'image writer not found: {path}')
    spec = importlib.util.spec_from_file_location('r39_gen_squashfs', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def install_block_encoder(module):
    """Replace the round-37 block encoder and compression-id table (round-39 fix)."""

    def comp_bytes(kind, data, block_size=4096):
        if kind == 'gzip':
            compressor = zlib.compressobj(9, zlib.DEFLATED, 15)
            return compressor.compress(data) + compressor.flush()
        return lzma.compress(
            data, format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC32,
            filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6}],
        )

    module.comp_bytes = comp_bytes
    module.COMP = {'gzip': 1, 'xz': 4}


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# pure-stdlib SquashFS 4.0 reader (damage recipes only)
# ---------------------------------------------------------------------------
META_UNCOMPRESSED = 1 << 15
BLOCK_UNCOMPRESSED = 1 << 24
INVALID_FRAG = 0xFFFFFFFF
MAGIC = {b'hsqs': '<', b'sqsh': '>'}
COMP_IDS = {1: 'gzip', 2: 'lzma', 3: 'lzo', 4: 'xz', 5: 'lz4', 6: 'zstd'}
TYPE_DIR, TYPE_FILE, TYPE_SYMLINK = 1, 2, 3
TYPE_LDIR, TYPE_LFILE, TYPE_LSYMLINK = 8, 9, 10


class SqfsError(Exception):
    pass


def _decompress(raw, comp):
    if comp == 'gzip':
        try:
            return zlib.decompress(raw)
        except zlib.error as exc:
            raise SqfsError('gzip metadata block: %s' % exc)
    if comp in ('xz', 'lzma'):
        try:
            return lzma.decompress(raw)
        except (lzma.LZMAError, EOFError) as exc:
            raise SqfsError('%s metadata block: %s' % (comp, exc))
    raise SqfsError('compression id %r not supported by this reader' % comp)


class _Stream:
    """Sequential reader over a metadata stream."""

    def __init__(self, meta, ptr, offset):
        self.meta = meta
        self.ptr = ptr
        self.off = offset

    def take(self, count):
        data = self.meta.read(self.ptr, self.off, count)
        self.off += count
        return data

    def u16(self):
        return struct.unpack(self.meta.e + 'H', self.take(2))[0]

    def u32(self):
        return struct.unpack(self.meta.e + 'I', self.take(4))[0]


class _Meta:
    """Concatenated metadata blocks of the inode or directory table."""

    def __init__(self, img, base, e, comp):
        self.img = img
        self.base = base
        self.e = e
        self.comp = comp
        self.cache = {}

    def block(self, ptr):
        hit = self.cache.get(ptr)
        if hit is not None:
            return hit
        if not 0 <= ptr <= len(self.img) - 2:
            raise SqfsError('metadata block pointer %d outside the image' % ptr)
        header = struct.unpack_from(self.e + 'H', self.img, self.base + ptr)[0]
        size = header & ~META_UNCOMPRESSED
        raw = self.img[self.base + ptr + 2:self.base + ptr + 2 + size]
        if len(raw) != size:
            raise SqfsError('metadata block at %d truncated' % ptr)
        data = raw if header & META_UNCOMPRESSED else _decompress(raw, self.comp)
        hit = (data, size + 2)
        self.cache[ptr] = hit
        return hit

    def read(self, ptr, offset, count):
        out = bytearray()
        cur, off = ptr, offset
        while len(out) < count:
            data, on_disk = self.block(cur)
            if off > len(data):
                raise SqfsError('metadata offset %d beyond block at %d' % (off, cur))
            out += data[off:off + (count - len(out))]
            if len(out) >= count:
                break
            cur, off = cur + on_disk, 0
        return bytes(out)


class _Sqfs:
    def __init__(self, buf):
        if len(buf) < 96:
            raise SqfsError('image is %d bytes, shorter than the superblock' % len(buf))
        magic = bytes(buf[:4])
        if magic not in MAGIC:
            raise SqfsError('unknown magic %r' % magic)
        self.buf = buf
        self.e = MAGIC[magic]
        (self.comp_id,) = struct.unpack_from(self.e + 'H', buf, 20)
        self.major, self.minor = struct.unpack_from(self.e + 'HH', buf, 28)
        (self.root_inode, self.bytes_used, self.id_table_start,
         _xattr, self.inode_table_start, self.dir_table_start,
         _frag, _export) = struct.unpack_from(self.e + 'QQQQQQQQ', buf, 32)
        if (self.major, self.minor) != (4, 0):
            raise SqfsError('not a SquashFS 4.0 image: %d.%d' % (self.major, self.minor))
        self.comp = COMP_IDS.get(self.comp_id)
        if self.comp is None:
            raise SqfsError('compression id %d unknown' % self.comp_id)
        (self.block_size,) = struct.unpack_from(self.e + 'I', buf, 12)
        self.inodes = _Meta(buf, self.inode_table_start, self.e, self.comp)
        self.dirs = _Meta(buf, self.dir_table_start, self.e, self.comp)
        self._cache = {}

    def inode(self, ref):
        hit = self._cache.get(ref)
        if hit is not None:
            return hit
        st = _Stream(self.inodes, ref >> 16, ref & 0xFFFF)
        kind = st.u16()
        node = {'ref': ref, 'type': kind}
        st.take(6)  # mode, uid, gid
        st.take(8)  # mtime, inode_number
        if kind in (TYPE_DIR, TYPE_LDIR):
            if kind == TYPE_DIR:
                node['start_block'] = st.u32()
                st.take(4)  # nlink
                node['file_size'] = st.u16()
                node['offset'] = st.u16()
            else:
                st.take(4)  # nlink
                node['file_size'] = st.u32()
                node['start_block'] = st.u32()
                st.take(8)  # parent, i_count
                node['offset'] = st.u16()
        elif kind in (TYPE_FILE, TYPE_LFILE):
            if kind == TYPE_FILE:
                node['start_block'] = st.u32()
                node['fragment'] = st.u32()
                st.take(4)  # frag offset
                node['file_size'] = st.u32()
            else:
                node['start_block'] = st.take(8)
                node['start_block'] = struct.unpack(self.e + 'Q', node['start_block'])[0]
                node['file_size'] = struct.unpack(self.e + 'Q', st.take(8))[0]
                st.take(8)  # sparse
                st.take(8)  # nlink, fragment
                st.take(4)  # frag offset
                node['fragment'] = INVALID_FRAG
            count = (node['file_size'] + self.block_size - 1) // self.block_size \
                if node['fragment'] == INVALID_FRAG else node['file_size'] // self.block_size
            if count > 8192:
                raise SqfsError('inode %#x declares %d data blocks' % (ref, count))
            node['block_list'] = [st.u32() for _ in range(count)]
        self._cache[ref] = node
        return node

    def entries(self, node):
        st = _Stream(self.dirs, node['start_block'], node['offset'])
        header = st.take(12)
        count, start = struct.unpack(self.e + 'II', header[:8])
        out = []
        for _ in range(count + 1):
            offset, _delta, typ, name_size = struct.unpack(
                self.e + 'HhHH', st.take(8))
            name = st.take(name_size + 1).decode('utf-8', 'surrogateescape')
            out.append({'name': name, 'type': typ, 'ref': (start << 16) | offset})
        return out

    def walk(self):
        """Directory-scan order, with a cycle guard.

        A malformed image must fail loudly, not hang: the lane writer collapses
        two directory records when a directory has no children (an empty record
        has no header, so the next record reuses offset 0), which makes an empty
        nested directory and its parent share one directory record.  Extraction
        tools skip the empty directory silently; this reader would recurse
        forever.  A repeated directory reference is therefore an error here.
        """
        order = []
        seen_dirs = set()

        def visit(path, ref):
            if ref in seen_dirs:
                raise SqfsError(
                    'directory reference %#x repeats at %r: the image reuses one '
                    'directory record (the writer emits no header for a directory '
                    'with no children)' % (ref, path or '/'))
            seen_dirs.add(ref)
            node = self.inode(ref)
            if node['type'] not in (TYPE_DIR, TYPE_LDIR):
                raise SqfsError('%r is not a directory' % (path or '/'))
            for entry in self.entries(node):
                child = posixpath.join(path, entry['name']) if path else entry['name']
                order.append((child, entry['type'], entry['ref']))
                if entry['type'] in (TYPE_DIR, TYPE_LDIR):
                    visit(child, entry['ref'])

        visit('', self.root_inode)
        return order

    def files(self):
        """Regular files with the absolute on-disk span of each data block."""
        out = []
        for path, typ, ref in self.walk():
            if typ not in (TYPE_FILE, TYPE_LFILE):
                continue
            node = self.inode(ref)
            pos = node['start_block']
            blocks = []
            for field in node['block_list']:
                on_disk = field & ~BLOCK_UNCOMPRESSED
                if on_disk == 0:
                    blocks.append({'offset': pos, 'length': 0,
                                   'compressed': False, 'sparse': True})
                    continue
                blocks.append({'offset': pos, 'length': on_disk,
                               'compressed': not (field & BLOCK_UNCOMPRESSED),
                               'sparse': False})
                pos += on_disk
            out.append({'path': path, 'ref': ref, 'size': node['file_size'],
                        'blocks': blocks})
        return out


# ---------------------------------------------------------------------------
# corruptions: bytearray(clean image) -> bytearray(corrupted image)
# ---------------------------------------------------------------------------
def corruption_zero_id_table(payload, endian):
    """Zero the id-table metadata block (header + payload).

    Superblock field id_table_start is a u64 at offset 48; it points just past
    the id metadata block at the 8-byte id table index, and that index holds the
    metadata block's start.  sasquatch reads the id table during filesystem
    init, before any file is written, so it fails with P=0:
    ``read_id_table: failed to read id table block``.
    """
    prefix = '>' if endian in ('be', 'avm') else '<'
    id_table_start = struct.unpack(prefix + 'Q', bytes(payload[48:56]))[0]
    if not 96 <= id_table_start <= len(payload) - 8:
        raise ValueError(
            f'id_table_start {id_table_start} outside image ({len(payload)} bytes)')
    id_meta_start = struct.unpack(
        prefix + 'Q', bytes(payload[id_table_start:id_table_start + 8]))[0]
    if not 96 <= id_meta_start < id_table_start <= len(payload):
        raise ValueError(
            f'id metadata block {id_meta_start}..{id_table_start} outside image')
    payload[id_meta_start:id_table_start] = bytes(id_table_start - id_meta_start)
    return payload


def corruption_bad_major(payload, endian):
    """s_major 4 -> 9: no v1..v4 handler pattern matches, so the image stays an
    unknown chunk and REA publishes no squashfs chunk."""
    prefix = '>' if endian in ('be', 'avm') else '<'
    major, minor = struct.unpack(prefix + 'HH', bytes(payload[28:32]))
    if (major, minor) != (4, 0):
        raise ValueError(f'unexpected squashfs version {major}.{minor}')
    payload[28:32] = struct.pack(prefix + 'HH', 9, 0)
    return payload


def corruption_partial(payload, endian, report=None):
    """Zero EVERY in-range compressed data block of every file but the FIRST.

    Round-42 rewrite of the round-41 single-block recipe.  Round 41 damaged only
    the last block of the last-extracted file, which makes the carrier depend on
    sasquatch choosing a NONZERO exit for that particular file.  Measured on the
    round-42 dev seed (dev arm H30, xz big-endian): the extractor wrote the corrupt
    copy, printed ``writer: failed to read/uncompress file`` and exited **0**, so
    the envelope carried no ``extractor-failure`` at all and the class landed
    ``clean``; the same carrier damaged on a different block exited 1.  The exit
    code is a function of WHERE the failure lands, not of the block size.

    So the recipe now damages every compressed, non-sparse block at or below
    ``MAX_DAMAGED_BLOCK`` of every file EXCEPT the first in walk order:

      * the first file is never touched, so the extractor publishes at least one
        file before anything fails: P > 0 holds by construction;
      * at least one mid-file failure is guaranteed (a non-last block of a
        non-last file), which is the configuration measured to exit nonzero
        (6/6 carriers on the dev seed, P = 2..8).

    ``MAX_DAMAGED_BLOCK`` still pins the per-block ceiling: a zeroed block above
    it can be ABSORBED by the decompressor fallback chain and never fail at all
    (R40-CL4 / MH-4), so such blocks are skipped rather than claimed.
    """
    image = _Sqfs(bytes(payload))
    entries = image.files()
    if len(entries) < 2:
        raise SqfsError('partial recipe needs at least 2 regular files, found %d'
                        % len(entries))
    damaged = []
    for entry in entries[1:]:
        for block in entry['blocks']:
            if not block['compressed'] or block['sparse']:
                continue
            if block['length'] > MAX_DAMAGED_BLOCK:
                continue
            start, length = block['offset'], block['length']
            if start + length > image.bytes_used:
                raise SqfsError('data block %d+%d beyond bytes_used %d'
                                % (start, length, image.bytes_used))
            payload[start:start + length] = bytes([PARTIAL_FILL]) * length
            damaged.append({'path': entry['path'], 'offset': start,
                            'length': length})
    if not damaged:
        raise SqfsError(
            'no compressed data block at or below the %d B partial pin outside the '
            'first file: a larger block can be absorbed by the decompressor '
            'fallback and never fail (R40-CL4)' % MAX_DAMAGED_BLOCK)
    if report is not None:
        report.update({'recipe': 'partial',
                       'files': len(entries),
                       'blocks': damaged,
                       'blocks_damaged': len(damaged),
                       'bytes_damaged': sum(d['length'] for d in damaged),
                       'paths': sorted({d['path'] for d in damaged}),
                       'fill': '%02x' % PARTIAL_FILL,
                       'pin': 'compressed-length',
                       'pin_max_block_length': MAX_DAMAGED_BLOCK,
                       'pin_measured_fail_range': [22, 136],
                       'pin_measured_absorbed_from': 1730,
                       'first_file': entries[0]['path']})
    return payload


CORRUPTIONS = {
    'zero-id-table': lambda payload, endian, report: corruption_zero_id_table(
        payload, endian),
    'bad-major': lambda payload, endian, report: corruption_bad_major(
        payload, endian),
    'partial': corruption_partial,
}


# ---------------------------------------------------------------------------
# deterministic tree material
# ---------------------------------------------------------------------------
def stream_bytes(material, size):
    """SHA-256 counter stream: independent of the interpreter's PRNG."""
    out = bytearray()
    counter = 0
    while len(out) < size:
        out += hashlib.sha256(material + b'#' + str(counter).encode()).digest()
        counter += 1
    return bytes(out[:size])


def pattern_bytes(material, size):
    """Compressible content: a unique 48-byte head followed by a letter cycle.

    The head keeps every file's sha256 distinct; the cycle keeps every data
    block compressed, which the partial recipe needs.
    """
    head = stream_bytes(material + b':head', 48)
    if size <= len(head):
        return head[:size]
    cycle = b'ABCDEFGH'
    body = (cycle * ((size - len(head)) // len(cycle) + 1))[:size - len(head)]
    return head + body


def token(rng, low=3, high=9):
    return ''.join(rng.choice(ALPHABET) for _ in range(rng.randint(low, high)))


def unique_name(rng, taken, prefix=''):
    while True:
        name = prefix + token(rng)
        if name not in taken:
            taken.add(name)
            return name


def _write_file(root, rel, material, size, content):
    data = pattern_bytes(material, size) if content == 'pattern' \
        else stream_bytes(material, size)
    with open(os.path.join(root, rel), 'wb') as handle:
        handle.write(data)


def build_tree(rng, material, root, link_kinds, content='stream',
               link_placement='rng'):
    """Create one random tree.

    ``link_placement='root-first'`` puts every link at the image root with a
    name starting '-' -- ASCII 0x2d sorts before every ALPHABET character, so
    the writer's name-ordered directory table hands unsquashfs the link before
    any file, and a link's unpublished-entry gap survives a damaged data block
    (the combined partial+symlink classes depend on that order).

    Returns (dirs, files, symlinks): directory paths, regular-file paths and
    [(relative path, link target, kind)] -- all relative posix strings.
    """
    depth = rng.randint(1, 3)
    dirs = []
    parts = []
    for _ in range(depth):
        parts.append(token(rng))
        dirs.append('/'.join(parts))
    for rel in dirs:
        os.makedirs(os.path.join(root, rel))

    slots = [''] + dirs
    taken = {rel: set() for rel in slots}
    for rel in dirs:
        parent = posixpath.dirname(rel)
        taken[parent].add(posixpath.basename(rel))

    files = []
    for _ in range(rng.randint(3, 8)):
        parent = rng.choice(slots)
        name = unique_name(rng, taken[parent])
        rel = f'{parent}/{name}' if parent else name
        _write_file(root, rel, material + b':' + rel.encode(),
                    rng.randrange(0, 20001), content)
        files.append(rel)

    symlinks = []
    first = link_placement == 'root-first'
    if first and link_kinds:
        slots = ['']
    for kind in link_kinds:
        if kind == 'escaping':
            parent = ''
            name = unique_name(rng, taken[parent], prefix='-' if first else '')
            target = '../' + token(rng)
            link_rel = f'{parent}/{name}' if parent else name
            os.symlink(target, os.path.join(root, link_rel))
            symlinks.append((link_rel, target, 'escaping'))
        elif kind == 'in-tree':
            target_rel = rng.choice([f for f in files if os.path.getsize(
                os.path.join(root, f)) > 0] or files)
            if first:
                parent = ''
            else:
                parent = rng.choice(slots)
                if parent == posixpath.dirname(target_rel) and len(slots) > 1:
                    parent = rng.choice([d for d in slots if d != parent])
            name = unique_name(rng, taken[parent], prefix='-' if first else '')
            link_rel = f'{parent}/{name}' if parent else name
            target = posixpath.relpath(target_rel, start=parent or '.')
            os.symlink(target, os.path.join(root, link_rel))
            symlinks.append((link_rel, target, 'in-tree'))
        else:
            raise ValueError(f'unknown symlink kind {kind!r}')
    return dirs, files, symlinks


def fill_empty_dirs(rng, material, root, dirs, files, content):
    """Give every directory at least one child.

    Why: the lane writer emits NOTHING for a directory with no children, so its
    ``dir_ref`` is ``(block, 0, 3)`` -- the same offset the next directory record
    gets.  Two directories then share one directory record: sqfs-list and this
    reader disagree, sasquatch silently skips the empty directory, and any reader
    that follows the record loops.  Measured on the combo family (seed
    ``b13ef790…``, k=8): ``78hgf8qhm`` and the empty ``78hgf8qhm/_2bjv9low``
    shared offset 0.  A one-file fill keeps the tree honest (the directory really
    is created on extraction) and keeps its oracle verifiable.

    The intentionally empty class (``clean-empty``) does NOT pass through here.
    """
    subdirs = {posixpath.dirname(d) for d in dirs if posixpath.dirname(d)}
    filled = []
    for d in sorted(dirs, key=lambda x: (-x.count('/'), x)):
        has_child = any(posixpath.dirname(f) == d for f in files) or d in subdirs
        if has_child:
            continue
        name = token(rng)
        rel = f'{d}/{name}'
        taken = {posixpath.basename(f) for f in files if posixpath.dirname(f) == d}
        while name in taken:
            name = token(rng)
            rel = f'{d}/{name}'
        _write_file(root, rel, material + b':fill:' + rel.encode(),
                    rng.randrange(1, 401), content)
        files.append(rel)
        filled.append(rel)
    return filled


def empty_tree(rng, material, root):
    """A valid image holding directories only: zero regular files, no links.

    One empty directory keeps the image a real tree (round-39 measured the
    same shape as ``full-be-dirempty-gzip``: handler present, no gap, P=0).
    """
    rel = token(rng)
    os.makedirs(os.path.join(root, rel))
    return [rel], [], []


def tree_oracle(root, dirs, files, symlinks):
    return {
        'directories': sorted(dirs),
        'files': [
            {'path': rel, 'sha256': sha256_file(os.path.join(root, rel)),
             'size': os.path.getsize(os.path.join(root, rel))}
            for rel in sorted(files)
        ],
        'symlinks': [
            {'path': rel, 'target': target, 'kind': kind}
            for rel, target, kind in sorted(symlinks)
        ],
    }


# ---------------------------------------------------------------------------
# nested image (the depth-limited classes)
# ---------------------------------------------------------------------------
def build_nested(writer, rng, material, work, tree, slots):
    """Write a real SquashFS v4 image INTO the carrier tree.

    Little-endian (``hsqs``) so the nested chunk is handler-recognisable by any
    later run: at ``--max-depth 1`` it is never reached, which is exactly the
    depth-limited case (a real chunk sits behind the cap), and a run at a deeper
    cap would genuinely extract it.  Returns the record stored in the manifest;
    the caller adds ``path`` to the file list so the outer oracle hashes it.
    """
    inner_tree = os.path.join(work, 'nested-tree')
    os.makedirs(inner_tree)
    sub = token(rng)
    os.makedirs(os.path.join(inner_tree, sub))
    inner_files = []
    for _ in range(rng.randint(1, 2)):
        rel = f'{sub}/{token(rng)}'
        _write_file(inner_tree, rel,
                    material + b':nested:' + rel.encode(),
                    rng.randrange(200, 1501), 'stream')
        inner_files.append(rel)
    image = os.path.join(work, 'nested.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(inner_tree, image, 'le', 'gzip')
    with open(image, 'rb') as handle:
        if handle.read(4) != b'hsqs':
            raise SqfsError('nested writer did not emit an LE SquashFS magic')
    parent = rng.choice(slots)
    while True:
        base = token(rng) + '.sqsh'
        rel = f'{parent}/{base}' if parent else base
        if not os.path.exists(os.path.join(tree, rel)):
            break
    shutil.copyfile(image, os.path.join(tree, rel))
    return {'path': rel, 'mode': 'le', 'compression': 'gzip',
            'handler_expected': 'squashfs_v4_le',
            'inner_files': inner_files,
            'size': os.path.getsize(os.path.join(tree, rel)),
            'sha256': sha256_file(os.path.join(tree, rel))}


# ---------------------------------------------------------------------------
# carrier build
# ---------------------------------------------------------------------------
def variant(recipe, k):
    """Resolve the per-replicate non-decision features."""
    endian = recipe['endian']
    if endian == 'k':
        endian = 'be' if k == 1 else 'le'
    comp = recipe['comp']
    if comp == 'k':
        comp = 'gzip' if k == 1 else 'xz'
    return endian, comp


def replicate_variation():
    return ['compression', 'tree-shape', 'endianness-where-the-class-allows']


TWO_CHUNK_PAD = 4096


def build_two_chunk(writer, rng, material, work, endian, comp):
    """Failure + depth cut in ONE carrier (round-41 amendment class).

    Layout, both chunks built by the same writer in the same endianness and
    compressor:

        offset 0      : a valid image whose tree holds ZERO regular files.  Its
                        extraction directory is the depth ceiling at
                        ``--max-depth 1``, and it publishes nothing.
        offset 4096   : a normal image whose id-table metadata block is zeroed.
                        Its extraction fails after the first chunk was already
                        staged, so the envelope carries BOTH gap kinds.

    Measured (dev probe, and re-measured by ``--verify``): G =
    {extractor-failure, depth-limited}, P = 1 -- the carve of the second chunk,
    ``4096-<end>.<handler>``, is the only published regular file, because a chunk
    that is not the root is carved on publication.  P = 0 is NOT constructible
    here: a root-chunk failure mints no depth-limited gap (measured), and any
    second chunk in the same input is carved.  See the report, §6 F7.
    """
    empty_tree_dir = os.path.join(work, 'chunk1-tree')
    os.makedirs(os.path.join(empty_tree_dir, token(rng)))
    chunk1 = os.path.join(work, 'chunk1.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(empty_tree_dir, chunk1, endian, comp)
    with open(chunk1, 'rb') as handle:
        chunk1_bytes = handle.read()
    if len(chunk1_bytes) > TWO_CHUNK_PAD:
        raise SqfsError('empty chunk is %d B, above the %d B pad (endian=%s comp=%s)'
                        % (len(chunk1_bytes), TWO_CHUNK_PAD, endian, comp))

    broken_tree = os.path.join(work, 'chunk2-tree')
    os.makedirs(os.path.join(broken_tree, token(rng)))
    for _ in range(rng.randint(2, 4)):
        rel = token(rng)
        _write_file(broken_tree, rel, material + b':chunk2:' + rel.encode(),
                    rng.randrange(200, 2001), 'pattern')
    chunk2 = os.path.join(work, 'chunk2.sqsh')
    with contextlib.redirect_stdout(io.StringIO()):
        writer.build_image(broken_tree, chunk2, endian, comp)
    with open(chunk2, 'rb') as handle:
        payload = bytearray(handle.read())
    corruption_zero_id_table(payload, endian)
    with open(chunk2, 'wb') as handle:
        handle.write(bytes(payload))

    image = os.path.join(work, 'carrier.sqsh')
    with open(image, 'wb') as handle:
        handle.write(chunk1_bytes)
        handle.write(bytes(TWO_CHUNK_PAD - len(chunk1_bytes)))
        with open(chunk2, 'rb') as tail:
            shutil.copyfileobj(tail, handle)
    handler = 'squashfs_v4_be' if endian in ('be', 'avm') else 'squashfs_v4_le'
    end = os.path.getsize(image)
    return image, {
        'layout': 'two-chunk',
        'pad': TWO_CHUNK_PAD,
        'parts': [
            {'offset': 0, 'length': len(chunk1_bytes),
             'sha256': sha256_file(chunk1),
             'role': 'valid image, zero regular files (depth ceiling, publishes nothing)',
             'endian': endian, 'compression': comp},
            {'offset': TWO_CHUNK_PAD, 'length': end - TWO_CHUNK_PAD,
             'sha256': sha256_file(chunk2),
             'role': 'id-table metadata block zeroed (extraction fails)',
             'endian': endian, 'compression': comp},
        ],
        'expected_published': [f'{TWO_CHUNK_PAD}-{end}.{handler}'],
        'corruption': {'recipe': 'zero-id-table', 'chunk': 2,
                       'chunk_offset': TWO_CHUNK_PAD},
    }, []


def build_carrier(seed, name, k, seq, writer, scratch, out_dir, pins,
                  fixtures_dir, cache_dir, fetch, used=None):
    """Build one carrier; return (manifest entry, build detail)."""
    recipe = RECIPES[name]
    if recipe.get('kind') == 'legacy':
        return build_legacy_carrier(seed, name, k, seq, out_dir, pins,
                                    fixtures_dir, cache_dir, fetch, used)
    if recipe.get('kind') == 'container':
        return build_container_carrier(seed, name, k, seq, writer, scratch,
                                       out_dir, pins, fixtures_dir, cache_dir,
                                       fetch, used)
    if recipe.get('kind') == 'residue':
        return build_residue_carrier(seed, name, k, seq, writer, scratch,
                                     out_dir, pins, fixtures_dir, cache_dir,
                                     fetch)
    class_index = list(RECIPES).index(name)
    rng = random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))
    material = f'{seed}:{name}:{k}'.encode()
    endian, comp = variant(recipe, k)

    work = os.path.join(scratch, f'build-{seq:02d}')
    os.makedirs(work)
    if recipe.get('layout') == 'two-chunk':
        image, two_chunk, _files = build_two_chunk(
            writer, rng, material, work, endian, comp)
        dirs, files, symlinks = [], [f'chunk{n}' for n in (1, 2)], []
        nested = None
        oracle = {'kind': 'two-chunk', **two_chunk}
        corruption_report = two_chunk['corruption']
    else:
        tree = os.path.join(work, 'tree')
        os.makedirs(tree)
        if recipe['tree'] == 'empty':
            dirs, files, symlinks = empty_tree(rng, material, tree)
        else:
            dirs, files, symlinks = build_tree(
                rng, material, tree, recipe['symlinks'], recipe['content'],
                link_placement=recipe.get('link_placement', 'rng'))
        nested = None
        if recipe.get('nested'):
            nested = build_nested(writer, rng, material, work, tree, [''] + dirs)
            files.append(nested['path'])
        if recipe['tree'] != 'empty':
            # `clean-empty` is the one class that must stay P=0: its empty
            # directory is the point (round-39 measured handler present, no gap,
            # zero regular files), so the fill skips it.
            fill_empty_dirs(rng, material, tree, dirs, files, recipe['content'])
        oracle = tree_oracle(tree, dirs, files, symlinks)

        image = os.path.join(work, 'carrier.sqsh')
        with contextlib.redirect_stdout(io.StringIO()):
            writer.build_image(tree, image, endian, comp)

        corruption_report = None
        if recipe['corruption']:
            with open(image, 'rb') as handle:
                payload = bytearray(handle.read())
            report = {}
            payload = CORRUPTIONS[recipe['corruption']](payload, endian, report)
            corruption_report = {'recipe': recipe['corruption'], **report}
            with open(image, 'wb') as handle:
                handle.write(bytes(payload))
        two_chunk = None

    carrier_id = f'H{seq:02d}'
    dest = os.path.join(out_dir, carrier_id)
    os.makedirs(dest, exist_ok=True)
    shutil.copyfile(image, os.path.join(dest, 'carrier.sqsh'))
    features = expected_features(name, endian)
    entry = {
        'id': carrier_id,
        'class': name,
        'label': recipe['label'],
        'action': ACTIONS[recipe['label']],
        'arm': 'ood' if recipe.get('ood') else recipe['arm'],
        'endian': endian,
        'compression': comp,
        'tree': recipe['tree'],
        'content': recipe['content'],
        'symlinks': list(recipe['symlinks']),
        'corruption': recipe['corruption'],
        'damage': corruption_report,
        'layout': recipe.get('layout', 'single-image'),
        'chunks': two_chunk['parts'] if two_chunk else None,
        'nested': nested,
        'rea': rea_params(recipe),
        'operation': 'inspect_firmware_regions' if recipe.get('ood')
        else 'extract_firmware',
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': sha256_file(os.path.join(dest, 'carrier.sqsh')),
        # The BINDING half, under EXACTLY ONE key (R41-CL1 fix).
        DECLARED_KEY: declared_tuple(features),
        DECLARED_EXTRAS_KEY: declared_extras(features),
        # The generator's own class expectation, REPORTED only (the scored
        # labels come from the frozen evaluator).  R41-CL1: no `features` key
        # here -- the tuple exists once, under `declared_features`.
        'class_expected': {
            'label': recipe['label'],
            'action': ACTIONS[recipe['label']],
            'reported_only': True,
        },
    }
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': seed, 'class': name, 'id': carrier_id,
                   'endian': endian, 'compression': comp,
                   'label': recipe['label'],
                   'action': ACTIONS[recipe['label']],
                   DECLARED_KEY: entry[DECLARED_KEY],
                   DECLARED_EXTRAS_KEY: entry[DECLARED_EXTRAS_KEY],
                   'class_expected': entry['class_expected'],
                   'nested': nested,
                   'chunks': entry['chunks'],
                   'oracle': oracle}, handle, indent=2)
        handle.write('\n')
    return entry, {'endian': endian, 'comp': comp,
                   'corruption': corruption_report,
                   'nested': nested,
                   'files': len(files), 'symlinks': len(symlinks)}


# ---------------------------------------------------------------------------
# legacy (v1-v3) carriers: pinned fixture bytes, never a generated image
# ---------------------------------------------------------------------------
def pad_fixture_section(payload, entry):
    """Place one fixture at the start of a 4096 B section (two-chunk layout)."""
    if len(payload) > FIXTURE_TWO_CHUNK_PAD:
        raise FixturePinError(
            f'fixture {entry["id"]} is {len(payload)} B, above the '
            f'{FIXTURE_TWO_CHUNK_PAD} B pad')
    return payload + bytes(FIXTURE_TWO_CHUNK_PAD - len(payload))


def build_legacy_carrier(seed, name, k, seq, out_dir, pins, fixtures_dir,
                         cache_dir, fetch, used=None):
    """Build one legacy carrier from the pinned fixtures the seed draws.

    Layout is `single-fixture` for every class but `legacy-partial`, which is
    `two-fixture`: the CLEAN fixture at offset 0 and the DAMAGED one at 4096, so
    the damaged chunk is a NON-ROOT chunk.  That distinction is what makes P > 0:
    a failing non-root chunk is carved and published as a regular file, a failing
    root chunk publishes nothing (measured this wave, and in round 41 F7).
    """
    recipe = RECIPES[name]
    primary, secondary = fixture_pair(seed, name, k, pins, used)
    features = legacy_features(recipe, primary, secondary)
    endian = primary['endian']
    parts = []
    damage_report = None

    if recipe.get('pair'):
        clean_bytes = fixture_bytes(primary, fixtures_dir, cache_dir, fetch)[0]
        secondary_bytes = fixture_bytes(secondary, fixtures_dir, cache_dir,
                                        fetch)[0]
        damaged_bytes = apply_fixture_damage(secondary_bytes, secondary)
        image = (pad_fixture_section(clean_bytes, primary)
                 + pad_fixture_section(damaged_bytes, secondary))
        parts = [
            {'offset': 0, 'length': FIXTURE_TWO_CHUNK_PAD,
             'fixture': primary['id'], 'handler': primary['handler'],
             'endian': primary['endian'], 'role': 'clean legacy fixture',
             'sha256': hashlib.sha256(clean_bytes).hexdigest()},
            {'offset': FIXTURE_TWO_CHUNK_PAD, 'length': FIXTURE_TWO_CHUNK_PAD,
             'fixture': secondary['id'], 'handler': secondary['handler'],
             'endian': secondary['endian'],
             'role': 'pinned 4-byte zero window (%d B) -> sasquatch fails'
                     % secondary['damage_len'],
             'sha256': hashlib.sha256(damaged_bytes).hexdigest()},
        ]
        damage_report = {'recipe': 'fixture-damage', 'fixture': secondary['id'],
                         'offset': secondary['damage_offset'],
                         'length': secondary['damage_len'],
                         'chunk': 2, 'chunk_offset': FIXTURE_TWO_CHUNK_PAD}
        oracle = {'kind': 'two-fixture', 'parts': parts}
        compression = secondary['compression']
        layout = 'two-fixture'
    else:
        raw = fixture_bytes(primary, fixtures_dir, cache_dir, fetch)[0]
        image = apply_fixture_damage(raw, primary) if recipe.get('damage') else raw
        if recipe.get('damage'):
            damage_report = {'recipe': 'fixture-damage',
                             'fixture': primary['id'],
                             'offset': primary['damage_offset'],
                             'length': primary['damage_len'], 'chunk': 1}
        oracle = {'kind': 'single-fixture', 'fixture': primary['id'],
                  'handler': primary['handler'], 'endian': primary['endian'],
                  'expected_files': primary.get('expected_files'),
                  'sha256_clean': primary['sha256'],
                  'sha256_carrier': hashlib.sha256(image).hexdigest()}
        compression = primary['compression']
        layout = 'single-fixture'

    carrier_id = f'H{seq:02d}'
    dest = os.path.join(out_dir, carrier_id)
    os.makedirs(dest, exist_ok=True)
    carrier = os.path.join(dest, 'carrier.sqsh')
    with open(carrier, 'wb') as handle:
        handle.write(image)
    entry = {
        'id': carrier_id,
        'class': name,
        'label': recipe['label'],
        'action': ACTIONS[recipe['label']],
        'arm': recipe['arm'],
        'endian': endian,
        'compression': compression,
        'tree': 'fixture',
        'content': 'fixture',
        'symlinks': [],
        'corruption': recipe['corruption'],
        'damage': damage_report,
        'layout': layout,
        'chunks': parts or None,
        'nested': None,
        'fixture': {
            'clean': {'id': primary['id'], 'handler': primary['handler'],
                      'endian': primary['endian'], 'sha256': primary['sha256'],
                      'url': fixture_url(primary)},
            'damaged': (None if secondary is None else
                        {'id': secondary['id'],
                         'handler': secondary['handler'],
                         'endian': secondary['endian'],
                         'sha256': secondary['sha256'],
                         'url': fixture_url(secondary)}),
            'pins': FIXTURE_PIN_COMMIT,
        },
        'rea': rea_params(recipe),
        'operation': 'extract_firmware',
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': hashlib.sha256(image).hexdigest(),
        DECLARED_KEY: declared_tuple(features),
        DECLARED_EXTRAS_KEY: declared_extras(features),
        'class_expected': {
            'label': recipe['label'],
            'action': ACTIONS[recipe['label']],
            'reported_only': True,
        },
    }
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': seed, 'class': name, 'id': carrier_id,
                   'endian': endian, 'compression': compression,
                   'label': recipe['label'],
                   'action': ACTIONS[recipe['label']],
                   'fixture': entry['fixture'],
                   'chunks': entry['chunks'],
                   DECLARED_KEY: entry[DECLARED_KEY],
                   DECLARED_EXTRAS_KEY: entry[DECLARED_EXTRAS_KEY],
                   'class_expected': entry['class_expected'],
                   'oracle': oracle}, handle, indent=2)
        handle.write('\n')
    entry['seed_dependent'] = False   # pinned third-party bytes
    return entry, {'endian': endian, 'comp': compression,
                   'corruption': damage_report, 'nested': None,
                   'files': 0, 'symlinks': 0,
                   'fixtures': [primary['id']] + ([secondary['id']]
                                                  if secondary else [])}


# ---------------------------------------------------------------------------
# A1 containers and residue
# ---------------------------------------------------------------------------
RESIDUE_TAIL = 64
# An 8-byte alphabet that appears in no SquashFS/tar/compression magic this
# pipeline matches; a seeded tail is drawn from it so the bytes are non-zero
# (trailing zeros are PADDING, not residue) and not a lane constant.
RESIDUE_BYTES = bytes.fromhex('d3a7f10c6b5e8429')
CHUNK_PAD = 4096
CONTAINER_MEMBER = 'rootfs.sqsh'


def residue_tail(seed, name, k, length=RESIDUE_TAIL):
    stream = stream_bytes(f'{seed}:residue:{name}:{k}'.encode(), length)
    return bytes(RESIDUE_BYTES[byte % len(RESIDUE_BYTES)] for byte in stream)


def pad_to_chunk(payload):
    """Zero-pad to the 4 KiB boundary unblob's chunk calculator rounds up to."""
    remainder = len(payload) % CHUNK_PAD
    return payload if not remainder else payload + bytes(CHUNK_PAD - remainder)


def build_tar(member, payload, dest):
    """A byte-stable USTAR container: mtime 0, root-owned, empty uname/gname."""
    import tarfile  # the container classes are the only tar producers
    with tarfile.open(dest, 'w', format=tarfile.USTAR_FORMAT) as tar:
        info = tarfile.TarInfo(member)
        info.size = len(payload)
        info.mtime = 0
        info.mode = 0o644
        info.uid = info.gid = 0
        info.uname = info.gname = ''
        tar.addfile(info, io.BytesIO(payload))


def build_container_carrier(seed, name, k, seq, writer, scratch, out_dir, pins,
                            fixtures_dir, cache_dir, fetch, used=None):
    """A squashfs image inside a tar, extracted at ``--max-depth 1``.

    Measured: H = {'tar'}, F = 0, G = {depth-limited}, P = 1 (the member
    ``rootfs.sqsh`` is published at the ceiling), no argv.  The image inside is
    never opened at this depth, which is the whole point of the class: no
    SquashFS handler at this depth is not evidence of no SquashFS image.
    """
    recipe = RECIPES[name]
    class_index = list(RECIPES).index(name)
    rng = random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))
    material = f'{seed}:{name}:{k}'.encode()
    work = os.path.join(scratch, f'build-{seq:02d}')
    os.makedirs(work)
    if k == 1:
        tree = os.path.join(work, 'tree')
        os.makedirs(tree)
        dirs, files, symlinks = build_tree(rng, material, tree, (), 'stream')
        fill_empty_dirs(rng, material, tree, dirs, files, 'stream')
        inner = os.path.join(work, 'member.sqsh')
        with contextlib.redirect_stdout(io.StringIO()):
            writer.build_image(tree, inner, 'le', 'gzip')
        body = open(inner, 'rb').read()
        inner_record = {'kind': 'generated-v4', 'endian': 'le',
                        'compression': 'gzip', 'handler': 'squashfs_v4_le',
                        'sha256': hashlib.sha256(body).hexdigest(),
                        'files': len(files)}
        endian, compression = 'le', 'gzip'
    else:
        fixture, _ = fixture_pair(seed, name, k, pins, used)
        body = fixture_bytes(fixture, fixtures_dir, cache_dir, fetch)[0]
        inner_record = {'kind': 'pinned-fixture', 'fixture': fixture['id'],
                        'handler': fixture['handler'],
                        'endian': fixture['endian'],
                        'sha256': fixture['sha256']}
        endian, compression = fixture['endian'], fixture['compression']
    image = os.path.join(work, 'carrier.tar')
    build_tar(CONTAINER_MEMBER, body, image)
    features = {
        'handler_set': ['tar'],
        'gap_kinds': ['depth-limited'],
        'gap_dependencies': [],
        'be_argv': 'n/a',
        'symlink_removed': False,
        'published': 'nonzero',
        'extraction_failed': False,
        'max_depth': 1,
    }
    payload = open(image, 'rb').read()
    return _finish_simple(name, k, seq, out_dir, recipe, features,
                          payload, {
                              'seed_dependent': k == 1,
                              'endian': endian, 'compression': compression,
                              'layout': 'tar-container',
                              'container': {'format': 'ustar',
                                            'member': CONTAINER_MEMBER,
                                            'member_size': len(body),
                                            'sha256': hashlib.sha256(payload).hexdigest()},
                              'inner': inner_record,
                              'oracle': {'kind': 'tar-container',
                                         'member': CONTAINER_MEMBER,
                                         'inner': inner_record},
                          })


def build_residue_carrier(seed, name, k, seq, writer, scratch, out_dir, pins,
                          fixtures_dir, cache_dir, fetch):
    """A squashfs image followed by seeded NON-PADDING bytes.

    Measured: G = {unknown-chunk-handler} (REA mints it for the chunk whose
    handler is null and publishes ``<start>-<end>.unknown``), H keeps the
    SquashFS handler, P = image files + the .unknown carve, no argv.
    """
    recipe = RECIPES[name]
    class_index = list(RECIPES).index(name)
    rng = random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))
    material = f'{seed}:{name}:{k}'.encode()
    work = os.path.join(scratch, f'build-{seq:02d}')
    os.makedirs(work)
    if k == 1:
        tree = os.path.join(work, 'tree')
        os.makedirs(tree)
        dirs, files, symlinks = build_tree(rng, material, tree, (), 'stream')
        fill_empty_dirs(rng, material, tree, dirs, files, 'stream')
        inner = os.path.join(work, 'body.sqsh')
        with contextlib.redirect_stdout(io.StringIO()):
            writer.build_image(tree, inner, 'le', 'gzip')
        body = open(inner, 'rb').read()
        handler, endian, compression = 'squashfs_v4_le', 'le', 'gzip'
        oracle = tree_oracle(tree, dirs, files, symlinks)
    else:
        fixture, _ = fixture_pair(seed, name, k, pins)
        body = fixture_bytes(fixture, fixtures_dir, cache_dir, fetch)[0]
        handler, endian, compression = (fixture['handler'], fixture['endian'],
                                        fixture['compression'])
        oracle = {'kind': 'pinned-fixture', 'fixture': fixture['id'],
                  'handler': fixture['handler']}
    body = pad_to_chunk(body)
    tail = residue_tail(seed, name, k)
    payload = body + tail
    features = {
        'handler_set': [handler],
        'gap_kinds': ['unknown-chunk-handler'],
        'gap_dependencies': [],
        'be_argv': 'n/a',
        'symlink_removed': False,
        'published': 'nonzero',
        'extraction_failed': False,
        'max_depth': DEFAULT_MAX_DEPTH,
    }
    return _finish_simple(name, k, seq, out_dir, recipe, features, payload, {
        'seed_dependent': True,   # the residue tail is seeded
        'endian': endian, 'compression': compression,
        'layout': 'image+residue',
        'residue': {'offset': len(body), 'length': len(tail),
                    'sha256': hashlib.sha256(tail).hexdigest()},
        'oracle': oracle,
    })


def _finish_simple(name, k, seq, out_dir, recipe, features, payload, detail):
    """Write one carrier whose bytes are decided by its builder."""
    carrier_id = f'H{seq:02d}'
    dest = os.path.join(out_dir, carrier_id)
    os.makedirs(dest, exist_ok=True)
    carrier = os.path.join(dest, 'carrier.sqsh')
    with open(carrier, 'wb') as handle:
        handle.write(payload)
    entry = {
        'id': carrier_id,
        'class': name,
        'label': recipe['label'],
        'action': ACTIONS[recipe['label']],
        'arm': recipe['arm'],
        'endian': detail['endian'],
        'compression': detail['compression'],
        'tree': recipe['tree'],
        'content': recipe['content'],
        'symlinks': [],
        'corruption': recipe['corruption'],
        'damage': None,
        'layout': detail['layout'],
        'chunks': None,
        'nested': None,
        'rea': rea_params(recipe),
        'operation': 'extract_firmware',
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': hashlib.sha256(payload).hexdigest(),
        DECLARED_KEY: declared_tuple(features),
        DECLARED_EXTRAS_KEY: declared_extras(features),
        'class_expected': {
            'label': recipe['label'],
            'action': ACTIONS[recipe['label']],
            'reported_only': True,
        },
    }
    entry['seed_dependent'] = bool(detail.get('seed_dependent'))
    for key in ('container', 'residue', 'inner'):
        if key in detail:
            entry[key] = detail[key]
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': None, 'class': name, 'id': carrier_id,
                   'label': recipe['label'], 'action': ACTIONS[recipe['label']],
                   DECLARED_KEY: entry[DECLARED_KEY],
                   DECLARED_EXTRAS_KEY: entry[DECLARED_EXTRAS_KEY],
                   'class_expected': entry['class_expected'],
                   'oracle': detail.get('oracle')}, handle, indent=2)
        handle.write('\n')
    return entry, {'endian': detail['endian'], 'comp': detail['compression'],
                   'corruption': None, 'nested': None,
                   'files': 0, 'symlinks': 0}


# ---------------------------------------------------------------------------
# the seeded factorial family
# ---------------------------------------------------------------------------
def build_combo_carrier(seed, k, seq, writer, scratch, out_dir, pins,
                        fixtures_dir, cache_dir, fetch):
    """Build one `combo` carrier (C01..C24) and declare the tuple its factors imply.

    Layout assembly, in this order: body (legacy fixture / generated v4 image /
    both) -> optional USTAR wrap -> optional seeded residue after the 4 KiB
    boundary.  The declared tuple is computed from the factor vector alone; no
    named class is consulted and nothing is measured at generation time.
    """
    rng, factors = combo_draw(seed, k, pins)
    material = f'{seed}:combo:{k}'.encode()
    declared = combo_declared(factors)
    legacy_pin = next(f for f in pins['fixtures']
                      if f['id'] == factors['legacy_fixture'])

    work = os.path.join(scratch, f'build-{seq:02d}')
    os.makedirs(work)
    parts, oracle = [], {}
    damage = None
    symlinks, files = [], []
    legacy_bytes = None
    v4_bytes = None

    if factors['base'] == 'legacy':
        raw = fixture_bytes(legacy_pin, fixtures_dir, cache_dir, fetch)[0]
        if factors['damage'] and not factors['second_v4']:
            legacy_bytes = apply_fixture_damage(raw, legacy_pin)
            damage = {'recipe': 'fixture-damage', 'fixture': legacy_pin['id'],
                      'offset': legacy_pin['damage_offset'],
                      'length': legacy_pin['damage_len'], 'chunk': 1}
        else:
            legacy_bytes = raw
        if not factors['second_v4']:
            parts = [{'offset': 0, 'length': len(legacy_bytes),
                      'fixture': legacy_pin['id'],
                      'handler': legacy_pin['handler'],
                      'endian': legacy_pin['endian'],
                      'sha256': hashlib.sha256(legacy_bytes).hexdigest()}]
        else:
            parts = [{'offset': 0, 'length': FIXTURE_TWO_CHUNK_PAD,
                      'fixture': legacy_pin['id'],
                      'handler': legacy_pin['handler'],
                      'endian': legacy_pin['endian'],
                      'sha256': hashlib.sha256(legacy_bytes).hexdigest()}]

    if factors['body_v4']:
        tree = os.path.join(work, 'tree')
        os.makedirs(tree)
        kinds = {'none': (), 'in-tree': ('in-tree',), 'escaping': ('escaping',),
                 'both': ('in-tree', 'escaping')}[factors['links']]
        content = 'pattern' if factors['damage'] else 'stream'
        dirs, files, symlinks = build_tree(
            rng, material, tree, kinds, content,
            # A damaged block must not pre-empt the links, or the declared
            # unpublished-entry / SR facts would depend on directory order.
            link_placement='root-first' if factors['damage'] else 'rng')
        fill_empty_dirs(rng, material, tree, dirs, files, content)
        oracle = tree_oracle(tree, dirs, files, symlinks)
        image = os.path.join(work, 'v4.sqsh')
        with contextlib.redirect_stdout(io.StringIO()):
            writer.build_image(tree, image, factors['endian'], factors['comp'])
        if factors['damage']:
            with open(image, 'rb') as handle:
                payload = bytearray(handle.read())
            report = {}
            payload = CORRUPTIONS['partial'](payload, factors['endian'], report)
            damage = {'recipe': 'partial', **report,
                      'chunk': 2 if factors['two_chunk'] else 1}
            with open(image, 'wb') as handle:
                handle.write(bytes(payload))
        v4_bytes = open(image, 'rb').read()
        offset = FIXTURE_TWO_CHUNK_PAD if factors['two_chunk'] else 0
        parts.append({'offset': offset, 'length': len(v4_bytes),
                      'role': 'generated SquashFS 4.0 image',
                      'endian': factors['endian'],
                      'compression': factors['comp'],
                      'handler': V4_HANDLER[factors['endian']],
                      'sha256': hashlib.sha256(v4_bytes).hexdigest()})

    if factors['two_chunk']:
        body = pad_fixture_section(legacy_bytes, legacy_pin) + v4_bytes
        layout = 'legacy+v4'
    elif factors['base'] == 'legacy':
        body = legacy_bytes
        layout = 'single-fixture'
    else:
        body = v4_bytes
        layout = 'single-image'

    container = None
    if factors['wrap']:
        tar_path = os.path.join(work, 'body.tar')
        build_tar(CONTAINER_MEMBER, body, tar_path)
        container = {'format': 'ustar', 'member': CONTAINER_MEMBER,
                     'member_size': len(body)}
        body = open(tar_path, 'rb').read()
        container['sha256'] = hashlib.sha256(body).hexdigest()
        layout = f'tar({layout})'

    residue = None
    if factors['residue']:
        padded = pad_to_chunk(body)
        tail = residue_tail(seed, 'combo', k)
        residue = {'offset': len(padded), 'length': len(tail),
                   'sha256': hashlib.sha256(tail).hexdigest()}
        body = padded + tail
        layout = f'{layout}+residue'

    carrier_id = f'{COMBO_ID_PREFIX}{k:02d}'
    dest = os.path.join(out_dir, carrier_id)
    os.makedirs(dest, exist_ok=True)
    carrier = os.path.join(dest, 'carrier.sqsh')
    with open(carrier, 'wb') as handle:
        handle.write(body)
    entry = {
        'id': carrier_id,
        'class': 'combo',
        'family': 'combo',
        'combo_index': k,
        'factors': dict(factors),
        'decisions': list(factors['decisions']),
        'label': None,
        'action': None,
        'arm': 'before' if factors['dep'] else 'after',
        'endian': factors['endian'],
        'compression': factors['comp'],
        'tree': 'random' if factors['body_v4'] else 'fixture',
        'content': ('pattern' if factors['damage'] else 'stream')
        if factors['body_v4'] else 'fixture',
        'symlinks': list(factors['links'] if factors['links'] != 'none' else ()),
        'corruption': damage['recipe'] if damage else None,
        'damage': damage,
        'layout': layout,
        'chunks': parts,
        'container': container,
        'residue': residue,
        'nested': None,
        'rea': {'max_depth': factors['max_depth']},
        'operation': 'extract_firmware',
        'carrier': f'{carrier_id}/carrier.sqsh',
        'sha256': hashlib.sha256(body).hexdigest(),
        DECLARED_KEY: declared,
        DECLARED_EXTRAS_KEY: {
            'extraction_failed': bool(
                (factors['damage'] or factors['dep'])
                and not (factors['wrap'] and factors['max_depth'] == 1)),
            'max_depth': factors['max_depth'],
        },
        # A combo has no class label: the evaluator alone supplies the expected
        # pair, so this field is null by design.
        'class_expected': None,
    }
    with open(os.path.join(dest, 'tree.json'), 'w', encoding='utf-8') as handle:
        json.dump({'seed': seed, 'class': 'combo', 'id': carrier_id,
                   'factors': dict(factors), 'decisions': list(factors['decisions']),
                   'endian': factors['endian'], 'compression': factors['comp'],
                   'chunks': parts, 'container': container, 'residue': residue,
                   DECLARED_KEY: declared,
                   DECLARED_EXTRAS_KEY: entry[DECLARED_EXTRAS_KEY],
                   'class_expected': None, 'oracle': oracle},
                  handle, indent=2)
        handle.write('\n')
    entry['seed_dependent'] = bool(factors['body_v4'] or factors['residue'])
    return entry, {'endian': factors['endian'], 'comp': factors['comp'],
                   'corruption': damage, 'nested': None,
                   'files': len(files), 'symlinks': len(symlinks)}


# ---------------------------------------------------------------------------
# REA runs
# ---------------------------------------------------------------------------
def rea_env(arm):
    env = dict(os.environ)
    home_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
    env['REA_UNBLOB_COMMAND'] = os.path.join(home_bin, 'unblob')
    if arm == 'before':
        want = os.path.realpath(home_bin)
        kept = [p for p in env.get('PATH', '').split(os.pathsep)
                if p and os.path.realpath(p) != want]
        env['PATH'] = os.pathsep.join(kept)
    return env


def _be_argv(commands):
    """'-be' in a recorded extractor child argv: 'yes' / 'no' / 'n/a'.

    unblob's SquashFSExtractor (26.6.4 handlers/filesystem/squashfs.py:30-42)
    appends '-be' for a BIG-endian v4 image UNLESS mkfs_time == bytes_used (the
    AVM marker, which drops it), and '-le' for little-endian.  Only a FAILED
    extraction leaves the argv in the envelope (ExtractCommandFailedReport), so
    a clean run reports 'n/a': the precedence text only reads BE on the
    extractor-failure branch, and a missing argv must not be read as 'no'.
    """
    seen = False
    for command in commands:
        tokens = command.split()
        if not tokens:
            continue
        base = posixpath.basename(tokens[0])
        if base.startswith('sasquatch') or base.startswith('unsquashfs'):
            seen = True
            if '-be' in tokens[1:]:
                return 'yes'
    return 'no' if seen else 'n/a'


def _envelope_parts(full):
    """(data object or None, subject sha256, shape summary) from a CLI envelope."""
    if not isinstance(full, dict) or not isinstance(full.get('data'), dict):
        return None, None, {}
    data = full['data']
    normalized = data.get('normalized_result') or {}
    reports = [diag.get('report') or {}
               for diag in normalized.get('diagnostics') or []]
    shape = {
        'operation': data.get('operation'),
        'provider': (data.get('provider') or {}).get('id'),
        'handlers': sorted({chunk.get('handler')
                            for chunk in normalized.get('chunks') or []
                            if chunk.get('handler')}),
        'failed_chunks': sorted({chunk.get('handler')
                                 for chunk in normalized.get('chunks') or []
                                 if chunk.get('extraction_failed') and chunk.get('handler')}),
        'gap_kinds': sorted({gap.get('kind')
                             for gap in normalized.get('extraction_gaps') or []
                             if gap.get('kind')}),
        'gap_dependencies': sorted({dep
                                    for gap in normalized.get('extraction_gaps') or []
                                    for dep in (gap.get('dependencies') or [])}),
        'diagnostics': sorted({report.get('__typename__')
                               for report in reports
                               if report.get('__typename__')}),
        # R41-C2 features beyond v2's shape: the two the precedence text reads
        # besides H/G/D/P (BE and SR), plus the realised depth and the
        # structural depth cap evidence.
        'be_argv': _be_argv([report.get('command') for report in reports
                             if report.get('command')]),
        'symlink_removed': any(report.get('__typename__')
                               == 'MaliciousSymlinkRemoved' for report in reports),
        'depth_limited_paths': len(normalized.get('depth_limited_paths') or []),
        'parameters': {'max_depth': (data.get('parameters') or {}).get('max_depth')},
        'files': len(normalized.get('files') or []),
        'coverage': normalized.get('coverage'),
    }
    subject = (data.get('subject') or {}).get('digest') or {}
    return data, subject.get('sha256'), shape


def _write_envelope(entry, full, gz):
    dest = os.path.join(OUT_DIR, entry['id'])
    payloads = {'envelope': full.get('data'),
                'rea-full': full}
    for stem, obj in payloads.items():
        path = os.path.join(dest, stem + '.json')
        blob = (json.dumps(obj, indent=2) + '\n').encode('utf-8')
        if gz:
            with open(path + '.gz', 'wb') as handle:
                with gzip.GzipFile(fileobj=handle, mode='wb', mtime=0) as stream:
                    stream.write(blob)
        else:
            with open(path, 'wb') as handle:
                handle.write(blob)


def _parse_stdout(stdout):
    text = (stdout or '').strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find('{')
        if start < 0:
            return None
        try:
            return json.loads(text[start:])
        except json.JSONDecodeError:
            return None


def run_rea(entry, scratch, keep_extraction, gz):
    """Run REA extract-firmware once for one carrier and store its envelope."""
    carrier = os.path.join(OUT_DIR, entry['carrier'])
    work = os.path.join(scratch, f'rea-{entry["id"]}')
    os.makedirs(work)
    outdir = os.path.join(work, 'out')  # REA refuses an existing output dir
    depth = str(entry['rea']['max_depth'])
    cmd = ['npx', '-y', REA_PACKAGE, 'extract-firmware', '--format', 'json',
           '--full-output', '--max-depth', depth, carrier, outdir]
    env = rea_env(entry['arm'])
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    home_bin = os.path.join(os.path.expanduser('~'), '.local', 'bin')
    record = {'id': entry['id'], 'class': entry['class'], 'arm': entry['arm'],
              'operation': 'extract_firmware',
              'max_depth': int(depth),
              'expected_label': entry['label'],
              'expected_action': entry['action'],
              'class_expected': entry.get('class_expected'),
              'declared': entry.get('declared'),
              'declared_extras': entry.get('declared_extras'),
              'factors': entry.get('factors'),
              'exit_code': proc.returncode,
              'rea_argv': [REA_PACKAGE, 'extract-firmware', '--format', 'json',
                           '--full-output', '--max-depth', depth,
                           entry['carrier'], '$out'],
              'unblob_command': env['REA_UNBLOB_COMMAND'],
              'home_bin_on_path': any(
                  os.path.realpath(p) == os.path.realpath(home_bin)
                  for p in env.get('PATH', '').split(os.pathsep) if p)}
    full = _parse_stdout(proc.stdout)
    data, subject_sha, shape = _envelope_parts(full)
    if data is None:
        record['error'] = 'no JSON envelope on stdout'
        record['stdout_head'] = (proc.stdout or '').strip()[:400]
        record['stderr_head'] = (proc.stderr or '').strip()[-400:]
    else:
        _write_envelope(entry, full, gz)
        record['ok'] = full.get('ok')
        record['subject_sha256'] = subject_sha
        record['digest_matches_carrier'] = subject_sha == entry['sha256']
        record['duration'] = (full.get('meta') or {}).get('duration')
        record.update(shape)
    with open(os.path.join(OUT_DIR, entry['id'], 'run.json'), 'w',
              encoding='utf-8') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    if not keep_extraction:
        shutil.rmtree(work, ignore_errors=True)
    return record


def out_of_domain_run(entry, scratch, keep_extraction, gz, operation=DEFAULT_OOD_OP):
    """Out-of-domain arm: run ``operation`` (not extract-firmware) on the carrier.

    PLACEHOLDER BINDING: the operation is the CLI ``--ood-op`` value and is
    stored in the manifest under ``out_of_domain.operation`` so the freeze can
    rebind it without touching this function.  The default,
    ``inspect-firmware-regions``, returns a complete Evidence envelope with
    ``operation == "inspect_firmware_regions"`` and ``provider.id == "binwalk"``
    on a SquashFS carrier -- a valid envelope that is not an unblob
    extract-firmware outcome.  It takes no output directory.
    """
    carrier = os.path.join(OUT_DIR, entry['carrier'])
    work = os.path.join(scratch, f'ood-{entry["id"]}')
    os.makedirs(work)
    cmd = ['npx', '-y', REA_PACKAGE, operation, '--format', 'json',
           '--full-output', carrier]
    env = rea_env('after')
    proc = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True)
    record = {'id': entry['id'], 'class': entry['class'], 'arm': 'ood',
              'operation': operation,
              'expected_label': entry['label'],
              'expected_action': entry['action'],
              'class_expected': entry.get('class_expected'),
              'declared': entry.get('declared'),
              'declared_extras': entry.get('declared_extras'),
              'exit_code': proc.returncode,
              'rea_argv': [REA_PACKAGE, operation, '--format', 'json',
                           '--full-output', entry['carrier']],
              'unblob_command': env['REA_UNBLOB_COMMAND']}
    full = _parse_stdout(proc.stdout)
    data, subject_sha, shape = _envelope_parts(full)
    if data is None:
        # An error envelope ({ok:false, error:...}) is itself out-of-domain
        # material, but the frozen set should hold structured evidence: record
        # the failure loudly instead of silently accepting it.
        record['error'] = 'no Evidence envelope on stdout'
        record['stdout_head'] = (proc.stdout or '').strip()[:400]
        record['stderr_head'] = (proc.stderr or '').strip()[-400:]
    else:
        _write_envelope(entry, full, gz)
        record['ok'] = full.get('ok')
        record['subject_sha256'] = subject_sha
        record['digest_matches_carrier'] = subject_sha == entry['sha256']
        record['duration'] = (full.get('meta') or {}).get('duration')
        record.update(shape)
    with open(os.path.join(OUT_DIR, entry['id'], 'run.json'), 'w',
              encoding='utf-8') as handle:
        json.dump(record, handle, indent=2)
        handle.write('\n')
    if not keep_extraction:
        shutil.rmtree(work, ignore_errors=True)
    return record


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
OUT_DIR = None


def parse_classes(value):
    wanted = [item.strip() for item in value.split(',') if item.strip()]
    if not wanted:
        raise SystemExit('--classes selected no class')
    known = list(RECIPES) + list(FAMILIES)
    unknown = [name for name in wanted if name not in known]
    if unknown:
        raise SystemExit(f'unknown class(es): {", ".join(unknown)}; '
                         f'known: {", ".join(known)}')
    return [name for name in known if name in wanted]


def actions_line(path):
    """Read the frozen `<!-- sqfs-triage-actions: ... -->` token line."""
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            if ACTIONS_LINE_TAG in line:
                body = line.split(ACTIONS_LINE_TAG, 1)[1]
                body = body.split('-->', 1)[0]
                tokens = body.split()
                if tokens:
                    return tokens
    raise SystemExit(f'no {ACTIONS_LINE_TAG} token line in {path}')


def check_action_tokens(tokens, path):
    """The manifest may only emit tokens the bound table line declares.

    ``none`` is the interpreter's no-match default, not a row token, so a line
    that lists only the row tokens is still consistent with a map that answers
    ``unclassified`` with ``none``.
    """
    want = set(ACTIONS.values()) - {NO_MATCH_TOKEN}
    have = set(tokens) - {NO_MATCH_TOKEN}
    if want == have:
        return
    missing = sorted(want - have)
    extra = sorted(have - want)
    raise SystemExit(
        f'action vocabulary mismatch against {path}: the selected '
        f'--actions-set {ACTION_SET_NAME!r} emits {missing} which the line does '
        f'not declare, and the line declares {extra} which the manifest does not '
        f'use.  Select the --actions-set whose tokens match the frozen line, or '
        f'edit ACTION_SETS; carriers are unaffected.')


def build_set(seed, classes, writer, out_dir, scratch, pins, fixtures_dir,
              cache_dir, fetch):
    """Build every carrier and the manifest into ``out_dir``."""
    os.makedirs(out_dir, exist_ok=True)
    carriers, details, seq, used_fixtures = [], {}, 0, set()
    for name in classes:
        if name in FAMILIES:
            for k in range(1, FAMILIES[name] + 1):
                seq += 1
                entry, extra = build_combo_carrier(
                    seed, k, seq, writer, scratch, out_dir, pins,
                    fixtures_dir, cache_dir, fetch)
                carriers.append(entry)
                details[entry['id']] = extra
            continue
        for k in range(1, CARRIERS_PER_CLASS + 1):
            seq += 1
            entry, extra = build_carrier(seed, name, k, seq, writer, scratch,
                                         out_dir, pins, fixtures_dir, cache_dir,
                                         fetch, used_fixtures)
            carriers.append(entry)
            details[entry['id']] = extra
    named_union = sorted({json.dumps(c[DECLARED_KEY], sort_keys=True)
                          for c in carriers if c['class'] != 'combo'})
    named_union_set = set(named_union)
    for entry in carriers:
        if entry['class'] == 'combo':
            entry['outside_named_union_declared'] = (
                json.dumps(entry[DECLARED_KEY], sort_keys=True)
                not in named_union_set)
    combos = [c for c in carriers if c['class'] == 'combo']
    unseen = [c['id'] for c in combos if c['outside_named_union_declared']]
    if (combos and len(unseen) * 2 < len(combos)
            and not ALLOW_UNSEEN_MINORITY):
        raise SystemExit(
            f'combo_unseen_majority does not hold: {len(unseen)}/{len(combos)} '
            f'combos are outside the named declared-tuple union.  The freeze '
            f'binding requires at least half, so the factor draw is too narrow '
            f'(critic P8: this must fail at build time, not after the freeze).  '
            f'Re-run with --allow-unseen-minority only to inspect the set.')
    manifest = {
        'seed': seed,
        'round': 42,
        'claim': 'R42-C2',
        'generator': {
            'name': 'heldout-gen-v4.py',
            'version': VERSION,
            'sha256': sha256_file(os.path.abspath(__file__)),
            'carriers_per_class': CARRIERS_PER_CLASS,
            'writer': {
                'name': 'gen-squashfs.py',
                'path': writer_logical_path(os.path.abspath(WRITER_PATH)),
                'sha256': sha256_file(os.path.abspath(WRITER_PATH)),
                'block_encoder': BLOCK_ENCODER,
            },
            'partial_pin': {
                'rule': 'R40-CL4',
                'pinned_by': 'compressed-length',
                'fill': '%02x' % PARTIAL_FILL,
                'max_damaged_block': MAX_DAMAGED_BLOCK,
                'measured_fail_range': [26, 136],
                'measured_absorbed_from': 1730,
                'measured_by': 'round-40 w2 R40W2MistakeHunt MH-4 §3',
            },
            'fixtures': {
                'pins': FIXTURE_PINS_LOGICAL,
                'pins_sha256': sha256_file(os.path.abspath(FIXTURE_PINS_PATH)),
                'project': FIXTURE_PIN_PROJECT,
                'commit': FIXTURE_PIN_COMMIT,
                'url_base': FIXTURE_URL_BASE,
                'license': pins['pinned'].get('license'),
                'count': len(pins['fixtures']),
                'resolution': ('committed copy under --fixtures-dir, else the '
                               'cache under --scratch, else the pinned URL with '
                               '--fetch; each candidate is sha256-checked'),
                'damage_recipe': ('pinned 4-byte zero window at '
                                  'damage_offset; pre-verified with sasquatch '
                                  '4.5.1 + REA 6.5.0, never probed at run time'),
            },
        },
        'action_vocabulary': sorted(set(ACTIONS.values())),
        'action_set': ACTION_SET_NAME,
        'action_source': ACTION_SOURCE,
        'label_actions': dict(ACTIONS),
        'new_labels': ['depth-limited', 'legacy-body-failure'],
        'new_label_tokens_binding': (
            'draft42 tokens are the round-42 precedence text verbatim (rule '
            '1-13); the frozen SKILL v4 action line decides, and a mismatch is '
            'a loud exit (--actions-set/--actions-file; carriers do not change)'),
        'precedence_observations': [
            {'rule': 3,
             'claim': 'every v1-v3 chunk resolves plain `sasquatch` [TBC]',
             'measured': ("CONFIRMED: unblob SquashFSExtractor runs `sasquatch "
                          "-be` for a v1-v3 BIG-endian chunk (handler version != "
                          "4), and the failing Command reports its own executable "
                          "(unblob/extractors/command.py:68-73), so D = "
                          "['sasquatch'] and rule 3 answers (dep-missing-le, "
                          "install-extractor-le) for a big-endian legacy chunk."),
             'carriers': ['legacy-dep-missing-be']},
            {'rule': 6,
             'claim': 'a v1-v3 body failure lands legacy-body-failure',
             'measured': ('CONFIRMED on all 14 pinned fixtures x both endianness '
                          'strata: G={extractor-failure}, P=0, argv -be/-le '
                          'recorded, handler from the v1-v3 family.')},
            {'rule': 8,
             'claim': 'depth-limited is minted whenever max_depth == 1',
             'measured': ('REFINED: only when an extraction actually reached the '
                          'ceiling.  A clean chunk at --max-depth 1 mints it; a '
                          'FAILING root chunk mints nothing (G={extractor-failure} '
                          'only). A failing non-root chunk does not suppress it, '
                          'because the sibling chunk still hits the ceiling.')},
        ],
        'rea': {'default_max_depth': DEFAULT_MAX_DEPTH,
                'per_class': {name: (rea_params(RECIPES[name])['max_depth']
                                     if name in RECIPES else None)
                              for name in classes}},
        'declared_schema': {
            'binding': 'observed_features_match_declared',
            'key': DECLARED_KEY,
            'fields': list(DECLARED_FIELDS),
            'types': {
                'handler_set': 'sorted list of handler names (empty = no chunk)',
                'gap_kinds': 'sorted list of extraction_gaps[].kind',
                'gap_dependencies': 'sorted union of extraction_gaps[].dependencies',
                'be_argv': "'yes' | 'no' | 'n/a' -- whether a recorded extractor "
                           "child argv carries -be; 'n/a' when no argv is recorded "
                           "(a successful run records none)",
                'symlink_removed': 'bool -- a MaliciousSymlinkRemoved diagnostic',
                'published': "'nonzero' (P > 0) | 'zero' (P == 0)",
            },
            'location': ('carriers[].declared_features -- ONE key for every class, '
                         'combos included (R41-CL1).  There is no `declared` key '
                         'and no `class_expected.features` key; declared_extras '
                         'carries extraction_failed and max_depth, which are NOT '
                         'part of the binding'),
        },
        'families': {name: {'count': count, 'id_prefix': COMBO_ID_PREFIX,
                            'factors': list(COMBO_FACTORS),
                            'combo_bases': list(COMBO_BASES),
                            'links_values': list(COMBO_LINKS),
                            'min_decisions': COMBO_MIN_DECISIONS,
                            'class_expected': None,
                            'note': 'factorial: expected tuple computed from the '
                                    'drawn factors, label given by the evaluator only'}
                     for name, count in FAMILIES.items()},
        'replicate_variation': replicate_variation(),
        'out_of_domain': {'operation': OOD_OP,
                          'label': RECIPES['out-of-domain']['label'],
                          'action': ACTIONS[RECIPES['out-of-domain']['label']]},
        'combo_unseen': {
            'binding': 'combo_unseen_majority',
            'definition': ('a combo is UNSEEN when its observed feature tuple is '
                           'outside the union of the NAMED classes\' declared '
                           'tuples; the union is the dev arm\'s, so the only way '
                           'to carry this at the freeze is a lookup control\'s '
                           'own key set'),
            'named_tuple_union_size': len(named_union),
            'named_tuple_union_sha256': hashlib.sha256(
                ('\n'.join(named_union) + '\n').encode()).hexdigest(),
            'combos': len(combos),
            'declared_outside': len(unseen),
            'declared_outside_ids': unseen,
            'decisions_per_combo': {c['id']: len(c['decisions']) for c in combos},
            'min_decisions': COMBO_MIN_DECISIONS,
            'note': ('declared_outside is the prediction from the declared '
                     'tuples; --verify recomputes it from the OBSERVED tuples and '
                     'prints both.  The two agree whenever the binding '
                     'observed_features_match_declared holds.'),
        },
        'classes': list(classes),
        'carriers': carriers,
    }
    with open(os.path.join(out_dir, 'manifest.json'), 'w', encoding='utf-8') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    for entry in carriers:
        extra = details[entry['id']]
        corruption = extra['corruption'] or {}
        nested = extra['nested'] or {}
        detail = (f"files={extra['files']} links={extra['symlinks']}"
                  + (f" damage={corruption.get('blocks_damaged')}blk"
                     f"/{corruption.get('bytes_damaged')}B"
                     if corruption.get('blocks_damaged') else '')
                  + (f" nested={nested.get('path')}" if nested else '')
                  + f" depth={entry['rea']['max_depth']}")
        print(f"{entry['id']}  {entry['class']:<26} {entry['endian']}/{entry['compression']:<4} "
              f"{entry['arm']:<6} {(entry['label'] or '-'):<26} "
              f"{(entry['action'] or '-'):<32} {entry['sha256']}  {detail}")
    return manifest, carriers


# ---------------------------------------------------------------------------
# dev proof: observed feature tuple vs the generator's own expectation
# ---------------------------------------------------------------------------
def observed_features(record):
    """The tuple the precedence text reads, as measured in one envelope."""
    return {
        'handler_set': sorted(record.get('handlers') or []),
        'gap_kinds': sorted(record.get('gap_kinds') or []),
        'gap_dependencies': sorted(record.get('gap_dependencies') or []),
        'symlink_removed': bool(record.get('symlink_removed')),
        'extraction_failed': bool(record.get('failed_chunks')),
        'published': 'nonzero' if (record.get('files') or 0) > 0 else 'zero',
        'be_argv': record.get('be_argv'),
        'max_depth': (record.get('parameters') or {}).get('max_depth'),
    }


def feature_diff(expected, observed):
    """Field-by-field difference; empty list means the tuple was reached."""
    return [f'{key}: want {want!r} got {observed.get(key)!r}'
            for key, want in expected.items() if observed.get(key) != want]


def expected_for(entry):
    """The tuple a carrier must reach: its DECLARED fields plus the reported extras.

    ``entry[DECLARED_KEY]`` is the six-field binding the counter checks; the two
    extras (``extraction_failed``, ``max_depth``) are cross-checked here as well
    because they are observable in every envelope.  A combo has no class
    expectation -- its tuple comes from the factors, and its label only from the
    evaluator.
    """
    expected = dict(entry[DECLARED_KEY])
    expected.update(entry.get(DECLARED_EXTRAS_KEY) or {})
    return expected


def verify(manifest, carriers):
    """Print carrier -> observed tuple and judge it against the declared tuple.

    Also scores the A1 binding ``combo_unseen_majority`` from the OBSERVED
    tuples: a combo is unseen when its six-field observed tuple is outside the
    union of the NAMED classes' declared tuples.
    """
    print('\n== dev feature table (observed vs DECLARED_FEATURES; labels are the '
          "evaluator's) ==")
    named_union = {json.dumps({k: e[DECLARED_KEY][k] for k in DECLARED_FIELDS},
                              sort_keys=True)
                   for e in carriers if e['class'] != 'combo'}
    rows, bad = [], 0
    unseen_observed, combo_observed = [], 0
    for entry in carriers:
        path = os.path.join(OUT_DIR, entry['id'], 'run.json')
        if not os.path.exists(path):
            rows.append((entry['id'], entry['class'], 'MISSING run.json', '', ''))
            bad += 1
            continue
        with open(path, encoding='utf-8') as handle:
            record = json.load(handle)
        observed = observed_features(record)
        diff = feature_diff(expected_for(entry), observed)
        if diff:
            bad += 1
        if entry['class'] == 'combo':
            combo_observed += 1
            key = json.dumps({k: observed[k] for k in DECLARED_FIELDS},
                             sort_keys=True)
            if key not in named_union:
                unseen_observed.append(entry['id'])
        rows.append((entry['id'], entry['class'],
                     json.dumps(observed, sort_keys=True),
                     'MATCH' if not diff else 'MISS',
                     '; '.join(diff)))
    width = max(len(row[2]) for row in rows)
    for cid, name, observed, verdict, diff in rows:
        print(f'{cid}  {name:<26} {verdict:<5} {observed:<{width}}'
              + (f'  {diff}' if diff else ''))
    print(f'\n{len(rows) - bad}/{len(rows)} carriers reached their declared tuple')
    declared_outside = manifest['combo_unseen']['declared_outside']
    majority = len(unseen_observed) * 2 >= max(combo_observed, 1)
    print(f"combo_unseen_majority: observed {len(unseen_observed)}/{combo_observed} "
          f"combos outside the named declared-tuple union "
          f"(declared prediction {declared_outside}/{manifest['combo_unseen']['combos']}) "
          f"{'PASS' if majority else 'FAIL'}")
    if unseen_observed:
        print(f"  unseen (observed): {', '.join(unseen_observed)}")
    return 1 if (bad or not majority) else 0


def regen_check(manifest, carriers, seed, classes, writer, pins, fixtures_dir,
                cache_dir, fetch, scratch):
    """Rebuild the whole set into a fresh directory and compare bytes.

    R42-C2 binds "carriers regenerate byte-identically"; a claim about a
    generator is only checkable by running it twice, so --verify does exactly
    that and compares the manifest and every carrier, not just the envelopes.
    """
    root = tempfile.mkdtemp(prefix='r42-regen-', dir=os.path.abspath(scratch))
    try:
        out = os.path.join(root, 'out')
        os.makedirs(out)
        local = tempfile.mkdtemp(prefix='build-regen-', dir=root)
        try:
            fresh, fresh_carriers = build_set(seed, list(classes), writer, out,
                                              local, pins, fixtures_dir,
                                              cache_dir, fetch)
        finally:
            shutil.rmtree(local, ignore_errors=True)
        checks = []
        original = sha256_file(os.path.join(OUT_DIR, 'manifest.json'))
        rebuilt = sha256_file(os.path.join(out, 'manifest.json'))
        checks.append(('manifest bytes identical', original == rebuilt,
                       f'{original[:16]} vs {rebuilt[:16]}'))
        differ = [a['id'] for a, b in zip(carriers, fresh_carriers)
                  if a['sha256'] != b['sha256']]
        checks.append(('every carrier byte-identical', not differ,
                       f'{len(carriers) - len(differ)}/{len(carriers)}'
                       + (f' differ: {differ[:4]}' if differ else '')))
        trees = []
        for entry in carriers:
            a = os.path.join(OUT_DIR, entry['id'], 'tree.json')
            b = os.path.join(out, entry['id'], 'tree.json')
            if sha256_file(a) != sha256_file(b):
                trees.append(entry['id'])
        checks.append(('every tree.json byte-identical', not trees,
                       f'{len(carriers) - len(trees)}/{len(carriers)}'
                       + (f' differ: {trees[:4]}' if trees else '')))
        for name, ok, detail in checks:
            print(f"{'PASS' if ok else 'FAIL'}  regen: {name}  {detail}")
        return 0 if all(ok for _, ok, _ in checks) else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


WRITER_PATH = None
OOD_OP = DEFAULT_OOD_OP
ALLOW_UNSEEN_MINORITY = False


def run_selftest(seed, writer, scratch_root, pins, fixtures_dir, cache_dir,
                 fetch):
    """Same seed twice -> identical manifest and carriers; other seed -> different."""
    work = tempfile.mkdtemp(prefix='r42-selftest-', dir=os.path.abspath(scratch_root))
    try:
        results = {}
        for tag, use_seed in (('a', seed), ('b', seed),
                              ('c', seed[::-1])):
            out = os.path.join(work, f'det-{tag}')
            os.makedirs(out)
            local_scratch = tempfile.mkdtemp(prefix=f'build-{tag}-', dir=work)
            try:
                manifest, carriers = build_set(use_seed, list(DEFAULT_CLASSES),
                                               writer, out, local_scratch, pins,
                                               fixtures_dir, cache_dir, fetch)
            finally:
                shutil.rmtree(local_scratch, ignore_errors=True)
            results[tag] = {
                'manifest': sha256_file(os.path.join(out, 'manifest.json')),
                'manifest_obj': manifest,
                'carriers': [c['sha256'] for c in carriers],
                'ids': [c['id'] for c in carriers],
            }
        checks = []

        def check(name, ok, detail):
            checks.append((name, ok, detail))
            print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")

        a, b, c = results['a'], results['b'], results['c']
        check('same seed: manifest bytes identical', a['manifest'] == b['manifest'],
              f"{a['manifest'][:16]} vs {b['manifest'][:16]}")
        check('same seed: every carrier sha256 identical', a['carriers'] == b['carriers'],
              f"{len(a['carriers'])} carriers")
        check('same seed: carrier ids identical', a['ids'] == b['ids'],
              f"{a['ids'][0]}..{a['ids'][-1]}")
        check('different seed: manifest differs', a['manifest'] != c['manifest'],
              f"{a['manifest'][:16]} vs {c['manifest'][:16]}")
        pinned = {e['id'] for e in a['manifest_obj']['carriers']
                  if not e.get('seed_dependent', True)}
        seed_dependent = [e['id'] for e in a['manifest_obj']['carriers']
                          if e['id'] not in pinned]
        pairs = {e['id']: (x, y) for e, x, y in
                 zip(a['manifest_obj']['carriers'], a['carriers'], c['carriers'])}
        same = [cid for cid in seed_dependent if pairs[cid][0] == pairs[cid][1]]
        check('different seed: every SEED-DEPENDENT carrier differs',
              not same,
              f"{len(seed_dependent) - len(same)}/{len(seed_dependent)} differ; "
              f"{len(pinned)} carriers are pinned third-party bytes and cannot "
              f"follow the seed" + (f"; same: {same[:3]}" if same else ''))
        per_class = {}
        for e, sha in zip(a['manifest_obj']['carriers'], a['carriers']):
            per_class.setdefault(e['class'], set()).add(sha)
        want = {name: (count if name in FAMILIES else CARRIERS_PER_CLASS)
                for name, count in FAMILIES.items()}
        dup_classes = sorted(
            name for name, seen in per_class.items()
            if len(seen) != want.get(name, CARRIERS_PER_CLASS))
        check('replicate variation: every class/family has distinct carriers',
              not dup_classes,
              f"{len(per_class)} classes, each with its own distinct carriers"
              if not dup_classes else
              f"repeats in {[(n, len(per_class[n]), want.get(n, CARRIERS_PER_CLASS)) for n in dup_classes]}")
        entries = a['manifest_obj']['carriers']
        partial = [c for c in entries if c['corruption'] == 'partial']
        check('R40-CL4: partial damage pinned by compressed length (multi-block)',
              bool(partial) and all(
                  c['damage']['pin'] == 'compressed-length'
                  and c['damage']['blocks_damaged'] >= 1
                  and all(0 < b['length'] <= MAX_DAMAGED_BLOCK
                          for b in c['damage']['blocks'])
                  and c['damage']['first_file'] not in c['damage']['paths']
                  for c in partial),
              f"{len(partial)} partial carriers, "
              f"{sorted({c['damage']['blocks_damaged'] for c in partial})} blocks "
              f"damaged each, every block <= {MAX_DAMAGED_BLOCK} B, first file "
              f"untouched")
        limited = [c for c in entries if c['class'].startswith('depth-limited')]
        check('depth-limited classes run at max_depth 1 with a nested image',
              bool(limited) and all(
                  c['rea']['max_depth'] == 1 and c['nested'] is not None
                  and c['nested']['handler_expected'] == 'squashfs_v4_le'
                  for c in limited),
              f"{len(limited)} carriers, depths "
              f"{sorted({c['rea']['max_depth'] for c in limited})}")
        combined = [c for c in entries
                    if c['class'] in ('partial-in-tree', 'partial-mixed',
                                      'depth-limited-alone',
                                      'depth-limited-in-tree',
                                      'depth-limited-mixed')]
        partial_combined = [c for c in combined if c['class'].startswith('partial-')]
        depth_combined = [c for c in combined if c['class'].startswith('depth-')]
        check('combined classes reach the precedence trap they exist for',
              len(completed := combined) == 10
              and all({'extractor-failure', 'unpublished-entry'}
                      <= set(c[DECLARED_KEY]['gap_kinds'])
                      for c in partial_combined)
              and all('depth-limited' in c[DECLARED_KEY]['gap_kinds']
                      for c in depth_combined)
              and all('unpublished-entry' in c[DECLARED_KEY]['gap_kinds']
                      for c in depth_combined if 'in-tree' in c['class']),
              f"{len(completed)} carriers; partial-* -> extractor-failure+"
              f"unpublished-entry, depth-* -> depth-limited"
              f"[+unpublished-entry]; gap sets "
              f"{sorted({tuple(c[DECLARED_KEY]['gap_kinds']) for c in combined})}")
        named = [c for c in entries if c['class'] != 'combo']
        combos = [c for c in entries if c['class'] == 'combo']
        check('every carrier declares the six binding fields under ONE key',
              all(DECLARED_KEY in c and set(DECLARED_FIELDS) == set(c[DECLARED_KEY])
                  for c in entries),
              f"{len(entries)} carriers, key {DECLARED_KEY!r}")
        check('R41-CL1: no second spelling of the tuple',
              all('declared' not in c for c in entries)
              and all(not (c.get('class_expected') or {}).get('features')
                      for c in entries),
              "no `declared` key, no `class_expected.features` key")
        check('named carriers keep a label/action cross-check; combos null',
              all(c['class_expected'] and c['class_expected']['label']
                  and c['class_expected']['action'] for c in named)
              and all(c['class_expected'] is None for c in combos)
              and all(c.get('factors') for c in combos),
              f"{len(named)} named, {len(combos)} combos")
        check('every combo draws >= 2 decision factors',
              all(len(c['decisions']) >= COMBO_MIN_DECISIONS for c in combos)
              and len({d for c in combos for d in c['decisions']}) >= 6,
              f"min {min(len(c['decisions']) for c in combos)} decisions, "
              f"max {max(len(c['decisions']) for c in combos)}; "
              f"factors seen {sorted({d for c in combos for d in c['decisions']})}")
        legacy = [c for c in entries if c['class'].startswith('legacy-')]
        check('legacy classes carry a pinned fixture record and a v1-v3 handler',
              len(legacy) == 10
              and all(c['fixture']['clean']['sha256'] and c['fixture']['pins']
                      for c in legacy)
              and all(all(h.startswith('squashfs_v') and not h.startswith('squashfs_v4')
                          for h in c[DECLARED_KEY]['handler_set'])
                      or c['class'] == 'legacy-partial'
                      for c in legacy),
              f"{len(legacy)} legacy carriers, handlers "
              f"{sorted({h for c in legacy for h in c[DECLARED_KEY]['handler_set']})}")
        check('legacy damage uses the pinned window only',
              all(c['damage']['recipe'] == 'fixture-damage'
                  and c['damage']['length'] == 4
                  for c in legacy if c['damage']),
              f"{len([c for c in legacy if c['damage']])} damaged legacy carriers")
        check('every legacy carrier is a pinned image or a pinned image + window',
              all(len(c['sha256']) == 64 for c in legacy),
              f"{sorted({c['layout'] for c in legacy})}")
        check('two-chunk carriers put the second chunk at 4096',
              all(part['offset'] == FIXTURE_TWO_CHUNK_PAD
                  for c in entries if c.get('chunks')
                  for part in c['chunks'][1:2]),
              f"{len([c for c in entries if c.get('chunks') and len(c['chunks']) > 1])}"
              f" multi-chunk carriers")
        failed = [name for name, ok, _ in checks if not ok]
        if failed:
            print(f'\n{len(failed)} selftest check(s) failed: {", ".join(failed)}')
            return 1
        print(f'\nall {len(checks)} selftest checks passed')
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    global OUT_DIR, WRITER_PATH, OOD_OP, ACTIONS, ACTION_SET_NAME, ACTION_SOURCE
    global FIXTURE_PINS_PATH, FIXTURE_PINS_LOGICAL, ALLOW_UNSEEN_MINORITY
    parser = argparse.ArgumentParser(
        description='Deterministic R42-C2 held-out SquashFS carrier generator '
                    '(table-v4 classes, amendment A1).')
    parser.add_argument('--seed', required=True,
                        help='hex seed (the freeze commit hash)')
    parser.add_argument('--out', help='output directory (required unless --selftest)')
    parser.add_argument('--classes', default=','.join(DEFAULT_CLASSES),
                        help='comma-separated recipe names (default: all classes)')
    parser.add_argument('--run', action='store_true',
                        help='run REA per carrier in its arm')
    parser.add_argument('--verify', action='store_true',
                        help='with --run: compare every envelope to its declared '
                             'tuple, score combo_unseen_majority, regenerate the '
                             'whole set byte-identically; exit 1 on any failure')
    parser.add_argument('--ood-op', default=DEFAULT_OOD_OP,
                        help='non-extract-firmware REA operation for the '
                             'out-of-domain class (default: %(default)s)')
    parser.add_argument('--actions-set', default=DEFAULT_ACTION_SET,
                        choices=sorted(ACTION_SETS),
                        help='action tokens for the (label, action) pairs '
                             '(default: %(default)s)')
    parser.add_argument('--actions-file',
                        help='file holding the frozen `<!-- sqfs-triage-actions: ... -->` '
                             'line; the selected set must equal its tokens')
    parser.add_argument('--gen', default=os.environ.get('KAIDOKU_GEN_SQUASHFS')
                        or default_writer_path(),
                        help='path to the SquashFS image writer (round-39 gen-squashfs.py)')
    parser.add_argument('--scratch', default=os.environ.get('TMPDIR')
                        or tempfile.gettempdir(),
                        help='scratch parent for trees, fixture cache, REA output '
                             'dirs and the selftest')
    parser.add_argument('--fixture-pins', default=default_fixture_pins(),
                        help='the fixtures.json pin list (default: beside this script)')
    parser.add_argument('--fixtures-dir',
                        help='directory holding the COMMITTED pinned fixture copies '
                             '(e.g. corpus/evidence/round-42/c2/fixtures); every file '
                             'is sha256-checked against the pin')
    parser.add_argument('--fetch', action='store_true',
                        help='download a missing pinned fixture from its pinned URL '
                             'into the cache under --scratch (sha256-checked)')
    parser.add_argument('--allow-unseen-minority', action='store_true',
                        help='build even when fewer than half of the combos are '
                             'outside the named declared-tuple union (inspection '
                             'only: the claim binds combo_unseen_majority)')
    parser.add_argument('--gzip', action='store_true',
                        help='write envelope.json.gz / rea-full.json.gz (mtime 0)')
    parser.add_argument('--keep-extraction', action='store_true',
                        help='keep REA output dirs in scratch (debug only)')
    parser.add_argument('--selftest', action='store_true',
                        help='determinism selftest (no --out needed)')
    args = parser.parse_args(argv)

    seed = args.seed.strip()
    if len(seed) < 16 or any(ch not in '0123456789abcdefABCDEF' for ch in seed):
        raise SystemExit(f'--seed must be at least 16 hex characters, got {seed!r}')

    WRITER_PATH = os.path.abspath(args.gen)
    OOD_OP = args.ood_op
    ACTIONS = ACTION_SETS[args.actions_set]
    ACTION_SET_NAME = args.actions_set
    missing = sorted({r['label'] for r in RECIPES.values()} - set(ACTIONS))
    if missing:
        raise SystemExit(
            f'--actions-set {ACTION_SET_NAME!r} has no row for label(s) {missing}; '
            f'that vocabulary predates them, so the (label, action) pairs would be '
            f'unscoreable.  Select a set that covers every class label.')
    if args.actions_file:
        tokens = actions_line(args.actions_file)
        check_action_tokens(tokens, args.actions_file)
        ACTION_SOURCE = {'file': os.path.abspath(args.actions_file),
                         'sha256': sha256_file(args.actions_file),
                         'tokens': tokens}
    FIXTURE_PINS_PATH = os.path.abspath(args.fixture_pins)
    FIXTURE_PINS_LOGICAL = (
        FIXTURE_PINS_NAME if os.path.dirname(FIXTURE_PINS_PATH)
        == os.path.dirname(os.path.abspath(__file__)) else FIXTURE_PINS_PATH)
    ALLOW_UNSEEN_MINORITY = args.allow_unseen_minority
    pins = load_fixture_pins(FIXTURE_PINS_PATH)
    writer = load_writer(WRITER_PATH)
    install_block_encoder(writer)
    os.makedirs(args.scratch, exist_ok=True)
    fixtures_dir = os.path.abspath(args.fixtures_dir) if args.fixtures_dir else None
    cache_dir = os.path.join(os.path.abspath(args.scratch), 'fixtures-cache')

    if args.selftest:
        return run_selftest(seed, writer, args.scratch, pins, fixtures_dir,
                            cache_dir, args.fetch)

    if not args.out:
        raise SystemExit('--out is required unless --selftest')
    selected = parse_classes(args.classes)
    OUT_DIR = os.path.abspath(args.out)
    if os.path.exists(os.path.join(OUT_DIR, 'manifest.json')):
        raise SystemExit(f'{OUT_DIR} already holds a manifest.json; use a fresh --out')
    scratch = tempfile.mkdtemp(prefix='r42-heldout-',
                               dir=os.path.abspath(args.scratch))
    try:
        manifest, carriers = build_set(seed, selected, writer, OUT_DIR, scratch,
                                       pins, fixtures_dir, cache_dir, args.fetch)
        print(f"manifest {os.path.join(OUT_DIR, 'manifest.json')} "
              f"{len(carriers)} carriers, {len({c['label'] for c in carriers})} labels, "
              f"{len({(c['label'], c['action']) for c in carriers})} decisions")
        if args.run:
            failures = 0
            for entry in carriers:
                recipe = RECIPES.get(entry['class']) or {}
                if recipe.get('ood'):
                    record = out_of_domain_run(entry, scratch, args.keep_extraction,
                                               args.gzip, OOD_OP)
                else:
                    record = run_rea(entry, scratch, args.keep_extraction, args.gzip)
                if 'error' in record:
                    failures += 1
                    print(f"run {entry['id']} {entry['class']:<26} ERROR "
                          f"{record.get('error')} exit={record['exit_code']}")
                    continue
                print(f"run {entry['id']} {entry['class']:<26} exit={record['exit_code']} "
                      f"depth={record.get('max_depth')} "
                      f"op={record.get('operation')} prov={record.get('provider')} "
                      f"handlers={','.join(record.get('handlers') or []) or '-'} "
                      f"failed={','.join(record.get('failed_chunks') or []) or '-'} "
                      f"gaps={','.join(record.get('gap_kinds') or []) or '-'} "
                      f"deps={','.join(record.get('gap_dependencies') or []) or '-'} "
                      f"sr={record.get('symlink_removed')} be={record.get('be_argv')} "
                      f"files={record.get('files')} "
                      f"{'digest-ok' if record.get('digest_matches_carrier') else 'DIGEST-MISMATCH'}")
            if failures:
                return 1
            if args.verify:
                status = verify(manifest, carriers)
                regen = regen_check(manifest, carriers, seed, selected, writer,
                                    pins, fixtures_dir, cache_dir, args.fetch,
                                    scratch)
                return 1 if (status or regen) else 0
        elif args.verify:
            raise SystemExit('--verify needs --run (there is no envelope to check)')
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
