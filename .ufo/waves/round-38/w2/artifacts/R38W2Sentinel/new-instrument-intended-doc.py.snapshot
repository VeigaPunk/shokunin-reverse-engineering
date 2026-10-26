#!/usr/bin/env python3
"""intended-doc: bind a repaired self-assessment pointer to its intended document.

Round-38 mistake M38-6: the frozen R38-C2 counter accepts any pointer whose
path exists, so materialising a stub file at the unresolved base path
(`evidence/doctor/doctor-6.5.0.txt`, no PROVINCE edit) scores the same
"1 -> 0 mismatches" as the real repair (wave-2 seat R38W2C2Controls, S2).
QUALITY 81 makes this the check: the pointer in the named unit must name
the intended path frozen with the claim, and that path's git tree/blob at the
measured revision must equal its object at the base, i.e. the document already
existed and was not written by the claimant.

Usage:
  intended-doc.py --root LANE --rev REV --base BASE --file PROVINCE.md \
      --unit 'REA MCP server' --intended .ufo/waves/round-19/evidence/doctor/

Reads only git objects. Exit 0: bound; 1: not bound (reasons listed); 2: unevaluable.
"""
import argparse, json, re, subprocess, sys

TOKEN = re.compile(r'`([^`\s]+)`')


def git(root, *a):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=True)


def obj(root, rev, path):
    p = git(root, 'rev-parse', '--verify', '-q', f'{rev}:{path.rstrip("/")}')
    return p.stdout.strip() if p.returncode == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    for k in ('root', 'rev', 'base', 'file', 'unit', 'intended'):
        ap.add_argument('--' + k, required=True)
    a = ap.parse_args(argv)
    res = {'tool': 'intended-doc', 'rev': a.rev, 'base': a.base, 'file': a.file, 'unit': a.unit, 'intended': a.intended}
    text = git(a.root, 'show', f'{a.rev}:{a.file}')
    if text.returncode or obj(a.root, a.base, a.file) is None:
        res['verdict'] = 'unevaluable'
        print(json.dumps(res))
        return 2
    rows = [l for l in text.stdout.splitlines() if l.lstrip().startswith('|') and l.strip().strip('|').split('|')[0].strip() == a.unit]
    reasons = []
    if len(rows) != 1:
        reasons.append(f'unit rows found: {len(rows)} (need exactly 1)')
    toks = TOKEN.findall(rows[0]) if len(rows) == 1 else []
    if a.intended not in toks:
        reasons.append('intended path not named in the unit row')
    at_rev, at_base = obj(a.root, a.rev, a.intended), obj(a.root, a.base, a.intended)
    res['object_at_rev'], res['object_at_base'] = at_rev, at_base
    if at_base is None:
        reasons.append('intended document absent at base (written by the claimant?)')
    elif at_rev != at_base:
        reasons.append('intended document changed between base and rev')
    res['reasons'] = reasons
    res['verdict'] = 'bound' if not reasons else 'not-bound'
    print(json.dumps(res, indent=1))
    return 0 if not reasons else 1


if __name__ == '__main__':
    sys.exit(main())
