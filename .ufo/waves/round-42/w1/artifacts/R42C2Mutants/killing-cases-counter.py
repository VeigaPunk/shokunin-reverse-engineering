#!/usr/bin/env python3
"""R42C2Mutants: killing-case verification for the v4 C2 counter.

Adds 11 selftest cases (plus their fixture muts/modes) to the base
c2-counter.py selftest, then runs:
  - pristine + cases  -> expect exactly the documented v3 failure
                         (the manifest-level tuple map is still read: exit 0)
  - <survivor> + cases -> expect exactly that survivor's new case in failures
Every case is thus shown to kill its mutant and pass a correct counter
(except the manifest-level case, which the v4 contract alone satisfies).
"""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'base')
SRC = os.path.join(BASE, 'c2-counter.py')
MUT = os.path.join(ROOT, 'muts')
OUT = os.path.join(ROOT, 'out')

CASES = [
    # (name, old-anchor, insertion) -- applied in order
    ('stub-eval-modes',
     "    if MODE == 'disagree_action' and ident == 'H01':\n"
     "        act = 'confirm-empty'\n"
     "    if MODE == 'disagree_label' and ident == 'H01':\n"
     "        lab, act = 'unclassified', 'none'\n",
     "    if MODE == 'disagree_action' and ident == 'H01':\n"
     "        act = 'confirm-empty'\n"
     "    if MODE == 'disagree_label' and ident == 'H01':\n"
     "        lab, act = 'unclassified', 'none'\n"
     "    if MODE == 'disagree_action2' and d.get('stub_class') == 'clean-empty':\n"
     "        act = 'none'\n"
     "    if MODE == 'disagree_label2' and d.get('stub_class') == 'clean-empty':\n"
     "        lab = 'clean'\n"),
    ('seed-prefix8',
     "        seed = '0' * 64 if params.get('seed') == 'zero' else freeze\n",
     "        seed = ('0' * 64 if params.get('seed') == 'zero'\n"
     "                else freeze[:8] + 'a' * 56 if params.get('seed') == 'prefix8'\n"
     "                else freeze)\n"),
    ('digest-pin-wrong',
     "            if 'digest_mismatch' in muts and cid == 'H01':\n"
     "                digest = '0' * 64\n"
     "            if 'swap_digest' in muts and cid == 'H01':\n"
     "                digest = sha_by_id.get('H02', c['sha256'])\n",
     "            if 'digest_mismatch' in muts and cid == 'H01':\n"
     "                digest = '0' * 64\n"
     "            if 'swap_digest' in muts and cid == 'H01':\n"
     "                digest = sha_by_id.get('H02', c['sha256'])\n"
     "            if 'pin_wrong' in muts and cid == 'H01':\n"
     "                digest = 'f' * 64\n"),
    ('entry-muts',
     "            entry = dict(c)\n",
     "            entry = dict(c)\n"
     "            if 'arm_swap' in muts and cid == 'H01':\n"
     "                entry['arm'] = 'before'\n"
     "            if 'dup_id' in muts and cid == 'H02':\n"
     "                entry['id'] = 'H01'\n"
     "            if 'pin_wrong' in muts and cid == 'H01':\n"
     "                entry['sha256'] = 'f' * 64\n"
     "            if 'declare_via_declared_features' in muts:\n"
     "                if isinstance(entry.get('class_expected'), dict) \\\n"
     "                        and 'features' in entry['class_expected']:\n"
     "                    entry['declared_features'] = entry['class_expected'].pop('features')\n"
     "                if isinstance(entry.get('features'), dict):\n"
     "                    entry['declared_features'] = entry.pop('features')\n"
     "            if 'declare_via_legacy_declared' in muts:\n"
     "                if isinstance(entry.get('class_expected'), dict) \\\n"
     "                        and 'features' in entry['class_expected']:\n"
     "                    entry['declared'] = entry['class_expected'].pop('features')\n"
     "                if isinstance(entry.get('features'), dict):\n"
     "                    entry['declared'] = entry.pop('features')\n"
     "            if 'manifest_level_tuples' in muts:\n"
     "                if isinstance(entry.get('class_expected'), dict) \\\n"
     "                        and 'features' in entry['class_expected']:\n"
     "                    entry['class_expected'].pop('features')\n"
     "                entry.pop('features', None)\n"),
    ('manifest-level-map',
     "        for rname in ('V1', 'V2', 'L1', 'L2'):\n",
     "        if 'manifest_level_tuples' in muts:\n"
     "            man['feature_tuples'] = {}\n"
     "            for e2 in man['carriers']:\n"
     "                man['feature_tuples'].setdefault(str(e2.get('class')), dict(FEAT))\n"
     "        for rname in ('V1', 'V2', 'L1', 'L2'):\n"),
    ('gen-seed-drift',
     "        claim = params.get('claim', 'after')\n"
     "        muts = params.get('muts', set())\n",
     "        claim = params.get('claim', 'after')\n"
     "        muts = params.get('muts', set())\n"
     "        if 'gen_seed_drift' in muts:\n"
     "            tool_tree[GEN] = gen_src.replace(\"man = {'seed': a.seed,\",\n"
     "                                             \"man = {'seed': str(a.seed) + '-drift',\")\n"),
    ('delete-frozen-claim',
     "        elif claim == 'befreeze':\n",
     "        elif claim == 'delete_frozen':\n"
     "            tree = dict(claim_files)\n"
     "            tree[MANIFEST] = man_text\n"
     "            tree.update(post)\n"
     "            commit(d, tree, 'claim data')\n"
     "            subprocess.run(['git', '-C', d, 'rm', '-q', COUNTER], check=True)\n"
     "            rev = commit(d, {}, 'delete a frozen tool')\n"
     "        elif claim == 'befreeze':\n"),
    ('new-cases',
     "        ('unevaluable: freeze not an ancestor of rev', dict(), 2, [], [], ('NONANCESTOR',)),\n"
     "    ]\n",
     "        ('unevaluable: freeze not an ancestor of rev', dict(), 2, [], [], ('NONANCESTOR',)),\n"
     "        ('green: tuples declared under the single key declared_features',\n"
     "         dict(muts={'declare_via_declared_features'}), 0, [],\n"
     "         ['observed_features_match_declared']),\n"
     "        ('red: tuples only under the legacy declared key stay a lookup failure',\n"
     "         dict(muts={'declare_via_legacy_declared'}), 1,\n"
     "         ['observed_features_match_declared'], []),\n"
     "        ('red: a manifest-level tuple map is not the declared key',\n"
     "         dict(muts={'manifest_level_tuples'}), 1,\n"
     "         ['observed_features_match_declared'], []),\n"
     "        ('red: seed shares the freeze prefix but differs',\n"
     "         dict(seed='prefix8'), 1, ['seed_matches_freeze'], []),\n"
     "        ('red: the frozen generator stamps a drifted seed into the regenerated manifest',\n"
     "         dict(muts={'gen_seed_drift'}), 1, ['regenerated_seed_matches_freeze'],\n"
     "         ['seed_matches_freeze']),\n"
     "        ('red: two carriers share one id', dict(muts={'dup_id'}), 1,\n"
     "         ['ids_unique'], []),\n"
     "        ('red: committed bytes match regeneration but the manifest pin points elsewhere',\n"
     "         dict(muts={'pin_wrong'}), 1, ['carriers_committed'], []),\n"
     "        ('red: a regenerated carrier ships the wrong arm',\n"
     "         dict(muts={'arm_swap'}), 1, ['carriers_regenerated'], []),\n"
     "        ('red: the evaluator rotates the action on one whole class',\n"
     "         dict(emode='disagree_action2'), 1, [],\n"
     "         ['row_decisions_consistent', 'evaluator_covers_all']),\n"
     "        ('red: the evaluator rotates the label on one whole class',\n"
     "         dict(emode='disagree_label2'), 1, [],\n"
     "         ['row_decisions_consistent', 'evaluator_covers_all']),\n"
     "        ('frozen: a frozen path is deleted by a later commit',\n"
     "         dict(claim='delete_frozen'), 2, [], []),\n"
     "    ]\n"),
]

NEW_CASE_NAMES = [
    'green: tuples declared under the single key declared_features',
    'red: tuples only under the legacy declared key stay a lookup failure',
    'red: a manifest-level tuple map is not the declared key',
    'red: seed shares the freeze prefix but differs',
    'red: the frozen generator stamps a drifted seed into the regenerated manifest',
    'red: two carriers share one id',
    'red: committed bytes match regeneration but the manifest pin points elsewhere',
    'red: a regenerated carrier ships the wrong arm',
    'red: the evaluator rotates the action on one whole class',
    'red: the evaluator rotates the label on one whole class',
    'frozen: a frozen path is deleted by a later commit',
]

# survivor / new-mutant patches, verbatim from the R41W2C2CounterMut driver
MUTANTS = {
    'M02': [("            row['pair_match'] = e is not None and row['label'] == e[0] \\\n"
             "                and row['action'] == e[1]\n",
             "            row['pair_match'] = e is not None and row['label'] == e[0]\n")],
    'M03': [("            row['pair_match'] = e is not None and row['label'] == e[0] \\\n"
             "                and row['action'] == e[1]\n",
             "            row['pair_match'] = e is not None and row['action'] == e[1]\n")],
    'M05': [("            elif isinstance(c.get('declared_features'), dict):\n"
             "                decl = c['declared_features']\n"
             "            elif decl_key:\n",
             "            elif isinstance(c.get('declared_features'), dict):\n"
             "                decl = c['declared_features']\n"
             "            elif isinstance(c.get('declared'), dict):\n"
             "                decl = c['declared']\n"
             "            elif decl_key:\n")],
    'M14': [("    b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze\n",
             "    b['seed_matches_freeze'] = str(man.get('seed', '')).lower()[:8] == freeze[:8]\n")],
    'M15': [("        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze\n",
             "        b['regenerated_seed_matches_freeze'] = True\n")],
    'M18': [("    b['v3_block_identical'] = v3_rev is not None and skill_fz is not None \\\n"
             "        and v3_rev == skill_fz\n",
             "    b['v3_block_identical'] = v3_rev is not None and skill_fz is not None\n")],
    'M21': [("            if st in ('M', 'D', 'R', 'T', 'U'):\n",
             "            if st in ('M', 'R', 'T', 'U'):\n")],
    'M37': [("    b['ids_unique'] = bool(ids) and len(set(ids)) == len(ids) and all(ids)\n",
             "    b['ids_unique'] = True\n")],
    'M46': [("            commit_ok = committed_sha is not None and committed_sha == msha\n",
             "            commit_ok = committed_sha is not None and committed_sha == regen_sha\n")],
    'M47': [("            regen_ok = bool(regen_sha) and regen_sha == msha \\\n"
             "                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm')\n",
             "            regen_ok = bool(regen_sha) and regen_sha == msha\n")],
    # new v4-contract mutant: the single declared key is not read at all
    'NM-C1': [("            elif isinstance(c.get('declared_features'), dict):\n"
               "                decl = c['declared_features']\n"
               "            elif decl_key:\n",
               "            elif decl_key:\n")],
}

# probe -> (mutant ids, expected failing new-case names on that variant)
PROBES = [
    ('pristine+cases', [], ['red: a manifest-level tuple map is not the declared key']),
    ('M02+cases', ['M02'], ['red: the evaluator rotates the action on one whole class']),
    ('M03+cases', ['M03'], ['red: the evaluator rotates the label on one whole class']),
    ('M05+cases', ['M05'], ['red: tuples only under the legacy declared key stay a lookup failure']),
    ('M14+cases', ['M14'], ['red: seed shares the freeze prefix but differs']),
    ('M15+cases', ['M15'], ['red: the frozen generator stamps a drifted seed into the regenerated manifest']),
    ('M18+cases', ['M18'], []),
    ('M21+cases', ['M21'], ['frozen: a frozen path is deleted by a later commit']),
    ('M37+cases', ['M37'], ['red: two carriers share one id']),
    ('M46+cases', ['M46'], ['red: committed bytes match regeneration but the manifest pin points elsewhere']),
    ('M47+cases', ['M47'], ['red: a regenerated carrier ships the wrong arm']),
    ('NM-C1+cases', ['NM-C1'],
     ['green: tuples declared under the single key declared_features']),
]


def apply(src, patches):
    out = src
    for old, new in patches:
        n = out.count(old)
        assert n == 1, 'anchor x%d: %r' % (n, old[:70])
        out = out.replace(old, new)
    return out


def run_variant(name, mut_ids):
    src = open(SRC, encoding='utf-8').read()
    base_sha = hashlib.sha256(src.encode()).hexdigest()
    for mid in mut_ids:
        src = apply(src, MUTANTS[mid])
    src = apply(src, [(old, new) for _name, old, new in CASES])
    path = os.path.join(MUT, 'kc-%s.py' % name.replace('+', '-'))
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(src)
    env = dict(os.environ)
    env['HYAKU_SCRATCH'] = os.path.join(ROOT, 'hs')
    env['TMPDIR'] = os.path.join(ROOT, 'tmp')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    p = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                       capture_output=True, text=True, env=env, timeout=600)
    doc = None
    for line in p.stdout.splitlines():
        if line.startswith('{'):
            try:
                doc = json.loads(line)
            except ValueError:
                pass
    fails = [f for f in (doc or {}).get('failures', [])]
    failed_names = sorted({n for n in NEW_CASE_NAMES
                           for f in fails if f.startswith(n + ':') or f.startswith(n + ' ')})
    return {'probe': name, 'mutants': mut_ids, 'variant_sha256':
            hashlib.sha256(src.encode()).hexdigest(), 'base_sha256': base_sha,
            'exit': p.returncode, 'cases': (doc or {}).get('cases'),
            'pass': (doc or {}).get('pass'), 'fail': (doc or {}).get('fail'),
            'failures': fails[:12],
            'new_case_failures': failed_names,
            'stderr_tail': (p.stderr or '')[-200:]}


def main():
    os.makedirs(MUT, exist_ok=True)
    results = []
    for name, mut_ids, expect in PROBES:
        row = run_variant(name, mut_ids)
        row['expected_new_failures'] = sorted(expect)
        results.append(row)
        print('%-16s exit=%d pass=%s/%s new_fails=%s expected=%s'
              % (name, row['exit'], row['pass'], row['cases'],
                 row['new_case_failures'], row['expected_new_failures']))
        sys.stdout.flush()
    # a probe "matches" when it fails exactly its expected new cases on top of
    # the pristine-only failures (the v4-only manifest-level case)
    pristine_only = set(results[0]['new_case_failures'])
    for row in results:
        row['pristine_only_failures'] = sorted(pristine_only)
        row['match'] = (set(row['new_case_failures']) - pristine_only) \
            == set(row['expected_new_failures'])
        print('%-16s match=%s' % (row['probe'], row['match']))
    with open(os.path.join(OUT, 'killing-cases-counter.json'), 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    ok = all(r['match'] for r in results)
    print('DONE %d probes, all_match=%s' % (len(results), ok))


if __name__ == '__main__':
    main()
