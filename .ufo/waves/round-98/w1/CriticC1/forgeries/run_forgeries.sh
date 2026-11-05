#!/bin/bash
# CriticC1: score each forgery and the identity control with the frozen battery.
S=/fast/scratch/hyaku/kaidoku-r98/CriticC1
C=$S/clone/tools/round-98/pe-upx-tamper-battery.py
REV=72346895a35a74af18151b125934fa0c09fe1e3c
mkdir -p "$S/out" "$S/w" "$S/cache_sized"
# size-keyed cache from the six untampered packs produced by the battery (probe1 cache)
for n in t32 t64 w32 w64 winhello fastlist64; do
  sz=$(stat -c %s "$S/w/base/$n.upx"); cp "$S/w/base/$n.upx" "$S/cache_sized/$sz.upx"
done
export CRITIC_CACHE="$S/cache_sized"
declare -A CMDS=(
  [identity]="$S/clone/tools/round-98/controls/identity-copy.py"
  [real]="$S/clone/tools/round-98/upx-pe-repair.py"
  [f1_fixed_offset]="$S/f1_fixed_offset.py"
  [f2_size_cache]="$S/f2_size_cache.py"
  [f3_names_only]="$S/f3_names_only.py"
  [f4_magic_only]="$S/f4_magic_only.py"
  [f5_refuser]="$S/f5_refuser.py"
  [f6_shotgun]="$S/f6_shotgun.py"
  [f7_lazy_anchor]="$S/f7_lazy_anchor.py"
)
for k in identity real f1_fixed_offset f2_size_cache f3_names_only f4_magic_only f5_refuser f6_shotgun f7_lazy_anchor; do
  w="$S/w/$k"; mkdir -p "$w"
  python3 -I -B "$C" --repair-cmd "${CMDS[$k]}" --work "$w" --json-out "$S/out/$k.json" --rev "$REV" > "$S/out/$k.stdout" 2>"$S/out/$k.stderr"
  rc=$?
  lab=$(head -1 "$S/out/$k.stdout")
  echo "$k | exit=$rc | $lab | stderr=$(tail -1 "$S/out/$k.stderr")"
done
