#!/usr/bin/env python3
"""RV-4: mechanically extract the verbatim old/new lines from SC-2's map-token-patch.md
and build machine-applicable unified diffs (one per variant) from those very bytes.

Usage: extract_and_build.py <artifact.md> <before-readme> <outdir>
"""
import difflib
import hashlib
import pathlib
import re
import sys


def fenced_after(text, heading_re):
    m = re.search(heading_re, text, re.M)
    if not m:
        raise SystemExit(f'heading not found: {heading_re}')
    rest = text[m.end():]
    b = re.search(r'```\n(.*?)\n```', rest, re.S)
    if not b:
        raise SystemExit(f'no fenced block after heading {heading_re}')
    return b.group(1)


def main():
    art_p, before_p, outdir = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3])
    outdir.mkdir(parents=True, exist_ok=True)
    art_text = pathlib.Path(art_p).read_text()
    art_sha = hashlib.sha256(art_text.encode()).hexdigest()

    old_line = fenced_after(art_text, r'^## Old line[^\n]*\n')
    primary = fenced_after(art_text, r'^## New line — PRIMARY[^\n]*\n')
    honest = fenced_after(art_text, r'^## New line — HONEST-STOP[^\n]*\n')
    (outdir / 'lines-extracted.txt').write_text(
        f'artifact_sha256: {art_sha}\n\n[old_line]\n{old_line}\n\n[primary]\n{primary}\n\n[honest_stop]\n{honest}\n')

    before_text = pathlib.Path(before_p).read_text()
    before_lines = before_text.splitlines(keepends=True)
    hits = [i for i, l in enumerate(before_lines) if l.rstrip('\n') == old_line]
    print(f'artifact_sha256: {art_sha}')
    print(f'old_line_matches_in_before: {hits} (expect exactly one, at 0-based index 37 = line 38)')
    if len(hits) != 1:
        raise SystemExit('old line does not match exactly once in the before README')

    for name, new_line in (('primary', primary), ('honest-stop', honest)):
        after_lines = list(before_lines)
        after_lines[hits[0]] = new_line + '\n'
        dl = list(difflib.unified_diff(before_lines, after_lines,
                                       fromfile='a/corpus/README.md', tofile='b/corpus/README.md', n=3))
        after_text = ''.join(after_lines)
        # real blob sha1 short hashes (a git-style `index` line must not read as a deletion)
        def blob_short(data):
            import subprocess as sp
            h = sp.run(['git', 'hash-object', '--stdin'], input=data,
                       capture_output=True, text=True, check=True).stdout.strip()
            return h[:7]
        dl.insert(0, f'diff --git a/corpus/README.md b/corpus/README.md\n'
                     f'index {blob_short(before_text)}..{blob_short(after_text)} 100644\n')
        patch = ''.join(dl)
        (outdir / f'{name}.patch').write_text(patch)
        (outdir / f'{name}.README.md').write_text(after_text)
        print(f'{name}: patch {len(patch)} bytes -> {outdir / (name + ".patch")}')
        print(f'{name}: after sha256 {hashlib.sha256(after_text.encode()).hexdigest()}')


if __name__ == '__main__':
    main()