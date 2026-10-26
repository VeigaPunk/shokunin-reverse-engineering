#!/usr/bin/env python3
"""R41C2Mutants phase 2a: add the survivor-killing selftest cases to a scratch
copy of the base c2-counter.py and show pristine passes all of them while each
mutant fails exactly its own case. Scratch-only."""
import hashlib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants'
BASE = open(S + '/c2-counter.base.py', encoding='utf-8').read()

F64 = 'f' * 64

PATCHES = [
    ('P1-stub-seed-override',
     "man = {'seed': a.seed,\n"
     "       'generator': {'name': 'heldout-gen-v2.py', 'version': 'r40-c2-stub',\n"
     "                     'sha256': hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()},\n"
     "       'classes': classes, 'carriers': out}",
     "SEEDX = '@@SEEDX@@'\n"
     "man = {'seed': (SEEDX if SEEDX else a.seed),\n"
     "       'generator': {'name': 'heldout-gen-v2.py', 'version': 'r40-c2-stub',\n"
     "                     'sha256': hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()},\n"
     "       'classes': classes, 'carriers': out}"),
    ('P2-build-materialises-override',
     "            INTERP: STUB_INTERP.replace('@@MODE@@', mode),\n            GEN: STUB_GEN,",
     "            INTERP: STUB_INTERP.replace('@@MODE@@', mode),\n"
     "            GEN: STUB_GEN.replace('@@SEEDX@@', params.get('regen_seed', '')),"),
    ('P3a-pin-swap-body',
     "            body = open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb').read()\n"
     "            if 'carrier_corrupt' in muts and cid == 'H01':\n"
     "                body += b'X'",
     "            body = open(os.path.join(gdir, cid, 'carrier.sqsh'), 'rb').read()\n"
     "            if 'carrier_corrupt' in muts and cid == 'H01':\n"
     "                body += b'X'\n"
     "            if 'pin_swap' in muts and cid == 'H01':\n"
     "                body = b'pin-swap-body'\n"
     "                c['sha256'] = hashlib.sha256(body).hexdigest()"),
    ('P3b-arm-flip-and-action-both',
     "            if 'mislabel' in muts and cid == 'H01':\n"
     "                entry['expected_label'] = 'dep-missing-be'",
     "            if 'mislabel' in muts and cid == 'H01':\n"
     "                entry['expected_label'] = 'dep-missing-be'\n"
     "            if 'arm_flip' in muts and cid == 'H01':\n"
     "                entry['arm'] = 'before'\n"
     "            if 'wrong_action_both' in muts and cid in ('H03', 'H04'):\n"
     "                entry['expected_action'] = 'install-extractor'"),
    ('P4a-claim-commit-restores-frozen-bytes',
     "        if claim == 'after':\n            tree = dict(claim_files)\n            tree[MANIFEST] = man_text\n            tree.update(post)\n            rev = commit(d, tree, 'claim data')",
     "        if claim == 'after':\n            tree = dict(claim_files)\n            tree[MANIFEST] = man_text\n            tree.update(post)\n"
     "            if params.get('frozen_restore'):\n"
     "                tree[params['frozen_restore']] = tool_tree[params['frozen_restore']]\n"
     "            rev = commit(d, tree, 'claim data')"),
    ('P4b-frozen-restore-edit-commit',
     "        if claim == 'after':\n            tree = dict(claim_files)\n            tree[MANIFEST] = man_text",
     "        if params.get('frozen_restore'):\n"
     "            fr = params['frozen_restore']\n"
     "            commit(d, {fr: tool_tree[fr] + '\\n# edited mid-range\\n'},\n"
     "                   'edit frozen path mid-range')\n"
     "        if claim == 'after':\n            tree = dict(claim_files)\n            tree[MANIFEST] = man_text"),
    ('P5a-case-tuple-unpack',
     "    for name, params, want, want_false, want_true, extra in cases:",
     "    for case_i in cases:\n"
     "        name, params, want, want_false, want_true, extra = case_i[:6]\n"
     "        want_matched = case_i[6] if len(case_i) > 6 else None"),
    ('P5b-want-matched-check',
     "                    if got == 0 and rec.get('distinct_decisions') != len(\n"
     "                            set(r.get('row') for r in rec.get('carriers', []))):\n"
     "                        ok = False\n"
     "                        fails.append('%s: distinct_decisions mismatch' % name)",
     "                    if got == 0 and rec.get('distinct_decisions') != len(\n"
     "                            set(r.get('row') for r in rec.get('carriers', []))):\n"
     "                        ok = False\n"
     "                        fails.append('%s: distinct_decisions mismatch' % name)\n"
     "                    if want_matched is not None and rec.get('matched') != want_matched:\n"
     "                        ok = False\n"
     "                        fails.append('%s: matched %r != expected %d'\n"
     "                                     % (name, rec.get('matched'), want_matched))"),
    ('P6-new-cases',
     "        ('explicit --base equal to derived base', dict(), 0, [], ['v1_table_identical'], ('BASE',)),\n    ]",
     "        ('explicit --base equal to derived base', dict(), 0, [], ['v1_table_identical'], ('BASE',)),\n"
     "        ('regenerated manifest seed is foreign', dict(regen_seed='0' * 64), 1,\n"
     "         ['regenerated_seed_matches_freeze'], [], ()),\n"
     "        ('committed carrier and pin tampered together', dict(muts={'pin_swap'}), 1,\n"
     "         ['carriers_regenerated'], [], ()),\n"
     "        ('manifest arm flipped against regeneration', dict(muts={'arm_flip'}), 1,\n"
     "         ['carriers_regenerated'], [], ()),\n"
     "        ('wrong expected action on both carriers of one class',\n"
     "         dict(muts={'wrong_action_both'}), 1, [], [], (), 6),\n"
     "        ('declared writer sha does not match the freeze blob',\n"
     "         dict(gen_obj='good',\n"
     "              writer_decl='{\"path\": \"tools/round-39/gen-squashfs.py\", \"sha256\": \"'\n"
     "                          + '" + F64 + "' + '\"}'),\n"
     "         1, ['writer_matches_manifest'], [], ()),\n"
     "        ('frozen path edited then restored before rev', dict(frozen_restore=GEN), 2,\n"
     "         [], [], ()),\n    ]"),
    ('P7-gen-obj-hash-of-materialised',
     "                'sha256': hashlib.sha256(STUB_GEN.encode()).hexdigest()\n"
     "                if params.get('gen_obj') == 'good' else 'f' * 64,",
     "                'sha256': hashlib.sha256(\n"
     "                    STUB_GEN.replace('@@SEEDX@@', '').encode()).hexdigest()\n"
     "                if params.get('gen_obj') == 'good' else 'f' * 64,"),
    ('P8-writer-decl-in-manifest',
     "                'carriers_per_class': 2}",
     "                'carriers_per_class': 2}\n"
     "            if params.get('writer_decl'):\n"
     "                man['generator']['writer'] = json.loads(params['writer_decl'])"),
    ('P9-case-debug',
     "            pr, rec = run_counter(d, rev, freeze, extra_args)\n            got = pr.returncode",
     "            pr, rec = run_counter(d, rev, freeze, extra_args)\n"
     "            if os.environ.get('C2CASE_DEBUG'):\n"
     "                print('CASE %-55s exit=%s bindings_false=%s matched=%s'\n"
     "                      % (name[:55], got, (rec or {}).get('bindings_false'),\n"
     "                         (rec or {}).get('matched')), file=sys.stderr)\n"
     "            got = pr.returncode"),
]

MUTANTS = [
    ('M02-regen-seed-vacuated',
     "        b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze",
     "        b['regenerated_seed_matches_freeze'] = True",
     'regenerated manifest seed is foreign'),
    ('M03-regen-digest-dropped',
     '            regen_ok = bool(regen_sha) and regen_sha == msha \\',
     '            regen_ok = bool(regen_sha) and True \\',
     'committed carrier and pin tampered together'),
    ('M04-regen-arm-dropped',
     "                and r.get('class') == c.get('class') and r.get('arm') == c.get('arm') \\",
     "                and r.get('class') == c.get('class') \\",
     'manifest arm flipped against regeneration'),
    ('M11-pair-match-label-only',
     "                row['pair_match'] = (row['label'] == row['expected_label']\n"
     "                                     and row['action'] == row['expected_action'])",
     "                row['pair_match'] = (row['label'] == row['expected_label'])",
     'wrong expected action on both carriers of one class'),
    ('M19-writer-sha-vacuated',
     "        b['writer_matches_manifest'] = declared_w_sha is None or declared_w_sha == w_sha",
     "        b['writer_matches_manifest'] = True",
     'declared writer sha does not match the freeze blob'),
    ('N01-frozen-scan-tip-only',
     "    p = subprocess.run(['git', '-C', root, 'log', '--format=%H', '--no-renames',\n"
     "                        '%s..%s' % (freeze, rev), '--', *FROZEN],\n"
     "                       capture_output=True, text=True)",
     "    p = subprocess.run(['git', '-C', root, 'diff', '--name-only',\n"
     "                        freeze, rev, '--', *FROZEN],\n"
     "                       capture_output=True, text=True)",
     'frozen path edited then restored before rev'),
]


def selftest(path):
    env = dict(os.environ)
    p = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                       capture_output=True, text=True, timeout=2400, env=env)
    doc = None
    for line in p.stdout.splitlines():
        if line.strip().startswith('{'):
            try:
                doc = json.loads(line)
            except Exception:
                pass
    return {'exit': p.returncode, 'doc': doc, 'stderr_tail': (p.stderr or '')[-400:]}


def main():
    src = BASE
    for pid, old, new in PATCHES:
        n = src.count(old)
        if n != 1:
            raise SystemExit('%s: anchor count %d' % (pid, n))
        src = src.replace(old, new)
    cased = S + '/counter-cased.py'
    open(cased, 'w').write(src)
    print('patched pristine selftest ...', flush=True)
    pris = selftest(cased)
    print(json.dumps(pris['doc']), flush=True)
    env = dict(os.environ, C2CASE_DEBUG='1')
    p = subprocess.run([sys.executable, '-I', '-B', cased, '--selftest'],
                       capture_output=True, text=True, timeout=2400, env=env)
    open(S + '/counter-cased-pristine-debug.err', 'w').write(p.stderr)
    results = {'pristine': pris}
    os.makedirs(S + '/cased-mutants', exist_ok=True)
    for mid, old, new, case_name in MUTANTS:
        n = src.count(old)
        if n != 1:
            raise SystemExit('%s: anchor count %d' % (mid, n))
        mpath = S + '/cased-mutants/cased-%s.py' % mid
        open(mpath, 'w').write(src.replace(old, new))
        print('cased mutant %s ...' % mid, flush=True)
        r = selftest(mpath)
        fails = (r['doc'] or {}).get('failures', [])
        killed = r['exit'] != 0 and any(case_name in f for f in fails)
        results[mid] = {'path': mpath, 'mutant_sha256':
                        hashlib.sha256(open(mpath, 'rb').read()).hexdigest(),
                        'selftest': r, 'target_case': case_name,
                        'fails_on_target_case': any(case_name in f for f in fails),
                        'n_fail': len(fails), 'verdict': 'KILLED' if killed else
                        ('killed-other' if r['exit'] != 0 else 'SURVIVED')}
        print('%s -> %s fail=%d %s' % (mid, results[mid]['verdict'], len(fails),
                                       fails[:2]), flush=True)
    with open(S + '/counter-case-results.json', 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    print('WROTE counter-case-results.json', flush=True)


if __name__ == '__main__':
    main()
