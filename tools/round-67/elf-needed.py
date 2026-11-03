#!/usr/bin/env python3
"""Bounded static ELF64LE dynamic declaration custody. Never loads a carrier.
0 complete declared profile, 1 malformed/custody conflict, 2 unsupported/input.
Resource limits are supplied by caller, not an OS sandbox.
"""
import argparse,hashlib,json,os,stat,struct,sys,tempfile,subprocess,pathlib
U=1<<64
class Refusal(Exception):
    def __init__(self,code,reason):self.code,self.reason=code,reason

def fail(code,reason):raise Refusal(code,reason)
def digest(b):return hashlib.sha256(b).hexdigest()
def solve(path):
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
    loads=[];dynamics=[];last=-1
    for ordinal in range(pn):
        typ,pf,off,va,pa,fs,ms,al=struct.unpack_from('<IIQQQQQQ',b,po+56*ordinal)
        if typ==2:dynamics.append((ordinal,off,va,fs,ms))
        if typ!=1:continue
        if fs>ms:fail(1,'filesz_gt_memsz')
        if va+ms>U:fail(1,'memory_overflow')
        if off+fs>U:fail(1,'file_overflow')
        if off+fs>len(b):fail(1,'file_outside')
        if al not in (0,1) and (al&(al-1) or va%al!=off%al):fail(1,'alignment')
        if va<last:fail(1,'load_order')
        last=va
        loads.append((ordinal,off,va,fs,ms))
    if not dynamics:fail(2,'dynamic_missing')
    if len(dynamics)>1:fail(2,'dynamic_multiple')
    ordinal,off,va,fs,ms=dynamics[0]
    if fs>ms:fail(1,'dynamic_filesz')
    if va+fs>U:fail(1,'dynamic_memory_overflow')
    if off+fs>U:fail(1,'dynamic_file_overflow')
    if off+fs>len(b):fail(1,'dynamic_outside')
    if not fs or fs%16:fail(1,'dynamic_shape')
    if fs>4096:fail(2,'dynamic_budget')
    def custody(start,size,prefix,physical=None):
        origins=[];data=bytearray()
        for delta in range(size):
            at=start+delta
            candidates=[x for x in loads if x[2]<=at<x[2]+x[4]]
            if not candidates:fail(1,prefix+'_unmapped')
            if len(candidates)>1:fail(1,prefix+'_ambiguous')
            ix,po,pv,pf,pm=candidates[0]
            if at>=pv+pf:fail(1,prefix+'_zero')
            location=po+at-pv
            if physical is not None and location!=physical+delta:fail(1,prefix+'_origin_mismatch')
            data.append(b[location]);origins.append((ix,location))
        return bytes(data),origins
    dyn,_=custody(va,fs,'dynamic',off)
    entries=[];term=None
    for i in range(fs//16):
        tag,value=struct.unpack_from('<qQ',dyn,16*i)
        if tag==0:term=i;break
        entries.append((i,tag,value))
    if term is None:fail(1,'dynamic_unterminated')
    singleton={}
    for i,tag,value in entries:
        if tag in (5,10):
            if tag in singleton:fail(1,'duplicate_strtab' if tag==5 else 'duplicate_strsz')
            singleton[tag]=value
    if 5 not in singleton:fail(1,'strtab_missing')
    if 10 not in singleton:fail(1,'strsz_missing')
    addr,size=singleton[5],singleton[10]
    if size==0:fail(2,'empty_strtab')
    if size>4096:fail(2,'strtab_budget')
    if addr+size>U:fail(1,'strtab_overflow')
    strings,origins=custody(addr,size,'strtab')
    if strings[0]!=0:fail(1,'strtab_first_nul')
    if strings[-1]!=0:fail(1,'strtab_last_nul')
    needed=[]
    for i,tag,index in entries:
        if tag!=1:continue
        if index>=size:fail(1,'needed_outside')
        end=strings.index(0,index);pieces=[]
        for load,pos in origins[index:end+1]:
            if pieces and pieces[-1]['load_ordinal']==load and pieces[-1]['file_offset']+pieces[-1]['length']==pos:
                pieces[-1]['length']+=1
            else:pieces.append(dict(load_ordinal=load,file_offset=pos,length=1))
        needed.append(dict(dynamic_index=i,entry_offset=off+16*i,string_offset=index,name_hex=strings[index:end].hex(),origins=pieces))
    return dict(schema=1,exit=0,finding='complete',elf_sha256=digest(b),elf_size=len(b),dynamic=dict(ordinal=ordinal,file_offset=off,vaddr=va,size=fs,terminator_index=term),strtab=dict(vaddr=addr,size=size),needed=needed)

def selftest():
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku67-reader-') as td:
        f=pathlib.Path(td)/'owned.elf'
        ident=b'\x7fELF'+bytes([2,1,1])+bytes(9)
        base=ident+struct.pack('<HHIQQQIHHHHHH',2,0,1,0,0,0,0,64,56,0,0,0,0)
        for name,blob,code,finding in [('missing_dynamic',base,2,'dynamic_missing'),('bad_magic',b'NOPE'+base[4:],1,'bad_magic'),('truncated',b'',1,'truncated_header')]:
            f.write_bytes(blob);cmd=[sys.executable,'-I','-B',__file__,'--elf',str(f)]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=5);v=json.loads(r.stdout)
            results.append(dict(case=name,exit=r.returncode,finding=v['finding'],ok=r.returncode==code and v['finding']==finding))
    print(json.dumps(dict(results=results,ok=all(x['ok'] for x in results))));return 0 if all(x['ok'] for x in results) else 1

def main():
    p=argparse.ArgumentParser();p.add_argument('--elf');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    if a.selftest:return selftest()
    try:
        if a.elf is None:fail(2,'input')
        r=solve(a.elf)
    except Refusal as e:r=dict(schema=1,exit=e.code,finding=e.reason)
    print(json.dumps(r,sort_keys=True));return r['exit']
if __name__=='__main__':raise SystemExit(main())
