#!/usr/bin/env bash
# Probe matrix v2: --json-out inside the lane only (the only accepted target), stdout receipts hashed.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
S=/fast/scratch/hyaku/kaidoku-r47/MutScratch
R=$S/r2; mkdir -p "$R"
OUTD=$LANE/.ufo/waves/round-47/w1/MutScratch     # my own report dir: the only legal --json-out target
mkdir -p "$OUTD"
REV=caafeffa330a15e59412bc037591f6942b51e5aa
F_PROMPT=5017e1f7299c3a812e87e7950148f54313dd279e
F_A4=1e2c3102952dc636650095643c1963c833859019
MARK=$S/.marker2; touch "$MARK"; sleep 1
cd "$LANE" || exit 9

run() { # name counter envmode jsonout freeze
  local name=$1 counter=$2 envmode=$3 jsonout=$4 freeze=${5:-}
  local e=()
  case "$envmode" in
    good) e=(env "HYAKU_SCRATCH=$S" "TMPDIR=$S") ;;
    tmp)  e=(env -u HYAKU_SCRATCH "TMPDIR=/tmp") ;;
    hyaku_tmp) e=(env "HYAKU_SCRATCH=/tmp" "TMPDIR=$S") ;;
    none) e=(env -u HYAKU_SCRATCH -u TMPDIR) ;;
  esac
  local args=(python3 -I -B "$LANE/tools/round-47/$counter.py" --root "$LANE" --rev "$REV")
  [ "$counter" = exact ] && args+=(--freeze "$freeze")
  [ "${jsonout+set}" = set ] && [ -n "$jsonout" ] && args+=(--json-out "$jsonout")
  ( "${e[@]}" "${args[@]}" ) >"$R/$name.out" 2>"$R/$name.err"
  local rc=$?
  local sha; sha=$(sha256sum "$R/$name.out" | cut -c1-16)
  local reason; reason=$(python3 - "$R/$name.out" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: print("NONJSON"); raise SystemExit
print(str(d.get("reason") or ("failing="+str(d.get("failing")) if d.get("failing") else
      "ok failing=[] battery="+str({k:v for k,v in (d.get("battery") or {}).items() if k!="fixtures"})))[:200])
PY
)
  printf '%-26s exit=%-2s sha=%s  %s\n' "$name" "$rc" "$sha" "$reason"
  printf '%s|%s|%s|%s|%s\n' "$name" "$rc" "$envmode" "$jsonout" "$reason" >> "$R/exits.txt"
}

echo "== C1 freeze=$F_A4 (no drift), env modes =="
run c1-good-a4 exact good "" "$F_A4"
run c1-tmpdir-a4 exact tmp "" "$F_A4"
run c1-noroot-a4 exact none "" "$F_A4"
run c1-hyakutmp-a4 exact hyaku_tmp "" "$F_A4"
echo "== C1 freeze=$F_PROMPT (drift) =="
run c1-good-prompt exact good "" "$F_PROMPT"
run c1-tmpdir-prompt exact tmp "" "$F_PROMPT"
echo "== C2 =="
run c2-good record good ""
run c2-tmpdir record tmp ""
run c2-noroot record none ""
run c2-hyakutmp record hyaku_tmp ""
echo "== json-out into own report dir (legal target) =="
run c1-jsonout-own exact good "$OUTD/c1-own.json" "$F_A4"
run c2-jsonout-own record good "$OUTD/c2-own.json"
echo "== json-out into own report dir, TMPDIR=/tmp =="
run c1-jsonout-tmp exact tmp "$OUTD/c1-own-tmp.json" "$F_A4"
run c2-jsonout-tmp record tmp "$OUTD/c2-own-tmp.json"
echo "== relative json-out from lane root: untracked residue test =="
run c1-rel-lane2 exact good "r47p2-c1.json" "$F_A4"
run c2-rel-lane2 record good "r47p2-c2.json"
for f in "$LANE"/r47p2-c1.json "$LANE"/r47p2-c2.json; do
  [ -f "$f" ] && { echo "RESIDUE $f sha=$(sha256sum "$f"|cut -c1-16)"; mv "$f" "$R/"; }
done
echo "== git status: new untracked entries after probes =="
git status --porcelain --untracked-files=all | grep -v '^ M \.ufo\|^?? \.ufo' | sed 's/^/  STATUS /'
echo "== /tmp residue =="
find /tmp -maxdepth 2 \( -name 'kaidoku-r47*' -o -name 'fx-*' -o -name 'repo-*' \) -newer "$MARK" 2>/dev/null | sed 's/^/  TEMPRESIDUE /'
echo done
