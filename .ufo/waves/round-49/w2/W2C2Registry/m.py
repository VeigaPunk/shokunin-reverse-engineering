import re,subprocess,shutil,os,sys,json
src=open('../c/corpus/SOURCES.md',encoding='utf-8').read().split('\n')
def idx(n): return next(i for i,l in enumerate(src) if l.startswith(f'| S{n} '))
def mut(name,fn):
    L=list(src); fn(L)
    d=f'm_{name}'; os.makedirs(d+'/corpus',exist_ok=True)
    # copy used-by paths needed
    for e in os.listdir('../c'):
        if e in ('.git','corpus'): continue
        os.symlink(os.path.abspath('../c/'+e),f'{d}/{e}')
    for e in os.listdir('../c/corpus'):
        if e=='SOURCES.md': continue
        os.symlink(os.path.abspath('../c/corpus/'+e),f'{d}/corpus/{e}')
    open(d+'/corpus/SOURCES.md','w',encoding='utf-8').write('\n'.join(L))
    return d
def cell(L,n,c,f):
    i=idx(n); p=L[i].split('|'); p[c-1]=f(p[c-1]); L[i]='|'.join(p)
M={
'M1_drop_pipe_S149': lambda L: L.__setitem__(idx(149), L[idx(149)].replace(' | on-request | — |',' on-request | — |')),
'M2_pipe_in_cell_S147': lambda L: cell(L,147,6,lambda s:s.replace('the lane','the | lane') if 'the lane' in s else s+' a | b'),
'M3_status_Mined_S148': lambda L: cell(L,148,9,lambda s:' Mined '),
'M4_community_tierA_S147': lambda L: cell(L,147,4,lambda s:' community '),
'M5_usedby_missing_S148': lambda L: cell(L,148,12,lambda s:' corpus/lessons/round-99.md '),
'M6_dup_id_S149_to_S148': lambda L: cell(L,149,2,lambda s:' S148 '),
'M7_sha_pin_flip_S147': lambda L: cell(L,147,7,lambda s:s.replace('2c2d48c6','2c2d48c7',1)),
'M8_recheck_bad_S147': lambda L: cell(L,147,11,lambda s:' tomorrow '),
'M9_opened_future_S148': lambda L: cell(L,148,10,lambda s:' 2027-01-01 '),
'M10_no_supersedes_S147': lambda L: cell(L,147,8,lambda s:s.replace('supersedes S145','follows S145')),
'M11_escaped_pipe_S149': lambda L: cell(L,149,8,lambda s:s.replace('REJECTED:','REJECTED \\| :')),
'M12_S145_tamper_locator': lambda L: cell(L,145,7,lambda s:s.replace('2. The Problem','3. The Problem')),
'M13_S149_status_to_mined_C_with_usedby': lambda L: cell(L,149,9,lambda s:' mined '),
'M14_S146_flip_to_mined': lambda L: cell(L,146,9,lambda s:' mined '),
'M15_snapshot_url_other_S148': lambda L: cell(L,148,3,lambda s:s.replace('3head.html','3head.htm')),
'M16_row_indented_4sp_S149': lambda L: L.__setitem__(idx(149),'    '+L[idx(149)]),
}
for k,f in M.items(): mut(k,f)
print(len(M))
