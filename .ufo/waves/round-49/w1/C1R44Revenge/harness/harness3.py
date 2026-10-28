import importlib.util, json, os, subprocess, copy, shutil
exec(open('/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/harness.py').read().split("out={}")[0])
A='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/artifacts'
out={}
def mint_write_commit(branch, envs, msg, base=F):
    git('checkout','-q','-B',branch,base)
    ids=M.evidence_ids(C, F, PKG, {f'{i}/after':envs[i] for i in IDS}, S+'/w')
    for i in IDS:
        envs[i]['evidence_id']=ids[f'{i}/after'][1]
        os.makedirs(f'{C}/corpus/evidence/round-49/c1/{i}',exist_ok=True)
        json.dump(envs[i],open(f'{C}/corpus/evidence/round-49/c1/{i}/after.json','w'),indent=2)
    git('add','corpus/evidence/round-49'); git('commit','-q','-m',msg)
    return git('rev-parse','HEAD')
def perdet(r,keys=('run_provenance_ok','gaps_ok','projection_ok','evidence_id_ok','matched')):
    return {i:{k:r['carriers'][i].get(k) for k in keys} for i in IDS}
# A. E4 with the provenance field fixed to the round-49 scratch segment
e4={}
for i in IDS:
    e=copy.deepcopy(ORIG[i]); nr=e['normalized_result']
    e['parameters']['output_directory']=f'/fast/scratch/hyaku/kaidoku-r49/C1R44Revenge/e4/{i}/rea-out'
    nr['diagnostics']=[{'report':{'__typename__':'ChunkSkipped'},'input_path':'$output/firmware.bin_extract'}]
    nr['unpublished_entries']=[{'kind':'fifo','relative_path':'firmware.bin_extract/fifo0'}]
    e4[i]=e
rev=mint_write_commit('e4b',copy.deepcopy(e4),'E4b diag + fifo, provenance fixed')
r=M.measure(C,rev,F,PKG,rerun=inj(e4),target=4)
out['A_diag_fifo_reproduced']={'summary':summ(r),'per':perdet(r)}
r=M.measure(C,rev,F,PKG,rerun=inj(ORIG),target=4)
out['A_diag_fifo_not_reproduced']={'summary':summ(r),'per':perdet(r)}
# B. plan's CTL-C1-4 shape (plain copy), which clause fails
r=M.measure(C,git('rev-parse','plainE2'),F,PKG,rerun=inj(ORIG),target=4)
out['B_plain_copy_clauses']={i:[k for k in M.CLAUSES if r['carriers'][i].get(k) is False] for i in IDS}
# C. forged receipts + landing blocks -> met_target?
git('checkout','-q','-B','met',git('rev-parse','9eb3b8d77211'))
prov=open(C+'/PROVINCE.md').read()
blockA=open(A+'/R49C1Doc/block-a-province-round-49-core-row.md').read()
blockB=open(A+'/R49C1Doc/block-b-province-frontier-note.md').read()
open(C+'/PROVINCE.md','w').write(prov.rstrip('\n')+'\n\n'+blockA.rstrip('\n')+'\n\n'+blockB.rstrip('\n')+'\n')
readme=open(C+'/corpus/README.md').read().split('\n')
si=readme.index('## Coverage map'); last=si
for j in range(si+1,len(readme)):
    if readme[j].startswith('## '): break
    if readme[j].lstrip().startswith('|'): last=j
rowC=[l for l in open(A+'/R49C1Doc/block-c-readme-coverage-map-row.md').read().split('\n') if l.lstrip().startswith('|') and 'Surface' not in l][0]
readme.insert(last+1,rowC)
open(C+'/corpus/README.md','w').write('\n'.join(readme))
os.makedirs(C+'/corpus/knowledge',exist_ok=True)
shutil.copy(A+'/R49EntryDraft/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md', C+'/corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md')
sr=open(C+'/corpus/SOURCES.md').read().split('\n'); n=0
for k,l in enumerate(sr):
    if l.startswith('| S138 ') or l.startswith('| S139 '):
        parts=l.split('|')
        parts[11]=' corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md, corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md '
        sr[k]='|'.join(parts); n+=1
assert n==2, n
open(C+'/corpus/SOURCES.md','w').write('\n'.join(sr))
git('add','-A','PROVINCE.md','corpus'); git('commit','-q','-m','met-attack: landing blocks over forged relabel receipts')
metrev=git('rev-parse','HEAD'); out['C_met_rev']=metrev
r=M.measure(C,metrev,F,PKG,rerun=inj(ORIG),target=4)
out['C_met_injected']={'summary':summ(r),'bindings':r['bindings'] and {k:v for k,v in r['bindings'].items() if k in M.BINDINGS},'met_target':r['met_target'],'exit_would_be':0 if r['met_target'] else 1}
json.dump(out,open(S+'/results3.json','w'),indent=1,sort_keys=True,default=str)
print(json.dumps(out,indent=1,sort_keys=True,default=str)[:6000])
