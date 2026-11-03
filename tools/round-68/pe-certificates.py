#!/usr/bin/env python3
"""Static bounded PE certificate byte custody, never execute or load subject.
--pe PATH: 0 descriptive result; 1 refused; 64 usage. --selftest: 0/1.
"""
import hashlib,json,os,stat,struct,sys,tempfile,pathlib,subprocess
class Refused(Exception):pass
def need(test):
    if not test:raise Refused()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as f:
        s=os.fstat(f.fileno());need(stat.S_ISREG(s.st_mode) and s.st_size<=1048576)
        b=f.read(1048577);need(len(b)<=1048576)
    return b
def solve(b):
    need(len(b)>=64 and b[:2]==b'MZ')
    pe=struct.unpack_from('<I',b,60)[0]
    need(pe+24<=len(b) and b[pe:pe+4]==b'PE\0\0')
    sections=struct.unpack_from('<H',b,pe+6)[0]
    size=struct.unpack_from('<H',b,pe+20)[0]
    opt=pe+24;need(sections<=96 and size>=2 and opt+size<=len(b))
    magic=struct.unpack_from('<H',b,opt)[0];need(magic in (0x10b,0x20b))
    fixed,fmt=(96,'pe32') if magic==0x10b else (112,'pe32plus')
    need(size>=fixed)
    count=struct.unpack_from('<I',b,opt+fixed-4)[0]
    need(fixed+count*8<=size)
    structural=opt+size+sections*40;need(structural<=len(b))
    absent={'status':'absent','format':fmt}
    if count<5:return absent
    pointer,length=struct.unpack_from('<II',b,opt+fixed+32)
    if pointer==0 and length==0:return absent
    need(pointer!=0 and length!=0 and pointer%8==0 and pointer>=structural)
    need(length<=4096 and pointer+length<=len(b))
    cursor=pointer;end=pointer+length;records=[]
    while cursor<end:
        need(len(records)<64 and cursor+8<=end)
        n,revision,kind=struct.unpack_from('<IHH',b,cursor);need(n>=8)
        stride=(n+7)//8*8
        need(cursor+n<=end and cursor+stride<=end)
        records.append({'offset':cursor,'length':n,'revision':revision,'type':kind,'declared_content_sha256':sha(b[cursor+8:cursor+n]),'alignment_padding_sha256':sha(b[cursor+n:cursor+stride])})
        cursor+=stride
    need(cursor==end)
    return {'status':'ok','format':fmt,'table_offset':pointer,'table_size':length,'records':records}
def main(argv):
    if argv==['--selftest']:
        with tempfile.TemporaryDirectory(prefix='kaidoku68-reader-') as t:
            p=pathlib.Path(t)/'bad.bin';p.write_bytes(b'not a PE');tests={}
            for name,path in [('invalid',p),('absent',p.with_name('absent'))]:
                r=subprocess.run([sys.executable,'-I','-B',__file__,'--pe',str(path)],capture_output=True,text=True)
                tests[name]=r.returncode==1 and json.loads(r.stdout)=={'status':'refused'}
            link=p.with_name('link');link.symlink_to(p)
            r=subprocess.run([sys.executable,'-I','-B',__file__,'--pe',str(link)],capture_output=True,text=True)
            tests['symlink']=r.returncode==1 and json.loads(r.stdout)=={'status':'refused'}
            print(json.dumps({'checks':tests,'ok':all(tests.values())}));return 0 if all(tests.values()) else 1
    if len(argv)!=2 or argv[0]!='--pe':return 64
    try:out=solve(read(argv[1]));code=0
    except (Refused,OSError,ValueError,struct.error):out={'status':'refused'};code=1
    print(json.dumps(out,sort_keys=True));return code
if __name__=='__main__':raise SystemExit(main(sys.argv[1:]))
