#!/bin/sh
# Reproduce R39C2ReconDep (round 39 wave 1, C2 dependency-outcome recon).
#
# Tools (measured 2026-10-26): unblob 26.6.4 (~/.local/bin, uv tool),
# sasquatch 4.5.1 and sasquatch-v4be 4.5.1 (~/.local/bin), rea-agents 6.5.0 (npx),
# node/npx from the interactive shell PATH (NOT ~/.local/bin).
# Nothing here writes inside the lane: carriers, outdirs and logs land in $S.
set -eu
LANE=${LANE:-/home/vgpnk/Projects/shokunin/kaidoku-shokunin}
GEN="$LANE/tools/round-37/gen-squashfs.py"
ART=${ART:-$LANE/.ufo/waves/round-39/w1/artifacts/R39C2ReconDep}
S=${S:-/fast/scratch/hyaku/kaidoku-r39/R39C2ReconDep}
NPX=${NPX:-$(command -v npx)}
STRIPPED_PATH=/usr/local/bin:/usr/bin:/bin     # ~/.local/bin removed: no sasquatch*
export TMPDIR="$S"
mkdir -p "$S/tree" "$S/img" "$S/logs" "$S/out"

# ---------------- source trees (fresh, authored here) ----------------
mkdir -p "$S/tree/be1/bin" "$S/tree/be1/docs/deep/nested" "$S/tree/be1/var/lib"
printf '#!/bin/sh\necho be1\n' > "$S/tree/be1/bin/run"; chmod +x "$S/tree/be1/bin/run"
printf 'hello from be1\n' > "$S/tree/be1/hello.txt"
printf '# be1 readme\n' > "$S/tree/be1/docs/readme.md"
head -c 9000 /dev/zero | tr '\0' 'A' > "$S/tree/be1/docs/deep/nested/payload.bin"
printf 'be1 var\n' > "$S/tree/be1/var/lib/data.cfg"
: > "$S/tree/be1/empty"

mkdir -p "$S/tree/be2/etc" "$S/tree/be2/usr/share/doc"
printf 'be2 alpha\n' > "$S/tree/be2/alpha.txt"
head -c 5000 /dev/zero | tr '\0' 'B' > "$S/tree/be2/etc/big.dat"
printf 'be2 doc\n' > "$S/tree/be2/usr/share/doc/notes.txt"

mkdir -p "$S/tree/le1/app/assets"
printf 'le1 main\n' > "$S/tree/le1/app/main.txt"
head -c 6000 /dev/zero | tr '\0' 'C' > "$S/tree/le1/app/assets/blob.dat"
printf 'le1 cfg\n' > "$S/tree/le1/app/cfg.ini"

mkdir -p "$S/tree/le2/srv/data"
printf 'le2 a\n' > "$S/tree/le2/srv/a.txt"
: > "$S/tree/le2/srv/data/zero.bin"
printf 'le2 last\n' > "$S/tree/le2/last.log"

mkdir -p "$S/tree/be-sym/docs/deep" "$S/tree/be-sym/lib"          # in-tree symlinks, file targets
printf 'be-sym target\n' > "$S/tree/be-sym/hello.txt"
printf 'be-sym flat\n' > "$S/tree/be-sym/lib/flat.txt"
printf 'be-sym root\n' > "$S/tree/be-sym/root.txt"
ln -s ../../hello.txt "$S/tree/be-sym/docs/deep/in-tree-link"
ln -s ../lib/flat.txt "$S/tree/be-sym/docs/flat-link"

mkdir -p "$S/tree/be-esc/docs"                                    # escaping symlink
printf 'be-esc doc\n' > "$S/tree/be-esc/docs/note.txt"
printf 'be-esc root\n' > "$S/tree/be-esc/root.txt"
printf 'be-esc lib\n' > "$S/tree/be-esc/keep.txt"
ln -s ../outside.txt "$S/tree/be-esc/escape-link"

mkdir -p "$S/tree/be-dirempty/onlydir"                            # zero publishable files
mkdir -p "$S/input"; head -c 1024 /dev/urandom > "$S/input/not-squashfs.bin"

# ---------------- carriers ----------------
python3 "$GEN" "$S/tree/be1"       "$S/img/be1-gzip.sqsh"       --endian be  --comp gzip
python3 "$GEN" "$S/tree/be2"       "$S/img/be2-gzip.sqsh"       --endian be  --comp gzip
python3 "$GEN" "$S/tree/le1"       "$S/img/le1-gzip.sqsh"       --endian le  --comp gzip
python3 "$GEN" "$S/tree/le2"       "$S/img/le2-gzip.sqsh"       --endian le  --comp gzip
python3 "$GEN" "$S/tree/be-sym"    "$S/img/be-sym-gzip.sqsh"    --endian be  --comp gzip
python3 "$GEN" "$S/tree/be-esc"    "$S/img/be-esc-gzip.sqsh"    --endian be  --comp gzip
python3 "$GEN" "$S/tree/be-dirempty" "$S/img/be-dirempty-gzip.sqsh" --endian be --comp gzip
python3 "$GEN" "$S/tree/be1"       "$S/img/be1-xz.sqsh"         --endian be  --comp xz
python3 "$GEN" "$S/tree/le1"       "$S/img/le1-xz.sqsh"         --endian le  --comp xz
python3 "$ART/make-avm-copy.py"    "$S/img/be1-gzip.sqsh"       "$S/img/be1-avm.sqsh"
python3 "$GEN" "$S/tree/be1"       "$S/img/be1-avm-native.sqsh" --endian avm --comp gzip
python3 "$ART/make-corrupt-copy.py" "$S/img/be1-gzip.sqsh"      "$S/img/be1-corrupt.sqsh"
python3 "$ART/make-corrupt-copy.py" "$S/img/le1-gzip.sqsh"      "$S/img/le1-corrupt.sqsh"

# ---------------- REA runs ----------------
rea() {  # rea <mode:full|stripped> <name> <input>
  mode=$1; name=$2; in=$3
  rm -rf "$S/out/$mode/$name"
  if [ "$mode" = stripped ]; then
    env PATH=$STRIPPED_PATH REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" "$NPX" -y rea-agents@6.5.0 \
        extract-firmware --format json --full-output "$in" "$S/out/$mode/$name" \
        > "$S/logs/stripped-$name.json" 2> "$S/logs/stripped-$name.err"
  else
    REA_UNBLOB_COMMAND="$HOME/.local/bin/unblob" "$NPX" -y rea-agents@6.5.0 \
        extract-firmware --format json --full-output "$in" "$S/out/full/$name" \
        > "$S/logs/full-$name.json" 2> "$S/logs/full-$name.err"
  fi
  echo "$mode $name exit=$? files=$(find "$S/out/$mode/$name" -type f | wc -l)"
}
# development controls (extractors reachable)
for n in be1-gzip be2-gzip le1-gzip le2-gzip be-sym-gzip be-esc-gzip be-dirempty-gzip \
         be1-avm be1-avm-native be1-corrupt le1-corrupt be1-xz le1-xz; do
  rea full "$n" "$S/img/$n.sqsh"
done
rea full not-squashfs "$S/input/not-squashfs.bin"
# dependency-missing runs (~/.local/bin stripped, REA_UNBLOB_COMMAND absolute)
for n in be1-gzip be2-gzip le1-gzip le2-gzip be-sym-gzip be-esc-gzip be1-avm; do
  rea stripped "$n" "$S/img/$n.sqsh"
done
# determinism repeat
rea stripped be1-gzip-repeat "$S/img/be1-gzip.sqsh"

# ---------------- feature extraction ----------------
python3 "$ART/sqfs-triage-dev.py" --table "$ART/candidate-triage-rows.md" \
  $(for f in "$S"/logs/*.json; do printf -- '--envelope %s ' "$f"; done) \
  --json-out "$S/dev-scored.json"
echo "scratch: $S"
