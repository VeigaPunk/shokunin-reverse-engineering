python3 -c '
import re, subprocess
from pathlib import Path
lane=Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
freeze="5017e1f7299c3a812e87e7950148f54313dd279e"
text=Path("/fast/scratch/hyaku/kaidoku-r47/ScoutSources/SOURCES.freeze.md").read_text()
rows=0; refs=[]; 
for i,s in enumerate(text.splitlines(),1):
    if not re.match(r"^\|\s*S[0-9]{3,}\s*\|", s):
        continue
    p=s.split("|")
    rows+=1
    if p[8].strip()!="mined":
        continue
    for t in re.split(r"[,;]", p[11]):
        q=t.strip()
        if q and q!="—":
            refs.append(q)
uniq=sorted(set(refs))
mc=mw=0
for q in uniq:
    r=subprocess.run(["git","-C",str(lane),"cat-file","-e",f"{freeze}:{q}"])
    if r.returncode!=0:
        mc+=1
        print("missing_commit", q)
    if not (lane/q).exists():
        mw+=1
        print("missing_worktree", q)
print(f"rows={rows} mined_refs={len(refs)} unique={len(uniq)} missing_commit={mc} missing_worktree={mw}")
'
