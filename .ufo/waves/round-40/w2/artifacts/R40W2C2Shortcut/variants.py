import json, os, sys, tempfile
sys.path.insert(0,'.')
from harness import *

work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work); dev=materialize('dev',work)

MIN=[
 row('no-squashfs-chunk', op='extract_firmware', h='none', action='inspect-input'),
 row('dep-missing-be', d='sasquatch-v4be', action='install-extractor-be'),
 row('dep-missing-le', d='sasquatch', action='install-extractor-le'),
 row('avm-marker-be-dropped', be='no', action='wrap-extractor-be'),
 row('body-extractor-failure', be='yes', files='0', action='preserve-failure'),
 row('partial-body-failure', g='extractor-failure', files='>0', action='salvage-partial'),
 row('mixed-symlinks', g='unpublished-entry', sr='yes', action='audit-symlinks'),
 row('in-tree-symlink-metadata', g='unpublished-entry', sr='no', action='count-gap'),
 row('escaping-symlink-removed', g='none', sr='yes', action='expect-link-absent'),
 row('clean', g='none', sr='no', files='>0', action='none'),
 row('clean-empty', h='squashfs_v4_*', g='none', files='0', action='confirm-empty'),
]
def cells(rows):
    return sum(1 for r in rows for c in r[1:9] if c!='*')
print('MIN cells',cells(MIN))

# 6-column variant: dependencies dropped, handler splits dep rows; provider guard instead of operation
MIN6=[
 row('no-squashfs-chunk', pv='unblob', h='none', action='inspect-input'),
 row('dep-missing-be', h='squashfs_v4_be', g='missing-extractor-dependency', action='install-extractor-be'),
 row('dep-missing-le', h='squashfs_v4_le', g='missing-extractor-dependency', action='install-extractor-le'),
 row('avm-marker-be-dropped', be='no', action='wrap-extractor-be'),
 row('body-extractor-failure', be='yes', files='0', action='preserve-failure'),
 row('partial-body-failure', g='extractor-failure', files='>0', action='salvage-partial'),
 row('mixed-symlinks', g='unpublished-entry', sr='yes', action='audit-symlinks'),
 row('in-tree-symlink-metadata', g='unpublished-entry', sr='no', action='count-gap'),
 row('escaping-symlink-removed', g='none', sr='yes', action='expect-link-absent'),
 row('clean', g='none', sr='no', files='>0', action='none'),
 row('clean-empty', h='squashfs_v4_*', g='none', files='0', action='confirm-empty'),
]
print('MIN6 cells',cells(MIN6))
for name,rows in (('MIN',MIN),('MIN6',MIN6)):
    sk=skill_file(rows, os.path.join(work,'sk-'+name+'.md'))
    for which,envs in (('held',held),('dev',dev)):
        r=score(sk,envs)
        print('%-5s %-5s exit=%d matched=%d/%d wrong=%s err=%s'%(name,which,r['exit'],r['matched'],r['n'],r['wrong'],r['stderr'][:120]))
# baseline: committed SKILL
r=score(LANE+'/SKILL.md',held); print('committed held exit=%d matched=%d/%d'%(r['exit'],r['matched'],r['n']))
r=score(LANE+'/SKILL.md',dev); print('committed dev  exit=%d matched=%d/%d'%(r['exit'],r['matched'],r['n']))
json.dump({'work':work,'min_cells':cells(MIN),'min6_cells':cells(MIN6)},open('variants.json','w'))
