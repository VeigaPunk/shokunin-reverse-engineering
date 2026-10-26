#!/usr/bin/env python3
"""R40MutR39 mutation harness. Mutants are (old -> new) single-logic edits applied
to scratch copies of the frozen round-39 tools. Detectors per tool:
  sqfs-triage.py : --selftest (35 cases) + label 20 held-out envelopes vs manifest
  c2-counter.py  : --selftest (27 cases) + verdict at REV=8b9634ed FREEZE=8fcda41c
  c1-counter.py  : --selftest (33 cases) + verdict at same revs (pkg65 rea-agents)
"""
import hashlib, json, os, shutil, subprocess, sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
P65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
REV = '8b9634ed8253653e7eb994aad9860a624e3b0366'
FREEZE = '8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b'
MIRROR = os.path.join(S, 'mirror', 'tools', 'round-39')

SHA = {'sqfs-triage.py': 'ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2',
       'c2-counter.py': '775766d86de0f1adbb2b7836664bc5641f92c0493bf0aa012b176ce03e7f0e41',
       'c1-counter.py': 'efb4b52658b6ccfaebe68516ce2a80794b38ff041a81f464c073974853577a91'}

# (id, tool, old, new, clause, provenance)  provenance: R39W2 survivor id or NEW
MUTANTS = [
 # ---- sqfs-triage.py: round-39 wave-2 survivors (18)
 ('T01', 'sqfs-triage.py', "handler.startswith('squashfs')", "handler.startswith('squash')", 'handler filter precision', 'R39 H-prefix-squash'),
 ('T02', 'sqfs-triage.py', "and handler.startswith('squashfs')", "", 'handler filter dropped', 'R39 H-no-filter'),
 ('T03', 'sqfs-triage.py', "handler.startswith('squashfs')", "handler.lower().startswith('squashfs')", 'handler filter case', 'R39 H-lower'),
 ('T04', 'sqfs-triage.py', "        kind = gap.get('kind')\n        if isinstance(kind, str):\n            gap_kinds.add(kind)", "        kind = gap.get('kind')\n        gap_kinds.add(kind)", 'gap kind str-guard', 'R39 G-nonstr-included'),
 ('T05', 'sqfs-triage.py', "            if isinstance(dep, str):\n                dependencies.add(dep)", "            dependencies.add(dep)", 'dependency str-guard', 'R39 D-nonstr-included'),
 ('T06', 'sqfs-triage.py', "        for cmd in commands:\n            if '-be' in", "        for cmd in commands[:1]:\n            if '-be' in", 'BE aggregation first-only', 'R39 BE-first-cmd-only'),
 ('T07', 'sqfs-triage.py', "        be = 'no'\n        for cmd in commands:\n            if '-be' in (command_tokens(cmd) or []):\n                be = 'yes'\n                break", "        be = 'yes'\n        for cmd in commands:\n            if '-be' not in (command_tokens(cmd) or []):\n                be = 'no'\n                break", 'BE aggregation any->all', 'R39 BE-any-to-all'),
 ('T08', 'sqfs-triage.py', " and cmd not in commands:", ":", 'command dedup dropped', 'R39 CMD-dedup-drop'),
 ('T09', 'sqfs-triage.py', "startswith('sasquatch'):", "startswith('sasquatch-v4be'):", 'sasquatch name set', 'R39 SQ-v4be-only'),
 ('T10', 'sqfs-triage.py', "if token.rsplit('/', 1)[-1].startswith('sasquatch'):", "if 'sasquatch' in token:", 'sasquatch substring', 'R39 SQ-substring'),
 ('T11', 'sqfs-triage.py', "if token.rsplit('/', 1)[-1].startswith('sasquatch'):", "if token.startswith('sasquatch'):", 'sasquatch basename strip', 'R39 SQ-no-basename'),
 ('T12', 'sqfs-triage.py', "    for diag in _as_list(nr.get('diagnostics')):\n        report = diag.get('report') if isinstance(diag, dict) else None\n        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:\n            symlink = 'yes'\n            break", "    for diag in []:\n        report = diag.get('report') if isinstance(diag, dict) else None\n        if isinstance(report, dict) and report.get('__typename__') == SYMLINK_TYPENAME:\n            symlink = 'yes'\n            break", 'SR diagnostics site dropped', 'R39 SR-raw-only'),
 ('T13', 'sqfs-triage.py', "__typename__') == SYMLINK_TYPENAME", "__typename__', '').__contains__(SYMLINK_TYPENAME)", 'SR typename substring', 'R39 SR-substring'),
 ('T14', 'sqfs-triage.py', "'P': len(_as_list(nr.get('files'))),", "'P': bool(_as_list(nr.get('files'))),", 'P granularity bool', 'R39 P-bool'),
 ('T15', 'sqfs-triage.py', "'P': len(_as_list(nr.get('files'))),", "'P': len(_as_list(nr.get('files'))) + len(_as_list(nr.get('unpublished_entries'))),", 'P includes unpublished', 'R39 P-plus-unpublished'),
 ('T16', 'sqfs-triage.py', 'fnmatch.fnmatchcase(value, payload)', 'fnmatch.fnmatch(value, payload)', 'fnmatch case sensitivity', 'R39 RM-fnmatch-nocase'),
 ('T17', 'sqfs-triage.py', "if files == '>0' and feat['P'] <= 0:", "if files == '>0' and feat['P'] < 0:", 'files >0 boundary', 'R39 RM-gt0-loose'),
 ('T18', 'sqfs-triage.py', "if files == '0' and feat['P'] != 0:", "if files == '0' and feat['P'] < 0:", 'files 0 boundary', 'R39 RM-zero-loose'),
 # ---- sqfs-triage.py: new, clauses round-40 keeps
 ('N-T1', 'sqfs-triage.py', "            gap_kinds.add(kind)", "            gap_kinds.add(kind.lower())", 'gap kind case-normalised', 'NEW gap clause'),
 ('N-T2', 'sqfs-triage.py', "    if kind == 'none':\n        return not values", "    if kind == 'none':\n        return True", 'set none-cell becomes any', 'NEW set equality'),
 ('N-T3', 'sqfs-triage.py', '    return frozenset(values) == payload', '    return bool(frozenset(values) & payload)', 'exact set -> nonempty intersection', 'NEW set equality'),
 ('N-T4', 'sqfs-triage.py', '        if not any(fnmatch.fnmatchcase(value, payload) for value in feat[\'H\']):', '        if not all(fnmatch.fnmatchcase(value, payload) for value in feat[\'H\']):', 'handler pattern any->all', 'NEW handler'),
 ('N-T5', 'sqfs-triage.py', 'def classify(rules, feat):\n    for rule in rules:\n        if rule_matches(rule, feat):\n            return rule\n    return None', 'def classify(rules, feat):\n    hits = [rule for rule in rules if rule_matches(rule, feat)]\n    return hits[-1] if hits else None', 'first-match order -> last-match', 'NEW first-match order'),
 # ---- c2-counter.py: round-39 wave-2 survivors (14)
 ('M01', 'c2-counter.py', "b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze", "b['seed_matches_freeze'] = str(man.get('seed', '')) == freeze", 'seed case-normalisation', 'R39 m01'),
 ('M03', 'c2-counter.py', "b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == freeze", "b['regenerated_seed_matches_freeze'] = str(rman.get('seed', '')).lower() == str(man.get('seed', '')).lower()", 'regen seed vs declared', 'R39 m03'),
 ('M04', 'c2-counter.py', " and r.get('label') == c.get('label')", "", 'regen label conjunct', 'R39 m04'),
 ('M05', 'c2-counter.py', " and r.get('arm') == c.get('arm')", "", 'regen arm conjunct', 'R39 m05'),
 ('M06', 'c2-counter.py', 'regen_ok = bool(regen_sha) and regen_sha == msha and', 'regen_ok = bool(regen_sha) and regen_sha != \'\' and', 'byte-identity regen==pin', 'R39 m06'),
 ('M12', 'c2-counter.py', "b['manifest_after_freeze'] = bool(ma) and ma != freeze and is_ancestor(root, freeze, ma)", "b['manifest_after_freeze'] = bool(ma) and ma != freeze", 'manifest descends from freeze', 'R39 m12'),
 ('M13', 'c2-counter.py', "b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) and all(", "b['manifest_before_envelopes'] = bool(ma) and bool(env_firsts) and any(", 'manifest before envelopes all->any', 'R39 m13'),
 ('M16', 'c2-counter.py', "b['triage_table_identical'] = blk_rev is not None and blk_fr is not None and blk_rev == blk_fr", "b['triage_table_identical'] = blk_rev == blk_fr", 'table identity None-guards', 'R39 m16'),
 ('M21', 'c2-counter.py', 'all(per.get(k) == 2 for k in classes)', 'all(per.get(k, 2) == 2 for k in classes)', 'classes_two_each default', 'R39 m21'),
 ('M22', 'c2-counter.py', 'consistent = met == recomputed', 'consistent = True', 'met consistency guard', 'R39 m22'),
 ('M23', 'c2-counter.py', 'if not consistent:', 'if False:', 'met consistency raise', 'R39 m23'),
 ('M27', 'c2-counter.py', 'if not is_ancestor(root, freeze, rev):', 'if False:', 'freeze-ancestor precheck', 'R39 m27'),
 ('M28', 'c2-counter.py', "'--no-renames',\n                        '--reverse', rev,", "'--no-renames',\n                        rev,", 'first_add latest-vs-earliest', 'R39 m28'),
 ('M29', 'c2-counter.py', "b['carriers_regenerated'] = N > 0 and all(r['regen_ok'] for r in res['carriers'])", "b['carriers_regenerated'] = N > 0 and any(r['regen_ok'] for r in res['carriers'])", 'carriers_regenerated all->any', 'R39 m29'),
 # ---- c2-counter.py: new
 ('N-M1', 'c2-counter.py', "b['seed_matches_freeze'] = str(man.get('seed', '')).lower() == freeze", "b['seed_matches_freeze'] = str(man.get('seed', '')).lower().startswith(freeze[:8])", 'seed==freeze 8-char prefix', 'NEW seed==freeze'),
 ('N-M2', 'c2-counter.py', 'and blk_rev == blk_fr', "and blk_rev.strip() == blk_fr.strip()", 'table identity whitespace-exact', 'NEW table byte-identity'),
 ('N-M5', 'c2-counter.py', "op_ok = eo.get('operation') == 'extract_firmware'", "op_ok = 'extract_firmware' in str(eo.get('operation'))", 'domain guard operation substring', 'NEW domain guard (R39-CL1 successor)'),
 ('N-M6', 'c2-counter.py', 'digest_ok = subject_sha(eo) == msha and bool(msha)', 'digest_ok = subject_sha(eo) == msha', 'digest empty-pin guard', 'NEW evidence digest'),
 # ---- c1-counter.py: new, clauses round-40 keeps
 ('N-C1', 'c1-counter.py', "return bool(candidate) and bool(rel) and (candidate == rel or candidate.endswith('/' + rel))", "return bool(candidate) and bool(rel) and candidate.endswith('/' + rel)", 'oracle same_rel exact-alternative', 'NEW oracle match'),
 ('N-C2', 'c1-counter.py', 'if any(sha == fs and same_rel(fp, rel) for fp, fs in files):', 'if any(sha == fs or same_rel(fp, rel) for fp, fs in files):', 'oracle hit and->or', 'NEW oracle match'),
 ('N-C3', 'c1-counter.py', "d['handler_ok'] = HANDLER in chunk_handlers(env)", "d['handler_ok'] = any(HANDLER in (h or '') for h in chunk_handlers(env))", 'handler exact->substring', 'NEW handler'),
 ('N-C4', 'c1-counter.py', "and ev[key][0].startswith('ev_'))", ")", 'evidence id ev_ prefix', 'NEW evidence id'),
 ('N-C5', 'c1-counter.py', "d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]\n                                   and ev[key][0].startswith('ev_'))", "d['evidence_id_ok'] = (key in ev and ev[key][0].lower() == ev[key][1].lower()\n                                   and ev[key][0].lower().startswith('ev_'))", 'evidence id case-exact', 'NEW evidence id'),
 ('N-C6', 'c1-counter.py', "    if sorted(seen) != sorted(in_tree):\n        return False, '%d gaps on %d in-tree symlinks' % (len(seen), len(in_tree))", "    if False:\n        return False, '%d gaps on %d in-tree symlinks' % (len(seen), len(in_tree))", 'gap cardinality check dropped', 'NEW gap clause'),
 ('N-C7', "c1-counter.py", "        if kind != 'unpublished-entry':", "        if kind not in ('unpublished-entry', 'extractor-failure'):", 'gap kind whitelist widened', 'NEW gap clause'),
 ('N-C8', 'c1-counter.py', "d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)", "d['receipt_fresh'] = bool(add) and is_ancestor(root, freeze, add)", 'receipt added at freeze allowed', 'NEW first-add'),
 ('N-C9', 'c1-counter.py', "                and d.get('oracle_hits') == d.get('oracle_files')\n", "", 'oracle coverage conjunct dropped', 'NEW oracle match'),
 ('N-C10', 'c1-counter.py', '    return lines[-1] if lines else None', '    return lines[0] if lines else None', 'c1 first_add latest-vs-earliest', 'NEW first-add'),
]


def apply_mutant(path, old, new, replace_all=False):
    src = open(path, encoding='utf-8').read()
    n = src.count(old)
    if n == 0:
        return 0, 'old-string not found'
    if n > 1 and not replace_all:
        return 0, 'old-string not unique (%d)' % n
    open(path, 'w', encoding='utf-8').write(src.replace(old, new) if replace_all else src.replace(old, new, 1))
    return 1, 'ok'


def run(cmd, timeout=280):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=os.path.join(S, 'hyaku')))
    return p.returncode, p.stdout, p.stderr


def detect(tool, mpath):
    out = {}
    if tool == 'sqfs-triage.py':
        rc, so, se = run([sys.executable, '-I', '-B', mpath, '--selftest'])
        out['selftest_exit'] = rc
        out['selftest_tail'] = so.strip().splitlines()[-1] if so.strip() else (se or '')[-200:]
        rc, so, se = run([sys.executable, '-I', '-B', os.path.join(S, 'label.py'), mpath])
        out['labels_raw'] = so.strip()[:400]
        try:
            r = json.loads(so)
            out['labels_exit'] = r.get('run_exit')
            out['agree'] = r.get('agree')
            out['flips'] = r.get('flips')
        except Exception:
            out['labels_exit'] = 'parse-error'
    else:
        rc, so, se = run([sys.executable, '-I', '-B', mpath, '--selftest'] +
                         ([] if tool == 'c2-counter.py' else ['--pkg65', P65]))
        out['selftest_exit'] = rc
        out['selftest_tail'] = so.strip().splitlines()[-1] if so.strip() else (se or '')[-200:]
        rc, so, se = run([sys.executable, '-I', '-B', mpath, '--root', os.path.join(S, 'clone'),
                          '--rev', REV, '--freeze', FREEZE] +
                         (['--pkg65', P65] if tool == 'c1-counter.py' else []) +
                         ['--json-out', os.path.join(S, 'last-verdict.json')])
        out['verdict_exit'] = rc
        out['verdict_stdout_tail'] = (so or '')[-200:]
        try:
            r = json.load(open(os.path.join(S, 'last-verdict.json')))
            out['met_target'] = r.get('met_target')
            out['matched'] = r.get('matched', r.get('carriers_matched'))
            out['n'] = r.get('n')
            out['bindings_false'] = r.get('bindings_false')
            out['reason'] = r.get('reason')
        except Exception:
            out['payload'] = 'none'
    return out


def verdict_class(d, base):
    if d.get('selftest_exit') != 0:
        return 'KILLED-SELFTEST'
    if 'labels_exit' in d:
        if d.get('labels_exit') != 0:
            return 'KILLED-LABELRUN'
        if d.get('agree') != base['agree']:
            return 'KILLED-LABELS'
        return 'SURVIVED'
    if d.get('verdict_exit') != base['verdict_exit'] or d.get('met_target') != base['met_target'] \
            or d.get('matched') != base['matched']:
        return 'KILLED-VERDICT'
    return 'SURVIVED'


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    basefile = os.path.join(S, 'baseline.json')
    base = json.load(open(basefile)) if os.path.exists(basefile) else None
    results = []
    outpath = os.path.join(S, 'results-%s.json' % which)
    for mid, tool, old, new, clause, prov in MUTANTS:
        if which not in ('all',) and not any(mid.startswith(w) for w in which.split(',')):
            continue
        if base is None:
            raise SystemExit('baseline.json missing')
        work = os.path.join(MIRROR, tool) if tool == 'c1-counter.py' else os.path.join(S, 'm.py')
        src = os.path.join(S, tool)
        if work != src:
            if os.path.exists(work):
                os.remove(work)
            shutil.copy(src, work)
        st, msg = apply_mutant(work, old, new, replace_all=(mid == 'T13'))
        if not st:
            results.append({'id': mid, 'tool': tool, 'apply_error': msg})
            continue
        mut_sha = hashlib.sha256(open(work, 'rb').read()).hexdigest()
        d = detect(tool, work)
        d.update({'id': mid, 'tool': tool, 'clause': clause, 'provenance': prov,
                  'mutant_sha256': mut_sha, 'verdict': verdict_class(d, base[tool])})
        results.append(d)
        print(json.dumps({k: d.get(k) for k in ('id', 'verdict', 'selftest_exit', 'agree',
                                                'verdict_exit', 'met_target', 'matched',
                                                'apply_error')}))
    json.dump(results, open(outpath, 'w'), indent=1)
    print('wrote', outpath, len(results))


if __name__ == '__main__':
    main()
