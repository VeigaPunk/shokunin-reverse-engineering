#!/usr/bin/env python3
"""Owned inert ELF construction oracle. Never reads ELF headers to derive expected mapping."""
import hashlib,json,pathlib,struct,sys
H=lambda b:hashlib.sha256(b).hexdigest()
U=2**64

def seg(v,o,n,m=None,t=1,a=1):return dict(v=v,o=o,n=n,m=n if m is None else m,t=t,a=a)
def build(ss,seed=b'X',**kw):
    count=kw.get('count',len(ss)); phoff=kw.get('phoff',64)
    size=max(64+56*len(ss),*(s['o']+s['n'] for s in ss if s['o']+s['n']<20000),1024)
    b=bytearray((seed*((size//len(seed))+1))[:size]);ident=b'\x7fELF'+bytes([2,1,1,0])+b'\0'*8
    b[:64]=struct.pack('<16sHHIQQQIHHHHHH',ident,kw.get('etype',2),62,1,0,phoff,0,0,64,56,count,64,0,0)
    for i,s in enumerate(ss):b[64+56*i:120+56*i]=struct.pack('<IIQQQQQQ',s['t'],4,s['o'],s['v'],0,s['n'],s['m'],s['a'])
    return bytes(b)
def oracle(b,ss,q,n):
    # Boundaries come from construction declarations, not decoded subject bytes.
    pts={q,q+n}
    for s in ss:
        if s['t']==1 and s['m']:
            pts.update(x for x in (s['v'],s['v']+s['n'],s['v']+s['m']) if q<x<q+n)
    pts=sorted(pts); spans=[]
    for left,right in zip(pts,pts[1:]):
        cs=[]
        for i,s in enumerate(ss):
            if s['t']!=1 or not (s['v']<=left<s['v']+s['m']):continue
            c=dict(ordinal=i,kind='zero')
            if left<s['v']+s['n']:
                off=s['o']+left-s['v'];c=dict(ordinal=i,kind='file',file_offset=off,sha256=H(b[off:off+right-left]))
            cs.append(c)
        spans.append(dict(start=left,length=right-left,kind='unmapped' if not cs else cs[0]['kind'] if len(cs)==1 else 'ambiguous',candidates=cs))
    return dict(schema=1,exit=0,finding='complete',elf_sha256=H(b),elf_size=len(b),query=dict(start=q,length=n),intervals=spans)
def main(out,salt):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=False);cases={};d=hashlib.sha256(salt.encode()).digest();v=0x1000+32*d[0];o=512+16*(d[1]%8);n=9+d[2]%8
    def put(key,b,q,l,e,code=0):
        (out/(key+'.elf')).write_bytes(b);cases[key]=dict(exit=code,elf_sha256=H(b),request=dict(start=str(q),length=str(l)),output=e)
    def good(key,ss,q,l,**kw):
        b=build(ss,d,**kw);put(key,b,q,l,oracle(b,ss,q,l))
    def bad(key,b,reason,code=1,q=None,l=None):put(key,b,v if q is None else q,n if l is None else l,dict(schema=1,exit=code,finding=reason),code)
    def patch(b,off,fmt,value):a=bytearray(b);struct.pack_into(fmt,a,off,value);return bytes(a)
    good('file_only',[seg(v,o,n)],v,n)
    good('zero_only',[seg(v,o,0,n)],v,n)
    good('file_zero',[seg(v,o,n,n+7)],v,n+7)
    good('gap_edges',[seg(v,o,n)],v-3,n+6)
    good('adjacent_different_delta',[seg(v,o,n),seg(v+n,o+80,n+2)],v,2*n+2)
    good('middle_gap',[seg(v,o,n),seg(v+n+5,o+80,n)],v,2*n+5)
    good('overlap_file',[seg(v,o,n+10),seg(v+4,o+80,n)],v,n+10)
    good('overlap_file_zero',[seg(v,o,3,n+10),seg(v+4,o+80,n)],v,n+10)
    good('identical_overlap',[seg(v,o,n),seg(v,o,n)],v,n)
    good('three_way',[seg(v,o,n+10),seg(v+2,o+80,3,n),seg(v+4,o+160,n)],v,n+14)
    good('nonload_decoy',[seg(v,o,n,t=4),seg(v+2,o+40,n)],v,n+4)
    good('empty_load',[seg(v,o,0,0),seg(v+5,o+40,n)],v,n+5)
    good('no_headers',[],v,n,phoff=U-1)
    good('query_unmapped',[seg(v,o,n)],v+n+20,n)
    good('end_address',[seg(U-n,o,n)],U-n,n)
    good('large_query',[seg(v,o,n)],v,4096)
    good('aligned',[seg(0x400200,512,n,a=256)],0x400200,n)
    good('alignment_zero',[seg(v,o,n,a=0)],v,n)
    good('dyn_linktime',[seg(v,o,n)],v,n,etype=3)
    ss=[seg(v,o,n)];b=build(ss,d);poison=patch(patch(patch(b,40,'<Q',U-1),60,'<H',65535),62,'<H',65535)
    put('ignored_sections',poison,v,n,oracle(poison,ss,v,n))
    good('count_boundary',[seg(v+i*2,0,0,1) for i in range(128)],v,256)
    # Exact EOF file range; explicit padding bytes remain owned construction.
    ss=[seg(v,1010,14)];b=build(ss,d);put('exact_eof',b,v,14,oracle(b,ss,v,14))
    normal=build([seg(v,o,n)],d)
    bad('query_zero',normal,'bad_query',2,l=0);bad('query_negative',normal,'bad_query',2,q=-1)
    bad('query_hex',normal,'bad_query',2,q='0x10');bad('query_budget',normal,'query_budget',2,l=4097)
    bad('query_overflow',normal,'query_overflow',q=U-1,l=2)
    bad('truncated_header',normal[:63],'truncated_header')
    bad('bad_magic',b'NOPE'+normal[4:],'bad_magic')
    for key,off,fmt,val,reason in [('elf32',4,'B',1,'elf_class'),('big_endian',5,'B',2,'elf_endian'),('ident_version',6,'B',0,'elf_version'),('elf_rel',16,'<H',1,'elf_type'),('header_version',20,'<I',0,'elf_version'),('header_size',52,'<H',63,'header_size'),('phdr_size',54,'<H',55,'phdr_size'),('extended_count',56,'<H',65535,'extended_phnum'),('phdr_budget',56,'<H',129,'phdr_budget')]:bad(key,patch(normal,off,fmt,val),reason,2)
    bad('table_overlap',patch(normal,32,'<Q',63),'table_overlap')
    bad('table_overflow',patch(normal,32,'<Q',U-20),'table_overflow')
    bad('table_truncated',normal[:119],'truncated_table')
    bad('filesz_gt_memsz',build([seg(v,o,n,n-1)],d),'filesz_gt_memsz')
    bad('memory_overflow',build([seg(U-2,o,1,3)],d),'memory_overflow')
    bad('file_overflow',build([seg(v,U-2,3)],d),'file_overflow')
    bad('file_outside',patch(normal,72,'<Q',len(normal)-n+1),'file_outside')
    bad('zero_file_outside',build([seg(v,20000,0,1)],d),'file_outside')
    bad('align_nonpower',build([seg(v,o,n,a=3)],d),'alignment')
    bad('align_mismatch',build([seg(0x400201,512,n,a=256)],d),'alignment')
    bad('load_order',build([seg(v+10,o,n),seg(v,o+80,n)],d),'load_order')
    bad('file_budget',normal+b'X'*(1048577-len(normal)),'file_budget',2)
    (out/'expected.json').write_text(json.dumps(cases,indent=2,sort_keys=True)+'\n');return cases
if __name__=='__main__':main(*sys.argv[1:])
