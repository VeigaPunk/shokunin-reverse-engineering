#!/usr/bin/env python3
"""Independent byte-level layout probe: reads the four R41-C1 carriers without
tools/round-41/sqfs-list.py and without unblob/REA. Confirms, per carrier:
magic 'sqsh', big-endian superblock (major 4 / minor 0 / block_size == 1<<block_log /
bytes_used == file size == mkfs_time), and that the 2-byte metadata block header at
inode_table_start reads as a plausible length ONLY little-endian."""
import hashlib, json, os, struct, sys
FIELDS = [('magic',0,4),('inode_count',4,4),('mkfs_time',8,4),('block_size',12,4),
          ('frag_count',16,4),('compression',20,2),('block_log',22,2),('flags',24,2),
          ('id_count',26,2),('major',28,2),('minor',30,2),('bytes_used',40,8),
          ('id_table_start',48,8),('xattr_table_start',56,8),('inode_table_start',64,8),
          ('directory_table_start',72,8),('fragment_table_start',80,8),('export_table_start',88,8)]
out={}
for cid,path in [a.split('=',1) for a in sys.argv[1:]]:
    b=open(path,'rb').read(); rec={'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    for endian,tag in (('>','be'),('<','le')):
        f={}
        for fn,off,ln in FIELDS:
            v=struct.unpack_from(endian+{2:'H',4:'I',8:'Q'}[ln],b,off)[0]
            f[fn]=b[off:off+4].decode('latin-1') if fn=='magic' else v
        rec[tag]=f
    be=rec['be']
    rec['be_marker_ok']=(be['magic']=='sqsh' and be['major']==4 and be['minor']==0
                         and be['mkfs_time']==be['bytes_used']==len(b)
                         and be['block_size']==(1<<be['block_log']))
    rec['le_major']=rec['le']['major']   # nonsense (1024) => structural fields are big-endian
    its=be['inode_table_start']; hdr=b[its:its+2]
    hle=struct.unpack('<H',hdr)[0]; hbe=struct.unpack('>H',hdr)[0]
    rec['meta_header_at_inode_table']={'hex':hdr.hex(),'le_len':hle&0x7fff,'le_compressed':not(hle&0x8000),
                                       'be_len':hbe&0x7fff,'be_compressed':not(hbe&0x8000),
                                       'le_walk_lands_on_directory_table':
                                           its+2+(hle&0x7fff)==be['directory_table_start']}
    out[cid]=rec
print(json.dumps(out,indent=1,sort_keys=True))
