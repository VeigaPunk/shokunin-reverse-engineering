#!/usr/bin/env python3
"""R41C2Mutants phase 1: re-derive the round-40 surviving mutants on the
round-41 base bytes (git show 49096c7e:tools/round-40/{c2-counter.py,sqfs-triage-v2.py})
and run the --selftest detector on each. Scratch-only; the lane is never written."""
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE_REV = '49096c7e6f226af0c750c4b003be58883cb6049f'
FREEZE_R40 = '7fce308631a8b457d6b7c5a4b39a923c4e9a49de'

BASE_C = open(S + '/c2-counter.base.py', encoding='utf-8').read()
BASE_I = open(S + '/sqfs-triage-v2.base.py', encoding='utf-8').read()

# ---- exact single-string mutations, copied from the round-40 wave-2 artifacts
COUNTER_MUTANTS = [
    ('M02-regen-seed-vacuated',
     "        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze",
     "        b['regenerated_seed_matches_freeze'] = True"),
    ('M03-regen-digest-dropped',
     '            regen_ok = bool(regen_sha) and regen_sha == msha \\',
     '            regen_ok = bool(regen_sha) and True \\'),
    ('M04-regen-arm-dropped',
     "                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm') \\",
     "                and r.get('class') == c.get('class') \\"),
    ('M11-pair-match-label-only',
     """                row['pair_match'] = (row['label'] == row['expected_label']
                                     and row['action'] == row['expected_action'])""",
     "                row['pair_match'] = (row['label'] == row['expected_label'])"),
    ('M19-writer-sha-vacuated',
     "        b['writer_matches_manifest'] = declared_w_sha is None or declared_w_sha == w_sha",
     "        b['writer_matches_manifest'] = True"),
    # new mutants on the restore-does-not-unblock clause (real base code)
    ('N01-frozen-scan-tip-only',
     """    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', '--no-renames',
                        '%s..%s' % (freeze, rev), '--', *FROZEN],
                       capture_output=True, text=True)""",
     """    p = subprocess.run(['git', '-C', root, 'diff', '--name-only',
                        freeze, rev, '--', *FROZEN],
                       capture_output=True, text=True)"""),
    ('N14-unevaluable-exit-1',
     "        out['exit_code'] = 2\n        out['argv'] = sys.argv",
     "        out['exit_code'] = 1\n        out['argv'] = sys.argv"),
]

INTERP_MUTANTS = [
    ('M05-last-marker-wins',
     "        if MARKER in lines[i]:\n            marker_line = i\n            break",
     "        if MARKER in lines[i]:\n            marker_line = i"),
    ('M07-none-set-cell-accepts-any',
     "        return not values", "        return True"),
    ('M15-repeated-set-member-accepted',
     "    if len(set(parts)) != len(parts):",
     "    if len(set(parts)) != len(parts) and False:"),
    ('M26-string-provider-ignored',
     "    elif isinstance(provider, str):\n        provider_id = provider",
     "    elif isinstance(provider, str):\n        provider_id = ''"),
    ('M28-blank-line-walk-disabled',
     "    while actions_line > start and not lines[actions_line].strip():",
     "    while actions_line > start and not lines[actions_line].strip() and False:"),
    ('M30-nr-diagnostics-be-source-dropped',
     "    for source in (nr.get('diagnostics'), data.get('diagnostics')):",
     "    for source in (data.get('diagnostics'),):"),
    ('M10-fnmatch-normcase',
     "        if not any(fnmatch.fnmatchcase(value, payload) for value in feat['H']):",
     "        if not any(fnmatch.fnmatch(value, payload) for value in feat['H']):"),
]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def apply_mutant(src, old, new, mid):
    n = src.count(old)
    if n != 1:
        raise SystemExit('%s: anchor count %d != 1' % (mid, n))
    return src.replace(old, new)


def selftest_detector(path):
    p = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                       capture_output=True, text=True, timeout=2400)
    doc = None
    for line in p.stdout.splitlines():
        if line.strip().startswith('{'):
            try:
                doc = json.loads(line)
            except Exception:
                pass
    return {'exit': p.returncode, 'doc': doc, 'stderr_tail': (p.stderr or '')[-200:]}


def heldout_detector(path, skill):
    held = os.path.join(LANE, 'corpus/evidence/round-40/c2/heldout')
    man = json.load(open(os.path.join(held, 'manifest.json')))
    la = man['label_actions']
    expect = {}
    for c in man['carriers']:
        expect[c['id']] = (c['label'], la[c['label']])
    envs = [os.path.join(held, i, 'envelope.json') for i in sorted(expect)]
    p = subprocess.run([sys.executable, '-I', '-B', path, '--skill', skill] + envs,
                       capture_output=True, text=True, timeout=600)
    wrong = []
    if p.returncode == 0:
        for line in p.stdout.splitlines():
            parts = line.split('\t')
            if len(parts) >= 3:
                cid = os.path.basename(os.path.dirname(parts[0]))
                got = (parts[1], parts[2])
                if cid in expect and got != expect[cid]:
                    wrong.append('%s:%s!=%s' % (cid, '/'.join(got), '/'.join(expect[cid])))
    return {'exit': p.returncode, 'wrong': wrong[:6], 'n_wrong': len(wrong)}


def main():
    os.makedirs(S + '/mutants', exist_ok=True)
    skill_base = os.path.join(S, 'SKILL.base.md')
    with open(skill_base, 'wb') as fh:
        fh.write(subprocess.run(['git', '-C', LANE, 'show', BASE_REV + ':SKILL.md'],
                                capture_output=True, check=True).stdout)
    out = {'base_rev': BASE_REV,
           'counter_base_sha256': sha_bytes(BASE_C.encode()),
           'interp_base_sha256': sha_bytes(BASE_I.encode())}

    pris_c = os.path.join(S, 'counter-pristine.py')
    pris_i = os.path.join(S, 'interp-pristine.py')
    open(pris_c, 'w').write(BASE_C)
    open(pris_i, 'w').write(BASE_I)
    print('baseline counter selftest ...', flush=True)
    out['baseline_counter_selftest'] = selftest_detector(pris_c)
    print(json.dumps(out['baseline_counter_selftest']['doc']), flush=True)
    print('baseline interp selftest ...', flush=True)
    out['baseline_interp_selftest'] = selftest_detector(pris_i)
    print(json.dumps(out['baseline_interp_selftest']['doc']), flush=True)
    out['baseline_interp_heldout_at_base_skill'] = heldout_detector(pris_i, skill_base)
    print(json.dumps(out['baseline_interp_heldout_at_base_skill']), flush=True)

    results = {}
    for mid, old, new in COUNTER_MUTANTS:
        mpath = os.path.join(S, 'mutants', 'counter-%s.py' % mid)
        open(mpath, 'w').write(apply_mutant(BASE_C, old, new, mid))
        print('counter mutant %s selftest ...' % mid, flush=True)
        results[mid] = {'kind': 'counter', 'path': mpath,
                        'mutant_sha256': sha_bytes(open(mpath, 'rb').read()),
                        'selftest': selftest_detector(mpath)}
        print(json.dumps(results[mid]['selftest']['doc']), flush=True)
    for mid, old, new in INTERP_MUTANTS:
        mpath = os.path.join(S, 'mutants', 'interp-%s.py' % mid)
        open(mpath, 'w').write(apply_mutant(BASE_I, old, new, mid))
        print('interp mutant %s selftest ...' % mid, flush=True)
        results[mid] = {'kind': 'interp', 'path': mpath,
                        'mutant_sha256': sha_bytes(open(mpath, 'rb').read()),
                        'selftest': selftest_detector(mpath),
                        'heldout': heldout_detector(mpath, skill_base)}
        print(json.dumps(results[mid]['selftest']['doc']), flush=True)
    out['mutants'] = results
    with open(os.path.join(S, 'derive-results.json'), 'w') as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print('WROTE derive-results.json', flush=True)


if __name__ == '__main__':
    main()
