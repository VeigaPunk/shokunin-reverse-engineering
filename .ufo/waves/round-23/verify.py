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
    os.environ.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
                      GIT_CONFIG_COUNT='2', GIT_CONFIG_KEY_0='core.hooksPath',
                      GIT_CONFIG_VALUE_0='/dev/null', GIT_CONFIG_KEY_1='core.attributesFile',
                      GIT_CONFIG_VALUE_1='/dev/null')
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
    def record(name, argv, expected_exit, predicate=lambda out: True, env_overrides=None):
        child_env = dict(os.environ, TMPDIR=str(runtime))
        child_env.update(env_overrides or {})
        r = subprocess.run(argv, env=child_env, capture_output=True, text=True, check=False)
        try:
            output = json.loads(r.stdout)
        except ValueError:
            output = {'text': r.stdout}
        passed = r.returncode == expected_exit and predicate(output)
        data = {'argv': argv, 'expected_exit': expected_exit, 'exit': r.returncode,
                'env_overrides': {'TMPDIR':str(runtime), **(env_overrides or {})},
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
        record('nonroot-refusal',[sys.executable,'-I','-B',str(counter),'--root',str(clone/'corpus'),'--rev',rev],2,lambda o:o.get('error')=='root_not_repository_top')
        record('after-c1',argv+['--rev',rev],1,lambda o:o.get('t1_exercised_count')==4 and o.get('t1_total')==6 and o.get('t1_exercised')==['identify-flutter-build','inspect-dart-aot','inspect-signal-decoders','decode-signal-recording'])
        record('selftest',argv+['--selftest'],0,lambda o:o.get('passed')==25 and o.get('total')==25)
        controlled_bin = clone/'.ufo/waves/round-23/runtime/controlled-git'
        controlled_bin.mkdir(parents=True, exist_ok=True)
        git_shim = controlled_bin/'git'
        git_shim.write_text('#!/bin/sh\nprintf \"controlled_git_failure\\\\n\" >&2\nexit 7\n')
        git_shim.chmod(0o755)
        record('selftest-setup-failure',argv+['--selftest'],2,
               lambda o:'controlled_git_failure' in o.get('error',''),
               {'PATH':str(controlled_bin)+os.pathsep+os.environ.get('PATH','')})
        fixture = w/'frozen/fixture.json'
        original = fixture.read_bytes()
        fixture.write_bytes(original+b'\n')
        record('frozen-input-red',argv+['--selftest'],2,lambda o:'snapshot_tampered' in o.get('error',''))
        fixture.write_bytes(original)
        record('r22-c1',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-22/tools/count-c1.py'),'--root',str(clone),'--rev',rev],1,lambda o:o.get('t1_exercised_count')==1)
        record('r22-c2',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-22/tools/count-c2.py'),'--root',str(clone),'--rev',rev],0,lambda o:o.get('accounted_count')==14)
        record('no-harm',[sys.executable,'-I','-B',str(clone/'.ufo/waves/round-21/controls.py'),'--root',str(clone),'--before',B,'--after',rev],0,lambda o:o.get('finding')=='controls_clean')
        def signal_ok(output):
            rows = output.get('records', [])
            if len(rows) != 5:
                return False
            for row in rows:
                if not row.get('stdout_byte_equal') or row.get('original_stderr') != '':
                    return False
                if row.get('ok') is True and (row.get('exit') != 0 or not row.get('argv_command_matches_meta')):
                    return False
                if row.get('name') in ('decode-uart-hi', 'decode-official-uart') and not (
                        row.get('subject_digest_matches_carrier') and row.get('argv_target_matches_subject')):
                    return False
            by_name = {row['name']: row for row in rows}
            if set(by_name) != {'inventory','uart-help','decode-uart-hi','decode-official-uart','decode-invalid-decoder'}:
                return False
            return (by_name['decode-uart-hi'].get('synthetic_exact') is True and
                    by_name['inventory'].get('decoder_count') == 110 and
                    by_name['decode-official-uart'].get('annotation_line_count') == 12885 and
                    by_name['decode-official-uart'].get('contains_literal_Hello_World') is False and
                    by_name['decode-invalid-decoder'].get('exit') == 1 and
                    by_name['decode-invalid-decoder'].get('error', {}).get('code') == 'execution_failure')
        signal = record('signal-records',[sys.executable,'-I','-B',str(w/'tools/describe-signals.py'),'--root',str(clone),'--rev',rev],0,signal_ok)
        record('dart-record',[sys.executable,'-I','-B',str(w/'tools/describe-dart.py'),'--root',str(clone),'--rev',rev],0,lambda o:o.get('stdout_byte_equal') and o.get('subject_digest_matches_fetch') and o.get('argv_target_matches_subject') and o.get('command_matches') and o.get('original_stderr')=='' and o.get('overall_coverage')=='partial' and o.get('libapp',{}).get('coverage')=='complete' and len(o.get('libapp',{}).get('sections',[]))==4 and o.get('string_pool_coverage')=='partial')
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
        fixture_runner = namespace['load'](w/'tools/counter-fixtures.py', 'independent_v3_red')
        manifest = json.loads((w/'frozen/expected-v3.json').read_text())
        red, red_code = fixture_runner.run(clone, w/'frozen/pre-v3-counter.py', manifest)
        failed_cases = [case['case'] for case in red['cases'] if not case['passed']]
        regression_ok = red_code == 1 and set(failed_cases) == set(manifest['red_regression']['named_false_accepts'])
        (a.out/'pre-v3-red.json').write_text(json.dumps({'source_rev':rev,'exit':red_code,'result':red,'named_false_accepts':failed_cases,'passed':regression_ok},indent=2)+'\n')
        checks.append({'name':'pre-v3-red','passed':regression_ok})
        # Immutable old-row and append-only province/skill controls, not freshness claims.
        def blob(ref,path): return git('show',ref+':'+path)
        old_rows=[x for x in blob(B,'corpus/SOURCES.md').splitlines() if x.startswith(b'| S')]
        new_rows=[x for x in blob(rev,'corpus/SOURCES.md').splitlines() if x.startswith(b'| S')]
        details={'old_rows':len(old_rows),'new_rows':len(new_rows),'old_rows_unchanged':new_rows[:len(old_rows)]==old_rows,
                 'skill_prefix':blob(rev,'SKILL.md').startswith(blob(B,'SKILL.md')),
                 'province_prefix':blob(rev,'PROVINCE.md').startswith(blob(B,'PROVINCE.md')),
                 'tiers_before':{},'tiers_after':{},'statuses_before':{},'statuses_after':{}}
        details['prior_wave_trees_identical'] = {
            name: git('rev-parse',rev+':.ufo/waves/'+name) == git('rev-parse',B+':.ufo/waves/'+name)
            for name in ('round-20','round-21','round-22')}
        readme_after = iter(line for line in blob(rev,'corpus/README.md').splitlines() if line.strip())
        details['readme_prior_nonempty_lines_preserved'] = all(
            any(old_line == new_line for new_line in readme_after)
            for old_line in blob(B,'corpus/README.md').splitlines() if old_line.strip())
        for rows,suffix in ((old_rows,'before'),(new_rows,'after')):
            for row in rows:
                cells=[c.strip().decode() for c in row.split(b'|')]
                details['tiers_'+suffix][cells[4]]=details['tiers_'+suffix].get(cells[4],0)+1
                details['statuses_'+suffix][cells[8]]=details['statuses_'+suffix].get(cells[8],0)+1
        ok=details['old_rows_unchanged'] and details['skill_prefix'] and details['province_prefix'] and len(old_rows)==57 and len(new_rows)==63 and all(details['prior_wave_trees_identical'].values()) and details['readme_prior_nonempty_lines_preserved']
        details['passed']=ok
        (a.out/'source-prefixes.json').write_text(json.dumps(details,indent=2)+'\n');checks.append({'name':'source-prefixes','passed':ok})
        census_script = Path('/home/vgpnk/Projects/shokunin/scripts/sources-census.sh')
        (a.out/'census-tool.json').write_text(json.dumps({'path':str(census_script),'sha256':hashlib.sha256(census_script.read_bytes()).hexdigest(),'input_scope':'private committed clone; explicit date2026-10-21'},indent=2)+'\n')
        record('snapshot-source-census',[str(census_script),'validate','--root','/home/vgpnk/Projects/shokunin','--today','2026-10-21','--file',str(clone/'corpus/SOURCES.md')],0,lambda o:str(clone/'corpus/SOURCES.md') in o.get('text',''))
        pins={str(path.relative_to(clone)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [counter,w/'tools/counter-fixtures.py',w/'frozen/expected-v3.json',w/'frozen/fixture.json',w/'frozen/pre-v3-counter.py',w/'tools/describe-signals.py',w/'tools/describe-dart.py']}
        (a.out/'source-pins.json').write_text(json.dumps({'source_rev':rev,'pins':pins},indent=2)+'\n')
    summary={'source_rev':rev,'before':B,'checks':checks,'passed':sum(x['passed'] for x in checks),'total':len(checks),'failed':[x['name'] for x in checks if not x['passed']]}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True))
    return 0 if not summary['failed'] else 1

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'finding':'unevaluable','error':str(error)}))
        raise SystemExit(2)
