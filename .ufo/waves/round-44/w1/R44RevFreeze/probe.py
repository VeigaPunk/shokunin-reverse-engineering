import json,hashlib,glob,subprocess,re
out={}
pins={'529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6':'v1-be','b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71':'v1-le','7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124':'v2-le','79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0':'v2-be'}
for r in ('round-42/c2/dev','round-42/c2/heldout','round-43/c1/heldout'):
    hits={}
    for p in glob.glob('corpus/evidence/%s/*/carrier.sqsh'%r):
        h=hashlib.sha256(open(p,'rb').read()).hexdigest()
        if h in pins: hits.setdefault(pins[h],[]).append(p.split('/')[-2])
    out['prior_rea_receipts_of_same_bytes:'+r]=hits
prior=json.load(open('tools/round-42/prior-pins.json'))
out['prior_pins_rounds']=sorted({e['round'] for e in prior['pins']})
out['prior_pins_has_c1_pins_for_v1v2']=[p for p in pins if any(e['sha256']==p for e in prior['pins'])]
def tracked(p): return subprocess.run(['git','ls-files','--error-unmatch',p],capture_output=True).returncode==0
out['tracked']={p:tracked(p) for p in ['tools/round-27/xpin-attribute.mjs','tools/round-42/c1-extra.py','tools/round-42/unblob-logtee.sh','tools/round-42/sqfs3-oracle.py','tools/round-42/rea-pkg.json','tools/round-42/prior-pins.json','.ufo/waves/round-43/l1/scores/c1-at-77d196c6.json','.ufo/waves/round-42/l1/scores/c1-at-eb8215ac.json']}
base='c29360e3ba5381a5ab69e372d0d9577970f85018'
for f in ['SKILL.md','SCORECARD.md','SHONEN.md','corpus/README.md','corpus/SOURCES.md','PROVINCE.md','LOG.md']:
    n=subprocess.run(['git','log','--oneline','-12','--format=%s','--',f],capture_output=True,text=True).stdout.splitlines()
    out['recent_commit_subjects:'+f]=[s[:70] for s in n[:3]]
out['shonen_pointers_into_files_C1_edits']=sorted(set(re.findall(r'(PROVINCE\.md|corpus/README\.md|corpus/SOURCES\.md):\d+',open('SHONEN.md').read()+open('SCORECARD.md').read())))
out['scorecard_line_pointers_into_README_SOURCES_PROVINCE']=len(re.findall(r'(?:corpus/README|corpus/SOURCES|PROVINCE)\.md:\d+',open('SCORECARD.md').read()))
out['knowledge_files']=len(subprocess.run(['git','ls-tree','-r','--name-only',base,'--','corpus/knowledge'],capture_output=True,text=True).stdout.splitlines())
print(json.dumps(out,indent=1,sort_keys=True))
