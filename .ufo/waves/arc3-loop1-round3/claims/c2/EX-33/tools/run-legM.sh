#!/usr/bin/env bash
# EX-33 leg M (mechanism) + A1/A2/A3 attacks — scratch only, never a custody path.
set -u
S=/var/tmp/ex33-selfpin
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
OLD=112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
TOOL=$R/.ufo/gates/custody-pair/custody-pair.py
mkdir -p "$S/m" "$S/out" "$S/sym"

exec > >(tee "$S/out/legM.log") 2>&1

echo "=== EX-33 legM run $(date -u +%FT%TZ) ==="
echo "canonical tool sha (independent): $(sha256sum "$TOOL" | cut -d' ' -f1)"

# ---- M0: canonical capture with the as-landed tool (the BEFORE state) ----
python3 "$TOOL" capture --out "$S/out/canon-pre.receipt" --label EX33-canon-pre
echo "M0 canon-pre exit=$?"
head -5 "$S/out/canon-pre.receipt"
python3 "$S/selfpin-audit.py" --tool "$TOOL" --receipt "$S/out/canon-pre.receipt" --label M0-canon-pre
echo "M0 audit exit=$?"

# ---- M1: scratch copy of the as-landed tool, capture ----
cp "$TOOL" "$S/m/tool.py"
printf 'selfpin fixture\n' > "$S/m/fixture.conf"
sha256sum "$S/m/tool.py" | tee "$S/out/m1-tool-pre.sha256"
echo "-- capture with the unrevised copy --"
python3 "$S/m/tool.py" capture --out "$S/out/m1.receipt" --paths "$S/m/fixture.conf" --label M1-unrevised-copy
echo "M1 capture exit=$?"
python3 "$S/selfpin-audit.py" --tool "$S/m/tool.py" --receipt "$S/out/m1.receipt" --label M1-unrevised-copy
echo "M1 audit exit=$?"

# ---- M2: simulate the revision on the copy, capture again ----
printf '\n# M2 simulated revision (appended comment changes the bytes)\n' >> "$S/m/tool.py"
sha256sum "$S/m/tool.py" | tee "$S/out/m2-tool-post.sha256"
python3 "$S/m/tool.py" capture --out "$S/out/m2.receipt" --paths "$S/m/fixture.conf" --label M2-revised-copy
echo "M2 capture exit=$?"
python3 "$S/selfpin-audit.py" --tool "$S/m/tool.py" --receipt "$S/out/m2.receipt" --expect-not "$OLD" --label M2-revised-copy
echo "M2 audit exit=$?"
echo "-- the two receipts' pins side by side (M1 must be old sha, M2 must be the revised sha) --"
grep -h '^# tool: ' "$S/out/m1.receipt" "$S/out/m2.receipt"

# ---- A1: executed image vs disk at render time ----
cp "$TOOL" "$S/m/a1.py"
python3 "$S/toctou-selfpin.py" "$S/m/a1.py" "$S/out/a1.receipt" "$S/m/fixture.conf"
echo "A1 driver exit=$?"

# ---- A2: copy provenance (pin names the copy, header carries basename only) ----
grep -h '^# tool: ' "$S/out/m2.receipt"
echo "A2 note: pin above is the scratch COPY's sha; the header carries no path, only the basename."

# ---- A3: symlink invocation resolves to the canonical file ----
ln -sf "$TOOL" "$S/sym/tool.py"
python3 "$S/sym/tool.py" capture --out "$S/out/a3.receipt" --paths "$S/m/fixture.conf" --label A3-symlink
echo "A3 capture exit=$?"
grep -h '^# tool: ' "$S/out/a3.receipt"
python3 "$S/selfpin-audit.py" --tool "$TOOL" --receipt "$S/out/a3.receipt" --label A3-symlink-invocation
echo "A3 audit exit=$?"

echo "=== legM done $(date -u +%FT%TZ) ==="