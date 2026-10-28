#!/usr/bin/env python3
"""R49-C1 counter (coverage: SquashFS v1 + v2 through REA `extract-firmware` -> Core).

Port of `git show c29360e3:tools/round-42/c1-counter.py` (round-49 seat
R49C1Counter). The claims text is `plans/round-49-claims.md` R49-C1; the
predicate is embedded here clause by clause:

  At the measured revision, for each of the four preregistered carriers
  (v1.0 le/be, v2.0 le/be), the committed round-49 REA 6.5.0
  `extract-firmware` after-receipt (unblob 26.6.4, sasquatch 4.5.1 on the child
  PATH) -- first added in a commit that descends from the freeze -- names the
  carrier's frozen `squashfs_v1`/`squashfs_v2` handler with no failed chunk,
  publishes every regular file of the frozen independent oracle (unsquashfs
  4.7.5 member census) at its exact relative path under the chunk extract root
  (segment-bounded, round-41 closure D5) with the same sha256 and size, and no
  extra regular file; accounts for every non-regular oracle row by the frozen
  gap rule (one `unpublished-entry` gap or one `MaliciousSymlinkRemoved`
  diagnostic per symlink; at most one structural `depth-limited`; no
  `unknown-chunk-handler`); has a subject digest equal to the carrier pin and
  recomputes its evidence id; the carrier bytes hash to the pin, are a regular
  file at the freeze and at the measured revision, and their v1/v2 superblock
  reads the frozen magic/major/minor/endianness and the observed compression
  class; the committed unblob `__output__` expected tree (S138) reproduces the
  frozen census rows and its frozen digest; **and** a counter-time REA rerun of
  the same bytes has the same semantic projection as the committed receipt (a
  receipt fabricated from the oracle, however its evidence id is minted, cannot
  equal a real run); `PROVINCE.md` holds the `## Round-49 additions to Core` row
  naming `squashfs_v1` and `squashfs_v2` and citing the round-49 knowledge
  entry, which cites SOURCES rows S138 and S139 (both opened this round and
  listing the entry in used-by); a round-49 frontier note supersedes the
  `SquashFS v1/v2` Frontier text; `corpus/README.md` maps the entry stem; no
  frozen C1 path changed after the freeze.

Target: exactly the four preregistered carrier ids (v1le, v1be, v2le, v2be;
`target` frozen in carriers.json) and every binding true.

Functional deltas from the round-42 counter (nothing else moved)
  (1) superblock probe     the v3 probe (family magics that select a variant,
                           119-byte packed struct, `bytes_used` u64@63, table
                           starts u64@87/95) is replaced by the v1/v2 probe.
                           SquashFS v1/v2 share one 32-byte packed superblock
                           (unblob 26.6.4 `SquashFSv1Handler.C_DEFINITIONS`,
                           S119): magic 0:4, inodes u32@4, bytes_used u32@8,
                           uid_start u32@12, guid_start u32@16,
                           inode_table_start u32@20, directory_table_start
                           u32@24, s_major u16@28, s_minor u16@30.  There is
                           NO compression field in v1/v2: zlib is the only
                           codec the format carries, so the class is OBSERVED
                           from the inode table's first metadata block body
                           (2-byte length header at `inode_table_start`, chain
                           witness `its + 2 + len == dts`) and compared with the
                           frozen `compression` value.  `file(1)` is never a
                           compression oracle: it applies the v4 field offsets
                           to every squashfs image, so its compressed/
                           uncompressed word is read from byte 20 (=
                           inode_table_start) and flips with byte order on
                           these very fixtures (R49C1Oracle / R44ConnRouted
                           measured it; unsquashfs reports data compressed on
                           all carriers).  Endianness comes from the magic
                           order: `hsqs` = little, `sqsh` = big.  The v2
                           nonstandard magics (`zlqs`/`sqlz`) are refused.
  (2) oracle binding       the v3 oracle path (a `sqfs3-oracle.py` table per
                           carrier plus a nonregular.tsv) is replaced by the
                           frozen unsquashfs 4.7.5 member census carried per
                           carrier in carriers.json, cross-checked against the
                           committed unblob `__output__` expected tree (S138):
                           the tree blobs at the measured revision must
                           reproduce the census rows exactly and hash to the
                           frozen tree digest, so neither oracle can be edited
                           on its own.
  (3) handler binding      each carrier freezes exactly `squashfs_v1` or
                           `squashfs_v2`; the family follows s_major (1/2) and
                           the magic order, not a magic->variant table (v1 and
                           v2 share the magic bytes).  Every squashfs-family
                           chunk handler the receipt names must equal the
                           carrier's handler -- a v3/v4 (or nonstandard)
                           handler on a v1/v2 carrier fails `handler_ok` and
                           leaves no extract root.
  (4) carrier custody      the round-49 carriers are committed lane blobs (the
                           four MIT unblob 26.6.4 fixtures, round-42 C2
                           held-out INPUTS, never a C1 carrier), so the bytes
                           are read from the git object at the measured
                           revision instead of a ``--carrier-cache``, and the
                           blob mode must be a regular file (100644) at the
                           freeze and at the revision.  The published-carrier
                           chain of round 42 (external URL, fetch receipt,
                           toolchain pin, extract-env.json) does not exist in
                           round 44 and is dropped with it.

Kept verbatim from `git show c29360e3:tools/round-42/c1-counter.py`
  - the freeze-integrity walk (`frozen_drift`, now merge-aware per the claims'
    freeze rule: `-m --diff-merges=first-parent`, M/D/R/T/U are changes, A is
    a change when the path existed at the freeze, and each frozen regular-file
    blob at the freeze must equal the blob at the revision);
  - the segment-bounded extract-root rule (`under_root`, `extract_rel`,
    `same_rel`, `path_shape_problem`, `subject_root`, `squashfs_roots`,
    `strip_output`, `receipt_paths`, `diagnostic_rel`/`trusted_run_root`);
  - the evidence-id recompute (`rea_package_problems` + `evidence_ids` through
    the frozen `tools/round-27/xpin-attribute.mjs` and the package's own
    `semanticProjection`);
  - the `counter_sha256` self-hash (`counter_identity`, `stamp_receipt`,
    `receipt_identity_ok`, `write_receipt`, `--verify-receipt`);
  - the counter-time REA rerun binding (`make_real_runner`, `projection`,
    `projection_diff`, replay of the receipt's recorded extraction parameters).

The extract root (R40-CL1 / R41-D5 rule, unchanged)
  Every path comparison against the oracle and non-regular tables is equality
  after mapping the receipt path into its chunk's extract root, never a suffix
  test, and the root is never reconstructed from the path text: `$output/` is
  stripped once, the root is the child path of the `derivations[]` edge whose
  handler EQUALS the carrier's frozen handler, exactly one such root is
  required (several roots are ambiguous and the freeze may name the intended
  one with the optional `oracle_root` key), and containment is segment-bounded:
  `P == root or P.startswith(root + '/')`, so a root `x_extract` does not own
  `x_extract2/...`.

Per-carrier clauses (all must hold; `matched` = conjunction):
  carrier_present          committed blob at REV, mode 100644 (regular file)
  carrier_pin_ok           sha256(bytes at REV) == the frozen pin
  carrier_size_ok          len(bytes at REV) == the frozen size
  carrier_fresh_ok         the pin is not one a previous C1 freeze already
                           scored (frozen prior-pins tables at the freeze)
  layout_ok                the v1/v2 superblock reads the frozen magic
                           (implied by endianness), s_major, s_minor, the
                           observed compression class, a sane `bytes_used` and
                           table-start pair, and the metadata-chain witness
  carve_ok                 the carrier is exactly the extent unblob calls the
                           chunk (`chunk_end`: `bytes_used` or its 4096/1024
                           zero-padded rounding)
  oracle_ok                the frozen census rows parse (path, sha256, size),
                           are unique, and number `expected_regular`
  tree_ok                  the committed `__output__` tree at REV reproduces
                           the census rows exactly and its digest equals the
                           frozen digest under the frozen digest rule
  receipt_present          corpus/evidence/round-49/c1/<id>/after.json parses
  receipt_fresh            first add at REV is a strict descendant of --freeze
  evidence_envelope_ok     the after-receipt is an REA evidence envelope, not a
                           score receipt (no `counter_sha256`/`exit_code` key)
  subject_pin_ok           subject.digest.sha256 == the frozen pin
  operation_ok             operation == extract_firmware, provider.id == unblob
  handler_ok               every squashfs-family chunk handler equals the
                           carrier's frozen handler exactly (no prefix test,
                           no default; a v3/v4 handler fails)
  chunks_ok                no chunk carries extraction_failed: true
  oracle_hits_ok           every census row is published at its exact path
                           under the extract root (rel ==, sha256 ==, size ==)
                           and no other regular file is published there
  gaps_ok                  disposition check: every path-carrying gap resolves
                           to exactly one non-regular row of an allowed kind;
                           structural gaps within their frozen allowance;
                           removals exclusive; every required row disposed
  nonregular_unpublished_ok  no published regular file path equals a
                           non-regular row path
  path_shape_ok            every normalised receipt path is a legal spelling
                           (no empty/`.`/`..` component, no trailing slash)
  run_provenance_ok        parameters.output_directory names this round's
                           scratch segment (/kaidoku-r49/)
  evidence_id_ok           stored evidence id == the id recomputed under the
                           frozen rea-agents 6.5.0 rule
  projection_ok            the counter's own REA run of the carrier bytes has
                           the same semantic projection as the committed
                           receipt (plus-extractor profile by default)

Non-vacuity bindings (properties of the frozen set):
  carriers_spec_ok         `target` == 4; exactly the four preregistered ids
                           (case-insensitive); distinct pins; every carrier
                           carries handler/endianness/s_major/s_minor/
                           compression/sha256/size/path/expected_regular and
                           its oracle rows; handler family agrees with s_major;
                           compression is a class
  gap_rule_ok              the embedded frozen rule parses and every non-regular
                           kind in any frozen oracle is a key of `allowed`
  endianness_coverage      >= 1 little-endian and >= 1 big-endian carrier
  family_coverage          >= 1 squashfs_v1 and >= 1 squashfs_v2 carrier
  frozen_tables_valid      carriers.json parses at the freeze commit itself
  oracle_tool_ok           the frozen oracle tool path resolves and, when the
                           table pins them, its sha256/version match

Documentation bindings:
  province_core_section    PROVINCE.md has the `## Round-49 additions to Core`
                           heading
  province_core_row        a row in that section names `squashfs_v1` and
                           `squashfs_v2`, names SquashFS v1/v2, and cites the
                           entry path
  frontier_note            one line carries `Round-49 frontier note`, the entry
                           stem and a SquashFS v1/v2 token
  entry_present            the knowledge entry exists at REV
  sourced                  the entry's `source:` lines cite S138 and S139; both
                           SOURCES rows are opened 2026-10-28 and list the
                           entry (path or stem) in used-by
  coverage_map_row         corpus/README.md `## Coverage map` maps the entry
                           stem

Freeze-drift binding: if any commit in FREEZE..REV touches a frozen C1 path (or
changes the blob of one that existed at FREEZE), the counter exits 2 with
reason `frozen_path_changed` and never reports met. A later restore does not
un-block: the log of the range is inspected, not the endpoints.

Receipt identity: every receipt this counter writes (`--json-out`) carries
`counter` (absolute path) and `counter_sha256` (sha256 of that file's bytes).
`--verify-receipt PATH` re-reads a written receipt and exits 0 (match), 1
(missing/mismatched key) or 2 (unreadable). The committed REA after-receipts
must NOT carry the key (`evidence_envelope_ok`).

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT
                [--json-out PATH] [--unblob PATH] [--rea-timeout SECONDS]
                [--work DIR] [--no-rerun]
  c1-counter.py --selftest [--pkg65 REA650_PKG_ROOT] [--work DIR]
  c1-counter.py --dev-arm --root LANE [--rev REV] [--work DIR]
                [--arm-dir DIR] [--arm-ids a,b] [--run-rea] [--json-out PATH]
  c1-counter.py --verify-receipt PATH
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure,
frozen path changed, rerun environment error, --no-rerun). Reads lane bytes only
through git objects (`git show REV:path`); writes only a private scratch dir
under $HYAKU_SCRATCH/kaidoku-r49/counter (or --work) and --json-out. Never calls
gettempdir(): `TMPDIR` is honoured for child processes by pointing it into the
private work dir.

`--selftest` is offline and deterministic: it drives measure() in-process over a
git fixture lane with a simulated REA runner (the simulator exists only inside
selftest(); main() never passes anything but the real runner). Synthetic v1/v2
superblocks are exactly what the layout probe tests; the four required cases are
(i) the correct map of a dev-arm-shaped receipt, (ii) a v3 receipt fed to a v1
carrier (red), (iii) a fabricated oracle-only envelope (red on the rerun
projection), (iv) the do-nothing lane (red).

`--dev-arm` is the positive development control (R44RevKill K3): it scores
REAL REA 6.5.0 envelopes for the frozen carriers into scratch -- either the
envelopes it runs itself (`--run-rea`) or a directory of already captured ones
(`--arm-dir <id>/after.json`) -- and never writes corpus/evidence/round-49/c1.
Exit 0 only when every requested carrier maps clean.
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
import zlib

CARRIERS = 'tools/round-49/carriers.json'
AFTERDIR = 'corpus/evidence/round-49/c1'
ENTRY = 'corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md'
STEM = '2026-10-28-r49-squashfs-v1v2-core'
CORE_HEADING = '## Round-49 additions to Core'
FRONTIER_MARK = 'Round-49 frontier note'
OPENED = '2026-10-28'
TARGET = 4
# The four preregistered carriers of plans/round-49-claims.md §R49-C1, in the
# id spelling of the frozen carriers.json. The comparison is case-insensitive so
# a table spelling V1LE cannot smuggle a different carrier set in; v2.1 is NOT
# part of this claim and its extra ids are a frozen-table defect, not coverage.
EXPECTED_IDS = ('v1le', 'v1be', 'v2le', 'v2be')
PROV_SEGMENT = '/kaidoku-r49/'
REA_PIN = 'rea-agents@6.5.0'
REA_VERSION = '6.5.0'
XPIN = 'tools/round-27/xpin-attribute.mjs'
REA_PKG_CANDIDATES = ('tools/round-49/rea-pkg.json', 'tools/round-42/rea-pkg.json')
PRIOR_PIN_CANDIDATES = ('tools/round-49/prior-pins.json', 'tools/round-42/prior-pins.json')
REQUIRED_SIDS = ('S138', 'S139')
# H1 (carried from round 42): the REA child and the counter's own node/npx
# lookups use one fixed PATH, so a seat's shim directory cannot be what
# `sasquatch` resolves to during a score.
FIXED_PATH = ':'.join(['/usr/local/bin', '/usr/bin', '/bin',
                       os.path.expanduser('~/.local/bin'),
                       os.path.expanduser('~/.local/share/fnm/node-versions/'
                                          'v24.21.0/installation/bin')])
FROZEN_PATHS = (
    'plans/round-49-claims.md',
    'tools/round-49/c1-counter.py',
    'tools/round-49/c1-run.sh',
    'tools/round-49/carriers.json',
    'tools/round-42/fixtures.json',
    'tools/round-42/c1-counter.py',
    'tools/round-42/prior-pins.json',
    'tools/round-42/rea-pkg.json',
    'tools/round-39/gen-squashfs.py',
    XPIN,
)
# `tools/round-49/*` and the committed S138 oracle trees are frozen path
# families: a new round-49 tool or an edited expected tree is drift.
FROZEN_PREFIXES = ('tools/round-49/', 'corpus/evidence/round-44/oracle/')
# SquashFS v1/v2 packed superblock (unblob 26.6.4 SquashFSv1Handler
# C_DEFINITIONS, S119). v1 and v2 share these bytes; s_major discriminates.
SB_SIZE = 32
SB_FIELDS = (
    ('magic', 0, 4),
    ('inodes', 4, 4),
    ('bytes_used', 8, 4),
    ('uid_start', 12, 4),
    ('guid_start', 16, 4),
    ('inode_table_start', 20, 4),
    ('directory_table_start', 24, 4),
    ('s_major', 28, 2),
    ('s_minor', 30, 2),
)
ENDIAN_BY_MAGIC = {b'hsqs': 'le', b'sqsh': 'be'}
MAGIC_BY_ENDIAN = {'le': b'hsqs', 'be': b'sqsh'}
HANDLER_BY_MAJOR = {1: 'squashfs_v1', 2: 'squashfs_v2'}
MAJOR_BY_HANDLER = {'squashfs_v1': 1, 'squashfs_v2': 2}
COMPRESSIONS = ('gzip', 'lzma')


def normalize_compression(value):
    """The compression class a frozen label names, or None.

    Frozen tables spell the v1/v2 codec as a bare class ('gzip') or as the
    vendor spelling ('zlib(gzip)'); both name the same class. Anything that is
    not a class of the format ('uncompressed', 'zstd', 'xz', ...) names no v1/v2
    codec and is refused rather than mapped to one."""
    if not isinstance(value, str):
        return None
    v = value.strip().lower()
    if '(' in v and v.endswith(')'):
        v = v[v.index('(') + 1:-1].strip()
    if v == 'zlib':
        v = 'gzip'
    return v if v in COMPRESSIONS else None
METADATA_MAX = 4096                    # v1/v2 metadata block length is 12-bit
UNCOMPRESSED_FLAG = 0x8000
SQUASHFS_HANDLER_RE = re.compile(r'^squashfs_v[1-4](_[a-z]+)?$')
HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])squashfs_v[12](?![A-Za-z0-9_-])')
SQFS12_TEXT_RE = re.compile(r'squashfs[ _-]?v?1(\.0)?|squashfs[ _-]?v?2(\.0)?'
                            r'|squashfs\s+[12]', re.IGNORECASE)
SID_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
SHA_RE = re.compile(r'^[0-9a-f]{64}$')
TREE_DIGEST_RULE = ("sha256 over the concatenation of '<path>\\t<sha256>\\n' "
                    "lines of `members`, sorted bytewise by path")
TREE_DIGEST_RULE_TOKENS = ('sha256', '<path>', '<sha256>', 'bytewise by path')
BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
            'entry_present', 'sourced', 'coverage_map_row', 'carriers_spec_ok',
            'gap_rule_ok', 'endianness_coverage', 'family_coverage',
            'frozen_tables_valid', 'oracle_tool_ok')
CLAUSES = ('carrier_present', 'carrier_pin_ok', 'carrier_size_ok',
           'carrier_fresh_ok', 'layout_ok', 'carve_ok', 'oracle_ok',
           'tree_ok', 'receipt_present', 'receipt_fresh', 'evidence_envelope_ok',
           'subject_pin_ok', 'operation_ok', 'handler_ok', 'chunks_ok',
           'oracle_hits_ok', 'gaps_ok', 'nonregular_unpublished_ok',
           'path_shape_ok', 'run_provenance_ok', 'evidence_id_ok',
           'projection_ok')
# The frozen gap rule of R49-C1 (claims text): one `unpublished-entry` gap or
# one `MaliciousSymlinkRemoved` diagnostic per symlink; at most one structural
# `depth-limited`; no `unknown-chunk-handler`. Frozen with the counter because
# all four carriers have zero non-regular members (measured: the unsquashfs
# census and the S138 trees list regular files only).
GAP_RULE = {
    'claim': 'R49-C1',
    'allowed': {'symlink': ['unpublished-entry'],
                'char-device': [], 'block-device': [],
                'fifo': ['unpublished-entry'], 'socket': ['unpublished-entry'],
                'dir': []},
    'required': {'symlink': True, 'char-device': False, 'block-device': False,
                 'fifo': False, 'socket': False, 'dir': False},
    'removed': {'diagnostic': 'MaliciousSymlinkRemoved', 'kinds': ['symlink'],
                'disposition': 'exclusive'},
    # Wave-1 amendment (R49C1Controls measured REA at its default depth 3 on all
    # four carriers: zero extraction gaps), so the claim freezes `gaps == []`:
    # no structural gap kind is allowed at all. The draft's "at most one
    # depth-limited" allowance is therefore zero, which is stricter, not looser.
    'structural': {'depth-limited': 0, 'unknown-chunk-handler': 0},
}


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


def blob_mode(root, rev, path):
    """`git ls-tree` mode of `path` at `rev` ('100644', '120000', ...), or None."""
    p = git(root, 'ls-tree', rev, '--', path, check=False)
    if p.returncode != 0:
        return None
    for line in p.stdout.decode(errors='replace').splitlines():
        f = line.split('\t', 1)
        if len(f) == 2 and f[1] == path:
            return f[0].split()[0]
    return None


def tree_entries(root, rev, path):
    """[(mode, blob, size, path)] for the recursive listing of `path` at `rev`."""
    p = git(root, 'ls-tree', '-r', '-l', rev, '--', path, check=False)
    out = []
    if p.returncode != 0:
        return out
    for line in p.stdout.decode(errors='replace').splitlines():
        head, _, name = line.partition('\t')
        f = head.split()
        if len(f) < 4 or not name:
            continue
        out.append((f[0], f[2], int(f[3]), name))
    return out


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


WORK_OVERRIDE = None


def scratch_root():
    """Private scratch directory; --work > $HYAKU_SCRATCH > /fast/scratch/hyaku.

    Deliberately never `tempfile.gettempdir()`: with TMPDIR and HYAKU_SCRATCH
    unset that resolves to /tmp (R44-SCR-TMP)."""
    if WORK_OVERRIDE:
        os.makedirs(WORK_OVERRIDE, exist_ok=True)
        return WORK_OVERRIDE
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'),
                     'kaidoku-r49', 'counter')
    os.makedirs(d, exist_ok=True)
    return d


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
    """Recompute the stored evidence id under the rea-agents 6.5.0 rule."""
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

def gap_rule_model(doc):
    """(model, problems) for the frozen gap rule (embedded constant or table)."""
    probs = []
    model = {'allowed': {}, 'required': {}, 'structural': {}, 'removed': {}}
    if not isinstance(doc, dict):
        return model, ['gap rule is not a JSON object']
    claim = doc.get('claim')
    if claim is not None and claim != 'R49-C1':
        probs.append('claim %r != R49-C1' % (claim,))
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
            silent = removed.get('silent', {}) or {}
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
            model['removed'] = {
                'diagnostic': diag.strip() if isinstance(diag, str) else None,
                'kinds': [k.strip().lower() for k in kinds],
                'disposition': disp,
                'silent': {str(k).strip().lower(): list(v)
                           for k, v in silent.items() if isinstance(v, list)},
            }
    return model, probs


def parse_rel_path(value):
    """A table row path as a filesystem-relative path, or (None, problem)."""
    if not isinstance(value, str) or not value:
        return None, 'empty path'
    p = value
    while p.startswith('./'):
        p = p[2:]
    if p.startswith('/'):
        return None, 'absolute path %r' % (value,)
    parts = p.split('/')
    if any(x == '' for x in parts):
        return None, 'empty component in %r' % (value,)
    if any(x in ('.', '..') for x in parts):
        return None, '. or .. component in %r' % (value,)
    return p, None


def oracle_rows(carrier):
    """(regular rows, nonregular rows, problems) from the frozen carrier entry.

    Accepted spellings (documented in the docstring): the rows live under
    `oracle.members` / `members` (regular files: path, sha256, size) and
    `oracle.nonregular` / `nonregular` (path, kind[, detail]).  Paths are
    relative to the filesystem root: the `unsquashfs -lls` census prefix
    `squashfs-root/` is stripped exactly once by the freezing seat, and this
    parser refuses whatever is left absolute or abnormal."""
    orc = carrier.get('oracle') if isinstance(carrier.get('oracle'), dict) else {}
    members = orc.get('members')
    if members is None:
        members = carrier.get('members')
    nonreg = orc.get('nonregular')
    if nonreg is None:
        nonreg = carrier.get('nonregular')
    probs = []
    rows = []
    if not isinstance(members, list):
        probs.append('carrier %r has no oracle member rows' % (carrier.get('id'),))
        members = []
    seen = set()
    for m in members:
        if not isinstance(m, dict):
            probs.append('non-object oracle member row')
            continue
        if m.get('type') not in (None, 'regular', 'file'):
            probs.append('oracle member %r type %r is not regular'
                         % (m.get('path'), m.get('type')))
            continue
        rel, why = parse_rel_path(m.get('path') if m.get('path') is not None
                                  else m.get('rel'))
        if why:
            probs.append('oracle member path: %s' % why)
            continue
        sha = m.get('sha256')
        if not (isinstance(sha, str) and SHA_RE.match(sha.lower())):
            probs.append('oracle member %r sha256 is not 64 hex' % (rel,))
            continue
        size = m.get('size')
        if not (isinstance(size, int) and not isinstance(size, bool) and size >= 0):
            probs.append('oracle member %r size is not a non-negative int' % (rel,))
            continue
        if rel in seen:
            probs.append('duplicate oracle member path %r' % (rel,))
            continue
        seen.add(rel)
        rows.append((rel, sha.lower(), size))
    if not rows:
        probs.append('carrier %r oracle has no regular rows' % (carrier.get('id'),))
    nrows = []
    if nonreg is None:
        nonreg = []
    if not isinstance(nonreg, list):
        probs.append('carrier %r nonregular is not a list' % (carrier.get('id'),))
        nonreg = []
    nseen = set()
    for n in nonreg:
        if not isinstance(n, dict):
            probs.append('non-object nonregular row')
            continue
        rel, why = parse_rel_path(n.get('path') if n.get('path') is not None
                                  else n.get('rel'))
        if why:
            probs.append('nonregular path: %s' % why)
            continue
        kind = n.get('kind')
        if not (isinstance(kind, str) and kind.strip()):
            probs.append('nonregular %r kind is empty' % (rel,))
            continue
        kind = kind.strip().lower()
        if (rel, kind) in nseen:
            probs.append('duplicate nonregular row %r' % ((rel, kind),))
            continue
        nseen.add((rel, kind))
        detail = n.get('detail')
        if detail is not None and not isinstance(detail, str):
            detail = str(detail)
        nrows.append((rel, kind, detail))
    overlap = {r for r, _s, _z in rows} & {r for r, _k, _d in nrows}
    if overlap:
        probs.append('paths in both oracle tables: %r' % sorted(overlap)[:4])
    return rows, nrows, probs


def output_tree_binding(carrier):
    """(root, digest, rule, problems) for the committed S138 expected tree."""
    orc = carrier.get('oracle') if isinstance(carrier.get('oracle'), dict) else {}
    ot = orc.get('output_tree')
    if ot is None:
        ot = carrier.get('output_tree')
    probs = []
    root = digest = rule = None
    if isinstance(ot, str):
        root = ot
        digest = carrier.get('output_tree_digest')
        rule = carrier.get('output_tree_digest_rule') or orc.get('output_tree_digest_def')
    elif isinstance(ot, dict):
        root = ot.get('root') or ot.get('extract_root')
        digest = ot.get('digest') or ot.get('output_tree_digest')
        rule = ot.get('digest_rule') or ot.get('digest_def') or \
            ot.get('output_tree_digest_def')
    if not isinstance(root, str) or not root:
        probs.append('carrier %r has no committed output_tree root'
                     % (carrier.get('id'),))
        root = None
    else:
        rel, why = parse_rel_path(root)
        if why:
            probs.append('output_tree root: %s' % why)
            root = None
        else:
            root = rel
            parts = root.split('/')
            if parts[0] == '..':
                probs.append('output_tree root escapes the lane')
                root = None
    if not (isinstance(digest, str) and SHA_RE.match(digest.lower())):
        probs.append('carrier %r has no 64-hex output_tree digest'
                     % (carrier.get('id'),))
        digest = None
    if rule is not None and (
            not isinstance(rule, str)
            or not all(tok in rule for tok in TREE_DIGEST_RULE_TOKENS)):
        probs.append('carrier %r output_tree digest rule %r is not the rule this '
                     'counter implements (%r)' % (carrier.get('id'), rule,
                                                  TREE_DIGEST_RULE))
    return root, (digest.lower() if isinstance(digest, str) else None), rule, probs


def carriers_spec(spec, target, expected_ids=EXPECTED_IDS):
    """(ids, problems, notes) for the frozen carrier list."""
    probs, notes = [], []
    if not isinstance(spec, dict):
        return [], ['carriers.json is not an object'], notes
    if 'claim' in spec and spec.get('claim') != 'R49-C1':
        probs.append('claim %r != R49-C1' % (spec.get('claim'),))
    if 'target' in spec and spec.get('target') != target:
        probs.append('frozen target %r != counter target %d'
                     % (spec.get('target'), target))
    # The frozen table's layout block is advisory only: the counter implements
    # the v1/v2 offsets from unblob's own v1/v2 class (S119). A block that
    # declares v3/v4 offsets is recorded, never used to parse (reading
    # `bytes_used` at 40 or "compression" at 20 is the R49-C1Oracle defect).
    layout = spec.get('superblock_layout')
    if isinstance(layout, dict):
        conflicts = []
        for name, off, width in SB_FIELDS:
            for key in (name + '_offset', name + '_len'):
                if key not in layout:
                    continue
                want = off if key.endswith('_offset') else width
                if layout[key] != want:
                    conflicts.append('%s=%r (v1/v2: %r)' % (key, layout[key], want))
        if 'compression_offset' in layout or 'compression_len' in layout:
            conflicts.append('compression fields are not part of the v1/v2 '
                             'superblock (the class is observed from the inode '
                             'table metadata block)')
        if conflicts:
            notes.append('carriers.json superblock_layout block disagrees with '
                         'the v1/v2 layout the counter implements: '
                         + '; '.join(conflicts[:4]))
    cs = spec.get('carriers')
    if not isinstance(cs, list):
        return [], probs + ['carriers is not a list'], notes
    ids = [c.get('id') for c in cs if isinstance(c, dict)]
    if len(ids) != target:
        probs.append('carriers has %d entries, want %d' % (len(ids), target))
    if len(set(ids)) != len(ids):
        probs.append('duplicate carrier ids %r' % (ids,))
    if expected_ids:
        got = {str(i).lower() for i in ids if isinstance(i, str)}
        want = {i.lower() for i in expected_ids}
        missing = sorted(want - got)
        extra = sorted(got - want)
        if missing:
            probs.append('missing preregistered carrier id(s) %r' % (missing,))
        if extra:
            probs.append('carrier id(s) %r are not part of R49-C1 (the claim '
                         'freezes exactly %r; v2.1 stays unbound)'
                         % (extra, list(expected_ids)))
    pins = [c.get('sha256') for c in cs if isinstance(c, dict)]
    if len(set(pins)) != len(pins):
        probs.append('duplicate carrier pins')
    for c in cs:
        if not isinstance(c, dict):
            probs.append('non-object carrier entry')
            continue
        cid = c.get('id')
        for key in ('id', 'handler', 'sha256', 'path'):
            v = c.get(key)
            if not isinstance(v, str) or not v:
                probs.append('carrier %r lacks %s' % (cid, key))
        sha = c.get('sha256')
        if isinstance(sha, str) and not SHA_RE.match(sha.lower()):
            probs.append('carrier %r sha256 is not 64 hex' % (cid,))
        size = c.get('size')
        if not (isinstance(size, int) and not isinstance(size, bool) and size > 0):
            probs.append('carrier %r size is not a positive int' % (cid,))
        rel, why = parse_rel_path(c.get('path'))
        if why:
            probs.append('carrier %r path: %s' % (cid, why))
        elif not (rel.startswith('corpus/evidence/') or rel.startswith('res/')):
            probs.append('carrier %r path %r is not a committed evidence blob'
                         % (cid, rel))
        handler = c.get('handler')
        if handler not in MAJOR_BY_HANDLER:
            probs.append('carrier %r handler %r is not squashfs_v1/squashfs_v2'
                         % (cid, handler))
            handler = None
        endian = c.get('endianness', c.get('endian'))
        if endian not in MAGIC_BY_ENDIAN:
            probs.append('carrier %r endianness %r is not le/be' % (cid, endian))
        major = c.get('s_major')
        if not (isinstance(major, int) and not isinstance(major, bool)):
            probs.append('carrier %r s_major is not an int' % (cid,))
        elif handler is not None and MAJOR_BY_HANDLER[handler] != major:
            probs.append('carrier %r handler %r contradicts s_major %r'
                         % (cid, handler, major))
        minor = c.get('s_minor')
        if not (isinstance(minor, int) and not isinstance(minor, bool) and minor >= 0):
            probs.append('carrier %r s_minor is not a non-negative int' % (cid,))
        if normalize_compression(c.get('compression')) is None:
            probs.append('carrier %r compression %r names no v1/v2 class %r'
                         % (cid, c.get('compression'), list(COMPRESSIONS)))
        expected = c.get('expected_regular')
        if not (isinstance(expected, int) and not isinstance(expected, bool)
                and expected > 0):
            probs.append('carrier %r expected_regular is not a positive int' % (cid,))
        rows, nrows, oprobs = oracle_rows(c)
        probs.extend('carrier %r: %s' % (cid, p) for p in oprobs)
        if rows and isinstance(expected, int) and len(rows) != expected:
            probs.append('carrier %r oracle has %d rows but expected_regular is %d'
                         % (cid, len(rows), expected))
        _root, _digest, _rule, tprobs = output_tree_binding(c)
        probs.extend('carrier %r: %s' % (cid, p) for p in tprobs)
        oracle_root = c.get('oracle_root')
        if oracle_root is not None:
            if not (isinstance(oracle_root, str) and oracle_root
                    and not oracle_root.startswith('/')
                    and '..' not in oracle_root.split('/')):
                probs.append('carrier %r oracle_root is not a relative path' % (cid,))
        receipt = c.get('receipt')
        if receipt is not None:
            _rel, why = parse_rel_path(receipt)
            if why:
                probs.append('carrier %r receipt: %s' % (cid, why))
    pp = spec.get('prior_pins')
    if pp is not None and not (isinstance(pp, list)
                               and all(isinstance(x, str) and SHA_RE.match(x.lower())
                                       for x in pp)):
        probs.append('prior_pins must be a list of 64-hex pins')
    prof = spec.get('projection', DEFAULT_PROFILE)
    if prof not in PROFILES:
        probs.append('projection profile %r not in %r' % (prof, list(PROFILES)))
    return ids, probs, notes


# ------------------------------------------------------------- carrier layout

def sb_u(raw, off, width, endian):
    return int.from_bytes(raw[off:off + width], 'big' if endian == 'be' else 'little')


def round_up(value, multiple):
    return ((value + multiple - 1) // multiple) * multiple


def chunk_end(raw, bytes_used, start=0):
    """unblob 26.6.4's chunk end for a SquashFS chunk at `start`, or None.

    `_SquashFSBase.calculate_chunk` seeks to `start + bytes_used`, reads up to
    `round_up(bytes_used, 4096) - bytes_used` bytes, and for pad_size in
    (4096, 1024) returns `start + round_up(bytes_used, pad_size)` when that many
    tail bytes are zero, else `start + bytes_used`."""
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


def metadata_length(raw, off, endian):
    """(length, uncompressed) of the metadata block header at `off`, or (None, None).

    SquashFS v1/v2 store a 2-byte header whose low 12 bits are the stored
    length and whose top bit marks an uncompressed block (squashfs-tools
    SQUASHFS_COMPRESSED_BIT_BLOCK); the frame is settled by the chain witness
    `off + 2 + length == directory_table_start`, which every frozen carrier
    satisfies in its own endianness (measured)."""
    if off < 0 or off + 2 > len(raw):
        return None, None
    header = sb_u(raw, off, 2, endian)
    length = header & ~UNCOMPRESSED_FLAG
    if not (1 <= length <= METADATA_MAX):
        return None, None
    return length, bool(header & UNCOMPRESSED_FLAG)


def compression_class(chunk):
    """'gzip' for a zlib stream, 'lzma' for an LZMA-alone/raw-LZMA1 stream, else None."""
    if len(chunk) >= 2 and chunk[0] == 0x78 and chunk[1] in (0x01, 0x5E, 0x9C, 0xDA):
        return 'gzip'
    if chunk[:2] == b'\x5d\x00' or chunk[:4] == b'\x00\x00\x80\x00':
        return 'lzma'
    import lzma as _lzma
    try:
        zlib.decompress(chunk)
        return 'gzip'
    except Exception:
        pass
    if chunk[:1] == b'\x00':
        try:
            dec = _lzma.LZMADecompressor(format=_lzma.FORMAT_RAW, filters=[
                {'id': _lzma.FILTER_LZMA1, 'lc': 3, 'lp': 0, 'pb': 2,
                 'dict_size': 1 << 23}])
            if dec.decompress(chunk, max_length=8192):
                return 'lzma'
        except Exception:
            pass
    return None


def layout_probe(raw, expect):
    """Decode a SquashFS v1/v2 superblock and check it against the frozen entry.

    The struct is the 32-byte packed one unblob 26.6.4 parses for v1/v2
    (`SquashFSv1Handler.C_DEFINITIONS`, S119): magic 0:4, inodes u32@4,
    bytes_used u32@8, uid_start u32@12, guid_start u32@16,
    inode_table_start u32@20, directory_table_start u32@24, s_major u16@28,
    s_minor u16@30.  There is no compression field: the class is observed from
    the inode table's first metadata block body, and the frame of that block is
    witnessed by `inode_table_start + 2 + length == directory_table_start`.
    Endianness is read from the magic order: `hsqs` = little, `sqsh` = big.
    Every expected value comes from the frozen carrier entry; the probe never
    supplies a default."""
    d = {'size': len(raw) if raw is not None else 0,
         'declared': {k: expect.get(k) for k in
                      ('handler', 'endian', 'endianness', 's_major', 's_minor',
                       'compression')} if isinstance(expect, dict) else None}
    if raw is None:
        d.update(ok=False, reason='absent')
        return d
    if not isinstance(expect, dict):
        d.update(ok=False, reason='no frozen carrier entry')
        return d
    if len(raw) < SB_SIZE:
        d.update(ok=False, reason='shorter than the 32-byte v1/v2 superblock')
        return d
    d['magic'] = raw[0:4].decode('latin1')
    endian = ENDIAN_BY_MAGIC.get(raw[0:4])
    d['endianness'] = endian
    d['frozen_endianness'] = expect.get('endianness', expect.get('endian'))
    d['magic_expected'] = (MAGIC_BY_ENDIAN[d['frozen_endianness']].decode('latin1')
                           if d['frozen_endianness'] in MAGIC_BY_ENDIAN else None)
    d['magic_ok'] = bool(endian is not None and d['magic_expected'] is not None
                         and raw[0:4] == MAGIC_BY_ENDIAN[d['frozen_endianness']])
    if endian is None:
        d.update(ok=False, reason='magic %r is not a SquashFS v1/v2 magic '
                                  '(hsqs/sqsh); zlqs/sqlz is v2 nonstandard'
                 % (d['magic'],))
        return d
    for name, off, width in SB_FIELDS[1:]:
        d[name] = sb_u(raw, off, width, endian)
    d['handler_implied'] = HANDLER_BY_MAJOR.get(d['s_major'])
    d['handler'] = expect.get('handler')
    d['s_major_ok'] = d['s_major'] == expect.get('s_major')
    d['s_minor_ok'] = d['s_minor'] == expect.get('s_minor')
    d['handler_ok'] = d['handler_implied'] is not None and d['handler_implied'] == d['handler']
    bu = d['bytes_used']
    its, dts = d['inode_table_start'], d['directory_table_start']
    d['bytes_used_sane'] = SB_SIZE <= bu <= len(raw)
    d['starts_sane'] = bool(d['bytes_used_sane'] and SB_SIZE <= its < dts <= bu)
    d['chunk_end'] = chunk_end(raw, bu) if d['bytes_used_sane'] else None
    d['meta_header_hex'] = None
    d['meta_len'] = d['meta_len_raw'] = None
    d['meta_uncompressed'] = None
    d['meta_chain_lands'] = False
    d['compression'] = None
    if d['starts_sane']:
        hdr = raw[its:its + 2]
        d['meta_header_hex'] = hdr.hex()
        length_raw = sb_u(raw, its, 2, endian)
        d['meta_len_raw'] = length_raw & ~UNCOMPRESSED_FLAG
        length, unc = metadata_length(raw, its, endian)
        d['meta_len'] = length
        d['meta_uncompressed'] = unc
        d['meta_chain_lands'] = bool(length is not None
                                     and its + 2 + length == dts)
        if length is not None and not unc:
            d['compression'] = compression_class(raw[its + 2:its + 2 + length])
    reason = None
    if not d['magic_ok']:
        reason = 'magic %r is not the frozen %r for %s' % (
            d['magic'], d['magic_expected'], d['frozen_endianness'])
    elif not d['s_major_ok']:
        reason = 's_major %d is not the frozen %r' % (d['s_major'], expect.get('s_major'))
    elif not d['s_minor_ok']:
        reason = 's_minor %d is not the frozen %r' % (d['s_minor'], expect.get('s_minor'))
    elif not d['handler_ok']:
        reason = 's_major %d implies handler %r, frozen %r' % (
            d['s_major'], d['handler_implied'], d['handler'])
    elif not d['bytes_used_sane']:
        reason = 'bytes_used %d outside 32..%d' % (bu, len(raw))
    elif not d['starts_sane']:
        reason = 'inode/directory table starts %d/%d outside the filesystem (%d)' % (
            its, dts, bu)
    elif d['meta_len'] is None:
        reason = ('first metadata block length does not decode %s-endian '
                  '(header %r)' % (endian, d['meta_header_hex']))
    elif d['meta_uncompressed']:
        reason = ('inode table metadata block is stored uncompressed: the '
                  'compression class is undetermined')
    elif not d['meta_chain_lands']:
        reason = ('metadata chain does not land on directory_table_start '
                  '(%d + 2 + %r != %d)' % (its, d['meta_len'], dts))
    elif d['compression'] is None:
        reason = 'compression undetermined from the inode table metadata block'
    elif normalize_compression(expect.get('compression')) is not None and \
            d['compression'] != normalize_compression(expect.get('compression')):
        reason = 'observed compression %r is not the frozen %r' % (
            d['compression'], expect.get('compression'))
    d['ok'] = reason is None
    d['reason'] = reason
    return d


# ------------------------------------------------------------- receipt shape

def provenance_ok(output_directory):
    """A receipt run by this round: absolute, inside the kaidoku-r49 segment."""
    if not isinstance(output_directory, str) or not os.path.isabs(output_directory):
        return False
    if PROV_SEGMENT not in output_directory:
        return False
    return '..' not in output_directory.split('/')


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
    """Components of a receipt path, `$output/` sigil removed, '.' dropped."""
    if not isinstance(path, str) or not path:
        return None
    p = path
    while p.startswith('$output/'):
        p = p[len('$output/'):]
    return [x for x in p.split('/') if x not in ('', '.')]


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


def receipt_paths(env):
    """Every path a receipt normalizes, relative to REA's unblob output root."""
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


def path_shape_ok(env):
    """(ok, first problem) over every path the receipt normalises."""
    for p in receipt_paths(env):
        problem = path_shape_problem(p)
        if problem:
            return False, problem
    return True, None


def strip_output(path):
    if not isinstance(path, str):
        return path
    if path.startswith('$output/'):
        return path[len('$output/'):]
    return path


def under_root(path, root):
    """Segment-bounded containment: `P == CR or P.startswith(CR + '/')` (R41-D5)."""
    if not isinstance(path, str) or not isinstance(root, str) or not root:
        return False
    p = strip_output(path)
    if p == root:
        return True
    return p.startswith(root.rstrip('/') + '/')


def squashfs_roots(env, handler):
    """The receipt's chunk extract roots for one frozen handler (exact equality)."""
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
    """(extract root, how) of the chunk whose filesystem the oracle describes."""
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
    root, how = subject_root(env, handler, hint)
    return {'roots': squashfs_roots(env, handler), 'subject': root, 'source': how}


def diagnostic_rel(diagnostic, root, output_directory=None):
    """A removal diagnostic's entry path relative to the chunk extract root."""
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
    """A receipt path relative to its chunk extract root, or None if not inside."""
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
    """The round-40 matcher, verbatim (defect R40-CL1). Selftest only."""
    return bool(candidate) and bool(rel) and (candidate == rel
                                              or candidate.endswith('/' + rel))


def published(env):
    nr = env.get('normalized_result') or {}
    out = []
    for f in (nr.get('files') or []):
        if isinstance(f, dict):
            out.append((f.get('relative_path') or '', f.get('sha256') or '',
                        f.get('size')))
    return out


def chunk_handlers(env):
    nr = env.get('normalized_result') or {}
    return [c.get('handler') for c in (nr.get('chunks') or []) if isinstance(c, dict)]


def squashfs_chunk_handlers(env):
    return [h for h in chunk_handlers(env)
            if isinstance(h, str) and SQUASHFS_HANDLER_RE.match(h)]


def chunk_failed(env):
    nr = env.get('normalized_result') or {}
    return any(isinstance(c, dict) and c.get('extraction_failed')
               for c in (nr.get('chunks') or []))


def gaps(env):
    nr = env.get('normalized_result') or {}
    return list(nr.get('extraction_gaps') or [])


def oracle_hits(rows, files, root):
    """Census rows published exactly: rel, sha256 and size."""
    if root is None:
        return 0
    hits = 0
    for rel, sha, want_size in rows:
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


def extra_published(rows, files, root):
    """Published regular files under the root that the census does not list."""
    if root is None:
        return []
    want = {strip_rel(row[0]) for row in rows}
    return [rel for rel in published_rels(files, root) if rel not in want]


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
    """Does an oracle row's detail name one of the rule's silent details?"""
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
    """Three families, all frozen data (R41C1DevCore 7.1, rule frozen in GAP_RULE)."""
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
            removed_rels[hits[0]] = removed_rels.get(hits[0], 0) + 1

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


# ------------------------------------------------------------- freeze walk

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
    """(pins, sources) a previous C1 freeze already scored."""
    pins, sources = set(), []
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
    listed = spec.get('prior_pins')
    if isinstance(listed, list):
        for p in listed:
            if isinstance(p, str) and SHA_RE.match(p.lower()):
                pins.add(p.lower())
        if listed:
            sources.append('prior_pins(extra)')
    return pins, sources


def _frozen_paths(spec):
    frozen = set(FROZEN_PATHS)
    for c in spec.get('carriers') or []:
        if not isinstance(c, dict):
            continue
        if isinstance(c.get('path'), str) and c['path']:
            frozen.add(c['path'])
        root, _d, _r, _p = output_tree_binding(c)
        if root:
            frozen.add(root)
    return frozen


def frozen_drift(root, freeze, rev, spec):
    """Commits in FREEZE..REV that change a frozen C1 path (claims freeze rule).

    Merge-aware (`-m --diff-merges=first-parent`): a frozen path edited inside a
    merged branch is a change. M/D/R/T/U are changes; A is a change whenever the
    path existed at FREEZE (a re-add is not a restore). Each frozen regular-file
    blob that exists at both endpoints must also be byte-identical: a later
    restore does not un-block."""
    frozen = _frozen_paths(spec)
    prefixes = FROZEN_PREFIXES

    def is_frozen(path):
        return path in frozen or any(path.startswith(p) for p in prefixes)

    p = git(root, 'log', '-m', '--diff-merges=first-parent', '--name-status',
            '--pretty=format:', f'{freeze}..{rev}', check=False)
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
                if path not in existed_cache:
                    existed_cache[path] = show(root, freeze, path) is not None
                if existed_cache[path]:
                    touched.add(path)
            elif code in 'MDRTU':
                touched.add(path)
    # blob equality at the endpoints (a path could be untouched in the log but
    # differ through an exotic diff; this is cheap and exact)
    for path in sorted(frozen):
        if not path.startswith(('plans/', 'tools/', 'corpus/', 'res/', '.ufo/')):
            continue
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
    """Path after the first `<something>_extract` chunk extract directory."""
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

    Everything that varies between two runs of the same bytes is excluded:
    evidence id, absolute paths, output directory, staged input name, provider
    and blob ids, continuation ids, timestamps, selection and analysis fields.
    The chunk extract directory is normalised away because the receipt records a
    run made in another scratch tree; rea-agents 6.5.0 stages every input as
    `firmware.bin`, so the normalisation is lossless."""
    if profile not in PROFILES:
        raise Unevaluable('unknown projection profile %r' % (profile,))
    nr = env.get('normalized_result') or {}
    subject = ((env.get('subject') or {}).get('digest') or {}).get('sha256')
    proj_root = subject_root(env, handler)[0] if handler else None

    def norm(path):
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

    gaps_out = []
    for g in nr.get('extraction_gaps') or []:
        if not isinstance(g, dict):
            continue
        deps = sorted((norm(d) for d in (g.get('dependencies') or [])),
                      key=lambda v: (v is not None, v or ''))
        gaps_out.append([g.get('kind'), norm(g.get('relative_path')), deps])
    gaps_out.sort(key=canonical)

    unpub = []
    for u in nr.get('unpublished_entries') or []:
        if not isinstance(u, dict):
            continue
        unpub.append([u.get('kind'), norm(u.get('relative_path'))])
    unpub.sort(key=canonical)

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
        'extraction_gaps': gaps_out,
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
DEFAULT_PROFILE = 'plus-extractor'
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
    (`parameters.max_depth`, `max_output_bytes`, `max_output_files`), because a
    receipt produced at a shallower depth is `partial` with a truncated
    published set and a rerun at REA's default depth could never match it."""
    unblob_path = unblob or os.path.expanduser('~/.local/bin/unblob')

    def run(carrier_bytes, cid, params=None):
        npx = which_fixed('npx') or shutil.which('npx')
        if npx is None:
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
        env['PATH'] = FIXED_PATH
        argv = [npx, '-y', REA_PIN, 'extract-firmware', '--format', 'json',
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
                               'error': envl.get('error'),
                               'stdout_head': text[:300],
                               'stderr': p.stderr.decode('utf-8', 'replace')[:300]}
        return 'ok', data

    return run


# ------------------------------------------------------------- measurement

def evaluate_carrier(env, carrier, rows, nonreg, model, pin, profile, hint):
    """The receipt-side clauses for one carrier (shared by score and dev arm)."""
    d = {}
    d['chunk_handlers'] = chunk_handlers(env)
    d['squashfs_handlers'] = squashfs_chunk_handlers(env)
    handler = carrier.get('handler')
    # every squashfs-family chunk handler must be EXACTLY the frozen handler: a
    # v3/v4 (or nonstandard) handler on a v1/v2 carrier fails here.
    d['handler_ok'] = (isinstance(handler, str)
                       and d['squashfs_handlers'] == [handler])
    d['chunks_ok'] = not chunk_failed(env)
    root_value, root_how = subject_root(env, handler, hint)
    d['extract_root'] = root_value
    d['extract_root_source'] = root_how
    d['chunk_roots'] = chunk_roots(env, handler, hint)
    d['extract_root_confirmed'] = bool(
        root_value and any(under_root(p, root_value) for p in receipt_paths(env)))
    files = published(env)
    d['published_files'] = len(files)
    d['oracle_files'] = len(rows)
    d['oracle_hits'] = oracle_hits(rows, files, root_value)
    d['published_rels'] = len(published_rels(files, root_value))
    extra = extra_published(rows, files, root_value)
    d['extra_published'] = extra[:5]
    d['oracle_hits_ok'] = (len(rows) > 0 and root_value is not None
                           and d['oracle_hits'] == len(rows)
                           and d['published_rels'] == len(rows)
                           and not extra)
    diags = diagnostics(env)
    d['diagnostics'] = len(diags)
    params = env.get('parameters') or {}
    od = params.get('output_directory') if isinstance(params, dict) else None
    d['output_directory'] = od
    d['removals'] = sorted(
        rel for rel in (diagnostic_rel(x, root_value, od) for x in diags)
        if rel is not None
        and diagnostic_typename(x) == (model.get('removed') or {}).get('diagnostic'))
    ok, why = disposition_check(gaps(env), diags, nonreg, model, root_value, od)
    d['gaps_ok'] = ok
    d['gaps_note'] = why
    esc = nonregular_published(files, nonreg, root_value)
    d['nonregular_published'] = esc[:5]
    d['nonregular_unpublished_ok'] = root_value is not None and not esc
    shape_ok, shape_why = path_shape_ok(env)
    d['path_shape_ok'] = shape_ok
    d['path_shape_note'] = shape_why
    d['run_provenance_ok'] = provenance_ok(od)
    subj = env.get('subject') or {}
    d['subject_sha256'] = ((subj.get('digest') or {}).get('sha256')
                           if isinstance(subj, dict) else None)
    d['subject_pin_ok'] = d['subject_sha256'] == pin
    prov = env.get('provider') or {}
    d['operation_ok'] = (env.get('operation') == 'extract_firmware'
                         and isinstance(prov, dict) and prov.get('id') == 'unblob')
    d['profile'] = profile
    return d


def measure(root, rev, freeze, pkg65, rerun=None, target=TARGET,
            unblob=None, rea_timeout=900, receipt_overrides=None,
            dev_arm=False):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'R49-C1',
           'target': target, 'seat': 'R49C1Counter'}
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
    res['frozen_tables_valid'] = True
    cur = show(root, rev, CARRIERS)
    res['carriers_unchanged'] = cur == frozen
    layout_notes = []
    ids, spec_probs, layout_notes = carriers_spec(spec, target)
    res['carriers_spec_problems'] = spec_probs
    res['superblock_layout_notes'] = layout_notes
    profile = spec.get('projection', DEFAULT_PROFILE)
    if profile not in PROFILES:
        profile = DEFAULT_PROFILE
    res['projection_profile'] = profile
    model, rule_probs = gap_rule_model(GAP_RULE)
    res['gap_rule_problems'] = rule_probs
    prior, prior_sources = prior_pins(root, freeze, spec)
    res['prior_pins'] = sorted(prior)
    res['prior_pin_sources'] = prior_sources

    drift = frozen_drift(root, freeze, rev, spec)
    res['frozen_path_changed'] = drift
    if drift:
        raise FrozenPathChanged(drift)

    work = tempfile.mkdtemp(prefix='c1-counter.', dir=scratch_root())
    try:
        runner = rerun or make_real_runner(work, unblob, rea_timeout)
        per, envs = {}, {}
        for c in spec.get('carriers') or []:
            if not isinstance(c, dict):
                continue
            k = c.get('id')
            d = {'id': k}
            pin = (c.get('sha256') or '').lower() or None
            handler = c.get('handler') if isinstance(c.get('handler'), str) else None
            d['handler'] = handler
            cpath = c.get('path') if isinstance(c.get('path'), str) else None
            d['carrier_path'] = cpath
            mode = blob_mode(root, rev, cpath) if cpath else None
            d['carrier_mode'] = mode
            raw = show(root, rev, cpath) if cpath else None
            d['carrier_present'] = raw is not None and mode == '100644'
            d['carrier_pin_ok'] = (raw is not None and pin is not None
                                   and hashlib.sha256(raw).hexdigest() == pin)
            d['carrier_size_ok'] = True
            d['carrier_fresh_ok'] = pin is not None and pin not in prior
            d['carrier_fresh_against'] = prior_sources
            d['layout'] = layout_probe(raw, c)
            d['layout_ok'] = bool(d['layout'].get('ok'))
            d['layout_reason'] = d['layout'].get('reason')
            d['compression'] = d['layout'].get('compression')
            d['endianness'] = d['layout'].get('endianness')
            bu = d['layout'].get('bytes_used')
            ce = d['layout'].get('chunk_end')
            d['carve'] = {'size': d['layout'].get('size'), 'bytes_used': bu,
                          'chunk_end': ce}
            d['carve_ok'] = bool(isinstance(ce, int)
                                 and d['layout'].get('size') == ce)

            rows, nonreg, oprobs = oracle_rows(c)
            d['oracle_error'] = oprobs[0] if oprobs else None
            d['oracle_files'] = len(rows)
            d['nonregular_entries'] = len(nonreg)
            d['nonregular_kinds'] = sorted({kind for _rel, kind, _d in nonreg})
            d['oracle_ok'] = not oprobs
            troot, tdigest, _trule, tprobs = output_tree_binding(c)
            d['tree'] = {'root': troot, 'digest': tdigest,
                         'problems': tprobs[:4]}
            d['tree_ok'], d['tree_note'] = tree_check(root, rev, troot, tdigest,
                                                     rows)

            if receipt_overrides is not None and k in receipt_overrides:
                env = receipt_overrides[k]
                d['receipt_path'] = '<dev-arm>'
            else:
                rpath = c.get('receipt') or '%s/%s/after.json' % (AFTERDIR, k)
                raw_receipt = show(root, rev, rpath)
                try:
                    env = json.loads(raw_receipt) if raw_receipt else None
                except json.JSONDecodeError:
                    env = None
                if not isinstance(env, dict):
                    env = None
                d['receipt_path'] = rpath
                d['receipt_digest'] = sha256_bytes(raw_receipt)
                add = first_add(root, rev, rpath) if raw_receipt is not None else None
                d['receipt_first_add'] = add
                d['receipt_fresh'] = bool(add) and add != freeze \
                    and is_ancestor(root, freeze, add)
            d['receipt_present'] = env is not None
            if dev_arm:
                # The dev arm scores freshly produced envelopes: first-add and
                # the envelope/pin shape are not evaluable there, and the rerun
                # clause has nothing to compare against yet.
                d['receipt_fresh'] = None
            if env is not None:
                envs[f'{k}/after'] = env
                d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}
                                                 & set(env))
                d.update(evaluate_carrier(env, c, rows, nonreg, model, pin,
                                          profile,
                                          c.get('oracle_root')
                                          if isinstance(c.get('oracle_root'), str)
                                          else None))
                if raw is not None and d['carrier_pin_ok'] and not dev_arm:
                    status, payload = runner(raw, k, env.get('parameters'))
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
                elif dev_arm:
                    d['projection_ok'] = None
                    d['projection_note'] = 'dev-arm: no committed receipt to compare'
                else:
                    d['projection_ok'] = False
                    d['projection_skipped'] = ('carrier_pin_ok'
                                               if not d.get('carrier_pin_ok')
                                               else 'carrier_absent')
            per[k] = d

        ev = evidence_ids(root, freeze, pkg65, envs, work)
        matched = 0
        dev_matched = 0
        for k, d in per.items():
            key = f'{k}/after'
            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]
                                   and ev[key][0].startswith('ev_'))
            if dev_arm:
                core = [x for x in CLAUSES
                        if x not in ('receipt_fresh', 'projection_ok')]
                ok = all(d.get(x) is True for x in core)
                d['dev_matched'] = bool(ok)
                dev_matched += bool(ok)
            else:
                d['matched'] = all(d.get(x) is True for x in CLAUSES)
                matched += bool(d['matched'])
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = matched
        res['dev_matched'] = dev_matched
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
    rows_p = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(
        'squashfs_v1' in r and 'squashfs_v2' in r and SQFS12_TEXT_RE.search(r)
        and ENTRY in r
        for r in rows_p)
    b['province_core_rows_seen'] = [cells(r)[0] for r in rows_p]
    b['frontier_note'] = any(FRONTIER_MARK in l and STEM in l
                             and SQFS12_TEXT_RE.search(l)
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
    b['sourced'] = all(sid in ok_ids for sid in REQUIRED_SIDS)
    readme = show(root, rev, 'corpus/README.md')
    cm = section(readme.decode(errors='replace'), '## Coverage map') if readme else None
    b['coverage_map_row'] = bool(cm) and any(
        STEM in l for l in cm if l.lstrip().startswith('|'))
    b['carriers_spec_ok'] = not spec_probs
    kinds_seen = set()
    for d in (res.get('carriers') or {}).values():
        kinds_seen |= set(d.get('nonregular_kinds') or [])
    uncovered = sorted(kinds_seen - set(model.get('allowed') or {}))
    b['gap_rule_ok'] = not rule_probs and not uncovered
    b['gap_rule_uncovered_kinds'] = uncovered
    ends = [d.get('endianness') for d in (res.get('carriers') or {}).values()]
    b['endianness_coverage'] = (any(e == 'le' for e in ends)
                                and any(e == 'be' for e in ends))
    b['endianness_detail'] = ends
    fams = [d.get('handler') for d in (res.get('carriers') or {}).values()]
    b['family_coverage'] = ('squashfs_v1' in fams and 'squashfs_v2' in fams)
    b['handler_detail'] = fams
    b['compression_detail'] = [d.get('compression')
                               for d in (res.get('carriers') or {}).values()]
    tok, tdetail = oracle_tool_ok(spec)
    b['oracle_tool_ok'] = tok
    b['oracle_tool_detail'] = tdetail
    b['frozen_tables_valid'] = bool(res.get('frozen_tables_valid'))
    b['superblock_layout_notes'] = layout_notes
    res['bindings'] = b
    if dev_arm:
        res['met_target'] = False
        res['dev_clean'] = (res['dev_matched'] == len(res.get('carriers') or {}))
    else:
        res['met_target'] = bool(res['carriers_unchanged']
                                 and res['carriers_matched'] == target
                                 and all(b[x] is True for x in BINDINGS))
    return res


def oracle_tool_ok(spec):
    """(ok, detail) for the frozen oracle identity against the live binary."""
    doc = spec.get('oracle') if isinstance(spec, dict) else None
    if not isinstance(doc, dict):
        return True, {'reason': 'no oracle block frozen (advisory)'}
    tool = doc.get('tool')
    detail = {'tool': tool}
    if not isinstance(tool, str) or not tool:
        return False, dict(detail, reason='oracle.tool is not a path')
    detail['path'] = tool
    if not (os.path.isfile(tool) and os.access(tool, os.X_OK)):
        return False, dict(detail, reason='oracle tool not executable')
    got = file_sha256(tool)
    detail['sha256'] = got
    want = doc.get('sha256') or doc.get('tool_sha256')
    ok = True
    if isinstance(want, str):
        detail['frozen_sha256'] = want
        ok = ok and got == want.lower()
    ver = doc.get('version')
    if isinstance(ver, str) and ver:
        try:
            r = subprocess.run([tool, '-version'], capture_output=True, text=True,
                               timeout=30)
            line = (r.stdout or r.stderr).splitlines()[0] if (r.stdout or r.stderr) else ''
        except (OSError, subprocess.SubprocessError):
            line = ''
        detail['version_line'] = line
        ok = ok and ver in line
    return ok, detail


def tree_check(root, rev, troot, tdigest, rows):
    """(ok, note) for the committed S138 expected tree against the census rows."""
    if troot is None:
        return False, 'no committed output_tree root in the frozen table'
    entries = tree_entries(root, rev, troot)
    if not entries:
        return False, 'output_tree %r has no files at %s' % (troot, rev)
    members = []
    for mode, _blob, _size, path in entries:
        if mode not in ('100644', '100755'):
            return False, 'output_tree contains a non-regular entry %r (mode %s)' \
                % (path, mode)
        rel = path[len(troot):].lstrip('/') if path.startswith(troot) else path
        body = show(root, rev, path)
        if body is None:
            return False, 'output_tree member %r unreadable at %s' % (path, rev)
        members.append((rel, hashlib.sha256(body).hexdigest(), len(body)))
    members.sort(key=lambda m: m[0].encode())
    digest = hashlib.sha256(''.join('%s\t%s\n' % (p, h)
                                    for p, h, _s in members).encode()).hexdigest()
    if tdigest is not None and digest != tdigest:
        return False, 'output_tree digest %s != frozen %s' % (digest, tdigest)
    want = sorted(rows, key=lambda r: r[0].encode())
    if members != want:
        extra = [m[0] for m in members if (m[0], m[1], m[2]) not in set(want)]
        missing = [r[0] for r in want if r not in set(members)]
        return False, ('output_tree disagrees with the census rows '
                       '(extra %r, missing %r)' % (extra[:4], missing[:4]))
    return True, 'output_tree digest %s, %d members' % (digest, len(members))


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


def failing_lists(res):
    """(per-carrier failing clause names, false binding names) for the receipt."""
    fails = []
    for k, v in (res.get('carriers') or {}).items():
        exempt = ('receipt_fresh', 'projection_ok') if v.get('dev_matched') is not None \
            else ()
        for x in CLAUSES:
            if x in exempt:
                continue
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
                    '$HYAKU_SCRATCH/kaidoku-r49/counter)')
    ap.add_argument('--rea-timeout', type=int, default=900)
    ap.add_argument('--no-rerun', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--dev-arm', action='store_true')
    ap.add_argument('--arm-dir', help='directory of captured REA envelopes: '
                    '<id>/after.json (dev arm)')
    ap.add_argument('--arm-ids', help='comma-separated carrier ids (dev arm)')
    ap.add_argument('--run-rea', action='store_true',
                    help='dev arm: run REA 6.5.0 on the carrier bytes into '
                         'scratch (never writes corpus/evidence/round-49/c1)')
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
    if a.dev_arm:
        return dev_arm(a)
    if a.no_rerun:
        out = {'reason': 'rerun_disabled',
               'detail': 'R49-C1 binds a fresh REA run of each carrier; '
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
                      rea_timeout=a.rea_timeout)
    except Unevaluable as e:
        res = {'unevaluable': str(e), 'reason': e.reason, 'argv': sys.argv,
               'exit_code': 2, 'seat': 'R49C1Counter'}
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
                                          'frozen_path_changed', 'bindings',
                                          'failing', 'bindings_false',
                                          'met_target', 'exit_code')},
                     sort_keys=True))
    if a.json_out:
        stamped, ok, why = write_receipt(res, a.json_out)
        if not ok:
            print(json.dumps({'reason': 'receipt_identity_failed', 'detail': why},
                             sort_keys=True), file=sys.stderr)
            return 2
    return res['exit_code']


# ------------------------------------------------------------- dev arm (K3)

def dev_arm(a):
    """Positive development control: score REAL REA envelopes for the carriers.

    R44RevKill K3: a counter that always exits 1 passes every red arm, so the
    claim needs a positive control driven by real REA 6.5.0 envelopes. This mode
    never writes `corpus/evidence/round-49/c1` and never claims anything: it
    either scores envelopes already captured under --arm-dir (`<id>/after.json`)
    or runs REA 6.5.0 itself into scratch (--run-rea). Exit 0 only when every
    requested carrier maps clean under the R49-C1 carrier clauses (the
    freeze-only clauses `receipt_fresh` and the rerun `projection_ok` have no
    committed endpoint here and are exempt; they are exercised by --selftest)."""
    root = a.root
    if not root:
        print('usage: --dev-arm needs --root', file=sys.stderr)
        return 2
    rev = a.rev or 'HEAD'
    pkg65 = a.pkg65 or find_rea_pkg()
    if not pkg65:
        print(json.dumps({'reason': 'no rea-agents package found for --pkg65',
                          'seat': 'R49C1Counter'}, sort_keys=True))
        return 2
    raw_spec = show(root, rev, CARRIERS)
    if raw_spec is None:
        print(json.dumps({'reason': 'carriers.json absent at %s' % rev},
                         sort_keys=True))
        return 2
    spec = json.loads(raw_spec)
    carriers = [c for c in spec.get('carriers') or [] if isinstance(c, dict)]
    wanted = ([x.strip().lower() for x in a.arm_ids.split(',') if x.strip()]
              if a.arm_ids else None)
    work = tempfile.mkdtemp(prefix='c1-devarm.', dir=scratch_root())
    envs, notes = {}, {}
    try:
        if a.arm_dir:
            for c in carriers:
                cid = c.get('id')
                if wanted and str(cid).lower() not in wanted:
                    continue
                for name in ('after.json', 'envelope.json', 'env.json'):
                    p = os.path.join(a.arm_dir, str(cid), name)
                    if os.path.isfile(p):
                        try:
                            with open(p) as fh:
                                doc = json.load(fh)
                        except (OSError, json.JSONDecodeError) as e:
                            notes[cid] = 'unreadable envelope: %s' % e
                            continue
                        if isinstance(doc, dict) and 'data' in doc \
                                and isinstance(doc['data'], dict):
                            doc = doc['data']
                        if isinstance(doc, dict):
                            envs[cid] = doc
                        else:
                            notes[cid] = 'envelope is not an object'
                        break
                else:
                    notes[cid] = 'no envelope under %r' % (a.arm_dir,)
        elif a.run_rea:
            runner = make_real_runner(work, a.unblob, a.rea_timeout)
            for c in carriers:
                cid = c.get('id')
                if wanted and str(cid).lower() not in wanted:
                    continue
                raw = show(root, rev, c.get('path'))
                if raw is None:
                    notes[cid] = 'carrier bytes absent at %s' % rev
                    continue
                status, payload = runner(raw, cid, {'max_depth': 3})
                if status == 'ok':
                    envs[cid] = payload
                else:
                    notes[cid] = 'REA run failed: %r' % (
                        {k: payload.get(k) for k in ('ok', 'exit', 'error')},)
        else:
            print(json.dumps({'reason': 'dev arm needs --arm-dir DIR or --run-rea',
                              'seat': 'R49C1Counter'}, sort_keys=True))
            return 2
        res = measure(root, rev, rev, pkg65, receipt_overrides=envs, dev_arm=True,
                      unblob=a.unblob, rea_timeout=a.rea_timeout)
    except Unevaluable as e:
        print(json.dumps({'reason': e.reason, 'detail': str(e),
                          'seat': 'R49C1Counter'}, sort_keys=True))
        return 2
    finally:
        shutil.rmtree(work, ignore_errors=True)
    fails, binds = failing_lists(res)
    scored = [k for k in (res.get('carriers') or {})
              if not wanted or str(k).lower() in wanted]
    per = {k: {'dev_matched': (res['carriers'][k] or {}).get('dev_matched'),
               'handler': (res['carriers'][k] or {}).get('handler'),
               'layout_ok': (res['carriers'][k] or {}).get('layout_ok'),
               'oracle_hits': (res['carriers'][k] or {}).get('oracle_hits'),
               'oracle_files': (res['carriers'][k] or {}).get('oracle_files'),
               'tree_ok': (res['carriers'][k] or {}).get('tree_ok'),
               'gaps_ok': (res['carriers'][k] or {}).get('gaps_ok'),
               'evidence_id_ok': (res['carriers'][k] or {}).get('evidence_id_ok')}
           for k in scored}
    clean = sum(1 for v in per.values() if v['dev_matched'])
    out = {'seat': 'R49C1Counter', 'mode': 'dev-arm', 'rev': rev,
           'scored': len(scored), 'dev_matched': clean,
           'per_carrier': per, 'notes': notes,
           'failing': fails, 'bindings_false': binds,
           'exit_code': 0 if (scored and clean == len(scored)) else 1}
    print(json.dumps(out, sort_keys=True))
    if a.json_out:
        write_receipt(out, a.json_out)
    return out['exit_code']


# ---------------------------------------------------------------- selftest

def find_xpin(here):
    """Locate tools/round-27/xpin-attribute.mjs from a checkout or an artifact dir."""
    for d in [here] + [os.path.dirname(here)] + \
            [os.path.abspath(os.path.join(here, *(['..'] * n))) for n in range(2, 12)]:
        for rel in ('round-27/xpin-attribute.mjs', 'tools/round-27/xpin-attribute.mjs'):
            p = os.path.join(d, rel)
            if os.path.isfile(p):
                return p
    raise SystemExit('xpin-attribute.mjs not found from ' + here)


def sb_v12(major, endian, *, minor=0, inodes=3, magic=None, bytes_used=None,
           pad=0, truncate=0, meta_len=None, meta_uncompressed=False,
           payload=None):
    """A fixture carrier: a coherent SquashFS v1/v2 image, laid out as the format is.

    Not a real filesystem -- `layout_probe` is a superblock/relocation test and
    these bytes exercise it exactly: the (endianness) magic, the shared v1/v2
    32-byte struct, one inode-table metadata block carrying a zlib body, the
    directory table the chain witness must land on, and the tables after it."""
    body = bytearray(SB_SIZE)
    body[0:4] = magic if magic is not None else MAGIC_BY_ENDIAN[endian]
    body += b'block-payload-' * 2
    its = len(body)
    if payload is None:
        payload = zlib.compress(b'R49C1 selftest inode table payload ' * 2, 9)
    length = len(payload) if meta_len is None else meta_len
    header = length | (UNCOMPRESSED_FLAG if meta_uncompressed else 0)
    body += header.to_bytes(2, 'big' if endian == 'be' else 'little') + payload
    dts = len(body)
    body += b'\x00' * 8
    fts = len(body)
    body += b'\x00' * 8
    lts = len(body)
    body += b'\x00' * 8
    order = 'big' if endian == 'be' else 'little'

    def put(off, width, value):
        body[off:off + width] = (int(value) & ((1 << (8 * width)) - 1)).to_bytes(
            width, order)

    used = len(body) if bytes_used is None else bytes_used
    put(4, 4, inodes)
    put(8, 4, used)
    put(12, 4, len(body) - 12)
    put(16, 4, 0)
    put(20, 4, its)
    put(24, 4, dts)
    put(28, 2, major)
    put(30, 2, minor)
    if pad:
        body += b'\x00' * pad
    raw = bytes(body)
    if truncate:
        raw = raw[:truncate]
    return raw


def mk_receipt(pin, rows, handler, outdir, chunk_dir='firmware.bin_extract',
               operation='extract_firmware', provider='unblob', gaps=(),
               unpub=(), diags=(), extra_files=(), derivations=None,
               coverage='complete', depth_limited=None):
    """A receipt-shaped REA envelope (`data` object) for a fixture carrier."""
    link_base = '%s/rea-firmware-fixture/extracted/%s' % (
        os.path.dirname(outdir.rstrip('/')), chunk_dir)
    files = []
    published_bytes = 0
    for rel, sha, size in list(rows) + list(extra_files):
        published_bytes += size
        files.append({'relative_path': '%s/%s' % (chunk_dir, rel),
                      'path': '%s/%s/%s' % (outdir, chunk_dir, rel),
                      'size': size, 'sha256': sha, 'reported_sha256': sha,
                      'mime_type': 'text/plain'})
    gaps_out = [{'kind': kind, 'input_path': '$output/%s/%s' % (chunk_dir, rel),
                 'relative_path': '%s/%s' % (chunk_dir, rel) if rel else None,
                 'handler': handler, 'dependencies': list(deps),
                 'continuation_id': 'continuation-fixture'}
                for kind, rel, deps in gaps]
    unpub_out = [{'relative_path': '%s/%s' % (chunk_dir, rel), 'kind': kind,
                  'link_target': target} for rel, kind, target in unpub]
    diag_out = [{'input_path': '$output/' + chunk_dir,
                 'report': {'__typename__': typename, 'severity': 'WARNING',
                            'link': '%s/%s' % (link_base, rel),
                            'target': target}}
                for typename, rel, target in diags]
    if derivations is None:
        derivations = [{'parent_path': '$input',
                        'child_path': '$output/' + chunk_dir,
                        'provider_blob_id': 'p1', 'handler': handler,
                        'parent_file_range': {'offset': 0, 'length': 4096}}]
        derivations += [{'parent_path': '$output/' + chunk_dir,
                         'child_path': '$output/%s/%s' % (chunk_dir, rel),
                         'provider_blob_id': 'p1', 'handler': None,
                         'parent_file_range': None} for rel, _s, _z in rows]
    return {
        'analysis_profile': None, 'authority': 'shipped-artifact',
        'confidence': 'observed', 'environment': None,
        'evidence_id': 'ev_' + '0' * 64, 'evidence_links': [], 'limitations': [],
        'locations': [{'kind': 'file-offset-range', 'start': 0, 'end': 4096}],
        'normalized_result': {
            'chunks': [{'input_path': '$input', 'provider_id': 'p1',
                        'range': {'offset': 0, 'length': 4096},
                        'handler': handler, 'encrypted': False,
                        'root_file_range': {'offset': 0, 'length': 4096},
                        'extraction_failed': False}],
            'coverage': coverage,
            'depth_limited_paths': ([] if depth_limited is None
                                    else ['$output/' + chunk_dir]),
            'derivations': derivations,
            'diagnostics': diag_out,
            'engine': {'name': 'unblob', 'version': '26.6.4',
                       'executable_path': '/x/unblob',
                       'executable_sha256': '0' * 64,
                       'source_revision': None, 'worker_count': 1},
            'extraction_continuations': [],
            'extraction_gaps': gaps_out,
            'files': files,
            'output_directory': outdir,
            'published_bytes': published_bytes,
            'selection': {'offset': 0, 'length': 4096, 'sha256': pin},
            'unpublished_entries': unpub_out,
        },
        'operation': operation,
        'parameters': {'path': '/x/carrier.bin', 'output_directory': outdir,
                       'max_depth': 3, 'max_output_bytes': 268435456,
                       'max_output_files': 10000},
        'predicate_type': 'rea.analysis',
        'provider': {'id': provider, 'name': 'Unblob', 'version': '26.6.4'},
        'raw_result': {}, 'relationship_coverage': None,
        'subject': {'name': 'carrier.bin', 'digest': {'sha256': pin},
                    'local_path': '/x/carrier.bin', 'format': 'file',
                    'architecture': None},
    }


def rehost(env, tag, chunk_dir='firmware.bin_extract'):
    """Copy of a receipt as a *second* run of the same bytes would emit it."""
    e = json.loads(json.dumps(env))
    root = '/fast/scratch/hyaku/kaidoku-r49/counter/rerun/%s' % tag
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
    tails = []
    for d in nr.get('diagnostics') or []:
        report = d.get('report')
        if isinstance(report, dict) and isinstance(report.get('link'), str):
            tails.append(diagnostic_rel({'report': {'link': report['link']}},
                                        old_root, old_out))
        else:
            tails.append(None)
    for f in nr.get('files') or []:
        rel = f.get('relative_path')
        p = strip_output(rel)
        if old_root and isinstance(p, str):
            if p == old_root:
                p = chunk_dir
            elif under_root(p, old_root):
                p = chunk_dir + p[len(old_root):]
            else:
                p = rel
            f['relative_path'] = p
            f['path'] = '%s/%s' % (outdir, p)
    for g in nr.get('extraction_gaps') or []:
        if g.get('relative_path') is None:
            g['input_path'] = '$output/' + chunk_dir
        else:
            g['relative_path'] = chunk_dir + '/' + extract_rel(
                g.get('relative_path'), old_root) if old_root else g.get('relative_path')
            g['input_path'] = '$output/' + g['relative_path']
        g['continuation_id'] = 'continuation-' + tag
    for u in nr.get('unpublished_entries') or []:
        rel = strip_output(u.get('relative_path'))
        if old_root and isinstance(rel, str) and under_root(rel, old_root):
            u['relative_path'] = chunk_dir + rel[len(old_root):]
    for deriv in nr.get('derivations') or []:
        for key in ('parent_path', 'child_path'):
            v = strip_output(deriv.get(key))
            if isinstance(v, str) and v and v != '$input':
                if old_root and under_root(v, old_root):
                    deriv[key] = '$output/' + chunk_dir + v[len(old_root):]
                else:
                    deriv[key] = '$output/' + v
    nr['output_directory'] = outdir
    nr['depth_limited_paths'] = ['$output/' + chunk_dir] if nr.get('depth_limited_paths') \
        else []
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
    node = which_fixed('node')
    r = subprocess.run([node, xpin_path, '--pkg65', pkg65, '--pkg67', pkg65]
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


def _province(row=True, heading=CORE_HEADING,
              text='`squashfs_v1` and `squashfs_v2` (SquashFS v1/v2, both byte '
                   'orders)', note=True, cited=ENTRY, stem=None,
              section_text='## Next'):
    r = ('| %s | x | y | `%s` |\n' % (text, cited)) if row else ''
    fn = (f'- {FRONTIER_MARK}, 2026-10-28: the `SquashFS v1/v2` clause is '
          f'superseded by `{stem or STEM}`.\n') if note else ''
    return (f'# P\n\n{heading}\n\n| Surface | Ports | Probe | Verified evidence |\n'
            f'|---|---|---|---|\n{r}\n{section_text}\n{fn}\n')


def _entry(sid_a='S138', sid_b='S139'):
    return f'# E\n\nsource: {sid_a} - x\nsource: {sid_b} - y\n'


def _registry(opened=OPENED, used=ENTRY, drop=()):
    rows = ''
    for sid in ('S135', 'S138', 'S139'):
        if sid in drop:
            continue
        rows += (f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | '
                 f'{used} |\n')
    return ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | '
            'teaches | status | opened | recheck | used-by |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|\n' + rows)


def _readme(stem=STEM):
    return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'


def selftest(pkg65):
    """Offline, deterministic --selftest over a git fixture lane."""
    here = os.path.dirname(os.path.abspath(__file__))
    sroot = scratch_root()
    xpin_path = find_xpin(here)
    xpin = open(xpin_path, 'rb').read()
    pkg65 = pkg65 or find_rea_pkg()
    if not pkg65:
        raise SystemExit('selftest needs --pkg65 (a rea-agents 6.5.0 package root)')
    node = which_fixed('node')
    if node is None:
        raise SystemExit('selftest needs node on the fixed PATH %r' % (FIXED_PATH,))
    work = tempfile.mkdtemp(prefix='c1-selftest-work.', dir=sroot)
    sha = lambda b: hashlib.sha256(b).hexdigest()
    ids = list(EXPECTED_IDS)

    # synthetic v1/v2 carriers: v1 le/be and v2 le/be, each with one metadata
    # block whose chain lands on the directory table (the probe's witness)
    carriers = {
        'v1le': sb_v12(1, 'le'),
        'v1be': sb_v12(1, 'be'),
        'v2le': sb_v12(2, 'le'),
        'v2be': sb_v12(2, 'be'),
    }
    handlers = {k: HANDLER_BY_MAJOR[int(k[1])] for k in ids}
    endians = {k: ('le' if k.endswith('le') else 'be') for k in ids}
    majors = {k: int(k[1]) for k in ids}
    pins = {k: sha(v) for k, v in carriers.items()}
    fsha = lambda i: sha(('f%s' % i).encode())
    members = {
        'v1le': [('apple.txt', fsha(1), 6), ('banana.txt', fsha(2), 7),
                 ('cherry.txt', fsha(3), 7)],
        'v1be': [('apple.txt', fsha(1), 6), ('banana.txt', fsha(2), 7),
                 ('cherry.txt', fsha(3), 7)],
        'v2le': [('apple1.txt', fsha(4), 7), ('apple2.txt', fsha(5), 7),
                 ('apple3.txt', fsha(6), 7), ('apple4.txt', fsha(7), 7)],
        'v2be': [('apple1.txt', fsha(4), 7), ('apple2.txt', fsha(5), 7),
                 ('apple3.txt', fsha(6), 7), ('apple4.txt', fsha(7), 7)],
    }
    nonreg = {k: [] for k in ids}

    def tree_root(k):
        return ('corpus/evidence/round-44/oracle/selftest/%s_extract' % k)

    def tree_digest(mem):
        return sha(''.join('%s\t%s\n' % (p, h)
                           for p, h, _s in sorted(mem, key=lambda m: m[0].encode())).encode())

    def tree_files(k):
        return {'%s/%s' % (tree_root(k), p): ('blob-%s-%s' % (k, p)).encode()
                for p, _h, _s in members[k]}

    # the fixture bodies are synthetic; make the tree blobs hash to the census
    # rows by writing the row's digest as the member content placeholder is not
    # possible, so the census rows are derived FROM the tree blobs instead.
    def blob(k, p):
        return ('blob-%s-%s' % (k, p)).encode()

    members = {k: [(p, sha(blob(k, p)), len(blob(k, p)))
                   for p, _h, _s in members[k]] for k in ids}
    spec_data = {k: dict(files=members[k]) for k in ids}

    def receipt_envs(over=None):
        out = {}
        for k in ids:
            out[k] = mk_receipt(pins[k], spec_data[k]['files'], handlers[k],
                                '/fast/scratch/hyaku/kaidoku-r49/selftest/%s' % k)
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
    DEFAULT_PRIOR = json.dumps({'rounds': [38, 39, 40, 41, 42, 43],
                                'pins': [{'sha256': 'f' * 64,
                                          'source': 'prior', 'id': 'OTHER'}]}, indent=1)

    def spec_json(pin_map=None, carrier_map=None, drop=(), target=TARGET,
                  oracle_over=None, tree_over=None, handler_over=None,
                  major_over=None, id_over=None, prior_pins=None,
                  projection=None, layout_block=None):
        pm = pin_map or pins
        cm = carrier_map or carriers
        cs = []
        for k in ids:
            if k in drop:
                continue
            rows = (oracle_over or {}).get(k, spec_data[k]['files'])
            cs.append({
                'id': (id_over or {}).get(k, k),
                'handler': (handler_over or {}).get(k, handlers[k]),
                'endian': endians[k],
                's_major': (major_over or {}).get(k, majors[k]),
                's_minor': 0,
                'compression': 'gzip',
                'sha256': pm[k],
                'size': len(cm[k]),
                'path': 'corpus/evidence/round-44/carriers/%s.bin' % k,
                'expected_regular': len(rows),
                'oracle': {
                    'tool': '/usr/bin/unsquashfs',
                    'version': '4.7.5',
                    'members': [{'path': p, 'sha256': h, 'size': s}
                                for p, h, s in rows],
                    'nonregular': list(nonreg[k]),
                },
                'output_tree': {
                    'root': tree_root(k),
                    'digest': (tree_over or {}).get(k, tree_digest(rows)),
                    'digest_rule': TREE_DIGEST_RULE,
                },
            })
        spec = {'claim': 'R49-C1', 'target': target, 'carriers': cs}
        if prior_pins is not None:
            spec['prior_pins'] = list(prior_pins)
        if projection is not None:
            spec['projection'] = projection
        if layout_block is not None:
            spec['superblock_layout'] = layout_block
        return json.dumps(spec, indent=1)

    def spec_plants(spec_text):
        """Repo files the frozen table names: carriers.json + carrier bytes."""
        doc = json.loads(spec_text)
        out = {}
        for c in doc['carriers']:
            k = c['id']
            if k in carriers:
                out[c['path']] = carriers[k]
            out[c['output_tree']['root']] = None
        return out

    def frozen_files(blob_over=None, spec_text=None, carrier_plant=True, **over):
        bm = dict(carriers)
        bm.update(blob_over or {})
        spec = spec_text if spec_text is not None else spec_json(
            carrier_map=bm, pin_map={k: sha(bm[k]) for k in ids})
        f = {
            XPIN: xpin,
            CARRIERS: spec,
            'plans/round-49-claims.md': b'# plan\n',
            'tools/round-49/c1-counter.py': open(os.path.abspath(__file__), 'rb').read(),
            'tools/round-49/rea-pkg.json': json.dumps(REA_PKG_DOC, indent=1).encode(),
            'tools/round-49/prior-pins.json': DEFAULT_PRIOR.encode(),
            'PROVINCE.md': _province(),
            ENTRY: _entry(),
            'corpus/SOURCES.md': _registry(),
            'corpus/README.md': _readme(),
        }
        if carrier_plant:
            for k in ids:
                f['corpus/evidence/round-44/carriers/%s.bin' % k] = bm[k]
            for k in ids:
                for p, content in tree_files(k).items():
                    f[p] = content
        f.update(over)
        return f

    def build(blob_over=None, env_over=None, receipt_over=None, spec_text=None,
              spec_over=None):
        bm = dict(carriers)
        bm.update(blob_over or {})
        pm = {k: sha(bm[k]) for k in ids}
        spec = spec_text
        if spec is None:
            kw = dict((spec_over or {}).get('kwargs', {}))
            kw['oracle_over'] = (spec_over or {}).get('oracle')
            spec = spec_json(carrier_map=bm, pin_map=pm, **kw)
        envs = receipt_envs(over=env_over)
        for k, i in mint_many(work, xpin_path, pkg65, envs).items():
            envs[k]['evidence_id'] = i
        r = receipts(envs)
        for p, content in (receipt_over or {}).items():
            if content is None:
                r.pop(p, None)
            else:
                r[p] = content
        return frozen_files(blob_over=bm, spec_text=spec), r

    def mutant(k, fn, remint=True):
        e = json.loads(json.dumps(green_envs[k]))
        fn(e)
        if remint:
            e['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': e})['m']
        envs = dict(green_envs)
        envs[k] = e
        return receipts(envs)

    sim_envs = receipt_envs()

    def sim_runner(carrier_bytes, cid, params=None):
        """What a real run of these bytes would emit, modelled from the fixture."""
        pin = sha(carrier_bytes)
        base = sim_envs.get(cid)
        if base is None:
            return 'no_data', {'ok': False, 'exit': 1, 'reason': 'no fixture run'}
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

    add('green (four v1/v2 carriers, receipts, docs)', [green_frozen, green_receipts],
        0, 0)
    add('do-nothing (frozen table only)', [frozen], 0, 1,
        want_fail='v1le:receipt_present')
    add('receipt missing (v2be)',
        [frozen, {k: v for k, v in good.items() if '/v2be/' not in k}], 0, 1,
        want_fail='v2be:receipt_present')

    # (ii) a v3 receipt fed to a v1 carrier: the handler binding is exact
    def v3_handler(e):
        for c in e['normalized_result']['chunks']:
            c['handler'] = 'squashfs_v3'
        for d in e['normalized_result']['derivations']:
            if d.get('handler') is not None:
                d['handler'] = 'squashfs_v3'

    add('v3 receipt fed to a v1 carrier',
        [frozen, mutant('v1le', v3_handler)], 0, 1, want_fail='v1le:handler_ok')
    add('v2 receipt fed to a v1 carrier (family mismatch)',
        [frozen, mutant('v1le', lambda e: [c.__setitem__('handler', 'squashfs_v2')
                                           for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='v1le:handler_ok')

    # (iii) a fabricated oracle-only envelope: files copied from the oracle, but
    # not what a real run of the bytes projects (the rerun is the witness)
    fabricate = mk_receipt(pins['v1be'], spec_data['v1be']['files'], handlers['v1be'],
                           '/fast/scratch/hyaku/kaidoku-r49/selftest/v1be')
    fabricate['normalized_result']['published_bytes'] += 1
    fabricate['evidence_id'] = mint_many(work, xpin_path, pkg65, {'m': fabricate})['m']
    envs = dict(green_envs)
    envs['v1be'] = fabricate
    add('fabricated oracle-only envelope (rerun projection mismatch)',
        [frozen, receipts(envs)], 0, 1, want_fail='v1be:projection_ok')
    add('rerun yields no evidence object',
        [frozen, good], 0, 1, want_fail='v1le:projection_ok', runner=boom_runner)
    add('rerun environment error is unevaluable', [frozen, good], 0, 2,
        'rerun_env_error', runner=env_boom_runner)

    # superblock / layout controls
    add('v2 nonstandard magic (zlqs) under a squashfs_v2 binding',
        list(build(blob_over={'v2le': sb_v12(2, 'le', magic=b'zlqs')})), 0, 1,
        want_fail='v2le:layout_ok')
    add('truncated superblock (shorter than 32 bytes)',
        list(build(blob_over={'v1le': sb_v12(1, 'le', truncate=24)})), 0, 1,
        want_fail='v1le:layout_ok')
    add('bytes_used beyond the file',
        list(build(blob_over={'v2be': sb_v12(2, 'be', bytes_used=0xFFFFFFF0)})), 0, 1,
        want_fail='v2be:layout_ok')
    add('s_major contradicts the frozen handler',
        list(build(spec_over={'kwargs': {'major_over': {'v1le': 2}}})), 0, 1,
        want_fail='v1le:layout_ok')
    add('metadata block stored uncompressed leaves compression undetermined',
        list(build(blob_over={'v1be': sb_v12(1, 'be', meta_uncompressed=True)})), 0, 1,
        want_fail='v1be:layout_ok')
    add('metadata length that does not land on the directory table',
        list(build(blob_over={'v2le': sb_v12(2, 'le', meta_len=3)})), 0, 1,
        want_fail='v2le:layout_ok')
    add('big-endian magic on a little-endian frozen carrier',
        list(build(blob_over={'v1le': sb_v12(1, 'be')})), 0, 1,
        want_fail='v1le:layout_ok')
    add('carrier padded past its chunk end (sloppy carve)',
        list(build(blob_over={'v2le': sb_v12(2, 'le', pad=64)})), 0, 1,
        want_fail='v2le:carve_ok')

    # oracle / tree controls
    flipped = dict(spec_data['v1le'])
    add('oracle census row sha flipped in the frozen table',
        list(build(spec_over={'oracle': {'v1le': [('apple.txt', 'a' * 64, 6)]}})), 0, 1,
        want_fail='v1le:oracle_hits_ok')
    add('receipt publishes a regular file the census does not list',
        [frozen, mutant('v2be', lambda e: e['normalized_result']['files'].append(
            {'relative_path': 'firmware.bin_extract/extra.txt',
             'path': '/x/extra.txt', 'size': 1, 'sha256': 'd' * 64}))], 0, 1,
        want_fail='v2be:oracle_hits_ok')
    add('symlink census row published as a regular file',
        [frozen, mutant('v2le', lambda e: e['normalized_result']['files'].append(
            {'relative_path': 'firmware.bin_extract/bin/link',
             'path': '/x/bin/link', 'size': 3, 'sha256': 'e' * 64}))], 0, 1,
        want_fail='v2le:oracle_hits_ok')
    add('committed output_tree digest does not match the frozen value',
        list(build(spec_over={'kwargs': {'tree_over': {'v1be': '0' * 64}}})), 0, 1,
        want_fail='v1be:tree_ok')

    # gaps: the wave-1 amendment freezes zero gaps
    add('a depth-limited gap is a divergence (zero-gap rule)',
        [frozen, mutant('v1le', lambda e: e['normalized_result']['extraction_gaps']
                        .append({'kind': 'depth-limited', 'input_path': '$output/'
                                 'firmware.bin_extract', 'relative_path': None,
                                 'handler': None, 'dependencies': [],
                                 'continuation_id': 'c'}))], 0, 1,
        want_fail='v1le:gaps_ok')
    add('missing-extractor-dependency gap (sasquatch stripped)',
        [frozen, mutant('v1be', lambda e: e['normalized_result']['extraction_gaps']
                        .append({'kind': 'missing-extractor-dependency',
                                 'input_path': '$output/firmware.bin_extract',
                                 'relative_path': None, 'handler': None,
                                 'dependencies': ['sasquatch'],
                                 'continuation_id': 'c'}))], 0, 1,
        want_fail='v1be:gaps_ok')

    # path rules
    add('receipt path climbing out of the run (.. provenance)',
        [frozen, mutant('v2le', lambda e: e['parameters'].__setitem__(
            'output_directory',
            '/fast/scratch/hyaku/kaidoku-r49/../kaidoku-r42/x'))], 0, 1,
        want_fail='v2le:run_provenance_ok')
    add('provenance of another round (/kaidoku-r42/)',
        [frozen, mutant('v2be', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r42/x'))], 0, 1,
        want_fail='v2be:run_provenance_ok')
    add('published file with a trailing slash',
        [frozen, mutant('v1le', lambda e: e['normalized_result']['files'][0]
                        .__setitem__('relative_path',
                                     e['normalized_result']['files'][0]['relative_path']
                                     + '/'))], 0, 1, want_fail='v1le:path_shape_ok')
    add('a path under x_extract2 cannot publish a row of root x_extract',
        [frozen, mutant('v1be', lambda e: (
            e['normalized_result']['derivations'].__setitem__(
                0, {'parent_path': '$input', 'child_path': '$output/x_extract',
                    'handler': handlers['v1be'], 'provider_blob_id': 'p1',
                    'parent_file_range': {'offset': 0, 'length': 4096}}),
            e['normalized_result']['files'].__setitem__(
                0, {'relative_path': 'x_extract2/apple.txt', 'path': '/x/apple.txt',
                    'size': 6, 'sha256': spec_data['v1be']['files'][0][1]})))],
        0, 1, want_fail='v1be:oracle_hits_ok')

    # receipt identity / freshness / envelope
    add('receipt added at the freeze is not fresh',
        [{**frozen, **good}], 0, 1, want_fail='v1le:receipt_fresh')
    add('score receipt relabelled as REA evidence',
        [frozen, mutant('v2be', lambda e: e.__setitem__('counter_sha256', '0' * 64))],
        0, 1, want_fail='v2be:evidence_envelope_ok')
    add('stale evidence id after an edit',
        [frozen, mutant('v2le', lambda e: e['normalized_result']['files'].append(
            {'relative_path': 'firmware.bin_extract/late.txt',
             'path': '/x/late.txt', 'size': 1, 'sha256': 'f' * 64}), remint=False)],
        0, 1, want_fail='v2le:evidence_id_ok')
    add('subject digest names another carrier',
        [frozen, mutant('v1le', lambda e: e['subject']['digest'].__setitem__(
            'sha256', '2' * 64))], 0, 1, want_fail='v1le:subject_pin_ok')

    # frozen-table controls
    add('carriers.json names a fifth (v2.1) carrier',
        [{**frozen, CARRIERS: spec_json(id_over={'v2be': 'v21be'})}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    add('carriers.json drops a preregistered carrier',
        [{**frozen, CARRIERS: spec_json(drop=('v2be',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
    add('carrier handler disagrees with s_major',
        [{**frozen, CARRIERS: spec_json(handler_over={'v1le': 'squashfs_v2'})}, good],
        0, 1, want_fail='b:carriers_spec_ok')
    one_end = {k: sb_v12(majors[k], 'le') for k in ids}
    le_spec = spec_json(carrier_map=one_end, pin_map={k: sha(one_end[k]) for k in ids},
                        **{}) 
    le_spec_doc = json.loads(le_spec)
    for c in le_spec_doc['carriers']:
        c['endian'] = 'le'
    add('all carriers little-endian (endianness coverage)',
        [frozen_files(blob_over=one_end, spec_text=json.dumps(le_spec_doc)),
         receipts(green_envs)], 0, 1, want_fail='b:endianness_coverage')

    # freeze integrity
    add('carriers.json changed after the freeze',
        [frozen, {**good, CARRIERS: spec_json(drop=('v2be',))}], 0, 2,
        'frozen_path_changed')
    add('carrier bytes changed after the freeze',
        [frozen, {**good, 'corpus/evidence/round-44/carriers/v1le.bin': b'x' * 10}],
        0, 2, 'frozen_path_changed')
    add('committed oracle tree edited after the freeze',
        [frozen, {**good, tree_root('v1be') + '/apple.txt': b'edited'}], 0, 2,
        'frozen_path_changed')
    add('frozen path touched then restored',
        [frozen, {**good, 'plans/round-49-claims.md': b'# edited\n'},
         {**good, 'plans/round-49-claims.md': b'# plan\n'}], 0, 2,
        'frozen_path_changed')

    # documentation bindings
    add('province has no Round-49 Core section',
        [{**frozen, 'PROVINCE.md': '# P\n\n## Next\n- x\n'}, good], 0, 1,
        want_fail='b:province_core_section')
    add('province row names only squashfs_v1',
        [{**frozen, 'PROVINCE.md': _province(text='`squashfs_v1` (v1 only)')}, good],
        0, 1, want_fail='b:province_core_row')
    add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': _province(
            cited='corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md')}, good],
        0, 1, want_fail='b:province_core_row')
    add('frontier note absent', [{**frozen, 'PROVINCE.md': _province(note=False)}, good],
        0, 1, want_fail='b:frontier_note')
    add('entry absent', [{**frozen, ENTRY: None}, good], 0, 1,
        want_fail='b:entry_present')
    add('entry cites only one S-id', [{**frozen, ENTRY: _entry(sid_b='S137')}, good],
        0, 1, want_fail='b:sourced')
    add('S139 row opened earlier',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-27')}, good], 0, 1,
        want_fail='b:sourced')
    add('S138 row missing', [{**frozen, 'corpus/SOURCES.md': _registry(drop=('S138',))},
                             good], 0, 1, want_fail='b:sourced')
    add('coverage map lacks the stem',
        [{**frozen, 'corpus/README.md': _readme(stem='2026-10-28-r49-other')}, good],
        0, 1, want_fail='b:coverage_map_row')

    receipt_probes = []

    def probe_receipt(desc, doc, want_ok, want_text=None):
        ok, why = receipt_identity_ok(doc)
        receipt_probes.append({'desc': desc, 'ok': ok, 'why': why,
                               'want_ok': want_ok, 'want_text': want_text})

    stamp_path = os.path.join(work, 'receipt-identity-probe.json')
    _s, _ok, _why = write_receipt({'selftest': 'identity'}, stamp_path)
    written = json.load(open(stamp_path))
    probe_receipt('receipt this counter wrote', written, True)
    for name, doc, text in (
            ('without counter_sha256', dict(written, **{'counter_sha256': None}),
             'counter_sha256 is null'),
            ('whose counter_sha256 names other bytes',
             dict(written, **{'counter_sha256': '0' * 64}), 'does not describe'),
            ('with a truncated counter_sha256',
             dict(written, **{'counter_sha256': 'abc'}), '64 hex')):
        probe_receipt(name, doc, False, text)
    no_key = dict(written)
    no_key.pop('counter_sha256')
    probe_receipt('without counter_sha256 key', no_key, False, 'missing counter_sha256')

    prefix_probes = [
        ('root itself', 'x_extract', 'x_extract', True),
        ('segment-bounded child', 'x_extract/var/info.txt', 'x_extract', True),
        ('$output sigil', '$output/x_extract/var/info.txt', 'x_extract', True),
        ('non-segment-bounded root (x_extract2)', 'x_extract2/var/info.txt',
         'x_extract', False),
        ('suffix is not containment', 'other/x_extract/var', 'x_extract', False),
        ('empty path', '', 'x_extract', False),
    ]

    fails = []
    green = red = 0
    prefix_results = []
    for desc, path, root, want in prefix_probes:
        got = under_root(path, root)
        prefix_results.append({'desc': desc, 'path': path, 'root': root,
                               'segment_bounded': got,
                               'naive_startswith': path.startswith(root),
                               'want': want})
        if got != want:
            fails.append('prefix probe %r: under_root %r, want %r' % (desc, got, want))
    for p in receipt_probes:
        if p['ok'] != p['want_ok']:
            fails.append('receipt probe %r: ok=%r want %r (%s)'
                         % (p['desc'], p['ok'], p['want_ok'], p['why']))
        elif p['want_text'] and p['want_text'] not in (p['why'] or ''):
            fails.append('receipt probe %r: reason %r lacks %r'
                         % (p['desc'], p['why'], p['want_text']))
    if not _ok:
        fails.append('stamped receipt failed its own identity check: %s' % _why)

    def runner_for(case, steps):
        return case['runner']

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
                    failing |= {'%s:%s' % (k, x) for x in CLAUSES
                                if v.get(x) is not True}
                failing |= {'b:' + x for x in BINDINGS
                            if res['bindings'][x] is not True}
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
                    detail = {'exit': got,
                              'carriers_matched': res['carriers_matched'],
                              'failing': sorted(failing),
                              'bindings_false': sorted(x for x in BINDINGS
                                                       if res['bindings'][x] is not True),
                              'drift': res['frozen_path_changed']}
                print('DETAIL\t%s\t%s' % (c['name'], json.dumps(detail)),
                      file=sys.stderr)
            ok = got == c['want'] and (c['reason'] is None or why == c['reason'])
            if ok and c['want_fail'] and c['want_fail'] not in failing:
                ok = False
                fails.append('%s: want failing %r, failing=%r'
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
                      'receipt_probes': len(receipt_probes),
                      'prefix_probes': len(prefix_results),
                      'probe_results': prefix_results + receipt_probes,
                      'failures': fails}, sort_keys=True))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
