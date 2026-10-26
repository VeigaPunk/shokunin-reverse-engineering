#!/usr/bin/env bash
# Fixture harness for tools/round-38/freeze-drift.py (seat R38W2FreezeDriftFixtures).
# Every git call names -C "$D"; identity is set per fixture repo only.
set -u
S=/fast/scratch/hyaku/kaidoku-r38/R38W2FreezeDriftFixtures
TOOL=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/freeze-drift.py
ART=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-38/w2/artifacts/R38W2FreezeDriftFixtures
export TMPDIR="$S"

mkrepo() { # $1 = label -> echoes dir
  local D; D=$(mktemp -d "$S/fx.$1.XXXX")
  git -C "$D" init -q
  local top; top=$(git -C "$D" rev-parse --show-toplevel)
  if [ "$(realpath "$top")" != "$(realpath "$D")" ]; then echo "FATAL: toplevel $top != $D" >&2; exit 9; fi
  git -C "$D" config user.email fx@example.invalid
  git -C "$D" config user.name fx
  git -C "$D" config commit.gpgsign false
  git -C "$D" config core.autocrlf false
  mkdir -p "$D"/{plans,tools/round-38,.ufo/waves/round-38/c1,corpus/evidence/round-37/c1/K1}
  printf 'claims v1\n' > "$D/plans/round-38-claims.md"
  printf '# c1 counter\nprint(1)\n' > "$D/tools/round-38/c1-counter.py"
  printf '# c2 counter\nprint(2)\n' > "$D/tools/round-38/c2-counter.py"
  printf '{"carriers":[]}\n' > "$D/.ufo/waves/round-38/c1/carriers.json"
  printf 'id\tval\nK1\t1\n' > "$D/corpus/evidence/round-37/c1/K1/oracle.tsv"
  echo "$D"
}

run() { # $1 dir, $2 label, rest: tool args
  local D="$1" L="$2"; shift 2
  local out; out=$(python3 "$TOOL" --root "$D" "$@" 2>&1); local rc=$?
  printf '\n### %s\n$ python3 freeze-drift.py --root %s %s\nEXIT %d\n%s\n' "$L" "$D" "$*" "$rc" "$out"
  return $rc
}

log() { printf '\n===== %s =====\n' "$*"; }

# ---------------- (a) clean history ----------------
log "(a) clean history"
D=$(mkrepo a)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
printf 'unrelated\n' > "$D/plans/other.md"
mkdir -p "$D/docs"; printf 'notes\n' > "$D/docs/notes.md"
git -C "$D" add -A && git -C "$D" commit -qm "unrelated docs"
printf 'x\n' > "$D/tools/round-38/harness.sh"
git -C "$D" add -A && git -C "$D" commit -qm "unrelated tool"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(a) clean: freeze=$F rev=$R" --freeze "$F" --rev "$R"
echo "A_FREEZE=$F A_REV=$R" > "$S/fx-a.env"

# ---------------- (b) counter edited after freeze ----------------
log "(b) counter edited after freeze"
D=$(mkrepo b)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
printf '# c1 counter v2\nprint(11)\n' > "$D/tools/round-38/c1-counter.py"
git -C "$D" add -A && git -C "$D" commit -qm "amend c1 counter"
E=$(git -C "$D" rev-parse HEAD)
printf 'clean\n' > "$D/plans/clean.md"; git -C "$D" add -A && git -C "$D" commit -qm "later unrelated"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(b) counter edit: freeze=$F edit=$E rev=$R" --freeze "$F" --rev "$R"
run "$D" "(b2) json-out" --freeze "$F" --rev "$R" --json-out "$S/fx-b.json" >/dev/null
echo "--- fx-b.json ---"; cat "$S/fx-b.json"

# ---------------- (c) oracle nested dir ----------------
log "(c) oracle under nested dir (glob :(glob)corpus/evidence/round-37/c1/*/oracle.tsv)"
D=$(mkrepo c)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
printf 'id\tval\nK1\t2\n' > "$D/corpus/evidence/round-37/c1/K1/oracle.tsv"
git -C "$D" add -A && git -C "$D" commit -qm "edit oracle K1"
R1=$(git -C "$D" rev-parse HEAD)
run "$D" "(c1) K1/oracle.tsv edited: rev=$R1" --freeze "$F" --rev "$R1"
mkdir -p "$D/corpus/evidence/round-37/c1/K2/deep"
printf 'id\tval\nK2\t1\n' > "$D/corpus/evidence/round-37/c1/K2/deep/oracle.tsv"
git -C "$D" add -A && git -C "$D" commit -qm "add oracle at deeper path"
R2=$(git -C "$D" rev-parse HEAD)
run "$D" "(c2) K2/deep/oracle.tsv added (glob '*' does not cross '/'): rev=$R2" --freeze "$F" --rev "$R2"
# explicit pathspec form used by instruments.json: c1_oracles "corpus/evidence/round-37/c1/K*/oracle.tsv"
run "$D" "(c3) pathspec 'corpus/evidence/round-37/c1/K*/oracle.tsv' over same range" --freeze "$F" --rev "$R2" 'corpus/evidence/round-37/c1/K*/oracle.tsv'

# ---------------- (d) rename of counter after freeze ----------------
log "(d) rename of counter after freeze"
D=$(mkrepo d)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" mv tools/round-38/c1-counter.py tools/round-38/c1-counter-renamed.py
git -C "$D" commit -qm "rename c1 counter"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(d) rename out of frozen name: rev=$R" --freeze "$F" --rev "$R"
# rename back in, then again with content change under the new name only
printf '# renamed body edited\nprint(99)\n' >> "$D/tools/round-38/c1-counter-renamed.py"
git -C "$D" add -A && git -C "$D" commit -qm "edit renamed counter body"
R2=$(git -C "$D" rev-parse HEAD)
run "$D" "(d2) after rename, edited under new name: rev=$R2" --freeze "$F" --rev "$R2"
# rename INTO a frozen path from elsewhere
D2=$(mkrepo d2)
git -C "$D2" add -A && git -C "$D2" commit -qm "freeze"
F2=$(git -C "$D2" rev-parse HEAD)
printf 'evil\n' > "$D2/plans/evil.md"; git -C "$D2" add -A && git -C "$D2" commit -qm "add evil"
git -C "$D2" mv plans/evil.md tools/round-38/c1-counter.py
git -C "$D2" commit -qm "rename evil onto frozen counter path"
R3=$(git -C "$D2" rev-parse HEAD)
run "$D2" "(d3) rename INTO frozen path: rev=$R3" --freeze "$F2" --rev "$R3"

# ---------------- (e) merge commit touching claims doc ----------------
log "(e) merge commits"
D=$(mkrepo e)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
git -C "$D" checkout -q -b side
printf 'claims side\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "side edits claims"
git -C "$D" checkout -q master 2>/dev/null || git -C "$D" checkout -q main
printf 'claims main\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "main edits claims"
git -C "$D" merge -q side >/dev/null 2>&1
printf 'claims merge resolution\n' > "$D/plans/round-38-claims.md"
git -C "$D" add -A && git -C "$D" commit -qm "merge side (claims resolved)"
M=$(git -C "$D" rev-parse HEAD)
echo "MERGE_HEAD_COUNT=$(git -C "$D" rev-list --parents -n1 "$M" | wc -w)"
run "$D" "(e1) conflict-resolution merge edits claims: rev=$M" --freeze "$F" --rev "$M"
# evil merge: no conflict, change introduced only in merge commit
D3=$(mkrepo e3)
git -C "$D3" add -A && git -C "$D3" commit -qm "freeze"
F3=$(git -C "$D3" rev-parse HEAD)
git -C "$D3" checkout -q -b side
printf 'side doc\n' > "$D3/plans/side.md"
git -C "$D3" add -A && git -C "$D3" commit -qm "side adds doc"
git -C "$D3" checkout -q master 2>/dev/null || git -C "$D3" checkout -q main
printf 'main doc\n' > "$D3/plans/main.md"
git -C "$D3" add -A && git -C "$D3" commit -qm "main adds doc"
git -C "$D3" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
printf 'claims changed in merge only\n' > "$D3/plans/round-38-claims.md"
git -C "$D3" add -A && git -C "$D3" commit -q --amend --no-edit
M3=$(git -C "$D3" rev-parse HEAD)
echo "EVIL_MERGE_PARENTS=$(git -C "$D3" rev-list --parents -n1 "$M3")"
run "$D3" "(e2) evil merge edits claims in merge commit: rev=$M3" --freeze "$F3" --rev "$M3"
# plain merge that merely introduces side's claims edit (no merge-commit-only change)
D4=$(mkrepo e4)
git -C "$D4" add -A && git -C "$D4" commit -qm "freeze"
F4=$(git -C "$D4" rev-parse HEAD)
git -C "$D4" checkout -q -b side
printf 'claims side\n' > "$D4/plans/round-38-claims.md"
git -C "$D4" add -A && git -C "$D4" commit -qm "side edits claims"
git -C "$D4" checkout -q master 2>/dev/null || git -C "$D4" checkout -q main
printf 'main doc\n' > "$D4/plans/main.md"
git -C "$D4" add -A && git -C "$D4" commit -qm "main adds doc"
git -C "$D4" merge -q --no-ff side -m "merge side" >/dev/null 2>&1
M4=$(git -C "$D4" rev-parse HEAD)
run "$D4" "(e3) plain merge introducing claims edit: rev=$M4" --freeze "$F4" --rev "$M4"

# ---------------- (f) freeze not an ancestor / unknown revision ----------------
log "(f) unevaluable cases"
D=$(mkrepo f)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
printf 'other\n' > "$D/plans/other.md"; git -C "$D" add -A && git -C "$D" commit -qm "second"
# rewrite history so F is no longer an ancestor: new root
git -C "$D" checkout -q --orphan rewritten
git -C "$D" rm -rq --cached . >/dev/null 2>&1
git -C "$D" add -A && git -C "$D" commit -qm "orphan root"
O=$(git -C "$D" rev-parse HEAD)
run "$D" "(f1) freeze=$F not ancestor of orphan=$O" --freeze "$F" --rev "$O"
run "$D" "(f2) unknown freeze revision" --freeze deadbeefdeadbeefdeadbeefdeadbeefdeadbeef --rev "$O"
run "$D" "(f3) unknown rev" --freeze "$O" --rev 0123456789012345678901234567890123456789
run "$D" "(f4) freeze==rev (empty range)" --freeze "$O" --rev "$O"

# ---------------- (g) extra probes: whitespace paths, non-default set, missing path ----------------
log "(g) extra probes"
D=$(mkrepo g)
git -C "$D" add -A && git -C "$D" commit -qm "freeze"
F=$(git -C "$D" rev-parse HEAD)
mkdir -p "$D/corpus/evidence/round-37/c1/K 9"
printf 'id\nK9\n' > "$D/corpus/evidence/round-37/c1/K 9/oracle.tsv"
git -C "$D" add -A && git -C "$D" commit -qm "oracle under space dir"
R=$(git -C "$D" rev-parse HEAD)
run "$D" "(g1) oracle dir with a space: rev=$R" --freeze "$F" --rev "$R"
printf 'new\n' > "$D/plans/brand-new.md"; git -C "$D" add -A && git -C "$D" commit -qm "brand new path"
R2=$(git -C "$D" rev-parse HEAD)
run "$D" "(g2) path absent at freeze, created later, default set" --freeze "$F" --rev "$R2"
run "$D" "(g3) explicit path that never existed" --freeze "$F" --rev "$R2" 'plans/does-not-exist.md'
echo DONE_ALL
