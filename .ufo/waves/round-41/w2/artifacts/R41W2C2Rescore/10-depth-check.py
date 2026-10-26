"""R41-C2 re-score: what REA parameters each held-out carrier actually ran at.

Reads only corpus/evidence/round-41/c2/heldout/<id>/run.json (recorded by the
generator's --run path) and cross-checks the recorded max_depth against the
--max-depth argv actually passed to rea-agents.
"""
import json
import os
import sys

HELD = os.path.join(sys.argv[1], 'corpus', 'evidence', 'round-41', 'c2', 'heldout')
man = json.load(open(os.path.join(HELD, 'manifest.json')))
by_id = {c['id']: c for c in man['carriers']}
rows, bad_exit, bad_depth = [], [], []
for cid in sorted(by_id):
    run = json.load(open(os.path.join(HELD, cid, 'run.json')))
    argv = run.get('rea_argv') or []
    joined = ' '.join(str(a) for a in argv)
    depth1 = '--max-depth 1' in joined
    md = run.get('max_depth')
    rows.append({'id': cid, 'class': run.get('class'), 'max_depth': md,
                 'argv_max_depth_1': depth1, 'exit_code': run.get('exit_code'),
                 'op': run.get('operation')})
    if run.get('exit_code') != 0:
        bad_exit.append(cid)
    if md is not None and (md == 1) != depth1:
        bad_depth.append(cid)

combo_depths = {r['id']: r['max_depth'] for r in rows if r['class'] == 'combo'}
depth_classes = {r['id']: r['max_depth'] for r in rows
                 if r['class'].startswith('depth-limited') or r['class'] == 'failure-depth-limited'}
summary = {
    'n': len(rows),
    'exit_nonzero': bad_exit,
    'depth_argv_disagreements': bad_depth,
    'n_at_depth1': sum(1 for r in rows if r['max_depth'] == 1),
    'n_at_depth3': sum(1 for r in rows if r['max_depth'] == 3),
    'n_no_depth': sum(1 for r in rows if r['max_depth'] is None),
    'combo_depths': combo_depths,
    'depth_class_depths': depth_classes,
    'depth_classes_all_at_1': all(v == 1 for v in depth_classes.values()),
    'manifest_rea_per_class': man['rea']['per_class'],
    'manifest_rea_default': man['rea']['default_max_depth'],
}
json.dump({'summary': summary, 'rows': rows}, sys.stdout, indent=1, sort_keys=True)
sys.stdout.write('\n')
