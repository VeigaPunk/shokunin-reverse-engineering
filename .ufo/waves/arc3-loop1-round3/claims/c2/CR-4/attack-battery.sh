#!/usr/bin/env bash
# =============================================================================
# CR-4 attack battery — custody-pair write-guard evasion hunt (arc3-loop1-round3,
# chain c2, role critic). Scratch-only: every write lands under $SB, a fresh
# /dev/shm dir; the real custody paths are never opened for writing.
#
# usage: attack-battery.sh <custody-pair.py> <variant-label>
# =============================================================================
set -u
export PYTHONDONTWRITEBYTECODE=1
TOOL="$(readlink -f "$1")"
LABEL="${2:-unlabeled}"
TOOL_SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
SB=$(mktemp -d /dev/shm/cr4-battery-XXXXXX) || exit 1
export TMPDIR="$SB"
H="$SB/home"; S="$SB/scope"
mkdir -p "$H/.config/devin" "$H/.omp/agent" "$H/.kimi-code" "$S"

printf 'sandbox bashrc\n'          > "$H/.bashrc"
printf 'sandbox profile\n'         > "$H/.profile"
printf '{sandbox}\n'               > "$H/.config/devin/mcp_config.json"
printf '{sandbox}\n'               > "$H/.omp/agent/mcp.json"
printf '[sandbox]\n'               > "$H/.kimi-code/config.toml"

echo "== CR-4 write-guard attack battery =="
echo "variant: $LABEL"
echo "tool tested: $TOOL"
echo "tool sha256: $TOOL_SHA"
echo "sandbox: $SB (HOME=$H)"
echo "python: $(python3 -V 2>&1)"

run() { # run <name> <victim-file-nonempty-when-in-scope> <out> <paths...>
  local name="$1" victim="$2" out="$3"; shift 3
  local before after rc
  before=$(sha256sum "$victim" | cut -d' ' -f1)
  HOME="$H" python3 "$TOOL" capture --out "$out" --paths "$@" --label "$name" \
      > "$SB/last.out" 2> "$SB/last.err"
  rc=$?
  after=$(sha256sum "$victim" | cut -d' ' -f1)
  printf '\n--- %s ---\n' "$name"
  printf 'cmd: capture --out %s --paths %s\n' "$out" "$*"
  printf 'exit=%d  victim=%s\n' "$rc" "$victim"
  printf 'victim sha256 before=%s after=%s\n' "$before" "$after"
  printf 'tool stdout: %s\n' "$(head -2 "$SB/last.out" | tr '\n' '|')"
  printf 'tool stderr: %s\n' "$(head -3 "$SB/last.err" | tr '\n' '|')"
  if [ "$rc" -eq 2 ]; then
    printf 'verdict: REFUSED'
  elif [ "$rc" -eq 0 ]; then
    printf 'verdict: ALLOWED'
  else
    printf 'verdict: OTHER-EXIT'
  fi
  if [ "$after" = "$before" ]; then printf ' / victim-UNCHANGED\n'; else printf ' / victim-CLOBBERED\n'; fi
  return 0
}

# --- T0 control: the round-2 VZ-4 finding, scoped path used as --out ---------
printf 'victim T0\n' > "$S/guarded.conf"
run "T0-scoped-as-out" "$S/guarded.conf" "$S/guarded.conf" "$S/guarded.conf"

# --- T1 hardlink alias of the scoped path -----------------------------------
printf 'victim T1\n' > "$S/hl.conf"; ln -f "$S/hl.conf" "$S/hl-alias.out"
run "T1-hardlink-alias-scoped" "$S/hl.conf" "$S/hl-alias.out" "$S/hl.conf"

# --- T2 symlink alias of the scoped path ------------------------------------
printf 'victim T2\n' > "$S/sl.conf"; ln -sfn "$S/sl.conf" "$S/sl-alias.out"
run "T2-symlink-alias-scoped" "$S/sl.conf" "$S/sl-alias.out" "$S/sl.conf"

# --- T3 relative/absolute spelling mismatch (resolved on both sides?) -------
printf 'victim T3\n' > "$S/rel.conf"
( cd "$S" && HOME="$H" python3 "$TOOL" capture --out ./rel.conf --paths rel.conf \
      --label T3-rel-vs-abs > "$SB/t3.out" 2> "$SB/t3.err" ); rc3=$?
b3=$(sha256sum "$S/rel.conf" | cut -d' ' -f1)
printf '\n--- T3-relative-args-both-sides ---\n'
printf 'cmd: (cd scope) capture --out ./rel.conf --paths rel.conf\n'
printf 'exit=%d  victim sha256 after=%s (pre-computed before=see script order)\n' "$rc3" "$b3"
printf 'tool stderr: %s\n' "$(head -2 "$SB/t3.err" | tr '\n' '|')"
if [ "$rc3" -eq 2 ]; then printf 'verdict: REFUSED'; else printf 'verdict: ALLOWED(exit %d)\n' "$rc3"; fi
if [ "$b3" = "$(printf 'victim T3\n' | sha256sum | cut -d' ' -f1)" ]; then printf ' / victim-UNCHANGED\n'; else printf ' / victim-CLOBBERED\n'; fi

# --- T4 /proc/self/fd alias to the scoped path ------------------------------
printf 'victim T4\n' > "$S/fd.conf"
exec 9<> "$S/fd.conf"
run "T4-proc-self-fd-alias" "$S/fd.conf" "/proc/self/fd/9" "$S/fd.conf"
exec 9>&-

# --- T5 /proc/self/root alias ------------------------------------------------
printf 'victim T5\n' > "$S/root.conf"
run "T5-proc-self-root-alias" "$S/root.conf" "/proc/self/root$S/root.conf" "$S/root.conf"

# --- T6 symlink-loop as --out (declared-map discipline) ---------------------
printf 'victim T6\n' > "$S/loop.conf"; ln -sfn loop-a "$S/loop-b"; ln -sfn loop-b "$S/loop-a"
run "T6-out-symlink-loop" "$S/loop.conf" "$S/loop-a" "$S/loop.conf"
rm -f "$S/loop-a" "$S/loop-b"

# --- T7 sidecar clobber: --out=foo, scoped=foo.sha256 -----------------------
printf 'victim T7 (the scoped file, name ends in .sha256)\n' > "$S/vic.sha256"
run "T7-sidecar-clobber" "$S/vic.sha256" "$S/vic" "$S/vic.sha256"

# --- T8 dangling-symlink --out pointing at the scoped path ------------------
printf 'victim T8\n' > "$S/dang.conf"; ln -sfn "$S/dang.conf" "$S/dang-link"
run "T8-dangling-symlink-to-nowhere? (target exists)" "$S/dang.conf" "$S/dang-link" "$S/dang.conf"
rm -f "$S/dang-link"

# --- T9 canonical-5 hardlink (D7 re-check at this revision) -----------------
printf 'sandbox bashrc v2\n' > "$H/.bashrc-victim"
cp "$H/.bashrc" "$H/.bashrc-orig"; printf 'sandbox bashrc\n' > "$H/.bashrc"
ln -f "$H/.bashrc" "$SB/bashrc-alias.out"
run "T9-canonical5-hardlink" "$H/.bashrc" "$SB/bashrc-alias.out" "$H/.bashrc" "$H/.profile"

# --- T10 canonical-5 symlink alias (control: resolve() should catch) --------
ln -sfn "$H/.profile" "$SB/profile-alias.out"
run "T10-canonical5-symlink" "$H/.profile" "$SB/profile-alias.out" "$H/.bashrc" "$H/.profile"

# --- T11 symlinked parent directory ------------------------------------------
printf 'victim T11\n' > "$S/dir.conf"; ln -sfn "$S" "$S/../scopedir-link"
run "T11-symlinked-parent-dir" "$S/dir.conf" "$S/../scopedir-link/dir.conf" "$S/dir.conf"

# --- T12 tilde spelling -------------------------------------------------------
printf 'victim T12\n' > "$H/twelve.conf"
run "T12-tilde-spelling" "$H/twelve.conf" "~/twelve.conf" "~/twelve.conf"

# --- T13 must-allow: ordinary fresh --out on an existing scope ---------------
# (regression guard: an inode arm using os.path.samefile on a not-yet-existing
#  --out raises FileNotFoundError -> traceback if uncaught)
printf 'victim T13\n' > "$S/normal.conf"
run "T13-must-allow-fresh-out" "$S/normal.conf" "$S/new-receipt.txt" "$S/normal.conf"
printf 'receipt written: %s\n' "$(test -s "$S/new-receipt.txt" && echo yes || echo no)"

# --- T14 must-allow: fresh --out with a missing scoped path ------------------
run "T14-must-allow-missing-scoped" "$S/normal.conf" "$S/new-receipt2.txt" "$S/does-not-exist.conf"
printf 'receipt written: %s\n' "$(test -s "$S/new-receipt2.txt" && echo yes || echo no)"

# --- T15 must-allow: fresh --out via an ordinary (non-alias) path ------------
run "T15-must-allow-plain" "$S/normal.conf" "$SB/plain-receipt.txt" "$S/normal.conf"
printf 'receipt written: %s\n' "$(test -s "$SB/plain-receipt.txt" && echo yes || echo no)"

# --- T16 --out whose parent is a regular file (mkdir is outside the try) -----
run "T16-out-parent-is-file" "$S/normal.conf" "$S/normal.conf/sub/receipt.txt" "$S/normal.conf"

# --- T17 empty --out ----------------------------------------------------------
run "T17-empty-out" "$S/normal.conf" "" "$S/normal.conf"

# --- T18 sidecar hardlink alias (no name coincidence needed) -----------------
printf 'victim T18\n' > "$S/anyname.conf"
ln -f "$S/anyname.conf" "$S/mk18.sha256"
run "T18-sidecar-hardlink-alias" "$S/anyname.conf" "$S/mk18" "$S/anyname.conf"

echo
echo "== battery done (variant $LABEL) =="
echo "sandbox kept for inspection: $SB"