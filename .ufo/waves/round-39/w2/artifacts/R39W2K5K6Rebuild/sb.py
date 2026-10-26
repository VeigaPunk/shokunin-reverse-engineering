import struct,sys,hashlib
for p in sys.argv[1:]:
    b=open(p,'rb').read()
    e='>' # BE
    magic=b[:4]
    print(p, 'magic', magic, 'len', len(b), 'sha', hashlib.sha256(b).hexdigest())
    (ninodes,mkfs,bsz,frags,comp,log,flags,no_ids,vmaj,vmin,root,bytes_used,
     id_tbl,xattr_tbl,inode_tbl,dir_tbl,frag_tbl,lookup_tbl)=struct.unpack(e+'IIIIHHHHHHQQQQQQQQ', b[4:96])
    print('  inodes=%d mkfs=%d block_size=%d frags=%d comp_id=%d block_log=%d flags=%#x ids=%d version=%d.%d root_ref=%#x bytes_used=%d'%(
      ninodes,mkfs,bsz,frags,comp,log,flags,no_ids,vmaj,vmin,root,bytes_used))
    print('  inode_tbl=%d dir_tbl=%d id_tbl=%d frag_tbl=%#x xattr=%#x lookup=%#x'%(inode_tbl,dir_tbl,id_tbl,frag_tbl,xattr_tbl,lookup_tbl))
    # walk inode table metadata (uncompressed here) and collect reg/lreg data block sizes
    data_start=96
    def meta_region(start,end):
        out=b'';pos=start
        while pos<end:
            hdr=struct.unpack(e+'H',b[pos:pos+2])[0]; pos+=2
            size=hdr & 0x7fff
            if hdr & 0x8000: chunk=b[pos:pos+size]; pos+=size
            else:
                raise SystemExit('compressed metadata unsupported in this probe')
            out+=chunk
        return out
    ino=meta_region(inode_tbl,dir_tbl)
    # find reg inodes by header scan is unreliable; instead parse sequentially
    pos=0; found=0
    while pos+16<=len(ino):
        t,perm,uid,gid,mtime,inum=struct.unpack(e+'HHHHII',ino[pos:pos+16])
        pos+=16
        if t==2:
            start,frag,off,fsize=struct.unpack(e+'IIII',ino[pos:pos+16]); pos+=16
            nb=(fsize+bsz-1)//bsz
            sizes=[]
            for _ in range(nb):
                v=struct.unpack(e+'I',ino[pos:pos+4])[0]; pos+=4; sizes.append(v)
            found+=1
            c=[s for s in sizes if s and not (s & 0x01000000)]
            rawv=[s & 0xffffff for s in sizes if s & 0x01000000]
            print('   REG ino=%d start=%d frag=%#x size=%d blocks=%d compressed_blocks=%d raw_blocks=%d first_xz_hdr=%s'%(
                inum,start,frag,fsize,len(sizes),len(c),len(rawv),
                b[start:start+6].hex() if c else '-'))
        elif t in (9,10):
            print('   EXTENDED inode type',t,'at pos',pos-16,'(probe stops)'); break
        elif t==1:
            pos+=16+4+4+2+2+4
        elif t==3:
            nlink,tsz=struct.unpack(e+'II',ino[pos:pos+8]); pos+=8+tsz
        else:
            print('   type',t,'unexpected; stop'); break
