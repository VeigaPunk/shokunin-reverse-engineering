#!/usr/bin/env bash
# R38ReviewerPredicateIdentity — C2 falsifiers (v2, line-scoped edits).
# Fixture repos from the REAL lane bytes at base 77091b49; shadow-row /
# decoy-document variants against the frozen c2-counter (working tree == freeze).
# A variant that exits 0 meets the frozen target while violating a P38-C2 sentence.
set -euo pipefail
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r38/R38ReviewerPredicateIdentity
D="$S/fx-c2"
ART="$LANE/.ufo/waves/round-38/w1/artifacts/R38ReviewerPredicateIdentity"
BASE=77091b492cc53f8743bd0701b1e7d5e66123dd84
mkdir -p "$ART"
rm -rf "$D"; mkdir -p "$D"
git -C "$D" init -q
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$(realpath "$TOP")" = "$(realpath "$D")" ] || { echo "toplevel mismatch" >&2; exit 2; }
git -C "$LANE" archive "$BASE" | tar -x -C "$D"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git -C "$D" add -A && git -C "$D" commit -qm 'base snapshot: real lane bytes at 77091b49'
BASEREV=$(git -C "$D" rev-parse HEAD)
echo "fixture base snapshot: $BASEREV"

run() {
  label=$1
  set +e
  python3 -I -B "$LANE/tools/round-38/c2-counter.py" --root "$D" --rev "$(git -C "$D" rev-parse HEAD)" --base "$BASEREV" \
    --json-out "$ART/c2-decoy-$label.json" > "$ART/c2-decoy-$label.stdout" 2>&1
  rc=$?
  set -e
  echo "decoy-$label counter-exit=$rc"
}

# ---- sanity: do-nothing on the base snapshot must reproduce the base mismatch (exit 1)
run base-sanity

# ---- decoy A: duplicate 'REA MCP server' row appended in ## Core; the later
# duplicate shadows the original unresolved-pointer row (units dict: last wins).
git -C "$D" checkout -q -b decoyA "$BASEREV"
python3 -c "
p='$D/PROVINCE.md'
lines=open(p).read().splitlines()
i=[n for n,l in enumerate(lines) if 'REA MCP server' in l and l.lstrip().startswith('|')][0]
orig=lines[i]
dup=orig.replace('\`evidence/doctor/\`','\`.ufo/waves/round-19/evidence/doctor/\`')
lines.insert(i+1,dup)
open(p,'w').write('\n'.join(lines)+'\n')
print('original:',orig[:80]); print('dup     :',dup[:80])
"
git -C "$D" add -A && git -C "$D" commit -qm 'decoyA: duplicate REA MCP server row, resolving pointer'
run A

# ---- decoy B: the bad pointer is repaired by a DIFFERENT document
# (corpus/evidence/doctor/) that merely ends with the same suffix.
git -C "$D" checkout -q -b decoyB "$BASEREV"
python3 -c "
import os
p='$D/PROVINCE.md'
lines=open(p).read().splitlines()
i=[n for n,l in enumerate(lines) if 'REA MCP server' in l and l.lstrip().startswith('|')][0]
lines[i]=lines[i].replace('\`evidence/doctor/\`','\`corpus/evidence/doctor/\`')
open(p,'w').write('\n'.join(lines)+'\n')
os.makedirs('$D/corpus/evidence/doctor',exist_ok=True)
open('$D/corpus/evidence/doctor/doctor-note.txt','w').write('decoy document, not the intended round-19 doctor tree\n')
"
git -C "$D" add -A && git -C "$D" commit -qm 'decoyB: repair redirected to decoy document corpus/evidence/doctor'
run B

# ---- decoy C: proper repair + a SECOND '## Owned axes' section in SCORECARD
# whose coverage row states a junk count; units() reads only the first heading.
git -C "$D" checkout -q -b decoyC "$BASEREV"
python3 -c "
p='$D/PROVINCE.md'
lines=open(p).read().splitlines()
i=[n for n,l in enumerate(lines) if 'REA MCP server' in l and l.lstrip().startswith('|')][0]
lines[i]=lines[i].replace('\`evidence/doctor/\`','\`.ufo/waves/round-19/evidence/doctor/\`')
open(p,'w').write('\n'.join(lines)+'\n')
s='$D/SCORECARD.md'
t=open(s).read()
t += ('\n## Owned axes\n\n| Axis | Baseline → current score, 0–10 | Observable and limitation | Evidence / counting command | Last-change round |\n'
      '|---|---|---|---|---|\n| coverage | 10 | 999/999 knowledge files mapped | \`corpus/README.md\` | r |\n')
open(s,'w').write(t)
"
git -C "$D" add -A && git -C "$D" commit -qm 'decoyC: shadow Owned-axes section with junk count'
run C

# ---- decoy D: proper repair + a SECOND contradictory count inside the SAME
# coverage row (stated() is re.search: only the first match is checked).
git -C "$D" checkout -q -b decoyD "$BASEREV"
python3 -c "
p='$D/PROVINCE.md'
lines=open(p).read().splitlines()
i=[n for n,l in enumerate(lines) if 'REA MCP server' in l and l.lstrip().startswith('|')][0]
lines[i]=lines[i].replace('\`evidence/doctor/\`','\`.ufo/waves/round-19/evidence/doctor/\`')
open(p,'w').write('\n'.join(lines)+'\n')
s='$D/SCORECARD.md'
lines=open(s).read().splitlines()
j=[n for n,l in enumerate(lines) if l.startswith('| coverage |')][0]
lines[j]=lines[j]+' 999/999 knowledge files mapped'
open(s,'w').write('\n'.join(lines)+'\n')
print('coverage row tail:',lines[j][-100:])
"
git -C "$D" add -A && git -C "$D" commit -qm 'decoyD: second contradictory count inside the coverage row'
run D
echo "fixture repo left at $D"
