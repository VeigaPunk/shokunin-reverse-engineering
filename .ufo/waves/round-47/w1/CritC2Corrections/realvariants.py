import hashlib, json, os, subprocess, sys
S = "/fast/scratch/hyaku/kaidoku-r47/CritC2Corrections"
C = os.path.join(S, "realclone")
REC = os.path.join(C, "tools/round-47/record.py")
CARD = os.path.join(C, "SCORECARD.md")
ORIG = "- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md"

def sh(*a):
    return subprocess.run(list(a), capture_output=True, text=True)

def measure(label):
    r = sh(sys.executable, "-I", "-B", REC, "--root", C, "--rev", "HEAD")
    rec = json.loads(r.stdout) if r.stdout.strip().startswith("{") else {"raw": r.stdout[:300]}
    return {"label": label, "exit": r.returncode,
            "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
            "failing": rec.get("failing"), "mismatches": rec.get("mismatches"),
            "corrections": rec.get("corrections"), "corrections_bad": rec.get("corrections_bad"),
            "exempted": [(e["class"], e["key"]) for e in (rec.get("exempted") or [])],
            "battery": {k: (rec.get("battery") or {}).get(k) for k in ("correction_forgeries", "forgeries_green")},
            "atom_window": [e["atom"][:120] for e in (rec.get("exempted") or []) if e["class"] == "window"]}

orig = open(CARD).read()
assert ORIG in orig
out = []
out.append(measure("T0-baseline-lane-tip"))

def commit(msg):
    sh("git", "-C", C, "add", "-A"); sh("git", "-C", C, "commit", "-q", "-m", msg)
    return sh("git", "-C", C, "rev-parse", "HEAD").stdout.strip()

# T1 tautological window: identical endpoints around the commit that made the change
open(CARD, "w").write(orig.replace(ORIG, "- corrects window round-46: empty in 332f4884..332f4884 -- tools/round-46 plans/round-46-claims.md"))
out[-1]["rev"] = sh("git", "-C", C, "rev-parse", "HEAD").stdout.strip()
commit("T1 tautology")
out.append(measure("T1-window-tautology-332f4884..332f4884")); out[-1]["rev"] = sh("git", "-C", C, "rev-parse", "HEAD").stdout.strip()

# T2 honest statement about the window the sentence actually names
h = orig.replace("- corrects window round-46: empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md",
                 "- corrects window round-46: empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md")
assert h != orig
open(CARD, "w").write(h); commit("T2 honest window")
out.append(measure("T2-honest-window-0425224..58eb04b6")); out[-1]["rev"] = sh("git", "-C", C, "rev-parse", "HEAD").stdout.strip()

# T3 window correction removed entirely
g = orig.replace(ORIG + " — the round-46 sentence named a `<tip>` placeholder no command can resolve; this is the concrete\n  window it meant, and `git log --name-status --format=` over it prints nothing.", "")
if g == orig:
    lines = orig.splitlines(True)
    g = "".join(l for i, l in enumerate(lines) if "corrects window round-46" not in l)
open(CARD, "w").write(g); commit("T3 window removed")
out.append(measure("T3-window-correction-removed")); out[-1]["rev"] = sh("git", "-C", C, "rev-parse", "HEAD").stdout.strip()

print(json.dumps(out, indent=1))
