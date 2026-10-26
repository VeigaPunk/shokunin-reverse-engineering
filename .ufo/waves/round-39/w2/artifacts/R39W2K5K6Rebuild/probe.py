import struct, sys
def u16(b,o): return struct.unpack('>H',b[o:o+2])[0]
def u32(b,o): return struct.unpack('>I',b[o:o+4])[0]
def u64(b,o): return struct.unpack('>Q',b[o:o+8])[0]
path = sys.argv[1]
b=open(path,'rb').read()
inode_tbl=u64(b,64); dir_tbl=u64(b,72); id_tbl=u64(b,48)
pos=dir_tbl; blocks=[]
while pos<id_tbl:
    h=u16(b,pos); sz=h&0x7fff; blocks.append((pos,sz,b[pos+2:pos+2+sz])); pos+=2+sz
print(path,'dir blocks:',[(hex(p),s) for p,s,_ in blocks])
ih=u16(b,inode_tbl); isz=ih&0x7fff; ino=b[inode_tbl+2:inode_tbl+2+isz]
print('inode stream size',isz)
def inode(off):
    t=u16(ino,off); perm=u16(ino,off+2); inum=u32(ino,off+12); p=off+16
    if t==1:
        start=u32(ino,p); nlink=u32(ino,p+4); isz2=u16(ino,p+8); doff=u16(ino,p+10); parent=u32(ino,p+12)
        return ('D',inum,start,nlink,doff,isz2,parent,p+16)
    if t==2:
        start=u32(ino,p); frag=u32(ino,p+4); foff=u32(ino,p+8); sz=u32(ino,p+12)
        nb=0 if sz==0 else (sz+4095)//4096
        p+=16
        return ('F',inum,start,frag,sz,[u32(ino,p+4*i) for i in range(nb)],p+4*nb)
    if t==3:
        nlink=u32(ino,p); tl=u32(ino,p+4); tgt=ino[p+8:p+8+tl]
        return ('L',inum,nlink,tgt,p+8+tl)
    return ('?',t,inum,off)
pos=0; dirs=[]
while pos<len(ino):
    k=inode(pos)
    if k[0]=='D': dirs.append(k)
    if k[0]=='?': print('unknown inode',k); break
    pos=k[-1]
print('n dirs',len(dirs),'consumed',pos,'of',len(ino))
def body_at(byteoff, dsz):
    p=dir_tbl; rem=byteoff
    while True:
        h=u16(b,p); sz=h&0x7fff; data=b[p+2:p+2+sz]
        if rem<sz: return data[rem:rem+dsz]
        rem-=sz; p+=2+sz
        if p>=id_tbl: return None
for d in dirs:
    _,inum,start,nlink,doff,dsz,parent,_=d
    body=body_at(start+doff,dsz)
    n='-'; ok=False
    if body is not None and len(body)==dsz:
        p=0; tot=0
        try:
            while p+12<=len(body):
                cnt=u32(body,p); p+=12
                for _ in range(cnt+1):
                    ns=u16(body,p+6); p+=8+ns+1
                tot+=cnt+1
            ok=(p==len(body)); n=tot
        except Exception:
            ok=False
    print('DIR inum=%-3d start=%-3d(nlink=%d) off=%-4d size=%-3d parent=%-3d body_ok=%s entries=%s'%(
        inum,start,nlink,doff,dsz,parent,ok,n))
