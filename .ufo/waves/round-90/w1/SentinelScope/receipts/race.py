import json,os,subprocess,sys,time
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; TOOL=LANE+"/tools/round-90/upx-break-repair.py"
S="/fast/scratch/hyaku/kaidoku-r90/SentinelScope"; R=os.path.join(S,"race")
os.makedirs(R,exist_ok=True)
path=os.path.join(R,"in"); out=os.path.join(R,"out")
fx=json.load(open(os.path.join(S,"fx.json"))); data=open(fx["jq"]["tampered"],"rb").read()
res={"trials":0,"hangs":0,"rcs":{},"tracebacks":0}
if os.path.lexists(path): os.unlink(path)
open(path,"wb").write(data)
mode="reg"
def flip():
    global mode
    try: os.unlink(path)
    except FileNotFoundError: pass
    if mode=="reg":
        open(path,"wb").write(data); mode="fifo"
    else:
        os.mkfifo(path); mode="reg"
t0=time.time()
for i in range(300):
    flip()
    try:
        p=subprocess.run([sys.executable,"-I","-B",TOOL,"--in",path,"--out",out],
                         capture_output=True,text=True,timeout=4)
        res["trials"]+=1
        res["rcs"][str(p.returncode)]=res["rcs"].get(str(p.returncode),0)+1
        if "Traceback" in (p.stderr or ""): res["tracebacks"]+=1
    except subprocess.TimeoutExpired:
        res["hangs"]+=1
        subprocess.run(["pkill","-9","-f","upx-break-repair.py --in "+path],check=False)
res["wall_s"]=round(time.time()-t0,1)
json.dump(res,open(os.path.join(S,"race.json"),"w"),indent=1)
print(json.dumps(res))
