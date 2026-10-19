#!/usr/bin/env python3
"""EX-14 projection runner (arc3-loop1-round3, c1).

Applies the drafted knowledge-entry + map-token patch to the /var/tmp scratch
clone of the lane repo, commits there (scratch-only git writes; the lane repo is
never written), and runs command A (SCORECARD.md Measurement recipe A, verbatim
`git show REV:path` form) at the scratch commit. Emits one JSON audit record.

Usage:
  project.py --entry-file <path> [--stem <stem>] [--new-line-file <path>]
             [--label <label>] [--out <json>]
  project.py --entry-patch <patch> ...        # apply a diff instead of a raw file

Checks: command A before (base rev) and after; prior-82 byte identity; README
line-neutrality; token stem parity; entry self-identity if the entry declares a
sha256 of itself.
"""
import argparse, hashlib, json, pathlib, re, subprocess, sys

CLONE = pathlib.Path('/var/tmp/ex14-scratch')
BASE = 'c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311'
TOKEN_RE = re.compile(r'2026-10-\d{2}-[a-z0-9-]+')


def git(*args, check=True, cwd=CLONE):
    p = subprocess.run(['git', '-C', str(cwd)] + list(args),
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f'git {" ".join(args)}: rc={p.returncode}\n{p.stderr}')
    return p


def command_a(rev, cwd=CLONE):
    """Command A, verbatim SCORECARD.md recipe (git show form)."""
    def get(path):
        return subprocess.check_output(['git', '-C', str(cwd), 'show', f'{rev}:{path}'],
                                       text=True)
    paths = subprocess.check_output(['git', '-C', str(cwd), 'ls-tree', '-r', '--name-only', rev,
                                     '--', 'corpus/knowledge'], text=True).splitlines()
    files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
    section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
    mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
    craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
    rules = re.split(r'(?m)^- \*\*', craft)[1:]
    pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
    resolved = 0
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = len(get('corpus/knowledge/' + name).splitlines())
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError:
                valid = False
        resolved += valid
    return {'revision': rev, 'mapped': len(files & mapped),
            'knowledge_files': len(files), 'missing': sorted(files - mapped),
            'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
            'rule_blocks': len(rules),
            'coverage_score': round(10*len(files & mapped)/len(files), 2),
            'depth_score': round(10*resolved/len(rules), 2)}


def sha256_text(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--entry-file')
    ap.add_argument('--entry-patch')
    ap.add_argument('--stem', required=True)
    ap.add_argument('--new-line-file', required=True,
                    help='file holding the exact new README line (with trailing newline)')
    ap.add_argument('--label', default='projection')
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    audit = {'label': args.label, 'base': BASE, 'stem': args.stem,
             'utc': subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'],
                                            text=True).strip()}

    # 0. reset clone to base
    git('reset', '--hard', BASE, '--quiet')
    git('clean', '-fdx', '--quiet')

    audit['command_a_before'] = command_a(BASE)

    readme_path = CLONE / 'corpus/README.md'
    before_text = readme_path.read_text()
    before_lines = before_text.splitlines(keepends=True)
    pristine_lines = list(before_lines)
    audit['readme_before'] = {'lines': len(before_lines),
                              'sha256': sha256_text(before_text)}

    # 1. entry file
    if args.entry_file:
        if args.entry_file == 'PLACEHOLDER':
            entry_text = '# placeholder rehearsal entry (NOT the real draft)\n'
            audit['entry_source'] = 'placeholder-rehearsal'
        else:
            entry_text = pathlib.Path(args.entry_file).read_text()
            audit['entry_source'] = 'raw:' + args.entry_file
        entry_dest = CLONE / ('corpus/knowledge/' + args.stem + '.md')
        entry_dest.write_text(entry_text)
        audit['entry_sha256'] = sha256_text(entry_text)
        audit['entry_bytes'] = len(entry_text.encode('utf-8'))
    elif args.entry_patch:
        p = subprocess.run(['git', '-C', str(CLONE), 'apply', '--verbose', args.entry_patch],
                           capture_output=True, text=True)
        audit['entry_apply'] = {'rc': p.returncode, 'log': (p.stdout + p.stderr)[-500:]}
        if p.returncode != 0:
            print(json.dumps(audit, indent=1, sort_keys=True))
            sys.exit(1)
        entry_dest = CLONE / ('corpus/knowledge/' + args.stem + '.md')
        audit['entry_sha256'] = sha256_text(entry_dest.read_text())

    # 2. map token — single-line substitution on the EVM row
    new_line = pathlib.Path(args.new_line_file).read_text()
    if not new_line.endswith('\n'):
        new_line += '\n'
    old_line = before_lines[37]
    audit['old_line_sha256'] = sha256_text(old_line)
    audit['new_line_sha256'] = sha256_text(new_line)
    if old_line == new_line:
        raise RuntimeError('new line identical to old — no-op')
    if not re.search(r'2026-10-\d{2}-[a-z0-9-]+', old_line):
        raise RuntimeError('old line 38 does not look like the EVM map row')
    before_lines[37] = new_line
    readme_path.write_text(''.join(before_lines))

    after_text = readme_path.read_text()
    after_lines = after_text.splitlines(keepends=True)
    audit['readme_after'] = {'lines': len(after_lines), 'sha256': sha256_text(after_text)}
    audit['line_neutral'] = len(before_lines) == len(after_lines)
    diff_lines = [i for i, (a, b) in enumerate(zip(pristine_lines, after_lines), 1) if a != b]
    audit['changed_line_numbers'] = diff_lines

    # token analysis (coverage map section)
    def map_tokens(t):
        sec = t.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
        return TOKEN_RE.findall(sec)
    tok_before = map_tokens(before_text)
    tok_after = map_tokens(after_text)
    new_tokens = sorted(set(tok_after) - set(tok_before))
    removed_tokens = sorted(set(tok_before) - set(tok_after))
    audit['tokens'] = {'unique_before': len(set(tok_before)),
                       'unique_after': len(set(tok_after)),
                       'new': new_tokens, 'removed': removed_tokens,
                       'occurrences_before': len(tok_before),
                       'occurrences_after': len(tok_after)}
    audit['token_equals_stem'] = new_tokens == [args.stem]

    # 3. commit in scratch clone
    git('add', '-A')
    c = git('commit', '--quiet', '-m',
            f'{args.label}: entry {args.stem} + map token (scratch-clone commit; EX-14 projection)')
    after_rev = git('rev-parse', 'HEAD').stdout.strip()
    audit['scratch_after_rev'] = after_rev
    audit['commit_out'] = (c.stdout + c.stderr).strip()

    # 4. command A after
    audit['command_a_after'] = command_a(after_rev)

    # 5. prior-82 byte identity + diff inventory
    ns = git('diff', '--name-status', BASE, after_rev).stdout.strip().splitlines()
    audit['diff_base_to_after'] = ns
    kns = git('diff', '--name-status', BASE, after_rev, '--', 'corpus/knowledge').stdout.strip().splitlines()
    audit['knowledge_diff'] = kns
    audit['prior82_byte_identical'] = kns == [f'A\tcorpus/knowledge/{args.stem}.md']

    # entry self-identity (rule #14): if the entry text embeds a claimed sha256
    # of itself, re-derive it.
    claimed = None
    if args.entry_file and args.entry_file != 'PLACEHOLDER':
        m = re.findall(r'(?:sha256|sha-256)[^0-9a-f]{0,24}([0-9a-f]{64})', entry_text, re.I)
        claimed = sorted(set(m))
    audit['entry_claimed_self_hashes'] = claimed
    if claimed:
        actual = hashlib.sha256(pathlib.Path(args.entry_file).read_bytes()).hexdigest()
        audit['entry_self_hash_actual'] = actual
        audit['entry_self_hash_match'] = actual in claimed

    # verdict of the projection
    ca = audit['command_a_after']
    audit['PROJECTION_PASS'] = (
        ca['knowledge_files'] == 83 and ca['mapped'] == 83 and ca['missing'] == []
        and ca['dangling'] == [] and ca['citation_resolved_rules'] == 14
        and ca['rule_blocks'] == 14
        and audit['line_neutral'] and audit.get('prior82_byte_identical') is True
        and audit.get('token_equals_stem') is True)

    out = json.dumps(audit, indent=1, sort_keys=True)
    if args.out:
        pathlib.Path(args.out).write_text(out + '\n')
    print(out)


if __name__ == '__main__':
    main()