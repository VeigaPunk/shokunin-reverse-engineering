#!/usr/bin/env bash
# Round-32 R32-C1 carrier builder: 12 ARM64X hybrid PE DLLs linked by the host LLVM 23.1.3
# (clang + llvm-mc + lld-link -machine:arm64x -Brepro). The two load-config inputs are
# LLVM's own lld test inputs at tag llvmorg-23.1.3 (S098), committed under
# corpus/evidence/round-32/c1/inputs/. Each carrier holds a native ARM64 object and an
# ARM64EC object; every function is an exported leaf, so no function is reachable
# only through a call. Spec columns: id native_count ec_count native_prefix ec_prefix opt.
# Usage: build-arm64x-carriers.sh <lane-root> <out-dir>
set -euo pipefail
LANE=${1:?lane root}
OUT=${2:?out dir}
IN="$LANE/corpus/evidence/round-32/c1/inputs"
mkdir -p "$OUT/obj"
SPEC='k01 1 1 f f 1
k02 2 2 f f 2
k03 3 3 f f 0
k04 4 1 f g 1
k05 1 4 f g 1
k06 5 5 f f 0
k07 6 2 f g 2
k08 2 6 f g 2
k09 7 3 n e 1
k10 3 7 n e 0
k11 8 8 f f 2
k12 1 2 n e 1'
gen() { # prefix count salt
  local p=$1 n=$2 s=$3 i
  for ((i = 1; i <= n; i++)); do
    printf '__declspec(dllexport) int %s%d(int a, int b) { return a * %d + b - %d; }\n' "$p" "$i" $((i * 7 + s)) $((i + s))
  done
}
llvm-mc -filetype=obj -triple=aarch64-windows "$IN/loadconfig-arm64.s" -o "$OUT/obj/lc-arm64.obj"
llvm-mc -filetype=obj -triple=arm64ec-windows "$IN/loadconfig-arm64ec.s" -o "$OUT/obj/lc-arm64ec.obj"
while read -r id nn ne pn pe opt; do
  gen "$pn" "$nn" 3 > "$OUT/obj/$id-native.c"
  gen "$pe" "$ne" 5 > "$OUT/obj/$id-ec.c"
  clang --target=aarch64-pc-windows-msvc -O"$opt" -c "$OUT/obj/$id-native.c" -o "$OUT/obj/$id-native.obj"
  clang --target=arm64ec-pc-windows-msvc -O"$opt" -c "$OUT/obj/$id-ec.c" -o "$OUT/obj/$id-ec.obj"
  lld-link -machine:arm64x -dll -noentry -nodefaultlib -Brepro \
    "$OUT/obj/$id-native.obj" "$OUT/obj/$id-ec.obj" "$OUT/obj/lc-arm64ec.obj" "$OUT/obj/lc-arm64.obj" \
    -out:"$OUT/$id.dll"
done <<< "$SPEC"
