import json, os, sys
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(ROOT,"tools/round-47")); sys.path.insert(0, os.path.join(ROOT,"tools/round-46"))
import gate, record
out={}
for rev in sys.argv[1:]:
    tip=gate.resolve(ROOT,rev)
    if tip is None:
        out[rev]={"resolved":None}; continue
    f=lambda p: gate.show(ROOT,tip,p)
    cov=record.coverage_pair(ROOT,tip,f); dep=record.depth_pair(f)
    def sc(p):
        return None if not p else round(10*p[0]/p[1],2)
    out[rev]={"resolved":tip,"coverage":cov,"coverage_score":sc(cov),"depth":dep,"depth_score":sc(dep)}
print(json.dumps(out,indent=1))
