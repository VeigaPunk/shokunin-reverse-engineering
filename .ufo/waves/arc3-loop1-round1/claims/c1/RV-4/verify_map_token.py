#!/usr/bin/env python3
"""RV-4 verifier: apply map-token patch on a scratch copy; check line-neutrality + token set.

Usage: verify_map_token.py <patch.md> <before-readme> <workdir>
"""
import hashlib
import pathlib
import re
import subprocess
import sys

TOKEN_RE = re.compile(r'2026-10-\d{2}-[a-z0-9-]+')


def extract_patch(text):
    """Pull the diff body out of the .patch.md artifact (fenced block or whole file)."""
    m = re.search(r'```(?:diff|patch)\n(.*?)```', text, re.S)
    if m:
        return m.group(1), 'fenced'
    return text, 'raw'


def coverage_section(readme_text):
    return readme_text.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]


def tokens_of(readme_text):
    return TOKEN_RE.findall(coverage_section(readme_text))


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def main():
    patch_path, before_path, workdir = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    workdir.mkdir(parents=True, exist_ok=True)

    before_text = pathlib.Path(before_path).read_text()
    before_lines = before_text.splitlines(keepends=True)
    before_tok_occ = tokens_of(before_text)
    before_tok_sorted = sorted(set(before_tok_occ))

    body, how = extract_patch(pathlib.Path(patch_path).read_text())
    extracted = (workdir / 'extracted.patch').resolve()
    extracted.write_text(body)

    # Apply with `git apply` inside a scratch git repo containing only README,
    # falling back to `patch` if git apply is unavailable/unsuitable.
    repo = workdir / 'repo'
    subprocess.run(['rm', '-rf', str(repo)], check=True)
    (repo / 'corpus').mkdir(parents=True)
    (repo / 'corpus' / 'README.md').write_text(before_text)
    subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
    subprocess.run(['git', 'add', '-A'], cwd=repo, check=True)

    applied = None
    r = subprocess.run(['git', 'apply', '--verbose', str(extracted)],
                       cwd=repo, capture_output=True, text=True)
    (workdir / 'git-apply.out').write_text(r.stdout + r.stderr)
    if r.returncode == 0:
        applied = 'git apply'
    else:
        rz = subprocess.run(['git', 'apply', '--unidiff-zero', '--verbose', str(extracted)],
                            cwd=repo, capture_output=True, text=True)
        (workdir / 'git-apply-zero.out').write_text(rz.stdout + rz.stderr)
        if rz.returncode == 0:
            applied = 'git apply --unidiff-zero'
        else:
            env = dict(**__import__('os').environ, TMPDIR=str(workdir))
            r2 = subprocess.run(['patch', '-p1', '--dry-run', '-i', str(extracted)],
                                cwd=repo, capture_output=True, text=True, env=env)
            if r2.returncode == 0:
                r3 = subprocess.run(['patch', '-p1', '-i', str(extracted)],
                                    cwd=repo, capture_output=True, text=True, env=env)
                if r3.returncode == 0:
                    applied = 'patch -p1'
                else:
                    applied = f'FAILED (patch rc={r3.returncode})'
            else:
                applied = (f'FAILED (git apply rc={r.returncode}; unidiff-zero rc={rz.returncode}; '
                           f'patch dry-run rc={r2.returncode})')

    print(f'patch_extraction: {how}')
    print(f'apply_method: {applied}')
    print(f'apply_stderr_tail: {r.stderr.strip().splitlines()[-3:] if r.stderr else []}')

    after_path = repo / 'corpus' / 'README.md'
    if not after_path.exists():
        print('RESULT: FAIL — no README after apply')
        return 1
    after_text = after_path.read_text()
    after_lines = after_text.splitlines(keepends=True)
    after_tok_occ = tokens_of(after_text)
    after_tok_sorted = sorted(set(after_tok_occ))

    # 1. line neutrality
    print(f'lines_before: {len(before_lines)}')
    print(f'lines_after:  {len(after_lines)}')
    line_neutral = len(before_lines) == len(after_lines)
    print(f'line_neutral: {line_neutral}')

    # 2. token set 81 -> 82
    print(f'token_occurrences_before: {len(before_tok_occ)}  unique_before: {len(before_tok_sorted)}')
    print(f'token_occurrences_after:  {len(after_tok_occ)}  unique_after: {len(after_tok_sorted)}')
    new_tokens = sorted(set(after_tok_sorted) - set(before_tok_sorted))
    removed_tokens = sorted(set(before_tok_sorted) - set(after_tok_sorted))
    print(f'new_tokens: {new_tokens}')
    print(f'removed_tokens: {removed_tokens}')
    print(f'token_count_81_to_82: {len(before_tok_sorted) == 81 and len(after_tok_sorted) == 82}')

    # 3. prior 81 tokens byte-identical (sorted before list == sorted after minus new)
    prior_identical = sorted(set(after_tok_sorted) - set(new_tokens)) == before_tok_sorted
    # 3b. order-sensitive: prior token occurrence sequence unchanged after removing new tokens
    after_occ_prior = [t for t in after_tok_occ if t not in set(new_tokens)]
    prior_occ_identical = after_occ_prior == before_tok_occ
    print(f'prior_tokens_byte_identical: {prior_identical}')
    print(f'prior_token_occurrence_sequence_identical: {prior_occ_identical}')

    # 4. whole-file token multiset drift (tokens outside coverage map)
    all_before = sorted(TOKEN_RE.findall(before_text))
    all_after = sorted(TOKEN_RE.findall(after_text))
    print(f'whole_readme_token_multiset_unchanged: {all_before == all_after}'
          if all_before == all_after else
          f'whole_readme_token_multiset_changed: added={sorted(set(all_after)-set(all_before))} removed={sorted(set(all_before)-set(all_after))}')

    # 5. diff shape: which files, which lines, additive-only?
    import difflib
    dl = list(difflib.unified_diff(before_lines, after_lines,
                                   fromfile='README.before', tofile='README.after', n=0))
    (workdir / 'readme.diff').write_text(''.join(dl))
    changed_hunks = sum(1 for l in dl if l.startswith('@@'))
    removed = [l[1:] for l in dl if l.startswith('-') and not l.startswith('---')]
    added = [l[1:] for l in dl if l.startswith('+') and not l.startswith('+++')]
    print(f'hunks: {changed_hunks}  removed_lines: {len(removed)}  added_lines: {len(added)}')
    print(f'removed_content: {[l[:120] for l in removed]}')
    print(f'added_content: {[l[:200] for l in added]}')

    # 5b. additive-only: each added line = its removed line with ONLY the new token
    # inserted (common prefix + common suffix must cover the rest of the old line)
    additive_ok = True
    insert_detail = []
    if len(removed) == len(added) and len(removed) >= 1:
        for r, a in zip(removed, added):
            rl, al = r.rstrip('\n'), a.rstrip('\n')
            # longest common prefix
            p = 0
            while p < len(rl) and p < len(al) and rl[p] == al[p]:
                p += 1
            # longest common suffix not overlapping the prefix
            s = 0
            while (s < len(rl) - p and s < len(al) - p
                   and rl[len(rl) - 1 - s] == al[len(al) - 1 - s]):
                s += 1
            extra = al[p:len(al) - s]
            stripped = re.sub(r'[`+, ]', '', extra)
            good = stripped in set(new_tokens)
            additive_ok = additive_ok and good
            insert_detail.append((extra, good))
    else:
        additive_ok = False
    print(f'additive_only_check: {additive_ok}')
    print(f'insert_detail: {insert_detail}')

    # 6. hashes
    print(f'sha256_before: {sha256(before_path)}')
    print(f'sha256_after:  {sha256(after_path)}')

    # 7. files touched by patch
    files = re.findall(r'^\+\+\+ (?:(?:[abiw])/)?(.+)$', body, re.M)
    print(f'files_touched_by_patch: {files}')

    # 8. new token corresponds to a knowledge file on disk?
    for t in new_tokens:
        kf = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge') / (t + '.md')
        print(f'new_token_knowledge_file_exists: {t} -> {kf.exists()} ({kf})')

    occurrences_delta = len(after_tok_occ) - len(before_tok_occ)
    print(f'coverage_map_occurrence_delta: {occurrences_delta}')
    ok = (line_neutral and len(before_tok_sorted) == 81 and len(after_tok_sorted) == 82
          and prior_identical and prior_occ_identical and not removed_tokens and additive_ok
          and len(new_tokens) == 1 and occurrences_delta == 1)
    print(f'VERDICT: {"PASS" if ok else "FAIL"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
