#!/usr/bin/env python3
"""Task 2 for seat MutPlan (corrected): v4 TABLE mutants, scoped to the v4 table.

Every mutant edits ONLY the v4 table block of a scratch copy of SKILL.md (the
earlier v1/v2/v3 tables in the same craft section are left alone), and the
UNMODIFIED v4 evaluator (copied to scratch) is run over the 126 committed
round-42 recon envelopes.  The label diff vs the baseline is reported.

Also: structural reachability of handler-cell globs under the v4 cell grammar
`^[A-Za-z0-9_?*.\\-\\[\\]]+$` (no negation, no alternation).
"""
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SKILL = os.path.join(LANE, 'SKILL.md')
EVAL = os.path.join(LANE, 'tools/round-42/sqfs-triage-v4.py')
ENV = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
OUT = os.path.join(S, 'table-mut')

HANDLERS = (
    'squashfs_v1', 'squashfs_v2', 'squashfs_v2_nonstandard', 'squashfs_v3',
    'squashfs_v3_ddwrt', 'squashfs_v3_broadcom', 'squashfs_v3_nonstandard',
    'squashfs_v4_le', 'squashfs_v4_be', 'squashfs_v4_broadcom',
)
NO_READER = ('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
             'squashfs_v3_nonstandard')
READER_LEGACY = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3', 'squashfs_v3_ddwrt')
CELL_RE = __import__('re').compile(r'^[A-Za-z0-9_?*.\-\[\]]+$')


def sha256_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


def v4_block(lines):
    """(first_row_index, last_row_index) of the v4 table data rows."""
    start = None
    for i, l in enumerate(lines):
        if '<!-- sqfs-triage-table v4 -->' in l:
            start = i
            break
    if start is None:
        raise SystemExit('no v4 marker')
    # the vocabulary line, then the header, then the separator, then data rows
    i = start + 1
    while not lines[i].lstrip().startswith('|'):
        i += 1
    header = i
    while i < len(lines) and lines[i].lstrip().startswith('|'):
        i += 1
    return header, i          # data rows are lines[header+2:i]


def row_cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def find_v4_row(lines, label):
    h, e = v4_block(lines)
    for i in range(h + 2, e):
        if row_cells(lines[i])[0] == label:
            return i
    raise SystemExit('v4 row %r not found' % label)


def set_cell(lines, i, col, value):
    cells = row_cells(lines[i])
    cells[col] = value
    lines[i] = '| ' + ' | '.join(cells) + ' |'


def make_row(label, handler, failing, gaps, files, action, cause, source):
    cells = [label, '`extract_firmware`', '`unblob`', handler, failing, gaps,
             '*', '*', '*', files, action, cause, source]
    return '| ' + ' | '.join(cells) + ' |'


NO_READER_GLOB = 'squashfs_v[23]_[bn]*'


def mutant(base_lines, name):
    lines = list(base_lines)
    desc = ''
    if name == 'A_legacy_narrow_bare_v123':
        i = find_v4_row(lines, 'legacy-body-failure')
        set_cell(lines, i, 4, 'squashfs_v[123]')
        desc = ("F1 narrowed the legacy-body-failure failing handler to the bare "
                "v1-v3 names: squashfs_v3_ddwrt (reader-backed) no longer matches")
    elif name == 'B_legacy_narrow_v123_star':
        i = find_v4_row(lines, 'legacy-body-failure')
        set_cell(lines, i, 4, 'squashfs_v[123]*')
        desc = 'control: legacy failing handler kept wide (the shipped glob)'
    elif name == 'B2_legacy_narrow_v12_star':
        i = find_v4_row(lines, 'legacy-body-failure')
        set_cell(lines, i, 4, 'squashfs_v[12]*')
        desc = ('legacy failing handler narrowed to v1/v2 only: drops every v3 '
                'family, reader-backed and no-reader alike')
    elif name == 'C_clean_handler_narrowed':
        i = find_v4_row(lines, 'clean')
        set_cell(lines, i, 3, 'squashfs_v[1345]*')
        desc = ("F2 attempted on the clean row alone: the handler glob is "
                "narrowed, which drops the reader-backed squashfs_v2 family too")
    elif name == 'D_v5_shaped_minimal':
        clean_i = find_v4_row(lines, 'clean')
        legacy_i = find_v4_row(lines, 'legacy-body-failure')
        rows = [
            make_row('clean-unverified', NO_READER_GLOB, '*', 'none', '>0',
                     'record-unverified',
                     'the handler family has no independent reader, so a gapless '
                     'run is unverified -> record the run as unverified and never '
                     'call it clean',
                     'round-50 attempt-2 C3; r49 entry "What stays Frontier"'),
            make_row('no-reader-failure', 'squashfs_*', NO_READER_GLOB,
                     'extractor-failure+', '0', 'preserve-unresolved',
                     'the handler family has no independent reader, so the failure '
                     'cannot be attributed -> preserve the failure unresolved, '
                     'never call the body damaged and never call the extractor '
                     'broken',
                     'round-50 attempt-2 C3; r49 entry "What stays Frontier"'),
        ]
        lines.insert(legacy_i, rows[1])       # no-reader-failure above legacy
        # the clean row moved down by one; re-locate it by label
        clean_j = find_v4_row(lines, 'clean')
        lines.insert(clean_j, rows[0])         # clean-unverified above clean
        for j, l in enumerate(lines):
            if '<!-- sqfs-triage-actions:' in l and j > find_marker(lines):
                lines[j] = l.replace('-->',
                                      ' record-unverified preserve-unresolved -->')
                break
        desc = ('minimal v5-shaped table mutant inside the v4 grammar: two new '
                'rows above the v4 rows, the no-reader families selected by the '
                'glob %s, the two new action tokens added to the vocabulary line'
                % NO_READER_GLOB)
    elif name == 'E_v5_shaped_plus_F1_narrow':
        lines, _d = mutant(base_lines, 'D_v5_shaped_minimal')
        i = find_v4_row(lines, 'legacy-body-failure')
        set_cell(lines, i, 4, 'squashfs_v[123]')
        desc = ('D plus the F1 narrowing (legacy failing handler = '
                'squashfs_v[123]): shows the reader-backed v3_ddwrt cross-flip '
                'the narrowing costs')
    elif name == 'F_clean_row_renamed':
        i = find_v4_row(lines, 'clean')
        set_cell(lines, i, 0, 'clean-unverified')
        desc = ('single-cell mutation: the clean row is renamed, so every clean '
                'envelope in every family changes label (a cross-flip)')
    else:
        raise SystemExit('unknown mutant %r' % name)
    return lines, desc


def find_marker(lines):
    for i, l in enumerate(lines):
        if '<!-- sqfs-triage-table v4 -->' in l:
            return i
    raise SystemExit('no marker')


def run_evaluator(skill_path, tag):
    env = dict(os.environ)
    env['TMPDIR'] = os.path.join(OUT, 'tmp')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    envs = sorted(os.path.join(ENV, d, 'envelope.json')
                  for d in os.listdir(ENV)
                  if os.path.isdir(os.path.join(ENV, d)))
    cmd = [sys.executable, '-I', '-B', os.path.join(OUT, 'sqfs-triage-v4.py'),
           '--skill', skill_path, '--json'] + envs
    t0 = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
    rec = {'tag': tag, 'utc': t0,
           'command': ('python3 -I -B <scratch>/sqfs-triage-v4.py --skill %s --json '
                       '<%d envelopes>' % (skill_path, len(envs))),
           'exit_code': p.returncode,
           'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
           'stderr_sha256': hashlib.sha256(p.stderr.encode()).hexdigest(),
           'stderr_tail': p.stderr[-300:]}
    labels = {}
    if p.returncode == 0:
        doc = json.loads(p.stdout)
        for r in doc['results']:
            name = r['path'].split('/envelopes/')[-1].split('/')[0]
            labels[name] = [r['label'], r['action']]
    rec['labels'] = labels
    return rec


def summarise(label_diff):
    fams = {}
    for k, v in label_diff.items():
        key = '%s|%s -> %s' % (v['baseline'][0], v['baseline'][1], v['mutant'][0])
        fams.setdefault(key, []).append(k)
    return {k: sorted(v) for k, v in sorted(fams.items())}


def main():
    os.makedirs(OUT, exist_ok=True)
    shutil.copy2(EVAL, os.path.join(OUT, 'sqfs-triage-v4.py'))
    base_text = open(SKILL, encoding='utf-8').read()
    base_lines = base_text.splitlines()

    report = {'part_a': {}, 'part_b': []}
    report['part_a']['no_reader_glob_used'] = NO_READER_GLOB
    report['part_a']['no_reader_glob_matches'] = sorted(
        n for n in HANDLERS if fnmatch.fnmatchcase(n, NO_READER_GLOB))
    report['part_a']['no_reader_glob_excludes'] = sorted(
        n for n in HANDLERS if not fnmatch.fnmatchcase(n, NO_READER_GLOB))
    report['part_a']['bare_v123_matches'] = sorted(
        n for n in HANDLERS if fnmatch.fnmatchcase(n, 'squashfs_v[123]'))
    report['part_a']['bare_v123_matches_ddwrt'] = fnmatch.fnmatchcase(
        'squashfs_v3_ddwrt', 'squashfs_v[123]')
    report['part_a']['negation_available_in_cell_grammar'] = bool(
        CELL_RE.match('squashfs_v[23]_[!bn]*'))
    report['part_a']['note'] = (
        'the v4 cell grammar is ^[A-Za-z0-9_?*.\\-\\[\\]]+$: no ! or ^, so a '
        'negated class cannot exclude a family; a glob that matches the bare '
        'squashfs_v3 must also match squashfs_v3_ddwrt, and a glob that matches '
        'squashfs_v1 must also match every name starting squashfs_v1')

    base_skill = os.path.join(OUT, 'SKILL-baseline.md')
    with open(base_skill, 'w', encoding='utf-8') as fh:
        fh.write(base_text)
    b = run_evaluator(base_skill, 'baseline')
    report['part_b'].append(b)

    names = ['A_legacy_narrow_bare_v123', 'B_legacy_narrow_v123_star',
             'B2_legacy_narrow_v12_star', 'C_clean_handler_narrowed',
             'D_v5_shaped_minimal', 'E_v5_shaped_plus_F1_narrow',
             'F_clean_row_renamed']
    for name in names:
        lines, desc = mutant(base_lines, name)
        text = '\n'.join(lines) + '\n'
        p = os.path.join(OUT, 'SKILL-%s.md' % name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        rec = run_evaluator(p, name)
        rec['description'] = desc
        rec['skill_sha256'] = sha256_text(text)
        diff = {}
        for k, v in rec.get('labels', {}).items():
            bv = b.get('labels', {}).get(k)
            if bv != v:
                diff[k] = {'baseline': bv, 'mutant': v}
        rec['label_diff_count'] = len(diff)
        rec['label_diff_summary'] = summarise(diff)
        rec['label_diff'] = diff
        rec['v2ns_ddefault_labels'] = {k: v for k, v in rec.get('labels', {}).items()
                                       if 'v2_nonstandard' in k and k.endswith('_ddefault')}
        report['part_b'].append(rec)
        print('%-32s exit=%s diff=%d' % (name, rec['exit_code'],
                                         rec['label_diff_count']), flush=True)
    with open(os.path.join(S, 'table-mut-report.json'), 'w', encoding='utf-8') as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
    print(json.dumps(report['part_a'], indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
