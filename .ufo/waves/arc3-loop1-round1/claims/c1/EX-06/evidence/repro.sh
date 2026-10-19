#!/usr/bin/env bash
# EX-06 reproduction script — hex-encoding form of the C1 EVM probe vs the raw form.
# Runs entirely on scratch (/dev/shm/ex06): no repo target is written.
# Usage: bash repro.sh 2>&1 | tee transcript.txt
set -u
SCRATCH=${SCRATCH:-/dev/shm/ex06}
SELF=$(cd "$(dirname "$0")" && pwd)
REA67=/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
REA64=/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents/scripts/rea.mjs
SOLC_PREFIX=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix
export TMPDIR=$SCRATCH/tmp   # required: the system /tmp tmpfs is usrquota-exhausted (EDQUOT)
mkdir -p "$TMPDIR"
# self-contained: scripts + source under test are taken from this evidence directory
cp "$SELF"/compile.js "$SELF"/keccak.js "$SELF"/plant.js "$SELF"/compare.js "$SELF"/KdxToken.sol "$SCRATCH"/

echo "== environment =="
echo "host: $(uname -srm)  user: $(whoami)  date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "node: $(node --version)"
echo "rea 6.7.0: $(node "$REA67" --version)  ($REA67)"
echo "rea 6.4.0: $(node "$REA64" --version)  ($REA64)"
echo "solc: $(node -e "console.log(require('$SOLC_PREFIX/node_modules/solc').version())")"
echo "soljson sha256: $(sha256sum "$SOLC_PREFIX/node_modules/solc/soljson.js" | cut -d' ' -f1)"
echo "df /tmp: $(df -h /tmp | tail -1)"
echo "df /dev/shm: $(df -h /dev/shm | tail -1)"

echo
echo "== step 1: compile the real contract (solc 0.8.37) =="
node "$SCRATCH/compile.js"
echo "carrier hashes:"
sha256sum "$SCRATCH/KdxToken.sol" "$SCRATCH/KdxToken.runtime.hex" "$SCRATCH/KdxToken.runtime.bin" \
          "$SCRATCH/KdxToken.creation.hex" "$SCRATCH/KdxToken.creation.bin"

echo
echo "== step 2: planted selector count K (pre-probe, independent keccak) =="
node "$SCRATCH/keccak.js"
node "$SCRATCH/plant.js"

echo
echo "== step 3: probe runs, 6.7.0 (hex forms + raw twin) =="
run() { # $1 = label, $2 = file, $3 = encoding
  node "$REA67" inspect-evm-interface "$2" "$3" --format json > "$SCRATCH/run-$1.json" 2> "$SCRATCH/run-$1.err"
  local rc=$?
  echo "[$1] exit=$rc stdout_bytes=$(wc -c < "$SCRATCH/run-$1.json") stderr_bytes=$(wc -c < "$SCRATCH/run-$1.err")"
}
printf '%s' "$(tr -d '\n' < "$SCRATCH/KdxToken.runtime.hex")" > "$SCRATCH/KdxToken.runtime.nonl.hex"
printf '0x%s' "$(tr -d '\n' < "$SCRATCH/KdxToken.runtime.hex")" > "$SCRATCH/KdxToken.runtime.0x.hex"
tr 'a-f' 'A-F' < "$SCRATCH/KdxToken.runtime.hex" > "$SCRATCH/KdxToken.runtime.upper.hex"
run raw           "$SCRATCH/KdxToken.runtime.bin"        raw
run hex           "$SCRATCH/KdxToken.runtime.hex"        hex
run hex-nonl      "$SCRATCH/KdxToken.runtime.nonl.hex"   hex
run hex-0x        "$SCRATCH/KdxToken.runtime.0x.hex"     hex
run hex-upper     "$SCRATCH/KdxToken.runtime.upper.hex"  hex
run hex-repeat    "$SCRATCH/KdxToken.runtime.hex"        hex
run creation-hex  "$SCRATCH/KdxToken.creation.hex"       hex
run creation-raw  "$SCRATCH/KdxToken.creation.bin"       raw
node "$REA64" inspect-evm-interface "$SCRATCH/KdxToken.runtime.hex" hex --format json > "$SCRATCH/run-hex-6.4.0.json" 2>&1
echo "[hex-6.4.0] exit=$?"
node "$REA64" inspect-evm-interface "$SCRATCH/KdxToken.runtime.bin" raw --format json > "$SCRATCH/run-raw-6.4.0.json" 2>&1
echo "[raw-6.4.0] exit=$?"

echo
echo "== step 4: raw vs hex deep comparison (normalized) =="
node "$SCRATCH/compare.js" run-raw.json run-hex.json run-hex-nonl.json run-hex-0x.json run-hex-upper.json run-hex-repeat.json

echo
echo "== step 5: input-shape traps (fail-closed surface) =="
cp "$SCRATCH/KdxToken.runtime.hex" "$SCRATCH/raw-of-hex.bin"
printf '6001 6001\n01' > "$SCRATCH/interior-ws.hex"
printf '600160010' > "$SCRATCH/oddlen.hex"
node -e "const fs=require('fs');const h=fs.readFileSync('$SCRATCH/KdxToken.runtime.hex','utf8').trim();
 fs.writeFileSync('$SCRATCH/wrapped.hex', h.replace(/(.{64})/g,'\$1\n'));
 fs.writeFileSync('$SCRATCH/crlf.hex', h.replace(/(.{64})/g,'\$1\r\n'));"
trap() { # $1 = label, $2 = file, $3 = encoding
  node "$REA67" inspect-evm-interface "$2" "$3" --format json > "$SCRATCH/trap-$1.json" 2>&1
  rc=$?
  echo "[$1] ($2 as $3) exit=$rc -> $(head -c 300 "$SCRATCH/trap-$1.json")"
}
trap raw-of-hex "$SCRATCH/raw-of-hex.bin" raw
trap interior-ws "$SCRATCH/interior-ws.hex" hex
trap oddlen "$SCRATCH/oddlen.hex" hex
trap wrapped "$SCRATCH/wrapped.hex" hex
trap crlf "$SCRATCH/crlf.hex" hex

echo
echo "== step 6: TMPDIR control (EDQUOT reproduction with system temp) =="
env -u TMPDIR node "$REA67" inspect-evm-interface "$SCRATCH/KdxToken.runtime.bin" raw --format json > "$SCRATCH/raw-noTMPDIR.json" 2>&1
echo "[raw, TMPDIR unset] exit=$? -> $(head -c 400 "$SCRATCH/raw-noTMPDIR.json")"
echo "[hex, TMPDIR unset] control:"
env -u TMPDIR node "$REA67" inspect-evm-interface "$SCRATCH/KdxToken.runtime.hex" hex --format json > "$SCRATCH/hex-noTMPDIR.json" 2>&1
echo "exit=$? -> $(head -c 400 "$SCRATCH/hex-noTMPDIR.json")"

echo
echo "== step 7: offset semantics check (r4 erratum: bytecodeOffset = JUMPDEST target) =="
node -e "
const fs=require('fs');const hex=fs.readFileSync('$SCRATCH/KdxToken.runtime.hex','utf8').trim();
const j=require('$SCRATCH/run-hex.json');
for (const f of j.raw_result.functions) console.log(f.selector,'offset',f.bytecodeOffset,'byte',hex.substr(f.bytecodeOffset*2,2));"

echo
echo "== step 8: metadata trailer cross-check (independent CBOR decode) =="
node -e "
const fs=require('fs'),crypto=require('crypto');
const {decode}=require('/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/cborg');
const bin=fs.readFileSync('$SCRATCH/KdxToken.runtime.bin');
const n=bin.readUInt16BE(bin.length-2);const meta=bin.subarray(bin.length-2-n,bin.length-2);
const d=decode(meta);
console.log('cborLength',n,'metadataStart',bin.length-2-n);
console.log('solc bytes',Buffer.from(d.solc).toString('hex'),'->',d.solc[1]+'.'+d.solc[2]+'.'+d.solc[3]);
console.log('ipfs digest',Buffer.from(d.ipfs).subarray(2).toString('hex'));
console.log('sha256(metadata)',crypto.createHash('sha256').update(meta).digest('hex'));"
echo "DONE"
