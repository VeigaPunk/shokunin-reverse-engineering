#!/usr/bin/env python3
"""MutC1Bindings probe: does each proposed fixture mutation actually flip the
counter's documentation binding?

The binding code is NOT re-implemented here. The binding block is extracted
verbatim from the counter source under test and exec'd in a namespace built from
that counter module's own globals, so ENTRY/STEM/CORE_HEADING/FRONTIER_MARK/
OPENED_DATES/ENTRY regexes/section()/cells()/sid_tokens() are the shipped bytes.
The receipt clause expressions are extracted with `ast` (exact source segment of
the `d['<key>'] = ...` assignment) and eval'd against the counter's own
all_adds/is_ancestor/squashfs_chunk_handlers.

No REA, no network, no lane writes: a scratch git fixture repo only.
Usage: probe.py <counter.py> <out.json> <scratchdir>
"""
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import types

CTR_PATH = sys.argv[1]
OUT_JSON = sys.argv[2]
SCRATCH = sys.argv[3]

DOC_BINDINGS = ('province_core_section', 'province_core_row', 'frontier_note',
                 'entry_present', 'sourced', 'coverage_map_row')

# the claims' citation set for the round-52 entry
CITE_SET = ('S243', 'S244', 'S245', 'S249', 'S250', 'S251', 'S252')


# ------------------------------------------------------------------ loading

def load_counter(path):
    """Import the counter under test.

    If it does not import as-is (the round-52 draft is missing the module-level
    TARGET/IDS names that measure()'s default arguments evaluate at def time),
    the loader injects the missing names into an IN-MEMORY copy only; the file
    on disk is never written. The injection is recorded in the output.
    """
    src = open(path).read()
    injected = []
    for name, value in (('TARGET', '4'),
                        ('IDS', "('g7581', 'g7582', 'c6490', 'c6430')")):
        if not re.search(r'^%s = ' % name, src, re.M):
            src = re.sub(r"(?m)^(OPENED_DATES = .*)$",
                         lambda m: m.group(1) + "\n%s = %s" % (name, value),
                         src, count=1)
            injected.append(name)
    mod = types.ModuleType('ctr_under_test')
    mod.__file__ = path
    exec(compile(src, path, 'exec'), mod.__dict__)
    mod.__injected__ = injected
    return mod


def extract_binding_block(src):
    """The binding block of measure(), verbatim, dedented to module level."""
    i = src.index('# ---------------------------------------------------------- bindings')
    i = src.rfind('\n', 0, i) + 1
    j = src.index("res['met_target']")
    j = src.rfind('\n', 0, j) + 1
    return textwrap.dedent(src[i:j])


def extract_stmt(src, key):
    """Exact source of `d['<key>'] = <expr>`, via ast source segments."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        tgt = node.targets[0]
        if (isinstance(tgt, ast.Subscript)
                and isinstance(tgt.value, ast.Name) and tgt.value.id == 'd'
                and isinstance(tgt.slice, ast.Constant) and tgt.slice.value == key):
            return ast.get_source_segment(src, node.value)
    raise KeyError(key)


# ------------------------------------------------------------------- git fs

def git(root, *args):
    return subprocess.run(['git', '-C', root, *args], capture_output=True,
                          text=True, check=True)


def write_files(root, files):
    for rel, content in files.items():
        p = os.path.join(root, rel)
        if content is None:
            if os.path.exists(p):
                os.remove(p)
            continue
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as fh:
            fh.write(content)


def new_repo(root):
    os.makedirs(root, exist_ok=True)
    git(root, 'init', '-q')
    git(root, 'config', 'user.name', 'MutC1Bindings probe')
    git(root, 'config', 'user.email', 'probe@example.invalid')


def commit(root, msg):
    git(root, 'add', '-A')
    git(root, 'commit', '-q', '--allow-empty', '-m', msg)
    return git(root, 'rev-parse', 'HEAD').stdout.strip()


# ----------------------------------------------------------------- fixtures

class Fixtures:
    """The pristine round-52 documentation fixture set, built from the counter
    under test's OWN constants (so the same probe runs against v1 and v2)."""

    def __init__(self, mod):
        self.ENTRY = mod.ENTRY
        self.STEM = mod.STEM
        self.CORE_HEADING = mod.CORE_HEADING
        self.FRONTIER_MARK = mod.FRONTIER_MARK
        win = tuple(mod.OPENED_DATES)
        self.WIN_IN = win[0]
        self.WIN_BEFORE = '2026-10-%02d' % (int(win[0][-2:]) - 1)
        self.WIN_AFTER = '2026-10-%02d' % (int(win[-1][-2:]) + 1)
        self.OTHER_STEM = '2026-10-26-r41-avm-be-squashfs-core'
        self.OTHER_ENTRY = ('corpus/knowledge/'
                            '2026-10-26-r41-avm-be-squashfs-core.md')

    # -- PROVINCE.md ---------------------------------------------------
    ROW_FIRST_CELL = ('genuine AVM-marker little-endian SquashFS v4 (`hsqs`, v4.0 xz, '
                      '`mkfs_time == bytes_used`) members of four public FRITZ!OS '
                      'images — handler `squashfs_v4_le`')

    def province(self, heading=None, cell=None, layout='AVM marker', cited=None,
                 note=True, token='LE AVM members (`hsqs`)', mark=None,
                 extra=()):
        heading = self.CORE_HEADING if heading is None else heading
        cell = self.ROW_FIRST_CELL if cell is None else cell
        cited = self.ENTRY if cited is None else cited
        mark = self.FRONTIER_MARK if mark is None else mark
        lines = ['# kaidoku-shokunin — Province', '', '## Core', '', '- nothing yet',
                 '', heading, '',
                 '| Surface | Layout | Status | Entry |',
                 '|---|---|---|---|',
                 '| %s | %s | x | `%s` |' % (cell, layout, cited), '']
        lines.extend(extra)
        lines.extend(['## Frontier', ''])
        if note:
            lines.append(
                '%s, 2026-10-30: %s moved Frontier → Core with `%s`; the earlier '
                'note is superseded. Still Frontier: AVM kernels, nested sub-images '
                'below depth 1.' % (mark, token, self.STEM))
            lines.append('')
        return '\n'.join(lines) + '\n'

    # -- the knowledge entry -------------------------------------------
    def entry(self, source_lines=None, receipts=True):
        if source_lines is None:
            source_lines = ['source: %s - x' % s for s in CITE_SET]
        elif isinstance(source_lines, str):
            source_lines = [source_lines]
        body = '# E\n\n' + '\n'.join(source_lines) + '\n'
        if receipts:
            body += '\nfresh receipts `corpus/evidence/round-52/c1/`\n'
        return body

    # -- corpus/SOURCES.md ---------------------------------------------
    def sources(self, sids=None, opened=None, used=None):
        sids = list(CITE_SET) if sids is None else list(sids)
        opened = self.WIN_IN if opened is None else opened
        used = self.ENTRY if used is None else used
        rows = '\n'.join(
            '| %s | source under test | docs | A | scope | anchor | teaches | mined '
            '| %s | 180d | %s |' % (i, opened, used) for i in sids)
        return ('# S\n\n| id | source | kind | tier | scope | anchor | teaches | status '
                '| opened | recheck | used-by |\n'
                '|---|---|---|---|---|---|---|---|---|---|---|\n' + rows + '\n')

    # -- corpus/README.md ----------------------------------------------
    def readme(self, stem=None, in_map=True, in_knowledge=False):
        stem = self.STEM if stem is None else stem
        map_row = ('| LE AVM (round 52) | `%s` |' % stem if in_map
                   else '| LE AVM (round 52) | none |')
        out = ['# R', '', '## Coverage map', '',
               '| section | entries |', '|---|---|', map_row, '']
        if in_knowledge:
            out.extend(['## Knowledge', '', '| `%s` |' % stem, ''])
        else:
            out.extend(['## Knowledge', '', '- k', ''])
        return '\n'.join(out)

    # -- the whole tree -------------------------------------------------
    def files(self, **over):
        f = {
            'PROVINCE.md': self.province(),
            self.ENTRY: self.entry(),
            'corpus/SOURCES.md': self.sources(),
            'corpus/README.md': self.readme(),
        }
        f.update(over)
        return f


# ------------------------------------------------------- binding evaluator

def make_binding_eval(mod, src):
    body = extract_binding_block(src)
    ns = dict(vars(mod))
    ns['spec_probs'] = []
    ns['plan_probs'] = []
    ns['model'] = {'allowed': {}}

    def run(root, rev):
        ns['res'] = {'carriers': {}, 'frozen_tables_valid': True}
        ns['root'] = root
        ns['rev'] = rev
        exec(compile(body, CTR_PATH + '#bindings', 'exec'), ns)
        return ns['res']['bindings']

    return run


def main():
    mod = load_counter(CTR_PATH)
    src = open(CTR_PATH).read()
    fx = Fixtures(mod)
    eval_bindings = make_binding_eval(mod, src)
    results = []

    def record(cid, kind, target, mutation, before, after, finding, note='',
               expect_flip=True):
        # doc-binding family: KILLED = the mutation flipped the binding (the
        # check is live and load-bearing). NO-OP = the mutation changed nothing
        # (a DEAD check). CASCADE = it flipped, but a different binding than
        # the one named.
        # no-op-risk family: DEAD = the mutation did NOT flip the named
        # obligation, i.e. the shipped bindings do not cover it at all.
        flipped = sorted(k for k in after if before.get(k) != after.get(k))
        if kind == 'no-op-risk':
            verdict = 'DEAD' if target not in flipped else 'COVERED'
        else:
            if target in flipped:
                verdict = 'KILLED'
            elif flipped:
                verdict = 'CASCADE'
            else:
                verdict = 'NO-OP'
        results.append({
            'case': cid, 'kind': kind, 'target': target, 'mutation': mutation,
            'before': {k: before.get(k) for k in before},
            'after': {k: after.get(k) for k in after},
            'flipped': flipped, 'flips_target': target in flipped,
            'expect_flip': expect_flip,
            'expected_finding': finding, 'verdict': verdict, 'note': note,
        })

    # ---------------------------------------------------------- baseline
    root = tempfile.mkdtemp(prefix='mutc1.', dir=SCRATCH)
    new_repo(root)
    write_files(root, fx.files())
    base_rev = commit(root, 'pristine')
    base = eval_bindings(root, base_rev)
    base_ok = all(base.get(b) is True for b in DOC_BINDINGS)
    results.append({'case': 'BASELINE', 'kind': 'baseline', 'target': '-',
                    'mutation': 'pristine documentation fixtures',
                    'before': {}, 'after': base, 'flipped': [], 'flips_target': True,
                    'expect_flip': True, 'expected_finding': '-',
                    'verdict': 'GREEN' if base_ok else 'BASELINE-RED',
                    'note': 'all six doc bindings must be true on the pristine tree'})
    if not base_ok:
        print(json.dumps(base, indent=1))
        raise SystemExit('baseline red: probe inconclusive')

    # ------------------------------------------------- doc binding cases
    doc_cases = [
        ('D01', 'province_core_section', 'heading typo: "addition to Core"',
         lambda: {'PROVINCE.md': fx.province(heading='## Round-52 addition to Core')},
         'b:province_core_section', ''),
        ('D02', 'province_core_section', 'heading carries a suffix',
         lambda: {'PROVINCE.md': fx.province(
             heading=fx.CORE_HEADING + ' (verified 2026-10-30)')},
         'b:province_core_section', 'section() needs an exact whole-line match'),
        ('D03', 'province_core_section', 'heading demoted to ### ',
         lambda: {'PROVINCE.md': fx.province(
             heading='### ' + fx.CORE_HEADING.lstrip('# '))},
         'b:province_core_section', ''),
        ('D04', 'province_core_row', 'first cell names the BE handler',
         lambda: {'PROVINCE.md': fx.province(
             cell=fx.ROW_FIRST_CELL.replace('`squashfs_v4_le`', '`squashfs_v4_be`'))},
         'b:province_core_row', ''),
        ('D05', 'province_core_row', 'handler prefix only (squashfs_v4)',
         lambda: {'PROVINCE.md': fx.province(
             cell=fx.ROW_FIRST_CELL.replace('`squashfs_v4_le`', '`squashfs_v4`'))},
         'b:province_core_row', 'HANDLER_RE is not a prefix test'),
        ('D06', 'province_core_row', 'the LE row is absent',
         lambda: {'PROVINCE.md': re.sub(
             r'^\| genuine AVM-marker.*\n', '', fx.province(), flags=re.M)},
         'b:province_core_row', ''),
        ('D07', 'province_core_row', 'row cites another entry path',
         lambda: {'PROVINCE.md': fx.province(cited=fx.OTHER_ENTRY)},
         'b:province_core_row', ''),
        ('D08', 'province_core_row', 'row moved out of the round-52 section',
         lambda: {'PROVINCE.md': fx.province(heading='## Round-51 additions to Core')},
         'b:province_core_row', 'the row now sits under another heading'),
        ('D09', 'province_core_row', 'the row names no AVM marker anywhere',
         lambda: {'PROVINCE.md': fx.province(
             cell=fx.ROW_FIRST_CELL.replace('AVM-marker', 'little-endian'),
             layout='little-endian squashfs')},
         'b:province_core_row', ''),
        ('D10', 'province_core_row',
         'the layout column drops the marker but the first cell keeps "AVM-marker"',
         lambda: {'PROVINCE.md': fx.province(layout='little-endian squashfs')},
         'b:province_core_row',
         'the marker regex scans the whole row, so the first cell\'s own wording '
         'keeps the row true: the layout column is not independently load-bearing'),
        ('D11', 'frontier_note', 'frontier note absent',
         lambda: {'PROVINCE.md': fx.province(note=False)},
         'b:frontier_note', ''),
        ('D12', 'frontier_note', 'wrong frontier mark (Round-51 frontier note)',
         lambda: {'PROVINCE.md': fx.province(mark='Round-51 frontier note')},
         'b:frontier_note', ''),
        ('D13', 'frontier_note', 'note keeps the stem but drops the LE-AVM token',
         lambda: {'PROVINCE.md': fx.province(token='the members')},
         'b:frontier_note',
         'specificity guard: the stem alone spells avm-le and must not satisfy '
         'the token'),
        ('D14', 'frontier_note', 'note carries the BE token (AVM BE)',
         lambda: {'PROVINCE.md': fx.province(token='AVM BE members')},
         'b:frontier_note', ''),
        ('D15', 'frontier_note', 'note names the wrong stem',
         lambda: {'PROVINCE.md': fx.province().replace(fx.STEM, fx.OTHER_STEM)},
         'b:frontier_note', ''),
        ('D16', 'entry_present', 'entry file renamed (stem moved)',
         lambda: {fx.ENTRY: None,
                  'corpus/knowledge/%s-v2.md' % fx.STEM: fx.entry()},
         'b:entry_present', ''),
        ('D17', 'sourced', 'used-by dropped (points at another entry)',
         lambda: {'corpus/SOURCES.md': fx.sources(used=fx.OTHER_ENTRY)},
         'b:sourced', ''),
        ('D18', 'sourced', 'source row opened BEFORE the window (%s)' % fx.WIN_BEFORE,
         lambda: {'corpus/SOURCES.md': fx.sources(opened=fx.WIN_BEFORE)},
         'b:sourced', ''),
        ('D19', 'sourced', 'source row opened AFTER the window (%s)' % fx.WIN_AFTER,
         lambda: {'corpus/SOURCES.md': fx.sources(opened=fx.WIN_AFTER)},
         'b:sourced', ''),
        ('D20', 'sourced', 'entry cites an S-id with no SOURCES row',
         lambda: {fx.ENTRY: fx.entry(source_lines=['source: S9999 - x'])},
         'b:sourced', ''),
        ('D21', 'sourced', 'S-id substring trap (entry says S11210, row says S1121)',
         lambda: {fx.ENTRY: fx.entry(source_lines=['source: S11210 - x'])},
         'b:sourced', 'SID_RE must not match a longer digit run'),
        ('D22', 'sourced', 'the SOURCES row has the wrong cell count (10)',
         lambda: {'corpus/SOURCES.md': fx.sources().replace(
             '| 180d |', '|')},
         'b:sourced', 'cells() length gate'),
        ('D23', 'coverage_map_row', 'map row removed',
         lambda: {'corpus/README.md': fx.readme(in_map=False)},
         'b:coverage_map_row', ''),
        ('D24', 'coverage_map_row', 'map row names another stem',
         lambda: {'corpus/README.md': fx.readme(stem=fx.OTHER_STEM)},
         'b:coverage_map_row', ''),
        ('D25', 'coverage_map_row',
         'stem appears only under ## Knowledge, not in the map',
         lambda: {'corpus/README.md': fx.readme(in_map=False, in_knowledge=True)},
         'b:coverage_map_row', 'the check is section-scoped'),
    ]

    for cid, target, desc, mut, finding, note in doc_cases:
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(root, exist_ok=True)
        new_repo(root)
        write_files(root, fx.files())
        commit(root, 'pristine')
        files = fx.files()
        files.update(mut())
        write_files(root, files)
        rev = commit(root, cid + ' ' + desc)
        after = eval_bindings(root, rev)
        record(cid, 'doc-binding', target, desc, base, after, finding, note)

    # ------------------------------------------- no-op risk (dead checks)
    noop_cases = [
        ('N01', 'sourced',
         'the entry drops the S250/S251 citations but keeps one in-window row',
         lambda: {fx.ENTRY: fx.entry(source_lines=['source: S243 - x'])},
         'b:sourced',
         'the landing bullet demands S243/S244/S245/S249 AND S250/S251; one '
         'matching row satisfies the shipped `sourced`'),
        ('N02', 'scorecard_head', 'SCORECARD coverage head still says 141/141',
         lambda: {'SCORECARD.md': '| coverage | 9.72 → 10.0 | 141/141 |\n'},
         '(no binding exists for the SCORECARD head)',
         'the claims demand 141/141 → 142/142; the nine bindings never read '
         'SCORECARD.md'),
        ('N03', 'frontier_note', 'the LE `hsqs` clause is left in the Frontier list',
         lambda: {'PROVINCE.md': fx.province(extra=[
             'Still Frontier: LE AVM members (`hsqs`), AVM kernels.'])},
         'b:frontier_note',
         'the binding proves a note LINE exists; it never proves the Frontier '
         'list dropped `LE AVM members (hsqs)` — the promotion itself is '
         'unchecked'),
        ('N04', 'log_entry', 'no LOG.md entry for round 52',
         lambda: {'LOG.md': '# log\n'},
         '(no binding exists for the LOG entry)',
         'the claims demand a LOG entry; no binding reads LOG.md'),
        ('N05', 'entry_receipts', 'the entry names no fresh receipt path',
         lambda: {fx.ENTRY: fx.entry(receipts=False)},
         '(no binding exists for the receipt citation)',
         'the claims demand the entry name the fresh receipts'),
        ('N07', 'frontier_note',
         'the frontier note says the members STAY Frontier (a non-promotion note)',
         lambda: {'PROVINCE.md': fx.province().replace(
             'moved Frontier \u2192 Core with', 'stay Frontier; measured only, with')},
         'b:frontier_note',
         'the shipped check only proves the MARK, the STEM and an LE-AVM token '
         'co-occur on one line: it cannot tell a promotion note from a '
         '"measured, not promoted" note'),
        ('N08', 'province_core_row',
         'the only AVM-marker mention in the row is the NEGATIVE BE clause',
         lambda: {'PROVINCE.md': fx.province(
             cell='little-endian SquashFS v4 (`hsqs`) members '
                  '\u2014 handler `squashfs_v4_le`',
             layout='the AVM marker test exists only in the BE branch')},
         'b:province_core_row',
         'AVM_MARKER_RE scans the whole row minus the entry path, so a row that '
         'says the marker is a BE-branch thing still satisfies "names the AVM '
         'marker": the binding does not pin the LAYOUT the row claims'),
        ('N06', 'registry_rows',
         'no instrument-registry v2 row for the round-52 counter',
         lambda: {'SKILL.md': '<!-- instrument-registry v2 -->\n\n'
                              '<!-- /instrument-registry -->\n'},
         '(no binding exists for the registry row count)',
         'the claims demand exactly one registry row per new instrument'),
    ]
    for cid, target, desc, mut, finding, note in noop_cases:
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(root, exist_ok=True)
        new_repo(root)
        write_files(root, fx.files())
        commit(root, 'pristine')
        files = fx.files()
        files.update(mut())
        write_files(root, files)
        rev = commit(root, cid + ' ' + desc)
        after = eval_bindings(root, rev)
        record(cid, 'no-op-risk', target, desc, base, after, finding, note,
               expect_flip=False)

    # ------------------------------------------------ receipt-side clauses
    expr_subject = extract_stmt(src, 'subject_pin_ok')
    expr_handler = extract_stmt(src, 'handler_ok')
    expr_fresh = extract_stmt(src, 'receipt_fresh')

    def clause_subject(env, pin):
        ns = dict(vars(mod))
        ns.update({'subj': env.get('subject') or {}, 'pin': pin})
        return bool(eval(expr_subject, ns))

    def clause_handler(env):
        d = {'squashfs_handlers': mod.squashfs_chunk_handlers(env)}
        ns = dict(vars(mod))
        ns.update({'d': d})
        return bool(eval(expr_handler, ns))

    def clause_fresh(root_, rev, freeze, rel):
        adds = mod.all_adds(root_, rev, rel)
        d = {}
        ns = dict(vars(mod))
        ns.update({'d': d, 'adds': adds, 'freeze': freeze, 'root': root_,
                   'is_ancestor': mod.is_ancestor})
        return bool(eval(expr_fresh, ns)), adds

    env_good = {
        'operation': 'extract_firmware',
        'provider': {'id': 'unblob'},
        'subject': {'name': 'g7581.bin', 'digest': {'sha256': 'a' * 64}},
        'normalized_result': {
            'chunks': [{'handler': 'squashfs_v4_le', 'input_path': '$input',
                        'provider_id': 'p9', 'extraction_failed': False}],
            'files': [], 'extraction_gaps': [], 'unpublished_entries': [],
            'derivations': [], 'diagnostics': [], 'depth_limited_paths': [],
            'output_directory': '/fast/scratch/hyaku/kaidoku-r52/x/out',
            'selection': {'offset': 0, 'length': 10, 'sha256': 'a' * 64}},
    }
    PIN = 'a' * 64

    def env_with(handler='squashfs_v4_le', digest=None):
        e = json.loads(json.dumps(env_good))
        e['normalized_result']['chunks'][0]['handler'] = handler
        if digest is not None:
            e['subject']['digest']['sha256'] = digest
        return e

    # R1: receipt subject digest != the carrier pin
    good_subject = clause_subject(env_good, PIN)
    bad_subject = clause_subject(env_with(digest='b' * 64), PIN)
    results.append({
        'case': 'R1', 'kind': 'receipt-clause', 'target': 'subject_pin_ok',
        'mutation': 'receipt subject digest != the carrier pin',
        'before': {'subject_pin_ok': good_subject},
        'after': {'subject_pin_ok': bad_subject},
        'flipped': ['subject_pin_ok'] if good_subject != bad_subject else [],
        'flips_target': good_subject != bad_subject, 'expect_flip': True,
        'expected_finding': 'g7581:subject_pin_ok',
        'verdict': 'KILLED' if (good_subject and not bad_subject) else 'NO-OP',
        'note': 'the receipt names a different subject than the pinned carrier'})

    # R2/R3/R4: wrong chunk handler
    good_handler = clause_handler(env_good)
    for cid, name, h in (('R2', 'squashfs_v4_be', 'squashfs_v4_be'),
                         ('R3', 'squashfs_v4 (bare prefix)', 'squashfs_v4'),
                         ('R4', 'squashfs_v3', 'squashfs_v3')):
        val = clause_handler(env_with(handler=h))
        results.append({
            'case': cid, 'kind': 'receipt-clause', 'target': 'handler_ok',
            'mutation': 'receipt chunk handler = %s' % name,
            'before': {'handler_ok': good_handler},
            'after': {'handler_ok': val},
            'flipped': ['handler_ok'] if good_handler != val else [],
            'flips_target': good_handler != val, 'expect_flip': True,
            'expected_finding': 'g7581:handler_ok',
            'verdict': 'KILLED' if (good_handler and not val) else 'NO-OP',
            'note': 'every squashfs-family chunk handler must equal the frozen one'})

    # R5/R6/R7: receipt freshness against a real history
    RECEIPT_REL = 'corpus/evidence/round-52/c1/g7581/after.json'
    for cid, label, when, expect in (
            ('R5', 'receipt added BEFORE the freeze commit', 'before', False),
            ('R6', 'receipt added AT the freeze commit', 'at', False),
            ('R7', 'receipt added AFTER the freeze commit', 'after', True)):
        shutil.rmtree(root, ignore_errors=True)
        os.makedirs(root, exist_ok=True)
        new_repo(root)
        write_files(root, fx.files())
        commit(root, 'pristine')
        if when == 'before':
            write_files(root, {RECEIPT_REL: '{"data": {}}\n'})
            commit(root, 'receipt before freeze')
            freeze = commit(root, 'FREEZE')
            rev = commit(root, 'after freeze')
        elif when == 'at':
            write_files(root, {RECEIPT_REL: '{"data": {}}\n'})
            freeze = commit(root, 'FREEZE (receipt added here)')
            rev = commit(root, 'after freeze')
        else:
            freeze = commit(root, 'FREEZE')
            write_files(root, {RECEIPT_REL: '{"data": {}}\n'})
            rev = commit(root, 'receipt after freeze')
        val, adds = clause_fresh(root, rev, freeze, RECEIPT_REL)
        results.append({
            'case': cid, 'kind': 'receipt-clause', 'target': 'receipt_fresh',
            'mutation': label,
            'before': {'receipt_fresh': True},
            'after': {'receipt_fresh': val, 'adds': adds},
            'flipped': ['receipt_fresh'] if val is not True else [],
            'flips_target': val is not True, 'expect_flip': (expect is False),
            'expected_finding': 'g7581:receipt_fresh',
            'verdict': ('KILLED' if ((val is False) == (expect is False))
                        else 'NO-OP'),
            'note': 'expect receipt_fresh=%s' % expect})

    # R8/R9: the receipt-fresh BASE is a round-sensitive constant the v2
    # counter must expose as --receipt-fresh-base. A base NEWER than the
    # receipt's add must make the clause red; a base OLDER must keep it green.
    RECEIPT_REL2 = 'corpus/evidence/round-52/c1/g7581/after.json'
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root, exist_ok=True)
    new_repo(root)
    write_files(root, fx.files())
    commit(root, 'pristine')
    base_old = commit(root, 'BASE (older)')
    write_files(root, {RECEIPT_REL2: '{"data": {}}\n'})
    add_commit = commit(root, 'receipt added')
    base_new = commit(root, 'BASE (newer, stale for this receipt)')
    rev = commit(root, 'rev')
    val_old, adds = clause_fresh(root, rev, base_old, RECEIPT_REL2)
    val_new, _ = clause_fresh(root, rev, base_new, RECEIPT_REL2)
    results.append({
        'case': 'R8', 'kind': 'receipt-clause', 'target': 'receipt_fresh',
        'mutation': 'stale receipt-fresh base: the base is NEWER than the receipt add',
        'before': {'receipt_fresh': True},
        'after': {'receipt_fresh': val_new, 'adds': adds},
        'flipped': ['receipt_fresh'] if val_new is not True else [],
        'flips_target': val_new is not True, 'expect_flip': True,
        'expected_finding': 'g7581:receipt_fresh',
        'verdict': 'KILLED' if val_new is False else 'NO-OP',
        'note': 'the round-50 receipts reused under the round-52 base must be RED '
                'on receipt_fresh unless the base is pinned to round-50'})
    results.append({
        'case': 'R9', 'kind': 'receipt-clause', 'target': 'receipt_fresh',
        'mutation': 'control: the base is OLDER than the receipt add',
        'before': {'receipt_fresh': False},
        'after': {'receipt_fresh': val_old, 'adds': adds},
        'flipped': ['receipt_fresh'] if val_old is True else [],
        'flips_target': val_old is True, 'expect_flip': True,
        'expected_finding': '(none: clause stays true)',
        'verdict': 'KILLED' if val_old is True else 'NO-OP',
        'note': 'proves receipt_fresh is not trivially always-false'})

    # R10: carrier_fresh_ok with the v2 re_scored_pins allow-list. The v1
    # counter has no allow-list constant, so this case is specified but the
    # probe records the v1 behaviour (pin in prior_pins => carrier_fresh_ok
    # false) as the pre-state the v2 must change.
    spec_src = open(CTR_PATH).read()
    has_allow = 're_scored_pins' in spec_src
    results.append({
        'case': 'R10', 'kind': 'receipt-clause', 'target': 'carrier_fresh_ok',
        'mutation': 'a re-scored pin carried on the frozen re_scored_pins '
                    'allow-list (the four round-50 carrier pins)',
        'before': {'carrier_fresh_ok': None},
        'after': {'carrier_fresh_ok': None},
        'flipped': [], 'flips_target': False, 'expect_flip': True,
        'expected_finding': 'g7581:carrier_fresh_ok',
        'verdict': 'NO-OP' if not has_allow else 'UNSPECIFIED',
        'note': 'the counter under test has NO re_scored_pins constant '
                '(has_allow=%s): under v1 semantics a re-scored pin is simply '
                'not fresh, so the v2 must ADD the allow-list and a case that '
                'proves the four pins pass ONLY through it' % has_allow})

    shutil.rmtree(root, ignore_errors=True)

    payload = {
        'counter_under_test': CTR_PATH,
        'counter_sha256': hashlib.sha256(open(CTR_PATH, 'rb').read()).hexdigest(),
        'injected_missing_names': list(getattr(mod, '__injected__', [])),
        'constants_under_test': {
            'ENTRY': mod.ENTRY, 'STEM': mod.STEM,
            'CORE_HEADING': mod.CORE_HEADING, 'FRONTIER_MARK': mod.FRONTIER_MARK,
            'OPENED_DATES': list(mod.OPENED_DATES), 'HANDLER': mod.HANDLER},
        'window': {'in': fx.WIN_IN, 'before': fx.WIN_BEFORE, 'after': fx.WIN_AFTER},
        'extracted_clause_expressions': {
            'subject_pin_ok': expr_subject, 'handler_ok': expr_handler,
            'receipt_fresh': expr_fresh},
        'doc_bindings_evaluated': list(DOC_BINDINGS),
        'cases': results,
        'summary': {
            'total': len(results),
            'killed': sum(1 for r in results if r['verdict'] == 'KILLED'),
            'no_op': sum(1 for r in results if r['verdict'] == 'NO-OP'),
            'cascade': sum(1 for r in results if r['verdict'] == 'CASCADE'),
            'dead': sum(1 for r in results if r['verdict'] == 'DEAD'),
            'covered': sum(1 for r in results if r['verdict'] == 'COVERED'),
            'green': sum(1 for r in results if r['verdict'] == 'GREEN'),
            'baseline_red': sum(1 for r in results
                                if r['verdict'] == 'BASELINE-RED'),
        },
    }
    with open(OUT_JSON, 'w') as fh:
        json.dump(payload, fh, indent=1, sort_keys=False)
    print(json.dumps(payload['summary'], sort_keys=True))
    for r in results:
        print('%-8s %-14s %-22s %-9s %s' % (r['case'], r['kind'], r['target'],
                                            r['verdict'], r['mutation'][:74]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
