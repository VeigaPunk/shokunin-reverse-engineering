#!/bin/sh
# C1FreezeWindow probe 4: does the claims file's own freeze DERIVATION
# (`git log --format=%H -1 -- plans/round-47-claims.md`) keep the window honest when the
# tamper edits the claims file itself? Fixture: freeze c1 -> tip c2 edits BOTH a frozen
# tool and the claims file.
set -u
S=/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow
export TMPDIR="$S" HYAKU_SCRATCH="$S"
cd "$S" || exit 9
D="$S/merge-fx4"
rm -rf "$D"
mkdir -p "$D" || exit 9
git -C "$D" init -q || exit 9
git -C "$D" config user.email fx@round47.local
git -C "$D" config user.name "round47 fixture"
TOP=$(git -C "$D" rev-parse --show-toplevel) || exit 9
if [ "$TOP" != "$D" ]; then echo "TOPLEVEL_MISMATCH got=$TOP want=$D"; exit 9; fi

mkdir -p "$D/tools/round-47" "$D/plans"
printf 'INTERPRETER-BYTES-A\n' > "$D/tools/round-47/exact.py"
cat > "$D/plans/round-47-claims.md" <<'EOF'
# fixture claims

## Frozen paths (exact)

- `plans/round-47-claims.md`
- `tools/round-47/`
EOF
printf 'graded\n' > "$D/SKILL.md"
git -C "$D" add -A && git -C "$D" commit -q -m c1
F=$(git -C "$D" rev-parse HEAD)

# the tamper: rewrite the frozen tool AND the claims file in the same commit
printf 'INTERPRETER-BYTES-B-TAMPERED\n' > "$D/tools/round-47/exact.py"
printf '\n- appended by the tamper\n' >> "$D/plans/round-47-claims.md"
git -C "$D" add -A && git -C "$D" commit -q -m c2
T=$(git -C "$D" rev-parse HEAD)

echo "PINNED_FREEZE=$F"; echo "TIP=$T"
echo "derived-freeze(git log -1 -- plans/round-47-claims.md)=$(git -C "$D" log --format=%H -1 -- plans/round-47-claims.md)"
DERIVED=$(git -C "$D" log --format=%H -1 -- plans/round-47-claims.md)
echo "-- window \$DERIVED..\$TIP -- frozen paths:"
git -C "$D" log --name-status --format= -m --diff-merges=first-parent "$DERIVED..$T" -- tools/round-47 plans/round-47-claims.md | sed 's/^/   /'
echo "   bytes=$(git -C "$D" log --name-status --format= -m --diff-merges=first-parent "$DERIVED..$T" -- tools/round-47 plans/round-47-claims.md | wc -c)"
echo "-- window \$PINNED..\$TIP -- frozen paths:"
git -C "$D" log --name-status --format= -m --diff-merges=first-parent "$F..$T" -- tools/round-47 plans/round-47-claims.md | sed 's/^/   /'
echo "exact.py@PINNED=$(git -C "$D" rev-parse "$F:tools/round-47/exact.py") exact.py@TIP=$(git -C "$D" rev-parse "$T:tools/round-47/exact.py")"
echo "$D" > "$S/fx4-dir.txt"; echo "$F" > "$S/fx4-pinned.txt"; echo "$T" > "$S/fx4-tip.txt"; echo "$DERIVED" > "$S/fx4-derived.txt"
echo "UTC=$(date -u +%FT%TZ)"
