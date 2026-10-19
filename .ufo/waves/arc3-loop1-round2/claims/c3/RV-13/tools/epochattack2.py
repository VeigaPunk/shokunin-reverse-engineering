import os,subprocess,sys,time
d='/var/tmp/rv13/epochattack2'; os.makedirs(d,exist_ok=True)
f=os.path.join(d,'subject.conf')
open(f,'wb').write(b'stand\n'+os.urandom(4100)); os.utime(f,(1700000000,1700000000))
TOOL='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/custody-pair/custody-pair.py'
ABL='/var/tmp/rv13/epoch-only.py'
for name,tool in (('ablated-epoch-only',ABL),('landed-112d01dc',TOOL)):
    rec=os.path.join(d,name+'.json')
    subprocess.run(['python3',tool,'capture','--out',rec,'--paths',f],check=True,capture_output=True)
    st=os.stat(f); data=open(f,'rb').read()
    open(f,'r+b').write(data); os.utime(f,ns=(st.st_atime_ns,st.st_mtime_ns))
    post=os.stat(f)
    p=subprocess.run(['python3',tool,'verify',rec,'--live'],capture_output=True,text=True)
    line=[l for l in p.stdout.splitlines() if l.startswith('PATH ')]
    print('%s: pre_ctime_epoch=%d post_ctime_epoch=%d same_second=%s' % (name,st.st_ctime,post.st_ctime,st.st_ctime==post.st_ctime))
    print('   '+(line[0] if line else p.stdout.strip()[:120]))
    print('   exit=%d' % p.returncode)
