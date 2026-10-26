#!/bin/sh
# make-measurements.sh — regenerate measurements.md from the copied fixtures, the installed
# tools and the artifacts in this directory.  Deterministic apart from timestamps inside the
# tools' own output.  Writes only to stdout; redirect it.
#
#   ./make-measurements.sh > measurements.md
#
# Inputs used: this directory (fixtures, dev envelopes, fixture-SKILL.md, tools).
set -u
A=$(cd "$(dirname "$0")" && pwd)
U=${UNBLOB_TREE:-$HOME/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob}
R=${REA_DIST:-$HOME/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist}
T=$(mktemp -d "${TMPDIR:-/tmp}/r42meas.XXXXXX")
trap 'rm -rf -- "$T"' EXIT

echo "# Measurements for block 21 (table v4) — commands, exit codes, verbatim output"
echo
echo "Regenerate: \`./make-measurements.sh > measurements.md\` in this directory."
echo
echo "## 0. Pins"
echo
echo '```'
echo "# installed sources (sha256 must equal the SOURCES row pins)"
sha256sum "$U/handlers/filesystem/squashfs.py" "$U/extractor.py" "$U/report.py" \
          "$U/extractors/command.py" | sed "s|$U/||"
echo "# REA 6.5.0 dist files"
sha256sum "$R/firmware/FirmwarePublication.js" "$R/domain/firmware/firmwareAnalysis.js" \
          "$R/firmware/FirmwareRelease.js" | sed "s|$R/||"
echo "# readers"
unsquashfs -version 2>&1 | head -1
7z 2>&1 | sed -n '3p'
echo '```'
echo
echo "## 1. Fixtures (unblob 26.6.4 test fixtures, MIT; LFS media path)"
echo
echo '```'
echo "base=https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs"
echo "# fetched: squashfs_v1/big_endian/__input__/squashfs_v1.0_be.bin"
echo "#          squashfs_v2/big_endian/__input__/squashfs_v2.0_be.bin"
echo "#          squashfs_v3/little_endian/__input__/squashfs_v3_le.bin"
echo "#          squashfs_v3/big_endian/__input__/squashfs_v3_be.bin"
echo "# rebuild: curl -sSL -o <name> \"\$base/<handler>/<endian>/__input__/<name>\""
sha256sum "$A"/squashfs_v*.bin | sed "s|$A/||"
ls -l "$A"/squashfs_v*.bin | awk '{print $5, $9}' | sed "s|$A/||"
echo '```'
echo
echo "## 2. unsquashfs 4.7.5 and 7-Zip 26.04 read v1, v2 and v3 (both endiannesses)"
echo
echo '```'
for f in "$A"/squashfs_v1.0_be.bin "$A"/squashfs_v2.0_be.bin "$A"/squashfs_v3_be.bin \
         "$A"/squashfs_v3_le.bin; do
  echo "\$ unsquashfs -s $(basename $f) | grep 'Found a valid'"
  unsquashfs -s "$f" 2>&1 | grep 'Found a valid'
  echo "\$ unsquashfs -lls $(basename $f)"
  unsquashfs -lls "$f" 2>&1 && rc=0 || rc=$?
  echo "  exit=$rc"
  echo
done
for f in "$A"/squashfs_v3_le.bin "$A"/squashfs_v3_be.bin; do
  echo "\$ 7z l $(basename $f)   (tail)"
  7z l "$f" > "$T/z" 2>&1 && rc=0 || rc=$?
  tail -9 "$T/z"
  echo "  exit=$rc"
  echo
done
echo '```'
echo
echo "## 3. unblob 26.6.4 argv on a v1-v3 chunk (plain sasquatch, -le or -be)"
echo
echo '```'
for f in "$A"/squashfs_v3_le.bin "$A"/squashfs_v3_be.bin; do
  d=$T/u-$(basename $f .bin); mkdir -p "$d"
  (cd "$d" && { unblob --depth 2 "$f" >/dev/null 2>&1 && echo "unblob exit=0" || echo "unblob exit=$?"; })
  grep -E 'Calculating chunk|Running extract command' "$d/unblob.log" \
    | sed "s|$d/||g; s|$T/||g"
  echo
done
echo '```'
echo
echo "## 3b. The residue: unblob's unknown-chunk carve and REA's gap mint"
echo
echo '```'
for n in 116 117 118 119 120 121 122 123 124 125; do printf "S118 extractor.py:%s: " $n; sed -n "${n}p" "$U/extractor.py"; done
for n in 226 227 228 233 234 235 236 286; do printf "S119 FirmwarePublication.js:%s: " $n; sed -n "${n}p" "$R/firmware/FirmwarePublication.js"; done
echo '```'
echo
echo "## 4. Damage arms: both readers fail with sasquatch's message"
echo
echo '```'
python3 - "$A/squashfs_v3_le.bin" "$T" <<'PY'
import pathlib, sys
src = pathlib.Path(sys.argv[1]).read_bytes(); out = pathlib.Path(sys.argv[2])
for lo, hi, name in ((0x40, 0x80, 'a'), (0x60, 0x100, 'b'), (0xD0, 0x110, 'c'),
                     (0xC0, 0x100, 'd'), (0xE0, 0x102, 'e'), (0x60, 0x70, 'f')):
    b = bytearray(src)
    for i in range(lo, min(hi, len(b))):
        b[i] = 0
    (out / ('dmg-%s.bin' % name)).write_bytes(bytes(b))
PY
for n in a b c d e f; do
  f=$T/dmg-$n.bin
  case $n in a) r='0x40-0x80';; b) r='0x60-0x100';; c) r='0xD0-0x110';;
            d) r='0xC0-0x100';; e) r='0xE0-0x102';; f) r='0x60-0x70';; esac
  echo "=== zeroed $r"
  unsquashfs -s "$f" >/dev/null 2>&1 && rc=0 || rc=$?; echo "  unsquashfs -s   exit=$rc"
  unsquashfs -lls "$f" >"$T/o" 2>&1 && rc=0 || rc=$?; echo "  unsquashfs -lls exit=$rc"; tail -2 "$T/o" | sed 's/^/    /'
  rm -rf "$T/od"; mkdir "$T/od"
  sasquatch -le -f -d "$T/od/x" "$f" >"$T/s" 2>&1 && rc=0 || rc=$?; echo "  sasquatch       exit=$rc"; tail -2 "$T/s" | sed 's/^/    /'
done
echo
echo "=== intact body (control)"
unsquashfs -lls "$A/squashfs_v3_le.bin" >/dev/null 2>&1 && rc=0 || rc=$?; echo "  unsquashfs -lls exit=$rc"
rm -rf "$T/oi"; mkdir "$T/oi"
sasquatch -le -f -d "$T/oi/x" "$A/squashfs_v3_le.bin" >/dev/null 2>&1 && rc=0 || rc=$?; echo "  sasquatch       exit=$rc"
find "$T/oi" -type f | sed "s|$T/|    |"
echo '```'
echo
echo "## 5. The drafted block parses in situ, and its reader's selftest"
echo
echo '```'
echo "\$ make-fixture.sh LANE c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c \$T/fixture-SKILL.md"
sh "$A/make-fixture.sh" /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
   c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c "$T/fixture-SKILL.md" 2>&1 | sed "s|$T/||"
echo "\$ v4-refparse.py --skill \$T/fixture-SKILL.md --table-only   (head)"
python3 -I -B "$A/v4-refparse.py" --skill "$T/fixture-SKILL.md" --table-only 2>&1 | sed -n '1,4p'
echo "\$ v4-refparse.py --selftest"
python3 -I -B "$A/v4-refparse.py" --selftest 2>&1 | tail -3
echo '```'
echo
echo "## 6. Drafted block vs the drafted precedence"
echo
echo '```'
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
git -C "$L" show c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:SKILL.md > "$T/base-SKILL.md"
echo "\$ python3 -I -B LANE/tools/round-41/sqfs-triage-v3.py --skill \$T/base-SKILL.md LANE/corpus/evidence/round-41/c2/heldout/*/envelope.json > \$T/c-v3pairs.tsv"
python3 -I -B "$L/tools/round-41/sqfs-triage-v3.py" --skill "$T/base-SKILL.md" \
  "$L"/corpus/evidence/round-41/c2/heldout/*/envelope.json > "$T/c-v3pairs.tsv" 2>"$T/v3.err"
echo "  rows=$(wc -l < "$T/c-v3pairs.tsv") exit=$?"
echo "\$ python3 -I -B check.py --skill \$T/fixture-SKILL.md --heldout LANE/corpus/evidence/round-41/c2/heldout \\"
echo "      --dev <the 8 dev envelopes> --out-prefix \$T/c"
# the committed fixture is the same bytes the check was run against; reuse it read-only
DEV="$A/dev-v3le-d1.json $A/dev-v3le-d3.json"
for f in trx-img-with trx-img-without trx-fs-with trx-fs-without x86-fs-with x86-fs-without; do
  DEV="$DEV $L/.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/$f.json"
done
python3 -I -B "$A/check.py" --skill "$A/fixture-SKILL.md" \
  --heldout "$L/corpus/evidence/round-41/c2/heldout" \
  --dev $DEV --out-prefix "$T/c" 2>&1
echo "  exit=$?"
echo '```'
echo
echo "## 7. R41-CL4 executed: the same legacy envelopes under v3 and under v4"
echo
echo '```'
echo "\$ python3 -I -B LANE/tools/round-41/sqfs-triage-v3.py --skill \$T/base-SKILL.md <the 8 dev envelopes>"
python3 -I -B "$L/tools/round-41/sqfs-triage-v3.py" \
  --skill "$T/base-SKILL.md" $DEV 2>&1 | sed "s|$A/||; s|$L/.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/||"
echo "\$ python3 -I -B v4-refparse.py --skill fixture-SKILL.md --json <the 8 dev envelopes>"
python3 -I -B "$A/v4-refparse.py" --skill "$A/fixture-SKILL.md" \
  --json $DEV 2>&1 | sed "s|$A/||; s|$L/.ufo/waves/round-42/w1/artifacts/R42C1DevRun/envelopes/||"
echo '```'
echo
echo "## 8. The four round-41 C1 receipts (real AVM envelopes), v4 and v3"
echo
echo '```'
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B "$A/v4-refparse.py" --skill "$A/fixture-SKILL.md" \
  --json "$L"/corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json 2>&1 | sed "s|$L/||"
python3 -I -B "$L/tools/round-41/sqfs-triage-v3.py" --skill "$T/base-SKILL.md" \
  "$L"/corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json 2>&1 | sed "s|$L/||"
echo '```'
echo
echo "## 9. REA 6.5.0 dev-arm envelopes (commands as run)"
echo
echo '```'
echo 'cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \'
echo '  --format json --full-output --max-depth 1 fx/squashfs_v3_le.bin out/rea-v3le     # exit 0'
echo 'cd $S && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \'
echo '  --format json --full-output --max-depth 3 fx/squashfs_v3_le.bin out/rea-v3le-d3  # exit 0'
echo "# the envelopes are copied here as dev-v3le-d1.json (--max-depth 1) and dev-v3le-d3.json (3):"
sha256sum "$A/dev-v3le-d1.json" "$A/dev-v3le-d3.json" | sed "s|$A/||"
python3 -I -B - "$A" <<'PY'
import importlib.util, json, os, sys
A = sys.argv[1]
spec = importlib.util.spec_from_file_location('r', os.path.join(A, 'v4-refparse.py'))
r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
spec = importlib.util.spec_from_file_location('p', os.path.join(A, 'precedence.py'))
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
for name in ('dev-v3le-d1.json', 'dev-v3le-d3.json'):
    path = os.path.join(A, name)
    f = r.load_envelope(path)
    print('%s  H=%s G=%s P=%d BE=%s SR=%s diag_files=%d -> precedence %s/%s'
          % (name, f['H'], f['G'] or 'none', f['P'], f['BE'], f['SR'],
             len(json.load(open(path))['data']['normalized_result'].get('diagnostics', [])),
             *p.decide(f)[:2]))
PY
echo '```'
