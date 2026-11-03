#!/usr/bin/env python3
"""Independent construction-only PE certificate fixtures; never invokes reader.
CLI: fixtures.py OUT SALT. Writes owned subjects + digest-pinned oracle. Exit0 success.
"""
import hashlib,json,pathlib,struct,sys
H=lambda b:hashlib.sha256(b).hexdigest()
def build(fmt='pe32plus', records=None, offset=1024, size=None, count=16, optional=None, sections=1, total=4096):
    plus=fmt=='pe32plus'; fixed=112 if plus else 96
    optsize=fixed+128 if optional is None else optional
    b=bytearray(total);b[:2]=b'MZ';struct.pack_into('<I',b,60,128);b[128:132]=b'PE\0\0'
    struct.pack_into('<HHIIIHH',b,132,0x8664 if plus else 0x14c,sections,0,0,0,optsize,2)
    struct.pack_into('<H',b,152,0x20b if plus else 0x10b)
    struct.pack_into('<I',b,152+fixed-4,count)
    table=bytearray(); rows=[]
    for length,revision,kind,payload,pad in (records or []):
        assert length>=8 and len(payload)==length-8
        ext=(-length)%8; assert len(pad)==ext
        rec=struct.pack('<IHH',length,revision,kind)+payload+pad
        rows.append({'offset':offset+len(table),'length':length,'revision':revision,'type':kind,'declared_content_sha256':H(payload),'alignment_padding_sha256':H(pad)})
        table+=rec
    if size is None:size=len(table)
    struct.pack_into('<II',b,152+fixed+32,offset,size)
    # One section deliberately maps RVA 1024 to physical2048, a wrong-directory-unit trap.
    sec=152+optsize
    if sec+40<=len(b):
        b[sec:sec+8]=b'.decoy\0\0';struct.pack_into('<IIII',b,sec+8,1024,1024,1024,2048)
    if offset+len(table)<=len(b):b[offset:offset+len(table)]=table
    expected={'status':'ok','format':fmt,'table_offset':offset,'table_size':size,'records':rows}
    return b,expected

def generate(out,salt):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True);cases=[]
    def payload(n,label):
        seed=hashlib.sha256((salt+label).encode()).digest();return (seed*((n+31)//32))[:n]
    def add(name,b,e):
        # Bytes outside parsed header/table vary without changing expected semantic records.
        b=bytearray(b)
        if len(b)>256:b[64:96]=hashlib.sha256((salt+name).encode()).digest()
        p=out/(name+'.bin');p.write_bytes(b)
        cases.append({'name':name,'file':p.name,'sha256':H(b),'expected':e,'exit':1 if e['status']=='refused' else 0})
    def ok(name,fmt='pe32plus',recs=None,**kw):
        if recs is None:recs=[(16,512,2,payload(8,name),b'')]
        b,e=build(fmt,recs,**kw);add(name,b,e)
    bad={'status':'refused'}
    for fmt in ['pe32','pe32plus']:
        ok(fmt+'-single',fmt)
        ok(fmt+'-ordered',fmt,[(16,512,2,payload(8,fmt+'a'),b''),(24,256,1,payload(16,fmt+'b'),b'')])
        p=payload(8,fmt+'repeat');ok(fmt+'-duplicates',fmt,[(16,512,2,p,b''),(16,512,2,p,b'')])
        ok(fmt+'-unaligned-declared',fmt,[(11,512,2,payload(3,fmt+'odd'),b'\0'*5)])
        ok(fmt+'-unknown-fields',fmt,[(8,65535,65535,b'',b'')])
        b,e=build(fmt,[],offset=0,size=0);add(fmt+'-absent',b,{'status':'absent','format':fmt})
        b,e=build(fmt,[],count=4,offset=0,size=0);add(fmt+'-directory-not-declared',b,{'status':'absent','format':fmt})
    b,e=build(records=[(16,512,2,payload(8,'hidden'),b'')],count=4);add('hidden-directory-decoy',b,{'status':'absent','format':'pe32plus'})
    ok('max-table',recs=[(4096,512,2,payload(4088,'big'),b'')],total=8192)
    ok('max-records',recs=[(8,512,i,b'',b'') for i in range(64)])
    ok('exact-eof',total=1040)
    ok('zero-sections',sections=0)
    ok('max-sections',sections=96,offset=8192,total=16384)
    ok('max-file',total=1048576)
    ok('minimal-five-directories',count=5,optional=152)
    ok('nonzero-external-padding',recs=[(11,512,2,b'ABC',b'12345')])
    # Profile reports padding bytes without interpreting authenticity or requiring zero.
    base,expect=build(records=[(16,512,2,b'12345678',b'')])
    def mutate(name,fn):
        b=bytearray(base);fn(b);add(name,b,bad)
    mutate('bad-mz',lambda b:b.__setitem__(slice(0,2),b'NO'))
    mutate('bad-pe',lambda b:b.__setitem__(slice(128,132),b'PX\0\0'))
    mutate('bad-magic',lambda b:struct.pack_into('<H',b,152,0x107))
    mutate('pe-offset-outside',lambda b:struct.pack_into('<I',b,60,0xfffffff0))
    mutate('optional-short-fixed',lambda b:struct.pack_into('<H',b,148,111))
    mutate('optional-short-directory',lambda b:struct.pack_into('<H',b,148,151))
    mutate('directory-count-over-header',lambda b:struct.pack_into('<I',b,260,17))
    mutate('section-count-over-limit',lambda b:struct.pack_into('<H',b,134,97))
    mutate('section-table-truncated',lambda b:struct.pack_into('<H',b,134,96))
    mutate('pointer-zero-size-nonzero',lambda b:struct.pack_into('<I',b,296,0))
    mutate('size-zero-pointer-nonzero',lambda b:struct.pack_into('<I',b,300,0))
    mutate('table-unaligned',lambda b:struct.pack_into('<I',b,296,1025))
    mutate('table-overlaps-headers',lambda b:struct.pack_into('<I',b,296,256))
    mutate('table-past-eof',lambda b:struct.pack_into('<I',b,296,4096))
    mutate('table-size-over-limit',lambda b:struct.pack_into('<I',b,300,4097))
    mutate('table-pointer-wrap',lambda b:struct.pack_into('<II',b,296,0xfffffff8,16))
    mutate('entry-length-zero',lambda b:struct.pack_into('<I',b,1024,0))
    mutate('entry-length-seven',lambda b:struct.pack_into('<I',b,1024,7))
    mutate('entry-length-over-table',lambda b:struct.pack_into('<I',b,1024,17))
    mutate('entry-padding-over-table',lambda b:struct.pack_into('<II',b,296,1024,11))
    mutate('trailing-partial-header',lambda b:struct.pack_into('<I',b,300,20))
    b,e=build(records=[(8,512,i,b'',b'') for i in range(65)]);add('records-over-limit',b,bad)
    add('truncated-dos',base[:63],bad);add('truncated-coff',base[:151],bad)
    add('over-file-limit',base+bytearray(1048577-len(base)),bad)
    (out/'expected.json').write_text(json.dumps({'schema':1,'salt':salt,'cases':cases},sort_keys=True,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'positive':sum(x['exit']==0 for x in cases),'refused':sum(x['exit']==1 for x in cases)}))
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit(64)
    generate(sys.argv[1],sys.argv[2])
