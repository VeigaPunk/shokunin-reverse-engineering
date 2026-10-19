#!/usr/bin/env bash
# RV-1 independent planted-selector verifier (chain c1, arc3-loop1-round1)
#
# Recomputes a planted selector set from Solidity source with RV-1's own
# from-spec Keccak-256 (keccak_ref.py), validated three ways:
#   1. 16 inputs across rate boundaries vs node/OpenSSL SHA3-256 and Python
#      stdlib SHA3-256, via padding-swap (keccak-256 = SHA3-256 with 0x01 pad)
#   2. published Keccak-256 vectors + the ERC-20 selector table
#   3. 17 inputs vs js-sha3@0.8.0 (the library bundled in solc's dep tree)
# Then compares against the planted list and, when a compiled carrier is given,
# verifies each selector sits at a real DUP1-PUSH4-EQ-PUSH2-JUMPI dispatch site.
#
# usage: verify-planted-set.sh <contract.sol> <planted-selectors.txt> [compiled-bytecode]
# exit: 0 = MATCH, 1 = MISMATCH, 2 = usage/read error
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
SOL="${1:-}"; SEL="${2:-}"; BIN="${3:-}"
if [ -z "$SOL" ] || [ -z "$SEL" ]; then
  echo "usage: $0 <contract.sol> <planted-selectors.txt> [compiled-bytecode]" >&2
  exit 2
fi
TMP="${TMPDIR:-/var/tmp}"
WORK="$(mktemp -d -p "$TMP" rv1-verify.XXXXXX)" || exit 2
trap 'rm -rf "$WORK"' EXIT

echo "== RV-1 independent verification =="
echo "sol:  $SOL"
echo "list: $SEL"
echo "bin:  ${BIN:-<none>}"
echo

echo "-- [1] recompute selectors from source text --"
python3 "$DIR/recompute.py" sol "$SOL" | tee "$WORK/rv1.txt"
echo

echo "-- [2] set comparison (planted vs RV-1) --"
python3 "$DIR/recompute.py" cmp "$SEL" "$WORK/rv1.txt"
CMP=$?
echo

if [ -n "$BIN" ]; then
  echo "-- [3] dispatch-site structure check in compiled carrier --"
  python3 - "$BIN" "$SEL" <<'PY'
import sys, hashlib
def load(p):
    raw = open(p, 'rb').read()
    try:
        t = raw.decode().strip()
        if len(t) > 100 and all(c in '0123456789abcdefABCDEFx \n\r' for c in t):
            return bytes.fromhex(t.removeprefix('0x').replace('\n', '').replace('\r', '').replace(' ', ''))
    except Exception:
        pass
    return raw
code = load(sys.argv[1])
planted = []
for l in open(sys.argv[2]):
    l = l.strip()
    if not l or l.startswith('#') or l.startswith('K='):
        continue
    planted.append(l.split()[0].lower().removeprefix('0x'))
sites = {}
for i in range(len(code) - 11):
    if code[i] == 0x80 and code[i+1] == 0x63 and code[i+6] == 0x14 and code[i+7] == 0x61 and code[i+10] == 0x57:
        sites[code[i+2:i+6].hex()] = {"push4_opcode_pc": i+1, "imm_pc": i+2, "jumpi_pc": i+10}
print(f"  carrier {len(code)} bytes  sha256 {hashlib.sha256(code).hexdigest()}")
print(f"  DUP1-PUSH4-EQ-PUSH2-JUMPI dispatch sites: {len(sites)}")
miss = 0
for s in sorted(set(planted)):
    st = sites.get(s)
    if st:
        print(f"  OK   {s} dispatch site {st}")
    else:
        miss += 1
        print(f"  FAIL {s} NOT at a dispatch site (raw-byte match only or absent)")
extra = sorted(set(sites) - set(planted))
print(f"  dispatch sites absent from planted list (false negatives): {extra}")
sys.exit(1 if (miss or extra) else 0)
PY
  SITE=$?
  echo
fi

echo "== VERDICT =="
if [ "$CMP" -eq 0 ] && [ "${SITE:-0}" -eq 0 ]; then
  echo "MATCH — RV-1 independently reproduces the planted selector set"
  exit 0
fi
echo "MISMATCH — see above"
exit 1
