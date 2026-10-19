#!/usr/bin/env bash
# EX-04 real-payload simulation: EX-01's rule #14 applied, then the refresh.
set -u
SP=/dev/shm/ex04
export TMPDIR=$SP/tmp
REPO=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ART=$REPO/.ufo/waves/arc3-loop1-round2/claims/c1/EX-04
EX01=$REPO/.ufo/waves/arc3-loop1-round2/claims/c1/EX-01
R=$ART/receipts
SIM=$SP/sim-real
mkdir -p "$R"

say() { echo; echo "##### $* #####"; }

say "R0 fresh scratch tree at lane HEAD"
rm -rf "$SIM"; mkdir -p "$SIM"
git -C "$REPO" archive HEAD | tar -x -C "$SIM"
git -C "$SIM" init -q; git -C "$SIM" config user.email ex04@shokunin.local; git -C "$SIM" config user.name EX-04
git -C "$SIM" add -A; git -C "$SIM" commit -qm "sim-real baseline: lane HEAD"
git -C "$SIM" rev-parse HEAD
sha256sum "$SIM/SKILL.md" "$SIM/SHONEN.md"

say "R1 extract EX-01 payload between markers; re-derive its identity"
python3 - "$EX01/rule14.patch.md" "$SP/rule14-payload.txt" <<'PY' | tee "$R/r1-payload-identity.txt"
import hashlib, pathlib, sys
src = pathlib.Path(sys.argv[1]).read_text()
block = src.split("<!-- payload-begin -->\n", 1)[1].split("<!-- payload-end -->", 1)[0]
pathlib.Path(sys.argv[2]).write_text(block)
b = block.encode()
print("payload bytes=%d lines=%d sha256=%s"
      % (len(b), block.count("\n"), hashlib.sha256(b).hexdigest()))
print("EX-01 claimed: 896 bytes / a47dc38d1e12856bb34b3f1310af7109d65c649f8eef17a5feb3c00781623b80")
PY

say "R2 apply via EX-01's own apply-rule14.py"
python3 "$EX01/evidence/apply-rule14.py" "$SIM" "$SP/rule14-payload.txt" | tee "$R/r2-apply.txt"
git -C "$SIM" add -A; git -C "$SIM" commit -qm "sim-real: EX-01 rule #14" | tee -a "$R/r2-apply.txt"
sha256sum "$SIM/SKILL.md" | tee -a "$R/r2-apply.txt"
wc -l "$SIM/SKILL.md" | tee -a "$R/r2-apply.txt"
echo "EX-01 claimed post identity: 19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90 / 385 lines" | tee -a "$R/r2-apply.txt"

say "R3 geometry + prior-rule byte-identity"
python3 - <<'PY' 2>&1 | tee "$R/r3-geometry.txt"
from pathlib import Path
s=(Path("/dev/shm/ex04/sim-real")/"SKILL.md").read_text().splitlines()
start=next(i for i,l in enumerate(s,1) if l.startswith("## Queue-drain craft"))
nxt=next(i for i,l in enumerate(s,1) if i>start and l.startswith("## "))
end=max(i for i in range(start,nxt) if s[i-1].strip())
blocks=[i for i in range(start,end+1) if s[i-1].startswith("- **")]
print("start",start,"next_heading",nxt,"last_rule_line",end,"blocks",len(blocks),"rule14_span",blocks[-1],end)
PY
git -C "$SIM" show HEAD~1:SKILL.md | sed -n '1,239p' > "$SP/prior239-pre.txt"
sed -n '1,239p' "$SIM/SKILL.md" > "$SP/prior239-post.txt"
cmp "$SP/prior239-pre.txt" "$SP/prior239-post.txt" && echo "cmp lines 1-239: IDENTICAL" | tee -a "$R/r3-geometry.txt"

say "R4 stale SHONEN: checker / command A / probes (end-anchored needle = rule #14 tail)"
python3 "$ART/craft-pointer-truth.py" "$SIM" 2>&1 | tee "$R/r4-checker-stale.txt"
(cd "$SIM" && python3 "$SP/scripts/commandA.py" HEAD) | tee "$R/r4-commandA.json"
(cd "$SIM" && python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict) | tee "$R/r4-probe-committed.txt"
python3 - "$SIM" "$SP" <<'PY'
import hashlib, json, pathlib, sys
sim, sp = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
t = json.loads((sim/".ufo/gates/citation-drift/pointer-table.json").read_text())
for e in t["entries"]:
    if e["id"] == "shonen-skill-range":
        e["must_match"] = ("An artifact that records its own byte-identity[\\s\\S]*"
                           "never a carried-over number\\.\\s*\\Z")
out = sp/"table-enda-real.json"; out.write_text(json.dumps(t, indent=2) + "\n")
exp = json.loads((sim/".ufo/gates/citation-drift/expected.json").read_text())
exp["pointer_table"] = {"sha256": hashlib.sha256(out.read_bytes()).hexdigest(), "note": "scratch end-anchored (rule #14 tail)"}
(sp/"expected-enda-real.json").write_text(json.dumps(exp, indent=2) + "\n")
PY
(cd "$SIM" && python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table "$SP/table-enda-real.json" --expected "$SP/expected-enda-real.json" --strict) | tee "$R/r4-probe-enda.txt"

say "R5 apply the pointer-refresh patch text (81-252, 14/14; EX-01 §4.3 wording)"
python3 - "$SIM" <<'PY' | tee "$R/r5-refresh.txt"
import hashlib, sys, pathlib
sim = pathlib.Path(sys.argv[1])
s=(sim/"SKILL.md").read_text().splitlines()
start=next(i for i,l in enumerate(s,1) if l.startswith("## Queue-drain craft"))
nxt=next(i for i,l in enumerate(s,1) if i>start and l.startswith("## "))
end=max(i for i in range(start,nxt) if s[i-1].strip())
blocks=[i for i in range(start,end+1) if s[i-1].startswith("- **")]
p=(sim/"SHONEN.md"); lines=p.read_text().splitlines(keepends=True)
new6=("  asserted: `SKILL.md:%d-%d` (craft section; rules #11-%d added arc2 rounds 4/7/9 + arc3 round 2); "
      "%d/%d rule blocks have resolvable citations, not a full semantic audit — `SCORECARD.md`, command A; "
      "no identified outside verifier.") % (start,end,len(blocks),len(blocks),len(blocks))
print("OLD:", lines[5].rstrip()); print("NEW:", new6)
lines[5]=new6+"\n"; p.write_text("".join(lines))
print("shonen sha256 after:", hashlib.sha256(p.read_bytes()).hexdigest())
PY
git -C "$SIM" add -A; git -C "$SIM" commit -qm "sim-real: SHONEN pointer refresh"
git -C "$SIM" diff HEAD~1 HEAD -- SHONEN.md > "$ART/shonen-refresh-rule14.patch"
cat "$ART/shonen-refresh-rule14.patch" | tee -a "$R/r5-refresh.txt"

say "R6 post-refresh verification"
python3 "$ART/craft-pointer-truth.py" "$SIM" 2>&1 | tee "$R/r6-checker.txt"
(cd "$SIM" && python3 "$SP/scripts/commandA.py" HEAD) | tee "$R/r6-commandA.json"
(cd "$SIM" && python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --strict) | tee "$R/r6-probe-committed.txt"
(cd "$SIM" && python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table "$SP/table-enda-real.json" --expected "$SP/expected-enda-real.json" --strict) | tee "$R/r6-probe-enda.txt"

say "R7 the refresh diff applies at the unrefreshed post-append tree (git apply --check)"
rm -rf "$SP/sim-real-check"; mkdir -p "$SP/sim-real-check"
git -C "$SIM" archive HEAD~1 | tar -x -C "$SP/sim-real-check"
(cd "$SP/sim-real-check" && git init -q && git apply --check "$ART/shonen-refresh-rule14.patch" && echo "APPLY-CHECK: OK at lane-HEAD+rule14 (SHONEN unrefreshed)") | tee "$R/r7-apply-check.txt"

say "R8 artifact inventory"
sha256sum "$ART/craft-pointer-truth.py" "$ART/shonen-refresh-rule14.patch" "$EX01/rule14.patch.md" "$SP/rule14-payload.txt" | tee "$R/r8-inventory.txt"

say "DONE"
