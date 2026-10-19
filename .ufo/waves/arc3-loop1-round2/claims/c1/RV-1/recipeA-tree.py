import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
files = {p.stem for p in (root/'corpus/knowledge').rglob('*.md')}
section = (root/'corpus/README.md').read_text().split('## Coverage map\n',1)[1].split('\n## ',1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = (root/'SKILL.md').read_text().split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
detail = []
for i, rule in enumerate(rules, 1):
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    bad = []
    for name, first, last in refs:
        p = root/'corpus/knowledge'/name
        try:
            count = len(p.read_text().splitlines())
            start, end = int(first or 1), int(last or first or 1)
            if not (1 <= start <= end <= count):
                valid = False; bad.append(f'{name}:{first}-{last} out-of-range({count})')
        except FileNotFoundError:
            valid = False; bad.append(f'{name} ABSENT')
    resolved += valid
    detail.append({'rule': i, 'refs': len(refs), 'valid': valid, 'bad': bad})
print(json.dumps({'mapped': len(files & mapped), 'knowledge_files': len(files),
 'missing': sorted(files - mapped), 'dangling': sorted(mapped - files),
 'citation_resolved_rules': resolved, 'rule_blocks': len(rules),
 'coverage_score': round(10*len(files & mapped)/len(files),2),
 'depth_score': round(10*resolved/len(rules),2),
 'rule_detail': detail}, sort_keys=True))
