#!/usr/bin/env python3
"""Independent bounded synthetic ZIP writer and recipe oracle; no reader imports.
Writes only chosen root fixed filenames. Exit 0 success; exceptions fail nonzero.
"""
import struct, zlib, hashlib, json, pathlib, sys

def make(entries, order=None):
    local=bytearray(); central=[]; records=[]
    for name,payload,method,flags,declared in entries:
        n=name.encode('ascii'); offset=len(local); crc=zlib.crc32(payload)&0xffffffff
        co=zlib.compressobj(wbits=-15); compressed=payload if method!=8 else co.compress(payload)+co.flush()
        size=len(payload) if declared is None else declared
        local += struct.pack('<IHHHHHIIIHH',0x04034b50,20,flags,method,0,0,crc,len(compressed),size,len(n),0)+n+compressed
        central.append(struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,20,20,flags,method,0,0,crc,len(compressed),size,len(n),0,0,0,0,0,offset)+n)
        records.append(dict(filename=name,header_offset=offset,size=len(payload),crc32=f'{crc:08x}',sha256=hashlib.sha256(payload).hexdigest()))
    order=list(range(len(entries))) if order is None else order
    c=b''.join(central[i] for i in order); count=len(order)
    data=bytes(local)+c+struct.pack('<IHHHHIIH',0x06054b50,0,0,count,count,len(c),len(local),0)
    out=[dict(ordinal=j,**records[i]) for j,i in enumerate(order)]
    groups={}
    for r in out: groups.setdefault(r['filename'],[]).append(r['ordinal'])
    return data,dict(occurrences=out,duplicate_groups=[dict(filename=n,ordinals=v) for n,v in groups.items() if len(v)>1])

def generate(root, salt):
    root=pathlib.Path(root); root.mkdir(parents=True,exist_ok=True); expected={}
    def e(n,p,m=0,f=0,d=None): return (n,p,m,f,d)
    def add(key,entries,order=None,code=0,finding='inventory_complete',mutate=None):
        data,semantic=make(entries,order)
        if mutate: data=mutate(data)
        (root/(key+'.zip')).write_bytes(data)
        expected[key]=dict(exit=code,finding=finding,archive_sha256=hashlib.sha256(data).hexdigest(),archive_size=len(data))
        if code==0: expected[key].update(semantic)
    a=('alpha-'+salt).encode(); b=('beta-'+salt*2).encode(); n='pkg/'+salt+'.txt'
    add('different_duplicates',[e(n,a),e(n,b)])
    add('reverse_payloads',[e(n,b),e(n,a)])
    add('central_reordered',[e(n,a),e('other/'+salt,b),e(n,b)],order=[2,0,1])
    add('same_payload',[e(n,a),e(n,a)])
    add('empty',[])
    add('metadata_names',[e('../'+salt,a),e('a\\'+salt,b),e('a/'+salt,b),e('/'+salt,b)])
    add('deflated',[e(n,a*70,8),e(n,b*41,8)])
    add('nul_name',[e('name\0suffix',a)],code=2,finding='unsupported_name')
    add('crc_invalid',[e(n,a)],code=1,finding='malformed_zip',mutate=lambda d:d[:30+len(n)]+bytes([d[30+len(n)]^1])+d[31+len(n):])
    add('truncated',[e(n,a)],code=1,finding='malformed_zip',mutate=lambda d:d[:-12])
    add('header_name_mismatch',[e(n,a)],code=1,finding='malformed_zip',mutate=lambda d:d[:30]+b'X'+d[31:])
    add('unsupported_method',[e(n,a,99)],code=2,finding='unsupported_compression')
    add('encrypted',[e(n,a,0,1)],code=2,finding='encrypted_member')
    add('member_budget',[e(n,b'',0,0,1048577)],code=2,finding='member_budget')
    add('total_budget',[e(str(i),b'',0,0,1048576) for i in range(5)],code=2,finding='total_budget')
    add('count_budget',[e(str(i),b'') for i in range(129)],code=2,finding='member_count_budget')
    add('count_boundary',[e(str(i),b'') for i in range(128)])
    add('member_boundary',[e(n,b'z'*1048576,8)])
    # Archive padding is bounded and inert. This arm refuses before ZIP parsing.
    add('archive_budget',[],code=2,finding='archive_budget',mutate=lambda d:d+b'0'*(8388609-len(d)))
    (root/'expected.json').write_text(json.dumps(expected,indent=2,sort_keys=True)+'\n')
    return expected
if __name__=='__main__': generate(sys.argv[1],sys.argv[2])
