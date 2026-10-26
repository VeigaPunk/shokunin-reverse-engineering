#!/usr/bin/env python3
"""Mutation driver — seat R41W2C2CounterMut (kaidoku round 41 wave 2).

Target: tools/round-41/c2-counter.py (frozen C2 counter).

Detector per mutant (bounded, identical for every probe):
  D1  python3 -I -B <mutant> --selftest
        -> exit code + selftest pass/fail counts + failure names
  D2  python3 -I -B <mutant> --root LANE --rev E9 --freeze D7 --json-out R
        -> exit code + (matched, n, met_target, bindings_false, unevaluable,
           declared_features missing/mismatch counts)

The lane tree is NEVER modified: every mutant is a scratch copy under
$S/muts; the measured repo is only read through read-only `git -C LANE`
commands (show/log/ls-tree/merge-base/rev-parse/cat-file).
"""
import hashlib
import json
import os
import subprocess
import sys
import time

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
SRC = LANE + '/tools/round-41/c2-counter.py'
S = '/fast/scratch/hyaku/kaidoku-r41/R41W2C2CounterMut'
MUTDIR = S + '/muts'
HS = S + '/hs'
REV = 'e9a24d07256d1606f01aa4d2d65f74e649c5f3d4'
FREEZE = 'd764389e9cbe61b9d1b07538ff3bff02d50bb34f'

M = {}


def mut(mid, old, new):
    assert mid not in M, mid
    M[mid] = [(old, new)]


# ---- evaluator-comparison area -------------------------------------------
mut('M01',
    "        b['evaluator_covers_all'] = set(want_ids) <= set(exp)\n",
    "        b['evaluator_covers_all'] = True\n")
mut('M28',
    "        b['evaluator_covers_all'] = set(want_ids) <= set(exp)\n",
    "        b['evaluator_covers_all'] = bool(exp)\n")
mut('M02',
    "            row['pair_match'] = e is not None and row['label'] == e[0] \\\n"
    "                and row['action'] == e[1]\n",
    "            row['pair_match'] = e is not None and row['label'] == e[0]\n")
mut('M03',
    "            row['pair_match'] = e is not None and row['label'] == e[0] \\\n"
    "                and row['action'] == e[1]\n",
    "            row['pair_match'] = e is not None and row['action'] == e[1]\n")

# ---- observed_features_match_declared area --------------------------------
mut('M05',
    "            elif isinstance(c.get('declared_features'), dict):\n"
    "                decl = c['declared_features']\n"
    "            elif decl_key:\n",
    "            elif isinstance(c.get('declared_features'), dict):\n"
    "                decl = c['declared_features']\n"
    "            elif isinstance(c.get('declared'), dict):\n"
    "                decl = c['declared']\n"
    "            elif decl_key:\n")
mut('M06',
    "        b['observed_features_match_declared'] = N > 0 and not feat_missing \\\n"
    "            and not feat_bad\n",
    "        b['observed_features_match_declared'] = True\n")
mut('M07',
    "        b['observed_features_match_declared'] = N > 0 and not feat_missing \\\n"
    "            and not feat_bad\n",
    "        b['observed_features_match_declared'] = N > 0 and not feat_bad\n")
mut('M08',
    "            if bad:\n"
    "                feat_bad.append({'id': cid, 'class': c.get('class'), 'differ': bad,\n",
    "            if bad and str(c.get('class')) != COMBO_CLASS:\n"
    "                feat_bad.append({'id': cid, 'class': c.get('class'), 'differ': bad,\n")

# ---- real_receipts area ----------------------------------------------------
mut('M11',
    "            ok = i_pair[0] == REAL_LABEL and e_pair is not None and i_pair == e_pair\n",
    "            ok = e_pair is not None and i_pair == e_pair\n")
mut('M12',
    "            ok = i_pair[0] == REAL_LABEL and e_pair is not None and i_pair == e_pair\n",
    "            ok = i_pair[0] == REAL_LABEL\n")
mut('M13',
    "        real_ok = bool(rpaths) and len(rpaths) == len(REAL_RECEIPTS)\n",
    "        real_ok = True\n")
mut('M30',
    "REAL_RECEIPTS = ('corpus/evidence/round-40/c1/V1/after.json',\n"
    "                 'corpus/evidence/round-40/c1/V2/after.json',\n"
    "                 'corpus/evidence/round-40/c1/L1/after.json',\n"
    "                 'corpus/evidence/round-40/c1/L2/after.json')\n",
    "REAL_RECEIPTS = ('corpus/evidence/round-40/c1/V1/after.json',\n"
    "                 'corpus/evidence/round-40/c1/V2/after.json',\n"
    "                 'corpus/evidence/round-40/c1/L1/after.json')\n")

# ---- seed==freeze area -----------------------------------------------------
mut('M14',
    "    b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze\n",
    "    b['seed_matches_freeze'] = str(man.get('seed', '')).lower()[:8] == freeze[:8]\n")
mut('M15',
    "        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze\n",
    "        b['regenerated_seed_matches_freeze'] = True\n")

# ---- manifest first-add area -----------------------------------------------
mut('M16',
    "        b['manifest_after_freeze'] = bool(ma) and ma != freeze and is_ancestor(root, freeze, ma)\n",
    "        b['manifest_after_freeze'] = bool(ma)\n")
mut('M17',
    "        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \\\n"
    "            and all(fa is not None and is_ancestor(root, ma, fa) for fa in env_firsts)\n",
    "        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \\\n"
    "            and all(fa is not None for fa in env_firsts)\n")
mut('M35',
    "        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \\\n"
    "            and all(fa is not None and is_ancestor(root, ma, fa) for fa in env_firsts)\n",
    "        b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) \\\n"
    "            and all(fa is not None and is_ancestor(root, freeze, fa) for fa in env_firsts)\n")

# ---- table bytes area ------------------------------------------------------
mut('M18',
    "    b['v3_block_identical'] = v3_rev is not None and skill_fz is not None \\\n"
    "        and v3_rev == skill_fz\n",
    "    b['v3_block_identical'] = v3_rev is not None and skill_fz is not None\n")
mut('M19',
    "    scanned = commits_touching(root, '%s..%s' % (freeze, rev), SKILL)\n",
    "    scanned = commits_touching(root, '%s..%s' % (freeze, rev), SKILL)[:1]\n")

# ---- frozen-path drift area ------------------------------------------------
mut('M20',
    "            if st in ('M', 'D', 'R', 'T', 'U'):\n",
    "            if st in ('M', 'D', 'R', 'T', 'U', 'A'):\n")
mut('M21',
    "            if st in ('M', 'D', 'R', 'T', 'U'):\n",
    "            if st in ('M', 'R', 'T', 'U'):\n")
mut('M22',
    "FROZEN_PATHS = (CLAIMS, 'tools/round-41', MANIFEST_DIR)\n",
    "FROZEN_PATHS = ('tools/round-41', MANIFEST_DIR)\n")
mut('M23',
    "    scope = {}\n"
    "    for p in WRITER_CANDIDATES:\n",
    "    scope = {}\n"
    "    for p in ():\n")

# ---- other bindings --------------------------------------------------------
mut('M37',
    "    b['ids_unique'] = bool(ids) and len(set(ids)) == len(ids) and all(ids)\n",
    "    b['ids_unique'] = True\n")
mut('M40',
    "        reported = bool(got) and all(\n"
    "            r.get('row') is not None\n"
    "            or (r.get('expected_label'), r.get('expected_action')) == NOMATCH_PAIR\n"
    "            for r in res['carriers'])\n",
    "        reported = bool(got) and all(\n"
    "            r.get('row') is not None\n"
    "            for r in res['carriers'])\n")
mut('M45',
    "        b['envelopes_valid'] = N > 0 and all(r['digest_ok'] for r in res['carriers'])\n",
    "        b['envelopes_valid'] = N > 0 and all(r['envelope'] is not None for r in res['carriers'])\n")
mut('M46',
    "            commit_ok = committed_sha is not None and committed_sha == msha\n",
    "            commit_ok = committed_sha is not None and committed_sha == regen_sha\n")
mut('M47',
    "            regen_ok = bool(regen_sha) and regen_sha == msha \\\n"
    "                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm')\n",
    "            regen_ok = bool(regen_sha) and regen_sha == msha\n")
mut('M32',
    "def envelope_data(obj):\n"
    "    if isinstance(obj, dict) and 'subject' not in obj and isinstance(obj.get('data'), dict):\n"
    "        return obj['data']\n"
    "    return obj\n",
    "def envelope_data(obj):\n"
    "    return obj\n")


def apply(src, patches):
    out = src
    for old, new in patches:
        n = out.count(old)
        if n != 1:
            raise SystemExit('patch %r matches %d times' % (old[:70], n))
        out = out.replace(old, new)
    return out


def run(cmd, env, timeout=1800):
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=env)
    return p, time.time() - t0


def selftest_probe(mpath, env):
    p, dt = run([sys.executable, '-I', '-B', mpath, '--selftest'], env)
    st = None
    for line in (p.stdout or '').splitlines():
        if line.startswith('{'):
            try:
                st = json.loads(line)
            except Exception:
                pass
    return {'exit': p.returncode, 'seconds': round(dt, 1),
            'pass': (st or {}).get('pass'), 'fail': (st or {}).get('fail'),
            'cases': (st or {}).get('cases'),
            'failures': (st or {}).get('failures', [])[:8],
            'stderr_tail': (p.stderr or '')[-200:]}


def real_probe(mpath, env, rout):
    p, dt = run([sys.executable, '-I', '-B', mpath, '--root', LANE,
                 '--rev', REV, '--freeze', FREEZE, '--json-out', rout], env)
    row = {'exit': p.returncode, 'seconds': round(dt, 1),
           'stdout': (p.stdout or '').strip()[:500],
           'stderr_tail': (p.stderr or '')[-300:]}
    if os.path.exists(rout):
        try:
            with open(rout, 'rb') as fh:
                blob = fh.read()
            rec = json.loads(blob.decode())
            df = rec.get('declared_features') or {}
            row.update({
                'receipt_sha256': hashlib.sha256(blob).hexdigest(),
                'receipt_bytes': len(blob),
                'matched': rec.get('matched'), 'n': rec.get('n'),
                'met_target': rec.get('met_target'),
                'bindings_false': rec.get('bindings_false'),
                'unevaluable': rec.get('unevaluable'),
                'frozen_paths_changed': rec.get('frozen_paths_changed'),
                'distinct_decisions': rec.get('distinct_decisions'),
                'matched_classes': rec.get('matched_classes'),
                'matched_combos': rec.get('matched_combos'),
                'df_missing_count': len(df.get('missing') or []),
                'df_mismatch_count': len(df.get('mismatch') or []),
                'df_source': df.get('source'),
                'exit_code': rec.get('exit_code'),
            })
        except Exception as e:
            row['receipt_error'] = repr(e)[:200]
    return row


def main(ids):
    os.makedirs(MUTDIR, exist_ok=True)
    os.makedirs(HS, exist_ok=True)
    with open(SRC, 'rb') as fh:
        src = fh.read().decode()
    base_sha = hashlib.sha256(src.encode()).hexdigest()
    env = dict(os.environ)
    env['HYAKU_SCRATCH'] = HS
    env['TMPDIR'] = S
    summary = MUTDIR + '/summary.jsonl'
    for mid in ids:
        if mid not in M:
            raise SystemExit('unknown mutant ' + mid)
        text = apply(src, M[mid])
        mpath = MUTDIR + '/' + mid + '.py'
        with open(mpath, 'w') as fh:
            fh.write(text)
        rout = MUTDIR + '/' + mid + '.receipt.json'
        if os.path.exists(rout):
            os.unlink(rout)
        row = {'id': mid, 'base_sha256': base_sha,
               'mutant_sha256': hashlib.sha256(text.encode()).hexdigest()}
        t0 = time.time()
        row['selftest'] = selftest_probe(mpath, env)
        row['real'] = real_probe(mpath, env, rout)
        row['wall'] = round(time.time() - t0, 1)
        with open(summary, 'a') as fh:
            fh.write(json.dumps(row, sort_keys=True) + '\n')
        print(json.dumps(row, sort_keys=True))
        sys.stdout.flush()
    print('DONE n=%d' % len(ids))


if __name__ == '__main__':
    main(sys.argv[1:] or sorted(M))
