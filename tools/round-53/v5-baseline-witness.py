#!/usr/bin/env python
"""v5-baseline-witness.py - R53-C1's before-arm: the v5 table's executability debt.

Replays the LANDED v5 triage table (SKILL.md rule block 26) at the declared base
revision over the frozen round-42 recon corpus, and audits the labels against the
frozen fixture-level reader census (tools/round-53/reader-census.json, read from git
at the FREEZE revision).  The audit counts exactly what R53-C1 fixes:

  executability_violations  envelopes the v5 table routes with the action
                            ``cross-read-legacy`` while their census status is
                            NO-READER - a cross-read prescribed on bytes no reader
                            can open.  At the declared base this is 1, naming
                            ``dmg_Z3_v3ddwrt_inode_table``.
  clean_residue             envelopes the v5 table labels ``clean`` while their
                            census status is NO-READER - an oracle-backed action
                            with no oracle.  At the declared base this is 7.

The witness is the claim's do-nothing control: a red here is the before-state, and
the v6 instrument's after-run (0/0) is measured against it.  It parses the v5 table
with the v5 grammar (13 columns, ``<!-- sqfs-triage-table v5 -->`` marker) and
replays the v5 family-level evaluator, so its labels are the landed v5 labels, not
the v6 ones.  Read-only: git objects and envelope files in, one receipt out; no REA,
no carriers, no network, nothing written into the lane tree.

PREDICATE (the same sentence lives in plans/round-53-claims.md R53-C1 and in every
receipt this tool writes):

  at the declared base the frozen witness command `python -X utf8 -I -B
  tools/round-53/v5-baseline-witness.py --root <LANE> --rev
  6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --freeze <FREEZE> --envelopes <DIR>
  --json-out <OUT2>` exits 1 with `executability_violations 1` naming
  `dmg_Z3_v3ddwrt_inode_table` and `clean_residue 7` naming the seven no-reader
  `clean` envelopes.

Exit codes: 1 when the audit finds any violation or residue (the expected before
state); 0 when the base table is clean (which would falsify the claim's before-arm);
2 could-not-evaluate.
"""

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys

MARKER_V5 = '<!-- sqfs-triage-table v5 -->'
ACTIONS_PREFIX = '<!-- sqfs-triage-actions:'
ACTIONS_SUFFIX = '-->'
HEADER = ['label', 'operation', 'provider', 'handler', 'failing handler', 'gap kinds',
          'dependencies', '-be in child argv', 'symlink removed', 'published files',
          'action', 'cause', 'source']
BE_VALUES = ('yes', 'no', 'n/a')
FILES_VALUES = ('0', '>0')
SYMLINK_TYPENAME = 'MaliciousSymlinkRemoved'
OPERATION_TOKEN = 'extract_firmware'
FAILURE_KIND = 'extractor-failure'
CENSUS_RELPATH = 'tools/round-53/reader-census.json'
BASE_REV = '6697518f0ad8e8399567ae4c9cd0207fc7c04d8b'

NO_READER_FAMILIES = ('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
                      'squashfs_v3_nonstandard')
READER_BACKED_V1V3 = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3', 'squashfs_v3_ddwrt')
KNOWN_HANDLERS = ('squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard',
                  'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v3_broadcom',
                  'squashfs_v3_nonstandard', 'squashfs_v4_le', 'squashfs_v4_be',
                  'squashfs_v4_broadcom')

PREDICATE = (
    'at the declared base the frozen witness command `python -X utf8 -I -B '
    'tools/round-53/v5-baseline-witness.py --root <LANE> --rev '
    '6697518f0ad8e8399567ae4c9cd0207fc7c04d8b --freeze <FREEZE> --envelopes <DIR> '
    '--json-out <OUT2>` exits 1 with `executability_violations 1` naming '
    '`dmg_Z3_v3ddwrt_inode_table` and `clean_residue 7` naming the seven no-reader '
    '`clean` envelopes.')


class WitnessError(Exception):
    """Could not evaluate (exit 2)."""


# --------------------------------------------------------------------------------------
# v5 table parsing (the 13-column grammar, ported unchanged from the v5 instrument)
# --------------------------------------------------------------------------------------

def clean_cell(raw):
    s = raw.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`' and s.count('`') == 2:
        s = s[1:-1].strip()
    return s


def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c for c in s.split('|')]


def _set_cell(cell):
    if cell in ('*', 'none'):
        return ('any', None) if cell == '*' else ('none', None)
    if cell.endswith('+'):
        return ('contains', frozenset(cell[:-1].split(',')))
    return ('exact', frozenset(cell.split('+')))


def _handler_cell(cell):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('none', None)
    parts = [p.strip() for p in cell.split(',')]
    if len(parts) == 1:
        return ('pattern', parts[0])
    return ('list', tuple(parts))


def parse_v5_table(lines, first_line_no):
    if len(lines) < 3:
        raise WitnessError('table at line %d too short' % first_line_no)
    header = [clean_cell(c) for c in split_row(lines[0])]
    if [c.lower() for c in header] != HEADER:
        raise WitnessError('table at line %d: header %r is not the v5 header'
                           % (first_line_no, header))
    rules = []
    for offset, raw_line in enumerate(lines[2:], start=3):
        cells = [clean_cell(c) for c in split_row(raw_line)]
        if len(cells) != len(HEADER):
            raise WitnessError('table row at line %d has %d cells'
                               % (first_line_no + offset - 1, len(cells)))
        (label, operation, provider, handler, failing, gap, dep, be, sr, files,
         action, cause, source) = cells
        rules.append({
            'index': len(rules) + 1, 'label': label,
            'operation': operation, 'provider': provider,
            'handler': _handler_cell(handler), 'failing_handler': _handler_cell(failing),
            'gap_kinds': _set_cell(gap), 'dependencies': _set_cell(dep),
            'be': be, 'symlink_removed': sr, 'files': files, 'action': action,
        })
    return rules


def parse_skill_v5(text):
    lines = text.splitlines()
    marker_index = None
    for i, line in enumerate(lines):
        if MARKER_V5 in line:
            marker_index = i
            break
    if marker_index is None:
        raise WitnessError('marker %r absent at the base revision' % MARKER_V5)
    table_start = None
    for i in range(marker_index + 1, len(lines)):
        if lines[i].lstrip().startswith('|'):
            table_start = i
            break
    if table_start is None:
        raise WitnessError('no markdown table after the v5 marker')
    table = []
    i = table_start
    while i < len(lines) and lines[i].lstrip().startswith('|'):
        table.append(lines[i])
        i += 1
    return parse_v5_table(table, table_start + 1)


# --------------------------------------------------------------------------------------
# v5 features and family-level evaluator (ported; NO census conditioning)
# --------------------------------------------------------------------------------------

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


def features(data):
    op = data.get('operation')
    provider = data.get('provider')
    if isinstance(provider, dict):
        pv = provider.get('id') if isinstance(provider.get('id'), str) else ''
    elif isinstance(provider, str):
        pv = provider
    else:
        pv = ''
    nr = data.get('normalized_result') or {}
    names = []
    for chunk in _as_list(nr.get('chunks')):
        h = chunk.get('handler') if isinstance(chunk, dict) else None
        if isinstance(h, str) and h and h not in names:
            names.append(h)
    failing = []
    for gap in _as_list(nr.get('extraction_gaps')):
        if isinstance(gap, dict) and gap.get('kind') == FAILURE_KIND:
            h = gap.get('handler')
            if isinstance(h, str) and h.startswith('squashfs') and h not in failing:
                failing.append(h)
    squashfs_names = [n for n in names if n.startswith('squashfs')]
    gaps = set()
    deps = set()
    for gap in _as_list(nr.get('extraction_gaps')):
        if isinstance(gap, dict):
            if isinstance(gap.get('kind'), str):
                gaps.add(gap['kind'])
            for d in _as_list(gap.get('dependencies')):
                if isinstance(d, str):
                    deps.add(d)
    commands = []
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            holders = [diag] if isinstance(diag, dict) else []
            if isinstance(diag, dict) and isinstance(diag.get('report'), dict):
                holders.append(diag['report'])
            for holder in holders:
                for key in ('command', 'argv', 'args'):
                    if key in holder:
                        cmd = holder[key]
                        tokens = command_tokens(cmd)
                        if tokens and any(t.rsplit('/', 1)[-1].startswith('sasquatch')
                                          for t in tokens) and cmd not in commands:
                            commands.append(cmd)
    be = 'n/a'
    if commands:
        be = 'no'
        for cmd in commands:
            if '-be' in (command_tokens(cmd) or []):
                be = 'yes'
                break
    sr = 'no'
    for source in (nr.get('diagnostics'), data.get('diagnostics')):
        for diag in _as_list(source):
            holders = [diag] if isinstance(diag, dict) else []
            if isinstance(diag, dict) and isinstance(diag.get('report'), dict):
                holders.append(diag['report'])
            for holder in holders:
                if isinstance(holder, dict) and holder.get('__typename__') == \
                        SYMLINK_TYPENAME:
                    sr = 'yes'
    for found in _iter_dicts(data.get('raw_result')):
        if isinstance(found, dict) and found.get('__typename__') == SYMLINK_TYPENAME:
            sr = 'yes'
    return {'OP': op if isinstance(op, str) else '', 'PV': pv,
            'F': squashfs_names, 'HF': failing or squashfs_names,
            'G': sorted(gaps), 'D': sorted(deps), 'BE': be, 'SR': sr,
            'P': len(_as_list(nr.get('files')))}


def load_envelope(path):
    with open(path, 'r', encoding='utf-8') as handle:
        obj = json.load(handle)
    if not isinstance(obj, dict):
        raise WitnessError('%s: not a JSON object' % path)
    data = obj if isinstance(obj.get('normalized_result'), dict) else obj.get('data')
    if not isinstance(data, dict):
        raise WitnessError('%s: no data object' % path)
    return features(data)


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not values
    if kind == 'contains':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def match_glob(spec, names):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'none':
        return not names
    if kind == 'list':
        return any(fnmatch.fnmatchcase(v, p) for p in payload for v in names)
    return any(fnmatch.fnmatchcase(v, payload) for v in names)


def rule_matches(rule, feat):
    if rule['operation'] != '*' and rule['operation'] != feat['OP']:
        return False
    if rule['provider'] != '*' and rule['provider'] != feat['PV']:
        return False
    if not match_glob(rule['handler'], feat['F']):
        return False
    if not match_glob(rule['failing_handler'], feat['HF']):
        return False
    if not match_set(rule['gap_kinds'], feat['G']):
        return False
    if not match_set(rule['dependencies'], feat['D']):
        return False
    if rule['be'] != '*' and rule['be'] != feat['BE']:
        return False
    if rule['symlink_removed'] != '*' and rule['symlink_removed'] != feat['SR']:
        return False
    if rule['files'] == '0' and feat['P'] != 0:
        return False
    if rule['files'] == '>0' and feat['P'] <= 0:
        return False
    return True


def classify(rules, feat):
    for rule in rules:
        if rule_matches(rule, feat):
            return rule
    return None


def evaluate_v5(feat):
    """The v5 family-level precedence, ported from the R50-C3 instrument."""
    f, g, d = feat['F'], set(feat['G']), set(feat['D'])
    hf, be, p, sr = feat['HF'], feat['BE'], feat['P'], feat['SR'] == 'yes'

    def meets(names, wanted):
        return any(n in wanted for n in names)

    NR = frozenset(NO_READER_FAMILIES)
    RB = frozenset(READER_BACKED_V1V3)
    if feat['OP'] != OPERATION_TOKEN or feat['PV'] != 'unblob':
        return 'unclassified', 'none', 1
    if not f and 'depth-limited' in g:
        return 'container-depth-limited', 'raise-depth', 2
    if not f:
        return 'no-squashfs-chunk', 'inspect-input', 3
    if 'missing-extractor-dependency' in g:
        if 'sasquatch-v4be' in d:
            return 'dep-missing-be', 'install-extractor-be', 4
        if 'sasquatch' in d:
            return 'dep-missing-le', 'install-extractor-le', 4
    if FAILURE_KIND in g and p > 0:
        return 'partial-body-failure', 'salvage-partial', 5
    if FAILURE_KIND in g and p == 0 and be == 'no' and 'squashfs_v4_be' in hf:
        return 'avm-marker-be-dropped', 'wrap-extractor-be', 6
    if FAILURE_KIND in g and p == 0 and meets(hf, RB):
        return 'legacy-body-failure', 'cross-read-legacy', 7
    if FAILURE_KIND in g and p == 0 and meets(hf, NR):
        return 'no-reader-failure', 'preserve-unresolved', 8
    if FAILURE_KIND in g and p == 0:
        return 'body-extractor-failure', 'preserve-failure', 9
    if 'unknown-chunk-handler' in g:
        return 'unknown-residue', 'isolate-residue', 10
    if 'depth-limited' in g:
        return 'depth-limited', 'raise-depth', 11
    if sr and 'unpublished-entry' in g:
        return 'mixed-symlinks', 'audit-symlinks', 12
    if sr and not g:
        return 'escaping-symlink-removed', 'expect-link-absent', 13
    if g == {'unpublished-entry'}:
        return 'in-tree-symlink-metadata', 'count-gap', 14
    if not g:
        if p > 0:
            if meets(f, NR):
                return 'clean-unverified', 'record-unverified', 15
            return 'clean', 'none', 16
        return 'clean-empty', 'confirm-empty', 16
    return 'unclassified', 'none', 17


# --------------------------------------------------------------------------------------
# census (shared format with the v6 instrument) and git access
# --------------------------------------------------------------------------------------

def load_census(root, freeze):
    proc = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (freeze, CENSUS_RELPATH)],
                          capture_output=True, text=True, encoding='utf-8')
    if proc.returncode != 0:
        raise WitnessError('cannot read %s at freeze %r' % (CENSUS_RELPATH, freeze))
    try:
        raw = json.loads(proc.stdout)
    except ValueError as exc:
        raise WitnessError('census does not parse: %s' % exc)
    by_digest = {}
    for row in raw.get('fixtures', []):
        by_digest.setdefault(row.get('sha256_12'), row.get('status'))
    lineage = {}
    for row in raw.get('derived_lineage', []):
        lineage[row.get('carrier_sha256_12')] = row.get('parent_status')
    return by_digest, lineage


def census_status(by_digest, lineage, digest, families):
    if digest:
        short = digest[:12]
        if short in by_digest:
            return by_digest[short]
        if short in lineage:
            return lineage[short]
    for fam in families:
        if fam in NO_READER_FAMILIES:
            return 'no-reader'
        if fam in READER_BACKED_V1V3:
            return 'readable'
    return 'unknown'


def git_show(root, rev, path):
    proc = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                          capture_output=True, text=True, encoding='utf-8')
    if proc.returncode != 0:
        return None
    return proc.stdout


def envelope_subject(path, obj, data):
    sha = (data.get('subject') or {}).get('digest', {}).get('sha256', '')
    if isinstance(sha, str) and re.match(r'^[0-9a-f]{64}$', sha):
        return sha
    return ''


def _self_sha256():
    try:
        with open(os.path.abspath(__file__), 'rb') as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


def envelope_entries(directory):
    out = []
    names = sorted(os.listdir(directory))
    for name in names:
        full = os.path.join(directory, name)
        if os.path.isdir(full):
            for leaf in ('envelope.json', 'rea-full.json', 'after.json'):
                candidate = os.path.join(full, leaf)
                if os.path.isfile(candidate):
                    out.append((name, candidate))
                    break
        elif name.endswith('.json'):
            out.append((os.path.splitext(name)[0], full))
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', required=True)
    parser.add_argument('--rev', default=BASE_REV)
    parser.add_argument('--freeze', required=True)
    parser.add_argument('--envelopes', required=True)
    parser.add_argument('--json-out', required=True)
    ns = parser.parse_args(argv)
    try:
        return witness(ns)
    except WitnessError as exc:
        print('v5-baseline-witness: %s' % exc, file=sys.stderr)
        return 2


def witness(ns):
    root = os.path.abspath(ns.root)
    if ns.rev != BASE_REV:
        raise WitnessError('the witness is frozen to the declared base %r, got %r'
                           % (BASE_REV, ns.rev))
    skill = git_show(root, ns.rev, 'SKILL.md')
    if skill is None:
        raise WitnessError('cannot read SKILL.md at %r' % ns.rev)
    rules = parse_skill_v5(skill)
    by_digest, lineage = load_census(root, ns.freeze)

    entries = envelope_entries(ns.envelopes)
    if not entries:
        raise WitnessError('no envelope found under %r' % ns.envelopes)

    violations = []
    residue = []
    pair_mismatches = []
    labels = {}
    for envelope_id, path in entries:
        with open(path, 'r', encoding='utf-8') as handle:
            obj = json.load(handle)
        data = obj if isinstance(obj.get('normalized_result'), dict) else obj.get('data')
        if not isinstance(data, dict):
            raise WitnessError('%s: no data object' % path)
        feat = features(data)
        sha = envelope_subject(path, obj, data)
        st = census_status(by_digest, lineage, sha, feat['HF'])
        rule = classify(rules, feat)
        label, action = (rule['label'], rule['action']) if rule else ('unclassified',
                                                                      'none')
        labels[envelope_id] = label
        ev = evaluate_v5(feat)
        if (label, action) != (ev[0], ev[1]):
            pair_mismatches.append({'envelope': envelope_id, 'table': (label, action),
                                    'evaluator': (ev[0], ev[1])})
        if action == 'cross-read-legacy' and st == 'no-reader':
            violations.append({'envelope': envelope_id, 'census_status': st,
                               'label': label, 'action': action})
        if label == 'clean' and st == 'no-reader':
            residue.append({'envelope': envelope_id, 'census_status': st})

    report = {
        'instrument': 'v5-baseline-witness.py',
        'instrument_sha256': _self_sha256(),
        'predicate': PREDICATE,
        'schema': 1,
        'root': root,
        'rev': ns.rev,
        'freeze': ns.freeze,
        'n_envelopes': len(entries),
        'pair_mismatches': pair_mismatches,
        'pair_mismatch_count': len(pair_mismatches),
        'executability_violations': violations,
        'executability_violation_count': len(violations),
        'clean_residue': residue,
        'clean_residue_count': len(residue),
        'table_labels': labels,
        'verdict': 'before-arm-red' if (violations or residue) else 'before-arm-clean',
    }
    with open(ns.json_out, 'w', encoding='utf-8') as handle:
        json.dump(report, handle, indent=1, sort_keys=True)
        handle.write('\n')
    with open(ns.json_out, 'r', encoding='utf-8') as handle:
        verify = json.load(handle)
    for key in ('predicate', 'executability_violations', 'clean_residue',
                'table_labels', 'n_envelopes', 'verdict', 'rev'):
        if key not in verify:
            raise WitnessError('receipt %r missing key %r' % (ns.json_out, key))
    print('witness at %s: envelopes %d   pair_mismatches %d   '
          'executability_violations %d   clean_residue %d'
          % (ns.rev, len(entries), len(pair_mismatches), len(violations),
             len(residue)))
    for row in violations:
        print('  EXECUTABILITY-VIOLATION %s: %s/%s on a no-reader fixture'
              % (row['envelope'], row['label'], row['action']))
    for row in residue:
        print('  CLEAN-RESIDUE %s' % row['envelope'])
    print('json: %s' % ns.json_out)
    return 1 if (violations or residue) else 0


if __name__ == '__main__':
    sys.exit(main())
