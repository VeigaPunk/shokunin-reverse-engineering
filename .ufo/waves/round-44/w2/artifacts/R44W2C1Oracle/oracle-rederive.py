import json, hashlib, os
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'; S='/fast/scratch/hyaku/kaidoku-r44/w2-R44W2C1Oracle'
C=json.load(open(f'{L}/tools/round-44/carriers.json')); car={c['id']:c for c in C['carriers']}
def sh(p):
    h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()
def tree(root): return sorted((os.path.relpath(os.path.join(dp,f),root), sh(os.path.join(dp,f)), os.path.getsize(os.path.join(dp,f))) for dp,dn,fn in os.walk(root) for f in fn)
out={}
for cid in ('v1le','v1be','v2le','v2be'):
    c=car[cid]; o=c['oracle']; row={}
    frozen_members=sorted((m['path'],m['sha256'],m['size']) for m in o['members'])
    mine=tree(f'{S}/x/{cid}/root'); seven=tree(f'{S}/z/{cid}/out')
    row['image_sha_ok']=sh(f"{L}/{c['path']}")==c['sha256'] and os.path.getsize(f"{L}/{c['path']}")==c['size']
    row['lls_stdout_sha_ok']=sh(f'{S}/x/{cid}/lls.out')==o['listing']['stdout_sha256']
    row['s_stdout_sha_ok']=sh(f'{S}/x/{cid}/s.out')==o['superblock_info']['stdout_sha256']
    row['extract_stdout_sha_ok']=sh(f'{S}/x/{cid}/extract.out')==o['extraction']['stdout_sha256']
    row['unsquashfs_members_eq_frozen']=mine==frozen_members
    row['sevenzip_members_eq_frozen']=seven==frozen_members
    row['committed_extract_eq_frozen']=tree(f"{L}/corpus/evidence/round-44/c1/{cid}/firmware.bin_extract")==frozen_members
    orc_root=f"{L}/corpus/evidence/round-44/oracle/{o['output_tree']['root'].split('corpus/evidence/round-44/oracle/')[1]}"
    row['oracle_tree_eq_frozen']=tree(orc_root)==frozen_members
    blob=''.join(f"{p}\t{h}\n" for p,h,s in sorted(mine))
    row['digest_recomputed']=hashlib.sha256(blob.encode()).hexdigest(); row['digest_frozen']=c['oracle']['output_tree_digest']
    row['digest_ok']=row['digest_recomputed']==row['digest_frozen']
    a=json.load(open(f"{L}/corpus/evidence/round-44/c1/{cid}/after.json")); nr=a['normalized_result']
    files=sorted((f['relative_path'].split('/',1)[1], f['sha256'], f['size']) for f in nr['files'])
    seq=[e for g in a['raw_result']['report'] for e in g['reports']]
    raw=[]; pend=None
    for e in seq:
        t=e.get('__typename__')
        if t=='StatReport' and e.get('is_file') and '/firmware.bin_extract/' in (e.get('path') or ''):
            pend=e
        elif t=='HashReport' and pend is not None:
            raw.append((pend['path'].split('/firmware.bin_extract/',1)[1], e['sha256'], pend['size'])); pend=None
    raw=sorted(raw)
    row['after_files_eq_frozen']=files==frozen_members
    row['raw_report_files_eq_frozen']=raw==frozen_members
    row['after_and_raw_agree']=files==raw
    row['gaps']=nr.get('extraction_gaps'); row['unpublished']=nr.get('unpublished_entries'); row['diagnostics']=nr.get('diagnostics')
    row['chunk']=[(x['handler'],x['extraction_failed'],x['encrypted']) for x in nr['chunks']]
    row['outdir']=a['parameters']['output_directory']
    row['members']=mine
    out[cid]=row
json.dump(out,open(f'{S}/table.json','w'),indent=1)
keys=[k for k in out['v1le'] if k not in ('members','digest_recomputed','digest_frozen')]
print('%-22s'%'check', ' | '.join(out))
for k in keys:
    print('%-22s'%k, ' | '.join(str(out[c][k])[:60] for c in out))
