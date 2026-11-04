import argparse,json,os,pathlib,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--root');ap.add_argument('--rev');ap.add_argument('--pkg');ap.add_argument('--work');ap.add_argument('--check-receipt');ap.add_argument('--child-env-log');ap.add_argument('--nonce-commitment');x=ap.parse_args()
w=pathlib.Path(x.work); r=w/'fake-run';r.mkdir(exist_ok=True)
e={'HOME':str(r/'home'),'TMPDIR':str(r/'tmp'),'LANG':'C','PATH':os.environ['PATH']}
if x.child_env_log:
 rows=[]
 for name in ('git','readelf'):
  subprocess.run([name,'--version'],env=e,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  (pathlib.Path(x.child_env_log).parent/(name+'.environ')).write_bytes(b'\0'.join((k+'='+v).encode() for k,v in e.items())+b'\0')
  rows.append({'argv':[name,'--version'],'env':e})
 pathlib.Path(x.child_env_log).write_text(''.join(json.dumps(row)+'\n' for row in rows))
 with open(w/'real-child.environ','wb') as f: subprocess.run(['/usr/bin/env','-0'],env=os.environ,stdout=f)
 print(json.dumps({'met':True,'checker_child_env':{'records':2,'children':{'git':1,'readelf':1},'all_allowlisted':True,'canary_present':False,'home_under_run':True,'tmpdir_under_run':True,'run_root':str(r)}}));sys.exit(0)
receipt=json.loads(pathlib.Path(x.check_receipt).read_text());mode=receipt.get('mode')
clauses={} if mode=='absent' else {'run_nonce':'wrong-nonce' not in x.check_receipt,'run_binding':'broken-binding' not in x.check_receipt}
print(json.dumps({'met':False,'failing':['deliberate contradictory checker failure'],'clauses':clauses}));sys.exit(1 if ('wrong-nonce' in x.check_receipt or 'broken-binding' in x.check_receipt) else 0)
