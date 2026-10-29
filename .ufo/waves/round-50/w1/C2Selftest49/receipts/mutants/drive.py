import subprocess, sys, json, os, concurrent.futures as cf
S='/fast/scratch/hyaku/kaidoku-r50/C2Selftest49/mm'
C=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-49/c2-mismatch.py').read()
T='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w1/C2Selftest49/tools/round-50/selftest-r49-c2.py'
M={
 'a1-stale-clause-off':("if d.get('stale') != stale:","if False:"),
 'a1-rewrite-clause-off':("if les is None or base is None or sha(les) != sha(base):","if False:"),
 'a2-dead-commit-off':("if r.is_commit(dead):","if False:"),
 'a2-real-ancestor-off':("elif not r.ancestor(real, rev):","elif False:"),
 'a3-keys-off':("if keys != sorted(LOG_KEYS):","if False:"),
 'a3-unnamed-off':("if un != sorted(UNNAMED):","if False:"),
 'a3-appendonly-off':("if base is None or now is None or not now.startswith(base):","if False:"),
 'a4-seats-off':("if d.get('seats') != str(len(names)):","if False:"),
 'a5-prefix-off':("if len(q) != 8 or stripped[:8] != q or raw[:8] == q:","if False:"),
 'a6-count-off':("if stated is None or stated != n:","if False:"),
 'a6-heading-off':("if not head or head not in c[5]:","if False:"),
 'a7-ex64-off':("if 'EX_USAGE 64' not in norm:","if False:"),
 'a7-teaches-off':("if not re.search(r'EX_USAGE is 64\\b', c[6]) or re.search(r'EX_USAGE is (?!64\\b)\\S', c[6]):","if False:"),
 'a8-late-filter-off':("ent = [l for l in ent if 'late entry' in l]","pass"),
 'a8-rows-off':("if (int(n.group(1)), int(n.group(2))) != want[:2]:","if False:"),
 'a9-line-off':("if len(hits) != 1 or hits[0].strip() != want:","if False:"),
 'freeze-ancestor-off':("if not r.ancestor(freeze, rev):\n        return 'freeze is not an ancestor of rev'","pass"),
 'freeze-touched-off':("    if t:\n        return 'frozen path touched","    if False:\n        return 'frozen path touched"),
 'dup-lesson-off':("if key in dups:","if False:"),
 'exit-always-0':("code = 0 if res['mismatches'] == 0 else 1","code = 0"),
 'battery-failing-ignored':("                if b['failing']:\n                    code = 1","                if False:\n                    code = 1"),
 'a9-comment-aware (fix)':("hits = [l for l in secs[0] if l.strip().startswith('- A9 ')]","hits = [l for l in __import__('re').sub(r'(?s)<!--.*?-->','',chr(10).join(secs[0])).splitlines() if l.strip().startswith('- A9 ')]"),
}
def go(item):
    name,(a,b)=item
    assert C.count(a)==1,(name,C.count(a))
    f=f'{S}/{name.split()[0]}.py'; open(f,'w').write(C.replace(a,b))
    env=dict(os.environ,TMPDIR=S,HYAKU_SCRATCH='/fast/scratch/hyaku')
    p=subprocess.run([sys.executable,'-I','-B',T,'--mutant-counter',f,'--json-out',f'{S}/{name.split()[0]}.json'],capture_output=True,env=env)
    try: j=json.load(open(f'{S}/{name.split()[0]}.json'))
    except Exception: return name,p.returncode,None,[p.stderr.decode()[-200:]]
    return name,p.returncode,f"{j['passed']}/{j['cases']}",[x['id'] for x in j['failed']]
with cf.ThreadPoolExecutor(4) as ex:
    out=list(ex.map(go,M.items()))
for r in out: print(r)
json.dump(out,open(f'{S}/summary.json','w'),indent=1)
