import sys, importlib.util
sys.dont_write_bytecode = True
S = '/fast/scratch/hyaku/kaidoku-r49/C1ScribeProvince'
W = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/C1ScribeProvince/'
spec = importlib.util.spec_from_file_location('c1c', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
prov = open(S+'/PROVINCE.base.md', encoding='utf8').read().rstrip('\n') + '\n\n' + open(W+'block-a.md', encoding='utf8').read().rstrip('\n') + '\n\n' + open(W+'block-b.md', encoding='utf8').read().rstrip('\n') + '\n'
rl = open(S+'/README.base.md', encoding='utf8').read().split('\n')
assert rl[103].startswith('| SquashFS v1/v2 through REA (round 44)'), rl[103][:60]
readme = '\n'.join(rl[:104] + [open(W+'block-c.md', encoding='utf8').read().rstrip('\n')] + rl[104:])
open(S+'/PROVINCE.composed.md','w',encoding='utf8').write(prov); open(S+'/README.composed.md','w',encoding='utf8').write(readme)
# province bindings, verbatim from c1-counter.py bindings block
sec = m.section(prov, m.CORE_HEADING)
print('province_core_section =', sec is not None)
rows_p = [l for l in (sec or []) if l.lstrip().startswith('|')]
print('province_core_row =', any('squashfs_v1' in r and 'squashfs_v2' in r and m.SQFS12_TEXT_RE.search(r) and m.ENTRY in r for r in rows_p))
print('frontier_note =', any(m.FRONTIER_MARK in l and m.STEM in l and m.SQFS12_TEXT_RE.search(l) for l in prov.splitlines()))
cm = m.section(readme, '## Coverage map')
print('coverage_map_row =', bool(cm) and any(m.STEM in l for l in cm if l.lstrip().startswith('|')))
print('coverage_map section rows containing STEM:', [l[:70] for l in cm if m.STEM in l])
print('Round-49 frontier note line:', [l[:90] for l in prov.splitlines() if m.FRONTIER_MARK in l])
