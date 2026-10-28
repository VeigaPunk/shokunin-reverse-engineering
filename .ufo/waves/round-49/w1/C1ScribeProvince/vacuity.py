import sys, importlib.util
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('c1c', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c1-counter.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
# (1) frontier_note: line with stem only, no SquashFS v1/v2 words, claims nothing
line = 'Round-49 frontier note, 2026-10-28: `2026-10-28-r49-squashfs-v1v2-core` moved Frontier -> Core.'
print('V1 frontier note with NO squashfs-v1/v2 prose; stem alone:', bool(m.FRONTIER_MARK in line and m.STEM in line and m.SQFS12_TEXT_RE.search(line)), m.SQFS12_TEXT_RE.search(line).group(0))
line2 = 'Round-49 frontier note, 2026-10-28: `2026-10-28-r49-squashfs-v1v2-core` (nothing supersedes anything; SquashFS v1/v2 stays Frontier)'
print('V1b frontier note saying Frontier still:', bool(m.FRONTIER_MARK in line2 and m.STEM in line2 and m.SQFS12_TEXT_RE.search(line2)))
# (2) province_core_row: a row asserting the opposite (Frontier) passes
row = '| `squashfs_v1` and `squashfs_v2` (SquashFS v1 and v2) | still Frontier, NOT Core; see entry | - | `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` |'
print('V2 contrary Core row passes:', bool('squashfs_v1' in row and 'squashfs_v2' in row and m.SQFS12_TEXT_RE.search(row) and m.ENTRY in row))
print('V2 SQFS12 hit by entry path alone:', m.SQFS12_TEXT_RE.search(m.ENTRY).group(0))
# (3) SQFS12 token alone: squashfs-v1v2 stem inside ENTRY/STEM satisfies the token in any line
for lbl, s in [('stem', m.STEM), ('entry path', m.ENTRY)]:
    print('token from', lbl, '->', m.SQFS12_TEXT_RE.search(s).group(0))
