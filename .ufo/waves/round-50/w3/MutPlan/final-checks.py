#!/usr/bin/env python3
"""Final checks for the table experiment.

C1: control for glob-search.py - can the search find ANY glob selecting the
    no-reader set {v2_nonstandard, v3_broadcom, v3_nonstandard}?  If yes, the
    null result for the reader-backed legacy set is meaningful.

C2: row-order variant - place the no-reader rows ABOVE partial-body-failure
    (so a no-reader run that failed but published files never reaches an
    oracle-backed action) and measure the label on a synthetic no-reader
    partial-failure envelope and on the 126 committed envelopes.
"""
import fnmatch
import json
import os
import shutil
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SKILL = os.path.join(LANE, 'SKILL.md')
ENV = os.path.join(LANE, '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes')
OUT = os.path.join(S, 'table-mut')
EVAL = os.path.join(OUT, 'sqfs-triage-v4.py')
NO_READER_GLOB = 'squashfs_v[23]_[bn]*'


def row_cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def v4_block(lines):
    start = None
    for i, l in enumerate(lines):
        if '<!-- sqfs-triage-table v4 -->' in l:
            start = i
            break
    i = start + 1
    while not lines[i].lstrip().startswith('|'):
        i += 1
    header = i
    while i < len(lines) and lines[i].lstrip().startswith('|'):
        i += 1
    return header, i


def find_v4_row(lines, label):
    h, e = v4_block(lines)
    for i in range(h + 2, e):
        if row_cells(lines[i])[0] == label:
            return i
    raise SystemExit('row not found: %r' % label)


def make_row(label, handler, failing, gaps, files, action, cause, source):
    cells = [label, '`extract_firmware`', '`unblob`', handler, failing, gaps,
             '*', '*', '*', files, action, cause, source]
    return '| ' + ' | '.join(cells) + ' |'


def build_d2(base_lines):
    """D2: the two no-reader rows placed ABOVE partial-body-failure."""
    lines = list(base_lines)
    partial_i = find_v4_row(lines, 'partial-body-failure')
    rows = [
        make_row('no-reader-failure', 'squashfs_*', NO_READER_GLOB,
                 'extractor-failure+', '0', 'preserve-unresolved',
                 'the handler family has no independent reader, so the failure '
                 'cannot be attributed -> preserve the failure unresolved',
                 'round-50 attempt-2 C3'),
        make_row('no-reader-partial', 'squashfs_*', NO_READER_GLOB,
                 'extractor-failure+', '>0', 'preserve-unresolved',
                 'the handler family has no independent reader, so the published '
                 'subset cannot be matched to an oracle -> preserve the failure '
                 'unresolved',
                 'round-50 attempt-2 C3'),
    ]
    lines.insert(partial_i, rows[0])
    lines.insert(partial_i + 1, rows[1])
    clean_j = find_v4_row(lines, 'clean')
    lines.insert(clean_j, make_row(
        'clean-unverified', NO_READER_GLOB, '*', 'none', '>0',
        'record-unverified',
        'the handler family has no independent reader, so a gapless run is '
        'unverified -> record the run as unverified and never call it clean',
        'round-50 attempt-2 C3'))
    # the vocabulary line DIRECTLY above the v4 table (the earlier tables have
    # their own; the v4 evaluator reads the one above the v4 marker)
    m = next(i for i, l in enumerate(lines)
             if '<!-- sqfs-triage-table v4 -->' in l)
    for j in range(m + 1, len(lines)):
        if '<!-- sqfs-triage-actions:' in lines[j]:
            lines[j] = lines[j].replace(
                '-->', ' record-unverified preserve-unresolved -->')
            break
    return '\n'.join(lines) + '\n'


def run(skill_path, envelopes):
    cmd = [sys.executable, '-I', '-B', EVAL, '--skill', skill_path, '--json'] + envelopes
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    rec = {'exit_code': p.returncode,
           'stdout_sha256': __import__('hashlib').sha256(
               p.stdout.encode()).hexdigest(),
           'stderr_tail': p.stderr[-200:]}
    labels = {}
    if p.returncode == 0:
        doc = json.loads(p.stdout)
        for r in doc['results']:
            labels[os.path.basename(r['path'])] = [r['label'], r['action']]
    rec['labels'] = labels
    return rec


def main():
    out = {}
    # C1: control for the glob search
    import importlib.util
    _sp = importlib.util.spec_from_file_location("gs", os.path.join(S, "glob-search.py"))
    gs = importlib.util.module_from_spec(_sp)
    _sp.loader.exec_module(gs)
    def search_for(target):
        orig = gs.TARGET
        gs.TARGET = target
        try:
            return gs.search()
        finally:
            gs.TARGET = orig
    hits, seen = gs.search()
    ctrl_hits, ctrl_seen = search_for(frozenset(gs.NO_READER))
    no_reader_target = frozenset(gs.NO_READER)
    control = [h for h in hits if gs.match_set(h) == no_reader_target]
    # the search's `hits` list only records the TARGET set; rerun the match
    # set over the visited patterns to find one for the no-reader set
    ctrl = None
    for pat in sorted(gs.seen) if hasattr(gs, 'seen') else []:
        pass
    out['c1_glob_search_control'] = {
        'target_hits': sorted(set(hits)),
        'no_reader_glob_works': sorted(gs.match_set(NO_READER_GLOB)),
        'no_reader_glob_is_exact': gs.match_set(NO_READER_GLOB) == no_reader_target,
        'searched_patterns': seen,
        'control_no_reader_set_hits': sorted(set(ctrl_hits)),
        'control_searched_patterns': ctrl_seen,
    }

    # C2: D2 table + synthetic probes
    base_lines = open(SKILL, encoding='utf-8').read().splitlines()
    text = build_d2(base_lines)
    p = os.path.join(OUT, 'SKILL-D2_rows_above_partial.md')
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(text)
    corpus = sorted(os.path.join(ENV, d, 'envelope.json')
                    for d in os.listdir(ENV)
                    if os.path.isdir(os.path.join(ENV, d)))
    syn = os.path.join(S, 'synthetic-envelopes')
    syn_files = sorted(os.path.join(syn, f) for f in os.listdir(syn)
                       if f.endswith('.json'))
    d2 = run(p, corpus)
    d2syn = run(p, syn_files)
    base = run(os.path.join(OUT, 'SKILL-baseline.md'), corpus)
    basesyn = run(os.path.join(OUT, 'SKILL-baseline.md'), syn_files)
    diff = {}
    for k, v in d2.get('labels', {}).items():
        if base.get('labels', {}).get(k) != v:
            diff[k] = {'baseline': base['labels'][k], 'mutant': v}
    out['c2_d2_rows_above_partial'] = {
        'corpus_exit': d2['exit_code'],
        'corpus_diff_count': len(diff),
        'corpus_diff_summary': sorted({('%s->%s' % (v['baseline'][0], v['mutant'][0]))
                                       for v in diff.values()}),
        'synthetic_exit': d2syn['exit_code'],
        'synthetic_baseline': basesyn.get('labels'),
        'synthetic_d2': d2syn.get('labels'),
        'skill_sha256': __import__('hashlib').sha256(text.encode()).hexdigest(),
    }
    with open(os.path.join(S, 'final-checks.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items()
                      if k != 'c1_glob_search_control'}, indent=1, sort_keys=True))
    print('control:', json.dumps({k: v for k, v in
                                  out['c1_glob_search_control'].items()
                                  if k != 'searched_patterns'}, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
