#!/bin/bash
# SC-1 probe battery — all legs, TMPDIR disk-backed
cd /var/tmp/sc1-r3
export TMPDIR=/var/tmp/sc1-r3/tmp
run() { # name carrier encoding version
  local name=$1 carrier=$2 enc=$3 ver=$4
  npx -y rea-agents@$ver inspect-evm-interface "$carrier" "$enc" --format json > "evidence/$name.json" 2> "evidence/$name.err"
  echo "$? $name" >> evidence/probe-exits.txt
}
: > evidence/probe-exits.txt
run probe-rv2-opt200-hex-6.4.0        out/Rv2Token.opt200.runtime.hex hex 6.4.0
run probe-rv2-opt200-hex-6.4.0.rerun  out/Rv2Token.opt200.runtime.hex hex 6.4.0
run probe-vault-opt200-hex-6.4.0      out/VaultCourt.opt200.runtime.hex hex 6.4.0
run probe-vault-opt200-raw-6.4.0      out/VaultCourt.opt200.runtime.bin raw 6.4.0
run probe-rv2-opt0-hex-6.4.0          out/Rv2Token.opt0.runtime.hex hex 6.4.0
run probe-vault-opt0-hex-6.4.0        out/VaultCourt.opt0.runtime.hex hex 6.4.0
run probe-vault-opt200-creation-hex-6.4.0 out/VaultCourt.opt200.creation.hex hex 6.4.0
run probe-dispatchless-hex-6.4.0      evidence/dispatchless.hex hex 6.4.0
run probe-vault-bin-ashex-6.4.0       out/VaultCourt.opt200.runtime.bin hex 6.4.0
run probe-vault-opt200-tampered-hex-6.4.0 evidence/VaultCourt.opt200.tampered.hex hex 6.4.0
run probe-rv2-opt200-hex-6.7.0        out/Rv2Token.opt200.runtime.hex hex 6.7.0
run probe-vault-opt200-hex-6.7.0      out/VaultCourt.opt200.runtime.hex hex 6.7.0
cat evidence/probe-exits.txt
