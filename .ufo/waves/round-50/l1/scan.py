import re,struct,sys,urllib.request,concurrent.futures as cf
B='https://download.avm.de/fritzbox/'
def get(u,rng=None):
    r=urllib.request.Request(u)
    if rng: r.add_header('Range','bytes=%d-%d'%rng)
    return urllib.request.urlopen(r,timeout=30).read()
def models():
    h=get(B).decode()
    return re.findall(r'href="(fritzbox-[^"/]+)/"',h)
def img(m):
    for loc in ('deutschland','international',''):
        try:
            u=f'{B}{m}/{loc}/fritz.os/' if loc else f'{B}{m}/fritz.os/'
            h=get(u).decode()
            fs=re.findall(r'href="([^"]+\.image)"',h)
            if fs: return u+fs[-1]
        except Exception as e: pass
def probe(m):
    try:
        u=img(m)
        if not u: return m,'noimage'
        off=0; 
        for _ in range(40):
            hd=get(u,(off,off+511))
            name=hd[:100].split(b'\0')[0].decode(); size=int(hd[124:135].split(b'\0')[0] or b'0',8)
            if name.endswith('filesystem.image'):
                d=get(u,(off+512,off+512+47))
                mg=d[:4]; e='<' if mg==b'hsqs' else '>'
                mk=struct.unpack(e+'I',d[8:12])[0]; maj,mi=struct.unpack(e+'HH',d[28:32]); comp=struct.unpack(e+'H',d[20:22])[0]
                bu=struct.unpack(e+'Q',d[40:48])[0]
                return m,(u.split('/')[-1],mg,maj,mi,'comp',comp,'avm' if mk==bu else 'std',size)
            off+=512+((size+511)//512)*512
        return m,(u,'no-fs-member')
    except Exception as e: return m,'err '+str(e)[:60]
ms=models()
with cf.ThreadPoolExecutor(8) as ex:
    for m,r in ex.map(probe,ms): print(m,r,flush=True)
