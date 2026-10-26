#!/usr/bin/env python3
"""mutdrive.py -- seat R41W2C2InterpMut mutation sweep (round 41 wave 2).

Tools under test (pristine copies in $S/pristine, sha256-recorded):
  sqfs-triage-v3.py   the frozen C2 interpreter (reads the SKILL v3 table)
  indep-eval-v3.py    the frozen C2 independent evaluator (precedence branches)

Kill check per mutant, exactly as tasked:
  1. the tool's own --selftest must still pass; and
  2. the (label, action) pairs over the 52 held-out envelopes
     (corpus/evidence/round-41/c2/heldout/<ID>/envelope.json, fed the same way
     c2-counter.py feeds them: interpreter gets the envelope paths, evaluator a
     flat directory of the same bytes) must equal the pristine baseline.
Killed if either check fails; survived otherwise.  Every mutant is a minimal
exact-string edit of the pristine source; anchors are asserted unique.
"""
import difflib
import json
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/kaidoku-r41/R41W2C2InterpMut'
PRIM = os.path.join(S, 'pristine')
ENV = os.path.join(S, 'env')
FLAT = os.path.join(S, 'evalenv')
OUT = os.path.join(S, 'out')
MUT = os.path.join(S, 'mut')
INTERP = 'sqfs-triage-v3.py'
EVAL = 'indep-eval-v3.py'


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def interp_pairs(exe):
    paths = [os.path.join(ENV, f) for f in sorted(os.listdir(ENV))]
    r = run([sys.executable, '-I', '-B', exe, '--skill',
             os.path.join(PRIM, 'SKILL.md'), *paths])
    if r.returncode != 0:
        return None, r
    pairs = {}
    for line in r.stdout.splitlines():
        if not line.strip():
            continue
        path, label, action = line.split('\t')
        cid = os.path.splitext(os.path.basename(path))[0]
        pairs[cid] = [label, action]
    return pairs, r


def eval_pairs(exe):
    r = run([sys.executable, '-I', '-B', exe, '--envelopes', FLAT])
    if r.returncode != 0:
        return None, r
    try:
        doc = json.loads(r.stdout)
    except ValueError:
        return None, r
    return {cid: [v['label'], v['action']]
            for cid, v in doc['labels'].items()}, r


def selftest(exe, tool):
    r = run([sys.executable, '-I', '-B', exe, '--selftest'])
    first_fail = None
    if tool == INTERP:
        for line in r.stdout.splitlines():
            if line.startswith('FAIL '):
                first_fail = line.split(':')[0][5:]
                break
        if first_fail is None and r.returncode != 0:
            first_fail = 'selftest-exit-%d' % r.returncode
    else:
        try:
            doc = json.loads(r.stdout)
            fails = doc.get('failures') or []
            if fails:
                first_fail = str(fails[0]).split(':')[0]
        except ValueError:
            first_fail = 'selftest-output-unparsable'
    return r.returncode, first_fail, r


# ---------------------------------------------------------------------------
# mutant specifications: minimal exact-string edits, each anchor asserted unique
# ---------------------------------------------------------------------------
MUTANTS = [
    # ---------------- sqfs-triage-v3.py (interpreter) ----------------
    dict(id='I01', tool=INTERP, axis='contains-form',
         edits=[("    if kind == 'contains':\n        return payload <= frozenset(values)",
                 "    if kind == 'contains':\n        return payload == frozenset(values)")],
         expect='selftest c_contains_single_matches_superset; pairs H27/H28 partial-in-tree'),
    dict(id='I02', tool=INTERP, axis='exact-vs-contains',
         edits=[("    return frozenset(values) == payload",
                 "    return payload <= frozenset(values)")],
         expect='selftest c_exact_single_rejects_superset; pairs need a superset D/G at an exact row'),
    dict(id='I03', tool=INTERP, axis='contains-form',
         edits=[("        return payload <= frozenset(values)",
                 "        return frozenset(values) <= payload")],
         expect='selftest c_contains_single_matches_superset; pairs H27/H28'),
    dict(id='I04', tool=INTERP, axis='contains-form',
         edits=[("    if contains and cell.endswith('+'):", "    if contains:")],
         expect='selftest c_exact_single_matches_singleton; pairs H09/H10 in-tree row misparse'),
    dict(id='I05', tool=INTERP, axis='contains-form',
         edits=[("        parts = body.split(',')", "        parts = body.split('+')")],
         expect='selftest c_contains_pair_matches; pairs: real SKILL table fails to parse'),
    dict(id='I06', tool=INTERP, axis='be-token',
         edits=[("            if '-be' in (command_tokens(cmd) or []):",
                 "            if '-be' in str(cmd):")],
         expect='selftest c_be_token_not_substring (-be=1 token)'),
    dict(id='I07', tool=INTERP, axis='be-token',
         edits=[("                be = 'yes'", "                pass")],
         expect='pairs H19/H20 body-extractor-failure(be=yes) -> avm-marker-be-dropped'),
    dict(id='I08', tool=INTERP, axis='sr-detection',
         edits=[("        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:",
                 "        if isinstance(report, dict) and report.get('type') == SYMLINK_TYPENAME:")],
         expect='pairs H07/H08/H11/H12 (SR carried as report.__typename__)'),
    dict(id='I09', tool=INTERP, axis='sr-detection',
         edits=[("    if symlink == 'no':\n        for found in _iter_dicts(data.get('raw_result')):\n            if found.get('__typename__') == SYMLINK_TYPENAME:\n                symlink = 'yes'\n                break",
                 "    if symlink == 'no':\n        pass")],
         expect='selftest c_sr_from_raw_result'),
    dict(id='I10', tool=INTERP, axis='p-counting',
         edits=[("        'P': len(_as_list(nr.get('files'))),",
                 "        'P': 1 if _as_list(nr.get('files')) else 0,")],
         expect='SURVIVOR prediction: table grammar only distinguishes 0 vs >0'),
    dict(id='I11', tool=INTERP, axis='p-counting',
         edits=[("        'P': len(_as_list(nr.get('files'))),",
                 "        'P': len(nr['files']) if isinstance(nr.get('files'), list) else 1,")],
         expect='SURVIVOR prediction: only out-of-domain envelopes lack files; no interpreter selftest case'),
    dict(id='I12', tool=INTERP, axis='step-order',
         edits=[("    for rule in rules:\n        if rule_matches(rule, feat):",
                 "    for rule in reversed(rules):\n        if rule_matches(rule, feat):")],
         expect='pairs H39/H40/C02/C06/C10 (partial row before depth row); selftest c_first_match_order'),
    dict(id='I14', tool=INTERP, axis='handler-set',
         edits=[("        if isinstance(handler, str) and handler.startswith('squashfs'):",
                 "        if isinstance(handler, str) and handler:")],
         expect='SURVIVOR prediction: every held-out chunk handler is squashfs_* or absent'),
    dict(id='I15', tool=INTERP, axis='p-counting',
         edits=[("    if files == '>0' and feat['P'] <= 0:",
                 "    if files == '>0' and feat['P'] < 0:")],
         expect='pairs H05/H06 clean-empty (P=0) -> clean row'),
    dict(id='I16', tool=INTERP, axis='contains-form',
         edits=[("            if part in RESERVED_MEMBERS:\n                raise TableError('%s cell %r uses the reserved word %r as a contains '",
                 "            if False and part in RESERVED_MEMBERS:\n                raise TableError('%s cell %r uses the reserved word %r as a contains '")],
         expect='selftest c_reserved_word_as_contains_member'),
    dict(id='I17', tool=INTERP, axis='contains-form',
         edits=[("        if len(set(parts)) != len(parts):\n            raise TableError('%s cell %r repeats a contains member' % (column, cell))",
                 "        if False:\n            raise TableError('%s cell %r repeats a contains member' % (column, cell))")],
         expect='selftest c_malformed_contains_duplicate'),
    dict(id='I18', tool=INTERP, axis='contains-form',
         edits=[("        for part in parts:\n            if not name_re.match(part):\n                raise TableError('%s cell %r has a malformed contains member %r'",
                 "        for part in parts:\n            if False and not name_re.match(part):\n                raise TableError('%s cell %r has a malformed contains member %r'")],
         expect='selftest c_malformed_contains_space'),
    dict(id='I18b', tool=INTERP, axis='exact-vs-contains',
         edits=[("    for part in parts:\n        if not name_re.match(part):\n            raise TableError('%s cell %r has a malformed member %r' % (column, cell, part))",
                 "    for part in parts:\n        if False and not name_re.match(part):\n            raise TableError('%s cell %r has a malformed member %r' % (column, cell, part))")],
         expect='selftest c_malformed_contains_space (exact branch)'),
    dict(id='I19', tool=INTERP, axis='be-token',
         edits=[("    if not commands:\n        be = 'n/a'", "    if not commands:\n        be = 'no'")],
         expect='selftest c_be_values; pairs need ef+P0+no-argv+be-handler envelope'),
    dict(id='I20', tool=INTERP, axis='domain-guard',
         edits=[("    if rule['provider'] != '*' and rule['provider'] != feat['PV']:", "    if False:")],
         expect='selftest c_domain_guard_provider; held-out out-of-domain deviates on op too'),

    # ---------------- indep-eval-v3.py (evaluator) ----------------
    dict(id='E01', tool=EVAL, axis='be-token',
         edits=[('    has = "-be" in tokens',
                 '    has = any("-be" in t for t in tokens)')],
         expect='SURVIVOR prediction: no -be-substring token in held-out argvs; evaluator selftest lacks the trap'),
    dict(id='E02', tool=EVAL, axis='be-token',
         edits=[('        return "n/a", "no diagnostics[].report.command recorded"',
                 '        return "no", "no diagnostics[].report.command recorded"')],
         expect='selftest s5-boundary-no-argv; pairs need ef+P0+no-argv+be-handler envelope'),
    dict(id='E03', tool=EVAL, axis='sr-detection',
         edits=[('TYPENAME_KEYS = ("__typename__", "type", "kind", "name")',
                 'TYPENAME_KEYS = ("type",)')],
         expect='selftest s8-mixed/s9-escaping; pairs H07/H08/H11/H12'),
    dict(id='E04', tool=EVAL, axis='sr-detection',
         edits=[('    if REMOVED_SYMLINK_TYPENAME in stdout:',
                 '    if False and REMOVED_SYMLINK_TYPENAME in stdout:')],
         expect='SURVIVOR prediction: no stdout-only SR case in selftest or held-out'),
    dict(id='E05', tool=EVAL, axis='sr-detection',
         edits=[('    for diag in nr.get("diagnostics") or []:\n        for holder in (diag, diag.get("report") if isinstance(diag.get("report"), dict) else None):\n            if not isinstance(holder, dict):\n                continue\n            for key in TYPENAME_KEYS:',
                 '    for diag in nr.get("diagnostics") or []:\n        for holder in (diag.get("report") if isinstance(diag.get("report"), dict) else None,):\n            if not isinstance(holder, dict):\n                continue\n            for key in TYPENAME_KEYS:')],
         expect='SURVIVOR prediction: real and synthetic envelopes nest the report'),
    dict(id='E06', tool=EVAL, axis='p-counting',
         edits=[('    p = len(files) if isinstance(files, list) else 0',
                 '    p = len(files) if isinstance(files, list) else 1')],
         expect='selftest b-files-absent-reads-as-p-zero; held-out files-absent envelopes are out-of-domain'),
    dict(id='E07', tool=EVAL, axis='p-counting',
         edits=[('    p = len(files) if isinstance(files, list) else 0',
                 '    p = 1 if isinstance(files, list) and files else 0')],
         expect='SURVIVOR prediction: pair oracle blind to P magnitude'),
    dict(id='E08', tool=EVAL, axis='step-order',
         edits=[('    if "missing-extractor-dependency" in g:\n        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)\n        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)\n        # neither name present: step 3 states no outcome; fall through.\n    # 4\n    if "extractor-failure" in g and p > 0:\n        return _done("partial-body-failure", 4)',
                 '    # 4\n    if "extractor-failure" in g and p > 0:\n        return _done("partial-body-failure", 4)\n    if "missing-extractor-dependency" in g:\n        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)\n        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)\n        # neither name present: step 3 states no outcome; fall through.')],
         expect='SURVIVOR prediction: no dep+failure envelope in held-out or selftest'),
    dict(id='E09', tool=EVAL, axis='step-order',
         edits=[('    # 4\n    if "extractor-failure" in g and p > 0:',
                 '    # 4\n    if "depth-limited" in g:\n        return _done("depth-limited", 7)\n    if "extractor-failure" in g and p > 0:'),
                ('    # 7\n    if "depth-limited" in g:\n        return _done("depth-limited", 7)',
                 '    # 7')],
         expect='selftest s7-partial-precedes-depth; pairs H39/H40/C02/C06/C10'),
    dict(id='E11', tool=EVAL, axis='contains-form',
         edits=[('    if g == {"unpublished-entry"}:',
                 '    if "unpublished-entry" in g:')],
         expect='selftest s10-boundary-singleton-not-met; pairs never reach step 10 with extra kinds'),
    dict(id='E12', tool=EVAL, axis='step-order',
         edits=[('    if sr and "unpublished-entry" in g:',
                 '    if sr or "unpublished-entry" in g:')],
         expect='selftest s9-escaping; pairs H07/H08/H09/H10'),
    dict(id='E13', tool=EVAL, axis='step-order',
         edits=[('        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)\n        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)',
                 '        if LE_DEPENDENCY in d:\n            return _done("dep-missing-le", 3)\n        if BE_DEPENDENCY in d:\n            return _done("dep-missing-be", 3)')],
         expect='selftest s3-dep-both-be-first; pairs need a both-dependencies envelope'),
    dict(id='E13b', tool=EVAL, axis='exact-vs-contains',
         edits=[('        if BE_DEPENDENCY in d:',
                 '        if any(LE_DEPENDENCY in x for x in d):'),
                ('        if LE_DEPENDENCY in d:',
                 '        if any(BE_DEPENDENCY in x for x in d):'),
                ('        if any(LE_DEPENDENCY in x for x in d):\n            return _done("dep-missing-be", 3)',
                 '        if any(LE_DEPENDENCY in x for x in d):\n            return _done("dep-missing-le", 3)'),
                ('        if any(BE_DEPENDENCY in x for x in d):\n            return _done("dep-missing-le", 3)',
                 '        if any(BE_DEPENDENCY in x for x in d):\n            return _done("dep-missing-be", 3)')],
         expect='substring dependency match with LE checked first; pairs H13/H14 dep-missing-be'),
    dict(id='E14', tool=EVAL, axis='handler-set',
         edits=[('SQUASHFS_HANDLER_PREFIX = "squashfs_v4_"',
                 'SQUASHFS_HANDLER_PREFIX = "squashfs_v4_be"')],
         expect='selftest s2-le-handler-is-a-squashfs-handler; pairs 19 le envelopes'),
    dict(id='E15', tool=EVAL, axis='step-order',
         edits=[('    step5_handlers = set(feats.get("HF") or []) or h',
                 '    step5_handlers = set(feats.get("HF") or [])')],
         expect='selftest s5-avm-marker-be-dropped (gap handler null); held-out avm envelopes record the gap handler'),
    dict(id='E16', tool=EVAL, axis='domain-guard',
         edits=[('    if op != "extract_firmware" or pr != "unblob":',
                 '    if op != "extract_firmware":')],
         expect='selftest s1-pr-binwalk; held-out out-of-domain deviates on op too'),
    dict(id='E18', tool=EVAL, axis='sr-detection',
         edits=[('    sr = (feats.get("SR") == "yes") or feats.get("SR") is True',
                 '    sr = feats.get("SR") == "yes"')],
         expect='selftest s8-mixed; pairs H07/H08/H11/H12 (features carry SR as bool)'),
    dict(id='E19', tool=EVAL, axis='p-counting',
         edits=[('    if "extractor-failure" in g and p > 0:',
                 '    if "extractor-failure" in g and p >= 0:')],
         expect='selftest s5-avm-marker-be-dropped; pairs H17-H20'),
    dict(id='E20', tool=EVAL, axis='step-order',
         edits=[('        return _done("clean" if p > 0 else "clean-empty", 11)',
                 '        return _done("clean" if p == 0 else "clean-empty", 11)')],
         expect='selftest s11-clean/s11-clean-empty; pairs H01-H06'),
    dict(id='E21', tool=EVAL, axis='step-order',
         edits=[('    # 2\n    if not squashfs:\n        return _done("no-squashfs-chunk", 2)',
                 ''),
                ('    # 12\n    return _done("unclassified", 12)',
                 '    # 2 (moved last by mutant E21)\n    if not squashfs:\n        return _done("no-squashfs-chunk", 2)\n    # 12\n    return _done("unclassified", 12)')],
         expect='selftest s3-dep-in-gap-only-handler; pairs H23/H24 -> clean-empty'),
    dict(id='E22', tool=EVAL, axis='be-token',
         edits=[('            for key in ("command", "argv", "args"):',
                 '            for key in ("argv", "args"):')],
         expect='selftest s5-avm-marker-be-dropped; pairs H17/H18 (REA records report.command)'),
]


def apply_mutant(spec):
    src = open(os.path.join(PRIM, spec['tool']), encoding='utf-8').read()
    for old, new in spec['edits']:
        n = src.count(old)
        if n != 1:
            raise RuntimeError('%s: anchor count %d for %r' % (spec['id'], n, old[:60]))
        src = src.replace(old, new)
    dst = os.path.join(MUT, '%s-%s' % (spec['tool'], spec['id']))
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(src)
    return dst


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(MUT, exist_ok=True)
    # flat evaluator input: same envelope.json bytes the interpreter gets
    for f in sorted(os.listdir(ENV)):
        with open(os.path.join(ENV, f), 'rb') as fh:
            data = fh.read()
        with open(os.path.join(FLAT, f), 'wb') as fh:
            fh.write(data)

    ib, ir = interp_pairs(os.path.join(PRIM, INTERP))
    eb, er = eval_pairs(os.path.join(PRIM, EVAL))
    assert ib is not None and len(ib) == 52, 'interpreter baseline broken'
    assert eb is not None and len(eb) == 52, 'evaluator baseline broken'
    agree = sorted(k for k in ib if ib[k] == eb.get(k))
    disagree = sorted(k for k in set(ib) | set(eb) if ib.get(k) != eb.get(k))
    results = {'baseline': {'cross_agreement': len(agree), 'cross_disagree': disagree},
               'mutants': []}
    print('baseline: interp %d pairs, eval %d pairs, cross-agreement %d/52, disagree %s'
          % (len(ib), len(eb), len(agree), disagree))

    for spec in MUTANTS:
        row = {'id': spec['id'], 'tool': spec['tool'], 'axis': spec['axis'],
               'expect': spec['expect']}
        try:
            dst = apply_mutant(spec)
        except RuntimeError as exc:
            row['verdict'] = 'ANCHOR-ERROR'
            row['error'] = str(exc)
            results['mutants'].append(row)
            print('%-5s ANCHOR-ERROR %s' % (spec['id'], exc))
            continue
        with open(os.path.join(PRIM, spec['tool']), encoding='utf-8') as fh:
            pristine_src = fh.read()
        with open(dst, encoding='utf-8') as fh:
            mutant_src = fh.read()
        diff = '\n'.join(difflib.unified_diff(
            pristine_src.splitlines(), mutant_src.splitlines(),
            fromfile='pristine/' + spec['tool'], tofile='mutant/' + spec['id'], lineterm=''))
        with open(os.path.join(MUT, 'diff-%s.diff' % spec['id']), 'w') as fh:
            fh.write(diff + '\n')
        row['mutant_path'] = dst
        st_exit, st_fail, st_r = selftest(dst, spec['tool'])
        row['selftest_exit'] = st_exit
        row['selftest_first_failure'] = st_fail
        if st_exit != 0:
            row['verdict'] = 'KILLED-SELFTEST'
            row['selftest_tail'] = (st_r.stdout + st_r.stderr)[-400:]
        else:
            pairs, r = (interp_pairs(dst) if spec['tool'] == INTERP else eval_pairs(dst))
            base = ib if spec['tool'] == INTERP else eb
            if pairs is None:
                row['verdict'] = 'KILLED-PAIRS'
                row['pairs_exit'] = r.returncode
                row['stderr_tail'] = (r.stderr or '')[-300:]
                row['changed'] = 'ALL (tool failed, exit %d)' % r.returncode
            else:
                changed = sorted(k for k in set(base) | set(pairs)
                                 if base.get(k) != pairs.get(k))
                row['pairs_exit'] = r.returncode
                row['n_changed'] = len(changed)
                if changed:
                    row['verdict'] = 'KILLED-PAIRS'
                    row['changed'] = {k: {'baseline': base.get(k),
                                          'mutant': pairs.get(k)} for k in changed}
                else:
                    row['verdict'] = 'SURVIVED'
        results['mutants'].append(row)
        print('%-5s %-6s %-18s selftest=%s%s' % (
            spec['id'], row['verdict'], spec['axis'], st_exit,
            (' first_fail=%s' % st_fail) if st_fail else ''))
        if row['verdict'] == 'KILLED-PAIRS' and isinstance(row.get('changed'), dict):
            print('      changed: %s' % ', '.join('%s:%s->%s' % (k, v['baseline'], v['mutant'])
                                                  for k, v in list(row['changed'].items())[:8]))

    with open(os.path.join(OUT, 'mutants-results.json'), 'w') as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    killed = sum(1 for m in results['mutants'] if m['verdict'].startswith('KILLED'))
    surv = sum(1 for m in results['mutants'] if m['verdict'] == 'SURVIVED')
    print('TOTAL %d mutants: %d killed, %d survived'
          % (len(results['mutants']), killed, surv))
    return 0


if __name__ == '__main__':
    sys.exit(main())
