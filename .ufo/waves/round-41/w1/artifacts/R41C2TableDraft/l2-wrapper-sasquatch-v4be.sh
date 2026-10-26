#!/bin/sh
# publishing -be wrapper: marks the -d dir, then execs the real binary with -be
out=""
prev=""
for arg in "$@"; do
  [ "$prev" = "-d" ] && out="$arg"
  prev="$arg"
done
[ -n "$out" ] && mkdir -p "$out" && printf 'wrapper ran with -be\n' > "$out/WRAPPER-MARKER"
exec /home/vgpnk/.local/bin/sasquatch-v4be -be "$@"
