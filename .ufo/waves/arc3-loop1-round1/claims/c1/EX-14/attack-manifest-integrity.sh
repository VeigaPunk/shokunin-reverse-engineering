#!/usr/bin/env bash
# attack-manifest-integrity.sh — SEAT EX-14 falsification harness for MANIFEST.draft
# usage: bash .ufo/waves/arc3-loop1-round1/claims/c1/EX-14/attack-manifest-integrity.sh  (from repo root)
#
# Attacks the manifest's integrity claim: "the check-file reproduces the tree".
# Method: copy the whole wave dir to scratch, REGENERATE the manifest+check-file there
# (clean baseline, immune to concurrent seats), then inject faults and read the detector.
# Scratch lives under /dev/shm/ex14 (tmpfs). NOTE: /tmp is quota-exhausted on this host
# (tmpfs usrquota; dd to /tmp fails EDQUOT 2026-10-19) — /dev/shm is the working tmpfs.
# Order matters: count checks (A5) run BEFORE fault injection (A2/A3 delete files).
set -u
WAVE=".ufo/waves/arc3-loop1-round1"
CHK_REL="claims/c1/EX-14/MANIFEST.draft.check.sha256"
SCRATCH="/dev/shm/ex14attack"
rm -rf "$SCRATCH"; mkdir -p "$SCRATCH/.ufo/waves"
trap 'rm -rf "$SCRATCH"' EXIT

echo "=== A0: clean baseline regenerated inside scratch ==="
cp -r "$WAVE" "$SCRATCH/.ufo/waves/"
( cd "$SCRATCH" && bash "$WAVE/claims/c1/EX-14/manifest-gen.sh" >/dev/null 2>&1 )
( cd "$SCRATCH" && cd "$WAVE" && sha256sum -c "$CHK_REL" >/dev/null 2>&1 ); echo "scratch baseline replay exit=$? (expect 0)"

echo "=== A1: live-tree replay (as the consumer runs it; tree is moving during the wave) ==="
( cd "$WAVE" && sha256sum -c "$CHK_REL" >/dev/null 2>&1 ); echo "live replay exit=$? (0 = manifest current; 1 = seats wrote since generation)"

echo "=== A4: self-reference guard (derived outputs must not be listed) ==="
SELFHITS=$(grep -c -E 'MANIFEST\.draft\.(txt|check\.sha256)|verify\.log' "$SCRATCH/$WAVE/$CHK_REL" || true)
echo "check-file entries naming derived outputs: $SELFHITS (expect 0)"

echo "=== A5: independent entry count (disk == check-file; manifest = check + 1 custody row) ==="
DISK=$(find "$SCRATCH/$WAVE/claims/c1" -type f ! -name 'MANIFEST.draft.txt' ! -name 'MANIFEST.draft.check.sha256' ! -name 'verify.log' ! -path '*/_scratch/*' ! -path '*/__pycache__/*' | wc -l)
CHK=$(grep -c -E '^[0-9a-f]{64}  ' "$SCRATCH/$WAVE/$CHK_REL")
MFT=$(grep -c -E '^[0-9a-f]{64}  ' "$SCRATCH/$WAVE/claims/c1/receipts/MANIFEST.draft.txt")
echo "disk=$DISK check-file=$CHK manifest=$MFT (expect disk=check, manifest=check+1)"

echo "=== A8: independent re-hash of a 5-entry sample (openssl dgst, not sha256sum) ==="
if command -v openssl >/dev/null 2>&1; then
  grep -E '^[0-9a-f]{64}  ' "$SCRATCH/$WAVE/$CHK_REL" | awk 'NR%20==1' | head -5 | while read -r h p; do
    got=$(openssl dgst -sha256 -r "$SCRATCH/$WAVE/$p" 2>/dev/null | awk '{print $1}')
    if [ "$got" = "$h" ]; then echo "OK   $p"; else echo "DIFF $p manifest=$h openssl=$got"; fi
  done
else echo "openssl absent — skipped"; fi

echo "=== A6: custody lines in manifest == pre-pair compact list ==="
PRE=$(grep -E '^[0-9a-f]{64}  /' "$SCRATCH/$WAVE/claims/cross/receipts/config-pre-pair.txt" | tail -5)
LIVE=$(sed -n '/^## section 2/,/^## section 3/p' "$SCRATCH/$WAVE/claims/c1/receipts/MANIFEST.draft.txt" | grep -E '^  live: ' | sed 's/^  live: //')
if [ "$PRE" = "$LIVE" ]; then echo "custody: IDENTICAL (5/5)"; else echo "custody: DIFF"; diff <(printf '%s\n' "$PRE") <(printf '%s\n' "$LIVE") || true; fi

echo "=== A2: tampered-file detection (exactly one injected fault) ==="
VICTIM=$(grep -m1 -E '^[0-9a-f]{64}  claims/c1/EX-11/' "$SCRATCH/$WAVE/$CHK_REL" | awk '{print $2}')
printf 'TAMPER' >> "$SCRATCH/$WAVE/$VICTIM"
A2=$( cd "$SCRATCH/$WAVE" && sha256sum -c "$CHK_REL" 2>&1 | grep -v ': OK$' )
echo "victim=$VICTIM"; echo "non-OK lines:"; printf '%s\n' "$A2"

echo "=== A3: absent-file detection (same victim, deleted) ==="
rm -f "$SCRATCH/$WAVE/$VICTIM"
A3=$( cd "$SCRATCH/$WAVE" && sha256sum -c "$CHK_REL" 2>&1 | grep -v ': OK$' )
echo "non-OK lines:"; printf '%s\n' "$A3"

echo "=== A7: live manifest sha256 (record in seat report) ==="
sha256sum "$WAVE/claims/c1/receipts/MANIFEST.draft.txt"
