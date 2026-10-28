import json, os, sys
S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, S)
import attack4, attack4b
env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
sys.path.insert(0, os.path.join("/home/vgpnk/Projects/shokunin/kaidoku-shokunin", "tools/round-47"))
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46")
import exact
skill = attack4b.git_show("HEAD", "SKILL.md")
blk = [b for b in exact.blocks_of(skill) if exact.MARKER in b][0]
rows = [list(r) for r in exact.table(blk)[1]]
print("tip rows:", [r[0][:22] for r in rows], [r[2] for r in rows])
extra = ["corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md"]
files0 = {p: attack4b.git_show("HEAD", p) for p in attack4b.FILES + extra}
cases = []
cases.append(("t0-genuine", rows))
r = [list(x) for x in rows]; r[0][0] = r[0][0].replace("R46-CL2", "R46-CL2x", 1)
cases.append(("t8-id-with-suffix", r))
r = [list(x) for x in rows]; r[2][0] = r[2][0].replace("R46-CL2", "R46-CL2x", 1)
cases.append(("t8b-substring-id-mid-table", r))
r = [list(x) for x in rows]; a = [x[2] for x in r]; a = a[1:] + a[:1]
for i in range(4): r[i][2] = a[i]
cases.append(("t10-arm-permutation", r))
out = []
for name, spec in cases:
    files = dict(files0); files["SKILL.md"] = attack4.build(skill, attack4.rows_of(spec))
    d, rev = attack4b.build_repo(files, name, env)
    v3, o3, cmd = attack4b.score(d, rev, "v3", env)
    v2, _, _ = attack4b.score(d, rev, "v2", env)
    rec = {"name": name, "fixture": d, "rev": rev, "command": cmd, "v3_exit": v3,
           "v2_exit": v2, "failing": json.loads(o3).get("failing"),
           "arm_tokens": json.loads(o3).get("arm_tokens"),
           "routed_counts": json.loads(o3).get("routed_counts"), "spec": spec}
    out.append(rec)
    print("%-28s v3=%d v2=%d %s" % (name, v3, v2, rec["failing"]))
json.dump(out, open(os.path.join(S, "tip-results.json"), "w"), indent=1)
