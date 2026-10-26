#!/usr/bin/env python3
"""R42-C1 counter (coverage: the SquashFS v3 handler family through REA -> Core).

Port of `tools/round-41/c1-counter.py` (round-42 seat R42C1Counter). The claims
text is `plans/round-42-claims.md` R42-C1; the predicate is embedded here clause
by clause:

  At the measured revision, for each frozen carrier, the committed round-42
  REA 6.5.0 `extract-firmware --max-depth 1` after-receipt (unblob 26.6.4,
  sasquatch 4.5.1 on the child PATH, never sasquatch-v4be), first added in a
  commit that descends from the freeze, names the carrier's frozen
  `squashfs_v3*` handler with no failed chunk, publishes every regular file of
  the frozen independent oracle at its exact relative path under the chunk
  extract root (segment-bounded, round-41 closure D5) with the same sha256 and
  size, publishes no non-regular oracle entry as a file, accounts for every
  non-regular oracle row by the frozen gap rule (one `unpublished-entry` gap or
  one `MaliciousSymlinkRemoved` diagnostic per symlink; devices and directories
  invisible; at most one structural `depth-limited`; no
  `unknown-chunk-handler`), has a subject digest equal to the carrier pin and
  recomputes its evidence id; the carrier bytes hash to the pin and their
  superblock reads the magic/major/minor/endianness/compression frozen per
  carrier, carved to exactly `bytes_used`; **and** a counter-time REA rerun of
  the same bytes has the same semantic projection as the committed receipt (a
  receipt fabricated from the oracle, however its evidence id is minted, cannot
  equal a real run); PROVINCE.md holds a `## Round-42 additions to Core` row
  naming the `squashfs_v3` handler family that cites the round-42 knowledge
  entry, which cites a SOURCES row opened 2026-10-26 whose used-by lists it; a
  round-42 frontier note supersedes the Frontier text for the v1-v3 family;
  corpus/README.md maps the entry stem; no frozen C1 path changed after the
  freeze.

Target: carriers_matched == 4 (ids frozen in carriers.json) and every binding
true.

Changes from the round-41 counter (all four are routed-defect repairs)
  (1) carrier layout      the AVM v4 layout probes (the `mkfs_time == bytes_used`
                          marker and the little-endian metadata header) are
                          replaced by a SquashFS v3 superblock probe driven by
                          the per-carrier frozen `superblock` block: family magic
                          bytes, `s_major`, minor, endianness, and the
                          compression class read from the inode table's first
                          compressed metadata block. `bytes_used` is now the
                          u64 at offset 63 (the packed v3 struct, verified
                          against squashfs-tools images) and `carve_ok` requires
                          the carve to be exactly `bytes_used` bytes.
  (2) handler binding     round 41 hardcoded `squashfs_v4_be` and accepted any
                          derivation edge whose handler starts `squashfs_v4`.
                          Here each carrier freezes its own v3-family handler
                          (`squashfs_v3[_ddwrt|_broadcom|_nonstandard]`); the
                          chunk must name it and the extract root is the
                          `derivations[]` edge whose handler equals it. No
                          prefix test, no default handler: a v4 handler on a v3
                          carrier fails `handler_ok` and leaves no root.
  (3) path rule           the exact relative-path rule is unchanged (R40-CL1),
                          and every prefix test is segment-bounded: `P == CR or
                          P.startswith(CR + '/')`, never `P.startswith(CR)`
                          (round-41 closure D5, `.ufo/waves/round-41/w2/
                          R41W2C1PathRule.md`). The two D5 findings are closed:
                          a removal diagnostic's `report.link` must sit under the
                          run's own extraction root (`dirname(output_directory)`),
                          so a decoy path segment-run no longer resolves, and a
                          receipt path with an empty / `.` / `..` component or a
                          trailing slash fails `path_shape_ok` instead of being
                          normalised into an oracle row.
  (4) receipt identity    every receipt this counter writes carries `counter`
                          and `counter_sha256` = sha256 of the counter file's own
                          bytes (round-41 closure D4: `counter_sha256 null` made
                          tool identity rest on a separate diff). `--verify-receipt`
                          re-checks a written receipt against the file it names.

The extract root (R40-CL1 repair; carried from round 41, per-carrier handler)
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
                       EQUALS the carrier's frozen handler
                       (FirmwareReports.js:341-357 taken from unblob's own
                       subtasks); a whole-file chunk's root is
                       `firmware.bin_extract` (`selected.bin_extract` under a
                       range selection), and a carved or nested chunk's root is
                       `<parent>/<start>-<end>.<handler>_extract`. Round 41
                       accepted any edge whose handler started `squashfs_v4`;
                       that prefix test is gone, so a receipt that extracted some
                       other SquashFS chunk cannot lend this carrier a root
    one root           the subject root is that root when the receipt has exactly
                       one; several roots of the carrier's handler are ambiguous
                       and the freeze can name the intended one with the optional
                       `oracle_root` key of the carrier entry, otherwise the
                       three path clauses fail closed with `extract_root: null`
    whole segments     `rel(P)` is `''` for P == root, `P[len(root)+1:]` for
                       `P.startswith(root + '/')`, else None - an entry outside
                       the root belongs to another namespace (a carve artifact of
                       the parent, a sibling root, a deeper root) and is neither
                       compared against this oracle nor reported as published.
                       The prefix test is segment-bounded in both directions: a
                       root `x_extract` does NOT own `x_extract2/...` (round-41
                       closure D5), which is why `under_root()` exists and why
                       the selftest pins it
    keyed by root      with one root per carrier the (root, rel) key collapses to
                       rel, and a path outside the root cannot satisfy a row
                       (R41C1Revenger C3: two roots carry `sbin/tool` with
                       different bytes)
  Round 40 matched with `candidate.endswith('/' + rel)` (defect R40-CL1: the
  regular file `usr/bin/busy` scored as the symlink entry `bin/busy`). Neither a
  suffix nor a fixed number of `_extract` segments is a root: a carve at a
  nonzero offset (`<root>/4096-6513.squashfs_v3_extract/...`) and a nested image
  (`<root>/nested/inner.squashfs_extract/...`) move the root as deep as the path
  to the chunk (R41C1Revenger C1/C2/C5).

Path shape (round-41 closure D5, second finding)
  A receipt path is a spelling, and a spelling that cannot name a regular file is
  not one: `path_shape_ok` requires every path the receipt normalises
  (`receipt_paths()`) to be `$input`, `$output/<rel>` or a bare `<rel>` whose
  components are non-empty, none is `.` or `..`, and which does not end in `/`.
  Round 41 normalised `firmware.bin_extract/var/info.txt/` and `/./` spellings
  into the oracle row `var/info.txt`; a trailing slash names a directory, so it
  fails closed here. The four committed round-41 receipts satisfy this rule
  unchanged (re-checked: 269/8188/28/29 receipt paths, 0 unclean).

Removal disposition (carried; the diagnostic path is now run-bound)
  unblob deletes escaping symlinks after reporting `MaliciousSymlinkRemoved`,
  deletes empty-target symlinks with no report at all, and never publishes a
  link as a regular file. The frozen gap rule may therefore carry a `removed`
  block; `gaps_ok` then becomes a three-family disposition check:
    path-resolved gap   kind allowed for that entry's kind (as before)
    removal             every diagnostic the rule names (`removed.diagnostic`)
                        must resolve at its exact path to a non-regular entry
                        whose kind is in `removed.kinds`, and no entry may be
                        both gapped and removed
    silent              an entry whose kind and oracle detail are listed under
                        `removed.silent` may carry no record at all; the check is
                        per row, so nothing else can hide behind the allowance
  A diagnostic's path is its `report.link`, an absolute path inside REA's private
  extraction root. Round 41 mapped it by searching for the root's segment run
  anywhere in the link, so `/scratch/decoy/firmware.bin_extract/bin/link`
  satisfied a required `bin/link` while the run wrote to
  `/scratch/run-V4/` (D5, first finding). The link is now bound to the run: it
  must start, segment-bounded, with `dirname(parameters.output_directory)` -
  measured on the committed round-41 receipts, where the run wrote to
  `<run>/extract` and unblob reported links under
  `<run>/rea-firmware-<uuid>/extracted/<root>/...` - and the root's segment run
  must appear after that prefix. No trusted prefix (relative or absent
  `output_directory`) means no resolution, which fails the check closed.
  With no `removed` block the clause behaves exactly as in round 40 (a required
  entry must be gapped).
  The rerun projection carries diagnostics as `[__typename__, rel]` instead of
  the typename alone, so a rerun that removed a *different* link no longer
  matches (R41C1DevCore 7.3).

Per-carrier clauses (all must hold; `matched` = conjunction):
  carrier_present          the carrier blob exists at REV
  carrier_pin_ok           sha256(bytes at REV) == the frozen pin
  carrier_fresh_ok         the pin is not one a previous C1 freeze already scored
                           (carriers.json `prior_pins` plus the previous round's
                           carrier table, both read at the freeze commit). The
                           claim's kill rule names relabelled round-41 receipts
                           as a control that must stop C1; without this clause a
                           rename is indistinguishable from new coverage
  layout_ok                the superblock is the v3 family image the table froze
                           (see layout_probe): the frozen 4 magic bytes, `s_major`
                           == 3 and the frozen minor, `bytes_used` (u64 at 63) in
                           (119, file size], `inode_table_start` and
                           `directory_table_start` inside the file, the 2-byte
                           metadata block header at `inode_table_start` decoding
                           as the superblock's endianness (length 1..8192, and
                           the single-block identity `its + 2 + len == dts` when
                           the opposite endianness is plausible too), and the
                           declared compression class present among the metadata
                           blocks of the inode table (zlib `78 xx` or LZMA
                           `5d 00 ..`). The round-41 AVM probes (BE `sqsh` v4.0,
                           `mkfs_time == bytes_used`, little-endian metadata
                           header) are gone: they describe a format v3 does not
                           have
  carve_ok                 the carrier is exactly the filesystem it claims: the
                           frozen carve `length` (external carrier) or the file
                           size (committed carrier) equals the superblock
                           `bytes_used` and the bytes are that length. A sloppy
                           carve leaves trailing bytes, unblob then stops the
                           chunk at the padding boundary or at `bytes_used`, the
                           chunk stops being the whole input and the oracle root
                           moves one `<start>-<end>.<handler>_extract` deeper
  oracle_ok                oracle.tsv parses (rel, sha256[, size]); >= 1 row; no
                           duplicate paths; every sha256 is 64 hex
  nonregular_ok            nonregular.tsv parses (rel, kind[, detail]); empty is
                           allowed; duplicate (rel, kind) rows are not
  receipt_present          corpus/evidence/round-42/c1/<id>/after.json parses
  receipt_fresh            its first-add commit at REV is a strict descendant of
                           --freeze (not the freeze commit itself)
  evidence_envelope_ok     the committed after-receipt is an REA evidence
                           envelope, not a score receipt: no `counter_sha256` or
                           `exit_code` key may appear in it (those belong to the
                           receipts this counter writes; a score receipt relabelled
                           as evidence would otherwise be indistinguishable)
  subject_pin_ok           subject.digest.sha256 == the frozen pin
  operation_ok             operation == extract_firmware and provider.id == unblob
  handler_ok               a chunk names the carrier's frozen v3-family handler
                           exactly (no prefix test, no default)
  chunks_ok                no chunk carries extraction_failed: true
  oracle_hits_ok           every oracle regular file is published at its exact
                           path under the chunk extract root (rel ==, sha256 ==
                           and size ==), the root taken from the receipt's
                           `derivations[]` edge for this carrier's handler
  gaps_ok                  disposition check: every extraction gap lands on
                           exactly one non-regular entry at its exact path and
                           its kind is allowed for that entry's kind; every
                           removal diagnostic the frozen rule names resolves to
                           a non-regular entry of a listed kind under the run's
                           own extraction root and no entry is both gapped and
                           removed; every entry the rule marks required carries
                           exactly one disposition (an allowed gap, a removal
                           diagnostic, or - only when the rule lists it under
                           `silent` - nothing at all)
  nonregular_unpublished_ok  no published regular file path equals a non-regular
                           entry path (a materialised symlink/device would both
                           publish the path and keep the gap); equality is exact
                           relative to the chunk extract root, so a deeper file
                           whose path merely ends with the entry path is not one
  path_shape_ok            every normalised receipt path is a legal spelling (see
                           `Path shape`): no empty/`.`/`..` component, no
                           trailing slash. Closes D5's second finding
  run_provenance_ok        parameters.output_directory names this round's scratch
                           segment (/kaidoku-r42/); `parameters` is inside the
                           hashed 6.5.0 semanticProjection, so it cannot be edited
                           without breaking evidence_id_ok
  evidence_id_ok           stored evidence id == the id recomputed under the
                           frozen rea-agents 6.5.0 rule (tools/round-27/
                           xpin-attribute.mjs, the package's own
                           semanticProjection)
  projection_ok            the counter's own REA run of the REV carrier bytes
                           (fresh scratch output directory) has the same
                           semantic projection as the committed receipt. Skipped
                           (and therefore false) when the carrier bytes or the
                           receipt are absent / the pin fails.

Non-vacuity bindings (properties of the frozen set, so they cannot be gamed after
the freeze):
  carriers_spec_ok         `target` frozen in carriers.json equals this counter's
                           target; exactly that many distinct ids; distinct pins;
                           id/path/sha256/oracle/nonregular/handler/superblock
                           present and well-formed; the handler is in the
                           `squashfs_v3` family and agrees with the frozen
                           variant (`squashfs_v3` for standard, `_ddwrt`,
                           `_broadcom`, `_nonstandard` otherwise); the superblock
                           block names a family magic, an endianness, major 3,
                           the matching variant and a compression class; an
                           external carrier also names `member_sha256` (and
                           `nested.sha256` when it has a `nested` block), so the
                           fetch chain is bound in the table rather than in the
                           fetcher (routed R40-CL6); an optional `oracle_root`
                           must be a relative path string and `prior_pins` a
                           list of 64-hex pins
  gap_rule_ok              gap-rule.json parses to {allowed: {kind: [gap kind]},
                           required?: {kind: bool}, removed?: {diagnostic, kinds,
                           disposition, silent?}, structural?: {kind: limit}};
                           every non-regular kind that appears in any frozen
                           nonregular.tsv is a key of `allowed`
  endianness_coverage      >= 1 carrier with the v3 little-endian family magic and
                           >= 1 with the big-endian family magic, so both
                           sasquatch legs (`-le`, `-be`) are bound. This replaces
                           round 41's gzip/xz binding: v3.0 has no compression id
                           field, and the extractor choice that matters here is
                           the endian flag
  frozen_tables_valid      carriers.json and gap-rule.json parse at the freeze
                           commit itself (routed R39-CL4)

Documentation bindings:
  province_core_section    PROVINCE.md has the `## Round-42 additions to Core`
                           heading
  province_core_row        a table row in that section whose first cell names a
                           `squashfs_v3*` handler, whose text names SquashFS v3
                           (squashfs[ _-]?v3) and cites the entry path
  frontier_note            one line carries `Round-42 frontier note`, the entry
                           stem and the SquashFS v3 token
  entry_present            the knowledge entry exists at REV
  sourced                  the entry's `source:` lines name an S-id whose
                           corpus/SOURCES.md row is opened 2026-10-26 and lists the
                           entry (path or stem) in used-by
  coverage_map_row         corpus/README.md `## Coverage map` maps the entry stem

Freeze-drift binding (routed defect R38-CL4, kept): if any commit in FREEZE..REV
touches plans/round-42-claims.md, tools/round-42/c1-counter.py,
tools/round-42/c1-extra.py, tools/round-42/c1-run.sh,
tools/round-42/fetch-carrier.py, tools/round-42/sqfs3-oracle.py,
.ufo/waves/round-42/c1/carriers.json, .ufo/waves/round-42/c1/gap-rule.json, or any
carrier/oracle/nonregular file carriers.json lists, the counter exits 2 with
reason `frozen_path_changed` and never reports met. A later restore does not
un-block (the log of the range is inspected, not the endpoints).

Receipt identity (round-41 closure D4)
  Every receipt this counter writes (`--json-out`, and the stdout summary is not
  a receipt) carries
      counter          the absolute path of the counter file that produced it
      counter_sha256   sha256 of that file's bytes
  so tool identity never rests on a separate `git diff`. `--verify-receipt PATH`
  re-reads a written receipt, hashes the file it names and exits 0 (match), 1
  (missing or mismatched key) or 2 (unreadable). The committed REA after-receipts
  must NOT carry the key: `counter_identity_ok` fails a receipt that mixes the
  two shapes, and the selftest pins both directions.

The rerun clause (routed R39-CL5)
  Between the receipt checks and the verdict, a carrier whose bytes hash to the
  pin and whose receipt parses is re-run by this counter:
      cwd = a private directory under $HYAKU_SCRATCH/kaidoku-r41,
      env REA_UNBLOB_COMMAND=<absolute unblob>, TMPDIR = that directory,
      argv = npx -y rea-agents@6.5.0 extract-firmware --format json
             --full-output <carrier bytes> <fresh outdir>
  and the fresh `.data` object is projected:

      projection = {subject_sha256,
                    files: sorted [path suffix after the chunk `*_extract`
                                   directory, sha256, size],
                    chunks: sorted [handler, range.offset, range.length,
                                    extraction_failed],
                    gaps: sorted [kind, path suffix, sorted dependencies],
                    unpublished_entries: sorted [kind, path suffix],
                    diagnostics: sorted multiset of report.__typename__}

  Everything that varies between two runs of the same bytes (absolute paths,
  output directory, evidence id, continuation ids, provider ids, timestamps,
  selection and analysis fields) is excluded; the field list is the one fixed by
  the R40C1Projection seat's item text (it is inlined here on purpose: scores
  must read frozen in-repo bytes, never a wave artifact). The chunk extract
  directory is normalised away because the receipt records a run made in another
  scratch tree. rea-agents 6.5.0 stages every input as `firmware.bin`
  (FirmwareFiles.snapshotFirmware: `join(root, "firmware.bin")`), so this
  normalisation is lossless: a rerun of the same bytes forms the same
  `firmware.bin_extract` directory, and the projection would compare equal
  without it.

  The comparison profile is frozen data: the optional `projection` key of
  carriers.json, default `plus-extractor` (the L1's ruling for this round).
  `core` is the draft's six fields and is oracle-closed - a forger holding the
  oracle and non-regular tables can reproduce it without running - while
  `plus-extractor` adds the extractor-determined fields (`derivations`, engine,
  published_bytes, coverage). All four profiles were measured stable across
  repeated real runs (artifacts: projection-profiles.json, depth-replay.json).

  The rerun also replays the extraction parameters recorded in the committed
  receipt (`parameters.max_depth`, `max_output_bytes`, `max_output_files`). A
  depth-1 extraction is `partial` with a different published set and an extra
  `depth-limited` gap, so a rerun at REA's default depth 3 could never match a
  depth-1 receipt; the replay is what makes the comparison about the image
  rather than about the flags.
  A carrier whose rerun produces a different projection fails `projection_ok`
  and is reported with the differing projection keys (`projection_diff`); a
  rerun that cannot run at all (no npx/node/unblob, unusable REA output) is
  unevaluable (exit 2 `rerun_env_error`), never met.
  `--no-rerun` is not a mode of the predicate: it exits 2 (`rerun_disabled`) and
  never reports met.

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT
                [--json-out PATH] [--unblob PATH] [--rea-timeout SECONDS]
                [--carrier-cache DIR] [--work DIR]
  c1-counter.py --selftest  --pkg65 REA650_PKG_ROOT
  c1-counter.py --selftest-rea --pkg65 REA650_PKG_ROOT --dev-carrier PATH
                [--unblob PATH] [--rea-timeout SECONDS]
  c1-counter.py --verify-receipt PATH
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed, rerun environment error, --no-rerun). Reads lane bytes only
through git objects (`git show REV:path`); writes only a private scratch dir
under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/kaidoku-r42/counter, or
--work, and --json-out.

`--selftest` is offline and deterministic: it drives measure() in-process with a
simulated REA runner (the simulator only exists inside selftest(); main() never
passes anything but the real runner). Its fixture carriers are synthetic v3
superblocks, which is exactly what `layout_probe` tests. `--selftest-rea` is the
real-path check: it runs REA 6.5.0 twice on the SquashFS v3 image named by
--dev-carrier (a development input the caller has established it may run REA on -
an unblob 26.6.4 test fixture or the OpenWrt Kamikaze 7.09 development image,
NEVER a published C1 candidate), builds a one-carrier fixture lane around the
first run, asserts a green verdict under the second, then replaces the receipt
with an oracle-only fabrication and asserts it red.
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

CARRIERS = '.ufo/waves/round-42/c1/carriers.json'
GAPRULE = '.ufo/waves/round-42/c1/gap-rule.json'
AFTERDIR = 'corpus/evidence/round-42/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md'
STEM = '2026-10-26-r42-squashfs-v3-core'
CORE_HEADING = '## Round-42 additions to Core'
FRONTIER_MARK = 'Round-42 frontier note'
DEFAULT_HANDLER = 'squashfs_v3'         # only for selftest fixtures
XPIN = 'tools/round-27/xpin-attribute.mjs'
PRIOR_PINS = 'tools/round-42/prior-pins.json'      # frozen union of rounds 38-41
REA_PKG = 'tools/round-42/rea-pkg.json'            # frozen digest of the REA package
OPENED = '2026-10-26'
TARGET = 4
IDS = ()                                # ids are frozen data in carriers.json
PROV_SEGMENT = '/kaidoku-r42/'
REA_PIN = 'rea-agents@6.5.0'
REA_VERSION = '6.5.0'
METADATA_MAX = 8192
UNCOMPRESSED_FLAG = 0x8000
# H1: the REA child and the counter's own node/npx lookups use one fixed PATH, so
# a seat's shim directory cannot be what "sasquatch" resolves to during a score.
FIXED_PATH = ':'.join(['/usr/local/bin', '/usr/bin', '/bin',
                       os.path.expanduser('~/.local/bin'),
                       # L1 freeze amendment: npx is not under /usr/bin on this host;
                       # the fnm node install dir is the stable location (c1-run.sh uses
                       # the identical string).
                       os.path.expanduser('~/.local/share/fnm/node-versions/v24.21.0/installation/bin')])
FROZEN_PATHS = (
    'plans/round-42-claims.md',
    'tools/round-42/c1-counter.py',
    'tools/round-42/c1-extra.py',
    'tools/round-42/c1-run.sh',
    'tools/round-42/fetch-carrier.py',
    'tools/round-42/sqfs3-oracle.py',
    'tools/round-42/unblob-logtee.sh',
    XPIN,
    PRIOR_PINS,
    REA_PKG,
    CARRIERS,
    GAPRULE,
)
# SquashFS v3 family: four unblob 26.6.4 handlers share one superblock layout and
# differ only in the 4 magic bytes. `hsqs`/`sqsh` is plain v3 (the pair the two
# non-sasquatch readers on PATH, unsquashfs 4.7.5 and 7z, both accept); the other
# three are vendor variants that need a lane reader for the oracle.
MAGIC_BY_VARIANT = {
    'standard': {'le': b'hsqs', 'be': b'sqsh'},
    'ddwrt': {'le': b'hsqt', 'be': b'tqsh'},
    'broadcom': {'le': b'shqs', 'be': b'qshs'},
    'nonstandard': {'le': b'zlqs', 'be': b'sqlz'},
}
HANDLER_BY_VARIANT = {
    'standard': 'squashfs_v3',
    'ddwrt': 'squashfs_v3_ddwrt',
    'broadcom': 'squashfs_v3_broadcom',
    'nonstandard': 'squashfs_v3_nonstandard',
}
VARIANT_BY_HANDLER = {h: v for v, h in HANDLER_BY_VARIANT.items()}
ENDIANNESSES = ('le', 'be')
COMPRESSIONS = ('gzip', 'lzma')
SQUASHFS3_SB_SIZE = 119                 # packed squashfs_super_block (v3)
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])squashfs_v3(_[a-z]+)?(?![A-Za-z0-9_-])')
SQFS3_TEXT_RE = re.compile(r'squashfs[ _-]?v3|squashfs\s+3', re.IGNORECASE)
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
            'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
            'gap_rule_ok', 'endianness_coverage', 'carrier_sources_ok',
            'frozen_tables_valid', 'extractor_bin_ok')
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'carrier_fresh_ok',
           'fetch_receipt_ok', 'layout_ok', 'carve_ok', 'oracle_ok',
           'nonregular_ok', 'receipt_present', 'receipt_fresh',
           'evidence_envelope_ok', 'extract_env_ok', 'subject_pin_ok',
           'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok',
           'gaps_ok', 'nonregular_unpublished_ok', 'path_shape_ok',
           'run_provenance_ok', 'evidence_id_ok', 'projection_ok')


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


def which_fixed(name):
    """Absolute path of `name` under FIXED_PATH, or None.

    The child PATH of a scored REA run is FIXED_PATH, so resolving through the
    caller's PATH would let a shim directory decide which `sasquatch`, `node` or
    `npx` the score uses (R42C1Sentinel H1/X2)."""
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


WORK_OVERRIDE = None


def scratch_root():
    """Private scratch directory for counter runs.

    $HYAKU_SCRATCH (or --work) decides; nothing is ever written to a hardcoded
    /tmp path."""
    if WORK_OVERRIDE:
        os.makedirs(WORK_OVERRIDE, exist_ok=True)
        return WORK_OVERRIDE
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                     'kaidoku-r42', 'counter')
    os.makedirs(d, exist_ok=True)
    return d


# ------------------------------------------------------------- receipt identity

def counter_identity(path=None):
    """(counter path, sha256 of its bytes) for the counter that writes a receipt.

    Round-41 closure D4: score receipts recorded `counter_sha256 null`, so tool
    identity rested on a separate `git diff` of the frozen path. The digest is of
    the counter file itself (the tool), which is what a reader can re-hash from
    the revision it names."""
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
    """(ok, why) for a receipt this counter wrote: key present and honest.

    A missing or null `counter_sha256`, a non-hex digest, or a digest that does
    not describe the file named by `counter` is a failure; an unreadable counter
    file is a failure too (a receipt must be checkable offline)."""
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

def rea_package_problems(root, freeze, pkg65):
    """(problems, doc) for the frozen rea-pkg.json against the live package.

    R42C1Sentinel H4: `--pkg65` is a mutable directory under the npm cache, so a
    byte-identical xpin tool can still hash under a rewritten rule. The freeze
    pins `package.json` and `package-lock.json` digests and the version; the
    counter refuses a package whose bytes differ. (`tree_sha256` is not
    recomputed here: the freeze's canonical form is not defined by this file, so
    the two unambiguous digests are what is checked.)"""
    raw = show(root, freeze, REA_PKG)
    if raw is None:
        return ['rea-pkg.json absent at freeze'], None
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return ['rea-pkg.json is not JSON: %s' % e], None
    if not isinstance(doc, dict):
        return ['rea-pkg.json is not an object'], None
    probs = []
    if doc.get('version') != REA_VERSION:
        probs.append('rea-pkg.json version %r != %r' % (doc.get('version'), REA_VERSION))
    pkg_root = os.path.abspath(pkg65)
    lock_candidates = [os.path.join(os.path.dirname(pkg_root), 'package-lock.json'),
                       os.path.join(os.path.dirname(os.path.dirname(pkg_root)),
                                    'package-lock.json')]
    lock_path = next((p for p in lock_candidates if os.path.isfile(p)), None)
    candidates = (('package.json', os.path.join(pkg_root, 'package.json'),
                   'package_json_sha256'),
                  ('package-lock.json', lock_path, 'package_lock_sha256'))
    for name, path, key in candidates:
        want = doc.get(key)
        if not (isinstance(want, str) and SHA_RE.match(want.lower())):
            probs.append('rea-pkg.json %s is not 64 hex' % key)
            continue
        got = file_sha256(path) if path else None
        if got is None:
            probs.append('%s unreadable beside --pkg65' % name)
        elif got != want.lower():
            probs.append('%s sha256 %s != frozen %s' % (name, got, want))
    return probs, doc


def evidence_ids(root, freeze, pkg65, envelopes, work):
    """Recompute the stored evidence id under the rea-agents 6.5.0 rule.

    The rule is not retyped: the frozen xpin tool evaluates the package's own
    `semanticProjection` and hashes it with the package's own digest code. Both
    the tool (a frozen path) and the package (its frozen digests) are bound, and
    `node` is resolved under FIXED_PATH so the interpreter is not a caller's."""
    probs, _doc = rea_package_problems(root, freeze, pkg65)
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
    """(rows[(rel, sha256, size|None)], error) for oracle.tsv.

    `tools/round-42/sqfs3-oracle.py` writes `relpath TAB sha256 TAB size` (the
    round-41 format); the size column is optional for older tables and is
    compared when present."""
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'row %r has %d fields, want >= 2 (rel, sha256[, size])' % (line, len(f))
        rel = f[0].strip()
        sha = f[1].strip().lower()
        if not rel:
            return [], 'empty path in %r' % (line,)
        if not SHA_RE.match(sha):
            return [], 'row %r sha256 is not 64 lowercase hex' % (line,)
        size = None
        if len(f) > 2 and f[2].strip():
            try:
                size = int(f[2].strip())
            except ValueError:
                return [], 'row %r size is not an int' % (line,)
            if size < 0:
                return [], 'row %r size is negative' % (line,)
        rows.append((rel, sha, size))
    if not rows:
        return [], 'no rows'
    seen = set()
    for rel, _h, _s in rows:
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
    if claim is not None and claim != 'R42-C1':
        probs.append('claim %r != R42-C1' % (claim,))
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
    """(ids, problems) for the frozen carrier list.

    Round 42 schema (R42C1Sentinel H2): every carrier is a PUBLISHED third-party
    image, so it must carry `external` (a committed `path` is the round-41
    lane-built shape and is rejected), `kind: "published"`, the SOURCES row that
    documents it (`source_id`), a frozen `fetch-<id>.json` receipt, its own
    `handler` and `superblock`, and both tables. `toolchain` pins the extractor
    and unblob digests the `extractor_bin_ok` binding recomputes."""
    probs = []
    if 'claim' in spec and spec.get('claim') != 'R42-C1':
        probs.append('claim %r != R42-C1' % (spec.get('claim'),))
    toolchain = spec.get('toolchain')
    if not isinstance(toolchain, dict):
        probs.append('`toolchain` must be an object pinning the extractors')
    else:
        for name in ('sasquatch', 'unblob'):
            entry = toolchain.get(name)
            if not isinstance(entry, dict):
                probs.append('toolchain.%s must be an object' % name)
                continue
            pin = entry.get('sha256')
            if not (isinstance(pin, str) and SHA_RE.match(pin.lower())):
                probs.append('toolchain.%s.sha256 is not 64 hex' % name)
        v4be = toolchain.get('sasquatch_v4be')
        if v4be is not None:
            if not isinstance(v4be, dict):
                probs.append('toolchain.sasquatch_v4be must be an object')
            elif not (isinstance(v4be.get('sha256'), str)
                      and SHA_RE.match(v4be['sha256'].lower())):
                probs.append('toolchain.sasquatch_v4be.sha256 is not 64 hex')
    cs = spec.get('carriers')
    if not isinstance(cs, list):
        return [], probs + ['carriers is not a list']
    if 'target' in spec and spec.get('target') != target:
        probs.append('frozen target %r != counter target %d' % (spec.get('target'), target))
    prof = spec.get('projection', DEFAULT_PROFILE)
    if prof not in PROFILES:
        probs.append('projection profile %r not in %r' % (prof, list(PROFILES)))
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
    if expected_ids and set(ids) != set(expected_ids):
        probs.append('carrier ids %r != %r' % (sorted(map(str, ids)), list(expected_ids)))
    pins = [c.get('sha256') for c in cs if isinstance(c, dict)]
    if len(set(pins)) != len(pins):
        probs.append('duplicate carrier pins')
    for c in cs:
        if not isinstance(c, dict):
            probs.append('non-object carrier entry')
            continue
        ext = c.get('external')
        keys = ('id', 'sha256', 'oracle', 'nonregular', 'handler', 'superblock',
                'kind', 'source_id', 'fetch_receipt')
        for key in keys:
            v = c.get(key)
            if not isinstance(v, (str, dict)):
                probs.append('carrier %r lacks %s' % (c.get('id'), key))
            elif isinstance(v, str) and not v:
                probs.append('carrier %r lacks %s' % (c.get('id'), key))
        if ext is None:
            probs.append('carrier %r has no external block: C1 carriers are '
                         'published third-party images, never a committed file '
                         '(a `path` carrier is the round-41 lane-built shape)'
                         % (c.get('id'),))
        if c.get('kind') != 'published':
            probs.append('carrier %r kind %r is not "published"'
                         % (c.get('id'), c.get('kind')))
        sid = c.get('source_id')
        if not (isinstance(sid, str) and SID_RE.match(sid)):
            probs.append('carrier %r source_id %r is not an S-id'
                         % (c.get('id'), sid))
        fr = c.get('fetch_receipt')
        if not (isinstance(fr, str) and fr and not fr.startswith('/')
                and '..' not in fr.split('/')):
            probs.append('carrier %r fetch_receipt is not a relative path'
                         % (c.get('id'),))
        if ext is not None:
            # External carriers (published vendor/distribution images that are not
            # redistributable) are pinned by URL -> image sha256 -> member ->
            # carve length -> carrier sha256 and fetched into --carrier-cache by
            # tools/round-42/fetch-carrier.py.
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
                url = ext.get('url')
                if not (isinstance(url, str) and url.startswith('https://')):
                    probs.append('carrier %r external url %r is not https'
                                 % (c.get('id'), url))
                offset = ext.get('offset')
                if offset is not None and not (isinstance(offset, int)
                                               and not isinstance(offset, bool)
                                               and offset >= 0):
                    probs.append('carrier %r external offset is not a '
                                 'non-negative int' % (c.get('id'),))
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
        # R42-C1: the carrier freezes its own handler and superblock. The handler
        # must be one of the four unblob 26.6.4 v3 handlers and must agree with
        # the frozen variant; the superblock block must name a family magic, an
        # endianness, major 3, the matching variant and a compression class. A v4
        # handler here is a table defect, never a carrier (routed round-41
        # hardcoded `squashfs_v4_be`).
        handler = c.get('handler')
        variant = None
        if not isinstance(handler, str) or handler not in VARIANT_BY_HANDLER:
            probs.append('carrier %r handler %r is not a squashfs_v3 family handler %r'
                         % (c.get('id'), handler, sorted(VARIANT_BY_HANDLER)))
        else:
            variant = VARIANT_BY_HANDLER[handler]
        sb = c.get('superblock')
        if not isinstance(sb, dict):
            probs.append('carrier %r lacks a superblock block' % (c.get('id'),))
        else:
            magic = sb.get('magic')
            endian = sb.get('endianness')
            if endian not in ENDIANNESSES:
                probs.append('carrier %r superblock.endianness %r is not le/be'
                             % (c.get('id'), endian))
            if not (isinstance(magic, str) and len(magic.encode('latin1', 'replace')) == 4):
                probs.append('carrier %r superblock.magic is not 4 bytes'
                             % (c.get('id'),))
            elif endian in ENDIANNESSES:
                implied = next((v for v, pair in MAGIC_BY_VARIANT.items()
                                if pair.get(endian) == magic.encode('latin1')), None)
                if implied is None:
                    probs.append('carrier %r superblock.magic %r is not a v3 family '
                                 'magic for %s' % (c.get('id'), magic, endian))
                elif sb.get('variant') is not None and sb.get('variant') != implied:
                    probs.append('carrier %r superblock.variant %r contradicts magic %r'
                                 % (c.get('id'), sb.get('variant'), magic))
                elif variant is not None and implied != variant:
                    probs.append('carrier %r handler %r is the %r variant but the '
                                 'superblock magic is %r'
                                 % (c.get('id'), handler, variant, implied))
            if sb.get('major') != 3:
                probs.append('carrier %r superblock.major %r is not 3'
                             % (c.get('id'), sb.get('major')))
            minor = sb.get('minor')
            if minor is not None and not (isinstance(minor, int)
                                          and not isinstance(minor, bool)
                                          and minor >= 0):
                probs.append('carrier %r superblock.minor is not a non-negative int'
                             % (c.get('id'),))
            if sb.get('compression') not in COMPRESSIONS:
                probs.append('carrier %r superblock.compression %r not in %r'
                             % (c.get('id'), sb.get('compression'),
                                list(COMPRESSIONS)))
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

def sb_u(raw, off, width, endian):
    """An unsigned superblock field, read with the filesystem's endianness."""
    return int.from_bytes(raw[off:off + width], 'big' if endian == 'be' else 'little')


def compression_class(chunk):
    """`gzip` / `lzma` for the first bytes of a compressed block, else None.

    v3 stored zlib streams (`78 01/5e/9c/da`) and, in the LZMA variants,
    LZMA-alone streams (`5d 00 ..`, or the 5-byte-props form `00 00 80 00`)."""
    if len(chunk) >= 2 and chunk[0] == 0x78 and chunk[1] in (0x01, 0x5E, 0x9C, 0xDA):
        return 'gzip'
    if chunk[:2] == b'\x5d\x00' or chunk[:4] == b'\x00\x00\x80\x00':
        return 'lzma'
    # L1 freeze amendment (QUALITY 84 dry run, `.ufo/waves/round-42/l1/dryrun-c1-pre.json`):
    # the OpenWrt Kamikaze and DD-WRT v24 squashfs-lzma 3.0 writers store metadata
    # blocks as RAW LZMA1 streams (no props header; the range coder's first byte is
    # 0x00), so the header test above read all four frozen carriers as undetermined.
    # Witness behaviourally: a block that raw-LZMA1-decodes (lc 3, lp 0, pb 2, the
    # sqlzma defaults) without error and is not a zlib stream is `lzma`.
    import lzma as _lzma
    import zlib as _zlib
    try:
        _zlib.decompress(chunk)
        return 'gzip'
    except Exception:
        pass
    if chunk[:1] == b'\x00':
        try:
            dec = _lzma.LZMADecompressor(format=_lzma.FORMAT_RAW, filters=[
                {'id': _lzma.FILTER_LZMA1, 'lc': 3, 'lp': 0, 'pb': 2, 'dict_size': 1 << 23}])
            if dec.decompress(chunk, max_length=8192):
                return 'lzma'
        except Exception:
            pass
    return None


def round_up(value, multiple):
    return ((value + multiple - 1) // multiple) * multiple


def chunk_end(raw, bytes_used, start=0):
    """unblob 26.6.4's chunk end for a SquashFS chunk at `start`, or None.

    `_SquashFSBase.calculate_chunk` (unblob 26.6.4 handlers/filesystem/
    squashfs.py:96-115) seeks to `start + bytes_used`, reads up to
    `round_up(bytes_used, 4096) - bytes_used` bytes, and for pad_size in
    (4096, 1024) returns `start + round_up(bytes_used, pad_size)` when that many
    tail bytes are zero, else `start + bytes_used`. The REA input is the carved
    extent of exactly this length (L1 ruling, round 42 w1), so `carve_ok`
    compares against it rather than against `bytes_used` alone."""
    if not isinstance(bytes_used, int) or isinstance(bytes_used, bool) or bytes_used <= 0:
        return None
    if not isinstance(start, int) or start < 0:
        return None
    end_of_data = start + bytes_used
    if end_of_data > len(raw):
        return None
    span = min(len(raw), start + round_up(bytes_used, 4096)) - end_of_data
    padding = raw[end_of_data:end_of_data + span]
    for pad_size in (4096, 1024):
        size = round_up(bytes_used, pad_size)
        pad_len = size - bytes_used
        if pad_len <= 0:
            continue
        if padding[:pad_len] == b'\x00' * pad_len:
            return start + size
    return end_of_data


def metadata_blocks(raw, start, stop, endian):
    """[(offset, length, uncompressed)] walking the metadata chain [start, stop).

    A metadata block is a 2-byte header (bit 15 = stored uncompressed, bits 0..14
    = length) followed by that many bytes, in the filesystem's endianness - the
    AVM little-endian header of round 41 is a v4-BE vendor quirk and does not
    exist in v3."""
    out = []
    o = start
    while o + 2 <= stop and o + 2 <= len(raw):
        header = sb_u(raw, o, 2, endian)
        length = header & ~UNCOMPRESSED_FLAG
        if not (1 <= length <= METADATA_MAX):
            break
        out.append((o, length, bool(header & UNCOMPRESSED_FLAG)))
        o += 2 + length
    return out


def layout_probe(raw, expect=None):
    """Decode a SquashFS v3 superblock and check it against the frozen block.

    squashfs_super_block (v3, packed, 119 bytes; verified field by field against
    squashfs-tools images in both endiannesses): magic 0:4, inodes 4:8,
    bytes_used_2 8:12, uid_start_2 12:16, guid_start_2 16:20,
    inode_table_start_2 20:24, directory_table_start_2 24:28, s_major 28:30,
    s_minor 30:32, block_size_1 32:34, block_log 34:36, flags 36, no_uids 37,
    no_guids 38, mkfs_time 39:43 (unaligned: the struct is packed), root_inode
    43:51, block_size 51:55, fragments 55:59, fragment_table_start_2 59:63,
    bytes_used 63:71, uid_start 71:79, guid_start 79:87, inode_table_start 87:95,
    directory_table_start 95:103, fragment_table_start 103:111,
    lookup_table_start 111:119.

    v3 has no compression-id field, no `mkfs_time == bytes_used` marker and no
    little-endian metadata header: the format signals are the 4 magic bytes
    (which also pick the unblob handler variant), major/minor, the endianness the
    fields decode with, and the compression class of the inode table's metadata
    blocks. Every expected value comes from the carrier's frozen `superblock`
    block - the probe never supplies a default."""
    d = {'size': len(raw) if raw is not None else 0, 'declared': expect}
    if raw is None:
        d.update(ok=False, reason='absent')
        return d
    if not isinstance(expect, dict):
        d.update(ok=False, reason='no frozen superblock block')
        return d
    if len(raw) < SQUASHFS3_SB_SIZE:
        d.update(ok=False, reason='shorter than the 119-byte v3 superblock')
        return d
    d['magic'] = raw[0:4].decode('latin1')
    endian = expect.get('endianness')
    d['endianness'] = endian
    if endian not in ENDIANNESSES:
        d.update(ok=False, reason='frozen endianness %r is not le/be' % (endian,))
        return d
    d['major'] = sb_u(raw, 28, 2, endian)
    d['minor'] = sb_u(raw, 30, 2, endian)
    d['block_size'] = sb_u(raw, 51, 4, endian)
    d['block_log'] = sb_u(raw, 34, 2, endian)
    d['flags'] = raw[36]
    d['bytes_used'] = bu = sb_u(raw, 63, 8, endian)
    d['inode_table_start'] = its = sb_u(raw, 87, 8, endian)
    d['directory_table_start'] = dts = sb_u(raw, 95, 8, endian)
    d['fragment_table_start'] = sb_u(raw, 103, 8, endian)
    d['lookup_table_start'] = sb_u(raw, 111, 8, endian)
    d['bytes_used_sane'] = SQUASHFS3_SB_SIZE <= bu <= len(raw)
    d['chunk_end'] = chunk_end(raw, bu) if d['bytes_used_sane'] else None
    d['starts_sane'] = bool(d['bytes_used_sane'] and SQUASHFS3_SB_SIZE <= its < dts <= bu)
    d['meta_header_hex'] = None
    d['meta_len'] = d['meta_len_other'] = None
    d['meta_signal'] = 'none'
    d['meta_identity'] = False
    d['meta_identity_other'] = False
    d['compression'] = None
    d['compression_signatures'] = {}
    if d['starts_sane']:
        other = 'le' if endian == 'be' else 'be'
        hdr = raw[its:its + 2]
        d['meta_header_hex'] = hdr.hex()
        length = int.from_bytes(hdr, 'big' if endian == 'be' else 'little')
        length_other = int.from_bytes(hdr, 'big' if other == 'be' else 'little')
        d['meta_len'] = length & ~UNCOMPRESSED_FLAG
        d['meta_len_other'] = length_other & ~UNCOMPRESSED_FLAG
        plausible = 1 <= d['meta_len'] <= METADATA_MAX
        plausible_other = 1 <= d['meta_len_other'] <= METADATA_MAX
        d['meta_identity'] = its + 2 + d['meta_len'] == dts
        d['meta_identity_other'] = its + 2 + d['meta_len_other'] == dts
        if plausible and not plausible_other:
            d['meta_signal'] = 'plausibility'
        elif plausible and plausible_other:
            # both decodes plausible: only the single-block identity separates them
            d['meta_signal'] = 'identity' if (d['meta_identity']
                                              and not d['meta_identity_other']) \
                else 'ambiguous'
            if d['meta_signal'] == 'ambiguous':
                # L1 freeze amendment (QUALITY 84 dry run, DEV-DWMINI: first header
                # 0x0606 reads 1542 both ways): walk the WHOLE inode-table chain in
                # each byte order; the order whose chain lands exactly on
                # directory_table_start is the witness, the other must not land.
                def _lands(order):
                    blocks = metadata_blocks(raw, its, dts, order)
                    return bool(blocks) and blocks[-1][0] + 2 + blocks[-1][1] == dts
                d['chain_lands'] = _lands(endian)
                d['chain_lands_other'] = _lands(other)
                if d['chain_lands'] and not d['chain_lands_other']:
                    d['meta_signal'] = 'chain'
        else:
            d['meta_signal'] = 'other' if plausible_other else 'neither'
        sigs = {}
        for off, blen, unc in metadata_blocks(raw, its, dts, endian):
            if unc:
                continue
            cls = compression_class(raw[off + 2:off + 2 + blen])
            if cls:
                sigs[cls] = sigs.get(cls, 0) + 1
        d['compression_signatures'] = sigs
        if sigs:
            d['compression'] = max(sorted(sigs), key=lambda k: sigs[k])
    variants = {v: pair for v, pair in MAGIC_BY_VARIANT.items()}
    d['variant_implied'] = next(
        (v for v, pair in variants.items() if pair.get(endian) == raw[0:4]), None)
    reason = None
    magic = expect.get('magic')
    if not isinstance(magic, str) or len(magic.encode('latin1', 'replace')) != 4:
        reason = 'frozen superblock has no 4-byte magic'
    elif raw[0:4] != magic.encode('latin1'):
        reason = 'magic %r is not the frozen %r' % (d['magic'], magic)
    elif d['variant_implied'] is None:
        reason = 'magic %r is not a v3 family magic for %s' % (d['magic'], endian)
    elif expect.get('variant') is not None and d['variant_implied'] != expect['variant']:
        reason = 'magic %r implies variant %r, frozen %r' % (
            d['magic'], d['variant_implied'], expect.get('variant'))
    elif d['major'] != 3:
        reason = 's_major %d is not 3' % d['major']
    elif expect.get('minor') is not None and d['minor'] != expect.get('minor'):
        reason = 's_minor %d is not the frozen %r' % (d['minor'], expect.get('minor'))
    elif not d['bytes_used_sane']:
        reason = 'bytes_used %d outside 119..%d' % (d['bytes_used'], len(raw))
    elif not d['starts_sane']:
        reason = 'inode/directory table starts %d/%d outside the filesystem (%d)' % (
            d['inode_table_start'], d['directory_table_start'], d['bytes_used'])
    elif d['meta_signal'] in ('neither', 'other'):
        reason = ('first metadata block length does not decode %s-endian (%s, '
                  'len %r)' % (endian, d['meta_signal'], d['meta_len']))
    elif d['meta_signal'] == 'ambiguous':
        reason = ('metadata length plausible both ways and the single-block '
                  'identity does not settle it (len %r vs %r, its %d, dts %d)'
                  % (d['meta_len'], d['meta_len_other'], its, dts))
    elif not d['compression_signatures']:
        reason = ('compression undetermined: no compressed metadata block in the '
                  'inode table (flags 0x%02x)' % d['flags'])
    elif (expect.get('compression') is not None
          and expect.get('compression') not in d['compression_signatures']):
        reason = 'compression %r absent from the inode table signatures %r' % (
            expect.get('compression'), d['compression_signatures'])
    d['ok'] = reason is None
    d['reason'] = reason
    return d


# ------------------------------------------------------------- receipt shape

def provenance_ok(output_directory):
    """A receipt run by this round: absolute, inside the kaidoku-r42 scratch
    segment, and without a `..` segment that could leave it."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:
        return False
    return '..' not in output_directory.split('/')


def trusted_run_root(output_directory):
    """The trusted directory a run's private extraction tree lives under.

    Measured on the committed round-41 receipts: `parameters.output_directory` is
    `<run>/extract` while unblob's `MaliciousSymlinkRemoved.link` is
    `<run>/rea-firmware-<uuid>/extracted/<root>/<rel>` (rea-agents 6.5.0
    FirmwareCommand.js:54, FirmwareProvider.js:151). `dirname(output_directory)`
    is therefore the component-bounded prefix that binds a diagnostic to its run;
    None when there is no absolute output directory to bind to (round-41 closure
    D5: the path rule accepted a decoy segment-run from any directory)."""
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


def path_shape_problem(path):
    """Why a receipt path is not a legal spelling, or None.

    Round-41 closure D5, second finding: `path_parts()` normalised a trailing
    slash and `/./` away, so a malformed publication `.../var/info.txt/` satisfied
    the oracle row `var/info.txt`. A trailing slash names a directory, an empty
    component is not a name, `.` and `..` are not names either, and an absolute
    path is not a receipt path. `$input` and one `$output/` sigil are the only
    prefixes REA emits."""
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
    parts = p.split('/')
    for comp in parts:
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


def under_root(path, root):
    """Segment-bounded containment: `P == CR or P.startswith(CR + '/')`.

    Never `P.startswith(CR)`: a root `x_extract` does not own `x_extract2/...`
    (round-41 closure D5). The round-40 matcher was the mirror-image defect - a
    suffix test - and both are pinned in the selftest."""
    if not isinstance(path, str) or not isinstance(root, str) or not root:
        return False
    p = strip_output(path)
    if p == root:
        return True
    return p.startswith(root.rstrip('/') + '/')


def squashfs_roots(env, handler):
    """The receipt's chunk extract roots for one frozen handler.

    unblob's subtasks are published as `derivations[]` edges and the child path
    is the directory a chunk was extracted into (rea-agents 6.5.0
    FirmwareReports.js:341-357). Only edges whose handler EQUALS the carrier's
    frozen handler are roots for this claim (round 41 accepted any handler
    starting `squashfs_v4`): a whole-file chunk's root is `firmware.bin_extract`
    (`selected.bin_extract` under a range selection), a carved chunk's root is
    `<parent>/<start>-<end>.<handler>_extract`, and a nested image's root is
    `<parent>/<path to image>_extract`.

    Returns them deepest first, so a caller that wants a deterministic default
    sees the most specific root first; the counter never uses that order to guess
    (see subject_root)."""
    nr = env.get('normalized_result') or {}
    out = set()
    if not isinstance(handler, str) or not handler:
        return []
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        if d.get('handler') != handler:
            continue
        child = strip_output(d.get('child_path'))
        if isinstance(child, str) and child:
            out.add(child.rstrip('/'))
    return sorted(out, key=lambda r: (-len(r), r))


def subject_root(env, handler, hint=None):
    """(extract root, how) of the chunk whose filesystem the oracle describes.

    Exactly one derivation root of the carrier's handler is the normal case and
    needs no hint. Several roots (a wrapper carrier that also extracted a nested
    image) cannot be resolved from the receipt alone, so the freeze may name the
    intended root per carrier (`oracle_root` in carriers.json); without that hint
    the answer is None and the three path clauses fail closed. A hint that names
    no root at all is a frozen-table error and also resolves to None."""
    roots = squashfs_roots(env, handler)
    if not roots:
        return None, 'no %s derivation edge' % (handler,)
    if hint is not None:
        if hint not in roots:
            return None, 'oracle_root %r not among %r' % (hint, roots)
        return hint, 'oracle_root from carriers.json'
    if len(roots) == 1:
        return roots[0], 'single %s derivation root' % (handler,)
    return None, 'ambiguous: %d %s roots %r (freeze oracle_root)' % (
        len(roots), handler, roots)


def chunk_roots(env, handler, hint=None):
    """[{extract_root, subject}] for the receipt, for reporting."""
    root, how = subject_root(env, handler, hint)
    return {'roots': squashfs_roots(env, handler), 'subject': root, 'source': how}


def diagnostic_rel(diagnostic, root, output_directory=None):
    """A removal diagnostic's entry path relative to the chunk extract root.

    unblob reports `MaliciousSymlinkRemoved(link=<absolute path inside its
    extraction dir>, target=...)` (unblob extractor.py:79-87) and REA stores it
    with `input_path` naming the task directory, so the entry path exists only in
    `link`. The link must sit under the run's own extraction tree
    (`trusted_run_root`, segment-bounded), and the root's segment run must appear
    after that prefix; None when it does not (that diagnostic cannot be resolved
    and fails the disposition check closed, round-41 closure D5)."""
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

    Exact: the path must be `<root>/<rel>` (or the root itself). Nothing else
    counts - not a suffix, not a basename. R40-CL1 was a suffix test
    (`candidate.endswith('/' + rel)`), under which the regular file
    `usr/bin/busy` scored as the symlink entry `bin/busy`."""
    if root is None or not isinstance(path, str) or not path:
        return None
    if not under_root(path, root):
        # the raw spelling is not inside the root, so no amount of component
        # normalisation may make it so (a root `x_extract` never owns
        # `x_extract2/...`; round-41 closure D5)
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


def chunk_failed(env):
    nr = env.get('normalized_result') or {}
    return any(isinstance(c, dict) and c.get('extraction_failed')
               for c in (nr.get('chunks') or []))


def gaps(env):
    nr = env.get('normalized_result') or {}
    return list(nr.get('extraction_gaps') or [])


def oracle_hits(oracle, files, root):
    """Oracle rows published exactly: rel, sha256 and (when frozen) size.

    The path is the exact relative path under the chunk extract root, never a
    suffix; the size column is compared when the frozen table carries one, so a
    same-hash row cannot stand in for a different length."""
    if root is None:
        return 0
    hits = 0
    for row in oracle:
        rel, sha = row[0], row[1]
        want_size = row[2] if len(row) > 2 else None
        for fp, fsha, fsize in files:
            if fsha != sha or not same_rel(fp, rel, root):
                continue
            if want_size is not None and fsize != want_size:
                continue
            hits += 1
            break
    return hits


def published_rels(files, root):
    """The distinct relative paths of published regular files under the root."""
    if root is None:
        return []
    out = set()
    for fp, _sha, _size in files:
        rel = extract_rel(fp, root)
        if rel:
            out.add(rel)
    return sorted(out)


def extra_published(oracle, files, root):
    """Published regular files under the root that the oracle does not list.

    Round 42 predicate tightening (L1, w1): the published regular set equals the
    oracle regular set, both directions. An extra file is as much a divergence as
    a missing one - and it is the shape a curated extraction would produce."""
    if root is None:
        return []
    want = {strip_rel(row[0]) for row in oracle}
    return [rel for rel in published_rels(files, root) if rel not in want]


def fetch_receipt_ok(raw, carrier):
    """(ok, why) for a frozen `fetch-<id>.json` against the frozen carrier entry.

    R42C1Sentinel H2: the counter never re-fetches, so the chain must be
    recomputable from frozen fields. The receipt records what the fetch saw
    (`final_url`, `http_status`) and the whole pin chain; this check requires no
    redirect, a 200, an https URL, and every pinned field to equal the carrier
    entry's, so a receipt cannot describe a different image, member or carve than
    the table it is frozen with."""
    if raw is None:
        return False, 'fetch receipt absent'
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return False, 'fetch receipt is not JSON: %s' % e
    if not isinstance(doc, dict):
        return False, 'fetch receipt is not an object'
    ext = carrier.get('external') if isinstance(carrier.get('external'), dict) else {}
    url = ext.get('url')
    if not (isinstance(url, str) and url.startswith('https://')):
        return False, 'carrier url %r is not https' % (url,)
    problems = []
    if doc.get('url') != url:
        problems.append('url %r != frozen %r' % (doc.get('url'), url))
    if doc.get('final_url') != url:
        problems.append('final_url %r != url (a redirect is not the frozen source)'
                        % (doc.get('final_url'),))
    if doc.get('http_status') != 200:
        problems.append('http_status %r != 200' % (doc.get('http_status'),))
    length = doc.get('content_length')
    if not (isinstance(length, int) and not isinstance(length, bool) and length > 0):
        problems.append('content_length %r is not a positive int' % (length,))
    for key, ext_key in (('image_sha256', 'image_sha256'),
                         ('member', 'member'), ('member_sha256', 'member_sha256')):
        if doc.get(key) != ext.get(ext_key):
            problems.append('%s %r != frozen %r' % (key, doc.get(key), ext.get(ext_key)))
    carve = doc.get('carve_len', doc.get('length'))
    if carve != ext.get('length'):
        problems.append('carve_len %r != frozen length %r'
                        % (carve, ext.get('length')))
    if doc.get('pin') != carrier.get('sha256'):
        problems.append('pin %r != carrier sha256 %r'
                        % (doc.get('pin'), carrier.get('sha256')))
    tool = doc.get('tool_sha256')
    if not (isinstance(tool, str) and SHA_RE.match(tool.lower())):
        problems.append('tool_sha256 is not 64 hex')
    return (not problems), ('; '.join(problems[:4]) if problems else 'ok')


def extract_env_ok(raw, carrier, toolchain):
    """(ok, why) for the committed `extract-env.json` next to an after-receipt.

    R42C1Sentinel H1: a successful REA envelope does not name its extractor, so
    the run records what resolved under the fixed PATH - the extractor digests,
    the PATH itself and the unblob log's extract command line. The check binds
    that record to the frozen toolchain pin and to this carrier's endianness:
    `sasquatch` with `-le`/`-be`, never `sasquatch-v4be`."""
    if raw is None:
        return False, 'extract-env.json absent'
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return False, 'extract-env.json is not JSON: %s' % e
    if not isinstance(doc, dict):
        return False, 'extract-env.json is not an object'
    toolchain = toolchain if isinstance(toolchain, dict) else {}
    problems = []
    want_sq = (toolchain.get('sasquatch') or {}).get('sha256')
    got_sq = (doc.get('sasquatch') or {}).get('sha256') \
        if isinstance(doc.get('sasquatch'), dict) else None
    if not (isinstance(want_sq, str) and got_sq == want_sq):
        problems.append('sasquatch sha256 %r != frozen %r' % (got_sq, want_sq))
    want_ub = (toolchain.get('unblob') or {}).get('sha256')
    got_ub = (doc.get('unblob') or {}).get('sha256') \
        if isinstance(doc.get('unblob'), dict) else None
    if not (isinstance(want_ub, str) and got_ub == want_ub):
        problems.append('unblob sha256 %r != frozen %r' % (got_ub, want_ub))
    if doc.get('path') != FIXED_PATH:
        problems.append('run PATH %r is not the fixed %r'
                        % (doc.get('path'), FIXED_PATH))
    log = doc.get('unblob_log') if isinstance(doc.get('unblob_log'), dict) else {}
    line = log.get('command_line')
    endian = ((carrier.get('superblock') or {}).get('endianness')
              if isinstance(carrier.get('superblock'), dict) else None)
    if not (isinstance(line, str) and line):
        problems.append('unblob_log.command_line absent')
    else:
        if 'sasquatch-v4be' in line:
            problems.append('the log names sasquatch-v4be')
        if 'sasquatch' not in line:
            problems.append('the log does not name sasquatch')
        want_flag = '-le' if endian == 'le' else '-be' if endian == 'be' else None
        if want_flag is None:
            problems.append('carrier endianness %r is not le/be' % (endian,))
        elif want_flag not in line.split():
            problems.append('the log does not run sasquatch %s' % (want_flag,))
    log_sha = log.get('sha256')
    if not (isinstance(log_sha, str) and SHA_RE.match(log_sha.lower())):
        problems.append('unblob_log.sha256 is not 64 hex')
    return (not problems), ('; '.join(problems[:4]) if problems else 'ok')


def extractor_bin_ok(spec):
    """(ok, detail) for the frozen toolchain against the binaries on FIXED_PATH.

    R42C1Sentinel H1: unblob invokes the bare name `sasquatch`, so a shim earlier
    on PATH is projection-invisible. The binding resolves the name under the
    fixed PATH, hashes the real path, and requires the frozen digest - the host
    value for sasquatch 4.5.1 is
    ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754."""
    toolchain = spec.get('toolchain') if isinstance(spec, dict) else None
    if not isinstance(toolchain, dict):
        return False, {'reason': 'no toolchain block'}
    detail = {}
    ok = True
    for name, binary in (('sasquatch', 'sasquatch'), ('unblob', 'unblob')):
        want = (toolchain.get(name) or {}).get('sha256') \
            if isinstance(toolchain.get(name), dict) else None
        path = which_fixed(binary)
        got = file_sha256(path) if path else None
        detail[name] = {'path': path, 'sha256': got, 'frozen': want}
        if not (isinstance(want, str) and got == want):
            ok = False
    detail['path'] = FIXED_PATH
    return ok, detail


def nonregular_published(files, nonreg, root):
    hits = []
    if root is None:
        return hits
    for fp, _, _ in files:
        for rel, _kind, _detail in nonreg:
            if same_rel(fp, rel, root):
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
                        allowance
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
    """
    if root is None:
        return False, 'no extract root: paths cannot be resolved'
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    removed = model.get('removed') or {}
    by_rel = {rel: (kind, detail) for rel, kind, detail in nonreg}
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
        hits = [r for r, _k, _d in nonreg if same_rel(rp, r, root)]
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
            hits = [r for r, _k, _d in nonreg if r == rel]
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


def first_add(root, rev, path):
    p = git(root, 'log', '--diff-filter=A', '--format=%H', rev, '--', path, check=False)
    if p.returncode != 0:
        return None
    lines = [l.strip() for l in p.stdout.decode().splitlines() if l.strip()]
    return lines[-1] if lines else None


def is_ancestor(root, ancestor, descendant):
    p = git(root, 'merge-base', '--is-ancestor', ancestor, descendant, check=False)
    return p.returncode == 0


def prior_pins(root, freeze, spec):
    """(pins, sources) a previous C1 freeze already scored.

    The claim's kill rule names "relabelled round-41 receipts" as a control that
    must stop C1, so a carrier whose bytes an earlier round scored cannot count as
    new coverage however the table names it. The only sources are frozen at the
    FREEZE commit (a table added or edited later cannot bless an old pin):
      tools/round-42/prior-pins.json   the frozen union of rounds 38-41 pins, each
                                       with the file and commit it came from
                                       (R42C1Sentinel H3: reading `.ufo/waves/
                                       round-4x/c1/carriers.json` at the measured
                                       revision made freshness forgeable)
      carriers.json `prior_pins`       an optional extra explicit list
    """
    pins, sources = set(), []
    raw = show(root, freeze, PRIOR_PINS)
    doc = None
    if raw is not None:
        try:
            doc = json.loads(raw)
        except json.JSONDecodeError:
            doc = None
    if isinstance(doc, dict):
        entries = doc.get('pins') if isinstance(doc.get('pins'), list) else []
        for e in entries:
            if isinstance(e, str) and SHA_RE.match(e.lower()):
                pins.add(e.lower())
            elif isinstance(e, dict) and isinstance(e.get('sha256'), str) \
                    and SHA_RE.match(e['sha256'].lower()):
                pins.add(e['sha256'].lower())
        sources.append(PRIOR_PINS)
    listed = spec.get('prior_pins')
    if isinstance(listed, list):
        for p in listed:
            if isinstance(p, str) and SHA_RE.match(p.lower()):
                pins.add(p.lower())
        if listed:
            sources.append('prior_pins(extra)')
    return pins, sources


def frozen_drift(root, freeze, rev, spec):
    """Commits in FREEZE..REV that touch a frozen C1 path (freeze-drift binding)."""
    frozen = set(FROZEN_PATHS)
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        for key in ('path', 'oracle', 'nonregular', 'fetch_receipt'):
            v = c.get(key)
            if isinstance(v, str) and v:
                frozen.add(v)
    # `after.json` and `extract-env.json` are added AFTER the freeze by design, so
    # they cannot be drift-checked (R42C1Sentinel L4): the score receipt carries
    # their digests instead, and extract-env is bound to the frozen toolchain by
    # the `extract_env_ok` clause.
    p = git(root, 'log', '--pretty=format:', '--name-only', '--no-renames',
            f'{freeze}..{rev}', check=False)
    if p.returncode != 0:
        raise Unevaluable('git log freeze..rev failed')
    touched = sorted({l.strip() for l in p.stdout.decode(errors='replace').splitlines()
                      if l.strip() and l.strip() in frozen})
    return touched


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


def projection(env, profile='core', handler=None):
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
    proj_root = subject_root(env, handler)[0] if handler else None

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
    for d in nr.get('diagnostics') or []:
        if not isinstance(d, dict):
            continue
        typename = diagnostic_typename(d) or '<none>'
        rel = diagnostic_rel(d, proj_root,
                             (env.get('parameters') or {}).get('output_directory')
                             if isinstance(env.get('parameters'), dict) else None) \
            if proj_root else None
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

REPLAY_PARAMS = (('--max-depth', 'max_depth'),
                 ('--max-output-bytes', 'max_output_bytes'),
                 ('--max-output-files', 'max_output_files'))


def make_real_runner(work, unblob, timeout):
    """REA 6.5.0 extract-firmware on the given carrier bytes, fresh outdir.

    The run replays the committed receipt's recorded extraction parameters
    (`parameters.max_depth`, `max_output_bytes`, `max_output_files`). A receipt
    produced at `--max-depth 1` is `partial` with a truncated published set, so a
    rerun at REA's default depth 3 could never match it under a profile that
    compares `coverage` or `published_bytes`."""
    unblob_path = unblob or os.path.expanduser('~/.local/bin/unblob')

    def run(carrier_bytes, cid, params=None):
        if shutil.which('npx') is None:
            raise RerunEnvError('npx not on PATH')
        d = os.path.join(work, 'rerun-' + re.sub(r'[^A-Za-z0-9_.-]', '_', str(cid)))
        inp = os.path.join(d, 'carrier.bin')
        outdir = os.path.join(d, 'out')
        os.makedirs(d, exist_ok=False)
        with open(inp, 'wb') as fh:
            fh.write(carrier_bytes)
        env = dict(os.environ)
        env['REA_UNBLOB_COMMAND'] = unblob_path
        env['TMPDIR'] = d
        argv = ['npx', '-y', REA_PIN, 'extract-firmware', '--format', 'json',
                '--full-output']
        replayed = {}
        if isinstance(params, dict):
            for flag, key in REPLAY_PARAMS:
                value = params.get(key)
                if isinstance(value, int) and not isinstance(value, bool):
                    argv += [flag, str(value)]
                    replayed[key] = value
        argv += [inp, outdir]
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

    return run


# ------------------------------------------------------------- measurement

def measure(root, rev, freeze, pkg65, rerun=None, target=TARGET,
            expected_ids=IDS, unblob=None, rea_timeout=900, carrier_cache=None):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P41-C1',
           'target': target}
    git(root, 'cat-file', '-e', f'{rev}^{{commit}}')
    git(root, 'cat-file', '-e', f'{freeze}^{{commit}}')

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
    res['frozen_tables_valid'] = isinstance(plan_doc, dict)

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
    model, plan_probs = gap_rule_model(plan_raw)
    res['gap_rule_problems'] = plan_probs
    prior, prior_sources = prior_pins(root, freeze, spec)
    res['prior_pins'] = sorted(prior)
    res['prior_pin_sources'] = prior_sources

    work = tempfile.mkdtemp(prefix='c1-counter.', dir=scratch_root())
    try:
        runner = rerun or make_real_runner(work, unblob, rea_timeout)
        per = {}
        envs = {}
        for c in spec.get('carriers') or []:
            if not isinstance(c, dict):
                continue
            k = c.get('id')
            d = {'id': k}
            pin = (c.get('sha256') or '').lower() or None
            handler = c.get('handler') if isinstance(c.get('handler'), str) else None
            d['handler'] = handler
            opath = c.get('oracle')
            npath = c.get('nonregular')
            rpath = c.get('receipt') or '%s/%s/after.json' % (AFTERDIR, k)
            epath = c.get('extract_env') or '%s/%s/extract-env.json' % (AFTERDIR, k)
            ext = c.get('external') if isinstance(c.get('external'), dict) else None
            if ext is not None and carrier_cache and pin:
                # published carrier: bytes fetched by fetch-carrier.py into
                # --carrier-cache; the pin (frozen in carriers.json) is still
                # checked below on these bytes.
                fp = os.path.join(carrier_cache, pin + '.bin')
                raw = open(fp, 'rb').read() if os.path.isfile(fp) else None
                d['carrier_cache'] = fp
            else:
                raw = None
                d['carrier_cache'] = None
            d['carrier_path'] = c.get('path')
            d['carrier_present'] = raw is not None
            d['carrier_pin_ok'] = (raw is not None and pin is not None
                                   and hashlib.sha256(raw).hexdigest() == pin)
            d['carrier_fresh_ok'] = (pin is not None and pin not in prior)
            d['carrier_fresh_against'] = prior_sources
            d['fetch_receipt_path'] = c.get('fetch_receipt')
            fok, fwhy = fetch_receipt_ok(
                show(root, rev, c['fetch_receipt'])
                if isinstance(c.get('fetch_receipt'), str) else None, c)
            d['fetch_receipt_ok'] = fok
            d['fetch_receipt_note'] = fwhy
            d['layout'] = layout_probe(raw, c.get('superblock'))
            d['layout_ok'] = bool(d['layout'].get('ok'))
            d['layout_reason'] = d['layout'].get('reason')
            d['compression'] = d['layout'].get('compression')
            d['endianness'] = d['layout'].get('endianness')
            # carve_ok: the carrier is exactly the extent unblob will call the
            # chunk. unblob stops a SquashFS chunk at `bytes_used`, or at
            # round_up(bytes_used, 4096|1024) when that tail is zero padding
            # (handlers/filesystem/squashfs.py calculate_chunk), so the frozen
            # carve length must equal that chunk end, not `bytes_used`
            # (R42C1Sentinel A5). A carve of any other length is not the image.
            bu = d['layout'].get('bytes_used')
            size = d['layout'].get('size')
            ce = d['layout'].get('chunk_end')
            carve_len = ext.get('length') if ext is not None else None
            d['carve'] = {'length': carve_len, 'bytes_used': bu, 'size': size,
                          'chunk_end': ce}
            d['carve_ok'] = (isinstance(ce, int) and size == ce
                             and (carve_len is None or carve_len == ce))

            oracle, oerr = parse_oracle(show(root, rev, opath) if opath else None)
            d['oracle_path'] = opath
            d['oracle_error'] = oerr
            d['oracle_files'] = len(oracle)
            d['oracle_ok'] = oerr is None and len(oracle) > 0

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
            d['receipt_present'] = env is not None

            add = first_add(root, rev, rpath) if raw_receipt is not None else None
            d['receipt_first_add'] = add
            d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)

            if env is not None:
                envs[f'{k}/after'] = env
                # a score receipt relabelled as evidence is not an REA envelope
                d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}
                                                 & set(env))
                d['evidence_digest'] = hashlib.sha256(raw_receipt).hexdigest()
                d['extract_env_path'] = epath
                eok, ewhy = extract_env_ok(show(root, rev, epath), c,
                                           spec.get('toolchain'))
                d['extract_env_ok'] = eok
                d['extract_env_note'] = ewhy
                params = env.get('parameters') or {}
                od = params.get('output_directory') if isinstance(params, dict) else None
                d['output_directory'] = od
                subj = env.get('subject') or {}
                d['subject_pin_ok'] = ((subj.get('digest') or {}).get('sha256')
                                       if isinstance(subj, dict) else None) == pin
                prov = env.get('provider') or {}
                d['operation_ok'] = (env.get('operation') == 'extract_firmware'
                                     and isinstance(prov, dict) and prov.get('id') == 'unblob')
                d['chunk_handlers'] = chunk_handlers(env)
                d['handler_ok'] = (handler is not None
                                   and handler in chunk_handlers(env))
                d['chunks_ok'] = not chunk_failed(env)
                hint = (c.get('oracle_root')
                        if isinstance(c.get('oracle_root'), str) else None)
                root_value, root_how = subject_root(env, handler, hint)
                d['extract_root'] = root_value
                d['extract_root_source'] = root_how
                d['chunk_roots'] = chunk_roots(env, handler, hint)
                if root_value:
                    d['extract_root_confirmed'] = any(
                        under_root(p, root_value) for p in receipt_paths(env))
                else:
                    d['extract_root_confirmed'] = False
                files = published(env)
                d['published_files'] = len(files)
                d['oracle_hits'] = oracle_hits(oracle, files, root_value)
                d['published_rels'] = len(published_rels(files, root_value))
                extra = extra_published(oracle, files, root_value)
                d['extra_published'] = extra[:5]
                # the published regular set equals the oracle regular set, both
                # directions (L1 predicate tightening, w1): a missing row and an
                # extra file are the same divergence
                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and root_value is not None
                                       and d['oracle_hits'] == d['oracle_files']
                                       and d['published_rels'] == d['oracle_files']
                                       and not extra)
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

                # rerun clause: fresh REA run of the REV carrier bytes
                if raw is not None and d['carrier_pin_ok']:
                    status, payload = runner(raw, k, params)
                    if status != 'ok':
                        d['projection_ok'] = False
                        d['projection_error'] = payload
                    else:
                        eq, keys, detail = projection_diff(
                            projection(env, profile, handler),
                            projection(payload, profile, handler),
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
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = matched
        # L4 (R42C1Sentinel): the score receipt carries the digest of every
        # after-receipt it scored, so a later rewrite of an already-added
        # evidence file is visible even though it did not exist at the freeze.
        res['evidence_digests'] = {
            k: {'path': v.get('receipt_path'),
                'sha256': v.get('evidence_digest')}
            for k, v in per.items() if v.get('evidence_digest')}
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
        HANDLER_RE.search(cells(r)[0]) and SQFS3_TEXT_RE.search(r) and ENTRY in r
        for r in rows)
    b['province_core_rows_seen'] = [
        cells(r)[0] for r in rows if HANDLER_RE.search(cells(r)[0])]
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and SQFS3_TEXT_RE.search(l)
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
            if c[0] in src_ids and c[8] == OPENED and (ENTRY in used or STEM in used):
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
    ends = [d.get('endianness') for d in (res.get('carriers') or {}).values()]
    # Both sasquatch legs must be bound: unblob 26.6.4 calls `sasquatch -le` for a
    # little-endian v3 superblock and `sasquatch -be` for a big-endian one, so a
    # freeze whose carriers are all one endianness tests one flag of the
    # extractor, not the family.
    b['endianness_coverage'] = (any(e == 'le' for e in ends)
                                and any(e == 'be' for e in ends))
    b['endianness_detail'] = ends
    b['compression_detail'] = [d.get('compression')
                               for d in (res.get('carriers') or {}).values()]
    eok, edetail = extractor_bin_ok(spec)
    b['extractor_bin_ok'] = eok
    b['extractor_bin_detail'] = edetail
    # every published carrier must name a SOURCES row that documents the host its
    # URL lives on (R42C1Sentinel H2 item 2)
    carrier_sources = {}
    if reg:
        rows = {}
        for line in reg.decode(errors='replace').splitlines():
            if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
                continue
            c = cells(line)
            if len(c) == 11:
                rows[c[0]] = c
        for c in spec.get('carriers') or []:
            if not isinstance(c, dict):
                continue
            sid = c.get('source_id')
            url = ((c.get('external') or {}).get('url')
                   if isinstance(c.get('external'), dict) else None)
            row = rows.get(sid) if isinstance(sid, str) else None
            host = None
            if isinstance(url, str) and '://' in url:
                host = url.split('://', 1)[1].split('/', 1)[0]
            carrier_sources[c.get('id')] = {
                'source_id': sid,
                'host': host,
                'row_present': row is not None,
                'host_in_row': bool(row and host and any(host in x for x in row)),
            }
    b['carrier_source_rows'] = carrier_sources
    b['carrier_sources_ok'] = (bool(carrier_sources)
                               and all(v['row_present'] and v['host_in_row']
                                       for v in carrier_sources.values()))
    b['frozen_tables_valid'] = bool(res.get('frozen_tables_valid'))
    res['bindings'] = b
    res['met_target'] = bool(res['carriers_unchanged'] and res['gap_rule_unchanged']
                             and res['carriers_matched'] == target
                             and all(b[x] is True for x in BINDINGS))
    return res


def write_receipt(doc, path):
    """Write a score receipt and prove its own identity on the way out.

    Round-41 closure D4: the receipt records the counter's digest, so a reader
    can re-hash the tool from the revision it names instead of trusting a
    separate diff. The check is done on the bytes that landed, not on the dict."""
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


def main(argv=None):
    global WORK_OVERRIDE
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--pkg65')
    ap.add_argument('--json-out')
    ap.add_argument('--unblob')
    ap.add_argument('--carrier-cache',
                    help='directory holding <sha256>.bin for external carriers '
                         '(filled by tools/round-42/fetch-carrier.py)')
    ap.add_argument('--work', help='scratch directory (default '
                    '$HYAKU_SCRATCH/kaidoku-r42/counter)')
    ap.add_argument('--rea-timeout', type=int, default=900)
    ap.add_argument('--no-rerun', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--selftest-rea', action='store_true')
    ap.add_argument('--dev-carrier', help='a v3 image the caller may run REA on '
                    '(unblob 26.6.4 fixture or the Kamikaze 7.09 dev image), used '
                    'by --selftest-rea')
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
        return selftest(a.pkg65)
    if a.selftest_rea:
        return selftest_rea(a.pkg65, a.unblob, a.rea_timeout, a.dev_carrier)
    if a.no_rerun:
        out = {'reason': 'rerun_disabled',
               'detail': 'P42-C1 binds a fresh REA run of each carrier; '
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
    res['argv'] = sys.argv
    res['exit_code'] = 0 if res['met_target'] else 1
    print(json.dumps({k: res[k] for k in ('revision', 'freeze', 'carriers_matched',
                                          'target', 'carriers_unchanged',
                                          'gap_rule_unchanged', 'frozen_path_changed',
                                          'bindings', 'met_target', 'exit_code')},
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


def sb_v3(variant='standard', endian='le', *, minor=0, compression='gzip',
          magic=None, major=3, bytes_used=None, meta_len=54,
          meta_header=None, meta_uncompressed=False, dts_override=None,
          dts_delta=0, pad=0):
    """A fixture carrier: a coherent SquashFS v3 image, laid out as the format is.

    Not a real filesystem - `layout_probe` is a superblock/relocation test and
    these bytes exercise it exactly: the (variant, endianness) magic, a data
    region, one inode-table metadata block carrying the declared compression
    signature, a directory table, and tables after it. `bytes_used` is the total
    length unless overridden; `pad` appends bytes past `bytes_used` (a sloppy
    carve); `meta_header` writes a given 2-byte header verbatim and `meta_len`
    still sizes the payload, so the plausibility/identity split can be driven."""
    body = bytearray(SQUASHFS3_SB_SIZE)
    m = magic if magic is not None else MAGIC_BY_VARIANT[variant][endian]
    body[0:4] = m
    body += b'block-payload-' * 3
    its = len(body)
    if compression == 'gzip':
        meta = b'\x78\x9c' + b'Z' * max(0, meta_len - 2)
    else:
        meta = b'\x5d\x00\x00' + b'Z' * max(0, meta_len - 3)
    meta = meta[:meta_len] if meta_len >= 2 else meta
    if meta_header is not None:
        header = meta_header
    else:
        header = (meta_len | (UNCOMPRESSED_FLAG if meta_uncompressed else 0)).to_bytes(
            2, 'big' if endian == 'be' else 'little')
    body += header + meta
    dts = its + 2 + meta_len + dts_delta if dts_override is None else dts_override
    if len(body) < dts:
        body += b'\x00' * (dts - len(body))
    fts = len(body) + 8
    lts = fts + 8
    total = lts + 8
    body += b'\x00' * (total - len(body))
    order = 'big' if endian == 'be' else 'little'

    def put(off, width, value):
        body[off:off + width] = (int(value) & ((1 << (8 * width)) - 1)).to_bytes(
            width, order)

    used = total if bytes_used is None else bytes_used
    put(4, 4, 4)                      # inodes
    put(28, 2, major)                 # s_major
    put(30, 2, minor)                 # s_minor
    put(32, 2, 0)                     # block_size_1
    put(34, 2, 16)                    # block_log
    body[36] = 0x40                   # flags: duplicates removed
    body[37] = 1                      # no_uids
    body[38] = 0                      # no_guids
    put(39, 4, 1640000000)            # mkfs_time (unaligned, packed struct)
    put(43, 8, 64)                    # root_inode
    put(51, 4, 65536)                 # block_size
    put(55, 4, 1)                     # fragments
    put(63, 8, used)                  # bytes_used
    put(71, 8, total - 12)            # uid_start
    put(79, 8, 0)                     # guid_start
    put(87, 8, its)                   # inode_table_start
    put(95, 8, dts)                   # directory_table_start
    put(103, 8, fts)                  # fragment_table_start
    put(111, 8, lts)                  # lookup_table_start
    if pad:
        body += b'\x00' * pad
    return bytes(body)


def mk_env(name, pin, files=(), gaps=(), unpub=(), diags=(), chunks=None,
           handler=DEFAULT_HANDLER,
           outdir='/fast/scratch/hyaku/kaidoku-r42/selftest/after',
           subject_name='carrier.sqsh', chunk_dir='firmware.bin_extract',
           operation='extract_firmware', provider='unblob', derivations=None):
    """A receipt-shaped REA envelope (`data` object) for fixture carriers.

    `derivations` defaults to the one edge rea-agents 6.5.0 publishes for a
    whole-file chunk (`$input` -> `$output/<chunk_dir>`, the carrier's own
    handler), which is what the counter reads the extract root from. Diagnostic
    links are absolute and sit under the run's extraction tree, the shape the
    committed round-41 receipts show: `<dirname(outdir)>/rea-firmware-<id>/
    extracted/<chunk_dir>/<rel>`."""
    link_base = '%s/rea-firmware-fixture/extracted/%s' % (
        os.path.dirname(outdir.rstrip('/')), chunk_dir)
    if chunks is None:
        chunks = [{'input_path': '$input', 'provider_id': '3028394:1',
                   'range': {'offset': 0, 'length': 4096},
                   'handler': handler, 'encrypted': False,
                   'root_file_range': {'offset': 0, 'length': 4096},
                   'extraction_failed': False}]
    if derivations is None:
        derivations = [{'parent_path': '$input',
                        'child_path': '$output/' + chunk_dir,
                        'provider_blob_id': '3028394:1', 'handler': handler,
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
            'relative_path': '%s/%s' % (chunk_dir, rel), 'handler': handler,
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
                       'link': '%s/%s' % (link_base, rel),
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
                       'max_depth': 3, 'max_output_bytes': 268435456,
                       'max_output_files': 10000},
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
    consistent and `subject_root` still derives the same namespace. Diagnostic
    links are re-homed under the new run's private extraction tree, because the
    counter resolves them relative to `dirname(output_directory)`."""
    e = json.loads(json.dumps(env))
    root = '/fast/scratch/hyaku/kaidoku-r42/counter/rerun/%s' % tag
    outdir = root + '/out'
    link_base = '%s/rea-firmware-%s/extracted/%s' % (root, tag, chunk_dir)
    nr = e['normalized_result']
    old_params = e.get('parameters') if isinstance(e.get('parameters'), dict) else {}
    old_out = old_params.get('output_directory')
    handler = None
    for deriv in nr.get('derivations') or []:
        if isinstance(deriv, dict) and isinstance(deriv.get('handler'), str):
            handler = deriv['handler']
            break
    old_root = subject_root(e, handler)[0]

    def remap(path):
        p = strip_output(path)
        if not isinstance(p, str) or not p:
            return p
        if old_root:
            if p == old_root:
                return chunk_dir
            if under_root(p, old_root):
                return chunk_dir + p[len(old_root):]
        return p

    tails = []
    for d in nr.get('diagnostics') or []:
        report = d.get('report')
        if isinstance(report, dict) and isinstance(report.get('link'), str):
            tails.append(diagnostic_rel({'report': {'link': report['link']}},
                                        old_root, old_out))
        else:
            tails.append(None)
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
    for deriv in nr.get('derivations') or []:
        for key in ('parent_path', 'child_path'):
            v = strip_output(deriv.get(key))
            if isinstance(v, str) and v and v != '$input':
                deriv[key] = '$output/' + remap(v)
    nr['depth_limited_paths'] = ['$output/' + remap(x)
                                 for x in nr.get('depth_limited_paths') or []]
    for d, tail in zip(nr.get('diagnostics') or [], tails):
        report = d.get('report')
        if isinstance(report, dict) and tail is not None:
            report['link'] = '%s/%s' % (link_base, tail)
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


def _province(row=True, heading=CORE_HEADING, cell='`squashfs_v3`',
              layout='SquashFS v3 rootfs', note=True, cited=ENTRY,
              stem=None, section_text='## Next'):
    r = f'| {cell} | {layout} | x | `{cited}` |\n' if row else ''
    fn = (f'- {FRONTIER_MARK}, 2026-10-26: the Frontier v1-v3 part is '
          f'superseded by `{stem or STEM}`.\n') if note else ''
    return (f'# P\n\n{heading}\n\n| Surface | Layout | a | Entry |\n|---|---|---|---|\n{r}\n'
            f'{section_text}\n{fn}\n')


def _entry(sid='S1121'):
    return f'# E\n\nsource: {sid} - x\n'


def _registry(sid='S1121', opened=OPENED, used=ENTRY, source_rows=None):
    rows = f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n'
    if sid != 'S112':
        rows += f'| S112 | s | docs | A | s | a | t | mined | {OPENED} | 180d | {ENTRY} |\n'
    for rsid, source in (source_rows or []):
        rows += (f'| {rsid} | {source} | image | A | s | a | t | mined | '
                 f'{OPENED} | 180d | {ENTRY} |\n')
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
    ids = list(IDS) or ['V3', 'V4', 'L3', 'L4']
    HANDLER = DEFAULT_HANDLER          # fixture-local: the plain v3 handler

    # Fixture carriers: four v3 images covering both endiannesses (so the
    # `endianness_coverage` binding is exercised) and three of the four family
    # handlers. All are exact carves: bytes_used == len(bytes).
    carriers = {
        'V3': sb_v3('standard', 'le'),
        'V4': sb_v3('standard', 'be'),
        'L3': sb_v3('ddwrt', 'le', minor=1),
        'L4': sb_v3('broadcom', 'be', minor=1),
    }
    handlers = {'V3': 'squashfs_v3', 'V4': 'squashfs_v3',
                'L3': 'squashfs_v3_ddwrt', 'L4': 'squashfs_v3_broadcom'}
    superblocks = {
        'V3': {'magic': 'hsqs', 'endianness': 'le', 'major': 3, 'minor': 0,
               'variant': 'standard', 'compression': 'gzip'},
        'V4': {'magic': 'sqsh', 'endianness': 'be', 'major': 3, 'minor': 0,
               'variant': 'standard', 'compression': 'gzip'},
        'L3': {'magic': 'hsqt', 'endianness': 'le', 'major': 3, 'minor': 1,
               'variant': 'ddwrt', 'compression': 'gzip'},
        'L4': {'magic': 'qshs', 'endianness': 'be', 'major': 3, 'minor': 1,
               'variant': 'broadcom', 'compression': 'gzip'},
    }
    pins = {k: sha(v) for k, v in carriers.items()}
    fsha = lambda i: sha(('f%s' % i).encode())

    # per-carrier fixture data (files, gaps, unpublished, diagnostics)
    spec_data = {
        'V3': dict(files=[('README.txt', fsha(1), 148), ('config/app.conf', fsha(2), 54)],
                   gaps=[('unpublished-entry', 'usr/share/demo/link-blob', []),
                         ('unpublished-entry', 'usr/share/demo/escape', [])],
                   unpub=[('usr/share/demo/link-blob', 'symlink', '../opt/blob.bin'),
                          ('usr/share/demo/escape', 'symlink', '../../../../etc/shadow')],
                   diags=[],
                   nonreg='usr/share/demo/link-blob\tsymlink\nusr/share/demo/escape\tsymlink\n'),
        'V4': dict(files=[('var/info.txt', fsha(3), 40)], gaps=[], unpub=[], diags=[],
                   nonreg=''),
        'L3': dict(files=[('bin/run', fsha(4), 12), ('docs/deep/blob.bin', fsha(5), 33)],
                   gaps=[('unpublished-entry', 'usr/lib/libfoo.so', [])],
                   unpub=[('usr/lib/libfoo.so', 'symlink', '../lib/libfoo.so.1')],
                   diags=[],
                   nonreg='usr/lib/libfoo.so\tsymlink\n'),
        'L4': dict(files=[('etc/motd', fsha(6), 9)], gaps=[], unpub=[],
                   diags=[('FileMagicMismatch', 'etc/motd')],
                   nonreg='dev/console\tdevice\n'),
    }
    # L4's device is required: give it a gap
    spec_data['L4']['gaps'] = [('unpublished-entry', 'dev/console', [])]
    spec_data['L4']['unpub'] = [('dev/console', 'device', None)]

    def receipt_envs(over=None):
        out = {}
        for k in ids:
            sd = spec_data[k]
            out[k] = mk_env(k.lower() + '.sqsh', pins[k],
                            files=sd['files'], gaps=sd['gaps'],
                            unpub=sd['unpub'], diags=sd['diags'],
                            handler=handlers[k],
                            outdir='/fast/scratch/hyaku/kaidoku-r42/selftest/%s-after' % k)
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

    rule = json.dumps({'claim': 'R42-C1',
                       'allowed': {'symlink': ['unpublished-entry'],
                                   'device': ['unpublished-entry']}}, indent=1)

    # ---- published-carrier fixture chain (Sentinel H2/H3/H4/H1) ----------
    HOST = 'download.example.invalid'
    SOURCE_IDS = {k: 'S9%02d' % (10 + i) for i, k in enumerate(ids)}
    IMAGE_PINS = {k: sha(('image-%s' % k).encode()) for k in ids}
    MEMBER_PINS = {k: sha(('member-%s' % k).encode()) for k in ids}
    SQ_PATH = which_fixed('sasquatch')
    UB_PATH = which_fixed('unblob')
    if not SQ_PATH or not UB_PATH:
        raise SystemExit('selftest needs sasquatch and unblob on the fixed PATH %r'
                         % (FIXED_PATH,))
    TOOLCHAIN = {'sasquatch': {'sha256': file_sha256(SQ_PATH)},
                 'unblob': {'sha256': file_sha256(UB_PATH)}}
    REA_PKG_DOC = {
        'version': REA_VERSION,
        'package_json_sha256': file_sha256(os.path.join(os.path.abspath(pkg65),
                                                        'package.json')),
        'package_lock_sha256': file_sha256(next(
            (p for p in (os.path.join(os.path.dirname(os.path.abspath(pkg65)),
                                      'package-lock.json'),
                         os.path.join(os.path.dirname(os.path.dirname(
                             os.path.abspath(pkg65))), 'package-lock.json'))
             if os.path.isfile(p)), '')),
    }
    # a pin no fixture carrier has, so freshness passes by default
    DEFAULT_PRIOR = json.dumps({'rounds': [38, 39, 40, 41],
                                'pins': [{'sha256': 'f' * 64,
                                          'source': '.ufo/waves/round-41/c1/carriers.json',
                                          'id': 'R41-OTHER'}]}, indent=1)
    FETCH = lambda k: '.ufo/waves/round-42/c1/fetch-%s.json' % k
    EXTRACT_ENV = lambda k: '%s/%s/extract-env.json' % (AFTERDIR, k)
    URL = lambda k: 'https://%s/vendor/%s.image' % (HOST, k.lower())
    CACHE = os.path.join(work, 'carrier-cache')
    os.makedirs(CACHE, exist_ok=True)

    def cache_put(blob):
        p = os.path.join(CACHE, sha(blob) + '.bin')
        if not os.path.isfile(p):
            with open(p, 'wb') as fh:
                fh.write(blob)
        return p

    def spec_json(pin_map=None, blob_map=None, drop=None, target=None,
                  receipt_override=None, projection=None, external=None,
                  oracle_root=None, external_drop=None, prior_pins=None,
                  handler_over=None, super_over=None, length_over=None,
                  url_over=None, kind_over=None):
        """carriers.json text for the fixture carriers.

        `external`/`external_drop` remove or break a chain key; `handler_over`/
        `super_over` replace a carrier's frozen handler or superblock;
        `length_over` freezes a carve length that is not the blob's;
        `url_over`/`kind_over` break the published-source shape (red cases)."""
        pm = pin_map or pins
        bm = blob_map or carriers
        cs = []
        for k in ids:
            if drop and k in drop:
                continue
            c = {'id': k,
                 'kind': (kind_over or {}).get(k, 'published'),
                 'source_id': SOURCE_IDS[k],
                 'sha256': pm[k],
                 'handler': (handler_over or {}).get(k, handlers[k]),
                 'fetch_receipt': FETCH(k),
                 'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
                 'nonregular': f'{AFTERDIR}/{k}/nonregular.tsv'}
            sb = (super_over or {}).get(k, superblocks[k])
            if sb is not None:
                c['superblock'] = dict(sb)
            if k == external:
                c['external'] = {'url': 'https://download.example.invalid/x.image',
                                 'image_sha256': IMAGE_PINS[k],
                                 'member': './var/tmp/fs.image',
                                 'member_sha256': MEMBER_PINS[k],
                                 'length': len(bm[k]), 'offset': 0}
                for key in (external_drop or ()):
                    c['external'].pop(key, None)
            else:
                c['external'] = {
                    'url': (url_over or {}).get(k, URL(k)),
                    'image_sha256': IMAGE_PINS[k],
                    'member': './var/tmp/fs.image',
                    'member_sha256': MEMBER_PINS[k],
                    'length': (length_over or {}).get(k, len(bm[k])),
                    'offset': 0}
            if oracle_root and k in oracle_root:
                c['oracle_root'] = oracle_root[k]
            if receipt_override and k in receipt_override:
                c['receipt'] = receipt_override[k]
            cs.append(c)
        spec = {'claim': 'R42-C1', 'toolchain': TOOLCHAIN, 'carriers': cs}
        if target is not None:
            spec['target'] = target
        if projection is not None:
            spec['projection'] = projection
        if prior_pins is not None:
            spec['prior_pins'] = list(prior_pins)
        return json.dumps(spec, indent=1)

    def oracle_tsv(k):
        rows = ''.join(f'{rel}\t{h}\t{size}\n' for rel, h, size in spec_data[k]['files'])
        return rows.encode()

    def fetch_receipt(k, pin_map=None, blob_map=None, length=None, **over):
        pm = pin_map or pins
        bm = blob_map or carriers
        doc = {'url': URL(k), 'final_url': URL(k), 'http_status': 200,
               'content_length': len(bm[k]) + 4096,
               'image_sha256': IMAGE_PINS[k],
               'member': './var/tmp/fs.image',
               'member_sha256': MEMBER_PINS[k],
               'carve_len': (length if length is not None else len(bm[k])),
               'pin': pm[k], 'tool_sha256': sha(b'fetch-tool')}
        doc.update(over)
        return json.dumps(doc, indent=1)

    def extract_env(k):
        flag = '-le' if superblocks[k]['endianness'] == 'le' else '-be'
        return json.dumps({
            'sasquatch': {'path': SQ_PATH, 'version': '4.5.1',
                          'sha256': TOOLCHAIN['sasquatch']['sha256']},
            'unblob': {'path': UB_PATH, 'version': '26.6.4',
                       'sha256': TOOLCHAIN['unblob']['sha256']},
            'path': FIXED_PATH,
            'unblob_log': {
                'command_line': 'sasquatch %s -no-exit-code -f -d <outdir> <inpath>'
                                % flag,
                'sha256': sha(('log-%s' % k).encode())},
        }, indent=1)

    def frozen_files(blob_map=None, pin_map=None, nonreg_map=None, rule_text=None,
                     oracle_map=None, prior_text=None, length_over=None,
                     fetch_over=None, env_over=None, spec_text=None, **over):
        bm = blob_map or carriers
        pm = pin_map or pins
        for k in ids:
            cache_put(bm[k])
        nm = nonreg_map if nonreg_map is not None else {
            k: spec_data[k]['nonreg'] for k in ids}
        om = oracle_map if oracle_map is not None else {k: oracle_tsv(k) for k in ids}
        f = {XPIN: xpin,
             CARRIERS: (spec_text if spec_text is not None
                        else spec_json(pin_map=pm, blob_map=bm,
                                       length_over=length_over)),
             GAPRULE: (rule_text if rule_text is not None else rule).encode(),
             'plans/round-42-claims.md': b'# plan\n',
             'tools/round-42/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
             PRIOR_PINS: (prior_text if prior_text is not None else DEFAULT_PRIOR).encode(),
             REA_PKG: json.dumps(REA_PKG_DOC, indent=1).encode(),
             'PROVINCE.md': _province(),
             ENTRY: _entry(),
             'corpus/SOURCES.md': _registry(
                 source_rows=[(SOURCE_IDS[k], URL(k).split('/', 3)[2]) for k in ids]),
             'corpus/README.md': _readme()}
        for k in ids:
            f[FETCH(k)] = (fetch_over or {}).get(k) or fetch_receipt(
                k, pin_map=pm, blob_map=bm,
                length=(length_over or {}).get(k))
            f[EXTRACT_ENV(k)] = (env_over or {}).get(k) or extract_env(k)
            f[f'{AFTERDIR}/{k}/oracle.tsv'] = om[k]
            f[f'{AFTERDIR}/{k}/nonregular.tsv'] = nm[k].encode()
        f.update(over)
        return f

    def build(blob_over=None, env_over=None, receipt_over=None, nonreg_over=None,
              oracle_over=None, rule_text=None, spec_text=None, length_over=None,
              fetch_over=None, extract_over=None, prior_text=None):
        """A pin-consistent (frozen files, receipts) pair for one variant."""
        bm = dict(carriers)
        bm.update(blob_over or {})
        pm = {k: sha(bm[k]) for k in ids}
        for k in ids:
            cache_put(bm[k])
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
                                  spec_text=spec_text, length_over=length_over,
                                  fetch_over=fetch_over, env_over=extract_over,
                                  prior_text=prior_text)
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

    def add(name, steps, freeze_index, want, reason=None, want_fail=None,
            runner=sim_runner, check=None):
        cases.append({'name': name, 'steps': steps, 'freeze': freeze_index,
                      'want': want, 'reason': reason, 'want_fail': want_fail,
                      'runner': runner, 'check': check})

    green_frozen, green_receipts = build()
    frozen = frozen_files()
    good = receipts(green_envs)

    def check_evidence_digests(res):
        got = {k: (v or {}).get('sha256')
               for k, v in (res.get('evidence_digests') or {}).items()}
        want = {k: sha(json.dumps(e).encode()) for k, e in green_envs.items()}
        missing = sorted(set(want) - set(got))
        wrong = sorted(k for k in want if got.get(k) != want[k])
        if missing or wrong:
            return 'evidence_digests missing=%r wrong=%r' % (missing, wrong)
        return None

    add('green (4 published v3 carriers, fresh receipts, docs)',
        [green_frozen, green_receipts], 0, 0, check=check_evidence_digests)
    add('do-nothing (freeze files only)', [frozen], 0, 1, want_fail='receipt_present')
    add('receipt missing (V4)',
        [frozen, {k: v for k, v in good.items() if '/V4/' not in k}], 0, 1,
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

    oracle_only = fabricate('V3', diags=[], chunk_handler='squashfs_v4_le')
    add('oracle-only fabrication with re-minted evidence id',
        [frozen, relabel(green_envs, 'V3', oracle_only)], 0, 1,
        want_fail='projection_ok')
    one_file_off = fabricate('V4', files=[('var/info.txt', fsha(99), 40)])
    add('fabrication differing only in one published sha256',
        [frozen, relabel(green_envs, 'V4', one_file_off)], 0, 1,
        want_fail='projection_ok')
    extra_gap = fabricate('L3', gaps=[('unpublished-entry', 'usr/lib/libfoo.so', []),
                                      ('extractor-failure', 'bin/run', ['xz'])])
    add('fabrication differing only in an extra gap',
        [frozen, relabel(green_envs, 'L3', extra_gap)], 0, 1, want_fail='gaps_ok')
    diags_dropped = fabricate('L4', drop_diag=True)
    add('fabrication differing only in the diagnostics multiset',
        [frozen, relabel(green_envs, 'L4', diags_dropped)], 0, 1,
        want_fail='projection_ok')
    add('rerun yields no evidence object (REA ok=false)',
        [frozen, good], 0, 1, want_fail='projection_ok', runner=boom_runner)
    add('rerun environment error (no npx) is unevaluable, never met',
        [frozen, good], 0, 2, 'rerun_env_error', runner=env_boom_runner)
    add('subject digest names another carrier',
        [frozen, mutant('V3', lambda e: e['subject']['digest'].__setitem__(
            'sha256', '2' * 64))], 0, 1, want_fail='subject_pin_ok')

    # ---- carrier layout controls (v3 superblock, both endiannesses)
    # wrong minor: the frozen superblock says 0, the bytes say 1
    add('s_minor does not match the frozen superblock',
        list(build(blob_over={'V3': sb_v3('standard', 'le', minor=1)})), 0, 1,
        want_fail='layout_ok')
    # a v4 image is not a v3 carrier even with a v3-family handler
    add('s_major 4 with the frozen v3 magic',
        list(build(blob_over={'V3': sb_v3('standard', 'le', major=4)})), 0, 1,
        want_fail='layout_ok')
    # the metadata header must decode in the superblock's endianness: write the
    # BE spelling of 54 on an LE carrier (LE reads 13824, implausible)
    add('metadata header in the other endianness',
        list(build(blob_over={'V3': sb_v3('standard', 'le', meta_header=b'\x00\x36')})),
        0, 1, want_fail='layout_ok')
    # 1c04: LE length 1052, BE length 7172 - plausible both ways, and neither is
    # excluded by plausibility, so the identity (its + 2 + len == dts) is the only
    # signal that can settle the header
    amb_no_id = sb_v3('standard', 'le', meta_len=1052, meta_header=b'\x1c\x04',
                      dts_delta=3948)
    add('metadata length plausible both ways and no identity settles it',
        list(build(blob_over={'V3': amb_no_id})), 0, 1, want_fail='layout_ok')
    amb_id = sb_v3('standard', 'le', meta_len=1052, meta_header=b'\x1c\x04')
    add('ambiguous length settled by the single-block identity',
        list(build(blob_over={'V3': amb_id})), 0, 0)
    # magic of the other endianness: hsqs on a carrier frozen as BE
    add('little-endian magic on a big-endian frozen carrier',
        list(build(blob_over={'V4': sb_v3('standard', 'le')})), 0, 1,
        want_fail='layout_ok')
    big_used = sb_v3('standard', 'le', bytes_used=0xFFFFFFF0)
    add('bytes_used beyond the file', list(build(blob_over={'V3': big_used})), 0, 1,
        want_fail='layout_ok')
    # declared compression must be visible in the inode table's metadata blocks
    lz = sb_v3('standard', 'le', compression='lzma')
    add('declared gzip but the inode table carries LZMA',
        list(build(blob_over={'V3': lz})), 0, 1, want_fail='layout_ok')
    unc = sb_v3('standard', 'le', meta_uncompressed=True)
    add('inode table metadata uncompressed leaves compression undetermined',
        list(build(blob_over={'V3': unc})), 0, 1, want_fail='layout_ok')

    # ---- missing / malformed frozen inputs (absent at the freeze itself)
    missing_pins = dict(pins)
    missing_pins['V4'] = '9' * 64
    no_carrier = {**frozen, CARRIERS: spec_json(pin_map=missing_pins),
                  FETCH('V4'): fetch_receipt('V4', pin_map=missing_pins)}
    add('carrier bytes absent from the cache', [no_carrier, good], 0, 1,
        want_fail='carrier_present')
    bad_oracle = {**frozen, f'{AFTERDIR}/V3/oracle.tsv': b'not-a-digest\n'}
    add('malformed oracle row', [bad_oracle, good], 0, 1, want_fail='oracle_ok')
    bad_nonreg = {**frozen, f'{AFTERDIR}/L3/nonregular.tsv': b'usr/lib/libfoo.so\n'}
    add('malformed nonregular row', [bad_nonreg, good], 0, 1,
        want_fail='nonregular_ok')

    # ---- receipt clause controls
    add('wrong operation (extract_filesystem)',
        [frozen, mutant('V3', lambda e: e.__setitem__('operation', 'extract_filesystem'))],
        0, 1, want_fail='operation_ok')
    add('provider is not unblob',
        [frozen, mutant('V4', lambda e: e['provider'].__setitem__('id', 'binwalk'))],
        0, 1, want_fail='operation_ok')
    add('failed chunk',
        [frozen, mutant('L3', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))], 0, 1,
        want_fail='chunks_ok')
    add('chunk handler is the LE handler',
        [frozen, mutant('L4', lambda e: [c.__setitem__('handler', 'squashfs_v4_le')
                                         for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('disallowed gap kind on a symlink entry',
        [frozen, mutant('V3', lambda e: e['normalized_result']['extraction_gaps'][0]
                        .__setitem__('kind', 'extractor-failure'))], 0, 1,
        want_fail='gaps_ok')
    add('gap on a path that is not a non-regular entry',
        [frozen, mutant('V4', lambda e: e['normalized_result']['extraction_gaps'].append({
            'kind': 'unpublished-entry', 'relative_path': 'firmware.bin_extract/var/ghost',
            'dependencies': []}))], 0, 1, want_fail='gaps_ok')
    add('required gap missing (symlink materialised)',
        [frozen, mutant('L3', lambda e: (
            e['normalized_result']['extraction_gaps'].pop(),
            e['normalized_result']['unpublished_entries'].pop(),
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/usr/lib/libfoo.so',
                'path': '/x/usr/lib/libfoo.so', 'size': 3, 'sha256': 'f' * 64})))],
        0, 1, want_fail='gaps_ok')
    add('escaping symlink published as a regular file',
        [frozen, mutant('V3', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/usr/share/demo/escape',
            'path': '/x/escape', 'size': 3, 'sha256': 'e' * 64}))], 0, 1,
        want_fail='nonregular_unpublished_ok')
    add('oracle file missing from the published set',
        [frozen, mutant('V4', lambda e: e['normalized_result']['files'].pop())], 0, 1,
        want_fail='oracle_hits_ok')
    add('foreign scratch provenance (/kaidoku-r39/)',
        [frozen, mutant('V3', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r39/l1/K1-after'))],
        0, 1, want_fail='run_provenance_ok')
    add('provenance path climbs out with ..',
        [frozen, mutant('V4', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r41/../kaidoku-r39/x'))],
        0, 1, want_fail='run_provenance_ok')
    add('evidence id stale after an edit',
        [frozen, mutant('L4', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/extra.txt', 'path': '/x/extra.txt',
            'size': 1, 'sha256': 'd' * 64}), remint=False)], 0, 1,
        want_fail='evidence_id_ok')

    # ---- path identity: exact relative to the chunk extract root (R40-CL1)
    # Round-40 defect: the suffix rule read the regular file `usr/bin/busy` as the
    # symlink entry `bin/busy`, so L2 scored 3/4 at 42c10a58 on a faithful
    # extraction. Every case below pins one shape of that collision; `path_probes`
    # and `root_probes` additionally assert that the round-40 matcher mis-scores
    # exactly these fixtures, so the selftest cannot silently stop discriminating.
    path_probes = []
    root_probes = []
    spec_probes = []

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

    def same_run(recs, k='V4'):
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
        env_over={'V4': lambda e: (pub(e, 'usr/bin/busy', fsha(7)),
                                   entry(e, 'bin/busy'))},
        nonreg_over={'V4': 'bin/busy\tsymlink\n'},
        oracle_over={'V4': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('usr/bin/busy', fsha(7), 5)])})
    add('regular usr/bin/busy does not satisfy the symlink entry bin/busy',
        [deep_file, deep_recs], 0, 0, runner=same_run(deep_recs))
    # dir 2: the symlink entry's path ends with a regular file's path
    short_file, short_recs = build(
        env_over={'V4': lambda e: (pub(e, 'sbin/tool', fsha(8), 40),
                                   entry(e, 'usr/sbin/tool', target='tool'))},
        nonreg_over={'V4': 'usr/sbin/tool\tsymlink\n'},
        oracle_over={'V4': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('sbin/tool', fsha(8), 40)])})
    add('regular sbin/tool does not satisfy the symlink entry usr/sbin/tool',
        [short_file, short_recs], 0, 0, runner=same_run(short_recs))
    # the tightened matcher must still catch a published symlink path
    materialised, materialised_recs = build(
        env_over={'V4': lambda e: (pub(e, 'usr/sbin/tool', fsha(9), 40),
                                   entry(e, 'usr/sbin/tool', gap=False,
                                         target='tool'))},
        nonreg_over={'V4': 'usr/sbin/tool\tsymlink\n'})
    add('published regular at the symlink entry usr/sbin/tool is still caught',
        [materialised, materialised_recs], 0, 1,
        want_fail='nonregular_unpublished_ok', runner=same_run(materialised_recs))
    # a deeper file cannot stand in for an oracle row (round-40 matched the suffix)
    oracle_shadow, oracle_shadow_recs = build(
        env_over={'V4': lambda e: pub(e, 'usr/bin/busy', fsha(7))},
        oracle_over={'V4': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('bin/busy', fsha(7), 5)])})
    add('deeper file with the oracle row sha256 does not publish oracle bin/busy',
        [oracle_shadow, oracle_shadow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(oracle_shadow_recs))
    wrong_gap, wrong_gap_recs = build(
        env_over={'V4': lambda e: (entry(e, 'bin/busy', gap=False),
                                   e['normalized_result']['extraction_gaps'].append({
                                       'kind': 'unpublished-entry',
                                       'handler': HANDLER,
                                       'relative_path':
                                           'firmware.bin_extract/usr/bin/busy',
                                       'dependencies': []}))},
        nonreg_over={'V4': 'bin/busy\tsymlink\n'})
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

    NESTED = 'firmware.bin_extract/core.sqsh_extract'
    hint = spec_json(oracle_root={'V4': NESTED})
    two_ok, two_ok_recs = build(
        env_over={'V4': lambda e: add_nested_chunk(e, True)}, spec_text=hint,
        oracle_over={'V4': oracle_rows([('lib/x', fsha(11), 7)])})
    add('two chunks with oracle_root: the nested extraction is its own namespace',
        [two_ok, two_ok_recs], 0, 0, runner=same_run(two_ok_recs))
    two_amb_frozen, two_amb_recs = build(
        env_over={'V4': lambda e: add_nested_chunk(e, True)})
    add('two squashfs roots without oracle_root fail closed',
        [two_amb_frozen, two_amb_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_amb_recs))
    two_wrong_frozen, two_wrong_recs = build(
        env_over={'V4': lambda e: add_nested_chunk(e, True)},
        spec_text=spec_json(oracle_root={'V4': 'no.such.root'}))
    add('oracle_root that names no derivation root fails closed',
        [two_wrong_frozen, two_wrong_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_wrong_recs))
    two_shadow, two_shadow_recs = build(
        env_over={'V4': lambda e: add_nested_chunk(e, True)}, spec_text=hint,
        oracle_over={'V4': oracle_rows([('var/info.txt', fsha(3), 40),
                                        ('lib/x', fsha(11), 7)])})
    add('two chunks: the nested chunk file does not publish outer-root row lib/x',
        [two_shadow, two_shadow_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_shadow_recs))
    for desc, envs, hint_root, want_root, want_src in (
            ('single chunk root', green_receipts, None, 'firmware.bin_extract',
             'single squashfs_v3 derivation root'),
            ('two roots with oracle_root', two_ok_recs, NESTED, NESTED,
             'oracle_root from carriers.json'),
            ('two roots without a hint', two_amb_recs, None, None,
             'ambiguous')):
        e = json.loads(envs[receipt_path('V4')])
        r, src = subject_root(e, HANDLER, hint_root)
        root_probes.append({'desc': desc, 'root': r, 'source': src,
                            'want_root': want_root,
                            'want_src': (src if want_src == 'ambiguous'
                                         and src.startswith('ambiguous') else want_src),
                            'chunk_roots': chunk_roots(e, HANDLER, hint_root)})
    # a v4 handler on the receipt's edge is not this carrier's root
    e_v4 = json.loads(green_receipts[receipt_path('V4')])
    for deriv in e_v4['normalized_result']['derivations']:
        deriv['handler'] = 'squashfs_v4_be'
    r_v4, src_v4 = subject_root(e_v4, HANDLER)
    root_probes.append({'desc': 'v4 derivation edge is not a v3 root',
                        'root': r_v4, 'source': src_v4,
                        'want_root': None,
                        'want_src': 'no squashfs_v3 derivation edge',
                        'chunk_roots': chunk_roots(e_v4, HANDLER)})

    # ---- measured chunk-directory shapes (carried from round 41)
    # unblob 26.6.4 through rea-agents 6.5.0 --max-depth 1 (measured on dev
    # carriers, round-41 artifacts/chunk-naming.json): a chunk that is only PART
    # of the input is extracted one level deeper than the input's own directory,
    # so a matcher that strips one `_extract` component scores 0 oracle rows on a
    # padded carrier. These cases pin both the depth and the ambiguity of two
    # v3 chunks in one receipt.
    PORTION = 'firmware.bin_extract/4096-4500.squashfs_v3_extract'
    rule_struct1 = json.dumps({'claim': 'R42-C1',
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
                                 env_over={'V4': padded_receipt})
    add('padded carrier: the oracle resolves under the portion chunk directory',
        [pad_frozen, pad_recs], 0, 0, runner=same_run(pad_recs))
    pad_shallow_frozen, pad_shallow_recs = build(
        rule_text=rule_struct1,
        env_over={'V4': lambda e: padded_receipt(e, shallow=True)})
    add('padded carrier: the same rows one level too shallow score nothing',
        [pad_shallow_frozen, pad_shallow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(pad_shallow_recs))
    for desc, recs, want_root, want_src in (
            ('portion chunk root', pad_recs, PORTION,
             'single squashfs_v3 derivation root'),
            ('portion chunk, shallow publish', pad_shallow_recs, PORTION,
             'single squashfs_v3 derivation root')):
        e = json.loads(recs[receipt_path('V4')])
        r, src = subject_root(e, HANDLER)
        root_probes.append({'desc': desc, 'root': r, 'source': src,
                            'want_root': want_root, 'want_src': want_src,
                            'chunk_roots': chunk_roots(e, HANDLER)})

    def two_portion_chunks(e):
        """Two v3 chunks in one input: no receipt data says which filesystem the
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
             'child_path': '$output/firmware.bin_extract/0-2500.squashfs_v3_extract',
             'provider_blob_id': 'p0', 'handler': HANDLER,
             'parent_file_range': {'offset': 0, 'length': 2500}},
            {'parent_path': '$input',
             'child_path': '$output/firmware.bin_extract/2500-5000.squashfs_v3_extract',
             'provider_blob_id': 'p1', 'handler': HANDLER,
             'parent_file_range': {'offset': 2500, 'length': 2500}}]
        e['normalized_result']['files'] = [
            {'relative_path': 'firmware.bin_extract/0-2500.squashfs_v3_extract/'
                              'var/info.txt',
             'path': '/x/var/info.txt', 'size': 40, 'sha256': fsha(3)},
            {'relative_path': 'firmware.bin_extract/2500-5000.squashfs_v3_extract/'
                              'etc/x',
             'path': '/x/etc/x', 'size': 9, 'sha256': fsha(14)}]
        e['normalized_result']['extraction_gaps'] = [
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '0-2500.squashfs_v3_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c0'},
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '2500-5000.squashfs_v3_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c1'}]
        e['normalized_result']['unpublished_entries'] = []

    two_frozen, two_recs2 = build(rule_text=rule_struct1,
                                  env_over={'V4': two_portion_chunks})
    add('two v3 chunks in one receipt are ambiguous, not guessed',
        [two_frozen, two_recs2], 0, 1, want_fail='gaps_ok',
        runner=same_run(two_recs2))
    e = json.loads(two_recs2[receipt_path('V4')])
    r, src = subject_root(e, HANDLER)
    root_probes.append({'desc': 'two portion chunk roots', 'root': r, 'source': src,
                        'want_root': None,
                        'want_src': src if src.startswith('ambiguous') else '',
                        'chunk_roots': chunk_roots(e, HANDLER)})

    # ---- the root derivation fails closed rather than guessing
    def no_input_handler(e):
        """Two handler chunks in the input and no derivation root for the whole
        filesystem: the receipt states two roots and the oracle could describe
        either."""
        e['normalized_result']['chunks'][0]['handler'] = 'squashfs_v4_le'
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

    amb_frozen, amb_recs = build(env_over={'V4': no_input_handler})
    add('two handler chunks and no input handler chunk fail closed',
        [amb_frozen, amb_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(amb_recs))
    e = json.loads(amb_recs[receipt_path('V4')])
    r, src = subject_root(e, HANDLER)
    root_probes.append({'desc': 'ambiguous handler chunks', 'root': r, 'source': src,
                        'want_root': None,
                        'want_src': src if src.startswith('ambiguous:') else '',
                        'chunk_roots': chunk_roots(e, HANDLER)})

    def outside_namespace(e):
        """A published file under a directory that is not the subject root."""
        e['normalized_result']['files'].append({
            'relative_path': 'other_extract/etc/x', 'path': '/x/other_extract/etc/x',
            'size': 5, 'sha256': fsha(12)})

    mix_frozen, mix_recs = build(env_over={'V4': outside_namespace})
    add('a file outside the subject root is another namespace, not an extra',
        [mix_frozen, mix_recs], 0, 0, runner=same_run(mix_recs))
    e = json.loads(mix_recs[receipt_path('V4')])
    r, src = subject_root(e, HANDLER)
    root_probes.append({'desc': 'outside-namespace file', 'root': r, 'source': src,
                        'want_root': 'firmware.bin_extract',
                        'want_src': 'single squashfs_v3 derivation root',
                        'chunk_roots': chunk_roots(e, HANDLER)})

    def no_derivations(e):
        e['normalized_result']['derivations'] = []

    nod_frozen, nod_recs = build(env_over={'V4': no_derivations})
    add('receipt with no squashfs derivation edge fails closed',
        [nod_frozen, nod_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nod_recs))

    # ---- removal disposition (R41C1DevCore 7.1-7.3, carried)
    # unblob deletes escaping symlinks after reporting MaliciousSymlinkRemoved and
    # empty-target symlinks with no report at all, and never publishes a link as a
    # regular file. A rootfs carrier needs the allowance, so the frozen rule may
    # carry a `removed` block and every row must land in exactly one disposition.
    rule_removed = json.dumps({
        'claim': 'R42-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': True},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive'},
        'structural': {'depth-limited': 1}}, indent=1)

    def link_for(e, rel):
        """An absolute diagnostic link under the run's private extraction tree."""
        out = e['parameters']['output_directory']
        return '%s/rea-firmware-fixture/extracted/firmware.bin_extract/%s' % (
            os.path.dirname(out.rstrip('/')), rel)

    def one_symlink(e, gap=True, removal=False, row_rel='bin/link',
                    diag_rel='bin/link', target='../usr/bin/x'):
        """V4 with exactly one symlink row and a chosen disposition."""
        if gap:
            entry(e, row_rel, gap=True, target=target)
        else:
            entry(e, row_rel, gap=False, target=target)
        if removal:
            e['normalized_result']['diagnostics'].append({
                'input_path': '$output/firmware.bin_extract',
                'report': {'__typename__': 'MaliciousSymlinkRemoved',
                           'severity': 'WARNING',
                           'link': link_for(e, diag_rel),
                           'target': '/etc/shadow'}})

    rem_frozen, rem_recs = build(
        rule_text=rule_removed, nonreg_over={'V4': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: one_symlink(e, gap=False, removal=True)})
    add('a removal diagnostic is an admitted disposition for a symlink row',
        [rem_frozen, rem_recs], 0, 0, runner=same_run(rem_recs))
    both_frozen, both_recs = build(
        rule_text=rule_removed, nonreg_over={'V4': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: one_symlink(e, gap=True, removal=True)})
    add('an entry cannot be both gapped and removed',
        [both_frozen, both_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(both_recs))
    none_frozen, none_recs = build(
        rule_text=rule_removed, nonreg_over={'V4': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: one_symlink(e, gap=False, removal=False)})
    add('a required symlink with no disposition fails',
        [none_frozen, none_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(none_recs))
    stray_frozen, stray_recs = build(
        rule_text=rule_removed, nonreg_over={'V4': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: one_symlink(e, gap=True, removal=True,
                                              diag_rel='var/nowhere')})
    add('a removal that resolves to no symlink row fails',
        [stray_frozen, stray_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(stray_recs))
    # round-41 closure D5, first finding: a link whose path merely CONTAINS the
    # root as a segment run, from a different directory, must not satisfy the row
    decoy_frozen, decoy_recs = build(
        rule_text=rule_removed, nonreg_over={'V4': 'bin/link\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: (
            entry(e, 'bin/link', gap=False, target='../usr/bin/x'),
            e['normalized_result']['diagnostics'].append({
                'input_path': '$output/firmware.bin_extract',
                'report': {'__typename__': 'MaliciousSymlinkRemoved',
                           'severity': 'WARNING',
                           'link': '/fast/scratch/hyaku/kaidoku-r42/decoy/'
                                   'firmware.bin_extract/bin/link',
                           'target': '/etc/shadow'}}))})
    add('a removal link outside the run extraction root fails closed (D5)',
        [decoy_frozen, decoy_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(decoy_recs))
    # a removal may not be used to hide a *regular* file: the row it names must be
    # of a kind the rule lists, and a device row is not one
    dev_frozen, dev_recs = build(
        rule_text=rule_removed,
        nonreg_over={'V4': 'dev/console\tdevice\t\n'},
        env_over={'V4': lambda e: (entry(e, 'dev/console', gap=False),
                                   e['normalized_result']['diagnostics'].append({
                                       'input_path': '$output/firmware.bin_extract',
                                       'report': {'__typename__':
                                                  'MaliciousSymlinkRemoved',
                                                  'severity': 'WARNING',
                                                  'link': link_for(e, 'dev/console'),
                                                  'target': '/x'}}))})
    add('a removal naming a row of an unlisted kind fails',
        [dev_frozen, dev_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(dev_recs))
    # silent empty-target removal: unblob deletes the link and reports nothing
    rule_silent = json.dumps({
        'claim': 'R42-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': True},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive',
                    'silent': {'symlink': ['empty-target']}},
        'structural': {'depth-limited': 1}}, indent=1)
    sil_frozen, sil_recs = build(
        rule_text=rule_silent, nonreg_over={'V4': 'bin/empty\tsymlink\t\n'},
        env_over={'V4': lambda e: entry(e, 'bin/empty', gap=False)})
    add('a silent empty-target symlink is admitted with no record',
        [sil_frozen, sil_recs], 0, 0, runner=same_run(sil_recs))
    sil2_frozen, sil2_recs = build(
        rule_text=rule_silent,
        nonreg_over={'V4': 'bin/empty\tsymlink\t../usr/bin/x\n'},
        env_over={'V4': lambda e: entry(e, 'bin/empty', gap=False)})
    add('a symlink with a non-empty target cannot hide behind the silent allowance',
        [sil2_frozen, sil2_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(sil2_recs))
    # projection carries the removal identity (R41C1DevCore 7.3): two symlink
    # rows, neither required, and the rerun removed the other one
    rule_opt = json.dumps({
        'claim': 'R42-C1',
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
                           'link': link_for(e, which),
                           'target': '/etc/shadow'}}]
        return apply

    proj_frozen, proj_recs = build(
        rule_text=rule_opt,
        nonreg_over={'V4': 'bin/one\tsymlink\t../x\nbin/two\tsymlink\t../y\n'},
        env_over={'V4': two_removed('bin/one')})

    def other_removal_runner(carrier_bytes, cid, params=None):
        """A rerun of the same bytes that removed the other symlink."""
        if cid != 'V4':
            return mk_same_runner(green_envs)(carrier_bytes, cid, params)
        e = json.loads(json.dumps(json.loads(proj_recs[receipt_path('V4')])))
        e['normalized_result']['diagnostics'][0]['report']['link'] = \
            link_for(e, 'bin/two')
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
        {'id': 'V1', 'sha256': pins['V3']},
        {'id': 'L2', 'sha256': pins['L4']}]})
    add('an earlier round carriers.json is not a freshness input (H3)',
        [{**frozen, '.ufo/waves/round-41/c1/carriers.json': prior_tbl}, good], 0, 0)
    add('prior_pins that are not 64-hex',
        [{**frozen, CARRIERS: spec_json(prior_pins=['not-a-pin'])}, good], 0, 1,
        want_fail='b:carriers_spec_ok')

    # ---- vendor spec chain and carve exactness (R41C1DevCore 7.4, routed R40-CL6)
    # The spec is checked directly: a vendor carrier cannot be loaded here (its
    # bytes live in --carrier-cache by licence), so an end-to-end case would fail
    # on carrier_present and prove nothing about the chain.
    def nested_spec(drop):
        doc = json.loads(spec_json(external='V3'))
        for c in doc['carriers']:
            if c['id'] == 'V3':
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
               spec_json(external='V3', external_drop=('member_sha256',)),
               False, 'lacks member_sha256')
    probe_spec('external carrier without a positive carve length',
               spec_json(external='V3', external_drop=('length',)),
               False, 'lacks length')
    probe_spec('external carrier with a member_sha256',
               spec_json(external='V3'), True)
    probe_spec('external carrier with a nested block and no nested.sha256',
               nested_spec(drop=True), False, 'nested.sha256')
    probe_spec('external carrier with nested.sha256',
               nested_spec(drop=False), True)
    probe_spec('oracle_root is a relative path',
               spec_json(oracle_root={'V3': 'firmware.bin_extract'}), True)
    probe_spec('oracle_root that is absolute',
               spec_json(oracle_root={'V3': '/firmware.bin_extract'}), False,
               'oracle_root')
    # R42-C1: the frozen handler must be a v3-family handler and agree with the
    # frozen superblock; a v4 handler is the round-41 hardcode coming back
    probe_spec('carrier handler squashfs_v4_le (the round-41 hardcode)',
               spec_json(handler_over={'V3': 'squashfs_v4_le'}), False,
               'not a squashfs_v3 family handler')
    probe_spec('carrier handler squashfs_v3 for a ddwrt magic',
               spec_json(handler_over={'L3': 'squashfs_v3'}), False, 'variant')
    probe_spec('carrier without a superblock block',
               spec_json(super_over={'V3': None}), False, 'superblock')
    probe_spec('superblock magic is not a v3 family magic',
               spec_json(super_over={'V3': {'magic': 'sqsh', 'endianness': 'le',
                                            'major': 3, 'variant': 'standard',
                                            'compression': 'gzip'}}), False, 'magic')
    probe_spec('superblock major is not 3',
               spec_json(super_over={'V3': {'magic': 'hsqs', 'endianness': 'le',
                                            'major': 4, 'variant': 'standard',
                                            'compression': 'gzip'}}), False, 'major')
    probe_spec('superblock compression is not a class',
               spec_json(super_over={'V3': {'magic': 'hsqs', 'endianness': 'le',
                                            'major': 3, 'variant': 'standard',
                                            'compression': 'zstd'}}), False,
               'compression')
    probe_spec('superblock broadly consistent with its handler',
               spec_json(), True)
    # carve_ok: bytes longer than the superblock bytes_used
    o_frozen, o_recs = build(blob_over={'V3': sb_v3('standard', 'le', pad=64)})
    add('carrier longer than its bytes_used (sloppy carve)',
        [o_frozen, o_recs], 0, 1, want_fail='carve_ok', runner=same_run(o_recs))
    # carve length frozen in the table but the bytes are another length
    bad_carve = json.loads(spec_json(external='V3'))
    for c in bad_carve['carriers']:
        if c['id'] == 'V3':
            c['external']['length'] = len(carriers['V3']) + 512
    add('external carve length differs from bytes_used',
        [{**frozen, CARRIERS: json.dumps(bad_carve, indent=1)}, good], 0, 1,
        want_fail='carve_ok')

    # ---- freeze integrity
    add('fetch receipt changed after freeze',
        [frozen, {**good, FETCH('V3'): fetch_receipt('V3', http_status=302)}],
        0, 2, 'frozen_path_changed')
    add('fetch receipt touched then restored',
        [frozen, {**good, FETCH('V3'): '{}\n'},
         {**good, FETCH('V3'): fetch_receipt('V3')}], 0, 2,
        'frozen_path_changed')
    add('oracle changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/V4/oracle.tsv': oracle_tsv('V4') + b'extra.txt\t'
          + b'3' * 64 + b'\t1\n'}], 0, 2, 'frozen_path_changed')
    add('nonregular table changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/L3/nonregular.tsv': b'usr/lib/libfoo.so\tsymlink\n'
         b'usr/lib/extra\tsymlink\n'}], 0, 2, 'frozen_path_changed')
    add('carriers.json changed after freeze',
        [frozen, {**good, CARRIERS: spec_json(drop=('L4',))}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json changed after freeze',
        [frozen, {**good, GAPRULE: json.dumps({'claim': 'R42-C1', 'allowed': {
            'symlink': ['unpublished-entry']}}).encode()}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json touched then restored',
        [frozen, {**good, GAPRULE: b'{}\n'}, {**good, GAPRULE: rule.encode()}], 0, 2,
        'frozen_path_changed')
    add('counter edited after freeze',
        [frozen, {**good, 'tools/round-42/c1-counter.py': b'#!/usr/bin/env python3\n'
         b'print(0)\n'}], 0, 2, 'frozen_path_changed')
    add('claims edited after freeze',
        [frozen, {**good, 'plans/round-42-claims.md': b'# new plan\n'}], 0, 2,
        'frozen_path_changed')

    # ---- frozen-table controls
    bad_pins = dict(pins)
    bad_pins['V3'] = '4' * 64
    add('frozen pin wrong (carrier untouched)',
        [{**frozen, CARRIERS: spec_json(pin_map=bad_pins)}, good], 0, 1,
        want_fail='carrier_pin_ok')
    add('carriers.json drops a carrier at the freeze (target 4)',
        [{**frozen, CARRIERS: spec_json(drop=('V4',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    one_end = {k: sb_v3('standard', 'le') for k in ids}
    le_pins = {k: sha(one_end[k]) for k in ids}
    le_super = {k: {'magic': 'hsqs', 'endianness': 'le', 'major': 3,
                    'minor': superblocks[k].get('minor', 0),
                    'variant': 'standard', 'compression': 'gzip'} for k in ids}
    le_spec = spec_json(pin_map=le_pins, blob_map=one_end, super_over=le_super,
                        handler_over={k: 'squashfs_v3' for k in ids})
    f1, r1 = build(blob_over=one_end, spec_text=le_spec)
    add('all carriers little-endian (endianness coverage)', [f1, r1], 0, 1,
        want_fail='b:endianness_coverage')
    thin = json.dumps({'claim': 'R42-C1', 'allowed': {'symlink': ['unpublished-entry']}})
    f2, r2 = build(rule_text=thin)
    add('gap rule omits the device kind', [f2, r2], 0, 1, want_fail='b:gap_rule_ok')
    add('gap rule is JSON but not an object at the freeze',
        list(build(rule_text='[]')), 0, 1, want_fail='b:frozen_tables_valid')
    add('gap rule names another claim',
        list(build(rule_text=json.dumps({'claim': 'R39-C1', 'allowed': {
            'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}}))),
        0, 1, want_fail='b:gap_rule_ok')

    # ---- structural gaps (unblob bookkeeping: null relative_path)
    rule_struct = json.dumps({'claim': 'R42-C1',
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
                                   env_over={'V3': add_struct})
    add('structural gap within its frozen allowance',
        [st_frozen, st_receipts], 0, 0,
        runner=mk_same_runner({**green_envs, 'V3': json.loads(st_receipts[
            receipt_path('V3')])}))
    st2_frozen, st2_receipts = build(
        rule_text=rule_struct, env_over={'V3': lambda e: add_struct(e, extra=1)})
    add('structural gaps over the allowance', [st2_frozen, st2_receipts], 0, 1,
        want_fail='gaps_ok')
    st3_frozen, st3_receipts = build(
        rule_text=rule_struct,
        env_over={'V3': lambda e: add_struct(e, kind='depth-limited')})
    add('path-less gap kind with no structural allowance', [st3_frozen, st3_receipts],
        0, 1, want_fail='gaps_ok')
    st4_frozen, st4_receipts = build(
        rule_text=rule_struct,
        env_over={'V3': lambda e: add_struct(e, path='usr/share/demo/extra-link')})
    add('structural gap kind that carries a path', [st4_frozen, st4_receipts], 0, 1,
        want_fail='gaps_ok')

    # ---- projection profile: the measured calibration limit of the core fields
    def bump_bytes(e):
        e['normalized_result']['published_bytes'] += 1
    core_frozen, core_receipts = build(
        env_over={'V3': bump_bytes}, spec_text=spec_json(projection='core'))
    add('explicit core profile accepts a projection-identical (oracle-closed) fabrication',
        [core_frozen, core_receipts], 0, 0)
    ext_frozen, ext_receipts = build(env_over={'V3': bump_bytes})
    add('default profile (plus-extractor) refuses the same fabrication',
        [ext_frozen, ext_receipts], 0, 1, want_fail='projection_ok')
    add('unknown projection profile in carriers.json',
        [{**frozen, CARRIERS: spec_json(projection='plus-everything')}, good], 0, 1,
        want_fail='b:carriers_spec_ok')

    # ---- rerun replays the receipt's recorded extraction parameters
    def depth_runner(expected):
        def run(carrier_bytes, cid, params=None):
            got = (params or {}).get('max_depth')
            if got != expected:
                return 'no_data', {'ok': False, 'reason': 'depth %r != %r'
                                   % (got, expected)}
            return sim_runner(carrier_bytes, cid, params)
        return run

    add('rerun passes the receipt max_depth (3) to REA', [frozen, good], 0, 0,
        runner=depth_runner(3))
    add('rerun takes max_depth from the receipt, not a constant',
        [frozen, mutant('V3', lambda e: e['parameters'].__setitem__('max_depth', 1))],
        0, 1, want_fail='projection_ok', runner=depth_runner(3))

    # ---- documentation bindings
    add('province has no Core section at all',
        [{**frozen, 'PROVINCE.md': '# P\n\n## Next\n- x\n'}, good], 0, 1,
        want_fail='b:province_core_section')
    add('province row outside the round-42 section',
        [{**frozen, 'PROVINCE.md': _province(heading='## Round-39 additions to Core')},
         good], 0, 1, want_fail='b:province_core_row')
    add('province row without a v3 handler in the first cell',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v2`')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row whose first cell is a v4 handler',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4_be`')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row absent', [{**frozen, 'PROVINCE.md': _province(row=False)}, good],
        0, 1, want_fail='b:province_core_row')
    add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': _province(
            cited='corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md')}, good],
        0, 1, want_fail='b:province_core_row')
    add('frontier note absent', [{**frozen, 'PROVINCE.md': _province(note=False)}, good],
        0, 1, want_fail='b:frontier_note')
    add('frontier note naming another entry stem',
        [{**frozen, 'PROVINCE.md': _province(
            stem='2026-10-26-r41-avm-be-squashfs-core')}, good], 0, 1,
        want_fail='b:frontier_note')
    add('entry absent', [{**frozen, ENTRY: None}, good], 0, 1, want_fail='b:entry_present')
    add('S-id substring S1120', [{**frozen, ENTRY: _entry('S1120')}, good], 0, 1,
        want_fail='b:sourced')
    add('source row opened earlier',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-25')}, good], 0, 1,
        want_fail='b:sourced')
    add('used-by lacks the entry',
        [{**frozen, 'corpus/SOURCES.md': _registry(used='corpus/lessons/round-40.md')},
         good], 0, 1, want_fail='b:sourced')
    add('coverage map lacks the stem',
        [{**frozen, 'corpus/README.md': _readme(stem='2026-10-26-r40-other')}, good], 0, 1,
        want_fail='b:coverage_map_row')

    # ---- round-42 red cases (the four this port must add, plus the D4 shape)
    # (a) a v4 handler on a v3 carrier: the chunk and the derivation edge name
    #     squashfs_v4_be while the frozen handler is squashfs_v3, so the handler
    #     clause fails and the receipt lends the oracle no root at all
    def v4_on_v3(e):
        for c in e['normalized_result']['chunks']:
            c['handler'] = 'squashfs_v4_be'
        for d in e['normalized_result']['derivations']:
            d['handler'] = 'squashfs_v4_be'

    v4_frozen, v4_recs = build(env_over={'V3': v4_on_v3})
    add('v4 handler on a v3 carrier', [v4_frozen, v4_recs], 0, 1,
        want_fail='handler_ok', runner=same_run(v4_recs))

    # (b) the prefix test is segment-bounded: a root `x_extract` does not own
    #     `x_extract2/...`, so the oracle row cannot be satisfied from there
    def prefix_collision(e):
        e['normalized_result']['derivations'] = [
            {'parent_path': '$input', 'child_path': '$output/x_extract',
             'handler': HANDLER, 'provider_blob_id': 'p0',
             'parent_file_range': {'offset': 0, 'length': 4096}}]
        e['normalized_result']['files'] = [
            {'relative_path': 'x_extract2/var/info.txt',
             'path': '/x/x_extract2/var/info.txt', 'size': 40, 'sha256': fsha(3)}]
        e['normalized_result']['extraction_gaps'] = []
        e['normalized_result']['unpublished_entries'] = []
        e['normalized_result']['depth_limited_paths'] = []

    pre_frozen, pre_recs = build(env_over={'V4': prefix_collision})
    add('a path under x_extract2 cannot publish a row of root x_extract',
        [pre_frozen, pre_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(pre_recs))

    # (c) D5's second finding: a trailing slash is a directory spelling, not a
    #     regular file, and must not be normalised into the oracle row
    def trailing_slash(e):
        for f in e['normalized_result']['files']:
            if f['relative_path'].endswith('var/info.txt'):
                f['relative_path'] = f['relative_path'] + '/'

    slash_frozen, slash_recs = build(env_over={'V4': trailing_slash})
    add('a published file with a trailing slash fails the path shape',
        [slash_frozen, slash_recs], 0, 1, want_fail='path_shape_ok',
        runner=same_run(slash_recs))

    # (d) a score receipt relabelled as evidence is not an REA envelope
    add('score receipt relabelled as REA evidence',
        [frozen, mutant('V4', lambda e: e.__setitem__('counter_sha256', '0' * 64))],
        0, 1, want_fail='evidence_envelope_ok')

    # (e) D4: the receipt this counter writes carries an honest counter digest
    receipt_probes = []

    def probe_receipt(desc, doc, want_ok, want_text=None):
        ok, why = receipt_identity_ok(doc)
        receipt_probes.append({'desc': desc, 'ok': ok, 'why': why,
                               'want_ok': want_ok, 'want_text': want_text})

    stamp_path = os.path.join(work, 'receipt-identity-probe.json')
    _stamped, _wrote_ok, _wrote_why = write_receipt({'selftest': 'identity'}, stamp_path)
    written_receipt = json.load(open(stamp_path))
    probe_receipt('receipt this counter wrote', written_receipt, True)
    no_counter = dict(written_receipt)
    no_counter.pop('counter_sha256', None)
    probe_receipt('receipt without counter_sha256', no_counter, False,
                  'missing counter_sha256')
    null_counter = dict(written_receipt)
    null_counter['counter_sha256'] = None
    probe_receipt('receipt with counter_sha256 null', null_counter, False,
                  'counter_sha256 is null')
    wrong_counter = dict(written_receipt)
    wrong_counter['counter_sha256'] = '0' * 64
    probe_receipt('receipt whose counter_sha256 names other bytes', wrong_counter,
                  False, 'does not describe')
    short_counter = dict(written_receipt)
    short_counter['counter_sha256'] = 'abc'
    probe_receipt('receipt with a truncated counter_sha256', short_counter, False,
                  '64 hex')
    no_path = dict(written_receipt)
    no_path.pop('counter', None)
    probe_receipt('receipt without the counter path', no_path, False,
                  'missing counter path')

    # ---- published chain (Sentinel H2): the fetch receipt is the provenance
    bad_fetch_frozen, bad_fetch_recs = build(
        fetch_over={'V3': fetch_receipt('V3',
                                        final_url='https://other.example.invalid/x')})
    add('fetch receipt records a redirect', [bad_fetch_frozen, bad_fetch_recs],
        0, 1, want_fail='fetch_receipt_ok')
    bad_status_frozen, bad_status_recs = build(
        fetch_over={'V3': fetch_receipt('V3', http_status=302)})
    add('fetch receipt records a non-200', [bad_status_frozen, bad_status_recs],
        0, 1, want_fail='fetch_receipt_ok')
    bad_pin_frozen, bad_pin_recs = build(
        fetch_over={'V3': fetch_receipt('V3', pin='0' * 64)})
    add('fetch receipt pins another carve', [bad_pin_frozen, bad_pin_recs],
        0, 1, want_fail='fetch_receipt_ok')
    http_doc = json.loads(spec_json())
    http_doc['carriers'][0]['external']['url'] = 'http://download.example.invalid/x'
    add('carrier url is not https',
        [{**frozen, CARRIERS: json.dumps(http_doc, indent=1)}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    path_doc = json.loads(spec_json())
    path_doc['carriers'][0].pop('external')
    path_doc['carriers'][0]['path'] = f'{AFTERDIR}/V3/carrier.sqsh'
    add('a path-committed carrier is not a published carrier',
        [{**frozen, CARRIERS: json.dumps(path_doc, indent=1)}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    kind_doc = json.loads(spec_json(kind_over={'V3': 'lane-built'}))
    add('a carrier whose kind is not "published"',
        [{**frozen, CARRIERS: json.dumps(kind_doc, indent=1)}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    sid_doc = json.loads(spec_json())
    sid_doc['carriers'][0]['source_id'] = 'S999'
    add('carrier source_id names no SOURCES row',
        [{**frozen, CARRIERS: json.dumps(sid_doc, indent=1)}, good], 0, 1,
        want_fail='b:carrier_sources_ok')
    tc_doc = json.loads(spec_json())
    tc_doc['toolchain']['sasquatch']['sha256'] = '0' * 64
    add('frozen toolchain pin is not the binary on the fixed PATH',
        [{**frozen, CARRIERS: json.dumps(tc_doc, indent=1)}, good], 0, 1,
        want_fail='b:extractor_bin_ok')

    # ---- extract-env (Sentinel H1): which extractor ran
    env_doc = json.loads(extract_env('V3'))
    env_doc['sasquatch']['sha256'] = '0' * 64
    env_frozen, env_recs = build(extract_over={'V3': json.dumps(env_doc)})
    add('extract-env names another sasquatch digest', [env_frozen, env_recs],
        0, 1, want_fail='extract_env_ok')
    env_le = json.loads(extract_env('V4'))
    env_le['unblob_log']['command_line'] = (
        'sasquatch -le -no-exit-code -f -d <outdir> <inpath>')
    env_le_frozen, env_le_recs = build(extract_over={'V4': json.dumps(env_le)})
    add('extract-env log runs the wrong endianness flag',
        [env_le_frozen, env_le_recs], 0, 1, want_fail='extract_env_ok')
    env_v4be = json.loads(extract_env('V3'))
    env_v4be['unblob_log']['command_line'] = (
        'sasquatch-v4be -f -d <outdir> <inpath>')
    env_v4be_frozen, env_v4be_recs = build(
        extract_over={'V3': json.dumps(env_v4be)})
    add('extract-env log names sasquatch-v4be',
        [env_v4be_frozen, env_v4be_recs], 0, 1, want_fail='extract_env_ok')

    # ---- freshness reads only the frozen prior-pins table (Sentinel H3)
    prior_text = json.dumps({'rounds': [38, 39, 40, 41],
                             'pins': [{'sha256': pins['V3'],
                                       'source': '.ufo/waves/round-41/c1/carriers.json',
                                       'id': 'V3'}]}, indent=1)
    prior_frozen, prior_recs = build(prior_text=prior_text)
    add('prior-pins names a frozen carrier pin', [prior_frozen, prior_recs],
        0, 1, want_fail='carrier_fresh_ok')

    # ---- published set equality (L1 tightening): an extra file is a divergence
    def extra_file(e):
        pub(e, 'var/extra.txt', fsha(21), 9)

    extra_frozen, extra_recs = build(env_over={'V4': extra_file})
    add('an extra published regular file is a divergence',
        [extra_frozen, extra_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(extra_recs))

    # ---- carve_ok is the unblob chunk end, so a padded carrier is legitimate
    padded = sb_v3('standard', 'le')
    padded = padded + b'\x00' * (round_up(len(padded), 4096) - len(padded))
    padded_frozen, padded_recs = build(blob_over={'V3': padded})

    def check_padded(res):
        v = res['carriers']['V3']
        if v.get('carve_ok') is not True:
            return 'carve_ok false on a padded carrier: %r' % (v.get('carve'),)
        if (v.get('carve') or {}).get('chunk_end') != len(padded):
            return 'chunk_end %r != %d' % ((v.get('carve') or {}).get('chunk_end'),
                                           len(padded))
        return None

    add('carrier padded to the 4096 boundary (unblob chunk end)',
        [padded_frozen, padded_recs], 0, 0, runner=same_run(padded_recs),
        check=check_padded)
    # a carve that stops at bytes_used truncates the padding unblob wants
    short_frozen, short_recs = build(blob_over={'V3': padded},
                                     length_over={'V3': 241})
    add('frozen carve length is bytes_used, not the chunk end',
        [short_frozen, short_recs], 0, 1, want_fail='carve_ok')

    fails = []
    green = red = 0
    discriminating = 0
    prefix_probes = [
        ('root itself', 'x_extract', 'x_extract', True),
        ('segment-bounded child', 'x_extract/var/info.txt', 'x_extract', True),
        ('$output sigil', '$output/x_extract/var/info.txt', 'x_extract', True),
        ('non-segment-bounded root (x_extract2)', 'x_extract2/var/info.txt',
         'x_extract', False),
        ('suffix is not containment', 'other/x_extract/var', 'x_extract', False),
        ('empty path', '', 'x_extract', False),
    ]
    prefix_results = []
    for desc, path, root, want in prefix_probes:
        got = under_root(path, root)
        # the naive prefix rule this replaced, kept so the probe discriminates
        naive = path.startswith(root)
        prefix_results.append({'desc': desc, 'path': path, 'root': root,
                               'segment_bounded': got, 'naive_startswith': naive,
                               'want': want})
        if got != want:
            fails.append('prefix probe %r: under_root %r, want %r'
                         % (desc, got, want))
    for p in receipt_probes:
        if p['ok'] != p['want_ok']:
            fails.append('receipt probe %r: ok=%r want %r (%s)'
                         % (p['desc'], p['ok'], p['want_ok'], p['why']))
        elif p['want_text'] and p['want_text'] not in (p['why'] or ''):
            fails.append('receipt probe %r: reason %r lacks %r'
                         % (p['desc'], p['why'], p['want_text']))
    if not _wrote_ok:
        fails.append('stamped receipt failed its own identity check: %s' % _wrote_why)
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
            for step, files in enumerate(c['steps']):
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
                              carrier_cache=CACHE)
                got = 0 if res['met_target'] else 1
                why = None
                failing = set()
                for k, v in res['carriers'].items():
                    failing |= {x for x in CLAUSES if v.get(x) is not True}
                failing |= {'b:' + x for x in BINDINGS if res['bindings'][x] is not True}
            except FrozenPathChanged as e:
                got, why, res, failing = 2, e.reason, None, set()
                err = str(e)
            except Unevaluable as e:
                got, why, res, failing = 2, e.reason, None, set()
                err = str(e)
            else:
                err = None
            if os.environ.get('C1_SELFTEST_DETAIL'):
                if res is None:
                    detail = {'exit': got, 'reason': why, 'error': err}
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
            if ok and c['check'] is not None and res is not None:
                problem = c['check'](res)
                if problem:
                    ok = False
                    fails.append('%s: %s' % (c['name'], problem))
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
                      'prefix_probes': len(prefix_probes),
                      'receipt_probes': len(receipt_probes),
                      'probe_results': (path_probes + root_probes + spec_probes
                                        + prefix_results + receipt_probes),
                      'failures': fails}))
    return 0 if not fails else 1


def selftest_rea(pkg65, unblob, timeout, dev_carrier=None):
    """Real-REA end-to-end: two REA runs of one SquashFS v3 development image.

    Builds a one-carrier fixture lane (target 1) whose committed receipt is the
    first real run, measures it with the counter's real runner (second run) and
    expects met_target, then replaces the receipt with an oracle-only fabrication
    and expects a projection mismatch. The oracle comes from `unsquashfs`, a
    reader that is not sasquatch and not REA.

    The image must be a development input the caller is entitled to extract
    (`--dev-carrier`): an unblob 26.6.4 test fixture or the OpenWrt Kamikaze 7.09
    image. Never a published C1 candidate."""
    if not dev_carrier or not os.path.isfile(dev_carrier):
        raise SystemExit('--dev-carrier PATH is required and must exist: a v3 '
                         'image this run may extract, never a published C1 '
                         'candidate')
    here = os.path.dirname(os.path.abspath(__file__))
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    raw_image = open(dev_carrier, 'rb').read()
    pair = next(((v, e) for v, d in MAGIC_BY_VARIANT.items()
                 for e, m in d.items() if m == raw_image[0:4]), None)
    if pair is None:
        raise SystemExit('not a v3 family image: magic %r' % (raw_image[0:4],))
    variant, endian = pair
    handler = HANDLER_BY_VARIANT[variant]
    used = int.from_bytes(raw_image[63:71], 'big' if endian == 'be' else 'little')
    if not (SQUASHFS3_SB_SIZE <= used <= len(raw_image)):
        raise SystemExit('development image has no usable bytes_used: %r' % (used,))
    # carve_ok requires the carrier to be exactly its filesystem: the fixture
    # carrier is the image truncated to bytes_used, the whole-input chunk shape
    # the claim's carriers are carved to.
    image = raw_image[:used]
    pin = hashlib.sha256(image).hexdigest()
    probe = layout_probe(image, {'magic': raw_image[0:4].decode('latin1'),
                                 'endianness': endian, 'major': 3,
                                 'variant': variant})
    if not probe.get('compression_signatures'):
        raise SystemExit('development image has no compressed metadata block: %r'
                         % (probe.get('reason'),))
    superblock = {'magic': raw_image[0:4].decode('latin1'), 'endianness': endian,
                  'major': 3, 'minor': probe['minor'], 'variant': variant,
                  'compression': probe['compression']}

    sroot = scratch_root()
    work = tempfile.mkdtemp(prefix='c1-selftest-rea.', dir=sroot)
    runner = make_real_runner(work, unblob, timeout)
    out = {'image': os.path.abspath(dev_carrier), 'image_sha256': pin,
           'bytes': len(image), 'carved_to_bytes_used': used,
           'handler': handler, 'superblock': superblock,
           'layout_probe': {k: probe.get(k) for k in
                            ('ok', 'reason', 'compression', 'compression_signatures',
                             'meta_signal', 'bytes_used')}}

    # oracle from a reader that is not sasquatch and not REA
    unsq = shutil.which('unsquashfs')
    if unsq is None:
        raise SystemExit('unsquashfs not on PATH (the oracle must not be sasquatch)')
    root = os.path.join(work, 'oracle')
    os.makedirs(root)
    carrier = os.path.join(work, 'carrier.sqsh')
    with open(carrier, 'wb') as fh:
        fh.write(image)
    p = subprocess.run([unsq, '-n', '-f', '-d', root, carrier], capture_output=True)
    oracle_rows, nonreg_rows = [], []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            if os.path.islink(full):
                nonreg_rows.append((rel, 'symlink', os.readlink(full)))
                continue
            if not os.path.isfile(full):
                continue
            data = open(full, 'rb').read()
            oracle_rows.append((rel, hashlib.sha256(data).hexdigest(), len(data)))
    oracle_rows.sort()
    oracle_tsv = ''.join('%s\t%s\t%d\n' % r for r in oracle_rows)
    nonreg_tsv = ''.join('%s\t%s\t%s\n' % r for r in nonreg_rows)
    out['unsquashfs_rc'] = p.returncode
    out['unsquashfs_stderr'] = p.stderr.decode('utf-8', 'replace')[:400]
    out['oracle_files'] = len(oracle_rows)
    out['oracle_rows'] = oracle_rows
    out['nonregular_rows'] = nonreg_rows

    # first real run -> committed receipt
    status, env = runner(image, 'D1')
    if status != 'ok':
        raise SystemExit('first REA run produced no evidence object: %r' % (env,))
    nr = env['normalized_result']
    out['committed_evidence_id'] = env.get('evidence_id')
    out['committed_handlers'] = [c.get('handler') for c in nr.get('chunks') or []]
    out['committed_chunk_ranges'] = [c.get('range') for c in nr.get('chunks') or []]
    out['committed_derivations'] = [(d.get('handler'), d.get('child_path'))
                                    for d in nr.get('derivations') or []]
    out['committed_parameters'] = env.get('parameters')
    out['committed_files'] = [(f.get('relative_path'), f.get('size'))
                              for f in nr.get('files') or []]
    out['committed_gaps'] = [(g.get('kind'), g.get('relative_path'))
                             for g in nr.get('extraction_gaps') or []]
    out['committed_unpublished'] = [(u.get('kind'), u.get('relative_path'))
                                    for u in nr.get('unpublished_entries') or []]
    out['committed_diagnostics'] = [((d.get('report') or {}).get('__typename__'),
                                     (d.get('report') or {}).get('link'))
                                    for d in nr.get('diagnostics') or []]

    d = tempfile.mkdtemp(prefix='c1-selftest-rea-repo.', dir=sroot)
    try:
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        ident = ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
        receipt_path = f'{AFTERDIR}/D1/after.json'
        # the dev arm exercises the extraction path, not provenance: the carrier is
        # a development fixture, so its "publication" fields are synthetic but
        # schema-shaped, and its bytes reach the counter through --carrier-cache.
        cache = os.path.join(work, 'cache')
        os.makedirs(cache, exist_ok=True)
        with open(os.path.join(cache, pin + '.bin'), 'wb') as fh:
            fh.write(image)
        dev_url = 'https://dev.example.invalid/%s' % os.path.basename(dev_carrier)
        dev_image_pin = hashlib.sha256(b'dev-image').hexdigest()
        dev_member_pin = hashlib.sha256(b'dev-member').hexdigest()
        toolchain = {'sasquatch': {'sha256': file_sha256(which_fixed('sasquatch') or '')},
                     'unblob': {'sha256': file_sha256(which_fixed('unblob') or '')}}
        rpkg = {'version': REA_VERSION,
                'package_json_sha256': file_sha256(os.path.join(
                    os.path.abspath(pkg65), 'package.json')),
                'package_lock_sha256': file_sha256(next(
                    (p for p in (os.path.join(os.path.dirname(os.path.abspath(pkg65)),
                                              'package-lock.json'),
                                 os.path.join(os.path.dirname(os.path.dirname(
                                     os.path.abspath(pkg65))), 'package-lock.json'))
                     if os.path.isfile(p)), ''))}
        flag = '-le' if endian == 'le' else '-be'
        extract_env = json.dumps({
            'sasquatch': {'path': which_fixed('sasquatch'), 'version': '4.5.1',
                          'sha256': toolchain['sasquatch']['sha256']},
            'unblob': {'path': which_fixed('unblob'), 'version': '26.6.4',
                       'sha256': toolchain['unblob']['sha256']},
            'path': FIXED_PATH,
            'unblob_log': {'command_line': 'sasquatch %s -no-exit-code -f -d '
                                           '<outdir> <inpath>' % flag,
                           'sha256': hashlib.sha256(b'dev-log').hexdigest()},
        }, indent=1)
        out['extract_env'] = json.loads(extract_env)
        frozen = {
            XPIN: xpin,
            REA_PKG: json.dumps(rpkg, indent=1),
            PRIOR_PINS: json.dumps({'rounds': [38, 39, 40, 41], 'pins': []}),
            CARRIERS: json.dumps({
                'claim': 'R42-C1', 'target': 1, 'toolchain': toolchain,
                'carriers': [{'id': 'D1', 'kind': 'published',
                              'source_id': 'S240',
                              'sha256': pin, 'handler': handler,
                              'superblock': superblock,
                              'fetch_receipt': '.ufo/waves/round-42/c1/fetch-D1.json',
                              'external': {'url': dev_url,
                                           'image_sha256': dev_image_pin,
                                           'member': './var/tmp/fs.image',
                                           'member_sha256': dev_member_pin,
                                           'length': len(image), 'offset': 0},
                              'oracle': f'{AFTERDIR}/D1/oracle.tsv',
                              'nonregular': f'{AFTERDIR}/D1/nonregular.tsv'}]},
                indent=1),
            GAPRULE: json.dumps(
                {'claim': 'R42-C1',
                 'allowed': {'symlink': ['unpublished-entry'],
                             'device': ['unpublished-entry']}},
                indent=1),
            'plans/round-42-claims.md': '# plan\n',
            'tools/round-42/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
            'PROVINCE.md': _province(),
            ENTRY: _entry('S240'),
            'corpus/SOURCES.md': _registry(
                'S240', used=ENTRY,
                source_rows=[('S240', 'https://dev.example.invalid/')]),
            'corpus/README.md': _readme(STEM),
            '.ufo/waves/round-42/c1/fetch-D1.json': json.dumps({
                'url': dev_url, 'final_url': dev_url, 'http_status': 200,
                'content_length': 4096, 'image_sha256': dev_image_pin,
                'member': './var/tmp/fs.image', 'member_sha256': dev_member_pin,
                'carve_len': len(image), 'pin': pin,
                'tool_sha256': hashlib.sha256(b'fetch-tool').hexdigest()},
                indent=1),
            f'{AFTERDIR}/D1/extract-env.json': extract_env,
            f'{AFTERDIR}/D1/oracle.tsv': oracle_tsv.encode(),
            f'{AFTERDIR}/D1/nonregular.tsv': nonreg_tsv.encode(),
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
        commit({receipt_path: json.dumps(env)})
        freeze, rev = revs[0], revs[-1]

        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('D1',), unblob=unblob, rea_timeout=timeout,
                          carrier_cache=cache)
            got = 0 if res['met_target'] else 1
            v = res['carriers']['D1']
            out['green'] = {'exit': got, 'met_target': res['met_target'],
                            'carriers_matched': res['carriers_matched'],
                            'failing': sorted({x for x in CLAUSES
                                               if v.get(x) is not True}),
                            'bindings_false': sorted(x for x in BINDINGS
                                                     if res['bindings'][x] is not True),
                            'projection_diff': v.get('projection_diff'),
                            'oracle_hits': [v.get('oracle_hits'), v.get('oracle_files')],
                            'extract_root': v.get('extract_root'),
                            'gaps_note': v.get('gaps_note'),
                            'layout_ok': v.get('layout_ok'),
                            'layout_reason': v.get('layout_reason'),
                            'carve': v.get('carve'), 'handler': v.get('handler'),
                            'chunk_handlers': v.get('chunk_handlers')}
        except Unevaluable as e:
            out['green'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        # oracle-only fabrication: publish exactly the oracle, no chunk geometry
        # and no diagnostics (what a receipt built from oracle.tsv alone holds;
        # the projection is a coarsening, so a fabrication that reproduced the
        # chunk geometry too would be semantically equal to a real run - that is
        # the documented limit of this binding, not a hole in it)
        fab = mk_env('carrier.sqsh', pin, handler=handler,
                     files=[(rel, h, size) for rel, h, size in oracle_rows],
                     chunks=[], diags=[], outdir=os.path.join(work, 'fab', 'out'))
        fab['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': fab})['m']
        commit({receipt_path: json.dumps(fab)})
        rev = revs[-1]
        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('D1',), unblob=unblob, rea_timeout=timeout,
                          carrier_cache=cache)
            v = res['carriers']['D1']
            out['fabrication'] = {'exit': 0 if res['met_target'] else 1,
                                  'met_target': res['met_target'],
                                  'failing': sorted({x for x in CLAUSES
                                                     if v.get(x) is not True}),
                                  'projection_diff': v.get('projection_diff'),
                                  'evidence_id_ok': v.get('evidence_id_ok')}
        except Unevaluable as e:
            out['fabrication'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        # a one-carrier wheel cannot satisfy endianness_coverage (the wheel would
        # need both ends of sasquatch), so that binding is excluded from the
        # assertion and reported as measured
        g = out.get('green', {})
        ok = (g.get('carriers_matched') == 1 and g.get('failing') == []
              and set(g.get('bindings_false') or []) <= {'endianness_coverage'}
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
