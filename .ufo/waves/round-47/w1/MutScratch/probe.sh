#!/usr/bin/env bash
# R47 scratch-discipline probes. Run from the lane root. Every receipt is written under $S.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r47/MutScratch
R=$S/receipts
mkdir -p "$R"
FREEZE=5017e1f7299c3a812e87e7950148f54313dd279e
REV=caafeffa330a15e59412bc037591f6942b51e5aa
cd "$LANE" || exit 9
MARK=$S/.marker; touch "$MARK"; sleep 1

run() { # run <name> <counter> <envmode> <jsonout> <cwd> [extra]
  local name=$1 counter=$2 envmode=$3 jsonout=$4 cwd=$5
  local case=()
  case "$envmode" in
    good) case=(env "HYAKU_SCRATCH=$S" "TMPDIR=$S") ;;
    tmp)  case=(env -u HYAKU_SCRATCH "TMPDIR=/tmp") ;;
    tmponly_hyaku) case=(env "HYAKU_SCRATCH=/tmp" "TMPDIR=$S") ;;
    none) case=(env -u HYAKU_SCRATCH -u TMPDIR) ;;
  esac
  local tool=tools/round-47/$counter.py
  local args=(python3 -I -B "$LANE/$tool" --root "$LANE" --rev "$REV")
  [ "$counter" = exact ] && args+=(--freeze "$FREEZE")
  [ -n "$jsonout" ] && args+=(--json-out "$jsonout")
  local out=$R/$name.out
  ( cd "$cwd" && "${case[@]}" "${args[@]}" ) >"$out" 2>"$R/$name.err"
  local rc=$?
  printf '%-28s exit=%-2s out_sha=%s err_sha=%s\n' "$name" "$rc" \
    "$(sha256sum "$out" | cut -c1-16)" "$(sha256sum "$R/$name.err" | cut -c1-16)"
  printf '%s\n' "$name|$rc|$envmode|$jsonout|$cwd" >> "$R/exits.txt"
}

echo "== baseline (own scratch root, absolute json-out) =="
run c1-base exact good "$S/c1-base.json" "$LANE"
run c2-base record good "$S/c2-base.json" "$LANE"

echo "== TMPDIR=/tmp, HYAKU_SCRATCH unset =="
run c1-tmpdir-tmp exact tmp "$S/c1-tmpdir-tmp.json" "$LANE"
run c2-tmpdir-tmp record tmp "$S/c2-tmpdir-tmp.json" "$LANE"

echo "== no HYAKU_SCRATCH, no TMPDIR =="
run c1-no-root exact none "$S/c1-no-root.json" "$LANE"
run c2-no-root record none "$S/c2-no-root.json" "$LANE"

echo "== HYAKU_SCRATCH=/tmp while TMPDIR=$S =="
run c1-hyaku-tmp exact tmponly_hyaku "$S/c1-hyaku-tmp.json" "$LANE"
run c2-hyaku-tmp record tmponly_hyaku "$S/c2-hyaku-tmp.json" "$LANE"

echo "== relative --json-out from lane root =="
run c1-rel-lane exact good "r47probe-c1-rel.json" "$LANE"
run c2-rel-lane record good "r47probe-c2-rel.json" "$LANE"
echo "lane-root residue: $(ls -l "$LANE"/r47probe-c*.json 2>/dev/null | wc -l) file(s)"
for f in "$LANE"/r47probe-c1-rel.json "$LANE"/r47probe-c2-rel.json; do
  [ -f "$f" ] && { echo "RESIDUE $f sha=$(sha256sum "$f" | cut -c1-16)"; mv "$f" "$R/$(basename "$f")"; }
done

echo "== relative --json-out from scratch cwd =="
run c1-rel-scratch exact good "rel-c1.json" "$S"
run c2-rel-scratch record good "rel-c2.json" "$S"
echo "scratch residue: $(ls "$S"/rel-c*.json 2>/dev/null | wc -l) file(s)"

echo "== --json-out on graded surfaces =="
for t in SKILL.md SCORECARD.md LOG.md ./SKILL.md tools/round-47/exact.py plans/round-47-claims.md .ufo/waves/round-47/w1/MutScratch/x.json; do
  safe=$(printf '%s' "$t" | tr '/.' '__')
  run "c1-graded-$safe" exact good "$t" "$LANE"
done
run c2-graded-skill record good SKILL.md "$LANE"

echo "== symlink to a graded file =="
ln -sfn "$LANE/SKILL.md" "$S/link-to-skill.json"
run c1-symlink exact good "$S/link-to-skill.json" "$LANE"
run c2-symlink record good "$S/link-to-skill.json" "$LANE"

echo "== --json-out is a directory =="
mkdir -p "$S/adir"
run c1-jsonout-dir exact good "$S/adir" "$LANE"
run c2-jsonout-dir record good "$S/adir" "$LANE"

echo "== --json-out empty string =="
run c1-jsonout-empty exact good "" "$LANE"

echo "== /tmp residue after all probes =="
find /tmp -maxdepth 2 \( -name 'kaidoku-r47-*' -o -name 'fx-*' -o -name 'repo-*' \) -newer "$MARK" 2>/dev/null | sed 's/^/  TEMPRESIDUE /' || true
echo "== done =="
