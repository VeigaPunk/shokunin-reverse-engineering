#!/usr/bin/env python3
"""Probe AVM .image tars: superblock of every filesystem-image-like member. Pure Python, no unblob/REA.
usage: probe.py URL=FILE ... -> TSV on stdout. Honors TMPDIR (reads tars via tarfile, no extraction)."""
import sys, tarfile, hashlib, struct, os
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def chain(f,start,end,fmt):
    # walk metadata-block length headers from start; True iff chain lands exactly on end (strong endian test)
    pos=start; n=0
    while pos<end:
        f.seek(pos); hd=f.read(2)
        if len(hd)<2: return f"short@{pos}"
        v=struct.unpack(fmt,hd)[0]; ln=v&0x7fff
        if ln==0 or ln>8192: return f"bad@{pos}(n={n})"
        pos+=2+ln; n+=1
    return f"exact(n={n})" if pos==end else f"overshoot({pos-end})(n={n})"
def rd(path,url,status):
    st=os.path.getsize(path); hs=sha(path)
    try: t=tarfile.open(path)
    except Exception as e:
        print(f"{url}\t{status}\t{st}\t{hs}\t-\t-\tNOT-TAR:{e}\t-\t-\t-\t-"); return
    for m in t:
        if not m.isfile(): continue
        f=t.extractfile(m); h=f.read(96)
        if len(h)<96 or h[:4] not in (b'sqsh',b'hsqs'):
            if 'filesystem' in m.name: print(f"{url}\t{status}\t{st}\t{hs}\t{m.name}\t{m.size}\t{h[:4]!r}\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-\t-")
            continue
        e='>' if h[:4]==b'sqsh' else '<'
        (mg,ino,mt,bs,fr,comp,bl,fl,nid,maj,mino,root,used,idt,xat,it,dt,ft,lt)=struct.unpack(e+'4sIIIIHHHHHHQQQQQQQQ',h[:96])
        marker = (mt==used)
        f.close(); f=t.extractfile(m); msha=hashlib.sha256(f.read()).hexdigest()
        f.close(); f=t.extractfile(m); f.seek(it); hd=f.read(2)
        if len(hd)<2: print(f"{url}\t{status}\t{st}\t{hs}\t{m.name}\t{m.size}\t{mg.decode()}\tv{maj}.{mino}\tcomp={comp}\t-\t-\t-\t-\t-\tit_hdr=UNREADABLE(it={it})\t-"); continue
        le=struct.unpack('<H',hd)[0]; be=struct.unpack('>H',hd)[0]
        def plaus(v): return (v&0x7fff)<=8192 and (v&0x7fff)>0
        reading=f"LE={le&0x7fff}{'u' if le&0x8000 else 'c'}{'ok' if plaus(le) else 'bad'};BE={be&0x7fff}{'u' if be&0x8000 else 'c'}{'ok' if plaus(be) else 'bad'}"
        f.close(); f=t.extractfile(m); cl=chain(f,it,dt,'<H'); f.close(); f=t.extractfile(m); cb=chain(f,it,dt,'>H')
        reading+=f";inode_chain_LE={cl};inode_chain_BE={cb}"
        print(f"{url}\t{status}\t{st}\t{hs}\t{m.name}\t{m.size}\t{mg.decode()}\tv{maj}.{mino}\tcomp={comp}\tbs={bs}\tinodes={ino}\tmkfs_time={mt}\tbytes_used={used}\tmarker={'YES' if marker else 'no'}\tit_hdr={reading}\tbytes_used_le_file={'==' if used==m.size else ('<' if used<m.size else '>')}{m.size-used}\t{msha}")
if __name__=='__main__':
    print("url\thttp_status\tbytes\tsha256\tmember\tmember_bytes\tmagic\tver\tcomp\tblock_size\tinodes\tmkfs_time\tbytes_used\tmarker\tinode_table_first_len_hdr\tmember_vs_bytes_used\tmember_sha256")
    for a in sys.argv[1:]:
        u,p=a.split('=',1); rd(p,u,200)
