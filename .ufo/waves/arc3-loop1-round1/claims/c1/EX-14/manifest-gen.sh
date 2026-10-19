#!/usr/bin/env bash
# manifest-gen.sh — SEAT EX-14 (chain c1, executor) receipt manifest generator
# wave: arc3-loop1-round1   repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# usage: bash .ufo/waves/arc3-loop1-round1/claims/c1/EX-14/manifest-gen.sh   (from repo root)
#
# Emits:
#   claims/c1/receipts/MANIFEST.draft.txt            (the draft manifest)
#   claims/c1/EX-14/MANIFEST.draft.check.sha256      (sha256sum -c compatible, paths rel. wave root)
#   claims/c1/EX-14/verify.log                       (self-verification output, appended per run)
#
# Scope: every file under claims/c1/ (recursive) + the custody pre-pair artifact.
# Excluded from listing (derived outputs, cannot self-hash): MANIFEST.draft.txt,
# MANIFEST.draft.check.sha256, verify.log; their hashes are recorded in the footer.
# NOTE: intentionally uses no temp files — /tmp is quota-exhausted on this host
# (tmpfs usrquota; dd to /tmp fails EDQUOT as of 2026-10-19T10:0xZ).
set -u
WAVE=".ufo/waves/arc3-loop1-round1"
OUT="$WAVE/claims/c1/receipts/MANIFEST.draft.txt"
CHK="$WAVE/claims/c1/EX-14/MANIFEST.draft.check.sha256"
CHK_REL="claims/c1/EX-14/MANIFEST.draft.check.sha256"   # wave-relative (sha256sum -c from WAVE)
LOG="$WAVE/claims/c1/EX-14/verify.log"
CUSTODY_PRE="$WAVE/claims/cross/receipts/config-pre-pair.txt"
GEN_REPO="$WAVE/claims/c1/EX-14/manifest-gen.sh"        # repo-relative (hash from repo root)
GEN_WAVE="claims/c1/EX-14/manifest-gen.sh"              # wave-relative (display)
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
HEAD=$(git rev-parse HEAD 2>/dev/null || echo "n/a (not a git work tree)")

utc() { date -u -d "@$1" +%Y-%m-%dT%H:%M:%SZ; }
hash_file() { sha256sum "$1" | cut -d' ' -f1; }

C1_ROSTER="PL-1 EX-01 EX-02 EX-03 EX-04 EX-05 EX-06 EX-07 EX-08 EX-09 EX-10 EX-11 EX-12 EX-13 EX-14 EX-15 SC-1 SC-2 SC-3 RV-1 RV-2 RV-3 RV-4 CR-1 CR-2 VZ-1"

mkdir -p "$(dirname "$OUT")" "$(dirname "$CHK")"

# ---- scan (no temp files) --------------------------------------------------
INCLUDE_SCRATCH=${INCLUDE_SCRATCH:-0}   # 1 = also list seat-local _scratch/ trees
ROWS=""; CHK_BODY=""; N=0; BYTES=0; VANISHED=0
scan() {
  ROWS=""; CHK_BODY=""; N=0; BYTES=0; VANISHED=0
  local f h s m rel
  local scratch_excl=()
  [ "$INCLUDE_SCRATCH" = "1" ] || scratch_excl=( ! -path '*/_scratch/*' ! -path '*/__pycache__/*' )
  while IFS= read -r f; do
    if [ ! -e "$f" ]; then ROWS+="VANISHED-DURING-SCAN  $f"$'\n'; VANISHED=$((VANISHED+1)); continue; fi
    h=$(hash_file "$f"); s=$(stat -c %s "$f"); m=$(utc "$(stat -c %Y "$f")"); c=$(utc "$(stat -c %Z "$f")"); rel="${f#"$WAVE"/}"
    ROWS+=$(printf '%s  %s  %s  %s  %s' "$h" "$s" "$m" "$c" "$rel")$'\n'
    CHK_BODY+=$(printf '%s  %s' "$h" "$rel")$'\n'
    N=$((N+1)); BYTES=$((BYTES+s))
  done < <(find "$WAVE/claims/c1" -type f \
             ! -name 'MANIFEST.draft.txt' \
             ! -name 'MANIFEST.draft.check.sha256' \
             ! -name 'verify.log' \
             ! -name '*.tmp' ! -name '*.swp' ! -name '*.part' \
             "${scratch_excl[@]}" \
           | LC_ALL=C sort)
}
# transient churn stats (always computed, even when excluded from listing):
# _scratch/ per wave rules (relocated from /tmp, which is quota-exhausted) and
# __pycache__/ (bytecode churn; excluded per SC-2's crosscheck finding).
SCRATCH_ROOTS=$(find "$WAVE/claims/c1" -type d \( -name '_scratch' -o -name '__pycache__' \) 2>/dev/null | LC_ALL=C sort | tr '\n' ' ')
SCRATCH_FILES=$(find "$WAVE/claims/c1" \( -path '*/_scratch/*' -o -path '*/__pycache__/*' \) -type f 2>/dev/null | wc -l)
SCRATCH_BYTES=$(find "$WAVE/claims/c1" \( -path '*/_scratch/*' -o -path '*/__pycache__/*' \) -type f -printf '%s\n' 2>/dev/null | awk '{s+=$1} END{print s+0}')

# ---- self-verify the snapshot (retry once on concurrent-write race) --------
attempt=0; ok=0; FAILOUT=""
while [ "$attempt" -lt 2 ]; do
  attempt=$((attempt+1))
  scan
  printf '%s' "$CHK_BODY" > "$CHK"
  FAILOUT=$( cd "$WAVE" && sha256sum -c "$CHK_REL" 2>&1 | grep -v ': OK$' )
  if [ -z "$FAILOUT" ]; then ok=1; break; fi
done
{
  echo "=== verify run $NOW (attempt $attempt, status $( [ "$ok" = 1 ] && echo PASS || echo FAIL)) ==="
  if [ "$ok" = 1 ]; then echo "sha256sum -c: all $N entries OK (run from $WAVE)"; else echo "sha256sum -c mismatches (seat wrote mid-scan):"; echo "$FAILOUT"; fi
} >> "$LOG"

# ---- custody live re-check vs pre-pair (no temp files) ---------------------
CUSTODY_PATHS=(/home/vgpnk/.config/devin/mcp_config.json /home/vgpnk/.omp/agent/mcp.json /home/vgpnk/.kimi-code/config.toml /home/vgpnk/.bashrc /home/vgpnk/.profile)
LIVE=""
for p in "${CUSTODY_PATHS[@]}"; do
  if [ -e "$p" ]; then LIVE+=$(printf '%s  %s' "$(hash_file "$p")" "$p")$'\n'; else LIVE+="ABSENT  $p"$'\n'; fi
done
PRE=$(grep -E '^[0-9a-f]{64}  /' "$CUSTODY_PRE" 2>/dev/null | tail -5)
CUSTODY_VERDICT="match (5/5)"
[ "$PRE" = "$(printf '%s' "$LIVE" | sed '/^ABSENT/d')" ] || CUSTODY_VERDICT="MISMATCH vs pre-pair"
PRE_CAP=$(sed -n 's/^# capture-utc: //p' "$CUSTODY_PRE" 2>/dev/null | head -1)

# ---- roster gaps -----------------------------------------------------------
GAP_LINES=""; present=0
for s in $C1_ROSTER; do
  if [ -d "$WAVE/claims/c1/$s" ] && [ -n "$(ls -A "$WAVE/claims/c1/$s" 2>/dev/null)" ]; then present=$((present+1)); else GAP_LINES="$GAP_LINES $s"; fi
done
REPORTS=$(ls "$WAVE/seats/" 2>/dev/null | sed 's/\.md$//' | tr '\n' ' ')

# ---- assemble manifest -----------------------------------------------------
{
  echo "# MANIFEST.draft — arc3-loop1-round1 chain c1 receipts (SEAT EX-14, executor)"
  echo "# status: DRAFT — point-in-time snapshot, regenerated until wave close"
  echo "# generated-utc: $NOW"
  echo "# repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin"
  echo "# repo-HEAD: $HEAD"
  echo "# verify: cd $WAVE && sha256sum -c $CHK_REL"
  echo "# scope: every file under claims/c1/ (recursive, excluding the three derived"
  echo "#        outputs in the footer, and seat-local _scratch/ trees unless INCLUDE_SCRATCH=1)"
  echo "#        + the custody pre-pair artifact under claims/cross/receipts/"
  echo "# columns: SHA256  SIZE_BYTES  MTIME_UTC  PATH (path relative to wave root)"
  echo "# entries: $N   total-bytes: $BYTES   vanished-during-scan: $VANISHED"
  echo
  echo "## section 1 — claims/c1 artifacts ($N)"
  printf '%s' "$ROWS"
  echo
  echo "## section 1b — excluded-transient (seat-local _scratch/ trees; not hashed)"
  echo "files: $SCRATCH_FILES   bytes: $SCRATCH_BYTES   roots: ${SCRATCH_ROOTS:-none}"
  echo "reason: wave rules put scratch under /tmp; /tmp is quota-exhausted on this host"
  echo "        (tmpfs usrquota, dd fails EDQUOT) so seats relocated scratch into seat dirs."
  echo "        Re-run with INCLUDE_SCRATCH=1 to hash these too."
  echo
  echo "## section 2 — custody pre-pair (cross-chain artifact referenced by this manifest)"
  if [ -e "$CUSTODY_PRE" ]; then
    printf '%s  %s  %s  %s\n' "$(hash_file "$CUSTODY_PRE")" "$(stat -c %s "$CUSTODY_PRE")" "$(utc "$(stat -c %Y "$CUSTODY_PRE")")" "${CUSTODY_PRE#"$WAVE"/}"
  else
    echo "ABSENT: $CUSTODY_PRE"
  fi
  echo "capture-utc (from receipt): ${PRE_CAP:-unknown}"
  echo "live re-check at $NOW vs pre-pair: $CUSTODY_VERDICT"
  printf '%s' "$LIVE" | sed 's/^/  live: /'
  echo
  echo "## section 3 — roster gaps (c1 chain, 26 seats)"
  echo "seat dirs with artifacts: $present/26   without:${GAP_LINES:- none}"
  echo "seat reports landed (seats/): ${REPORTS:-none}"
  echo
  echo "## footer — derived outputs (excluded from listing; cannot self-hash)"
  echo "generator  $(hash_file "$GEN_REPO")  $GEN_WAVE"
  echo "check-file $(hash_file "$CHK")  $CHK_REL"
  echo "verify-log $(hash_file "$LOG")  claims/c1/EX-14/verify.log"
  echo "manifest   self: not listed; sha256 recorded in seats/EX-14.md"
} > "$OUT"

# ---- summary ---------------------------------------------------------------
echo "MANIFEST: $OUT"
echo "entries=$N bytes=$BYTES vanished=$VANISHED verify=$( [ "$ok" = 1 ] && echo PASS || echo FAIL) custody=$CUSTODY_VERDICT"
echo "manifest sha256: $(hash_file "$OUT")"
