#!/usr/bin/env bash
# C1SrcUnblob probe (round 50, wave 1). Read-only w.r.t. the lane tree.
# Usage: S=<scratch dir> bash probe-le-handler.sh
# Fetches unblob 26.6.4 squashfs.py, builds a host LE v4 xz image (no vendor bytes),
# makes a SYNTHETIC AVM-marker twin (mkfs_time := bytes_used), and runs sasquatch -le
# and unblob 26.6.4 under three PATH variants. Prints one line per receipt.
set -u
: "${S:?set S to the scratch dir}"
export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
mkdir -p "$S/probe" && cd "$S/probe" || exit 2
UNBLOB=$HOME/.local/bin/unblob
SRC_URL=https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py

echo "UTC $(date -u +%FT%TZ)"
code=$(curl -sS -o unblob-26.6.4-squashfs.py -w '%{http_code} %{size_download}' "$SRC_URL"); echo "fetch squashfs.py http/bytes: $code"
echo "sha256 squashfs.py: $(sha256sum unblob-26.6.4-squashfs.py | cut -c1-64)"
cmp -s unblob-26.6.4-squashfs.py "$HOME/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py"; echo "cmp vs installed uv copy exit=$?"

rm -rf src && mkdir -p src/etc
printf 'hello avm-marker probe\n' > src/etc/motd
head -c 300000 /dev/urandom > src/blob.bin
ln -sf etc/motd src/link_motd
mksquashfs src std-le-v4-xz.sqsh -comp xz -noappend -all-root -all-time 0 -mkfs-time 1700000000 -quiet; echo "mksquashfs exit=$?"

python3 - <<'EOF'
import struct, hashlib
b = bytearray(open('std-le-v4-xz.sqsh', 'rb').read())
inodes, mkfs, bs, frag, comp, blog, flags, noids, maj, mnr = struct.unpack('<IIIIHHHHHH', b[4:32])
bytes_used = struct.unpack('<Q', b[40:48])[0]
print('std superblock: magic', bytes(b[:4]), 'mkfs_time', mkfs, 'bytes_used', bytes_used, 'comp', comp, 'major', maj, 'minor', mnr)
c = bytearray(b); struct.pack_into('<I', c, 8, bytes_used & 0xFFFFFFFF)
open('avmmarker-SYNTHETIC-le-v4-xz.sqsh', 'wb').write(c)
print('synthetic superblock: mkfs_time', struct.unpack('<I', c[8:12])[0], 'bytes_used', bytes_used, 'equal', struct.unpack('<I', c[8:12])[0] == bytes_used)
for n in ['std-le-v4-xz.sqsh', 'avmmarker-SYNTHETIC-le-v4-xz.sqsh']:
    print('sha256', n, hashlib.sha256(open(n, 'rb').read()).hexdigest())
EOF

tree_sha() { (cd "$1" && find . -print0 | LC_ALL=C sort -z | xargs -0 -I{} sh -c 'if [ -f "{}" ]; then printf "%s " "{}"; sha256sum "{}" | cut -c1-64; elif [ -L "{}" ]; then printf "%s -> %s\n" "{}" "$(readlink "{}")"; else printf "%s dir\n" "{}"; fi') | sha256sum | cut -c1-64; }

for img in std-le-v4-xz.sqsh avmmarker-SYNTHETIC-le-v4-xz.sqsh; do
  rm -rf "sasq-$img"
  sasquatch -le -no-exit-code -f -d "sasq-$img" "$img" >/dev/null 2>&1; echo "sasquatch -le $img exit=$? tree_sha=$(tree_sha "sasq-$img")"
done

PATH_FULL="$PATH"
mkdir -p nobe/bin nosasq/bin && ln -sf "$HOME/.local/bin/sasquatch" nobe/bin/sasquatch
run_unblob() { # label image path-value
  local label=$1 img=$2 p=$3
  rm -rf "ub-$label"; mkdir -p "ub-$label"
  env PATH="$p" timeout 300 "$UNBLOB" -e "ub-$label/ex" -f --report "ub-$label/report.json" --log "ub-$label/unblob.log" "$img" >"ub-$label/stdout" 2>"ub-$label/stderr"
  echo "unblob [$label] $img exit=$?"
  python3 - "ub-$label" <<'EOF'
import json, re, sys
d = sys.argv[1]
s = json.dumps(json.load(open(d + '/report.json')))
print('  handlers', sorted(set(re.findall(r'"handler_name": "([^"]+)"', s))))
print('  error_report_types', sorted(set(re.findall(r'"__typename__": "(\w*Report)"', s)) & {'ExtractCommandFailedReport', 'ExtractorDependencyNotFoundReport', 'ExtractorTimedOut'}))
print('  dependency_reports', re.findall(r'"dependencies": \[[^\]]*\]', s))
log = open(d + '/unblob.log', encoding='utf-8', errors='replace').read()
print('  extract_commands', re.findall(r"Running extract command\s+command='([^']*)'", log))
EOF
}
run_unblob std-full "std-le-v4-xz.sqsh" "$PATH_FULL"
run_unblob synth-full "avmmarker-SYNTHETIC-le-v4-xz.sqsh" "$PATH_FULL"
run_unblob synth-nobe "avmmarker-SYNTHETIC-le-v4-xz.sqsh" "$PWD/nobe/bin:/usr/bin:/bin"
run_unblob std-nosasq "std-le-v4-xz.sqsh" "$PWD/nosasq/bin:/usr/bin:/bin"
for d in ub-std-full ub-synth-full ub-synth-nobe ub-std-nosasq; do echo "tree $d $(tree_sha "$d/ex" 2>/dev/null)"; done
