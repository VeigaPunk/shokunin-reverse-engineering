#!/bin/bash
# EX-28 re-derivation recipe (rule #14) — v1 back-compat on the custody-pair tool.
#   usage: bash rerun-v1-compat.sh [TOOL] [REPO]
#     TOOL  default: <REPO>/.ufo/gates/custody-pair/custody-pair.py
#     REPO  default: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
# Run from a scratch dir under /dev/shm or /var/tmp (never /tmp: EDQUOT).
# The script pins the tool by sha into a snapshot copy, so a moving target cannot
# mis-attribute a row; every transcript header names its revision.
set -u
REPO=${2:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
TOOL=${1:-$REPO/.ufo/gates/custody-pair/custody-pair.py}
D=$(cd "$(dirname "$0")" && pwd)
case "$PWD" in /dev/shm/*|/var/tmp/*) ;; *) echo "refusing: run from /dev/shm or /var/tmp, not $PWD" >&2; exit 2;; esac
R1=$REPO/.ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt
R2=$REPO/.ufo/waves/arc3-loop1-round2/claims/c3/receipts/config-pre-pair-v2.txt
R3=$REPO/.ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt
S=$(sha256sum "$TOOL" | cut -d' ' -f1)
mkdir -p "snap/$S" out st
cp "$TOOL" "snap/$S/custody-pair.py"; T="snap/$S/custody-pair.py"
echo "REVISION: $S  bytes=$(stat -c %s "$TOOL")  mtime=$(stat -c %y "$TOOL")  lines=$(wc -l < "$T")"
python3 - "$TOOL" <<'PY'
import pathlib, re, sys
t = pathlib.Path(sys.argv[1]).read_text()
wired = re.search(r'add_argument\(\s*"--require-paths"', t)
used  = re.search(r'getattr\(args,\s*"require_paths"', t)
print("--require-paths wired:", "yes" if (wired and used) else "NO (declared in docstring only)")
PY
run(){ n=$1; shift; { echo "\$ python3 <tool@$S> $*"; TMPDIR=/dev/shm python3 "$T" "$@" ; echo "exit=$?"; } > "out/$n.txt" 2>&1
        printf '%-26s exit=%s\n' "$n" "$(tail -1 "out/$n.txt" | sed 's/exit=//')"; }
export TMPDIR
# frozen pair (expect 0 and 12)
run core-sums-frozen    verify "$D/v1-sums-round1.txt" "$R2"
run core-stanza-frozen  verify "$R1" "$R2"
run core-r1-vs-r3       verify "$R1" "$R3"
run core-r3-live        verify "$R3" --live
# live controls (expect 0; round-1 pins vs live expect 10 while the 12:57:45Z kimi drift stands)
run core-sums-livelive  verify "$D/v1-sums-live.txt" --live
run core-sums-live      verify "$D/v1-sums-round1.txt" --live
run core-stanza-live    verify "$R1" --live
# attacks
for a in sums-binary-marker sums-upper sums-1space sums-tab sums-crlf sums-nonl sums-dotpath sums-tilde sums-dup sums-dup-rev sums-1of5 stanza-exists-no stanza-no-kimi-sha-live; do
  [ -f "$D/$a.txt" ] && run "atk-$a" verify "$D/$a.txt" --live
done
run atk-1of5-require    verify "$D/sums-1of5.txt" --live --require-paths 5
run atk-empty           verify "$D/sums-empty.txt" --live
# A4b: v1 stanza omitting SHA256, content swapped same-size/same-mode
mkdir -p fx && printf 'AAA' > fx/f.conf
{ echo "PATH: $PWD/fx/f.conf"; echo "EXISTS: yes"; echo "SIZE: 3"; printf 'MODE: 644  UID: %s  GID: %s\n' "$(id -u)" "$(id -g)"; } > fx/v1-no-sha.txt
run omit-sha-before     verify fx/v1-no-sha.txt --live
printf 'BBB' > fx/f.conf
run omit-sha-after      verify fx/v1-no-sha.txt --live
# selftest + declared-class probes
run selftest            selftest --scratch "$PWD/st"
run selftest-badscratch selftest --scratch "$PWD/no-such-dir"
echo "--- selftest summary ---"; tail -2 out/selftest.txt
echo "--- D6 probe ---"; tail -2 out/selftest-badscratch.txt
echo "--- post-run tool sha (must equal revision) ---"; sha256sum "$TOOL"
echo "REVISION $S" > out/REVISION.txt