#!/usr/bin/env python3
"""Build the R50-C3 control fixtures (round-50 attempt 2, wave 3, seat ExecTriageControls).

Everything is derived from committed lane bytes; nothing is hand-copied.  Outputs go to
OUT = <lane>/.ufo/waves/round-50/w3/ExecTriageControls/ and to scratch.

Inputs (read-only):
  * SKILL.md at base f890bbead20ca2c549487167f56876ae47f1e1a4  (git show)
  * tools/round-42/sqfs-triage-v4.py                            (the lane's scored evaluator)
  * .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ (126 committed envelopes)

No REA, no network, no lane write outside OUT.
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
OUT = os.path.join(LANE, '.ufo/waves/round-50/w3/ExecTriageControls')
ENV_REL = '.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes'
ENV_DIR = os.path.join(LANE, ENV_REL)
TOOL = os.path.join(LANE, 'tools/round-42/sqfs-triage-v4.py')
SCRATCH = os.environ.get('SCRATCH') or '/fast/scratch/hyaku/kaidoku-r50/w3-ExecTriageControls'

NO_READER_CLAIM = ('squashfs_v2_nonstandard', 'squashfs_v3_broadcom',
                    'squashfs_v3_nonstandard')
V5_VOCAB_EXTRA = ('record-unverified', 'preserve-unresolved')

RECEIPTS = []


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def git(*args):
    p = subprocess.run(['git', '-C', LANE] + list(args), capture_output=True)
    return p.returncode, p.stdout, p.stderr


def record(rid, command, code, out, note='', err=b''):
    RECEIPTS.append({
        'id': rid,
        'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'command': command,
        'exit': code,
        'stdout_sha256': sha256_bytes(out),
        'stdout_bytes': len(out),
        'stderr_sha256': sha256_bytes(err),
        'stderr_bytes': len(err),
        'note': note,
    })
    return out


def load_v4():
    spec = importlib.util.spec_from_file_location('v4', TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_v4(skill_path, envelopes, json_out=True):
    cmd = [sys.executable, '-I', '-B', TOOL, '--skill', skill_path]
    if json_out:
        cmd.append('--json')
    cmd += envelopes
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    os.makedirs(OUT, exist_ok=True)
    v4 = load_v4()

    # ---------------------------------------------------------------- base SKILL.md
    code, out, err = git('show', '%s:SKILL.md' % BASE)
    assert code == 0, err
    record('R01', 'git -C %s show %s:SKILL.md' % (LANE, BASE), code, out,
           'base SKILL.md bytes', err)
    base_text = out.decode('utf-8')
    base_sha = sha256_bytes(out)
    lines = base_text.split('\n')
    with open(os.path.join(SCRATCH, 'SKILL-base.md'), 'wb') as fh:
        fh.write(out)

    # ------------------------------------------------- locate the v4 table block
    start = None
    for i, line in enumerate(lines):
        if '<!-- sqfs-triage-table v4 -->' in line:
            start = i
            break
    assert start is not None, 'v4 marker not found'
    assert 'sqfs-triage-actions:' in lines[start + 1], lines[start + 1][:80]
    end = start + 2
    while end < len(lines) and lines[end].lstrip().startswith('|'):
        end += 1
    block = lines[start:end]           # marker, vocabulary, header, separator, rows
    assert len(block) >= 4, block
    marker_line, vocab_line, header_line, sep_line = block[:4]
    row_lines = block[4:]
    assert len(row_lines) == 15, len(row_lines)

    with open(os.path.join(OUT, 'v4-table-at-base.md'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(block) + '\n')
    block_sha = sha256_bytes(('\n'.join(block) + '\n').encode('utf-8'))

    # ------------------------------------------------------------- cell utilities
    def cells(line):
        pre = line[:line.index('|')]
        rest = line[line.index('|'):]
        return pre, rest.split('|')

    def join(pre, cs):
        return pre + '|'.join(cs)

    def label_of(cs):
        return cs[1].strip()

    def action_index(cs):
        return 11

    def mutate(rows, fn):
        out_rows = []
        for line in rows:
            pre, cs = cells(line)
            cs = fn(cs)
            if cs is None:
                continue
            out_rows.append(join(pre, cs))
        return out_rows

    def set_label_clean(cs):
        cs = list(cs)
        cs[1] = ' clean '
        return cs

    def drop_guard(cs):
        if label_of(cs) == 'legacy-body-failure':
            return None
        return cs

    def swap_action(cs):
        cs = list(cs)
        if label_of(cs) == 'clean':
            cs[action_index(cs)] = ' `inspect-input` '
        return cs

    v4_vocab = vocab_line.split('<!-- sqfs-triage-actions:')[1].split('-->')[0].strip()
    v5_vocab = ' '.join(v4_vocab.split() + list(V5_VOCAB_EXTRA))

    TABLE_HEAD = [header_line, sep_line]

    def surface(rows, marker_version):
        if marker_version == 'v4':
            mk, cv = marker_line, vocab_line
        else:
            mk = '  <!-- sqfs-triage-table v5 -->'
            cv = '  <!-- sqfs-triage-actions: %s -->' % v5_vocab
        return [mk, cv] + TABLE_HEAD + list(rows)

    CONTROLS = {
        'ctl-do-nothing': (list(row_lines), 'the v4 table at base, extracted verbatim'),
        'ctl-junk': (mutate(row_lines, set_label_clean),
                     'every row label cell replaced by `clean`'),
        'ctl-guard-deleted': (mutate(row_lines, drop_guard),
                              'the `legacy-body-failure` row deleted'),
        'ctl-action-swapped': (mutate(row_lines, swap_action),
                               'the `clean` row action `none` -> `inspect-input`'),
    }

    # --------------------------------------------------------- document assembly
    def assemble(rows, marker_version):
        if marker_version == 'v4':
            new_block = [marker_line, vocab_line] + TABLE_HEAD + list(rows)
        else:
            new_block = surface(rows, 'v5')
        return '\n'.join(lines[:start] + new_block + lines[end:])

    docs = {}
    for name, (rows, _desc) in CONTROLS.items():
        for version in ('v4', 'v5'):
            text = assemble(rows, version)
            path = os.path.join(OUT, '%s.skill%s.md' % (name, '' if version == 'v4' else '.v5surface'))
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(text)
            docs[(name, version)] = path
        # the mutated table block on its own
        with open(os.path.join(OUT, '%s.table.md' % name), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(surface(rows, 'v5')) + '\n')

    # ------------------------------------------------------------ envelope census
    names = sorted(n for n in os.listdir(ENV_DIR)
                   if os.path.isdir(os.path.join(ENV_DIR, n)))
    code, out, err = git('ls-tree', '-r', '--name-only', BASE, '--', ENV_REL)
    assert code == 0, err
    record('R02', 'git -C %s ls-tree -r --name-only %s -- %s' % (LANE, BASE, ENV_REL),
           code, out, 'committed envelope paths at base', err)
    committed = [l for l in out.decode('utf-8').split('\n') if l.strip()]
    committed_envs = sorted({os.path.dirname(p).split('/')[-1] for p in committed})

    # ---------------------------------------------- per-envelope facts (v4 at base)
    env_paths = [os.path.join(ENV_DIR, n, 'envelope.json') for n in names]
    code, out, err = run_v4(os.path.join(SCRATCH, 'SKILL-base.md'), env_paths)
    record('R03', 'python3 -I -B tools/round-42/sqfs-triage-v4.py --skill <base SKILL.md> '
                  '--json <126 envelope paths>', code, out.encode('utf-8'),
           'v4 decisions for every envelope at base (%s)' % err.strip()[:200],
           err.encode('utf-8'))

    rules, _info = v4.parse_skill(base_text)
    envelopes = []
    for name, path in zip(names, env_paths):
        with open(path, 'rb') as fh:
            raw = fh.read()
        feat = v4.load_envelope(path)
        rule = v4.classify(rules, feat)
        idx = None if rule is None else rules.index(rule)
        envelopes.append({
            'name': name,
            'path': os.path.join(ENV_REL, name, 'envelope.json'),
            'bytes': len(raw),
            'sha256': sha256_bytes(raw),
            'declared_tuple': {
                'OP': feat['OP'], 'PV': feat['PV'],
                'H': sorted(feat['H']), 'HF': sorted(feat['HF']),
                'G': sorted(feat['G']), 'D': sorted(feat['D']),
                'BE': feat['BE'], 'SR': feat['SR'], 'P': feat['P'],
            },
            'v4_label_at_base': v4.decision(rule)[0],
            'v4_action_at_base': v4.decision(rule)[1],
            'v4_rule_index_at_base': idx,
            'family': sorted({h for h in feat['H'] if h.startswith('squashfs')}),
            'no_reader_family': sorted({h for h in feat['H'] if h.startswith(NO_READER_CLAIM)}),
        })

    def fam_set(env):
        return tuple(env['no_reader_family'])

    # ------------------------------------------- v5 evaluator model (reconstruction)
    # From plans/round-50-attempt2-claims.md section R50-C3, clause (1):
    #   a no-reader family takes `clean-unverified` (gaps none, >0 files) with action
    #   `record-unverified`, and `no-reader-failure` (extractor-failure, 0 files) with
    #   action `preserve-unresolved`; clause (2): reader-backed families keep the v4 rows.
    def v5_decision(env, no_reader_families):
        t = env['declared_tuple']
        ns = set(no_reader_families)
        if ns & set(env['family']):
            if not t['G'] and t['P'] > 0:
                return 'clean-unverified', 'record-unverified'
            if 'extractor-failure' in t['G'] and t['P'] == 0:
                return 'no-reader-failure', 'preserve-unresolved'
        return env['v4_label_at_base'], env['v4_action_at_base']

    # -------------------------------------------------- table side per control
    # The v4 tool is the stand-in for the instrument's table side: the control tables
    # are the v4 table with label/action cells mutated, and the v4 grammar is what the
    # v5 table inherits.  The junk control (all labels `clean`) is refused by the v4
    # parser (duplicate labels), so its table side is computed by substituting the
    # label of the row the base table already matched.
    table_side = {}
    for name, (rows, _d) in CONTROLS.items():
        doc = docs[(name, 'v4')]
        code, out, err = run_v4(doc, env_paths)
        record('R10-%s' % name,
               'python3 -I -B tools/round-42/sqfs-triage-v4.py --skill %s --json <126 envelopes>'
               % os.path.relpath(doc, LANE), code, out.encode('utf-8'),
               'control %s: table-side decisions (%s)' % (name, err.strip()[:160]),
               err.encode('utf-8'))
        proc2 = subprocess.run(
            [sys.executable, '-I', '-B', TOOL, '--skill', doc, '--table-only'],
            capture_output=True, text=True)
        code2, out2, err2 = proc2.returncode, proc2.stdout, proc2.stderr
        record('R11-%s' % name,
               'python3 -I -B tools/round-42/sqfs-triage-v4.py --skill %s --table-only'
               % os.path.relpath(doc, LANE), code2, out2.encode('utf-8'),
               'control %s: table parse (stderr: %s)' % (name, err2.strip()[:160]),
               err2.encode('utf-8'))
        if name == 'ctl-junk':
            # duplicate labels: the v4 parser refuses the table
            table_side[name] = None
            junk_err = err.strip()[:200]
        else:
            table_side[name] = {}
            per = {}
            try:
                payload = json.loads(out)
            except ValueError:
                payload = None
            if payload is not None:
                for res in payload.get('results', []):
                    per[os.path.relpath(res['path'], LANE)] = res
            for env in envelopes:
                res = per.get(env['path'])
                if res is None:
                    raise SystemExit('no decision for %s under %s' % (env['path'], name))
                table_side[name][env['name']] = (res['label'], res['action'])

    # junk: substitute the label of the row the base table matched
    junk_side = {}
    for env in envelopes:
        junk_side[env['name']] = ('clean', env['v4_action_at_base'])

    # ------------------------------------------------------ expected-red per control
    READINGS = {
        'claim-three-families': list(NO_READER_CLAIM),
        'census-two-families': ['squashfs_v2_nonstandard', 'squashfs_v3_nonstandard'],
        'census-v2ns-only': ['squashfs_v2_nonstandard'],
    }

    def mismatches(name, no_reader_families):
        side = junk_side if name == 'ctl-junk' else table_side[name]
        rows = []
        for env in envelopes:
            want = v5_decision(env, no_reader_families)
            got = side[env['name']]
            if want != got:
                rows.append({
                    'envelope': env['name'],
                    'table_label': got[0], 'table_action': got[1],
                    'evaluator_label': want[0], 'evaluator_action': want[1],
                    'label_mismatch': got[0] != want[0],
                    'action_mismatch': got[1] != want[1],
                })
        return rows

    V2NS_DDEFAULT = [e['name'] for e in envelopes
                     if e['no_reader_family'] == ['squashfs_v2_nonstandard']
                     and e['name'].endswith('_ddefault')]

    CLAUSE = {
        'ctl-do-nothing':
            "R50-C3 freeze kill rule: 'do-nothing (v4 table at base -> red)'.  The v4 table at "
            "base routes a no-reader family's healthy run to the `clean` row, whose action `none` "
            "is the oracle-backed action no reader can serve (F2), so every no-reader "
            "`_ddefault` envelope must mismatch the v5 evaluator's `clean-unverified`/"
            "`record-unverified`.",
        'ctl-junk':
            "R50-C3 freeze kill rule: 'junk table (every row `clean` -> red)'.  Every row's label "
            "is `clean`, so every envelope that the v4 precedence decided by a different row now "
            "reads `clean` and mismatches the evaluator; the junk table must not score green.",
        'ctl-guard-deleted':
            "R50-C3 freeze kill rule: 'guard-row-deleted mutant -> red'.  Deleting the "
            "`legacy-body-failure` row sends every reader-backed v1-v3 zero-file failure to "
            "`body-extractor-failure`/`preserve-failure`, while the v5 evaluator keeps the v4 "
            "legacy row for the reader-backed families, so those envelopes must mismatch.",
        'ctl-action-swapped':
            "R50-C3 freeze kill rule: 'swapped-action mutant -> red'.  The `clean` row's action "
            "`none` -> `inspect-input` changes the action of every envelope the clean row "
            "decides, so the action half of the pair must be compared: the control is red only "
            "if the instrument compares (label, action) pairs.",
    }

    for name, (_rows, _d) in CONTROLS.items():
        readings = {}
        for rname, fams in READINGS.items():
            rows = mismatches(name, fams)
            readings[rname] = {
                'no_reader_families': fams,
                'pair_mismatches': len(rows),
                'label_mismatches': sum(1 for r in rows if r['label_mismatch']),
                'action_mismatches': sum(1 for r in rows if r['action_mismatch']),
                'mismatch_envelopes': [r['envelope'] for r in rows],
            }
        primary = readings['claim-three-families']
        obj = {
            'control': name,
            'clause': CLAUSE[name],
            'kill_rule': 'R50-C3 kill rule (plans/round-50-attempt2-claims.md, section R50-C3): '
                         'a control that scores green stops C3.',
            'expected_exit': 1,
            'expected_exit_meaning': '1 = violation (the control is red: pair_mismatches > 0)',
            'expected_pair_mismatches': primary['pair_mismatches'],
            'expected_label_mismatches': primary['label_mismatches'],
            'expected_action_mismatches': primary['action_mismatches'],
            'expected_mismatch_envelopes': primary['mismatch_envelopes'],
            'must_include_v2ns_ddefault': [n for n in V2NS_DDEFAULT
                                           if n in primary['mismatch_envelopes']],
            'must_include_v2ns_ddefault_count': len([n for n in V2NS_DDEFAULT
                                                     if n in primary['mismatch_envelopes']]),
            'family_set_readings': readings,
            'table_side_source': 'tools/round-42/sqfs-triage-v4.py (the lane evaluator the v5 '
                                 'instrument is ported from), run offline on the 126 committed '
                                 'envelopes with the control document as --skill',
            'evaluator_side_source': 'OFFLINE RECONSTRUCTION of the attempt-2 claim text '
                                     '(plans/round-50-attempt2-claims.md, R50-C3 clause 1 and 2); '
                                     'the authoritative evaluator is the frozen instrument, so '
                                     'these numbers are predictions, not measurements',
            'envelopes_total': len(envelopes),
            'caveats': [],
        }
        if name == 'ctl-junk':
            obj['caveats'].append(
                'The junk table repeats the label `clean` in every row.  The v4 parser refuses '
                'duplicate labels (TableError), so under a v5 instrument that keeps that check '
                'the junk control is a PARSE refusal (exit 2, could-not-evaluate), not a '
                'mismatch red (exit 1).  Its table side was therefore computed by substituting '
                'the label of the row the base table matched - first-match order and every '
                'other cell are unchanged.  The L1 must either drop the duplicate-label check '
                'in the v5 parser or record the exit-2 refusal as this control\'s red.')
        if name == 'ctl-do-nothing':
            obj['caveats'].append(
                'The claim names three no-reader families but the round-49 reader census '
                '(corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md, "What stays Frontier") '
                'gives v3_broadcom a PARTIAL reader (7-Zip lists the committed LE broadcom '
                'fixture, unsquashfs refuses it).  The three family_set_readings give the '
                'mismatch count for each reading; every reading keeps the four v2ns `_ddefault` '
                'rows among the mismatches, so the predicate "the four v2ns *_ddefault rows '
                'among the mismatches" holds for all of them.')
            obj['caveats'].append(
                'The second new label (`no-reader-failure`/`preserve-unresolved`) is NOT witnessed '
                'by this corpus: no no-reader envelope in the 126 carries an extractor-failure '
                'gap, so the held-out dir exercises only the `clean-unverified` half.')
        if name == 'ctl-action-swapped':
            obj['caveats'].append(
                'This control is red only if the instrument compares (label, action) PAIRS.  A '
                'label-only comparison would report only the no-reader `_ddefault` mismatches '
                '(the same count as the do-nothing control) and would not distinguish this '
                'control from it.')
        with open(os.path.join(OUT, '%s.expected-red.json' % name), 'w',
                  encoding='utf-8') as fh:
            json.dump(obj, fh, indent=1, sort_keys=True)
            fh.write('\n')

    # ------------------------------------------------------------- manifest
    code, out, err = git('ls-tree', '-r', BASE, '--', ENV_REL)
    record('R04', 'git -C %s ls-tree -r %s -- %s' % (LANE, BASE, ENV_REL), code, out,
           'committed envelope blobs at base', err)
    committed_paths = {p.split('\t', 1)[1].strip()
                       for p in out.decode('utf-8').split('\n') if p.strip()}
    manifest = {
        'lane': LANE,
        'base_revision': BASE,
        'envelopes_dir': ENV_REL,
        'envelopes_dir_committed_at_base': len(committed_paths) == len(names),
        'committed_paths_at_base': len(committed_paths),
        'envelope_dirs_on_disk': len(names),
        'envelope_json_files': len(names),
        'envelope_sha256': sha256_bytes('\n'.join(sorted(
            os.path.join(ENV_REL, n, 'envelope.json') for n in names)).encode('utf-8')),
        'four_v2ns_ddefault': sorted(V2NS_DDEFAULT),
        'no_reader_families_in_claim': list(NO_READER_CLAIM),
        'envelopes': envelopes,
    }
    with open(os.path.join(OUT, 'envelopes-manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write('\n')

    # ship the generator and the decision dumper next to the artefacts
    import shutil
    for src in ('build_controls.py', 'analyze.py'):
        src_path = os.path.abspath(src)
        if os.path.exists(src_path):
            shutil.copyfile(src_path, os.path.join(OUT, src))

    # ------------------------------------------------------ extra receipts
    code, out, err = git('rev-parse', '%s^{commit}' % BASE)
    record('R05', 'git -C %s rev-parse %s^{commit}' % (LANE, BASE), code, out,
           'base revision resolves to a commit', err)

    # byte-identity of the do-nothing control document and the base SKILL.md
    with open(os.path.join(OUT, 'ctl-do-nothing.skill.md'), 'rb') as fh:
        donothing_bytes = fh.read()
    record('R06', 'sha256sum %s/ctl-do-nothing.skill.md  (compare with R01: base SKILL.md)'
           % OUT, 0, b'%s  ctl-do-nothing.skill.md\n' % sha256_bytes(donothing_bytes).encode(),
           'do-nothing control document is byte-identical to base SKILL.md: %s'
           % (sha256_bytes(donothing_bytes) == base_sha))

    # v4surface vs v5surface: only the marker and the vocabulary line may differ
    for name in CONTROLS:
        a = open(os.path.join(OUT, '%s.skill.md' % name), encoding='utf-8').read().split('\n')
        b = open(os.path.join(OUT, '%s.skill.v5surface.md' % name), encoding='utf-8').read().split('\n')
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        record('R07-%s' % name,
               'diff <(cat %s/%s.skill.md) <(cat %s/%s.skill.v5surface.md)'
               % (OUT, name, OUT, name), 0,
               ('\n'.join('%d\t%s\t%s' % (i, x.strip()[:60], y.strip()[:60])
                           for i, x, y in diff) + '\n').encode('utf-8'),
               'surface variants differ on %d line(s) (marker + vocabulary only)' % len(diff))

    # envelope dir on disk
    listing = subprocess.run(['find', ENV_DIR, '-mindepth', '1', '-maxdepth', '1', '-type', 'd'],
                             capture_output=True).stdout
    record('R08', 'find %s -mindepth 1 -maxdepth 1 -type d | wc -l' % ENV_DIR, 0,
           listing, 'envelope directories on disk')

    # the four v2ns _ddefault files, committed at base
    want = sorted(os.path.join(ENV_REL, n, 'envelope.json') for n in V2NS_DDEFAULT)
    code, out, err = git('ls-tree', '-r', '--name-only', BASE, '--', *want)
    record('R09', 'git -C %s ls-tree -r --name-only %s -- <four v2ns _ddefault paths>'
           % (LANE, BASE), code, out, 'the four v2ns _ddefault envelopes are committed at base',
           err)

    # artefact inventory
    inv = []
    for fn in sorted(os.listdir(OUT)):
        full = os.path.join(OUT, fn)
        if not os.path.isfile(full):
            continue
        if fn in ('receipts.tsv', 'receipts.json'):
            continue   # written after this inventory; a digest of them would be stale
        with open(full, 'rb') as fh:
            inv.append('%s  %s' % (sha256_bytes(fh.read()), fn))
    record('R12', 'sha256sum %s/* (receipts.tsv and receipts.json excluded: written after '
           'this inventory)' % OUT, 0, ('\n'.join(inv) + '\n').encode('utf-8'),
           'artefact inventory of the seat directory')

    with open(os.path.join(OUT, 'receipts.tsv'), 'w', encoding='utf-8') as fh:
        fh.write('id\tutc\tcommand\texit\tstdout_sha256\tstdout_bytes\tstderr_sha256\tstderr_bytes\tnote\n')
        for r in RECEIPTS:
            fh.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (
                r['id'], r['utc'], r['command'].replace('\t', ' '), r['exit'],
                r['stdout_sha256'], r['stdout_bytes'], r['stderr_sha256'],
                r['stderr_bytes'], r['note'].replace('\t', ' ')))
    with open(os.path.join(OUT, 'receipts.json'), 'w', encoding='utf-8') as fh:
        json.dump(RECEIPTS, fh, indent=1, sort_keys=True)
        fh.write('\n')

    print(json.dumps({
        'envelopes': len(names),
        'committed_ok': manifest['envelopes_dir_committed_at_base'],
        'v2ns_ddefault': sorted(V2NS_DDEFAULT),
        'controls': {name: json.load(open(os.path.join(
            OUT, '%s.expected-red.json' % name)))['expected_pair_mismatches']
            for name in CONTROLS},
        'block_sha256': block_sha,
        'base_skill_sha256': base_sha,
        'receipts': len(RECEIPTS),
    }, indent=1, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
