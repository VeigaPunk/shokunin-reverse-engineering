import json,os,subprocess,glob,datetime
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE="f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
def git(*a): return subprocess.run(["git","-C",LANE,*a],capture_output=True,text=True,check=True).stdout
rows=[]
for line in git("log","--reverse","--format=%H%x09%cI%x09%s",f"{FREEZE}..HEAD").strip().splitlines():
    h,ts,s=line.split("\t",2); rows.append({"commit":h,"committed":ts,"subject":s})
dec=json.JSONDecoder(); rec=[]
for p in sorted(glob.glob(f"{LANE}/.ufo/waves/round-45/**/preflight*.json",recursive=True)):
    txt=open(p).read(); i=0; objs=[]
    while i<len(txt):
        while i<len(txt) and txt[i] in " \n\t\r": i+=1
        if i>=len(txt): break
        try: o,j=dec.raw_decode(txt,i); objs.append(o); i=j
        except Exception: break
    if not objs: continue
    d=objs[-1]; mt=datetime.datetime.fromtimestamp(os.path.getmtime(p),datetime.timezone.utc)
    rec.append({"file":os.path.relpath(p,LANE),"rev":d.get("rev"),
        "mtime_utc":mt.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "vacuous": d.get("rev")==d.get("freeze"),"pathspec":d.get("pathspec")})
parse=lambda ts: datetime.datetime.fromisoformat(ts).astimezone(datetime.timezone.utc)
print("freeze",FREEZE)
print("== post-freeze commits: gate receipt scoring the PARENT, older than the commit ==")
preceded=0
for i,r in enumerate(rows):
    parent=FREEZE if i==0 else rows[i-1]["commit"]; ct=parse(r["committed"])
    hits=[x for x in rec if x["rev"]==parent and parse(x["mtime_utc"])<ct]
    real=[x for x in hits if not x["vacuous"]]
    if real: preceded+=1
    print(f"{r['commit'][:8]} {r['committed']} parent={parent[:8]} gate_before="
          f"{[x['file'].split('/')[-1]+('(vacuous)' if x['vacuous'] else '') for x in hits] or 'NONE'}")
print(f"preceded_by_a_real_gate_run = {preceded}/{len(rows)}")
print("== all round-45 preflight receipts by mtime ==")
for x in sorted(rec,key=lambda z:z["mtime_utc"]):
    print(f"{x['mtime_utc']} rev={(x['rev'] or 'NONE')[:8]} vacuous={x['vacuous']} {x['file']}")
