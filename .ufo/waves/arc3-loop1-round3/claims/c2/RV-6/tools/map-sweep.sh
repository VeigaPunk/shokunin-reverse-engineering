#!/usr/bin/env bash
# RV-6 declared-map sweep on one arm (bonus check for the landed revision).
# usage: map-sweep.sh <arm> <tool.py>
set -u
ARM="$1"; TOOL="$2"
FX=/var/tmp/rv6/fx
RUN=/var/tmp/rv6/runs/$ARM
mkdir -p "$RUN"
DECL="0 10 11 12 13 14 2 3"
chk() { # chk <label> <exit>
  local ok="OUT-OF-MAP"
  for d in $DECL; do [ "$2" = "$d" ] && ok="declared"; done
  printf '%-38s exit=%-3s %s\n' "$1" "$2" "$ok"
}
echo "=== declared-map sweep arm=$ARM tool-sha=$(sha256sum "$TOOL" | cut -d' ' -f1) ==="
python3 "$TOOL" capture --out "$RUN/s-absent.txt" --paths "$FX/nope.conf" >/dev/null 2>&1; chk "capture absent" $?
chmod 000 "$FX/unreadable.conf"
python3 "$TOOL" capture --out "$RUN/s-unreadable.txt" --paths "$FX/unreadable.conf" >/dev/null 2>&1; chk "capture unreadable file" $?
chmod 644 "$FX/unreadable.conf"
chmod 000 "$FX/blocked"
python3 "$TOOL" capture --out "$RUN/s-blocked.txt" --paths "$FX/blocked/inner.conf" >/dev/null 2>&1; chk "capture blocked dir" $?
chmod 755 "$FX/blocked"
python3 "$TOOL" verify "$RUN/definitely-not-a-receipt.txt" --live >/dev/null 2>&1; chk "verify missing receipt (USAGE)" $?
python3 "$TOOL" verify "$RUN/s-absent.txt" --live >/dev/null 2>&1; chk "verify absent-pair" $?
python3 "$TOOL" selftest --scratch /var/tmp/rv6/no-such-dir-xyz >/dev/null 2>&1; chk "selftest missing scratch (D6)" $?
python3 "$TOOL" capture --out /tmp/rv6-forbidden.txt --paths "$FX/good.conf" >/dev/null 2>&1; chk "capture into /tmp (advisory)" $?
python3 "$TOOL" --definitely-not-a-flag >/dev/null 2>&1; chk "unknown flag (USAGE)" $?
echo "=== sweep done ==="