#!/usr/bin/env bash
# EX-8 (arc3-loop1-round6, c2): compile VariantVault.vy under the optimizer/hardfork
# forms the r4 entry names as an Unknown; one directory per form + receipt.
set -eu
VY=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper
SRC=$(pwd)/src/VariantVault.vy
OUT=$(pwd)/out
mkdir -p "$OUT"
run() {
  tag="$1"; shift
  d="$OUT/$tag"; mkdir -p "$d"
  {
    echo "tag: $tag"
    echo "vyper: $($VY --version)"
    echo "vyper_sha256: $(sha256sum "$(readlink -f "$VY")" | cut -d' ' -f1)"
    echo "source: $SRC"
    echo "source_sha256: $(sha256sum "$SRC" | cut -d' ' -f1)"
    echo "flags: $*"
    echo "recorded_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } > "$d/receipt.txt"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f bytecode_runtime "$SRC" | sed 's/^0x//' | tr -d '\n' > "$d/runtime.hex"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f bytecode "$SRC" | sed 's/^0x//' | tr -d '\n' > "$d/creation.hex"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f abi "$SRC" > "$d/abi.json"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f method_identifiers "$SRC" > "$d/method-identifiers.json"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f opcodes_runtime "$SRC" > "$d/opcodes.txt"
  TMPDIR=/var/tmp/ex08-r6/vy/tmp $VY "$@" -f settings "$SRC" > "$d/settings.json"
  xxd -r -p "$d/runtime.hex"  > "$d/runtime.bin"
  xxd -r -p "$d/creation.hex" > "$d/creation.bin"
  {
    echo "runtime_bytes: $(stat -c%s "$d/runtime.bin")"
    echo "creation_bytes: $(stat -c%s "$d/creation.bin")"
    for f in runtime.hex runtime.bin creation.hex creation.bin abi.json method-identifiers.json opcodes.txt settings.json; do
      echo "$f sha256: $(sha256sum "$d/$f" | cut -d' ' -f1)"
    done
  } >> "$d/receipt.txt"
  echo "$tag runtime_bytes=$(stat -c%s "$d/runtime.bin") sha=$(sha256sum "$d/runtime.bin" | cut -c1-16)"
}
run default
run Ocodesize -O codesize
run Onone -O none
run nooptimize --no-optimize
run paris-default --evm-version paris
run paris-codesize -O codesize --evm-version paris
