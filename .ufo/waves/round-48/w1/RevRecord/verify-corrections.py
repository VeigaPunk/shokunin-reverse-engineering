import json, subprocess, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48")
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47")
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46")
import record2, gate
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "ac02a79ff84133220d01ce3b59a4789b7004dbc5"
def files(p):
    r = subprocess.run(["git","-C",ROOT,"show",f"{REV}:{p}"],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
card = files("SCORECARD.md")
secs = record2.section_bodies(card)
mod = record2.oracle(ROOT, REV)
spawns = record2.spawns_cache(mod, files)
out = {}
# candidate seats correction for round 47
c1 = {"class":"seats","key":"47","text":"- corrects seats round-47: 1 wave, 75 seats total","statement":"1 wave, 75 seats total"}
out["seats_r47"] = mod["corrects"](c1, files, ROOT, REV, spawns)
# candidate quote correction
c2 = {"class":"quote","key":"47","text":"- corrects quote round-47: exempted 1","statement":"exempted 1"}
out["quote_r47"] = record2._quote_correction(c2, secs, files)
# sanity: wrong-value variants must fail
c3 = dict(c1, statement="1 wave, 74 seats total"); out["seats_r47_wrong"] = mod["corrects"](c3, files, ROOT, REV, spawns)
c4 = dict(c2, statement="exempted 2"); out["quote_r47_samevalue"] = record2._quote_correction(c4, secs, files)
c5 = dict(c2, statement="exempted 9"); out["quote_r47_unbacked"] = record2._quote_correction(c5, secs, files)
print(json.dumps(out, indent=1, default=str))
