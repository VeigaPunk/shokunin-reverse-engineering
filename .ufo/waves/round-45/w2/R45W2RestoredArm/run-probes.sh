#!/usr/bin/env bash
# Follow-up probes: (d) mode-only tamper, (e) chmod+restore, plus mutants of the
# scratch copy proving what M1 does and does not kill.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RestoredArm
export TMPDIR="$S"
R="$S/receipts"

mk() { local d; d=$(mktemp -d -p "$S" "fx-$1-XXXX"); git -C "$d" init -q -b main
  git -C "$d" config user.email "seat@restored-arm"; git -C "$d" config user.name "restored arm"; echo "$d"; }
top_ok() { local d=$1 t; t=$(git -C "$d" rev-parse --show-toplevel)
  [ "$t" = "$d" ] && echo "toplevel_ok $d" || { echo "TOPLEVEL_MISMATCH $d -> $t"; exit 9; }; }
commit() { git -C "$1" add -A && git -C "$1" commit -q -m "$2" && git -C "$1" rev-parse HEAD; }
put() { mkdir -p "$(dirname "$1/$2")"; printf '%s' "$3" > "$1/$2"; }

run_pf() { # run_pf <label> <python> <dir> <freeze> <rev> [extra...]
  local label=$1 py=$2 d=$3 f=$4 v=$5; shift 5
  local out="$R/$label.stdout" err="$R/$label.stderr" t0; t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  python3 -I -B "$py" --root "$d" --freeze "$f" --rev "$v" "$@" --json-out "$R/$label.json" >"$out" 2>"$err"
  local code=$?; local sha; sha=$(sha256sum "$out" | cut -d' ' -f1)
  { printf 'label=%s\nutc=%s\ninterpreter=%s\nroot=%s\nfreeze=%s\nrev=%s\nargs=%s\nexit=%d\nstdout_sha256=%s\n' \
      "$label" "$t0" "$py" "$d" "$f" "$v" "$*" "$code" "$sha"
    printf 'stdout=%s\n' "$(cat "$out")"; [ -s "$err" ] && printf 'stderr=%s\n' "$(cat "$err")"; } > "$R/$label.receipt.txt"
  echo "--- $label exit=$code sha=$sha"; cat "$out"; echo; }

# ---------------------------------------------------------- (d) mode-only ---
Dd=$(mk d); top_ok "$Dd"
put "$Dd" frozen/a.txt 'alpha
'; put "$Dd" frozen/b.txt 'beta
'; put "$Dd" other.txt 'other
'
Fd=$(commit "$Dd" freeze)
run_pf d-baseline "$S/preflight.py" "$Dd" "$Fd" "$Fd" --pathspec frozen/ --freeze-path frozen --require-pathspec
chmod +x "$Dd/frozen/a.txt"            # mode 100644 -> 100755, content untouched
Md=$(commit "$Dd" chmod_only_tamper)
echo "d-mode: freeze_mode=$(git -C "$Dd" ls-tree "$Fd" frozen/a.txt | awk '{print $1}') rev_mode=$(git -C "$Dd" ls-tree "$Md" frozen/a.txt | awk '{print $1}')"
echo "d-blob: freeze=$(git -C "$Dd" rev-parse "$Fd:frozen/a.txt") rev=$(git -C "$Dd" rev-parse "$Md:frozen/a.txt")"
run_pf d-chmod-only "$S/preflight.py" "$Dd" "$Fd" "$Md" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "D_FREEZE=$Fd D_REV=$Md" > "$R/d.shas"

# ------------------------------------------------ (e) chmod then restore ----
De=$(mk e); top_ok "$De"
put "$De" frozen/a.txt 'alpha
'; put "$De" frozen/b.txt 'beta
'; put "$De" other.txt 'other
'
Fe=$(commit "$De" freeze)
run_pf e-baseline "$S/preflight.py" "$De" "$Fe" "$Fe" --pathspec frozen/ --freeze-path frozen --require-pathspec
put "$De" frozen/a.txt 'tampered
'; chmod +x "$De/frozen/a.txt"
commit "$De" tamper_and_chmod >/dev/null
git -C "$De" show "$Fe:frozen/a.txt" > "$De/frozen/a.txt"   # content restored, mode left 755
Re=$(commit "$De" restore_content_only)
echo "e-mode: freeze=$(git -C "$De" ls-tree "$Fe" frozen/a.txt | awk '{print $1}') rev=$(git -C "$De" ls-tree "$Re" frozen/a.txt | awk '{print $1}')"
run_pf e-restore-content-only "$S/preflight.py" "$De" "$Fe" "$Re" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "E_FREEZE=$Fe E_REV=$Re" > "$R/e.shas"

# ------------------------------------------------------------- mutants ------
# mu1: drop the restored branch (the exact mutation the round-45 lesson names).
python3 - <<'PY'
src = open('/fast/scratch/hyaku/kaidoku-r45/R45W2RestoredArm/preflight.py').read()
old = "        elif any(t[\"path\"] == path for t in touched):\n            restored.append(path)"
assert src.count(old) == 1, src.count(old)
open('/fast/scratch/hyaku/kaidoku-r45/R45W2RestoredArm/preflight-mu1.py','w').write(
    src.replace(old, "        elif False:\n            restored.append(path)"))
# mu2: tip-equality classifier (no commit-history predicate) — the round-44 defect.
old2 = "        elif any(t[\"path\"] == path for t in touched):\n            restored.append(path)"
open('/fast/scratch/hyaku/kaidoku-r45/R45W2RestoredArm/preflight-mu2.py','w').write(
    src.replace(old2, "        else:\n            restored.append(path)"))
PY
sha256sum "$S/preflight-mu1.py" "$S/preflight-mu2.py" | tee "$R/mutants.sha256"

Dm=$(mk mk); top_ok "$Dm"
put "$Dm" frozen/a.txt 'alpha
'; put "$Dm" frozen/b.txt 'beta
'; put "$Dm" other.txt 'other
'
Fm=$(commit "$Dm" freeze)
put "$Dm" frozen/a.txt 'tampered
'
commit "$Dm" tamper >/dev/null
git -C "$Dm" show "$Fm:frozen/a.txt" > "$Dm/frozen/a.txt"
Rm=$(commit "$Dm" restore)
echo "MUT_FREEZE=$Fm MUT_REV=$Rm" > "$R/mut.shas"
# the same M1 detector, on pristine / mu1 / mu2 bytes
run_pf mut-pristine-on-m1 "$S/preflight.py"     "$Dm" "$Fm" "$Rm" --pathspec frozen/ --freeze-path frozen --require-pathspec
run_pf mut-mu1-on-m1    "$S/preflight-mu1.py"   "$Dm" "$Fm" "$Rm" --pathspec frozen/ --freeze-path frozen --require-pathspec
run_pf mut-mu2-on-m1    "$S/preflight-mu2.py"   "$Dm" "$Fm" "$Rm" --pathspec frozen/ --freeze-path frozen --require-pathspec
# the clean control: no touch at all, must be exit 0
run_pf mut-pristine-clean "$S/preflight.py"   "$Dm" "$Fm" "$Fm" --pathspec frozen/ --freeze-path frozen --require-pathspec
run_pf mut-mu2-clean       "$S/preflight-mu2.py" "$Dm" "$Fm" "$Fm" --pathspec frozen/ --freeze-path frozen --require-pathspec
# mu1 on the clean control too
run_pf mut-mu1-clean       "$S/preflight-mu1.py" "$Dm" "$Fm" "$Fm" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "== done =="
