#!/usr/bin/env python3
"""Independent exact JSON/exit comparison; runs only explicitly supplied reviewed reader."""
import argparse,hashlib,json,pathlib,subprocess,sys,resource,datetime,tempfile

def unique(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate key')
        d[k]=v
    return d

def parse(s):return json.loads(s,object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite')))
def exact(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(exact(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def cases_of(raw):
    if 'cases' not in raw:return raw
    if type(raw.get('schema')) is not int or raw['schema']!=1 or type(raw['cases']) is not list or not raw['cases']:raise ValueError('oracle_schema')
    cases={}
    for x in raw['cases']:
        if type(x) is not dict or type(x.get('name')) is not str:raise ValueError('oracle_case')
        name=x['name']
        if not name.replace('_','').replace('-','').isalnum() or x.get('file')!=name+'.bin' or name in cases:raise ValueError('oracle_case_identity')
        if type(x.get('exit')) is not int or x['exit'] not in (0,1) or type(x.get('expected')) is not dict:raise ValueError('oracle_case_shape')
        cases[name]={'file':x['file'],'pe_sha256':x['sha256'],'output':x['expected'],'exit':x['exit']}
    return cases

def limits():
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456));resource.setrlimit(resource.RLIMIT_CPU,(4,4));resource.setrlimit(resource.RLIMIT_FSIZE,(2097152,2097152));resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))

def selftest():
    checks={'typed_bool':not exact(True,1),'nested_bool':not exact({'a':[False]},{'a':[0]}),'extra_key':not exact({'a':1,'b':2},{'a':1}),'array_order':not exact([1,2],[2,1]),'complete_green':exact({'a':[1,'x']},{'a':[1,'x']}),'missing':not exact({}, {'a':1})}
    for key,text in [('duplicate','{"a":1,"a":1}'),('nan','NaN'),('empty','')]:
        try:parse(text);checks[key]=False
        except ValueError:checks[key]=True
    good={'schema':1,'cases':[{'name':'a','file':'a.bin','sha256':'0'*64,'exit':0,'expected':{'status':'absent'}}]}
    for label,change in [('schema_bool',lambda x:x.update(schema=True)),('duplicate_case',lambda x:x['cases'].append(dict(x['cases'][0]))),('unsafe_path',lambda x:x['cases'][0].update(file='../a.bin')),('empty_cases',lambda x:x.update(cases=[]))]:
        raw=json.loads(json.dumps(good));change(raw)
        try:cases_of(raw);checks[label]=False
        except ValueError:checks[label]=True
    with tempfile.TemporaryDirectory(prefix='kaidoku68-compare-selftest-') as td:
        root=pathlib.Path(td); (root/'one.pe').write_bytes(b'owned inert comparator fixture')
        want={'schema':1,'exit':0,'finding':'complete','occurrences':[]}
        oracle=root/'expected.json'; oracle.write_text(json.dumps({'one':{'exit':0,'output':want,'pe_sha256':hashlib.sha256((root/'one.pe').read_bytes()).hexdigest()}}))
        programs={'positive':"print("+repr(json.dumps(want))+")",'boolean':"print("+repr(json.dumps(dict(want,schema=True)))+")",'duplicate':"print("+repr('{"schema":1,"schema":1,"exit":0,"finding":"complete","occurrences":[]}')+")",'empty':"pass"}
        for name,code in programs.items():
            reader=root/(name+'.py');reader.write_text(code+'\n')
            cmd=[sys.executable,'-I','-B',str(pathlib.Path(__file__).resolve()),'--reader',str(reader),'--fixtures',td,'--reader-sha256',hashlib.sha256(reader.read_bytes()).hexdigest(),'--oracle-sha256',hashlib.sha256(oracle.read_bytes()).hexdigest()]
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=15); body=parse(r.stdout)
            checks['outer_'+name]=r.returncode==(0 if name=='positive' else 1) and body['matched']==(1 if name=='positive' else 0)
        (root/'one.pe').write_bytes(b'altered own snapshot')
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=15);body=parse(r.stdout)
        checks['outer_snapshot_tampered']=r.returncode==2 and body['finding']=='snapshot_tampered'
    print(json.dumps({'checks':checks,'ok':all(checks.values())}));return 0 if all(checks.values()) else 1

def main():
    p=argparse.ArgumentParser();p.add_argument('--reader');p.add_argument('--fixtures');p.add_argument('--reader-sha256');p.add_argument('--oracle-sha256');p.add_argument('--selftest',action='store_true');a=p.parse_args()
    if a.selftest:return selftest()
    if not all([a.reader,a.fixtures,a.reader_sha256,a.oracle_sha256]):p.error('pins and paths required')
    reader=pathlib.Path(a.reader).resolve();root=pathlib.Path(a.fixtures).resolve();oracle=root/'expected.json'
    if hashlib.sha256(reader.read_bytes()).hexdigest()!=a.reader_sha256 or hashlib.sha256(oracle.read_bytes()).hexdigest()!=a.oracle_sha256:
        print(json.dumps({'ok':False,'reason':'pin_mismatch'}));return 2
    raw=parse(oracle.read_text()); cases=cases_of(raw);rows=[]
    for name,e in cases.items():
        if not name.replace('_','').replace('-','').isalnum():raise ValueError('unsafe fixture name')
        filename=e.get('file',name+'.pe')
        if filename not in (name+'.pe',name+'.bin'):raise ValueError('unsafe fixture file')
        path=root/filename
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest()!=e.get('pe_sha256'):
            print(json.dumps(dict(exit=2,finding='snapshot_tampered',case=name)));return 2
    for name,e in sorted(cases.items()):
        if not name.replace('_','').replace('-','').isalnum():raise ValueError('unsafe fixture name')
        filename=e.get('file',name+'.pe')
        if filename not in (name+'.pe',name+'.bin'):raise ValueError('unsafe fixture file')
        path=root/filename;cmd=[sys.executable,'-I','-B',str(reader),'--pe',str(path)]
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=8,preexec_fn=limits)
            try:out=parse(r.stdout);match=exact(out,e['output']) and type(r.returncode) is int and r.returncode==e['exit'];error=None
            except ValueError as ex:out=None;match=False;error=str(ex)
            rows.append(dict(case=name,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=cmd,ok=match,exit=r.returncode,output=out,stdout=r.stdout,stderr=r.stderr,parse_error=error,fixture_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        except subprocess.TimeoutExpired:rows.append(dict(case=name,ok=False,error='timeout'))
    ok=bool(rows) and all(r['ok'] for r in rows)
    print(json.dumps(dict(ok=ok,passed=sum(r['ok'] for r in rows),total=len(rows),cases=len(rows),matched=sum(r['ok'] for r in rows),exit=0 if ok else 1,finding='all_matched' if ok else 'mismatch',expected_sha256=a.oracle_sha256,reader_sha256=a.reader_sha256,oracle_sha256=a.oracle_sha256,results=rows),indent=2));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
