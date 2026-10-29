
import json, subprocess, importlib.util, os, sys
S, CLONE, LANE, FREEZE = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
def g(*a): return subprocess.run(['git','-C',CLONE,*a],capture_output=True,text=True).stdout.strip()
def imp(name, path):
    sp = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
c1 = imp('c1c', LANE+'/tools/round-50/c1-counter.py')
c2 = imp('c2r', LANE+'/tools/round-50/c2-record.py')
sp = json.loads(subprocess.run(['git','-C',CLONE,'show',FREEZE+':tools/round-50/carriers.json'],capture_output=True).stdout)
BASE='f890bbead20ca2c549487167f56876ae47f1e1a4'
r = c2.Git(CLONE)
out = {'c1_drift_at_base': c1.frozen_drift(CLONE, FREEZE, BASE, sp),
       'c2_freeze_at_base': list(c2.freeze_check(r, FREEZE, BASE))}
for label, path in (('planned','tools/round-50/sqfs-triage-v5.py'),
                    ('outside','tools/round-50-c3/sqfs-triage-v5.py')):
    subprocess.run(['git','-C',CLONE,'checkout','--detach',BASE],check=True,capture_output=True)
    fp = os.path.join(CLONE, path); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp,'w').write('# fixture instrument\n')
    subprocess.run(['git','-C',CLONE,'add',path],check=True,capture_output=True)
    subprocess.run(['git','-C',CLONE,'commit','-q','-m','fixture: C3 instrument at '+path],check=True,capture_output=True)
    rev = g('rev-parse','HEAD')
    out['case_'+label] = {'path': path, 'rev': rev,
        'c1_frozen_drift': c1.frozen_drift(CLONE, FREEZE, rev, sp),
        'c2_freeze_check': list(c2.freeze_check(r, FREEZE, rev))}
print(json.dumps(out, indent=1, sort_keys=True))
