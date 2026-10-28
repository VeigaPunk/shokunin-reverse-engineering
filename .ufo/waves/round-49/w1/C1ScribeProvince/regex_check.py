import sys, re, importlib.util, subprocess
sys.dont_write_bytecode = True
DRAFT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py'
spec = importlib.util.spec_from_file_location('c1c', DRAFT)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
W = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts/R49C1Doc/'
A = open(W+'block-a-province-round-49-core-row.md', encoding='utf8').read()
Bb = open(W+'block-b-province-frontier-note.md', encoding='utf8').read()
C = open(W+'block-c-readme-coverage-map-row.md', encoding='utf8').read()
print('CONSTANTS', m.CORE_HEADING, '|', m.FRONTIER_MARK, '|', m.STEM, '|', m.ENTRY)
print('SQFS12_TEXT_RE pattern =', m.SQFS12_TEXT_RE.pattern)
# province_core_section + province_core_row, exactly as bindings do (section(), lines starting '|')
prov = m.B if False else None
sec_lines = A.splitlines()
sec = m.section('\n'.join(['# x', '', *sec_lines]), m.CORE_HEADING)
print('section found:', sec is not None, 'lines:', len(sec or []))
rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
for r in rows:
    print('ROW cells[0]=', m.cells(r)[0][:60], '| n_cells=', len(m.cells(r)))
    print('  squashfs_v1 in row:', 'squashfs_v1' in r, '| squashfs_v2 in row:', 'squashfs_v2' in r)
    mt = m.SQFS12_TEXT_RE.search(r); print('  SQFS12 match:', repr(mt.group(0)) if mt else None, 'at', mt.span() if mt else None)
    print('  ENTRY in row:', m.ENTRY in r)
print('province_core_row =', any('squashfs_v1' in r and 'squashfs_v2' in r and m.SQFS12_TEXT_RE.search(r) and m.ENTRY in r for r in rows))
# frontier_note: any line in PROVINCE text (here block-b as the only line)
fn = [l for l in Bb.splitlines() if m.FRONTIER_MARK in l and m.STEM in l and m.SQFS12_TEXT_RE.search(l)]
print('frontier_note lines matched =', len(fn), '| match:', [m.SQFS12_TEXT_RE.search(l).group(0) for l in fn])
# coverage_map_row: README section
readme = '# R\n\n## Coverage map\n\n' + C + '\n\n## Knowledge\n'
cm = m.section(readme, '## Coverage map')
hits = [l for l in cm if l.lstrip().startswith('|') and m.STEM in l]
print('coverage_map_row =', bool(cm) and bool(hits), '| cells:', [len(m.cells(h)) for h in hits])
print('block-c cells:', [m.cells(l)[0] for l in C.splitlines() if l.startswith('|')], len(m.cells(C.splitlines()[0])))
print('AFTER-DATA markers:', re.findall(r'<AFTER-DATA[^>]*>', A+Bb+C))
