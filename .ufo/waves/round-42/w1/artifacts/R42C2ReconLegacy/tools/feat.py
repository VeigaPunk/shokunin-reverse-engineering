#!/usr/bin/env python3
"""Feature extraction for REA envelopes under the round-41/v4 precedence vocabulary."""
import json, os, sys, glob

RUNS = '/fast/scratch/hyaku/kaidoku-r42/R42C2ReconLegacy/runs'


def features(d):
    n = d.get('normalized_result') or {}
    op = d.get('operation')
    pr = (d.get('provider') or {}).get('id') if isinstance(d.get('provider'), dict) else d.get('provider')
    chunks = n.get('chunks') or []
    gaps = n.get('extraction_gaps') or []
    H = sorted({c.get('handler') for c in chunks if c.get('handler')} |
               {g.get('handler') for g in gaps if g.get('handler')})
    G = sorted({g.get('kind') for g in gaps if g.get('kind')})
    D = sorted({x for g in gaps for x in (g.get('dependencies') or [])})
    argvs = []
    for x in n.get('diagnostics') or []:
        rep = x.get('report') or {}
        cmd = rep.get('command')
        if cmd is None:
            cmd = x.get('command')
        if isinstance(cmd, list):
            argvs.append(cmd)
        elif isinstance(cmd, str):
            argvs.append(cmd.split())
    if not argvs:
        be = 'n/a'
    elif any('-be' in a for a in argvs):
        be = 'yes'
    else:
        be = 'no'
    sr = 'yes' if any(x.get('producer') == 'MaliciousSymlinkRemoved' or
                      x.get('kind') == 'MaliciousSymlinkRemoved' or
                      'MaliciousSymlinkRemoved' in json.dumps(x) for x in (n.get('diagnostics') or [])) else 'no'
    P = len(n.get('files') or [])
    return dict(OP=op, PR=pr, H=H, G=G, D=D, BE=be, SR=sr, P=P,
                chunks=[c.get('handler') for c in chunks],
                files=[f.get('relative_path') for f in n.get('files') or []],
                diag_kinds=[(x.get('kind'), x.get('producer'), (x.get('report') or {}).get('command')) for x in n.get('diagnostics') or []])


def main():
    only = sys.argv[1:] or None
    for w in sorted(glob.glob(os.path.join(RUNS, '*'))):
        name = os.path.basename(w)
        if only and not any(o in name for o in only):
            continue
        envp = os.path.join(w, 'envelope.json')
        try:
            e = json.load(open(envp))
        except Exception as exc:
            print(name, 'UNREADABLE', exc, open(os.path.join(w, 'rea.err')).read()[-300:])
            continue
        if not e.get('ok'):
            print(name, 'NOT-OK', json.dumps(e.get('error'))[:200])
            continue
        f = features(e['data'])
        print(json.dumps({'run': name, **{k: f[k] for k in ('OP', 'PR', 'H', 'G', 'D', 'BE', 'SR', 'P')},
                          'chunks': f['chunks'], 'diagnostics': f['diag_kinds'],
                          'files': f['files']}, sort_keys=False))


if __name__ == '__main__':
    main()
