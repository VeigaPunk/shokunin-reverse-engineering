# Read-only census: directory indexes (GET) + tar-header and superblock reads by HTTP Range (<=512 B each).
import re,struct,urllib.request,concurrent.futures as cf,sys,time
B='https://download.avm.de/fritzbox/'
REQ=[0]
def get(u,rng=None):
    r=urllib.request.Request(u,headers={'User-Agent':'kaidoku-r50-c1-adversary/1.0'})
    if rng: r.add_header('Range','bytes=%d-%d'%rng)
    REQ[0]+=1
    with urllib.request.urlopen(r,timeout=40) as resp:
        return resp.read()
def links(h): return re.findall(r'href="([^"]+)"',h)
def tar_members(u,maxn=40):
    out=[]; off=0
    for _ in range(maxn):
        try:
            hd=get(u,(off,off+511))
        except urllib.error.HTTPError as ex:
            if ex.code==416: break
            raise
        if len(hd)<512 or hd==b'\0'*512: break
        name=hd[:100].split(b'\0')[0].decode('latin1')
        size=int(hd[124:136].split(b'\0')[0].strip() or b'0',8)
        typ=hd[156:157]
        out.append((name,size,off+512,typ))
        off=off+512+((size+511)//512)*512
    return out
def sb(u,doff):
    d=get(u,(doff,doff+47))
    mg=d[:4]
    if mg not in (b'hsqs',b'sqsh'): return {'magic':mg.hex()}
    e='<' if mg==b'hsqs' else '>'
    maj,mi=struct.unpack(e+'HH',d[28:32])
    mk=struct.unpack(e+'I',d[8:12])[0]; bu=struct.unpack(e+'Q',d[40:48])[0]
    return dict(magic=mg.decode(),endian='LE' if e=='<' else 'BE',ver=f'{maj}.{mi}',comp=struct.unpack(e+'H',d[20:22])[0],mkfs=mk,bytes_used=bu,marker=(mk==bu))
def image_census(u):
    rows=[]
    try:
        mem=tar_members(u)
    except Exception as ex:
        return [dict(url=u,error=str(ex)[:80])]
    for name,size,doff,typ in mem:
        if typ not in (b'0',b'\0') : continue
        if name.endswith('filesystem.image'):
            try: s=sb(u,doff)
            except Exception as ex: s={'error':str(ex)[:60]}
            rows.append(dict(url=u,member=name,member_size=size,member_off=doff,exact_rootfs_path=(name=='./var/tmp/filesystem.image'),**s))
    if not rows: rows.append(dict(url=u,member=None,note='no filesystem.image member',members=len(mem)))
    return rows
def sub(u):
    return [l.rstrip('/') for l in links(get(u).decode('utf8','replace')) if l.endswith('/') and not l.startswith('..') and not l.startswith('/')]
def modelroots():
    return [l.rstrip('/') for l in links(get(B).decode()) if l.startswith('fritzbox-') and l.endswith('/')]
def fritzos_images(model):
    res=[]
    for loc in sub(B+model+'/'):
        base=f'{B}{model}/{loc}/fritz.os/'
        try:
            h=get(base).decode('utf8','replace')
        except Exception:
            continue
        for m in re.finditer(r'href="([^"]+\.image)">[^<]*</a>\s+(\S+ \S+)\s+(\d+)',h):
            res.append(dict(model=model,locale=loc,url=base+m.group(1),file=m.group(1),index_date=m.group(2),index_bytes=int(m.group(3))))
    return res
if __name__=='__main__':
    t0=time.time()
    roots=modelroots()
    import json
    allimgs=json.load(open('census-images.json'))
    with cf.ThreadPoolExecutor(6) as ex:
        res=list(ex.map(lambda i: (i,image_census(i['url'])), allimgs))
    out=[]
    for i,rows in res:
        for r in rows:
            r.update({k:i[k] for k in ('model','locale','file','index_date','index_bytes')})
            out.append(r)
    json.dump(out,open('census-members.json','w'),indent=1)
    print('MEMBER_ROWS',len(out),'requests',REQ[0],'t',round(time.time()-t0),flush=True)
