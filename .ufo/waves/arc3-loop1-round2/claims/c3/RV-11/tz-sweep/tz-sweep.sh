#!/bin/bash
# RV-11 attack A: TZ-independence of the tool's capture rendering.
# Usage: tz-sweep.sh <tool> <outdir> [capture-args...]
# Runs the tool's capture under TZ=UTC / TZ=America/Toronto / TZ=Asia/Tokyo and diffs.
set -u
tool="$1"; outdir="$2"; shift 2
args=("$@")
mkdir -p "$outdir"
for tz in UTC America/Toronto Asia/Tokyo Pacific/Kiritimati; do
  slug=$(echo "$tz" | tr '/' '_')
  TZ="$tz" python3 "$tool" "${args[@]}" > "$outdir/capture-$slug.out" 2> "$outdir/capture-$slug.err"
  echo "TZ=$tz exit=$? out-$slug lines=$(wc -l < "$outdir/capture-$slug.out")"
done
for f in "$outdir"/capture-UTC.out; do :; done
ref="$outdir/capture-UTC.out"
rc=0
for tz in America_Toronto Asia_Tokyo Pacific_Kiritimati; do
  if diff -q "$ref" "$outdir/capture-$tz.out" >/dev/null 2>&1; then
    echo "TZ-INDEPENDENT: capture-UTC.out == capture-$tz.out"
  else
    echo "TZ-SENSITIVE: capture-UTC.out != capture-$tz.out"; diff "$ref" "$outdir/capture-$tz.out" | head -12; rc=1
  fi
done
exit $rc
