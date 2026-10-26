#!/usr/bin/env python3
"""action-scoring-check -- a label-only comparison cannot see a mutated cause column.

Round-39 routed defect R39-CL3 (third part). `c2-counter.py` compares `label == expected_label`
only; `sqfs-triage.py` declares `cause -> action` and `source` "documentation only". Measured by
`w2/R39W2C2AxisFit.md` section 3(c): replacing all eight cause cells with
"THIS CAUSE IS DELIBERATELY WRONG -> DO THE OPPOSITE" leaves every label byte-identical, so an
8-row nonsense-cause table still scores 20/20. The depth-bearing column of the round-39 depth
claim is 0% scored.

This script runs the FROZEN interpreter twice over the 20 held-out envelopes: once with the
frozen SKILL and once with a scratch copy whose cause cells are replaced by nonsense. It then
reports
  (a) label agreement frozen vs mutant  -> the label-only scorer's view (expected 20/20, blind);
  (b) (label, cause) agreement          -> the action-aware scorer's view (expected 0/20).
Pass (exit 0) requires a self-comparison of the frozen table with itself to agree 20/20 (no
false positive) AND the action-aware comparison to disagree on the mutant.

Usage: action-scoring-check.py --root LANE --work DIR
Exit 0 pass; 1 findings; 2 usage. Red-shaped result: (a) 20/20 while (b) 20/20.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile

NONSENSE = 'deliberate nonsense cause -> do the opposite of the evidence'
MARKER = '<!-- sqfs-triage-table v1 -->'


def mutate_causes(text):
    out = []
    in_table = False
    for line in text.splitlines():
        if line.strip() == MARKER:
            in_table = True
            out.append(line)
            continue
        if in_table and line.lstrip().startswith('|'):
            cells = line.strip().strip('|').split('|')
            if len(cells) == 9:
                head = cells[0].strip()
                if head not in ('label',) and set(''.join(cells)) - set('-: '):
                    cells[7] = f' {NONSENSE} '
                    out.append('|' + '|'.join(cells) + '|')
                    continue
        elif in_table and line.strip() and not line.lstrip().startswith('|'):
            in_table = False
        out.append(line)
    return '\n'.join(out) + '\n'


def run(interpreter, skill, envelopes):
    proc = subprocess.run([sys.executable, '-I', '-B', interpreter, '--skill', skill,
                           '--json', *envelopes], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f'interpreter exit {proc.returncode}: {proc.stderr.strip()[:200]}')
    results = json.loads(proc.stdout)['results']
    return {r['path']: (r['label'], r['row'][7]) for r in results}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir())
    args = ap.parse_args(argv)

    interpreter = os.path.join(args.root, 'tools/round-39/sqfs-triage.py')
    skill = os.path.join(args.root, 'SKILL.md')
    envelopes = sorted(glob.glob(os.path.join(
        args.root, 'corpus/evidence/round-39/c2/heldout/H*/envelope.json')))
    if not envelopes:
        print('USAGE no held-out envelopes', file=sys.stderr)
        return 2

    work = tempfile.mkdtemp(prefix='action-scoring-', dir=os.path.abspath(args.work))
    mutant = os.path.join(work, 'SKILL-mutant.md')
    with open(skill, encoding='utf-8') as fh:
        text = fh.read()
    with open(mutant, 'w', encoding='utf-8') as fh:
        fh.write(mutate_causes(text))

    frozen = run(interpreter, skill, envelopes)
    again = run(interpreter, skill, envelopes)
    mutant_res = run(interpreter, mutant, envelopes)

    n = len(envelopes)
    self_pairs = sum(1 for p in frozen if frozen[p] == again[p])
    label_agree = sum(1 for p in frozen if frozen[p][0] == mutant_res[p][0])
    pair_agree = sum(1 for p in frozen if frozen[p] == mutant_res[p])

    print(f'envelopes={n}')
    print(f'self-comparison (frozen vs frozen): pairs agree {self_pairs}/{n}')
    print(f'mutant, label-only scorer:          labels agree  {label_agree}/{n}')
    print(f'mutant, action-aware scorer:        pairs agree   {pair_agree}/{n}')
    findings = []
    if self_pairs != n:
        findings.append(f'self-comparison disagrees on {n - self_pairs} envelopes (unstable)')
    if label_agree != n:
        findings.append('label-only scorer already separates the mutant; expected it to be blind')
    if pair_agree == n:
        findings.append('action-aware scorer is also blind: the cause column is still unscored')
    print(f'findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
