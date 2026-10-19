#!/usr/bin/env bash
# =============================================================================
# CR-4 TOCTOU probe — is the resolve()-then-write guard check-vs-use racy?
# Scratch-only (/dev/shm). A swapper atomically retargets a symlink between
# $H/safe.out (unguarded) and $H/.bashrc (the canonical custody path #4, under
# the sandbox HOME) while `capture` runs with --out <link> and DEFAULT --paths.
#
# A refusal (exit 2) means the guard resolved the link to .bashrc in time.
# A hit means the guard resolved it to the safe target but open() followed the
# link after the swap: receipt bytes landed in the guarded file.
#
# The landed round-3 docstring declares TOCTOU inherent and out of scope; this
# probe quantifies the declared-out window rather than claiming a defect.
#
# usage: toctou-race.sh <custody-pair.py> <iterations> <label>
# =============================================================================
set -u
export PYTHONDONTWRITEBYTECODE=1
TOOL="$(readlink -f "$1")"; N="${2:-300}"; LABEL="${3:-unlabeled}"
TOOL_SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
SB=$(mktemp -d /dev/shm/cr4-toctou-XXXXXX) || exit 1
export TMPDIR="$SB"
H="$SB/home"
mkdir -p "$H"
printf 'sandbox bashrc\n' > "$H/.bashrc"
printf 'sandbox profile\n' > "$H/.profile"

echo "== CR-4 TOCTOU probe =="
echo "variant: $LABEL"
echo "tool: $TOOL  sha256=$TOOL_SHA"
echo "iterations: $N   sandbox: $SB"

cat > "$SB/swapper.py" <<'PY'
import itertools, os, sys
H = sys.argv[1]
link = os.path.join(H, "link.out")
targets = (os.path.join(H, "safe.out"), os.path.join(H, ".bashrc"))
for t in itertools.cycle(targets):
    tmp = os.path.join(H, "link.tmp")
    try:
        os.symlink(t, tmp)
        os.rename(tmp, link)
    except FileExistsError:
        os.remove(tmp)
PY

python3 "$SB/swapper.py" "$H" &
SW=$!
sleep 0.2
refused=0; allowed=0; hits=0; other=0
for i in $(seq 1 "$N"); do
  printf 'sandbox bashrc\n' > "$H/.bashrc"
  HOME="$H" python3 "$TOOL" capture --out "$H/link.out" --label toctou-$i \
      >/dev/null 2>"$SB/last.err"; rc=$?
  if head -c 26 "$H/.bashrc" 2>/dev/null | grep -q "custody-pair receipt v2"; then
    hits=$((hits+1)); cp "$H/.bashrc" "$SB/hit-$i.bashrc" 2>/dev/null
    printf 'HIT at iteration %d (exit=%d) stderr=%s\n' "$i" "$rc" "$(head -1 "$SB/last.err")"
  fi
  case $rc in
    2) refused=$((refused+1));;
    0) allowed=$((allowed+1));;
    *) other=$((other+1));;
  esac
done
kill "$SW" 2>/dev/null; wait "$SW" 2>/dev/null
echo "refusals(exit2)=$refused  allowed(exit0)=$allowed  other=$other"
echo "guarded file clobbered through the raced link: $hits / $N"
[ "$hits" -gt 0 ] && echo "verdict: RACY — check-vs-use window observed" || echo "verdict: no hit in $N tries (window not observed)"
echo "sandbox kept: $SB"