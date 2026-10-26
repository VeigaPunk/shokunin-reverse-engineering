import struct, json, hashlib, os
SB='>IIIIIHHHHHHQQQQQQQQ'
K=('magic','inodes','mkfs_time','block_size','fragments','compression','block_log',
   'flags','no_ids','s_major','s_minor','root_inode','bytes_used','id_table_start',
   'xattr_id_table_start','inode_table_start','directory_table_start',
   'fragment_table_start','lookup_table_start')

def walk(d,start,end,endian,fmtlen=True,limit=100000):
    pos=start;n=0;lens=[]
    while pos<end and n<limit:
        raw=struct.unpack(('<H' if endian=='le' else '>H'),d[pos:pos+2])[0]
        size=raw & 0x7FFF if fmtlen else raw
        if size==0 or size>8192: return dict(landed=False,pos=pos,blocks=n,lens=lens[:4],why='implausible %d at %d'%(size,pos))
        lens.append(raw); pos+=2+size; n+=1
    return dict(landed=(pos==end),pos=pos,blocks=n,lens=lens[:4],why='ended %d vs %d'%(pos,end))

res={}
for cid in ('V1','V2','L1','L2'):
    p='out/%s/carrier'%cid; d=open(p,'rb').read()
    s=dict(zip(K,struct.unpack(SB,d[:96])))
    # LE misread of structural fields, for contrast
    sle=struct.unpack('<IIIIIHHHHHHQQQQQQQQ',d[:96])
    r=dict(sha256=hashlib.sha256(d).hexdigest(),size=len(d),
           magic='0x%08x'%s['magic'], mkfs_time=s['mkfs_time'], bytes_used=s['bytes_used'],
           marker=s['mkfs_time']==s['bytes_used'],
           inode_table_start=s['inode_table_start'], directory_table_start=s['directory_table_start'],
           fragment_table_start=s['fragment_table_start'], inode_delta=s['directory_table_start']-s['inode_table_start'],
           be_inodes=s['inodes'], be_version='%d.%d'%(s['s_major'],s['s_minor']),
           le_inodes=sle[1], le_compression=sle[5], le_block_log=sle[6],
           walks={})
    for label,start,end in (('inode->directory',s['inode_table_start'],s['directory_table_start']),
                            ('directory->fragment',s['directory_table_start'],s['fragment_table_start'])):
        if end==0xFFFFFFFFFFFFFFFF: continue
        for endian in ('le','be'):
            r['walks']['%s/%s'%(label,endian)]=walk(d,start,end,endian)
    res[cid]=r
print(json.dumps(res,indent=1))
