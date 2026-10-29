#!/usr/bin/env python3
"""Fixture-clone measurement: where can the C3 instrument land without tripping C1 drift?"""
import importlib.util, json, os, subprocess, sys, tempfile
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
sp = importlib.util.spec_from_file_location('cc', LANE + '/tools/round-50/c1-counter.py')
cc = importlib.util.module_from_spec(sp); sp.loader.exec_module(cc)

def fixture(land_path):
    D = tempfile.mkdtemp(prefix='drift-', dir='/fast/scratch/hyaku/kaidoku-r50/w3-SentReceipts')
    subprocess.run(['git', '-C', D, 'init', '-q'], check=True)
    assert subprocess.run(['git','-C',D,'rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip() == D
    for k, v in (('user.name','fixture'), ('user.email','fixture@example.invalid')):
        subprocess.run(['git','-C',D,'config',k,v], check=True)
    for p, c in (('plans/round-50-claims.md','# plan\n'), ('tools/round-50/c1-counter.py','print(1)\n'),
                 ('tools/round-50/carriers.json','{}\n'), ('tools/round-50/gap-rule.json','{}\n'),
                 ('tools/round-50/fetch-vendor.py','ORIGINAL\n')):
        fp = os.path.join(D, p); os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp,'w').write(c)
    subprocess.run(['git','-C',D,'add','-A'],check=True)
    subprocess.run(['git','-C',D,'commit','-q','-m','freeze'],check=True)
    F = subprocess.run(['git','-C',D,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    lp = os.path.join(D, land_path); os.makedirs(os.path.dirname(lp), exist_ok=True)
    open(lp,'w').write('# instrument\n')
    subprocess.run(['git','-C',D,'add','-A'],check=True)
    subprocess.run(['git','-C',D,'commit','-q','-m','land instrument'],check=True)
    R = subprocess.run(['git','-C',D,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    drift = cc.frozen_drift(D, F, R, {'carriers':[]})
    ls = subprocess.run(['git','-C',D,'ls-tree','-r','--name-only',R,'--','tools/round-50'],capture_output=True,text=True).stdout.split()
    in_census = any('round-50-c3' in x for x in ls)
    subprocess.run(['rm','-rf',D])
    return drift, in_census

for p in ('tools/round-50/sqfs-triage-v5.py', 'tools/round-50-c3/sqfs-triage-v5.py'):
    d, c = fixture(p)
    print(json.dumps({'land_path': p, 'frozen_drift': d,
                      'c1_exit_would_be': 2 if d else 0,
                      'in_b9_census_tools_round-50': c}))
