#!/usr/bin/env bash
# VZ-4 independent verification of EX-01's rule-#14 patch text (chain c1).
# Applies the payload to a scratch SKILL.md copy per the patch's anchor form and
# re-derives every identity the patch claims. Nothing in the repo is modified.
set -u
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
PATCH="$R/.ufo/waves/arc3-loop1-round2/claims/c1/EX-01/rule14.patch.md"
W=/var/tmp/vz4/c1; rm -rf "$W"; mkdir -p "$W"
cp "$R/PROVINCE.md" "$R/SCORECARD.md" "$W/"
echo "utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "patch_sha256=$(sha256sum "$PATCH" | cut -d' ' -f1)"
echo "pre_SKILL_lines=$(wc -l < "$R/SKILL.md")  pre_SKILL_sha=$(sha256sum "$R/SKILL.md" | cut -d' ' -f1)"
echo
echo "=== 1. payload identity (markers stripped, no leading/trailing blank) ==="
python3 - "$PATCH" "$W/SKILL.md" <<'PY'
import hashlib, pathlib, sys
text = pathlib.Path(sys.argv[1]).read_text()
body = text.split("<!-- payload-begin -->\n", 1)[1].split("<!-- payload-end -->", 1)[0]
assert body.endswith("\n")
payload = body                          # trailing newline INCLUDED (the patch's own unit)
print("payload_bytes=%d payload_sha256=%s" % (len(payload.encode()), hashlib.sha256(payload.encode()).hexdigest()))
print("claimed_bytes=1071 claimed_sha256=6cc388cb61a3023e8e62a0f63c0ff2e275665706373b184ad7d4801c3c91718f")
src = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md").read_text()
anchor = "  kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).\n"
print("anchor_occurrences=%d" % src.count(anchor))
assert src.count(anchor) == 1, "anchor must be unique"
patched = src.replace(anchor, anchor + payload + "\n", 1)
out = pathlib.Path(sys.argv[2]); out.write_text(patched)
print("patched_lines=%d patched_sha256=%s" % (len(patched.splitlines()),
      hashlib.sha256(patched.encode()).hexdigest()))
print("claimed_lines=385 claimed_sha256=19057c131038352ba1bee1aec007401de774cc88a9ef42cde2cc09dcbe6f4e90")
PY
echo
echo "=== 2. prior-rule bytes unchanged (lines 1-239 cmp) ==="
head -239 "$R/SKILL.md" > "$W/pre-239.txt"; head -239 "$W/SKILL.md" > "$W/post-239.txt"
if cmp -s "$W/pre-239.txt" "$W/post-239.txt"; then echo "lines 1-239: BYTE-IDENTICAL"; else echo "lines 1-239: DIFFER"; diff "$W/pre-239.txt" "$W/post-239.txt" | head -5; fi
echo
echo "=== 3. rule census: pre vs post (my c1-rulecheck) ==="
mkdir -p "$W/corpus"; cp -r "$R/corpus/knowledge" "$W/corpus/" 2>/dev/null
python3 "$R/.ufo/waves/arc3-loop1-round2/claims/cross/VZ-4/c1-rulecheck.py" "tree:$R" 2>/dev/null | head -1
python3 "$R/.ufo/waves/arc3-loop1-round2/claims/cross/VZ-4/c1-rulecheck.py" "tree:$W" 2>/dev/null | head -1
echo
echo "=== 4. census (landed v11) over patched scratch root ==="
python3 "$R/.ufo/gates/c1-census-v10.py" --root "$W" --quiet 2>&1 | grep -E "SKILL.md |G2 |VERDICT"
echo
echo "=== 5. same census over unpatched repo root (control) ==="
python3 "$R/.ufo/gates/c1-census-v10.py" --root "$R" --quiet 2>&1 | grep -E "SKILL.md |G2 |VERDICT"
