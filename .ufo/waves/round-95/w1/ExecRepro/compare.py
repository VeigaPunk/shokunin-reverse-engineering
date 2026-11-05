import json, sys, os, hashlib
SEAT, LANE = sys.argv[1], sys.argv[2]
def J(p):
    with open(p) as f: return json.load(f)
def T(p):
    with open(p, encoding="utf-8") as f: return f.read()
def rc(p): return int(T(p).strip())
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def cmp(label, mine, theirs, fields):
    print("##", label)
    for k in fields:
        m = mine.get(k) if isinstance(mine, dict) else None
        t = theirs.get(k) if isinstance(theirs, dict) else None
        print(f"  {k}: mine={m!r} committed={t!r} -> {'match' if m==t else 'MISMATCH'}")
S_ = LANE + "/.ufo/waves/round-95/l1/scores"
P_ = LANE + "/.ufo/waves/round-95/pre"
F_ = LANE + "/.ufo/waves/round-95/forgery"
# honest v5 run
cmp("honest v5 (L1 committed honest-pos.json)", J(SEAT+"/honest-pos.json"), J(S_+"/honest-pos.json"),
    ["class","counter_sha256","counts","exit","expect","fresh_roundtrip" if False else "counts"])
print("  stdout equal:", T(SEAT+"/honest-pos.stdout")==T(S_+"/honest-pos.stdout"), " rc mine=%d committed=%d" % (rc(SEAT+"/honest-pos.rc"), rc(S_+"/honest-pos.rc")))
print("  stderr equal:", T(SEAT+"/honest-pos.stderr")==T(S_+"/honest-pos.stderr"))
mj, cj = J(SEAT+"/honest-pos.json"), J(S_+"/honest-pos.json")
print("  json keys equal:", sorted(mj)==sorted(cj), " full json equal:", mj==cj)
print("  json diff keys:", [k for k in set(mj)|set(cj) if mj.get(k)!=cj.get(k)])
# forgery
mf, cf = J(SEAT+"/forgery.json"), J(S_+"/c1-forgery-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json")
print("## forgery battery vs l1 committed c1-forgery-at-4bda...json")
print("  full json equal:", mf==cf, " diff keys:", [k for k in set(mf)|set(cf) if mf.get(k)!=cf.get(k)])
for k in ["met","expect","instrument_revision","world_revision","counter_sha256","before","honest"]:
    print(f"  {k}: mine={mf.get(k)!r} committed={cf.get(k)!r} -> {'match' if mf.get(k)==cf.get(k) else 'MISMATCH'}")
print("  forgeries mine:", [(f['name'],f['exit'],f['reasons'],f['refused']) for f in mf['forgeries']])
print("  forgeries committed:", [(f['name'],f['exit'],f['reasons'],f['refused']) for f in cf['forgeries']])
print("  stdout equal to committed c1-forgery-stdout.txt:", T(SEAT+"/forgery.stdout")==T(S_+"/c1-forgery-stdout.txt"))
print("  stdout mine:", repr(T(SEAT+"/forgery.stdout")))
print("  committed stdout:", repr(T(S_+"/c1-forgery-stdout.txt")))
print("  rc mine=%d" % rc(SEAT+"/forgery.rc"))
# fixture sha
print("## forgery fixtures: sha256 of committed vs fixture_sha256 pinned in receipt")
for name, d in mf["fixture_sha256"].items():
    for ext, want in d.items():
        p = f"{F_}/forge-{name}.{ext}" if name!="pos" else f"{F_}/forge-pos.{ext}"
        got = sha(p) if os.path.exists(p) else None
        print(f"  {name}.{ext}: got={got} pinned={want} -> {'match' if got==want else 'MISMATCH'}")
print("  fixture rc contents:", {n: T(f"{F_}/forge-{n}.rc").strip() for n in ["pos","F1","F2","F3"]})
# probe v5
mp, cp = J(SEAT+"/probe-v5.json"), J(S_+"/c1-symlink-v5-at-4bda1d1dd3788973f10e61212b70df18b3b14ea0.json")
print("## probe v5 vs committed c1-symlink-v5-at-4bda...json")
print("  full json equal:", mp==cp, " diff keys:", [k for k in set(mp)|set(cp) if mp.get(k)!=cp.get(k)])
for k in ["met","receipt_label","receipt_met","receipt_valid","revision","verdict","victim_intact","tmp_is_symlink","tmp_left","writer_rc"]:
    print(f"  {k}: mine={mp.get(k)!r} committed={cp.get(k)!r} -> {'match' if mp.get(k)==cp.get(k) else 'MISMATCH'}")
print("  probe rc mine=%d" % rc(SEAT+"/probe-v5.rc"))
# probe v4 at base
md, cd = J(SEAT+"/probe-v4-at-base.json"), J(P_+"/c1-symlink-v4-at-base.json")
print("## probe v4 at base vs pre/c1-symlink-v4-at-base.json")
print("  full json equal:", md==cd, " diff keys:", [k for k in set(md)|set(cd) if md.get(k)!=cd.get(k)])
for k in ["met","receipt_label","receipt_met","receipt_valid","revision","verdict","victim_intact","tmp_is_symlink","tmp_left","writer_rc","writer"]:
    print(f"  {k}: mine={md.get(k)!r} committed={cd.get(k)!r} -> {'match' if md.get(k)==cd.get(k) else 'MISMATCH'}")
print("  probe rc mine=%d" % rc(SEAT+"/probe-v4-at-base.rc"))
# old counter at base
mo, co = J(SEAT+"/d1-old-counter.json"), J(P_+"/c1-old-counter-admits-at-base.json")
print("## old counter over committed forge fixtures vs pre/c1-old-counter-admits-at-base.json")
print("  full json equal:", mo==co, " diff keys:", [k for k in set(mo)|set(co) if mo.get(k)!=co.get(k)])
for k in ["met","counts_of_4","prefix"]:
    print(f"  {k}: mine={mo.get(k)!r} committed={co.get(k)!r} -> {'match' if mo.get(k)==co.get(k) else 'MISMATCH'}")
print("  rc mine=%d" % rc(SEAT+"/d1-old-counter.rc"))
