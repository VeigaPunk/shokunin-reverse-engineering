#!/usr/bin/env python3
# Independent v1/v2 packed superblock parser (own implementation; no repo code).
import struct, sys, json, zlib, datetime, os, hashlib
def parse(path):
    b=open(path,'rb').read()
    m=b[:4]
    if m==b'sqsh': e='>'; order='be'
    elif m==b'hsqs': e='<'; order='le'
    else: raise SystemExit('bad magic %r'%m)
    magic,inodes,bytes_used,uid_start,guid_start,it_start,dt_start=struct.unpack(e+'4s6I'.replace('4s','4s'),b[:28]) if False else (m,)+struct.unpack(e+'6I',b[4:28])
    s_major,s_minor=struct.unpack(e+'2H',b[28:32])
    bs1,blog=struct.unpack(e+'2H',b[32:36])
    flags,nuid,ngid=struct.unpack('3B',b[36:39])
    mk,=struct.unpack(e+'I',b[39:43])
    d=dict(path=os.path.basename(path),sha256=hashlib.sha256(b).hexdigest(),size=len(b),magic=m.decode(),order=order,inodes=inodes,bytes_used=bytes_used,uid_start=uid_start,guid_start=guid_start,inode_table_start=it_start,directory_table_start=dt_start,s_major=s_major,s_minor=s_minor,block_size_1=bs1,block_log=blog,flags=flags,no_uids=nuid,no_guids=ngid,mkfs_time=mk,mkfs_utc=datetime.datetime.fromtimestamp(mk,datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    d['zlib_78da_offsets']=[i for i in range(len(b)-1) if b[i]==0x78 and b[i+1]==0xda]
    d['zlib_78xx_offsets']=[i for i in range(len(b)-1) if b[i]==0x78 and b[i+1] in (0x01,0x5e,0x9c,0xda)]
    # validate each 78da stream actually inflates
    ok=[]
    for o in d['zlib_78da_offsets']:
        try:
            dobj=zlib.decompressobj(); out=dobj.decompress(b[o:]); ok.append((o,len(out),dobj.eof,len(b[o:])-len(dobj.unused_data)-o+o))
        except Exception as ex: ok.append((o,'ERR',str(ex)))
    d['inflate']=ok
    # metadata block headers (u16 at inode_table_start, dir_table_start)
    for nm,off in (('inode',it_start),('dir',dt_start)):
        if off+2<=len(b):
            h,=struct.unpack(e+'H',b[off:off+2]); d[nm+'_meta_hdr']=hex(h)
    # tail past bytes_used all zero?
    d['pad_after_bytes_used_zero']=all(x==0 for x in b[bytes_used:])
    return d
if __name__=='__main__':
    out=[parse(p) for p in sys.argv[1:]]
    print(json.dumps(out,indent=1))
