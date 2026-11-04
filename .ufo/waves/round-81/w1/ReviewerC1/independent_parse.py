import argparse, collections, hashlib, json, pathlib, re, subprocess
p = argparse.ArgumentParser()
p.add_argument('--root', required=True)
p.add_argument('--rev', required=True)
p.add_argument('--work', required=True)
p.add_argument('--out', required=True)
a = p.parse_args()
assert pathlib.Path(a.work).is_dir()
def blob(path):
    return subprocess.check_output(['git', '-C', a.root, 'show', a.rev + ':' + path])
text = blob('SKILL.md').decode()
start = text.index('<!-- instrument-registry v2 -->')
end = text.index('<!-- /instrument-registry -->', start)
legacy = {'tools/round-69/' + n + '.py' for n in ('packed-elf', 'mutation-check', 'contract-probe', 'controls')}
rows = []
for n, line in enumerate(text[:end].splitlines(), 1):
    if n <= text[:start].count('\n') + 1 or not line.startswith('| `tools/'):
        continue
    cells = [c.strip().replace('\\|', '|') for c in re.split(r'(?<!\\)\|', line.strip()[1:-1])]
    path = cells[0].strip('`')
    errors = []
    if len(cells) != 7 and not (path in legacy and len(cells) == 8):
        errors.append('cells>7' if len(cells) > 7 else 'pinned-empty')
    exists = subprocess.run(['git', '-C', a.root, 'cat-file', '-e', a.rev + ':' + path], capture_output=True).returncode == 0
    if not exists:
        errors.append('path-absent')
    rows.append(dict(path=path, file_line=n, cells=cells, count=len(cells), errors=errors))
freq = collections.Counter(r['path'] for r in rows)
out = dict(rev=a.rev, parser='independent regex negative-lookbehind; no counter import', limits='Not a general GFM renderer; consecutive backslashes require separate semantic inspection.', rows=len(rows), paths=len(freq), histogram=dict(collections.Counter(r['count'] for r in rows)), duplicates=[k for k,v in freq.items() if v>1], nonconformant=[r for r in rows if r['errors']], legacy=[r for r in rows if r['path'] in legacy], all_paths=sorted(freq), counter_sha256=hashlib.sha256(blob('tools/round-71/registry-census.py')).hexdigest())
pathlib.Path(a.out).write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k:out[k] for k in ('rows','paths','histogram','duplicates','counter_sha256')}))
print('nonconformant', [(r['path'], r['count'], r['errors']) for r in out['nonconformant']])
print('legacy', [(r['path'], r['count']) for r in out['legacy']])
print('do_nothing_meets_target', not out['nonconformant'])
