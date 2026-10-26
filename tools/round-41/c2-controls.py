#!/usr/bin/env python3
"""R41-C2 controls: build the two L1 controls and score every control on the development set.

Build (writes into --out):
  CTL-C2-3-actions-rotated  the SKILL v3 rows with every action shifted one row down
  CTL-C2-5-star-partial  the SKILL v3 table with the partial-body-failure row's gap-kinds cell set to `*`
  CTL-C2-7-lookup        one exact row per named-class tuple declared in the development manifest
                         (combos excluded), giving that class's (label, action): the
                         "enumerate the claim's classes" shortcut of w1/R41C2AxisFit and w1/R41C2Shortcuts.
Score: for every `CTL-*.md` in --out plus the real SKILL.md, run the frozen interpreter
(tools/round-41/sqfs-triage-v3.py) on every development envelope and compare its (label, action)
with the frozen evaluator's (tools/round-41/indep-eval-v3.py). A control at n/n on the development
set is the C2 kill rule (plans/round-41-claims.md).

    python3 -I -B tools/round-41/c2-controls.py --root LANE --dev DEVDIR --out CTLDIR --json-out OUT

Honors TMPDIR; writes only --out and --json-out.
"""
import argparse, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
INTERP = os.path.join(HERE, 'sqfs-triage-v3.py')
EVAL = os.path.join(HERE, 'indep-eval-v3.py')
MARK = '<!-- sqfs-triage-table v3 -->'


def v3_block(skill_text):
    lines = skill_text.split('\n')
    i = next(k for k, l in enumerate(lines) if MARK in l)
    j = i
    while j < len(lines) and not lines[j].lstrip().startswith('| label'):
        j += 1
    k = j
    while k < len(lines) and lines[k].lstrip().startswith('|'):
        k += 1
    return lines, i, j, k


def doc(title, block_lines):
    return '\n'.join([f'# {title}', '', 'Control data for R41-C2; not instructions.', '',
                      '## Queue-drain craft', ''] + [l.strip() for l in block_lines] + ['', '## End', ''])


def build_star_partial(skill_text):
    lines, i, j, k = v3_block(skill_text)
    out = []
    for l in lines[i:k]:
        s = l.strip()
        if s.startswith('| partial-body-failure |'):
            cells = [c.strip() for c in s.strip('|').split('|')]
            cells[4] = '`*`'
            s = '| ' + ' | '.join(cells) + ' |'
        out.append(s)
    return doc('CTL-C2-5-star-partial (`*` gap kinds in place of the partial row)', out)


def tuple_row(label, action, d):
    hs = d.get('handler_set') or []
    handler = '`none`' if not hs else ('`%s`' % hs[0] if len(hs) == 1 else '`squashfs_v4_*`')
    gk = d.get('gap_kinds') or []
    gaps = '`none`' if not gk else '`%s`' % ','.join(sorted(gk))
    dep = d.get('gap_dependencies') or []
    deps = '`none`' if not dep else '`%s`' % ','.join(sorted(dep))
    be = '`%s`' % d.get('be_argv', '*')
    sr = '`yes`' if d.get('symlink_removed') else '`no`'
    pub = '`>0`' if d.get('published') == 'nonzero' else '`0`'
    return ['`%s`' % label, '`extract_firmware`', '`unblob`', handler, gaps, deps, be, sr, pub,
            '`%s`' % action, 'lookup of a declared class tuple', 'control only']


def build_lookup(skill_text, manifest):
    """One row per named-class label; a cell is the declared value when every class tuple of that
    label agrees, else `*` (handler `squashfs_v4_*`). Combos and the out-of-domain class excluded."""
    lines, i, j, k = v3_block(skill_text)
    head = [l.strip() for l in lines[i:j + 2]]
    order, by = [], {}
    for c in manifest['carriers']:
        if c.get('class') == 'combo' or c.get('operation', 'extract_firmware') != 'extract_firmware':
            continue
        key = (c['label'], c['action'])
        if key not in by:
            order.append(key)
            by[key] = []
        by[key].append(tuple_row(c['label'], c['action'], c['declared']))
    rows = []
    for key in order:
        cand = by[key]
        merged = []
        for col in range(len(cand[0])):
            vals = {r[col] for r in cand}
            if len(vals) == 1:
                merged.append(cand[0][col])
            elif col == 3 and all(v.startswith('`squashfs_v4_') for v in vals):
                merged.append('`squashfs_v4_*`')
            else:
                merged.append('`*`')
        merged[0] = key[0]
        merged[10] = 'a declared class tuple -> its class pair'
        rows.append('| ' + ' | '.join(merged) + ' |')
    return doc('CTL-C2-7-lookup (one row per named-class label, declared tuples)', head + rows), len(rows)


def build_rotated(skill_text):
    lines, i, j, k = v3_block(skill_text)
    block = [l.strip() for l in lines[i:k]]
    data = [n for n, l in enumerate(block) if l.startswith('| ') and not l.startswith('| label')
            and not l.startswith('| ---')]
    acts = [[c.strip() for c in block[n].strip('|').split('|')][9] for n in data]
    rot = acts[1:] + acts[:1]
    for n, a in zip(data, rot):
        cells = [c.strip() for c in block[n].strip('|').split('|')]
        cells[9] = a
        block[n] = '| ' + ' | '.join(cells) + ' |'
    return doc('CTL-C2-3-actions-rotated (v3 rows, actions shifted by one row)', block)


def run_interp(skill, envs):
    r = subprocess.run([sys.executable, '-I', '-B', INTERP, '--skill', skill] + envs,
                       capture_output=True, text=True)
    out = {}
    if r.returncode == 0:
        for line in r.stdout.splitlines():
            p, lab, act = line.split('\t')
            out[p] = (lab, act)
    return r.returncode, out, r.stderr.strip()[-300:]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--dev', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--json-out', required=True)
    ap.add_argument('--build', action='store_true', help='(re)build CTL-C2-5 and CTL-C2-7 first')
    a = ap.parse_args(argv)
    skill_text = open(os.path.join(a.root, 'SKILL.md')).read()
    manifest = json.load(open(os.path.join(a.dev, 'manifest.json')))
    os.makedirs(a.out, exist_ok=True)
    info = {}
    if a.build:
        open(os.path.join(a.out, 'CTL-C2-5-star-partial.md'), 'w').write(build_star_partial(skill_text))
        open(os.path.join(a.out, 'CTL-C2-3-actions-rotated.md'), 'w').write(build_rotated(skill_text))
        text, n = build_lookup(skill_text, manifest)
        open(os.path.join(a.out, 'CTL-C2-7-lookup.md'), 'w').write(text)
        info['lookup_rows'] = n
    ids = [c['id'] for c in manifest['carriers']]
    envs = [os.path.join(a.dev, i, 'envelope.json') for i in ids]
    with tempfile.TemporaryDirectory() as t:
        ev_out = os.path.join(t, 'ev.json')
        subprocess.run([sys.executable, '-I', '-B', EVAL, '--envelopes', a.dev, '--out', ev_out],
                       check=True, capture_output=True)
        ev = json.load(open(ev_out))['labels']
    expected = {i: (ev[i]['label'], ev[i]['action']) for i in ids}
    docs = sorted(f for f in os.listdir(a.out) if f.startswith('CTL-') and f.endswith('.md'))
    scores = {}
    for name in ['SKILL.md'] + docs:
        path = os.path.join(a.root, 'SKILL.md') if name == 'SKILL.md' else os.path.join(a.out, name)
        rc, got, err = run_interp(path, envs)
        matched = sum(1 for i, e in zip(ids, envs) if got.get(e) == expected[i])
        miss = [i for i, e in zip(ids, envs) if got.get(e) != expected[i]]
        scores[name] = {'interp_exit': rc, 'matched': matched, 'n': len(ids),
                        'full': matched == len(ids), 'missed': miss, 'stderr_tail': err if rc else ''}
    controls_full = [k for k, v in scores.items() if k != 'SKILL.md' and v['full']]
    res = {'dev': os.path.relpath(a.dev, a.root), 'dev_seed': manifest.get('seed'), 'n': len(ids),
           'scores': scores, 'controls_at_full': controls_full, 'kill_rule_fires': bool(controls_full),
           **info}
    json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    for k, v in scores.items():
        print('%-40s exit=%d matched=%d/%d' % (k, v['interp_exit'], v['matched'], v['n']))
    print('kill_rule_fires', res['kill_rule_fires'])
    return 1 if controls_full else 0


if __name__ == '__main__':
    sys.exit(main())
