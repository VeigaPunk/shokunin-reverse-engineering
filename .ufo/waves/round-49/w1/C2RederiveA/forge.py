import subprocess, json, sys, re
D='/fast/scratch/hyaku/kaidoku-r49/C2RederiveA/clone'
F='6b4eb599e1808acc9a8b887b9014ade8d5951def'; A='86504a1ad5ce56157b9fe62e1001ca27c65eb08a'
BASE='e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
g=lambda *a: subprocess.run(['git','-C',D]+list(a),capture_output=True,text=True)
assert g('rev-parse','--show-toplevel').stdout.strip()==D
def forge(name, edits):
    g('checkout','-q','--detach',A)
    for p,fn in edits.items():
        t=open(f'{D}/{p}',encoding='utf8').read(); t2=fn(t); assert t2!=t,(name,p)
        open(f'{D}/{p}','w',encoding='utf8').write(t2)
    g('add','-A'); r=g('commit','-q','-m','forge '+name); assert r.returncode==0,r.stderr
    rev=g('rev-parse','HEAD').stdout.strip()
    o=f'{D}/../fo-{name}.json'
    p=subprocess.run(['python3','-I','-B',f'{D}/tools/round-49/c2-mismatch.py','--root',D,'--rev',rev,'--freeze',F,'--json-out',o],capture_output=True,text=True)
    j=json.load(open(o)); bad={k:v['why'] for k,v in j['atoms'].items() if not v['ok']}
    print(name,'rev',rev[:8],'exit',p.returncode,'mismatches',j['mismatches'],'red',bad)
LES='corpus/lessons/round-49.md'
sub=lambda a,b:(lambda t:t.replace(a,b))
forge('A3-partial-set', {LES: lambda t: re.sub(r'- A3 .*', '- A3 log_2e785632=3440,3441,3445 unnamed=deadbeef', t)})
forge('A3-one-hash-unnamed-wrong', {LES: lambda t: re.sub(r'- A3 .*', '- A3 log_33f65a91=3440,3441,3444 unnamed=577a02a5', t)})
forge('A2-other-real', {LES: lambda t: re.sub(r'- A2 .*', '- A2 dead=%s actual=%s'%(BASE[:8]+'0'*32, BASE), t)})
sc='SCORECARD.md'
forge('A1-scorecard-rewritten', {sc: sub('**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`','**Declared freeze:** `%s`'%BASE),
   LES: sub('declared=b6f7ca2a6391964dfdedd477cd560bd42159873a','declared=%s'%BASE)})
