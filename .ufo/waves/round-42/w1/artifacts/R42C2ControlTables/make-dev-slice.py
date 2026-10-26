#!/usr/bin/env python3
"""Materialize the round-42 C2 legacy DEV arm from the raw REA envelopes.

Reads `fixtures.json` (this directory) and `rea-raw/<raw>.json` (the CLI envelope REA
6.5.0 wrote for that fixture/command) and writes, into --out:

  <ID>/envelope.json   the bare `data` object (the shape every consumer reads)
  <ID>/rea-full.json   the untouched CLI envelope
  manifest.json        one carrier record per envelope, with
                       * the ONE feature key the round-42 contract uses:
                         `declared_features` (round-41 routed defect R41-CL1: the
                         generator wrote `declared`, the counter read other keys);
                       * `expected` = the draft precedence's (label, action, step),
                         from the independent evaluator it is given;
                       * provenance: fixture URL + sha256 + damage recipe + max_depth.

`declared_features` is the OBSERVED tuple (the interpreter's `--json` features), so the
manifest models exactly what heldout-gen-v4.py must write: observed, under one key.

    python3 -I -B make-dev-slice.py --out DIR [--raw DIR] [--fixtures FILE] \\
        [--interp PATH] [--eval PATH]

Honors TMPDIR; writes only --out.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def envelope_id(path):
    base = os.path.basename(path)
    if base in ('envelope.json', 'rea-full.json'):
        return os.path.basename(os.path.dirname(path))
    return os.path.splitext(base)[0]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--raw', default=os.path.join(HERE, 'rea-raw'))
    ap.add_argument('--fixtures', default=os.path.join(HERE, 'fixtures.json'))
    ap.add_argument('--interp', default=os.path.join(HERE, 'v4-check-interp.py'))
    ap.add_argument('--eval', default=os.path.join(HERE, 'preview-precedence.py'))
    ap.add_argument('--skill', default=os.path.join(HERE, 'CTL-C2-REF-v4-precedence.md'),
                    help='only used to make the interpreter parse a v4 table')
    a = ap.parse_args(argv)
    fixtures = json.load(open(a.fixtures, encoding='utf-8'))
    os.makedirs(a.out, exist_ok=True)
    records = []
    for src in fixtures['sources']:
        eid = src['id']
        raw = json.load(open(os.path.join(a.raw, src['raw']), encoding='utf-8'))
        data = raw.get('data', raw)
        d = os.path.join(a.out, eid)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'envelope.json'), 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
            fh.write('\n')
        with open(os.path.join(d, 'rea-full.json'), 'w', encoding='utf-8') as fh:
            json.dump(raw, fh, indent=1, sort_keys=True)
            fh.write('\n')
        records.append(src)

    envs = [os.path.join(a.out, r['id'], 'envelope.json') for r in records]
    feats = features(a.interp, a.skill, envs)
    ev = evaluate(a.eval, a.out)
    carriers = []
    for src in records:
        eid = src['id']
        f = feats[eid]
        rec = {
            'id': eid,
            'class': src['class'],
            'expected': {'label': ev[eid]['label'], 'action': ev[eid]['action'],
                         'step': ev[eid]['step']},
            'declared_features': f,
            'provenance': {
                'raw': src['raw'],
                'input': src['input'],
                'url': (fixtures['fixtures_base'] + src['url_path']
                        if src.get('url_path') else None),
                'sha256': src['sha256'],
                'max_depth': src['max_depth'],
                'damage': src['damage'],
                'rea_command': fixtures['rea_command'],
                'note': src.get('note'),
            },
        }
        carriers.append(rec)
    manifest = {
        'claim': 'R42-C2',
        'arm': 'legacy-dev',
        'generator': {'name': 'make-dev-slice.py', 'kind': 'real-REA-replay'},
        'rea': 'rea-agents 6.5.0 (extract-firmware), unblob 26.6.4, sasquatch 4.5.1',
        'n': len(carriers),
        'declared_features_key': 'declared_features',
        'carriers': carriers,
    }
    with open(os.path.join(a.out, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
        fh.write('\n')
    print('wrote %s (%d envelopes)' % (a.out, len(carriers)))
    return 0


def features(interp, skill, envs):
    r = subprocess.run([sys.executable, '-I', '-B', interp, '--skill', skill, '--json']
                       + envs, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('interpreter features failed (exit %d): %s'
                         % (r.returncode, r.stderr.strip()[-300:]))
    out = {}
    for rec in json.loads(r.stdout)['results']:
        f = rec['features']
        out[envelope_id(rec['path'])] = {
            'OP': f.get('OP'), 'PV': f.get('PV'), 'H': f.get('H') or [],
            'HF': f.get('HF') or [], 'G': f.get('G') or [], 'D': f.get('D') or [],
            'BE': f.get('BE'), 'SR': f.get('SR'), 'P': f.get('P') or 0,
        }
    return out


def evaluate(evaluator, dev):
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, 'ev.json')
        r = subprocess.run([sys.executable, '-I', '-B', evaluator, '--envelopes', dev,
                            '--out', out], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit('evaluator failed (exit %d): %s'
                             % (r.returncode, r.stderr.strip()[-300:]))
        return json.load(open(out))['labels']


if __name__ == '__main__':
    sys.exit(main())
