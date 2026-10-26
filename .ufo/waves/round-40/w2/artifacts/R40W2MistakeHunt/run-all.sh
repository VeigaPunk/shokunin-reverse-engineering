#!/bin/sh
# Reproduce every MH-* red/green run cited in ../R40W2MistakeHunt.md.
# Run from anywhere; writes only $S (scratch) and stdout.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
A="$LANE/.ufo/waves/round-40/w2/artifacts/R40W2MistakeHunt"
S=/fast/scratch/hyaku/kaidoku-r40/R40W2MistakeHunt
REV=42c10a58cb2cae3a4a0122af35a0cf95ac718043
mkdir -p "$S"

run() {
    printf '\n$ %s\n' "$*"
    "$@" 2>&1
    printf 'exit=%d\n' "$?"
}

echo "# environment"
printf '$ python3 -V\n'; python3 -V
printf '$ unblob --version\n'; "$HOME/.local/bin/unblob" --version 2>&1 | head -1
printf '$ sasquatch-v4be -version\n'; sasquatch-v4be -version 2>&1 | head -2
printf '$ node -v\n'; node -v
printf '$ git -C LANE rev-parse HEAD\n'; git -C "$LANE" rev-parse HEAD
printf '$ python3 -c "import sys;print(sys.version)"\n'; python3 -c 'import sys;print(sys.version)'

echo
echo "# MH-1  one path helper, two domains (publication + gap resolution)"
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher frozen --oracle
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --oracle
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher frozen --control materialised --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --control materialised --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --control deeper --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher frozen --control wrong-root --oracle --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --control wrong-root --oracle --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher frozen --gaps
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --gaps
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher frozen --gaps --control bogus-gap --ids L2
run python3 -I -B "$A/mh1-suffix-domain.py" --root "$LANE" --rev "$REV" --matcher exact --gaps --control bogus-gap --ids L2

echo
echo "# MH-2  candidate reservation (a pick is not a reserved input)"
run python3 -I -B "$A/mh2-candidate-reservation.py" --reserved "$LANE/.ufo/waves/round-40/c1/carriers.json" --scan "$LANE/.ufo/waves/round-40/w1/artifacts"
run python3 -I -B "$A/mh2-candidate-reservation.py" --reserved "$A/rig-draft-7430.json" --scan "$LANE/.ufo/waves/round-40/w1/artifacts"

echo
echo "# MH-3  report placement / duplicate authority"
run python3 -I -B "$A/mh3-report-placement.py" --wave "$LANE/.ufo/waves/round-40/w1"
run python3 -I -B "$A/mh3-report-placement.py" --wave "$LANE/.ufo/waves/round-40/w1" --fixture-move "$S/fx-w1"
rm -f "$S/fx-w1/R40SrcFreetz.md"
run python3 -I -B "$A/mh3-report-placement.py" --wave "$S/fx-w1"

echo
echo "# MH-4  recipe fit: fill byte x compressor (zero fill vs 0xFF)"
rm -rf "$S/mh4"
run python3 -I -B "$A/mh4-recipe-fit.py" --work "$S/mh4" --shapes s1,s2,s3,h1,h2 --fills 00 --comps gzip,xz --expect partial-body-failure
run python3 -I -B "$A/mh4-recipe-fit.py" --work "$S/mh4" --shapes s1,s2,s3,h1,h2 --fills ff --comps gzip,xz --expect partial-body-failure

echo
echo "# MH-5  vendor-restricted payload pins"
rm -rf "$S/fx-vendor"; mkdir -p "$S/fx-vendor/artifacts/R40C1VendorV1"
python3 -c "open('$S/fx-vendor/artifacts/R40C1VendorV1/carrier-v1-be.sqsh','wb').truncate(5442392)"
python3 -c "
import hashlib,json
h=hashlib.sha256(open('$S/fx-vendor/artifacts/R40C1VendorV1/carrier-v1-be.sqsh','rb').read()).hexdigest()
json.dump({'pins':[{'id':'fixture-vendor-bytes','sha256':h,'length':5442392}]}, open('$A/rig-vendor-fixture.json','w'), indent=1)
print('fixture sha256', h)"
run python3 -I -B "$A/mh5-vendor-bytes.py" --rig "$A/rig-vendor-fixture.json" --root "$S/fx-vendor"
rm -f "$S/fx-vendor/artifacts/R40C1VendorV1/carrier-v1-be.sqsh"
run python3 -I -B "$A/mh5-vendor-bytes.py" --rig "$A/rig-vendor-fixture.json" --root "$S/fx-vendor"
run python3 -I -B "$A/mh5-vendor-bytes.py" --rig "$A/rig-vendor-pins.json" --root "$LANE" --git
rm -rf "$S/fx-git"; mkdir -p "$S/fx-git"
( cd "$S/fx-git" && git init -q . && test "$(git rev-parse --show-toplevel)" = "$(pwd -P)" \
  && python3 -c "open('carrier-v1-be.sqsh','wb').truncate(5442392)" \
  && git add carrier-v1-be.sqsh \
  && git -c user.name=fx -c user.email=fx@fx commit -qm "fixture: same-length dummy" \
  && echo "fixture repo ready: $(git rev-parse --short HEAD)" )
run python3 -I -B "$A/mh5-vendor-bytes.py" --rig "$A/rig-vendor-fixture.json" --root "$S/fx-git" --git

echo
echo "# lane state at the time of these runs"
git -C "$LANE" status --porcelain
