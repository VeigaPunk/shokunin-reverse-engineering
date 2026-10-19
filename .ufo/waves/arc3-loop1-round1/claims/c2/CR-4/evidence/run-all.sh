#!/usr/bin/env bash
# CR-4 (c2 critic) — cross-chain attack: "could an honest census scope re-key
# (EX-28) trip the citation-drift probe guard falsely?" Re-runnable, read-only
# on the lane repo. Scratch in /dev/shm/cr4 (/tmp is EDQUOT for this user).
# Every transcript in this directory is produced by this script. Quota-sensitive
# writes are retried (the host's tmpfs usrquota fluctuates); every check that
# could silently go vacuous carries an assertion.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/dev/shm/cr4
E=$R/.ufo/gates/citation-drift
D=$(cd "$(dirname "$0")" && pwd)
retry() { local i; for i in $(seq 1 40); do "$@" && return 0; sleep 3; done; return 1; }
rm -rf $S; mkdir -p $S $S/census-tree
cd "$R"

# ---------------------------------------------------------------- 01 baseline
{
echo "== environment: /tmp write test (EDQUOT evidence) =="
(echo x > /tmp/cr4-probe-write-test) 2>&1 || true; rm -f /tmp/cr4-probe-write-test
echo "== instruments, sha256 =="
sha256sum .ufo/gates/c1-census-v10.py "$E"/citation-drift-probe.py "$E"/expected.json "$E"/pointer-table.json
echo "== probe at HEAD (probe semantics) =="
python3 "$E"/citation-drift-probe.py --root . --rev HEAD --table "$E"/pointer-table.json --expected "$E"/expected.json; echo "exit=$?"
echo "== probe at HEAD (--strict) =="
python3 "$E"/citation-drift-probe.py --root . --rev HEAD --table "$E"/pointer-table.json --expected "$E"/expected.json --strict; echo "exit=$?"
echo "== probe selftest =="
python3 "$E"/citation-drift-probe.py --selftest --expected "$E"/expected.json; echo "exit=$?"
echo "== census at HEAD =="
python3 .ufo/gates/c1-census-v10.py --quiet; echo "exit=$?"
echo "== probe target files (table entries+quoted) — disjointness check =="
python3 - "$E"/pointer-table.json <<'PY'
import json,sys
t=json.load(open(sys.argv[1]))
targets=sorted({e['file'] for e in t.get('entries',[])+t.get('quoted',[])})
print("distinct targets:",len(targets))
for f in targets: print("  ",f)
print("gates-dir targets:",[f for f in targets if f.startswith('.ufo/gates')])
PY
} > "$D"/01-baseline.txt 2>&1

# ------------------------------------------------- 02 census re-key invariance
{
echo "== scratch clone (shared objects, no checkout), retried under quota =="
retry git clone -q --shared --no-checkout "$R" $S/scratch || { echo "ENV-BLOCKED: clone failed"; exit 9; }
echo "clone size: $(du -sh $S/scratch | cut -f1)"
cd $S/scratch && git read-tree HEAD && echo "read-tree-ok"
echo "== baseline probe at scratch HEAD =="
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev HEAD --table "$E"/pointer-table.json --expected "$E"/expected.json | tail -1
echo "== build sim commit: honest census re-key (header disposition + one bound re-key) =="
python3 - <<'PY'
src=open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py').read()
mod=src.replace('"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d."""',
 '"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d.\nE22 disposition sim (arc3-loop1-round1 EX-28): bound 702 -> 703 re-keyed per measured HEAD block end."""',1)
assert mod!=src
open('/dev/shm/cr4/census-sim.py','w').write(mod)
print("census-sim: +1 header line, one bound re-keyed")
PY
blob=$(git hash-object -w $S/census-sim.py)
git update-index --cacheinfo 100644,$blob,.ufo/gates/c1-census-v10.py
tree=$(git write-tree)
c1=$(git -c user.name=cr4 -c user.email=cr4@x commit-tree $tree -p HEAD -m "sim: honest census re-key (EX-28 shape)")
git update-ref refs/heads/sim-census $c1
echo "sim-census commit: $c1"
echo "== census blob sha256 HEAD vs sim-census (proof the commit edits the instrument) =="
git show HEAD:.ufo/gates/c1-census-v10.py | sha256sum | cut -d' ' -f1
git show sim-census:.ufo/gates/c1-census-v10.py | sha256sum | cut -d' ' -f1
echo "== probe at sim-census rev (probe semantics) =="
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev sim-census --table "$E"/pointer-table.json --expected "$E"/expected.json; echo "exit=$?"
echo "== probe at sim-census rev (--strict) =="
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev sim-census --table "$E"/pointer-table.json --expected "$E"/expected.json --strict | tail -1
echo "== table blob digest HEAD vs sim-census (the digest EX-16 pins must be invariant) =="
git show HEAD:.ufo/gates/citation-drift/pointer-table.json | sha256sum | cut -d' ' -f1
git show sim-census:.ufo/gates/citation-drift/pointer-table.json | sha256sum | cut -d' ' -f1
} > "$D"/02-census-rekey-invariance.txt 2>&1

# --------------------------------------------- 03 C1 edge: README.md edit shapes
{
cd $S/scratch
echo "== sim A: line-neutral token appended to corpus/README.md line 22 (C1's claimed shape) =="
git show HEAD:corpus/README.md > $S/readme-A.md
python3 - <<'PY'
p='/dev/shm/cr4/readme-A.md'; ls=open(p).read().split('\n')
assert 'r7:' in ls[21]
ls[21]=ls[21].rstrip()+' evm-r9-token'
open(p,'w').write('\n'.join(ls))
PY
blob=$(git hash-object -w $S/readme-A.md)
git read-tree sim-census && git update-index --cacheinfo 100644,$blob,corpus/README.md
tree=$(git write-tree); cA=$(git -c user.name=cr4 -c user.email=cr4@x commit-tree $tree -p sim-census -m "sim: README line-neutral append")
git update-ref refs/heads/sim-readme-A $cA; echo "commit: $cA"
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev sim-readme-A --table "$E"/pointer-table.json --expected "$E"/expected.json | tail -1
echo
echo "== sim B: one line INSERTED before corpus/README.md:175 (non-line-neutral shape) =="
git show HEAD:corpus/README.md > $S/readme-B.md
python3 - <<'PY'
p='/dev/shm/cr4/readme-B.md'; ls=open(p).read().split('\n')
ls.insert(174,'| r9-evm | new map row inserted (sim) |')
open(p,'w').write('\n'.join(ls))
PY
blob=$(git hash-object -w $S/readme-B.md)
git read-tree sim-census && git update-index --cacheinfo 100644,$blob,corpus/README.md
tree=$(git write-tree); cB=$(git -c user.name=cr4 -c user.email=cr4@x commit-tree $tree -p sim-census -m "sim: README line insertion")
git update-ref refs/heads/sim-readme-B $cB; echo "commit: $cB"
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev sim-readme-B --table "$E"/pointer-table.json --expected "$E"/expected.json; echo "exit=$?"
} > "$D"/03-readme-edge.txt 2>&1

# --------------------------------------------------- 04 guard simulation
{
cat > $S/guard-sim.py <<'EOF'
#!/usr/bin/env python3
"""CR-4 simulation of the DECLARED EX-16 preflight guard (NOT the real guard).
Declared semantics (claims-frozen.md:46-50; EX-20 row text; PL-2 prototype spec):
expected.json pins sha256(pointer-table.json); absent/unreadable/unpinned/mismatch
-> exit 2 could-not-evaluate before any entry is evaluated; else delegate."""
import hashlib, subprocess, sys
expected, table, pin = sys.argv[1], sys.argv[2], sys.argv[3]
try: data = open(table, 'rb').read()
except OSError as exc:
    print("CITATION_DRIFT: pointer_table_unreadable entry=%s %s" % (table, exc))
    print("CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2"); sys.exit(2)
got = hashlib.sha256(data).hexdigest()
if got != pin:
    print("CITATION_DRIFT: pointer_table_tampered entry=%s sha256 %s != pinned %s" % (table, got, pin))
    print("CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2"); sys.exit(2)
sys.exit(subprocess.run([sys.executable, sys.argv[4], '--root', sys.argv[5], '--rev', sys.argv[6],
                         '--table', table, '--expected', expected]).returncode)
EOF
PIN=$(sha256sum "$E"/pointer-table.json | cut -d' ' -f1)
echo "pin = sha256(pointer-table.json) = $PIN"
echo "== case 1: real table + real pin, rev = sim-census (after the honest re-key) =="
python3 $S/guard-sim.py "$E"/expected.json "$E"/pointer-table.json "$PIN" "$E"/citation-drift-probe.py $S/scratch sim-census; echo "exit=$?"
echo "== case 2: ONE honest appended table entry under the same (stale) pin =="
python3 - <<'PY'
import json
t=json.load(open('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json'))
t['entries'].append({"id":"sim-honest-future-entry","kind":"anchor","file":"SHONEN.md","must_match":"x","note":"honest future edit sim"})
json.dump(t, open('/dev/shm/cr4/table-edited.json','w'))
PY
python3 $S/guard-sim.py "$E"/expected.json $S/table-edited.json "$PIN" "$E"/citation-drift-probe.py $S/scratch HEAD; echo "exit=$?"
echo "== case 3: absent table =="
python3 $S/guard-sim.py "$E"/expected.json $S/absent.json "$PIN" "$E"/citation-drift-probe.py $S/scratch HEAD; echo "exit=$?"
echo "== pre-guard baseline: real probe + edited table (the debt, both modes silent) =="
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev HEAD --table $S/table-edited.json --expected "$E"/expected.json | tail -1
python3 "$E"/citation-drift-probe.py --root $S/scratch --rev HEAD --table $S/table-edited.json --expected "$E"/expected.json --strict | tail -1
} > "$D"/04-guard-sim.txt 2>&1

# ------------------------------------------- 05 mirror: EX-20 row vs census
{
CT=$S/census-tree
for f in PROVINCE.md SKILL.md SCORECARD.md; do retry cp "$R/$f" $CT/ || echo "ENV-BLOCKED: cp $f"; done
echo "== census on pristine 3-file tree =="
python3 "$R"/.ufo/gates/c1-census-v10.py --root $CT --quiet; echo "exit=$?"
DIF=$R/.ufo/waves/arc3-loop1-round1/claims/c2/SC-4/scratch/registry-row.diff
echo "== EX-20 diff (SC-4-extracted) sha256 =="; sha256sum "$DIF"
cd $CT
retry patch -p1 < "$DIF" >/dev/null 2>&1
H=$(sha256sum $CT/SKILL.md | cut -d' ' -f1)
echo "== patched SKILL.md sha256 = $H"
echo "   (SC-4 claimed after: fa94a4696ce68f96c8cdf717ac6d270ca7f0df5a4b590585bdedec95ff1628c5)"
if [ "$H" = "fa94a4696ce68f96c8cdf717ac6d270ca7f0df5a4b590585bdedec95ff1628c5" ]; then echo "ASSERT: patch applied, hash reproduced"; else echo "ENV-BLOCKED: patch did not land; subsequent sections invalid"; fi
echo "== census on EX-20-patched tree (C2's SKILL.md edit vs C3's instrument) =="
python3 "$R"/.ufo/gates/c1-census-v10.py --root $CT --quiet; echo "exit=$?"
echo
echo "== token-stress: add rea-agents@6.7.0 into the patched registry row (boundary demo) =="
python3 - <<'PY'
p='/dev/shm/cr4/census-tree/SKILL.md'; ls=open(p).read().split('\n')
assert 'citation-drift' in ls[370] and 'preflight table guard' in ls[370], "patched row absent — env-blocked"
ls[370]=ls[370].replace('preflight table guard','preflight table guard (pin re-checked vs rea-agents@6.7.0)')
open(p,'w').write('\n'.join(ls))
print("token inserted; row now carries rea-agents@6.7.0")
PY
python3 "$R"/.ufo/gates/c1-census-v10.py --root $CT --quiet; echo "exit=$?"
retry cp "$R/SKILL.md" $CT/SKILL.md
echo
echo "== records-append variant (a): realistic token-free records block =="
cat >> $CT/SCORECARD.md <<'EOF'

## arc3-loop1-round1 records (sim, token-free shape)
- C1: solc install receipt; real-bytecode selectors recovered; map token landed.
- C2: citation-drift guard landed; probe findings=0 at HEAD; selftest 13/13.
- C3: census v10 PASS 0/0/0/0 at the records commit (E22 dispositioned by measurement).
EOF
python3 "$R"/.ufo/gates/c1-census-v10.py --root $CT --quiet; echo "exit=$?"
echo
echo "== records-append variant (b): ONE pin-bearing records line added =="
cat >> $CT/SCORECARD.md <<'EOF'
- C1: pin re-checked against rea-agents@6.5.0 (devin/omp) at the records commit.
EOF
python3 "$R"/.ufo/gates/c1-census-v10.py --root $CT --quiet 2>&1 | tail -6; echo "exit=${PIPESTATUS[0]}"
} > "$D"/05-census-mirror.txt 2>&1

echo "transcripts written to $D"
ls -la "$D"
