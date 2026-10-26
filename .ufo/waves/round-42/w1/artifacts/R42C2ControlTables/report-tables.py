#!/usr/bin/env python3
"""Render the two evidence tables of the R42-C2 control run from the scored JSON.

    python3 -I -B report-tables.py --scores scores-a1.json --out DIR \\
        --env-dir DIR [--env-dir DIR ...] --eval indep-eval.py --interp interp.py \\
        [--v4only scores-a1-v4only.json]

Writes DIR/step-matrix.md (control x A1 step miss counts) and DIR/class-tuples.md
(one row per DEV envelope: features, expected pair, deciding step).  Features come from
the interpreter's `--json` output (H, HF, G, D, BE, SR, P) and the expected pair from the
evaluator, so every slice is rendered the same way regardless of its manifest shape.
"""
import argparse
import json
import os
import subprocess
import sys

STEPS = list(range(1, 16))


def envelope_id(path):
    base = os.path.basename(path)
    if base in ('envelope.json', 'rea-full.json'):
        return os.path.basename(os.path.dirname(path))
    return os.path.splitext(base)[0]


def envs_of(dirs):
    out = []
    for d in dirs:
        for name in sorted(os.listdir(d)):
            sub = os.path.join(d, name)
            if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, 'envelope.json')):
                out.append(os.path.join(sub, 'envelope.json'))
    return out


def classes_of(dirs):
    out = {}
    for d in dirs:
        p = os.path.join(d, 'manifest.json')
        if not os.path.isfile(p):
            continue
        for c in json.load(open(p)).get('carriers') or []:
            out[c['id']] = c.get('class')
    return out


def features(interp, skill, envs):
    r = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', skill, '--json']
                       + envs, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('interpreter features failed: %s' % r.stderr.strip()[-300:])
    return {envelope_id(x['path']): x['features'] for x in json.loads(r.stdout)['results']}


def evaluate(evaluator, dirs):
    import tempfile
    merged = {}
    for d in dirs:
        with tempfile.TemporaryDirectory() as t:
            out = os.path.join(t, 'ev.json')
            r = subprocess.run([sys.executable, '-I', '-B', evaluator, '--envelopes', d,
                                '--out', out], capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit('evaluator failed: %s' % r.stderr.strip()[-300:])
            merged.update(json.load(open(out))['labels'])
    return merged


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--scores', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--env-dir', action='append', default=[])
    ap.add_argument('--interp', required=True)
    ap.add_argument('--eval', required=True)
    ap.add_argument('--skill', default=None,
                    help='v4 table the interpreter must parse for features '
                         '(default: <out>/controls/CTL-C2-REF-v4-precedence.md)')
    ap.add_argument('--v4only')
    a = ap.parse_args(argv)
    s = json.load(open(a.scores))
    os.makedirs(a.out, exist_ok=True)

    rows = []
    for name, v in s['scores'].items():
        if 'REF' in name:
            continue
        cells = [str(v['missed_by_step'].get(str(k), 0)) for k in STEPS]
        rows.append('| `%s` | %d | %d/%d | %s | %s | %s |'
                    % (name, v['interp_exit'], v['matched'], v['n'],
                       '%d/%d' % tuple(v['combo']), '%d/%d' % tuple(v['named']),
                       ' | '.join(cells)))
    head = ('| control | exit | matched | combo | named | '
            + ' | '.join('s%d' % k for k in STEPS) + ' |')
    note = [
        '# R42-C2 control step matrix (A1 grammar, 15 precedence steps)',
        '',
        'Cell = number of DEV envelopes whose expected step is that column and whose',
        'observed (label, action) pair differs. `matched` reproduces the scorer row.',
        'Arm: %d envelopes (%s).' % (s['n'], ', '.join(s['dev_slices'])),
        'Interpreter: `%s`; evaluator: `%s`.' % (s['interp'], s['eval']),
        '',
        head, '|' + '---|' * (5 + len(STEPS)),
    ] + rows + [
        '',
        'Expected-step census: `%s`' % json.dumps(s['expected_steps'], sort_keys=True),
        '',
        'The reference row (`CTL-C2-REF`) is omitted: it is the reachability witness,',
        'not a control.',
        '',
    ]
    if a.v4only:
        v = json.load(open(a.v4only))
        note += ['## The same controls on the v4-only slice (52 round-41 dev envelopes)',
                 '', '| control | exit | matched |', '|---|---|---|']
        for name, rec in v['scores'].items():
            note.append('| `%s` | %d | %d/%d |'
                        % (name, rec['interp_exit'], rec['matched'], rec['n']))
        note.append('')
    open(os.path.join(a.out, 'step-matrix.md'), 'w').write('\n'.join(note) + '\n')

    envs = envs_of(a.env_dir)
    cls = classes_of(a.env_dir)
    skill = a.skill or os.path.join(a.out, 'controls', 'CTL-C2-REF-v4-precedence.md')
    feats = features(a.interp, skill, envs)
    ev = evaluate(a.eval, a.env_dir)
    lines = [
        '# R42-C2 DEV envelope tuples (A1 features)',
        '',
        '`H` = squashfs handler names; `HF` = handlers of the extractor-failure gaps',
        '(falls back to F); `G` gap kinds; `D` dependency names; `BE`; `SR`; `P`',
        'published regular files. `step` is the A1 precedence step that decides the pair.',
        '',
        '| id | class | H | HF | G | D | BE | SR | P | label | action | step |',
        '|---|---|---|---|---|---|---|---|---|---|---|---|',
    ]
    for path in envs:
        eid = envelope_id(path)
        f = feats[eid]
        e = ev.get(eid) or {}
        lines.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            eid, cls.get(eid, '-'),
            ' '.join(f.get('H') or []) or '-', ' '.join(f.get('HF') or []) or '-',
            ' '.join(f.get('G') or []) or '-', ' '.join(f.get('D') or []) or '-',
            f.get('BE'), f.get('SR'), f.get('P'),
            e.get('label'), e.get('action'), e.get('step')))
    lines.append('')
    open(os.path.join(a.out, 'class-tuples.md'), 'w').write('\n'.join(lines) + '\n')
    print('wrote %s/{step-matrix.md,class-tuples.md}' % a.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
