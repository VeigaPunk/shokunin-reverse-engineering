#!/usr/bin/env python3
"""ref-eval-v4draft.py - reference implementation of the round-42 DRAFT (A1)
SquashFS label precedence over feature tuples, plus first-match-table emulators.

Source of truth: plans/round-42-claims.md `## R42-C2`, amendment A1 (2026-10-26
~22:20Z), steps 1-15, and the L1 grammar decision of 2026-10-26 (13th column
`failing handler` globbed against HF; `handler` cell globs over F; `dependencies`
cell gains the contains form `name+`).

This tool NEVER reads SKILL.md, the v3/v4 interpreters or the generators; it is
the same kind of independent evaluator the round-42 seats build, kept here as
the grammar seat's reference so both selftests can diff against it.

Feature tuple (one REA envelope, A1 wording):
  OP  operation string                     PR  provider.id
  H   handler names, chunks[] union gaps[] (nulls dropped)
  HF  handlers carried by extractor-failure gaps (nulls dropped;
      if none carries a handler, HF = F)   -- A1 pins the fallback to F
  G   set of extraction_gaps[].kind        D   union of gaps' dependencies
  BE  yes|no|n/a (recorded -be token)      SR  yes|no (MaliciousSymlinkRemoved)
  P   published file count (absent -> 0)
Derived: F = {h in H : h.startswith('squashfs_')};
          L = {h in F : h matches squashfs_v1*|squashfs_v2*|squashfs_v3*}
          (unblob 26.6.4 names: squashfs_v1, squashfs_v2, squashfs_v2_nonstandard,
           squashfs_v3, squashfs_v3_ddwrt, squashfs_v3_broadcom,
           squashfs_v3_nonstandard; v4: squashfs_v4_le, squashfs_v4_be,
           squashfs_v4_broadcom -- handlers/filesystem/squashfs.py:102-568).

Subcommands:
  --vectors FILE            validate a vectors JSON against classify() (exit 0/1)
  --glob FILE --vectors F   run vectors through a table emulator; print per-vector
                            agreement and write a JSON divergence list to --out
  --sweep --out FILE        order matrix (which steps need order) + full-space
                            divergence census: A1 two-column table vs the
                            one-column variant vs classify()
  --controls --vectors F    score the draft's control-table variants on the vectors
  --frozen-check IDS        build envelopes (build-envelope.py) for the ids and run
                            the FROZEN tools/round-41/sqfs-triage-v3.py with the
                            one-column table under a v3 marker; compares frozen
                            output to the one-column emulator (fidelity proof)
  --selftest                hard-wired sanity asserts
"""

import argparse
import fnmatch
import itertools
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
FROZEN_V3 = LANE + '/tools/round-41/sqfs-triage-v3.py'

SQUASHFS_PREFIX = 'squashfs_'
AVM_HANDLER = 'squashfs_v4_be'
LEGACY_RE = re.compile(r'^squashfs_v[123](_|$)')
DEP_BE = 'sasquatch-v4be'
DEP_LE = 'sasquatch'

# (label, action) per step; step 4 arm B and step 14 arm B handled inline.
STEP_PAIRS = {
    1: ('unclassified', 'none'),
    2: ('container-depth-limited', 'raise-depth'),
    3: ('no-squashfs-chunk', 'inspect-input'),
    4: ('dep-missing-be', 'install-extractor-be'),
    5: ('partial-body-failure', 'salvage-partial'),
    6: ('avm-marker-be-dropped', 'wrap-extractor-be'),
    7: ('legacy-body-failure', 'cross-read-legacy'),
    8: ('body-extractor-failure', 'preserve-failure'),
    9: ('unknown-residue', 'isolate-residue'),
    10: ('depth-limited', 'raise-depth'),
    11: ('mixed-symlinks', 'audit-symlinks'),
    12: ('escaping-symlink-removed', 'expect-link-absent'),
    13: ('in-tree-symlink-metadata', 'count-gap'),
    14: ('clean', 'none'),
    15: ('unclassified', 'none'),
}


def derived(feat):
    h = set(feat.get('H') or [])
    f_set = {x for x in h if x.startswith(SQUASHFS_PREFIX)}
    l_set = {x for x in f_set if LEGACY_RE.match(x)}
    hf_named = {x for x in (feat.get('HF') or []) if x}
    hf = hf_named if hf_named else set(f_set)
    return f_set, l_set, hf


def classify(feat):
    """Return (label, action, step) per the A1 precedence, first match wins."""
    op = feat.get('OP')
    pr = feat.get('PR')
    g = set(feat.get('G') or [])
    d = set(feat.get('D') or [])
    be = feat.get('BE')
    sr = (feat.get('SR') == 'yes') or (feat.get('SR') is True)
    p = feat.get('P') or 0
    f_set, l_set, hf = derived(feat)

    if op != 'extract_firmware' or pr != 'unblob':
        return (*STEP_PAIRS[1], 1)
    if not f_set and 'depth-limited' in g:
        return (*STEP_PAIRS[2], 2)
    if not f_set:
        return (*STEP_PAIRS[3], 3)
    if 'missing-extractor-dependency' in g:
        if DEP_BE in d:
            return (*STEP_PAIRS[4], 4)
        if DEP_LE in d:
            return ('dep-missing-le', 'install-extractor-le', 4)
    if 'extractor-failure' in g and p > 0:
        return (*STEP_PAIRS[5], 5)
    if 'extractor-failure' in g and p == 0:
        if be == 'no' and AVM_HANDLER in hf:
            return (*STEP_PAIRS[6], 6)
        if hf & l_set:
            return (*STEP_PAIRS[7], 7)
        return (*STEP_PAIRS[8], 8)
    if 'unknown-chunk-handler' in g:
        return (*STEP_PAIRS[9], 9)
    if 'depth-limited' in g:
        return (*STEP_PAIRS[10], 10)
    if sr and 'unpublished-entry' in g:
        return (*STEP_PAIRS[11], 11)
    if sr and not g:
        return (*STEP_PAIRS[12], 12)
    if g == {'unpublished-entry'}:
        return (*STEP_PAIRS[13], 13)
    if not g:
        return (('clean', 'none', 14) if p > 0
                else ('clean-empty', 'confirm-empty', 14))
    return (*STEP_PAIRS[15], 15)


# Raw guards: "step i would fire if reached" (no earlier-step suppression).
def guards(feat):
    op = feat.get('OP')
    pr = feat.get('PR')
    g = set(feat.get('G') or [])
    d = set(feat.get('D') or [])
    be = feat.get('BE')
    sr = (feat.get('SR') == 'yes') or (feat.get('SR') is True)
    p = feat.get('P') or 0
    f_set, l_set, hf = derived(feat)
    domain_ok = op == 'extract_firmware' and pr == 'unblob'
    out = {}
    out[1] = not domain_ok
    out[2] = domain_ok and not f_set and 'depth-limited' in g
    out[3] = domain_ok and not f_set
    out[4] = domain_ok and f_set and 'missing-extractor-dependency' in g and bool(d)
    out[5] = domain_ok and f_set and 'extractor-failure' in g and p > 0
    out[6] = domain_ok and f_set and 'extractor-failure' in g and p == 0 and be == 'no' and AVM_HANDLER in hf
    out[7] = domain_ok and f_set and 'extractor-failure' in g and p == 0 and bool(hf & l_set)
    out[8] = domain_ok and f_set and 'extractor-failure' in g and p == 0
    out[9] = domain_ok and f_set and 'unknown-chunk-handler' in g
    out[10] = domain_ok and f_set and 'depth-limited' in g
    out[11] = domain_ok and f_set and sr and 'unpublished-entry' in g
    out[12] = domain_ok and f_set and sr and not g
    out[13] = domain_ok and f_set and g == {'unpublished-entry'}
    out[14] = domain_ok and f_set and not g
    out[15] = domain_ok and f_set and bool(g - {'unpublished-entry'}) and not (
        'unknown-chunk-handler' in g or 'depth-limited' in g or sr)
    return out


# --------------------------------------------------------------------------------------
# table emulators
# --------------------------------------------------------------------------------------

HEADER13 = ['label', 'operation', 'provider', 'handler', 'failing handler',
            'gap kinds', 'dependencies', '-be in child argv', 'symlink removed',
            'published files', 'action', 'cause', 'source']
HEADER12 = [c for c in HEADER13 if c != 'failing handler']


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
    return s.split('|')


def parse_set_cell(cell, contains_allowed):
    if cell == '*':
        return ('any', None)
    if cell == 'none':
        return ('exact', frozenset())
    if cell.endswith('+'):
        if not contains_allowed:
            raise ValueError('contains form not allowed in this table: %r' % cell)
        return ('contains', frozenset(cell[:-1].split(',')))
    return ('exact', frozenset(cell.split(',')))


def parse_table(path):
    """Parse one markdown triage table (12- or 13-column) into emulator rows."""
    with open(path, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()
    header = None
    rows = []
    for line in lines:
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [clean_cell(c) for c in split_row(s)]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set(':-') for c in cells):
            continue
        rows.append(cells)
    if header is None:
        raise ValueError('%s: no table found' % path)
    if header == [h.lower() for h in HEADER13]:
        cols = HEADER13
    elif header == [h.lower() for h in HEADER12]:
        cols = HEADER12
    else:
        raise ValueError('%s: unexpected header %r' % (path, header))
    out = []
    for cells in rows:
        if len(cells) != len(cols):
            raise ValueError('%s: row has %d cells, expected %d: %r'
                             % (path, len(cells), len(cols), cells))
        row = dict(zip(cols, cells))
        gap_kind, gap_payload = parse_set_cell(row['gap kinds'], True)
        dep_kind, dep_payload = parse_set_cell(row['dependencies'], True)
        out.append({
            'label': row['label'],
            'operation': row['operation'],
            'provider': row['provider'],
            'handler': row['handler'],
            'failing': row.get('failing handler', '*'),
            'gaps': (gap_kind, gap_payload),
            'deps': (dep_kind, dep_payload),
            'be': row['-be in child argv'],
            'sr': row['symlink removed'],
            'files': row['published files'],
            'action': row['action'],
        })
    return out


def match_cell_enum(cell, value):
    return cell == '*' or cell == value


def match_files(cell, p):
    if cell == '*':
        return True
    if cell == '0':
        return p == 0
    if cell == '>0':
        return p > 0
    raise ValueError('bad files cell %r' % cell)


def match_set(spec, values):
    kind, payload = spec
    if kind == 'any':
        return True
    if kind == 'contains':
        return payload <= frozenset(values)
    return frozenset(values) == payload


def match_handler_cell(cell, f_set):
    """`handler` cell globs over F; `none` = F empty (L1 grammar decision)."""
    if cell == '*':
        return True
    if cell == 'none':
        return not f_set
    return any(fnmatch.fnmatchcase(x, cell) for x in f_set)


def match_failing_cell(cell, hf):
    """`failing handler` cell globs over HF; `*` matches anything incl. empty."""
    if cell == '*':
        return True
    if cell == 'none':
        return not hf
    return any(fnmatch.fnmatchcase(x, cell) for x in hf)


def table_classify(rows, feat):
    op = feat.get('OP')
    pr = feat.get('PR')
    g = set(feat.get('G') or [])
    d = set(feat.get('D') or [])
    be = feat.get('BE')
    sr = feat.get('SR')
    p = feat.get('P') or 0
    f_set, _l, hf = derived(feat)
    for row in rows:
        if row['operation'] != '*' and row['operation'] != op:
            continue
        if row['provider'] != '*' and row['provider'] != pr:
            continue
        if not match_handler_cell(row['handler'], f_set):
            continue
        if not match_failing_cell(row['failing'], hf):
            continue
        if not match_set(row['gaps'], g):
            continue
        if not match_set(row['deps'], d):
            continue
        if not match_cell_enum(row['be'], be):
            continue
        if not match_cell_enum(row['sr'], sr):
            continue
        if not match_files(row['files'], p):
            continue
        return row['label'], row['action']
    return 'unclassified', 'none'


# --------------------------------------------------------------------------------------
# sweep space
# --------------------------------------------------------------------------------------

H_NAMES = ['squashfs_v3', 'squashfs_v4_be', 'squashfs_v4_le',
           'squashfs_v4_broadcom', 'trx_v1', 'cpio']
G_NAMES = ['missing-extractor-dependency', 'extractor-failure', 'depth-limited',
           'unpublished-entry', 'encrypted-chunk', 'unknown-chunk-handler']
D_NAMES = ['sasquatch-v4be', 'sasquatch', 'unsquashfs']


def _submasks(mask):
    for sub in range(1 << len(H_NAMES)):
        if sub & ~mask == 0:
            yield sub


def sweep_tuples():
    """Yield feature dicts over the bounded space (OP/PR in-domain)."""
    for h_mask in range(1 << len(H_NAMES)):
        h = [H_NAMES[i] for i in range(len(H_NAMES)) if h_mask >> i & 1]
        for hf_mask in _submasks(h_mask):
            hf = [H_NAMES[i] for i in range(len(H_NAMES)) if hf_mask >> i & 1]
            for g_mask in range(1 << len(G_NAMES)):
                g = [G_NAMES[i] for i in range(len(G_NAMES)) if g_mask >> i & 1]
                for d_mask in range(1 << len(D_NAMES)):
                    d = [D_NAMES[i] for i in range(len(D_NAMES)) if d_mask >> i & 1]
                    for be in ('yes', 'no', 'n/a'):
                        for sr in ('no', 'yes'):
                            for p in (0, 7):
                                yield {'OP': 'extract_firmware', 'PR': 'unblob',
                                       'H': h, 'HF': hf, 'G': g, 'D': d,
                                       'BE': be, 'SR': sr, 'P': p}


def order_matrix():
    """Pairwise raw-guard overlap over the sweep space; step 1 analytic."""
    pairs = {}
    witnesses = {}
    for feat in sweep_tuples():
        gs = guards(feat)
        true_steps = [s for s in range(2, 16) if gs[s]]
        for i, j in itertools.combinations(true_steps, 2):
            pairs[(i, j)] = pairs.get((i, j), 0) + 1
            witnesses.setdefault((i, j), feat)
    return pairs, witnesses


# --------------------------------------------------------------------------------------
# vector handling
# --------------------------------------------------------------------------------------

def load_vectors(path):
    with open(path, 'r', encoding='utf-8') as handle:
        doc = json.load(handle)
    return doc


def check_vectors(doc):
    failures = []
    for vec in doc['vectors']:
        got_label, got_action, step = classify(vec['features'])
        want = vec['expected']
        if (got_label, got_action) != (want['label'], want['action']):
            failures.append({'id': vec['id'], 'want': want,
                             'got': [got_label, got_action], 'step': step})
        elif step != vec['decides']:
            failures.append({'id': vec['id'], 'want': want,
                             'got': [got_label, got_action],
                             'step': step, 'declared_step': vec['decides']})
    return failures


# --------------------------------------------------------------------------------------
# control variants (draft control tables, emulated)
# --------------------------------------------------------------------------------------

def control_rows(name, base_rows):
    if name == 'CTL-C2-0b':          # the v3 table under the v4 marker
        return parse_table(os.path.join(HERE, 'glob-table-v3-transcribed.md'))
    if name == 'CTL-C2-8':           # v4 without the legacy-failure row
        return [r for r in base_rows if r['label'] != 'legacy-body-failure']
    if name == 'CTL-C2-9':           # handler cells left at squashfs_v4_*
        out = []
        for r in base_rows:
            r = dict(r)
            if r['handler'] == 'squashfs_*':
                r['handler'] = 'squashfs_v4_*'
            out.append(r)
        return out
    if name == 'CTL-C2-10':          # no container and residue rows
        return [r for r in base_rows
                if r['label'] not in ('container-depth-limited', 'unknown-residue')]
    if name == 'CTL-C2-4':           # exact sets only: contains cells stripped
        out = []
        for r in base_rows:
            r = dict(r)
            kind, payload = r['gaps']
            if kind == 'contains':
                r['gaps'] = ('exact', payload)
            kind, payload = r['deps']
            if kind == 'contains':
                r['deps'] = ('exact', payload)
            out.append(r)
        return out
    raise ValueError('unknown control %r' % name)


CONTROLS = ('CTL-C2-0b', 'CTL-C2-4', 'CTL-C2-8', 'CTL-C2-9', 'CTL-C2-10')


def run_controls(doc, base_rows):
    report = {}
    for name in CONTROLS:
        rows = control_rows(name, base_rows)
        mism = []
        for vec in doc['vectors']:
            got = table_classify(rows, vec['features'])
            want = vec['expected']
            if got != (want['label'], want['action']):
                mism.append(vec['id'])
        report[name] = {'mismatched_vectors': mism,
                        'killed': len(mism), 'of': len(doc['vectors'])}
    return report


# --------------------------------------------------------------------------------------
# frozen-interpreter check
# --------------------------------------------------------------------------------------

def frozen_check(ids, vectors_path, out_path):
    sys.path.insert(0, HERE)
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location('build_envelope',
                                         os.path.join(HERE, 'build-envelope.py'))
    build_envelope = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(build_envelope)
    doc = load_vectors(vectors_path)
    by_id = {v['id']: v for v in doc['vectors']}
    work = os.environ.get('TMPDIR') or '/tmp'
    os.makedirs(work, exist_ok=True)
    onecol = parse_table(os.path.join(HERE, 'glob-table-onecol-v4draft.md'))
    skeleton = os.path.join(work, 'sk-frozen-v3marker.md')
    with open(os.path.join(HERE, 'glob-table-onecol-v4draft.md')) as handle:
        table_text = handle.read()
    # the frozen v3 interpreter only knows the v3 marker; re-marshal the rows
    table_text = table_text.replace('sqfs-triage-table v4', 'sqfs-triage-table v3')
    with open(skeleton, 'w', encoding='utf-8') as handle:
        handle.write('# SKILL\n\n## Queue-drain craft\n\nprose\n\n'
                     + table_text + '\n\n## Later\n\nprose\n')
    lines = []
    for vid in ids:
        vec = by_id[vid]
        env_path = os.path.join(work, 'env-%s.json' % vid)
        with open(env_path, 'w', encoding='utf-8') as handle:
            json.dump(build_envelope.envelope_from_vector(vec), handle, indent=1)
        res = subprocess.run(
            [sys.executable, '-I', '-B', FROZEN_V3, '--skill', skeleton, env_path],
            capture_output=True, text=True)
        if res.returncode != 0:
            lines.append('%s FROZEN-ERROR exit=%d stderr=%s'
                         % (vid, res.returncode, res.stderr.strip()[:200]))
            continue
        got = None
        for line in res.stdout.splitlines():
            if line.count('\t') == 2:
                got = '\t'.join(line.split('\t')[1:])
        emul = table_classify(onecol, vec['features'])
        want = vec['expected']
        ok_emul = (got == '%s\t%s' % emul) if got else False
        ok_ref = (emul == (want['label'], want['action']))
        lines.append('%s frozen=%s emulator=%s reference=%s emulator_fidelity=%s ref_agrees=%s'
                     % (vid, got, '%s %s' % emul,
                        '%s %s' % (want['label'], want['action']), ok_emul, ok_ref))
    with open(out_path, 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(lines) + '\n')
    return lines


# --------------------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------------------

def _f(**kw):
    base = {'OP': 'extract_firmware', 'PR': 'unblob', 'H': [], 'HF': [],
            'G': [], 'D': [], 'BE': 'n/a', 'SR': 'no', 'P': 0}
    base.update(kw)
    return base


def selftest():
    checks = [
        # step 1 domain guard first
        (_f(OP='extract_image', H=['squashfs_v4_be'], P=1), ('unclassified', 'none', 1)),
        # step 2 container: F empty + depth
        (_f(H=['trx_v1'], G=['depth-limited']), ('container-depth-limited', 'raise-depth', 2)),
        # step 3 no-squashfs wins over dep when F empty
        (_f(H=['cpio'], G=['missing-extractor-dependency'], D=['sasquatch']),
         ('no-squashfs-chunk', 'inspect-input', 3)),
        # step 4 membership, be arm first
        (_f(H=['squashfs_v4_be'], G=['missing-extractor-dependency'],
            D=['sasquatch', 'sasquatch-v4be']), ('dep-missing-be', 'install-extractor-be', 4)),
        (_f(H=['squashfs_v3'], G=['missing-extractor-dependency'], D=['sasquatch']),
         ('dep-missing-le', 'install-extractor-le', 4)),
        # step 5 partial beats handler rows
        (_f(H=['squashfs_v3'], HF=['squashfs_v3'], G=['extractor-failure'],
            BE='no', P=3), ('partial-body-failure', 'salvage-partial', 5)),
        # step 6 avm: membership on HF
        (_f(H=['squashfs_v4_be'], HF=['squashfs_v4_be'], G=['extractor-failure'], BE='no'),
         ('avm-marker-be-dropped', 'wrap-extractor-be', 6)),
        # step 7 legacy, no BE condition
        (_f(H=['squashfs_v3'], HF=['squashfs_v3'], G=['extractor-failure'], BE='yes'),
         ('legacy-body-failure', 'cross-read-legacy', 7)),
        # step 8 body residual
        (_f(H=['squashfs_v4_le'], HF=['squashfs_v4_le'], G=['extractor-failure'], BE='no'),
         ('body-extractor-failure', 'preserve-failure', 8)),
        # step 9 residue before depth
        (_f(H=['squashfs_v4_le'], G=['unknown-chunk-handler', 'depth-limited'], P=2),
         ('unknown-residue', 'isolate-residue', 9)),
        # step 10 depth
        (_f(H=['squashfs_v4_le'], G=['depth-limited'], P=6), ('depth-limited', 'raise-depth', 10)),
        # step 11 mixed
        (_f(H=['squashfs_v4_le'], G=['unpublished-entry'], SR='yes', P=4),
         ('mixed-symlinks', 'audit-symlinks', 11)),
        # step 12 escaping
        (_f(H=['squashfs_v4_be'], SR='yes', P=2),
         ('escaping-symlink-removed', 'expect-link-absent', 12)),
        # step 13 in-tree exact singleton
        (_f(H=['squashfs_v4_le'], G=['unpublished-entry'], P=1),
         ('in-tree-symlink-metadata', 'count-gap', 13)),
        # step 14 clean / clean-empty
        (_f(H=['squashfs_v3'], P=5), ('clean', 'none', 14)),
        (_f(H=['squashfs_v1'], P=0), ('clean-empty', 'confirm-empty', 14)),
        # step 15
        (_f(H=['squashfs_v4_le'], G=['unpublished-entry', 'encrypted-chunk'], P=2),
         ('unclassified', 'none', 15)),
        # HF fallback = F (A1): no failing gap handler recorded
        (_f(H=['squashfs_v3', 'squashfs_v4_be'], G=['extractor-failure'], BE='no'),
         ('avm-marker-be-dropped', 'wrap-extractor-be', 6)),
        # mixed chunk sets: failing handler decides, not H
        (_f(H=['squashfs_v3', 'squashfs_v4_be'], HF=['squashfs_v3'], G=['extractor-failure'], BE='no'),
         ('legacy-body-failure', 'cross-read-legacy', 7)),
        (_f(H=['squashfs_v4_le', 'squashfs_v4_be'], HF=['squashfs_v4_le'], G=['extractor-failure'], BE='no'),
         ('body-extractor-failure', 'preserve-failure', 8)),
    ]
    bad = []
    for feat, want in checks:
        got = classify(feat)
        if got != want:
            bad.append((feat, want, got))
    if bad:
        for feat, want, got in bad:
            print('FAIL %r want=%s got=%s' % (feat, want, got), file=sys.stderr)
        return 1
    print('selftest ok: %d checks' % len(checks))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--vectors')
    parser.add_argument('--glob')
    parser.add_argument('--out')
    parser.add_argument('--sweep', action='store_true')
    parser.add_argument('--controls', action='store_true')
    parser.add_argument('--frozen-check')
    parser.add_argument('--selftest', action='store_true')
    ns = parser.parse_args(argv)

    if ns.selftest:
        return selftest()
    if ns.vectors and not ns.glob and not ns.controls and not ns.frozen_check:
        doc = load_vectors(ns.vectors)
        failures = check_vectors(doc)
        print('vectors: %d checked, %d failures' % (len(doc['vectors']), len(failures)))
        for f in failures:
            print(json.dumps(f, sort_keys=True))
        return 1 if failures else 0
    if ns.glob and ns.vectors:
        doc = load_vectors(ns.vectors)
        rows = parse_table(ns.glob)
        results = []
        for vec in doc['vectors']:
            got = table_classify(rows, vec['features'])
            want = vec['expected']
            results.append({'id': vec['id'],
                            'agrees': got == (want['label'], want['action']),
                            'table_pair': list(got),
                            'expected': [want['label'], want['action']],
                            'decides': vec['decides']})
        div = [r for r in results if not r['agrees']]
        print('table %s: %d vectors, %d divergences' % (ns.glob, len(results), len(div)))
        for r in div:
            print('DIVERGE %s table=%s expected=%s (step %d)' %
                  (r['id'], r['table_pair'], r['expected'], r['decides']))
        if ns.out:
            with open(ns.out, 'w', encoding='utf-8') as handle:
                json.dump({'table': ns.glob, 'results': results}, handle, indent=1)
        return 0
    if ns.sweep:
        pairs, witnesses = order_matrix()
        base_rows = parse_table(os.path.join(HERE, 'glob-table-v4draft.md'))
        onecol_rows = parse_table(os.path.join(HERE, 'glob-table-onecol-v4draft.md'))
        census = {}
        n = 0
        for feat in sweep_tuples():
            n += 1
            ref = classify(feat)[:2]
            two = table_classify(base_rows, feat)
            one = table_classify(onecol_rows, feat)
            if two != ref:
                key = 'twocol|%s|%s' % (ref[0], two[0])
                e = census.setdefault(key, {'count': 0, 'witness': feat})
                e['count'] += 1
            if one != ref:
                key = 'onecol|%s|%s' % (ref[0], one[0])
                e = census.setdefault(key, {'count': 0, 'witness': feat})
                e['count'] += 1
        doc = {'space_size': n,
               'order_pairs': {'%d<%d' % k: {'overlapping_tuples': v,
                                             'witness': witnesses[k]}
                               for k, v in sorted(pairs.items())},
               'divergence_census': census}
        out = ns.out or os.path.join(os.environ.get('TMPDIR') or '.', 'sweep.json')
        with open(out, 'w', encoding='utf-8') as handle:
            json.dump(doc, handle, indent=1, sort_keys=True, default=str)
        print('sweep: %d tuples; order pairs %d; divergence classes %d -> %s'
              % (n, len(pairs), len(census), out))
        twocol = [k for k in census if k.startswith('twocol')]
        onecol = [k for k in census if k.startswith('onecol')]
        print('two-column divergences: %d classes' % len(twocol))
        for k in twocol:
            print('  %s count=%d' % (k, census[k]['count']))
        print('one-column divergences: %d classes' % len(onecol))
        for k in sorted(onecol):
            print('  %s count=%d' % (k, census[k]['count']))
        return 0
    if ns.controls and ns.vectors:
        doc = load_vectors(ns.vectors)
        base_rows = parse_table(os.path.join(HERE, 'glob-table-v4draft.md'))
        report = run_controls(doc, base_rows)
        out = ns.out or os.path.join(os.environ.get('TMPDIR') or '.', 'controls.json')
        with open(out, 'w', encoding='utf-8') as handle:
            json.dump(report, handle, indent=1, sort_keys=True)
        for name in sorted(report):
            print('%s killed %d/%d vectors: %s'
                  % (name, report[name]['killed'], report[name]['of'],
                     ' '.join(report[name]['mismatched_vectors'])))
        return 0
    if ns.frozen_check:
        ids = ns.frozen_check.split(',')
        lines = frozen_check(ids, ns.vectors, ns.out or os.path.join(
            os.environ.get('TMPDIR') or '.', 'frozen-check.tsv'))
        for line in lines:
            print(line)
        return 0
    parser.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
