#!/usr/bin/env python3
"""VZ-4 C1 landing projection — builds the after-state PROJECTION on a scratch
mirror from the chain's draft artifacts, without touching corpus/.

  mirror  = copy of corpus/knowledge/*.md + corpus/README.md + SKILL.md
  entry   = literal text between BEGIN/END LITERAL ENTRY TEXT in the draft
  map     = the PRIMARY (or HONEST-STOP) new row line substituted at :38

Then it re-derives: entry bytes/sha/line count, README line count and the
changed-line count, and prints the command-A tree-mode call for the caller.
usage: c1-project.py <draft.md> <map-patch.md> <mirror-root> [primary|honest-stop]
"""
import hashlib, pathlib, re, subprocess, sys

draft = pathlib.Path(sys.argv[1]); mapf = pathlib.Path(sys.argv[2])
mirror = pathlib.Path(sys.argv[3]); form = sys.argv[4] if len(sys.argv) > 4 else 'primary'

dtext = draft.read_text()
m = re.search(r'<!-- BEGIN LITERAL ENTRY TEXT -->\n(.*?)<!-- END LITERAL ENTRY TEXT -->', dtext, re.S)
if not m:
    print('PROJECT: no literal entry block in draft', file=sys.stderr); sys.exit(2)
entry = m.group(1)
stem_m = re.search(r'landing stem:?\s*`?([a-z0-9-]+)`?', dtext) or re.search(r'`(2026-10-19-arc3-r3-[a-z-]+)`', dtext)
stem = stem_m.group(1) if stem_m else '2026-10-19-arc3-r3-evm-optimizer-shapes'
edir = mirror / 'corpus/knowledge'; edir.mkdir(parents=True, exist_ok=True)
efile = edir / (stem + '.md')
efile.write_text(entry)
print(f"ENTRY stem={stem} bytes={len(entry.encode())} lines={entry.count(chr(10))} sha256={hashlib.sha256(entry.encode()).hexdigest()}")

mtext = mapf.read_text()
hdr = 'PRIMARY' if form == 'primary' else 'HONEST-STOP'
mm = re.search(r'## New line — ' + hdr + r'[^\n]*\n+```\n(.*?)\n```', mtext, re.S)
if not mm:
    print(f'PROJECT: no {hdr} row block in map patch', file=sys.stderr); sys.exit(2)
newline = mm.group(1)

readme = mirror / 'corpus/README.md'
lines = readme.read_text().splitlines(keepends=True)
idx = None
for i, l in enumerate(lines):
    if l.startswith('| EVM |'):
        idx = i; break
if idx is None:
    print('PROJECT: no EVM row in README', file=sys.stderr); sys.exit(2)
old = lines[idx]
lines[idx] = newline + '\n'
readme.write_text(''.join(lines))
print(f"README EVM row at file line {idx+1}; lines before/after = {len(old.splitlines())}→{len(lines)}")
print(f"OLD {old.rstrip()[:120]}")
print(f"NEW {newline.rstrip()[:120]}")
print(f"README sha256 after={hashlib.sha256(readme.read_bytes()).hexdigest()} lines={len(readme.read_text().splitlines())}")
print(f"PROJECT: apply-time identities bound to draft sha256={hashlib.sha256(dtext.encode()).hexdigest()} "
      f"map sha256={hashlib.sha256(mtext.encode()).hexdigest()}")