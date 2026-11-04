import importlib.util, json, sys
P="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-68/registry-conformance.py"
spec=importlib.util.spec_from_file_location("rc",P); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
MARK_OPEN=m.MARK_OPEN
def skill(rows):
    return "\n".join([MARK_OPEN,"| tool | g | v | s | p | w | o |","|---|---|---|---|---|---|---|",*rows,m.MARK_CLOSE,""])
def row(p,v="0=met; 1=not met; 2=could-not-evaluate"):
    return f"| `{p}` | g | {v} | s | p | w | o |"
execs={"tools/round-67/a.py","tools/round-50/a.py"}
reg=skill([row("tools/round-67/a.py"),row("tools/round-50/a.py")])

# A: the untested combination -- registry populated (2 rows), scope collapsed to zero (no plans read)
rA=m.census({}, reg, execs)
print("A scope0_registry2", json.dumps({k:rA[k] for k in ("ok","mismatches","scope_size","registry_rows","unregistered","row_absent","thin","duplicate_rows")},sort_keys=True))

# B: control -- same registry, one plan naming a registered tool (scope 1)
rB=m.census({"plans/round-67-claims.md":"uses tools/round-67/a.py"}, reg, execs)
print("B scope1_registry2", json.dumps({k:rB[k] for k in ("ok","mismatches","scope_size","registry_rows")},sort_keys=True))

# C: control -- registry populated, plan names an UNregistered tool (must be red)
rC=m.census({"plans/round-67-claims.md":"uses tools/round-67/zz.py"}, reg, execs|{"tools/round-67/zz.py"})
print("C scope1_unregistered", json.dumps({k:rC[k] for k in ("ok","mismatches","scope_size","unregistered")},sort_keys=True))

# D: registry rows whose paths are all absent from the tree, scope zero -> row_absent should fire
rD=m.census({}, skill([row("tools/round-99/gone.py")]), execs)
print("D scope0_rowabsent", json.dumps({k:rD[k] for k in ("ok","mismatches","scope_size","row_absent")},sort_keys=True))
