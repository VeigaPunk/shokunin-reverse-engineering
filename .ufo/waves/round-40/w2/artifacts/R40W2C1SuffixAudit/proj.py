import importlib.util, json, copy
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=importlib.util.spec_from_file_location('cc',LANE+'/tools/round-40/c1-counter.py')
cc=importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
env=json.load(open(LANE+'/corpus/evidence/round-40/c1/L2/after.json'))
base=cc.projection(env,'plus-extractor')

# (a) strip the chunk root entirely from every path — not a shape REA emits
e=copy.deepcopy(env); nr=e['normalized_result']
for k in ('files','extraction_gaps','unpublished_entries'):
    for x in nr[k]:
        p=x.get('relative_path')
        if isinstance(p,str) and p.startswith('firmware.bin_extract/'):
            x['relative_path']=p[len('firmware.bin_extract/'):]
        elif isinstance(p,str) and p=='firmware.bin_extract':
            x['relative_path']=''
print('(a) rootless receipt projects equal:', cc.projection_diff(base, cc.projection(e,'plus-extractor'),'plus-extractor'))

# (b) an entry AT the chunk root: staged name differs between receipt and rerun
e2=copy.deepcopy(env); nr2=e2['normalized_result']
nr2['files'].append({'relative_path':'firmware.bin_extract','sha256':'ab'*32,'size':0,'mime_type':'inode/x'})
e3=copy.deepcopy(e2); nr3=e3['normalized_result']
for k in ('files','extraction_gaps','unpublished_entries'):
    for x in nr3[k]:
        p=x.get('relative_path')
        if isinstance(p,str) and p.startswith('firmware.bin_extract'):
            x['relative_path']=p.replace('firmware.bin_extract','carrier.bin_extract',1)
print('(b) same bytes, different staged name, root entry:', cc.projection_diff(cc.projection(e2,'plus-extractor'), cc.projection(e3,'plus-extractor'),'plus-extractor'))

# (c) two chunk roots in one receipt collapse to the same suffix
e4=copy.deepcopy(env); nr4=e4['normalized_result']
nr4['files']=[{'relative_path':'a_extract/usr/bin/busy','sha256':'cd'*32,'size':40000,'mime_type':'m'},
              {'relative_path':'b_extract/usr/bin/busy','sha256':'ef'*32,'size':40000,'mime_type':'m'}]
print('(c) file suffixes:', [r[0] for r in cc.projection(e4,'core')['files']])

# (d) traversal survives the projection
print('(d) rel_suffix traversal:', cc.rel_suffix('$output/a_extract/../../etc/passwd'))
