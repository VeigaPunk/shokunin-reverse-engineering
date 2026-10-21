#!/usr/bin/env python3
"""Run one committed R23 source snapshot; retain actual child records.

Probe:0 all declared finite conditions observed,1 discrepancy,2 invocation/input
failure. No target replay. Git writes only in a removed private clone under the
lane runtime. It is not independent admission, authentication or an OS sandbox.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

B = 'aa1450b82f9ede35aada63efe8a34e01c6e02f72'

def main():
    for key in tuple(os.environ):
        if key.startswith('GIT_'):
            del os.environ[key]
    os.environ['GIT_NO_REPLACE_OBJECTS'] = '1'
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, required=True)
    p.add_argument('--rev', required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    root = a.root.resolve()
    def git(*args):
        r = subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=False)
        if r.returncode:
            raise ValueError('git_input_unreadable')
        return r.stdout
    rev = git('rev-parse', '--verify', '--end-of-options', a.rev+'^{commit}').decode().strip()
    a.out.mkdir(parents=True, exist_ok=False)
    checks = []
    def record(name, argv, expected_exit, predicate=lambda out: True):
        r = subprocess.run(argv, capture_output=True, text=True, check=False)
        try:
            output = json.loads(r.stdout)
        except ValueError:
            output = {}
        passed = r.returncode == expected_exit and predicate(output)
        data = {'argv': argv, 'expected_exit': expected_exit, 'exit': r.returncode,
                'stdout': r.stdout, 'stderr': r.stderr, 'source_rev': rev, 'passed': passed}
        (a.out/(name+'.json')).write_text(json.dumps(data, indent=2)+'\n')
        checks.append({'name': name, 'passed': passed})
        return output
    runtime = root/'.ufo/waves/round-23/runtime'
    runtime.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='verify-', dir=runtime) as directory:
        clone = Path(directory)/'snapshot'
        subprocess.run(['git','clone','--shared','--no-checkout',str(root),str(clone)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(clone),'checkout',rev],check=True,capture_output=True)
        w = clone/'.ufo/waves/round-23'
        counter = w/'tools/count-c1.py'
        argv = [sys.executable,'-I','-B',str(counter),'--root',str(clone)]
        record('before-c1',argv+['--rev',B],1,lambda o:o.get('t1_exercised_count')==1 and o.get('t1_total')==6)
        record('after-c1',argv+['--rev',rev],1,lambda o:o.get('t1_exercised_count')==4 and o.get('t1_total')==6 and o.get('t1_exercised')==['identify-flutter-build','inspect-dart-aot','inspect-signal-decoders','decode-signal-recording'])
        record('selftest',argv+['--selftest'],0,lambda o:o.get('passed')==21 and o.get('total')==21)
        fixture = w/'frozen/fixture.json'
        original = fixture.read_bytes()
        fixture.write_bytes(original+b'\n')
        record('frozen-input-red',argv+['--selftest'],2,lambda o:'snapshot_tampered' in o.get('error',''))
        fixture.write_bytes(original)
        record('r22-c1',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-22/tools/count-c1.py'),'--root',str(clone),'--rev',rev],1,lambda o:o.get('t1_exercised_count')==1)
        record('r22-c2',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-22/tools/count-c2.py'),'--root',str(clone),'--rev',rev],0,lambda o:o.get('accounted_count')==14)
        record('no-harm',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-21/controls.py'),'--root',str(clone),'--before',B,'--after',rev],0,lambda o:o.get('finding')=='controls_clean')
        signal = record('signal-records',[sys.executable,'-I','-B',str(w/'tools/describe-signals.py'),'--root',str(clone),'--rev',rev],0,lambda o:len(o.get('records',[]))==5 and all(x.get('stdout_byte_equal') for x in o.get('records',[])))
        record('dart-record',[sys.executable,'-I','-B',str(w/'tools/describe-dart.py'),'--root',str(clone),'--rev',rev],0,lambda o:o.get('stdout_byte_equal') and o.get('subject_digest_matches_fetch') and o.get('argv_target_matches_subject') and o.get('libapp',{}).get('coverage')=='complete' and len(o.get('libapp',{}).get('sections',[]))==4 and o.get('string_pool_coverage')=='partial')
        # Same synthetic envelope, same exact input, legacy versus strengthened binder.
        namespace = {'__file__':str(counter),'__name__':'r23_reviewed'}
        exec(compile(counter.read_bytes(),str(counter),'exec'),namespace)
        r22 = namespace['load'](clone/'.ufo/waves/round-22/tools/count-c1.py','r22_reviewed')
        tempfile.tempdir = str(runtime)
        r21,_ = r22.revision_helpers(clone,rev)
        templates=json.loads((w/'frozen/fixture.json').read_text())['documents']
        comparisons=[]
        for name in ('positive','meta_false','meta_array'):
            envelope=json.loads(json.dumps(templates['inspect-signal-decoders']))
            if name=='meta_false': envelope['meta']['ok']=False
            if name=='meta_array': envelope['meta']['raw_result']=[{'ok':False}]
            text=json.dumps(envelope); eid=envelope['data']['evidence_id']
            old=r22.bind_cli(r21,text,'inspect-signal-decoders',eid)
            new=namespace['bind_new'](r22,r21,text,'inspect-signal-decoders',eid)
            comparisons.append({'case':name,'envelope':envelope,'legacy':old,'current':new})
        binding_ok=[(x['legacy'],x['current']) for x in comparisons]==[(0,0),(0,1),(0,1)]
        (a.out/'metadata-red-green.json').write_text(json.dumps({'source_rev':rev,'legacy_sha256':namespace['LEGACY_SHA256'],'counter_sha256':hashlib.sha256(counter.read_bytes()).hexdigest(),'comparisons':comparisons,'passed':binding_ok},indent=2)+'\n')
        checks.append({'name':'metadata-red-green','passed':binding_ok})
        # Immutable old-row and append-only province/skill controls, not freshness claims.
        def blob(ref,path): return git('show',ref+':'+path)
        old_rows=[x for x in blob(B,'corpus/SOURCES.md').splitlines() if x.startswith(b'| S')]
        new_rows=[x for x in blob(rev,'corpus/SOURCES.md').splitlines() if x.startswith(b'| S')]
        details={'old_rows':len(old_rows),'new_rows':len(new_rows),'old_rows_unchanged':new_rows[:len(old_rows)]==old_rows,
                 'skill_prefix':blob(rev,'SKILL.md').startswith(blob(B,'SKILL.md')),
                 'province_prefix':blob(rev,'PROVINCE.md').startswith(blob(B,'PROVINCE.md')),
                 'tiers_before':{},'tiers_after':{},'statuses_before':{},'statuses_after':{}}
        for rows,suffix in ((old_rows,'before'),(new_rows,'after')):
            for row in rows:
                cells=[c.strip().decode() for c in row.split(b'|')]
                details['tiers_'+suffix][cells[4]]=details['tiers_'+suffix].get(cells[4],0)+1
                details['statuses_'+suffix][cells[8]]=details['statuses_'+suffix].get(cells[8],0)+1
        ok=details['old_rows_unchanged'] and details['skill_prefix'] and details['province_prefix'] and len(old_rows)==57 and len(new_rows)==61
        details['passed']=ok
        (a.out/'source-prefixes.json').write_text(json.dumps(details,indent=2)+'\n');checks.append({'name':'source-prefixes','passed':ok})
        pins={str(path.relative_to(clone)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [counter,w/'tools/counter-fixtures.py',w/'frozen/expected-v2.json',w/'frozen/fixture.json',w/'tools/describe-signals.py',w/'tools/describe-dart.py']}
        (a.out/'source-pins.json').write_text(json.dumps({'source_rev':rev,'pins':pins},indent=2)+'\n')
    census=record('source-census',['/home/vgpnk/Projects/shokunin/scripts/sources-census.sh','validate','--root','/home/vgpnk/Projects/shokunin','kaidoku'],0)
    # Census prints text, not JSON; exit is its outer conformance verdict only.
    summary={'source_rev':rev,'before':B,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'failed':[x['name'] for x in checks if not x['passed']]}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    return 0 if not summary['failed'] else 1

if __name__=='__main__':
    raise SystemExit(main())
