import importlib.util, json
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
S="/fast/scratch/hyaku/kaidoku-r68/ConnectorCross"
for label,path in [("pristine",S+"/rc-pristine.py"),("mut-okguard",S+"/rc-mut-okguard.py")]:
    m=load(label,path)
    def skill(rows): return "\n".join([m.MARK_OPEN,"| tool | g | v | s | p | w | o |","|---|---|---|---|---|---|---|",*rows,m.MARK_CLOSE,""])
    row=lambda p,v="0=met; 1=not met; 2=could-not-evaluate": f"| `{p}` | g | {v} | s | p | w | o |"
    r=m.census({}, skill([row("tools/round-67/a.py"),row("tools/round-50/a.py")]),
               {"tools/round-67/a.py","tools/round-50/a.py"})
    print(label, json.dumps({k:r[k] for k in ("ok","mismatches","scope_size","registry_rows")},sort_keys=True))
