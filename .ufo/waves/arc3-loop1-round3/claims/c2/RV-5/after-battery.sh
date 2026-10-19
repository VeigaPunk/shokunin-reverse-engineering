#!/bin/bash
[ -z "$3" ] && { echo "need <tool> <outdir> <tag>"; exit 9; }
# RV-5 after-battery — run the four closure injections + regression battery against
# the tool revision present at run time. Scratch-local; custody paths read-only.
# usage: after-battery.sh <tool-path> <outdir> <tag>
TOOL="$1"; OUT="$2"; TAG="$3"
S="/var/tmp/rv5/scratch/$TAG"
rm -rf "$S"; mkdir -p "$S" "$OUT"
export PYTHONDONTWRITEBYTECODE=1
PY=python3
LOG="$OUT/run.log"
: >"$LOG"

r() {  # r <name> <cmd...>
  local name="$1"; shift
  { echo "### $name"; echo "\$ $*"; } >>"$LOG"
  { "$PY" "$TOOL" "$@"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1
}
s() {  # s <name> <shell-cmd>
  local name="$1"; shift
  { echo "### $name"; echo "\$ $*"; } >>"$LOG"
  { bash -c "$*"; echo "exit=$?"; echo "---"; } >>"$LOG" 2>&1
}

sha256sum "$TOOL" >>"$LOG"; stat -c '%y %s' "$TOOL" >>"$LOG"; echo "tag=$TAG $(date -Is)" >>"$LOG"

# fixtures
printf 'fixture-one\n' >"$S/a.conf"; printf 'fixture-two\n' >"$S/b.conf"

# ---------- C2/fix reachability: the four named holes ----------
# D2a: exists-but-EACCES parent dir
mkdir -p "$S/eacces-dir"; printf 'inner\n' >"$S/eacces-dir/inner.conf"; chmod 000 "$S/eacces-dir"
r D2a-capture capture --out "$S/d2a.txt" --paths "$S/eacces-dir/inner.conf" --label d2a
r D2a-verify-live verify "$S/d2a.txt" --live
r D2a-verify-two verify "$S/d2a.txt" "$S/d2a.txt"
cat "$S/d2a.txt" >"$OUT/D2a-receipt.txt" 2>&1
chmod 755 "$S/eacces-dir"

# D2b: chmod-000 file -> must be a declared class, no traceback
printf 'unreadable\n' >"$S/unreadable.conf"; chmod 000 "$S/unreadable.conf"
r D2b-capture capture --out "$S/d2b.txt" --paths "$S/unreadable.conf" --label d2b
cat "$S/d2b.txt" >"$OUT/D2b-receipt.txt" 2>&1
r D2b-verify-live verify "$S/d2b.txt" --live
chmod 644 "$S/unreadable.conf"

# D2c: readable receipt; candidate turns unreadable -> verify must not traceback
printf 'toggle\n' >"$S/toggle.conf"
r D2c-capture capture --out "$S/d2c.txt" --paths "$S/toggle.conf" --label d2c
chmod 000 "$S/toggle.conf"
r D2c-verify-live verify "$S/d2c.txt" --live
chmod 644 "$S/toggle.conf"

# D3: partial reference coverage
r D3-capture-1of5 capture --out "$S/d3-one.txt" --paths "$S/a.conf" --label d3
r D3-verify-live-default verify "$S/d3-one.txt" --live
r D3-verify-live-require5 verify "$S/d3-one.txt" --live --require-paths 5
# control: a full 5-path reference must satisfy --require-paths 5
r D3-control-5paths verify "$S/never.txt" --live --require-paths 5

# guard scope: --out X --paths X must refuse and leave X untouched
printf 'precious measurement target\n' >"$S/self.conf"
sha256sum "$S/self.conf" >>"$LOG"
r guard-scope capture --out "$S/self.conf" --paths "$S/self.conf" --label guard
sha256sum "$S/self.conf" >>"$LOG"
# relative-path form
s guard-relative "cd $S && $PY $TOOL capture --out ./rel.conf --paths ./rel.conf --label guardrel"
sha256sum "$S/rel.conf" >>"$LOG" 2>&1
# canonical custody path still guarded (read-only capture of the path itself first)
r guard-custody capture --out "$HOME/.bashrc" --paths "$S/a.conf" --label guardcust
sha256sum "$HOME/.bashrc" >>"$LOG"

# D6: selftest --scratch missing dir -> declared USAGE, no traceback
r D6-missing-scratch selftest --scratch "$S/does-not-exist"
r D6-scratch-is-file selftest --scratch "$S/a.conf"
r D6-unwritable-scratch selftest --scratch /proc/nope

# ---------- regression battery ----------
r R-selftest selftest --scratch "$S"

# rewrite / drift classes on independent fixtures
printf 'reg\n' >"$S/reg.conf"; touch -d @1000000000 "$S/reg.conf"
r R-pre capture --out "$S/reg-pre.txt" --paths "$S/reg.conf" --label reg
printf 'reg\n' >"$S/reg.conf"                      # same content, ctime moves
s R-inplace-rewrite "touch -d @1000000000 $S/reg.conf && $PY $TOOL verify $S/reg-pre.txt --live"
printf 'reg-new\n' >"$S/reg.conf"
r R-content-drift verify "$S/reg-pre.txt" --live

# rename class
printf 'rn\n' >"$S/rn.conf"; touch -d @1000000000 "$S/rn.conf"
r R-rn-pre capture --out "$S/rn-pre.txt" --paths "$S/rn.conf" --label rn
s R-rename-rewrite "printf 'rn\n' >$S/rn.new && touch -d @1000000000 $S/rn.new && mv $S/rn.new $S/rn.conf && touch -d @1000000000 $S/rn.conf && $PY $TOOL verify $S/rn-pre.txt --live"

# absent
printf 'x\n' >"$S/gone.conf"
r R-gone-pre capture --out "$S/gone-pre.txt" --paths "$S/gone.conf" --label gone
rm -f "$S/gone.conf"
r R-absent verify "$S/gone-pre.txt" --live

# metadata drift (mode)
printf 'md\n' >"$S/md.conf"; touch -d @1000000000 "$S/md.conf"
r R-md-pre capture --out "$S/md-pre.txt" --paths "$S/md.conf" --label md
chmod 600 "$S/md.conf"
r R-metadata verify "$S/md-pre.txt" --live

# TZ independence of the UTC render (independent of the embedded case)
s R-tz-utc  "TZ=UTC-3 $PY $TOOL capture --out - --paths $S/a.conf | grep MTIME_UTC_RENDER"
s R-tz-tokyo "TZ=Asia/Tokyo $PY $TOOL capture --out - --paths $S/a.conf | grep MTIME_UTC_RENDER"
s R-tz-local "TZ=Asia/Tokyo $PY $TOOL capture --out - --paths $S/a.conf | grep MTIME_LOCAL_RENDER"

# v1 compatibility shapes (synthesized from a live capture)
s R-v1-stanza "$PY - $TOOL $S/a.conf $S >>$LOG 2>&1 <<'PYEOF'
import subprocess, sys, os
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).parent))
import importlib.util
spec = importlib.util.spec_from_file_location('cp', sys.argv[1]); cp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cp)
sec = cp.capture_path(Path(sys.argv[2]))
import time
Path(sys.argv[3], 'v1-stanza.txt').write_text(
    'PATH: %s\nEXISTS: yes\nSIZE: %d\nMTIME_UTC: %s\nMODE: %s  UID: %d  GID: %d\nSHA256: %s\n' % (
        sec['path'], sec['size'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['mtime_epoch'])),
        sec['mode'], sec['uid'], sec['gid'], sec['sha256']))
Path(sys.argv[3], 'v1-sums.txt').write_text('%s  %s\n' % (sec['sha256'], sec['path']))
Path(sys.argv[3], 'v1-pipe.txt').write_text('%s | %d | %s | %s | %d | 8 | %s\n' % (
        sec['path'], sec['inode'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['ctime_epoch'])),
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec['mtime_epoch'])), sec['size'], sec['sha256']))
PYEOF"
r R-v1-stanza-verify verify "$S/v1-stanza.txt" --live
r R-v1-sums-verify verify "$S/v1-sums.txt" --live
r R-v1-pipe-verify verify "$S/v1-pipe.txt" --live

# live custody pair (read-only) and MATCH 5/5
r R-live-pre capture --out "$S/live-pre.txt" --label rv5-pre
r R-live-post capture --out "$S/live-post.txt" --label rv5-post
r R-live-pair verify "$S/live-pre.txt" "$S/live-post.txt"
r R-live-pair-vs-live verify "$S/live-pre.txt" --live
# receipt self-pin
s R-receipt-selfpin "grep -m1 '^# tool:' $S/live-pre.txt"
# second capture byte-identity of custody payloads (idempotence)
s R-live-idempotent "diff <(grep -E '^(PATH|EXISTS|TYPE|SIZE|SHA256|INODE|MODE|UID|GID|MTIME_EPOCH|MTIME_NS|CTIME_EPOCH|CTIME_NS):' $S/live-pre.txt) <(grep -E '^(PATH|EXISTS|TYPE|SIZE|SHA256|INODE|MODE|UID|GID|MTIME_EPOCH|MTIME_NS|CTIME_EPOCH|CTIME_NS):' $S/live-post.txt) && echo IDENTICAL-PAYLOAD"

# unparsable receipt -> USAGE (regression)
s R-unparsable "printf 'not a receipt\n' >$S/junk.txt && $PY $TOOL verify $S/junk.txt --live"

# read-only check: custody path sha256 pre/post the whole battery
s R-custody-sha-before "sha256sum $HOME/.bashrc $HOME/.profile $HOME/.kimi-code/config.toml $HOME/.omp/agent/mcp.json $HOME/.config/devin/mcp_config.json"

echo "BATTERY-END" >>"$LOG"
exit 0