#!/usr/bin/env python3
"""Recount retained index/citation proxies and immutable-history controls."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


def selftest():
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-controls-') as directory:
        root=Path(directory)
        def git(*args):
            return subprocess.check_output(['git','-C',directory,*args],stderr=subprocess.PIPE).decode().strip()
        git('init','-q')
        files={'corpus/knowledge/2026-10-21-fixture.md':'original\n',
               'corpus/README.md':'## Coverage map\n2026-10-21-fixture\n## Other\n',
               'SKILL.md':'## Queue-drain craft fixture\n- **Rule** corpus/knowledge/2026-10-21-fixture.md:1\n## Next\n',
               'corpus/QUALITY.md':'| 1 | original | fixture | — |\n',
               'LOG.md':'original log\n','SCORECARD.md':'original score\n'}
        for path,text in files.items():
            target=root/path
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(text,encoding='utf-8')
        def commit():
            git('add','.')
            git('-c','user.name=kaidoku-controls-fixture','-c','user.email=fixture@invalid','commit','-q','--allow-empty','-m','fixture')
            return git('rev-parse','HEAD')
        before=commit()
        for name,text,wanted,finding in [('unchanged','original\n',0,'controls_clean'),('prior_changed','mutated\n',1,'controls_failed')]:
            (root/'corpus/knowledge/2026-10-21-fixture.md').write_text(text,encoding='utf-8')
            after=commit()
            proc=subprocess.run([sys.executable,'-I','-B',__file__,'--root',directory,'--before',before,'--after',after],capture_output=True,text=True,check=False)
            actual=json.loads(proc.stdout).get('finding')
            results.append({'id':name,'exit':proc.returncode,'finding':actual,'ok':proc.returncode==wanted and actual==finding})
    ok=all(x['ok'] for x in results)
    print(json.dumps({'finding':'selftest_clean' if ok else 'selftest_failed','cases':results},sort_keys=True))
    return 0 if ok else 1


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root')
    p.add_argument('--before')
    p.add_argument('--after')
    p.add_argument('--selftest',action='store_true')
    a=p.parse_args()
    if a.selftest:
        return selftest()
    if not all((a.root,a.before,a.after)):
        p.error('--root --before --after required')
    def git(*args):
        return subprocess.check_output(['git','--no-optional-locks','-C',a.root,*args])
    def blob(rev,path):
        return git('show',rev+':'+path)
    def mapping(rev):
        paths=git('ls-tree','-r','--name-only',rev,'--','corpus/knowledge').decode().splitlines()
        files={PurePosixPath(x).stem for x in paths if x.endswith('.md')}
        section=blob(rev,'corpus/README.md').decode().split('## Coverage map\n',1)[1].split('\n## ',1)[0]
        mapped=set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+',section))
        craft=blob(rev,'SKILL.md').decode().split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
        rules=re.split(r'(?m)^- \*\*',craft)[1:]
        resolved=0
        for rule in rules:
            refs=re.findall(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?',rule)
            valid=bool(refs)
            for name,first,last in refs:
                count=len(blob(rev,'corpus/knowledge/'+name).splitlines())
                start,end=int(first or 1),int(last or first or 1)
                valid=valid and 1<=start<=end<=count
            resolved+=valid
        return {'mapped':len(files & mapped),'knowledge_files':len(files),'missing':sorted(files-mapped),'dangling':sorted(mapped-files),'rules':len(rules),'resolved':resolved,'coverage_score':round(10*len(files & mapped)/len(files),2),'depth_score':round(10*resolved/len(rules),2)}
    try:
        before=git('rev-parse',a.before+'^{commit}').decode().strip()
        after=git('rev-parse',a.after+'^{commit}').decode().strip()
        paths=git('ls-tree','-r','--name-only',before).decode().splitlines()
        prior=[x for x in paths if x.startswith('.ufo/waves/round-20/') or x.startswith('corpus/knowledge/') or x.startswith('corpus/lessons/')]
        changed=[x for x in prior if blob(before,x)!=blob(after,x)]
        prefix={x:blob(after,x).startswith(blob(before,x)) for x in ['LOG.md','SCORECARD.md']}
        old_rows=[x for x in blob(before,'corpus/QUALITY.md').split(b'## Signals of weak material',1)[0].splitlines() if re.match(rb'^\| [0-9]+ \|',x)]
        new_rows=[x for x in blob(after,'corpus/QUALITY.md').split(b'## Signals of weak material',1)[0].splitlines() if re.match(rb'^\| [0-9]+ \|',x)]
        b,m=mapping(before),mapping(after)
        ok=not changed and all(prefix.values()) and new_rows[:len(old_rows)]==old_rows and m['coverage_score']>=b['coverage_score'] and m['depth_score']>=b['depth_score']
        result={'finding':'controls_clean' if ok else 'controls_failed','before':before,'after':after,'mapping_before':b,'mapping_after':m,'prior_files_checked':len(prior),'prior_files_changed':changed,'append_only_prefixes':prefix,'quality_prior_rows_identical':new_rows[:len(old_rows)]==old_rows,'quality_rows_before':len(old_rows),'quality_rows_after':len(new_rows),'limit':'structural proxies and byte preservation only, not a semantic/province/security audit'}
        print(json.dumps(result,sort_keys=True))
        return 0 if ok else 1
    except (OSError,ValueError,subprocess.SubprocessError) as error:
        print(json.dumps({'finding':'controls_unevaluable','error':str(error)}))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
