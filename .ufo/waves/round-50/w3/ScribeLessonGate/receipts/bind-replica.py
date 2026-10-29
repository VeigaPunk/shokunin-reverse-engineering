import importlib.util, sys, json, re, subprocess
spec = importlib.util.spec_from_file_location('c1', 'tools/round-50/c1-counter.py')
c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
rev = subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
def show(root, rev, path):
    r = subprocess.run(['git','-C',root,'show',rev+':'+path],capture_output=True)
    return r.stdout if r.returncode==0 else None
b={}
prov=show('.',rev,'PROVINCE.md'); prov_text=prov.decode(errors='replace') if prov else ''
sec=c1.section(prov_text,c1.CORE_HEADING) if prov else None
b['province_core_section']= sec is not None
rows=[l for l in (sec or []) if l.lstrip().startswith('|')]
b['province_core_row']=any(c1.HANDLER_RE.search(c1.cells(r)[0]) and c1.AVM_MARKER_RE.search(r.replace(c1.ENTRY,'')) and c1.ENTRY in r for r in rows)
b['frontier_note']=any(c1.FRONTIER_MARK in l and c1.STEM in l and c1.LE_AVM_RE.search(l.replace(c1.STEM,'')) for l in prov_text.splitlines())
ent=show('.',rev,c1.ENTRY); b['entry_present']= ent is not None
src_ids=set()
if ent:
    for line in ent.decode(errors='replace').splitlines():
        if line.startswith('source:'): src_ids|=c1.sid_tokens(line)
reg=show('.',rev,'corpus/SOURCES.md'); ok=[]
if reg:
    for line in reg.decode(errors='replace').splitlines():
        if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|',line): continue
        cc=c1.cells(line)
        if len(cc)!=11: continue
        used=cc[10]
        if cc[0] in src_ids and cc[8] in c1.OPENED_DATES and (c1.ENTRY in used or c1.STEM in used): ok.append(cc[0])
b['opened_source_rows']=sorted(ok); b['sourced']=bool(ok)
readme=show('.',rev,'corpus/README.md')
cm=c1.section(readme.decode(errors='replace'),'## Coverage map') if readme else None
b['coverage_map_row']=bool(cm) and any(c1.STEM in l for l in cm if l.lstrip().startswith('|'))
print(json.dumps(b,indent=1,sort_keys=True))
