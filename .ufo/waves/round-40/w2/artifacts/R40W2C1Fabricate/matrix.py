import copy, importlib.util, json
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('c1', L+'/tools/round-40/c1-counter.py')
c1=importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
base=json.load(open('fab/L1.env.json'))
real=sum(1 for _ in [0])
oracle,_=c1.parse_oracle(open(L+'/corpus/evidence/round-40/c1/L1/oracle.tsv','rb').read())
nonreg,_=c1.parse_nonregular(open(L+'/corpus/evidence/round-40/c1/L1/nonregular.tsv','rb').read())
rule=json.load(open(L+'/.ufo/waves/round-40/c1/gap-rule.json'))
model,_=c1.gap_rule_model(json.dumps(rule).encode())
fresh=c1.projection(json.load(open('probe-real-L1.json')),'plus-extractor') if False else None
committed=json.loads(__import__('subprocess').run(['git','-C',L,'show','42c10a58cb2cae3a4a0122af35a0cf95ac718043:corpus/evidence/round-40/c1/L1/after.json'],capture_output=True).stdout)
# the fresh rerun projection was measured equal to the committed one by the counter run;
# use the committed receipt's projection as the reference for clause attribution.
ref=c1.projection(committed,'plus-extractor')

def mutate(fn):
    e=copy.deepcopy(base); fn(e); return e

def gapfail(e):
    ok,why=c1.gap_check(c1.gaps(e),nonreg,model)
    files=c1.published(e)
    return ok, c1.oracle_hits(oracle,files)==len(oracle), not c1.nonregular_published(files,nonreg)

cases={
 'baseline (fabricated, unchanged)': lambda e: None,
 'gaps omitted entirely (tables only: files, no symlink gaps)': lambda e: (e['normalized_result'].__setitem__('extraction_gaps',[]), e['normalized_result'].__setitem__('unpublished_entries',[])),
 'extra gap on a directory (bin)': lambda e: e['normalized_result']['extraction_gaps'].append({'kind':'unpublished-entry','relative_path':'firmware.bin_extract/bin','dependencies':[]}),
 'unpublished_entries dropped, gaps kept': lambda e: e['normalized_result'].__setitem__('unpublished_entries',[]),
 'chunk length block-aligned (231424)': lambda e: (e['normalized_result']['chunks'][0]['range'].__setitem__('length',231424), e['normalized_result']['chunks'][0]['root_file_range'].__setitem__('length',231424)),
 'coverage = complete': lambda e: e['normalized_result'].__setitem__('coverage','complete'),
 'engine version 6.4.9': lambda e: e['normalized_result']['engine'].__setitem__('version','6.4.9'),
 'derivation child names the staged input (carrier.bin_extract)': lambda e: e['normalized_result']['derivations'][0].__setitem__('child_path','$output/carrier.bin_extract'),
 'published_bytes = carrier size (compressed)': lambda e: e['normalized_result'].__setitem__('published_bytes',230884),
 'per-file HashReport (sasquatch-derived md5/sha1)': lambda e: e['raw_result']['report'].append({'task':{'path':'/x/extracted/firmware.bin_extract/etc/version','depth':1},'reports':[{'__typename__':'HashReport','md5':'baa04b836054a621edb2621dad17c0c8','sha1':'48497a28ea0b8bae331dbbf04f56962d52bb3684','sha256':oracle[1][1]}]}),
 'truthful mime_type on each file': lambda e: [f.__setitem__('mime_type','text/plain') for f in e['normalized_result']['files']],
 'one diagnostic attached': lambda e: e['normalized_result'].__setitem__('diagnostics',[{'report':{'__typename__':'MaliciousSymlinkRemoved'}}]),
 'handler squashfs_v4_le': lambda e: e['normalized_result']['chunks'][0].__setitem__('handler','squashfs_v4_le'),
 'one file size off by one': lambda e: e['normalized_result']['files'][0].__setitem__('size',e['normalized_result']['files'][0]['size']+1),
 'raw_result.execution + limitations + authority replaced with fiction': lambda e: (e['raw_result'].__setitem__('execution',{'command':'/usr/bin/true','args':['--lie'],'exit_code':0}), e.__setitem__('limitations',['nothing was executed']), e.__setitem__('authority','derived-from-oracle')),
}
print('%-72s %-9s %-9s %-9s %s'%('mutant','proj_ok','gaps_ok','oracle_ok','differing projection keys / gap reason'))
for name,fn in cases.items():
    e=mutate(fn)
    eq,keys,detail=c1.projection_diff(ref,c1.projection(e,'plus-extractor'),'plus-extractor')
    gok,why=c1.gap_check(c1.gaps(e),nonreg,model)
    oh=c1.oracle_hits(oracle,c1.published(e))==len(oracle)
    print('%-72s %-9s %-9s %-9s %s'%(name[:72],eq,gok,oh,keys if keys else ('-' if gok else why)))
