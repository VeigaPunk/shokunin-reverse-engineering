#!/usr/bin/env python3
"""R40-C1 counter (coverage: genuine AVM-layout big-endian SquashFS v4 -> Core).

Predicate P40-C1 (draft `plans/round-40-claims.md`, embedded here clause by clause):
  At the measured revision, for each frozen AVM carrier, the committed round-40
  REA 6.5.0 `extract-firmware` after-receipt (unblob 26.6.4, sasquatch-v4be 4.5.1
  reachable on the child PATH), first added in a commit that descends from the
  freeze, names the `squashfs_v4_be` handler with no failed chunk, publishes every
  regular file of the frozen independent oracle (same relative-path suffix, same
  sha256), carries only the extraction gaps the frozen gap rule allows, has a
  subject digest equal to the carrier pin and recomputes to its evidence id; the
  carrier bytes hash to the frozen pin and its superblock is the genuine AVM
  layout (big-endian `sqsh`, v4.0, `mkfs_time == bytes_used`, first metadata block
  length little-endian); **and** a fresh REA run of the same carrier made by this
  counter at scoring time (scratch output directory) yields the same semantic
  projection as the committed receipt (routed R39-CL5: a receipt fabricated from
  the oracle, however its evidence id is minted, cannot equal a real run);
  PROVINCE.md holds a `## Round-40 additions to Core` row naming the AVM layout
  that cites the round-40 knowledge entry, which cites a SOURCES.row opened
  2026-10-26 whose used-by lists it; a round-40 frontier note supersedes the AVM
  part of the Frontier text; corpus/README.md maps the entry stem; no frozen C1
  path changed after the freeze.

Target: carriers_matched == 4 (V1, V2, L1, L2) and every binding true.

Per-carrier clauses (all must hold; `matched` = conjunction):
  carrier_present          the carrier blob exists at REV
  carrier_pin_ok           sha256(bytes at REV) == the frozen pin
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
  nonregular_ok            nonregular.tsv parses (rel, kind[, ...]); empty is
                           allowed; duplicate (rel, kind) rows are not
  receipt_present          corpus/evidence/round-40/c1/<id>/after.json parses
  receipt_fresh            its first-add commit at REV is a strict descendant of
                           --freeze (not the freeze commit itself)
  subject_pin_ok           subject.digest.sha256 == the frozen pin
  operation_ok             operation == extract_firmware and provider.id == unblob
  handler_ok               a chunk names squashfs_v4_be
  chunks_ok                no chunk carries extraction_failed: true
  oracle_hits_ok           every oracle regular file is published (same
                           relative-path suffix, same sha256)
  gaps_ok                  every extraction gap lands on exactly one non-regular
                           entry and its kind is allowed for that entry's kind by
                           the frozen gap rule, and every entry the rule marks
                           required carries at least one allowed gap
  nonregular_unpublished_ok  no published regular file path equals a non-regular
                           entry path (a materialised symlink/device would both
                           publish the path and keep the gap)
  run_provenance_ok        parameters.output_directory names this round's scratch
                           segment (/kaidoku-r40/); `parameters` is inside the
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
                           present and well-formed
  gap_rule_ok              gap-rule.json parses to {allowed: {kind: [gap kind]},
                           required?: {kind: bool}}; every non-regular kind that
                           appears in any frozen nonregular.tsv is a key of
                           `allowed`
  compression_coverage     >= 1 carrier with the gzip compression id and >= 1 with
                           an xz id (2 = squashfs-tools XZ, 4 = the lane writer's
                           xz), so both decompressor legs are bound
  frozen_tables_valid      carriers.json and gap-rule.json parse at the freeze
                           commit itself (routed R39-CL4)

Documentation bindings:
  province_core_section    PROVINCE.md has the `## Round-40 additions to Core`
                           heading
  province_core_row        a table row in that section whose first cell names
                           `squashfs_v4_be`, whose text names the AVM layout
                           (AVM[ _-]layout) and cites the entry path
  frontier_note            one line carries `Round-40 frontier note`, the entry
                           stem and the AVM-layout token
  entry_present            the knowledge entry exists at REV
  sourced                  the entry's `source:` lines name an S-id whose
                           corpus/SOURCES.md row is opened 2026-10-26 and lists the
                           entry (path or stem) in used-by
  coverage_map_row         corpus/README.md `## Coverage map` maps the entry stem

Freeze-drift binding (routed defect R38-CL4, kept): if any commit in FREEZE..REV
touches plans/round-40-claims.md, tools/round-40/c1-counter.py,
.ufo/waves/round-40/c1/carriers.json, .ufo/waves/round-40/c1/gap-rule.json, or any
carrier/oracle/nonregular file carriers.json lists, the counter exits 2 with
reason `frozen_path_changed` and never reports met. A later restore does not
un-block (the log of the range is inspected, not the endpoints).

The rerun clause (routed R39-CL5)
  Between the receipt checks and the verdict, a carrier whose bytes hash to the
  pin and whose receipt parses is re-run by this counter:
      cwd = a private directory under $HYAKU_SCRATCH/kaidoku-r40,
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
  output directory, input file name and therefore the chunk extract directory
  name, evidence id, continuation ids, provider ids, timestamps, selection and
  analysis fields) is excluded; the field list is the one fixed by the
  R40C1Projection seat's item text (it is inlined here on purpose: scores must
  read frozen in-repo bytes, never a wave artifact). Ignoring the chunk
  directory is load bearing - the counter's own run stages the carrier as
  `carrier.bin`, so a suffix-normalising projection is what makes a real rerun
  comparable at all.

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
  c1-counter.py --selftest  --pkg65 REA650_PKG_ROOT
  c1-counter.py --selftest-rea --pkg65 REA650_PKG_ROOT [--unblob PATH]
                [--rea-timeout SECONDS]
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed, rerun environment error, --no-rerun). Reads lane bytes only
through git objects (`git show REV:path`); writes only a private scratch dir
under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/kaidoku-r40/counter and
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

CARRIERS = '.ufo/waves/round-40/c1/carriers.json'
GAPRULE = '.ufo/waves/round-40/c1/gap-rule.json'
AFTERDIR = 'corpus/evidence/round-40/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
STEM = '2026-10-26-r40-avm-be-squashfs-core'
CORE_HEADING = '## Round-40 additions to Core'
FRONTIER_MARK = 'Round-40 frontier note'
HANDLER = 'squashfs_v4_be'
XPIN = 'tools/round-27/xpin-attribute.mjs'
OPENED = '2026-10-26'
TARGET = 4
IDS = ('V1', 'V2', 'L1', 'L2')
PROV_SEGMENT = '/kaidoku-r40/'
REA_PIN = 'rea-agents@6.5.0'
METADATA_MAX = 8192
UNCOMPRESSED_FLAG = 0x8000
GZIP_ID = 1
XZ_IDS = (2, 4)
DEV_AVM_IMAGE = ('/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/'
                 'avm-be.squashfs')
FROZEN_PATHS = (
    'plans/round-40-claims.md',
    'tools/round-40/c1-counter.py',
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
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'layout_ok', 'oracle_ok',
           'nonregular_ok', 'receipt_present', 'receipt_fresh', 'subject_pin_ok',
           'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok',
           'gaps_ok', 'nonregular_unpublished_ok', 'run_provenance_ok',
           'evidence_id_ok', 'projection_ok')


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
                     'kaidoku-r40', 'counter')
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
    """(rows[(rel, kind)], error) for nonregular.tsv. Empty table is allowed."""
    if raw is None:
        return [], 'absent'
    rows = []
    for line in raw.decode(errors='replace').splitlines():
        if not line.strip():
            continue
        f = [c.rstrip('\r') for c in line.split('\t')]
        if len(f) < 2:
            return [], 'row %r has %d fields, want >= 2 (rel, kind)' % (line, len(f))
        rel = f[0].strip()
        kind = f[1].strip().lower()
        if (rel, kind) == ('relative_path', 'kind'):
            continue                      # tolerated header row
        if not rel or not kind:
            return [], 'empty path/kind in %r' % (line,)
        rows.append((rel, kind))
    seen = set()
    for row in rows:
        if row in seen:
            return [], 'duplicate nonregular row %r' % (row,)
        seen.add(row)
    return rows, None


def gap_rule_model(raw):
    """(model, problems) for gap-rule.json.

    model = {'allowed': {nonregular kind: [gap kind]}, 'required': {kind: bool}}.
    `required` is optional; a kind with a non-empty `allowed` list is required by
    default (a non-regular entry that produced no gap at all is a materialised
    entry, which is what R39-CL3 separates from a clean extraction)."""
    probs = []
    model = {'allowed': {}, 'required': {}, 'structural': {}}
    if raw is None:
        return model, ['absent']
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as e:
        return model, ['not JSON: %s' % e]
    if not isinstance(doc, dict):
        return model, ['not a JSON object']
    claim = doc.get('claim')
    if claim is not None and claim != 'R40-C1':
        probs.append('claim %r != R40-C1' % (claim,))
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
    return model, probs


def carriers_spec(spec, target, expected_ids):
    """(ids, problems) for the frozen carrier list."""
    probs = []
    if 'claim' in spec and spec.get('claim') != 'R40-C1':
        probs.append('claim %r != R40-C1' % (spec.get('claim'),))
    cs = spec.get('carriers')
    if not isinstance(cs, list):
        return [], probs + ['carriers is not a list']
    if 'target' in spec and spec.get('target') != target:
        probs.append('frozen target %r != counter target %d' % (spec.get('target'), target))
    prof = spec.get('projection', DEFAULT_PROFILE)
    if prof not in PROFILES:
        probs.append('projection profile %r not in %r' % (prof, list(PROFILES)))
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
        for key in ('id', 'path', 'sha256', 'oracle', 'nonregular'):
            v = c.get(key)
            if not isinstance(v, str) or not v:
                probs.append('carrier %r lacks %s' % (c.get('id'), key))
        sha = c.get('sha256')
        if isinstance(sha, str) and not SHA_RE.match(sha.lower()):
            probs.append('carrier %r sha256 is not 64 hex' % (c.get('id'),))
        receipt = c.get('receipt')
        if receipt is not None and not isinstance(receipt, str):
            probs.append('carrier %r receipt is not a string' % (c.get('id'),))
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
    """A receipt run by this round: absolute, inside the kaidoku-r40 scratch
    segment, and without a `..` segment that could leave it."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:
        return False
    return '..' not in output_directory.split('/')


def same_rel(candidate, rel):
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


def oracle_hits(oracle, files):
    hits = 0
    for rel, sha in oracle:
        if any(sha == fs and same_rel(fp, rel) for fp, fs, _ in files):
            hits += 1
    return hits


def nonregular_published(files, nonreg):
    hits = []
    for fp, _, _ in files:
        for rel, _kind in nonreg:
            if same_rel(fp, rel):
                hits.append(fp)
    return hits


def gap_check(gaps_list, nonreg, model):
    """Gaps only where the frozen rule allows them.

    Two families, both frozen data:
      path-resolved   a gap with a relative_path must resolve (suffix match) to
                      exactly one non-regular entry and its kind must be listed
                      for that entry's kind in `allowed`
      structural      a gap with relative_path null (unblob's own bookkeeping:
                      `unknown-chunk-handler` for a residual chunk,
                      `depth-limited` for a truncated task) must have its kind in
                      `structural` and must not exceed that kind's per-carrier
                      allowance
    Every entry whose kind is required must carry >= 1 allowed path-resolved gap."""
    allowed = model.get('allowed') or {}
    structural = model.get('structural') or {}
    required = model.get('required') or {}
    seen = {}
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
        hits = [r for r, _ in nonreg if same_rel(rp, r)]
        if len(hits) != 1:
            return False, 'gap path %r matches %d non-regular entries' % (rp, len(hits))
        entry_kind = dict(nonreg)[hits[0]]
        if kind not in allowed.get(entry_kind, []):
            return False, 'gap kind %r not allowed for %r entry %r (allowed %r)' % (
                kind, entry_kind, hits[0], allowed.get(entry_kind, []))
        seen.setdefault(hits[0], []).append(kind)
    over = {k: [n, structural[k]] for k, n in struct_count.items()
            if n > structural[k]}
    if over:
        return False, 'structural gaps over allowance %r' % (over,)
    missing = []
    for rel, kind in nonreg:
        need = required.get(kind, bool(allowed.get(kind)))
        if not need:
            continue
        if not seen.get(rel):
            missing.append(rel)
    if missing:
        return False, 'required gap absent on %r' % (sorted(missing),)
    return True, '%d gaps (%d structural) on %d non-regular entries' % (
        len(gaps_list), sum(struct_count.values()), len(nonreg))


def first_add(root, rev, path):
    p = git(root, 'log', '--diff-filter=A', '--format=%H', rev, '--', path, check=False)
    if p.returncode != 0:
        return None
    lines = [l.strip() for l in p.stdout.decode().splitlines() if l.strip()]
    return lines[-1] if lines else None


def is_ancestor(root, ancestor, descendant):
    p = git(root, 'merge-base', '--is-ancestor', ancestor, descendant, check=False)
    return p.returncode == 0


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
      core            the six fields of the P40-C1 draft (R40C1Projection's item
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

    hashes = {}
    if profile in ('plus-content', 'plus-extractor'):
        for task in (env.get('raw_result') or {}).get('report') or []:
            if not isinstance(task, dict):
                continue
            key = rel_suffix((task.get('task') or {}).get('path'))
            if key is None:
                continue
            for report in task.get('reports') or []:
                if isinstance(report, dict) and report.get('__typename__') == 'HashReport':
                    hashes[key] = [report.get('md5'), report.get('sha1')]

    files = []
    for e in nr.get('files') or []:
        if not isinstance(e, dict):
            continue
        row = [rel_suffix(e.get('relative_path')), e.get('sha256'), e.get('size')]
        if profile != 'core':
            row.append(e.get('mime_type'))
        if profile in ('plus-content', 'plus-extractor'):
            row += hashes.get(rel_suffix(e.get('relative_path')) or '', [None, None])
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
        deps = sorted((rel_suffix(d) for d in (g.get('dependencies') or [])),
                      key=lambda v: (v is not None, v or ''))
        gaps.append([g.get('kind'), rel_suffix(g.get('relative_path')), deps])
    gaps.sort(key=canonical)

    unpub = []
    for u in nr.get('unpublished_entries') or []:
        if not isinstance(u, dict):
            continue
        unpub.append([u.get('kind'), rel_suffix(u.get('relative_path'))])
    unpub.sort(key=canonical)

    diags = sorted(((d.get('report') or {}).get('__typename__') or '<none>')
                   for d in nr.get('diagnostics') or [] if isinstance(d, dict))

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
            edges.append([rel_suffix(deriv.get('parent_path')),
                          rel_suffix(deriv.get('child_path')),
                          deriv.get('handler')])
        edges.sort(key=canonical)
        engine = nr.get('engine') or {}
        out['derivations'] = edges
        out['engine'] = [engine.get('name'), engine.get('version')]
        out['published_bytes'] = nr.get('published_bytes')
        out['coverage'] = nr.get('coverage')
    return out


PROFILES = ('core', 'plus-mime', 'plus-content', 'plus-extractor')
DEFAULT_PROFILE = 'plus-extractor'      # L1 ruling, round 40 wave 1: every carrier
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
            return 'no_data', {'ok': envl.get('ok'), 'exit': p.returncode,
                               'replayed': replayed,
                               'stderr': p.stderr.decode('utf-8', 'replace')[:300]}
        return 'ok', data

    return run


# ------------------------------------------------------------- measurement

def measure(root, rev, freeze, pkg65, rerun=None, target=TARGET,
            expected_ids=IDS, unblob=None, rea_timeout=900):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P40-C1',
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

            raw = show(root, rev, cpath) if cpath else None
            d['carrier_path'] = cpath
            d['carrier_present'] = raw is not None
            d['carrier_pin_ok'] = (raw is not None and pin is not None
                                   and hashlib.sha256(raw).hexdigest() == pin)
            d['layout'] = layout_probe(raw)
            d['layout_ok'] = bool(d['layout'].get('ok'))
            d['compression'] = d['layout'].get('compression')

            oracle, oerr = parse_oracle(show(root, rev, opath) if opath else None)
            d['oracle_path'] = opath
            d['oracle_error'] = oerr
            d['oracle_files'] = len(oracle)
            d['oracle_ok'] = oerr is None and len(oracle) > 0

            nonreg, nerr = parse_nonregular(show(root, rev, npath) if npath else None)
            d['nonregular_path'] = npath
            d['nonregular_error'] = nerr
            d['nonregular_entries'] = len(nonreg)
            d['nonregular_kinds'] = sorted({kind for _, kind in nonreg})
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
                d['handler_ok'] = HANDLER in chunk_handlers(env)
                d['chunks_ok'] = not chunk_failed(env)
                files = published(env)
                d['published_files'] = len(files)
                d['oracle_hits'] = oracle_hits(oracle, files)
                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and d['oracle_hits'] == d['oracle_files'])
                ok, why = gap_check(gaps(env), nonreg, model)
                d['gaps_ok'] = ok
                d['gaps_note'] = why
                esc = nonregular_published(files, nonreg)
                d['nonregular_published'] = esc[:5]
                d['nonregular_unpublished_ok'] = not esc
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
               'detail': 'P40-C1 binds a fresh REA run of each carrier; '
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
                      rea_timeout=a.rea_timeout)
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
           outdir='/fast/scratch/hyaku/kaidoku-r40/selftest/after',
           subject_name='carrier.sqsh', chunk_dir='firmware.bin_extract',
           operation='extract_firmware', provider='unblob'):
    """A receipt-shaped REA envelope (`data` object) for fixture carriers."""
    if chunks is None:
        chunks = [{'input_path': '$input', 'provider_id': '3028394:1',
                   'range': {'offset': 0, 'length': 4096},
                   'handler': HANDLER, 'encrypted': False,
                   'root_file_range': {'offset': 0, 'length': 4096},
                   'extraction_failed': False}]
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
    diag_rows = [{'input_path': '$input',
                  'report': {'__typename__': t, 'severity': 'WARNING',
                             'link': '%s/%s/x' % (outdir, chunk_dir),
                             'target': '/etc/shadow'}} for t in diags]
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
            'depth_limited_paths': [],
            'derivations': [],
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


def rehost(env, tag, chunk_dir='carrier.bin_extract'):
    """Copy of a receipt as a *second* run of the same bytes would emit it:
    different absolute paths, different staged input name (hence a different
    chunk extract directory), different evidence id. Projection-invariant."""
    e = json.loads(json.dumps(env))
    root = '/fast/scratch/hyaku/kaidoku-r40/counter/rerun/%s' % tag
    outdir = root + '/out'
    nr = e['normalized_result']
    nr['output_directory'] = outdir
    for f in nr.get('files') or []:
        suffix = rel_suffix(f.get('relative_path') or '')
        f['relative_path'] = '%s/%s' % (chunk_dir, suffix)
        f['path'] = '%s/%s/%s' % (outdir, chunk_dir, suffix)
    for g in nr.get('extraction_gaps') or []:
        suffix = rel_suffix(g.get('relative_path') or '')
        g['relative_path'] = '%s/%s' % (chunk_dir, suffix) if suffix else None
        g['input_path'] = '$output/%s/%s' % (chunk_dir, suffix)
        g['continuation_id'] = 'continuation-' + tag
    for u in nr.get('unpublished_entries') or []:
        suffix = rel_suffix(u.get('relative_path') or '')
        u['relative_path'] = '%s/%s' % (chunk_dir, suffix)
    for d in nr.get('diagnostics') or []:
        d['report']['link'] = '%s/%s/x' % (outdir, chunk_dir)
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
        'V1': sb_carrier(GZIP_ID, b'V1-avm'),
        'V2': sb_carrier(4, b'V2-avm'),
        'L1': sb_carrier(GZIP_ID, b'L1-avm'),
        'L2': sb_carrier(2, b'L2-avm'),
    }
    pins = {k: sha(v) for k, v in carriers.items()}
    fsha = lambda i: sha(('f%s' % i).encode())

    # per-carrier fixture data (files, gaps, unpublished, diagnostics)
    spec_data = {
        'V1': dict(files=[('README.txt', fsha(1), 148), ('config/app.conf', fsha(2), 54)],
                   gaps=[('unpublished-entry', 'usr/share/demo/link-blob', []),
                         ('unpublished-entry', 'usr/share/demo/escape', [])],
                   unpub=[('usr/share/demo/link-blob', 'symlink', '../opt/blob.bin'),
                          ('usr/share/demo/escape', 'symlink', '../../../../etc/shadow')],
                   diags=['MaliciousSymlinkRemoved'],
                   nonreg='usr/share/demo/link-blob\tsymlink\nusr/share/demo/escape\tsymlink\n'),
        'V2': dict(files=[('var/info.txt', fsha(3), 40)], gaps=[], unpub=[], diags=[],
                   nonreg=''),
        'L1': dict(files=[('bin/run', fsha(4), 12), ('docs/deep/blob.bin', fsha(5), 33)],
                   gaps=[('unpublished-entry', 'usr/lib/libfoo.so', [])],
                   unpub=[('usr/lib/libfoo.so', 'symlink', '../lib/libfoo.so.1')],
                   diags=[],
                   nonreg='usr/lib/libfoo.so\tsymlink\n'),
        'L2': dict(files=[('etc/motd', fsha(6), 9)], gaps=[], unpub=[],
                   diags=['FileMagicMismatch'],
                   nonreg='dev/console\tdevice\n'),
    }
    # L2's device is required: give it a gap
    spec_data['L2']['gaps'] = [('unpublished-entry', 'dev/console', [])]
    spec_data['L2']['unpub'] = [('dev/console', 'device', None)]

    def receipt_envs(over=None):
        out = {}
        for k in ids:
            sd = spec_data[k]
            out[k] = mk_env(k.lower() + '.sqsh', pins[k],
                            files=sd['files'], gaps=sd['gaps'],
                            unpub=sd['unpub'], diags=sd['diags'],
                            outdir='/fast/scratch/hyaku/kaidoku-r40/selftest/%s-after' % k)
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

    rule = json.dumps({'claim': 'R40-C1',
                       'allowed': {'symlink': ['unpublished-entry'],
                                   'device': ['unpublished-entry']}}, indent=1)

    def spec_json(pin_map=None, drop=None, target=None, receipt_override=None,
                  projection=None):
        pm = pin_map or pins
        cs = []
        for k in ids:
            if drop and k in drop:
                continue
            c = {'id': k,
                 'path': f'{AFTERDIR}/{k}/carrier.sqsh',
                 'sha256': pm[k],
                 'oracle': f'{AFTERDIR}/{k}/oracle.tsv',
                 'nonregular': f'{AFTERDIR}/{k}/nonregular.tsv'}
            if receipt_override and k in receipt_override:
                c['receipt'] = receipt_override[k]
            cs.append(c)
        spec = {'claim': 'R40-C1', 'carriers': cs}
        if target is not None:
            spec['target'] = target
        if projection is not None:
            spec['projection'] = projection
        return json.dumps(spec, indent=1)

    def oracle_tsv(k):
        rows = ''.join(f'{rel}\t{h}\t{size}\n' for rel, h, size in spec_data[k]['files'])
        return rows.encode()

    def frozen_files(blob_map=None, pin_map=None, nonreg_map=None, rule_text=None,
                     **over):
        bm = blob_map or carriers
        pm = pin_map or pins
        nm = nonreg_map if nonreg_map is not None else {
            k: spec_data[k]['nonreg'] for k in ids}
        f = {XPIN: xpin,
             CARRIERS: spec_json(pin_map=pm),
             GAPRULE: (rule_text if rule_text is not None else rule).encode(),
             'plans/round-40-claims.md': b'# plan\n',
             'tools/round-40/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
             'PROVINCE.md': _province(),
             ENTRY: _entry(),
             'corpus/SOURCES.md': _registry(),
             'corpus/README.md': _readme()}
        for k in ids:
            f[f'{AFTERDIR}/{k}/carrier.sqsh'] = bm[k]
            f[f'{AFTERDIR}/{k}/oracle.tsv'] = oracle_tsv(k)
            f[f'{AFTERDIR}/{k}/nonregular.tsv'] = nm[k].encode()
        f.update(over)
        return f

    def build(blob_over=None, env_over=None, receipt_over=None, nonreg_over=None,
              rule_text=None, spec_text=None):
        """A pin-consistent (frozen files, receipts) pair for one variant."""
        bm = dict(carriers)
        bm.update(blob_over or {})
        pm = {k: sha(bm[k]) for k in ids}
        nm = {k: spec_data[k]['nonreg'] for k in ids}
        nm.update(nonreg_over or {})
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
                                  rule_text=rule_text, **(over_spec(spec_text)))
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
    add('receipt missing (V2)',
        [frozen, {k: v for k, v in good.items() if '/V2/' not in k}], 0, 1,
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

    oracle_only = fabricate('V1', diags=[], chunk_handler='squashfs_v4_le')
    add('oracle-only fabrication with re-minted evidence id',
        [frozen, relabel(green_envs, 'V1', oracle_only)], 0, 1,
        want_fail='projection_ok')
    one_file_off = fabricate('V2', files=[('var/info.txt', fsha(99), 40)])
    add('fabrication differing only in one published sha256',
        [frozen, relabel(green_envs, 'V2', one_file_off)], 0, 1,
        want_fail='projection_ok')
    extra_gap = fabricate('L1', gaps=[('unpublished-entry', 'usr/lib/libfoo.so', []),
                                      ('extractor-failure', 'bin/run', ['xz'])])
    add('fabrication differing only in an extra gap',
        [frozen, relabel(green_envs, 'L1', extra_gap)], 0, 1, want_fail='gaps_ok')
    diags_dropped = fabricate('L2', drop_diag=True)
    add('fabrication differing only in the diagnostics multiset',
        [frozen, relabel(green_envs, 'L2', diags_dropped)], 0, 1,
        want_fail='projection_ok')
    add('rerun yields no evidence object (REA ok=false)',
        [frozen, good], 0, 1, want_fail='projection_ok', runner=boom_runner)
    add('rerun environment error (no npx) is unevaluable, never met',
        [frozen, good], 0, 2, 'rerun_env_error', runner=env_boom_runner)
    add('subject digest names another carrier',
        [frozen, mutant('V1', lambda e: e['subject']['digest'].__setitem__(
            'sha256', '2' * 64))], 0, 1, want_fail='subject_pin_ok')

    # ---- carrier layout controls
    stripped = sb_carrier(4, b'V1-stripped', marker=False)
    s_frozen, s_receipts = build(blob_over={'V1': stripped})
    add('marker-stripped genuine-LE-lengths carrier', [s_frozen, s_receipts], 0, 1,
        want_fail='layout_ok')
    add('standard-BE carrier (BE block lengths)',
        [build(blob_over={'V1': sb_carrier(GZIP_ID, b'V1-be', meta_le=False)})[0],
         build(blob_over={'V1': sb_carrier(GZIP_ID, b'V1-be', meta_le=False)})[1]],
        0, 1, want_fail='layout_ok')
    # 8c00: LE length 140, BE length 3072 - plausible both ways, asymmetric
    ambiguous = sb_carrier(GZIP_ID, b'V1-amb', meta_header=b'\x8c\x00', pad=200)
    add('metadata length plausible both ways (no identity)',
        [build(blob_over={'V1': ambiguous})[0], build(blob_over={'V1': ambiguous})[1]],
        0, 1, want_fail='layout_ok')
    amb_id = sb_carrier(GZIP_ID, b'V1-ambid', meta_header=b'\x8c\x00', pad=200,
                        identity_le=True)
    add('ambiguous length settled by the single-block identity',
        [build(blob_over={'V1': amb_id})[0], build(blob_over={'V1': amb_id})[1]], 0, 0)
    lx = sb_carrier(4, b'V1-le-magic')
    lx = b'hsqs' + lx[4:]
    add('little-endian superblock magic', [build(blob_over={'V1': lx})[0],
                                          build(blob_over={'V1': lx})[1]], 0, 1,
        want_fail='layout_ok')
    big_used = sb_carrier(GZIP_ID, b'V1-used', marker_value=0xFFFFFFF0)
    add('bytes_used beyond the file', [build(blob_over={'V1': big_used})[0],
                                      build(blob_over={'V1': big_used})[1]], 0, 1,
        want_fail='layout_ok')

    # ---- missing / malformed frozen inputs (absent at the freeze itself)
    no_carrier = {**frozen, f'{AFTERDIR}/V2/carrier.sqsh': None}
    add('carrier listed but never committed', [no_carrier, good], 0, 1,
        want_fail='carrier_present')
    bad_oracle = {**frozen, f'{AFTERDIR}/V1/oracle.tsv': b'not-a-digest\n'}
    add('malformed oracle row', [bad_oracle, good], 0, 1, want_fail='oracle_ok')
    bad_nonreg = {**frozen, f'{AFTERDIR}/L1/nonregular.tsv': b'usr/lib/libfoo.so\n'}
    add('malformed nonregular row', [bad_nonreg, good], 0, 1,
        want_fail='nonregular_ok')

    # ---- receipt clause controls
    add('wrong operation (extract_filesystem)',
        [frozen, mutant('V1', lambda e: e.__setitem__('operation', 'extract_filesystem'))],
        0, 1, want_fail='operation_ok')
    add('provider is not unblob',
        [frozen, mutant('V2', lambda e: e['provider'].__setitem__('id', 'binwalk'))],
        0, 1, want_fail='operation_ok')
    add('failed chunk',
        [frozen, mutant('L1', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))], 0, 1,
        want_fail='chunks_ok')
    add('chunk handler is the LE handler',
        [frozen, mutant('L2', lambda e: [c.__setitem__('handler', 'squashfs_v4_le')
                                         for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
    add('disallowed gap kind on a symlink entry',
        [frozen, mutant('V1', lambda e: e['normalized_result']['extraction_gaps'][0]
                        .__setitem__('kind', 'extractor-failure'))], 0, 1,
        want_fail='gaps_ok')
    add('gap on a path that is not a non-regular entry',
        [frozen, mutant('V2', lambda e: e['normalized_result']['extraction_gaps'].append({
            'kind': 'unpublished-entry', 'relative_path': 'firmware.bin_extract/var/ghost',
            'dependencies': []}))], 0, 1, want_fail='gaps_ok')
    add('required gap missing (symlink materialised)',
        [frozen, mutant('L1', lambda e: (
            e['normalized_result']['extraction_gaps'].pop(),
            e['normalized_result']['unpublished_entries'].pop(),
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/usr/lib/libfoo.so',
                'path': '/x/usr/lib/libfoo.so', 'size': 3, 'sha256': 'f' * 64})))],
        0, 1, want_fail='gaps_ok')
    add('escaping symlink published as a regular file',
        [frozen, mutant('V1', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/usr/share/demo/escape',
            'path': '/x/escape', 'size': 3, 'sha256': 'e' * 64}))], 0, 1,
        want_fail='nonregular_unpublished_ok')
    add('oracle file missing from the published set',
        [frozen, mutant('V2', lambda e: e['normalized_result']['files'].pop())], 0, 1,
        want_fail='oracle_hits_ok')
    add('foreign scratch provenance (/kaidoku-r39/)',
        [frozen, mutant('V1', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r39/l1/K1-after'))],
        0, 1, want_fail='run_provenance_ok')
    add('provenance path climbs out with ..',
        [frozen, mutant('V2', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r40/../kaidoku-r39/x'))],
        0, 1, want_fail='run_provenance_ok')
    add('evidence id stale after an edit',
        [frozen, mutant('L2', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/extra.txt', 'path': '/x/extra.txt',
            'size': 1, 'sha256': 'd' * 64}), remint=False)], 0, 1,
        want_fail='evidence_id_ok')

    # ---- freeze integrity
    add('carrier bytes changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/V1/carrier.sqsh': b'changed carrier\n'}],
        0, 2, 'frozen_path_changed')
    add('carrier bytes changed then restored',
        [frozen, {**good, f'{AFTERDIR}/V1/carrier.sqsh': b'changed carrier\n'},
         {**good, f'{AFTERDIR}/V1/carrier.sqsh': carriers['V1']}], 0, 2,
        'frozen_path_changed')
    add('oracle changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/V2/oracle.tsv': oracle_tsv('V2') + b'extra.txt\t'
          + b'3' * 64 + b'\t1\n'}], 0, 2, 'frozen_path_changed')
    add('nonregular table changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/L1/nonregular.tsv': b'usr/lib/libfoo.so\tsymlink\n'
         b'usr/lib/extra\tsymlink\n'}], 0, 2, 'frozen_path_changed')
    add('carriers.json changed after freeze',
        [frozen, {**good, CARRIERS: spec_json(drop=('L2',))}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json changed after freeze',
        [frozen, {**good, GAPRULE: json.dumps({'claim': 'R40-C1', 'allowed': {
            'symlink': ['unpublished-entry']}}).encode()}], 0, 2,
        'frozen_path_changed')
    add('gap-rule.json touched then restored',
        [frozen, {**good, GAPRULE: b'{}\n'}, {**good, GAPRULE: rule.encode()}], 0, 2,
        'frozen_path_changed')
    add('counter edited after freeze',
        [frozen, {**good, 'tools/round-40/c1-counter.py': b'#!/usr/bin/env python3\n'
         b'print(0)\n'}], 0, 2, 'frozen_path_changed')
    add('claims edited after freeze',
        [frozen, {**good, 'plans/round-40-claims.md': b'# new plan\n'}], 0, 2,
        'frozen_path_changed')

    # ---- frozen-table controls
    bad_pins = dict(pins)
    bad_pins['V1'] = '4' * 64
    add('frozen pin wrong (carrier untouched)',
        [{**frozen, CARRIERS: spec_json(pin_map=bad_pins)}, good], 0, 1,
        want_fail='carrier_pin_ok')
    add('carriers.json drops a carrier at the freeze (target 4)',
        [{**frozen, CARRIERS: spec_json(drop=('V2',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    one_leg = {k: sb_carrier(GZIP_ID, ('%s-gzip' % k).encode()) for k in ids}
    f1, r1 = build(blob_over=one_leg)
    add('no xz carrier (compression coverage)', [f1, r1], 0, 1,
        want_fail='b:compression_coverage')
    thin = json.dumps({'claim': 'R40-C1', 'allowed': {'symlink': ['unpublished-entry']}})
    f2, r2 = build(rule_text=thin)
    add('gap rule omits the device kind', [f2, r2], 0, 1, want_fail='b:gap_rule_ok')
    add('gap rule is JSON but not an object at the freeze',
        list(build(rule_text='[]')), 0, 1, want_fail='b:frozen_tables_valid')
    add('gap rule names another claim',
        list(build(rule_text=json.dumps({'claim': 'R39-C1', 'allowed': {
            'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}}))),
        0, 1, want_fail='b:gap_rule_ok')

    # ---- structural gaps (unblob bookkeeping: null relative_path)
    rule_struct = json.dumps({'claim': 'R40-C1',
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
                                   env_over={'V1': add_struct})
    add('structural gap within its frozen allowance',
        [st_frozen, st_receipts], 0, 0,
        runner=mk_same_runner({**green_envs, 'V1': json.loads(st_receipts[
            receipt_path('V1')])}))
    st2_frozen, st2_receipts = build(
        rule_text=rule_struct, env_over={'V1': lambda e: add_struct(e, extra=1)})
    add('structural gaps over the allowance', [st2_frozen, st2_receipts], 0, 1,
        want_fail='gaps_ok')
    st3_frozen, st3_receipts = build(
        rule_text=rule_struct,
        env_over={'V1': lambda e: add_struct(e, kind='depth-limited')})
    add('path-less gap kind with no structural allowance', [st3_frozen, st3_receipts],
        0, 1, want_fail='gaps_ok')
    st4_frozen, st4_receipts = build(
        rule_text=rule_struct,
        env_over={'V1': lambda e: add_struct(e, path='usr/share/demo/extra-link')})
    add('structural gap kind that carries a path', [st4_frozen, st4_receipts], 0, 1,
        want_fail='gaps_ok')

    # ---- projection profile: the measured calibration limit of the core fields
    def bump_bytes(e):
        e['normalized_result']['published_bytes'] += 1
    core_frozen, core_receipts = build(
        env_over={'V1': bump_bytes}, spec_text=spec_json(projection='core'))
    add('explicit core profile accepts a projection-identical (oracle-closed) fabrication',
        [core_frozen, core_receipts], 0, 0)
    ext_frozen, ext_receipts = build(env_over={'V1': bump_bytes})
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
        [frozen, mutant('V1', lambda e: e['parameters'].__setitem__('max_depth', 1))],
        0, 1, want_fail='projection_ok', runner=depth_runner(3))

    # ---- documentation bindings
    add('province has no Core section at all',
        [{**frozen, 'PROVINCE.md': '# P\n\n## Next\n- x\n'}, good], 0, 1,
        want_fail='b:province_core_section')
    add('province row outside the round-40 section',
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
                      'green_ok': green, 'red_ok': red, 'failures': fails}))
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
    pin = hashlib.sha256(image).hexdigest()

    sroot = scratch_root()
    work = tempfile.mkdtemp(prefix='c1-selftest-rea.', dir=sroot)
    runner = make_real_runner(work, unblob, timeout)
    out = {'image': DEV_AVM_IMAGE, 'image_sha256': pin, 'bytes': len(image)}

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
    status, env = runner(image, 'V1-committed')
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
        entry = 'corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md'
        stem = '2026-10-26-r40-avm-be-squashfs-core'
        frozen = {
            XPIN: xpin,
            '.ufo/waves/round-40/c1/carriers.json': json.dumps({
                'claim': 'R40-C1', 'target': 1,
                'carriers': [{'id': 'V1',
                              'path': 'corpus/evidence/round-40/c1/V1/carrier.sqsh',
                              'sha256': pin,
                              'oracle': 'corpus/evidence/round-40/c1/V1/oracle.tsv',
                              'nonregular': 'corpus/evidence/round-40/c1/V1/nonregular.tsv'}]},
                indent=1),
            '.ufo/waves/round-40/c1/gap-rule.json': json.dumps(
                {'claim': 'R40-C1', 'allowed': {'symlink': ['unpublished-entry']}},
                indent=1),
            'plans/round-40-claims.md': '# plan\n',
            'tools/round-40/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
            'PROVINCE.md': _province(),
            entry: _entry('S240'),
            'corpus/SOURCES.md': _registry('S240', used=entry),
            'corpus/README.md': _readme(stem),
            'corpus/evidence/round-40/c1/V1/carrier.sqsh': image,
            'corpus/evidence/round-40/c1/V1/oracle.tsv': oracle_tsv.encode(),
            'corpus/evidence/round-40/c1/V1/nonregular.tsv': b'',
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
        commit({'corpus/evidence/round-40/c1/V1/after.json': json.dumps(env)})
        freeze, rev = revs[0], revs[-1]

        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('V1',), unblob=unblob, rea_timeout=timeout)
            got = 0 if res['met_target'] else 1
            out['green'] = {'exit': got, 'met_target': res['met_target'],
                            'carriers_matched': res['carriers_matched'],
                            'failing': sorted({x for x in CLAUSES
                                               if res['carriers']['V1'].get(x) is not True}),
                            'bindings_false': sorted(x for x in BINDINGS
                                                     if res['bindings'][x] is not True),
                            'projection_diff': res['carriers']['V1'].get('projection_diff'),
                            'layout': res['carriers']['V1'].get('layout')}
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
                     outdir='/fast/scratch/hyaku/kaidoku-r40/selftest-rea/fab')
        fab['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': fab})['m']
        commit({'corpus/evidence/round-40/c1/V1/after.json': json.dumps(fab)})
        rev = revs[-1]
        try:
            res = measure(d, rev, freeze, pkg65, rerun=None, target=1,
                          expected_ids=('V1',), unblob=unblob, rea_timeout=timeout)
            v = res['carriers']['V1']
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
