#!/usr/bin/env python3
"""R41-C1 counter (coverage: genuine AVM-layout big-endian SquashFS v4 -> Core).

Predicate P41-C1 (draft `plans/round-41-claims.md`, embedded here clause by clause):
  At the measured revision, for each frozen AVM carrier, the committed round-41
  REA 6.5.0 `extract-firmware` after-receipt (unblob 26.6.4, sasquatch-v4be 4.5.1
  reachable on the child PATH), first added in a commit that descends from the
  freeze, names the `squashfs_v4_be` handler with no failed chunk, publishes every
  regular file of the frozen independent oracle at the exact path relative to the
  chunk's extract root (same sha256), publishes no non-regular entry at its exact
  path, carries only the extraction gaps the frozen gap rule allows, has a
  subject digest equal to the carrier pin and recomputes to its evidence id; the
  carrier bytes hash to the frozen pin and its superblock is the genuine AVM
  layout (big-endian `sqsh`, v4.0, `mkfs_time == bytes_used`, first metadata block
  length little-endian); **and** a fresh REA run of the same carrier made by this
  counter at scoring time (scratch output directory) yields the same semantic
  projection as the committed receipt (routed R39-CL5: a receipt fabricated from
  the oracle, however its evidence id is minted, cannot equal a real run);
  PROVINCE.md holds a `## Round-41 additions to Core` row naming the AVM layout
  that cites the round-41 knowledge entry, which cites a SOURCES.row opened
  2026-10-26 whose used-by lists it; a round-41 frontier note supersedes the AVM
  part of the Frontier text; corpus/README.md maps the entry stem; no frozen C1
  path changed after the freeze.

Target: carriers_matched == 4 (V3, V4, L3, L4) and every binding true.

The extract root (R40-CL1 repair; R41C1Revenger 1 is the normative rule)
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
                       starts `squashfs_v4` (FirmwareReports.js:341-357 taken from
                       unblob's own subtasks); a whole-file chunk's root is
                       `firmware.bin_extract` (`selected.bin_extract` under a
                       range selection), and a carved or nested chunk's root is
                       `<parent>/<start>-<end>.<handler>_extract`
    one root           the subject root is that root when the receipt has exactly
                       one; several `squashfs_v4` roots are ambiguous and the
                       freeze can name the intended one with the optional
                       `oracle_root` key of the carrier entry, otherwise the
                       three path clauses fail closed with `extract_root: null`
    whole segments     `rel(P)` is `''` for P == root, `P[len(root)+1:]` for
                       `P.startswith(root + '/')`, else None - an entry outside
                       the root belongs to another namespace (a carve artifact of
                       the parent, a sibling root, a deeper root) and is neither
                       compared against this oracle nor reported as published
    keyed by root      with one root per carrier the (root, rel) key collapses to
                       rel, and a path outside the root cannot satisfy a row
                       (R41C1Revenger C3: two roots carry `sbin/tool` with
                       different bytes)
  Round 40 matched with `candidate.endswith('/' + rel)` (defect R40-CL1: the
  regular file `usr/bin/busy` scored as the symlink entry `bin/busy`). Neither a
  suffix nor a fixed number of `_extract` segments is a root: a carve at a
  nonzero offset (`<root>/4096-6513.squashfs_v4_be_extract/...`) and a nested
  image (`<root>/nested/inner.squashfs_extract/...`) move the root as deep as
  the path to the chunk (R41C1Revenger C1/C2/C5).

Removal disposition (R41C1DevCore 7.1-7.3, for the V4 rootfs carrier)
  unblob deletes escaping symlinks after reporting `MaliciousSymlinkRemoved`,
  deletes empty-target symlinks with no report at all, and never publishes a
  link as a regular file. The frozen gap rule may therefore carry a `removed`
  block; `gaps_ok` then becomes a three-family disposition check:
    path-resolved gap   kind allowed for that entry's kind (as before)
    removal             every diagnostic the rule names (`removed.diagnostic`)
                        must resolve at its exact path to a non-regular entry
                        whose kind is in `removed.kinds`, and no entry may be
                        both gapped and removed
    silent              an entry whose kind and FROZEN detail are listed under
                        `removed.silent` may carry no record at all; the check is
                        per row (stricter than the count rule the routing text
                        states, which the freeze should re-word to match), so
                        nothing else can hide behind the allowance. The detail is
                        the frozen `nonregular.tsv` third column - the oracle's
                        own record - never a value the scored run writes, so the
                        admission token cannot be minted by the run
  A diagnostic's path is its `report.link`, an absolute path inside REA's private
  extraction root; it is mapped by locating the subject root as whole segments and
  taking the remainder. With no `removed` block the clause behaves exactly as in
  round 40 (a required entry must be gapped).
  The rerun projection carries diagnostics as `[__typename__, rel]` instead of
  the typename alone, so a rerun that removed a *different* link no longer
  matches (R41C1DevCore 7.3).

Per-carrier clauses (all must hold; `matched` = conjunction):
  carrier_present          the carrier blob exists at REV
  carrier_pin_ok           sha256(bytes at REV) == the frozen pin
  carrier_fresh_ok         the pin is not one a previous C1 freeze already scored:
                           every committed `.ufo/waves/round-*/c1/carriers.json`
                           pin, every committed `corpus/evidence/**/after.json`
                           subject digest and carriers.json `prior_pins`, all read
                           at the freeze commit. The claim's kill rule names
                           relabelled round-40 receipts as a control that must
                           stop C1; without this clause a rename is
                           indistinguishable from new coverage
  layout_ok                genuine AVM layout (see layout_probe): BE `sqsh` magic,
                           v4.0, mkfs_time == bytes_used (the AVM marker),
                           0 < bytes_used <= file size, and the 2-byte metadata
                           block header at inode_table_start decodes as a
                           little-endian block length (1..8192) while the
                           big-endian decode does not, or the single-block
                           identity `inode_table_start + 2 + len ==
                           directory_table_start` settles it
  oracle_ok                oracle.tsv parses (rel, sha256[, size]); >= 1 row; no
                           duplicate paths; every sha256 is 64 hex
  nonregular_ok            nonregular.tsv parses (rel, kind[, detail]); empty is
                           allowed; duplicate (rel, kind) rows are not
  carve_ok                 the carrier is exactly the filesystem it claims: for an
                           external carrier the frozen carve `length` equals the
                           superblock `bytes_used` and the bytes are that length;
                           for a committed carrier the file size equals
                           `bytes_used`. A sloppy carve leaves trailing bytes, the
                           chunk stops being the whole input, and the oracle root
                           moves one `<start>-<end>.<handler>_extract` deeper
  receipt_present          corpus/evidence/round-41/c1/<id>/after.json parses
  receipt_fresh            its first-add commit at REV is a strict descendant of
                           --freeze (not the freeze commit itself)
  subject_pin_ok           subject.digest.sha256 == the frozen pin
  operation_ok             operation == extract_firmware and provider.id == unblob
  handler_ok               exactly one chunk names squashfs_v4_be (two AVM
                           filesystems in one receipt cannot be told apart)
  chunks_ok                no chunk carries extraction_failed: true
  geometry_agrees          the derivation root equals the root implied by the
                           receipt's own chunk geometry (`chunks[].range` +
                           handler + the leading extract directory): a whole-file
                           chunk -> the leading directory, a carve ->
                           `<leading>/<start>-<end>.<handler>_extract`. A
                           disagreement means the root and the chunk tell
                           different stories about which directory holds the
                           filesystem
  oracle_hits_ok           every oracle regular file is published at its exact
                           path under the chunk extract root (rel ==, sha256 ==
                           and size ==), the root taken from the receipt's
                           `derivations[]` edge, not from path text
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
                           relative to the chunk extract root, so a deeper file
                           whose path merely ends with the entry path is not one
  run_provenance_ok        parameters.output_directory names this round's scratch
                           segment (/kaidoku-r41/); `parameters` is inside the
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
                           target; exactly that many distinct ids; the expected id
                           set; distinct pins; id/path/sha256/oracle/nonregular
                           present and well-formed; an external carrier also
                           names `member_sha256` (and `nested.sha256` when it has
                           a `nested` block), so the fetch chain is bound in the
                           table rather than in the fetcher (routed R40-CL6); an
                           optional `oracle_root` must be a path string and
                           `prior_pins` a list of 64-hex pins
  gap_rule_ok              gap-rule.json parses to {allowed: {kind: [gap kind]},
                           required?: {kind: bool}, removed?: {diagnostic, kinds,
                           disposition, silent?}, structural?: {kind: limit}};
                           every non-regular kind that appears in any frozen
                           nonregular.tsv is a key of `allowed`
  compression_coverage     >= 1 carrier with the gzip compression id and >= 1 with
                           an xz id (2 = squashfs-tools XZ, 4 = the lane writer's
                           xz), so both decompressor legs are bound
  frozen_tables_valid      carriers.json and gap-rule.json parse at the freeze
                           commit itself (routed R39-CL4)

Documentation bindings:
  province_core_section    PROVINCE.md has the `## Round-41 additions to Core`
                           heading
  province_core_row        a table row in that section whose first cell names
                           `squashfs_v4_be`, whose text names the AVM layout
                           (AVM[ _-]layout) and cites the entry path
  frontier_note            one line carries `Round-41 frontier note`, the entry
                           stem and the AVM-layout token
  entry_present            the knowledge entry exists at REV
  sourced                  the entry's `source:` lines name an S-id whose
                           corpus/SOURCES.md row is opened 2026-10-26 and lists the
                           entry (path or stem) in used-by
  coverage_map_row         corpus/README.md `## Coverage map` maps the entry stem

Freeze-drift binding (routed defect R38-CL4, kept): if any commit in FREEZE..REV
touches plans/round-41-claims.md, tools/round-41/c1-counter.py,
.ufo/waves/round-41/c1/carriers.json, .ufo/waves/round-41/c1/gap-rule.json, or any
carrier/oracle/nonregular file carriers.json lists, the counter exits 2 with
reason `frozen_path_changed` and never reports met. A later restore does not
un-block (the log of the range is inspected, not the endpoints).

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
  REA's inventory races unblob's symlink fix-up (`ENOENT ... readlink <link>`
  inside the extraction), measured twice on the round-40 V1 carrier in this wave,
  so a rerun is retried up to 3 times on exactly that failure - each attempt a
  fresh outdir and a real run - and the count is recorded
  (`projection_attempts`). No other failure is retried, and a retry never
  weakens the comparison: the projection still has to match.
  `--no-rerun` is not a mode of the predicate: it exits 2 (`rerun_disabled`) and
  never reports met.

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT
                [--json-out PATH] [--unblob PATH] [--rea-timeout SECONDS]
  c1-counter.py --selftest  --pkg65 REA650_PKG_ROOT
  c1-counter.py --selftest-rea --pkg65 REA650_PKG_ROOT [--unblob PATH]
                [--rea-timeout SECONDS]
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed, rerun environment error, --no-rerun). Reads lane bytes only
through git objects (`git show REV:path`); writes only a private scratch dir
under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/kaidoku-r41/counter and
--json-out.

`--selftest` is offline and deterministic: it drives measure() in-process with a
simulated REA runner (the simulator only exists inside selftest(); main() never
passes anything but the real runner). `--selftest-rea` is the real-path check:
it runs REA 6.5.0 on the retained development AVM image
/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs
(sha256 c7f74691...; NOT a C1 carrier), builds a one-carrier fixture lane around
two real runs and asserts a green verdict, then relabels an oracle-only
fabrication and asserts it red.
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

CARRIERS = '.ufo/waves/round-41/c1/carriers.json'
GAPRULE = '.ufo/waves/round-41/c1/gap-rule.json'
AFTERDIR = 'corpus/evidence/round-41/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md'
STEM = '2026-10-26-r41-avm-be-squashfs-core'
CORE_HEADING = '## Round-41 additions to Core'
FRONTIER_MARK = 'Round-41 frontier note'
HANDLER = 'squashfs_v4_be'
SQUASHFS_PREFIX = 'squashfs_v4'         # derivation handlers of a SquashFS chunk
XPIN = 'tools/round-27/xpin-attribute.mjs'
PRIOR_TABLE_RE = re.compile(r'^\.ufo/waves/round-[^/]+/c1/carriers\.json$')
OPENED = '2026-10-26'
TARGET = 4
IDS = ('V3', 'V4', 'L3', 'L4')
PROV_SEGMENT = '/kaidoku-r41/'
REA_PIN = 'rea-agents@6.5.0'
METADATA_MAX = 8192
UNCOMPRESSED_FLAG = 0x8000
GZIP_ID = 1
XZ_IDS = (2, 4)
DEV_AVM_IMAGE = ('/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/'
                 'avm-be.squashfs')
FROZEN_PATHS = (
    'plans/round-41-claims.md',
    'tools/round-41/c1-counter.py',
    'tools/round-41/c1-extra.py',
    'tools/round-41/c1-run.sh',
    'tools/round-41/fetch-vendor.py',
    'tools/round-41/sqfs-list.py',
    'tools/round-41/gen-squashfs.py',
    'tools/round-41/mk-l-carriers.py',
    CARRIERS,
    GAPRULE,
)
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
AVM_LAYOUT_RE = re.compile(r'AVM[ _-]layout', re.IGNORECASE)
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
            'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
            'gap_rule_ok', 'compression_coverage', 'frozen_tables_valid')
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'carrier_fresh_ok', 'layout_ok',
           'carve_ok', 'oracle_ok', 'nonregular_ok', 'receipt_present',
           'receipt_fresh', 'subject_pin_ok', 'operation_ok', 'handler_ok',
           'chunks_ok', 'geometry_agrees', 'oracle_hits_ok', 'gaps_ok',
           'nonregular_unpublished_ok', 'run_provenance_ok', 'evidence_id_ok',
           'projection_ok')


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


def scratch_root():
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                     'kaidoku-r41', 'counter')
    os.makedirs(d, exist_ok=True)
    return d


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

def evidence_ids(root, freeze, pkg65, envelopes, work):
    """Recompute the stored evidence id under the rea-agents 6.5.0 rule.

    The rule is not retyped: the frozen xpin tool evaluates the package's own
    `semanticProjection` and hashes it with the package's own digest code."""
    tool = show(root, freeze, XPIN)
    if tool is None:
        raise Unevaluable('xpin tool absent at freeze')
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
    r = subprocess.run(['node', tpath, '--pkg65', pkg65, '--pkg67', pkg65]
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
    """(rows[(rel, sha256)], error) for oracle.tsv. >= 2 columns, 64-hex digest."""
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
        rows.append((rel, sha))
    if not rows:
        return [], 'no rows'
    seen = set()
    for rel, _ in rows:
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
    if claim is not None and claim != 'R41-C1':
        probs.append('claim %r != R41-C1' % (claim,))
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
    if 'claim' in spec and spec.get('claim') != 'R41-C1':
        probs.append('claim %r != R41-C1' % (spec.get('claim'),))
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
    """Decode the AVM layout signals of a carrier's SquashFS v4 superblock.

    SquashFS v4 big-endian superblock: magic 0:4, inodes 4:8, mkfs_time 8:12,
    block_size 12:16, fragments 16:20, compression 20:22, block_log 22:24,
    flags 24:26, no_ids 26:28, s_major 28:30, s_minor 30:32, root_inode 32:40,
    bytes_used 40:48, id_table_start 48:56, xattr_id_table_start 56:64,
    inode_table_start 64:72, directory_table_start 72:80, ... (96 bytes).

    The AVM layout keeps every superblock field big-endian and writes the 2-byte
    metadata block-length header (bit 15 = uncompressed, bits 0..14 = length)
    little-endian. The marker `mkfs_time == bytes_used` is a timestamp proxy and
    is necessary but not sufficient: a standard BE body with a normalised
    timestamp carries it and fails extraction, so the block-length endianness is
    the format test."""
    d = {'size': len(raw) if raw is not None else 0}
    if raw is None:
        d.update(ok=False, reason='absent')
        return d
    if len(raw) < 96:
        d.update(ok=False, reason='shorter than a 96-byte superblock')
        return d
    d['magic'] = raw[0:4].decode('latin1')
    d['be_magic'] = raw[0:4] == b'sqsh'
    d['mkfs_time'] = int.from_bytes(raw[8:12], 'big')
    d['block_size'] = int.from_bytes(raw[12:16], 'big')
    d['compression'] = int.from_bytes(raw[20:22], 'big')
    d['major'] = int.from_bytes(raw[28:30], 'big')
    d['minor'] = int.from_bytes(raw[30:32], 'big')
    d['bytes_used'] = int.from_bytes(raw[40:48], 'big')
    d['inode_table_start'] = its = int.from_bytes(raw[64:72], 'big')
    d['directory_table_start'] = dts = int.from_bytes(raw[72:80], 'big')
    d['marker'] = d['mkfs_time'] == d['bytes_used']
    d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)
    d['version_v4'] = (d['major'], d['minor']) == (4, 0)
    d['meta_header_hex'] = None
    d['meta_len_le'] = d['meta_len_be'] = None
    d['le_plausible'] = d['be_plausible'] = False
    d['le_identity'] = d['be_identity'] = False
    d['layout_le'] = False
    d['meta_signal'] = 'none'
    if not (0 < its <= len(raw) - 2):
        d.update(ok=False, reason='inode_table_start %d outside the file' % its)
        return d
    hdr = raw[its:its + 2]
    d['meta_header_hex'] = hdr.hex()
    le = int.from_bytes(hdr, 'little')
    be = int.from_bytes(hdr, 'big')
    d['meta_len_le'] = le &~ UNCOMPRESSED_FLAG
    d['meta_len_be'] = be &~ UNCOMPRESSED_FLAG
    d['meta_flag_le'] = bool(le & UNCOMPRESSED_FLAG)
    d['meta_flag_be'] = bool(be & UNCOMPRESSED_FLAG)
    d['le_plausible'] = 1 <= d['meta_len_le'] <= METADATA_MAX
    d['be_plausible'] = 1 <= d['meta_len_be'] <= METADATA_MAX
    d['le_identity'] = its + 2 + d['meta_len_le'] == dts
    d['be_identity'] = its + 2 + d['meta_len_be'] == dts
    if d['le_plausible'] and not d['be_plausible']:
        d['layout_le'] = True
        d['meta_signal'] = 'plausibility'
    elif d['le_plausible'] and d['be_plausible']:
        if d['le_identity'] and not d['be_identity']:
            d['layout_le'] = True
            d['meta_signal'] = 'identity'
        else:
            d['meta_signal'] = 'ambiguous'
    else:
        d['meta_signal'] = 'be' if d['be_plausible'] else 'neither'
    reason = None
    if not d['be_magic']:
        reason = 'magic %r is not big-endian sqsh' % (d['magic'],)
    elif not d['version_v4']:
        reason = 'version %d.%d is not 4.0' % (d['major'], d['minor'])
    elif not d['marker']:
        reason = 'AVM marker absent (mkfs_time %d != bytes_used %d)' % (
            d['mkfs_time'], d['bytes_used'])
    elif not d['bytes_used_sane']:
        reason = 'bytes_used %d outside 1..%d' % (d['bytes_used'], len(raw))
    elif not d['layout_le']:
        reason = 'first metadata block length is not little-endian (%s)' % d['meta_signal']
    d['ok'] = reason is None
    d['reason'] = reason
    return d


# ------------------------------------------------------------- receipt shape

def provenance_ok(output_directory):
    """A receipt run by this round: absolute, inside the kaidoku-r41 scratch
    segment, and without a `..` segment that could leave it."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:
        return False
    return '..' not in output_directory.split('/')


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


def squashfs_roots(env):
    """The receipt's chunk extract roots, read from its own derivations.

    unblob's subtasks are published as `derivations[]` edges and the child path
    is the directory a chunk was extracted into (rea-agents 6.5.0
    FirmwareReports.js:341-357). Only edges whose handler starts
    `squashfs_v4` are filesystem roots for this claim: a whole-file chunk's root
    is `firmware.bin_extract` (`selected.bin_extract` under a range selection),
    a carved chunk's root is `<parent>/<start>-<end>.<handler>_extract`, and a
    nested image's root is `<parent>/<path to image>_extract`.

    Returns them deepest first, so a caller that wants a deterministic default
    sees the most specific root first; the counter never uses that order to guess
    (see subject_root)."""
    nr = env.get('normalized_result') or {}
    out = set()
    for d in nr.get('derivations') or []:
        if not isinstance(d, dict):
            continue
        h = d.get('handler')
        if not (isinstance(h, str) and h.startswith(SQUASHFS_PREFIX)):
            continue
        child = strip_output(d.get('child_path'))
        if isinstance(child, str) and child:
            out.add(child.rstrip('/'))
    return sorted(out, key=lambda r: (-len(r), r))


def subject_root(env, hint=None):
    """(extract root, how) of the chunk whose filesystem the oracle describes.

    Exactly one `squashfs_v4` derivation root is the normal case and needs no
    hint. Several roots (a wrapper carrier that also extracted a nested image)
    cannot be resolved from the receipt alone, so the freeze may name the
    intended root per carrier (`oracle_root` in carriers.json); without that hint
    the answer is None and the three path clauses fail closed. A hint that names
    no root at all is a frozen-table error and also resolves to None."""
    roots = squashfs_roots(env)
    if not roots:
        return None, 'no squashfs_v4 derivation edge'
    if hint is not None:
        if hint not in roots:
            return None, 'oracle_root %r not among %r' % (hint, roots)
        return hint, 'oracle_root from carriers.json'
    if len(roots) == 1:
        return roots[0], 'single squashfs_v4 derivation root'
    return None, 'ambiguous: %d squashfs_v4 roots %r (freeze oracle_root)' % (
        len(roots), roots)


def chunk_roots(env, hint=None):
    """[{extract_root, subject}] for the receipt, for reporting."""
    root, how = subject_root(env, hint)
    return {'roots': squashfs_roots(env), 'subject': root, 'source': how}


def diagnostic_rel(diagnostic, root):
    """A removal diagnostic's entry path relative to the chunk extract root.

    unblob reports `MaliciousSymlinkRemoved(link=<absolute path inside its
    extraction dir>, target=...)` (unblob extractor.py:79-87) and REA stores it
    with `input_path` naming the task directory, so the entry path exists only in
    `link`. The root is located as a run of whole segments and the remainder is
    the entry's path; None when the link carries no such run (that diagnostic
    cannot be resolved and fails the disposition check closed)."""
    if root is None or not isinstance(diagnostic, dict):
        return None
    report = diagnostic.get('report')
    link = report.get('link') if isinstance(report, dict) else None
    if not isinstance(link, str) or not link:
        return None
    segs = [x for x in link.split('/') if x not in ('', '.')]
    rsegs = root.split('/')
    for i in range(len(segs) - len(rsegs), -1, -1):
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
    if root is None:
        return 0
    hits = 0
    for rel, sha in oracle:
        if any(sha == fs and same_rel(fp, rel, root) for fp, fs, _ in files):
            hits += 1
    return hits


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


def disposition_check(gaps_list, diags, nonreg, model, root):
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
            rel = diagnostic_rel(d, root)
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
    """(pins, sources) a previous C1 freeze already scored, read at the freeze.

    The claim's kill rule names "relabelled round-40 receipts" as a control that
    must stop C1, so a carrier whose bytes (or whose receipt subject) a previous
    freeze already scored cannot count as new coverage however the table names
    it. The forbidden set is derived from the tree, not from one round's table,
    because a narrow set would let a future AVM-layout carrier from an older
    round through (today `layout_ok` happens to reject the older LE/standard-BE
    carriers, which is identity work the layout clause should not be doing):

      every committed `.ufo/waves/round-<r>/c1/carriers.json` pin (any round)
      every committed `corpus/evidence/**/after.json` subject digest
      carriers.json `prior_pins` - an explicit list, the belt
    All three are read from the FREEZE commit, so a table added later cannot
    bless an old pin, and this claim's own carriers.json / evidence directory are
    excluded (a freeze that somehow contained them would otherwise flag itself).
    """
    pins, sources = set(), []
    listed = spec.get('prior_pins')
    if isinstance(listed, list):
        for p in listed:
            if isinstance(p, str) and SHA_RE.match(p.lower()):
                pins.add(p.lower())
        if listed:
            sources.append('prior_pins')
    p = git(root, 'ls-tree', '-r', '--name-only', freeze, '--', '.ufo/waves',
            'corpus/evidence', check=False)
    if p.returncode != 0:
        raise Unevaluable('git ls-tree failed at the freeze commit')
    names = [l for l in p.stdout.decode(errors='replace').splitlines() if l]
    tables = sorted(n for n in names
                    if PRIOR_TABLE_RE.match(n) and n != CARRIERS)
    receipts = sorted(n for n in names
                      if n.startswith('corpus/evidence/') and n.endswith('/after.json')
                      and not n.startswith(AFTERDIR + '/'))
    from_table = 0
    for n in tables:
        raw = show(root, freeze, n)
        try:
            doc = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            doc = None
        if not isinstance(doc, dict):
            continue
        for c in doc.get('carriers') or []:
            if isinstance(c, dict) and isinstance(c.get('sha256'), str) \
                    and SHA_RE.match(c['sha256'].lower()):
                pins.add(c['sha256'].lower())
                from_table += 1
    from_receipt = 0
    for n in receipts:
        raw = show(root, freeze, n)
        try:
            doc = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            doc = None
        if not isinstance(doc, dict):
            continue
        sha = ((doc.get('subject') or {}).get('digest') or {}).get('sha256')
        if isinstance(sha, str) and SHA_RE.match(sha.lower()):
            pins.add(sha.lower())
            from_receipt += 1
    if tables:
        sources.append('%d prior c1/carriers.json (%d pins)' % (len(tables), from_table))
    if receipts:
        sources.append('%d prior after.json (%d digests)' % (len(receipts), from_receipt))
    return pins, sources


def frozen_drift(root, freeze, rev, spec):
    """Commits in FREEZE..REV that touch a frozen C1 path (freeze-drift binding)."""
    frozen = set(FROZEN_PATHS)
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        for key in ('path', 'oracle', 'nonregular'):
            v = c.get(key)
            if isinstance(v, str) and v:
                frozen.add(v)
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
    for d in nr.get('diagnostics') or []:
        if not isinstance(d, dict):
            continue
        typename = diagnostic_typename(d) or '<none>'
        rel = diagnostic_rel(d, proj_root) if proj_root else None
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


RETRY_ATTEMPTS = 3          # bounded retry for REA's inventory/symlink race only

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


def rea_inventory_race(payload):
    """Is this failed REA run the inventory/symlink race (retryable by us)?

    Measured payload (round-40 V1, this wave): `error.details.diagnostics.reason`
    = "ENOENT: no such file or directory, readlink '<extraction>/<link>'" with
    `category: execution_failure`. Only that shape is retried; anything else is
    reported as it happened."""
    err = payload.get('error') if isinstance(payload, dict) else None
    if not isinstance(err, dict):
        return False
    reason = ''
    details = err.get('details')
    if isinstance(details, dict):
        diag = details.get('diagnostics')
        if isinstance(diag, dict) and isinstance(diag.get('reason'), str):
            reason = diag['reason']
    text = ' '.join([reason, str(err.get('message') or '')])
    return 'readlink' in text and 'ENOENT' in text


def make_real_runner(work, unblob, timeout, attempts=RETRY_ATTEMPTS):
    """REA 6.5.0 extract-firmware on the given carrier bytes, fresh outdir.

    The run replays the committed receipt's recorded extraction parameters
    (`parameters.max_depth`, `max_output_bytes`, `max_output_files`). A receipt
    produced at `--max-depth 1` is `partial` with a truncated published set, so a
    rerun at REA's default depth 3 could never match it under a profile that
    compares `coverage` or `published_bytes`.

    REA's own inventory races unblob's symlink fix-up: `inventoryFirmwareOutput`
    walks the extraction while `fix_extracted_directory` rewrites/removes links,
    so a run of a carrier with many symlinks can die with
    `ENOENT ... readlink '<...>/<link>'` (`execution_failure`, non-retryable in its
    own words). Measured on the round-40 V1 carrier twice in this wave. A bounded
    retry on exactly that failure is a measurement-stability fix, not a weakening:
    every attempt is a fresh outdir and a real run of the same bytes, the
    projection is still compared, and the attempts are recorded
    (`projection_attempts`). Any other failure is reported as it happened."""
    unblob_path = unblob or os.path.expanduser('~/.local/bin/unblob')

    def attempt(carrier_bytes, cid, params, n):
        d = os.path.join(work, 'rerun-%s-%d'
                         % (re.sub(r'[^A-Za-z0-9_.-]', '_', str(cid)), n))
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
            # keep REA's own error object: the reason must be in the record
            return 'no_data', {'ok': envl.get('ok'), 'exit': p.returncode,
                               'attempt': n, 'replayed': replayed,
                               'error': envl.get('error'),
                               'stdout_head': text[:300],
                               'stderr': p.stderr.decode('utf-8', 'replace')[:300]}
        return 'ok', data

    def run(carrier_bytes, cid, params=None):
        if shutil.which('npx') is None:
            raise RerunEnvError('npx not on PATH')
        tried = []
        for n in range(1, attempts + 1):
            status, payload = attempt(carrier_bytes, cid, params, n)
            if status == 'ok':
                if isinstance(payload, dict):
                    payload['attempts'] = len(tried) + 1
                return 'ok', payload
            tried.append(payload)
            if not rea_inventory_race(payload):
                break
        return 'no_data', {'attempts': tried}

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
                subj = env.get('subject') or {}
                d['subject_pin_ok'] = ((subj.get('digest') or {}).get('sha256')
                                       if isinstance(subj, dict) else None) == pin
                prov = env.get('provider') or {}
                d['operation_ok'] = (env.get('operation') == 'extract_firmware'
                                     and isinstance(prov, dict) and prov.get('id') == 'unblob')
                # exactly one AVM chunk: two filesystems in one receipt cannot be
                # told apart (no clause may pick between them), so a legal carrier
                # extracts one; R41CritC1Draft asked for this explicitly
                d['handler_ok'] = chunk_handlers(env).count(HANDLER) == 1
                d['chunks_ok'] = not chunk_failed(env)
                root_value, root_how = subject_root(
                    env, (c.get('oracle_root')
                          if isinstance(c.get('oracle_root'), str) else None))
                d['extract_root'] = root_value
                d['extract_root_source'] = root_how
                d['chunk_roots'] = chunk_roots(
                    env, (c.get('oracle_root')
                          if isinstance(c.get('oracle_root'), str) else None))
                # Geometry cross-check, recorded not scored (R41CritC1Draft 2):
                # the extraction directory unblob would use for each AVM chunk,
                # from chunks[].range+handler, next to the derivation root. A
                # disagreement is visible per carrier without adding a clause
                # that no reserved carrier can be measured against yet.
                sel = (env.get('normalized_result') or {}).get('selection') or {}
                staged = sel.get('length') if isinstance(sel.get('length'), int) else None
                lead = None
                for pth in receipt_paths(env):
                    parts = path_parts(pth)
                    if parts and parts[0].endswith('_extract'):
                        lead = parts[0]
                        break
                geo = []
                for ch in (env.get('normalized_result') or {}).get('chunks') or []:
                    if not isinstance(ch, dict) or ch.get('handler') != HANDLER:
                        continue
                    rng = ch.get('range') or {}
                    off, ln = rng.get('offset'), rng.get('length')
                    whole = (off == 0 and staged is not None and ln == staged)
                    if not (isinstance(off, int) and isinstance(ln, int)):
                        exp = None
                    elif whole:
                        exp = lead
                    else:
                        exp = ('%s/%d-%d.%s_extract' % (lead, off, off + ln,
                                                        HANDLER)
                               if lead else None)
                    geo.append({'handler': ch.get('handler'), 'offset': off,
                                'length': ln, 'whole_input': whole,
                                'geometry_root': exp,
                                'agrees': exp == root_value})
                d['chunk_summary'] = geo
                d['geometry_agrees'] = bool(geo) and all(x['agrees'] for x in geo)
                if root_value:
                    rp = root_value.split('/')
                    d['extract_root_confirmed'] = any(
                        (path_parts(p) or [])[:len(rp)] == rp
                        for p in receipt_paths(env))
                else:
                    d['extract_root_confirmed'] = False
                files = published(env)
                d['published_files'] = len(files)
                d['oracle_hits'] = oracle_hits(oracle, files, root_value)
                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and root_value is not None
                                       and d['oracle_hits'] == d['oracle_files'])
                diags = diagnostics(env)
                d['diagnostics'] = len(diags)
                d['removals'] = sorted(
                    rel for rel, diag in
                    ((diagnostic_rel(x, root_value), x) for x in diags)
                    if rel is not None
                    and diagnostic_typename(diag) == (model.get('removed') or {}
                                                      ).get('diagnostic'))
                ok, why = disposition_check(gaps(env), diags, nonreg, model,
                                            root_value)
                d['gaps_ok'] = ok
                d['gaps_note'] = why
                esc = nonregular_published(files, nonreg, root_value)
                d['nonregular_published'] = esc[:5]
                d['nonregular_unpublished_ok'] = (root_value is not None
                                                  and not esc)
                params = env.get('parameters') or {}
                od = params.get('output_directory') if isinstance(params, dict) else None
                d['output_directory'] = od
                d['run_provenance_ok'] = provenance_ok(od)

                # rerun clause: fresh REA run of the REV carrier bytes
                if raw is not None and d['carrier_pin_ok']:
                    status, payload = runner(raw, k, params)
                    if status != 'ok':
                        d['projection_ok'] = False
                        d['projection_error'] = payload
                    else:
                        d['projection_attempts'] = payload.get('attempts')
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
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = matched
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
        HANDLER_RE.search(cells(r)[0]) and AVM_LAYOUT_RE.search(r) and ENTRY in r
        for r in rows)
    b['province_core_rows_seen'] = [
        cells(r)[0] for r in rows if HANDLER_RE.search(cells(r)[0])]
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and AVM_LAYOUT_RE.search(l)
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
    comps = [d.get('compression') for d in (res.get('carriers') or {}).values()]
    b['compression_coverage'] = (any(c == GZIP_ID for c in comps)
                                 and any(c in XZ_IDS for c in comps))
    b['compression_detail'] = comps
    b['frozen_tables_valid'] = bool(res.get('frozen_tables_valid'))
    res['bindings'] = b
    res['met_target'] = bool(res['carriers_unchanged'] and res['gap_rule_unchanged']
                             and res['carriers_matched'] == target
                             and all(b[x] is True for x in BINDINGS))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--pkg65')
    ap.add_argument('--json-out')
    ap.add_argument('--unblob')
    ap.add_argument('--carrier-cache',
                    help='directory holding <sha256>.bin for external vendor carriers '
                         '(filled by tools/round-41/fetch-vendor.py)')
    ap.add_argument('--rea-timeout', type=int, default=900)
    ap.add_argument('--no-rerun', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--selftest-rea', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.pkg65)
    if a.selftest_rea:
        return selftest_rea(a.pkg65, a.unblob, a.rea_timeout)
    if a.no_rerun:
        out = {'reason': 'rerun_disabled',
               'detail': 'P41-C1 binds a fresh REA run of each carrier; '
                         '--no-rerun cannot be scored',
               'argv': sys.argv, 'exit_code': 2}
        print(json.dumps({k: out[k] for k in ('reason', 'detail')}, sort_keys=True))
        if a.json_out:
            json.dump(out, open(a.json_out, 'w'), indent=1, sort_keys=True)
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
            json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 2
    res['argv'] = sys.argv
    res['exit_code'] = 0 if res['met_target'] else 1
    print(json.dumps({k: res[k] for k in ('revision', 'freeze', 'carriers_matched',
                                          'target', 'carriers_unchanged',
                                          'gap_rule_unchanged', 'frozen_path_changed',
                                          'bindings', 'met_target', 'exit_code')},
                     sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
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


def sb_carrier(compression, tag=b'', *, marker=True, meta_le=True,
               meta_header=None, identity_le=False, marker_value=None, pad=64):
    """A fixture carrier: a coherent BE SquashFS v4 superblock, a metadata block
    header at inode_table_start and nothing else.

    Not a real filesystem - the layout clause is a superblock test and these
    bytes exercise it exactly. `meta_le` writes a little-endian block length;
    `meta_header` writes given bytes verbatim (for headers whose length is
    plausible both ways); `identity_le` aims directory_table_start at the
    LE-computed next metadata block."""
    meta_len = 116 if meta_le else 58
    its = 512
    body = bytearray(its + 2 + pad)
    body[0:4] = b'sqsh'
    body[12:16] = (4096).to_bytes(4, 'big')
    body[20:22] = compression.to_bytes(2, 'big')
    body[28:30] = (4).to_bytes(2, 'big')
    body[30:32] = (0).to_bytes(2, 'big')
    if meta_header is not None:
        hdr = meta_header
    else:
        hdr = (meta_len | (0x8000 if meta_le else 0)).to_bytes(
            2, 'little' if meta_le else 'big')
    body[its:its + 2] = hdr
    used = len(body) if marker_value is None else marker_value
    mkfs = (used & 0xFFFFFFFF) if marker else 1700000000
    body[8:12] = mkfs.to_bytes(4, 'big')
    body[40:48] = used.to_bytes(8, 'big')
    body[64:72] = its.to_bytes(8, 'big')
    if identity_le:
        dts = its + 2 + (int.from_bytes(hdr, 'little') & ~UNCOMPRESSED_FLAG)
    else:
        dts = len(body) - 8
    body[72:80] = dts.to_bytes(8, 'big')
    if tag:
        body[-len(tag):] = tag
    return bytes(body)


def mk_env(name, pin, files=(), gaps=(), unpub=(), diags=(), chunks=None,
           outdir='/fast/scratch/hyaku/kaidoku-r41/selftest/after',
           subject_name='carrier.sqsh', chunk_dir='firmware.bin_extract',
           operation='extract_firmware', provider='unblob', derivations=None):
    """A receipt-shaped REA envelope (`data` object) for fixture carriers.

    `derivations` defaults to the one edge rea-agents 6.5.0 publishes for a
    whole-file chunk (`$input` -> `$output/<chunk_dir>`, handler
    `squashfs_v4_be`), which is what the counter reads the extract root from.
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
    consistent and `subject_root` still derives the same namespace."""
    e = json.loads(json.dumps(env))
    root = '/fast/scratch/hyaku/kaidoku-r41/counter/rerun/%s' % tag
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
                tail = diagnostic_rel({'report': {'link': link}}, old_root)
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


def _province(row=True, heading=CORE_HEADING, cell='`squashfs_v4_be`',
              layout='AVM layout', note=True, cited=ENTRY):
    r = f'| {cell} | {layout} | x | `{cited}` |\n' if row else ''
    fn = (f'- {FRONTIER_MARK}, 2026-10-26: the Frontier AVM-layout part is '
          f'superseded by `{STEM}`.\n') if note else ''
    return (f'# P\n\n{heading}\n\n| Surface | Layout | a | Entry |\n|---|---|---|---|\n{r}\n'
            f'## Next\n{fn}\n')


def _entry(sid='S1121'):
    return f'# E\n\nsource: {sid} - x\n'


def _registry(sid='S1121', opened=OPENED, used=ENTRY):
    rows = f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n'
    if sid != 'S112':
        rows += f'| S112 | s | docs | A | s | a | t | mined | {OPENED} | 180d | {ENTRY} |\n'
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

    # fixture carriers: AVM layout, gzip and xz legs
    carriers = {
        'V3': sb_carrier(GZIP_ID, b'V3-avm'),
        'V4': sb_carrier(4, b'V4-avm'),
        'L3': sb_carrier(GZIP_ID, b'L3-avm'),
        'L4': sb_carrier(2, b'L4-avm'),
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
                            outdir='/fast/scratch/hyaku/kaidoku-r41/selftest/%s-after' % k)
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

    rule = json.dumps({'claim': 'R41-C1',
                       'allowed': {'symlink': ['unpublished-entry'],
                                   'device': ['unpublished-entry']}}, indent=1)

    def spec_json(pin_map=None, drop=None, target=None, receipt_override=None,
                  projection=None, external=None, oracle_root=None,
                  external_drop=None, prior_pins=None):
        """carriers.json text. `external` turns one carrier into a vendor entry
        (with a member_sha256 block that `external_drop` can remove a key from)."""
        pm = pin_map or pins
        cs = []
        for k in ids:
            if drop and k in drop:
                continue
            c = {'id': k,
                 'sha256': pm[k],
                 'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
                 'nonregular': f'{AFTERDIR}/{k}/nonregular.tsv'}
            if k == external:
                ext = {'url': 'https://download.avm.de/fritzbox/x/y.image',
                       'image_sha256': 'a' * 64,
                       'member': './var/tmp/filesystem.image',
                       'member_sha256': 'b' * 64,
                       'length': 4096}
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
        spec = {'claim': 'R41-C1', 'carriers': cs}
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
             'plans/round-41-claims.md': b'# plan\n',
             'tools/round-41/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
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

    def add(name, steps, freeze_index, want, reason=None, want_fail=None,
            runner=sim_runner):
        cases.append({'name': name, 'steps': steps, 'freeze': freeze_index,
                      'want': want, 'reason': reason, 'want_fail': want_fail,
                      'runner': runner})

    green_frozen, green_receipts = build()
    frozen = frozen_files()
    good = receipts(green_envs)

    add('green (4 AVM carriers, fresh receipts, docs)', [green_frozen, green_receipts],
        0, 0)
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

    # ---- carrier layout controls
    stripped = sb_carrier(4, b'V3-stripped', marker=False)
    s_frozen, s_receipts = build(blob_over={'V3': stripped})
    add('marker-stripped genuine-LE-lengths carrier', [s_frozen, s_receipts], 0, 1,
        want_fail='layout_ok')
    add('standard-BE carrier (BE block lengths)',
        [build(blob_over={'V3': sb_carrier(GZIP_ID, b'V3-be', meta_le=False)})[0],
         build(blob_over={'V3': sb_carrier(GZIP_ID, b'V3-be', meta_le=False)})[1]],
        0, 1, want_fail='layout_ok')
    # 8c00: LE length 140, BE length 3072 - plausible both ways, asymmetric
    ambiguous = sb_carrier(GZIP_ID, b'V3-amb', meta_header=b'\x8c\x00', pad=200)
    add('metadata length plausible both ways (no identity)',
        [build(blob_over={'V3': ambiguous})[0], build(blob_over={'V3': ambiguous})[1]],
        0, 1, want_fail='layout_ok')
    amb_id = sb_carrier(GZIP_ID, b'V3-ambid', meta_header=b'\x8c\x00', pad=200,
                        identity_le=True)
    add('ambiguous length settled by the single-block identity',
        [build(blob_over={'V3': amb_id})[0], build(blob_over={'V3': amb_id})[1]], 0, 0)
    lx = sb_carrier(4, b'V3-le-magic')
    lx = b'hsqs' + lx[4:]
    add('little-endian superblock magic', [build(blob_over={'V3': lx})[0],
                                          build(blob_over={'V3': lx})[1]], 0, 1,
        want_fail='layout_ok')
    big_used = sb_carrier(GZIP_ID, b'V3-used', marker_value=0xFFFFFFF0)
    add('bytes_used beyond the file', [build(blob_over={'V3': big_used})[0],
                                      build(blob_over={'V3': big_used})[1]], 0, 1,
        want_fail='layout_ok')

    # ---- missing / malformed frozen inputs (absent at the freeze itself)
    no_carrier = {**frozen, f'{AFTERDIR}/V4/carrier.sqsh': None}
    add('carrier listed but never committed', [no_carrier, good], 0, 1,
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
        nonreg_over={'V4': 'bin/busy\tsymlink\n'})
    add('regular usr/bin/busy does not satisfy the symlink entry bin/busy',
        [deep_file, deep_recs], 0, 0, runner=same_run(deep_recs))
    # dir 2: the symlink entry's path ends with a regular file's path
    short_file, short_recs = build(
        env_over={'V4': lambda e: (pub(e, 'sbin/tool', fsha(8), 40),
                                   entry(e, 'usr/sbin/tool', target='tool'))},
        nonreg_over={'V4': 'usr/sbin/tool\tsymlink\n'})
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
            'handler': 'squashfs_v4', 'encrypted': False,
            'root_file_range': {'offset': 4096, 'length': 2048},
            'extraction_failed': False})
        e['normalized_result']['derivations'].append({
            'parent_path': '$output/firmware.bin_extract',
            'child_path': '$output/firmware.bin_extract/core.sqsh_extract',
            'handler': 'squashfs_v4',
            'provider_blob_id': '3028394:2',
            'parent_file_range': {'offset': 4096, 'length': 2048}})
        if publish:
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/core.sqsh_extract/lib/x',
                'path': '/x/core.sqsh_extract/lib/x', 'size': 7,
                'sha256': fsha(11)})

    hint = spec_json(oracle_root={'V4': 'firmware.bin_extract'})
    two_ok, two_ok_recs = build(
        env_over={'V4': lambda e: add_nested_chunk(e, True)}, spec_text=hint)
    add('two chunks with oracle_root: the nested file is another namespace',
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
             'single squashfs_v4 derivation root'),
            ('two roots with oracle_root', two_ok_recs, 'firmware.bin_extract',
             'firmware.bin_extract', 'oracle_root from carriers.json'),
            ('two roots without a hint', two_amb_recs, None, None,
             'ambiguous')):
        e = json.loads(envs[receipt_path('V4')])
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
    PORTION = 'firmware.bin_extract/4096-4500.squashfs_v4_be_extract'
    rule_struct1 = json.dumps({'claim': 'R41-C1',
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
             'single squashfs_v4 derivation root'),
            ('portion chunk, shallow publish', pad_shallow_recs, PORTION,
             'single squashfs_v4 derivation root')):
        e = json.loads(recs[receipt_path('V4')])
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
             'child_path': '$output/firmware.bin_extract/0-2500.squashfs_v4_be_extract',
             'provider_blob_id': 'p0', 'handler': HANDLER,
             'parent_file_range': {'offset': 0, 'length': 2500}},
            {'parent_path': '$input',
             'child_path': '$output/firmware.bin_extract/2500-5000.squashfs_v4_be_extract',
             'provider_blob_id': 'p1', 'handler': HANDLER,
             'parent_file_range': {'offset': 2500, 'length': 2500}}]
        e['normalized_result']['files'] = [
            {'relative_path': 'firmware.bin_extract/0-2500.squashfs_v4_be_extract/'
                              'var/info.txt',
             'path': '/x/var/info.txt', 'size': 40, 'sha256': fsha(3)},
            {'relative_path': 'firmware.bin_extract/2500-5000.squashfs_v4_be_extract/'
                              'etc/x',
             'path': '/x/etc/x', 'size': 9, 'sha256': fsha(14)}]
        e['normalized_result']['extraction_gaps'] = [
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '0-2500.squashfs_v4_be_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c0'},
            {'kind': 'depth-limited', 'input_path': '$output/firmware.bin_extract/'
             '2500-5000.squashfs_v4_be_extract', 'relative_path': None,
             'handler': None, 'dependencies': [], 'continuation_id': 'c1'}]
        e['normalized_result']['unpublished_entries'] = []

    two_frozen, two_recs2 = build(rule_text=rule_struct1,
                                  env_over={'V4': two_portion_chunks})
    add('two AVM chunks in one receipt are ambiguous, not guessed',
        [two_frozen, two_recs2], 0, 1, want_fail='gaps_ok',
        runner=same_run(two_recs2))
    e = json.loads(two_recs2[receipt_path('V4')])
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

    mix_frozen, mix_recs = build(env_over={'V4': outside_namespace})
    add('a file outside the subject root is another namespace, not an extra',
        [mix_frozen, mix_recs], 0, 0, runner=same_run(mix_recs))
    e = json.loads(mix_recs[receipt_path('V4')])
    r, src = subject_root(e)
    root_probes.append({'desc': 'outside-namespace file', 'root': r, 'source': src,
                        'want_root': 'firmware.bin_extract',
                        'want_src': 'single squashfs_v4 derivation root',
                        'chunk_roots': chunk_roots(e)})

    def no_derivations(e):
        e['normalized_result']['derivations'] = []

    nod_frozen, nod_recs = build(env_over={'V4': no_derivations})
    add('receipt with no squashfs derivation edge fails closed',
        [nod_frozen, nod_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nod_recs))

    # ---- removal disposition (R41C1DevCore 7.1-7.3, for the V4 rootfs carrier)
    # unblob deletes escaping symlinks after reporting MaliciousSymlinkRemoved and
    # empty-target symlinks with no report at all, and never publishes a link as a
    # regular file. V4's rootfs carrier needs the allowance, so the frozen rule may
    # carry a `removed` block and every row must land in exactly one disposition.
    rule_removed = json.dumps({
        'claim': 'R41-C1',
        'allowed': {'symlink': ['unpublished-entry'],
                    'device': ['unpublished-entry']},
        'required': {'symlink': True, 'device': True},
        'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                    'disposition': 'exclusive'},
        'structural': {'depth-limited': 1}}, indent=1)

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
                           'link': '/x/firmware.bin_extract/' + diag_rel,
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
                                                  'link': '/x/firmware.bin_extract/'
                                                          'dev/console',
                                                  'target': '/x'}}))})
    add('a removal naming a row of an unlisted kind fails',
        [dev_frozen, dev_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(dev_recs))
    # silent empty-target removal: unblob deletes the link and reports nothing
    rule_silent = json.dumps({
        'claim': 'R41-C1',
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
        'claim': 'R41-C1',
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
                           'link': '/x/firmware.bin_extract/' + which,
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
            '/x/firmware.bin_extract/bin/two'
        e['subject']['digest']['sha256'] = sha(carrier_bytes)
        e['normalized_result']['selection']['sha256'] = sha(carrier_bytes)
        return 'ok', rehost(e, 'selftest-other-removal')

    add('a rerun that removed a different link breaks the projection',
        [proj_frozen, proj_recs], 0, 1, want_fail='projection_ok',
        runner=other_removal_runner)

    # ---- the rerun retry only covers REA's own inventory race
    path_probes.append({
        'desc': 'REA inventory race is retryable',
        'new': rea_inventory_race({'error': {
            'category': 'execution_failure',
            'message': 'Analysis could not complete.',
            'details': {'diagnostics': {'reason':
                "ENOENT: no such file or directory, readlink "
                "'/x/extracted/firmware.bin_extract/sbin/lsmod'"}}}}),
        'legacy': rea_inventory_race({'error': {
            'category': 'output_limit',
            'message': 'Staging entry budget exceeded (10000)',
            'details': {'diagnostics': {'reason': 'too many entries'}}}}),
        'want_new': True, 'want_legacy': False, 'candidate': 'inventory-race',
        'rel': None})

    # ---- freshness: a relabelled previous-round carrier is not coverage
    add('relabelled previous-round pins (prior_pins)',
        [{**frozen, CARRIERS: spec_json(prior_pins=[pins[k] for k in ids])}, good],
        0, 1, want_fail='carrier_fresh_ok')
    prior_tbl = json.dumps({'claim': 'R40-C1', 'target': 4, 'carriers': [
        {'id': 'V1', 'sha256': pins['V3']},
        {'id': 'L2', 'sha256': pins['L4']}]})
    add('previous round table in the lane names two frozen pins',
        [{**frozen, '.ufo/waves/round-40/c1/carriers.json': prior_tbl}, good], 0, 1,
        want_fail='carrier_fresh_ok')
    add('prior_pins that are not 64-hex',
        [{**frozen, CARRIERS: spec_json(prior_pins=['not-a-pin'])}, good], 0, 1,
        want_fail='b:carriers_spec_ok')

    # ---- geometry cross-check and the receipt half of the freshness set
    def portion_geometry(e):
        """Chunk says "carved at 4096", derivation says "the whole input"."""
        e['normalized_result']['selection']['length'] = 4500
        e['locations'] = [{'kind': 'file-offset-range', 'start': 0, 'end': 4500}]
        e['normalized_result']['chunks'][0]['range'] = {'offset': 4096, 'length': 404}

    geom_frozen, geom_recs = build(env_over={'V4': portion_geometry})
    add('chunk geometry and derivation root disagree',
        [geom_frozen, geom_recs], 0, 1, want_fail='geometry_agrees',
        runner=same_run(geom_recs))
    prior_receipt = json.dumps({'subject': {'digest': {'sha256': pins['V3']}},
                                'normalized_result': {}})
    add('a committed prior receipt names the frozen carrier pin',
        [{**frozen,
          'corpus/evidence/round-40/c1/V1/after.json': prior_receipt}, good], 0, 1,
        want_fail='carrier_fresh_ok')

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
    # carve_ok: bytes longer than the superblock bytes_used
    over_len = sb_carrier(GZIP_ID, b'V3-long', marker_value=None)
    over_len = sb_carrier(GZIP_ID, b'V3-long', marker_value=len(over_len) - 64)
    o_frozen, o_recs = build(blob_over={'V3': over_len})
    add('carrier longer than its bytes_used (sloppy carve)',
        [o_frozen, o_recs], 0, 1, want_fail='carve_ok', runner=same_run(o_recs))

    # ---- freeze integrity
    add('carrier bytes changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/V3/carrier.sqsh': b'changed carrier\n'}],
        0, 2, 'frozen_path_changed')
    add('carrier bytes changed then restored',
        [frozen, {**good, f'{AFTERDIR}/V3/carrier.sqsh': b'changed carrier\n'},
         {**good, f'{AFTERDIR}/V3/carrier.sqsh': carriers['V3']}], 0, 2,
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
        [frozen, {**good, GAPRULE: json.dumps({'claim': 'R41-C1', 'allowed': {
            'symlink': ['unpublished-entry']}}).encode()}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json touched then restored',
        [frozen, {**good, GAPRULE: b'{}\n'}, {**good, GAPRULE: rule.encode()}], 0, 2,
        'frozen_path_changed')
    add('counter edited after freeze',
        [frozen, {**good, 'tools/round-41/c1-counter.py': b'#!/usr/bin/env python3\n'
         b'print(0)\n'}], 0, 2, 'frozen_path_changed')
    add('claims edited after freeze',
        [frozen, {**good, 'plans/round-41-claims.md': b'# new plan\n'}], 0, 2,
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
    one_leg = {k: sb_carrier(GZIP_ID, ('%s-gzip' % k).encode()) for k in ids}
    f1, r1 = build(blob_over=one_leg)
    add('no xz carrier (compression coverage)', [f1, r1], 0, 1,
        want_fail='b:compression_coverage')
    thin = json.dumps({'claim': 'R41-C1', 'allowed': {'symlink': ['unpublished-entry']}})
    f2, r2 = build(rule_text=thin)
    add('gap rule omits the device kind', [f2, r2], 0, 1, want_fail='b:gap_rule_ok')
    add('gap rule is JSON but not an object at the freeze',
        list(build(rule_text='[]')), 0, 1, want_fail='b:frozen_tables_valid')
    add('gap rule names another claim',
        list(build(rule_text=json.dumps({'claim': 'R39-C1', 'allowed': {
            'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}}))),
        0, 1, want_fail='b:gap_rule_ok')

    # ---- structural gaps (unblob bookkeeping: null relative_path)
    rule_struct = json.dumps({'claim': 'R41-C1',
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
    add('province row outside the round-41 section',
        [{**frozen, 'PROVINCE.md': _province(heading='## Round-39 additions to Core')},
         good], 0, 1, want_fail='b:province_core_row')
    add('province row without the handler in the first cell',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4_le`')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row that does not name the AVM layout',
        [{**frozen, 'PROVINCE.md': _province(layout='big-endian squashfs')}, good], 0, 1,
        want_fail='b:province_core_row')
    add('province row absent', [{**frozen, 'PROVINCE.md': _province(row=False)}, good],
        0, 1, want_fail='b:province_core_row')
    add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': _province(
            cited='corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md')}, good],
        0, 1, want_fail='b:province_core_row')
    add('frontier note absent', [{**frozen, 'PROVINCE.md': _province(note=False)}, good],
        0, 1, want_fail='b:frontier_note')
    add('frontier note without the AVM token',
        [{**frozen, 'PROVINCE.md': (f'# P\n\n{CORE_HEADING}\n\n| Surface | Layout | a | Entry |\n'
                                    f'|---|---|---|---|\n| `squashfs_v4_be` | AVM layout | x | '
                                    f'`{ENTRY}` |\n\n## Next\n- {FRONTIER_MARK}: `{STEM}`.\n')},
         good], 0, 1, want_fail='b:frontier_note')
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
                res = measure(d, rv, fz, pkg65, rerun=c['runner'])
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


def selftest_rea(pkg65, unblob, timeout):
    """Real-REA end-to-end: two runs of the retained development AVM image.

    Builds a one-carrier fixture lane (target 1) whose committed receipt is the
    first real run, then measures it with the counter's real runner (second run)
    and expects met_target. Then replaces the receipt with an oracle-only
    fabrication and expects a projection mismatch."""
    here = os.path.dirname(os.path.abspath(__file__))
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    if not os.path.isfile(DEV_AVM_IMAGE):
        raise SystemExit('development AVM image absent: ' + DEV_AVM_IMAGE)
    image = open(DEV_AVM_IMAGE, 'rb').read()
    # The retained image is a 4096-byte dump whose superblock says bytes_used 365.
    # carve_ok requires the carrier to be exactly its filesystem, so the fixture
    # carrier is the image truncated to bytes_used - the same filesystem, and the
    # whole-input chunk shape the claim's carriers are carved to.
    used = int.from_bytes(image[40:48], 'big')
    if not (0 < used <= len(image)):
        raise SystemExit('development AVM image has no usable bytes_used')
    image = image[:used]
    pin = hashlib.sha256(image).hexdigest()

    sroot = scratch_root()
    work = tempfile.mkdtemp(prefix='c1-selftest-rea.', dir=sroot)
    runner = make_real_runner(work, unblob, timeout)
    out = {'image': DEV_AVM_IMAGE, 'image_sha256': pin, 'bytes': len(image),
           'carved_to_bytes_used': used}

    # oracle from the independent extractor (sasquatch-v4be, no -be)
    sq = shutil.which('sasquatch-v4be')
    if sq is None:
        raise SystemExit('sasquatch-v4be not on PATH')
    root = os.path.join(work, 'oracle')
    os.makedirs(root)
    carrier = os.path.join(work, 'carrier.sqsh')
    with open(carrier, 'wb') as fh:
        fh.write(image)
    p = subprocess.run([sq, '-f', '-d', root, carrier], capture_output=True)
    oracle_rows = []
    for dirpath, _dirs, names in os.walk(root):
        for name in sorted(names):
            full = os.path.join(dirpath, name)
            if not os.path.isfile(full) or os.path.islink(full):
                continue
            rel = os.path.relpath(full, root).replace(os.sep, '/')
            data = open(full, 'rb').read()
            oracle_rows.append((rel, hashlib.sha256(data).hexdigest(), len(data)))
    oracle_rows.sort()
    oracle_tsv = ''.join('%s\t%s\t%d\n' % r for r in oracle_rows)
    out['sasquatch_rc'] = p.returncode
    out['oracle_files'] = len(oracle_rows)

    # first real run -> committed receipt
    status, env = runner(image, 'V3-committed')
    if status != 'ok':
        raise SystemExit('first REA run produced no evidence object: %r' % (env,))
    out['committed_evidence_id'] = env.get('evidence_id')
    out['committed_handlers'] = [c.get('handler')
                                 for c in env['normalized_result'].get('chunks') or []]

    d = tempfile.mkdtemp(prefix='c1-selftest-rea-repo.', dir=sroot)
    try:
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        ident = ['-c', 'user.name=fx', '-c', 'user.email=fx@fx']
        entry = 'corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md'
        stem = '2026-10-26-r41-avm-be-squashfs-core'
        frozen = {
            XPIN: xpin,
            '.ufo/waves/round-41/c1/carriers.json': json.dumps({
                'claim': 'R41-C1', 'target': 1,
                'carriers': [{'id': 'V3',
                              'path': 'corpus/evidence/round-41/c1/V3/carrier.sqsh',
                              'sha256': pin,
                              'oracle': 'corpus/evidence/round-41/c1/V3/oracle.tsv',
                              'nonregular': 'corpus/evidence/round-41/c1/V3/nonregular.tsv'}]},
                indent=1),
            '.ufo/waves/round-41/c1/gap-rule.json': json.dumps(
                {'claim': 'R41-C1', 'allowed': {'symlink': ['unpublished-entry']}},
                indent=1),
            'plans/round-41-claims.md': '# plan\n',
            'tools/round-41/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
            'PROVINCE.md': _province(),
            entry: _entry('S240'),
            'corpus/SOURCES.md': _registry('S240', used=entry),
            'corpus/README.md': _readme(stem),
            'corpus/evidence/round-41/c1/V3/carrier.sqsh': image,
            'corpus/evidence/round-41/c1/V3/oracle.tsv': oracle_tsv.encode(),
            'corpus/evidence/round-41/c1/V3/nonregular.tsv': b'',
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
        commit({'corpus/evidence/round-41/c1/V3/after.json': json.dumps(env)})
        freeze, rev = revs[0], revs[-1]

        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('V3',), unblob=unblob, rea_timeout=timeout)
            got = 0 if res['met_target'] else 1
            out['green'] = {'exit': got, 'met_target': res['met_target'],
                            'carriers_matched': res['carriers_matched'],
                            'failing': sorted({x for x in CLAUSES
                                               if res['carriers']['V3'].get(x) is not True}),
                            'bindings_false': sorted(x for x in BINDINGS
                                                     if res['bindings'][x] is not True),
                            'projection_diff': res['carriers']['V3'].get('projection_diff'),
                            'layout': res['carriers']['V3'].get('layout')}
        except Unevaluable as e:
            out['green'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        # oracle-only fabrication: publish exactly the oracle, no chunk geometry
        # and no diagnostics (what a receipt built from oracle.tsv alone holds;
        # the projection is a coarsening, so a fabrication that reproduced the
        # chunk geometry too would be semantically equal to a real run - that is
        # the documented limit of this binding, not a hole in it)
        fab = mk_env('carrier.sqsh', pin,
                     files=[(rel, h, size) for rel, h, size in oracle_rows],
                     chunks=[], diags=[],
                     outdir='/fast/scratch/hyaku/kaidoku-r41/selftest-rea/fab')
        fab['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': fab})['m']
        commit({'corpus/evidence/round-41/c1/V3/after.json': json.dumps(fab)})
        rev = revs[-1]
        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('V3',), unblob=unblob, rea_timeout=timeout)
            v = res['carriers']['V3']
            out['fabrication'] = {'exit': 0 if res['met_target'] else 1,
                                  'met_target': res['met_target'],
                                  'failing': sorted({x for x in CLAUSES
                                                     if v.get(x) is not True}),
                                  'projection_diff': v.get('projection_diff'),
                                  'evidence_id_ok': v.get('evidence_id_ok')}
        except Unevaluable as e:
            out['fabrication'] = {'exit': 2, 'reason': e.reason, 'detail': str(e)}

        # the one-carrier fixture lane cannot satisfy the two-leg compression
        # binding (the retained development image is xz only), so that binding
        # is excluded from the assertion and reported as measured
        g = out.get('green', {})
        ok = (g.get('carriers_matched') == 1 and g.get('failing') == []
              and set(g.get('bindings_false') or []) <= {'compression_coverage'}
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
