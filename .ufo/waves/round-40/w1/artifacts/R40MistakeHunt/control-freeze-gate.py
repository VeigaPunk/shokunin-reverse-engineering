#!/usr/bin/env python3
"""control-freeze-gate -- a registered kill-control input must exist AND parse at the freeze.

Round-39 routed defect R39-CL4 (QUALITY 80 pattern): the C2 kill controls CTL-C2-5 and
CTL-C2-6 were only scoreable from `.formatfix` tables first committed at 72359309, i.e.
AFTER the freeze 8fcda41c. The scored value (8/20, 12/20 in ctl-c2-dev-scores.json) therefore
certifies table bytes the freeze never held.

Rule enforced here, for every control table present at HEAD under --tables:
  A. the same path exists at --freeze (git cat-file -e FREEZE:path);
  B. the frozen bytes parse under the frozen interpreter (extract the FREEZE blob to scratch,
     run `<interpreter> --skill <blob> --table-only`, require exit 0).
A control whose input arrives later is not a control on the frozen claim.

Exit 0 all inputs frozen+valid; 1 any finding; 2 usage/IO error.
Red: lane, --freeze 8fcda41c, --tables .ufo/waves/round-39/controls/tables
     -> both tables ABSENT_AT_FREEZE.
Green: a fixture repo whose tables are committed in the freeze commit -> 0 findings.
Green-half check: a malformed copy (cause cell without `->`) -> FORMAT_INVALID finding.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

EXIT_OK, EXIT_FINDING, EXIT_USAGE = 0, 1, 2


def git(root, *args, check=True):
    return subprocess.run(['git', '-C', root, *args], capture_output=True, text=True,
                          check=check)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='git repo root (worktree path)')
    ap.add_argument('--freeze', required=True, help='freeze commit')
    ap.add_argument('--tables', required=True, help='repo-relative control-table directory')
    ap.add_argument('--interpreter', required=True, help='sqfs-triage style interpreter path')
    ap.add_argument('--work', default=os.environ.get('TMPDIR') or tempfile.gettempdir(),
                    help='scratch dir (honours TMPDIR)')
    args = ap.parse_args(argv)

    ls = git(args.root, 'ls-tree', '-r', '--name-only', 'HEAD', '--', args.tables)
    paths = [p for p in ls.stdout.splitlines() if p.endswith('.md')]
    if not paths:
        print(f'USAGE no control tables at HEAD under {args.tables}', file=sys.stderr)
        return EXIT_USAGE

    work = tempfile.mkdtemp(prefix='ctrl-freeze-', dir=os.path.abspath(args.work))
    findings = []
    rows = []
    try:
        for path in paths:
            present = git(args.root, 'cat-file', '-e', f'{args.freeze}:{path}', check=False).returncode == 0
            if not present:
                rows.append((path, 'ABSENT_AT_FREEZE', ''))
                findings.append(f'{path}: not present at freeze {args.freeze}')
                continue
            blob = git(args.root, 'show', f'{args.freeze}:{path}').stdout
            local = os.path.join(work, os.path.basename(path))
            with open(local, 'w', encoding='utf-8') as fh:
                fh.write(blob)
            proc = subprocess.run([sys.executable, '-I', '-B', args.interpreter,
                                   '--skill', local, '--table-only'],
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                rows.append((path, f'FORMAT_INVALID(exit {proc.returncode})',
                             proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ''))
                findings.append(f'{path}: frozen bytes do not parse (exit {proc.returncode})')
            else:
                rows.append((path, 'frozen+valid', ''))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    width = max(len(r[0]) for r in rows)
    for path, state, extra in rows:
        print(f'{path:<{width}}  {state}  {extra}')
    print(f'freeze={args.freeze} tables={len(rows)} findings={len(findings)}')
    for f in findings:
        print(f'FINDING {f}')
    return EXIT_OK if not findings else EXIT_FINDING


if __name__ == '__main__':
    sys.exit(main())
