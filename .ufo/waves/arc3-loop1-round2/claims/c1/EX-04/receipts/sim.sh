#!/usr/bin/env bash
# SEAT EX-04 (c1, arc3-loop1-round2): pointer-refresh insert simulation.
# All work in /dev/shm/ex04 (scratch). Writes receipts under the seat artifact.
set -u
SP=/dev/shm/ex04
export TMPDIR=$SP/tmp
SIM=$SP/sim
ART=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/claims/c1/EX-04
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
R=$ART/receipts
CHK=$ART/craft-pointer-truth.py
mkdir -p "$SP/tmp" "$R"

say() { echo; echo "##### $* #####"; }
gc() { git -C "$SIM" add -A >/dev/null && git -C "$SIM" commit -qm "$1" && git -C "$SIM" rev-parse HEAD; }
probe() { # $1 label, rest probe args
  local label="$1"; shift
  (cd "$SIM" && python3 .ufo/gates/citation-drift/citation-drift-probe.py "$@") 
}

say "T0 fresh sim tree from lane HEAD"
rm -rf "$SIM"; mkdir -p "$SIM"
git -C "$REPO" archive HEAD | tar -x -C "$SIM"
git -C "$SIM" init -q; git -C "$SIM" config user.email ex04@shokunin.local; git -C "$SIM" config user.name EX-04
git -C "$SIM" add -A; git -C "$SIM" commit -qm "sim baseline: lane HEAD"

say "T0 baseline: tree identity"
sha256sum "$SIM/SKILL.md" "$SIM/SHONEN.md" | tee "$R/t0-tree-sha.txt"
wc -l "$SIM/SKILL.md" "$SIM/SHONEN.md" | tee -a "$R/t0-tree-sha.txt"
git -C "$SIM" rev-parse HEAD | tee -a "$R/t0-tree-sha.txt"

say "T0 checker (expect FAIL: stated end 243 vs last rule 239)"
python3 "$CHK" "$SIM" | tee "$R/t0-checker.txt"

say "T0 command A (expect 13/13, 82/82, 10.0/10.0)"
(cd "$SIM" && python3 "$SP/scripts/commandA.py" HEAD) | tee "$R/t0-commandA.json"

say "T0 committed probe run (expect clean findings=0)"
probe baseline --root . --rev HEAD --strict | tee "$R/t0-probe.txt"

say "T1 insert block A (representative rule #14 shape) via EX-05 harness"
wc -l "$SP/blockA.md" | tee "$R/t1-blockA.txt"
python3 "$REPO/.ufo/waves/arc3-loop1-round2/claims/c1/EX-05/insert-rule.py" "$SIM" "$SP/blockA.md" | tee -a "$R/t1-blockA.txt"
gc "sim T1: synthetic rule #14 (block A)" | tee -a "$R/t1-blockA.txt"
wc -l "$SIM/SKILL.md" | tee -a "$R/t1-blockA.txt"

say "T1 geometry after insert"
python3 - <<'PY' | tee "$R/t1-geometry.txt"
from pathlib import Path
s=(Path("/dev/shm/ex04/sim")/"SKILL.md").read_text().splitlines()
start=next(i for i,l in enumerate(s,1) if l.startswith("## Queue-drain craft"))
nxt=next(i for i,l in enumerate(s,1) if i>start and l.startswith("## "))
end=max(i for i in range(start,nxt) if s[i-1].strip())
blocks=[i for i in range(start,end+1) if s[i-1].startswith("- **")]
print("start",start,"next_heading",nxt,"last_rule_line",end,"blocks",len(blocks))
print("rule14_span",blocks[-1], end)
PY

say "T1 checker (expect FAIL: end + count)"
python3 "$CHK" "$SIM" | tee "$R/t1-checker-stale.txt"

say "T1 command A (expect 14/14)"
(cd "$SIM" && python3 "$SP/scripts/commandA.py" HEAD) | tee "$R/t1-commandA.json"

say "T1 probe, committed (content-anywhere) table: expect CLEAN = silent pass"
probe stale-committed --root . --rev HEAD --strict | tee "$R/t1-probe-committed.txt"

say "T1 probe, E16-style end-anchored scratch table (needle re-anchored to rule #14 tail)"
python3 - "$SIM" "$SP" <<'PY'
import hashlib, json, pathlib, sys
sim, sp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
t = json.loads((sim/".ufo/gates/citation-drift/pointer-table.json").read_text())
for e in t["entries"]:
    if e["id"] == "shonen-skill-range":
        e["must_match"] = ("An artifact that records its own byte-identity"
                           "[\\s\\S]*queue-b-ready\\.md:11`\\)\\.\\s*\\Z")
        e["note"] = ("SIMULATED end-anchored form (E16 §3.2 shape, re-anchored to the "
                     "newest rule's closing text): the stated range must END on the last "
                     "craft rule, not run past the next heading.")
out = sp/"table-enda.json"
out.write_text(json.dumps(t, indent=2) + "\n")
exp = json.loads((sim/".ufo/gates/citation-drift/expected.json").read_text())
exp["pointer_table"] = {"sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                        "note": "scratch end-anchored table, digest re-pinned for this simulation"}
(sp/"expected-enda.json").write_text(json.dumps(exp, indent=2) + "\n")
print("wrote", out, hashlib.sha256(out.read_bytes()).hexdigest())
PY
probe stale-enda --root . --rev HEAD --table "$SP/table-enda.json" --expected "$SP/expected-enda.json" --strict | tee "$R/t1-probe-enda.txt"

say "T2 apply the pointer-refresh patch text to SHONEN.md (end = last rule line, 14/14)"
python3 - "$SIM" <<'PY' | tee "$R/t2-refresh.txt"
import pathlib, re, sys
sim = pathlib.Path(sys.argv[1])
s = (sim/"SKILL.md").read_text().splitlines()
start = next(i for i, l in enumerate(s, 1) if l.startswith("## Queue-drain craft"))
nxt = next(i for i, l in enumerate(s, 1) if i > start and l.startswith("## "))
end = max(i for i in range(start, nxt) if s[i-1].strip())
blocks = [i for i in range(start, end+1) if s[i-1].startswith("- **")]
before = (sim/"SHONEN.md").read_text()
new6 = ("  asserted: `SKILL.md:%d-%d` (craft section; rules #11-%d added arc2 rounds 4/7/9 + arc3-loop1-round2); "
        "%d/%d rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; "
        "no identified outside verifier.") % (start, end, len(blocks), len(blocks), len(blocks))
lines = before.splitlines(keepends=True)
print("OLD:", lines[5].rstrip())
print("NEW:", new6)
lines[5] = new6 + "\n"
(sim/"SHONEN.md").write_text("".join(lines))
import hashlib
print("shonen_md_sha256_after", hashlib.sha256((sim/"SHONEN.md").read_bytes()).hexdigest())
print("shonen_lines_after", len((sim/"SHONEN.md").read_text().splitlines()))
PY
gc "sim T2: SHONEN pointer refresh" | tee -a "$R/t2-refresh.txt"
git -C "$SIM" show --stat --format=short HEAD | tee -a "$R/t2-refresh.txt"

say "T2 checker (expect PASS)"
python3 "$CHK" "$SIM" | tee "$R/t2-checker.txt"

say "T2 command A (expect 14/14 unchanged)"
(cd "$SIM" && python3 "$SP/scripts/commandA.py" HEAD) | tee "$R/t2-commandA.json"

say "T2 probe committed table (expect clean)"
probe refreshed-committed --root . --rev HEAD --strict | tee "$R/t2-probe-committed.txt"

say "T2 probe end-anchored table (expect clean now)"
probe refreshed-enda --root . --rev HEAD --table "$SP/table-enda.json" --expected "$SP/expected-enda.json" --strict | tee "$R/t2-probe-enda.txt"

say "T3 sensitivity: short block (3 lines) in a fresh scratch repo"
SIM2=$SP/sim2
rm -rf "$SIM2"; mkdir -p "$SIM2"
git -C "$REPO" archive HEAD | tar -x -C "$SIM2"
git -C "$SIM2" init -q; git -C "$SIM2" config user.email ex04@shokunin.local; git -C "$SIM2" config user.name EX-04
git -C "$SIM2" add -A; git -C "$SIM2" commit -qm "sim2 baseline"
python3 "$REPO/.ufo/waves/arc3-loop1-round2/claims/c1/EX-05/insert-rule.py" "$SIM2" "$SP/blockB.md" | tee "$R/t3-blockB.txt"
git -C "$SIM2" add -A; git -C "$SIM2" commit -qm "sim2 rule14 block B" >/dev/null
(cd "$SIM2" && python3 "$SP/scripts/commandA.py" HEAD) | tee -a "$R/t3-blockB.txt"
python3 - <<'PY' | tee "$R/t3-geometry.txt"
from pathlib import Path
for tag, root in (("A-8line", Path("/dev/shm/ex04/sim")), ("B-3line", Path("/dev/shm/ex04/sim2"))):
    s=(root/"SKILL.md").read_text().splitlines()
    start=next(i for i,l in enumerate(s,1) if l.startswith("## Queue-drain craft"))
    nxt=next(i for i,l in enumerate(s,1) if i>start and l.startswith("## "))
    end=max(i for i in range(start,nxt) if s[i-1].strip())
    print(f"{tag}: heading={start} next_heading={nxt} last_rule_line={end} -> SHONEN end must be {end}")
PY

say "T4 the instantiated refresh diff, and its applicability at an unrefreshed post-append tree"
git -C "$SIM" diff "$(git -C "$SIM" rev-parse HEAD~1)" HEAD -- SHONEN.md > "$ART/shonen-refresh-example.patch"
cat "$ART/shonen-refresh-example.patch" | tee "$R/t4-diff.txt"
git -C "$SIM2" apply --check "$ART/shonen-refresh-example.patch" && echo "APPLY-CHECK: OK at sim2 (rule appended, SHONEN unrefreshed)" | tee "$R/t4-apply-check.txt"

say "T5 receipt inventory"
sha256sum "$ART/craft-pointer-truth.py" "$SP/blockA.md" "$SP/blockB.md" "$ART/shonen-refresh-example.patch" "$R"/*.txt "$R"/*.json 2>/dev/null | tee "$R/t5-inventory.txt"
cp "$SP/blockA.md" "$SP/blockB.md" "$R/" 2>/dev/null

say "DONE"
