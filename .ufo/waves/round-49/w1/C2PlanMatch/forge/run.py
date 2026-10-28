import hashlib, json, os, re, shutil, subprocess, sys
S='/fast/scratch/hyaku/kaidoku-r49/C2PlanMatch'; C=S+'/clone'; FZ=open(S+'/freeze.txt').read().strip()
W='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49'
CNT=W+'/draft/tools/round-49/c2-mismatch.py'
sha=lambda b: hashlib.sha256(b).hexdigest()
def g(d,*a,inp=None):
    return subprocess.run(['git','-C',d]+list(a),capture_output=True)
def fork(name):
    d=f'{S}/forge/{name}'
    shutil.rmtree(d,ignore_errors=True); shutil.copytree(C,d,symlinks=True)
    assert g(d,'rev-parse','--show-toplevel').stdout.decode().strip()==d, 'toplevel'
    return d
def commit(d,msg):
    assert g(d,'rev-parse','--show-toplevel').stdout.decode().strip()==d
    g(d,'add','-A'); r=g(d,'commit','-q','-m',msg); assert r.returncode==0, r.stderr
    return g(d,'rev-parse','HEAD').stdout.decode().strip()
def rd(d,p): return open(f'{d}/{p}','rb').read()
def wr(d,p,b):
    os.makedirs(os.path.dirname(f'{d}/{p}'),exist_ok=True); open(f'{d}/{p}','wb').write(b)
def count(d,rev,battery=False):
    a=['python3','-I','-B',CNT,'--root',d,'--rev',rev,'--freeze',FZ]+(['--battery'] if battery else [])
    p=subprocess.run(a,capture_output=True,text=True)
    j=json.loads(p.stdout)
    red=[k for k,v in (j.get('atoms') or {}).items() if not v['ok']]
    return dict(exit=p.returncode, mismatches=j.get('mismatches'), reason=j.get('reason'), red=red, why={k:v['why'] for k,v in (j.get('atoms') or {}).items() if not v['ok']}, battery_failing=(j.get('battery') or {}).get('failing'))
LES='corpus/lessons/round-49.md'
out={}
which=sys.argv[1:]
def run(name,fn):
    if which and name not in which: return
    d=fork(name); fn(d); rev=commit(d,'forgery '+name); out[name]=dict(rev=rev, **count(d,rev))
    print(name, json.dumps(out[name])[:900], flush=True)
def f_a4(d):
    wr(d,'.ufo/waves/round-48/w1/C1Battery.md',b'# forged seat report\n')
    t=rd(d,LES).decode().replace('reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers','reports=73 missing=C1Meaning,ScribeReportNumbers')
    wr(d,LES,t.encode())
def f_a5(d):
    p='.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
    new=rd(d,p).rstrip(b'\n')+b' \n'
    wr(d,p,new); raw=sha(new); st=sha(new[:-1])
    t=rd(d,LES).decode()
    t=re.sub(r'c1_raw=\w+ c1_stripped=\w+', f'c1_raw={raw} c1_stripped={st}', t).replace('report_c1=3cc2d72d', f'report_c1={st[:8]}')
    wr(d,LES,t.encode())
def f_a9(d):
    p='corpus/lessons/round-48-verifier-spotcheck.md'
    t=rd(d,p).decode().replace('Both claims verify against fresh runs and committed receipts.','Both claims FAIL against fresh runs and committed receipts.')
    wr(d,p,t.encode())
def f_a1(d):
    t=rd(d,'SCORECARD.md').decode()
    old='**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`'
    assert old in t, 'declared not found'
    wr(d,'SCORECARD.md',t.replace(old,'**Declared freeze:** `0ce6f7611c274955d626501ac576f94892e2daf9`').encode())
    l=rd(d,LES).decode().replace('declared=b6f7ca2a6391964dfdedd477cd560bd42159873a','declared=0ce6f7611c274955d626501ac576f94892e2daf9')
    wr(d,LES,l.encode())
def f_a3_8hex(d):
    t=rd(d,LES).decode().replace('unnamed=577a02a5,8847042a','unnamed=577a02a5,8847042a,33f65a91'); wr(d,LES,t.encode())
def f_a3_40hex(d):
    t=rd(d,LES).decode().replace('unnamed=577a02a5,8847042a','unnamed=577a02a5,8847042a,33f65a9100000000000000000000000000000000'); wr(d,LES,t.encode())
def f_a3_drop(d):
    t=rd(d,LES).decode().replace(' log_33f65a91=3440,3441,3444',''); wr(d,LES,t.encode())
def f_a8_inflate(d):
    t=rd(d,'corpus/SOURCES.md').decode().replace('- 2026-10-28 round 49 — Question: do the S145/S146 locators and rationale survive a re-open? identified 2, screened 2','- 2026-10-28 round 49 — Question: do the S145/S146 locators and rationale survive a re-open? identified 40, screened 2')
    wr(d,'corpus/SOURCES.md',t.encode())
def f_a6_snap(d):
    q1="falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific"
    fake=f'<html><body><h2>2. Backdrop to Popper’s Thought</h2><p>{q1}.</p><h2>3. The Problem of Demarcation</h2></body></html>'.encode()
    old=sha(rd(d,'corpus/evidence/round-49/c2/popper.html')); new=sha(fake)
    wr(d,'corpus/evidence/round-49/c2/popper.html',fake)
    t=rd(d,'corpus/SOURCES.md').decode(); assert old in t; wr(d,'corpus/SOURCES.md',t.replace(old,new).encode())
def f_a1_control_lesson_rewrite(d):
    t=rd(d,'corpus/lessons/round-48.md').decode(); wr(d,'corpus/lessons/round-48.md',t.replace('0f06251b','0f06251c',1).encode())
def f_freeze_edit(d):
    wr(d,'tools/round-49/c2-mismatch.py',rd(d,'tools/round-49/c2-mismatch.py')+b'\n# edit\n')
def f_freeze_restore(d):
    f_freeze_edit(d); commit(d,'edit frozen')
    g(d,'checkout','-q',FZ,'--','tools/round-49/c2-mismatch.py')
for n,f in [('F_A4_fake_seat_report',f_a4),('F_A5_receipt_rewrite',f_a5),('F_A9_closure_rewrite',f_a9),('F_A1_scorecard_redeclare',f_a1),
            ('F_A3_unnamed_8hex_control',f_a3_8hex),('F_A3_unnamed_40hex_fake',f_a3_40hex),('F_A3_drop_log_key',f_a3_drop),
            ('F_A8_identified_inflate',f_a8_inflate),('F_A6_forged_snapshot',f_a6_snap),('F_CTL_round48_lesson_rewrite',f_a1_control_lesson_rewrite),('F_FREEZE_edit',f_freeze_edit)]:
    run(n,f)
if not which or 'F_FREEZE_restore' in which:
    d=fork('F_FREEZE_restore'); f_freeze_restore(d); rev=commit(d,'restore'); out['F_FREEZE_restore']=dict(rev=rev,**count(d,rev)); print('F_FREEZE_restore',json.dumps(out['F_FREEZE_restore'])[:900],flush=True)
json.dump(out,open(S+'/forge/results.json','w'),indent=1,ensure_ascii=False)
