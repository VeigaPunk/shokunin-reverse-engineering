import importlib.util, json, os
from pathlib import Path
REPO=Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
FREEZE="3663e6b21dccf4c4957f459301156664d8b151d6"
REV="6dcc447eeca251e2435c14048bc0c5065e12df1f"
spec=importlib.util.spec_from_file_location("r67",REPO/"tools/round-67/avm-le-counter.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
eng,dg=m.load_engine(REPO)
work=Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims/o/probe-work");work.mkdir(parents=True,exist_ok=True)
p=m.patch_engine(eng,(REPO/m.RULE_V2).resolve(),work,REPO)
rel=eng.GAPRULE
out={"counter_sha256":m.sha256_file(REPO/"tools/round-67/avm-le-counter.py"),
     "patched_gaprule":rel,"is_relative":not rel.startswith("/"),
     "show_at_freeze":eng.show(REPO,FREEZE,rel) is not None,
     "show_at_rev":eng.show(REPO,REV,rel) is not None,
     "patches":p}
try:
    res=eng.measure(str(REPO),REV,FREEZE,"/nonexistent",target=m.TARGET,
                    expected_ids=eng.IDS,carrier_cache="/fast/scratch/hyaku/kaidoku-r67/CriticClaims/o/empty-cache")
    out["measure_reached"]=True
    out["matched"]=res.get("matched");out["met_target"]=res.get("met_target")
    out["failing"]=m.failing_lists(res)[0][:6]
except Exception as e:
    out["measure_reached"]=False
    out["exception"]="%s: %s"%(type(e).__name__,str(e)[:300])
Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims/o/probe-fixed.json").write_text(json.dumps(out,indent=1,sort_keys=True)+"\n")
print(json.dumps(out,indent=1,sort_keys=True)[:2000])
