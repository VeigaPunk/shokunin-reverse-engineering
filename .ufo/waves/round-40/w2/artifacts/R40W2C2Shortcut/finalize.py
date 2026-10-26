import json, os, sys, subprocess, hashlib, tempfile
sys.path.insert(0,'.')
from harness import *
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
OUT=LANE+'/.ufo/waves/round-40/w2/artifacts/R40W2C2Shortcut'
os.makedirs(OUT,exist_ok=True)
work=tempfile.mkdtemp(dir='/fast/scratch/hyaku/kaidoku-r40/R40W2C2Shortcut')
held=materialize('held',work); dev=materialize('dev',work)
COLS=['operation','provider','handler','gap kinds','dependencies','-be in child argv','symlink removed','published files']
MIN=[
 row('no-squashfs-chunk', op='extract_firmware', h='none', action='inspect-input',
     cause='no squashfs handler ran on any chunk -> inspect the magic and superblock'),
 row('dep-missing-be', d='sasquatch-v4be', action='install-extractor-be',
     cause='the BE v4 handler lost sasquatch-v4be from the child PATH -> install it and rerun'),
 row('dep-missing-le', d='sasquatch', action='install-extractor-le',
     cause='the LE v4 handler lost sasquatch from the child PATH -> install it and rerun'),
 row('avm-marker-be-dropped', be='no', action='wrap-extractor-be',
     cause='the recorded sasquatch argv has no -be, so the AVM marker handshake dropped it -> wrap the extractor and append -be'),
 row('body-extractor-failure', be='yes', files='0', action='preserve-failure',
     cause='the extractor ran with the recorded argv and failed publishing nothing -> keep the failing command'),
 row('partial-body-failure', g='extractor-failure', files='>0', action='salvage-partial',
     cause='the extractor failed after publishing files -> keep them and mark the run incomplete'),
 row('mixed-symlinks', g='unpublished-entry', sr='yes', action='audit-symlinks',
     cause='removed links and unpublished entries in one envelope -> audit both kinds'),
 row('in-tree-symlink-metadata', g='unpublished-entry', sr='no', action='count-gap',
     cause='every non-file entry stayed in-tree as one gap each -> count them, install nothing'),
 row('escaping-symlink-removed', g='none', sr='yes', action='expect-link-absent',
     cause='a link escaped the root and was removed with no gap recorded -> expect it absent'),
 row('clean', g='none', sr='no', files='>0', action='none',
     cause='every regular file published, no gap, no link removed -> nothing to fix'),
 row('clean-empty', h='squashfs_v4_*', g='none', files='0', action='confirm-empty',
     cause='the extractor completed with no gap and the image tree holds no regular file -> confirm the oracle is empty'),
]
MIN6=[
 row('no-squashfs-chunk', pv='unblob', h='none', action='inspect-input', cause='no squashfs chunk -> inspect input'),
 row('dep-missing-be', h='squashfs_v4_be', g='missing-extractor-dependency', action='install-extractor-be',
     cause='BE v4 handler without its extractor binary -> install sasquatch-v4be'),
 row('dep-missing-le', h='squashfs_v4_le', g='missing-extractor-dependency', action='install-extractor-le',
     cause='LE v4 handler without its extractor binary -> install sasquatch'),
 row('avm-marker-be-dropped', be='no', action='wrap-extractor-be', cause='argv without -be -> wrap and rerun'),
 row('body-extractor-failure', be='yes', files='0', action='preserve-failure', cause='ran and failed, nothing published -> preserve'),
 row('partial-body-failure', g='extractor-failure', files='>0', action='salvage-partial', cause='failed after publishing -> salvage'),
 row('mixed-symlinks', g='unpublished-entry', sr='yes', action='audit-symlinks', cause='both link outcomes -> audit'),
 row('in-tree-symlink-metadata', g='unpublished-entry', sr='no', action='count-gap', cause='in-tree entries only -> count gaps'),
 row('escaping-symlink-removed', g='none', sr='yes', action='expect-link-absent', cause='link removed, no gap -> expect absent'),
 row('clean', g='none', sr='no', files='>0', action='none', cause='no gap, files published -> clean'),
 row('clean-empty', h='squashfs_v4_*', g='none', files='0', action='confirm-empty', cause='no gap, no files -> confirm empty'),
]
def nz(rows):
    per={c:0 for c in COLS}; tot=0
    for r in rows:
        for c,v in zip(COLS,r[1:9]):
            if v!='*': per[c]+=1; tot+=1
    return tot,per
def emit(rows,name,tag):
    sk=skill_file(rows, os.path.join(work,name+'.md'))
    rep={}
    for which,envs in (('heldout',held),('dev',dev)):
        r=score(sk,envs); rep[which]={'exit':r['exit'],'matched':r['matched'],'n':r['n'],'wrong':r['wrong']}
    print(name, nz(rows), rep)
    # artifact copy of the block only
    text=open(sk).read()
    blk=text.split('<!-- sqfs-triage-table v2 -->')[1]
    open(os.path.join(OUT,name+'.md'),'w').write('<!-- sqfs-triage-table v2 -->'+blk)
    return rep
reps={'min21':emit(MIN,'min-v2-table-21cells','w2-min'),
      'min23':emit(MIN6,'min6-v2-table-23cells','w2-min6')}
json.dump({'min21':{'cells':nz(MIN)[0],'per_column':nz(MIN)[1],'scores':reps['min21']},
           'min23':{'cells':nz(MIN6)[0],'per_column':nz(MIN6)[1],'scores':reps['min23']}},
          open(os.path.join(OUT,'minimal-tables.json'),'w'),indent=1)
