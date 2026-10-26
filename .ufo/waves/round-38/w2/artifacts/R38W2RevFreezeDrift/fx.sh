#!/bin/bash
# Fixture for freeze-drift.py semantics review (R38W2RevFreezeDrift). Scratch-only.
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2RevFreezeDrift
D=$(mktemp -d "$S/fx.XXXX")
export GIT_AUTHOR_NAME=fx GIT_AUTHOR_EMAIL=fx@fx GIT_COMMITTER_NAME=fx GIT_COMMITTER_EMAIL=fx@fx
git -C "$D" init -q
T=$(git -C "$D" rev-parse --show-toplevel)
[ "$T" = "$D" ] || { echo "TOPLEVEL-MISMATCH $T != $D"; exit 9; }
echo "fixture=$D"
BR=$(git -C "$D" symbolic-ref --short HEAD); echo "branch=$BR git=$(git --version)"

mk() { mkdir -p "$D/$(dirname "$1")"; printf '%s\n' "$2" > "$D/$1"; }
mk plans/claims.md 'frozen-rule-v1'
mk tools/c1.py 'counter-v1'
mk corpus/evidence/round-37/c1/K1/oracle.tsv 'k1'
mk corpus/evidence/round-37/c1/K2/oracle.tsv 'k2'
mk corpus/evidence/round-37/c1/X/Y/oracle.tsv 'deep'
mk corpus/evidence/round-37/c1/K1/oracle.tsv.bak 'bak'
git -C "$D" add -A && git -C "$D" commit -qm base
BASE=$(git -C "$D" rev-parse HEAD)

# A: drift on claims doc (amendment survives)
printf 'amended-rule\n' > "$D/plans/claims.md"; git -C "$D" commit -qam amend-claims
# B: rename counter (old frozen path must stay visible)
git -C "$D" mv tools/c1.py tools/c2.py; git -C "$D" commit -qm rename-counter
# C: side branch tampers K1 oracle; merged -s ours so the tamper does NOT survive
git -C "$D" checkout -qb side
printf 'tampered\n' > "$D/corpus/evidence/round-37/c1/K1/oracle.tsv"; git -C "$D" commit -qam side-touch-oracle
git -C "$D" checkout -q "$BR"
git -C "$D" merge -q --no-ff -s ours -m merge-ours side
# D: deep oracle edit on main (survives) — answers whether * crosses /
printf 'deep-new\n' > "$D/corpus/evidence/round-37/c1/X/Y/oracle.tsv"; git -C "$D" commit -qam main-deep-edit
# E: conflicting claims-doc edits resolved to a third content (merge differs from both parents)
git -C "$D" checkout -qb b2 "$BASE"
printf 'b2-new\n' > "$D/plans/claims.md"; git -C "$D" commit -qam b2-edit
git -C "$D" checkout -q "$BR"
printf 'main-new\n' > "$D/plans/claims.md"; git -C "$D" commit -qam main-edit
if ! git -C "$D" merge --no-ff --no-edit -m merge-resolve b2 >/dev/null 2>&1; then
  printf 'merge-resolved\n' > "$D/plans/claims.md"
  git -C "$D" add plans/claims.md; git -C "$D" commit -qm merge-resolve
fi
HEADREV=$(git -C "$D" rev-parse HEAD)
echo "BASE=$BASE HEADREV=$HEADREV"
echo "--- full log graph:"; git -C "$D" log --oneline --graph --all | sed 's/^/  /'

TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
run() { # name, then tool args after the fixed ones
  local n=$1; shift
  python3 "$TOOL" --root "$D" --freeze "$BASE" --rev "$HEADREV" --json-out "$S/fx-$n.json" "$@" >"$S/fx-$n.stdout" 2>"$S/fx-$n.stderr"
  echo "case[$n] exit=$?"
}

echo "=== T1 claims doc exact";      run t1 'plans/claims.md'
echo "=== T2 oracle glob K*";        run t2 'corpus/evidence/round-37/c1/*/oracle.tsv'
echo "=== T3 old renamed path";      run t3 'tools/c1.py'
echo "=== T4 bad magic (:(icase))";  run t4 ':(icase)plans/claims.md'
echo "=== T5 nonexistent path";      run t5 'does/not/exist.tsv'
echo "=== T6 any *.tsv (cross /?)";  run t6 '*.tsv'
echo "=== T7 unknown rev";  python3 "$TOOL" --root "$D" --freeze "$BASE" --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef >/dev/null 2>&1; echo "case[t7] exit=$?"
echo "=== T8 freeze not ancestor";  python3 "$TOOL" --root "$D" --freeze "$HEADREV" --rev "$BASE" >/dev/null 2>&1; echo "case[t8] exit=$?"
echo "=== T9 bad root";     python3 "$TOOL" --root "$S/definitely-missing" --freeze "$BASE" --rev "$HEADREV" >/dev/null 2>&1; echo "case[t9] exit=$?"

echo "=== R1 raw git log WITHOUT --no-renames (diff.renames default) for tools/c1.py"
git -C "$D" log --format=%H --name-only "$BASE..$HEADREV" -- tools/c1.py | sed 's/^/  |/'
echo "=== R2 raw git log WITH -M explicitly for tools/c1.py"
git -C "$D" log -M --format=%H --name-only "$BASE..$HEADREV" -- tools/c1.py | sed 's/^/  |/'
echo "=== R3 raw git log --name-only for the merge-resolve commit (path list for a merge?)"
MRG=$(git -C "$D" log --format=%H --grep=merge-resolve -1); git -C "$D" show --name-only --format='COMMIT %h %s' "$MRG" | sed 's/^/  |/'
echo "=== R4 plain (no magic) pathspec for comparison: corpus/evidence/round-37/c1/*/oracle.tsv"
git -C "$D" log --format=%h --name-only "$BASE..$HEADREV" -- 'corpus/evidence/round-37/c1/*/oracle.tsv' | sed 's/^/  |/'
echo "=== R5 which files differ freeze..HEADREV (full name-status)"
git -C "$D" diff --name-status "$BASE" "$HEADREV" | sed 's/^/  |/'
echo "=== jsonout==stdout checks"
for f in t1 t2 t3 t4 t5 t6; do
  if diff -q <(cat "$S/fx-$f.json") <(sed -e '$a\' "$S/fx-$f.stdout") >/dev/null 2>&1; then echo "  fx-$f: json==stdout"; else echo "  fx-$f: DIFFERS (stdout may have trailing newline only)"; fi
  python3 -c "import json,sys; json.load(open('$S/fx-$f.json'))" && echo "  fx-$f.json: valid JSON"
done
echo "FIXTURE-REMAINING=$D (cleaned by caller trap)"
