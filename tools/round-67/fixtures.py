#!/usr/bin/env python3
"""Reviewer-owned construction oracle; no candidate imports or ELF reparsing."""
import hashlib,json,pathlib,struct,sys
H=lambda b:hashlib.sha256(b).hexdigest()
U=2**64

def main(out,salt):
 out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False);cases={};seed=hashlib.sha256(salt.encode()).digest();v=0x4000+seed[0]*32;sv=v+0x2000;do=1024;so=4096;word=b'lib'+seed[:5].hex().encode()+b'.so';table=b'\0'+word+b'\0tail\0';base=[(5,sv),(1,1),(10,len(table)),(0,0)]
 def seg(t,o,a,n,m=None):return [t,4,o,a,0,n,n if m is None else m,1]
 def make(entries=None,tab=None,loads=None,dyn=None,extra=None,patch=None):
  entries=base[:] if entries is None else entries;tab=table if tab is None else tab
  loads=[seg(1,do,v,len(entries)*16),seg(1,so,sv,len(tab))] if loads is None else loads
  dyn=seg(2,do,v,len(entries)*16) if dyn is None else dyn;ss=loads+([dyn] if dyn else [])+(extra or [])
  b=bytearray((seed*384)[:12288]);b[:64]=struct.pack('<16sHHIQQQIHHHHHH',b'\x7fELF'+bytes([2,1,1])+bytes(9),3,62,1,0,64,0,0,64,56,len(ss),0,0,0)
  for i,s in enumerate(ss):struct.pack_into('<IIQQQQQQ',b,64+i*56,*s)
  for i,(tag,val) in enumerate(entries):struct.pack_into('<qQ',b,do+16*i,tag,val)
  # Explicit construction assignment to virtual table locations, not parsing subject headers.
  for j,value in enumerate(tab):
   for s in loads:
    if s[0]==1 and s[3]<=sv+j<s[3]+s[5] and s[2]+sv+j-s[3]<len(b):b[s[2]+sv+j-s[3]]=value
  if patch:patch(b)
  return bytes(b),ss,entries,tab
 def expected(b,ss,entries,tab):
  di=next(i for i,s in enumerate(ss) if s[0]==2);d=ss[di];end=next(i for i,e in enumerate(entries) if e[0]==0);ns=[]
  for i,(t,k) in enumerate(entries[:end]):
   if t!=1:continue
   z=tab.index(0,k);orig=[]
   for j in range(k,z+1):
    idx,s=next((idx,s) for idx,s in enumerate(ss) if s[0]==1 and s[3]<=sv+j<s[3]+s[5]);o=s[2]+sv+j-s[3]
    if orig and orig[-1]['load_ordinal']==idx and orig[-1]['file_offset']+orig[-1]['length']==o:orig[-1]['length']+=1
    else:orig.append(dict(load_ordinal=idx,file_offset=o,length=1))
   ns.append(dict(dynamic_index=i,entry_offset=do+16*i,string_offset=k,name_hex=tab[k:z].hex(),origins=orig))
  return dict(schema=1,exit=0,finding='complete',elf_sha256=H(b),elf_size=len(b),dynamic=dict(ordinal=di,file_offset=d[2],vaddr=d[3],size=d[5],terminator_index=end),strtab=dict(vaddr=sv,size=len(tab)),needed=ns)
 def put(name,args=None,reason=None,code=1):
  b,ss,es,tab=make(**(args or {}));e=expected(b,ss,es,tab) if reason is None else dict(schema=1,exit=code,finding=reason);(out/(name+'.elf')).write_bytes(b);cases[name]=dict(exit=e['exit'],elf_sha256=H(b),output=e)
 put('ordinary')
 put('duplicate_occurrences',dict(entries=[(1,1),(5,sv),(1,1),(10,len(table)),(0,0)]))
 put('substring_reference',dict(entries=[(5,sv),(10,len(table)),(1,4),(0,0)]))
 put('empty_names',dict(entries=[(5,sv),(10,len(table)),(1,0),(1,len(table)-1),(0,0)]))
 put('raw_nonutf8',dict(tab=b'\0\xff\x80\0',entries=[(5,sv),(10,4),(1,1),(0,0)]))
 put('ordered_unsorted',dict(entries=[(5,sv),(10,len(table)),(1,len(word)+2),(1,1),(0,0)]))
 put('no_needed',dict(entries=[(5,sv),(10,len(table)),(0,0)]))
 put('ignored_unknown_tags',dict(entries=[(-7,U-1),(5,sv),(10,len(table)),(1,1),(0,0)]))
 put('post_null_decoys',dict(entries=base+[(5,U-1),(1,U-1),(10,0)]))
 put('ignored_sections',dict(patch=lambda b:struct.pack_into('<Q',b,40,U-1)))
 for label,cut in [('prefix',1),('middle',5),('terminator',len(table)-1)]:
  put('split_table_'+label,dict(loads=[seg(1,do,v,64),seg(1,so,sv,cut),seg(1,6000,sv+cut,len(table)-cut)]))
 put('split_dynamic',dict(loads=[seg(1,do,v,23),seg(1,do+23,v+23,41),seg(1,so,sv,len(table))]))
 put('dynamic_ordinal_nonload',dict(loads=[seg(4,0,0,0),seg(1,do,v,64),seg(1,so,sv,len(table))]))
 # Exact accepted resource edges and NUL itself at a distinct physical origin.
 bigtab=b'\0'+word+b'\0'+b'Q'*(4096-len(word)-3)+b'\0'
 put('strtab_exact_budget',dict(tab=bigtab,entries=[(5,sv),(10,4096),(1,4095),(0,0)]))
 longentries=[(5,sv),(10,len(table)),(1,1)]+[(99,0)]*252+[(0,0)]
 put('dynamic_exact_budget',dict(entries=longentries,loads=[seg(1,do,v,4096),seg(1,6000,sv,len(table))]))
 cut=len(word)+1
 put('name_nul_crosses_origin',dict(loads=[seg(1,do,v,64),seg(1,so,sv,cut),seg(1,6000,sv+cut,len(table)-cut)]))
 # Explicit one-defect negative constructions. Validation precedence is contractual.
 put('dynamic_missing',dict(dyn=[]),'dynamic_missing',2)
 put('dynamic_multiple',dict(extra=[seg(2,do,v,64)]),'dynamic_multiple',2)
 for key,d,reason,code in [('dynamic_filesz',seg(2,do,v,64,63),'dynamic_filesz',1),('dynamic_memory_overflow',seg(2,do,U-8,64),'dynamic_memory_overflow',1),('dynamic_file_overflow',seg(2,U-8,v,64),'dynamic_file_overflow',1),('dynamic_outside',seg(2,12280,v,64),'dynamic_outside',1),('dynamic_empty',seg(2,do,v,0),'dynamic_shape',1),('dynamic_remainder',seg(2,do,v,63),'dynamic_shape',1),('dynamic_budget',seg(2,do,v,4112),'dynamic_budget',2)]:put(key,dict(dyn=d),reason,code)
 for suffix,ls in [('unmapped',[seg(1,so,sv,len(table))]),('ambiguous',[seg(1,do,v,64),seg(1,do,v,64),seg(1,so,sv,len(table))]),('zero',[seg(1,do,v,0,64),seg(1,so,sv,len(table))]),('origin_mismatch',[seg(1,do+8,v,64),seg(1,so,sv,len(table))])]:put('dynamic_'+suffix,dict(loads=ls),'dynamic_'+suffix)
 put('dynamic_unterminated',dict(entries=base[:-1]+[(99,0)]),'dynamic_unterminated')
 put('null_before_duplicates',dict(entries=base[:-1]+[(5,sv)]),'dynamic_unterminated')
 put('duplicate_strtab',dict(entries=base[:-1]+[(5,sv),(0,0)]),'duplicate_strtab')
 put('duplicate_strsz',dict(entries=base[:-1]+[(10,len(table)),(0,0)]),'duplicate_strsz')
 put('strtab_missing',dict(entries=[(10,len(table)),(0,0)]),'strtab_missing')
 put('strsz_missing',dict(entries=[(5,sv),(0,0)]),'strsz_missing')
 for name,val,reason,code in [('empty_strtab',0,'empty_strtab',2),('strtab_budget',4097,'strtab_budget',2)]:put(name,dict(entries=[(5,sv),(10,val),(0,0)]),reason,code)
 put('strtab_overflow',dict(entries=[(5,U-2),(10,8),(0,0)]),'strtab_overflow')
 for suffix,ls in [('unmapped',[seg(1,do,v,64)]),('ambiguous',[seg(1,do,v,64),seg(1,so,sv,len(table)),seg(1,so,sv,len(table))]),('zero',[seg(1,do,v,64),seg(1,so,sv,len(table)-1,len(table))]),('middle_gap',[seg(1,do,v,64),seg(1,so,sv,3),seg(1,so+4,sv+4,len(table)-4)])]:put('strtab_'+suffix,dict(loads=ls),'strtab_unmapped' if suffix=='middle_gap' else 'strtab_'+suffix)
 put('first_nul',dict(tab=b'X'+table[1:]),'strtab_first_nul')
 put('last_nul_beyond_bound',dict(tab=table[:-1]+b'X',patch=lambda b:b.__setitem__(so+len(table),0)),'strtab_last_nul')
 put('needed_at_bound',dict(entries=[(5,sv),(10,len(table)),(1,len(table)),(0,0)]),'needed_outside')
 put('needed_huge',dict(entries=[(5,sv),(10,len(table)),(1,U-1),(0,0)]),'needed_outside')
 put('post_null_origin_gap',dict(entries=base+[(99,0)],loads=[seg(1,do,v,64),seg(1,so,sv,len(table))]),'dynamic_unmapped')
 put('unreferenced_table_gap',dict(entries=[(5,sv),(10,len(table)),(1,1),(0,0)],loads=[seg(1,do,v,64),seg(1,so,sv,len(word)+2)]),'strtab_unmapped')
 put('load_invalid_first',dict(loads=[seg(1,do,v,64,63),seg(1,so,sv,len(table))]),'filesz_gt_memsz')
 (out/'expected.json').write_text(json.dumps(cases,sort_keys=True,indent=2)+'\n');return cases
if __name__=='__main__':main(*sys.argv[1:])
