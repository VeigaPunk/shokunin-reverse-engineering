#!/usr/bin/env python3
"""Documentary census only; not a claim counter or production gate."""
import collections,json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]); rev=sys.argv[2]
w=root/'.ufo/waves/round-52'
d=json.loads((w/'w1-dispatch.json').read_text())
r=json.loads((w/'r52-w1-results.json').read_text())
tasks=d['taskCall']['tasks']; roles=collections.Counter(t['agent'] for t in tasks)
statuses={}; missing=[]; malformed=[]
for t in tasks:
 p=w/'w1'/t['name']/'status.json'
 if not p.exists(): missing.append(t['name']); continue
 try: statuses[t['name']]=json.loads(p.read_text()).get('status','unknown')
 except (ValueError,OSError): malformed.append(t['name'])
def git(*a): return subprocess.check_output(['/usr/bin/git','--no-replace-objects','-C',str(root),*a],text=True)
paths=set(git('ls-tree','-r','--name-only',rev).splitlines())
old=json.loads(git('show',rev+':.ufo/waves/round-50/l1/scores/c1-after-attempt2.json'))
print(json.dumps({'revision':rev,'seats':len(tasks),'results_rows':len(r['results']),'role_mix':dict(roles),'strict_attack_seats':sum(roles[k] for k in ('reviewer','critic','mutation-tester','labrat')),'status_histogram':dict(collections.Counter(statuses.values())),'status_by_seat':statuses,'missing_status':missing,'malformed_status':malformed,'handoff_has_ids':all('id' in x for x in r['results']),'handoff_has_status':all('status' in x for x in r['results']),'dead_seats':'not derivable from handoff; failed/blocked statuses are work outcomes, not provider deaths','historical_c1_matched':old.get('carriers_matched'),'historical_c1_exit':old.get('exit_code'),'r52_production_tools':sorted(p for p in paths if p.startswith('tools/round-52/')),'r52_data_receipts':sorted(p for p in paths if p.startswith('corpus/evidence/round-52/')),'r52_freeze_record_present':'.ufo/waves/round-52/l1/FREEZE' in paths},indent=2,sort_keys=True))
