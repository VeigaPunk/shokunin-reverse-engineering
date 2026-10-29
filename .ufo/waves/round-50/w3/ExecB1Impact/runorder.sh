#!/usr/bin/env bash
# ExecB1Impact: run the frozen C2 counter WITH --battery at each order-variant clone,
# with FREEZE = the C1 freeze 435d41fd (the real scoring shape).
# Usage: runorder.sh <SCRATCH> <variant-name>
set -u
S="$1"; name="$2"
clone="$S/$name"
rev=$(git -C "$clone" rev-parse HEAD)
export TMPDIR="$S"
mkdir -p "$S/receipts"
out="$S/receipts/$name.json"
start=$(date -u +%Y-%m-%dT%H:%M:%SZ)
( cd "$clone" && python3 -I -B tools/round-50/c2-record.py --root "$clone" --rev "$rev" \
    --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --battery --work "$S/w-$name" --json-out "$out" ) \
    >"$S/receipts/$name.out" 2>"$S/receipts/$name.err"
ec=$?
end=$(date -u +%Y-%m-%dT%H:%M:%SZ)
printf '%s\n' \
  "name=$name" "rev=$rev" \
  "cmd=( cd $clone && python3 -I -B tools/round-50/c2-record.py --root $clone --rev $rev --freeze 435d41fd4ad9211d1579fc447936fb33d2b74467 --battery --work $S/w-$name --json-out $out )" \
  "exit=$ec" "utc_start=$start" "utc_end=$end" \
  "stdout_sha256=$(sha256sum "$S/receipts/$name.out" | cut -d' ' -f1)" \
  "json_sha256=$(sha256sum "$out" 2>/dev/null | cut -d' ' -f1)" \
  "stderr_sha256=$(sha256sum "$S/receipts/$name.err" | cut -d' ' -f1)" > "$S/receipts/$name.txt"
echo "done $name exit=$ec"
