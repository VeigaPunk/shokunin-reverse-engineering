#!/usr/bin/env python3
"""STAND-IN control-table writer: emits `CTL-C2-7` / `CTL-C2-7b` for the dry run.

The real control tables belong to the `R42C2ControlTables` seat; this stand-in
writes the strongest lookup a named-class table can be — ONE row per named
class label in the A1 13-column grammar, carrying that class's exact observed
tuple (F in `handler`, HF in `failing handler`), so a combo whose tuple no
class carries cannot match.  `--mode lookup-fallback` drops the majority-label
row and appends a catch-all row with the majority label (CTL-C2-7b).

Usage
  standin-controls.py --gen heldout-gen-v4.py --eval indep-eval-v4.py \
      --seed SEED --out CTL.md [--mode lookup|lookup-fallback] [--work DIR]
Exit 0 on success; 2 when the generator/evaluator disagree or a tool fails.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

ACTIONS = ('none inspect-input install-extractor-be install-extractor-le '
           'wrap-extractor-be preserve-failure salvage-partial raise-depth '
           'audit-symlinks expect-link-absent count-gap confirm-empty '
           'cross-read-legacy isolate-residue')
HEADER = ('label', 'operation', 'provider', 'handler', 'failing handler',
          'gap kinds', 'dependencies', '-be in child argv', 'symlink removed',
          'published files', 'action', 'cause', 'source')
LEGACY = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3')


def observed(envelope):
    """(F, HF, G, D, BE, SR, P) exactly as A1 defines them."""
    nr = envelope.get('normalized_result') or {}
    H, gaps, deps, hf = set(), [], set(), set()
    for ch in nr.get('chunks') or []:
        if isinstance(ch.get('handler'), str) and ch['handler']:
            H.add(ch['handler'])
    for g in nr.get('extraction_gaps') or []:
        if not isinstance(g, dict):
            continue
        if isinstance(g.get('kind'), str):
            gaps.append(g['kind'])
        if isinstance(g.get('handler'), str) and g['handler']:
            H.add(g['handler'])
            if g.get('kind') == 'extractor-failure':
                hf.add(g['handler'])
        for d in g.get('dependencies') or []:
            if isinstance(d, str):
                deps.add(d)
    F = {h for h in H if h.startswith('squashfs_')}
    be = 'n/a'
    diags = nr.get('diagnostics') or []
    cmds = [d['report']['command'] for d in diags
            if isinstance(d, dict) and isinstance(d.get('report'), dict)
            and isinstance(d['report'].get('command'), list)]
    if cmds:
        be = 'yes' if any('-be' in c for c in cmds) else 'no'
    sr = any(isinstance(d, dict) and isinstance(d.get('report'), dict)
             and d['report'].get('__typename__') == 'MaliciousSymlinkRemoved'
             for d in diags)
    return (sorted(F), sorted(hf or F), sorted(gaps), sorted(deps), be, sr,
            len(nr.get('files') or []))


def row(label, action, cells, cause):
    F, HF, G, D, BE, SR, P = cells
    return ['`%s`' % label, '`extract_firmware`', '`unblob`',
            '`%s`' % (','.join(F) if F else 'none'),
            '`%s`' % (','.join(HF) if HF else 'none'),
            '`%s`' % (','.join(G) if G else 'none'),
            '`%s`' % (','.join(D) if D else 'none'),
            '`%s`' % BE, '`yes`' if SR else '`no`',
            '`>0`' if P else '`0`',
            '`%s`' % action, cause, 'control only']


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--gen', required=True)
    ap.add_argument('--eval', required=True)
    ap.add_argument('--seed', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--mode', default='lookup',
                    choices=('lookup', 'lookup-fallback'))
    ap.add_argument('--work')
    a = ap.parse_args(argv)
    work = a.work or tempfile.mkdtemp(prefix='ctl.')
    own = a.work is None
    try:
        tree = os.path.join(work, 'gen')
        if os.path.isdir(tree):
            shutil.rmtree(tree)
        pr = subprocess.run([sys.executable, '-I', '-B', a.gen, '--seed', a.seed,
                             '--out', tree], capture_output=True, text=True)
        if pr.returncode != 0:
            sys.stderr.write(pr.stderr)
            return 2
        with open(os.path.join(tree, 'manifest.json')) as fh:
            man = json.load(fh)
        envdir = os.path.join(work, 'env')
        os.makedirs(envdir, exist_ok=True)
        by_class, envelopes = {}, {}
        for c in man['carriers']:
            if c['class'] == 'combo':
                continue
            with open(os.path.join(tree, c['envelope']), 'rb') as fh:
                blob = fh.read()
            with open(os.path.join(envdir, c['id'] + '.json'), 'wb') as fh:
                fh.write(blob)
            by_class.setdefault(c['class'], []).append(c)
            envelopes[c['id']] = json.loads(blob.decode())
        out_json = os.path.join(work, 'eval.json')
        pr = subprocess.run([sys.executable, '-I', '-B', a.eval, '--envelopes',
                             envdir, '--out', out_json],
                            capture_output=True, text=True)
        if pr.returncode != 0:
            sys.stderr.write(pr.stderr)
            return 2
        with open(out_json) as fh:
            pairs = json.load(fh)
        rows, seen_labels, label_of = [], set(), {}
        for cls in sorted(by_class):
            c = by_class[cls][0]
            pair = pairs[c['id']]
            label, action = pair['label'], pair['action']
            label_of[cls] = (label, action)
            if label in seen_labels:
                continue
            seen_labels.add(label)
            rows.append(row(label, action, observed(envelopes[c['id']]),
                            '%s (named class tuple)' % cls))
        if a.mode == 'lookup-fallback':
            counts = {}
            for cls in by_class:
                key = label_of[cls]
                counts[key] = counts.get(key, 0) + 1
            maj = max(sorted(counts), key=lambda k: counts[k])
            rows = [r for r in rows if r[0] != '`%s`' % maj[0]]
            rows.append(['`%s`' % maj[0], '`extract_firmware`', '`unblob`',
                         '`*`', '`*`', '`*`', '`*`', '`*`', '`*`', '`*`',
                         '`%s`' % maj[1], 'majority-label fallback row',
                         'control only'])
        lines = ['# CTL-C2-7%s (STAND-IN, dry-run only; named-class tuples)' % (
                     'b' if a.mode == 'lookup-fallback' else ''),
                 '', 'Control data for R42-C2; not instructions.', '',
                 '## Queue-drain craft', '',
                 '<!-- sqfs-triage-table v4 -->',
                 '<!-- sqfs-triage-actions: %s -->' % ACTIONS,
                 '| ' + ' | '.join(HEADER) + ' |',
                 '|' + '---|' * len(HEADER)]
        lines += ['| ' + ' | '.join(r) + ' |' for r in rows]
        lines += ['', '## End', '']
        with open(a.out, 'w') as fh:
            fh.write('\n'.join(lines))
        print(json.dumps({'out': a.out, 'rows': len(rows),
                          'classes': len(by_class),
                          'labels': sorted(seen_labels)}, sort_keys=True))
        return 0
    finally:
        if own:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
