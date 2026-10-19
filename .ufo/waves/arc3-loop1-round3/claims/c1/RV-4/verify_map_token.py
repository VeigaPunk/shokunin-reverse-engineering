#!/usr/bin/env python3
"""RV-4 (arc3-loop1-round3) verifier: apply the map-token patch on a scratch copy;
check line-neutrality + token set 82 -> 83 + prior 82 tokens byte-identical.

Usage: verify_map_token.py <patch.md> <before-readme> <workdir>
Exit 0 == PASS.  Never touches the real repo; everything under <workdir>.
"""
import difflib
import hashlib
import os
import pathlib
import re
import subprocess
import sys

TOKEN_RE = re.compile(r'2026-10-\d{2}-[a-z0-9-]+')
REPO = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')

EXPECT_BEFORE_LINES = 190
EXPECT_BEFORE_TOKENS = 82
EXPECT_AFTER_TOKENS = 83


def extract_patch(text):
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
            env = dict(os.environ, TMPDIR=str(workdir))
            r2 = subprocess.run(['patch', '-p1', '--dry-run', '-i', str(extracted)],
                                cwd=repo, capture_output=True, text=True, env=env)
            if r2.returncode == 0:
                r3 = subprocess.run(['patch', '-p1', '-i', str(extracted)],
                                    cwd=repo, capture_output=True, text=True, env=env)
                applied = 'patch -p1' if r3.returncode == 0 else f'FAILED (patch rc={r3.returncode})'
            else:
                applied = (f'FAILED (git apply rc={r.returncode}; unidiff-zero rc={rz.returncode}; '
                           f'patch dry-run rc={r2.returncode})')

    print(f'patch_extraction: {how}')
    print(f'apply_method: {applied}')
    print(f'apply_log_tail: {(r.stdout + r.stderr).strip().splitlines()[-3:] if (r.stdout or r.stderr) else []}')

    after_path = repo / 'corpus' / 'README.md'
    if not after_path.exists():
        print('RESULT: FAIL — no README after apply')
        return 1
    after_text = after_path.read_text()
    after_lines = after_text.splitlines(keepends=True)
    after_tok_occ = tokens_of(after_text)
    after_tok_sorted = sorted(set(after_tok_occ))

    print(f'lines_before: {len(before_lines)}')
    print(f'lines_after:  {len(after_lines)}')
    line_neutral = len(before_lines) == len(after_lines)
    print(f'line_neutral: {line_neutral}')

    print(f'token_occurrences_before: {len(before_tok_occ)}  unique_before: {len(before_tok_sorted)}')
    print(f'token_occurrences_after:  {len(after_tok_occ)}  unique_after: {len(after_tok_sorted)}')
    new_tokens = sorted(set(after_tok_sorted) - set(before_tok_sorted))
    removed_tokens = sorted(set(before_tok_sorted) - set(after_tok_sorted))
    print(f'new_tokens: {new_tokens}')
    print(f'removed_tokens: {removed_tokens}')
    print(f'token_count_{EXPECT_BEFORE_TOKENS}_to_{EXPECT_AFTER_TOKENS}: '
          f'{len(before_tok_sorted) == EXPECT_BEFORE_TOKENS and len(after_tok_sorted) == EXPECT_AFTER_TOKENS}')

    prior_identical = sorted(set(after_tok_sorted) - set(new_tokens)) == before_tok_sorted
    after_occ_prior = [t for t in after_tok_occ if t not in set(new_tokens)]
    prior_occ_identical = after_occ_prior == before_tok_occ
    print(f'prior_tokens_byte_identical: {prior_identical}')
    print(f'prior_token_occurrence_sequence_identical: {prior_occ_identical}')

    # whole-file token multiset drift (coverage-map deltas only?)
    all_before = sorted(TOKEN_RE.findall(before_text))
    all_after = sorted(TOKEN_RE.findall(after_text))
    whole_ok = all_before == all_after
    print(f'whole_readme_token_multiset_unchanged: {whole_ok}')
    if not whole_ok:
        print(f'  whole_readme_added: {sorted(set(all_after) - set(all_before))}')
        print(f'  whole_readme_removed: {sorted(set(all_before) - set(all_after))}')

    # diff shape
    dl = list(difflib.unified_diff(before_lines, after_lines,
                                   fromfile='README.before', tofile='README.after', n=0))
    (workdir / 'readme.diff').write_text(''.join(dl))
    hunks = sum(1 for l in dl if l.startswith('@@'))
    removed = [l[1:] for l in dl if l.startswith('-') and not l.startswith('---')]
    added = [l[1:] for l in dl if l.startswith('+') and not l.startswith('+++')]
    print(f'hunks: {hunks}  removed_lines: {len(removed)}  added_lines: {len(added)}')
    print(f'removed_content: {[l[:160] for l in removed]}')
    print(f'added_content: {[l[:240] for l in added]}')

    # additive-only: each added line == its removed line with ONLY the new token inserted
    additive_ok = True
    insert_detail = []
    if len(removed) == len(added) and len(removed) >= 1:
        for rr, aa in zip(removed, added):
            rl, al = rr.rstrip('\n'), aa.rstrip('\n')
            p = 0
            while p < len(rl) and p < len(al) and rl[p] == al[p]:
                p += 1
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

    print(f'sha256_before: {sha256(before_path)}')
    print(f'sha256_after:  {sha256(after_path)}')

    files = re.findall(r'^\+\+\+ (?:(?:[abiw])/)?(.+)$', body, re.M)
    print(f'files_touched_by_patch: {files}')
    files_ok = files == ['corpus/README.md']

    # scope: every changed before-line must lie inside the coverage-map section
    sec_start = next(i for i, l in enumerate(before_lines, 1) if l.startswith('## Coverage map'))
    sec_end = next(i for i, l in enumerate(before_lines, 1) if i > sec_start and l.startswith('## ')) - 1
    hunk_starts = [int(m) for m in re.findall(r'^@@ -(\d+)', ''.join(dl), re.M)]
    scope_ok = all(sec_start < h <= sec_end for h in hunk_starts)
    print(f'coverage_section_lines: {sec_start}-{sec_end}  hunk_starts: {hunk_starts}  scope_ok: {scope_ok}')

    for t in new_tokens:
        kf = REPO / 'corpus' / 'knowledge' / (t + '.md')
        print(f'new_token_knowledge_file_on_disk: {t} -> {kf.exists()} ({kf})')

    occurrences_delta = len(after_tok_occ) - len(before_tok_occ)
    print(f'coverage_map_occurrence_delta: {occurrences_delta}')
    # seat-named criteria (RV-4 task): line count equal; token set 82 -> 83;
    # prior 82 tokens byte-identical (set AND occurrence order)
    seat_ok = (applied is not None and not applied.startswith('FAILED')
               and line_neutral
               and len(before_tok_sorted) == EXPECT_BEFORE_TOKENS
               and len(after_tok_sorted) == EXPECT_AFTER_TOKENS
               and prior_identical and prior_occ_identical and not removed_tokens
               and len(new_tokens) == 1 and occurrences_delta == 1)
    print(f'VERDICT_SEAT_CRITERIA (line-neutral | 82->83 | prior-82 identical): '
          f'{"PASS" if seat_ok else "FAIL"}')
    print(f'prior_82_tokens_byte_identical_detail: set_identical={prior_identical} '
          f'occurrence_order_identical={prior_occ_identical} removed={removed_tokens}')
    print(f'files_touched_ok: {files_ok}')
    print(f'STRICT_additive_only (r1 form; prose rewrite not allowed): {additive_ok}')
    ok = seat_ok and additive_ok and files_ok and scope_ok
    print(f'VERDICT: {"PASS" if ok else "FAIL"}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())