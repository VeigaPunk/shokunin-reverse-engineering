import importlib.util, json
D='/fast/scratch/hyaku/kaidoku-r49/C2SearchLog/clone'; AF='77580bf4503066fa093564641026e761bb4b34bb'
spec=importlib.util.spec_from_file_location('c2m', D+'/tools/round-49/c2-mismatch.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r=m.Git(D); reg=r.show(AF,'corpus/SOURCES.md').decode()
s148=[l for l in reg.split('\n') if l.startswith('| S148 ')][0]
dup=reg.replace(s148, s148+'\n'+s148.replace('EX_USAGE is 64','EX_USAGE is 64 (duplicate)'))
g=m.score(m.Overlay(r,AF,{'corpus/SOURCES.md':dup.encode()}),AF)
print(json.dumps({'dup_S148_row_added':{'A8':g['A8'],'all_red':sorted(a for a,v in g.items() if v), 'census_grep_lines': sum(1 for l in dup.split('\n') if __import__('re').match(r'^\|\s*S\d{3,}\s*\|',l))}}, indent=1))
