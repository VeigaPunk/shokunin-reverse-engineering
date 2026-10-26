#!/usr/bin/env python3
"""R40W2C2CounterMutants: single-logic mutation testing of c2-counter.py.

Detectors per mutant:
  D1 --selftest            (pristine: exit 0, 42/42 pass)
  D2 real run at REV=42c10a58.. FREEZE=7fce3086.. (pristine: exit 0, matched 26/26)
The lane is never modified: mutants are copies under scratch.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC = os.path.join(LANE, 'tools/round-40/c2-counter.py')
REV = '42c10a58cb2cae3a4a0122af35a0cf95ac718043'
FREEZE = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'
S = os.path.dirname(os.path.abspath(__file__))
MUTDIR = os.path.join(S, 'mut')
os.makedirs(MUTDIR, exist_ok=True)

MUTANTS = [
    ('M01-seed-match-vacuated',
     'seed==freeze binding vacuated: seed_matches_freeze := True',
     "    b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze",
     "    b['seed_matches_freeze'] = True"),
    ('M02-regen-seed-vacuated',
     'regenerated-manifest seed==freeze binding vacuated',
     "        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze",
     "        b['regenerated_seed_matches_freeze'] = True"),
    ('M03-regen-digest-dropped',
     'regeneration compare: regenerated carrier sha256 no longer compared to manifest pin',
     '            regen_ok = bool(regen_sha) and regen_sha == msha \\',
     '            regen_ok = bool(regen_sha) and True \\'),
    ('M04-regen-arm-dropped',
     'regeneration compare: regenerated arm no longer compared to manifest arm',
     "                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm') \\",
     "                and r.get('class') == c.get('class') \\"),
    ('M05-v2-identity-vacuated',
     'v2 table identity: v2_table_identical no longer compares rev bytes to freeze bytes',
     "    b['v2_table_identical'] = v2_rev is not None and v2_fz is not None and v2_rev == v2_fz",
     "    b['v2_table_identical'] = v2_rev is not None and v2_fz is not None"),
    ('M06-v2-columns-no-action',
     'v2 columns check no longer requires the action column',
     "V2_COLUMNS = ('label', 'operation', 'provider', 'action')",
     "V2_COLUMNS = ('label', 'operation', 'provider')"),
    ('M07-manifest-after-freeze-weakened',
     'manifest-after-freeze: first-add ordering checks (!= freeze, is_ancestor) dropped',
     "        b['manifest_after_freeze'] = bool(ma) and ma != freeze and is_ancestor(root, freeze, ma)",
     "        b['manifest_after_freeze'] = bool(ma)"),
    ('M08-manifest-before-env-vacuated',
     'manifest-before-envelopes binding vacuated',
     """        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \\
            and all(fa is not None and is_ancestor(root, ma, fa) for fa in env_firsts)""",
     "        b['manifest_before_envelopes'] = True"),
    ('M09-envelope-digest-dropped',
     'digest check: envelope subject digest no longer compared to carrier pin',
     '                    digest_ok = bool(msha) and subject_sha(eo) == msha',
     '                    digest_ok = ebytes is not None'),
    ('M10-committed-digest-dropped',
     'digest check: committed carrier bytes no longer compared to manifest pin',
     '            commit_ok = committed_sha is not None and committed_sha == msha',
     '            commit_ok = committed_sha is not None'),
    ('M11-pair-match-label-only',
     'pair match: observed action no longer compared to expected action',
     """                row['pair_match'] = (row['label'] == row['expected_label']
                                     and row['action'] == row['expected_action'])""",
     "                row['pair_match'] = (row['label'] == row['expected_label'])"),
    ('M12-pair-match-vacuated',
     'pair match vacuated: pair_match := True for every carrier',
     """                row['pair_match'] = (row['label'] == row['expected_label']
                                     and row['action'] == row['expected_action'])""",
     "                row['pair_match'] = True"),
    ('M13-nomatch-row-exemption-gone',
     'L1-added NOMATCH handling (reported): carriers with the unclassified label no longer exempt from reporting a row',
     """        reported = bool(got) and all(r.get('row') is not None or r.get('label') == NOMATCH_PAIR[0]
                                     for r in res['carriers'])""",
     """        reported = bool(got) and all(r.get('row') is not None
                                     for r in res['carriers'])"""),
    ('M14-nomatch-pair-exemption-gone',
     'L1-added NOMATCH handling (consistent): the no-match pair no longer exempt from the row-consistency check',
     "        consistent = reported and all(len(v) == 1 and (None not in v or k == NOMATCH_PAIR)",
     "        consistent = reported and all(len(v) == 1 and (None not in v)"),
    ('M15-arms-valid-drop-ood',
     "arms_valid no longer accepts the 'ood' arm",
     "    b['arms_valid'] = bool(carriers) and all(c.get('arm') in ('after', 'before', 'ood')",
     "    b['arms_valid'] = bool(carriers) and all(c.get('arm') in ('after', 'before')"),
    ('M16-met-target-drops-bindings',
     'met_target formula: bindings_ok dropped from met (single site; consistency guard should fire)',
     '        met = bool(matched == N and bindings_ok)',
     '        met = bool(matched == N)'),
    ('M17-frozen-scope-counter-only',
     'freeze integrity: frozen-path scan narrowed to the counter itself',
     "                        '%s..%s' % (freeze, rev), '--', *FROZEN],",
     "                        '%s..%s' % (freeze, rev), '--', COUNTER],"),
    ('M18-generator-sha-vacuated',
     'manifest generator digest no longer compared to freeze blob',
     "        b['generator_sha_matches_freeze'] = declared_gen_sha is None or declared_gen_sha == gen_sha",
     "        b['generator_sha_matches_freeze'] = True"),
    ('M19-writer-sha-vacuated',
     'manifest writer digest no longer compared to freeze blob',
     "        b['writer_matches_manifest'] = declared_w_sha is None or declared_w_sha == w_sha",
     "        b['writer_matches_manifest'] = True"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def detector_selftest(path):
    p = run([sys.executable, '-I', '-B', path, '--selftest'])
    doc = None
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith('{'):
            try:
                doc = json.loads(line)
            except Exception:
                pass
    return {'exit': p.returncode, 'doc': doc,
            'stderr_tail': (p.stderr or '')[-300:]}


def detector_real(path, out_json):
    p = run([sys.executable, '-I', '-B', path, '--root', LANE, '--rev', REV,
             '--freeze', FREEZE, '--json-out', out_json])
    doc = None
    for line in p.stdout.splitlines():
        line = line.strip()
        if line.startswith('{'):
            try:
                doc = json.loads(line)
            except Exception:
                pass
    rec = None
    if os.path.exists(out_json):
        try:
            with open(out_json) as fh:
                rec = json.load(fh)
        except Exception:
            pass
    return {'exit': p.returncode, 'stdout': doc, 'stderr_tail': (p.stderr or '')[-300:]}


def main():
    with open(SRC, 'rb') as fh:
        pristine = fh.read()
    lane_sha_before = sha(pristine)
    assert lane_sha_before == '9bd792494ca042d840371e525ed6ea6a1f841f68415e4c405c41c13057183dd1', lane_sha_before

    base_st = detector_selftest(SRC)
    base_real = detector_real(SRC, os.path.join(S, 'baseline-real.json'))
    assert base_st['exit'] == 0 and base_st['doc']['fail'] == 0, base_st
    assert base_real['exit'] == 0 and base_real['stdout']['matched'] == 26, base_real
    print('baseline ok: selftest %s; real %s' % (base_st['doc'], base_real['stdout']))

    results = []
    for name, desc, old, new in MUTANTS:
        cnt = pristine.decode().count(old)
        if cnt != 1:
            results.append({'name': name, 'error': 'old_string count=%d' % cnt})
            print(name, 'SKIP count=%d' % cnt)
            continue
        mutpath = os.path.join(MUTDIR, name + '.py')
        mutated = pristine.decode().replace(old, new, 1)
        with open(mutpath, 'w') as fh:
            fh.write(mutated)
        st = detector_selftest(mutpath)
        real = detector_real(mutpath, os.path.join(S, 'mut-%s.json' % name))
        kill_selftest = st['exit'] != 0 or st['doc'] != base_st['doc']
        kill_real = real['exit'] != 0 or real['stdout'] != base_real['stdout']
        killed_by = []
        if kill_selftest:
            killed_by.append('selftest')
        if kill_real:
            killed_by.append('real')
        verdict = 'killed (%s)' % '+'.join(killed_by) if killed_by else 'SURVIVED'
        r = {
            'name': name, 'description': desc,
            'mutant_sha256': sha(mutated.encode()),
            'selftest_exit': st['exit'],
            'selftest_doc': st['doc'],
            'selftest_differs': kill_selftest,
            'real_exit': real['exit'],
            'real_stdout': real['stdout'],
            'real_differs': kill_real,
            'verdict': verdict,
        }
        if st['doc'] and st['doc'].get('failures'):
            r['selftest_failures'] = st['doc']['failures'][:4]
        if real['stdout']:
            r['real_bindings_false'] = real['stdout'].get('bindings_false')
            r['real_matched'] = real['stdout'].get('matched')
        if real['exit'] == 2:
            r['real_unevaluable'] = (rec_unev(os.path.join(S, 'mut-%s.json' % name)))
        results.append(r)
        print('%-38s selftest_exit=%d real_exit=%d -> %s' %
              (name, st['exit'], real['exit'], verdict))

    lane_after = sha(open(SRC, 'rb').read())
    summary = {
        'target': SRC, 'rev': REV, 'freeze': FREEZE,
        'pristine_sha256': lane_sha_before,
        'lane_sha256_after_all_runs': lane_after,
        'lane_untouched': lane_after == lane_sha_before,
        'pristine_selftest': base_st['doc'],
        'pristine_real': base_real['stdout'],
        'mutants': results,
    }
    with open(os.path.join(S, 'mutants-summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print('lane untouched:', lane_after == lane_sha_before)


def rec_unev(path):
    try:
        with open(path) as fh:
            d = json.load(fh)
        return d.get('unevaluable')
    except Exception:
        return None


if __name__ == '__main__':
    main()
