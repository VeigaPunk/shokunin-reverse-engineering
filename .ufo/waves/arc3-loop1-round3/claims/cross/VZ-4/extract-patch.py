#!/usr/bin/env python3
"""VZ-4 patch extractor — pulls the diff body (or the payload block) out of a
*.patch.md artifact without trusting any prose claim inside it.

Extraction order:
  1. `<!-- payload-begin -->` … `<!-- payload-end -->` markers (payload text), else
  2. the first fenced block whose body starts with `--- `, `diff --git` or `@@ `
     (a unified diff), else
  3. the first fenced block whose info string is diff/patch/udiff/git-diff.

usage: extract-patch.py <patch.md> [payload|diff|--all]
"""
import re, sys

src = open(sys.argv[1]).read()
mode = sys.argv[2] if len(sys.argv) > 2 else 'diff'

payload = re.findall(r'<!-- payload-begin -->\n(.*?)\n<!-- payload-end -->', src, re.S)
fences = re.findall(r'```([^\n`]*)\n(.*?)```', src, re.S)
diffs = [b for info, b in fences if re.match(r'\s*(?:--- |diff --git|@@ )', b)]
info_named = [b for info, b in fences if info.strip() in ('diff', 'patch', 'udiff', 'git-diff')]

if mode == 'payload':
    body = payload[0] if payload else ''
    if not body:
        print('EXTRACT: no payload markers found', file=sys.stderr); sys.exit(2)
elif mode == '--all':
    body = ''.join(diffs or info_named)
else:
    body = (diffs or info_named or payload)
    body = body[0] if body else ''
if not body:
    print('EXTRACT: no diff or payload block found', file=sys.stderr)
    sys.exit(2)
sys.stdout.write(body if body.endswith('\n') else body + '\n')
print('EXTRACT: payload_markers=%d fences=%d diff_like=%d named=%d mode=%s bytes=%d'
      % (len(payload), len(fences), len(diffs), len(info_named), mode, len(body)), file=sys.stderr)