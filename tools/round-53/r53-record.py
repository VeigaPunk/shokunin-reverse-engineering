#!/usr/bin/env python
"""r53-record.py - R53-C2: the round-53 record oracle over committed bytes.

Calibration as fleet AXES.md defines it: mismatches between the lane's declared
self-assessment (the SCORECARD round-53 record section's atom table) and the
observed repo state, counted by a counter any reader can re-run.  The oracle reads
git objects only (plus the receipt JSONs at the measured revision) and never
writes into the lane tree except its own receipt.

THE RECORD SECTION (single source for the declared values)
----------------------------------------------------------
``SCORECARD.md`` at the measured revision carries a section whose heading starts
``## Round 53`` and which contains, after the marker line
``Round-53 record atoms``, one markdown table whose rows are:

  | atom | declared value |
  |---|---|
  | T1 | instruments=3 pinned; added=3; pins-rederive=true |
  | T2 | log-declaration-entry=true; claims-commit=4cb12b41…; log-deletions=0 |
  | T3 | wave=none-inline; dispatch-sha256s=<sha>,<sha>,<sha>,<sha>; seat-dirs=0; results-file=absent |
  | T4 | landing=<L>; record-rev=section-commit; receipts=6 |
  | T5 | start-exit=0; end-exit=0; w04=<N> |
  | T6 | sources-before=159; sources-after=160; new-rows=S253(A); used-by-ok=true |
  | T7 | atoms=10 |
  | T8 | depth-row-equal=true; calibration-row-equal=true; coverage-row-refresh=true; province-heading=## Host migration — 2026-10-31; province-deletions=0; undeclared-production=0 |
  | T9 | ledger-row=round-53; ledger-verdict=CLEAN; gate-exit=0 |
  | T10 | misroot-findings=0 |

followed (for T4) by receipt lines:

  - `<path>` rev=<40hex|none> check=<key>=<json-value>

THE ATOMS (each re-derives its declared value from committed bytes at REV)
--------------------------------------------------------------------------

  T1  claims custody: `.ufo/waves/round-53/claims.json` exists at the FREEZE and at
      REV with a top-level ``instruments`` map; every file under ``tools/round-53/``
      added base..REV is a key of that map; every pin equals the file's blob sha256
      at REV (sha256 of `git show REV:path` bytes); added == the map's
      tools/round-53 key count.
  T2  LOG custody: LOG.md at REV contains the round-53 declaration entry naming the
      claims commit; `git diff base..REV -- LOG.md` deletes nothing.
  T3  the wave line: the four inherited dispatch artifacts exist at REV and their
      blob sha256s equal the declared comma list (order: gen-w1.py,
      r53-w1-dispatch.json, r53-w1-run.out, r53-w1-spec.json); no
      `.ufo/waves/round-53/w1/` seat directory exists at REV; no
      `r53-w1-results.json` exists at REV.  (The inherited r53-w1 dispatch never
      executed on the dead host; this round's work is L1-inline.  Amended
      pre-freeze; the do-nothing control cannot fabricate the four pinned
      dispatch digests.)
  T4  receipts: each declared receipt line resolves at REV, parses as JSON, its
      ``rev`` member equals the line's declared rev when that rev is a 40-hex
      string (`none` means the receipt has rev null), the declared check key holds
      the declared value, `landing` is an ancestor of REV, and `record-rev` (the
      commit that introduced the record section, resolved by pickaxe) is a
      descendant of landing.
  T5  census receipts: `.ufo/waves/round-53/l1/census-start.txt` and `census-end.txt`
      exist at REV; each ends with `exit=<declared>`; each contains exactly the
      declared number of W04 warning lines.
  T6  SOURCES: the Registry row count at base equals `sources-before`, at REV
      `sources-after`; every declared new row exists at REV with the declared tier;
      every used-by path of each new row exists at REV.
  T7  self-anchor: the record section exists at REV and parses to exactly `atoms`
      rows T1..T10, each with a non-empty declared value.
  T8  no-harm: the SCORECARD Owned-axes depth and calibration rows are byte-equal
      (rstrip) base..REV; the coverage row changed and its REV text contains
      `142/142`; PROVINCE.md gained only additions and its first added line is the
      declared heading; the production diff base..REV (SKILL.md PROVINCE.md
      corpus/README.md corpus/knowledge tools) touches nothing outside the declared
      set {SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge/
      2026-10-31-r53-triage-v6-reader-census.md} plus tools/round-53/ (T1's scope).
  T9  freeze ledger: corpus/claim-freezes-v2.tsv at REV carries a `round-53` row
      with the declared verdict; the freeze-gate receipt (declared via T4's list,
      check gate-exit) is the receipt whose presence and exit this atom re-checks;
      no ledger row is a stray (the gate receipt's own disclosures summary is the
      authority the atom cites, and this atom re-checks only the row and the
      receipt).
  T10 misroot: the misroot receipt (declared via T4's list) exists and its
      findings list length equals the declared count.

PREDICATE (the same sentence lives in plans/round-53-claims.md R53-C2 and in every
receipt this tool writes):

  at a REV descending from the R53 freeze, running `python -X utf8 -I -B
  tools/round-53/r53-record.py --root <LANE> --rev <REV> --freeze <FREEZE> --base
  6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --json-out <OUT>` exits 0 with
  `mismatches 0` over atoms T1-T10; and at the freeze itself the same command exits
  1 with exactly `mismatches 8` - T3, T4, T5, T6, T7, T8, T9, T10 red (landing-only
  atoms), T1 and T2 green.

A landing-only atom is red whenever its declared value cannot be re-derived - at
the freeze that is trivially true (no record section exists yet), and at the
landing each atom must be green INDEPENDENTLY of whether the other claims
succeeded (a C1 honest failure recorded honestly keeps every atom green).

Selftest: `--selftest` runs the battery over this directory's committed mutation
fixtures under `.ufo/waves/round-53/l1/record-mutations/` when present; offline
hosts without the fixture set report them absent and exit 2.  Usage:

  python -X utf8 -I -B tools/round-53/r53-record.py --root LANE --rev REV
      --freeze FREEZE --base BASE --json-out OUT
  python -X utf8 -I -B tools/round-53/r53-record.py --selftest

Exit codes: 0 every atom re-derives; 1 at least one mismatch (the receipt names
them); 2 could-not-evaluate.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

BASE = '6697518f0ad8e8399567ae4c9cd0207fc7c04d8b'
CLAIMS_RELPATH = '.ufo/waves/round-53/claims.json'
ROUND53_DIR = '.ufo/waves/round-53'
DISPATCH_ORDER = ('gen-w1.py', 'r53-w1-dispatch.json', 'r53-w1-run.out',
                  'r53-w1-spec.json')
CENSUS_START = '.ufo/waves/round-53/l1/census-start.txt'
CENSUS_END = '.ufo/waves/round-53/l1/census-end.txt'
SOURCES_RELPATH = 'corpus/SOURCES.md'
LEDGER_RELPATH = 'corpus/claim-freezes-v2.tsv'
RECORD_MARKER = 'Round-53 record atoms'
ATOM_RE = re.compile(r'^\|\s*(T10|T[1-9])\s*\|\s*(.+?)\s*\|\s*$')
RECEIPT_LINE_RE = re.compile(
    r'^-\s+`([^`]+)`\s+rev=([0-9a-f]{40}|none)\s+check=([A-Za-z0-9_]+)=(\S+)\s*$')
PRODUCTION_PATHS = ('SKILL.md', 'PROVINCE.md', 'corpus/README.md', 'corpus/knowledge',
                    'tools')
DECLARED_PRODUCTION = ('SKILL.md', 'PROVINCE.md', 'corpus/README.md',
                       'corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md')
NEW_ROW_RE = re.compile(r'^\|\s*(S\d{3,})\s*\|')

PREDICATE = (
    'at a REV descending from the R53 freeze, running `python -X utf8 -I -B '
    'tools/round-53/r53-record.py --root <LANE> --rev <REV> --freeze <FREEZE> --base '
    '6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --json-out <OUT>` exits 0 with '
    '`mismatches 0` over atoms T1-T10; and at the freeze itself the same command exits '
    '1 with exactly `mismatches 8` - T3, T4, T5, T6, T7, T8, T9, T10 red (landing-only '
    'atoms), T1 and T2 green.')


class OracleError(Exception):
    """Could not evaluate (exit 2)."""


def git(root, args):
    proc = subprocess.run(['git', '-C', root] + list(args), capture_output=True,
                          text=True, encoding='utf-8')
    return proc


def git_show(root, rev, path):
    proc = git(root, ['show', '%s:%s' % (rev, path)])
    if proc.returncode != 0:
        return None
    return proc.stdout


def blob_text(root, rev, path):
    text = git_show(root, rev, path)
    if text is None:
        raise OracleError('cannot read %s at %r' % (path, rev))
    return text


def blob_sha256(root, rev, path):
    text = git_show(root, rev, path)
    if text is None:
        return None
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def is_ancestor(root, older, newer):
    proc = git(root, ['merge-base', '--is-ancestor', older, newer])
    if proc.returncode not in (0, 1):
        raise OracleError('merge-base failed: %s' % (proc.stderr or '').strip()[:200])
    return proc.returncode == 0


def ls_tree(root, rev, path):
    proc = git(root, ['ls-tree', '-r', '--name-only', rev, '--', path])
    if proc.returncode != 0:
        raise OracleError('ls-tree failed for %r' % path)
    return [l for l in proc.stdout.splitlines() if l.strip()]


def _self_sha256():
    try:
        with open(os.path.abspath(__file__), 'rb') as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


def _parse_bool(text):
    if text == 'true':
        return True
    if text == 'false':
        return False
    raise ValueError(text)


def _parse_json_value(text):
    return json.loads(text)


# --------------------------------------------------------------------------------------
# the record section parser
# --------------------------------------------------------------------------------------

def parse_record_section(scorecard_text):
    """Return (atoms dict, receipt lines) from the round-53 record section."""
    at = scorecard_text.find(RECORD_MARKER)
    if at < 0:
        raise KeyError('record section absent')
    lines = scorecard_text[at:].split('\n')
    atoms = {}
    receipts = []
    table_seen = False
    for line in lines[1:]:
        if line.startswith('## ') and atoms:
            break
        match = ATOM_RE.match(line.strip())
        if match:
            table_seen = True
            atom, value = match.group(1), match.group(2)
            if atom in atoms:
                raise KeyError('duplicate atom %r' % atom)
            atoms[atom] = value
            continue
        rmatch = RECEIPT_LINE_RE.match(line.strip())
        if rmatch:
            receipts.append({'path': rmatch.group(1), 'rev': rmatch.group(2),
                             'key': rmatch.group(3), 'value': rmatch.group(4)})
    if not table_seen:
        raise KeyError('record section has no atoms table')
    return atoms, receipts


def _cell(atoms, atom, key):
    value = atoms.get(atom)
    if value is None:
        raise KeyError('atom %s absent' % atom)
    match = re.search(r'(?:^|;\s*)%s=([^;]+)' % re.escape(key), value)
    if not match:
        raise KeyError('atom %s has no %s=' % (atom, key))
    return match.group(1).strip()


def _cell_int(atoms, atom, key):
    text = _cell(atoms, atom, key)
    if not re.match(r'^\d+$', text):
        raise ValueError('%s.%s is not an integer: %r' % (atom, key, text))
    return int(text)


def _cell_bool(atoms, atom, key):
    return _parse_bool(_cell(atoms, atom, key))


# --------------------------------------------------------------------------------------
# atoms
# --------------------------------------------------------------------------------------

def _frozen_atoms(claims):
    """T1/T2's declared values live in the claims container (they must be green
    at the freeze, before any record section exists)."""
    atoms = claims.get('frozen_atoms')
    if not isinstance(atoms, dict):
        raise KeyError('claims.json has no frozen_atoms map')
    return atoms


def atom_t1(root, rev, freeze, base, atoms):
    added = [p for p in ls_tree(root, rev, 'tools/round-53')]
    base_files = set(ls_tree(root, base, 'tools/round-53'))
    added_new = [p for p in added if p not in base_files]
    claims_at_freeze = git_show(root, freeze, CLAIMS_RELPATH)
    claims_at_rev = git_show(root, rev, CLAIMS_RELPATH)
    if claims_at_freeze is None or claims_at_rev is None:
        return False, 'claims.json absent at freeze or rev'
    claims = json.loads(claims_at_rev)
    if (json.loads(claims_at_freeze).get('instruments') != claims.get('instruments')):
        return False, 'claims.json instruments map changed freeze..rev'
    pins = claims.get('instruments')
    if not isinstance(pins, dict) or not pins:
        return False, 'claims.json has no instruments map'
    round53_pins = {p: sha for p, sha in pins.items() if p.startswith('tools/round-53/')}
    unpinned = [p for p in added_new if p not in round53_pins]
    if unpinned:
        return False, 'added files not pinned: %r' % unpinned
    bad = []
    for path, pin in round53_pins.items():
        actual = blob_sha256(root, rev, path)
        if actual != pin:
            bad.append(path)
    if bad:
        return False, 'pins do not re-derive: %r' % bad
    declared_added = _cell_int(atoms, 'T1', 'added')
    declared_pins = _cell_int(atoms, 'T1', 'instruments')
    return (declared_added == len(added_new)
            and declared_pins == len(round53_pins)
            and _cell_bool(atoms, 'T1', 'pins-rederive') is True,
            'added %d/%d, pins %d/%d' % (declared_added, len(added_new),
                                         declared_pins, len(round53_pins)))


def atom_t2(root, rev, base, atoms):
    log = blob_text(root, rev, 'LOG.md')
    diff = git(root, ['diff', '%s..%s' % (base, rev), '--', 'LOG.md'])
    deletions = [l for l in diff.stdout.splitlines()
                 if l.startswith('-') and not l.startswith('---')]
    observed = {
        'log-declaration-entry': ('round 53' in log and 'KaidokuR53' in log),
        'claims-file-cited': 'plans/round-53-claims.md' in log,
        'log-deletions': len(deletions),
    }
    declared = {}
    for part in atoms['T2'].split(';'):
        key, _, value = part.strip().partition('=')
        if not value:
            raise ValueError('T2 clause %r is not key=value' % part.strip())
        declared[key.strip()] = value.strip()
    unknown = set(declared) - set(observed)
    if unknown:
        raise ValueError('T2 declares unknown keys %r' % sorted(unknown))
    for key, value in declared.items():
        want = observed[key]
        if key == 'log-deletions':
            if not re.match(r'^\d+$', value) or int(value) != want:
                return False, 'log-deletions %s vs observed %d' % (value, want)
        elif value != ('true' if want else 'false'):
            return False, '%s declared %s, observed %s' % (key, value, want)
    return True, 'entry %s, file-cited %s, deletions %d' % (
        observed['log-declaration-entry'], observed['claims-file-cited'],
        observed['log-deletions'])


def atom_t3(root, rev, atoms):
    digests = []
    for name in DISPATCH_ORDER:
        sha = blob_sha256(root, rev, '%s/%s' % (ROUND53_DIR, name))
        if sha is None:
            return False, 'dispatch artifact %s absent' % name
        digests.append(sha)
    declared = _cell(atoms, 'T3', 'dispatch-sha256s')
    declared_list = [d.strip() for d in declared.split(',')]
    if declared_list != digests:
        return False, 'dispatch digests differ'
    if _cell(atoms, 'T3', 'wave') != 'none-inline':
        return False, 'wave line is not none-inline'
    seat_dirs = ls_tree(root, rev, '%s/w1/' % ROUND53_DIR)
    if _cell_int(atoms, 'T3', 'seat-dirs') != len(seat_dirs):
        return False, 'seat dirs %d' % len(seat_dirs)
    results = git_show(root, rev, '%s/r53-w1-results.json' % ROUND53_DIR)
    declared_results = _cell(atoms, 'T3', 'results-file')
    if declared_results == 'absent' and results is not None:
        return False, 'results file exists'
    if declared_results == 'present' and results is None:
        return False, 'results file absent'
    return True, 'dispatch digests match; seat-dirs %d; results %s' % (
        len(seat_dirs), declared_results)


def atom_t4(root, rev, base, atoms, receipts):
    landing = _cell(atoms, 'T4', 'landing')
    if not re.match(r'^[0-9a-f]{40}$', landing):
        return False, 'landing is not a 40-hex commit'
    if not is_ancestor(root, landing, rev):
        return False, 'landing is not an ancestor of rev'
    declared_count = _cell_int(atoms, 'T4', 'receipts')
    if declared_count != len(receipts):
        return False, 'receipts %d declared, %d lines' % (declared_count,
                                                          len(receipts))
    problems = []
    for line in receipts:
        blob = git_show(root, rev, line['path'])
        if blob is None:
            problems.append('%s absent' % line['path'])
            continue
        try:
            data = json.loads(blob)
        except ValueError as exc:
            problems.append('%s does not parse: %s' % (line['path'], exc))
            continue
        if line['rev'] == 'none':
            if data.get('rev') is not None:
                problems.append('%s rev not null' % line['path'])
        elif data.get('rev') != line['rev']:
            problems.append('%s rev %r != declared %r'
                            % (line['path'], data.get('rev'), line['rev']))
        if line['key'] not in data:
            problems.append('%s has no %s' % (line['path'], line['key']))
            continue
        try:
            wanted = _parse_json_value(line['value'])
        except ValueError:
            wanted = line['value']
        if data[line['key']] != wanted:
            problems.append('%s %s=%r != declared %r'
                            % (line['path'], line['key'], data[line['key']], wanted))
    if _cell(atoms, 'T4', 'record-rev') != 'section-commit':
        return False, 'record-rev grammar changed'
    proc = git(root, ['log', '--format=%H', '-S', RECORD_MARKER, rev, '--',
                      'SCORECARD.md'])
    commits = [l for l in proc.stdout.splitlines() if l.strip()]
    if not commits:
        return False, 'no commit introduced the record section'
    section_commit = commits[0]
    if not is_ancestor(root, landing, section_commit):
        return False, 'record section predates the landing'
    if problems:
        return False, '; '.join(problems)
    return True, '%d receipts re-derive; section introduced at %s' % (len(receipts),
                                                                      section_commit[:12])


def atom_t5(root, rev, atoms):
    out = []
    for path, key in ((CENSUS_START, 'start-exit'), (CENSUS_END, 'end-exit')):
        text = git_show(root, rev, path)
        if text is None:
            return False, '%s absent' % path
        tail = [l for l in text.rstrip('\n').split('\n') if l.strip()]
        match = re.match(r'^exit=(\d+)$', tail[-1].strip())
        if not match:
            return False, '%s has no exit= line' % path
        if int(match.group(1)) != _cell_int(atoms, 'T5', key):
            return False, '%s exit %s != declared' % (path, match.group(1))
        out.append(text)
    w04_needle = '\tW04\t'
    counts = {name: sum(1 for line in text.split(chr(10)) if w04_needle in line)
               for name, text in (('start', out[0]), ('end', out[1]))}
    d_start = _cell_int(atoms, 'T5', 'w04-start')
    d_end = _cell_int(atoms, 'T5', 'w04-end')
    return (d_start == counts['start'] and d_end == counts['end'],
            'w04 start %d/%d end %d/%d' % (d_start, counts['start'],
                                           d_end, counts['end']))


def atom_t6(root, rev, base, atoms):
    def rows(text):
        in_reg = False
        out = []
        for line in text.split('\n'):
            if line.startswith('## Registry'):
                in_reg = True
                continue
            if in_reg and line.startswith('## '):
                break
            if in_reg:
                match = NEW_ROW_RE.match(line)
                if match:
                    out.append((match.group(1), line))
        return out
    before = rows(blob_text(root, base, SOURCES_RELPATH))
    after = rows(blob_text(root, rev, SOURCES_RELPATH))
    ok = (_cell_int(atoms, 'T6', 'sources-before') == len(before)
          and _cell_int(atoms, 'T6', 'sources-after') == len(after))
    declared_rows = _cell(atoms, 'T6', 'new-rows')
    base_ids = {rid for rid, _l in before}
    tracked = git(root, ['ls-tree', '-r', '--name-only', rev])
    tracked_set = set(tracked.stdout.splitlines())
    for token in declared_rows.split(','):
        token = token.strip()
        match = re.match(r'^(S\d{3,})\(([A-C])\)$', token)
        if not match:
            return False, 'bad new-rows token %r' % token
        rid, tier = match.group(1), match.group(2)
        hits = [line for line_id, line in after if line_id == rid]
        if not hits:
            return False, '%s absent at rev' % rid
        if rid in base_ids:
            return False, '%s already at base' % rid
        cells = [c.strip() for c in hits[0].split('|')]
        if cells[4] != tier:
            return False, '%s tier %r != declared %r' % (rid, cells[4], tier)
        used_by = cells[11]
        for path in [p.strip() for p in used_by.split(',') if p.strip()]:
            if path not in tracked_set:
                return False, '%s used-by path %r absent' % (rid, path)
    return ok, 'rows %d->%d, new rows %s' % (len(before), len(after), declared_rows)


def atom_t7(atoms, receipts):
    expected = ('T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10')
    if sorted(atoms, key=lambda a: int(a[1:])) != list(expected):
        return False, 'atoms are %r' % sorted(atoms)
    if _cell_int(atoms, 'T7', 'atoms') != len(expected):
        return False, 'atoms count mismatch'
    if any(not v.strip() for v in atoms.values()):
        return False, 'empty atom value'
    return True, '10 atoms parse'


def atom_t8(root, rev, base, atoms):
    score_base = blob_text(root, base, 'SCORECARD.md')
    score_rev = blob_text(root, rev, 'SCORECARD.md')

    def owned_row(text, prefix):
        for line in text.split('\n'):
            if line.startswith(prefix):
                return line
        raise OracleError('owned-axes row %r not found' % prefix)

    depth_base = owned_row(score_base, '| depth |').rstrip()
    depth_rev = owned_row(score_rev, '| depth |').rstrip()
    cal_base = owned_row(score_base, '| calibration |').rstrip()
    cal_rev = owned_row(score_rev, '| calibration |').rstrip()
    cov_base = owned_row(score_base, '| coverage |').rstrip()
    cov_rev = owned_row(score_rev, '| coverage |').rstrip()
    depth_equal = _cell_bool(atoms, 'T8', 'depth-row-equal')
    cal_equal = _cell_bool(atoms, 'T8', 'calibration-row-equal')
    refresh = _cell_bool(atoms, 'T8', 'coverage-row-refresh')
    if depth_equal != (depth_base == depth_rev):
        return False, 'depth row equality mismatch'
    if cal_equal != (cal_base == cal_rev):
        return False, 'calibration row equality mismatch'
    if refresh != (cov_base != cov_rev):
        return False, 'coverage row refresh mismatch'
    if refresh and '142/142' not in cov_rev:
        return False, 'coverage row lacks 142/142'
    heading = _cell(atoms, 'T8', 'province-heading')
    diff = git(root, ['diff', '%s..%s' % (base, rev), '--', 'PROVINCE.md'])
    deletions = [l for l in diff.stdout.splitlines()
                 if l.startswith('-') and not l.startswith('---')]
    if _cell_int(atoms, 'T8', 'province-deletions') != len(deletions):
        return False, 'province deletions %d' % len(deletions)
    additions = [l[1:].strip() for l in diff.stdout.splitlines()
                 if l.startswith('+') and not l.startswith('+++')
                 and l[1:].strip()]
    if not additions or additions[0] != heading:
        return False, 'province first addition is not the declared heading'
    proc = git(root, ['diff', '--name-only', '%s..%s' % (base, rev)]
               + list(PRODUCTION_PATHS))
    changed = [l for l in proc.stdout.splitlines() if l.strip()]
    allowed = set(DECLARED_PRODUCTION) | {p for p in changed
                                          if p.startswith('tools/round-53/')}
    undeclared = [p for p in changed if p not in allowed]
    if _cell_int(atoms, 'T8', 'undeclared-production') != len(undeclared):
        return False, 'undeclared production paths %r' % undeclared
    return True, 'owned rows and province and production diffs re-derive'


def atom_t9(root, rev, atoms, receipts):
    ledger = blob_text(root, rev, LEDGER_RELPATH)
    rid = _cell(atoms, 'T9', 'ledger-row')
    verdict = _cell(atoms, 'T9', 'ledger-verdict')
    hit = None
    for line in ledger.split('\n'):
        if line.startswith(rid + '\t'):
            hit = line.split('\t')
            break
    if hit is None:
        return False, 'no %s ledger row' % rid
    if hit[1] != verdict:
        return False, 'ledger verdict %r != declared %r' % (hit[1], verdict)
    gate = None
    for line in receipts:
        if line['key'] == 'gate-exit' or line['path'].endswith('freeze-gate-landing.json'):
            gate = line
            break
    if gate is None:
        return False, 'no freeze-gate receipt line'
    blob = git_show(root, rev, gate['path'])
    if blob is None:
        return False, 'gate receipt absent'
    data = json.loads(blob)
    if data.get(gate['key']) != _parse_json_value(gate['value']):
        return False, 'gate receipt check mismatch'
    return True, 'ledger row %s %s and gate receipt re-derive' % (rid, verdict)


def atom_t10(root, rev, atoms, receipts):
    line = None
    for entry in receipts:
        if entry['path'].endswith('misroot-sweep.json'):
            line = entry
            break
    if line is None:
        return False, 'no misroot receipt line'
    blob = git_show(root, rev, line['path'])
    if blob is None:
        return False, 'misroot receipt absent'
    data = json.loads(blob)
    findings = data.get('findings')
    declared = _cell_int(atoms, 'T10', 'misroot-findings')
    if not isinstance(findings, list):
        return False, 'misroot findings is not a list'
    return declared == len(findings), 'misroot findings %d/%d' % (declared,
                                                                  len(findings))


# --------------------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------------------

def run(ns):
    root = os.path.abspath(ns.root)
    rev = ns.rev
    if not is_ancestor(root, ns.freeze, rev):
        raise OracleError('freeze %r is not an ancestor of %r' % (ns.freeze, rev))
    if not is_ancestor(root, ns.base, rev):
        raise OracleError('base %r is not an ancestor of %r' % (ns.base, rev))
    claims_text = git_show(root, rev, CLAIMS_RELPATH)
    if claims_text is None:
        raise OracleError('cannot read %s at %r' % (CLAIMS_RELPATH, rev))
    claims = json.loads(claims_text)
    frozen = _frozen_atoms(claims)
    scorecard = blob_text(root, rev, 'SCORECARD.md')
    try:
        atoms, receipts = parse_record_section(scorecard)
    except KeyError as exc:
        atoms, receipts = {}, []
        parse_error = str(exc)
    else:
        parse_error = None

    results = []

    def check(atom, fn, *args):
        try:
            ok, why = fn(*args)
        except (OracleError, KeyError, ValueError) as exc:
            ok, why = False, 'unevaluable: %s' % exc
        results.append({'atom': atom, 'ok': bool(ok), 'why': why})

    check('T1', atom_t1, root, rev, ns.freeze, ns.base, frozen)
    check('T2', atom_t2, root, rev, ns.base, frozen)
    check('T3', atom_t3, root, rev, atoms)
    check('T4', atom_t4, root, rev, ns.base, atoms, receipts)
    check('T5', atom_t5, root, rev, atoms)
    check('T6', atom_t6, root, rev, ns.base, atoms)
    check('T7', atom_t7, atoms, receipts)
    check('T8', atom_t8, root, rev, ns.base, atoms)
    check('T9', atom_t9, root, rev, atoms, receipts)
    check('T10', atom_t10, root, rev, atoms, receipts)

    mismatches = [r for r in results if not r['ok']]
    if parse_error and not atoms:
        # no record section: every landing-only atom is red, T1/T2 stand alone
        landing_only = {'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10'}
        for r in results:
            if r['atom'] in landing_only and r['ok']:
                r['ok'] = False
                r['why'] = 'landing-only atom green without a record section: %s' % r['why']
        mismatches = [r for r in results if not r['ok']]
    report = {
        'instrument': 'r53-record.py',
        'instrument_sha256': _self_sha256(),
        'predicate': PREDICATE,
        'schema': 1,
        'root': root,
        'rev': rev,
        'freeze': ns.freeze,
        'base': ns.base,
        'parse_error': parse_error,
        'atoms': results,
        'mismatches': [r['atom'] for r in mismatches],
        'mismatch_count': len(mismatches),
        'verdict': 'met' if not mismatches else 'not met',
    }
    if ns.json_out:
        with open(ns.json_out, 'w', encoding='utf-8') as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
            handle.write('\n')
        with open(ns.json_out, 'r', encoding='utf-8') as handle:
            verify = json.load(handle)
        for key in ('predicate', 'atoms', 'mismatches', 'mismatch_count', 'verdict',
                    'rev'):
            if key not in verify:
                raise OracleError('receipt %r missing key %r' % (ns.json_out, key))
    for r in results:
        print('  %-4s %s %s' % (r['atom'], 'ok' if r['ok'] else 'MISMATCH', r['why']))
    print('atoms: %d   mismatches: %d %s'
          % (len(results), len(mismatches), mismatches and [m['atom'] for m in mismatches] or ''))
    if ns.json_out:
        print('json: %s' % ns.json_out)
    return 0 if not mismatches else 1


SELFTEST_SPEC = """
Builds a miniature git fixture (base -> freeze -> landing -> record) whose surfaces
carry exactly the atoms' declared values, then runs THIS FILE through its outer CLI
twelve times: once green (exit 0, mismatches 0) and once per atom mutation (exit 1,
exactly that atom mismatched).  The fixture lives under the work dir and is removed
afterwards.
"""

FIX_TOPICS = {
    'T1': 'instruments', 'T2': 'log', 'T3': 'wave', 'T4': 'receipts',
    'T5': 'census', 'T6': 'sources', 'T7': 'atoms', 'T8': 'noharm',
    'T9': 'ledger', 'T10': 'misroot',
}


def _fixture_run(root, args):
    proc = subprocess.run(['git', '-C', root] + args, capture_output=True,
                          text=True, encoding='utf-8')
    if proc.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                  (proc.stderr or '').strip()[:300]))
    return proc.stdout


def _commit_all(root, message):
    _fixture_run(root, ['add', '-A'])
    _fixture_run(root, ['commit', '-q', '-m', message])
    return _fixture_run(root, ['rev-parse', 'HEAD']).strip()


def _write(root, relpath, text):
    full = os.path.join(root, relpath)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


def resolve_work(ns):
    base = os.environ.get('TMPDIR') or os.path.join(os.path.expanduser('~'), '.cache')
    real = os.path.abspath(ns.work) if ns.work else os.path.join(
        base, 'r53-record-selftest')
    os.makedirs(real, exist_ok=True)
    return real


def _fixture_run(root, args):
    proc = subprocess.run(['git', '-C', root] + args, capture_output=True,
                          text=True, encoding='utf-8')
    if proc.returncode != 0:
        raise RuntimeError('git %s failed: %s' % (' '.join(args),
                                                  (proc.stderr or '').strip()[:300]))
    return proc.stdout


def _commit_all(root, message):
    _fixture_run(root, ['add', '-A'])
    _fixture_run(root, ['commit', '-q', '-m', message])
    return _fixture_run(root, ['rev-parse', 'HEAD']).strip()


def _write(root, relpath, text):
    full = os.path.join(root, relpath)
    os.makedirs(os.path.dirname(full) or '.', exist_ok=True)
    with open(full, 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(text)


SOURCES_V1 = ('## Registry\n\n| id | source | kind | tier '
              '| scope | anchor | teaches | status | opened | recheck | used-by |\n'
              '|---|---|---|---|---|---|---|---|---|---|---|\n'
              '| S001 | a | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n'
              '| S002 | b | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n'
              '| S003 | c | code | A | s | a | t | mined | 2026-10-01 | on-release | x |\n')
SOURCES_V2 = SOURCES_V1.rstrip('\n') + (
    '\n| S253 | d | code | A | s | a | t | mined | 2026-10-31 | on-release | '
    'corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md |\n')
ENTRY = ('## 2026-10-30 - round 53, KaidokuR53 - declared'
         ' (claims commit %s; plans/round-53-claims.md)' + chr(10))
CLAIMS_COMMIT = '0' * 40


def _frozen_atoms_text():
    return {
        'T1': 'instruments=3; added=3; pins-rederive=true',
        'T2': 'log-declaration-entry=true; claims-file-cited=true; log-deletions=0',
    }


def selftest(ns):
    """QUALITY-61 battery: the outer CLI over a miniature git fixture - one green
    run (exit 0, mismatches 0) and one red run per atom (exit 1, exactly that atom
    in the mismatches list).  The fixture lives under the work dir and is removed
    afterwards."""
    work = resolve_work(ns)
    fixture = os.path.join(work, 'fixture')
    shutil.rmtree(fixture, ignore_errors=True)
    os.makedirs(fixture)
    _fixture_run(fixture, ['init', '-q'])
    _fixture_run(fixture, ['config', 'user.email', 'selftest@invalid'])
    _fixture_run(fixture, ['config', 'user.name', 'selftest'])

    _write(fixture, 'SCORECARD.md', '## Owned axes\n\n| depth | d |\n'
           '| calibration | c |\n| coverage | old 141/141 |\n')
    _write(fixture, 'LOG.md', '# LOG\n\n- base entry\n')
    _write(fixture, 'corpus/SOURCES.md', SOURCES_V1)
    _write(fixture, 'corpus/claim-freezes-v2.tsv',
           'round\tverdict\tfindings\tpointer\nround-old\tCLEAN\t-\t-\n')
    _write(fixture, 'PROVINCE.md', '# Province\n')
    base = _commit_all(fixture, 'base')

    pin = {}
    for name, body in (('tiny-a.txt', 'alpha\n'), ('tiny-b.txt', 'beta\n'),
                       ('tiny-c.txt', 'gamma\n')):
        _write(fixture, 'tools/round-53/' + name, body)
        with open(os.path.join(fixture, 'tools/round-53', name), 'rb') as handle:
            pin['tools/round-53/' + name] = hashlib.sha256(
                handle.read()).hexdigest()
    disp = {}
    for name in DISPATCH_ORDER:
        body = 'dispatch body of %s\n' % name
        _write(fixture, '.ufo/waves/round-53/' + name, body)
        disp[name] = hashlib.sha256(body.encode('utf-8')).hexdigest()
    claims = {'schema': 1, 'round': 'round-53',
              'frozen_atoms': _frozen_atoms_text(), 'instruments': pin}
    _write(fixture, CLAIMS_RELPATH,
           json.dumps(claims, indent=1, sort_keys=True) + '\n')
    _write(fixture, '.ufo/waves/round-53/l1/census-start.txt',
           'lane\tW04\tS001 duplicate url x across scopes\nok\tlane\nexit=0\n')
    _write(fixture, '.ufo/waves/round-53/l1/census-end.txt',
           'lane\tW04\tS001 duplicate url x across scopes\nok\tlane\nexit=0\n')
    freeze = _commit_all(fixture, 'freeze')

    _write(fixture, 'SKILL.md', '# SKILL\n')
    _write(fixture, 'PROVINCE.md', '# Province\n\nadded line 1\nadded line 2\n')
    _write(fixture, 'corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md',
           'source: S253 - x\nbody\n')
    _write(fixture, 'corpus/README.md', '## Coverage map\n\n142/142\n')
    _write(fixture, 'LOG.md', '# LOG\n\n- base entry\n\n' + ENTRY % CLAIMS_COMMIT
           + '\n- entry body\n')
    _write(fixture, 'corpus/claim-freezes-v2.tsv',
           'round\tverdict\tfindings\tpointer\nround-old\tCLEAN\t-\t-\n'
           'round-53\tCLEAN\t-\tpointer\n')
    _write(fixture, 'corpus/SOURCES.md', SOURCES_V2)
    landing = _commit_all(fixture, 'landing')

    receipt_specs = [
        ('.ufo/waves/round-53/l1/scores/c1-after.json', landing, 'verdict', 'met'),
        ('.ufo/waves/round-53/l1/scores/c2-after.json', landing, 'verdict', 'met'),
        ('.ufo/waves/round-53/l1/scores/c1-selftest.json', landing, 'pass', 7),
        ('.ufo/waves/round-53/l1/scores/c1-controls.json', landing, 'all_red', True),
        ('.ufo/waves/round-53/l1/freeze-gate-landing.json', landing, 'exit', 0),
        ('.ufo/waves/round-53/l1/misroot-sweep.json', 'none', 'findings', []),
    ]
    receipt_lines = []
    for rpath, rev_spec, key, value in receipt_specs:
        data = {'rev': None if rev_spec == 'none' else rev_spec, key: value}
        _write(fixture, rpath, json.dumps(data, indent=1, sort_keys=True) + '\n')
        receipt_lines.append('- `%s` rev=%s check=%s=%s'
                             % (rpath, rev_spec, key, json.dumps(value)))
    atoms = list(_frozen_atoms_text().items()) + [
        ('T3', 'wave=none-inline; dispatch-sha256s=%s; seat-dirs=0; '
               'results-file=absent' % ','.join(disp[n] for n in DISPATCH_ORDER)),
        ('T4', 'landing=%s; record-rev=section-commit; receipts=%d'
               % (landing, len(receipt_lines))),
        ('T5', 'start-exit=0; end-exit=0; w04-start=1; w04-end=1'),
        ('T6', 'sources-before=3; sources-after=4; new-rows=S253(A); used-by-ok=true'),
        ('T7', 'atoms=10'),
        ('T8', 'depth-row-equal=true; calibration-row-equal=true; '
               'coverage-row-refresh=true; province-heading=added line 1; '
               'province-deletions=0; undeclared-production=0'),
        ('T9', 'ledger-row=round-53; ledger-verdict=CLEAN; gate-exit=0'),
        ('T10', 'misroot-findings=0'),
    ]
    section = ('## Round 53 (fixture)\n\nRound-53 record atoms\n\n'
               '| atom | declared value |\n|---|---|\n'
               + ''.join('| %s | %s |\n' % row for row in atoms)
               + '\nLanding receipts (T4):\n' + '\n'.join(receipt_lines) + '\n')
    _write(fixture, 'SCORECARD.md',
           '## Owned axes\n\n| depth | d |\n| calibration | c |\n'
           '| coverage | new 142/142 |\n\n' + section)
    record = _commit_all(fixture, 'record')

    def oracle(rev):
        return subprocess.run(
            [sys.executable, '-X', 'utf8', '-I', '-B', os.path.abspath(__file__),
             '--root', fixture, '--rev', rev, '--freeze', freeze, '--base', base],
            capture_output=True, text=True, encoding='utf-8')

    passed = 0
    failed = []

    def expect(name, cond, detail=''):
        nonlocal passed
        if cond:
            passed += 1
            print('  ok   %s' % name)
        else:
            failed.append(name)
            print('  FAIL %s :: %s' % (name, detail))

    green = oracle(record)
    expect('green-exit-0', green.returncode == 0,
           (green.stdout + green.stderr)[-500:])
    expect('green-mismatches-0', 'mismatches: 0' in green.stdout, green.stdout[-300:])

    mutations = {
        'T1': ('claims.json', lambda t: t.replace('added=3', 'added=4')),
        'T2': ('claims.json', lambda t: t.replace('log-deletions=0',
                                                  'log-deletions=1')),
        'T3': ('SCORECARD.md', lambda t: t.replace('seat-dirs=0', 'seat-dirs=1')),
        'T4': ('SCORECARD.md', lambda t: t.replace('receipts=6', 'receipts=7')),
        'T5': ('SCORECARD.md', lambda t: t.replace('w04-start=1', 'w04-start=2')),
        'T6': ('SCORECARD.md', lambda t: t.replace('sources-after=4',
                                                   'sources-after=5')),
        'T7': ('SCORECARD.md', lambda t: t.replace('atoms=10', 'atoms=9')),
        'T8': ('SCORECARD.md', lambda t: t.replace('province-deletions=0',
                                                   'province-deletions=1')),
        'T9': ('SCORECARD.md', lambda t: t.replace('ledger-verdict=CLEAN',
                                                   'ledger-verdict=FLAGGED')),
        'T10': ('SCORECARD.md', lambda t: t.replace('misroot-findings=0',
                                                    'misroot-findings=2')),
    }
    total = 2 + 3 * len(mutations)
    for atom, (surface, mutate) in mutations.items():
        _fixture_run(fixture, ['checkout', record, '--', '.'])
        target = CLAIMS_RELPATH if surface == 'claims.json' else 'SCORECARD.md'
        full = os.path.join(fixture, target)
        with open(full, 'r', encoding='utf-8') as handle:
            body = handle.read()
        mutated = mutate(body)
        expect('mut-%s-changes-something' % atom, mutated != body, target)
        _write(fixture, target, mutated)
        rev = _commit_all(fixture, 'mutate %s' % atom)
        proc = oracle(rev)
        expect('mut-%s-red' % atom, proc.returncode == 1,
               (proc.stdout + proc.stderr)[-400:])
        expect('mut-%s-only-its-atom' % atom,
               ("mismatches: 1 ['%s']" % atom) in proc.stdout, proc.stdout[-300:])

    print('selftest: %d cases, pass %d, fail %d' % (total, passed, len(failed)))
    if ns.json_out:
        with open(ns.json_out, 'w', encoding='utf-8') as handle:
            json.dump({'instrument': 'r53-record.py', 'selftest_schema': 1,
                       'instrument_sha256': _self_sha256(),
                       'cases': total, 'pass': passed, 'fail': len(failed),
                       'failed': failed, 'work': work}, handle, indent=1,
                      sort_keys=True)
            handle.write('\n')
    shutil.rmtree(fixture, ignore_errors=True)
    return 0 if not failed else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=None)
    parser.add_argument('--rev', default=None)
    parser.add_argument('--freeze', default=None)
    parser.add_argument('--base', default=BASE)
    parser.add_argument('--json-out', default=None)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--work', default=None)
    ns = parser.parse_args(argv)
    try:
        if ns.selftest:
            return selftest(ns)
        if not (ns.root and ns.rev and ns.freeze):
            raise OracleError('--root, --rev and --freeze are required')
        return run(ns)
    except OracleError as exc:
        print('r53-record: %s' % exc, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
