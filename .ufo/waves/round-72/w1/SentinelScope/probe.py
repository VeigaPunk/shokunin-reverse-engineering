#!/usr/bin/env python3
"""Read-only frozen-instrument probes; only seat scratch and receipts are written."""
import contextlib, hashlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile
R = pathlib.Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
S = pathlib.Path('/fast/scratch/hyaku/kaidoku-r72/SentinelScope')
OUT = R / '.ufo/waves/round-72/w1/SentinelScope'
REV = '34fe7aa70b627d92e2d27dbce308d9f5bebda63d'
NAMES = ['packed-elf.py','seam-probe.py','mutation-check.py','capsule-audit.py','capsule_audit.py','controls.py']
def git(*args):
    return subprocess.check_output(['/usr/bin/git','-C',str(R),*args])
def run(args):
    p = subprocess.run([sys.executable,'-I','-B',*map(str,args)], cwd=R, env={**os.environ,'TMPDIR':str(S),'PYTHONDONTWRITEBYTECODE':'1'}, capture_output=True, text=True, timeout=60)
    try: payload = json.loads(p.stdout)
    except ValueError: payload = None
    return {'rc':p.returncode,'json':payload,'stderr':p.stderr[-1500:]}
def entries():
    return sorted(p.name for p in S.iterdir())
S.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
result = {'revision':REV,'axes':['execution provenance','read containment','scratch placement','canary disclosure','failure cleanup'],'sources':{}}
try:
    for name in NAMES:
        data = git('show',f'{REV}:tools/round-72/{name}')
        (S/name).write_bytes(data)
        result['sources'][name] = hashlib.sha256(data).hexdigest()
    receipt = json.loads((R/'.ufo/waves/round-72/l1/pre/route-at-declaration.json').read_text())
    outside = pathlib.Path('/etc/hostname')
    outside_sha = hashlib.sha256(outside.read_bytes()).hexdigest()
    (S/'outside-link').symlink_to(outside)
    result['capsule_paths'] = {}
    for label, path in [('absolute',str(outside)),('traversal',os.path.relpath(outside,R)),('symlink',str(S/'outside-link'))]:
        changed = json.loads(json.dumps(receipt))
        changed.setdefault('child_env_observed',{})['log'] = path
        rp = S/f'{label}.json'
        rp.write_text(json.dumps(changed))
        res = run([S/'packed-elf.py','--root',R,'--rev',REV,'--check-receipt',rp,'--work',S])
        result['capsule_paths'][label] = res
    sys.path.insert(0,str(S))
    import capsule_audit
    result['direct_outside_audit'] = capsule_audit.audit(str(outside),{})
    result['outside_sha_matches'] = result['direct_outside_audit'].get('sha256') == outside_sha
    empty = S/'nonobject.json'; empty.write_text('[]')
    before = entries()
    result['checker_early_failure'] = run([S/'packed-elf.py','--root',R,'--rev',REV,'--check-receipt',empty])
    result['checker_early_failure']['leaked'] = sorted(set(entries())-set(before))
    before = entries()
    result['controls_missing_input'] = run([S/'controls.py','--root',R,'--base-rev',REV,'--decl-rev',REV,'--receipt',S/'missing','--commitment','0'*64,'--expect-upx','/usr/bin/upx','--work',S])
    result['controls_missing_input']['leaked'] = sorted(set(entries())-set(before))
    before = entries()
    result['mutation_bad_pristine'] = run([S/'mutation-check.py','--root',R,'--rev',REV,'--tool','tools/round-72/controls.py','--patch-set','r72','--work',S])
    result['mutation_bad_pristine']['leaked'] = sorted(set(entries())-set(before))
    result['scratch_modes'] = {p.name:oct(p.stat().st_mode & 0o777) for p in S.iterdir() if p.is_dir()}
    scan = subprocess.run(['/usr/bin/git','-C',str(R),'grep','-n','-F','-e','probe-canary-r72','-e','probe-canary','-e','control-canary',REV,'--','.'],capture_output=True,text=True)
    (OUT/'canary-tracked.txt').write_text(scan.stdout)
    result['canary_scan'] = {'rc':scan.returncode,'matching_lines':len(scan.stdout.splitlines()),'scope':f'git grep at {REV} (tracked frozen bytes)'}
    result['scratch_cleanup'] = 'finally shutil.rmtree(S); receipt written before removal'
    (OUT/'observations.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('capsule_paths',)},indent=2))
    print('capsule checker results:',json.dumps({k:{'rc':v['rc'],'capsule':(v['json'] or {}).get('capsule')} for k,v in result['capsule_paths'].items()}))
finally:
    shutil.rmtree(S)
