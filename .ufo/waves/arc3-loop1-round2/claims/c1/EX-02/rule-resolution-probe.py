#!/usr/bin/env python3
"""Command A's citation-resolution test applied to candidate rule #14 texts,
inserted into a scratch SKILL.md copy. Usage: rule-resolution-probe.py <block-file> [label]"""
import pathlib, re, shutil, subprocess, sys, json, hashlib
W = pathlib.Path('/var/tmp/ex02-dryrun')
block = pathlib.Path(sys.argv[1]).read_text().rstrip("\n") + "\n"
label = sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(sys.argv[1]).stem
work = W / f'tree-cand-{label}'
if work.exists(): shutil.rmtree(work)
shutil.copytree(W / 'tree', work)
p = work / 'SKILL.md'
text = p.read_text(); MARKER = "## Config custody for live-probe rounds (SOP)"
head, tail = text.split(MARKER, 1)
p.write_text(head.rstrip("\n") + "\n\n" + block + "\n" + MARKER + tail)
def get(path): return (work / path).read_text()
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0; detail = []
for i, rule in enumerate(rules, 1):
    refs = re.findall(pattern, rule); valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except FileNotFoundError:
            valid = False
    resolved += valid
    if i >= len(rules) - 1: detail.append({'rule': i, 'refs': refs, 'resolved': valid})
print(json.dumps({'label': label, 'block_sha256': hashlib.sha256(block.encode()).hexdigest(),
  'rule_blocks': len(rules), 'citation_resolved_rules': resolved,
  'depth_score': round(10*resolved/len(rules), 2), 'last_rule_detail': detail}, sort_keys=True))
