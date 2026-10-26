#!/usr/bin/env python3
"""table-copies-gate -- a frozen interpreter may not carry a second copy of the rule it reads.

`tools/round-39/sqfs-triage.py` embeds `TABLE_BLOCK` and builds every selftest fixture from it
(`_skel(TABLE_BLOCK)`, lines 680-910), while the counter scores the table in `SKILL.md`. The two
copies are not the same rule: measured here, the embedded table pins `dep-missing-be`/
`dep-missing-le` to published files `0` (shipped: `*`) and pins `escaping-symlink-removed`,
`in-tree-symlink-metadata` and `clean` to `squashfs_v4_be` (shipped: `squashfs_v4_*`). A 35-case
selftest green therefore describes a table the lane does not ship.

Rule: the embedded block must parse to the same rows as the SKILL block (cells included). When
`--heldout` is given, the embedded table is also scored on the held-out set through the frozen
interpreter, so the divergence is shown as a label delta, not only as text.

Usage:
  table-copies-gate.py --interpreter tools/round-39/sqfs-triage.py --skill SKILL.md \
      --heldout corpus/evidence/round-39/c2/heldout --work "$TMPDIR" [--fix-out PATH]
`--fix-out` writes a copy whose embedded literal is the SKILL block (the single-source fix), so
the same check can be shown green. Exit 0 identical; 1 divergence; 2 usage.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

MARKER = '<!-- sqfs-triage-table v1 -->'
LITERAL = re.compile(r'(TABLE_BLOCK\s*=\s*)"""(.*?)"""', re.S)


def rows(text):
    out = []
    for line in text.splitlines():
        if line.strip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if set(''.join(cells)) - set('-: '):
                out.append(cells)
    return out


def skill_block(text):
    start = text.index(MARKER)
    end = text.index('\n## ', start)
    return text[start:end]


def embedded_block(source):
    match = LITERAL.search(source)
    if not match:
        raise SystemExit('USAGE no TABLE_BLOCK literal in the interpreter')
    return match.group(2)


def score(interpreter, skill_text, heldout, work):
    path = os.path.join(work, 'copy-skill.md')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('## Queue-drain craft \n\n' + skill_text.strip('\n') + '\n\n## next\n')
    envelopes = [os.path.join(heldout, d, 'envelope.json')
                 for d in sorted(os.listdir(heldout)) if d.startswith('H')]
    proc = subprocess.run([sys.executable, '-I', '-B', interpreter, '--skill', path,
                           '--json', *envelopes], capture_output=True, text=True)
    if proc.returncode != 0:
        return None, proc.stderr.strip()[:160]
    results = json.loads(proc.stdout)['results']
    manifest = json.load(open(os.path.join(heldout, 'manifest.json'), encoding='utf-8'))
    expected = {row['id']: row['label'] for row in manifest['carriers']}
    got = {os.path.basename(os.path.dirname(r['path'])): r['label'] for r in results}
    matched = sum(1 for cid, label in expected.items() if got.get(cid) == label)
    return (matched, len(expected)), ''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--interpreter', required=True)
    ap.add_argument('--skill', required=True)
    ap.add_argument('--heldout')
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir())
    ap.add_argument('--fix-out')
    args = ap.parse_args(argv)

    source = open(args.interpreter, encoding='utf-8').read()
    skill = open(args.skill, encoding='utf-8').read()
    block = skill_block(skill)
    emb = embedded_block(source)
    emb_rows, skill_rows = rows(emb), rows(block)

    findings = []
    if MARKER not in emb:
        findings.append('embedded block has no v1 marker')
    if len(emb_rows) != len(skill_rows):
        findings.append(f'row count differs: embedded {len(emb_rows)} vs SKILL {len(skill_rows)}')
    for a, b in zip(emb_rows, skill_rows):
        if a != b:
            diffs = [f'cell {i}: embedded={x[:60]!r} skill={y[:60]!r}'
                     for i, (x, y) in enumerate(zip(a, b)) if x != y]
            findings.append(f'row {a[0][:28]!r} differs: ' + '; '.join(diffs))

    if args.fix_out:
        fixed = LITERAL.sub(lambda m: m.group(1) + '"""' + block + '"""', source, count=1)
        with open(args.fix_out, 'w', encoding='utf-8') as fh:
            fh.write(fixed)
        print(f'wrote single-source copy {args.fix_out}')

    work = tempfile.mkdtemp(prefix='table-copies-', dir=os.path.abspath(args.work))
    if args.heldout:
        shipped, err = score(args.interpreter, block, args.heldout, work)
        embedded, err2 = score(args.interpreter, emb, args.heldout, work)
        print(f'held-out score, shipped SKILL block: {shipped} {err}')
        print(f'held-out score, embedded TABLE_BLOCK: {embedded} {err2}')
        if shipped and embedded and shipped != embedded:
            findings.append(f'embedded table scores {embedded[0]}/{embedded[1]} where the shipped '
                            f'table scores {shipped[0]}/{shipped[1]}')

    print(f'interpreter={args.interpreter} embedded_rows={len(emb_rows)} '
          f'skill_rows={len(skill_rows)} findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return 0 if not findings else 1


if __name__ == '__main__':
    sys.exit(main())
