#!/usr/bin/env python3
"""FinalC1Measure-2 independent PE comparator (round-32 a2residual).

Independence note: written fresh for this seat. It does NOT import or call
tools/round-32/arm64x_oracle.py (the lane oracle). It re-implements the frozen
R32-C1 field rules from the committed structures:

  * DOS e_lfanew -> PE signature -> COFF header (Machine, NumberOfSections).
  * PE32+ optional header: ImageBase (+24), SizeOfHeaders (+60), data dirs (+112).
  * Section table: name, VirtualSize, VirtualAddress, SizeOfRawData,
    PointerToRawData, in file order.
  * Export directory (data dir 0, primary/native view): NumberOfFunctions (+0x14),
    NumberOfNames (+0x18), AddressOfNames (+0x20); names are ASCIIZ strings.
  * Load config (data dir 10): CHPEMetadataPointer VA at +0xC8; IMAGE_ARM64EC
    metadata v2: Version(+0), CodeMapRVA(+4), CodeMapCount(+8); map entries are
    {u32 StartOffset-with-type-in-low-2-bits, u32 Length}; types 0 ARM64,
    1 ARM64EC, 2 AMD64.
  * Envelope segments = Headers pseudo-segment [ImageBase, ImageBase+SizeOfHeaders)
    then each section with start=ImageBase+VA, length=max(VirtualSize,
    SizeOfRawData), end=start+length, image_base=hex(ImageBase), address_space=ram.

Compares committed envelopes (byte copies of bb0af56c:
corpus/evidence/round-32/c1/envelopes/k*.json) against (a) this byte parse of the
chattr +i pinned carriers and (b) this seat's own llvm-readobj 23.1.3 runs.
"""
import struct, json, hashlib, re, sys

u16=lambda b,o:struct.unpack_from('<H',b,o)[0]
u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
u64=lambda b,o:struct.unpack_from('<Q',b,o)[0]
RMAP={0:"ARM64",1:"ARM64EC",2:"AMD64",3:"type3"}

def own_parse(path):
    b=open(path,'rb').read()
    assert b[:2]==b'MZ'
    pe=u32(b,0x3c); assert b[pe:pe+4]==b'PE\0\0'
    machine=u16(b,pe+4); nsec=u16(b,pe+6); optsize=u16(b,pe+20)
    opt=pe+24; assert u16(b,opt)==0x20b
    image_base=u64(b,opt+24); soh=u32(b,opt+60); ndirs=u32(b,opt+108)
    dd=lambda i:(u32(b,opt+112+8*i),u32(b,opt+112+8*i+4)) if i<ndirs else (0,0)
    secs=[]
    for i in range(nsec):
        s=opt+optsize+40*i
        secs.append(dict(name=b[s:s+8].rstrip(b'\0').decode(),vsize=u32(b,s+8),
                         va=u32(b,s+12),rsize=u32(b,s+16),rptr=u32(b,s+20)))
    def off(rva):
        for s in secs:
            if s['va']<=rva<s['va']+max(s['vsize'],s['rsize']): return s['rptr']+rva-s['va']
        raise ValueError('rva %#x'%rva)
    exrva,_=dd(0); eo=off(exrva)
    nfuncs=u32(b,eo+0x14); nnames=u32(b,eo+0x18); nnames_rva=u32(b,eo+0x20)
    names=[]
    for i in range(nnames):
        o=off(u32(b,off(nnames_rva)+4*i)); names.append(b[o:b.index(b'\0',o)].decode())
    lcrva,_=dd(10); lc=off(lcrva); lcsize=u32(b,lc)
    chpe_va=u64(b,lc+0xc8) if lcsize>=0xd0 else 0
    codemap=[]
    if chpe_va:
        m=off(chpe_va-image_base); cmrva=u32(b,m+4); cmcount=u32(b,m+8)
        for i in range(cmcount):
            st,ln=struct.unpack_from('<II',b,off(cmrva)+8*i)
            codemap.append(dict(type=RMAP.get(st&3,'?'),start=st&~3,end=(st&~3)+ln,length=ln))
    hexstr=lambda v:'0x%x'%v
    segs=[dict(name="Headers",start=hexstr(image_base),end=hexstr(image_base+soh),
               length=soh,image_base=hexstr(image_base),address_space="ram")]
    for s in secs:
        ln=max(s['vsize'],s['rsize']); st=image_base+s['va']
        segs.append(dict(name=s['name'],start=hexstr(st),end=hexstr(st+ln),length=ln,
                         image_base=hexstr(image_base),address_space="ram"))
    sha=hashlib.sha256(b).hexdigest()
    return dict(sha=sha,machine=machine,image_base=hexstr(image_base),soh=soh,sections=secs,
                exports=names,nfuncs=nfuncs,nnames=nnames,codemap=codemap,segments=segs,
                segment_count=len(segs),document="target-%s.dll"%sha[:12],size=len(b))

def parse_readobj(fn):
    txt=open(fn).read().splitlines()
    res={'primary_exports':[],'hybrid_exports':[],'sections':[],'codemap':[],
         'imgbase':None,'sectioncount':None}
    hyb=False; insec=False; cur={}; inexp=False; ename=None; incm=False; cm_done=False
    for ln in txt:
        s=ln.strip()
        if s.startswith('SectionCount:') and res['sectioncount'] is None:
            res['sectioncount']=int(s.split(':')[1])
        if s.startswith('ImageBase:') and res['imgbase'] is None and not hyb:
            res['imgbase']=int(s.split(':')[1].strip(),16)
        if s.startswith('HybridObject'): hyb=True
        if s=='CodeMap [' and not cm_done and not hyb: incm=True; continue
        if incm and s==']': incm=False; cm_done=True; continue
        if incm:
            m=re.match(r'(0x[0-9A-Fa-f]+) - (0x[0-9A-Fa-f]+)\s+(\w+)',s)
            if m: res['codemap'].append(dict(type=m.group(3),start=int(m.group(1),16),end=int(m.group(2),16)))
            continue
        if s=='Section {' and not hyb: insec=True; cur={}; continue
        if insec:
            if s.startswith('Name:'): cur['name']=s.split()[1]
            elif s.startswith('VirtualSize:'): cur['vsize']=int(s.split(':')[1],16)
            elif s.startswith('VirtualAddress:'): cur['va']=int(s.split(':')[1],16)
            elif s.startswith('RawDataSize:'): cur['rsize']=int(s.split(':')[1].split('(')[0].strip() if '(' not in s else s.split(':')[1].split()[0],0)
            elif s.startswith('PointerToRawData:'): cur['rptr']=int(s.split(':')[1],16)
            elif s=='}': insec=False; res['sections'].append(cur)
            continue
        if s=='Export {': inexp=True; continue
        if inexp:
            if s.startswith('Name:'): ename=s.split(':',1)[1].strip()
            elif s=='}':
                inexp=False
                (res['hybrid_exports'] if hyb else res['primary_exports']).append(ename)
            continue
    return res

if __name__=='__main__':
    SCR, CAR, ENV, RO = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    ids=[f"k{i:02d}" for i in range(1,13)]
    tsv={r.split('\t')[0]:r.split('\t') for r in open(f"{SCR}/carriers.tsv").read().splitlines()[1:]}
    pred={r.split('\t')[0]:r.split('\t') for r in open(f"{SCR}/predictions.tsv").read().splitlines()[1:]}
    fails=0; out={}
    for cid in ids:
        own=own_parse(f"{CAR}/{cid}.dll")
        env=json.load(open(f"{ENV}/{cid}.json"))
        nr=env['data']['normalized_result']; subj=env['data']['subject']
        ro=parse_readobj(f"{RO}/ro-{cid}.txt")
        checks={
         'subject_sha_eq_own_eq_tsv': subj['digest']['sha256']==own['sha']==tsv[cid][2],
         'segments_eq_own': nr['segments']==own['segments'],
         'segment_count_eq_pred': nr['segment_count']==own['segment_count']==int(pred[cid][2]),
         'sections_eq_readobj': [(s['name'],s['va'],s['vsize'],s['rsize'],s['rptr']) for s in ro['sections']]==[(s['name'],s['va'],s['vsize'],s['rsize'],s['rptr']) for s in own['sections']],
         'proc_eq_own_eq_ro_eq_pred_eq_tsvnative': nr['procedure_count']==own['nnames']==len(ro['primary_exports'])==int(pred[cid][1])==int(tsv[cid][4]),
         'export_names_eq_readobj': own['exports']==ro['primary_exports'],
         'hybrid_n_eq_tsv_ec': len(ro['hybrid_exports'])==int(tsv[cid][5]),
         'document_eq': nr['document']==own['document'],
         'image_base_eq': nr['image_base']==own['image_base'],
         'machine_0xaa64': own['machine']==0xAA64,
         'codemap_has_a64_and_ec': {c['type'] for c in own['codemap']}>={'ARM64','ARM64EC'},
         'codemap_eq_readobj': [(c['type'] if c['type']!='AMD64' else 'X64',c['start'],c['end']) for c in own['codemap']]==[(c['type'],c['start'],c['end']) for c in ro['codemap']],
        }
        bad=[k for k,v in checks.items() if not v]
        fails+=len(bad)
        out[cid]=dict(checks=checks,fails=bad,sha=own['sha'],procs=nr['procedure_count'],
                      segs=nr['segment_count'],names=own['exports'],
                      hybrid=ro['hybrid_exports'])
        print(f"{cid}: {'ALL-PASS' if not bad else 'FAIL:'+','.join(bad)} "
              f"procs={nr['procedure_count']} segs={nr['segment_count']} sha={own['sha'][:12]}")
    json.dump(out,open(f"{SCR}/compare-own.json",'w'),indent=1,sort_keys=True)
    print(f"SUMMARY carriers=12 checks={sum(len(v['checks']) for v in out.values())} fails={fails}")
    sys.exit(0 if fails==0 else 1)
