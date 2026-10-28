#!/usr/bin/env bash
# R45W2RestoredArm — adversarial probes of the `restored` classifier.
# Read-only w.r.t. the lane: the interpreter is a byte-identical scratch copy.
set -u
S=/fast/scratch/hyaku/kaidoku-r45/R45W2RestoredArm
export TMPDIR="$S"
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
SRC="$LANE/tools/round-45/frozen-path-preflight.py"
cp "$SRC" "$S/preflight.py"
mkdir -p "$S/receipts"
echo "== interpreter identity =="
sha256sum "$SRC" "$S/preflight.py"
cmp -s "$SRC" "$S/preflight.py"; echo "cmp_exit=$?"

R="$S/receipts"

mk() { # mk <name> -> echoes dir
  local d; d=$(mktemp -d -p "$S" "fx-$1-XXXX")
  git -C "$d" init -q -b main
  git -C "$d" config user.email "seat@restored-arm"
  git -C "$d" config user.name "restored arm"
  echo "$d"
}
top_ok() { # assert toplevel is the fixture
  local d=$1 t; t=$(git -C "$d" rev-parse --show-toplevel)
  if [ "$t" = "$d" ]; then echo "toplevel_ok $d"; else echo "TOPLEVEL_MISMATCH $d -> $t"; exit 9; fi
}
commit() { git -C "$1" add -A && git -C "$1" commit -q -m "$2" && git -C "$1" rev-parse HEAD; }
put() { mkdir -p "$(dirname "$1/$2")"; printf '%s' "$3" > "$1/$2"; }

# run_preflight <label> <dir> <freeze> <rev> [extra args...]
run_preflight() {
  local label=$1 d=$2 f=$3 v=$4; shift 4
  local out="$R/$label.stdout" err="$R/$label.stderr"
  local t0; t0=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  python3 -I -B "$S/preflight.py" --root "$d" --freeze "$f" --rev "$v" "$@" \
      --json-out "$R/$label.json" >"$out" 2>"$err"
  local code=$?
  local sha; sha=$(sha256sum "$out" | cut -d' ' -f1)
  {
    printf 'label=%s\nutc=%s\nroot=%s\nfreeze=%s\nrev=%s\nargs=%s\nexit=%d\nstdout_sha256=%s\n' \
      "$label" "$t0" "$d" "$f" "$v" "$*" "$code" "$sha"
    printf 'stdout=%s\n' "$(cat "$out")"
    if [ -s "$err" ]; then printf 'stderr=%s\n' "$(cat "$err")"; fi
  } > "$R/$label.receipt.txt"
  echo "--- $label exit=$code sha=$sha"
  cat "$out"; echo
  return 0
}

# ---------------------------------------------------------------- M1 main ---
# exact tamper then exact byte restore inside a frozen directory.
D=$(mk m1); top_ok "$D"
put "$D" frozen/a.txt 'alpha
'; put "$D" frozen/b.txt 'beta
'; put "$D" other.txt 'other
'
F=$(commit "$D" freeze)
run_preflight m1-baseline "$D" "$F" "$F" --pathspec frozen/ --freeze-path frozen --require-pathspec
put "$D" frozen/a.txt 'tampered
'
T=$(commit "$D" tamper)
git -C "$D" show "$F:frozen/a.txt" > "$D/frozen/a.txt"
# verify the restored bytes are byte-identical to the freeze blob
git -C "$D" hash-object "$D/frozen/a.txt"; git -C "$D" rev-parse "$F:frozen/a.txt"
R1=$(commit "$D" restore)
run_preflight m1-restored "$D" "$F" "$R1" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "M1_FREEZE=$F M1_TAMPER=$T M1_REV=$R1" > "$R/m1.shas"

# ------------------------------------------------------- (a) trailing NL ----
Da=$(mk a); top_ok "$Da"
put "$Da" frozen/a.txt 'alpha
'; put "$Da" frozen/b.txt 'beta
'; put "$Da" other.txt 'other
'
Fa=$(commit "$Da" freeze)
run_preflight a-baseline "$Da" "$Fa" "$Fa" --pathspec frozen/ --freeze-path frozen --require-pathspec
put "$Da" frozen/a.txt 'tampered
'
commit "$Da" tamper >/dev/null
git -C "$Da" show "$Fa:frozen/a.txt" > "$Da/frozen/a.txt"
printf '\n' >> "$Da/frozen/a.txt"     # FREEZE bytes + one trailing newline
echo "a-bytecheck: freeze_sha=$(git -C "$Da" rev-parse "$Fa:frozen/a.txt") tip_sha=$(git -C "$Da" hash-object "$Da/frozen/a.txt")"
Ra=$(commit "$Da" restore_with_trailing_nl)
run_preflight a-trailing-nl "$Da" "$Fa" "$Ra" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "A_FREEZE=$Fa A_REV=$Ra" > "$R/a.shas"

# ------------------------------------------- (b) tamper BEFORE the freeze ---
Db=$(mk b); top_ok "$Db"
put "$Db" frozen/a.txt 'alpha
'; put "$Db" frozen/b.txt 'beta
'; put "$Db" other.txt 'other
'
C1=$(commit "$Db" initial)
put "$Db" frozen/a.txt 'tampered-before-freeze
'
C2=$(commit "$Db" tamper_before_freeze)
put "$Db" other.txt 'freeze-marker
'
Fb=$(commit "$Db" freeze_after_tamper)   # FREEZE = the tampered state
run_preflight b-baseline "$Db" "$Fb" "$Fb" --pathspec frozen/ --freeze-path frozen --require-pathspec
put "$Db" other.txt 'unrelated
'
Rb=$(commit "$Db" unrelated)
run_preflight b-pre-freeze-tamper "$Db" "$Fb" "$Rb" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "B_C1=$C1 B_C2=$C2 B_FREEZE=$Fb B_REV=$Rb" > "$R/b.shas"

# ------------------------------- (c) added after FREEZE, deleted before REV -
Dc=$(mk c); top_ok "$Dc"
put "$Dc" frozen/a.txt 'alpha
'; put "$Dc" frozen/b.txt 'beta
'; put "$Dc" other.txt 'other
'
Fc=$(commit "$Dc" freeze)
run_preflight c-baseline "$Dc" "$Fc" "$Fc" --pathspec frozen/ --freeze-path frozen --require-pathspec
put "$Dc" frozen/new.txt 'born-after-freeze
'
commit "$Dc" add_after_freeze >/dev/null
rm -f "$Dc/frozen/new.txt"
Rc=$(commit "$Dc" delete_before_rev)
run_preflight c-add-then-delete "$Dc" "$Fc" "$Rc" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "C_FREEZE=$Fc C_REV=$Rc" > "$R/c.shas"

# --------------------------- BONUS squash-merge hiding tamper+restore history
# A side branch tampers and restores; a squash merge folds it to a no-op commit.
Ds=$(mk squash); top_ok "$Ds"
put "$Ds" frozen/a.txt 'alpha
'; put "$Ds" frozen/b.txt 'beta
'; put "$Ds" other.txt 'other
'
Fs=$(commit "$Ds" freeze)
run_preflight s-baseline "$Ds" "$Fs" "$Fs" --pathspec frozen/ --freeze-path frozen --require-pathspec
git -C "$Ds" checkout -q -b side
put "$Ds" frozen/a.txt 'tampered
'
commit "$Ds" side_tamper >/dev/null
git -C "$Ds" show "$Fs:frozen/a.txt" > "$Ds/frozen/a.txt"
commit "$Ds" side_restore >/dev/null
git -C "$Ds" checkout -q main
git -C "$Ds" merge -q --squash side >/dev/null 2>&1
put "$Ds" other.txt 'squashed
'   # the squash result also carries an unrelated path so the merge is not empty
Rs=$(commit "$Ds" squash_merge_of_side)
run_preflight s-squash "$Ds" "$Fs" "$Rs" --pathspec frozen/ --freeze-path frozen --require-pathspec
echo "S_FREEZE=$Fs S_REV=$Rs"
echo "== git history of the squash range =="
git -C "$Ds" log --oneline "$Fs..$Rs"
echo "== files touched per commit in range =="
git -C "$Ds" log -m --diff-merges=first-parent --name-status --format='COMMIT %h' "$Fs..$Rs" -- frozen/
echo "S_FREEZE=$Fs S_REV=$Rs" > "$R/s.shas"

echo "== done =="
