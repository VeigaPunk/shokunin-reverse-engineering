import hashlib, subprocess, sys, json
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
def blob(rev):
    if rev=="WORKTREE": return open(f"{LANE}/SKILL.md","rb").read()
    return subprocess.run(["git","-C",LANE,"show",f"{rev}:SKILL.md"],capture_output=True,check=True).stdout
def region(data):
    lines=data.split(b"\n")
    i=[k for k,l in enumerate(lines) if b"<!-- sqfs-triage-table v4 -->" in l][0]
    j=i
    while j+1 < len(lines):
        s=lines[j+1].strip()
        if s.startswith(b"|") or lines[j+1].startswith(b"  <!--"): j+=1; continue
        if s==b"":
            m=j+1
            while m<len(lines) and lines[m].strip()==b"": m+=1
            if m<len(lines) and lines[m].strip().startswith(b"|"): j=m-1; continue
        break
    return b"\n".join(lines[i:j+1])
out={}
for rev in ["WORKTREE","c29360e3","c48f8a4b","55bcce69","8bb1090a","d1681696","eb8215ac","e1c83313"]:
    seg=region(blob(rev)); out[rev]={"bytes":len(seg),"sha256":hashlib.sha256(seg).hexdigest()}
print(json.dumps(out,indent=1,sort_keys=True))
