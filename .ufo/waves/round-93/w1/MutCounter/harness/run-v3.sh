#!/usr/bin/env bash
# MutCounter v3 batch. Each run: fresh --work, TMPDIR under scratch, no --json-out (frozen crash), stdout+stderr+exit captured.
S=/fast/scratch/hyaku/kaidoku-r93/MutCounter; C=$S/clone; MT=$S/mut-tree; O=$S/out/v3; H=$S/harness
mkdir -p "$O"; export TMPDIR=$S/tmp
SHA=92a240521bd1bf2213b75d18d9b176a8dafdc67c
FROZ='repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2'
FORGED='repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12'
cd "$S"
run() { # id, description, command...
  local id=$1; shift; local desc=$1; shift
  "$@" > "$O/$id.out" 2> "$O/$id.err"; local rc=$?
  echo "$rc" > "$O/$id.rc"
  printf '%-22s exit=%s | %s | %s\n' "$id" "$rc" "$desc" "$(tail -1 "$O/$id.out" | cut -c1-200)"
}
# full-pipeline plain runs (frozen expect)
for m in orig M1 M2 M5a M5b M7; do
  f=$MT/tools/round-93/$([ $m = orig ] && echo orig-v3 || echo $m).py
  run "plain-$m" "frozen expect" python3 -I -B "$f" --root "$MT" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work/plain-$m" --rev $SHA --expect "$FROZ"
done
# M6: forged expect that is a substring of the frozen label
run "forged-orig" "forged expect (substring)" python3 -I -B "$MT/tools/round-93/orig-v3.py" --root "$MT" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work/forged-orig" --rev $SHA --expect "$FORGED"
run "forged-M6" "forged expect (substring)" python3 -I -B "$MT/tools/round-93/M6.py" --root "$MT" --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work/forged-M6" --rev $SHA --expect "$FORGED"
# injections (same harness for honest and mutant)
for m in orig M3; do run "inj-m3-$m" "second pack differs" python3 -I -B "$H/inject.py" --mode m3 --counter "$MT/tools/round-93/$([ $m = orig ] && echo orig-v3 || echo $m).py" --root "$MT" --clone "$C" --work "$S/work/inj-m3-$m" --expect "$FROZ"; done
for m in orig M4; do run "inj-m4-$m" "fresh pack collides with public image" python3 -I -B "$H/inject.py" --mode m4 --counter "$MT/tools/round-93/$([ $m = orig ] && echo orig-v3 || echo $m).py" --root "$MT" --clone "$C" --work "$S/work/inj-m4-$m" --expect "$FROZ"; done
for m in orig M5a M5b; do run "inj-m5none-$m" "roundtrip_sha returns None" python3 -I -B "$H/inject.py" --mode m5none --counter "$MT/tools/round-93/$([ $m = orig ] && echo orig-v3 || echo $m).py" --root "$MT" --clone "$C" --work "$S/work/inj-m5none-$m" --expect "$FROZ"; done
for m in orig M7; do run "inj-m7-$m" "fresh intact answered with altered bytes" python3 -I -B "$H/inject.py" --mode m7 --counter "$MT/tools/round-93/$([ $m = orig ] && echo orig-v3 || echo $m).py" --root "$MT" --clone "$C" --work "$S/work/inj-m7-$m" --expect "$FROZ"; done
# M2 forger probe: constant-nonce fresh image pinned by F4
run "f4-orig" "F4 constant-nonce pin vs honest random nonce" python3 -I -B "$H/inject.py" --mode f4 --counter "$MT/tools/round-93/orig-v3.py" --root "$MT" --clone "$C" --work "$S/work/f4-orig" --expect "$FROZ"
run "f4-M2" "F4 constant-nonce pin vs M2 constant nonce" python3 -I -B "$H/inject.py" --mode f4 --counter "$MT/tools/round-93/M2.py" --root "$MT" --clone "$C" --work "$S/work/f4-M2" --expect "$FROZ"
