import sys,subprocess
D,variant=sys.argv[1:3]
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
lines=open(L+'/SKILL.md').read().split('\n')
assert lines[342].startswith('  | clean |'), lines[342][:30]
CIT='corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:11-28'
tbl=['  <!-- sqfs-triage-table v2 -->',
 '  <!-- action-vocabulary: rerun-with-dependency | rerun-with-be-wrapper | inspect-damage | expect-no-path | accept-metadata | none | stop-out-of-domain -->',
 '  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |',
 '  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
 '  | clean | `extract_firmware` | `unblob` | `squashfs_v4_*` | `none` | `none` | `n/a` | `no` | `>0` | `none` | dummy | S119 |']
if variant=='ok':   blk=['','- **SquashFS extract-firmware outcome triage v2 (round 40).** Dummy text',f'  (`{CIT}`).','']+tbl
elif variant=='bullets': blk=['','- **SquashFS triage v2 (round 40).** Dummy',f'  (`{CIT}`).','','  Action vocabulary:','  - **rerun-with-dependency** put binary on PATH','  - **none** nothing']+['']+tbl
elif variant=='badrange': blk=['','- **v2 dummy.** Dummy','  (`corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md:11-9999`).','']+tbl
elif variant=='nocite': blk=['','- **v2 dummy.** Dummy no citation','']+tbl
elif variant=='bullet_in_table_cell_comment': blk=['','- **v2 dummy.** Dummy',f'  (`{CIT}`).','','<!-- sqfs-triage-table v2 -->','<!-- action: x -->']+tbl[2:]
new=lines[:343]+blk+lines[343:]
open(D+'/SKILL.md','w').write('\n'.join(new))
