#!/usr/bin/env python3
"""R50-C1 counter (coverage: genuine AVM-marker little-endian SquashFS v4 -> Core).

Port of `tools/round-41/c1-counter.py` (the R41-C1 counter, genuine AVM-layout
BIG-endian vendor carriers) to the little-endian layout, with the non-v1/v2-specific
round-49 hardening carried over (see PORT-DELTA.md for every delta). The claims
text is `plans/round-50-claims.md` R50-C1; the predicate is embedded here clause
by clause:

  At the measured revision REV, for each frozen carrier, the committed round-50
  REA 6.5.0 `extract-firmware --max-depth 1` after-receipt (unblob 26.6.4,
  sasquatch 4.5.1 on the child PATH, no `-be` binary needed), first added in a
  commit that descends from the freeze, names the `squashfs_v4_le` handler for
  the carrier's chunk with no failed chunk, publishes every regular file of the
  frozen independent oracle (unsquashfs 4.7.5 listing + per-file sha256; the
  lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout is the second
  reader that equals it) at its exact path relative to the chunk extract root
  (equality after mapping into the root, never a suffix) with the same sha256
  and size, and no extra regular file; accounts for every non-regular oracle
  entry by the frozen gap/removal rule (round-41 `gaps_ok` three-family
  disposition); has a subject digest equal to the carrier pin and recomputes
  its evidence id; the carrier bytes hash to the frozen pin and their superblock
  reads the frozen layout -- little-endian `hsqs`, v4.0, compression id 4,
  `mkfs_time == bytes_used` (the AVM marker); **and** a counter-time REA rerun
  of the same bytes (scratch output directory, carriers fetched through the
  pinned chain or the `--carrier-cache`; executed by node on the REA package at
  `--pkg65`, never through `npx`; repeated, up to 3 attempts, only when REA reports
  its own `provider_timeout`) has the same semantic projection as the
  committed receipt; **and** a scoring-time `unsquashfs` 4.7.5 re-derivation of
  the carrier bytes yields exactly the frozen oracle table (both directions);
  **and** the receipt's `parameters.output_directory` starts
  with `/fast/scratch/hyaku/kaidoku-r50/` (prefix test, no `..`); documentation
  bindings: `PROVINCE.md` holds a `## Round-50 additions to Core` section whose
  row names `squashfs_v4_le` with the AVM marker and cites the entry path; one
  line carries `Round-50 frontier note`, the entry stem and an LE-AVM token; the
  entry exists at REV and its `source:` lines cite SOURCES rows opened
  2026-10-28..2026-10-29 that list the entry in `used-by`; `corpus/README.md`
  `## Coverage map` maps the entry stem; no frozen C1 path changed after the
  freeze.

Target: carriers_matched == 4 (g7581, g7582, c6490, c6430), every binding true,
`frozen_path_changed []`, exit 0.

What the layout test is NOT (round-50 delta, deliberate): there is no big-endian
field and no little-endian-block-length special case. In the big-endian AVM layout
the metadata block headers were little-endian inside a big-endian superblock, so
the marker `mkfs_time == bytes_used` alone could not tell a genuine AVM image from
a standard BE image with a normalised timestamp and the block-length endianness was
the format test. A little-endian image has ONE byte order: `hsqs` fixes the whole
file, so the superblock reads the marker directly and the only extra tests are
sanity ones (v4.0, compression id 4, table starts inside `bytes_used`).
The marker is invisible to unblob (`SquashFSExtractor` runs `sasquatch -le` for every
little-endian image and only branches on `mkfs_time == bytes_used` for BIG-endian
v4): the claim is "REA publishes every oracle file of the pinned LE AVM members",
not "REA recognises AVM". The marker is a CONSTANT OF THE PINNED BYTES: once
`carrier_pin_ok` holds the bytes are fixed and the marker adds no evidence beyond
it; the counter does NOT claim that `layout_ok` separates genuine AVM images from
re-stamped ones (anyone can write `mkfs_time = bytes_used`). `layout_ok` is kept as
a frozen-layout statement about the pin and as the second red for a planted
STANDARD little-endian carrier (control CTL-C1-4 is red on `carrier_pin_ok` AND on
`layout_ok`).

The extract root (R40-CL1 repair; R41C1Revenger 1 is the normative rule; R49 closure)
  Every path comparison against the oracle and non-regular tables is equality
  after mapping the receipt path into its chunk's extract root, never a suffix
  test, and the root is never reconstructed from the path text:

    strip once         `$output/` is stripped once: `files[].relative_path`,
                       `unpublished_entries[].relative_path` and gap
                       `relative_path` are bare, while gap `input_path`,
                       `derivations[].parent_path/child_path` and
                       `depth_limited_paths[]` are `$output/`-prefixed
                       (rea-agents 6.5.0 FirmwareFiles.js:177 vs :191-200)
    root               the child path of every `derivations[]` edge whose handler
                       EQUALS `squashfs_v4_le` (round 49: equality, not the
                       round-41 `startswith('squashfs_v4')` prefix); a whole-file
                       chunk's root is `firmware.bin_extract`, and a carved or
                       nested chunk's root is `<parent>/<start>-<end>.<handler>_extract`
    one root           the subject root is that root when the receipt has exactly
                       one; several roots are ambiguous and the freeze can name
                       the intended one with the optional `oracle_root` key of the
                       carrier entry, otherwise the path clauses fail closed with
                       `extract_root: null`
    whole segments     `P == root or P.startswith(root + '/')` (round 49
                       `under_root`): a root `x_extract` does not own
                       `x_extract2/...`; `rel(P)` is `''` for P == root, the
                       remainder for a contained P, else None - an entry outside
                       the root belongs to another namespace and is neither
                       compared against this oracle nor reported as published
    keyed by root      with one root per carrier the (root, rel) key collapses to
                       rel, and a path outside the root cannot satisfy a row

Removal disposition (R41C1DevCore 7.1-7.3, unchanged)
  unblob deletes escaping symlinks after reporting `MaliciousSymlinkRemoved`,
  deletes empty-target symlinks with no report at all, and never publishes a
  link as a regular file. The frozen gap rule (`GAPRULE`) may carry a `removed`
  block; `gaps_ok` is then a three-family disposition check:
    path-resolved gap   kind allowed for that entry's kind
    removal             every diagnostic the rule names (`removed.diagnostic`)
                        must resolve at its exact path to a non-regular entry
                        whose kind is in `removed.kinds`, and no entry may be
                        both gapped and removed
    silent              an entry whose kind and oracle detail are listed under
                        `removed.silent` may carry no record at all (per row)
  A diagnostic's path is its `report.link`, an absolute path that must lie
  under the receipt's own trusted run root (round 49: the parent directory of
  `parameters.output_directory`), then be mapped by locating the subject root as
  whole segments. The rerun projection carries diagnostics as
  `[__typename__, rel]`, so a rerun that removed a *different* link no longer
  matches. A path-less gap kind that is not in `structural` (so
  `missing-extractor-dependency`, the REA kind unblob reports when `sasquatch`
  is absent from the child PATH) fails `gaps_ok`.

Per-carrier clauses (all must hold; `matched` = conjunction):
  carrier_present          the carrier blob exists at REV (committed `path`, or
                           the `--carrier-cache` entry `<pin>.bin` of an
                           `external` vendor carrier)
  carrier_pin_ok           sha256(bytes) == the frozen pin
  carrier_fresh_ok         the pin is not one a previous C1 freeze already scored
                           (carriers.json `prior_pins`, the previous C1 carrier
                           tables and the frozen prior-pins tables, all read at
                           the freeze commit)
  layout_ok                a statement about the pinned bytes, not a provenance
                           test (see the note above): the frozen layout (see
                           layout_probe): little-endian
                           `hsqs` magic, v4.0, compression id 4 (xz),
                           `mkfs_time == bytes_used` (the AVM marker),
                           0 < bytes_used <= file size, 96-byte superblock, and
                           0 < inode_table_start < directory_table_start <=
                           bytes_used
  oracle_ok                the oracle table parses (rel, sha256, size); >= 1 row;
                           no duplicate paths; every sha256 is 64 hex; every
                           size is a non-negative integer (round 50: size is
                           mandatory, it is compared)
  oracle_rederived_ok      scoring-time oracle re-derivation (round 50, from the
                           wave-1 shortcut critique S5/S6): the counter runs
                           `/usr/bin/unsquashfs` (version 4.7.5) on the carrier
                           bytes (`-no-xattrs -no-progress -f -no-exit-code` into
                           its scratch directory) and requires the set of regular
                           files `(rel, sha256, size)` to EQUAL the frozen oracle
                           table in both directions, so a shrunk, extended or
                           lane-built oracle table fails. Non-regular entries are
                           not re-derived (an unprivileged extraction cannot make
                           device nodes). A tool that cannot run is unevaluable
                           (exit 2 `oracle_env_error`), never a green.
  nonregular_ok            the non-regular table parses (rel, kind[, detail]);
                           empty is allowed; duplicate (rel, kind) rows are not
  carve_ok                 the carrier is exactly the filesystem it claims: for an
                           external carrier the frozen carve `length` equals the
                           superblock `bytes_used` and the bytes are that length;
                           for a committed carrier the file size equals
                           `bytes_used`. A sloppy carve leaves trailing bytes, the
                           chunk stops being the whole input, and the oracle root
                           moves one `<start>-<end>.<handler>_extract` deeper
  receipt_present          corpus/evidence/round-50/c1/<id>/after.json parses
  receipt_fresh            EVERY commit that adds the receipt path in the full
                           history of REV (`git log -m --full-history
                           --diff-filter=A`; the default simplified history hid a
                           pre-freeze add behind a TREESAME merge in round 49) is
                           a strict descendant of --freeze (not the freeze commit
                           itself)
  evidence_envelope_ok     the after-receipt is an REA evidence envelope, not a
                           score receipt (no `counter_sha256`/`exit_code` key)
  subject_pin_ok           subject.digest.sha256 == the frozen pin
  operation_ok             operation == extract_firmware and provider.id == unblob
  handler_ok               the receipt's squashfs-family chunk handlers are
                           exactly [`squashfs_v4_le`] (round 49: no prefix test,
                           no default; `squashfs_v4_be`, `squashfs_v3`, ... fail)
  chunks_ok                no chunk carries extraction_failed: true
  oracle_hits_ok           every oracle regular file is published at its exact
                           path under the chunk extract root (rel ==, sha256 ==
                           and size ==), the root taken from the receipt's
                           `derivations[]` edge, not from path text; and NO other
                           regular file is published under that root (round 49
                           `extra_published`; round 41 only counted hits)
  gaps_ok                  disposition check (R41C1DevCore 7.1): every extraction
                           gap lands on exactly one non-regular entry at its exact
                           path and its kind is allowed for that entry's kind;
                           every removal diagnostic the frozen rule names resolves
                           to a non-regular entry of a listed kind and no entry is
                           both gapped and removed; every entry the rule marks
                           required carries exactly one disposition (an allowed
                           gap, a removal diagnostic, or - only when the rule
                           lists it under `silent` - nothing at all)
  nonregular_unpublished_ok  no published regular file path equals a non-regular
                           entry path (a materialised symlink/device would both
                           publish the path and keep the gap); equality is exact
                           relative to the chunk extract root
  path_shape_ok            every normalised receipt path is a legal spelling (no
                           empty/`.`/`..` component, no trailing slash, no
                           absolute path) -- round 49, from the R41-D5 finding
  run_provenance_ok        parameters.output_directory is an absolute path that
                           STARTS WITH `/fast/scratch/hyaku/kaidoku-r50/` (prefix
                           test, no `..`; round 41 tested a substring);
                           `parameters` is inside the hashed 6.5.0
                           semanticProjection, so it cannot be edited without
                           breaking evidence_id_ok. It authenticates neither the
                           writer nor the round: a relabelled genuine replay of
                           real receipts passes (plan: disclosed limit 3)
  parameters_ok            the receipt's `parameters` carry the FROZEN extraction
                           parameters (`rea_parameters` of carriers.json:
                           max_depth 1, max_output_bytes, max_output_files);
                           round 41 froze nothing here and the rerun replayed
                           whatever the receipt recorded
  evidence_id_ok           stored evidence id == the id recomputed under the
                           frozen rea-agents 6.5.0 rule (tools/round-27/
                           xpin-attribute.mjs, the package's own
                           semanticProjection)
  projection_ok            the counter's own REA run of the carrier bytes (fresh
                           scratch output directory, PATH fixed, `sasquatch`
                           required on it) has the same semantic projection as
                           the committed receipt (the frozen `plus-extractor`
                           profile: `derivations[]`, the source of the oracle
                           root, are compared). Skipped (and therefore false)
                           when the carrier bytes or the receipt are absent / the
                           pin fails. The run is node + the package CLI entry at
                           `--pkg65` (no `npx`, no ambient PATH resolution);
                           its toolchain is bound and recorded (see the rerun
                           clause).

Non-vacuity bindings (properties of the frozen set, so they cannot be gamed after
the freeze):
  carriers_spec_ok         `target` frozen in carriers.json equals this counter's
                           target; exactly that many distinct ids; the expected id
                           set (case-insensitive); distinct pins; id/sha256/oracle/
                           nonregular present and well-formed (and `path` for a
                           committed carrier); an external carrier also names
                           `url`, `image_sha256`, `member`, `member_sha256` and a
                           positive `length` (and `nested.sha256` when it has a
                           `nested` block), so the fetch chain is bound in the
                           table rather than in the fetcher (routed R40-CL6); an
                           optional `oracle_root` must be a relative path string
                           and `prior_pins` a list of 64-hex pins; `target` must
                           be present; `projection` must be present and equal
                           `plus-extractor` (round 50: it is no longer a free
                           choice or a default); `rea_parameters` is an object with
                           positive integer max_depth (== 1), max_output_bytes
                           and max_output_files (round 50)
  gap_rule_ok              the gap rule parses to {allowed: {kind: [gap kind]},
                           required?: {kind: bool}, removed?: {diagnostic, kinds,
                           disposition, silent?}, structural?: {kind: limit}} with
                           claim R50-C1; every non-regular kind that appears in
                           any frozen nonregular table is a key of `allowed`
  frozen_tables_valid      carriers.json and gap-rule.json parse at the freeze
                           commit itself (routed R39-CL4) and every oracle /
                           nonregular table carriers.json lists exists at the
                           freeze commit (round 50: a table first committed after
                           the freeze would be an unfrozen oracle)
  (REMOVED in round 50: `compression_coverage`, which demanded one gzip and one
  xz carrier; all four frozen LE carriers are xz, so the per-carrier
  `layout_ok` compression id 4 test replaces it.)

Documentation bindings:
  province_core_section    PROVINCE.md has the `## Round-50 additions to Core`
                           heading
  province_core_row        a table row in that section whose first cell names
                           `squashfs_v4_le`, whose text names the AVM marker
                           (AVM[ _-]marker) and cites the entry path
  frontier_note            one line carries `Round-50 frontier note`, the entry
                           stem and an LE-AVM token (LE AVM / AVM LE)
  entry_present            the knowledge entry exists at REV
  sourced                  the entry's `source:` lines name an S-id whose
                           corpus/SOURCES.md row is opened 2026-10-28..2026-10-29
                           and lists the entry (path or stem) in used-by
  coverage_map_row         corpus/README.md `## Coverage map` maps the entry stem

Counter bytes (round 50, from the shortcut critique S3): the counter file that is
running must be byte-identical to `tools/round-50/c1-counter.py` at FREEZE, else
exit 2 `counter_not_frozen` (and likewise when the freeze holds no counter).

Freeze-drift binding (routed defect R38-CL4, kept; round-49 merge-aware form): if
any commit in FREEZE..REV changes a frozen C1 path (the claims text, everything
under `tools/round-50/`, the carried-over inputs the counter names, carriers.json,
gap-rule.json, every carrier/oracle/nonregular file carriers.json lists) -- M/D/R/T/U,
an A under a frozen prefix, or an A of a path that existed at the freeze, read with
`-m --diff-merges=first-parent` so an edit inside a merged branch counts -- or a
frozen blob differs between FREEZE and REV, the counter exits 2 with reason
`frozen_path_changed` and never reports met. A later restore does not un-block (the
log of the range is inspected, not the endpoints).

The rerun clause (routed R39-CL5)
  Between the receipt checks and the verdict, a carrier whose bytes hash to the
  pin and whose receipt parses is re-run by this counter:
      cwd = a private directory under $HYAKU_SCRATCH/kaidoku-r50 (or --work),
      env REA_UNBLOB_COMMAND=<absolute unblob>, TMPDIR = that directory,
          PATH = FIXED_PATH (round 49: a seat's shim directory cannot be what
          `sasquatch` resolves to during a score),
      argv = <node on FIXED_PATH> <--pkg65>/<package.json bin rea-agents>
             extract-firmware --format json
             --full-output --max-depth 1 --max-output-bytes B --max-output-files F
             <carrier bytes> <fresh outdir>        (B, F, depth from `rea_parameters`)
  Round 50 (shortcut critique S1): the REA that runs is the package at `--pkg65`
  (version 6.5.0, the one the evidence-id recompute is bound to), executed by node
  directly; `npx -y rea-agents@6.5.0` is gone, so no ambient PATH or registry
  resolution picks a different REA. Before the first run the toolchain is bound:
  `unblob --version` must equal the frozen `26.6.4` (else exit 2
  `rerun_env_error`); `sasquatch` must resolve on FIXED_PATH; the unblob, sasquatch,
  node and REA package paths, sha256 and versions are recorded in the counter
  receipt (`rerun_toolchain`). A shim directory in the caller's PATH cannot
  satisfy any of it.
  and the fresh `.data` object is projected:

      projection = {subject_sha256,
                    files: sorted [path suffix after the chunk `*_extract`
                                   directory, sha256, size],
                    chunks: sorted [handler, range.offset, range.length,
                                    extraction_failed],
                    gaps: sorted [kind, path suffix, sorted dependencies],
                    unpublished_entries: sorted [kind, path suffix],
                    diagnostics: sorted [__typename__, rel]}
                  + (plus-extractor) derivations, engine, published_bytes, coverage

  Everything that varies between two runs of the same bytes (absolute paths,
  output directory, evidence id, continuation ids, provider ids, timestamps,
  selection and analysis fields) is excluded. The comparison profile is frozen
  data: the optional `projection` key of carriers.json, default `plus-extractor`.
  The rerun replays the FROZEN extraction parameters (`rea_parameters` of
  carriers.json; `parameters_ok` binds the receipt to the same values): a depth-1
  extraction is `partial` with a different published set, so a rerun at REA's
  default depth 3 could never match a depth-1 receipt, and a ~13k-file rootfs
  needs the raised budgets (REA's default 10000-entry staging budget fails).
  `sasquatch` must resolve on FIXED_PATH: when it does not, the rerun is
  unevaluable (exit 2 `rerun_env_error`, detail `missing-extractor-dependency`),
  never a green and never a silent downgrade. `sasquatch-v4be` is NOT required
  (round-41 needed it; a little-endian carrier never reaches it). A rerun that
  cannot run at all (no npx/node/unblob, unusable REA output) is unevaluable
  (exit 2 `rerun_env_error`). `--no-rerun` is not a mode of the predicate: it
  exits 2 (`rerun_disabled`) and never reports met.

Receipt identity (round 49): every receipt this counter writes (`--json-out`)
carries `counter` (absolute path) and `counter_sha256` (sha256 of that file's
bytes). `--verify-receipt PATH` re-reads a written receipt and exits 0 (match), 1
(missing/mismatched key) or 2 (unreadable). The committed REA after-receipts must
NOT carry the key (`evidence_envelope_ok`). The evidence-id recompute also binds
the rea-agents package: the frozen `rea-pkg.json` (package.json and
package-lock.json sha256 + version 6.5.0) must match the `--pkg65` package, else
the run is unevaluable.

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT
                [--work DIR] [--carrier-cache DIR] [--json-out PATH]
                [--unblob PATH] [--rea-timeout SECONDS]
  c1-counter.py --selftest  [--pkg65 REA650_PKG_ROOT] [--work DIR]
  c1-counter.py --selftest-rea --pkg65 REA650_PKG_ROOT --dev-image LE_AVM_MEMBER
                [--unblob PATH] [--rea-timeout SECONDS]
  c1-counter.py --verify-receipt PATH
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed, rerun environment error, --no-rerun). Reads lane bytes only
through git objects (`git show REV:path`) and `--carrier-cache`; writes only a
private scratch dir under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/
kaidoku-r50/counter (or --work) and --json-out. Never calls gettempdir().

`--selftest` is offline and deterministic: it drives measure() in-process over a
git fixture lane with a simulated REA runner (the simulator only exists inside
selftest(); main() never passes anything but the real runner). The fixture
carriers are synthetic little-endian `hsqs` superblocks: the layout clause is a
superblock test and these bytes exercise it exactly. `--selftest-rea` is the
real-path check: it runs REA 6.5.0 on a lane-supplied LE AVM member
(`--dev-image`, NOT a C1 carrier unless the caller says so), builds a one-carrier
fixture lane around two real runs and asserts a green verdict, then relabels an
oracle-only fabrication and asserts it red. (Not run by the porting seat: no REA
run in wave 1 of the port.)
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CARRIERS = 'tools/round-50/carriers.json'
GAPRULE = 'tools/round-50/gap-rule.json'
AFTERDIR = 'corpus/evidence/round-50/c1'
ENTRY = 'corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md'
STEM = '2026-10-28-r50-avm-le-squashfs-core'
CORE_HEADING = '## Round-50 additions to Core'
FRONTIER_MARK = 'Round-50 frontier note'
HANDLER = 'squashfs_v4_le'
XPIN = 'tools/round-27/xpin-attribute.mjs'
# Pins earlier C1 freezes already scored: the round-41 BE vendor/lane carriers and
# the round-49 v1/v2 fixtures. Read at the freeze commit (a table added later
# cannot bless an old pin).
PRIOR_CARRIER_TABLES = ('.ufo/waves/round-41/c1/carriers.json',
                        'tools/round-49/carriers.json')
PRIOR_PIN_CANDIDATES = ('tools/round-50/prior-pins.json',
                        'tools/round-49/prior-pins.json',
                        'tools/round-42/prior-pins.json')
REA_PKG_CANDIDATES = ('tools/round-50/rea-pkg.json', 'tools/round-49/rea-pkg.json',
                      'tools/round-42/rea-pkg.json')
OPENED_DATES = ('2026-10-28', '2026-10-29')
TARGET = 4
IDS = ('g7581', 'g7582', 'c6490', 'c6430')
PROV_SEGMENT = '/kaidoku-r50/'
PROV_BASE = '/fast/scratch/hyaku/kaidoku-r50/'
REA_VERSION = '6.5.0'
SB_SIZE = 96
XZ_ID = 4
UNBLOB_VERSION = '26.6.4'
UNSQUASHFS = '/usr/bin/unsquashfs'
UNSQUASHFS_VERSION = '4.7.5'
COUNTER_PATH = 'tools/round-50/c1-counter.py'
ORACLE_FLAGS = ('-no-xattrs', '-no-progress', '-f', '-no-exit-code')
# H1 (carried from round 49): the REA child and the counter's own node/npx
# lookups use one fixed PATH, so a seat's shim directory cannot be what
# `sasquatch` resolves to during a score.
FIXED_PATH = ':'.join(['/usr/local/bin', '/usr/bin', '/bin',
                       os.path.expanduser('~/.local/bin'),
                       os.path.expanduser('~/.local/share/fnm/node-versions/'
                                          'v24.21.0/installation/bin')])
FROZEN_PATHS = (
    'plans/round-50-claims.md',
    'tools/round-41/fetch-vendor.py',
    'tools/round-41/sqfs-list.py',
    'tools/round-42/prior-pins.json',
    'tools/round-42/rea-pkg.json',
    XPIN,
    CARRIERS,
    GAPRULE,
)
# `tools/round-50/**` (counter, run harness, carriers, gap rule, control
# fixtures) is a frozen path family: a new or edited file under it is drift.
FROZEN_PREFIXES = ('tools/round-50/',)
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
AVM_MARKER_RE = re.compile(r'AVM[ _-]marker', re.IGNORECASE)
LE_AVM_RE = re.compile(r'\bLE[ _-]AVM\b|\bAVM[ _-]LE\b', re.IGNORECASE)
SQUASHFS_HANDLER_RE = re.compile(r'^squashfs_v[1-4](_[a-z0-9]+)*$')
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
            'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
            'gap_rule_ok', 'frozen_tables_valid')
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'carrier_fresh_ok', 'layout_ok',
           'carve_ok', 'oracle_ok', 'oracle_rederived_ok', 'nonregular_ok',
           'receipt_present',
           'receipt_fresh', 'evidence_envelope_ok', 'subject_pin_ok',
           'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok',
           'gaps_ok', 'nonregular_unpublished_ok', 'path_shape_ok',
           'run_provenance_ok', 'parameters_ok', 'evidence_id_ok', 'projection_ok')


class Unevaluable(Exception):
    reason = 'unevaluable'


class FrozenPathChanged(Unevaluable):
    reason = 'frozen_path_changed'

    def __init__(self, paths):
        self.paths = list(paths)
        super().__init__('frozen path changed after freeze: ' + ', '.join(self.paths))


class RerunEnvError(Unevaluable):
    reason = 'rerun_env_error'


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Unevaluable('git ' + ' '.join(args) + ': '
                          + p.stderr.decode(errors='replace').strip())
    return p


def show(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}', check=False)
    return p.stdout if p.returncode == 0 else None


WORK_OVERRIDE = None


def scratch_root():
    """Private scratch directory; --work > $HYAKU_SCRATCH > /fast/scratch/hyaku.

    Deliberately never `tempfile.gettempdir()`: with TMPDIR and HYAKU_SCRATCH
    unset that resolves to /tmp (R44-SCR-TMP, carried from round 49)."""
    if WORK_OVERRIDE:
        os.makedirs(WORK_OVERRIDE, exist_ok=True)
        return WORK_OVERRIDE
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                     'kaidoku-r50', 'counter')
    os.makedirs(d, exist_ok=True)
    return d


def which_fixed(name):
    """Absolute path of `name` under FIXED_PATH, or None."""
    for d in FIXED_PATH.split(':'):
        if not d:
            continue
        p = os.path.join(d, name)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


def file_sha256(path):
    """sha256 of a file's bytes following symlinks (a tool's real content)."""
    try:
        real = os.path.realpath(path)
        with open(real, 'rb') as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else None


# ------------------------------------------------------------- receipt identity

def counter_identity(path=None):
    """(counter path, sha256 of its bytes) for the counter that writes a receipt."""
    p = path or os.path.abspath(__file__)
    try:
        with open(p, 'rb') as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return {'counter': p, 'counter_sha256': None}
    return {'counter': p, 'counter_sha256': digest}


def stamp_receipt(doc, path=None):
    doc.update(counter_identity(path))
    return doc


def receipt_identity_ok(doc):
    """(ok, why) for a receipt this counter wrote: key present and honest."""
    if not isinstance(doc, dict):
        return False, 'not an object'
    if 'counter_sha256' not in doc:
        return False, 'missing counter_sha256'
    digest = doc.get('counter_sha256')
    if digest is None:
        return False, 'counter_sha256 is null'
    if not isinstance(digest, str) or not SHA_RE.match(digest.lower()):
        return False, 'counter_sha256 is not 64 hex'
    path = doc.get('counter')
    if not isinstance(path, str) or not path:
        return False, 'missing counter path'
    try:
        with open(path, 'rb') as fh:
            actual = hashlib.sha256(fh.read()).hexdigest()
    except OSError as e:
        return False, 'counter file unreadable: %s' % e
    if actual != digest.lower():
        return False, 'counter_sha256 does not describe %s' % path
    return True, 'ok'


def write_receipt(doc, path):
    """Write a score receipt and prove its own identity on the way out."""
    stamped = stamp_receipt(dict(doc))
    with open(path, 'w') as fh:
        json.dump(stamped, fh, indent=1, sort_keys=True)
    try:
        with open(path) as fh:
            written = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        return stamped, False, 'receipt unreadable after write: %s' % e
    ok, why = receipt_identity_ok(written)
    return stamped, ok, why


def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def sid_tokens(text):
    return set(SID_RE.findall(text))


# ------------------------------------------------------------- evidence id

def find_rea_pkg():
    """Locate a rea-agents 6.5.0 package root under the npm npx cache."""
    cache = os.environ.get('npm_config_cache') or os.path.expanduser('~/.npm')
    base = os.path.join(cache, '_npx')
    if not os.path.isdir(base):
        return None
    for name in sorted(os.listdir(base)):
        root = os.path.join(base, name, 'node_modules', 'rea-agents')
        pj = os.path.join(root, 'package.json')
        if not os.path.isfile(pj):
            continue
        try:
            with open(pj) as fh:
                if json.load(fh).get('version') == REA_VERSION:
                    return root
        except (OSError, json.JSONDecodeError):
            continue
    return None


def rea_pkg_path(root, freeze):
    """The frozen rea-pkg document, from the first candidate present at freeze."""
    for path in REA_PKG_CANDIDATES:
        raw = show(root, freeze, path)
        if raw is not None:
            return path, raw
    return None, None


def rea_package_problems(root, freeze, pkg65):
    """(problems, doc, path) for the frozen rea-pkg document against the package."""
    path, raw = rea_pkg_path(root, freeze)
    if raw is None:
        return ['rea-pkg pin absent at freeze (%r)' % (REA_PKG_CANDIDATES,)], None, None
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return ['rea-pkg pin is not JSON: %s' % e], None, path
    if not isinstance(doc, dict):
        return ['rea-pkg pin is not an object'], None, path
    probs = []
    if doc.get('version') != REA_VERSION:
        probs.append('rea-pkg version %r != %r' % (doc.get('version'), REA_VERSION))
    pkg_root = os.path.abspath(pkg65)
    lock_candidates = [os.path.join(os.path.dirname(pkg_root), 'package-lock.json'),
                       os.path.join(os.path.dirname(os.path.dirname(pkg_root)),
                                    'package-lock.json')]
    lock_path = next((p for p in lock_candidates if os.path.isfile(p)), None)
    candidates = (('package.json', os.path.join(pkg_root, 'package.json'),
                   'package_json_sha256'),
                  ('package-lock.json', lock_path, 'package_lock_sha256'))
    for name, p, key in candidates:
        want = doc.get(key)
        if not (isinstance(want, str) and SHA_RE.match(want.lower())):
            probs.append('rea-pkg %s is not 64 hex' % key)
            continue
        got = file_sha256(p) if p else None
        if got is None:
            probs.append('%s unreadable beside --pkg65' % name)
        elif got != want.lower():
            probs.append('%s sha256 %s != frozen %s' % (name, got, want))
    return probs, doc, path


def evidence_ids(root, freeze, pkg65, envelopes, work):
    """Recompute the stored evidence id under the rea-agents 6.5.0 rule.

    The rule is not retyped: the frozen xpin tool evaluates the package's own
    `semanticProjection` and hashes it with the package's own digest code. The
    package itself is bound to the frozen rea-pkg pin (round 49)."""
    probs, _doc, _path = rea_package_problems(root, freeze, pkg65)
    if probs:
        raise Unevaluable('rea package does not match the freeze: '
                          + '; '.join(probs[:3]))
    tool = show(root, freeze, XPIN)
    if tool is None:
        raise Unevaluable('xpin tool absent at freeze')
    node = which_fixed('node')
    if node is None:
        raise Unevaluable('node not found on the fixed PATH %r' % (FIXED_PATH,))
    tpath = os.path.join(work, 'xpin-attribute.mjs')
    with open(tpath, 'wb') as fh:
        fh.write(tool)
    paths = []
    for name, env in envelopes.items():
        p = os.path.join(work, name.replace('/', '_') + '.wrapped.json')
        with open(p, 'w') as fh:
            json.dump({'data': env}, fh)
        paths.append((name, p))
    if not paths:
        return {}
    r = subprocess.run([node, tpath, '--pkg65', pkg65, '--pkg67', pkg65]
                       + [p for _, p in paths], capture_output=True, text=True)
    if r.returncode != 0:
        raise Unevaluable('xpin: ' + r.stderr.strip())
    out = {}
    lines = [l for l in r.stdout.splitlines() if l]
    if len(lines) != len(paths):
        raise Unevaluable('xpin line count mismatch')
    for (name, _), line in zip(paths, lines):
        f = line.split('\t')
        if len(f) < 3:
            raise Unevaluable('xpin bad line: ' + line)
        out[name] = (f[1], f[2])
    return out


# ------------------------------------------------------------- frozen tables

def parse_oracle(raw):
    """(rows[(rel, sha256, size)], error) for the oracle table.

    Exactly three columns (round 50; the round-41 parser accepted two and never
    compared the size): relative path, 64-hex sha256, non-negative decimal size.
    The path is a filesystem-relative spelling (a tar-style `./` prefix is the
    only normalisation; no absolute path, no `.`/`..` component)."""
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) != 3:
            return [], 'row %r has %d fields, want 3 (rel, sha256, size)' % (line, len(f))
        rel = strip_rel(f[0].strip())
        sha = f[1].strip().lower()
        if not rel:
            return [], 'empty path in %r' % (line,)
        if rel.startswith('/') or any(x in ('', '.', '..') for x in rel.split('/')):
            return [], 'illegal path spelling in %r' % (line,)
        if not SHA_RE.match(sha):
            return [], 'row %r sha256 is not 64 lowercase hex' % (line,)
        size = f[2].strip()
        if not size.isdigit():
            return [], 'row %r size is not a non-negative decimal integer' % (line,)
        rows.append((rel, sha, int(size)))
    if not rows:
        return [], 'no rows'
    seen = set()
    for rel, _, _ in rows:
        if rel in seen:
            return [], 'duplicate oracle path %r' % (rel,)
        seen.add(rel)
    return rows, None


def parse_nonregular(raw):
    """(rows[(rel, kind, detail)], error) for nonregular.tsv.

    `detail` is the optional third column (the stored link target as the oracle
    listed it); `removed.silent` matches on it. Empty table is allowed."""
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'row %r has %d fields, want >= 2 (rel, kind[, detail])' % (line, len(f))
        rel = f[0].strip()
        kind = f[1].strip().lower()
        if (rel, kind) == ('relative_path', 'kind'):
            continue                      # tolerated header row
        if not rel or not kind:
            return [], 'empty path/kind in %r' % (line,)
        rows.append((rel, kind, f[2] if len(f) > 2 else None))
    seen = set()
    for row in rows:
        if (row[0], row[1]) in seen:
            return [], 'duplicate nonregular row %r' % (row[:2],)
        seen.add((row[0], row[1]))
    return rows, None


def gap_rule_model(raw):
    """(model, problems) for gap-rule.json.

    model = {'allowed': {kind: [gap kind]}, 'required': {kind: bool},
             'structural': {gap kind: limit}, 'removed': {...}}.
    `required` is optional; a kind with a non-empty `allowed` list is required by
    default (a non-regular entry that accounts for nothing at all is a
    materialised entry, which is what R39-CL3 separates from a clean extraction).
    `removed` is the extractor-determined disposition of R41C1DevCore 7.1:
    `{diagnostic, kinds, disposition: "exclusive", silent?: {kind: [detail]}}`."""
    probs = []
    model = {'allowed': {}, 'required': {}, 'structural': {}, 'removed': {}}
    if raw is None:
        return model, ['absent']
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return model, ['not JSON: %s' % e]
    if not isinstance(doc, dict):
        return model, ['not a JSON object']
    claim = doc.get('claim')
    if claim is not None and claim != 'R50-C1':
        probs.append('claim %r != R50-C1' % (claim,))
    structural = doc.get('structural')
    if structural is not None:
        if not isinstance(structural, dict):
            probs.append('`structural` must be an object')
        else:
            for kind, limit in structural.items():
                if not isinstance(kind, str) or not kind.strip():
                    probs.append('non-string structural gap kind %r' % (kind,))
                    continue
                if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
                    probs.append('structural[%r] must be a non-negative int' % (kind,))
                    continue
                model['structural'][kind.strip()] = limit
    allowed = doc.get('allowed')
    if not isinstance(allowed, dict) or not allowed:
        probs.append('`allowed` must be a non-empty object')
        allowed = allowed if isinstance(allowed, dict) else {}
    for kind, kinds in allowed.items():
        if not isinstance(kind, str) or not kind.strip():
            probs.append('non-string non-regular kind %r' % (kind,))
            continue
        if not isinstance(kinds, list) or not all(isinstance(k, str) and k for k in kinds):
            probs.append('allowed[%r] must be a list of gap kinds' % (kind,))
            continue
        if len(set(kinds)) != len(kinds):
            probs.append('allowed[%r] repeats a gap kind' % (kind,))
        model['allowed'][kind.strip().lower()] = [k.strip() for k in kinds]
    required = doc.get('required')
    if required is not None:
        if not isinstance(required, dict):
            probs.append('`required` must be an object')
        else:
            for kind, flag in required.items():
                key = kind.strip().lower() if isinstance(kind, str) else None
                if key not in model['allowed']:
                    probs.append('required[%r] names a kind absent from allowed' % (kind,))
                    continue
                if not isinstance(flag, bool):
                    probs.append('required[%r] must be a boolean' % (kind,))
                    continue
                model['required'][key] = flag
    removed = doc.get('removed')
    if removed is not None:
        if not isinstance(removed, dict):
            probs.append('`removed` must be an object')
        else:
            diag = removed.get('diagnostic')
            kinds = removed.get('kinds')
            disp = removed.get('disposition', 'exclusive')
            silent = removed.get('silent', {})
            if not (isinstance(diag, str) and diag.strip()):
                probs.append('removed.diagnostic must be a non-empty string')
                diag = None
            if not (isinstance(kinds, list) and kinds
                    and all(isinstance(k, str) and k for k in kinds)):
                probs.append('removed.kinds must be a non-empty list of kinds')
                kinds = []
            if disp != 'exclusive':
                probs.append('removed.disposition %r != "exclusive"' % (disp,))
            if not isinstance(silent, dict):
                probs.append('removed.silent must be an object')
                silent = {}
            for kind, details in silent.items():
                if not (isinstance(details, list)
                        and all(isinstance(x, str) for x in details)):
                    probs.append('removed.silent[%r] must be a list of details'
                                 % (kind,))
                    continue
            model['removed'] = {
                'diagnostic': diag.strip() if isinstance(diag, str) else None,
                'kinds': [k.strip().lower() for k in kinds],
                'disposition': disp,
                'silent': {str(k).strip().lower(): list(v)
                           for k, v in silent.items() if isinstance(v, list)},
            }
    return model, probs


def carriers_spec(spec, target, expected_ids):
    """(ids, problems) for the frozen carrier list."""
    probs = []
    if 'claim' in spec and spec.get('claim') != 'R50-C1':
        probs.append('claim %r != R50-C1' % (spec.get('claim'),))
    cs = spec.get('carriers')
    if not isinstance(cs, list):
        return [], probs + ['carriers is not a list']
    if spec.get('target') != target:
        probs.append('frozen target %r != counter target %d' % (spec.get('target'), target))
    prof = spec.get('projection')
    if prof != DEFAULT_PROFILE:
        probs.append('projection %r must be frozen explicitly as %r (round 50: '
                     'derivations[], the source of the oracle root, are compared '
                     'in the rerun)' % (prof, DEFAULT_PROFILE))
    if 'prior_pins' in spec:
        pp = spec.get('prior_pins')
        if not (isinstance(pp, list)
                and all(isinstance(x, str) and SHA_RE.match(x.lower())
                        for x in pp)):
            probs.append('prior_pins must be a list of 64-hex pins')
    ids = [c.get('id') for c in cs if isinstance(c, dict)]
    if len(ids) != target:
        probs.append('carriers has %d entries, want %d' % (len(ids), target))
    if len(set(ids)) != len(ids):
        probs.append('duplicate carrier ids %r' % (ids,))
    if expected_ids:
        got = {str(i).lower() for i in ids if isinstance(i, str)}
        want = {i.lower() for i in expected_ids}
        if got != want:
            probs.append('carrier ids %r != %r' % (sorted(map(str, ids)),
                                                  list(expected_ids)))
    # The REA extraction parameters are frozen data (round 50): the round-41
    # counter replayed whatever `parameters` the committed receipt recorded, so a
    # receipt made at any depth/budget was compared with a rerun at the same
    # depth/budget. The claim is `--max-depth 1` and the budgets the frozen table
    # names; `parameters_ok` binds the receipt to them and the rerun replays them.
    rp = spec.get('rea_parameters')
    if not isinstance(rp, dict):
        probs.append('rea_parameters is not an object')
    else:
        for key in ('max_depth', 'max_output_bytes', 'max_output_files'):
            v = rp.get(key)
            if not (isinstance(v, int) and not isinstance(v, bool) and v > 0):
                probs.append('rea_parameters.%s is not a positive int' % key)
        if rp.get('max_depth') != 1:
            probs.append('rea_parameters.max_depth %r != 1 (the claim is depth 1)'
                         % (rp.get('max_depth'),))
    pins = [c.get('sha256') for c in cs if isinstance(c, dict)]
    if len(set(pins)) != len(pins):
        probs.append('duplicate carrier pins')
    for c in cs:
        if not isinstance(c, dict):
            probs.append('non-object carrier entry')
            continue
        ext = c.get('external')
        keys = ('id', 'sha256', 'oracle', 'nonregular') if ext is not None else \
            ('id', 'path', 'sha256', 'oracle', 'nonregular')
        for key in keys:
            v = c.get(key)
            if not isinstance(v, str) or not v:
                probs.append('carrier %r lacks %s' % (c.get('id'), key))
        if ext is not None:
            # Round-40 L1 amendment (before the freeze): vendor AVM members are not
            # redistributable (AVM licence, R40SrcAvmVendor), so their bytes are pinned
            # by URL -> image sha256 -> tar member -> carve length -> carrier sha256 and
            # fetched into --carrier-cache by tools/round-41/fetch-vendor.py.
            if not isinstance(ext, dict):
                probs.append('carrier %r external is not an object' % (c.get('id'),))
            else:
                # Round-41 amendment (KaidokuR41): the whole chain is frozen in the
                # table, not in the fetcher - url, image sha256, tar member, the
                # member's own sha256, the carve length and the carrier pin, so a
                # changed image or member cannot pass unnoticed (routed R40-CL6).
                for key in ('url', 'image_sha256', 'member', 'member_sha256',
                            'length'):
                    if key not in ext:
                        probs.append('carrier %r external lacks %s' % (c.get('id'), key))
                isha = ext.get('image_sha256')
                if not (isinstance(isha, str) and SHA_RE.match(isha.lower())):
                    probs.append('carrier %r external image_sha256 is not 64 hex' % (c.get('id'),))
                msha = ext.get('member_sha256')
                if not (isinstance(msha, str) and SHA_RE.match(msha.lower())):
                    probs.append('carrier %r external member_sha256 is not 64 hex'
                                 % (c.get('id'),))
                length = ext.get('length')
                if not (isinstance(length, int) and not isinstance(length, bool)
                        and length > 0):
                    probs.append('carrier %r external length is not a positive int'
                                 % (c.get('id'),))
                nested = ext.get('nested')
                if nested is not None:
                    if not isinstance(nested, dict):
                        probs.append('carrier %r external nested is not an object'
                                     % (c.get('id'),))
                    else:
                        nsha = nested.get('sha256')
                        if not (isinstance(nsha, str) and SHA_RE.match(nsha.lower())):
                            probs.append('carrier %r nested.sha256 is not 64 hex'
                                         % (c.get('id'),))
            if c.get('path') is not None:
                probs.append('carrier %r has both path and external' % (c.get('id'),))
        sha = c.get('sha256')
        if isinstance(sha, str) and not SHA_RE.match(sha.lower()):
            probs.append('carrier %r sha256 is not 64 hex' % (c.get('id'),))
        receipt = c.get('receipt')
        if receipt is not None and not isinstance(receipt, str):
            probs.append('carrier %r receipt is not a string' % (c.get('id'),))
        oracle_root = c.get('oracle_root')
        if oracle_root is not None:
            if not (isinstance(oracle_root, str) and oracle_root
                    and not oracle_root.startswith('/')
                    and '..' not in oracle_root.split('/')):
                probs.append('carrier %r oracle_root is not a relative path'
                             % (c.get('id'),))
    return ids, probs


# ------------------------------------------------------------- carrier layout

def layout_probe(raw):
    """Decode the frozen layout of a carrier's little-endian SquashFS v4 superblock.

    SquashFS v4 little-endian superblock (96 bytes): magic 0:4, inodes 4:8,
    mkfs_time 8:12, block_size 12:16, fragments 16:20, compression 20:22,
    block_log 22:24, flags 24:26, no_ids 26:28, s_major 28:30, s_minor 30:32,
    root_inode 32:40, bytes_used 40:48, id_table_start 48:56,
    xattr_id_table_start 56:64, inode_table_start 64:72,
    directory_table_start 72:80, fragment_table_start 80:88,
    lookup_table_start 88:96 (unblob 26.6.4 SquashFSv4LEHandler.C_DEFINITIONS).

    The frozen layout (R50-C1) is: little-endian `hsqs`, v4.0, compression id 4
    (xz), `mkfs_time == bytes_used` (the AVM marker: AVM writes the filesystem
    size where a standard mksquashfs writes the build time), 0 < bytes_used <=
    file size, and the inode/directory table starts inside `bytes_used` in order.
    Every field is little-endian: `hsqs` fixes the whole file, so there is no
    big-endian decode, and no block-length endianness to settle (the round-41
    `layout_le` / plausibility / single-block-identity logic is removed with the
    big-endian layout it separated). A standard little-endian image carries a
    real timestamp, so the marker is what keeps it out of an AVM carrier slot
    (control CTL-C1-4)."""
    d = {'size': len(raw) if raw is not None else 0}
    if raw is None:
        d.update(ok=False, reason='absent')
        return d
    if len(raw) < SB_SIZE:
        d.update(ok=False, reason='shorter than a %d-byte superblock' % SB_SIZE)
        return d

    def u(off, width):
        return int.from_bytes(raw[off:off + width], 'little')

    d['magic'] = raw[0:4].decode('latin1')
    d['le_magic'] = raw[0:4] == b'hsqs'
    d['mkfs_time'] = u(8, 4)
    d['block_size'] = u(12, 4)
    d['compression'] = u(20, 2)
    d['major'] = u(28, 2)
    d['minor'] = u(30, 2)
    d['bytes_used'] = u(40, 8)
    d['inode_table_start'] = its = u(64, 8)
    d['directory_table_start'] = dts = u(72, 8)
    d['marker'] = d['mkfs_time'] == d['bytes_used']
    d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)
    d['version_v4'] = (d['major'], d['minor']) == (4, 0)
    d['compression_xz'] = d['compression'] == XZ_ID
    d['tables_sane'] = 0 < its < dts <= d['bytes_used']
    reason = None
    if not d['le_magic']:
        reason = 'magic %r is not little-endian hsqs' % (d['magic'],)
    elif not d['version_v4']:
        reason = 'version %d.%d is not 4.0' % (d['major'], d['minor'])
    elif not d['compression_xz']:
        reason = 'compression id %d is not %d (xz)' % (d['compression'], XZ_ID)
    elif not d['marker']:
        reason = 'AVM marker absent (mkfs_time %d != bytes_used %d)' % (
            d['mkfs_time'], d['bytes_used'])
    elif not d['bytes_used_sane']:
        reason = 'bytes_used %d outside 1..%d' % (d['bytes_used'], len(raw))
    elif not d['tables_sane']:
        reason = ('inode_table_start %d / directory_table_start %d not inside '
                  'bytes_used %d in order' % (its, dts, d['bytes_used']))
    d['ok'] = reason is None
    d['reason'] = reason
    return d


# ------------------------------------------------------------- receipt shape

def provenance_ok(output_directory):
    """A receipt run by this round: an absolute path under the round's scratch
    prefix `PROV_BASE` (a prefix, not a substring; no `..`; never /tmp)."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if '..' in output_directory.split('/'):
        return False
    return output_directory.startswith(PROV_BASE)


def trusted_run_root(output_directory):
    """The trusted directory a run's private extraction tree lives under."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return None
    if '..' in output_directory.split('/'):
        return None
    parent = os.path.dirname(output_directory.rstrip('/'))
    if not parent or parent == '/':
        return None
    return parent


# ------------------------------------------------------------- extract root

def path_parts(path):
    """Components of a receipt path, `$output/` sigil removed, '.' dropped.

    Returns None for a non-string. An absolute path is not a receipt path (REA
    normalizes every published path to `$output/<rel>`), but its components are
    still returned so the caller can refuse it explicitly."""
    if not isinstance(path, str) or not path:
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    return [x for x in p.split('/') if x not in ('', '.')]


def receipt_paths(env):
    """Every path a receipt normalizes, as relative to REA's unblob output root.

    `normalized_result` is the only source: files, unpublished entries,
    path-carrying extraction gaps, depth-limited task paths, derivation edges and
    the chunks' own input paths (a nested chunk's input names the extract
    directory that contains it)."""
    nr = env.get('normalized_result') or {}
    out = []

    def take(value):
        if isinstance(value, str) and value:
            out.append(value)

    for f in nr.get('files') or []:
        if isinstance(f, dict):
            take(f.get('relative_path'))
    for u in nr.get('unpublished_entries') or []:
        if isinstance(u, dict):
            take(u.get('relative_path'))
    for g in nr.get('extraction_gaps') or []:
        if isinstance(g, dict):
            take(g.get('relative_path'))
    for p in nr.get('depth_limited_paths') or []:
        take(p)
    for d in nr.get('derivations') or []:
        if isinstance(d, dict):
            take(d.get('parent_path'))
            take(d.get('child_path'))
    for c in nr.get('chunks') or []:
        if isinstance(c, dict):
            take(c.get('input_path'))
    return out


def strip_output(path):
    """A receipt path with one optional `$output/` prefix removed.

    The receipt mixes two namespaces: `files[].relative_path`,
    `unpublished_entries[].relative_path` and gap `relative_path` are bare, while
    gap `input_path`, `derivations[].parent_path/child_path` and
    `depth_limited_paths[]` carry the `$output/` sigil (R41C1Revenger 1.1)."""
    if not isinstance(path, str):
        return path
    if path.startswith('$output/'):
        return path[len('$output/'):]
    return path


def path_shape_problem(path):
    """Why a receipt path is not a legal spelling, or None (R41-D5, 2nd finding)."""
    if not isinstance(path, str) or not path:
        return 'empty path'
    p = path
    if p == '$input':
        return None
    if p.startswith('$output/'):
        p = p[len('$output/'):]
    elif p.startswith('/'):
        return 'absolute path %r' % (path,)
    if not p:
        return 'empty path after $output/'
    if p.endswith('/'):
        return 'trailing slash in %r' % (path,)
    for comp in p.split('/'):
        if comp == '':
            return 'empty component in %r' % (path,)
        if comp in ('.', '..'):
            return '%r component in %r' % (comp, path)
    return None


def path_shape_ok(env):
    """(ok, first problem) over every path the receipt normalises."""
    for p in receipt_paths(env):
        problem = path_shape_problem(p)
        if problem:
            return False, problem
    return True, None


def under_root(path, root):
    """Segment-bounded containment: `P == CR or P.startswith(CR + '/')` (R41-D5)."""
    if not isinstance(path, str) or not isinstance(root, str) or not root:
        return False
    p = strip_output(path)
    if p == root:
        return True
    return p.startswith(root.rstrip('/') + '/')


def squashfs_roots(env):
    """The receipt's chunk extract roots for the frozen handler (exact equality).

    unblob's subtasks are published as `derivations[]` edges and the child path
    is the directory a chunk was extracted into (rea-agents 6.5.0
    FirmwareReports.js:341-357). Only edges whose handler EQUALS `squashfs_v4_le`
    are filesystem roots for this claim (round 41 took every `squashfs_v4*`
    prefix): a whole-file chunk's root is `firmware.bin_extract`, a carved
    chunk's root is `<parent>/<start>-<end>.<handler>_extract`, and a nested
    image's root is `<parent>/<path to image>_extract`.

    Returns them deepest first; the counter never uses that order to guess
    (see subject_root)."""
    nr = env.get('normalized_result') or {}
    out = set()
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        if d.get('handler') != HANDLER:
            continue
        child = strip_output(d.get('child_path'))
        if isinstance(child, str) and child:
            out.add(child.rstrip('/'))
    return sorted(out, key=lambda r: (-len(r), r))


def subject_root(env, hint=None):
    """(extract root, how) of the chunk whose filesystem the oracle describes.

    Exactly one `squashfs_v4_le` derivation root is the normal case and needs no
    hint. Several roots (a wrapper carrier that also extracted a nested image)
    cannot be resolved from the receipt alone, so the freeze may name the
    intended root per carrier (`oracle_root` in carriers.json); without that hint
    the answer is None and the three path clauses fail closed. A hint that names
    no root at all is a frozen-table error and also resolves to None."""
    roots = squashfs_roots(env)
    if not roots:
        return None, 'no %s derivation edge' % (HANDLER,)
    if hint is not None:
        if hint not in roots:
            return None, 'oracle_root %r not among %r' % (hint, roots)
        return hint, 'oracle_root from carriers.json'
    if len(roots) == 1:
        return roots[0], 'single %s derivation root' % (HANDLER,)
    return None, 'ambiguous: %d %s roots %r (freeze oracle_root)' % (
        len(roots), HANDLER, roots)


def chunk_roots(env, hint=None):
    """[{extract_root, subject}] for the receipt, for reporting."""
    root, how = subject_root(env, hint)
    return {'roots': squashfs_roots(env), 'subject': root, 'source': how}


def diagnostic_rel(diagnostic, root, output_directory=None):
    """A removal diagnostic's entry path relative to the chunk extract root.

    unblob reports `MaliciousSymlinkRemoved(link=<absolute path inside its
    extraction dir>, target=...)` (unblob extractor.py:79-87) and REA stores it
    with `input_path` naming the task directory, so the entry path exists only in
    `link`. Round 49: the link must lie under the run's trusted root (the parent
    of `parameters.output_directory`, where TMPDIR pointed during the run), so a
    forged `link` naming another tree cannot be mapped. The subject root is then
    located as a run of whole segments after that prefix and the remainder is the
    entry's path; None when the link carries no such run (that diagnostic cannot
    be resolved and fails the disposition check closed)."""
    if root is None or not isinstance(diagnostic, dict):
        return None
    report = diagnostic.get('report')
    link = report.get('link') if isinstance(report, dict) else None
    if not isinstance(link, str) or not link:
        return None
    trusted = trusted_run_root(output_directory)
    if trusted is None:
        return None
    if not under_root(link, trusted):
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    tsegs = [x for x in trusted.split('/') if x not in ('', '.')]
    if segs[:len(tsegs)] != tsegs:
        return None
    rsegs = root.split('/')
    start = len(tsegs)
    for i in range(len(segs) - len(rsegs), start - 1, -1):
        if segs[i:i + len(rsegs)] == rsegs:
            return '/'.join(segs[i + len(rsegs):])
    return None


def diagnostics(env):
    nr = env.get('normalized_result') or {}
    return [d for d in (nr.get('diagnostics') or []) if isinstance(d, dict)]


def diagnostic_typename(diagnostic):
    report = diagnostic.get('report')
    return report.get('__typename__') if isinstance(report, dict) else None


def extract_rel(path, root):
    """A receipt path relative to its chunk extract root, or None if not inside.

    Exact: the path must be `<root>/<rel>` (or the root itself) on whole
    segments. Nothing else counts - not a suffix, not a basename. R40-CL1 was a
    suffix test (`candidate.endswith('/' + rel)`), under which the regular file
    `usr/bin/busy` scored as the symlink entry `bin/busy`."""
    if root is None or not isinstance(path, str) or not path:
        return None
    if not under_root(path, root):
        return None
    parts = path_parts(path)
    if parts is None:
        return None
    pret = root.split('/')
    if parts[:len(pret)] != pret:
        return None
    rest = parts[len(pret):]
    return '/'.join(rest) if rest else ''


def strip_rel(rel):
    """A table row without a leading './' or '/' (tar-style prefixes name the
    same file; nothing else is normalised)."""
    if not isinstance(rel, str):
        return rel
    r = rel
    while r.startswith('./'):
        r = r[2:]
    return r.lstrip('/')


def same_rel(candidate, rel, root):
    """Exact match of a receipt path against a filesystem-relative table row."""
    if not rel:
        return False
    return extract_rel(candidate, root) == strip_rel(rel)


def legacy_same_rel(candidate, rel):
    """The round-40 matcher, verbatim (defect R40-CL1). Selftest only: every
    collision case asserts that this rule mis-scores what `same_rel` scores
    right, so the selftest cannot silently stop discriminating."""
    return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))


def published(env):
    nr = env.get('normalized_result') or {}
    out = []
    for f in (nr.get('files') or []):
        if isinstance(f, dict):
            out.append((f.get('relative_path') or '', f.get('sha256') or '', f.get('size')))
    return out


def chunk_handlers(env):
    nr = env.get('normalized_result') or {}
    return [c.get('handler') for c in (nr.get('chunks') or []) if isinstance(c, dict)]


def squashfs_chunk_handlers(env):
    """The receipt's chunk handlers that belong to the SquashFS family."""
    return [h for h in chunk_handlers(env)
            if isinstance(h, str) and SQUASHFS_HANDLER_RE.match(h)]

def chunk_failed(env):
    nr = env.get('normalized_result') or {}
    return any(isinstance(c, dict) and c.get('extraction_failed')
               for c in (nr.get('chunks') or []))


def gaps(env):
    nr = env.get('normalized_result') or {}
    return list(nr.get('extraction_gaps') or [])


def published_index(files, root, nested=()):
    """{rel: [(sha256, size), ...]} for the published files under the extract root.

    One pass over the receipt (round 50): a rootfs carrier publishes ~13k
    regular files, and the round-41 per-row scan was O(rows x files). The index
    is keyed by the exact path relative to the root (`extract_rel`), so the
    exactness of the match is unchanged. Files under a `nested` extract root (the
    `<root>/<image>_extract` directory of another chunk) belong to that chunk's
    namespace and are not indexed."""
    idx = {}
    if root is None:
        return idx
    for fp, fsha, fsize in files:
        if any(under_root(fp, n) for n in nested):
            continue
        rel = extract_rel(fp, root)
        if rel:
            idx.setdefault(rel, []).append((fsha, fsize))
    return idx


def nested_roots(env, root):
    """Extract roots of OTHER chunks that lie inside `root` (a nested image's
    `<root>/<path>_extract`), from the receipt's own derivation edges."""
    if root is None:
        return []
    nr = env.get('normalized_result') or {}
    out = set()
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        child = strip_output(d.get('child_path'))
        if isinstance(child, str) and child.rstrip('/').startswith(root + '/'):
            out.add(child.rstrip('/'))
    return sorted(out)


def oracle_hits(rows, files, root, nested=()):
    """Oracle rows published exactly: rel, sha256 and size (round 49 added size)."""
    if root is None:
        return 0
    idx = published_index(files, root, nested)
    hits = 0
    for rel, sha, want_size in rows:
        if any(s == sha and z == want_size for s, z in idx.get(strip_rel(rel), [])):
            hits += 1
    return hits


def published_rels(files, root, nested=()):
    """The distinct relative paths of published regular files under the root."""
    return sorted(published_index(files, root, nested))


def extra_published(rows, files, root, nested=()):
    """Published regular files under the root that the oracle does not list."""
    if root is None:
        return []
    want = {strip_rel(row[0]) for row in rows}
    return [rel for rel in published_rels(files, root, nested) if rel not in want]


def nonregular_published(files, nonreg, root):
    """Published file paths that equal a non-regular entry's path under the root."""
    hits = []
    if root is None:
        return hits
    entries = {strip_rel(rel) for rel, _kind, _detail in nonreg}
    for fp, _, _ in files:
        rel = extract_rel(fp, root)
        if rel and rel in entries:
            hits.append(fp)
    return hits


def silent_detail_matches(detail, allowed):
    """Does an oracle row's detail name one of the rule's silent details?

    `empty-target` is the rule's label for the empty link target unblob deletes
    without any report (unblob extractor.py:68-71), so it matches an empty third
    column; any other label matches the column verbatim. A row with no third
    column has no detail and matches nothing."""
    if detail is None:
        return False
    for label in allowed:
        if label == 'empty-target':
            if detail == '':
                return True
        elif detail == label:
            return True
    return False


def disposition_check(gaps_list, diags, nonreg, model, root, output_directory=None):
    """Three families, all frozen data (R41C1DevCore 7.1).

    path-resolved gap   a gap with a relative_path must resolve (exact match after
                        the chunk extract root) to exactly one non-regular entry
                        and its kind must be listed for that entry's kind
    structural gap      a gap with relative_path null (unblob's own bookkeeping:
                        `unknown-chunk-handler` for a residual chunk,
                        `depth-limited` for a truncated task) must have its kind in
                        `structural` and must not exceed that kind's per-carrier
                        allowance. A kind not listed (e.g. REA's
                        `missing-extractor-dependency`, reported when `sasquatch`
                        is absent from the child PATH) fails here.
    removal             every diagnostic whose `__typename__` the rule names is a
                        removal: it must resolve at its exact path to a
                        non-regular entry whose kind is in `removed.kinds`, and
                        that entry may not also carry a gap ('exclusive')

    Then every entry whose kind is required must carry exactly one disposition:
    an allowed gap, a removal, or - only when the rule lists the entry's
    kind/detail under `silent` - nothing at all (unblob deletes an empty-target
    symlink without any report, unblob extractor.py:68-71). The silent admission
    is per row, so the routing text's count-based wording is met and nothing else
    can hide behind the allowance. An unknown root fails closed.

    Round 50: the entry lookups are dictionary lookups on the exact relative path
    (the round-41 form scanned every non-regular row per gap, O(gaps x rows); a
    rootfs carrier has ~850 non-regular rows and as many gaps).
    """
    if root is None:
        return False, 'no extract root: paths cannot be resolved'
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    removed = model.get('removed') or {}
    by_rel = {rel: (kind, detail) for rel, kind, detail in nonreg}
    rows_at = {}
    for rel, _kind, _detail in nonreg:
        rows_at.setdefault(strip_rel(rel), []).append(rel)
    gapped = {}
    struct_count = {}
    for g in gaps_list:
        if not isinstance(g, dict):
            return False, 'non-object gap'
        kind = g.get('kind')
        rp = g.get('relative_path')
        if rp is None:
            if kind not in structural:
                return False, 'gap kind %r has no path and no structural allowance' % (kind,)
            struct_count[kind] = struct_count.get(kind, 0) + 1
            continue
        if kind in structural:
            return False, 'structural gap kind %r carries a path %r' % (kind, rp)
        rel_in_root = extract_rel(rp, root)
        hits = rows_at.get(rel_in_root, []) if rel_in_root else []
        if len(hits) != 1:
            return False, 'gap path %r matches %d non-regular entries' % (rp, len(hits))
        entry_kind = by_rel[hits[0]][0]
        if kind not in allowed.get(entry_kind, []):
            return False, 'gap kind %r not allowed for %r entry %r (allowed %r)' % (
                kind, entry_kind, hits[0], allowed.get(entry_kind, []))
        gapped.setdefault(hits[0], []).append(kind)
    over = {k: [n, structural[k]] for k, n in struct_count.items()
            if n > structural[k]}
    if over:
        return False, 'structural gaps over allowance %r' % (over,)

    removal_name = removed.get('diagnostic')
    removal_kinds = removed.get('kinds') or []
    removed_rels = {}
    if removal_name:
        for d in diags:
            if diagnostic_typename(d) != removal_name:
                continue
            rel = diagnostic_rel(d, root, output_directory)
            if rel is None:
                return False, ('removal diagnostic without a path under the root: %r'
                               % (d.get('input_path'),))
            hits = rows_at.get(rel, [])
            if len(hits) != 1:
                return False, ('removal resolves to %d non-regular entries at %r'
                               % (len(hits), rel))
            entry_kind = by_rel[hits[0]][0]
            if entry_kind not in removal_kinds:
                return False, ('removal at %r names a %r entry; removed.kinds is %r'
                               % (rel, entry_kind, removal_kinds))
            if gapped.get(hits[0]):
                return False, 'entry %r is both gapped and removed' % (hits[0],)
            removed_rels.setdefault(hits[0], 0)
            removed_rels[hits[0]] += 1

    missing = []
    silent_admitted = []
    for rel, kind, detail in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
        if gapped.get(rel) or removed_rels.get(rel):
            continue
        allowed_details = (removed.get('silent') or {}).get(kind)
        if allowed_details and silent_detail_matches(detail, allowed_details):
            silent_admitted.append(rel)
            continue
        missing.append(rel)
    if missing:
        return False, ('required entry with no disposition (no gap, no %s) on %r'
                       % (removal_name or 'removal', sorted(missing)[:8]))
    return True, ('%d gaps (%d structural), %d removals, %d silent, on %d '
                  'non-regular entries' % (
                      len(gaps_list), sum(struct_count.values()),
                      sum(removed_rels.values()), len(silent_admitted),
                      len(nonreg)))


def all_adds(root, rev, path):
    """Every commit in the FULL history of `rev` that adds `path`, newest first.

    `--full-history -m` (round 50, shortcut critique S4): the default simplified
    history follows only the first TREESAME parent of a merge, so a pre-freeze add
    on the other side of a merge was invisible in round 49. None when git fails."""
    p = git(root, 'log', '-m', '--full-history', '--diff-filter=A', '--format=%H',
            rev, '--', path, check=False)
    if p.returncode != 0:
        return None
    seen, out = set(), []
    for l in p.stdout.decode().splitlines():
        l = l.strip()
        if l and l not in seen:
            seen.add(l)
            out.append(l)
    return out


def is_ancestor(root, ancestor, descendant):
    p = git(root, 'merge-base', '--is-ancestor', ancestor, descendant, check=False)
    return p.returncode == 0


def prior_pins(root, freeze, spec):
    """(pins, sources) a previous C1 freeze already scored.

    The claim's kill rule names relabelled earlier-round receipts as a control
    that must stop C1, so a carrier whose bytes are a pin an earlier round scored
    cannot be counted as new coverage however the table names it. Frozen sources,
    all read at the FREEZE commit (a table added later cannot bless an old pin):
      carriers.json `prior_pins`   an explicit list of 64-hex pins
      PRIOR_CARRIER_TABLES         the round-41 BE carrier table and the round-49
                                   v1/v2 carrier table (their `carriers[].sha256`)
      PRIOR_PIN_CANDIDATES         `{pins: [...]}` documents (round 42/49/50)
    """
    pins, sources = set(), []
    listed = spec.get('prior_pins')
    if isinstance(listed, list):
        for p in listed:
            if isinstance(p, str) and SHA_RE.match(p.lower()):
                pins.add(p.lower())
        if listed:
            sources.append('prior_pins')
    for path in PRIOR_CARRIER_TABLES:
        raw = show(root, freeze, path)
        if raw is None:
            continue
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict):
            for c in doc.get('carriers') or []:
                if isinstance(c, dict) and isinstance(c.get('sha256'), str) \
                        and SHA_RE.match(c['sha256'].lower()):
                    pins.add(c['sha256'].lower())
            sources.append(path)
    for path in PRIOR_PIN_CANDIDATES:
        raw = show(root, freeze, path)
        if raw is None:
            continue
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(doc, dict) and isinstance(doc.get('pins'), list):
            for e in doc['pins']:
                if isinstance(e, str) and SHA_RE.match(e.lower()):
                    pins.add(e.lower())
                elif isinstance(e, dict) and isinstance(e.get('sha256'), str) \
                        and SHA_RE.match(e['sha256'].lower()):
                    pins.add(e['sha256'].lower())
            sources.append(path)
    return pins, sources


def _frozen_paths(spec):
    frozen = set(FROZEN_PATHS)
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        for key in ('path', 'oracle', 'nonregular'):
            v = c.get(key)
            if isinstance(v, str) and v:
                frozen.add(v)
    return frozen


def frozen_drift(root, freeze, rev, spec):
    """Commits in FREEZE..REV that change a frozen C1 path (freeze-drift binding).

    Merge-aware (`-m --diff-merges=first-parent`): a frozen path edited inside a
    merged branch is a change. M/D/R/T/U are changes; A is a change under a
    frozen prefix and for any frozen path that existed at FREEZE (a re-add is not
    a restore). Each frozen blob that exists at FREEZE must also be
    byte-identical at REV: a later restore does not un-block."""
    frozen = _frozen_paths(spec)
    prefixes = FROZEN_PREFIXES

    def is_frozen(path):
        return path in frozen or any(path.startswith(p) for p in prefixes)

    p = git(root, '-c', 'core.quotePath=false', 'log', '-m', '--diff-merges=first-parent',
            '--name-status', '--pretty=format:', f'{freeze}..{rev}', check=False)
    if p.returncode != 0:
        raise Unevaluable('git log freeze..rev failed')
    existed_cache = {}
    touched = set()
    for line in p.stdout.decode(errors='replace').splitlines():
        line = line.strip()
        if not line:
            continue
        f = line.split('\t')
        status = f[0]
        paths = [x for x in f[1:] if x]
        if not paths:
            continue
        code = status[0]
        for path in paths:
            if not is_frozen(path):
                continue
            if code == 'A':
                if any(path.startswith(pfx) for pfx in prefixes):
                    touched.add(path)
                else:
                    if path not in existed_cache:
                        existed_cache[path] = show(root, freeze, path) is not None
                    if existed_cache[path]:
                        touched.add(path)
            elif code in 'MDRTU':
                touched.add(path)
    # blob equality at the endpoints (a path could be untouched in the log but
    # differ through an exotic diff; this is cheap and exact). Prefix families are
    # enumerated at the freeze.
    at_freeze = set(frozen)
    for pfx in prefixes:
        t = git(root, 'ls-tree', '-r', '--name-only', freeze, '--', pfx, check=False)
        if t.returncode == 0:
            at_freeze |= {x.strip() for x in t.stdout.decode(errors='replace')
                          .splitlines() if x.strip()}
    for path in sorted(at_freeze):
        b = git(root, 'rev-parse', f'{freeze}:{path}', check=False)
        if b.returncode != 0:
            continue
        a = git(root, 'rev-parse', f'{rev}:{path}', check=False)
        if a.returncode != 0:
            touched.add(path)
            continue
        if a.stdout.strip() != b.stdout.strip():
            touched.add(path)
    return sorted(touched)


# ------------------------------------------------------------- projection

def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def rel_suffix(path):
    """Path after the first `<something>_extract` chunk extract directory.

    Same rule as the R40C1Projection seat's projection.py (artifact, not
    frozen): unblob extracts a chunk into `<something>_extract/`, and `something`
    tracks the staged input name, which differs between the round run and the
    counter's rerun. A null path is preserved (gaps of an extraction that never
    produced entries carry relative_path: null)."""
    if path is None:
        return None
    if not isinstance(path, str):
        return None
    while path.startswith('$output/'):
        path = path[len('$output/'):]
    parts = [p for p in path.split('/') if p not in ('', '.')]
    for i, part in enumerate(parts):
        if part.endswith('_extract') and i + 1 < len(parts):
            return '/'.join(parts[i + 1:])
    return '/'.join(parts)


def projection(env, profile='core'):
    """Semantic projection compared between a committed receipt and a fresh run.

    `profile` is frozen data (the optional `projection` key of carriers.json,
    default `core`), so the freeze chooses how much of the run is compared
    without editing this file:
      core            the six fields of the P41-C1 draft (R40C1Projection's item
                      text): subject digest, files (suffix, sha256, size), chunks
                      (handler, start, end, failed), gaps (kind, suffix, deps),
                      unpublished entries, diagnostics typenames.
      plus-mime       core + files[].mime_type (libmagic output, not in the oracle)
      plus-content    plus-mime + files[].md5/sha1 from the run's HashReport
      plus-extractor  plus-mime + combinations + engine name/version +
                      published_bytes + coverage (extractor-determined)
    All four were measured stable across three real runs of one carrier
    (artifacts/R40C1Counter/projection-profiles.json). The fields are inlined
    here on purpose: scores must read frozen in-repo bytes, never a wave
    artifact. Everything that varies between two runs of the same bytes is
    excluded: evidence id, absolute paths, output directory, staged input name,
    provider/blob ids, continuation ids, timestamps, selection and analysis
    fields."""
    if profile not in PROFILES:
        raise Unevaluable('unknown projection profile %r' % (profile,))
    nr = env.get('normalized_result') or {}
    subject = ((env.get('subject') or {}).get('digest') or {}).get('sha256')
    proj_root = subject_root(env)[0]

    def norm(path):
        """Run-invariant form of a receipt path: its rel under the subject root.

        The root is the receipt's own derivation root, so a carve directory that
        only exists in one of the two runs does not leak into the projection; a
        path outside that root falls back to the round-40 suffix normalisation so
        carve artifacts still project (and still have to match)."""
        if proj_root is not None:
            rel = extract_rel(path, proj_root)
            if rel is not None:
                return rel
        return rel_suffix(path)

    hashes = {}
    if profile in ('plus-content', 'plus-extractor'):
        for task in (env.get('raw_result') or {}).get('report') or []:
            if not isinstance(task, dict):
                continue
            key = norm((task.get('task') or {}).get('path'))
            if key is None:
                continue
            for report in task.get('reports') or []:
                if isinstance(report, dict) and report.get('__typename__') == 'HashReport':
                    hashes[key] = [report.get('md5'), report.get('sha1')]

    files = []
    for e in nr.get('files') or []:
        if not isinstance(e, dict):
            continue
        row = [norm(e.get('relative_path')), e.get('sha256'), e.get('size')]
        if profile != 'core':
            row.append(e.get('mime_type'))
        if profile in ('plus-content', 'plus-extractor'):
            row += hashes.get(norm(e.get('relative_path')) or '', [None, None])
        files.append(row)
    files.sort(key=lambda r: (r[0] if r[0] is not None else '', canonical(r[1:])))

    chunks = []
    for c in nr.get('chunks') or []:
        if not isinstance(c, dict):
            continue
        rng = c.get('range') or {}
        start = rng.get('offset')
        end = None
        if isinstance(start, int) and isinstance(rng.get('length'), int):
            end = start + rng['length']
        chunks.append([c.get('handler'), start, end,
                       bool(c.get('extraction_failed'))])
    chunks.sort(key=canonical)

    gaps = []
    for g in nr.get('extraction_gaps') or []:
        if not isinstance(g, dict):
            continue
        deps = sorted((norm(d) for d in (g.get('dependencies') or [])),
                      key=lambda v: (v is not None, v or ''))
        gaps.append([g.get('kind'), norm(g.get('relative_path')), deps])
    gaps.sort(key=canonical)

    unpub = []
    for u in nr.get('unpublished_entries') or []:
        if not isinstance(u, dict):
            continue
        unpub.append([u.get('kind'), norm(u.get('relative_path'))])
    unpub.sort(key=canonical)

    # A diagnostic is projected with the entry it names, not the typename alone:
    # once removals are an admitted disposition, a rerun that removed a different
    # link must not match (R41C1DevCore 7.3). The entry path is the root-mapped
    # `report.link` when the root is known, else the task path; `rel_suffix` is
    # the run-invariant normalisation (the staged directory name is the same in
    # every rea-agents 6.5.0 run, so nothing is lost).
    diags = []
    run_params = env.get('parameters')
    od_run = run_params.get('output_directory') if isinstance(run_params, dict) else None
    for d in nr.get('diagnostics') or []:
        if not isinstance(d, dict):
            continue
        typename = diagnostic_typename(d) or '<none>'
        rel = diagnostic_rel(d, proj_root, od_run) if proj_root else None
        if rel is None:
            rel = norm(d.get('input_path'))
        diags.append([typename, rel])
    diags.sort(key=canonical)

    out = {
        'subject_sha256': subject,
        'files': files,
        'chunks': chunks,
        'extraction_gaps': gaps,
        'unpublished_entries': unpub,
        'diagnostics': diags,
    }
    if profile == 'plus-extractor':
        edges = []
        for deriv in nr.get('derivations') or []:
            if not isinstance(deriv, dict):
                continue
            edges.append([norm(deriv.get('parent_path')),
                          norm(deriv.get('child_path')),
                          deriv.get('handler')])
        edges.sort(key=canonical)
        engine = nr.get('engine') or {}
        out['derivations'] = edges
        out['engine'] = [engine.get('name'), engine.get('version')]
        out['published_bytes'] = nr.get('published_bytes')
        out['coverage'] = nr.get('coverage')
    return out


PROFILES = ('core', 'plus-mime', 'plus-content', 'plus-extractor')
DEFAULT_PROFILE = 'plus-extractor'      # carried from round 40 (L1 ruling, w1)
PROJECTION_KEYS = ('subject_sha256', 'files', 'chunks', 'extraction_gaps',
                   'unpublished_entries', 'diagnostics')
PROJECTION_KEYS_BY_PROFILE = {
    'core': PROJECTION_KEYS,
    'plus-mime': PROJECTION_KEYS,
    'plus-content': PROJECTION_KEYS,
    'plus-extractor': PROJECTION_KEYS + ('derivations', 'engine',
                                        'published_bytes', 'coverage'),
}


def projection_diff(a, b, profile='core'):
    """(equal, differing keys, short detail) between two projections."""
    keys = []
    detail = {}
    for k in PROJECTION_KEYS_BY_PROFILE[profile]:
        if a.get(k) == b.get(k):
            continue
        keys.append(k)
        if isinstance(a.get(k), list):
            only_a = [x for x in a.get(k) or [] if x not in (b.get(k) or [])]
            only_b = [x for x in b.get(k) or [] if x not in (a.get(k) or [])]
            detail[k] = {'committed_only': only_a[:3], 'fresh_only': only_b[:3],
                         'counts': [len(a.get(k) or []), len(b.get(k) or [])]}
        else:
            detail[k] = {'committed': a.get(k), 'fresh': b.get(k)}
    return not keys, keys, detail


# ------------------------------------------------------------- rerun

MAX_REA_ATTEMPTS = 3          # round 50: attempts at one REA run when REA reports `provider_timeout`
REPLAY_PARAMS = (('--max-depth', 'max_depth'),
                 ('--max-output-bytes', 'max_output_bytes'),
                 ('--max-output-files', 'max_output_files'))


class CounterNotFrozen(Unevaluable):
    reason = 'counter_not_frozen'


class OracleEnvError(Unevaluable):
    reason = 'oracle_env_error'


def rea_entry(pkg65):
    """(CLI entry path, version, package.json sha256, problem) of the REA package.

    The entry is the `rea-agents` (or bare string) `bin` of the package at
    `--pkg65`; node runs it directly (round 50: no npx)."""
    pj = os.path.join(os.path.abspath(pkg65), 'package.json')
    try:
        with open(pj) as fh:
            doc = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        return None, None, None, 'package.json unreadable: %s' % e
    bins = doc.get('bin')
    entry = bins.get('rea-agents') if isinstance(bins, dict) else bins
    if not isinstance(entry, str) or not entry:
        return None, doc.get('version'), None, 'package.json has no rea-agents bin'
    full = os.path.join(os.path.abspath(pkg65), entry)
    if not os.path.isfile(full):
        return None, doc.get('version'), None, 'bin entry %r is not a file' % (entry,)
    return full, doc.get('version'), file_sha256(pj), None


def _first_line(argv, timeout=60):
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout,
                           env=dict(os.environ, PATH=FIXED_PATH))
    except (OSError, subprocess.SubprocessError):
        return None
    text = (p.stdout or p.stderr or '').strip()
    return text.splitlines()[0].strip() if text else ''


def toolchain_record(unblob_path, pkg65):
    """The bound toolchain of the rerun, or a RerunEnvError.

    Round 50 (shortcut critique S1): the unblob that REA is told to run must report
    the frozen version (`unblob --version` == 26.6.4), `sasquatch` must resolve on
    FIXED_PATH (never on the caller's PATH), node must resolve on FIXED_PATH, and the
    REA package at --pkg65 must be version 6.5.0. Paths, sha256 and versions go
    into the counter receipt."""
    rec = {}
    ver = _first_line([unblob_path, '--version'])
    rec['unblob'] = {'path': unblob_path, 'realpath': os.path.realpath(unblob_path),
                     'sha256': file_sha256(unblob_path), 'version': ver}
    if ver != UNBLOB_VERSION:
        raise RerunEnvError('unblob version %r != frozen %r (%s)'
                            % (ver, UNBLOB_VERSION, unblob_path))
    sas = which_fixed('sasquatch')
    if sas is None:
        raise RerunEnvError('missing-extractor-dependency: sasquatch is not '
                            'on the fixed child PATH %r' % (FIXED_PATH,))
    rec['sasquatch'] = {'path': sas, 'realpath': os.path.realpath(sas),
                        'sha256': file_sha256(sas),
                        'version_line': _first_line([sas, '-version'])}
    node = which_fixed('node')
    if node is None:
        raise RerunEnvError('node is not on the fixed child PATH %r' % (FIXED_PATH,))
    rec['node'] = {'path': node, 'realpath': os.path.realpath(node),
                   'version': _first_line([node, '--version'])}
    entry, version, pj_sha, why = rea_entry(pkg65)
    if entry is None:
        raise RerunEnvError('REA package at --pkg65: %s' % (why,))
    if version != REA_VERSION:
        raise RerunEnvError('REA package version %r != %r' % (version, REA_VERSION))
    rec['rea'] = {'package': os.path.abspath(pkg65), 'entry': entry,
                  'version': version, 'package_json_sha256': pj_sha}
    return rec


def make_real_runner(work, unblob, timeout, pkg65):
    """REA 6.5.0 extract-firmware on the given carrier bytes, fresh outdir.

    Executed as `node <pkg65>/<bin> extract-firmware ...` (round 50: the package
    the evidence-id recompute is bound to, not whatever `npx` resolves). The run
    replays the FROZEN extraction parameters (`rea_parameters` of carriers.json:
    `max_depth`, `max_output_bytes`, `max_output_files`; round 41 replayed the
    committed receipt's own parameters). A receipt produced at `--max-depth 1` is
    `partial` with a truncated published set, so a rerun at REA's default depth 3
    could never match it under a profile that compares `coverage` or
    `published_bytes`; and a rootfs carrier (~13k files) needs the raised budgets
    or REA fails with a staging-entry budget error.

    The child PATH is FIXED_PATH and must resolve `sasquatch` (the extractor for
    every little-endian v4 image: unblob runs `sasquatch -le ...`);
    `sasquatch-v4be` is not required. A PATH that does not resolve it, an unblob
    that is not 26.6.4 or a package that is not 6.5.0 is an unevaluable
    environment (`rerun_env_error`), never a green run and never a silent
    downgrade. The bound toolchain is exposed as `run.toolchain` after the first
    run."""
    unblob_path = unblob or os.path.expanduser('~/.local/bin/unblob')

    def run(carrier_bytes, cid, params=None):
        run.toolchain = toolchain_record(unblob_path, pkg65)
        node = run.toolchain['node']['path']
        entry = run.toolchain['rea']['entry']
        d = os.path.join(work, 'rerun-' + re.sub(r'[^A-Za-z0-9_.-]', '_', str(cid)))
        inp = os.path.join(d, 'carrier.bin')
        outdir = os.path.join(d, 'out')
        os.makedirs(d, exist_ok=False)
        with open(inp, 'wb') as fh:
            fh.write(carrier_bytes)
        env = dict(os.environ)
        env['REA_UNBLOB_COMMAND'] = unblob_path
        env['TMPDIR'] = d
        env['PATH'] = FIXED_PATH
        argv = [node, entry, 'extract-firmware', '--format', 'json',
                '--full-output']
        replayed = {}
        if isinstance(params, dict):
            for flag, key in REPLAY_PARAMS:
                value = params.get(key)
                if isinstance(value, int) and not isinstance(value, bool):
                    argv += [flag, str(value)]
                    replayed[key] = value
        argv += [inp, outdir]
        attempts = 0
        while True:
            attempts += 1
            try:
                p = subprocess.run(argv, cwd=d, capture_output=True, env=env, timeout=timeout)
            except FileNotFoundError as e:
                raise RerunEnvError('rea could not start: %s' % e)
            except subprocess.TimeoutExpired:
                raise RerunEnvError('rea timed out after %ss' % timeout)
            text = p.stdout.decode('utf-8', 'replace')
            try:
                envl = json.loads(text)
            except json.JSONDecodeError:
                raise RerunEnvError('rea stdout is not JSON (exit %d): %r'
                                    % (p.returncode, text[:200]))
            if not isinstance(envl, dict):
                raise RerunEnvError('rea stdout JSON is not an object')
            # round 50: REA's own 120 s provider timeout (FIRMWARE_LIMITS.timeoutMs, not
            # tunable) fires on a loaded host for a ~13k-file rootfs; it is an environment
            # flake, not a verdict, so the SAME run is repeated (fresh outdir) up to
            # MAX_REA_ATTEMPTS times. A real run is still required to succeed.
            err_obj = envl.get('error') if isinstance(envl.get('error'), dict) else {}
            if (envl.get('ok') is not True and err_obj.get('code') == 'provider_timeout'
                    and attempts < MAX_REA_ATTEMPTS):
                shutil.rmtree(outdir, ignore_errors=True)
                continue
            break
        replayed['attempts'] = attempts
        data = envl.get('data')
        if envl.get('ok') is not True or not isinstance(data, dict):
            # keep REA's own error object: a rerun that fails is unevaluable-only
            # when the environment is broken, and the reason must be in the record
            return 'no_data', {'ok': envl.get('ok'), 'exit': p.returncode,
                               'replayed': replayed,
                               'error': envl.get('error'),
                               'stdout_head': text[:300],
                               'stderr': p.stderr.decode('utf-8', 'replace')[:300]}
        return 'ok', data

    run.toolchain = None
    return run


def rederive_oracle(raw, work, tag='carrier'):
    """The regular-file set [(rel, sha256, size)] `unsquashfs` extracts from the bytes.

    Round 50 (shortcut critique S5/S6): the frozen oracle table is re-derived at
    scoring time from the carrier bytes themselves, so a shrunk, extended or
    lane-built table cannot pass. `/usr/bin/unsquashfs` (fixed path, version 4.7.5)
    extracts into a fresh scratch directory (`ORACLE_FLAGS`); symlinks, directories
    and device nodes are not regular files and are left out; the directory is
    removed afterwards. A tool that is missing, is another version, or extracts
    nothing from bytes that parsed is an OracleEnvError (exit 2)."""
    if not (os.path.isfile(UNSQUASHFS) and os.access(UNSQUASHFS, os.X_OK)):
        raise OracleEnvError('%s is not executable' % UNSQUASHFS)
    ver = _first_line([UNSQUASHFS, '-version'])
    if not (isinstance(ver, str) and UNSQUASHFS_VERSION in ver):
        raise OracleEnvError('unsquashfs version line %r lacks %s'
                             % (ver, UNSQUASHFS_VERSION))
    base = tempfile.mkdtemp(prefix='oracle-' + re.sub(r'[^A-Za-z0-9_.-]', '_', str(tag))
                            + '.', dir=work)
    try:
        img = os.path.join(base, 'carrier.bin')
        with open(img, 'wb') as fh:
            fh.write(raw)
        dest = os.path.join(base, 'tree')
        p = subprocess.run([UNSQUASHFS, *ORACLE_FLAGS, '-d', dest, img],
                           capture_output=True, text=True)
        if not os.path.isdir(dest):
            raise OracleEnvError('unsquashfs produced no tree (exit %d): %s'
                                 % (p.returncode, (p.stderr or p.stdout)[:200]))
        # an extraction with restrictive modes must stay readable for the walk
        subprocess.run(['chmod', '-R', 'u+rwX', dest], capture_output=True)
        rows = []
        for dirpath, dirs, names in os.walk(dest):
            for name in names:
                full = os.path.join(dirpath, name)
                if os.path.islink(full) or not os.path.isfile(full):
                    continue
                h = hashlib.sha256()
                size = 0
                with open(full, 'rb') as fh:
                    for blk in iter(lambda: fh.read(1 << 20), b''):
                        h.update(blk)
                        size += len(blk)
                rows.append((os.path.relpath(full, dest).replace(os.sep, '/'),
                             h.hexdigest(), size))
        rows.sort()
        return rows
    finally:
        subprocess.run(['chmod', '-R', 'u+rwX', base], capture_output=True)
        shutil.rmtree(base, ignore_errors=True)


# ------------------------------------------------------------- measurement

def measure(root, rev, freeze, pkg65, rerun=None, target=TARGET,
            expected_ids=IDS, unblob=None, rea_timeout=900, carrier_cache=None,
            rederive=None):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P50-C1',
           'target': target}
    git(root, 'cat-file', '-e', f'{rev}^{{commit}}')
    git(root, 'cat-file', '-e', f'{freeze}^{{commit}}')

    # the counter that is running IS the counter frozen at FREEZE (round 50, S3)
    own_sha = file_sha256(os.path.abspath(__file__))
    frozen_counter = show(root, freeze, COUNTER_PATH)
    res['counter_sha256'] = own_sha
    res['counter_frozen_sha256'] = sha256_bytes(frozen_counter)
    if frozen_counter is None or sha256_bytes(frozen_counter) != own_sha:
        raise CounterNotFrozen(
            'the running counter (%s) is not %s at the freeze (%s)'
            % (own_sha, COUNTER_PATH, res['counter_frozen_sha256']))

    frozen = show(root, freeze, CARRIERS)
    if frozen is None:
        raise Unevaluable('carriers.json absent at freeze')
    try:
        spec = json.loads(frozen)
    except json.JSONDecodeError as e:
        raise Unevaluable('carriers.json at freeze is not JSON: %s' % e)
    if not isinstance(spec, dict):
        raise Unevaluable('carriers.json at freeze is not an object')
    plan_raw = show(root, freeze, GAPRULE)
    if plan_raw is None:
        raise Unevaluable('gap-rule.json absent at freeze')
    try:
        plan_doc = json.loads(plan_raw)
    except json.JSONDecodeError as e:
        raise Unevaluable('gap-rule.json at freeze is not JSON: %s' % e)
    # frozen tables valid at the freeze commit itself: both parse, and every
    # oracle / non-regular table carriers.json lists already exists there
    # (round 50: a table first committed after the freeze is an unfrozen oracle)
    unfrozen = []
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        for key in ('oracle', 'nonregular'):
            v = c.get(key)
            if isinstance(v, str) and v and show(root, freeze, v) is None:
                unfrozen.append(v)
    res['tables_absent_at_freeze'] = sorted(unfrozen)
    res['frozen_tables_valid'] = isinstance(plan_doc, dict) and not unfrozen

    cur = show(root, rev, CARRIERS)
    res['carriers_unchanged'] = cur == frozen
    res['gap_rule_unchanged'] = show(root, rev, GAPRULE) == plan_raw

    drift = frozen_drift(root, freeze, rev, spec)
    res['frozen_path_changed'] = drift
    if drift:
        raise FrozenPathChanged(drift)

    ids, spec_probs = carriers_spec(spec, target, expected_ids)
    res['carriers_spec_problems'] = spec_probs
    profile = spec.get('projection', DEFAULT_PROFILE)
    if profile not in PROFILES:
        profile = DEFAULT_PROFILE             # spec_probs already records the fault
    res['projection_profile'] = profile
    rea_params = spec.get('rea_parameters') if isinstance(
        spec.get('rea_parameters'), dict) else {}
    res['rea_parameters'] = {kk: rea_params.get(kk) for kk in
                             ('max_depth', 'max_output_bytes', 'max_output_files')}
    model, plan_probs = gap_rule_model(plan_raw)
    res['gap_rule_problems'] = plan_probs
    prior, prior_sources = prior_pins(root, freeze, spec)
    res['prior_pins'] = sorted(prior)
    res['prior_pin_sources'] = prior_sources

    work = tempfile.mkdtemp(prefix='c1-counter.', dir=scratch_root())
    try:
        runner = rerun or make_real_runner(work, unblob, rea_timeout, pkg65)
        derive = rederive or (lambda raw, cid: rederive_oracle(raw, work, cid))
        per = {}
        envs = {}
        for c in spec.get('carriers') or []:
            if not isinstance(c, dict):
                continue
            k = c.get('id')
            d = {'id': k}
            pin = (c.get('sha256') or '').lower() or None
            cpath = c.get('path')
            opath = c.get('oracle')
            npath = c.get('nonregular')
            rpath = c.get('receipt') or '%s/%s/after.json' % (AFTERDIR, k)

            if cpath:
                raw = show(root, rev, cpath)
            elif isinstance(c.get('external'), dict) and carrier_cache and pin:
                # external vendor carrier: bytes fetched by fetch-vendor.py; the pin
                # (frozen in carriers.json) is still checked below on these bytes.
                fp = os.path.join(carrier_cache, pin + '.bin')
                raw = open(fp, 'rb').read() if os.path.isfile(fp) else None
            else:
                raw = None
            d['carrier_path'] = cpath
            d['carrier_present'] = raw is not None
            d['carrier_pin_ok'] = (raw is not None and pin is not None
                                   and hashlib.sha256(raw).hexdigest() == pin)
            d['carrier_fresh_ok'] = (pin is not None and pin not in prior)
            d['carrier_fresh_against'] = prior_sources
            d['layout'] = layout_probe(raw)
            d['layout_ok'] = bool(d['layout'].get('ok'))
            d['compression'] = d['layout'].get('compression')
            # carve_ok: the carrier is exactly the filesystem it claims. A carve
            # that runs past bytes_used leaves trailing bytes, unblob then stops
            # the chunk at bytes_used, the chunk is no longer the whole input and
            # the oracle root moves one `<start>-<end>.<handler>_extract` deeper
            # (measured: R41C1Counter artifacts/chunk-naming.json, 'trailing-512').
            ext = c.get('external') if isinstance(c.get('external'), dict) else None
            bu = d['layout'].get('bytes_used')
            size = d['layout'].get('size')
            if ext is not None:
                carve_len = ext.get('length')
                d['carve'] = {'length': carve_len, 'bytes_used': bu, 'size': size}
                d['carve_ok'] = (isinstance(carve_len, int)
                                 and isinstance(bu, int)
                                 and carve_len == bu == size)
            else:
                d['carve'] = {'bytes_used': bu, 'size': size}
                d['carve_ok'] = isinstance(bu, int) and bu == size

            oracle, oerr = parse_oracle(show(root, rev, opath) if opath else None)
            d['oracle_path'] = opath
            d['oracle_error'] = oerr
            d['oracle_files'] = len(oracle)
            d['oracle_ok'] = oerr is None and len(oracle) > 0
            # scoring-time oracle re-derivation: the frozen table must equal what
            # unsquashfs extracts from these bytes, in both directions
            if raw is not None and d['carrier_pin_ok'] and d['oracle_ok']:
                derived = derive(raw, k)
                want_set, got_set = set(oracle), set(derived)
                d['oracle_derived_files'] = len(derived)
                d['oracle_rederived_ok'] = want_set == got_set
                if want_set != got_set:
                    d['oracle_rederived_diff'] = {
                        'frozen_only': sorted(want_set - got_set)[:3],
                        'derived_only': sorted(got_set - want_set)[:3]}
            else:
                d['oracle_rederived_ok'] = False
                d['oracle_rederived_skipped'] = ('carrier_pin_ok' if not d.get(
                    'carrier_pin_ok') else 'oracle_ok' if not d['oracle_ok']
                    else 'carrier_absent')

            nonreg, nerr = parse_nonregular(show(root, rev, npath) if npath else None)
            d['nonregular_path'] = npath
            d['nonregular_error'] = nerr
            d['nonregular_entries'] = len(nonreg)
            d['nonregular_kinds'] = sorted({kind for _, kind, _d in nonreg})
            d['nonregular_ok'] = nerr is None

            raw_receipt = show(root, rev, rpath)
            try:
                env = json.loads(raw_receipt) if raw_receipt else None
            except json.JSONDecodeError:
                env = None
            if not isinstance(env, dict):
                env = None
            d['receipt_path'] = rpath
            d['receipt_digest'] = sha256_bytes(raw_receipt)
            d['receipt_present'] = env is not None

            adds = all_adds(root, rev, rpath) if raw_receipt is not None else None
            d['receipt_adds'] = adds
            d['receipt_first_add'] = adds[-1] if adds else None
            d['receipt_fresh'] = bool(adds) and all(
                a != freeze and is_ancestor(root, freeze, a) for a in adds)

            if env is not None:
                envs[f'{k}/after'] = env
                d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}
                                                 & set(env))
                subj = env.get('subject') or {}
                d['subject_pin_ok'] = ((subj.get('digest') or {}).get('sha256')
                                       if isinstance(subj, dict) else None) == pin
                prov = env.get('provider') or {}
                d['operation_ok'] = (env.get('operation') == 'extract_firmware'
                                     and isinstance(prov, dict) and prov.get('id') == 'unblob')
                d['chunk_handlers'] = chunk_handlers(env)
                d['squashfs_handlers'] = squashfs_chunk_handlers(env)
                # every squashfs-family chunk handler is EXACTLY the frozen one (no
                # prefix test, no default): `squashfs_v4_be`, `squashfs_v3`, ... fail
                d['handler_ok'] = bool(d['squashfs_handlers']) and all(
                    h == HANDLER for h in d['squashfs_handlers'])
                d['chunks_ok'] = not chunk_failed(env)
                root_hint = (c.get('oracle_root')
                             if isinstance(c.get('oracle_root'), str) else None)
                root_value, root_how = subject_root(env, root_hint)
                d['extract_root'] = root_value
                d['extract_root_source'] = root_how
                d['chunk_roots'] = chunk_roots(env, root_hint)
                d['extract_root_confirmed'] = bool(
                    root_value and any(under_root(p, root_value)
                                       for p in receipt_paths(env)))
                files = published(env)
                d['published_files'] = len(files)
                nested = nested_roots(env, root_value)
                d['nested_roots'] = nested
                d['oracle_hits'] = oracle_hits(oracle, files, root_value, nested)
                d['published_rels'] = len(published_rels(files, root_value, nested))
                extra = extra_published(oracle, files, root_value, nested)
                d['extra_published'] = extra[:5]
                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and root_value is not None
                                       and d['oracle_hits'] == d['oracle_files']
                                       and not extra)
                params = env.get('parameters') or {}
                od = params.get('output_directory') if isinstance(params, dict) else None
                d['output_directory'] = od
                diags = diagnostics(env)
                d['diagnostics'] = len(diags)
                d['removals'] = sorted(
                    rel for rel, diag in
                    ((diagnostic_rel(x, root_value, od), x) for x in diags)
                    if rel is not None
                    and diagnostic_typename(diag) == (model.get('removed') or {}
                                                      ).get('diagnostic'))
                ok, why = disposition_check(gaps(env), diags, nonreg, model,
                                            root_value, od)
                d['gaps_ok'] = ok
                d['gaps_note'] = why
                esc = nonregular_published(files, nonreg, root_value)
                d['nonregular_published'] = esc[:5]
                d['nonregular_unpublished_ok'] = (root_value is not None
                                                  and not esc)
                shape_ok, shape_why = path_shape_ok(env)
                d['path_shape_ok'] = shape_ok
                d['path_shape_note'] = shape_why
                d['run_provenance_ok'] = provenance_ok(od)
                # the receipt was made with the frozen extraction parameters
                want_p = {kk: rea_params.get(kk) for kk in
                          ('max_depth', 'max_output_bytes', 'max_output_files')}
                got_p = {kk: (params.get(kk) if isinstance(params, dict) else None)
                         for kk in want_p}
                d['parameters'] = got_p
                d['parameters_ok'] = (all(isinstance(v, int)
                                          and not isinstance(v, bool)
                                          for v in want_p.values())
                                      and got_p == want_p)

                # rerun clause: fresh REA run of the REV carrier bytes, replaying
                # the FROZEN parameters
                if raw is not None and d['carrier_pin_ok']:
                    status, payload = runner(raw, k, want_p)
                    if status != 'ok':
                        perr = payload.get('error') if isinstance(payload, dict) else None
                        if isinstance(perr, dict) and perr.get('code') == 'provider_timeout':
                            # REA's own 120 s deadline on a loaded host: the environment, not
                            # the receipt, failed; never a verdict (exit 2, round 50)
                            raise RerunEnvError(
                                'REA provider_timeout on %s after %s attempt(s); repeat on a quieter host'
                                % (k, (payload.get('replayed') or {}).get('attempts')))
                        d['projection_ok'] = False
                        d['projection_error'] = payload
                    else:
                        eq, keys, detail = projection_diff(
                            projection(env, profile), projection(payload, profile),
                            profile)
                        d['projection_ok'] = eq
                        d['projection_diff'] = keys
                        if not eq:
                            d['projection_detail'] = detail
                else:
                    d['projection_ok'] = False
                    d['projection_skipped'] = ('carrier_pin_ok'
                                               if not d.get('carrier_pin_ok')
                                               else 'carrier_absent')
            per[k] = d

        ev = evidence_ids(root, freeze, pkg65, envs, work)
        matched = 0
        for k, d in per.items():
            key = f'{k}/after'
            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]
                                   and ev[key][0].startswith('ev_'))
            ok = all(d.get(x) is True for x in CLAUSES)
            d['matched'] = bool(ok)
            matched += bool(ok)
        res['rerun_toolchain'] = getattr(runner, 'toolchain', None)
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = matched
        res['evidence_digests'] = {
            k: {'path': v.get('receipt_path'), 'sha256': v.get('receipt_digest')}
            for k, v in per.items() if v.get('receipt_digest')}
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # ---------------------------------------------------------- bindings
    b = {}
    prov = show(root, rev, 'PROVINCE.md')
    prov_text = prov.decode(errors='replace') if prov else ''
    sec = section(prov_text, CORE_HEADING) if prov else None
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        HANDLER_RE.search(cells(r)[0]) and AVM_MARKER_RE.search(r.replace(ENTRY, ''))
        and ENTRY in r
        for r in rows)
    b['province_core_rows_seen'] = [
        cells(r)[0] for r in rows if HANDLER_RE.search(cells(r)[0])]
    # the token is searched with the stem removed: the stem itself spells
    # `avm-le` and would satisfy the token on its own
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and LE_AVM_RE.search(l.replace(STEM, ''))
                             for l in prov_text.splitlines())
    ent = show(root, rev, ENTRY)
    b['entry_present'] = ent is not None
    src_ids = set()
    if ent:
        for line in ent.decode(errors='replace').splitlines():
            if line.startswith('source:'):
                src_ids |= sid_tokens(line)
    b['entry_source_ids'] = sorted(src_ids)
    reg = show(root, rev, 'corpus/SOURCES.md')
    ok_ids = []
    if reg:
        for line in reg.decode(errors='replace').splitlines():
            if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
                continue
            c = cells(line)
            if len(c) != 11:
                continue
            used = c[10]
            if c[0] in src_ids and c[8] in OPENED_DATES and (ENTRY in used or STEM in used):
                ok_ids.append(c[0])
    b['opened_source_rows'] = sorted(ok_ids)
    b['sourced'] = bool(ok_ids)
    readme = show(root, rev, 'corpus/README.md')
    cm = section(readme.decode(errors='replace'), '## Coverage map') if readme else None
    b['coverage_map_row'] = bool(cm) and any(
        STEM in l for l in cm if l.lstrip().startswith('|'))
    b['carriers_spec_ok'] = not spec_probs
    kinds_seen = set()
    for d in (res.get('carriers') or {}).values():
        kinds_seen |= set(d.get('nonregular_kinds') or [])
    uncovered = sorted(kinds_seen - set(model.get('allowed') or {}))
    b['gap_rule_ok'] = not plan_probs and not uncovered
    b['gap_rule_uncovered_kinds'] = uncovered
    b['compression_detail'] = [d.get('compression')
                               for d in (res.get('carriers') or {}).values()]
    b['frozen_tables_valid'] = bool(res.get('frozen_tables_valid'))
    res['bindings'] = b
    res['met_target'] = bool(res['carriers_unchanged'] and res['gap_rule_unchanged']
                             and res['carriers_matched'] == target
                             and all(b[x] is True for x in BINDINGS))
    return res


def failing_lists(res):
    """(per-carrier failing clause names, false binding names) for the receipt."""
    fails = []
    for k, v in (res.get('carriers') or {}).items():
        for x in CLAUSES:
            if v.get(x) is not True:
                fails.append('%s:%s' % (k, x))
    binds = [x for x in BINDINGS if (res.get('bindings') or {}).get(x) is not True]
    return sorted(fails), binds


def main(argv=None):
    global WORK_OVERRIDE
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--pkg65')
    ap.add_argument('--json-out')
    ap.add_argument('--unblob')
    ap.add_argument('--work', help='scratch directory (default '
                    '$HYAKU_SCRATCH/kaidoku-r50/counter)')
    ap.add_argument('--carrier-cache',
                    help='directory holding <sha256>.bin for external vendor carriers '
                         '(filled by tools/round-41/fetch-vendor.py)')
    ap.add_argument('--rea-timeout', type=int, default=900)
    ap.add_argument('--no-rerun', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--selftest-rea', action='store_true')
    ap.add_argument('--dev-image', help='LE AVM member for --selftest-rea')
    ap.add_argument('--verify-receipt', help='exit 0 if the receipt at PATH carries '
                    'a counter_sha256 that describes the counter file it names')
    a = ap.parse_args(argv)
    if a.work:
        WORK_OVERRIDE = os.path.abspath(a.work)
        os.makedirs(WORK_OVERRIDE, exist_ok=True)
    if a.verify_receipt:
        try:
            with open(a.verify_receipt) as fh:
                doc = json.load(fh)
        except (OSError, json.JSONDecodeError) as e:
            print(json.dumps({'verify': a.verify_receipt, 'reason': str(e),
                              'ok': False}, sort_keys=True))
            return 2
        ok, why = receipt_identity_ok(doc)
        print(json.dumps({'verify': a.verify_receipt, 'ok': ok,
                          'counter': doc.get('counter') if isinstance(doc, dict) else None,
                          'counter_sha256': (doc.get('counter_sha256')
                                             if isinstance(doc, dict) else None),
                          'detail': why}, sort_keys=True))
        return 0 if ok else 1
    if a.selftest:
        return selftest(a.pkg65 or find_rea_pkg())
    if a.selftest_rea:
        return selftest_rea(a.pkg65, a.unblob, a.rea_timeout, a.dev_image)
    if a.no_rerun:
        out = {'reason': 'rerun_disabled',
               'detail': 'P50-C1 binds a fresh REA run of each carrier; '
                         '--no-rerun cannot be scored',
               'argv': sys.argv, 'exit_code': 2}
        print(json.dumps({k: out[k] for k in ('reason', 'detail')}, sort_keys=True))
        if a.json_out:
            write_receipt(out, a.json_out)
        return 2
    if not (a.root and a.rev and a.freeze and a.pkg65):
        print('usage: --root --rev --freeze --pkg65 required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.pkg65, unblob=a.unblob,
                      rea_timeout=a.rea_timeout, carrier_cache=a.carrier_cache)
    except Unevaluable as e:
        res = {'unevaluable': str(e), 'reason': e.reason, 'argv': sys.argv,
               'exit_code': 2}
        if isinstance(e, FrozenPathChanged):
            res['frozen_path_changed'] = e.paths
        print(json.dumps({'reason': e.reason, 'detail': str(e),
                          'frozen_path_changed': res.get('frozen_path_changed', [])},
                         sort_keys=True))
        if a.json_out:
            write_receipt(res, a.json_out)
        return 2
    fails, binds = failing_lists(res)
    res['failing'] = fails
    res['bindings_false'] = binds
    res['argv'] = sys.argv
    res['exit_code'] = 0 if res['met_target'] else 1
    print(json.dumps({k: res[k] for k in ('revision', 'freeze', 'carriers_matched',
                                          'target', 'carriers_unchanged',
                                          'gap_rule_unchanged', 'frozen_path_changed',
                                          'bindings', 'failing', 'bindings_false',
                                          'met_target', 'exit_code')},
                     sort_keys=True))
    if a.json_out:
        stamped, ok, why = write_receipt(res, a.json_out)
        if not ok:
            print(json.dumps({'reason': 'receipt_identity_failed', 'detail': why},
                             sort_keys=True), file=sys.stderr)
            return 2
    return res['exit_code']


# ---------------------------------------------------------------- selftest

def find_xpin(here):
    """Locate tools/round-27/xpin-attribute.mjs from a checkout or an artifact dir."""
    for d in [here] + [os.path.dirname(here)] + \
            [os.path.abspath(os.path.join(here, *(['..'] * n))) for n in range(2, 10)]:
        for rel in ('round-27/xpin-attribute.mjs', 'tools/round-27/xpin-attribute.mjs'):
            p = os.path.join(d, rel)
            if os.path.isfile(p):
                return p
    raise SystemExit('xpin-attribute.mjs not found from ' + here)


# The extraction parameters every fixture receipt carries: the frozen
# `rea_parameters` of the fixture carriers.json (the real data run needs the
# raised budgets: REA's default 10000-entry staging budget fails on a rootfs).
FIXTURE_REA_PARAMETERS = {'max_depth': 1, 'max_output_bytes': 536870912,
                          'max_output_files': 100000}


def sb_carrier(compression, tag=b'', *, marker=True, big=False, major=4, minor=0,
               marker_value=None, mkfs_value=None, its=96, dts=128, size=640):
    """A fixture carrier: a coherent SquashFS v4 superblock and filler bytes.

    Not a real filesystem - the layout clause is a superblock test and these
    bytes exercise it exactly. The default is the frozen layout: little-endian
    `hsqs`, v4.0, `compression`, `mkfs_time == bytes_used == size` and table
    starts 96 < 128 <= bytes_used. `marker=False` writes a real timestamp (a
    STANDARD little-endian image); `big=True` writes `sqsh` and every integer
    big-endian (a big-endian image, with or without the marker);
    `marker_value` sets bytes_used (and the marker) to another value;
    `mkfs_value` sets mkfs_time alone."""
    body = bytearray(size)
    order = 'big' if big else 'little'

    def put(off, width, value):
        body[off:off + width] = value.to_bytes(width, order)

    body[0:4] = b'sqsh' if big else b'hsqs'
    used = size if marker_value is None else marker_value
    if mkfs_value is not None:
        mkfs = mkfs_value
    else:
        mkfs = (used & 0xFFFFFFFF) if marker else 1700000000
    put(8, 4, mkfs)
    put(12, 4, 4096)
    put(20, 2, compression)
    put(28, 2, major)
    put(30, 2, minor)
    put(40, 8, used)
    put(64, 8, its)
    put(72, 8, dts)
    if tag:
        body[-len(tag):] = tag
    return bytes(body)


def mk_env(name, pin, files=(), gaps=(), unpub=(), diags=(), chunks=None,
           outdir='/fast/scratch/hyaku/kaidoku-r50/selftest/after',
           subject_name='carrier.sqsh', chunk_dir='firmware.bin_extract',
           operation='extract_firmware', provider='unblob', derivations=None):
    """A receipt-shaped REA envelope (`data` object) for fixture carriers.

    `derivations` defaults to the one edge rea-agents 6.5.0 publishes for a
    whole-file chunk (`$input` -> `$output/<chunk_dir>`, handler
    `squashfs_v4_le`), which is what the counter reads the extract root from.
    `diags` is a list of (typename, rel) or (typename, rel, target)."""
    if chunks is None:
        chunks = [{'input_path': '$input', 'provider_id': '3028394:1',
                   'range': {'offset': 0, 'length': 4096},
                   'handler': HANDLER, 'encrypted': False,
                   'root_file_range': {'offset': 0, 'length': 4096},
                   'extraction_failed': False}]
    if derivations is None:
        derivations = [{'parent_path': '$input',
                        'child_path': '$output/' + chunk_dir,
                        'provider_blob_id': '3028394:1', 'handler': HANDLER,
                        'parent_file_range': {'offset': 0, 'length': 4096}}]
    rel_files = []
    published_bytes = 0
    for rel, sha, size in files:
        published_bytes += size
        rel_files.append({
            'relative_path': '%s/%s' % (chunk_dir, rel),
            'path': '%s/%s/%s' % (outdir, chunk_dir, rel),
            'size': size, 'sha256': sha, 'reported_sha256': sha,
            'mime_type': 'text/plain', 'original_file_range': None,
            'analysis_depth': 1, 'runtime_address': None,
        })
    gap_rows = []
    for kind, rel, deps in gaps:
        gap_rows.append({
            'kind': kind, 'input_path': '$output/%s/%s' % (chunk_dir, rel),
            'relative_path': '%s/%s' % (chunk_dir, rel), 'handler': HANDLER,
            'provider_id': '3028394:1', 'range': None, 'root_file_range': None,
            'dependencies': list(deps), 'continuation_id': 'continuation-fixture',
        })
    unpub_rows = [{'relative_path': '%s/%s' % (chunk_dir, rel), 'kind': kind,
                   'link_target': target} for rel, kind, target in unpub]
    diag_rows = []
    for item in diags:
        if isinstance(item, str):
            typename, rel, target = item, 'x', '/etc/shadow'
        elif len(item) == 2:
            typename, rel = item
            target = '/etc/shadow'
        else:
            typename, rel, target = item
        diag_rows.append({
            'input_path': '$output/' + chunk_dir,
            'report': {'__typename__': typename, 'severity': 'WARNING',
                       'link': '%s/%s/%s' % (outdir, chunk_dir, rel),
                       'target': target}})
    return {
        'analysis_profile': None,
        'authority': 'shipped-artifact',
        'confidence': 'observed',
        'environment': None,
        'evidence_id': 'ev_' + '0' * 64,
        'evidence_links': [],
        'limitations': [],
        'locations': [{'kind': 'file-offset-range', 'start': 0, 'end': 4096}],
        'normalized_result': {
            'chunks': chunks,
            'coverage': 'complete',
            'depth_limited_paths': ['$output/' + chunk_dir],
            'derivations': derivations,
            'diagnostics': diag_rows,
            'engine': {'name': 'unblob', 'version': '26.6.4',
                       'executable_path': '/x/unblob', 'executable_sha256': '0' * 64,
                       'source_revision': None, 'worker_count': 1},
            'extraction_continuations': [],
            'extraction_gaps': gap_rows,
            'files': rel_files,
            'output_directory': outdir,
            'published_bytes': published_bytes,
            'selection': {'offset': 0, 'length': 4096, 'sha256': pin},
            'unpublished_entries': unpub_rows,
        },
        'operation': operation,
        'parameters': {'path': '/x/' + subject_name, 'output_directory': outdir,
                       **FIXTURE_REA_PARAMETERS},
        'predicate_type': 'rea.analysis',
        'provider': {'id': provider, 'name': 'Unblob', 'version': '26.6.4'},
        'raw_result': {},
        'relationship_coverage': None,
        'subject': {'name': subject_name, 'digest': {'sha256': pin},
                    'local_path': '/x/' + subject_name, 'format': 'file',
                    'architecture': None},
    }


def rehost(env, tag, chunk_dir='firmware.bin_extract'):
    """Copy of a receipt as a *second* run of the same bytes would emit it.

    Different absolute paths, different evidence id, and optionally a different
    staged extraction directory name. Every path a receipt normalizes is moved
    with the root (files, gaps, unpublished entries, derivation edges,
    depth-limited task paths, diagnostic links), so the receipt stays internally
    consistent and `subject_root` still derives the same namespace."""
    e = json.loads(json.dumps(env))
    old_od = env['parameters']['output_directory']
    root = '/fast/scratch/hyaku/kaidoku-r50/counter/rerun/%s' % tag
    outdir = root + '/out'
    nr = e['normalized_result']
    old_root = subject_root(e)[0]

    def remap(path):
        p = strip_output(path)
        if not isinstance(p, str) or not p:
            return p
        if old_root:
            if p == old_root:
                return chunk_dir
            if p.startswith(old_root + '/'):
                return chunk_dir + p[len(old_root):]
        return p

    nr['output_directory'] = outdir
    for f in nr.get('files') or []:
        rel = remap(f.get('relative_path'))
        f['relative_path'] = rel
        f['path'] = '%s/%s' % (outdir, rel)
    for g in nr.get('extraction_gaps') or []:
        if g.get('relative_path') is None:
            g['input_path'] = '$output/' + remap(g.get('input_path') or '')
        else:
            rel = remap(g.get('relative_path'))
            g['relative_path'] = rel
            g['input_path'] = '$output/' + rel
        g['continuation_id'] = 'continuation-' + tag
    for u in nr.get('unpublished_entries') or []:
        u['relative_path'] = remap(u.get('relative_path'))
    for d in nr.get('derivations') or []:
        for key in ('parent_path', 'child_path'):
            v = strip_output(d.get(key))
            if isinstance(v, str) and v and v != '$input':
                d[key] = '$output/' + remap(v)
    nr['depth_limited_paths'] = ['$output/' + remap(x)
                                 for x in nr.get('depth_limited_paths') or []]
    for d in nr.get('diagnostics') or []:
        report = d.get('report')
        if isinstance(report, dict):
            link = report.get('link')
            if isinstance(link, str) and link:
                # the link is absolute; keep its tail after the old root
                tail = diagnostic_rel({'report': {'link': link}}, old_root, old_od)
                report['link'] = ('%s/%s/%s' % (outdir, chunk_dir, tail)
                                  if tail is not None else link)
            d['input_path'] = '$output/' + chunk_dir
    e['parameters'] = dict(e['parameters'])
    e['parameters']['path'] = root + '/carrier.bin'
    e['parameters']['output_directory'] = outdir
    e['subject'] = dict(e['subject'])
    e['subject']['name'] = 'carrier.bin'
    e['subject']['local_path'] = root + '/carrier.bin'
    e['evidence_id'] = 'ev_' + hashlib.sha256(
        json.dumps(e, sort_keys=True).encode()).hexdigest()
    return e


def mint_many(work, xpin_path, pkg65, envs):
    paths = []
    for k, env in envs.items():
        p = os.path.join(work, 'mint-%s.json' % k.replace('/', '_'))
        with open(p, 'w') as fh:
            json.dump({'data': env}, fh)
        paths.append((k, p))
    r = subprocess.run(['node', xpin_path, '--pkg65', pkg65, '--pkg67', pkg65]
                       + [p for _, p in paths], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('xpin mint failed: ' + r.stderr.strip())
    lines = [l for l in r.stdout.splitlines() if l]
    if len(lines) != len(paths):
        raise SystemExit('xpin mint line count mismatch')
    out = {}
    for (k, _), line in zip(paths, lines):
        out[k] = line.split('\t')[2]
    return out


def _province(row=True, heading=CORE_HEADING, cell='`squashfs_v4_le`',
              layout='AVM marker', note=True, cited=ENTRY, token='LE AVM'):
    r = f'| {cell} | {layout} | x | `{cited}` |\n' if row else ''
    fn = (f'- {FRONTIER_MARK}, 2026-10-28: the Frontier {token} part is '
          f'superseded by `{STEM}`.\n') if note else ''
    return (f'# P\n\n{heading}\n\n| Surface | Layout | a | Entry |\n|---|---|---|---|\n{r}\n'
            f'## Next\n{fn}\n')


def _entry(sid='S1121'):
    return f'# E\n\nsource: {sid} - x\n'


def _registry(sid='S1121', opened=OPENED_DATES[0], used=ENTRY):
    rows = f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n'
    if sid != 'S112':
        rows += f'| S112 | s | docs | A | s | a | t | mined | {OPENED_DATES[0]} | 180d | {ENTRY} |\n'
    return ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches '
            '| status | opened | recheck | used-by |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|\n' + rows)


def _readme(stem=STEM):
    return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'


def selftest(pkg65):
    here = os.path.dirname(os.path.abspath(__file__))
    sroot = scratch_root()
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    work = tempfile.mkdtemp(prefix='c1-selftest-work.', dir=sroot)

    sha = lambda b: hashlib.sha256(b).hexdigest()
    ids = list(IDS)

    # fixture carriers: the frozen LE AVM-marker layout, xz, four distinct pins
    carriers = {k: sb_carrier(XZ_ID, ('%s-avm' % k).encode()) for k in ids}
    # the frozen rea-pkg pin of the fixture lane, derived from the --pkg65 package
    pkg_root = os.path.abspath(pkg65)
    lock = next((p for p in (
        os.path.join(os.path.dirname(pkg_root), 'package-lock.json'),
        os.path.join(os.path.dirname(os.path.dirname(pkg_root)), 'package-lock.json'))
        if os.path.isfile(p)), None)
    rea_doc = json.dumps({
        'schema': 'selftest', 'name': 'rea-agents', 'version': REA_VERSION,
        'package_json_sha256': file_sha256(os.path.join(pkg_root, 'package.json')),
        'package_lock_sha256': file_sha256(lock) if lock else None})

    def lnk(e, rel):
        """A removal-diagnostic link inside the receipt's own run root."""
        return e['parameters']['output_directory'] + '/firmware.bin_extract/' + rel
    pins = {k: sha(v) for k, v in carriers.items()}
    fsha = lambda i: sha(('f%s' % i).encode())

    # per-carrier fixture data (files, gaps, unpublished, diagnostics)
    spec_data = {
        'g7581': dict(files=[('README.txt', fsha(1), 148), ('config/app.conf', fsha(2), 54)],
                   gaps=[('unpublished-entry', 'usr/share/demo/link-blob', []),
                         ('unpublished-entry', 'usr/share/demo/escape', [])],
                   unpub=[('usr/share/demo/link-blob', 'symlink', '../opt/blob.bin'),
                          ('usr/share/demo/escape', 'symlink', '../../../../etc/shadow')],
                   diags=[],
                   nonreg='usr/share/demo/link-blob\tsymlink\nusr/share/demo/escape\tsymlink\n'),
        'g7582': dict(files=[('var/info.txt', fsha(3), 40)], gaps=[], unpub=[], diags=[],
                   nonreg=''),
        'c6490': dict(files=[('bin/run', fsha(4), 12), ('docs/deep/blob.bin', fsha(5), 33)],
                   gaps=[('unpublished-entry', 'usr/lib/libfoo.so', [])],
                   unpub=[('usr/lib/libfoo.so', 'symlink', '../lib/libfoo.so.1')],
                   diags=[],
                   nonreg='usr/lib/libfoo.so\tsymlink\n'),
        'c6430': dict(files=[('etc/motd', fsha(6), 9)], gaps=[], unpub=[],
                   diags=[('FileMagicMismatch', 'etc/motd')],
                   nonreg='dev/console\tdevice\n'),
    }
    # c6430's device is required: give it a gap
    spec_data['c6430']['gaps'] = [('unpublished-entry', 'dev/console', [])]
    spec_data['c6430']['unpub'] = [('dev/console', 'device', None)]

    def receipt_envs(over=None):
        out = {}
        for k in ids:
            sd = spec_data[k]
            out[k] = mk_env(k.lower() + '.sqsh', pins[k],
                            files=sd['files'], gaps=sd['gaps'],
                            unpub=sd['unpub'], diags=sd['diags'],
                            outdir='/fast/scratch/hyaku/kaidoku-r50/selftest/%s-after' % k)
        for k, fn in (over or {}).items():
            fn(out[k])
        return out

    green_envs = receipt_envs()
    for k, i in mint_many(work, xpin_path, pkg65, green_envs).items():
        green_envs[k]['evidence_id'] = i

    def receipt_path(k):
        return f'{AFTERDIR}/{k}/after.json'

    def receipts(envs):
        return {receipt_path(k): json.dumps(e) for k, e in envs.items()}

    rule = json.dumps({'claim': 'R50-C1',
                       'allowed': {'symlink': ['unpublished-entry'],
                                   'device': ['unpublished-entry']}}, indent=1)

    def spec_json(pin_map=None, drop=None, target=None, receipt_override=None,
                  projection=None, external=None, oracle_root=None,
                  external_drop=None, prior_pins=None, rea=None, omit=()):
        """carriers.json text. `external` (an id, or a set of ids) turns carriers
        into vendor entries (with a member_sha256 block that `external_drop` can
        remove a key from); `rea` replaces the frozen `rea_parameters`; `omit`
        removes top-level keys."""
        pm = pin_map or pins
        ext_ids = {external} if isinstance(external, str) else set(external or ())
        cs = []
        for k in ids:
            if drop and k in drop:
                continue
            c = {'id': k,
                 'sha256': pm[k],
                 'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
                 'nonregular': f'{AFTERDIR}/{k}/nonregular.tsv'}
            if k in ext_ids:
                ext = {'url': 'https://download.avm.de/fritzbox/x/y.image',
                       'image_sha256': 'a' * 64,
                       'member': './var/tmp/filesystem.image',
                       'member_sha256': 'b' * 64,
                       'length': len(carriers[k])}
                for key in (external_drop or ()):
                    ext.pop(key, None)
                c['external'] = ext
            else:
                c['path'] = f'{AFTERDIR}/{k}/carrier.sqsh'
            if oracle_root and k in oracle_root:
                c['oracle_root'] = oracle_root[k]
            if receipt_override and k in receipt_override:
                c['receipt'] = receipt_override[k]
            cs.append(c)
        spec = {'claim': 'R50-C1', 'target': TARGET if target is None else target,
                'projection': DEFAULT_PROFILE if projection is None else projection,
                'rea_parameters': (dict(FIXTURE_REA_PARAMETERS) if rea is None
                                   else rea),
                'carriers': cs}
        if prior_pins is not None:
            spec['prior_pins'] = list(prior_pins)
        for key in omit:
            spec.pop(key, None)
        return json.dumps(spec, indent=1)

    def oracle_tsv(k):
        rows = ''.join(f'{rel}\t{h}\t{size}\n' for rel, h, size in spec_data[k]['files'])
        return rows.encode()

    def frozen_files(blob_map=None, pin_map=None, nonreg_map=None, rule_text=None,
                     oracle_map=None, **over):
        bm = blob_map or carriers
        pm = pin_map or pins
        nm = nonreg_map if nonreg_map is not None else {
            k: spec_data[k]['nonreg'] for k in ids}
        om = oracle_map if oracle_map is not None else {k: oracle_tsv(k) for k in ids}
        f = {XPIN: xpin,
             CARRIERS: spec_json(pin_map=pm),
             GAPRULE: (rule_text if rule_text is not None else rule).encode(),
             'plans/round-50-claims.md': b'# plan\n',
             'tools/round-50/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
             'tools/round-50/rea-pkg.json': rea_doc,
             'tools/round-41/sqfs-list.py': b'# stand-in second reader\n',
             'tools/round-41/fetch-vendor.py': b'# stand-in fetcher\n',
             'PROVINCE.md': _province(),
             ENTRY: _entry(),
             'corpus/SOURCES.md': _registry(),
             'corpus/README.md': _readme()}
        for k in ids:
            f[f'{AFTERDIR}/{k}/carrier.sqsh'] = bm[k]
            f[f'{AFTERDIR}/{k}/oracle.tsv'] = om[k]
            f[f'{AFTERDIR}/{k}/nonregular.tsv'] = nm[k].encode()
        f.update(over)
        return f

    def build(blob_over=None, env_over=None, receipt_over=None, nonreg_over=None,
              oracle_over=None, rule_text=None, spec_text=None):
        """A pin-consistent (frozen files, receipts) pair for one variant."""
        bm = dict(carriers)
        bm.update(blob_over or {})
        pm = {k: sha(bm[k]) for k in ids}
        nm = {k: spec_data[k]['nonreg'] for k in ids}
        nm.update(nonreg_over or {})
        om = {k: oracle_tsv(k) for k in ids}
        om.update(oracle_over or {})
        envs = receipt_envs(over=env_over)   # applies env_over exactly once
        for k in ids:
            if bm[k] != carriers[k]:
                envs[k]['subject']['digest']['sha256'] = pm[k]
                envs[k]['normalized_result']['selection']['sha256'] = pm[k]
        for k, i in mint_many(work, xpin_path, pkg65,
                              {k: envs[k] for k in ids}).items():
            envs[k]['evidence_id'] = i
        r = receipts(envs)
        for p, content in (receipt_over or {}).items():
            if content is None:
                r.pop(p, None)
            else:
                r[p] = content
        frozen_map = frozen_files(blob_map=bm, pin_map=pm, nonreg_map=nm,
                                  oracle_map=om, rule_text=rule_text,
                                  **(over_spec(spec_text)))
        return frozen_map, r

    def over_spec(spec_text):
        return {CARRIERS: spec_text} if spec_text is not None else {}

    def mutant(k, fn, remint=True):
        e = json.loads(json.dumps(green_envs[k]))
        fn(e)
        if remint:
            e['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': e})['m']
        envs = dict(green_envs)
        envs[k] = e
        return receipts(envs)

    # --- simulated REA runner (selftest only) -----------------------------
    sim_envs = receipt_envs()

    def sim_runner(carrier_bytes, cid, params=None):
        """What a real run of these bytes would emit, modelled from the fixture
        data: the pristine receipt for that carrier with the run-varying parts
        replaced (paths, chunk dir, evidence id) and the real subject pin."""
        pin = sha(carrier_bytes)
        base = sim_envs.get(cid)
        if base is None:
            return 'no_data', {'ok': False, 'exit': 1, 'reason': 'fixture has no run'}
        base = json.loads(json.dumps(base))
        base['subject']['digest']['sha256'] = pin
        base['normalized_result']['selection']['sha256'] = pin
        return 'ok', rehost(base, 'selftest-' + str(cid))

    def boom_runner(carrier_bytes, cid, params=None):
        return 'no_data', {'ok': False, 'exit': 1,
                          'stderr': 'ExtractCommandFailedReport'}

    def env_boom_runner(carrier_bytes, cid, params=None):
        raise RerunEnvError('npx not on PATH')

    def mk_same_runner(envs):
        """A real run whose output is the given envelope (projection-equal by
        construction): used to isolate a rule clause from the rerun clause."""
        def run(carrier_bytes, cid, params=None):
            e = json.loads(json.dumps(envs[cid]))
            e['subject']['digest']['sha256'] = sha(carrier_bytes)
            e['normalized_result']['selection']['sha256'] = sha(carrier_bytes)
            return 'ok', rehost(e, 'selftest-same-' + str(cid))
        return run

    cases = []

    def lane_rows(lane, cid):
        """What the simulated unsquashfs re-derivation returns by default: the
        frozen table of that lane (so the other cases isolate their own clause);
        the dedicated cases pass `rederive=` to model a table that disagrees."""
        rows, _err = parse_oracle(open(os.path.join(lane, AFTERDIR, cid,
                                                    'oracle.tsv'), 'rb').read())
        return rows

    def add(name, steps, freeze_index, want, reason=None, want_fail=None,
            runner=sim_runner, cache=None, rederive=None):
        cases.append({'name': name, 'steps': steps, 'freeze': freeze_index,
                      'want': want, 'reason': reason, 'want_fail': want_fail,
                      'runner': runner, 'cache': cache, 'rederive': rederive})

    green_frozen, green_receipts = build()
    frozen = frozen_files()
    good = receipts(green_envs)

    add('green (4 AVM carriers, fresh receipts, docs)', [green_frozen, green_receipts],
        0, 0)
    add('do-nothing (freeze files only)', [frozen], 0, 1, want_fail='receipt_present')
    add('receipt missing (g7582)',
        [frozen, {k: v for k, v in good.items() if '/g7582/' not in k}], 0, 1,
        want_fail='receipt_present')
    add('receipt added at freeze', [{**frozen, **good}], 0, 1, want_fail='receipt_fresh')
    add('receipt added before freeze', [frozen, good, {}, {}], 2, 1,
        want_fail='receipt_fresh')

    # ---- R39-CL5: fabrications that differ from a real run in the projection
    def fabricate(k, *, files=None, gaps=None, diags=None, chunk_handler=None,
                  drop_diag=False):
        sd = spec_data[k]
        e = mk_env('carrier.sqsh', pins[k],
                   files=files if files is not None else sd['files'],
                   gaps=gaps if gaps is not None else sd['gaps'],
                   unpub=sd['unpub'],
                   diags=[] if drop_diag else (diags if diags is not None else sd['diags']))
        if chunk_handler is not None:
            e['normalized_result']['chunks'][0]['handler'] = chunk_handler
        return e

    def relabel(envs_map, k, env):
        envs = dict(green_envs)
        envs[k] = env
        env['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': env})['m']
        return receipts(envs)

    oracle_only = fabricate('g7581', diags=[])
    # what a forger holding only the oracle tables cannot know: unblob's chunk
    # geometry for the real bytes (here: a guessed chunk length)
    oracle_only['normalized_result']['chunks'][0]['range'] = {'offset': 0, 'length': 639}
    add('oracle-only fabrication with re-minted evidence id',
        [frozen, relabel(green_envs, 'g7581', oracle_only)], 0, 1,
        want_fail='projection_ok')
    one_file_off = fabricate('g7582', files=[('var/info.txt', fsha(99), 40)])
    add('fabrication differing only in one published sha256',
        [frozen, relabel(green_envs, 'g7582', one_file_off)], 0, 1,
        want_fail='projection_ok')
    extra_gap = fabricate('c6490', gaps=[('unpublished-entry', 'usr/lib/libfoo.so', []),
                                      ('extractor-failure', 'bin/run', ['xz'])])
    add('fabrication differing only in an extra gap',
        [frozen, relabel(green_envs, 'c6490', extra_gap)], 0, 1, want_fail='gaps_ok')
    diags_dropped = fabricate('c6430', drop_diag=True)
    add('fabrication differing only in the diagnostics multiset',
        [frozen, relabel(green_envs, 'c6430', diags_dropped)], 0, 1,
        want_fail='projection_ok')
    add('rerun yields no evidence object (REA ok=false)',
        [frozen, good], 0, 1, want_fail='projection_ok', runner=boom_runner)
    add('rerun environment error (no npx) is unevaluable, never met',
        [frozen, good], 0, 2, 'rerun_env_error', runner=env_boom_runner)

    def timeout_runner(carrier_bytes, cid, params=None):
        return 'no_data', {'ok': False, 'exit': 1, 'replayed': {'attempts': 3},
                           'error': {'code': 'provider_timeout', 'retryable': True}}
    add('rerun hits REA provider_timeout (3 attempts) is unevaluable, never a projection verdict',
        [frozen, good], 0, 2, 'rerun_env_error', runner=timeout_runner)
    add('subject digest names another carrier',
        [frozen, mutant('g7581', lambda e: e['subject']['digest'].__setitem__(
            'sha256', '2' * 64))], 0, 1, want_fail='subject_pin_ok')

    # ---- carrier layout controls: the frozen layout is little-endian `hsqs`,
    # v4.0, compression id 4, `mkfs_time == bytes_used` (the AVM marker).
    spec_probes = []

    def layout_case(name, blob, reason_text):
        lf, lr = build(blob_over={'g7581': blob})
        add(name, [lf, lr], 0, 1, want_fail='layout_ok')
        p = layout_probe(blob)
        spec_probes.append({'desc': 'layout probe: ' + name, 'ok': bool(p.get('ok')),
                            'problems': [p.get('reason') or ''],
                            'want_ok': False, 'want_text': reason_text})

    # CTL-C1-4 shape: a STANDARD little-endian image (real timestamp in mkfs_time)
    layout_case('standard-LE carrier (mkfs_time is a timestamp, no AVM marker)',
                sb_carrier(XZ_ID, b'g7581-std', marker=False), 'AVM marker absent')
    layout_case('marker off by one (mkfs_time == bytes_used + 1)',
                sb_carrier(XZ_ID, b'g7581-off', mkfs_value=641), 'AVM marker absent')
    # the round-41 carriers' shape: a big-endian image carrying the marker
    layout_case('big-endian AVM-marker image (sqsh) is not the little-endian layout',
                sb_carrier(XZ_ID, b'g7581-be', big=True), 'not little-endian hsqs')
    layout_case('standard big-endian image (sqsh, no marker)',
                sb_carrier(XZ_ID, b'g7581-bestd', big=True, marker=False),
                'not little-endian hsqs')
    hybrid = b'hsqs' + sb_carrier(XZ_ID, b'g7581-hyb', big=True)[4:]
    layout_case('hsqs magic over big-endian fields is not a little-endian image',
                hybrid, 'version')
    layout_case('compression id 1 (gzip) is not the frozen xz',
                sb_carrier(1, b'g7581-gz'), 'compression id 1')
    layout_case('compression id 2 (lzma; round 41 counted it as xz)',
                sb_carrier(2, b'g7581-lzma'), 'compression id 2')
    layout_case('compression id 6 (zstd)', sb_carrier(6, b'g7581-zstd'),
                'compression id 6')
    layout_case('squashfs 3.0 major', sb_carrier(XZ_ID, b'g7581-v3', major=3),
                'version 3.0')
    layout_case('squashfs 4.1 minor', sb_carrier(XZ_ID, b'g7581-v41', minor=1),
                'version 4.1')
    layout_case('bytes_used beyond the file',
                sb_carrier(XZ_ID, b'g7581-used', marker_value=0xFFFFFFF0),
                'bytes_used')
    layout_case('inode table after the directory table',
                sb_carrier(XZ_ID, b'g7581-order', its=128, dts=96),
                'in order')
    layout_case('directory table past bytes_used',
                sb_carrier(XZ_ID, b'g7581-dts', dts=639, marker_value=600),
                'in order')
    layout_case('inode table at offset 0', sb_carrier(XZ_ID, b'g7581-its0', its=0),
                'in order')
    layout_case('shorter than a superblock', sb_carrier(XZ_ID, b'g7581-short')[:64],
                'shorter than a 96-byte superblock')
    spec_probes.append({
        'desc': 'layout probe: the frozen layout is accepted',
        'ok': bool(layout_probe(carriers['g7581']).get('ok')),
        'problems': [layout_probe(carriers['g7581']).get('reason') or ''],
        'want_ok': True, 'want_text': None})

    # CTL-C1-4: a STANDARD little-endian carrier planted in a carrier slot under the
    # genuine pin. The marker adds no evidence beyond the pin (it is a constant of
    # the pinned bytes), so the case is red on carrier_pin_ok AND on layout_ok.
    plant = sb_carrier(XZ_ID, b'g7581-plant', marker=False)
    plant_frozen = frozen_files(blob_map={**carriers, 'g7581': plant}, pin_map=pins)
    add('CTL-C1-4: a standard LE carrier planted under the genuine pin (carrier_pin_ok)',
        [plant_frozen, good], 0, 1, want_fail='carrier_pin_ok')
    add('CTL-C1-4: a standard LE carrier planted under the genuine pin (layout_ok)',
        [plant_frozen, good], 0, 1, want_fail='layout_ok')

    # ---- missing / malformed frozen inputs (absent at the freeze itself)
    no_carrier = {**frozen, f'{AFTERDIR}/g7582/carrier.sqsh': None}
    add('carrier listed but never committed', [no_carrier, good], 0, 1,
        want_fail='carrier_present')
    bad_oracle = {**frozen, f'{AFTERDIR}/g7581/oracle.tsv': b'not-a-digest\n'}
    add('malformed oracle row', [bad_oracle, good], 0, 1, want_fail='oracle_ok')
    bad_nonreg = {**frozen, f'{AFTERDIR}/c6490/nonregular.tsv': b'usr/lib/libfoo.so\n'}
    add('malformed nonregular row', [bad_nonreg, good], 0, 1,
        want_fail='nonregular_ok')

    # ---- receipt clause controls
    add('wrong operation (extract_filesystem)',
        [frozen, mutant('g7581', lambda e: e.__setitem__('operation', 'extract_filesystem'))],
        0, 1, want_fail='operation_ok')
    add('provider is not unblob',
        [frozen, mutant('g7582', lambda e: e['provider'].__setitem__('id', 'binwalk'))],
        0, 1, want_fail='operation_ok')
    add('failed chunk',
        [frozen, mutant('c6490', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))], 0, 1,
        want_fail='chunks_ok')
    add('chunk handler is the BE handler (squashfs_v4_be)',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v4_be')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('chunk handler is squashfs_v3',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v3')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('chunk handler is the bare prefix squashfs_v4',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v4')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('one LE chunk and one BE chunk: every squashfs handler must be the frozen one',
        [frozen, mutant('c6430', lambda e: e['normalized_result']['chunks'].append(
            {'input_path': '$input', 'provider_id': 'p9',
             'range': {'offset': 4096, 'length': 100}, 'handler': 'squashfs_v4_be',
             'encrypted': False,
             'root_file_range': {'offset': 4096, 'length': 100},
             'extraction_failed': False}))],
        0, 1, want_fail='handler_ok')
    add('no squashfs chunk at all (padding only)',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'padding')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('disallowed gap kind on a symlink entry',
        [frozen, mutant('g7581', lambda e: e['normalized_result']['extraction_gaps'][0]
                        .__setitem__('kind', 'extractor-failure'))], 0, 1,
        want_fail='gaps_ok')
    add('gap on a path that is not a non-regular entry',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['extraction_gaps'].append({
            'kind': 'unpublished-entry', 'relative_path': 'firmware.bin_extract/var/ghost',
            'dependencies': []}))], 0, 1, want_fail='gaps_ok')
    add('required gap missing (symlink materialised)',
        [frozen, mutant('c6490', lambda e: (
            e['normalized_result']['extraction_gaps'].pop(),
            e['normalized_result']['unpublished_entries'].pop(),
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/usr/lib/libfoo.so',
                'path': '/x/usr/lib/libfoo.so', 'size': 3, 'sha256': 'f' * 64})))],
        0, 1, want_fail='gaps_ok')
    add('escaping symlink published as a regular file',
        [frozen, mutant('g7581', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/usr/share/demo/escape',
            'path': '/x/escape', 'size': 3, 'sha256': 'e' * 64}))], 0, 1,
        want_fail='nonregular_unpublished_ok')
    add('oracle file missing from the published set',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].pop())], 0, 1,
        want_fail='oracle_hits_ok')
    add('foreign scratch provenance (/kaidoku-r39/)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r39/l1/K1-after'))],
        0, 1, want_fail='run_provenance_ok')
    add('provenance path climbs out with ..',
        [frozen, mutant('g7582', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r50/../kaidoku-r39/x'))],
        0, 1, want_fail='run_provenance_ok')
    add('evidence id stale after an edit',
        [frozen, mutant('c6430', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/extra.txt', 'path': '/x/extra.txt',
            'size': 1, 'sha256': 'd' * 64}), remint=False)], 0, 1,
        want_fail='evidence_id_ok')
    # ---- round-50 hardening cases (carried from round 49 / new in the port)
    add('an extra regular file published under the extract root',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/var/extra.txt',
            'path': '/x/extra.txt', 'size': 5, 'sha256': 'd' * 64}))], 0, 1,
        want_fail='oracle_hits_ok')
    add('a published file with the oracle sha256 but another size',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'][0]
                        .__setitem__('size', 41))], 0, 1, want_fail='oracle_hits_ok')
    add('oracle table row without the size column',
        [{**frozen, f'{AFTERDIR}/g7581/oracle.tsv':
          ''.join(f'{rel}\t{h}\n' for rel, h, _s in spec_data['g7581']['files']).encode()},
         good], 0, 1, want_fail='oracle_ok')
    add('oracle table row with a non-numeric size',
        [{**frozen, f'{AFTERDIR}/g7581/oracle.tsv':
          ''.join(f'{rel}\t{h}\tbig\n' for rel, h, _s in
                  spec_data['g7581']['files']).encode()}, good], 0, 1,
        want_fail='oracle_ok')
    add('oracle table row with a .. component',
        [{**frozen, f'{AFTERDIR}/g7582/oracle.tsv':
          b'../etc/x\t' + fsha(3).encode() + b'\t40\n'}, good], 0, 1,
        want_fail='oracle_ok')
    add('receipt path with a .. component',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/../etc/x', 'path': '/x/etc/x',
            'size': 5, 'sha256': 'd' * 64}))], 0, 1, want_fail='path_shape_ok')
    add('a score receipt (counter_sha256) committed as the after-receipt',
        [frozen, mutant('c6490', lambda e: e.__setitem__('counter_sha256', '0' * 64))],
        0, 1, want_fail='evidence_envelope_ok')
    add('a score receipt (exit_code) committed as the after-receipt',
        [frozen, mutant('c6490', lambda e: e.__setitem__('exit_code', 0))],
        0, 1, want_fail='evidence_envelope_ok')
    add('provenance by substring only (/tmp/.../kaidoku-r50/...)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/tmp/fast/scratch/hyaku/kaidoku-r50/x'))],
        0, 1, want_fail='run_provenance_ok')
    add('provenance names the previous round scratch (kaidoku-r41)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r41/run-V4/extract'))],
        0, 1, want_fail='run_provenance_ok')
    add('provenance is a relative path',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', 'fast/scratch/hyaku/kaidoku-r50/x'))],
        0, 1, want_fail='run_provenance_ok')
    add('receipt made at max_depth 3 (the claim freezes depth 1)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__('max_depth', 3))],
        0, 1, want_fail='parameters_ok')
    add('receipt made under a smaller output budget than the frozen one',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'max_output_files', 10000))], 0, 1, want_fail='parameters_ok')
    add('receipt without recorded parameters',
        [frozen, mutant('g7581', lambda e: e['parameters'].pop('max_output_bytes'))],
        0, 1, want_fail='parameters_ok')
    add('missing-extractor-dependency gap (sasquatch absent from the child PATH)',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['extraction_gaps']
                        .append({'kind': 'missing-extractor-dependency',
                                 'input_path': '$output/firmware.bin_extract',
                                 'relative_path': None, 'handler': HANDLER,
                                 'dependencies': ['sasquatch'],
                                 'continuation_id': 'continuation-dep'}))],
        0, 1, want_fail='gaps_ok')
    add('a failed chunk reported by REA when sasquatch is absent',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))],
        0, 1, want_fail='chunks_ok')

    # ---- the rerun executes the REA package at --pkg65 (no npx) and binds its toolchain
    stubdir = os.path.join(work, 'stubs')
    os.makedirs(stubdir, exist_ok=True)

    def stub_pkg(version=REA_VERSION, bin_entry='scripts/rea.mjs', name='rea'):
        """A stand-in REA package whose CLI prints its argv/env as an evidence object."""
        root_ = os.path.join(stubdir, 'pkg-' + name)
        os.makedirs(os.path.join(root_, 'scripts'), exist_ok=True)
        doc = {'name': 'rea-agents', 'version': version, 'type': 'module'}
        if bin_entry:
            doc['bin'] = {'rea-agents': bin_entry}
        with open(os.path.join(root_, 'package.json'), 'w') as fh:
            json.dump(doc, fh)
        with open(os.path.join(root_, 'scripts', 'rea.mjs'), 'w') as fh:
            fh.write('console.log(JSON.stringify({ok: true, data: {stub: true, '
                     'argv: process.argv.slice(2), unblob: process.env.REA_UNBLOB_COMMAND, '
                     'path: process.env.PATH, tmpdir: process.env.TMPDIR}}));\n')
        return root_

    def stub_unblob(version):
        pth = os.path.join(stubdir, 'unblob-' + version)
        with open(pth, 'w') as fh:
            fh.write('#!/bin/sh\necho %s\n' % version)
        os.chmod(pth, 0o755)
        return pth

    def runner_probe(desc, unblob, pkg, want_ok, want_text=None, cid=None, check=None):
        rn = make_real_runner(work, unblob, 30, pkg)
        try:
            status, data = rn(b'carrier', cid or ('probe-' + str(len(spec_probes))),
                              dict(FIXTURE_REA_PARAMETERS))
            ok = status == 'ok' and (check is None or check(data, rn.toolchain))
            problems = [] if ok else ['ran but the check failed: %r' % (data,)]
        except RerunEnvError as e:
            ok, problems = False, [str(e)]
        spec_probes.append({'desc': 'real runner: ' + desc, 'ok': ok,
                            'problems': problems, 'want_ok': want_ok,
                            'want_text': want_text})

    def argv_ok(data, tc):
        a = data['argv']
        return (data.get('stub') is True and a[0] == 'extract-firmware'
                and a[a.index('--max-depth') + 1] == '1'
                and a[a.index('--max-output-bytes') + 1] == '536870912'
                and a[a.index('--max-output-files') + 1] == '100000'
                and data['path'] == FIXED_PATH
                and data['unblob'] == stub_unblob('26.6.4')
                and tc['rea']['entry'].startswith(stub_pkg())
                and tc['unblob']['version'] == UNBLOB_VERSION
                and tc['sasquatch']['sha256'] and tc['sasquatch']['path']
                and tc['node']['path'] and 'npx' not in ' '.join(a))

    runner_probe('node executes the package CLI at --pkg65 (no npx), frozen flags, '
                 'FIXED_PATH, toolchain recorded', stub_unblob('26.6.4'), stub_pkg(),
                 True, check=argv_ok)
    runner_probe('unblob that is not 26.6.4 is refused', stub_unblob('26.6.3'),
                 stub_pkg(), False, 'unblob version')
    runner_probe('a package that is not 6.5.0 is refused', stub_unblob('26.6.4'),
                 stub_pkg(version='6.4.0', name='old'), False, 'REA package version')
    runner_probe('a package without a bin entry is refused', stub_unblob('26.6.4'),
                 stub_pkg(bin_entry=None, name='nobin'), False, 'no rea-agents bin')
    runner_probe('a package whose bin entry is missing is refused',
                 stub_unblob('26.6.4'), stub_pkg(bin_entry='scripts/gone.mjs',
                                                 name='gone'), False, 'is not a file')

    # a shim `sasquatch` first on the CALLER's PATH must not be what the child gets
    shim = os.path.join(stubdir, 'shim')
    os.makedirs(shim, exist_ok=True)
    with open(os.path.join(shim, 'sasquatch'), 'w') as fh:
        fh.write('#!/bin/sh\necho shim\n')
    os.chmod(os.path.join(shim, 'sasquatch'), 0o755)
    saved_path = os.environ.get('PATH', '')
    os.environ['PATH'] = shim + ':' + saved_path
    try:
        runner_probe('a shim sasquatch on the caller PATH is not resolved', stub_unblob('26.6.4'),
                     stub_pkg(), True, cid='probe-shim',
                     check=lambda data, tc: (
                         not tc['sasquatch']['path'].startswith(shim)
                         and os.path.dirname(tc['sasquatch']['path']) in FIXED_PATH.split(':')
                         and data['path'] == FIXED_PATH and shim not in data['path']))
    finally:
        os.environ['PATH'] = saved_path

    # ---- the running counter is the frozen counter (round 50, S3)
    add('the running counter is not the counter frozen at the freeze',
        [{**frozen, 'tools/round-50/c1-counter.py': b'# some other counter\n'}, good],
        0, 2, 'counter_not_frozen')
    add('no counter at the freeze',
        [{**frozen, 'tools/round-50/c1-counter.py': None}, good], 0, 2,
        'counter_not_frozen')

    # ---- receipt freshness reads the FULL history (round 50, S4)
    fh_good = good
    add('a receipt added pre-freeze on a side branch and re-added after the freeze, '
        'merged: not fresh',
        [{'base.txt': b'b\n'},
         {'__ops__': [('git', 'checkout', '-q', '-b', 'side'), ('write', fh_good),
                      ('commit', 'P1'), ('git', 'checkout', '-q', '-')]},
         frozen, fh_good, {'__ops__': [('git', 'merge', '--no-ff', '-q', '-m', 'M',
                                        'side')]}],
        2, 1, want_fail='receipt_fresh')
    add('the same history with the receipt added only after the freeze is fresh',
        [{'base.txt': b'b\n'},
         {'__ops__': [('git', 'checkout', '-q', '-b', 'side'),
                      ('write', {'side.txt': b's\n'}), ('commit', 'S1'),
                      ('git', 'checkout', '-q', '-')]},
         frozen, fh_good, {'__ops__': [('git', 'merge', '--no-ff', '-q', '-m', 'M',
                                        'side')]}],
        2, 0)

    # ---- the oracle is re-derived at scoring time (round 50, S5/S6)
    def rows_of(k):
        return sorted(spec_data[k]['files'])

    def extra_row(raw, cid):
        return rows_of(cid) + ([('usr/hidden.bin', fsha(77), 5)] if cid == 'g7581' else [])

    def short_rows(raw, cid):
        return rows_of(cid)[:-1] if cid == 'g7581' else rows_of(cid)

    def wrong_sha(raw, cid):
        rows = rows_of(cid)
        return ([(rows[0][0], fsha(78), rows[0][2])] + rows[1:]) if cid == 'g7581' else rows

    def wrong_size(raw, cid):
        rows = rows_of(cid)
        return ([(rows[0][0], rows[0][1], rows[0][2] + 1)] + rows[1:]) if cid == 'g7581' else rows

    def nothing(raw, cid):
        return []

    def exact_rows(raw, cid):
        return rows_of(cid)

    def no_unsquashfs(raw, cid):
        raise OracleEnvError('%s is not executable' % UNSQUASHFS)

    add('oracle re-derivation equal to the frozen tables (green)', [frozen, good], 0, 0,
        rederive=exact_rows)
    add('frozen oracle table shrunk: the carrier holds a file the table omits',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=extra_row)
    add('frozen oracle table extended: a row the carrier does not hold',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=short_rows)
    add('frozen oracle row with another sha256 than the carrier holds',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=wrong_sha)
    add('frozen oracle row with another size than the carrier holds',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=wrong_size)
    add('the carrier derives nothing while the table lists files',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=nothing)
    add('unsquashfs cannot run: unevaluable, never green', [frozen, good], 0, 2,
        'oracle_env_error', rederive=no_unsquashfs)

    # the real re-derivation (no simulation): a lane-built LE image through the
    # host unsquashfs equals the tree it was built from, and a doctored table differs
    probe_work = os.path.join(work, 'oracle-probe')
    os.makedirs(probe_work, exist_ok=True)
    img, img_why = lane_le_avm_image(probe_work)
    if img is None:
        spec_probes.append({'desc': 'real unsquashfs re-derivation: lane image',
                            'ok': False, 'problems': [img_why], 'want_ok': True,
                            'want_text': None})
    else:
        built = []
        for dp, _dn, fns in os.walk(os.path.join(probe_work, 'src')):
            for fn in fns:
                full = os.path.join(dp, fn)
                if os.path.isfile(full) and not os.path.islink(full):
                    data = open(full, 'rb').read()
                    built.append((os.path.relpath(full, os.path.join(probe_work, 'src')),
                                  sha(data), len(data)))
        built.sort()
        got = rederive_oracle(img, probe_work, 'probe')
        spec_probes.append({'desc': 'real unsquashfs re-derivation equals the built tree',
                            'ok': got == built, 'problems': [repr(got[:2])],
                            'want_ok': True, 'want_text': None})
        spec_probes.append({'desc': 'real unsquashfs re-derivation differs from a '
                                    'doctored table', 'ok': got == built[:-1],
                            'problems': [], 'want_ok': False, 'want_text': None})
        spec_probes.append({'desc': 'real unsquashfs re-derivation leaves no scratch tree',
                            'ok': not [n for n in os.listdir(probe_work)
                                       if n.startswith('oracle-')],
                            'problems': [], 'want_ok': True, 'want_text': None})
    for what, attr, value, text in (
            ('a missing tool', 'UNSQUASHFS', '/nonexistent/unsquashfs', 'not executable'),
            ('another version', 'UNSQUASHFS_VERSION', '9.9.9', 'lacks 9.9.9')):
        saved_attr = globals()[attr]
        globals()[attr] = value
        try:
            try:
                rederive_oracle(b'x', probe_work, 'env')
                res_txt = 'ran'
            except OracleEnvError as e:
                res_txt = str(e)
        finally:
            globals()[attr] = saved_attr
        spec_probes.append({'desc': 'real unsquashfs re-derivation: ' + what,
                            'ok': False, 'problems': [res_txt], 'want_ok': False,
                            'want_text': text})

    # ---- the real runner refuses a child PATH that does not resolve sasquatch
    def runner_env_probe():
        global FIXED_PATH
        saved = FIXED_PATH
        empty = tempfile.mkdtemp(prefix='c1-emptypath.', dir=sroot)
        FIXED_PATH = empty
        try:
            try:
                make_real_runner(work, stub_unblob('26.6.4'), 5, stub_pkg())(
                    b'x', 'probe-nosas', dict(FIXTURE_REA_PARAMETERS))
                return 'ran'
            except RerunEnvError as e:
                return str(e)
        finally:
            FIXED_PATH = saved
            shutil.rmtree(empty, ignore_errors=True)

    env_probe = runner_env_probe()
    spec_probes.append({'desc': 'real runner: sasquatch not on the child PATH',
                        'ok': False, 'problems': [env_probe], 'want_ok': False,
                        'want_text': 'missing-extractor-dependency'})

    # ---- external vendor carriers read through --carrier-cache (the real shape)
    cache_ok = tempfile.mkdtemp(prefix='c1-cache.', dir=sroot)
    cache_empty = tempfile.mkdtemp(prefix='c1-cache-empty.', dir=sroot)
    cache_bad = tempfile.mkdtemp(prefix='c1-cache-bad.', dir=sroot)
    for k in ids:
        with open(os.path.join(cache_ok, pins[k] + '.bin'), 'wb') as fh:
            fh.write(carriers[k])
        with open(os.path.join(cache_bad, pins[k] + '.bin'), 'wb') as fh:
            fh.write(carriers[k] + b'\x00')
    ext_spec = spec_json(external=set(ids))
    ext_frozen, ext_recs = build(spec_text=ext_spec)
    add('four external carriers, bytes from --carrier-cache (green)',
        [ext_frozen, ext_recs], 0, 0, cache=cache_ok)
    add('four external carriers, empty cache', [ext_frozen, ext_recs], 0, 1,
        want_fail='carrier_present', cache=cache_empty)
    add('four external carriers, no --carrier-cache', [ext_frozen, ext_recs], 0, 1,
        want_fail='carrier_present', cache=None)
    add('four external carriers, cache bytes are not the pinned carrier',
        [ext_frozen, ext_recs], 0, 1, want_fail='carrier_pin_ok', cache=cache_bad)
    ext_len = json.loads(ext_spec)
    for c in ext_len['carriers']:
        if c['id'] == 'g7581':
            c['external']['length'] = len(carriers['g7581']) - 64
    add('external carve length differs from bytes_used',
        [{**ext_frozen, CARRIERS: json.dumps(ext_len, indent=1)}, ext_recs], 0, 1,
        want_fail='carve_ok', cache=cache_ok)

    # ---- the frozen rea-agents package pin (round 49)
    add('rea package does not match the frozen pin',
        [{**frozen, 'tools/round-50/rea-pkg.json': json.dumps({
            'version': REA_VERSION, 'package_json_sha256': '0' * 64,
            'package_lock_sha256': '0' * 64})}, good], 0, 2, 'unevaluable')
    add('no rea-pkg pin at the freeze', [{**frozen, 'tools/round-50/rea-pkg.json': None,
                                          'tools/round-42/rea-pkg.json': None}, good],
        0, 2, 'unevaluable')
    # ---- path identity: exact relative to the chunk extract root (R40-CL1)
    # Round-40 defect: the suffix rule read the regular file `usr/bin/busy` as the
    # symlink entry `bin/busy`, so L2 scored 3/4 at 42c10a58 on a faithful
    # extraction. Every case below pins one shape of that collision; `path_probes`
    # and `root_probes` additionally assert that the round-40 matcher mis-scores
    # exactly these fixtures, so the selftest cannot silently stop discriminating.
    path_probes = []
    root_probes = []
    # (spec_probes is defined with the layout controls above)

    def probe(desc, candidate, rel, want_new, want_legacy):
        path_probes.append({
            'desc': desc, 'candidate': candidate, 'rel': rel,
            'new': same_rel(candidate, rel, 'firmware.bin_extract'),
            'legacy': legacy_same_rel(candidate, rel),
            'want_new': want_new, 'want_legacy': want_legacy})

    def pub(e, rel, h, size=5):
        e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/' + rel,
            'path': '/x/' + rel, 'size': size, 'sha256': h})

    def entry(e, rel, gap=True, target='../sbin/tool'):
        e['normalized_result']['unpublished_entries'].append({
            'relative_path': 'firmware.bin_extract/' + rel, 'kind': 'symlink',
            'link_target': target})
        if gap:
            e['normalized_result']['extraction_gaps'].append({
                'kind': 'unpublished-entry', 'handler': HANDLER,
                'relative_path': 'firmware.bin_extract/' + rel,
                'dependencies': []})

    def oracle_rows(rows):
        return ''.join(f'{rel}\t{h}\t{size}\n' for rel, h, size in rows).encode()

    def same_run(recs, k='g7582'):
        return mk_same_runner({**green_envs, k: json.loads(recs[receipt_path(k)])})

    probe('dir 1: regular usr/bin/busy vs symlink entry bin/busy',
          'firmware.bin_extract/usr/bin/busy', 'bin/busy', False, True)
    probe('dir 2: regular sbin/tool vs symlink entry usr/sbin/tool',
          'firmware.bin_extract/sbin/tool', 'usr/sbin/tool', False, False)
    probe('materialised symlink at its own entry path',
          'firmware.bin_extract/usr/sbin/tool', 'usr/sbin/tool', True, True)
    probe('deeper-than-oracle file vs oracle row usr/bin/busy',
          'firmware.bin_extract/x/usr/bin/busy', 'usr/bin/busy', False, True)
    probe('nested chunk root file vs outer-root table row lib/x',
          'firmware.bin_extract/core.sqsh_extract/lib/x', 'lib/x', False, True)
    probe('plain oracle row', 'firmware.bin_extract/var/info.txt', 'var/info.txt',
          True, True)

    # dir 1: the regular file ends with the symlink entry's path (round-40 false
    # positive: the published regular was reported as the materialised symlink)
    deep_file, deep_recs = build(
        env_over={'g7582': lambda e: (pub(e, 'usr/bin/busy', fsha(7)),
                                      entry(e, 'bin/busy'))},
        oracle_over={'g7582': oracle_rows([('var/info.txt', fsha(3), 40),
                                           ('usr/bin/busy', fsha(7), 5)])},
        nonreg_over={'g7582': 'bin/busy\tsymlink\n'})
    add('regular usr/bin/busy does not satisfy the symlink entry bin/busy',
        [deep_file, deep_recs], 0, 0, runner=same_run(deep_recs))
    # dir 2: the symlink entry's path ends with a regular file's path
    short_file, short_recs = build(
        env_over={'g7582': lambda e: (pub(e, 'sbin/tool', fsha(8), 40),
                                      entry(e, 'usr/sbin/tool', target='tool'))},
        oracle_over={'g7582': oracle_rows([('var/info.txt', fsha(3), 40),
                                           ('sbin/tool', fsha(8), 40)])},
        nonreg_over={'g7582': 'usr/sbin/tool\tsymlink\n'})
    add('regular sbin/tool does not satisfy the symlink entry usr/sbin/tool',
        [short_file, short_recs], 0, 0, runner=same_run(short_recs))
    # the tightened matcher must still catch a published symlink path
    materialised, materialised_recs = build(
        env_over={'g7582': lambda e: (pub(e, 'usr/sbin/tool', fsha(9), 40),
                                   entry(e, 'usr/sbin/tool', gap=False,
                                         target='tool'))},
        nonreg_over={'g7582': 'usr/sbin/tool\tsymlink\n'})
    add('published regular at the symlink entry usr/sbin/tool is still caught',
        [materialised, materialised_recs], 0, 1,
        want_fail='nonregular_unpublished_ok', runner=same_run(materialised_recs))
    # a deeper file cannot stand in for an oracle row (round-40 matched the suffix)
    oracle_shadow, oracle_shadow_recs = build(
        env_over={'g7582': lambda e: pub(e, 'usr/bin/busy', fsha(7))},
        oracle_over={'g7582': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('bin/busy', fsha(7), 5)])})
    add('deeper file with the oracle row sha256 does not publish oracle bin/busy',
        [oracle_shadow, oracle_shadow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(oracle_shadow_recs))
    wrong_gap, wrong_gap_recs = build(
        env_over={'g7582': lambda e: (entry(e, 'bin/busy', gap=False),
                                   e['normalized_result']['extraction_gaps'].append({
                                       'kind': 'unpublished-entry',
                                       'handler': HANDLER,
                                       'relative_path':
                                           'firmware.bin_extract/usr/bin/busy',
                                       'dependencies': []}))},
        nonreg_over={'g7582': 'bin/busy\tsymlink\n'})
    add('gap on usr/bin/busy does not resolve to the symlink entry bin/busy',
        [wrong_gap, wrong_gap_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(wrong_gap_recs))

    # ---- two chunks: each file resolves against its own chunk's extract root
    def add_nested_chunk(e, publish, oracle_rel=None):
        """A depth-1 squashfs chunk under the top extraction, publishing one file
        in its own `*_extract` directory. `oracle_rel` names the table row that
        file must (or must not) satisfy."""
        e['normalized_result']['chunks'].append({
            'input_path': '$output/firmware.bin_extract/core.sqsh',
            'provider_id': '3028394:2',
            'range': {'offset': 4096, 'length': 2048},
            'handler': HANDLER, 'encrypted': False,
            'root_file_range': {'offset': 4096, 'length': 2048},
            'extraction_failed': False})
        e['normalized_result']['derivations'].append({
            'parent_path': '$output/firmware.bin_extract',
            'child_path': '$output/firmware.bin_extract/core.sqsh_extract',
            'handler': HANDLER,
            'provider_blob_id': '3028394:2',
            'parent_file_range': {'offset': 4096, 'length': 2048}})
        if publish:
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/core.sqsh_extract/lib/x',
                'path': '/x/core.sqsh_extract/lib/x', 'size': 7,
                'sha256': fsha(11)})

    hint = spec_json(oracle_root={'g7582': 'firmware.bin_extract'})
    two_ok, two_ok_recs = build(
        env_over={'g7582': lambda e: add_nested_chunk(e, True)}, spec_text=hint)
    add('two chunks with oracle_root: the nested file is another namespace',
        [two_ok, two_ok_recs], 0, 0, runner=same_run(two_ok_recs))
    two_amb_frozen, two_amb_recs = build(
        env_over={'g7582': lambda e: add_nested_chunk(e, True)})
    add('two squashfs roots without oracle_root fail closed',
        [two_amb_frozen, two_amb_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_amb_recs))
    two_wrong_frozen, two_wrong_recs = build(
        env_over={'g7582': lambda e: add_nested_chunk(e, True)},
        spec_text=spec_json(oracle_root={'g7582': 'no.such.root'}))
    add('oracle_root that names no derivation root fails closed',
        [two_wrong_frozen, two_wrong_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_wrong_recs))
    two_shadow, two_shadow_recs = build(
        env_over={'g7582': lambda e: add_nested_chunk(e, True)}, spec_text=hint,
        oracle_over={'g7582': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('lib/x', fsha(11), 7)])})
    add('two chunks: the nested chunk file does not publish outer-root row lib/x',
        [two_shadow, two_shadow_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_shadow_recs))
    for desc, envs, hint_root, want_root, want_src in (
            ('single chunk root', green_receipts, None, 'firmware.bin_extract',
             'single squashfs_v4_le derivation root'),
            ('two roots with oracle_root', two_ok_recs, 'firmware.bin_extract',
             'firmware.bin_extract', 'oracle_root from carriers.json'),
            ('two roots without a hint', two_amb_recs, None, None,
             'ambiguous')):
        e = json.loads(envs[receipt_path('g7582')])
        r, src = subject_root(e, hint_root)
        root_probes.append({'desc': desc, 'root': r, 'source': src,
                            'want_root': want_root,
                            'want_src': (src if want_src == 'ambiguous'
                                         and src.startswith('ambiguous') else want_src),
                            'chunk_roots': chunk_roots(e, hint_root)})

    # ---- measured chunk-directory shapes (round-41 critique of the refreeze)
    # unblob 26.6.4 through rea-agents 6.5.0 --max-depth 1 (measured on dev
    # carriers, artifacts/chunk-naming.json): a chunk that is only PART of the
    # input is extracted one level deeper than the input's own directory, so a
    # matcher that strips one `_extract` component scores 0 oracle rows on a
    # padded carrier. These cases pin both the depth and the ambiguity of two
    # AVM chunks in one receipt.
    PORTION = 'firmware.bin_extract/4096-4500.squashfs_v4_le_extract'
    rule_struct1 = json.dumps({'claim': 'R50-C1',
                               'allowed': {'symlink': ['unpublished-entry'],
                                           'device': ['unpublished-entry']},
                               'structural': {'depth-limited': 1}})

    def padded_receipt(e, shallow=False):
        """A 4500-byte input: 4096 bytes of padding, then an AVM filesystem."""
        e['normalized_result']['selection']['length'] = 4500
        e['locations'] = [{'kind': 'file-offset-range', 'start': 0, 'end': 4500}]
        e['normalized_result']['chunks'] = [
            {'input_path': '$input', 'provider_id': 'p0',
             'range': {'offset': 0, 'length': 4096}, 'handler': 'padding',
             'encrypted': False,
             'root_file_range': {'offset': 0, 'length': 4096},
             'extraction_failed': False},
            {'input_path': '$input', 'provider_id': 'p1',
             'range': {'offset': 4096, 'length': 404}, 'handler': HANDLER,
             'encrypted': False,
             'root_file_range': {'offset': 4096, 'length': 404},
             'extraction_failed': False}]
        e['normalized_result']['derivations'] = [
            {'parent_path': '$input',
             'child_path': '$output/' + PORTION, 'provider_blob_id': 'p1',
             'handler': HANDLER,
             'parent_file_range': {'offset': 4096, 'length': 404}}]
        e['normalized_result']['files'] = [
            {'relative_path': 'firmware.bin_extract/0-4096.padding',
             'path': '/x/0-4096.padding', 'size': 4096, 'sha256': fsha(13)},
            {'relative_path': ('firmware.bin_extract/var/info.txt' if shallow
                               else PORTION + '/var/info.txt'),
             'path': '/x/var/info.txt', 'size': 40, 'sha256': fsha(3)}]
        e['normalized_result']['extraction_gaps'] = [
            {'kind': 'depth-limited', 'input_path': '$output/' + PORTION,
             'relative_path': None, 'handler': None, 'dependencies': [],
             'continuation_id': 'continuation-pad'}]
        e['normalized_result']['unpublished_entries'] = []
        e['normalized_result']['depth_limited_paths'] = ['$output/' + PORTION]

    pad_frozen, pad_recs = build(rule_text=rule_struct1,
                                 env_over={'g7582': padded_receipt})
    add('padded carrier: the oracle resolves under the portion chunk directory',
        [pad_frozen, pad_recs], 0, 0, runner=same_run(pad_recs))
    pad_shallow_frozen, pad_shallow_recs = build(
        rule_text=rule_struct1,
        env_over={'g7582': lambda e: padded_receipt(e, shallow=True)})
    add('padded carrier: the same rows one level too shallow score nothing',
        [pad_shallow_frozen, pad_shallow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(pad_shallow_recs))
    for desc, recs, want_root, want_src in (
            ('portion chunk root', pad_recs, PORTION,
             'single squashfs_v4_le derivation root'),
            ('portion chunk, shallow publish', pad_shallow_recs, PORTION,
             'single squashfs_v4_le derivation root')):
        e = json.loads(recs[receipt_path('g7582')])
        r, src = subject_root(e)
        root_probes.append({'desc': desc, 'root': r, 'source': src,
                            'want_root': want_root, 'want_src': want_src,
                            'chunk_roots': chunk_roots(e)})

    def two_portion_chunks(e):
        """Two AVM chunks in one input: no receipt data says which filesystem the
        oracle describes, and each brings its own depth-limited gap."""
        e['normalized_result']['selection']['length'] = 5000
        e['locations'] = [{'kind': 'file-offset-range', 'start': 0, 'end': 5000}]
        e['normalized_result']['chunks'] = [
            {'input_path': '$input', 'provider_id': 'p0',
             'range': {'offset': 0, 'length': 2500}, 'handler': HANDLER,
             'encrypted': False, 'root_file_range': {'offset': 0, 'length': 2500},
             'extraction_failed': False},
            {'input_path': '$input', 'provider_id': 'p1',
             'range': {'offset': 2500, 'length': 2500}, 'handler': HANDLER,
             'encrypted': False,
             'root_file_range': {'offset': 2500, 'length': 2500},
             'extraction_failed': False}]
        e['normalized_result']['derivations'] = [
            {'parent_path': '$input',
             'child_path': '$output/firmware.bin_extract/0-2500.squashfs_v4_le_extract',
             'provider_blob_id': 'p0', 'handler': HANDLER,
             'parent_file_range': {'offset': 0, 'length': 2500}},
            {'parent_path': '$input',
             'child_path': '$output/firmware.bin_extract/2500-5000.squashfs_v4_le_extract',
             'provider_blob_id': 'p1', 'handler': HANDLER,
             'parent_file_range': {'offset': 2500, 'length': 2500}}]
        e['normalized_result']['files'] = [
            {'relative_path': 'firmware.bin_extract/0-2500.squashfs_v4_le_extract/'
                              'var/info.txt',
             'path': '/x/var/info.txt', 'size': 40, 'sha256': fsha(3)},
            {'relative_path': 'firmware.bin_extract/2500-5000.squashfs_v4_le_extract/'
                              'etc/x',
             'path': '/x/etc/x', 'size': 9, 'sha256': fsha(14)}]
        e['normalized_result']['extraction_gaps'] = [
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '0-2500.squashfs_v4_le_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c0'},
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '2500-5000.squashfs_v4_le_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c1'}]
        e['normalized_result']['unpublished_entries'] = []

    two_frozen, two_recs2 = build(rule_text=rule_struct1,
                                  env_over={'g7582': two_portion_chunks})
    add('two AVM chunks in one receipt are ambiguous, not guessed',
        [two_frozen, two_recs2], 0, 1, want_fail='gaps_ok',
        runner=same_run(two_recs2))
    e = json.loads(two_recs2[receipt_path('g7582')])
    r, src = subject_root(e)
    root_probes.append({'desc': 'two portion chunk roots', 'root': r, 'source': src,
                        'want_root': None,
                        'want_src': src if src.startswith('ambiguous') else '',
                        'chunk_roots': chunk_roots(e)})

    # ---- the root derivation fails closed rather than guessing
    def no_input_handler(e):
        """Two handler chunks in the input and no derivation root for the whole
        filesystem: the receipt states two roots and the oracle could describe
        either."""
        e['normalized_result']['chunks'][0]['handler'] = 'padding'
        e['normalized_result']['derivations'] = [
            {'parent_path': '$input', 'provider_blob_id': 'p' + n,
             'child_path': '$output/firmware.bin_extract/%s_extract' % n,
             'handler': HANDLER,
             'parent_file_range': {'offset': off, 'length': 2048}}
            for n, off in (('a.sqsh', 4096), ('b.sqsh', 8192))]
        for name, off in (('a.sqsh', 4096), ('b.sqsh', 8192)):
            e['normalized_result']['chunks'].append({
                'input_path': '$output/firmware.bin_extract/' + name,
                'provider_id': '3028394:' + name,
                'range': {'offset': off, 'length': 2048},
                'handler': HANDLER, 'encrypted': False,
                'root_file_range': {'offset': off, 'length': 2048},
                'extraction_failed': False})
        for name in ('a.sqsh', 'b.sqsh'):
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/%s_extract/var/info.txt' % name,
                'path': '/x/%s_extract/var/info.txt' % name, 'size': 40,
                'sha256': fsha(3)})

    amb_frozen, amb_recs = build(env_over={'g7582': no_input_handler})
    add('two handler chunks and no input handler chunk fail closed',
        [amb_frozen, amb_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(amb_recs))
    e = json.loads(amb_recs[receipt_path('g7582')])
    r, src = subject_root(e)
    root_probes.append({'desc': 'ambiguous handler chunks', 'root': r, 'source': src,
                        'want_root': None,
                        'want_src': src if src.startswith('ambiguous:') else '',
                        'chunk_roots': chunk_roots(e)})

    def outside_namespace(e):
        """A published file under a directory that is not the subject root."""
        e['normalized_result']['files'].append({
            'relative_path': 'other_extract/etc/x', 'path': '/x/other_extract/etc/x',
            'size': 5, 'sha256': fsha(12)})

    mix_frozen, mix_recs = build(env_over={'g7582': outside_namespace})
    add('a file outside the subject root is another namespace, not an extra',
        [mix_frozen, mix_recs], 0, 0, runner=same_run(mix_recs))
    e = json.loads(mix_recs[receipt_path('g7582')])
    r, src = subject_root(e)
    root_probes.append({'desc': 'outside-namespace file', 'root': r, 'source': src,
                        'want_root': 'firmware.bin_extract',
                        'want_src': 'single squashfs_v4_le derivation root',
                        'chunk_roots': chunk_roots(e)})

    def no_derivations(e):
        e['normalized_result']['derivations'] = []

    nod_frozen, nod_recs = build(env_over={'g7582': no_derivations})
    add('receipt with no squashfs derivation edge fails closed',
        [nod_frozen, nod_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nod_recs))

    # ---- removal disposition (R41C1DevCore 7.1-7.3, for the g7582 rootfs carrier)
    # unblob deletes escaping symlinks after reporting MaliciousSymlinkRemoved and
    # empty-target symlinks with no report at all, and never publishes a link as a
    # regular file. g7582's rootfs carrier needs the allowance, so the frozen rule may
    # carry a `removed` block and every row must land in exactly one disposition.
    rule_removed = json.dumps({
        'claim': 'R50-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': True},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive'},
        'structural': {'depth-limited': 1}}, indent=1)

    def one_symlink(e, gap=True, removal=False, row_rel='bin/link',
                    diag_rel='bin/link', target='../usr/bin/x'):
        """g7582 with exactly one symlink row and a chosen disposition."""
        if gap:
            entry(e, row_rel, gap=True, target=target)
        else:
            entry(e, row_rel, gap=False, target=target)
        if removal:
            e['normalized_result']['diagnostics'].append({
                'input_path': '$output/firmware.bin_extract',
                'report': {'__typename__': 'MaliciousSymlinkRemoved',
                           'severity': 'WARNING',
                           'link': lnk(e, diag_rel),
                           'target': '/etc/shadow'}})

    rem_frozen, rem_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: one_symlink(e, gap=False, removal=True)})
    add('a removal diagnostic is an admitted disposition for a symlink row',
        [rem_frozen, rem_recs], 0, 0, runner=same_run(rem_recs))
    foreign_frozen, foreign_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: (
            one_symlink(e, gap=False, removal=True),
            e['normalized_result']['diagnostics'][-1]['report'].__setitem__(
                'link', '/e1/e2/e3/e4/e5/e6/firmware.bin_extract/bin/link'))})
    add('a removal whose link lies outside the run root cannot be mapped',
        [foreign_frozen, foreign_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(foreign_recs))
    nopar_frozen, nopar_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: (
            one_symlink(e, gap=False, removal=True),
            e['parameters'].__setitem__('output_directory', '/x'))})
    add('a removal with a run root that is the filesystem root cannot be mapped',
        [nopar_frozen, nopar_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nopar_recs))
    both_frozen, both_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: one_symlink(e, gap=True, removal=True)})
    add('an entry cannot be both gapped and removed',
        [both_frozen, both_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(both_recs))
    none_frozen, none_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: one_symlink(e, gap=False, removal=False)})
    add('a required symlink with no disposition fails',
        [none_frozen, none_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(none_recs))
    stray_frozen, stray_recs = build(
        rule_text=rule_removed, nonreg_over={'g7582': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: one_symlink(e, gap=True, removal=True,
                                              diag_rel='var/nowhere')})
    add('a removal that resolves to no symlink row fails',
        [stray_frozen, stray_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(stray_recs))
    # a removal may not be used to hide a *regular* file: the row it names must be
    # of a kind the rule lists, and a device row is not one
    dev_frozen, dev_recs = build(
        rule_text=rule_removed,
        nonreg_over={'g7582': 'dev/console\tdevice\t\n'},
        env_over={'g7582': lambda e: (entry(e, 'dev/console', gap=False),
                                   e['normalized_result']['diagnostics'].append({
                                       'input_path': '$output/firmware.bin_extract',
                                       'report': {'__typename__':
                                                  'MaliciousSymlinkRemoved',
                                                  'severity': 'WARNING',
                                                  'link': lnk(e, 'dev/console'),
                                                  'target': '/x'}}))})
    add('a removal naming a row of an unlisted kind fails',
        [dev_frozen, dev_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(dev_recs))
    # silent empty-target removal: unblob deletes the link and reports nothing
    rule_silent = json.dumps({
        'claim': 'R50-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': True},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive',
                    'silent': {'symlink': ['empty-target']}},
        'structural': {'depth-limited': 1}}, indent=1)
    sil_frozen, sil_recs = build(
        rule_text=rule_silent, nonreg_over={'g7582': 'bin/empty\tsymlink\t\n'},
        env_over={'g7582': lambda e: entry(e, 'bin/empty', gap=False)})
    add('a silent empty-target symlink is admitted with no record',
        [sil_frozen, sil_recs], 0, 0, runner=same_run(sil_recs))
    sil2_frozen, sil2_recs = build(
        rule_text=rule_silent,
        nonreg_over={'g7582': 'bin/empty\tsymlink\t../usr/bin/x\n'},
        env_over={'g7582': lambda e: entry(e, 'bin/empty', gap=False)})
    add('a symlink with a non-empty target cannot hide behind the silent allowance',
        [sil2_frozen, sil2_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(sil2_recs))
    # projection carries the removal identity (R41C1DevCore 7.3): two symlink
    # rows, neither required, and the rerun removed the other one
    rule_opt = json.dumps({
        'claim': 'R50-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': False, 'device': False},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive'},
        'structural': {'depth-limited': 1}}, indent=1)

    def two_removed(which):
        def apply(e):
            entry(e, 'bin/one', gap=False, target='../x')
            entry(e, 'bin/two', gap=False, target='../y')
            e['normalized_result']['diagnostics'] = [{
                'input_path': '$output/firmware.bin_extract',
                'report': {'__typename__': 'MaliciousSymlinkRemoved',
                           'severity': 'WARNING',
                           'link': lnk(e, which),
                           'target': '/etc/shadow'}}]
        return apply

    proj_frozen, proj_recs = build(
        rule_text=rule_opt,
        nonreg_over={'g7582': 'bin/one\tsymlink\t../x\nbin/two\tsymlink\t../y\n'},
        env_over={'g7582': two_removed('bin/one')})

    def other_removal_runner(carrier_bytes, cid, params=None):
        """A rerun of the same bytes that removed the other symlink."""
        if cid != 'g7582':
            return mk_same_runner(green_envs)(carrier_bytes, cid, params)
        e = json.loads(json.dumps(json.loads(proj_recs[receipt_path('g7582')])))
        e['normalized_result']['diagnostics'][0]['report']['link'] = \
            lnk(e, 'bin/two')
        e['subject']['digest']['sha256'] = sha(carrier_bytes)
        e['normalized_result']['selection']['sha256'] = sha(carrier_bytes)
        return 'ok', rehost(e, 'selftest-other-removal')

    add('a rerun that removed a different link breaks the projection',
        [proj_frozen, proj_recs], 0, 1, want_fail='projection_ok',
        runner=other_removal_runner)

    # ---- freshness: a relabelled previous-round carrier is not coverage
    add('relabelled previous-round pins (prior_pins)',
        [{**frozen, CARRIERS: spec_json(prior_pins=[pins[k] for k in ids])}, good],
        0, 1, want_fail='carrier_fresh_ok')
    prior_tbl = json.dumps({'claim': 'R41-C1', 'target': 4, 'carriers': [
        {'id': 'V3', 'sha256': pins['g7581']},
        {'id': 'L4', 'sha256': pins['c6430']}]})
    add('round-41 carrier table in the lane names two frozen pins',
        [{**frozen, '.ufo/waves/round-41/c1/carriers.json': prior_tbl}, good], 0, 1,
        want_fail='carrier_fresh_ok')
    add('round-49 carrier table in the lane names a frozen pin',
        [{**frozen, 'tools/round-49/carriers.json': json.dumps(
            {'carriers': [{'id': 'v1le', 'sha256': pins['g7582']}]})}, good], 0, 1,
        want_fail='carrier_fresh_ok')
    add('prior-pins document names a frozen pin',
        [{**frozen, 'tools/round-42/prior-pins.json': json.dumps(
            {'pins': [pins['c6490']]})}, good], 0, 1, want_fail='carrier_fresh_ok')
    add('prior_pins that are not 64-hex',
        [{**frozen, CARRIERS: spec_json(prior_pins=['not-a-pin'])}, good], 0, 1,
        want_fail='b:carriers_spec_ok')

    # ---- vendor spec chain and carve exactness (R41C1DevCore 7.4, routed R40-CL6)
    # The spec is checked directly: a vendor carrier cannot be loaded here (its
    # bytes live in --carrier-cache by licence), so an end-to-end case would fail
    # on carrier_present and prove nothing about the chain.
    def nested_spec(drop):
        doc = json.loads(spec_json(external='g7581'))
        for c in doc['carriers']:
            if c['id'] == 'g7581':
                c['external']['nested'] = {'member': './var/tmp/inner.image',
                                           'length': 4096}
                if not drop:
                    c['external']['nested']['sha256'] = 'c' * 64
        return json.dumps(doc, indent=1)

    def probe_spec(desc, spec_text, want_ok, want_text=None):
        _ids, probs = carriers_spec(json.loads(spec_text), TARGET, IDS)
        spec_probes.append({'desc': desc, 'ok': not probs,
                            'problems': [p[:160] for p in probs[:4]],
                            'want_ok': want_ok, 'want_text': want_text})

    probe_spec('external carrier without member_sha256',
               spec_json(external='g7581', external_drop=('member_sha256',)),
               False, 'lacks member_sha256')
    probe_spec('external carrier without a positive carve length',
               spec_json(external='g7581', external_drop=('length',)),
               False, 'lacks length')
    probe_spec('external carrier with a member_sha256',
               spec_json(external='g7581'), True)
    probe_spec('external carrier with a nested block and no nested.sha256',
               nested_spec(drop=True), False, 'nested.sha256')
    probe_spec('external carrier with nested.sha256',
               nested_spec(drop=False), True)
    probe_spec('oracle_root is a relative path',
               spec_json(oracle_root={'g7581': 'firmware.bin_extract'}), True)
    probe_spec('oracle_root that is absolute',
               spec_json(oracle_root={'g7581': '/firmware.bin_extract'}), False,
               'oracle_root')
    probe_spec('target missing from carriers.json',
               spec_json(omit=('target',)), False, 'frozen target')
    probe_spec('target frozen at 3', spec_json(target=3), False, 'frozen target')
    probe_spec('rea_parameters missing', spec_json(omit=('rea_parameters',)), False,
               'rea_parameters is not an object')
    probe_spec('rea_parameters at depth 3',
               spec_json(rea=dict(FIXTURE_REA_PARAMETERS, max_depth=3)), False,
               'max_depth')
    probe_spec('rea_parameters without a budget',
               spec_json(rea={'max_depth': 1, 'max_output_bytes': 1}), False,
               'max_output_files')
    probe_spec('rea_parameters with a non-integer budget',
               spec_json(rea=dict(FIXTURE_REA_PARAMETERS, max_output_files='many')),
               False, 'max_output_files')
    probe_spec('carrier ids compare case-insensitively',
               spec_json().replace('"g7581"', '"G7581"'), True)
    probe_spec('a fifth carrier id outside the claim',
               spec_json().replace('"g7581"', '"z9999"'), False, 'carrier ids')
    # carve_ok: bytes longer than the superblock bytes_used
    over_len = sb_carrier(XZ_ID, b'g7581-long', marker_value=None)
    over_len = sb_carrier(XZ_ID, b'g7581-long', marker_value=len(over_len) - 64)
    o_frozen, o_recs = build(blob_over={'g7581': over_len})
    add('carrier longer than its bytes_used (sloppy carve)',
        [o_frozen, o_recs], 0, 1, want_fail='carve_ok', runner=same_run(o_recs))

    # ---- freeze integrity
    add('carrier bytes changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/g7581/carrier.sqsh': b'changed carrier\n'}],
        0, 2, 'frozen_path_changed')
    add('carrier bytes changed then restored',
        [frozen, {**good, f'{AFTERDIR}/g7581/carrier.sqsh': b'changed carrier\n'},
         {**good, f'{AFTERDIR}/g7581/carrier.sqsh': carriers['g7581']}], 0, 2,
        'frozen_path_changed')
    add('oracle changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/g7582/oracle.tsv': oracle_tsv('g7582') + b'extra.txt\t'
          + b'3' * 64 + b'\t1\n'}], 0, 2, 'frozen_path_changed')
    add('nonregular table changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/c6490/nonregular.tsv': b'usr/lib/libfoo.so\tsymlink\n'
         b'usr/lib/extra\tsymlink\n'}], 0, 2, 'frozen_path_changed')
    add('carriers.json changed after freeze',
        [frozen, {**good, CARRIERS: spec_json(drop=('c6430',))}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json changed after freeze',
        [frozen, {**good, GAPRULE: json.dumps({'claim': 'R50-C1', 'allowed': {
            'symlink': ['unpublished-entry']}}).encode()}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json touched then restored',
        [frozen, {**good, GAPRULE: b'{}\n'}, {**good, GAPRULE: rule.encode()}], 0, 2,
        'frozen_path_changed')
    add('counter edited after freeze',
        [frozen, {**good, 'tools/round-50/c1-counter.py': b'#!/usr/bin/env python3\n'
         b'print(0)\n'}], 0, 2, 'frozen_path_changed')
    add('claims edited after freeze',
        [frozen, {**good, 'plans/round-50-claims.md': b'# new plan\n'}], 0, 2,
        'frozen_path_changed')
    add('a new file under tools/round-50 after the freeze',
        [frozen, {**good, 'tools/round-50/extra.py': b'print(1)\n'}], 0, 2,
        'frozen_path_changed')
    add('rea-pkg pin edited after the freeze',
        [frozen, {**good, 'tools/round-50/rea-pkg.json': b'{}\n'}], 0, 2,
        'frozen_path_changed')
    add('carried-over second reader edited after the freeze',
        [frozen, {**good, 'tools/round-41/sqfs-list.py': b'# edited\n'}], 0, 2,
        'frozen_path_changed')
    add('carried-over fetcher edited after the freeze',
        [frozen, {**good, 'tools/round-41/fetch-vendor.py': b'# edited\n'}], 0, 2,
        'frozen_path_changed')
    add('xpin tool edited after the freeze',
        [frozen, {**good, XPIN: b'// edited\n'}], 0, 2, 'frozen_path_changed')
    add('oracle table first committed after the freeze is not frozen',
        [{**frozen, f'{AFTERDIR}/g7582/oracle.tsv': None},
         {**good, f'{AFTERDIR}/g7582/oracle.tsv': oracle_tsv('g7582')}], 0, 1,
        want_fail='b:frozen_tables_valid')
    # merge-aware freeze walk (round 49): the edit is visible only through the
    # merge commit's own diff against its first parent, or only inside the side branch
    add('frozen plan edited only by the merge commit itself (evil merge)',
        [frozen, {'__merge__': {'plans/round-50-claims.md': b'# new plan\n'}}], 0, 2,
        'frozen_path_changed')
    add('frozen counter edited on a side branch and merged',
        [frozen, {'__merge__': {}, '__side__': {'tools/round-50/c1-counter.py':
                                                 b'print(0)\n'}}], 0, 2,
        'frozen_path_changed')
    add('a clean merge touching nothing frozen does not trip the freeze walk',
        [frozen, {**good}, {'__merge__': {'notes.txt': b'n\n'}}], 0, 0)
    # ---- frozen-table controls
    bad_pins = dict(pins)
    bad_pins['g7581'] = '4' * 64
    add('frozen pin wrong (carrier untouched)',
        [{**frozen, CARRIERS: spec_json(pin_map=bad_pins)}, good], 0, 1,
        want_fail='carrier_pin_ok')
    add('carriers.json drops a carrier at the freeze (target 4)',
        [{**frozen, CARRIERS: spec_json(drop=('g7582',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    add('all four carriers read gzip (compression id 1)',
        list(build(blob_over={k: sb_carrier(1, ('%s-gzip' % k).encode())
                              for k in ids})), 0, 1, want_fail='layout_ok')
    thin = json.dumps({'claim': 'R50-C1', 'allowed': {'symlink': ['unpublished-entry']}})
    f2, r2 = build(rule_text=thin)
    add('gap rule omits the device kind', [f2, r2], 0, 1, want_fail='b:gap_rule_ok')
    add('gap rule is JSON but not an object at the freeze',
        list(build(rule_text='[]')), 0, 1, want_fail='b:frozen_tables_valid')
    add('gap rule names another claim',
        list(build(rule_text=json.dumps({'claim': 'R39-C1', 'allowed': {
            'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}}))),
        0, 1, want_fail='b:gap_rule_ok')

    # ---- structural gaps (unblob bookkeeping: null relative_path)
    rule_struct = json.dumps({'claim': 'R50-C1',
                              'allowed': {'symlink': ['unpublished-entry'],
                                          'device': ['unpublished-entry']},
                              'required': {'symlink': True, 'device': True},
                              'structural': {'unknown-chunk-handler': 1}})

    def add_struct(e, kind='unknown-chunk-handler', path=None, extra=0):
        base = {'kind': kind, 'relative_path': path, 'dependencies': []}
        e['normalized_result']['extraction_gaps'].append(dict(base))
        for _ in range(extra):
            e['normalized_result']['extraction_gaps'].append(dict(base))

    st_frozen, st_receipts = build(rule_text=rule_struct,
                                   env_over={'g7581': add_struct})
    add('structural gap within its frozen allowance',
        [st_frozen, st_receipts], 0, 0,
        runner=mk_same_runner({**green_envs, 'g7581': json.loads(st_receipts[
            receipt_path('g7581')])}))
    st2_frozen, st2_receipts = build(
        rule_text=rule_struct, env_over={'g7581': lambda e: add_struct(e, extra=1)})
    add('structural gaps over the allowance', [st2_frozen, st2_receipts], 0, 1,
        want_fail='gaps_ok')
    st3_frozen, st3_receipts = build(
        rule_text=rule_struct,
        env_over={'g7581': lambda e: add_struct(e, kind='depth-limited')})
    add('path-less gap kind with no structural allowance', [st3_frozen, st3_receipts],
        0, 1, want_fail='gaps_ok')
    st4_frozen, st4_receipts = build(
        rule_text=rule_struct,
        env_over={'g7581': lambda e: add_struct(e, path='usr/share/demo/extra-link')})
    add('structural gap kind that carries a path', [st4_frozen, st4_receipts], 0, 1,
        want_fail='gaps_ok')

    # ---- projection profile: frozen explicitly as plus-extractor (round 50, S11)
    def bump_bytes(e):
        e['normalized_result']['published_bytes'] += 1
    core_frozen, core_receipts = build(
        env_over={'g7581': bump_bytes}, spec_text=spec_json(projection='core'))
    add('a frozen core profile (oracle-closed: it would accept the fabrication) is refused',
        [core_frozen, core_receipts], 0, 1, want_fail='b:carriers_spec_ok')
    plus_frozen, plus_receipts = build(env_over={'g7581': bump_bytes})
    add('the frozen plus-extractor profile refuses a projection-different fabrication',
        [plus_frozen, plus_receipts], 0, 1, want_fail='projection_ok')
    add('projection missing from carriers.json',
        [{**frozen, CARRIERS: spec_json(omit=('projection',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    add('plus-mime is not the frozen profile',
        [{**frozen, CARRIERS: spec_json(projection='plus-mime')}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    add('unknown projection profile in carriers.json',
        [{**frozen, CARRIERS: spec_json(projection='plus-everything')}, good], 0, 1,
        want_fail='b:carriers_spec_ok')

    # ---- rerun replays the FROZEN extraction parameters (not the receipt's own)
    def depth_runner(expected):
        def run(carrier_bytes, cid, params=None):
            got = (params or {}).get('max_depth')
            if got != expected:
                return 'no_data', {'ok': False, 'reason': 'depth %r != %r'
                                   % (got, expected)}
            return sim_runner(carrier_bytes, cid, params)
        return run

    def budget_runner(carrier_bytes, cid, params=None):
        want = FIXTURE_REA_PARAMETERS
        if {k: (params or {}).get(k) for k in want} != want:
            return 'no_data', {'ok': False, 'reason': 'params %r != %r'
                               % (params, want)}
        return sim_runner(carrier_bytes, cid, params)

    add('rerun passes the frozen max_depth (1) to REA', [frozen, good], 0, 0,
        runner=depth_runner(1))
    add('rerun passes the frozen output budgets to REA', [frozen, good], 0, 0,
        runner=budget_runner)
    add('rerun takes the parameters from the frozen table, not from the receipt',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__('max_depth', 3))],
        0, 1, want_fail='parameters_ok', runner=depth_runner(1))

    # ---- documentation bindings
    add('province has no Core section at all',
        [{**frozen, 'PROVINCE.md': '# P\n\n## Next\n- x\n'}, good], 0, 1,
        want_fail='b:province_core_section')
    add('province row outside the round-50 section',
        [{**frozen, 'PROVINCE.md': _province(heading='## Round-49 additions to Core')},
         good], 0, 1, want_fail='b:province_core_row')
    add('province row names the BE handler, not the LE one',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4_be`')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row without the handler in the first cell',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4`')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row that does not name the AVM marker',
        [{**frozen, 'PROVINCE.md': _province(layout='little-endian squashfs')}, good],
        0, 1, want_fail='b:province_core_row')
    add('province row that names the round-41 AVM layout, not the marker',
        [{**frozen, 'PROVINCE.md': _province(layout='AVM layout')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row absent', [{**frozen, 'PROVINCE.md': _province(row=False)}, good],
        0, 1, want_fail='b:province_core_row')
    add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': _province(
            cited='corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md')}, good],
        0, 1, want_fail='b:province_core_row')
    add('frontier note absent', [{**frozen, 'PROVINCE.md': _province(note=False)}, good],
        0, 1, want_fail='b:frontier_note')
    add('frontier note without the LE-AVM token',
        [{**frozen, 'PROVINCE.md': (f'# P\n\n{CORE_HEADING}\n\n| Surface | Layout | a | Entry |\n'
                                    f'|---|---|---|---|\n| `squashfs_v4_le` | AVM marker | x | '
                                    f'`{ENTRY}` |\n\n## Next\n- {FRONTIER_MARK}: `{STEM}`.\n')},
         good], 0, 1, want_fail='b:frontier_note')
    add('frontier note with the round-41 BE token (AVM BE)',
        [{**frozen, 'PROVINCE.md': _province(token='AVM BE')}, good], 0, 1,
        want_fail='b:frontier_note')
    add('frontier note with the AVM-LE spelling is accepted',
        [{**frozen, 'PROVINCE.md': _province(token='AVM-LE')}, good], 0, 0)
    add('entry absent', [{**frozen, ENTRY: None}, good], 0, 1, want_fail='b:entry_present')
    add('S-id substring S1120', [{**frozen, ENTRY: _entry('S1120')}, good], 0, 1,
        want_fail='b:sourced')
    add('source row opened before the window',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-27')}, good], 0, 1,
        want_fail='b:sourced')
    add('source row opened after the window',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-30')}, good], 0, 1,
        want_fail='b:sourced')
    add('source row opened on the last day of the window (2026-10-29)',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-29')}, good], 0, 0)
    add('used-by lacks the entry',
        [{**frozen, 'corpus/SOURCES.md': _registry(used='corpus/lessons/round-49.md')},
         good], 0, 1, want_fail='b:sourced')
    add('coverage map lacks the stem',
        [{**frozen, 'corpus/README.md': _readme(stem='2026-10-26-r41-other')}, good], 0, 1,
        want_fail='b:coverage_map_row')

    fails = []
    green = red = 0
    discriminating = 0
    for p in path_probes:
        if p['new'] != p['want_new']:
            fails.append('probe %r: exact matcher %r, want %r'
                         % (p['desc'], p['new'], p['want_new']))
        if p['legacy'] != p['want_legacy']:
            fails.append('probe %r: round-40 matcher %r, want %r '
                         '(the legacy replica no longer mis-scores this shape)'
                         % (p['desc'], p['legacy'], p['want_legacy']))
        discriminating += p['new'] != p['legacy']
    if discriminating < 3:
        fails.append('only %d matcher probes discriminate exact from the '
                     'round-40 suffix rule, want >= 3' % discriminating)
    for p in root_probes:
        if (p['root'], p['source']) != (p['want_root'], p['want_src']):
            fails.append('root probe %r: (%r, %r), want (%r, %r)'
                         % (p['desc'], p['root'], p['source'],
                            p['want_root'], p['want_src']))
    for p in spec_probes:
        if p['ok'] != p['want_ok']:
            fails.append('spec probe %r: ok=%r want %r (problems %r)'
                         % (p['desc'], p['ok'], p['want_ok'], p['problems']))
        elif p['want_text'] and not any(p['want_text'] in x
                                        for x in p['problems']):
            fails.append('spec probe %r: no problem mentions %r (problems %r)'
                         % (p['desc'], p['want_text'], p['problems']))
    for c in cases:
        d = tempfile.mkdtemp(prefix='c1-selftest.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                                 capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            ident = ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
            revs = []
            def write_files(files):
                for p, content in files.items():
                    full = os.path.join(d, p)
                    if content is None:
                        if os.path.exists(full):
                            os.remove(full)
                        continue
                    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
                    data = content if isinstance(content, bytes) else content.encode()
                    with open(full, 'wb') as fh:
                        fh.write(data)

            def git_c(*a):
                subprocess.run(['git', '-C', d] + ident + list(a), check=True,
                               capture_output=True)

            for step, files in enumerate(c['steps']):
                if '__merge__' in files:
                    # a real merge: a side branch (optionally carrying `__side__`
                    # files), an unrelated commit on the first-parent line, then a
                    # --no-ff merge whose own commit carries the `__merge__` files
                    git_c('checkout', '-q', '-b', 'side')
                    write_files(files.get('__side__') or {'side.txt': b'side\n'})
                    git_c('add', '-A')
                    git_c('commit', '-qm', 'side%d' % step, '--allow-empty')
                    git_c('checkout', '-q', '-')
                    write_files({'main-%d.txt' % step: b'main\n'})
                    git_c('add', '-A')
                    git_c('commit', '-qm', 'main%d' % step)
                    git_c('merge', '--no-ff', '--no-commit', '-q', 'side')
                    write_files(files['__merge__'])
                    git_c('add', '-A')
                    git_c('commit', '-qm', 'merge%d' % step, '--allow-empty')
                    git_c('branch', '-q', '-D', 'side')
                elif '__ops__' in files:
                    # a scripted topology: ('write', files) / ('commit', msg) /
                    # ('git', args...)
                    for op in files['__ops__']:
                        if op[0] == 'write':
                            write_files(op[1])
                        elif op[0] == 'commit':
                            git_c('add', '-A')
                            git_c('commit', '-qm', op[1], '--allow-empty')
                        else:
                            git_c(*op[1:])
                else:
                    write_files(files)
                    subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
                    subprocess.run(['git', '-C', d] + ident
                                   + ['commit', '-qm', 'step%d' % step, '--allow-empty'],
                                   check=True)
                revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                                           capture_output=True, text=True).stdout.strip())
            fz = revs[c['freeze']]
            rv = revs[-1]
            try:
                res = measure(d, rv, fz, pkg65, rerun=c['runner'],
                              carrier_cache=c.get('cache'),
                              rederive=c.get('rederive')
                              or (lambda raw, cid, d=d: lane_rows(d, cid)))
                got = 0 if res['met_target'] else 1
                why = None
                failing = set()
                for k, v in res['carriers'].items():
                    failing |= {x for x in CLAUSES if v.get(x) is not True}
                failing |= {'b:' + x for x in BINDINGS if res['bindings'][x] is not True}
            except FrozenPathChanged as e:
                got, why, res, failing = 2, e.reason, None, set()
            except Unevaluable as e:
                got, why, res, failing = 2, e.reason, None, set()
            if os.environ.get('C1_SELFTEST_DETAIL'):
                if res is None:
                    detail = {'exit': got, 'reason': why}
                else:
                    detail = {
                        'exit': got,
                        'carriers_matched': res['carriers_matched'],
                        'failing': sorted(failing),
                        'failing_by_carrier': {
                            k: sorted(list({x for x in CLAUSES if v.get(x) is not True})
                                      + (['hits %r/%r' % (v.get('oracle_hits'),
                                                          v.get('oracle_files'))]
                                         if v.get('oracle_hits') != v.get('oracle_files')
                                         else []))
                            for k, v in res['carriers'].items()
                            if any(v.get(x) is not True for x in CLAUSES)
                            or v.get('oracle_hits') != v.get('oracle_files')},
                        'gaps_notes': {k: v.get('gaps_note')
                                       for k, v in res['carriers'].items()},
                        'bindings_false': sorted(x for x in BINDINGS
                                                 if res['bindings'][x] is not True),
                        'projection_diff': {k: v.get('projection_diff')
                                            for k, v in res['carriers'].items()
                                            if v.get('projection_diff')},
                        'drift': res['frozen_path_changed'],
                    }
                print('DETAIL\t%s\t%s' % (c['name'], json.dumps(detail)), file=sys.stderr)
            ok = got == c['want'] and (c['reason'] is None or why == c['reason'])
            if ok and c['want_fail'] and c['want_fail'] not in failing:
                ok = False
                fails.append('%s: want failing clause %r, failing=%r'
                             % (c['name'], c['want_fail'], sorted(failing)))
            if ok:
                green += got == 0
                red += got != 0
            else:
                detail = '' if why is None else ' (%s)' % why
                fails.append('%s: want %d got %d%s' % (c['name'], c['want'], got, detail))
        finally:
            shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({'selftest': 'c1-counter', 'cases': len(cases),
                      'green_ok': green, 'red_ok': red,
                      'path_probes': len(path_probes),
                      'path_probes_discriminating': discriminating,
                      'root_probes': len(root_probes),
                      'spec_probes': len(spec_probes),
                      'probe_results': path_probes + root_probes + spec_probes,
                      'failures': fails}))
    return 0 if not fails else 1


def lane_le_avm_image(work):
    """A lane-built little-endian AVM-marker SquashFS member, or an error string.

    mksquashfs (squashfs-tools 4.7.x, xz) writes a standard little-endian v4
    image; patching `mkfs_time` to `bytes_used` and truncating to `bytes_used`
    gives the frozen layout without any vendor bytes (unblob and sasquatch never
    read mkfs_time for a little-endian image)."""
    mk = shutil.which('mksquashfs')
    if mk is None:
        return None, 'mksquashfs not on PATH (pass --dev-image)'
    src = os.path.join(work, 'src')
    for rel, body in (('README.txt', b'dev tree readme\n' * 9),
                      ('etc/app.conf', b'k=v\n' * 40),
                      ('usr/share/doc/blob.bin', bytes(range(256)) * 17),
                      ('var/info.txt', b'info\n')):
        full = os.path.join(src, rel)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(body)
    os.symlink('app.conf', os.path.join(src, 'etc', 'app.link'))
    img = os.path.join(work, 'lane.sqsh')
    p = subprocess.run([mk, src, img, '-comp', 'xz', '-noappend', '-no-progress',
                        '-all-root', '-no-xattrs', '-quiet'], capture_output=True)
    if p.returncode != 0:
        return None, 'mksquashfs failed: %s' % p.stderr.decode(errors='replace')[:200]
    raw = bytearray(open(img, 'rb').read())
    used = int.from_bytes(raw[40:48], 'little')
    if not (0 < used <= len(raw)):
        return None, 'lane image has no usable bytes_used'
    raw[8:12] = (used & 0xFFFFFFFF).to_bytes(4, 'little')
    return bytes(raw[:used]), None


def selftest_rea(pkg65, unblob, timeout, dev_image=None):
    """Real-REA end-to-end: two runs of a little-endian AVM-marker member.

    The member is `--dev-image` (a real LE AVM member the caller supplies, NOT a
    C1 carrier unless the caller says so) or, when absent, a lane-built image
    (`lane_le_avm_image`). Builds a one-carrier fixture lane (target 1) whose
    committed receipt is the first real run, then measures it with the counter's
    real runner (second run) and expects met_target. Then replaces the receipt with
    an oracle-only fabrication and expects a projection mismatch. The run needs
    scratch under /fast/scratch/hyaku/kaidoku-r50/ (`run_provenance_ok`).
    Not exercised by the porting seat."""
    if not pkg65:
        raise SystemExit('--selftest-rea needs --pkg65')
    here = os.path.dirname(os.path.abspath(__file__))
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    sroot = scratch_root()
    work = tempfile.mkdtemp(prefix='c1-selftest-rea.', dir=sroot)
    out = {}
    if dev_image:
        if not os.path.isfile(dev_image):
            raise SystemExit('dev image absent: ' + dev_image)
        image = open(dev_image, 'rb').read()
        used = int.from_bytes(image[40:48], 'little')
        if not (0 < used <= len(image)):
            raise SystemExit('dev image has no usable bytes_used')
        image = image[:used]
        out['image'] = dev_image
    else:
        image, why = lane_le_avm_image(work)
        if image is None:
            raise SystemExit(why)
        out['image'] = 'lane-built (mksquashfs xz, mkfs_time patched to bytes_used)'
    pin = hashlib.sha256(image).hexdigest()
    out.update(image_sha256=pin, bytes=len(image), layout=layout_probe(image))
    if not out['layout'].get('ok'):
        raise SystemExit('the image does not read the frozen layout: %r'
                         % (out['layout'].get('reason'),))
    runner = make_real_runner(work, unblob, timeout, pkg65)

    # oracle from the independent extractor (unsquashfs; sasquatch is the
    # extractor under test, so it is not its own oracle)
    uq = shutil.which('unsquashfs')
    if uq is None:
        raise SystemExit('unsquashfs not on PATH')
    carrier = os.path.join(work, 'carrier.sqsh')
    with open(carrier, 'wb') as fh:
        fh.write(image)
    oroot = os.path.join(work, 'oracle')
    p = subprocess.run([uq, '-no-xattrs', '-f', '-d', oroot, carrier],
                       capture_output=True)
    oracle_rows, nonreg_rows = [], []
    for dirpath, dirs, names in os.walk(oroot):
        for name in sorted(names + dirs):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, oroot).replace(os.sep, '/')
            if os.path.islink(full):
                nonreg_rows.append((rel, 'symlink', os.readlink(full)))
            elif os.path.isfile(full):
                data = open(full, 'rb').read()
                oracle_rows.append((rel, hashlib.sha256(data).hexdigest(), len(data)))
    oracle_rows.sort()
    nonreg_rows.sort()
    oracle_tsv = ''.join('%s\t%s\t%d\n' % r for r in oracle_rows)
    nonreg_tsv = ''.join('%s\t%s\t%s\n' % r for r in nonreg_rows)
    out['unsquashfs_rc'] = p.returncode
    out['oracle_files'] = len(oracle_rows)
    out['nonregular_entries'] = len(nonreg_rows)

    # first real run -> committed receipt (the frozen parameters, as the data run uses)
    status, env = runner(image, 'g7581-committed', dict(FIXTURE_REA_PARAMETERS))
    if status != 'ok':
        raise SystemExit('first REA run produced no evidence object: %r' % (env,))
    out['committed_evidence_id'] = env.get('evidence_id')
    out['committed_handlers'] = [c.get('handler')
                                 for c in env['normalized_result'].get('chunks') or []]

    pkg_root = os.path.abspath(pkg65)
    lock = next((q for q in (
        os.path.join(os.path.dirname(pkg_root), 'package-lock.json'),
        os.path.join(os.path.dirname(os.path.dirname(pkg_root)), 'package-lock.json'))
        if os.path.isfile(q)), None)
    rea_doc = json.dumps({
        'schema': 'selftest', 'name': 'rea-agents', 'version': REA_VERSION,
        'package_json_sha256': file_sha256(os.path.join(pkg_root, 'package.json')),
        'package_lock_sha256': file_sha256(lock) if lock else None})
    gap_rule = json.dumps({
        'claim': 'R50-C1',
        'allowed': {'symlink': ['unpublished-entry'], 'char-device': [],
                    'block-device': [], 'fifo': ['unpublished-entry'],
                    'socket': ['unpublished-entry'], 'dir': []},
        'required': {'symlink': True, 'char-device': False, 'block-device': False,
                     'fifo': False, 'socket': False, 'dir': False},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive', 'silent': {}},
        'structural': {'depth-limited': 1, 'unknown-chunk-handler': 0}}, indent=1)
    cid = IDS[0]
    d = tempfile.mkdtemp(prefix='c1-selftest-rea-repo.', dir=sroot)
    try:
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        ident = ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
        frozen = {
            XPIN: xpin,
            CARRIERS: json.dumps({
                'claim': 'R50-C1', 'target': 1,
                'rea_parameters': dict(FIXTURE_REA_PARAMETERS),
                'carriers': [{'id': cid, 'path': '%s/%s/carrier.sqsh' % (AFTERDIR, cid),
                              'sha256': pin,
                              'oracle': '%s/%s/oracle.tsv' % (AFTERDIR, cid),
                              'nonregular': '%s/%s/nonregular.tsv' % (AFTERDIR, cid)}]},
                indent=1),
            GAPRULE: gap_rule,
            'plans/round-50-claims.md': '# plan\n',
            'tools/round-50/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
            'tools/round-50/rea-pkg.json': rea_doc,
            'PROVINCE.md': _province(),
            ENTRY: _entry('S240'),
            'corpus/SOURCES.md': _registry('S240', used=ENTRY),
            'corpus/README.md': _readme(STEM),
            '%s/%s/carrier.sqsh' % (AFTERDIR, cid): image,
            '%s/%s/oracle.tsv' % (AFTERDIR, cid): oracle_tsv.encode(),
            '%s/%s/nonregular.tsv' % (AFTERDIR, cid): nonreg_tsv.encode(),
        }
        revs = []

        def commit(files):
            for pth, content in files.items():
                full = os.path.join(d, pth)
                if content is None:
                    if os.path.exists(full):
                        os.remove(full)
                    continue
                os.makedirs(os.path.dirname(full) or d, exist_ok=True)
                data = content if isinstance(content, bytes) else content.encode()
                with open(full, 'wb') as fh:
                    fh.write(data)
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d] + ident
                           + ['commit', '-qm', 'step%d' % len(revs), '--allow-empty'],
                           check=True)
            revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                                       capture_output=True, text=True).stdout.strip())

        commit(frozen)
        commit({'%s/%s/after.json' % (AFTERDIR, cid): json.dumps(env)})
        freeze, rev = revs[0], revs[-1]

        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=(cid,), unblob=unblob, rea_timeout=timeout)
            got = 0 if res['met_target'] else 1
            out['green'] = {'exit': got, 'met_target': res['met_target'],
                            'carriers_matched': res['carriers_matched'],
                            'failing': sorted({x for x in CLAUSES
                                               if res['carriers'][cid].get(x) is not True}),
                            'bindings_false': sorted(x for x in BINDINGS
                                                     if res['bindings'][x] is not True),
                            'projection_diff': res['carriers'][cid].get('projection_diff'),
                            'gaps_note': res['carriers'][cid].get('gaps_note'),
                            'layout': res['carriers'][cid].get('layout')}
        except Unevaluable as e:
            out['green'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        # oracle-only fabrication: publish exactly the oracle, no chunk geometry
        # and no diagnostics (what a receipt built from the oracle tables alone
        # holds; the projection is a coarsening, so a fabrication that reproduced
        # the chunk geometry too would be semantically equal to a real run - that
        # is the documented limit of this binding, not a hole in it)
        fab = mk_env('carrier.sqsh', pin,
                     files=[(rel, h, size) for rel, h, size in oracle_rows],
                     chunks=[], diags=[],
                     outdir='/fast/scratch/hyaku/kaidoku-r50/selftest-rea/fab')
        fab['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': fab})['m']
        commit({'%s/%s/after.json' % (AFTERDIR, cid): json.dumps(fab)})
        rev = revs[-1]
        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=(cid,), unblob=unblob, rea_timeout=timeout)
            v = res['carriers'][cid]
            out['fabrication'] = {'exit': 0 if res['met_target'] else 1,
                                  'met_target': res['met_target'],
                                  'failing': sorted({x for x in CLAUSES
                                                     if v.get(x) is not True}),
                                  'projection_diff': v.get('projection_diff'),
                                  'evidence_id_ok': v.get('evidence_id_ok')}
        except Unevaluable as e:
            out['fabrication'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        g = out.get('green', {})
        ok = (g.get('carriers_matched') == 1 and g.get('failing') == []
              and g.get('bindings_false') == []
              and out.get('fabrication', {}).get('met_target') is False
              and 'projection_ok' in out.get('fabrication', {}).get('failing', []))
        out['selftest_rea'] = 'ok' if ok else 'FAILED'
        print(json.dumps(out, indent=1, sort_keys=True))
        return 0 if ok else 1
    finally:
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
