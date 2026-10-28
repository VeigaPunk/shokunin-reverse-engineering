import importlib.util, json, os, subprocess, copy, hashlib
exec(open('/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/harness.py').read().split("out={}")[0])
out={}
spec_at_F=json.loads(M.show(C,F,M.CARRIERS))
def mint_write_commit(branch, envs, msg):
    git('checkout','-q','-B',branch,F)
    ids=M.evidence_ids(C, F, PKG, {f'{i}/after':envs[i] for i in IDS}, S+'/w')
    for i in IDS:
        envs[i]['evidence_id']=ids[f'{i}/after'][1]
        os.makedirs(f'{C}/corpus/evidence/round-49/c1/{i}',exist_ok=True)
        json.dump(envs[i],open(f'{C}/corpus/evidence/round-49/c1/{i}/after.json','w'),indent=2)
    git('add','corpus/evidence/round-49'); git('commit','-q','-m',msg)
    return git('rev-parse','HEAD')
# ---- E3 freeze walk
git('checkout','-q','-B','e3add',F)
os.makedirs(C+'/tools/round-49',exist_ok=True)
open(C+'/tools/round-49/zz-added-after-freeze.txt','w').write('post-freeze addition\n')
git('add','tools/round-49/zz-added-after-freeze.txt'); git('commit','-q','-m','E3 add file under frozen directory')
e3add=git('rev-parse','HEAD')
git('checkout','-q','-B','e3mod',F)
open(C+'/tools/round-49/c1-counter.py','a').write('\n# post-freeze edit\n')
git('add','tools/round-49/c1-counter.py'); git('commit','-q','-m','E3 edit frozen counter')
e3mod=git('rev-parse','HEAD')
out['E3_frozen_drift_added_file']=M.frozen_drift(C,F,e3add,spec_at_F)
out['E3_frozen_drift_edited_counter']=M.frozen_drift(C,F,e3mod,spec_at_F)
out['E3_added_file_rev']=e3add
# ---- E4 non-removal diagnostic + unpublished entry, REA reproduces it (injected rerun == committed)
e4={}
for i in IDS:
    e=copy.deepcopy(ORIG[i]); nr=e['normalized_result']
    nr['diagnostics']=[{'report':{'__typename__':'ChunkSkipped'},'input_path':'$output/firmware.bin_extract'}]
    nr['unpublished_entries']=[{'kind':'fifo','relative_path':'firmware.bin_extract/fifo0'}]
    e4[i]=e
rev_e4=mint_write_commit('e4',copy.deepcopy(e4),'E4 non-removal diagnostic + fifo unpublished entry')
r=M.measure(C,rev_e4,F,PKG,rerun=inj(e4),target=4)
out['E4a_diag_reproduced_by_rea']={'summary':summ(r),'per':{i:{k:r['carriers'][i].get(k) for k in ('gaps_ok','gaps_note','projection_ok','matched','diagnostics')} for i in IDS}}
r=M.measure(C,rev_e4,F,PKG,rerun=inj(ORIG),target=4)
out['E4b_diag_not_reproduced']={'summary':summ(r)}
# ---- E4c structural depth-limited gap (control; plan-consistent red)
e4c={}
for i in IDS:
    e=copy.deepcopy(ORIG[i]); e['normalized_result']['extraction_gaps']=[{'kind':'depth-limited','relative_path':None,'dependencies':[]}]
    e4c[i]=e
rev_e4c=mint_write_commit('e4c',copy.deepcopy(e4c),'E4c depth-limited gap control')
r=M.measure(C,rev_e4c,F,PKG,rerun=inj(e4c),target=4)
out['E4c_depth_limited_control']={'summary':summ(r),'gaps_note':{i:r['carriers'][i].get('gaps_note') for i in IDS}}
# ---- E5 output_directory naming: committed evidence path inside scratch segment
e5={}
for i in IDS:
    e=copy.deepcopy(ORIG[i]); e['parameters']['output_directory']=f'/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/x/corpus/evidence/round-49/c1/{i}'
    e5[i]=e
rev_e5=mint_write_commit('e5',copy.deepcopy(e5),'E5 output_directory equals committed-path shape inside scratch')
r=M.measure(C,rev_e5,F,PKG,rerun=inj(ORIG),target=4)
out['E5_committed_path_in_scratch']={'summary':summ(r)}
out['E5_provenance_direct']={p:M.provenance_ok(p) for p in [
 '/fast/scratch/hyaku/kaidoku-r49/x/corpus/evidence/round-49/c1/v1le',
 '/tmp/kaidoku-r49/x',
 '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-49/c1/v1le/kaidoku-r49/x',
 '/fast/scratch/hyaku/kaidoku-r49/x/../y',
 'kaidoku-r49/x',
 '/fast/scratch/hyaku/kaidoku-r44/x']}
# ---- oracle independence re-open (unsquashfs 4.7.5 extraction vs frozen census)
import shutil
W=S+'/unsq'; shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
car=json.loads(M.show(C,F,M.CARRIERS))['carriers']
chk={}
for c in car:
    raw=open(LANE+'/'+c['path'],'rb').read()
    magic=raw[:4]
    d=f"{W}/{c['id']}"
    r=subprocess.run(['/usr/bin/unsquashfs','-d',d,LANE+'/'+c['path']],capture_output=True,text=True)
    members=[]
    for root_,dirs,files in os.walk(d):
        for f in files:
            p=os.path.join(root_,f); rel=os.path.relpath(p,d)
            members.append((rel, hashlib.sha256(open(p,'rb').read()).hexdigest(), os.path.getsize(p)))
    members.sort()
    frozen=sorted(((m.get('path') or '').replace('squashfs-root/',''),m.get('sha256'),m.get('size')) for m in c['oracle']['members'])
    census_rows=[(x['rel'],x['size']) for x in c['oracle']['census'] if x['type']=='regular']
    digest=hashlib.sha256(''.join(f'{p}\t{h}\n' for p,h,_ in sorted(members)).encode()).hexdigest()
    chk[c['id']]={'magic':magic.decode('latin1'),'unsquashfs_exit':r.returncode,'live_regular':[(p,s) for p,_,s in members],
                  'frozen_census_regular':census_rows,'census_matches_live':sorted(census_rows)==sorted((p,s) for p,_,s in members),
                  'live_tree_digest':digest,'frozen_members_match_live': sorted(frozen)==sorted(members), 'frozen_member_rows': len(frozen), 'frozen_tree_digest': c.get('output_tree') if not isinstance(c.get('output_tree'),dict) else c['output_tree'].get('digest'),
                  'oracle_keys':sorted(c['oracle'].keys()), 'carrier_sha256_ok': hashlib.sha256(raw).hexdigest()==c['sha256'],
                  'magic_expected': {'le':'hsqs','be':'sqsh'}[c['endian']] }
out['oracle_recheck']=chk
json.dump(out,open(S+'/results2.json','w'),indent=1,sort_keys=True,default=str)
print(json.dumps(out,indent=1,sort_keys=True,default=str)[:12000])
