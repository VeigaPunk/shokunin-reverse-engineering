#!/usr/bin/env python3
"""Bounded static ELF64LE LOAD-span provenance; never loads/executes a carrier.
0 mapped profile (including gaps/ambiguity),1 malformed,2 unsupported/input.
Resource limits are supplied by caller and are not an OS sandbox.
"""
import argparse,hashlib,json,os,re,stat,struct,sys,tempfile,subprocess,pathlib
U=1<<64
class Refusal(Exception):
    def __init__(self,code,reason):self.code,self.reason=code,reason

def fail(code,reason):raise Refusal(code,reason)
def digest(b):return hashlib.sha256(b).hexdigest()
def solve(path,start,length):
    if not re.fullmatch(r'[0-9]+',start) or not re.fullmatch(r'[0-9]+',length):fail(2,'bad_query')
    # Bound decimal conversion independently of interpreter giant-integer settings.
    start=start.lstrip('0') or '0';length=length.lstrip('0') or '0'
    if len(start)>20:fail(2,'bad_query')
    a=int(start)
    if a>=U or length=='0':fail(2,'bad_query')
    if len(length)>20:fail(2,'query_budget')
    n=int(length)
    if a>=U or n<1:fail(2,'bad_query')
    if n>4096:fail(2,'query_budget')
    end=a+n
    if end>U:fail(1,'query_overflow')
    try:
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        with os.fdopen(fd,'rb') as f:
            st=os.fstat(f.fileno())
            if not stat.S_ISREG(st.st_mode):fail(2,'input')
            if st.st_size>1048576:fail(2,'file_budget')
            b=f.read(1048577)
    except OSError:fail(2,'input')
    if len(b)>1048576:fail(2,'file_budget')
    if len(b)<64:fail(1,'truncated_header')
    if b[:4]!=b'\x7fELF':fail(1,'bad_magic')
    for ix,want,reason in [(4,2,'elf_class'),(5,1,'elf_endian'),(6,1,'elf_version')]:
        if b[ix]!=want:fail(2,reason)
    et,mach,ver,entry,po,so,flags,eh,pe,pn,se,sn,si=struct.unpack_from('<HHIQQQIHHHHHH',b,16)
    if et not in (2,3):fail(2,'elf_type')
    if ver!=1:fail(2,'elf_version')
    if eh!=64:fail(2,'header_size')
    if pe!=56:fail(2,'phdr_size')
    if pn==65535:fail(2,'extended_phnum')
    if pn>128:fail(2,'phdr_budget')
    if pn:
        if po<64:fail(1,'table_overlap')
        if po+56*pn>U:fail(1,'table_overflow')
        if po+56*pn>len(b):fail(1,'truncated_table')
    loads=[];last=-1
    for ordinal in range(pn):
        typ,pf,off,va,pa,fs,ms,al=struct.unpack_from('<IIQQQQQQ',b,po+56*ordinal)
        if typ!=1:continue
        if fs>ms:fail(1,'filesz_gt_memsz')
        if va+ms>U:fail(1,'memory_overflow')
        if off+fs>U:fail(1,'file_overflow')
        if off+fs>len(b):fail(1,'file_outside')
        if al not in (0,1) and (al&(al-1) or va%al!=off%al):fail(1,'alignment')
        if va<last:fail(1,'load_order')
        last=va
        loads.append((ordinal,off,va,fs,ms))
    cuts={a,end}
    for _,off,va,fs,ms in loads:
        if ms:
            cuts.update(x for x in (va,va+fs,va+ms) if a<x<end)
    cuts=sorted(cuts);intervals=[]
    for x,y in zip(cuts,cuts[1:]):
        candidates=[]
        for ordinal,off,va,fs,ms in loads:
            if va<=x and y<=va+ms:
                if x<va+fs:
                    p=off+x-va;candidates.append(dict(ordinal=ordinal,kind='file',file_offset=p,sha256=digest(b[p:p+y-x])))
                else:candidates.append(dict(ordinal=ordinal,kind='zero'))
        kind='unmapped' if not candidates else (candidates[0]['kind'] if len(candidates)==1 else 'ambiguous')
        intervals.append(dict(start=x,length=y-x,kind=kind,candidates=candidates))
    return dict(schema=1,exit=0,finding='complete',elf_sha256=digest(b),elf_size=len(b),query=dict(start=a,length=n),intervals=intervals)

def selftest():
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku66-reader-') as td:
        f=pathlib.Path(td)/'owned.elf'
        ident=b'\x7fELF'+bytes([2,1,1])+bytes(9)
        good=ident+struct.pack('<HHIQQQIHHHHHH',2,0,1,0,0,0,0,64,56,0,0,0,0)
        for name,blob,start,length,code,finding in [('empty_profile',good,'1','3',0,'complete'),('bad_magic',b'NOPE'+good[4:],'0','1',1,'bad_magic'),('zero_query',good,'0','0',2,'bad_query'),('wrap_query',good,str(U-1),'2',1,'query_overflow')]:
            f.write_bytes(blob);cmd=[sys.executable,'-I','-B',__file__,'--elf',str(f),'--start',start,'--length',length]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=5);v=json.loads(r.stdout)
            results.append(dict(case=name,exit=r.returncode,finding=v['finding'],ok=r.returncode==code and v['finding']==finding))
    print(json.dumps(dict(results=results,ok=all(x['ok'] for x in results))));return 0 if all(x['ok'] for x in results) else 1

def main():
    p=argparse.ArgumentParser();p.add_argument('--elf');p.add_argument('--start');p.add_argument('--length');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    if a.selftest:return selftest()
    try:
        if a.elf is None or a.start is None or a.length is None:fail(2,'input')
        r=solve(a.elf,a.start,a.length)
    except Refusal as e:r=dict(schema=1,exit=e.code,finding=e.reason)
    print(json.dumps(r,sort_keys=True));return r['exit']
if __name__=='__main__':raise SystemExit(main())
