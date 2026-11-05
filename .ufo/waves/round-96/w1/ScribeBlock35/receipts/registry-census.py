import importlib.util, json, os, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r96/ScribeBlock35"
C = os.path.join(S, "clone")
spec = importlib.util.spec_from_file_location(
    "regconf", os.path.join(C, "tools/round-68/registry-conformance.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

plans = {}
for name in sorted(os.listdir(os.path.join(C, "plans"))):
    if name.startswith("round-") and name.endswith("-claims.md"):
        p = os.path.join(C, "plans", name)
        plans["plans/" + name] = open(p, encoding="utf-8").read()

existing = set(subprocess.run(
    ["git", "-C", C, "ls-tree", "-r", "--name-only", "HEAD"],
    capture_output=True, text=True, check=True).stdout.split())

base_skill = subprocess.run(["git", "-C", C, "show", "HEAD:SKILL.md"],
                            capture_output=True, text=True, check=True).stdout
after_skill = open(os.path.join(C, "SKILL.md"), encoding="utf-8").read()

out = {"tool": "tools/round-68/registry-conformance.py",
       "method": "census() called in-memory on the base SKILL.md (git show HEAD:SKILL.md) "
                 "and on the worktree SKILL.md with the ten seat rows applied; "
                 "the CLI reads SKILL.md at --rev, so it cannot see an uncommitted row",
       "base_revision": "3baac2ef4b9b2830d299125b8184ca06d9e6584d"}
for label, text in (("base", base_skill), ("after_worktree", after_skill)):
    c = m.census(plans, text, existing)
    out[label] = {"mismatches": c["mismatches"],
                  "unregistered": c["unregistered"],
                  "thin": c["thin"],
                  "duplicate_rows": c["duplicate_rows"],
                  "row_absent": c["row_absent"]}
out["registered_by_the_ten_rows"] = sorted(
    set(out["base"]["unregistered"]) - set(out["after_worktree"]["unregistered"]))
out["still_unregistered_round_96"] = [
    p for p in out["after_worktree"]["unregistered"] if "/round-96/" in p]
print(json.dumps(out, indent=1, sort_keys=True))
