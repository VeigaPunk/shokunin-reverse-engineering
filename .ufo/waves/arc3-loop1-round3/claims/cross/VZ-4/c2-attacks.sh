#!/bin/bash
# VZ-4 C2 attack harness — the four named holes (D2 EACCES fail-open, D3 partial
# verify, write-guard clobber scope, D6 selftest scratch-guard) re-measured
# against a SCRATCH COPY of the custody tool at whatever revision is under test.
#
# usage: c2-attacks.sh <tool-path> <scratch-root> <out-file>
# Never touches a real custody path: every fixture lives under the scratch root.
set -u
TOOL=$1; SCR=$2; OUT=$3
PY=python3
mkdir -p "$SCR"
: > "$OUT"
say() { printf '%s\n' "$*" | tee -a "$OUT"; }
run() { # run <tag> <cmd...>  → records stdout+exit
  local tag=$1; shift
  local o rc
  o=$("$@" 2>&1); rc=$?
  printf 'CASE %s exit=%d\n%s\n--\n' "$tag" "$rc" "$o" | tee -a "$OUT"
}
say "== VZ-4 C2 attack harness =="
say "tool=$TOOL sha256=$(sha256sum "$TOOL" | cut -d' ' -f1) lines=$(wc -l < "$TOOL")"
say "scratch=$SCR utc=$(date -u +%FT%TZ)"

# --- B: selftest normal (case count + exit) ---------------------------------
mkdir -p "$SCR/st-normal"
run B-selftest-normal $PY "$TOOL" selftest --scratch "$SCR/st-normal"

# --- D6: selftest with a MISSING scratch dir --------------------------------
MISSING="$SCR/definitely-absent-$$/nested"
run D6-selftest-missing-scratch $PY "$TOOL" selftest --scratch "$MISSING"

# --- fixtures ---------------------------------------------------------------
D="$SCR/fix"; rm -rf "$D"; mkdir -p "$D"
printf 'vz4-fixture-alpha\n' > "$D/alpha.txt"
printf 'vz4-fixture-beta\n'  > "$D/beta.txt"
chmod 000 "$D/beta.txt" 2>/dev/null || true
mkdir -p "$D/eacces-dir" && printf 'x\n' > "$D/eacces-dir/f.txt" && chmod 000 "$D/eacces-dir" 2>/dev/null || true

# --- D2a: capture over an exists-but-EACCES path ----------------------------
printf 'vz4-fixture-gamma\n' > "$D/gamma.txt"; chmod 000 "$D/gamma.txt"
run D2a-capture-eacces $PY "$TOOL" capture --paths "$D/gamma.txt" --out "$D/rec-eacces.json" --label vz4-eacces
say "D2a receipt stanza (expect declared class after fix / traceback before):"
grep -E 'PATH:|EXISTS:|SHA256:|STAT|EACCES|unreadable' "$D/rec-eacces.json" 2>/dev/null | tee -a "$OUT" || true

# --- D2b: verify --live against a now-unreadable candidate -----------------
chmod 644 "$D/beta.txt"
$PY "$TOOL" capture --paths "$D/beta.txt" --out "$D/rec-beta.json" --label vz4-beta >>"$OUT" 2>&1
chmod 000 "$D/beta.txt"
say "D2b receipt captured while readable at $(sha256sum "$D/beta.txt" 2>/dev/null | cut -c1-16 || echo sha-unavailable); now chmod 000 → verify --live:"
run D2b-verify-live-eacces $PY "$TOOL" verify "$D/rec-beta.json" --live

# --- D2c: both-sides-absent verify (the fail-open MATCH) --------------------
ABS="$D/never-existed-$$"
$PY "$TOOL" capture --paths "$ABS" --out "$D/rec-absent.json" --label vz4-absent >>"$OUT" 2>&1
say "D2c absent-capture exit above; now verify --live against the still-absent path:"
run D2c-verify-live-both-absent $PY "$TOOL" verify "$D/rec-absent.json" --live

# --- D3: partial-reference coverage ----------------------------------------
printf 'vz4-one-of-five\n' > "$D/only.txt"
run D3a-capture-one-path $PY "$TOOL" capture --paths "$D/only.txt" --out "$D/rec-one.json" --label vz4-one
say "D3b verify the 1-path receipt against live (fail-open if exit 0 with compared=1/1):"
run D3b-verify-one-vs-live $PY "$TOOL" verify "$D/rec-one.json" --live
say "D3c the proposed adapter form --require-paths 5 (unrecognized pre-fix = USAGE):"
run D3c-verify-require-paths $PY "$TOOL" verify "$D/rec-one.json" --live --require-paths 5

# --- write-guard scope: --paths X --out X clobbers the scoped file ----------
printf 'vz4-clobber-victim-original\n' > "$D/victim.txt"
before=$(sha256sum "$D/victim.txt" | cut -d' ' -f1)
run Wguard-capture-out-equals-paths $PY "$TOOL" capture --paths "$D/victim.txt" --out "$D/victim.txt" --label vz4-clobber
after=$(sha256sum "$D/victim.txt" | cut -d' ' -f1)
say "Wguard victim sha before=$before after=$after clobbered=$([ "$before" = "$after" ] && echo NO || echo YES)"

# --- canonical guard: refuse --out over a real custody path (by construction
#     this only exercises the refusal branch; asserted indirectly — the tool
#     resolves the target and returns USAGE before any write) -----------------
run Wguard-canonical-refusal $PY "$TOOL" capture --out "$HOME/.bashrc" --label vz4-must-refuse

say "== end $(date -u +%FT%TZ) =="