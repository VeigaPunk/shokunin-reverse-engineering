#!/usr/bin/env python3
"""In-process differential probes for surviving sqfs-triage mutants (N-T1, N-T2, N-T4):
pristine vs mutant parse_skill+features+classify on crafted tables/envelopes."""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)

sp = importlib.util.spec_from_file_location('tp', os.path.join(S, 'sqfs-triage.py'))
P = importlib.util.module_from_spec(sp); sp.loader.exec_module(P)

REAL_TABLE_SKILL = None  # filled from the lane SKILL.md block for realism


def skill_with_table(rows):
    header = '| label | handler | gap kinds | dependencies | -be in child argv | ' \
             'symlink removed | published files | cause -> action | source |'
    sep = '| ' + ' | '.join(['---'] * 9) + ' |'
    body = '\n'.join('| ' + ' | '.join(r) + ' |' for r in rows)
    return ('# K\n\n## Queue-drain craft (x)\n\n- rule text\n\n'
            '<!-- sqfs-triage-table v1 -->\n\n' + header + '\n' + sep + '\n' + body +
            '\n\n## Next\n\n- other\n')


def env(kind=None, deps=None, handlers=None, be_cmds=None, sr=False, nfiles=0):
    nr = {'chunks': [{'handler': h} for h in (handlers or [])],
          'extraction_gaps': ([{'kind': kind, 'dependencies': deps or []}] if kind is not None
                              else []),
          'files': [{'relative_path': 'f%d' % i, 'sha256': '0' * 64} for i in range(nfiles)],
          'diagnostics': ([] if not sr else
                          [{'report': {'__typename__': 'MaliciousSymlinkRemoved'}}])}
    data = {'normalized_result': nr}
    if be_cmds:
        nr['diagnostics'] = nr['diagnostics'] + [
            {'report': {'command': c}} for c in be_cmds]
    return data


def load_mutant(mid):
    import mutate
    for m_id, tool, old, new, clause, prov in mutate.MUTANTS:
        if m_id == mid:
            path = os.path.join(S, 't-%s.py' % mid)
            shutil.copy(os.path.join(S, tool), path)
            src = open(path, encoding='utf-8').read()
            assert src.count(old) == 1, (mid, src.count(old))
            open(path, 'w', encoding='utf-8').write(src.replace(old, new))
            sp = importlib.util.spec_from_file_location('tm' + mid, path)
            mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
            return mod
    raise SystemExit('unknown mutant ' + mid)


def classify_both(mid, skill_text, envelope):
    rules_p, _ = P.parse_skill(skill_text)
    mod = load_mutant(mid)
    rules_m, _ = mod.parse_skill(skill_text)
    feat_p = P.features(P.envelope_data(envelope))
    feat_m = mod.features(mod.envelope_data(envelope))
    r_p = P.classify(rules_p, feat_p)
    r_m = mod.classify(rules_m, feat_m)
    return (r_p['label'] if r_p else 'unclassified',
            r_m['label'] if r_m else 'unclassified',
            feat_p, feat_m)


results = {}

# ---- N-T1: gap kind case-normalised
rows = [['dep', '`squashfs_v4_be`', '`unpublished-entry`', '`*`', '`*`', '`*`', '`*`', 'c -> a', 's']]
skill = skill_with_table(rows)
e = env(kind='Unpublished-Entry', handlers=['squashfs_v4_be'], nfiles=1)
results['N-T1'] = classify_both('N-T1', skill, e)
print('N-T1', results['N-T1'][:2])

# ---- N-T2: none-cell becomes any (crafted row order)
rows = [['early', '`squashfs_v4_be`', '`none`', '`*`', '`n/a`', '`no`', '`>0`', 'c -> a', 's'],
        ['correct', '`squashfs_v4_be`', '`unpublished-entry`', '`*`', '`n/a`', '`no`', '`>0`', 'c -> a', 's']]
skill = skill_with_table(rows)
e = env(kind='unpublished-entry', handlers=['squashfs_v4_be'], nfiles=3)
results['N-T2'] = classify_both('N-T2', skill, e)
print('N-T2', results['N-T2'][:2])

# ---- N-T4: handler pattern any->all (two squashfs handlers, exact pattern)
rows = [['be-only', '`squashfs_v4_be`', '`none`', '`none`', '`n/a`', '`no`', '`>0`', 'c -> a', 's']]
skill = skill_with_table(rows)
e = env(handlers=['squashfs_v4_be', 'squashfs_v4_le'], nfiles=1)
results['N-T4'] = classify_both('N-T4', skill, e)
print('N-T4', results['N-T4'][:2])

json.dump({k: {'pristine': v[0], 'mutant': v[1]} for k, v in results.items()},
          open(os.path.join(S, 'probe-t-results.json'), 'w'), indent=1)
print('wrote probe-t-results.json')
