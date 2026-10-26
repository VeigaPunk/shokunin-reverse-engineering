#!/usr/bin/env bash
# R41W2SrcReopen — exact commands run for the live re-open of SOURCES rows S127/S128.
# Scratch: S=/fast/scratch/hyaku/kaidoku-r41/R41W2SrcReopen (removed after the seat finished;
#          it is re-creatable, one fetch produces every byte the checker reads).
# Lane:    L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin   (read-only git only)
# Nothing here writes outside S and the seat artifact dir. No VCS mutation. No REA/unblob run.
set -u
S=${S:-/fast/scratch/hyaku/kaidoku-r41/R41W2SrcReopen}
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
A=$L/.ufo/waves/round-41/w2/artifacts/R41W2SrcReopen
mkdir -p "$S/s127" "$S/s128"; cd "$S"

# 1. frozen rows (read-only)
git -C "$L" show e9a24d07256d1606f01aa4d2d65f74e649c5f3d4:corpus/SOURCES.md > "$S/SOURCES-e9a24d07.md"

# 2. S127 (5490) — listing, both info files, image HEAD; then sha256 + size
U=https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/
curl -sS --max-time 60 -o s127/listing.html -D s127/listing.hdr -w 'listing %{http_code} %{size_download}\n' "$U"
curl -sS --max-time 60 -o s127/info_en.txt  -D s127/info_en.hdr  -w 'info_en %{http_code} %{size_download}\n' "${U}info_en.txt"
curl -sS --max-time 60 -o s127/info_de.txt  -D s127/info_de.hdr  -w 'info_de %{http_code} %{size_download}\n' "${U}info_de.txt"
curl -sSI --max-time 60 -D s127/image.head -o /dev/null -w 'HEAD %{http_code}\n' "${U}FRITZ.Box_5490-07.31.image"
sha256sum s127/listing.html s127/info_en.txt s127/info_de.txt

# 3. S128 (5491) — same set
U=https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/
curl -sS --max-time 60 -o s128/listing.html -D s128/listing.hdr -w 'listing %{http_code} %{size_download}\n' "$U"
curl -sS --max-time 60 -o s128/info_en.txt  -D s128/info_en.hdr  -w 'info_en %{http_code} %{size_download}\n' "${U}info_en.txt"
curl -sS --max-time 60 -o s128/info_de.txt  -D s128/info_de.hdr  -w 'info_de %{http_code} %{size_download}\n' "${U}info_de.txt"
curl -sSI --max-time 60 -D s128/image.head -o /dev/null -w 'HEAD %{http_code}\n' "${U}FRITZ.Box_5491-07.31.image"
sha256sum s128/listing.html s128/info_en.txt s128/info_de.txt

# 4. second fetch of every GET body the rows hash (stability, second independent pair)
for m in 5490 5491; do
  d=$([ "$m" = 5490 ] && echo s127 || echo s128)
  B=https://download.avm.de/fritzbox/fritzbox-$m/other/fritz.os/
  curl -sS --max-time 60 -o $d/info_en.2.txt    "$B/info_en.txt"
  curl -sS --max-time 60 -o $d/listing.2.html   "$B"
done

# 5. conditional GET on the info files (validator stability)
curl -sS -o /dev/null -w '%{http_code}\n' -H 'If-None-Match: "673b48d5-c5dd"' \
  https://download.avm.de/fritzbox/fritzbox-5490/other/fritz.os/info_en.txt
curl -sS -o /dev/null -w '%{http_code}\n' -H 'If-None-Match: "673b48a0-cfae"' \
  https://download.avm.de/fritzbox/fritzbox-5491/other/fritz.os/info_en.txt

# 6. vendor image bodies, hashed and deleted in place (licence: no redistribution, no retention)
for m in 5490 5491; do
  curl -sS --max-time 300 -o "img-$m.bin" -w "$m %{http_code} %{size_download}\n" \
    "https://download.avm.de/fritzbox/fritzbox-$m/other/fritz.os/FRITZ.Box_$m-07.31.image"
  sha256sum "img-$m.bin"; stat -c '%n %s' "img-$m.bin"
done
rm -f img-5490.bin img-5491.bin      # only the digests survive (vendor-image-digests.txt)

# 7. re-derive every row claim from those bytes (exit 0 = all checks pass)
python3 -I -B "$A/check-reopen.py" --sources "$S/SOURCES-e9a24d07.md" --dir "$S" \
  --carriers "$L/.ufo/waves/round-41/c1/carriers.json" | tee "$A/check-reopen-output.txt"
echo "checker exit=$?"      # observed 0, 89 PASS, 0 FAIL

# 8. registry shape / novelty / used-by checks -> row-shape.txt (see that artifact for the exact awk)
