import hashlib, json, subprocess, datetime, os
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
PATHS=["tools/round-46","plans/round-46-claims.md"]
windows=["332f4884..58eb04b6","0425224..58eb04b6","58eb04b6..58eb04b6","332f4884..332f4884",
         "0425224..332f4884","0425224..0425224"]
arms=[[],["-m"],["--diff-merges=first-parent"],["-m","--diff-merges=first-parent"]]
out={"lane":LANE,"paths":PATHS,"merges_in_range":{"332f4884..58eb04b6":0,"0425224..58eb04b6":0},
     "runs":[]}
for w in windows:
    for arm in arms:
        cmd=["git","-C",LANE,"log","--name-status","--format="]+arm+[w,"--"]+PATHS
        t=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        r=subprocess.run(cmd,capture_output=True)
        out["runs"].append({"window":w,"arm":arm,"cmd":" ".join(cmd),"rc":r.returncode,
            "bytes":len(r.stdout),"sha256":hashlib.sha256(r.stdout).hexdigest(),
            "stdout_repr":r.stdout.decode(errors="replace"),
            "utc":t})
with open(os.path.join(LANE,".ufo/waves/round-47/w1/LabWindowProbe/window-receipt.json"),"w") as fh:
    json.dump(out,fh,indent=1)
print(json.dumps([{k:r[k] for k in ("window","arm","rc","bytes","sha256")} for r in out["runs"]],indent=0))
