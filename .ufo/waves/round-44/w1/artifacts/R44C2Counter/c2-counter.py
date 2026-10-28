#!/usr/bin/env python3
"""P44-C2 — calibration counter: re-derive a frozen rubric's asserted values at REV.

Implements `plans/round-44-claims.md` R44-C2 (calibration: a frozen rubric of
self-assessment statements).  The counter

  1. walks the freeze integrity (FREEZE must be an ancestor of REV; every frozen
     path of the rubric — the rubric file itself included — must be untouched in
     FREEZE..REV, except rubric-named paths whose repair is bound by the
     rubric's `expected_edit` clause: the blob at REV must be the blob at FREEZE
     plus the bound block, byte for byte (or line-identity over the appended
     lines), never a suffix containment and never a raw numstat);
  2. exports the measured revision's tree into a scratch clone (`--work`,
     read-only) and runs every rubric entry's check argv there;
  3. compares each check's observation with the rubric's asserted value.  A NOTE
     IS NEVER EVIDENCE: an appended note can never make an entry pass.  A
     repaired entry must re-derive its value from REV state through the
     entry's `repair_command`; the re-derived value is compared with the
     asserted value like any other observation;
  4. exits 0 iff `mismatches == 0`, every entry was evaluable and at least one
     entry was evaluated, 1 on a mismatch, 2 when the rubric is malformed, a
     frozen file is absent, a frozen path changed, no entry was evaluable, or a
     check cannot run.  Exit 2 means COULD-NOT-EVALUATE, never "not a pass":
     it never counts toward the target.

Usage
-----
    python3 -I -B c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> \
        --work <SCRATCH> --json-out <OUT> [--rubric <FILE>] \
        [--export auto|full|<glob,glob>] [--seat <NAME>]

    python3 -I -B c2-counter.py --root <LANE> --rev <BASE> --work <SCRATCH> \
        --json-out <OUT> --rubric <FILE> --pre-freeze

    python3 -I -B c2-counter.py --selftest

Exit codes: 0 = met/clean, 1 = failed (mismatch), 2 = could-not-evaluate.

`--pre-freeze` runs the base census (CTL-C2-0's honest-stop gate): the freeze
walk is reported but not enforced, because at the base the freeze is not yet an
ancestor of the measured revision.  The receipt always carries `pre_freeze`,
`entries_evaluated` and `mismatches`; a pre-freeze receipt is a census, never
a claim score (`claim_score` is false in it).

Rubric schema (frozen at `tools/round-44/c2-rubric.json`)
---------------------------------------------------------
Top level (object):

    {
      "predicate": "P44-C2",
      "freeze": "<commit>",
      "frozen_paths": ["SCORECARD.md", ...],        # or [{"path": ..., "expected_edit": {...}}]
      "expected_edits": {"SCORECARD.md": {...}},    # optional map form
      "frozen_dirs": ["tools/round-44"],            # directory pathspecs: every
                                                    #   file under them that
                                                    #   existed at FREEZE is frozen
      "export_paths": ["corpus/knowledge"],          # optional globs
      "entries": [ <entry>, ... ]
    }

Entry (object) — `check` and `command` are REQUIRED, `asserted` is REQUIRED:

    {
      "id": "<stable id>",
      "check": "<check label: json | text | exit | descriptive label>",
      "command": ["python3", "-I", "-B", "tools/round-44/c2-checks.py", "<kind>"],
      "asserted": <value>,                          # the expected observation
      "compare": "eq" | "set_eq" | "numeric_eq" | "subset" | "ge" | "le",
      "observed_key": "observed",                   # JSON key holding the observation
      "file": "SCORECARD.md",                       # rubric-named file (frozen subject)
      "files": ["corpus/knowledge"],                # extra paths the check reads
      "timeout": 300,
      "repair_command": ["python3", "-I", "-B", "...", "<kind>"],  # optional
      "expected_edit": {
          "append": ["<line>", ...],       # line-identity binding (order matters)
          "append_text": "<exact bytes>",  # byte-for-byte binding
          "preserve": ["<sha256 of a cited line>"],  # cited-line digests
          "marker": "<text>"               # a marker line must be present
      }
    }

`expected_edit` binds a repair; it is never evidence.  The file's blob at REV
must be the blob at FREEZE plus the bound block: `append_text` demands byte
equality of the appended bytes, `append` demands line identity of the appended
lines (blank separator lines ignored), and `preserve` demands that every cited
line digest still occurs in the REV blob.  Nothing may be edited in place and
nothing may be deleted (the freeze blob must be a prefix of the REV blob).  The
bound file must be rubric-named.  A file that changed without a bound
`expected_edit` is `frozen_path_changed` — exit 2, never a pass.

Check-command contract: the command runs with the exported tree as its working
directory and must print the observation on stdout.  `check: "json"` parses
stdout as JSON and reads `observed_key` (default `observed`, then `value`,
`result`, `match`, `ok`) from the object; `check: "text"` takes stdout verbatim
(stripped); `check: "exit"` maps the exit status to a boolean.  A descriptive
label behaves like `json` with a text fallback.  A command that cannot start
(missing binary), times out, or exits non-zero with empty stdout cannot be
evaluated — the whole score is then exit 2, never a pass.

A NOTE IS NEVER EVIDENCE.  When an entry's check fails at REV, the counter
does not accept an appended note as a repair.  The entry may declare a
`repair_command`: a second argv that re-derives the repaired value from REV
state (the note is read as text; the VALUE is re-derived independently).  Only
when the re-derived value equals the asserted value is the entry repaired.
Without a `repair_command` an appended note leaves the entry a mismatch.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

EXIT_MET = 0
EXIT_FAIL = 1
EXIT_CANT = 2

RUBRIC_PATH = 'tools/round-44/c2-rubric.json'
COUNTER_PATH = 'tools/round-44/c2-counter.py'
# The frozen files the R44-C2 claim pins by name (plans/round-44-claims.md,
# "Frozen paths"): the self-assessment surfaces the rubric measures, plus
# SKILL.md, whose instrument-registry rows the rubric cites.  corpus/SOURCES.md
# is NOT here: C1 appends its S138/S139 rows there, and the claim states C2's
# rubric pins no SOURCES row count.
C2_DEFAULT_FROZEN = ('SCORECARD.md', 'SHONEN.md', 'corpus/README.md', 'SKILL.md')
# The self-assessment surface a calibration check may read at run time.  A check
# that discovers paths while it runs cannot declare them, so the default export
# covers the surfaces the R44-C2 claim names (plus the map and the lessons).
C2_DEFAULT_SURFACE = (
    'SCORECARD.md', 'SHONEN.md', 'PROVINCE.md', 'SKILL.md', 'LOG.md',
    'MANIFEST.json', 'corpus/README.md', 'corpus/SOURCES.md',
    'corpus/knowledge/*', 'corpus/lessons/*', 'corpus/evidence/*.json',
)
DEFAULT_SEAT = 'R44C2Counter'
CHECK_TIMEOUT = 600

ENTRY_LIST_KEYS = ('entries', 'checks', 'items', 'statements', 'rubric')
ID_KEYS = ('id', 'check_id', 'entry_id', 'name', 'label')
CHECK_KEYS = ('check', 'check_kind', 'kind', 'check_type', 'type')
COMMAND_KEYS = ('command', 'argv', 'check_argv', 'check_command', 'cmd', 'run')
ASSERT_KEYS = ('asserted', 'assert', 'expected', 'expected_value', 'value')
COMPARE_KEYS = ('compare', 'comparison', 'mode')
OBSERVED_KEYS = ('observed', 'value', 'result', 'match', 'ok', 'observed_value')
FILE_KEYS = ('file', 'path', 'target', 'subject')
FILES_KEYS = ('files', 'reads', 'inputs')
EDIT_KEYS = ('expected_edit', 'edit', 'repair')

STATUS_CHANGE = set('MDTRU')


class Unevaluable(Exception):
    """The score cannot be evaluated at all (exit 2)."""

    def __init__(self, reason, receipt=None):
        super().__init__(reason)
        self.reason = reason
        self.receipt = receipt or {}


# --------------------------------------------------------------------- utils
def sha256_bytes(data):
    if data is None:
        return None
    return hashlib.sha256(data).hexdigest()


def sha256_text(text):
    if text is None:
        return None
    return hashlib.sha256(text.encode('utf-8', 'replace')).hexdigest()


def canon(value):
    """A canonical, type-aware representation used for equality."""
    if isinstance(value, bool):
        return ('bool', value)
    if isinstance(value, (int, float)):
        return ('num', float(value))
    if value is None:
        return ('null', None)
    if isinstance(value, str):
        return ('str', value)
    if isinstance(value, (list, tuple)):
        return ('list', [canon(v) for v in value])
    if isinstance(value, dict):
        return ('dict', {str(k): canon(value[k]) for k in sorted(value, key=str)})
    return ('other', repr(value))


def numeric(value):
    """The value as a float when it is numeric (or a numeric string), else None."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except (TypeError, ValueError):
            return None
    return None


def compare_values(observed, asserted, mode):
    """(matched, reason).  `eq` coerces a numeric string against a number."""
    mode = (mode or 'eq').lower()
    if mode == 'eq':
        if canon(observed) == canon(asserted):
            return True, 'equal'
        a, b = numeric(observed), numeric(asserted)
        if a is not None and b is not None and abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b)):
            return True, 'numeric_equal'
        return False, 'not_equal'
    if mode == 'numeric_eq':
        a, b = numeric(observed), numeric(asserted)
        if a is None or b is None:
            return False, 'not_numeric'
        return (abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b)), 'numeric_equal')
    if mode == 'set_eq':
        if not isinstance(observed, list) or not isinstance(asserted, list):
            return False, 'not_a_list'
        return (sorted(map(repr, observed)) == sorted(map(repr, asserted)), 'set_equal')
    if mode == 'subset':
        if not isinstance(observed, list) or not isinstance(asserted, list):
            return False, 'not_a_list'
        return (all(any(canon(x) == canon(y) for x in observed) for y in asserted),
                'subset')
    if mode in ('ge', 'le'):
        a, b = numeric(observed), numeric(asserted)
        if a is None or b is None:
            return False, 'not_numeric'
        ok = a >= b if mode == 'ge' else a <= b
        return ok, mode
    return False, 'unknown_compare_mode'


# ----------------------------------------------------------------------- git
def git(root, *args, check=False):
    proc = subprocess.run(['git', '-C', root] + list(args), capture_output=True,
                          text=True)
    if check and proc.returncode:
        raise Unevaluable('git %s failed: %s' % (' '.join(args), proc.stderr.strip()))
    return proc


def full_rev(root, rev):
    proc = git(root, 'rev-parse', '--verify', '%s^{commit}' % rev)
    if proc.returncode:
        raise Unevaluable('unknown revision %r' % rev)
    return proc.stdout.strip()


def show(root, rev, path):
    """Blob bytes at `rev`, or None when absent/unreadable."""
    proc = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                          capture_output=True)
    if proc.returncode:
        return None
    return proc.stdout


def present(root, rev, path):
    return show(root, rev, path) is not None


def is_ancestor(root, ancestor, descendant):
    proc = git(root, 'merge-base', '--is-ancestor', ancestor, descendant)
    return proc.returncode == 0


def path_status_changes(root, freeze, rev, path):
    """[(commit, status)] for `path` in FREEZE..REV (merge diffs, first-parent)."""
    proc = git(root, 'log', '--diff-merges=first-parent', '--no-renames',
               '--name-status', '--format=%x01%H', '%s..%s' % (freeze, rev),
               '--', path)
    if proc.returncode:
        return []
    commit = None
    out = []
    for line in proc.stdout.splitlines():
        if line.startswith('\x01'):
            commit = line[1:].strip()
            continue
        if not line.strip():
            continue
        status = line.split('\t', 1)[0].strip()
        out.append((commit, status))
    return out


def changed_paths(root, freeze, rev):
    """Every path touched in FREEZE..REV (name-only walk + merge first-parent)."""
    touched = set()
    for args in (['log', '--pretty=format:', '--name-only', '--no-renames'],
                 ['log', '--diff-merges=first-parent', '--pretty=format:',
                  '--name-only', '--no-renames']):
        proc = git(root, *(args + ['%s..%s' % (freeze, rev)]))
        if proc.returncode:
            continue
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line:
                touched.add(line)
    return touched


# ------------------------------------------------------------------- rubric
def pick(entry, keys, default=None):
    for key in keys:
        if key in entry and entry[key] is not None:
            return entry[key]
    return default


def parse_rubric(raw):
    """(rubric, entries, frozen_spec, malformed_reason).

    `frozen_spec` maps a rubric-named path to its `expected_edit` clause
    (None when the path is frozen without a bound repair).
    """
    if raw is None:
        return None, None, None, None, None, 'rubric_absent'
    try:
        doc = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, None, None, None, None, 'rubric_unparseable: %s' % exc
    if not isinstance(doc, dict):
        return None, None, None, None, None, 'rubric_not_an_object'

    raw_entries = None
    for key in ENTRY_LIST_KEYS:
        value = doc.get(key)
        if isinstance(value, list):
            raw_entries = value
            break
    if raw_entries is None:
        return None, None, None, None, None, 'rubric_has_no_entry_list'

    entries = []
    seen = set()
    for index, raw_entry in enumerate(raw_entries):
        if not isinstance(raw_entry, dict):
            return None, None, None, None, None, 'entry_%d_not_an_object' % index
        check = pick(raw_entry, CHECK_KEYS)
        command = pick(raw_entry, COMMAND_KEYS)
        if not isinstance(check, str) or not check.strip():
            return None, None, None, None, None, 'entry_%d_missing_check' % index
        if isinstance(command, str):
            argv = shlex.split(command)
        elif isinstance(command, (list, tuple)):
            argv = [str(t) for t in command]
        else:
            argv = []
        if not argv:
            return None, None, None, None, None, 'entry_%d_missing_command' % index
        asserted = pick(raw_entry, ASSERT_KEYS, default=_MISSING)
        if asserted is _MISSING:
            return None, None, None, None, None, 'entry_%d_missing_asserted' % index
        ident = pick(raw_entry, ID_KEYS)
        if not isinstance(ident, str) or not ident.strip():
            ident = 'entry-%03d' % index
        if ident in seen:
            return None, None, None, None, None, 'duplicate_entry_id_%s' % ident
        seen.add(ident)
        repair = pick(raw_entry, ('repair_command', 'repair_argv', 'recheck'))
        if isinstance(repair, str):
            repair_argv = shlex.split(repair)
        elif isinstance(repair, (list, tuple)):
            repair_argv = [str(t) for t in repair]
        else:
            repair_argv = None
        if repair_argv is not None and not repair_argv:
            return None, None, None, None, None, 'entry_%d_empty_repair_command' % index
        timeout = raw_entry.get('timeout')
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            timeout = CHECK_TIMEOUT
        entry = {
            'id': ident,
            'index': index,
            'check': check.strip(),
            'argv': argv,
            'command': argv,
            'asserted': asserted,
            'compare': str(pick(raw_entry, COMPARE_KEYS, default='eq') or 'eq'),
            'observed_key': pick(raw_entry, ('observed_key', 'observation_key',
                                             'json_key')),
            'file': pick(raw_entry, FILE_KEYS),
            'files': [str(f) for f in (pick(raw_entry, FILES_KEYS, default=[]) or [])],
            'timeout': int(timeout),
            'expected_edit': pick(raw_entry, EDIT_KEYS),
            'repair_command': repair_argv,
        }
        if not isinstance(entry['file'], str) or not entry['file'].strip():
            entry['file'] = None
        entries.append(entry)

    # frozen paths ------------------------------------------------------------
    frozen_spec = {}
    declared = set()

    def add_frozen(path, edit=None, explicit=False):
        if not isinstance(path, str) or not path.strip():
            return
        path = path.strip()
        if explicit:
            declared.add(path)
        if path in frozen_spec:
            if edit is not None and frozen_spec[path] is None:
                frozen_spec[path] = edit
            return
        frozen_spec[path] = edit

    declared_edits = doc.get('expected_edits')
    if isinstance(declared_edits, dict):
        for path, edit in declared_edits.items():
            add_frozen(path, edit, explicit=True)
    for item in doc.get('frozen_paths') or []:
        if isinstance(item, str):
            add_frozen(item, declared_edits.get(item) if isinstance(declared_edits, dict) else None,
                       explicit=True)
        elif isinstance(item, dict):
            path = pick(item, FILE_KEYS)
            add_frozen(path, pick(item, EDIT_KEYS), explicit=True)
    for entry in entries:
        if entry['expected_edit'] is not None:
            path = entry['expected_edit'].get('file') if isinstance(entry['expected_edit'], dict) else None
            if path:
                add_frozen(path, entry['expected_edit'], explicit=True)
    for path in C2_DEFAULT_FROZEN:
        add_frozen(path)
    add_frozen(RUBRIC_PATH)
    add_frozen(COUNTER_PATH)

    # every expected_edit must name a rubric-named path AND bind content:
    # `append_text` (byte-for-byte) or a non-empty `append` (line identity).
    # `marker` and `preserve` are additional, never sufficient on their own.
    for path, edit in list(frozen_spec.items()):
        if edit is None:
            continue
        if not isinstance(edit, dict):
            return None, None, None, None, None, 'expected_edit_not_an_object:%s' % path
        if 'append' in edit and not isinstance(edit['append'], list):
            return None, None, None, None, None, 'expected_edit_append_not_a_list:%s' % path
        has_text = isinstance(edit.get('append_text'), str) and edit['append_text']
        has_append = (isinstance(edit.get('append'), list)
                      and any(str(w).strip() for w in edit['append']))
        if not (has_text or has_append):
            return None, None, None, None, None, \
                'expected_edit_binds_no_content:%s' % path
    frozen_dirs = []
    for item in doc.get('frozen_dirs') or []:
        if isinstance(item, str) and item.strip():
            frozen_dirs.append(item.strip().rstrip('/'))
    return doc, entries, frozen_spec, declared, frozen_dirs, None


_MISSING = object()


# --------------------------------------------------------------- freeze walk
def appended_text(freeze_bytes, rev_bytes):
    """The bytes appended after the freeze blob, or None when not append-only."""
    if rev_bytes is None or freeze_bytes is None:
        return None
    if not rev_bytes.startswith(freeze_bytes):
        return None
    return rev_bytes[len(freeze_bytes):].decode('utf-8', 'replace')


def verify_expected_edit(freeze_bytes, rev_bytes, edit):
    """(ok, reason, appended_lines).  Line identity, never a raw numstat.

    The appended block's non-blank lines must equal the bound lines exactly, in
    order; blank separator lines (a markdown block is usually appended after an
    empty line) are ignored.  Nothing else may be appended and nothing may be
    edited in place — the blob must be the freeze blob plus the bound block.
    """
    appended = appended_text(freeze_bytes, rev_bytes)
    if appended is None:
        return False, 'not_append_only', None
    lines = appended.splitlines()
    want = edit.get('append')
    want_text = edit.get('append_text')
    marker = edit.get('marker')
    preserve = edit.get('preserve')
    if isinstance(want_text, str):
        # byte-for-byte: blob_REV == blob_FREEZE + the declared bytes
        if appended.encode('utf-8') != want_text.encode('utf-8'):
            return False, 'appended_bytes_differ_from_expected_edit', lines
    if isinstance(want, list):
        want_lines = [str(w).strip() for w in want if str(w).strip()]
        got_lines = [l.strip() for l in lines if l.strip()]
        if got_lines != want_lines:
            return False, 'appended_block_differs_from_expected_edit', lines
    if isinstance(marker, str) and marker:
        if not any(marker in l for l in lines):
            return False, 'marker_absent_from_appended_block', lines
    if isinstance(preserve, list) and preserve:
        rev_lines = [l for l in rev_bytes.decode('utf-8', 'replace').splitlines()]
        digests = {hashlib.sha256(l.encode('utf-8')).hexdigest() for l in rev_lines}
        for want_digest in preserve:
            if str(want_digest).lower() not in digests:
                return False, 'cited_line_digest_absent', lines
    if want is None and want_text is None and marker is None and not preserve:
        return False, 'expected_edit_binds_nothing', lines
    return True, 'bound_edit', lines


def freeze_integrity(root, freeze, rev, frozen_spec, declared=(), frozen_dirs=()):
    """(changed_paths, notes).  A changed frozen path is exit 2, never a pass."""
    changed = []
    notes = []
    union = changed_paths(root, freeze, rev)
    # directory pathspecs: every file under them that existed at FREEZE is frozen
    for directory in frozen_dirs:
        prefix = directory + '/'
        for path in sorted(p for p in union if p.startswith(prefix)):
            freeze_bytes = show(root, freeze, path)
            rev_bytes = show(root, rev, path)
            if freeze_bytes is None:
                changed.append(path)
                notes.append({'path': path, 'state': 'added_under_frozen_dir'})
                continue
            if rev_bytes is None or freeze_bytes != rev_bytes:
                changed.append(path)
                notes.append({'path': path, 'state': 'changed_under_frozen_dir'})
            else:
                changed.append(path)
                notes.append({'path': path, 'state': 'touched_under_frozen_dir'})
    for path in sorted(frozen_spec):
        edit = frozen_spec[path]
        freeze_bytes = show(root, freeze, path)
        rev_bytes = show(root, rev, path)
        if freeze_bytes is None:
            if rev_bytes is not None and path in (RUBRIC_PATH, COUNTER_PATH):
                changed.append(path)
                notes.append({'path': path, 'state': 'added_after_freeze'})
            elif path in declared:
                changed.append(path)
                notes.append({'path': path, 'state': 'absent_frozen_file'})
            else:
                notes.append({'path': path, 'state': 'absent_at_freeze'})
            continue
        statuses = path_status_changes(root, freeze, rev, path)
        touched = [s for (_c, s) in statuses
                   if s in STATUS_CHANGE or (s == 'A' and freeze_bytes is not None)]
        if path in union and not touched:
            # the path-filtered walk missed it; the union walk did not
            touched = ['union-walk']
        if edit is None:
            if freeze_bytes != rev_bytes:
                changed.append(path)
                notes.append({'path': path, 'state': 'blob_changed',
                              'statuses': sorted(set(s for _c, s in statuses))})
            elif touched:
                changed.append(path)
                notes.append({'path': path, 'state': 'touched_after_freeze',
                              'statuses': sorted(set(touched))})
            else:
                notes.append({'path': path, 'state': 'unchanged'})
            continue
        # relaxed arm: an appended, bound repair only
        if rev_bytes == freeze_bytes:
            notes.append({'path': path, 'state': 'unchanged',
                          'bound_edit_declared': True})
            continue
        ok, reason, lines = verify_expected_edit(freeze_bytes, rev_bytes, edit)
        if not ok:
            changed.append(path)
            notes.append({'path': path, 'state': 'bound_edit_violation',
                          'reason': reason,
                          'statuses': sorted(set(s for _c, s in statuses))})
        else:
            notes.append({'path': path, 'state': 'bound_edit_applied',
                          'reason': reason, 'appended_lines': len(lines)})
    return changed, notes


# ------------------------------------------------------------------- export
def repo_paths(root, rev):
    proc = git(root, 'ls-tree', '-r', '--name-only', rev)
    if proc.returncode:
        return []
    return [l.strip() for l in proc.stdout.splitlines() if l.strip()]


PATH_LITERAL_RE = re.compile(
    r'[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|json|sh|txt|yaml|yml|toml|tsv|csv)')


def collect_strings(node, out):
    if isinstance(node, str):
        out.add(node)
    elif isinstance(node, dict):
        for value in node.values():
            collect_strings(value, out)
    elif isinstance(node, list):
        for value in node:
            collect_strings(value, out)
    return out


def select_paths(root, rev, rubric, entries, mode):
    """The repo paths to export into the scratch tree.

    `auto` exports the union of
      * the paths the rubric names (frozen paths, entry files, path-like
        literals inside the check commands),
      * the rubric's `export_paths` globs, and
      * C2_DEFAULT_SURFACE — the self-assessment surface a calibration check
        may read (a check that discovers paths at runtime cannot declare them).
    """
    all_paths = repo_paths(root, rev)
    if mode == 'full':
        return all_paths, 'full'
    patterns = []
    if mode not in ('auto', ''):
        patterns.extend(p.strip() for p in mode.split(',') if p.strip())
    if isinstance(rubric, dict):
        for pattern in rubric.get('export_paths') or []:
            if isinstance(pattern, str) and pattern.strip():
                patterns.append(pattern.strip())
    if mode in ('auto', ''):
        patterns.extend(C2_DEFAULT_SURFACE)
    selected = set()
    for pattern in patterns:
        for path in all_paths:
            if fnmatch.fnmatch(path, pattern) or path == pattern:
                selected.add(path)
    strings = collect_strings(rubric, set())
    for path in all_paths:
        if path in strings:
            selected.add(path)
            continue
        for token in strings:
            if '/' in token and token.endswith('/') and path.startswith(token):
                selected.add(path)
                break
    for entry in entries:
        for name in [entry['file']] + entry['files']:
            if not name:
                continue
            name = name.rstrip('/')
            for path in all_paths:
                if path == name or path.startswith(name + '/'):
                    selected.add(path)
        for token in entry['argv']:
            if token in all_paths:
                selected.add(token)
            elif token.endswith('/') and any(p.startswith(token) for p in all_paths):
                selected.update(p for p in all_paths if p.startswith(token))
            # path-like literals inside the command text (a check may read a file
            # it names in its own source)
            for literal in PATH_LITERAL_RE.findall(token):
                literal = literal.lstrip('./')
                if literal in all_paths:
                    selected.add(literal)
                elif any(p.startswith(literal + '/') for p in all_paths):
                    selected.update(p for p in all_paths if p.startswith(literal + '/'))
    if not selected:
        return all_paths, 'auto_fallback_full'
    return sorted(selected), 'auto'


def extract_tar(stream, dest):
    """Extract a git-archive tar into `dest` (no escaping members)."""
    dest = os.path.abspath(dest)
    os.makedirs(dest, exist_ok=True)
    count = 0
    with tarfile.open(fileobj=stream, mode='r|') as tar:
        for member in tar:
            name = member.name.lstrip('./')
            if not name or name.startswith('/'):
                continue
            target = os.path.abspath(os.path.join(dest, name))
            if not (target == dest or target.startswith(dest + os.sep)):
                continue
            if member.isdir():
                os.makedirs(target, exist_ok=True)
            elif member.isfile():
                os.makedirs(os.path.dirname(target), exist_ok=True)
                src = tar.extractfile(member)
                if src is None:
                    continue
                with open(target, 'wb') as handle:
                    shutil.copyfileobj(src, handle)
                count += 1
            elif member.issym():
                link = member.linkname
                if os.path.isabs(link):
                    continue
                resolved = os.path.abspath(os.path.join(os.path.dirname(target), link))
                if not resolved.startswith(dest + os.sep):
                    continue
                os.makedirs(os.path.dirname(target), exist_ok=True)
                if os.path.lexists(target):
                    os.unlink(target)
                os.symlink(link, target)
    return count


def export_tree(root, rev, paths, tree_dir):
    """Materialise `paths` of `rev` into `tree_dir` (read-only export)."""
    os.makedirs(tree_dir, exist_ok=True)
    if not paths:
        return 0
    proc = subprocess.Popen(['git', '-C', root, 'archive', '--format=tar', rev, '--']
                             + list(paths), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    count = extract_tar(proc.stdout, tree_dir)
    proc.stdout.close()
    err = proc.stderr.read().decode('utf-8', 'replace')
    proc.wait()
    if proc.returncode:
        raise Unevaluable('git archive failed: %s' % err.strip())
    return count


# --------------------------------------------------------------- check runs
PLACEHOLDER_RE = re.compile(r'\{(rev|freeze|root|tree|repo|work|rubric|seat)\}')


def substitute(argv, subst):
    """Expand only the known placeholders; other braces are left alone."""
    out = []
    for token in argv:
        out.append(PLACEHOLDER_RE.sub(lambda m: str(subst.get(m.group(1), m.group(0))),
                                      token))
    return out


def extract_observation(stdout, kind, observed_key):
    """(observed, kind_resolved, error)."""
    text = stdout.strip()
    if kind == 'exit':
        return None, 'exit', None
    if kind == 'text':
        if not text:
            return None, 'text', 'empty_output'
        return text, 'text', None
    # json (default) with a text fallback
    doc = None
    try:
        doc = json.loads(text) if text else None
    except json.JSONDecodeError:
        doc = None
    if doc is None:
        if not text:
            return None, 'json', 'empty_output'
        return text, 'text_fallback', None
    if isinstance(doc, dict):
        keys = ([observed_key] if observed_key else []) + list(OBSERVED_KEYS)
        for key in keys:
            if key and key in doc:
                return doc[key], 'json', None
        return doc, 'json_object', None
    return doc, 'json_scalar', None


def run_entry(entry, tree, repo, env, root, rev, freeze):
    """(record, error).  `error` means the check could not be evaluated."""
    check_env = dict(env)
    check_env.update({
        'HYAKU_TREE': tree,
        'HYAKU_REPO': repo,
        'HYAKU_ROOT': root,
        'HYAKU_REV': rev,
        'HYAKU_FREEZE': freeze,
        'HYAKU_RUBRIC': env.get('HYAKU_RUBRIC', ''),
        'HYAKU_WORK': env.get('HYAKU_WORK', ''),
        'HYAKU_SEAT': env.get('HYAKU_SEAT', DEFAULT_SEAT),
    })
    subst = {
        'rev': rev, 'freeze': freeze, 'root': os.path.abspath(root),
        'tree': tree, 'repo': repo, 'work': check_env.get('HYAKU_WORK', ''),
        'rubric': check_env.get('HYAKU_RUBRIC', ''),
        'seat': check_env.get('HYAKU_SEAT', DEFAULT_SEAT),
    }
    argv = substitute(entry['argv'], subst)
    started = time.time()
    try:
        proc = subprocess.run(argv, cwd=tree, env=check_env, capture_output=True,
                              text=True, timeout=entry['timeout'])
    except FileNotFoundError as exc:
        return ({'id': entry['id'], 'command': argv, 'exit_code': None,
                 'stdout_sha256': sha256_text(''), 'stderr_sha256': None,
                 'wall_seconds': round(time.time() - started, 6),
                 'error': 'command_not_found: %s' % exc},
                'command_not_found')
    except PermissionError as exc:
        return ({'id': entry['id'], 'command': argv, 'exit_code': None,
                 'stdout_sha256': sha256_text(''), 'stderr_sha256': None,
                 'wall_seconds': round(time.time() - started, 6),
                 'error': 'permission_denied: %s' % exc},
                'permission_denied')
    except subprocess.TimeoutExpired:
        return ({'id': entry['id'], 'command': argv, 'exit_code': None,
                 'stdout_sha256': None, 'stderr_sha256': None,
                 'wall_seconds': round(time.time() - started, 6),
                 'error': 'timeout'},
                'timeout')
    except OSError as exc:
        return ({'id': entry['id'], 'command': argv, 'exit_code': None,
                 'stdout_sha256': sha256_text(''), 'stderr_sha256': None,
                 'wall_seconds': round(time.time() - started, 6),
                 'error': 'os_error: %s' % exc},
                'os_error')
    wall = round(time.time() - started, 6)
    record = {
        'id': entry['id'],
        'check': entry['check'],
        'command': argv,
        'exit_code': proc.returncode,
        'stdout_sha256': sha256_text(proc.stdout),
        'stderr_sha256': sha256_text(proc.stderr),
        'stdout_bytes': len(proc.stdout.encode('utf-8', 'replace')),
        'wall_seconds': wall,
        'stdout_head': proc.stdout[:2000],
        'stderr_head': proc.stderr[:1000],
    }
    if proc.returncode != 0 and not proc.stdout.strip():
        record['error'] = 'nonzero_exit_without_output'
        return record, 'nonzero_exit_without_output'
    if entry['check'] == 'exit':
        record['observed'] = (proc.returncode == 0)
        record['kind_resolved'] = 'exit'
        return record, None
    observed, kind, error = extract_observation(proc.stdout, entry['check'],
                                                entry['observed_key'])
    record['kind_resolved'] = kind
    if error:
        record['error'] = error
        return record, error
    record['observed'] = observed
    return record, None


# -------------------------------------------------------------------- score
def score(root, rev_arg, freeze_arg, work, rubric_path, export_mode, seat,
          keep_work=False, pre_freeze=False):
    started = time.time()
    rev = full_rev(root, rev_arg)
    if freeze_arg:
        freeze = full_rev(root, freeze_arg)
    elif pre_freeze:
        freeze = rev
    else:
        raise Unevaluable('freeze_required')

    rubric_source = 'freeze'
    if rubric_path:
        try:
            with open(rubric_path, 'rb') as handle:
                raw = handle.read()
        except OSError as exc:
            raise Unevaluable('rubric_file_unreadable: %s' % exc)
        rubric_source = 'file'
    else:
        raw = show(root, freeze, RUBRIC_PATH)
        if raw is None and pre_freeze:
            raw = show(root, rev, RUBRIC_PATH)
            if raw is not None:
                rubric_source = 'rev'
        if raw is None and pre_freeze:
            on_disk = os.path.join(os.path.abspath(root), RUBRIC_PATH)
            try:
                with open(on_disk, 'rb') as handle:
                    raw = handle.read()
                rubric_source = 'working_tree'
            except OSError:
                raw = None
        if raw is None:
            raise Unevaluable('rubric_absent_at_freeze:%s' % RUBRIC_PATH)

    rubric, entries, frozen_spec, declared, frozen_dirs, malformed = parse_rubric(raw)
    if malformed:
        raise Unevaluable('rubric_malformed: %s' % malformed)

    declared_freeze = rubric.get('freeze') if isinstance(rubric, dict) else None
    declared_rev = None
    if isinstance(declared_freeze, str) and declared_freeze.strip():
        try:
            declared_rev = full_rev(root, declared_freeze.strip())
        except Unevaluable:
            declared_rev = declared_freeze.strip()
        if not pre_freeze and declared_rev != freeze:
            raise Unevaluable('rubric_freeze_mismatch: %s != %s' % (declared_rev, freeze))

    result = {
        'predicate': 'P44-C2',
        'seat': seat,
        'root': os.path.abspath(root),
        'revision': rev,
        'freeze': freeze,
        'rubric_path': rubric_path or RUBRIC_PATH,
        'rubric_source': rubric_source,
        'rubric_sha256': sha256_bytes(raw),
        'counter_path': COUNTER_PATH,
        'counter_sha256': None,
        'counter_sha256_at_freeze': None,
        'ancestor_ok': False,
        'pre_freeze': bool(pre_freeze),
        'claim_score': bool((not pre_freeze) and rubric_source == 'freeze'),
        'declared_freeze': declared_rev,
        'frozen_dirs': sorted(frozen_dirs),
        'frozen_paths': sorted(frozen_spec),
        'frozen_path_changed': [],
        'freeze_notes': [],
        'entries': [],
        'entries_count': len(entries),
        'entries_evaluated': 0,
        'mismatches': [],
        'mismatches_count': 0,
        'mismatch_details': [],
        'unevaluable': [],
        'unevaluable_count': 0,
        'exported_paths': [],
        'export_mode': export_mode,
        'met_target': False,
        'exit_code': EXIT_CANT,
    }
    try:
        result['counter_sha256'] = sha256_bytes(show(root, rev, COUNTER_PATH))
        result['counter_sha256_at_freeze'] = sha256_bytes(show(root, freeze, COUNTER_PATH))
    except Exception:
        pass

    if pre_freeze:
        # the census at the base: the freeze is not yet an ancestor of REV, so
        # the freeze walk is reported but not enforced
        result['ancestor_ok'] = None
        result['freeze_notes'].append({'state': 'pre_freeze_not_enforced'})
    elif not is_ancestor(root, freeze, rev):
        result['freeze_notes'].append({'state': 'freeze_not_ancestor'})
        result['unevaluable'].append({'id': None, 'reason': 'freeze_not_ancestor'})
        result['exit_code'] = EXIT_CANT
        result['wall_seconds'] = round(time.time() - started, 6)
        return result
    else:
        result['ancestor_ok'] = True

    # the rubric file itself is frozen: byte-compare FREEZE -> REV
    if rubric_source == 'freeze':
        freeze_bytes = show(root, freeze, RUBRIC_PATH)
        rev_bytes = show(root, rev, RUBRIC_PATH)
        if freeze_bytes != rev_bytes:
            result['frozen_path_changed'].append(RUBRIC_PATH)
            result['freeze_notes'].append({'path': RUBRIC_PATH, 'state': 'rubric_changed'})
            result['unevaluable'].append({'id': None, 'reason': 'frozen_path_changed'})
            result['exit_code'] = EXIT_CANT
            result['wall_seconds'] = round(time.time() - started, 6)
            return result

    changed, notes = freeze_integrity(root, freeze, rev, frozen_spec, declared,
                                      frozen_dirs)
    result['frozen_path_changed'] = changed
    result['freeze_notes'] = notes
    if changed and not pre_freeze:
        result['unevaluable'].append({'id': None, 'reason': 'frozen_path_changed',
                                       'paths': changed})
        result['exit_code'] = EXIT_CANT
        result['wall_seconds'] = round(time.time() - started, 6)
        return result

    # scratch clone + export ------------------------------------------------
    base = work or os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
    workdir = tempfile.mkdtemp(prefix='c2-counter.', dir=base) if os.path.isdir(base) \
        else tempfile.mkdtemp(prefix='c2-counter.')
    repo_dir = os.path.join(workdir, 'repo')
    tree_dir = os.path.join(workdir, 'tree')
    env = dict(os.environ)
    env['HYAKU_WORK'] = workdir
    env['HYAKU_SEAT'] = seat
    env['HYAKU_RUBRIC'] = os.path.abspath(rubric_path) if rubric_path else RUBRIC_PATH
    try:
        clone = subprocess.run(['git', 'clone', '--shared', '--no-checkout',
                                '--quiet', os.path.abspath(root), repo_dir],
                               capture_output=True, text=True)
        if clone.returncode:
            raise Unevaluable('scratch_clone_failed: %s' % clone.stderr.strip())
        paths, mode = select_paths(root, rev, rubric, entries, export_mode)
        result['exported_paths'] = paths if len(paths) <= 400 else paths[:400]
        result['exported_path_count'] = len(paths)
        result['export_mode'] = mode
        export_tree(root, rev, paths, tree_dir)
        if not os.path.isdir(tree_dir):
            raise Unevaluable('export_empty')

        for entry in entries:
            record, error = run_entry(entry, tree_dir, repo_dir, env, root, rev, freeze)
            record['asserted'] = entry['asserted']
            record['compare'] = entry['compare']
            record['file'] = entry['file']
            if error:
                record['match'] = None
                result['entries'].append(record)
                result['unevaluable'].append({'id': entry['id'], 'reason': error})
                continue
            matched, reason = compare_values(record['observed'], entry['asserted'],
                                             entry['compare'])
            record['match'] = bool(matched)
            record['match_reason'] = reason
            if not matched:
                # A NOTE IS NEVER EVIDENCE.  The entry may re-derive its value
                # from REV state through `repair_command`; only that
                # re-derivation can repair the entry.
                repaired = False
                if entry['repair_command']:
                    repair_entry = dict(entry)
                    repair_entry['argv'] = entry['repair_command']
                    repair_entry['id'] = entry['id'] + ':repair'
                    repair_record, repair_error = run_entry(
                        repair_entry, tree_dir, repo_dir, env, root, rev, freeze)
                    repair_record['asserted'] = entry['asserted']
                    repair_record['compare'] = entry['compare']
                    record['repair_check'] = repair_record
                    if repair_error is None:
                        repair_ok, _reason = compare_values(
                            repair_record['observed'], entry['asserted'],
                            entry['compare'])
                        if repair_ok:
                            repaired = True
                            record['match'] = True
                            record['match_reason'] = 'repaired_by_rederived_value'
                            record['repaired'] = True
                if not repaired:
                    result['mismatches'].append(entry['id'])
                    result['mismatch_details'].append({
                        'id': entry['id'],
                        'check': entry['check'],
                        'observed': record['observed'],
                        'asserted': entry['asserted'],
                        'compare': entry['compare'],
                        'file': entry['file'],
                        'command': record['command'],
                    })
            result['entries'].append(record)
    finally:
        if not keep_work:
            shutil.rmtree(workdir, ignore_errors=True)

    result['mismatches_count'] = len(result['mismatches'])
    result['unevaluable_count'] = len(result['unevaluable'])
    result['entries_count'] = len(entries)
    result['entries_evaluated'] = sum(1 for e in result['entries']
                                      if e.get('observed') is not None
                                      and not e.get('error'))
    if result['entries_evaluated'] == 0:
        result['unevaluable'].append({'id': None, 'reason': 'no_evaluable_entries'})
        result['unevaluable_count'] = len(result['unevaluable'])
    result['met_target'] = (not result['mismatches'] and not result['unevaluable']
                             and not (result['frozen_path_changed']
                                      and not pre_freeze)
                             and result['entries_evaluated'] > 0)
    result['exit_code'] = EXIT_MET if result['met_target'] else (
        EXIT_FAIL if result['mismatches'] and not result['unevaluable'] else EXIT_CANT)
    result['wall_seconds'] = round(time.time() - started, 6)
    return result


# ----------------------------------------------------------------- selftest
SELFTEST_CHECK = '''import json, pathlib, sys
name = sys.argv[1] if len(sys.argv) > 1 else "doc.md"
mode = sys.argv[2] if len(sys.argv) > 2 else "first"
claims = [int(l.split(": ", 1)[1])
          for l in pathlib.Path(name).read_text().splitlines()
          if l.startswith("claim: ")]
claim = claims[0] if mode == "first" else claims[-1]
actual = len(pathlib.Path("real.txt").read_text().splitlines())
json.dump({"observed": claim == actual, "claimed": claim, "actual": actual},
          sys.stdout)
'''


_SELFTEST_ENTRY = {
    'id': 'claim-vs-reality',
    'check': 'json',
    'command': ['python3', '-I', '-B', 'check.py', 'doc.md', 'first'],
    'asserted': True,
    'file': 'doc.md',
    'files': ['real.txt'],
}

_SELFTEST_STALE_ENTRY = {
    'id': 'stale-claim',
    'check': 'json',
    'command': ['python3', '-I', '-B', 'check.py', 'stale.md', 'first'],
    'asserted': True,
    'file': 'stale.md',
    'files': ['real.txt'],
}


def _selftest_repo(base):
    """A tiny git repo: doc.md claims 3 (true), stale.md claims 2 (false)."""
    repo = os.path.join(base, 'repo')
    os.makedirs(repo, exist_ok=True)
    run = lambda *a: subprocess.run(a, cwd=repo, capture_output=True, text=True)
    run('git', 'init', '-q', '-b', 'main')
    run('git', 'config', 'user.email', 'selftest@kaidoku.local')
    run('git', 'config', 'user.name', 'c2-counter selftest')
    with open(os.path.join(repo, 'doc.md'), 'w') as handle:
        handle.write('claim: 3\n')
    with open(os.path.join(repo, 'stale.md'), 'w') as handle:
        handle.write('claim: 2\n')
    with open(os.path.join(repo, 'real.txt'), 'w') as handle:
        handle.write('a\nb\nc\n')
    with open(os.path.join(repo, 'check.py'), 'w') as handle:
        handle.write(SELFTEST_CHECK)
    os.makedirs(os.path.join(repo, 'tools', 'round-44'), exist_ok=True)
    with open(os.path.join(repo, 'tools', 'round-44', 'other.py'), 'w') as handle:
        handle.write('# a frozen round-44 tool\n')
    with open(os.path.join(repo, 'tools', 'round-44', 'c2-rubric.json'), 'w') as handle:
        handle.write(_selftest_rubric([_SELFTEST_ENTRY]))
    run('git', 'add', '-A')
    run('git', 'commit', '-q', '-m', 'base')
    freeze = run('git', 'rev-parse', 'HEAD').stdout.strip()
    return repo, freeze


def _selftest_rubric(entries, frozen=None, frozen_dirs=None):
    doc = {
        'predicate': 'P44-C2',
        'frozen_paths': frozen if frozen is not None else ['doc.md'],
        'entries': entries,
    }
    if frozen_dirs:
        doc['frozen_dirs'] = frozen_dirs
    return json.dumps(doc, indent=1)


def selftest():
    base = os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
    root_dir = os.path.join(base, 'kaidoku-r44')
    os.makedirs(root_dir, exist_ok=True)
    work = tempfile.mkdtemp(prefix='c2-counter-selftest.', dir=root_dir)
    arms = []

    def record(name, expected, got, detail):
        arms.append({'arm': name, 'expected_exit': expected, 'exit_code': got,
                     'ok': expected == got, 'detail': detail})

    repo, freeze = _selftest_repo(work)
    entry = dict(_SELFTEST_ENTRY)

    def run_arm(name, rubric_text, expect, rev=None, use_repo_rubric=False,
                pre_freeze=False):
        # (the rubric text may name the repo's own base commit)
        rubric_file = None
        if not use_repo_rubric:
            rubric_file = os.path.join(work, 'rubric-%s.json' % name)
            with open(rubric_file, 'w') as handle:
                handle.write(rubric_text)
        try:
            res = score(repo, rev or freeze, freeze if not pre_freeze else None,
                        work, rubric_file, 'auto', DEFAULT_SEAT, keep_work=False,
                        pre_freeze=pre_freeze)
            code = res['exit_code']
            detail = {'mismatches': res['mismatches'],
                      'entries_evaluated': res['entries_evaluated'],
                      'unevaluable': [u.get('reason') for u in res['unevaluable']],
                      'frozen_path_changed': res['frozen_path_changed'],
                      'met_target': res['met_target'],
                      'pre_freeze': res['pre_freeze'],
                      'claim_score': res['claim_score']}
        except Unevaluable as exc:
            code = EXIT_CANT
            detail = {'unevaluable': exc.reason}
        record(name, expect, code, detail)
        return code

    def git_commit(message):
        subprocess.run(['git', '-C', repo, 'commit', '-qam', message],
                       capture_output=True, text=True)
        return subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'],
                              capture_output=True, text=True).stdout.strip()

    def reset():
        subprocess.run(['git', '-C', repo, 'reset', '-q', '--hard', freeze],
                       capture_output=True, text=True)

    # arm 1: a clean dev rubric at the base -> 0
    run_arm('clean', _selftest_rubric([entry]), EXIT_MET)

    # arm 2: a seeded mismatch on the reality side -> 1 (mismatch reported)
    with open(os.path.join(repo, 'real.txt'), 'w') as handle:
        handle.write('a\nb\n')
    seeded = git_commit('seeded reality')
    run_arm('seeded_mismatch_reality', _selftest_rubric([entry]), EXIT_FAIL, rev=seeded)
    reset()

    # arm 3: a seeded mismatch on the claim side (claim file not frozen) -> 1
    with open(os.path.join(repo, 'doc.md'), 'w') as handle:
        handle.write('claim: 2\n')
    seeded_claim = git_commit('seeded claim')
    run_arm('seeded_mismatch_claim', _selftest_rubric([entry], frozen=[]),
            EXIT_FAIL, rev=seeded_claim)
    reset()

    # arm 4: a rubric entry with no command -> 2 (malformed rubric)
    broken = dict(entry)
    broken.pop('command')
    run_arm('missing_command', _selftest_rubric([broken]), EXIT_CANT)

    # arm 5: the committed rubric edited after the freeze -> 2 (frozen_path_changed)
    rubric_in_repo = os.path.join(repo, 'tools', 'round-44', 'c2-rubric.json')
    with open(rubric_in_repo, 'w') as handle:
        handle.write(_selftest_rubric([entry]).replace('"asserted": true',
                                                       '"asserted": false'))
    rubric_edited = git_commit('rubric edited')
    run_arm('rubric_edited_after_freeze', None, EXIT_CANT, rev=rubric_edited,
            use_repo_rubric=True)
    reset()

    # arm 6: an appended repair bound by expected_edit -> 0
    with open(os.path.join(repo, 'doc.md'), 'a') as handle:
        handle.write('claim: 3\n')
    repaired = git_commit('appended repair')
    run_arm('bound_append_repair', _selftest_rubric([entry], frozen=[
        {'path': 'doc.md', 'expected_edit': {'append': ['claim: 3']}}]),
        EXIT_MET, rev=repaired)

    # arm 7: the same append without a bound expected_edit -> 2
    run_arm('unbound_append', _selftest_rubric([entry]), EXIT_CANT, rev=repaired)

    # arm 8: a note alone never repairs -> 1 (the mismatch stands)
    with open(os.path.join(repo, 'stale.md'), 'a') as handle:
        handle.write('claim: 3\n')
    noted = git_commit('appended correction note')
    stale = dict(_SELFTEST_STALE_ENTRY)
    run_arm('note_alone_does_not_repair', _selftest_rubric([stale], frozen=[
        {'path': 'stale.md', 'expected_edit': {'append': ['claim: 3']}}]),
        EXIT_FAIL, rev=noted)

    # arm 9: a note plus an independent re-derivation -> 0 (repaired)
    stale_repair = dict(_SELFTEST_STALE_ENTRY)
    stale_repair['repair_command'] = ['python3', '-I', '-B', 'check.py', 'stale.md',
                                      'last']
    run_arm('note_with_rederived_value', _selftest_rubric([stale_repair], frozen=[
        {'path': 'stale.md', 'expected_edit': {'append': ['claim: 3']}}]),
        EXIT_MET, rev=noted)

    # arm 10: an empty rubric -> 2 (no entry was evaluable)
    run_arm('empty_rubric', _selftest_rubric([]), EXIT_CANT)

    # arm 11: a file changed under a frozen directory pathspec -> 2
    with open(os.path.join(repo, 'tools', 'round-44', 'other.py'), 'w') as handle:
        handle.write('# a frozen round-44 tool, edited after the freeze\n')
    dir_changed = git_commit('round-44 tool edited')
    run_arm('frozen_dir_changed', _selftest_rubric([entry], frozen_dirs=[
        'tools/round-44']), EXIT_CANT, rev=dir_changed)
    reset()

    # arm 11b: a file ADDED under a frozen directory pathspec -> 2
    with open(os.path.join(repo, 'tools', 'round-44', 'added.py'), 'w') as handle:
        handle.write('# added after the freeze\n')
    subprocess.run(['git', '-C', repo, 'add', '-A'], capture_output=True, text=True)
    dir_added = git_commit('round-44 tool added')
    run_arm('frozen_dir_added', _selftest_rubric([entry], frozen_dirs=[
        'tools/round-44']), EXIT_CANT, rev=dir_added)
    reset()

    # arm 13: a weak expected_edit (marker only) -> 2 (malformed rubric)
    weak = dict(_SELFTEST_STALE_ENTRY)
    weak['expected_edit'] = {'marker': 'claim: 3'}
    run_arm('weak_expected_edit', _selftest_rubric([weak], frozen=[
        {'path': 'stale.md', 'expected_edit': {'marker': 'claim: 3'}}]),
        EXIT_CANT)

    # arm 14: the pre-freeze census of a rubric that declares the freeze -> 1
    census = json.dumps({
        'predicate': 'P44-C2', 'freeze': freeze,
        'frozen_paths': [], 'entries': [_SELFTEST_STALE_ENTRY]})
    run_arm('pre_freeze_with_declared_freeze', census, EXIT_FAIL, pre_freeze=True)

    # arm 12: the pre-freeze census at the base -> the mismatch is reported
    run_arm('pre_freeze_census', _selftest_rubric([_SELFTEST_STALE_ENTRY]),
            EXIT_FAIL, pre_freeze=True)

    ok = all(arm['ok'] for arm in arms)
    print(json.dumps({'selftest': 'P44-C2', 'ok': ok,
                      'arms': arms}, indent=1, sort_keys=True))
    shutil.rmtree(work, ignore_errors=True)
    return EXIT_MET if ok else EXIT_FAIL


# ---------------------------------------------------------------------- CLI
def main(argv=None):
    parser = argparse.ArgumentParser(
        description='P44-C2 calibration counter (frozen rubric, re-derived at REV).')
    parser.add_argument('--root')
    parser.add_argument('--rev')
    parser.add_argument('--freeze')
    parser.add_argument('--work')
    parser.add_argument('--json-out')
    parser.add_argument('--rubric')
    parser.add_argument('--export', default='auto')
    parser.add_argument('--seat', default=os.environ.get('HYAKU_SEAT', DEFAULT_SEAT))
    parser.add_argument('--keep-work', action='store_true')
    parser.add_argument('--pre-freeze', action='store_true',
                        help='base census: report the freeze walk but do not '
                             'enforce it (the freeze is not yet an ancestor)')
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--schema', action='store_true',
                        help='print the rubric schema contract and exit')
    args = parser.parse_args(argv)

    if args.schema:
        print(__doc__)
        return EXIT_MET
    if args.selftest:
        return selftest()
    if not (args.root and args.rev) or (not args.freeze and not args.pre_freeze):
        print('usage: --root --rev --freeze [--work --json-out] '
              '(--pre-freeze without --freeze) (or --selftest)', file=sys.stderr)
        return EXIT_CANT
    if not os.path.isdir(os.path.abspath(args.root)):
        print('root is not a directory: %s' % args.root, file=sys.stderr)
        return EXIT_CANT

    try:
        result = score(args.root, args.rev, args.freeze, args.work, args.rubric,
                       args.export, args.seat, keep_work=args.keep_work,
                       pre_freeze=args.pre_freeze)
    except Unevaluable as exc:
        payload = {'predicate': 'P44-C2', 'seat': args.seat, 'exit_code': EXIT_CANT,
                   'unevaluable': exc.reason, 'argv': sys.argv}
        payload.update(exc.receipt or {})
        print(json.dumps({'unevaluable': exc.reason, 'exit_code': EXIT_CANT},
                         sort_keys=True))
        if args.json_out:
            directory = os.path.dirname(os.path.abspath(args.json_out))
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(args.json_out, 'w') as handle:
                json.dump(payload, handle, indent=1, sort_keys=True)
        return EXIT_CANT

    summary = {
        'predicate': result['predicate'],
        'seat': result['seat'],
        'revision': result['revision'],
        'freeze': result['freeze'],
        'pre_freeze': result['pre_freeze'],
        'claim_score': result['claim_score'],
        'rubric_source': result['rubric_source'],
        'entries': result['entries_count'],
        'entries_evaluated': result['entries_evaluated'],
        'mismatches': result['mismatches'],
        'mismatches_count': result['mismatches_count'],
        'unevaluable_count': result['unevaluable_count'],
        'frozen_path_changed': result['frozen_path_changed'],
        'met_target': result['met_target'],
        'counter_sha256': result['counter_sha256'],
        'counter_sha256_at_freeze': result['counter_sha256_at_freeze'],
        'exit_code': result['exit_code'],
    }
    print(json.dumps(summary, sort_keys=True))
    if args.json_out:
        directory = os.path.dirname(os.path.abspath(args.json_out))
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(args.json_out, 'w') as handle:
            json.dump(result, handle, indent=1, sort_keys=True)
    return result['exit_code']


if __name__ == '__main__':
    sys.exit(main())
