#!/usr/bin/env python3
"""R64 admission: committed pins, chronology, complete semantic receipts and craft binding.
0 met, 1 named mismatch, 2 unevaluable. Read-only Git objects, never runs candidate code.
--selftest writes/removes one isolated private Git repository per case.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

CLAIMS = '.ufo/waves/round-64/claims.json'
RECEIPT = '.ufo/waves/round-64/data/comparison.json'
FIXTURES = '.ufo/waves/round-64/data/fixtures/'
KNOWLEDGE = 'corpus/knowledge/2026-11-03-r64-zip-occurrences.md'
PREDICATE = 'All frozen case names match fresh post-freeze ZIP occurrence records and refusal classes, with committed provenance and a source-linked craft rule.'
SELF = 'tools/round-64/admit.py'
PLAN = 'plans/round-64-claims.md'

def sha(b): return hashlib.sha256(b).hexdigest()
def equal(a,b): return json.dumps(a,sort_keys=True,separators=(",",":")) == json.dumps(b,sort_keys=True,separators=(",",":"))
def env():
    e = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    e.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', GIT_NO_REPLACE_OBJECTS='1',
             GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='core.hooksPath', GIT_CONFIG_VALUE_0='/dev/null',
             GIT_CONFIG_KEY_1='core.attributesFile', GIT_CONFIG_VALUE_1='/dev/null')
    return e

def git(root,*args):
    p=subprocess.run(['git','-C',str(root),*args],capture_output=True,env=env(),timeout=30)
    if p.returncode: raise ValueError('git_failed:'+str(args[:2]))
    return p.stdout

def blob(root,rev,path): return git(root,'show',rev+':'+path)
def obj(b):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise ValueError('duplicate_json_key')
            d[k]=v
        return d
    return json.loads(b,object_pairs_hook=pairs)
def instant(s):
    x=dt.datetime.fromisoformat(s.replace('Z','+00:00'))
    if x.tzinfo is None: raise ValueError('timezone_required')
    return x.timestamp()
def first(root,rev,path):
    lines=git(root,'log','--diff-filter=A','--format=%ct',rev,'--',path).decode().splitlines()
    if not lines: raise ValueError('first_commit_absent:'+path)
    return min(map(int,lines))

def audit(root,rev,freeze):
    rev=git(root,'rev-parse','--verify',rev+'^{commit}').decode().strip()
    freeze=git(root,'rev-parse','--verify',freeze+'^{commit}').decode().strip()
    git(root,'merge-base','--is-ancestor',freeze,rev)
    c=obj(blob(root,freeze,CLAIMS)); findings=[]
    def check(ok,name):
        if not ok: findings.append(name)
    actual_freeze=git(root,'log','--diff-filter=A','--format=%H',rev,'--',CLAIMS).decode().splitlines()[-1]
    check(freeze==actual_freeze,'not_first_freeze')
    check(c['predicate']==PREDICATE,'predicate_mismatch')
    for path in (CLAIMS,PLAN):
        check(blob(root,actual_freeze,path)==blob(root,rev,path),'frozen_record_changed:'+path)
        check(not git(root,'log','--format=%H',actual_freeze+'..'+rev,'--',path).strip(),'frozen_record_touched:'+path)
    check(c['instruments'].get(SELF)==sha(Path(__file__).read_bytes()),'executed_gate_pin')
    frozen_time=int(git(root,'show','-s','--format=%ct',freeze).decode())
    birth=0
    for path,pin in c['instruments'].items():
        check(sha(blob(root,freeze,path))==pin,'freeze_pin:'+path)
        check(sha(blob(root,rev,path))==pin,'current_pin:'+path)
        check(not git(root,'log','--format=%H',freeze+'..'+rev,'--',path).strip(),'instrument_touched:'+path)
        birth=max(birth,first(root,freeze,path))
    check(birth<=frozen_time,'instrument_after_freeze')
    r=obj(blob(root,rev,RECEIPT)); expected=obj(blob(root,rev,FIXTURES+'expected.json'))
    check(sorted(expected)==sorted(c['case_names']),'oracle_case_set')
    check(r.get('expected_sha256')==sha(blob(root,rev,FIXTURES+'expected.json')),'oracle_pin')
    check(r.get('reader_sha256')==c['instruments']['tools/round-64/zip-occurrences.py'],'reader_pin')
    rows=r.get('results',[])
    check(isinstance(rows,list) and sorted(x.get('case','') for x in rows)==sorted(c['case_names']),'receipt_case_set')
    check(type(r.get('cases')) is int and type(r.get('matched')) is int and type(r.get('exit')) is int and r.get('cases')==len(c['case_names']) and r.get('matched')==len(c['case_names']) and r.get('exit')==0 and r.get('finding')=='all_matched','summary')
    for path in [RECEIPT,FIXTURES+'expected.json']+[FIXTURES+n+'.zip' for n in c['case_names']]:
        check(first(root,rev,path)>=max(birth,frozen_time),'preinstrument_data:'+path)
    for name,want in expected.items():
        check(sha(blob(root,rev,FIXTURES+name+'.zip'))==want['archive_sha256'],'fixture_pin:'+name)
    for row in rows:
        name=row['case']; want=expected[name]
        check(instant(row['utc'])>=max(birth,frozen_time),'preinstrument_run:'+name)
        check(type(row['exit']) is int and row['exit']==want['exit'],'process_exit:'+name)
        got=obj(row['stdout'])
        check(type(got.get('exit')) is int and got.get('exit')==want['exit'] and type(got.get('schema')) is int and got.get('schema')==1,'body_exit:'+name)
        check(got.get('finding')==want['finding'],'finding:'+name)
        check(got.get('reader_sha256')==r['reader_sha256'],'body_reader_pin:'+name)
        if want['exit']==0:
            for k in ('archive_sha256','archive_size','occurrences','duplicate_groups'):
                check(equal(got.get(k),want[k]),'semantic:'+name+':'+k)
        else:
            check('occurrences' not in got and 'duplicate_groups' not in got,'partial_error:'+name)
    skill=blob(root,rev,'SKILL.md').decode(); knowledge=blob(root,rev,KNOWLEDGE).decode()
    check(skill.count('<!-- r64-zip-occurrence-craft -->')==1 and KNOWLEDGE+':1-' in skill,'craft_binding')
    check(knowledge.startswith('source: S264') and '[OBSERVATION]' in knowledge and '[UNKNOWN]' in knowledge,'knowledge_binding')
    sources=blob(root,rev,'corpus/SOURCES.md').decode()
    check(any(x.startswith('| S264 |') and '| mined |' in x and KNOWLEDGE in x for x in sources.splitlines()),'source_binding')
    return dict(exit=1 if findings else 0,finding='not_met' if findings else 'met',findings=findings,
                predicate=c['predicate'],rev=rev,freeze=freeze,cases=len(c['case_names']),
                limit='Pins and committed receipt association are not provenance authentication; independent rerun required.')

def selftest():
    results=[]
    for mode in ('positive','wrong_semantic','old_run','wrong_fixture','missing_craft','touched_instrument','old_data','bool_semantic','alternate_freeze','changed_claim','bool_schema'):
        with tempfile.TemporaryDirectory(prefix='kaidoku64-admit-') as d:
            root=Path(d)
            def put(p,b):
                q=root/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(b if isinstance(b,bytes) else b.encode())
            def commit(year):
                git(root,'add','--','.')
                e=env(); e.update(GIT_AUTHOR_DATE=year+'-01-01T00:00:00Z',GIT_COMMITTER_DATE=year+'-01-01T00:00:00Z')
                subprocess.run(['git','-C',d,'-c','user.name=fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],env=e,check=True,capture_output=True)
                return git(root,'rev-parse','HEAD').decode().strip()
            git(root,'init','-q')
            reader='tools/round-64/zip-occurrences.py'
            put(SELF,Path(__file__).read_bytes()); put(reader,b'# inert selftest placeholder; never executed\n')
            if mode=='old_data': put(FIXTURES+'one.zip',b'old bytes')
            commit('2020')
            c=dict(predicate=PREDICATE,instruments={SELF:sha(Path(__file__).read_bytes()),reader:sha((root/reader).read_bytes())},case_names=['one'])
            put(CLAIMS,json.dumps(c)); put(PLAN,'frozen selftest plan\n'); freeze=commit('2021')
            data=b'owned inert fixture'
            want=dict(exit=0,finding='inventory_complete',archive_sha256=sha(data),archive_size=len(data),occurrences=[],duplicate_groups=[])
            put(FIXTURES+'one.zip',data if mode!='wrong_fixture' else b'changed')
            eb=json.dumps({'one':want}).encode(); put(FIXTURES+'expected.json',eb)
            got=dict(want,schema=1,reader_sha256=c['instruments'][reader])
            if mode=='wrong_semantic': got['occurrences']=[False]
            if mode=='bool_schema': got['schema']=True
            if mode=='bool_semantic': got['archive_size']=True; want['archive_size']=1; eb=json.dumps({'one':want}).encode(); put(FIXTURES+'expected.json',eb)
            row=dict(case='one',utc=('2019' if mode=='old_run' else '2022')+'-01-01T00:00:00Z',exit=0,stdout=json.dumps(got))
            put(RECEIPT,json.dumps(dict(results=[row],expected_sha256=sha(eb),reader_sha256=c['instruments'][reader],cases=1,matched=1,exit=0,finding='all_matched')))
            put('SKILL.md','' if mode=='missing_craft' else '<!-- r64-zip-occurrence-craft -->\n'+KNOWLEDGE+':1-20')
            put(KNOWLEDGE,'source: S264\n[OBSERVATION] fixture\n[UNKNOWN] runtime\n')
            put('corpus/SOURCES.md','| S264 | docs | mined | '+KNOWLEDGE+' |\n')
            if mode=='touched_instrument': put(reader,b'# changed inert placeholder\n')
            if mode=='changed_claim': put(CLAIMS,json.dumps(dict(c,changed=True)))
            rev=commit('2022')
            if mode=='alternate_freeze': freeze=rev
            cmd=[sys.executable,'-I','-B',str(Path(__file__).resolve()),'--root',d,'--rev',rev,'--freeze',freeze]
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=30,env=env()); r=obj(p.stdout)
            code=0 if mode=='positive' else 1
            expected={'positive':None,'wrong_semantic':'semantic:one:occurrences','old_run':'preinstrument_run:one','wrong_fixture':'fixture_pin:one','missing_craft':'craft_binding','touched_instrument':'instrument_touched:'+reader,'old_data':'preinstrument_data:'+FIXTURES+'one.zip','bool_semantic':'semantic:one:archive_size','alternate_freeze':'not_first_freeze','changed_claim':'frozen_record_changed:'+CLAIMS,'bool_schema':'body_exit:one'}[mode]
            results.append(dict(case=mode,exit=p.returncode,finding=r['finding'],findings=r['findings'],passed=p.returncode==code and (expected is None or expected in r['findings'])))
    return dict(exit=0 if all(x['passed'] for x in results) else 1,finding='selftest',results=results)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--root');p.add_argument('--rev');p.add_argument('--freeze');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    try: r=selftest() if a.selftest else audit(a.root,a.rev,a.freeze)
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError) as e: r=dict(exit=2,finding='unevaluable',detail=str(e))
    print(json.dumps(r,sort_keys=True));return r['exit']
if __name__=='__main__':sys.exit(main())
