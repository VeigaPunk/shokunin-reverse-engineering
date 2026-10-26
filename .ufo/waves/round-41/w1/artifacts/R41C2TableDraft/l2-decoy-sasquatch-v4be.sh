#!/bin/sh
echo "ran: $*" >> /tmp/r41-decoy.log
out=""
while [ $# -gt 0 ]; do case "$1" in -d) out="$2"; shift 2;; *) shift;; esac; done
[ -n "$out" ] && mkdir -p "$out" && printf 'decoy tmp-log ran\n' > "$out/DECOY-MARKER"
exit 0
