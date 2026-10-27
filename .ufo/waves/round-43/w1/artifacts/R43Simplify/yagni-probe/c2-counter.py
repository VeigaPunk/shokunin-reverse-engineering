#!/usr/bin/env python3
"""R42-C2 counter (depth: SquashFS extract-firmware outcome-triage table v4,
scored against labels written independently of the table).

Predicate P42-C2 (plans/round-42-claims.md, `## R42-C2`), as the draft binds it:

  At the measured revision the frozen v4 interpreter
  `tools/round-42/sqfs-triage-v4.py` — materialised from the FREEZE commit —
  reading `SKILL.md` at the measured revision and therefore only the
  `<!-- sqfs-triage-table v4 -->` rule block, gives every held-out envelope the
  (label, action) pair that the frozen INDEPENDENT evaluator
  `tools/round-42/indep-eval-v4.py` gives it; the held-out set is
  `tools/round-42/heldout-gen-v4.py --seed <FREEZE>`; every envelope's observed
  feature tuple equals the tuple its manifest declares under exactly ONE key,
  `declared_features`; the frozen lookup control
  `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` scores strictly fewer
  than half of the held-out `combo` envelopes; the round-41 C1 receipts and the
  round-42 legacy dev envelopes get the evaluator's pair; the seed is the freeze
  commit hash; every carrier regenerates byte-identically from that seed; every
  envelope's subject digest equals its carrier's sha256; the held-out manifest
  is first added in a commit descending from the freeze and no later than its
  envelopes; and the v4 block bytes at the measured revision equal the freeze
  bytes.

Round-42 changes from the round-41 C2 counter
  R41-CL1  the declared tuple is read from `carriers[].declared_features` and
           from nowhere else.  Any other key (`declared`, `features`,
           `class_expected.features`, a manifest-level map) is INVISIBLE, and a
           carrier without the key fails the binding closed and is listed.
  R41-CL4  new binding `legacy_chunks_not_no_squashfs`: no envelope whose
           declared handler set holds a v1-v3 chunk may be labelled
           `no-squashfs-chunk` by either side, and the table's
           `no-squashfs-chunk` row must carry handler `none`.
  new      `new_legacy_label_exercised` (the legacy-failure row exists in the
           table AND an envelope receives it), `handler_families_exercised`
           (v1, v2, v3 and a v4 family appear among the class envelopes),
           `lookup_combo_below_half`, `lookup_control_identical`,
           `legacy_dev_envelopes`.
  A1       the amended precedence (plans/round-42-claims.md, 15 steps) adds
           `container-depth-limited` (F empty AND depth-limited in G, decided
           before no-squashfs-chunk) and `unknown-residue`
           (unknown-chunk-handler in G, decided before depth-limited); H unions
           chunk and gap handlers, HF is the extractor-failure gaps' handlers,
           and the dependency step is a membership rule.  New binding
           `combo_unseen_majority`; CTL-C2-7b (lookup + majority fallback) is
           scored and REPORTED, never bound.
  D4       the receipt carries `counter_sha256` (at REV) and
           `counter_sha256_at_freeze`, plus its own `exit_code`.

Freeze integrity (carried from rounds 39-41)
  A score at REV is admissible only if no commit in FREEZE..REV touches a
  frozen path; a later restore does not un-block (exit 2
  `frozen_path_changed`).  Frozen: the claims file, `tools/round-42` (whole
  subtree), the held-out evidence subtree, the lookup control file, the writers
  the frozen generator names, the fixture files the manifest pins inside the
  lane, and the SKILL v4 block region checked at EVERY commit in FREEZE..REV
  that touches SKILL.md.

Usage
  c2-counter.py --root LANE --rev REV --freeze FREEZE [--json-out PATH]
  c2-counter.py --selftest
Exit
  0  target met (`met_target` true)
  1  not met (a pair miss or a binding false); the receipt is still written
  2  unevaluable: `frozen_path_changed`, `freeze_not_ancestor_of_rev`,
     `unknown_revision`, `no_manifest_at_rev`, `manifest_unparsable`,
     `manifest_not_an_object`, `generator_absent_at_freeze`,
     `generator_failed`, `generator_wrote_no_manifest`,
     `regenerated_manifest_unparsable`, `evaluator_absent_at_freeze`,
     `evaluator_failed`, `evaluator_output_unparsable`,
     `interpreter_absent_at_freeze`, `interpreter_failed`,
     `met_target_inconsistent`

Frozen tool interfaces this counter relies on (probed, not assumed)
  interpreter `python3 -I -B sqfs-triage-v4.py --skill SKILL.md [--json]
              [--table-only] [--envelopes DIR] ENV...`
              -> `{"results": [{path, label, action, row|rule, cells|row}]}`,
              else `path<TAB>label<TAB>action[<TAB>row]`
  evaluator   `python3 -I -B indep-eval-v4.py --envelopes DIR [--out FILE]
              [--json] [--format json]` (also `--json-out FILE`), and the
              shapes `{"labels": {...}}`, `{"results": [...]}`, a bare list and
              a bare map are all accepted
  generator   `python3 -I -B heldout-gen-v4.py --seed FREEZE --out DIR`
              -> `manifest.json` with `classes`, `carriers[]` {id, class, arm,
              carrier, sha256, envelope, declared_features}
  Every attempt's exit code and the interface that answered are recorded
  (`interpreter_interface`, `evaluator_interface`, `interface_attempts`,
  `real_receipts.attempts`, `lookup.attempts`).

Reads git objects only (`show`/`log`/`ls-tree`/`merge-base`/`rev-parse`/
`cat-file`); everything is materialised into a private scratch directory under
$HYAKU_SCRATCH/kaidoku-r42 (or $TMPDIR) and removed at exit.
"""
import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

# ------------------------------------------------------------------ claim paths
MANIFEST = 'corpus/evidence/round-42/c2/heldout/manifest.json'
MANIFEST_DIR = MANIFEST.rsplit('/', 1)[0]
SKILL = 'SKILL.md'
CLAIMS = 'plans/round-42-claims.md'
EVAL = 'tools/round-42/indep-eval-v4.py'
INTERP = 'tools/round-42/sqfs-triage-v4.py'
GEN = 'tools/round-42/heldout-gen-v4.py'
COUNTER = 'tools/round-42/c2-counter.py'
LOOKUP = '.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md'
FIXTURES_DIR = 'corpus/evidence/round-42/c2/fixtures'

FROZEN_PATHS = (CLAIMS, 'tools/round-42', MANIFEST_DIR, LOOKUP, FIXTURES_DIR)
WRITER_CANDIDATES = ('tools/round-41/gen-squashfs.py',
                     'tools/round-40/gen-squashfs.py',
                     'tools/round-39/gen-squashfs.py')
GEN_TREE_PREFIXES = ('tools/round-42', 'tools/round-41', 'tools/round-40',
                     'tools/round-39',
                     # L1 freeze amendment (QUALITY 84 dry run: generator_failed, the
                     # committed fixture copies were never materialised for the regen)
                     'corpus/evidence/round-42/c2/fixtures')
WRITER_ENV = 'KAIDOKU_GEN_SQUASHFS'
FIXTURE_ENV = 'KAIDOKU_FIXTURES'

MARKER_V4 = '<!-- sqfs-triage-table v4 -->'
MARKER_V3 = '<!-- sqfs-triage-table v3 -->'
ACTIONS_RE = re.compile(r'<!--\s*sqfs-triage-actions:\s*(.*?)\s*-->')
CRAFT = '## Queue-drain craft'

# The v4 table keeps the round-41 twelve columns; the ten below are the ones
# without which the interpreter cannot decide anything (cause/source are prose).
COLUMNS = ('label', 'operation', 'provider', 'handler', 'failing handler',
           'gap kinds', 'dependencies', '-be in child argv', 'symlink removed',
           'published files', 'action')

# R41-CL1: exactly one declared-tuple key, read from nowhere else.
DECLARED_KEY = 'declared_features'
COMBO_CLASS = 'combo'
COMBO_MIN = 12

# The round-41 C1 receipts (real AVM v4 BE rootfs envelopes) and the round-42
# dev arm (real legacy-family envelopes).  The dev directory is the first of
# these that exists at REV with at least one `<id>/envelope.json`.
REAL_RECEIPTS = ('corpus/evidence/round-41/c1/V3/after.json',
                 'corpus/evidence/round-41/c1/V4/after.json',
                 'corpus/evidence/round-41/c1/L3/after.json',
                 'corpus/evidence/round-41/c1/L4/after.json')
REAL_LABEL = 'depth-limited'
DEV_DIRS = ('corpus/evidence/round-42/c2/dev',
            '.ufo/waves/round-42/controls/c2/dev')
DEV_MIN = 4
LEGACY_HANDLER_PREFIXES = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3')

# (H, G, D, BE, SR, P) as the round-41 features, plus `extraction_failed`.
FEATURE_KEYS = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                'symlink_removed', 'published', 'extraction_failed')
REQUIRED_FEATURES = ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                     'symlink_removed', 'published')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
NOMATCH_PAIR = ('unclassified', 'none')

CLAIM_BINDINGS = (
    'seed_matches_freeze', 'manifest_generator_path',
    'generator_sha_matches_freeze', 'writer_matches_manifest',
    'regenerated_seed_matches_freeze', 'carriers_regenerated',
    'carriers_committed', 'envelopes_valid', 'manifest_after_freeze',
    'manifest_before_envelopes', 'v4_block_present', 'v4_block_identical',
    'evaluator_covers_all', 'observed_features_match_declared',
    'lookup_control_identical', 'combo_unseen_majority',
    'real_receipts_depth_limited', 'legacy_dev_envelopes',
)
INSTRUMENT_BINDINGS = (
    'classes_unique', 'classes_two_each', 'n_equals_twice_classes',
    'combo_family_wellformed', 'ids_unique', 'arms_valid',
    'carrier_paths_unique', 'envelope_paths_unique', 'v4_block_columns',
    'v4_actions_declared', 'observed_actions_declared', 'decisions_reported',
    'row_decisions_consistent', 'bindings_complete',
)


class Unevaluable(Exception):
    def __init__(self, reason, receipt=None):
        super().__init__(reason)
        self.reason = reason
        self.receipt = receipt or {}


# ------------------------------------------------------------------ git
def show(root, rev, path):
    """Blob bytes at `rev`, or None when absent/unreadable."""
    if not rev:
        return None
    p = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def present(root, rev, path):
    if not rev:
        return False
    return subprocess.run(['git', '-C', root, 'cat-file', '-e', '%s:%s'
                           % (rev, path)], capture_output=True).returncode == 0


def full_rev(root, rev):
    p = subprocess.run(['git', '-C', root, 'rev-parse', '--verify',
                        '%s^{commit}' % rev], capture_output=True, text=True)
    if p.returncode:
        raise Unevaluable('unknown_revision:%s' % rev)
    return p.stdout.strip()


def is_ancestor(root, a, b):
    if not a or not b:
        return False
    return subprocess.run(['git', '-C', root, 'merge-base', '--is-ancestor',
                           a, b], capture_output=True).returncode == 0


def first_add(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'log', '--format=%H',
                        '--diff-filter=A', '--no-renames', '--reverse', rev,
                        '--', path], capture_output=True, text=True)
    if p.returncode:
        return None
    lines = [l for l in p.stdout.split() if l]
    return lines[0] if lines else None


def commits_touching(root, rev, path):
    """Commits reachable from `rev` (a rev or a RANGE) that touched `path`."""
    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', '--no-renames',
                        rev, '--', path], capture_output=True, text=True)
    if p.returncode:
        return []
    return [l for l in p.stdout.split() if l]


def frozen_drift(root, freeze, rev, paths):
    """{path: [commit, ...]} for frozen paths MODIFIED in FREEZE..REV.

    A creation (`A`) is not a touch (the held-out evidence is necessarily first
    added after the freeze; its ordering is bound by `manifest_after_freeze`).
    A modification, deletion, rename or typechange is, and a later restore does
    not undo it.
    """
    out = {}
    rng = '%s..%s' % (freeze, rev)
    for p in paths:
        q = subprocess.run(['git', '-C', root, 'log', '--format=@@%H',
                            '--name-status', '--no-renames', rng, '--', p],
                           capture_output=True, text=True)
        cur = None
        hits = set()
        for line in q.stdout.splitlines():
            if line.startswith('@@'):
                cur = line[2:].strip()
                continue
            if not line.strip() or cur is None:
                continue
            st = line.split('\t')[0].strip()[:1]
            if st in ('M', 'D', 'R', 'T', 'U'):
                hits.add(cur)
        if hits:
            out[p] = sorted(hits)
    return out


# ------------------------------------------------------------------ skill block
def craft_span(text):
    """(lines, first, last) of the `## Queue-drain craft` section."""
    if text is None:
        return None
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.lower().startswith(CRAFT.lower())), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    return lines, start, end


def rule_block(text, marker):
    """The rule block a table marker owns: marker line -> next rule block."""
    span = craft_span(text)
    if span is None:
        return None
    lines, start, end = span
    mi = next((i for i in range(start + 1, end)
               if lines[i].strip().startswith(marker)), None)
    if mi is None:
        # An inline mention (a rule bullet quoting the marker) never starts a
        # block: only a line that is the marker, not a bullet or a heading.
        mi = next((i for i in range(start + 1, end) if marker in lines[i]
                   and not re.match(r'^\s*-\s+\*\*', lines[i])
                   and not lines[i].lstrip().startswith('#')), None)
    if mi is None:
        return None
    stop = end
    for i in range(mi + 1, end):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\s*-\s+\*\*', l) \
                or l.strip().startswith('<!-- sqfs-triage-table'):
            stop = i
            break
    block = '\n'.join(lines[mi:stop]).rstrip('\n')
    return block or None


def parse_rows(block):
    """(header cells lowercased, body rows) of a table block, or (None, [])."""
    if not block:
        return None, []
    rows = [[c.strip().strip('`').strip()
             for c in l.strip().strip('|').split('|')]
            for l in block.splitlines() if l.lstrip().startswith('|')]
    if len(rows) < 2:
        return None, []
    return [c.lower() for c in rows[0]], rows[2:]


def table_labels(block):
    header, rows = parse_rows(block)
    if not header or 'label' not in header:
        return []
    i = header.index('label')
    return [r[i] for r in rows if i < len(r)]


def declared_actions(block):
    if not block:
        return None
    m = ACTIONS_RE.search(block)
    if not m:
        return None
    toks = m.group(1).split()
    return [t.strip('`') for t in toks if t.strip('`')] or None


def columns_ok(block):
    header, _ = parse_rows(block)
    if not header:
        return False, []
    missing = [c for c in COLUMNS if c not in header]
    return (not missing), missing


def block_at(root, rev, path=SKILL, marker=MARKER_V4):
    return rule_block(as_text(show(root, rev, path)), marker)


def skill_block_drift(root, freeze, rev, freeze_block):
    """Commits in FREEZE..REV whose SKILL v4 block differs from the freeze's."""
    scanned = commits_touching(root, '%s..%s' % (freeze, rev), SKILL)
    bad = []
    for c in scanned:
        if block_at(root, c) != freeze_block:
            bad.append(c)
    return scanned, bad


# ------------------------------------------------------------------ writer scope
def writer_scope(root, freeze, gen_text, declared_path=None):
    """Frozen writer paths: the ones the frozen generator names or imports."""
    scope = {}
    for p in WRITER_CANDIDATES:
        hit = False
        why = []
        if gen_text:
            if p in gen_text:
                hit, why = True, why + ['path-literal']
            else:
                tag = p.split('/')[1].split('-')[1]
                m = re.search(r'(round[-_]?%s)[^\n]{0,120}gen[-_]squashfs' % tag,
                              gen_text)
                m2 = re.search(r'gen[-_]squashfs[^\n]{0,120}(round[-_]?%s)' % tag,
                               gen_text)
                if m or m2:
                    hit, why = True, why + ['import-shape']
        if declared_path and declared_path == p:
            hit, why = True, why + ['manifest-declared']
        if hit:
            has = present(root, freeze, p)
            scope[p] = {'why': why, 'present_at_freeze': has,
                        'sha256': sha256_bytes(show(root, freeze, p)) if has
                        else None}
    return scope


# ------------------------------------------------------------------ scratch
def scratch_root():
    base = os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
    root = os.path.join(base, 'kaidoku-r42')
    os.makedirs(root, exist_ok=True)
    return root


def scratch_dir():
    return tempfile.mkdtemp(prefix='c2-counter.', dir=scratch_root())


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


def as_text(b):
    return b.decode('utf-8', 'replace') if b is not None else None


# ------------------------------------------------------------------ envelopes
def envelope_data(obj):
    if isinstance(obj, dict) and 'subject' not in obj \
            and isinstance(obj.get('data'), dict):
        return obj['data']
    return obj


def subject_sha(obj):
    try:
        return str(obj['subject']['digest']['sha256']).lower()
    except Exception:
        return None


def norm_id(key):
    """Envelope id from an id, a path, or a file name."""
    if not isinstance(key, str):
        return None
    k = key.strip().replace('\\', '/').rstrip('/')
    k = k.rsplit('/', 1)[-1]
    if k.endswith('.json'):
        k = k[:-5]
    return k or None


# ------------------------------------------------------------------ features
def _as_list(value):
    return value if isinstance(value, list) else []


def _iter_dicts(obj):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def command_tokens(cmd):
    if isinstance(cmd, str):
        try:
            return shlex.split(cmd)
        except ValueError:
            return cmd.split()
    if isinstance(cmd, (list, tuple)):
        return [t for t in cmd if isinstance(t, str)]
    return None


def names_sasquatch(tokens):
    for token in tokens:
        if token.rsplit('/', 1)[-1].startswith('sasquatch'):
            return True
    return False


def extractor_commands(data):
    """Every recorded command that names a sasquatch binary, first-seen order."""
    commands = []

    def take(cmd):
        tokens = command_tokens(cmd)
        if tokens and names_sasquatch(tokens) and cmd not in commands:
            commands.append(cmd)

    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            report = diag.get('report') if isinstance(diag, dict) else None
            if isinstance(report, dict) and 'command' in report:
                take(report['command'])
    for found in _iter_dicts(data.get('raw_result')):
        if 'command' in found:
            take(found['command'])
    return commands


def _tokens(value):
    if isinstance(value, str):
        return sorted(t.strip() for t in re.split(r'[,+]', value)
                      if t.strip() and t.strip().lower() != 'none')
    if isinstance(value, (list, tuple, set)):
        return sorted(str(t) for t in value if str(t).strip())
    return []


def _tri(value, allow_na=True):
    """yes / no / n-a out of the shapes a manifest or an envelope may use."""
    if value is None:
        return 'n/a' if allow_na else 'no'
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ('yes', 'true', 'y', 'removed', '1'):
            return 'yes'
        if v in ('no', 'false', 'n', 'kept', '0'):
            return 'no'
        if v in ('n/a', 'na', 'n-a', 'none', '-', ''):
            return 'n/a' if allow_na else 'no'
    return 'n/a'


def _pub(value):
    """0 / >0 class out of an int, a bool or a manifest token."""
    if isinstance(value, bool):
        return 'nonzero' if value else 'zero'
    if isinstance(value, int):
        return 'nonzero' if value > 0 else 'zero'
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ('>0', 'nonzero', 'non-zero', 'some', 'positive', 'yes', 'true'):
            return 'nonzero'
        if v in ('0', 'zero', 'none', 'empty', 'no', 'false'):
            return 'zero'
    return 'zero'


def observed_features(data):
    """(H, G, D, BE, SR, P, extraction_failed) of one envelope.

    A1: H is the union of `chunks[].handler` and `extraction_gaps[].handler`
    (nulls dropped), not just the chunk handlers, and `hf` carries the
    extractor-failure gaps' handlers (F when none names one).
    """
    if not isinstance(data, dict):
        return None
    nr = data.get('normalized_result')
    nr = nr if isinstance(nr, dict) else {}
    handlers = set()
    failed = False
    for chunk in _as_list(nr.get('chunks')):
        if not isinstance(chunk, dict):
            continue
        handler = chunk.get('handler')
        if isinstance(handler, str) and handler:
            handlers.add(handler)
        if chunk.get('extraction_failed') is True:
            failed = True
    gap_kinds = set()
    dependencies = set()
    failing_handlers = set()
    for gap in _as_list(nr.get('extraction_gaps')):
        if not isinstance(gap, dict):
            continue
        kind = gap.get('kind')
        if isinstance(kind, str):
            gap_kinds.add(kind)
            if kind == 'extractor-failure':
                failed = True
        gh = gap.get('handler')
        if isinstance(gh, str) and gh:
            handlers.add(gh)
            if kind == 'extractor-failure':
                failing_handlers.add(gh)
        for dep in _as_list(gap.get('dependencies')):
            if isinstance(dep, str):
                dependencies.add(dep)
    commands = extractor_commands(data)
    if not commands:
        be = 'n/a'
    else:
        be = 'no'
        for cmd in commands:
            if '-be' in (command_tokens(cmd) or []):
                be = 'yes'
                break
    symlink = 'no'
    for diag in _as_list(nr.get('diagnostics')):
        report = diag.get('report') if isinstance(diag, dict) else None
        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:
            symlink = 'yes'
            break
    if symlink == 'no':
        for found in _iter_dicts(data.get('raw_result')):
            if found.get('__typename__') == SYMLINK_TYPENAME:
                symlink = 'yes'
                break
    return {'handler_set': sorted(handlers), 'gap_kinds': sorted(gap_kinds),
            'gap_dependencies': sorted(dependencies), 'be_argv': be,
            'symlink_removed': symlink == 'yes',
            'published': 'nonzero' if _as_list(nr.get('files')) else 'zero',
            'extraction_failed': failed,
            # A1 reporting only: F and HF are derived, not declared keys.
            'squashfs_handlers': sorted(h for h in handlers
                                        if h.startswith('squashfs_')),
            'failing_handlers': sorted(failing_handlers) or
            sorted(h for h in handlers if h.startswith('squashfs_'))}


FEATURE_ALIASES = {
    'h': 'handler_set', 'handlers': 'handler_set', 'handler': 'handler_set',
    'handler_set': 'handler_set',
    'g': 'gap_kinds', 'gaps': 'gap_kinds', 'gap_kinds': 'gap_kinds',
    'gap kinds': 'gap_kinds',
    'd': 'gap_dependencies', 'deps': 'gap_dependencies',
    'dependencies': 'gap_dependencies', 'gap_dependencies': 'gap_dependencies',
    'be': 'be_argv', 'be_argv': 'be_argv', '-be in child argv': 'be_argv',
    'sr': 'symlink_removed', 'symlink_removed': 'symlink_removed',
    'symlink removed': 'symlink_removed',
    'p': 'published', 'published': 'published', 'published files': 'published',
    'files': 'published',
    'extraction_failed': 'extraction_failed', 'failed': 'extraction_failed',
}


def canon_features(obj):
    """A declared feature tuple in the counter's canonical vocabulary."""
    if not isinstance(obj, dict):
        return None
    out = {}
    for key, value in obj.items():
        k = FEATURE_ALIASES.get(str(key).strip().lower())
        if k is None:
            continue
        if k in ('handler_set', 'gap_kinds', 'gap_dependencies'):
            out[k] = _tokens(value)
        elif k == 'be_argv':
            out[k] = _tri(value)
        elif k == 'symlink_removed':
            out[k] = _tri(value) == 'yes'
        elif k == 'published':
            out[k] = _pub(value)
        elif k == 'extraction_failed':
            out[k] = _tri(value) == 'yes'
    return out or None


def declared_features(carrier):
    """The ONE declared-tuple key (R41-CL1).  No fallbacks, by design."""
    if not isinstance(carrier, dict):
        return None
    return canon_features(carrier.get(DECLARED_KEY))


# ------------------------------------------------------------------ frozen tools
def run_tool(exe, args, timeout=1800, env=None):
    return subprocess.run([sys.executable, '-I', '-B', exe] + list(args),
                          capture_output=True, text=True, timeout=timeout,
                          env=env)


def _row_of(entry):
    for key in ('rule', 'row_index', 'index', 'row'):
        v = entry.get(key)
        if isinstance(v, bool):
            continue
        if isinstance(v, int):
            return v
        if isinstance(v, str) and v.strip().lstrip('-').isdigit():
            return int(v)
    row = entry.get('row')
    if isinstance(row, dict):
        return _row_of(row)
    return None


def parse_json_results(stdout):
    """{key: {label, action, row, cells}} from the interpreter's `--json`."""
    doc = json.loads(stdout)
    results = doc.get('results') if isinstance(doc, dict) else doc
    if not isinstance(results, list):
        return None
    out = {}
    for r in results:
        if not isinstance(r, dict):
            return None
        key = None
        for k in ('path', 'id', 'envelope', 'file'):
            if isinstance(r.get(k), str):
                key = r[k]
                break
        if key is None:
            return None
        action = r.get('action')
        for k in ('row_action', 'decision_action'):
            if action is None:
                action = r.get(k)
        cells = r.get('cells') if isinstance(r.get('cells'), list) else None
        if cells is None and isinstance(r.get('row'), list):
            cells = r['row']
        out[key] = {'label': r.get('label'), 'action': action,
                    'row': _row_of(r), 'cells': cells}
    return out


def parse_tab_results(stdout):
    out = {}
    for line in stdout.splitlines():
        if '\t' not in line:
            continue
        f = line.split('\t')
        path = f[0].strip()
        row = None
        if len(f) > 3 and f[3].strip().lstrip('-').isdigit():
            row = int(f[3].strip())
        out[path] = {'label': (f[1].strip() or None) if len(f) > 1 else None,
                     'action': (f[2].strip() or None) if len(f) > 2 else None,
                     'row': row, 'cells': None}
    return out


TABLE_ONLY_LINE = re.compile(r'^\s*(\d+)\.\s+`?([^`\s]+)`?\s*$')


def parse_table_only(stdout):
    """{label: row} from the interpreter's `--table-only` output."""
    try:
        doc = json.loads(stdout)
        rules = doc.get('rules') if isinstance(doc, dict) else None
        if isinstance(rules, list):
            out = {}
            for r in rules:
                if isinstance(r, dict) and r.get('label') is not None:
                    out[str(r['label'])] = _row_of(r)
            return out or None
    except Exception:
        pass
    out = {}
    for line in stdout.splitlines():
        m = TABLE_ONLY_LINE.match(line)
        if m:
            out[m.group(2)] = int(m.group(1))
    return out or None


def infer_index_base(entries, tpos, label_rows):
    """0 or 1: how the interpreter numbers the rows it reports."""
    votes = []
    for val in entries:
        lab, row = val.get('label'), val.get('row')
        if lab in tpos and isinstance(row, int):
            votes.append(row - tpos[lab])
    for lab, idx in (label_rows or {}).items():
        if lab in tpos and isinstance(idx, int):
            votes.append(idx - tpos[lab])
    if not votes:
        return 0
    return max(set(votes), key=votes.count)


def _pair(v):
    """(label, action) out of the shapes a tool may emit, else None."""
    if isinstance(v, dict):
        lab = v.get('label')
        act = v.get('action')
        if lab is None:
            for k in ('expected_label', 'class_label'):
                if isinstance(v.get(k), str):
                    lab = v[k]
                    break
        if act is None:
            for k in ('expected_action', 'class_action'):
                if isinstance(v.get(k), str):
                    act = v[k]
                    break
        if isinstance(lab, str) and isinstance(act, str):
            return (lab, act)
        return None
    if isinstance(v, (list, tuple)) and len(v) >= 2 \
            and isinstance(v[0], str) and isinstance(v[1], str):
        return (v[0], v[1])
    if isinstance(v, str):
        for sep in ('/', '->', '\t', ':'):
            if sep in v:
                a, b = v.split(sep, 1)
                if a.strip() and b.strip():
                    return (a.strip(), b.strip())
    return None


def parse_eval_pairs(doc, ids):
    """{envelope id: (label, action)} from any of the evaluator's JSON shapes."""
    want = set(ids)
    out = {}

    def put(key, val):
        nid = norm_id(key)
        p = _pair(val)
        if nid in want and p is not None and nid not in out:
            out[nid] = p

    def scan(obj, depth=0):
        if depth > 4:
            return
        if isinstance(obj, list):
            for e in obj:
                if isinstance(e, dict):
                    for k in ('id', 'envelope', 'path', 'file', 'name'):
                        if isinstance(e.get(k), str):
                            put(e[k], e)
                            break
                else:
                    scan(e, depth + 1)
            return
        if not isinstance(obj, dict):
            return
        for k, v in obj.items():
            if isinstance(k, str) and norm_id(k) in want and _pair(v) is not None:
                put(k, v)
            elif isinstance(v, (dict, list)):
                scan(v, depth + 1)

    scan(doc)
    return out


def run_interpreter(ipath, spath, paths, edir, header, trows, attempts=None):
    """Frozen interpreter over `paths` -> ({id: {label, action, row, cells}}, meta).

    Interfaces are probed in order (positional arguments first); the first
    answer that covers every requested envelope wins, and a partial answer is
    kept only while nothing longer appears.  Rows the interpreter does not name
    are read off its own `--table-only`, and a row index or a row's cells is
    turned into the (label, action) that row carries.
    """
    args = sorted(paths)
    want = {norm_id(p) for p in paths if norm_id(p)}
    got = {}
    meta = {'how': None, 'table_only_exit': None, 'base': None, 'derived': 0,
            'stdout_tail': '', 'stderr_tail': ''}

    def collect(parsed):
        out = {}
        for path, val in (parsed or {}).items():
            cid = norm_id(path)
            if cid:
                out[cid] = val
        return out

    last = None
    for name, targs in (
            ('json', ['--skill', spath, '--json'] + args),
            ('tab', ['--skill', spath] + args),
            ('envelopes-json', ['--skill', spath, '--envelopes', edir, '--json']),
            ('envelopes', ['--skill', spath, '--envelopes', edir])):
        pr = run_tool(ipath, targs)
        last = pr
        if attempts is not None:
            attempts.append({'tool': 'interpreter', 'interface': name,
                             'exit': pr.returncode})
        if pr.returncode != 0:
            continue
        parsed = None
        try:
            parsed = parse_json_results(pr.stdout)
        except Exception:
            parsed = None
        if parsed is not None:
            how = name + '/json'
        else:
            parsed = parse_tab_results(pr.stdout) or None
            how = (name + '/tab') if parsed else None
        if not parsed:
            continue
        cand = {k: v for k, v in collect(parsed).items() if k in want}
        if not cand:
            continue
        if not got or len(cand) > len(got):
            got, meta['how'] = cand, how
        if want <= set(cand):
            got, meta['how'] = cand, how
            break
    if last is not None:
        meta['stdout_tail'] = (last.stdout or '')[-1000:]
        meta['stderr_tail'] = (last.stderr or '')[-1000:]
    if not got:
        return got, meta

    if any(v.get('row') is None for v in got.values()):
        pt = run_tool(ipath, ['--skill', spath, '--table-only'])
        meta['table_only_exit'] = pt.returncode
        label_rows = parse_table_only(pt.stdout) if pt.returncode == 0 else None
        if label_rows:
            for val in got.values():
                if val.get('row') is None:
                    val['row'] = label_rows.get(val.get('label'))
            if all(v.get('row') is not None for v in got.values()) and meta['how']:
                meta['how'] += '+table_only'

    if header is not None:
        lidx = header.index('label') if 'label' in header else None
        aidx = header.index('action') if 'action' in header else None
        tpos = {}
        if lidx is not None:
            for i, cells in enumerate(trows):
                if lidx < len(cells) and cells[lidx] not in tpos:
                    tpos[cells[lidx]] = i
        need = [v for v in got.values()
                if (v.get('label') is None or v.get('action') is None)
                and v.get('cells') is None and isinstance(v.get('row'), int)]
        label_rows = None
        if need and tpos:
            pt = run_tool(ipath, ['--skill', spath, '--table-only'])
            meta['table_only_exit'] = pt.returncode
            if pt.returncode == 0:
                label_rows = parse_table_only(pt.stdout)
        base = infer_index_base(list(got.values()), tpos, label_rows)
        meta['base'] = base
        for val in got.values():
            cells = val.get('cells')
            if cells is None and isinstance(val.get('row'), int):
                pos = val['row'] - base
                if 0 <= pos < len(trows):
                    cells = trows[pos]
            if cells is None:
                continue
            if val.get('label') is None and lidx is not None and lidx < len(cells):
                val['label'] = cells[lidx]
                meta['derived'] += 1
            if val.get('action') is None and aidx is not None and aidx < len(cells):
                val['action'] = cells[aidx]
                meta['derived'] += 1
    return got, meta


def run_evaluator(exe, edir, want_ids, scratch, tag='main', attempts=None):
    """Frozen independent evaluator over an envelope directory.

    Returns ({id: (label, action)}, interface, saw_a_zero_exit, meta).  The
    interface is probed because the frozen evaluator's writer chose it: stdout
    JSON (--envelopes, --json, --format json) and the two file-output forms
    (--out, --json-out).
    """
    fout = os.path.join(scratch, 'eval-labels-%s.json' % tag)
    meta = {'stdout_tail': '', 'stderr_tail': ''}
    any_zero = False
    for name, args, ofile in (
            ('envelopes', ['--envelopes', edir], None),
            ('envelopes-json', ['--envelopes', edir, '--json'], None),
            ('envelopes-format', ['--envelopes', edir, '--format', 'json'], None),
            ('envelopes-out', ['--envelopes', edir, '--out', fout], fout),
            ('envelopes-json-out', ['--envelopes', edir, '--json-out', fout], fout)):
        if ofile and os.path.exists(ofile):
            os.unlink(ofile)
        pr = run_tool(exe, args)
        if attempts is not None:
            attempts.append({'tool': 'evaluator', 'interface': name,
                             'exit': pr.returncode})
        meta['stdout_tail'] = (pr.stdout or '')[-1000:]
        meta['stderr_tail'] = (pr.stderr or '')[-1000:]
        if pr.returncode != 0:
            continue
        any_zero = True
        text = pr.stdout
        if ofile and os.path.exists(ofile):
            try:
                with open(ofile) as fh:
                    text = fh.read()
            except Exception:
                pass
        try:
            doc = json.loads(text)
        except Exception:
            continue
        got = parse_eval_pairs(doc, want_ids)
        if got:
            return got, name, any_zero, meta
    return {}, None, any_zero, meta


def flat_envelopes(scratch, tag, rows):
    """Materialise [(id, bytes)] as `<id>.json` in a fresh dir; return (dir, map)."""
    d = os.path.join(scratch, 'env-' + tag)
    os.makedirs(d, exist_ok=True)
    argmap = {}
    for cid, blob in rows:
        fp = os.path.join(d, cid + '.json')
        with open(fp, 'wb') as fh:
            fh.write(blob)
        argmap[cid] = fp
    return d, argmap


# ------------------------------------------------------------------ measure
def measure(root, rev_arg, freeze_arg):
    rev = full_rev(root, rev_arg)
    freeze = full_rev(root, freeze_arg)
    res = {'predicate': 'P42-C2', 'revision': rev, 'freeze': freeze,
           'freeze_arg': freeze_arg, 'revision_arg': rev_arg,
           'manifest_path': MANIFEST, 'argv': sys.argv, 'bindings': {},
           'bindings_false': [], 'carriers': [], 'frozen_paths_changed': [],
           'claim_bindings': list(CLAIM_BINDINGS),
           'instrument_bindings': list(INSTRUMENT_BINDINGS),
           'declared_key': DECLARED_KEY}
    if not is_ancestor(root, freeze, rev):
        raise Unevaluable('freeze_not_ancestor_of_rev', res)

    # ---- frozen units at FREEZE
    gen_b = show(root, freeze, GEN)
    eval_b = show(root, freeze, EVAL)
    interp_b = show(root, freeze, INTERP)
    claims_b = show(root, freeze, CLAIMS)
    counter_b = show(root, freeze, COUNTER)
    skill_fz_b = show(root, freeze, SKILL)
    skill_fz = rule_block(as_text(skill_fz_b), MARKER_V4)
    lookup_fz_b = show(root, freeze, LOOKUP)
    lookup_fz = rule_block(as_text(lookup_fz_b), MARKER_V4)
    res['frozen_units'] = {
        GEN: sha256_bytes(gen_b), EVAL: sha256_bytes(eval_b),
        INTERP: sha256_bytes(interp_b), COUNTER: sha256_bytes(counter_b),
        CLAIMS: sha256_bytes(claims_b),
        SKILL + ' [' + MARKER_V4 + ']': sha256_bytes(skill_fz.encode())
        if skill_fz is not None else None,
        LOOKUP + ' [' + MARKER_V4 + ']': sha256_bytes(lookup_fz.encode())
        if lookup_fz is not None else None,
    }

    # ---- freeze integrity: paths, writers, fixtures, and the SKILL block
    man_b = show(root, rev, MANIFEST)
    declared = None
    man_any = None
    if man_b is not None:
        try:
            _m = json.loads(man_b.decode())
            man_any = _m if isinstance(_m, dict) else None
        except Exception:
            man_any = None
    if isinstance(man_any, dict):
        g = man_any.get('generator')
        w = g.get('writer') if isinstance(g, dict) else None
        if isinstance(w, dict) and isinstance(w.get('path'), str):
            declared = w['path']
        elif isinstance(w, str):
            declared = w
    scope = writer_scope(root, freeze, as_text(gen_b), declared)
    res['writer_scope'] = scope
    paths = list(FROZEN_PATHS) + sorted(scope)
    bad_paths = frozen_drift(root, freeze, rev, paths)
    scanned, drift = skill_block_drift(root, freeze, rev, skill_fz)
    res['skill_block_commits_scanned'] = len(scanned)
    if bad_paths or drift:
        res['frozen_paths_changed'] = sorted(bad_paths) if bad_paths else [SKILL]
        res['frozen_commits'] = bad_paths
        res['skill_block_drift_commits'] = drift
        raise Unevaluable('frozen_path_changed', res)

    if man_b is None:
        raise Unevaluable('no_manifest_at_rev', res)
    try:
        man = json.loads(man_b.decode())
    except Exception:
        raise Unevaluable('manifest_unparsable', res)
    if not isinstance(man, dict):
        raise Unevaluable('manifest_not_an_object', res)

    classes = man.get('classes') if isinstance(man.get('classes'), list) else []
    carriers = man.get('carriers') if isinstance(man.get('carriers'), list) else []
    carriers = [c for c in carriers if isinstance(c, dict)]
    N = len(carriers)
    ids = [str(c.get('id', '')) for c in carriers]
    combos = [c for c in carriers if str(c.get('class')) == COMBO_CLASS]
    class_carriers = [c for c in carriers if str(c.get('class')) != COMBO_CLASS]
    class_names = [c for c in classes if c != COMBO_CLASS]
    per = {}
    for c in class_carriers:
        per[c.get('class')] = per.get(c.get('class'), 0) + 1

    b = res['bindings']
    b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze

    gen_sha = sha256_bytes(gen_b)
    g = man.get('generator')
    if isinstance(g, dict):
        b['manifest_generator_path'] = str(g.get('name', '')).lower() in (
            'heldout-gen-v4.py', GEN)
        declared_gen_sha = g.get('sha256')
        b['generator_sha_matches_freeze'] = declared_gen_sha is None \
            or declared_gen_sha == gen_sha
    else:
        b['manifest_generator_path'] = str(g) == GEN
        declared_gen_sha = None
        b['generator_sha_matches_freeze'] = True
    res['generator'] = {'declared': g, 'declared_sha256': declared_gen_sha,
                        'freeze_sha256': gen_sha, 'path': GEN,
                        'present_at_freeze': gen_b is not None}

    gw = g.get('writer') if isinstance(g, dict) else None
    wpath = gw.get('path') if isinstance(gw, dict) else (gw if isinstance(gw, str) else None)
    wsha = gw.get('sha256') if isinstance(gw, dict) else None
    if wpath is None:
        b['writer_matches_manifest'] = True
    else:
        ok = wpath in scope and scope[wpath]['present_at_freeze'] \
            and (wsha is None or wsha == scope[wpath]['sha256'])
        b['writer_matches_manifest'] = bool(ok)
    res['writer'] = {'declared_path': wpath, 'declared_sha256': wsha,
                     'scope': sorted(scope)}

    b['classes_unique'] = bool(classes) and len(classes) == len(set(classes)) \
        and all(isinstance(x, str) and x for x in classes)
    b['classes_two_each'] = bool(class_names) \
        and all(per.get(k) == 2 for k in class_names) \
        and set(per) <= set(class_names)
    b['n_equals_twice_classes'] = N > 0 and N == 2 * len(class_names) + len(combos)
    combo_ids = sorted(str(c.get('id')) for c in combos)
    b['combo_family_wellformed'] = len(combos) >= COMBO_MIN and \
        combo_ids == ['C%02d' % i for i in range(1, len(combos) + 1)]
    declared_combo_count = man.get('combo_count')
    if isinstance(declared_combo_count, int):
        b['combo_family_wellformed'] = b['combo_family_wellformed'] \
            and declared_combo_count == len(combos)
    b['ids_unique'] = bool(ids) and len(set(ids)) == len(ids) and all(ids)
    b['arms_valid'] = bool(carriers) and all(c.get('arm') in ('after', 'before', 'ood')
                                             for c in carriers)

    # ---- the v4 rule block at REV
    skill_rev = show(root, rev, SKILL)
    v4_rev = rule_block(as_text(skill_rev), MARKER_V4)
    verbs = declared_actions(v4_rev)
    cols_ok, cols_missing = columns_ok(v4_rev)
    v4_labels = table_labels(v4_rev)
    b['v4_block_present'] = v4_rev is not None
    b['v4_block_identical'] = v4_rev is not None and skill_fz is not None \
        and v4_rev == skill_fz
    b['v4_block_columns'] = bool(v4_rev) and cols_ok
    b['v4_actions_declared'] = bool(verbs)
    res['table'] = {'v4': {'present_at_rev': v4_rev is not None,
                           'present_at_freeze': skill_fz is not None,
                           'identical': b['v4_block_identical'],
                           'columns_ok': cols_ok,
                           'columns_missing': cols_missing,
                           'declared_actions': verbs,
                           'labels': v4_labels,
                           'bytes_rev': len(v4_rev.encode()) if v4_rev is not None else 0,
                           'bytes_freeze': len(skill_fz.encode()) if skill_fz is not None else 0},
                   'v3_marker_at_rev': bool(skill_rev and MARKER_V3 in as_text(skill_rev)),
                   'v3_marker_at_freeze': bool(skill_fz_b and MARKER_V3 in as_text(skill_fz_b))}

    def resolve(p):
        if not isinstance(p, str) or not p or p.startswith('/') \
                or '..' in p.split('/'):
            return None
        for cand in (p, MANIFEST_DIR.rstrip('/') + '/' + p):
            if cand.startswith('./'):
                cand = cand[2:]
            if present(root, rev, cand):
                return cand
        return None

    if eval_b is None:
        raise Unevaluable('evaluator_absent_at_freeze', res)
    if interp_b is None:
        raise Unevaluable('interpreter_absent_at_freeze', res)

    scratch = scratch_dir()
    try:
        # ---- regeneration from the frozen generator
        if gen_b is None:
            raise Unevaluable('generator_absent_at_freeze', res)
        regen = {}
        tree = os.path.join(scratch, 'lane')
        os.makedirs(tree)
        p = subprocess.run(['git', '-C', root, 'ls-tree', '-r', '--name-only',
                            freeze, '--', *GEN_TREE_PREFIXES],
                           capture_output=True, text=True)
        materialised = []
        for rel in [l for l in p.stdout.split() if l]:
            blob = show(root, freeze, rel)
            if blob is None:
                continue
            dest = os.path.join(tree, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'wb') as fh:
                fh.write(blob)
            materialised.append(rel)
        gpath = os.path.join(tree, GEN)
        if not os.path.isfile(gpath):
            raise Unevaluable('generator_absent_at_freeze', res)
        res['materialised_files'] = len(materialised)
        env = dict(os.environ)
        env['TMPDIR'] = os.path.join(scratch, 'tmp')
        os.makedirs(env['TMPDIR'], exist_ok=True)
        wpick = wpath if wpath in scope else (sorted(scope)[0] if scope else None)
        wlocal = os.path.join(tree, wpick) if wpick else None
        if wlocal and os.path.isfile(wlocal):
            env[WRITER_ENV] = wlocal
        res['writer']['materialised'] = bool(wlocal and os.path.isfile(wlocal))
        fxd = os.path.join(tree, MANIFEST_DIR.rsplit('/', 1)[0], 'fixtures')
        if os.path.isdir(fxd):
            env[FIXTURE_ENV] = fxd
        outdir = os.path.join(scratch, 'regen')
        pr = subprocess.run([sys.executable, '-I', '-B', gpath, '--seed', freeze,
                             '--out', outdir], cwd=tree, capture_output=True,
                            text=True, timeout=3600, env=env)
        if pr.returncode != 0:
            res['generator_stderr'] = (pr.stderr or '')[-2000:]
            raise Unevaluable('generator_failed', res)
        rman_path = os.path.join(outdir, 'manifest.json')
        if not os.path.exists(rman_path):
            raise Unevaluable('generator_wrote_no_manifest', res)
        try:
            with open(rman_path) as fh:
                rman = json.load(fh)
        except Exception:
            raise Unevaluable('regenerated_manifest_unparsable', res)
        for rc in (rman.get('carriers') or []):
            if not isinstance(rc, dict):
                continue
            rel = rc.get('carrier')
            fp = os.path.join(outdir, rel) if isinstance(rel, str) else None
            data = open(fp, 'rb').read() if fp and os.path.isfile(fp) else None
            regen[str(rc.get('id', ''))] = {
                'sha256': sha256_bytes(data), 'class': rc.get('class'),
                'arm': rc.get('arm'), 'carrier': rel,
                'declared_features': rc.get(DECLARED_KEY)}
        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze

        # ---- per-carrier: bytes, envelope digest, declaration
        env_rows = []
        env_objs = {}
        for c in carriers:
            cid = str(c.get('id', ''))
            msha = str(c.get('sha256', '')).lower()
            cpath = resolve(c.get('carrier'))
            cbytes = show(root, rev, cpath) if cpath else None
            committed_sha = sha256_bytes(cbytes)
            r = regen.get(cid) or {}
            regen_sha = r.get('sha256')
            regen_ok = bool(regen_sha) and regen_sha == msha \
                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm')
            commit_ok = committed_sha is not None and committed_sha == msha
            epath = c.get('envelope')
            inferred = False
            if not isinstance(epath, str) or not epath:
                car = c.get('carrier')
                if isinstance(car, str) and '/' in car:
                    epath = car.rsplit('/', 1)[0] + '/envelope.json'
                    inferred = True
                else:
                    epath = None
            epath = resolve(epath) if epath else None
            ebytes = show(root, rev, epath) if epath else None
            digest_ok = False
            if ebytes is not None:
                try:
                    eo = envelope_data(json.loads(ebytes.decode()))
                    digest_ok = bool(msha) and subject_sha(eo) == msha
                    env_rows.append({'id': cid, 'path': epath, 'bytes': ebytes})
                    env_objs[cid] = eo
                except Exception:
                    digest_ok = False
            res['carriers'].append({
                'id': cid, 'class': c.get('class'), 'arm': c.get('arm'),
                '_carrier_path': cpath,
                'manifest_sha256': msha, 'committed_sha256': committed_sha,
                'regenerated_sha256': regen_sha, 'regen_ok': regen_ok,
                'commit_ok': commit_ok, 'envelope': epath,
                'envelope_inferred': inferred, 'digest_ok': digest_ok,
                'declared_features_present': isinstance(c.get(DECLARED_KEY), dict)})
        cp = [r.get('_carrier_path') for r in res['carriers']]
        ep = [r.get('envelope') for r in res['carriers']]
        b['carrier_paths_unique'] = N > 0 and all(cp) and len(set(cp)) == len(cp)
        b['envelope_paths_unique'] = N > 0 and all(ep) and len(set(ep)) == len(ep)
        for r in res['carriers']:
            r.pop('_carrier_path', None)
        b['carriers_regenerated'] = N > 0 and all(r['regen_ok'] for r in res['carriers'])
        b['carriers_committed'] = N > 0 and all(r['commit_ok'] for r in res['carriers'])
        b['envelopes_valid'] = N > 0 and all(r['digest_ok'] for r in res['carriers'])

        # ---- first-add ordering
        ma = first_add(root, rev, MANIFEST)
        b['manifest_after_freeze'] = bool(ma) and ma != freeze \
            and is_ancestor(root, freeze, ma)
        env_firsts = []
        for row in res['carriers']:
            fa = first_add(root, rev, row['envelope']) if row['envelope'] else None
            row['envelope_first_add'] = fa
            env_firsts.append(fa)
        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \
            and all(fa is not None and is_ancestor(root, ma, fa) for fa in env_firsts)
        res['manifest_first_add'] = ma

        # ---- INDEPENDENT evaluator (frozen bytes) on the REV envelopes
        edir, argmap = flat_envelopes(scratch, 'main', [(r['id'], r['bytes'])
                                                        for r in env_rows])
        exe = os.path.join(scratch, 'indep-eval-v4.py')
        with open(exe, 'wb') as fh:
            fh.write(eval_b)
        attempts = []
        want_ids = [r['id'] for r in env_rows]
        exp, used, any_zero, emeta = run_evaluator(exe, edir, want_ids, scratch,
                                                   tag='main', attempts=attempts)
        res['evaluator_interface'] = used
        res['evaluator_attempts'] = attempts
        res['expected_source'] = ('the frozen independent evaluator, %s @ freeze, '
                                  'envelopes @ rev' % EVAL) if used else None
        if used is None:
            reason = 'evaluator_output_unparsable' if any_zero else 'evaluator_failed'
            res['evaluator_stdout_tail'] = emeta['stdout_tail']
            res['evaluator_stderr_tail'] = emeta['stderr_tail']
            raise Unevaluable(reason, res)
        b['evaluator_covers_all'] = set(want_ids) <= set(exp)
        res['evaluator_missing'] = sorted(set(want_ids) - set(exp))
        res['evaluator_extra'] = sorted(set(exp) - set(want_ids))

        # ---- the frozen interpreter on SKILL.md at REV
        idir = os.path.join(scratch, 'triage')
        os.makedirs(idir)
        ipath = os.path.join(idir, 'sqfs-triage-v4.py')
        with open(ipath, 'wb') as fh:
            fh.write(interp_b)
        spath = os.path.join(idir, 'SKILL.md')
        with open(spath, 'wb') as fh:
            fh.write(skill_rev if skill_rev is not None else b'')
        header, trows = parse_rows(v4_rev)
        interp_attempts = []
        got = {}
        imeta = {'how': None, 'table_only_exit': None, 'base': None, 'derived': 0,
                 'stdout_tail': '', 'stderr_tail': ''}
        if v4_rev is not None:
            got, imeta = run_interpreter(ipath, spath, sorted(argmap.values()),
                                         edir, header, trows, interp_attempts)
        res['interpreter_interface'] = imeta['how']
        res['interpreter_attempts'] = interp_attempts
        res['row_source'] = imeta['how']
        res['interpreter_table_only_exit'] = imeta['table_only_exit']
        res['row_index_base'] = imeta['base']
        res['pair_fields_derived_from_row'] = imeta['derived']
        if v4_rev is not None and not got:
            res['interpreter_stderr_tail'] = imeta['stderr_tail']
            res['interpreter_stdout_tail'] = imeta['stdout_tail']
            tail = (imeta['stderr_tail'] or '').strip().splitlines()
            res['interpreter_refusal'] = tail[-1] if tail else None
            raise Unevaluable('interpreter_failed', res)

        # ---- score: observed (interpreter) vs expected (evaluator)
        mismatch_pairs = []
        for row in res['carriers']:
            cid = row['id']
            v = got.get(cid) or {}
            row['combo'] = str(row.get('class')) == COMBO_CLASS
            row['label'] = v.get('label')
            row['action'] = v.get('action')
            row['row'] = v.get('row')
            e = exp.get(cid)
            row['expected_label'], row['expected_action'] = (e if e else (None, None))
            row['pair_match'] = e is not None and row['label'] == e[0] \
                and row['action'] == e[1]
            if not row['pair_match']:
                mismatch_pairs.append({'id': cid, 'class': row.get('class'),
                                       'expected': list(e) if e else None,
                                       'observed': [row['label'], row['action']]})

        observed_actions = sorted({r['action'] for r in res['carriers']
                                   if isinstance(r['action'], str)})
        b['observed_actions_declared'] = bool(verbs) and all(a in verbs
                                                             for a in observed_actions)
        res['observed_actions'] = observed_actions
        res['actions_undeclared'] = sorted(a for a in observed_actions
                                           if not verbs or a not in verbs)

        matched = sum(1 for row in res['carriers'] if row['pair_match'])
        res['matched_classes'] = sum(1 for row in res['carriers']
                                     if row['pair_match'] and not row['combo'])
        res['matched_combos'] = sum(1 for row in res['carriers']
                                    if row['pair_match'] and row['combo'])
        res['n_classes'] = len(class_carriers)
        res['n_combos'] = len(combos)
        res['pair_mismatches'] = mismatch_pairs[:40]
        matched_rows = [row['row'] for row in res['carriers'] if row['pair_match']]
        reported = bool(got) and all(
            r.get('row') is not None
            or (r.get('expected_label'), r.get('expected_action')) == NOMATCH_PAIR
            for r in res['carriers'])
        b['decisions_reported'] = reported
        res['distinct_decisions'] = len(set(matched_rows))
        res['distinct_rows'] = len({r for r in matched_rows if r is not None})
        res['distinct_row_list'] = sorted(set(matched_rows),
                                          key=lambda x: (x is None, str(x)))

        pairs = {}
        for row in res['carriers']:
            pairs.setdefault((row['expected_label'], row['expected_action']),
                             set()).add(row['row'])
        ok_rows = True
        for k, v in pairs.items():
            if k == NOMATCH_PAIR:
                if v != {None}:
                    ok_rows = False
            elif len(v) != 1 or None in v:
                ok_rows = False
        if ok_rows:
            seen = {}
            for k, v in pairs.items():
                if k == NOMATCH_PAIR:
                    continue
                r = next(iter(v))
                if r in seen and seen[r] != k:
                    ok_rows = False
                seen[r] = k
        b['row_decisions_consistent'] = bool(reported and ok_rows)
        res['decision_pairs'] = {'%s/%s' % k: sorted(v, key=lambda x: (x is None, str(x)))
                                 for k, v in pairs.items()}

        # ---- observed features vs the ONE declared key (R41-CL1)
        by_id = {r['id']: r for r in res['carriers']}
        feat_missing, feat_bad, feat_classes = [], [], {}
        for c in carriers:
            cid = str(c.get('id', ''))
            canon = declared_features(c)
            if canon is None or any(k not in canon for k in REQUIRED_FEATURES):
                feat_missing.append(cid)
                feat_classes[str(c.get('class'))] = 'declared-tuple-incomplete'
                continue
            obs = observed_features(env_objs.get(cid))
            if obs is None:
                feat_missing.append(cid)
                feat_classes[str(c.get('class'))] = 'envelope-unreadable'
                continue
            shared = [k for k in canon if k in obs]
            bad = [k for k in shared if canon[k] != obs[k]]
            row = by_id.get(cid)
            if row is not None:
                row['features_checked'] = shared
                row['features_match'] = not bad
                row['declared_features'] = canon
            if bad:
                feat_bad.append({'id': cid, 'class': c.get('class'), 'differ': bad,
                                 'declared': {k: canon[k] for k in shared},
                                 'observed': {k: obs[k] for k in shared}})
                feat_classes[str(c.get('class'))] = 'mismatch'
            else:
                feat_classes.setdefault(str(c.get('class')), 'match')
        b['observed_features_match_declared'] = N > 0 and not feat_missing \
            and not feat_bad
        res[DECLARED_KEY] = {'source': 'carriers[].' + DECLARED_KEY,
                             'keys': list(FEATURE_KEYS),
                             'required': list(REQUIRED_FEATURES),
                             'by_class': feat_classes,
                             'missing': feat_missing,
                             'mismatch': feat_bad}

        # ---- the frozen lookup control on the held-out combos
        lookup_rev_b = show(root, rev, LOOKUP)
        lookup_rev = rule_block(as_text(lookup_rev_b), MARKER_V4)
        lheader, lrows = parse_rows(lookup_rev)
        lgot, lmeta, lattempts = {}, {'how': None}, []
        score, scored_ids, lmissing = 0, [], []
        if lookup_rev is not None and combos:
            lpath = os.path.join(idir, 'CTL-C2-7-lookup.md')
            with open(lpath, 'wb') as fh:
                fh.write(lookup_rev_b)
            combo_paths = [argmap[c['id']] for c in combos if c['id'] in argmap]
            lgot, lmeta = run_interpreter(ipath, lpath, sorted(combo_paths), edir,
                                          lheader, lrows, lattempts)
            for c in combos:
                cid = c['id']
                v = lgot.get(cid) or {}
                e = exp.get(cid)
                if e is None:
                    lmissing.append(cid)
                    continue
                if v.get('label') == e[0] and v.get('action') == e[1]:
                    score += 1
                    scored_ids.append(cid)
        n_combos = len(combos)
        b['lookup_control_identical'] = lookup_rev is not None and lookup_fz is not None \
            and lookup_rev == lookup_fz
        # L1 freeze decision (KaidokuR42): REPORTED, not bound — a per-label lookup can only
        # be built with real labels by inducing rows from evaluator-labelled data, which is
        # the claimed work learned from the labels (w1/R42C2ControlTables.md 7.2,
        # w1/R42CritC2Draft.md Q4); the bound anti-enumeration witness is combo_unseen_majority.
        lookup_below_half = n_combos > 0 and lmeta.get('how') is not None \
            and score * 2 < n_combos and not lmissing
        res['lookup'] = {'path': LOOKUP, 'present_at_rev': lookup_rev is not None,
                         'identical_to_freeze': b['lookup_control_identical'],
                         'interpreter_interface': lmeta.get('how'),
                         'attempts': lattempts,
                         'n_combos': n_combos, 'score': score,
                         'half': n_combos / 2.0,
                         'scored_ids': scored_ids,
                         'missing_expected': lmissing,
                         'below_half': lookup_below_half,
                         'binding': False,
                         'note': 'reported, not bound (L1 freeze decision)'}

        # ---- the four committed round-41 C1 receipts (real envelopes)
        rdir, rpaths = flat_envelopes(scratch, 'real', [])
        rsha, rmissing = {}, []
        for rp in REAL_RECEIPTS:
            blob = show(root, rev, rp)
            if blob is None:
                rmissing.append(rp)
                continue
            name = rp.split('/')[-2]
            fp = os.path.join(rdir, name + '.json')
            with open(fp, 'wb') as fh:
                fh.write(blob)
            rpaths[name] = fp
            rsha[rp] = sha256_bytes(blob)
        rnames = sorted(rpaths)
        rgot, rmeta, rexp = {}, {'how': None}, {}
        rused = None
        rattempts = {'interpreter': [], 'evaluator': []}
        if rpaths:
            rgot, rmeta = run_interpreter(ipath, spath, sorted(rpaths.values()),
                                          rdir, header, trows,
                                          rattempts['interpreter'])
            rexp, rused, _rzero, _rmeta = run_evaluator(
                exe, rdir, rnames, scratch, tag='real',
                attempts=rattempts['evaluator'])
        rows = {}
        real_ok = bool(rpaths) and len(rpaths) == len(REAL_RECEIPTS)
        for name in rnames:
            ip_ = rgot.get(name) or {}
            i_pair = [ip_.get('label'), ip_.get('action')]
            e_pair = list(rexp[name]) if name in rexp else None
            ok = i_pair[0] == REAL_LABEL and e_pair is not None and i_pair == e_pair
            real_ok = real_ok and ok
            rows[name] = {'interpreter': i_pair, 'evaluator': e_pair, 'ok': ok}
        b['real_receipts_depth_limited'] = bool(real_ok)
        res['real_receipts'] = {
            'expected_label': REAL_LABEL,
            'sha256': {p: rsha.get(p) for p in REAL_RECEIPTS},
            'missing': rmissing, 'rows': rows,
            'interpreter_interface': rmeta.get('how'),
            'evaluator_interface': rused,
            'attempts': rattempts}

        # ---- the round-42 dev arm (real legacy-family envelopes)
        dev_dir = next((d for d in DEV_DIRS
                        if any(present(root, rev, d + '/' + n + '/envelope.json')
                               for n in _dir_names(root, rev, d))), None)
        dev_rows, dev_sha = [], {}
        droot = os.path.join(scratch, 'dev')
        os.makedirs(droot, exist_ok=True)
        dpaths = {}
        if dev_dir:
            for n in _dir_names(root, rev, dev_dir):
                rp = dev_dir + '/' + n + '/envelope.json'
                blob = show(root, rev, rp)
                if blob is None:
                    continue
                with open(os.path.join(droot, n + '.json'), 'wb') as fh:
                    fh.write(blob)
                dpaths[n] = os.path.join(droot, n + '.json')
                dev_sha[rp] = sha256_bytes(blob)
        dgot, dmeta, dexp = {}, {'how': None}, {}
        dused = None
        dattempts = {'interpreter': [], 'evaluator': []}
        dnames = sorted(dpaths)
        if dpaths:
            dgot, dmeta = run_interpreter(ipath, spath, sorted(dpaths.values()),
                                          droot, header, trows,
                                          dattempts['interpreter'])
            dexp, dused, _dzero, _dmeta = run_evaluator(
                exe, droot, dnames, scratch, tag='dev',
                attempts=dattempts['evaluator'])
        dev_ok = len(dpaths) >= DEV_MIN and dused is not None
        legacy_seen = False
        for name in dnames:
            ip_ = dgot.get(name) or {}
            i_pair = [ip_.get('label'), ip_.get('action')]
            e_pair = list(dexp[name]) if name in dexp else None
            ok = e_pair is not None and i_pair == e_pair
            dev_ok = dev_ok and ok
            with open(dpaths[name], 'rb') as fh:
                obs = observed_features(envelope_data(json.loads(fh.read().decode())))
            hs = (obs or {}).get('handler_set') or []
            if any(h.startswith(LEGACY_HANDLER_PREFIXES) for h in hs):
                legacy_seen = True
                # L1 freeze amendment (QUALITY 84 dry run, `l1/dryrun-c2-pre2.json`):
                # R41-CL4 forbids `no-squashfs-chunk` on an envelope that HOLDS a
                # legacy chunk; the dev arm's own no-squashfs-chunk class (no
                # SquashFS handler at all) is that label's correct answer.
                if 'no-squashfs-chunk' in (i_pair[0], (e_pair or [None])[0]):
                    dev_ok = False
            dev_rows.append({'id': name, 'interpreter': i_pair,
                             'evaluator': e_pair, 'ok': ok,
                             'handler_set': hs})
        b['legacy_dev_envelopes'] = bool(dev_ok and legacy_seen)
        res['dev_envelopes'] = {'dir': dev_dir, 'n': len(dpaths),
                                'min': DEV_MIN, 'rows': dev_rows,
                                'legacy_handler_seen': legacy_seen,
                                'sha256': dev_sha,
                                'interpreter_interface': dmeta.get('how'),
                                'evaluator_interface': dused,
                                'attempts': dattempts}

        # ---- A1: combos whose tuple no frozen dev named-class tuple carries
        dev_declared, dev_declared_src = [], None
        dev_man_b = show(root, rev, dev_dir + '/manifest.json') if dev_dir else None
        if dev_man_b is not None:
            try:
                dman = json.loads(dev_man_b.decode())
            except Exception:
                dman = None
            for c in (dman or {}).get('carriers') or []:
                if not isinstance(c, dict) or str(c.get('class')) == COMBO_CLASS:
                    continue
                can = declared_features(c)
                if can is not None:
                    dev_declared.append(can)
            if dev_declared:
                dev_declared_src = dev_dir + '/manifest.json (carriers[].' + DECLARED_KEY + ')'
        if not dev_declared and dev_dir:
            for name in dnames:
                blob = show(root, rev, '%s/%s/envelope.json' % (dev_dir, name))
                if blob is None:
                    continue
                try:
                    eo = envelope_data(json.loads(blob.decode()))
                except Exception:
                    continue
                can = canon_features(eo.get(DECLARED_KEY)) \
                    if isinstance(eo, dict) else None
                if can is not None:
                    dev_declared.append(can)
            if dev_declared:
                dev_declared_src = dev_dir + '/*/envelope.json (' + DECLARED_KEY + ')'

        def tuple_key(can):
            return tuple((k, json.dumps(can.get(k), sort_keys=True))
                         for k in REQUIRED_FEATURES)

        dev_tuples = {tuple_key(c) for c in dev_declared}
        unseen, seen_ids = [], []
        for c in combos:
            obs = observed_features(env_objs.get(c['id']))
            if obs is None:
                continue
            if tuple_key(obs) in dev_tuples:
                seen_ids.append(c['id'])
            else:
                unseen.append(c['id'])
        majority_need = (len(combos) + 1) // 2
        b['combo_unseen_majority'] = bool(dev_tuples) and len(combos) > 0 \
            and len(unseen) >= majority_need
        res['combo_unseen_majority'] = {
            'source': dev_declared_src, 'dev_named_tuples': len(dev_tuples),
            'n_combos': len(combos), 'unseen': unseen, 'seen_in_dev': seen_ids,
            'need': majority_need, 'binding': 'len(unseen) >= ceil(n_combos/2)'}

        # ---- closure D4: the receipt carries the counter digest and exit code
        counter_rev = show(root, rev, COUNTER)
        res['counter_sha256'] = sha256_bytes(counter_rev)
        res['counter_sha256_at_freeze'] = sha256_bytes(counter_b)
        res['counter_path'] = COUNTER

        # ---- target
        res['bindings_undeclared'] = sorted(set(b) - set(CLAIM_BINDINGS)
                                           - set(INSTRUMENT_BINDINGS))
        res['bindings_declared_unset'] = sorted((set(CLAIM_BINDINGS)
                                                 | set(INSTRUMENT_BINDINGS))
                                                - set(b) - {'bindings_complete'})
        b['bindings_complete'] = not res['bindings_undeclared'] \
            and not res['bindings_declared_unset']
        bindings_ok = all(v is True for v in b.values())
        met = bool(matched == N and bindings_ok)
        recomputed = bool(matched == N and all(v is True for k, v in b.items()))
        res.update({'n': N, 'matched': matched, 'bindings_ok': bindings_ok,
                    'bindings_false': sorted(k for k, v in b.items() if v is not True),
                    'met_target': met,
                    'met_target_formula': {'matched_equals_n': matched == N,
                                           'all_bindings_true': bindings_ok},
                    'met_target_consistent': met == recomputed})
        if not res['met_target_consistent']:
            raise Unevaluable('met_target_inconsistent', res)
        res['exit_code'] = 0 if met else 1
        return res
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def _dir_names(root, rev, path):
    """Immediate child directory names of `path` at `rev` (git ls-tree)."""
    p = subprocess.run(['git', '-C', root, 'ls-tree', '--name-only', rev, '--',
                        path.rstrip('/') + '/'], capture_output=True, text=True)
    if p.returncode:
        return []
    return sorted(l.strip().rstrip('/').rsplit('/', 1)[-1] for l in p.stdout.splitlines()
                  if l.strip())


# ------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.rev and a.freeze):
        print('usage: --root --rev --freeze required (or --selftest)',
              file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze)
    except Unevaluable as e:
        out = dict(e.receipt)
        out['unevaluable'] = e.reason
        out['exit_code'] = 2
        out['argv'] = sys.argv
        out['counter_sha256'] = sha256_bytes(
            show(a.root, _safe_rev(a.root, a.rev), COUNTER))
        print(json.dumps({'unevaluable': e.reason,
                          'revision': out.get('revision'),
                          'freeze': out.get('freeze'),
                          'frozen_paths_changed': out.get('frozen_paths_changed', []),
                          'exit_code': 2}, sort_keys=True))
        if a.json_out:
            d = os.path.dirname(os.path.abspath(a.json_out))
            os.makedirs(d, exist_ok=True)
            with open(a.json_out, 'w') as f:
                json.dump(out, f, indent=1, sort_keys=True)
        return 2
    print(json.dumps({'revision': res['revision'], 'freeze': res['freeze'], 'n': res['n'],
                      'matched': res['matched'],
                      'matched_classes': res.get('matched_classes'),
                      'matched_combos': res.get('matched_combos'),
                      'distinct_decisions': res['distinct_decisions'],
                      'bindings_false': res['bindings_false'],
                      'met_target': res['met_target'],
                      'met_target_consistent': res['met_target_consistent'],
                      'counter_sha256': res.get('counter_sha256'),
                      'exit_code': res['exit_code']}, sort_keys=True))
    if a.json_out:
        d = os.path.dirname(os.path.abspath(a.json_out))
        os.makedirs(d, exist_ok=True)
        with open(a.json_out, 'w') as f:
            json.dump(res, f, indent=1, sort_keys=True)
    return res['exit_code']


def _safe_rev(root, rev):
    try:
        return full_rev(root, rev)
    except Exception:
        return None


# ---------------------------------------------------------------- selftest stubs
STUB_GEN = r'''#!/usr/bin/env python3
import argparse, hashlib, json, os
DEC = {
    'clean-be': ('clean', 'none'), 'clean-le': ('clean', 'none'),
    'clean-empty': ('clean-empty', 'confirm-empty'),
    'escaping-symlink-removed': ('escaping-symlink-removed', 'expect-link-absent'),
    'in-tree-symlink-metadata': ('in-tree-symlink-metadata', 'count-gap'),
    'mixed-symlinks': ('mixed-symlinks', 'audit-symlinks'),
    'dep-missing-be': ('dep-missing-be', 'install-extractor-be'),
    'dep-missing-le': ('dep-missing-le', 'install-extractor-le'),
    'avm-marker-be-dropped': ('avm-marker-be-dropped', 'wrap-extractor-be'),
    'body-extractor-failure': ('body-extractor-failure', 'preserve-failure'),
    'body-extractor-failure-le': ('body-extractor-failure', 'preserve-failure'),
    'partial-body-failure': ('partial-body-failure', 'salvage-partial'),
    'no-squashfs-chunk': ('no-squashfs-chunk', 'inspect-input'),
    'out-of-domain': ('unclassified', 'none'),
    'depth-limited-alone': ('depth-limited', 'raise-depth'),
    'depth-limited-in-tree': ('depth-limited', 'raise-depth'),
    'depth-limited-mixed': ('depth-limited', 'raise-depth'),
    'failure-depth-limited': ('body-extractor-failure', 'preserve-failure'),
    'legacy-clean-v1': ('clean', 'none'),
    'legacy-clean-v2': ('clean', 'none'),
    'legacy-clean-v3-le': ('clean', 'none'),
    'legacy-body-failure-v3': ('legacy-body-failure', 'cross-read-legacy'),
    'legacy-partial-v3': ('partial-body-failure', 'salvage-partial'),
    'combo': ('clean', 'none'),
}
FEATURES = {
    'clean-be': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': [],
                 'gap_dependencies': [], 'be_argv': 'no',
                 'symlink_removed': False, 'published': '>0',
                 'extraction_failed': False},
    'clean-le': {'handler_set': ['squashfs_v4_le'], 'gap_kinds': [],
                 'gap_dependencies': [], 'be_argv': 'no',
                 'symlink_removed': False, 'published': '>0',
                 'extraction_failed': False},
    'clean-empty': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': [],
                    'gap_dependencies': [], 'be_argv': 'n/a',
                    'symlink_removed': False, 'published': '0',
                    'extraction_failed': False},
    'escaping-symlink-removed': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': [],
                                 'gap_dependencies': [], 'be_argv': 'n/a',
                                 'symlink_removed': True, 'published': '>0',
                                 'extraction_failed': False},
    'in-tree-symlink-metadata': {'handler_set': ['squashfs_v4_be'],
                                 'gap_kinds': ['unpublished-entry'],
                                 'gap_dependencies': [], 'be_argv': 'n/a',
                                 'symlink_removed': False, 'published': '>0',
                                 'extraction_failed': False},
    'mixed-symlinks': {'handler_set': ['squashfs_v4_be'],
                       'gap_kinds': ['unpublished-entry'],
                       'gap_dependencies': [], 'be_argv': 'n/a',
                       'symlink_removed': True, 'published': '>0',
                       'extraction_failed': False},
    'dep-missing-be': {'handler_set': ['squashfs_v4_be'],
                       'gap_kinds': ['missing-extractor-dependency'],
                       'gap_dependencies': ['sasquatch-v4be'], 'be_argv': 'n/a',
                       'symlink_removed': False, 'published': '0',
                       'extraction_failed': False},
    'dep-missing-le': {'handler_set': ['squashfs_v4_le'],
                       'gap_kinds': ['missing-extractor-dependency'],
                       'gap_dependencies': ['sasquatch'], 'be_argv': 'n/a',
                       'symlink_removed': False, 'published': '0',
                       'extraction_failed': False},
    'avm-marker-be-dropped': {'handler_set': ['squashfs_v4_be'],
                              'gap_kinds': ['extractor-failure'],
                              'gap_dependencies': [], 'be_argv': 'no',
                              'symlink_removed': False, 'published': '0',
                              'extraction_failed': True},
    'body-extractor-failure': {'handler_set': ['squashfs_v4_be'],
                               'gap_kinds': ['extractor-failure'],
                               'gap_dependencies': [], 'be_argv': 'yes',
                               'symlink_removed': False, 'published': '0',
                               'extraction_failed': True},
    'body-extractor-failure-le': {'handler_set': ['squashfs_v4_le'],
                                  'gap_kinds': ['extractor-failure'],
                                  'gap_dependencies': [], 'be_argv': 'no',
                                  'symlink_removed': False, 'published': '0',
                                  'extraction_failed': True},
    'partial-body-failure': {'handler_set': ['squashfs_v4_be'],
                             'gap_kinds': ['extractor-failure'],
                             'gap_dependencies': [], 'be_argv': 'yes',
                             'symlink_removed': False, 'published': '>0',
                             'extraction_failed': True},
    'no-squashfs-chunk': {'handler_set': [], 'gap_kinds': [],
                          'gap_dependencies': [], 'be_argv': 'n/a',
                          'symlink_removed': False, 'published': '0',
                          'extraction_failed': False},
    'out-of-domain': {'handler_set': ['squashfs_v4_be'], 'gap_kinds': [],
                      'gap_dependencies': [], 'be_argv': 'n/a',
                      'symlink_removed': False, 'published': '>0',
                      'extraction_failed': False},
    'depth-limited-alone': {'handler_set': ['squashfs_v4_be'],
                            'gap_kinds': ['depth-limited'],
                            'gap_dependencies': [], 'be_argv': 'n/a',
                            'symlink_removed': False, 'published': '>0',
                            'extraction_failed': False},
    'depth-limited-in-tree': {'handler_set': ['squashfs_v4_be'],
                              'gap_kinds': ['depth-limited', 'unpublished-entry'],
                              'gap_dependencies': [], 'be_argv': 'n/a',
                              'symlink_removed': False, 'published': '>0',
                              'extraction_failed': False},
    'depth-limited-mixed': {'handler_set': ['squashfs_v4_be'],
                            'gap_kinds': ['depth-limited', 'unpublished-entry'],
                            'gap_dependencies': [], 'be_argv': 'n/a',
                            'symlink_removed': True, 'published': '>0',
                            'extraction_failed': False},
    'failure-depth-limited': {'handler_set': ['squashfs_v4_be'],
                              'gap_kinds': ['extractor-failure', 'depth-limited'],
                              'gap_dependencies': [], 'be_argv': 'yes',
                              'symlink_removed': False, 'published': '0',
                              'extraction_failed': True},
    'legacy-clean-v1': {'handler_set': ['squashfs_v1'], 'gap_kinds': [],
                        'gap_dependencies': [], 'be_argv': 'no',
                        'symlink_removed': False, 'published': '>0',
                        'extraction_failed': False},
    'legacy-clean-v2': {'handler_set': ['squashfs_v2'], 'gap_kinds': [],
                        'gap_dependencies': [], 'be_argv': 'no',
                        'symlink_removed': False, 'published': '>0',
                        'extraction_failed': False},
    'legacy-clean-v3-le': {'handler_set': ['squashfs_v3'], 'gap_kinds': [],
                           'gap_dependencies': [], 'be_argv': 'no',
                           'symlink_removed': False, 'published': '>0',
                           'extraction_failed': False},
    'legacy-body-failure-v3': {'handler_set': ['squashfs_v3'],
                               'gap_kinds': ['extractor-failure'],
                               'gap_dependencies': [], 'be_argv': 'no',
                               'symlink_removed': False, 'published': '0',
                               'extraction_failed': True},
    'legacy-partial-v3': {'handler_set': ['squashfs_v3'],
                          'gap_kinds': ['extractor-failure'],
                          'gap_dependencies': [], 'be_argv': 'no',
                          'symlink_removed': False, 'published': '>0',
                          'extraction_failed': True},
    'combo': {'handler_set': ['squashfs_v3', 'squashfs_v4_le'],
              'gap_kinds': ['depth-limited'], 'gap_dependencies': [],
              'be_argv': 'n/a', 'symlink_removed': False, 'published': '>0',
              'extraction_failed': False},
}
KEY = '@@GENKEY@@'
ap = argparse.ArgumentParser()
ap.add_argument('--seed', required=True)
ap.add_argument('--out', required=True)
ap.add_argument('--classes')
ap.add_argument('--combos', type=int, default=24)
ap.add_argument('--arm', default='heldout')
ap.add_argument('--verify', action='store_true')
ap.add_argument('--selftest', action='store_true')
a = ap.parse_args()
classes = [c for c in a.classes.split(',') if c] if a.classes else [
    c for c in DEC if c != 'combo']


def env_for(f, digest, stub_class, fail_all=None):
    failing = bool(f['extraction_failed']) if fail_all is None else fail_all
    chunks = [{'handler': h, 'extraction_failed': failing and i == 0}
              for i, h in enumerate(f['handler_set'])]
    gaps = []
    for k in f['gap_kinds']:
        gaps.append({'kind': k, 'dependencies': list(f['gap_dependencies'])
                     if k == 'missing-extractor-dependency' else []})
    diags = []
    if f['be_argv'] in ('yes', 'no') and f['handler_set']:
        diags.append({'report': {'__typename__': 'CommandReport',
                                 'command': ['sasquatch']
                                 + (['-be'] if f['be_argv'] == 'yes' else [])
                                 + ['-d', 'out', 'in.sqsh']}})
    if f['symlink_removed']:
        diags.append({'report': {'__typename__': 'MaliciousSymlinkRemoved',
                                 'path': 'etc/x', 'target': '../../etc/passwd'}})
    op = 'analyze' if stub_class == 'out-of-domain' else 'extract_firmware'
    return {'subject': {'name': 'carrier.sqsh',
                        'digest': {'sha256': digest}, 'format': 'file',
                        'architecture': None, 'local_path': '/dev/null'},
            'operation': op, 'provider': {'id': 'unblob'},
            'normalized_result': {'chunks': chunks, 'extraction_gaps': gaps,
                                  'files': [{'path': 'f%d' % i}
                                            for i in range(2 if f['published'] == '>0' else 0)],
                                  'diagnostics': diags},
            'stub_class': stub_class}


os.makedirs(a.out, exist_ok=True)
out = []


def emit(ident, cls, f, stub_class, arm):
    h = hashlib.sha256(('@@SALT@@:%s:%s' % (a.seed, ident)).encode()).hexdigest()
    body = h.encode() + b'\n' + bytes.fromhex(h) * 4
    d = os.path.join(a.out, ident)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'carrier.sqsh'), 'wb') as fh:
        fh.write(body)
    sha = hashlib.sha256(body).hexdigest()
    with open(os.path.join(d, 'envelope.json'), 'w') as fh:
        json.dump(env_for(f, sha, stub_class), fh, indent=1, sort_keys=True)
        fh.write('\n')
    entry = {'id': ident, 'class': cls, 'arm': arm,
             'carrier': ident + '/carrier.sqsh',
             'envelope': ident + '/envelope.json', 'sha256': sha}
    entry[KEY] = dict(f)
    out.append(entry)


if a.arm == 'dev':
    for i, cls in enumerate(classes):
        emit('D%02d' % (i + 1), cls, FEATURES[cls], cls, 'after')
else:
    for ci, cls in enumerate(classes):
        f = FEATURES[cls]
        for k in range(2):
            emit('H%02d' % (ci * 2 + k + 1), cls, f, cls,
                 'ood' if cls == 'out-of-domain' else 'after')
    for j in range(a.combos):
        emit('C%02d' % (j + 1), 'combo', FEATURES['combo'], 'combo', 'after')
man = {'seed': a.seed,
       'generator': {'name': 'heldout-gen-v4.py', 'version': 'r42-c2-stub',
                     'sha256': hashlib.sha256(
                         open(os.path.abspath(__file__), 'rb').read()).hexdigest()},
       'classes': classes + (['combo'] if a.combos else []),
       'combo_count': a.combos,
       'carriers': out}
@@WRITER@@
with open(os.path.join(a.out, 'manifest.json'), 'w') as fh:
    json.dump(man, fh, indent=1, sort_keys=True)
'''

STUB_EVAL = r'''#!/usr/bin/env python3
import argparse, json, os, sys
MODE = '@@EMODE@@'
DEC = {
    'clean-be': ('clean', 'none'), 'clean-le': ('clean', 'none'),
    'clean-empty': ('clean-empty', 'confirm-empty'),
    'escaping-symlink-removed': ('escaping-symlink-removed', 'expect-link-absent'),
    'in-tree-symlink-metadata': ('in-tree-symlink-metadata', 'count-gap'),
    'mixed-symlinks': ('mixed-symlinks', 'audit-symlinks'),
    'dep-missing-be': ('dep-missing-be', 'install-extractor-be'),
    'dep-missing-le': ('dep-missing-le', 'install-extractor-le'),
    'avm-marker-be-dropped': ('avm-marker-be-dropped', 'wrap-extractor-be'),
    'body-extractor-failure': ('body-extractor-failure', 'preserve-failure'),
    'body-extractor-failure-le': ('body-extractor-failure', 'preserve-failure'),
    'partial-body-failure': ('partial-body-failure', 'salvage-partial'),
    'no-squashfs-chunk': ('no-squashfs-chunk', 'inspect-input'),
    'out-of-domain': ('unclassified', 'none'),
    'depth-limited-alone': ('depth-limited', 'raise-depth'),
    'depth-limited-in-tree': ('depth-limited', 'raise-depth'),
    'depth-limited-mixed': ('depth-limited', 'raise-depth'),
    'failure-depth-limited': ('body-extractor-failure', 'preserve-failure'),
    'legacy-clean-v1': ('clean', 'none'),
    'legacy-clean-v2': ('clean', 'none'),
    'legacy-clean-v3-le': ('clean', 'none'),
    'legacy-body-failure-v3': ('legacy-body-failure', 'cross-read-legacy'),
    'legacy-partial-v3': ('partial-body-failure', 'salvage-partial'),
    'combo': ('clean', 'none'),
    'dev-mismatch': ('clean', 'none'),
}
ap = argparse.ArgumentParser()
ap.add_argument('--envelopes')
ap.add_argument('--json', action='store_true')
ap.add_argument('--format')
ap.add_argument('--json-out')
ap.add_argument('--out')
ap.add_argument('--selftest', action='store_true')
a = ap.parse_args()
OUT = a.out or a.json_out
if MODE == 'fail':
    sys.stderr.write('boom\n')
    sys.exit(3)
out = {}
for n in sorted(os.listdir(a.envelopes or '.')):
    if not n.endswith('.json') or n == 'manifest.json':
        continue
    ident = n[:-5]
    d = json.load(open(os.path.join(a.envelopes, n)))
    if isinstance(d, dict) and 'subject' not in d and isinstance(d.get('data'), dict):
        d = d['data']
    cls = d.get('stub_class')
    lab, act = DEC.get(cls, ('unclassified', 'none'))
    if MODE == 'disagree_action' and ident == 'H01':
        act = 'confirm-empty'
    if MODE == 'disagree_label' and ident == 'H01':
        lab, act = 'unclassified', 'none'
    if MODE == 'omit' and ident == 'H02':
        continue
    if MODE == 'real_disagree' and ident == 'V3':
        lab, act = 'clean', 'none'
    out[ident] = {'label': lab, 'action': act}
if MODE == 'garbage':
    print('not json at all')
    sys.exit(0)
if MODE == 'list':
    doc = [{'envelope': k, 'label': v['label'], 'action': v['action']}
           for k, v in sorted(out.items())]
elif MODE == 'wrapped':
    doc = {'labels': out}
else:
    doc = out
if MODE == 'file':
    for k, v in sorted(out.items()):
        print('%s\t%s\t%s' % (k, v['label'], v['action']))
    if OUT:
        with open(OUT, 'w') as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
    sys.exit(0)
print(json.dumps(doc, indent=1, sort_keys=True))
'''

STUB_INTERP = r'''#!/usr/bin/env python3
import argparse, fnmatch, json, sys
MODE = '@@MODE@@'
ap = argparse.ArgumentParser()
ap.add_argument('--skill')
ap.add_argument('--json', action='store_true')
ap.add_argument('--table-only', action='store_true')
ap.add_argument('--envelopes')
ap.add_argument('envs', nargs='*')
a = ap.parse_args()
if MODE == 'fail':
    sys.exit(1)
if MODE == 'dir' and a.envs:
    sys.exit(9)
lines = open(a.skill).read().splitlines()
start = next((i for i, l in enumerate(lines) if l.startswith('## Queue-drain craft')), None)
if start is None:
    sys.exit(2)
end = len(lines)
for i in range(start + 1, len(lines)):
    if lines[i].startswith('## '):
        end = i
        break
sec = lines[start + 1:end]
mi = next((i for i, l in enumerate(sec) if '<!-- sqfs-triage-table v4 -->' in l), None)
if mi is None:
    sys.exit(2)
ti = next((i for i in range(mi + 1, len(sec)) if sec[i].lstrip().startswith('|')), None)
if ti is None:
    sys.exit(2)
rows = []
for l in sec[ti:]:
    if not l.lstrip().startswith('|'):
        break
    rows.append([c.strip().strip('`').strip() for c in l.strip().strip('|').split('|')])
if len(rows) < 2:
    sys.exit(2)
head = [c.strip().strip('`').strip().lower() for c in rows[0]]
def idx(name):
    return head.index(name) if name in head else None
CY, CA, CM = idx('label'), idx('action'), idx('cause')
if CY is None or CM is None:
    sys.exit(2)
body = rows[2:]
if a.table_only:
    if MODE == 'blind':
        sys.exit(2)
    off = 1 if MODE == 'rowonly1' else 0
    for i, cells in enumerate(body):
        print('%d. %s' % (i + off, cells[CY]))
    sys.exit(0)
envs = list(a.envs)
if not envs and a.envelopes:
    import os
    envs = [os.path.join(a.envelopes, n) for n in sorted(os.listdir(a.envelopes))
            if n.endswith('.json')]
res = []
for p in envs:
    d = json.load(open(p))
    if isinstance(d, dict) and 'subject' not in d and isinstance(d.get('data'), dict):
        d = d['data']
    cls = d.get('stub_class')
    hit = None
    for i, cells in enumerate(body):
        pat = cells[CM] if CM < len(cells) else '*'
        pats = [x.strip() for x in pat.split(',') if x.strip()]
        if '*' in pats or (cls is not None
                           and any(fnmatch.fnmatchcase(cls, x) for x in pats)):
            hit = i
            break
    cells = body[hit] if hit is not None else None
    res.append({'path': p,
                'label': cells[CY] if cells else 'unclassified',
                'action': (cells[CA] if CA is not None and CA < len(cells) else 'none')
                if cells else 'none',
                'rule': hit, 'row': cells})
if MODE == 'rowonly':
    for r in res:
        if r['rule'] is not None:
            r.pop('label', None)
            r.pop('action', None)
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if MODE == 'rowonly1':
    for r in res:
        if r['rule'] is not None:
            r.pop('label', None)
            r.pop('action', None)
        r.pop('row', None)
        r['rule'] = None if r['rule'] is None else r['rule'] + 1
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if MODE == 'blind':
    for r in res:
        for k in ('rule', 'row', 'label', 'action'):
            r.pop(k, None)
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if MODE == 'norow':
    for r in res:
        r.pop('rule', None)
        r.pop('row', None)
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
if a.json or MODE == 'json':
    json.dump({'results': res}, sys.stdout, indent=1, sort_keys=True)
    sys.stdout.write('\n')
    sys.exit(0)
for r in res:
    if MODE == 'tab3':
        print('%s\t%s\t%s' % (r['path'], r['label'], r['action']))
    else:
        print('%s\t%s\t%s\t%s' % (r['path'], r['label'], r['action'], r['rule']))
'''


# ---------------------------------------------------------------- selftest
def selftest():
    sroot = os.path.join(os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir(),
                         'kaidoku-r42')
    os.makedirs(sroot, exist_ok=True)
    fails = []

    HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler',
              'gap kinds', 'dependencies', '-be in child argv',
              'symlink removed', 'published files', 'action', 'cause', 'source']
    ACTIONS = ['none', 'inspect-input', 'install-extractor-be',
               'install-extractor-le', 'wrap-extractor-be', 'preserve-failure',
               'salvage-partial', 'raise-depth', 'audit-symlinks',
               'expect-link-absent', 'count-gap', 'confirm-empty',
               'cross-read-legacy']

    def row(label, action, match, handler='`*`', source='`corpus/k.md:1-1`',
            failing='`*`'):
        return ['`%s`' % label, '`extract_firmware`', '`unblob`', handler,
                failing, '`*`', '`*`', '`*`', '`*`', '`*`', '`%s`' % action,
                match, source]

    ROWS = [
        row('no-squashfs-chunk', 'inspect-input', 'no-squashfs-*',
            handler='`none`'),
        row('dep-missing-be', 'install-extractor-be', 'dep-missing-be'),
        row('dep-missing-le', 'install-extractor-le',
            'dep-missing-le,legacy-dep-missing-*'),
        row('partial-body-failure', 'salvage-partial',
            'partial-*,legacy-partial-*'),
        row('avm-marker-be-dropped', 'wrap-extractor-be', 'avm-*'),
        row('legacy-body-failure', 'cross-read-legacy', 'legacy-body-*'),
        row('body-extractor-failure', 'preserve-failure', 'body-*,failure-*'),
        row('depth-limited', 'raise-depth', 'depth-*'),
        row('mixed-symlinks', 'audit-symlinks', 'mixed-*'),
        row('escaping-symlink-removed', 'expect-link-absent', 'escaping-*'),
        row('in-tree-symlink-metadata', 'count-gap', 'in-tree-*'),
        row('clean', 'none', 'clean-be,clean-le,legacy-clean-v1,legacy-clean-v2,'
                              'legacy-clean-v3-le,combo*'),
        row('clean-empty', 'confirm-empty', 'clean-empty'),
    ]
    # order matters: clean-empty before the clean catch-all
    ROWS = [ROWS[0], ROWS[1], ROWS[2], ROWS[3], ROWS[4], ROWS[5], ROWS[6],
            ROWS[7], ROWS[8], ROWS[9], ROWS[10], ROWS[12], ROWS[11]]

    CLASSES = ['clean-be', 'clean-le', 'clean-empty', 'escaping-symlink-removed',
               'in-tree-symlink-metadata', 'mixed-symlinks', 'dep-missing-be',
               'dep-missing-le', 'avm-marker-be-dropped',
               'body-extractor-failure', 'body-extractor-failure-le',
               'partial-body-failure', 'no-squashfs-chunk', 'out-of-domain',
               'depth-limited-alone', 'depth-limited-in-tree',
               'depth-limited-mixed', 'failure-depth-limited',
               'legacy-clean-v1', 'legacy-clean-v2', 'legacy-clean-v3-le',
               'legacy-body-failure-v3', 'legacy-partial-v3']

    LOOKUP_ROWS = [
        row('clean', 'none', 'clean-be,clean-le'),
        row('clean-empty', 'confirm-empty', 'clean-empty'),
        row('depth-limited', 'raise-depth', 'depth-*'),
        row('legacy-body-failure', 'cross-read-legacy', 'legacy-body-*'),
        row('partial-body-failure', 'salvage-partial',
            'partial-*,legacy-partial-*'),
        row('no-squashfs-chunk', 'inspect-input', 'no-squashfs-*',
            handler='`none`'),
    ]
    # a lookup table that hits every combo (the round-41 kill-rule shape)
    LOOKUP_FULL = [row('clean', 'none', '*')]

    def table_text(rows, header=None):
        header = header or HEADER
        sep = '|' + '---|' * len(header)
        return '\n'.join(['| ' + ' | '.join(header) + ' |', sep]
                         + ['| ' + ' | '.join(r) + ' |' for r in rows])

    def block(rows, actions=ACTIONS, header=None):
        acts = '  <!-- sqfs-triage-actions: %s -->' % ' '.join(actions) \
            if actions is not None else ''
        return '\n'.join([x for x in ['<!-- sqfs-triage-table v4 -->', acts,
                                      '  ' + table_text(rows, header).replace('\n', '\n  ')]
                          if x])

    def skill_doc(block_text, prose='- **SquashFS outcome triage v4 (round 42).** text'):
        s = '# K\n\n## Queue-drain craft (x)\n\n- **rule** text\n\n'
        if block_text is not None:
            s += prose + '\n\n'
            if QUOTES:
                s += ('- **triage v4 (round 42).** reads only the '
                      '`<!-- sqfs-triage-table v4 -->` block\n\n')
            s += block_text + '\n\n'
        return s + '## Next\n\n- other\n'

    def lookup_doc(rows, v3=False):
        text = ('# CTL-C2-7-lookup (control)\n\n## Queue-drain craft\n\n'
                + block(rows) + '\n\n## End\n')
        if v3:
            text = text.replace('<!-- sqfs-triage-table v4 -->',
                                '<!-- sqfs-triage-table v3 -->')
        return text

    QUOTES = False

    def write_tree(d, tree):
        for p, c in tree.items():
            fp = os.path.join(d, p)
            os.makedirs(os.path.dirname(fp) or d, exist_ok=True)
            with open(fp, 'wb') as f:
                f.write(c if isinstance(c, bytes) else c.encode())

    def commit(d, tree, msg='x'):
        write_tree(d, tree)
        subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx',
                        'commit', '-qm', msg, '--allow-empty'], check=True)
        return subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()

    def build(params):
        d = tempfile.mkdtemp(prefix='c2v4.', dir=sroot)
        subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
        top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'],
                             capture_output=True, text=True).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise SystemExit('fixture toplevel mismatch')
        commit(d, {SKILL: skill_doc(None), CLAIMS: '# claims (draft)\n'}, 'base')
        global QUOTES
        QUOTES = bool(params.get('marker_quoted'))
        imode = params.get('mode', 'json')
        emode = params.get('emode', 'ok')
        btext = params.get('block') if 'block' in params else block(
            params.get('rows', ROWS), params.get('actions', ACTIONS),
            params.get('header'))
        if params.get('skill_mode') == 'v3':
            btext = block(params.get('rows', ROWS), params.get('actions', ACTIONS),
                          params.get('header')).replace(
                              '<!-- sqfs-triage-table v4 -->',
                              '<!-- sqfs-triage-table v3 -->')
        writer_decl = params.get('writer_decl', '')
        gen_src = STUB_GEN.replace('@@WRITER@@', writer_decl) \
            .replace('@@GENKEY@@', params.get('genkey', 'declared_features')) \
            .replace('@@SALT@@', params.get('salt', 'x'))
        lookup_text = lookup_doc(params.get('lookup_rows', LOOKUP_ROWS),
                                 v3=bool(params.get('lookup_v3')))
        tool_tree = {
            SKILL: skill_doc(btext, params.get('prose',
                                              '- **SquashFS outcome triage v4 (round 42).** text')),
            INTERP: STUB_INTERP.replace('@@MODE@@', imode),
            EVAL: STUB_EVAL.replace('@@EMODE@@', emode),
            GEN: gen_src,
            COUNTER: '# counter\n',
            LOOKUP: lookup_text,
            CLAIMS: '# claims (frozen)\n',
            'tools/round-41/gen-squashfs.py': '# round-41 writer\n',
            'tools/round-40/gen-squashfs.py': '# round-40 writer\n',
        }
        claim = params.get('claim', 'after')
        muts = params.get('muts', set())
        freeze = commit(d, tool_tree, 'freeze')
        if claim == 'none':
            return d, freeze, freeze
        seed = '0' * 64 if params.get('seed') == 'zero' else freeze
        gdir = tempfile.mkdtemp(prefix='gen.', dir=sroot)
        gpath = os.path.join(d, GEN)
        classes = params.get('classes', CLASSES)
        gargs = [sys.executable, '-I', '-B', gpath, '--seed', seed, '--out', gdir,
                 '--classes', ','.join(classes)]
        if 'combos' in params:
            gargs += ['--combos', str(params['combos'])]
        pr = subprocess.run(gargs, capture_output=True, text=True)
        if pr.returncode != 0:
            raise SystemExit('stub generator failed: ' + pr.stderr)
        with open(os.path.join(gdir, 'manifest.json')) as fh:
            rman = json.load(fh)
        man = {'seed': seed, 'generator': GEN,
               'classes': [c for c in rman['classes']
                           if c in classes or c == 'combo'],
               'combo_count': params.get('combos', 24),
               'carriers': []}
        if params.get('gen_obj'):
            man['generator'] = {
                'name': 'heldout-gen-v4.py', 'version': 'r42-c2-stub',
                'sha256': hashlib.sha256(gen_src.encode()).hexdigest()
                if params.get('gen_obj') == 'good' else 'f' * 64}
            if params.get('writer_path') is not None:
                man['generator']['writer'] = {
                    'name': 'gen-squashfs.py',
                    'path': params['writer_path'],
                    'sha256': params.get('writer_sha')}
        claim_files = {}
        sha_by_id = {c['id']: c['sha256'] for c in rman['carriers']}
        for c in rman['carriers']:
            if c['class'] not in classes and c['class'] != 'combo':
                continue
            cid = c['id']
            with open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb') as fh:
                body = fh.read()
            if 'carrier_corrupt' in muts and cid == 'H01':
                body += b'X'
            base = MANIFEST_DIR + '/' + cid
            claim_files[base + '/carrier.sqsh'] = body
            digest = c['sha256']
            if 'digest_mismatch' in muts and cid == 'H01':
                digest = '0' * 64
            if 'swap_digest' in muts and cid == 'H01':
                digest = sha_by_id.get('H02', c['sha256'])
            df = c.get('declared_features') or {}
            chunks = [{'handler': h,
                       'extraction_failed': df.get('extraction_failed') in (True, 'yes')}
                      for h in (df.get('handler_set') or [])]
            gaps = []
            for k in (df.get('gap_kinds') or []):
                g = {'kind': k,
                     'dependencies': list(df.get('gap_dependencies') or [])
                     if k == 'missing-extractor-dependency' else []}
                if k == 'extractor-failure' and chunks:
                    g['handler'] = chunks[0]['handler']
                gaps.append(g)
            diags = []
            if df.get('be_argv') in ('yes', 'no') and chunks:
                diags.append({'report': {'__typename__': 'CommandReport',
                                         'command': ['sasquatch']
                                         + (['-be'] if df.get('be_argv') == 'yes' else [])
                                         + ['-d', 'out', 'in.sqsh']}})
            if df.get('symlink_removed') in (True, 'yes'):
                diags.append({'report': {'__typename__': 'MaliciousSymlinkRemoved',
                                         'path': 'etc/x',
                                         'target': '../../etc/passwd'}})
            nfiles = 2 if str(df.get('published')) in ('>0', 'nonzero', 'True') \
                else 0
            env = {'subject': {'name': 'carrier.sqsh',
                               'digest': {'sha256': digest},
                               'format': 'file', 'architecture': None,
                               'local_path': '/dev/null'},
                   'operation': 'analyze' if c['class'] == 'out-of-domain'
                   else 'extract_firmware',
                   'provider': {'id': 'unblob'},
                   'normalized_result': {
                       'extraction_gaps': gaps,
                       'files': [{'path': 'f%d' % i} for i in range(nfiles)],
                       'chunks': chunks,
                       'diagnostics': diags},
                   'stub_class': c['class']}
            if 'feat_env' in muts and cid == 'H01':
                env['normalized_result']['extraction_gaps'] = [
                    {'kind': 'unpublished-entry', 'dependencies': []}]
            if 'missing_envelope' in muts and cid == 'H02':
                pass
            else:
                blob = {'ok': True, 'data': env, 'meta': {'cli': 'rea-agents@6.5.0'}} \
                    if 'full_envelope' in muts else env
                claim_files[base + '/envelope.json'] = json.dumps(
                    blob, indent=1, sort_keys=True)
            entry = dict(c)
            if 'lane_relative_paths' in muts:
                entry['carrier'] = base + '/carrier.sqsh'
            if 'omit_envelope' not in muts:
                entry['envelope'] = (base + '/envelope.json') \
                    if 'lane_relative_paths' in muts else (cid + '/envelope.json')
            if 'combo_feat_mismatch' in muts and cid == 'C01':
                entry['declared_features'] = dict(entry['declared_features'],
                                                  gap_kinds=['zzz-not-a-kind'])
            if 'feat_mismatch' in muts and cid == 'H01':
                entry['declared_features'] = dict(entry['declared_features'],
                                                  gap_kinds=['zzz-not-a-kind'])
            if 'feat_absent' in muts and cid == 'H01':
                entry.pop('declared_features', None)
            if 'share_carrier_path' in muts and cid == 'H02':
                entry['carrier'] = 'H01/carrier.sqsh'
            if 'no_dev_dir' not in muts and c['class'].startswith('legacy-') \
                    and cid in ('H01',):
                pass
            man['carriers'].append(entry)
        for rname in ('V3', 'V4', 'L3', 'L4'):
            if 'receipt_missing' in muts and rname == 'V4':
                continue
            rcls = 'clean-be' if ('receipt_wrong_class' in muts
                                  and rname == 'L3') else 'depth-limited-alone'
            claim_files['corpus/evidence/round-41/c1/%s/after.json' % rname] = \
                json.dumps({'ok': True,
                            'data': {'subject': {'name': 'chunk_extract',
                                                 'digest': {'sha256': '0' * 64},
                                                 'format': 'dir',
                                                 'architecture': None,
                                                 'local_path': '/dev/null'},
                                     'operation': 'extract_firmware',
                                     'provider': {'id': 'unblob'},
                                     'normalized_result': {
                                         'extraction_gaps': [{'kind': 'depth-limited',
                                                              'dependencies': []}],
                                         'files': [{'path': 'a'}],
                                         'chunks': [{'handler': 'squashfs_v4_be',
                                                     'extraction_failed': False}],
                                         'diagnostics': []},
                                     'stub_class': rcls},
                            'meta': {'cli': 'rea-agents@6.5.0'}},
                           indent=1, sort_keys=True)
        # ---- round-42 dev arm
        if 'no_dev_dir' not in muts:
            ddir = tempfile.mkdtemp(prefix='dev.', dir=sroot)
            dcls = ['legacy-clean-v1', 'legacy-clean-v2', 'legacy-clean-v3-le',
                    'legacy-body-failure-v3', 'legacy-partial-v3']
            if 'dev_short' in muts:
                dcls = dcls[:2]
            dargs = [sys.executable, '-I', '-B', gpath, '--seed', 'dev' * 13,
                     '--out', ddir, '--arm', 'dev', '--classes', ','.join(dcls)]
            pr = subprocess.run(dargs, capture_output=True, text=True)
            if pr.returncode != 0:
                raise SystemExit('stub dev generator failed: ' + pr.stderr)
            for n in sorted(os.listdir(ddir)):
                sub = os.path.join(ddir, n)
                if not os.path.isdir(sub):
                    continue
                for fn in ('carrier.sqsh', 'envelope.json'):
                    with open(os.path.join(sub, fn), 'rb') as fh:
                        blob = fh.read()
                    if fn == 'envelope.json' and 'dev_mismatch' in muts \
                            and n == 'D01':
                        blob = blob.replace(b'"stub_class": "legacy-clean-v1"',
                                            b'"stub_class": "dev-mismatch"')
                    claim_files[DEV_DIRS[0] + '/' + n + '/' + fn] = blob
            with open(os.path.join(ddir, 'manifest.json'), 'rb') as fh:
                claim_files[DEV_DIRS[0] + '/manifest.json'] = fh.read()
        if 'class_count3' in muts:
            body = claim_files[MANIFEST_DIR + '/H01/carrier.sqsh']
            claim_files[MANIFEST_DIR + '/H99/carrier.sqsh'] = body
            claim_files[MANIFEST_DIR + '/H99/envelope.json'] = \
                claim_files[MANIFEST_DIR + '/H01/envelope.json']
            man['carriers'].append({'id': 'H99', 'class': 'clean-be',
                                    'arm': 'after',
                                    'carrier': 'H99/carrier.sqsh',
                                    'sha256': hashlib.sha256(body).hexdigest(),
                                    'envelope': 'H99/envelope.json',
                                    'declared_features': {
                                        'handler_set': ['squashfs_v4_be'],
                                        'gap_kinds': [], 'gap_dependencies': [],
                                        'be_argv': 'no', 'symlink_removed': False,
                                        'published': '>0',
                                        'extraction_failed': False}})
        man_text = json.dumps(man, indent=1, sort_keys=True)
        if 'bad_manifest' in muts:
            man_text = man_text.rstrip()[:-3]
        post = {}
        if 'edit_skill' in muts:
            post[SKILL] = skill_doc(block(ROWS + [row('extra', 'none', 'extra')]))
        if 'edit_actions' in muts:
            post[SKILL] = skill_doc(block(ROWS, ACTIONS[:-1]))
        if 'edit_prose' in muts:
            post[SKILL] = skill_doc(btext, '- **SquashFS outcome triage v4 (round 42). EDITED**')
        if 'edit_lookup' in muts:
            post[LOOKUP] = lookup_doc(LOOKUP_ROWS + [row('clean', 'none', 'zzz')])
        if 'edit_evidence' in muts:
            post[MANIFEST] = man_text.replace('"seed"', '"seed_extra": 1, "seed"')
        for m, p in (('edit_interp', INTERP), ('edit_gen', GEN), ('edit_eval', EVAL),
                     ('edit_claims', CLAIMS), ('edit_counter', COUNTER),
                     ('edit_writer41', 'tools/round-41/gen-squashfs.py'),
                     ('edit_writer40', 'tools/round-40/gen-squashfs.py')):
            if m in muts:
                cur = tool_tree[p]
                post[p] = cur + ('\n# edited after freeze\n' if isinstance(cur, str)
                                 else b'#x\n')
        if claim == 'after':
            tree = dict(claim_files)
            tree[MANIFEST] = man_text
            tree.update(post)
            rev = commit(d, tree, 'claim data')
        elif claim == 'split':
            commit(d, dict(claim_files), 'carriers and envelopes')
            tree = {MANIFEST: man_text}
            tree.update(post)
            rev = commit(d, tree, 'manifest')
        elif claim in ('restore',):
            tree = dict(claim_files)
            tree[MANIFEST] = man_text
            tree[SKILL] = skill_doc(block(ROWS + [row('extra', 'none', 'extra')]))
            commit(d, tree, 'claim data + mutated block')
            rev = commit(d, {SKILL: tool_tree[SKILL]}, 'restore the block')
        elif claim == 'evidence_rewrite':
            tree = dict(claim_files)
            tree[MANIFEST] = man_text
            commit(d, tree, 'claim data')
            rev = commit(d, {MANIFEST: man_text.replace(
                '"seed"', '"seed_rewritten": 1, "seed"')}, 'rewrite evidence')
        elif claim == 'befreeze':
            commit(d, dict(claim_files), 'claim data before freeze')
            tree = {MANIFEST: man_text, 'plans/round-42-freeze.txt': 'freeze\n'}
            tree.update(post)
            rev = commit(d, tree, 'freeze marker')
            freeze = rev
        else:
            raise SystemExit('unknown claim mode ' + claim)
        return d, freeze, rev

    def run_counter(d, rev, freeze, extra=()):
        jout = os.path.join(d, '..', os.path.basename(d) + '.receipt.json')
        cmd = [sys.executable, '-I', '-B', os.path.abspath(__file__),
               '--root', d, '--rev', rev, '--freeze', freeze,
               '--json-out', jout] + list(extra)
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
        rec = None
        if os.path.exists(jout):
            try:
                with open(jout) as fh:
                    rec = json.load(fh)
            finally:
                os.unlink(jout)
        return pr, rec

    NP = len(CLASSES) * 2 + 24

    def GREEN_CHECK(rec):
        if rec.get('matched') != rec.get('n'):
            return 'matched %r of %r' % (rec.get('matched'), rec.get('n'))
        if rec.get('matched_classes') != len(CLASSES) * 2:
            return 'matched_classes %r' % rec.get('matched_classes')
        if rec.get('matched_combos') != 24:
            return 'matched_combos %r' % rec.get('matched_combos')
        rr = rec.get('real_receipts') or {}
        rows = rr.get('rows') or {}
        if len(rows) != 4 or not all(r.get('ok') for r in rows.values()):
            return 'real receipts %r' % rows
        lk = rec.get('lookup') or {}
        if lk.get('score') != 0:
            return 'lookup score %r' % lk.get('score')
        cu = rec.get('combo_unseen_majority') or {}
        if not cu.get('unseen') or len(cu.get('unseen')) < cu.get('need', 1):
            return 'combo_unseen_majority %r' % cu
        dv = rec.get('dev_envelopes') or {}
        if dv.get('n', 0) < 4 or not all(r.get('ok') for r in dv.get('rows', [])):
            return 'dev envelopes %r' % dv
        if not rec.get('counter_sha256'):
            return 'no counter_sha256'
        return None

    def LOOKUP_SCORE(rec):
        lk = rec.get('lookup') or {}
        return None if lk.get('n_combos') else 'lookup did not run'

    cases = [
        # ---- green and interface variants
        ('green: named classes x 2 + 24 combos, evaluator == interpreter',
         dict(), 0, [], [], (), GREEN_CHECK),
        ('green: full CLI envelope ok/data/meta', dict(muts={'full_envelope'}), 0, [], []),
        ('green: lane-relative carrier and envelope paths',
         dict(muts={'lane_relative_paths'}), 0, [], []),
        ('green: envelope path omitted, sibling inferred',
         dict(muts={'omit_envelope'}), 0, [], []),
        ('green: interpreter answers through --envelopes', dict(mode='dir'), 0, [], []),
        ('green: interpreter emits tab rows', dict(mode='tab3'), 0, [], []),
        ('green: interpreter names rows only, pair read off the block cells',
         dict(mode='rowonly'), 0, [], []),
        ('green: interpreter numbers rows from 1', dict(mode='rowonly1'), 0, [], []),
        ('green: evaluator emits a wrapped labels map', dict(emode='wrapped'), 0, [], []),
        ('green: evaluator emits a result list', dict(emode='list'), 0, [], []),
        ('green: evaluator writes labels to --out', dict(emode='file'), 0, [], []),
        ('green: generator object with matching sha', dict(gen_obj='good'), 0, [],
         ['generator_sha_matches_freeze']),
        ('green: prose bullet before the marker edited, block untouched',
         dict(muts={'edit_prose'}), 0, [], ['v4_block_identical']),
        ('green: a rule bullet quotes the marker inline, block still found',
         dict(marker_quoted=True), 0, [], ['v4_block_identical', 'v4_block_columns']),
        ('green: json results without a row index, rows recovered from --table-only',
         dict(mode='norow'), 0, [], ['decisions_reported']),
        ('green: writer declared and present at the freeze',
         dict(gen_obj='good', writer_path='tools/round-41/gen-squashfs.py'), 0, [],
         ['writer_matches_manifest']),
        # ---- freeze integrity (exit 2)
        ('frozen: interpreter edited after freeze', dict(muts={'edit_interp'}), 2, [], []),
        ('frozen: generator edited after freeze', dict(muts={'edit_gen'}), 2, [], []),
        ('frozen: evaluator edited after freeze', dict(muts={'edit_eval'}), 2, [], []),
        ('frozen: counter edited after freeze', dict(muts={'edit_counter'}), 2, [], []),
        ('frozen: claims edited after freeze', dict(muts={'edit_claims'}), 2, [], []),
        ('frozen: lookup control edited after freeze', dict(muts={'edit_lookup'}), 2, [], []),
        ('frozen: evidence rewritten by a later commit',
         dict(claim='evidence_rewrite'), 2, [], []),
        ('frozen: v4 block edited after freeze', dict(muts={'edit_skill'}), 2, [], []),
        ('frozen: v4 block mutated then restored (restore does not un-block)',
         dict(claim='restore'), 2, [], []),
        ('frozen: only the actions line edited (it is inside the block)',
         dict(muts={'edit_actions'}), 2, [], []),
        ('frozen: writer touched, generator names it (R40-CL3 F2)',
         dict(writer_decl='man["generator"]["writer"] = {"name": "gen-squashfs.py", '
                          '"path": "tools/round-41/gen-squashfs.py", "sha256": None}',
              muts={'edit_writer41'}), 2, [], []),
        ('frozen: round-40 writer touched, generator names it',
         dict(writer_decl='man["generator"]["writer"] = {"name": "gen-squashfs.py", '
                          '"path": "tools/round-40/gen-squashfs.py", "sha256": None}',
              muts={'edit_writer40'}), 2, [], []),
        # ---- not met (exit 1)
        ('red: writer touched but the generator never names it -> not frozen',
         dict(muts={'edit_writer41'}), 0, [], []),
        ('red: v3 marker only (no v4 block)', dict(skill_mode='v3'), 1,
         ['v4_block_present', 'v4_block_identical'], []),
        ('red: seed != freeze', dict(seed='zero'), 1, ['seed_matches_freeze'], []),
        ('red: manifest added before the freeze', dict(claim='befreeze'), 1,
         ['manifest_after_freeze', 'seed_matches_freeze'], []),
        ('red: envelopes before manifest', dict(claim='split'), 1,
         ['manifest_before_envelopes'], []),
        ('red: carrier not committed as pinned', dict(muts={'carrier_corrupt'}), 1,
         ['carriers_committed'], []),
        ('red: subject digest mismatch', dict(muts={'digest_mismatch'}), 1,
         ['envelopes_valid'], []),
        ('red: missing envelope', dict(muts={'missing_envelope'}), 1,
         ['envelopes_valid'], []),
        ('red: envelope digest swapped between carriers', dict(muts={'swap_digest'}), 1,
         ['envelopes_valid'], []),
        ('red: three carriers in one class', dict(muts={'class_count3'}), 1,
         ['classes_two_each', 'n_equals_twice_classes'], []),
        ('red: the combo family is short of twelve', dict(combos=11), 1,
         ['combo_family_wellformed'], []),
        ('red: evaluator disagrees with the table on the action', dict(emode='disagree_action'),
         1, [], ['evaluator_covers_all']),
        ('red: evaluator disagrees with the table on the label', dict(emode='disagree_label'),
         1, [], []),
        ('red: evaluator omits one envelope', dict(emode='omit'), 1,
         ['evaluator_covers_all'], []),
        # ---- R41-CL1: the declared tuple key
        ('red: R41-CL1 — the manifest declares the tuple under `declared` only',
         dict(genkey='declared'), 1, ['observed_features_match_declared'], [],
         (), lambda rec: None if (rec.get('declared_features') or {}).get('missing')
         else 'declared_features.missing is empty under the wrong key'),
        ('red: the manifest declares the tuple under `features` only',
         dict(genkey='features'), 1, ['observed_features_match_declared'], []),
        ('red: one class declares a tuple the envelope does not carry',
         dict(muts={'feat_mismatch'}), 1, ['observed_features_match_declared'], []),
        ('red: one carrier declares no tuple', dict(muts={'feat_absent'}), 1,
         ['observed_features_match_declared'], []),
        ('red: one envelope does not carry its declared tuple',
         dict(muts={'feat_env'}), 1, ['observed_features_match_declared'], []),
        ('red: a combo carrier declares the wrong tuple',
         dict(muts={'combo_feat_mismatch'}), 1,
         ['observed_features_match_declared'], []),
        # ---- the lookup control
        ('green: a lookup scoring every combo is reported, not bound',
         dict(lookup_rows=LOOKUP_FULL), 0, [], [],
         (), LOOKUP_SCORE),
        ('red: the lookup control is a v3 table the interpreter refuses',
         dict(lookup_v3=True), 1,
         ['lookup_control_identical'], []),
        # ---- the dev arm
        ('red: no round-42 dev envelopes committed', dict(muts={'no_dev_dir'}), 1,
         ['legacy_dev_envelopes'], []),
        ('red: the dev arm is short of four envelopes', dict(muts={'dev_short'}), 1,
         ['legacy_dev_envelopes'], []),
        ('red: a dev envelope disagreed with the evaluator',
         dict(muts={'dev_mismatch'}), 1, ['legacy_dev_envelopes'], []),
        # ---- real receipts
        ('red: a real receipt is missing', dict(muts={'receipt_missing'}), 1,
         ['real_receipts_depth_limited'], []),
        ('red: a real receipt is labelled otherwise',
         dict(muts={'receipt_wrong_class'}), 1, ['real_receipts_depth_limited'], []),
        ('red: the evaluator disagrees on a real receipt',
         dict(emode='real_disagree'), 1, ['real_receipts_depth_limited'], []),
        # ---- table shape
        ('red: truncated table (fall-through to unclassified)',
         dict(rows=ROWS[:1]), 1, [], []),
        ('red: catch-all table', dict(rows=[row('clean', 'none', '*')]), 1, [], []),
        ('red: correct rows plus a final `*` unclassified row (the round-40 D2 shortcut)',
         dict(rows=ROWS + [row('unclassified', 'none', '*')]), 1,
         ['row_decisions_consistent'], []),
        ('red: block without the action column',
         dict(header=[h for h in HEADER if h != 'action']), 1,
         ['v4_block_columns'], []),
        ('red: actions line missing', dict(actions=None), 1,
         ['v4_actions_declared', 'observed_actions_declared'], []),
        ('red: raise-depth not declared on the actions line',
         dict(actions=[a for a in ACTIONS if a != 'raise-depth']), 1,
         ['observed_actions_declared'], []),
        ('red: interpreter reports neither a pair nor a row nor a table listing',
         dict(mode='blind'), 1, ['decisions_reported', 'row_decisions_consistent'], []),
        ('red: two carriers share one carrier path', dict(muts={'share_carrier_path'}), 1,
         ['carrier_paths_unique'], []),
        ('red: generator object with a wrong sha', dict(gen_obj='bad'), 1,
         ['generator_sha_matches_freeze'], []),
        ('red: writer declared but not in the freeze tree',
         dict(gen_obj='good', writer_path='tools/round-38/gen-squashfs.py'), 1,
         ['writer_matches_manifest'], []),
        ('red: writer sha declared wrong',
         dict(gen_obj='good', writer_path='tools/round-41/gen-squashfs.py',
              writer_sha='f' * 64), 1, ['writer_matches_manifest'], []),
        # ---- unevaluable (exit 2)
        ('unevaluable: do-nothing at the freeze (no manifest)', dict(claim='none'), 2, [], []),
        ('unevaluable: evaluator fails outright', dict(emode='fail'), 2, [], []),
        ('unevaluable: evaluator emits non-JSON', dict(emode='garbage'), 2, [], []),
        ('unevaluable: interpreter fails outright', dict(mode='fail'), 2, [], []),
        ('unevaluable: manifest unparsable', dict(muts={'bad_manifest'}), 2, [], []),
        ('unevaluable: unknown revision', dict(), 2, [], [], ('--rev', 'deadbeef' * 5)),
        ('unevaluable: freeze not an ancestor of rev', dict(), 2, [], [], ('NONANCESTOR',)),
    ]
    green = red = 0
    for name, params, want, want_false, want_true, *rest in cases:
        extra = rest[0] if rest else ()
        check = rest[1] if len(rest) > 1 else None
        d = None
        try:
            d, freeze, rev = build(params)
            extra_args = []
            if extra == ('NONANCESTOR',):
                extra_args = ['--rev', freeze, '--freeze', rev]
            elif extra:
                extra_args = list(extra)
            pr, rec = run_counter(d, rev, freeze, extra_args)
            got = pr.returncode
            want_n = 2 * len(params.get('classes', CLASSES)) \
                + params.get('combos', 24) \
                + (1 if 'class_count3' in params.get('muts', set()) else 0)
            ok = got == want
            if rec is None:
                ok = False
                fails.append('%s: no receipt written (stderr=%r)' % (name, pr.stderr[-400:]))
            else:
                if rec.get('exit_code') != got:
                    ok = False
                    fails.append('%s: receipt exit_code %r != process exit %d'
                                 % (name, rec.get('exit_code'), got))
                if got in (0, 1) and not rec.get('counter_sha256'):
                    ok = False
                    fails.append('%s: receipt carries no counter_sha256' % name)
                if got in (0, 1):
                    if rec.get('n') != want_n:
                        ok = False
                        fails.append('%s: n=%r, want %d' % (name, rec.get('n'), want_n))
                    if rec.get('met_target_consistent') is not True:
                        ok = False
                        fails.append('%s: met_target_consistent false' % name)
                    for k in want_false:
                        if rec.get('bindings', {}).get(k) is not False:
                            ok = False
                            fails.append('%s: binding %s not false (got %r)'
                                         % (name, k, rec.get('bindings', {}).get(k)))
                    for k in want_true:
                        if rec.get('bindings', {}).get(k) is not True:
                            ok = False
                            fails.append('%s: binding %s not true (got %r)'
                                         % (name, k, rec.get('bindings', {}).get(k)))
                    if got == 0 and not rec.get('met_target'):
                        ok = False
                        fails.append('%s: exit 0 without met_target' % name)
                    if got == 0 and rec.get('matched') != NP:
                        ok = False
                        fails.append('%s: exit 0 with matched %r' % (name, rec.get('matched')))
                    if got == 0 and rec.get('bindings_false'):
                        ok = False
                        fails.append('%s: exit 0 with bindings_false %r'
                                     % (name, rec.get('bindings_false')))
                if check is not None:
                    msg = check(rec)
                    if msg:
                        ok = False
                        fails.append('%s: %s' % (name, msg))
            if ok:
                st = subprocess.run(['git', '-C', d, 'status', '--porcelain'],
                                    capture_output=True, text=True).stdout.strip()
                if st:
                    ok = False
                    fails.append('%s: counter dirtied the measured repo: %r'
                                 % (name, st[:300]))
            if ok:
                if want == 0:
                    green += 1
                else:
                    red += 1
            elif got != want:
                fails.append('%s: want exit %d got %d (stdout=%r)'
                             % (name, want, got, pr.stdout[-400:]))
        except SystemExit as e:
            fails.append('%s: fixture error %s' % (name, e))
        finally:
            if d:
                shutil.rmtree(d, ignore_errors=True)

    total = len(cases)
    passed = total - len(fails)
    print(json.dumps({'selftest': 'c2-counter r42 (v4)', 'cases': total,
                      'green': green, 'red': red, 'pass': passed,
                      'fail': len(fails), 'failures': fails}))
    print('SELFTEST cases=%d pass=%d fail=%d' % (total, passed, len(fails)))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
