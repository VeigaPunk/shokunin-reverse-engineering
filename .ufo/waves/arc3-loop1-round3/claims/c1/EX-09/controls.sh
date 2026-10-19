#!/bin/bash
# EX-09 controls — byte-sensitivity and dest-repair, scratch copies only.
# Usage: bash controls.sh   (run from repo root; scratch under /var/tmp/ex09/scratch)
set -u
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round3/claims/c1/EX-09
S=/var/tmp/ex09/scratch; mkdir -p "$S"
CA="$D/target-carrierA-r3.runtime.hex" OV="$D/target-OptVault.runtime.hex" CK="$D/target-carrier-A-control.hex"
python3 - "$S" "$CA" "$OV" "$CK" <<'PY'
import sys
S,ca,ov,ck=sys.argv[1:5]
def rd(name): return bytearray(bytes.fromhex(open(name).read().strip()))
# carrier A/2 (9f7392ac): flip first byte of the 01681a62 immediate (pc 90 -> imm 91)
b=rd(ca); b[91]=0x02; open(f"{S}/carrierA-r3.tampered.hex","w").write(b.hex()+"\n")
# OptVault A/3 (544469b7): flip first byte of the 16c38b3c immediate (pc 20 -> imm 21)
b=rd(ov); b[21]=0x17; open(f"{S}/OptVault.tampered.hex","w").write(b.hex()+"\n")
# legacy control A/1: (a) tamper a9059cbb last byte; (b) one-byte dest repair
b=rd(ck)
t=bytearray(b); t[11]=0xbc; open(f"{S}/carrier-A.tampered.hex","w").write(t.hex()+"\n")
r=bytearray(b); r[14]=0x28; r[24]=0x32; r[34]=0x3c
open(f"{S}/carrier-A.destfixed.hex","w").write(r.hex()+"\n")
print("scratch copies written:", S)
PY
python3 "$D/ex09-recon.py" extract "$CA" hex | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/2 baseline eq selectors:',d['dispatch_selectors'])"
python3 "$D/ex09-recon.py" extract "$S/carrierA-r3.tampered.hex" hex | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/2 tampered  eq selectors:',d['dispatch_selectors'])"
python3 "$D/ex09-recon.py" scan "$S/carrierA-r3.tampered.hex" hex "$D/sigs-carrierA-r3.txt" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/2 tampered keccak scan found:',d['found'],'/',d['total'],'missing:',[r['selector'] for r in d['results'] if not r['offsets']])"
python3 "$D/ex09-recon.py" scan "$OV" hex "$D/sigs-OptVault.txt" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/3 baseline keccak scan found:',d['found'],'/',d['total'])"
python3 "$D/ex09-recon.py" scan "$S/OptVault.tampered.hex" hex "$D/sigs-OptVault.txt" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/3 tampered keccak scan found:',d['found'],'/',d['total'],'missing:',[r['selector'] for r in d['results'] if not r['offsets']])"
python3 "$D/ex09-recon.py" extract "$S/carrier-A.tampered.hex" hex | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/1 tampered  chain:',[(c['selector'],c['dest']) for c in d['dispatch_chain']])"
python3 "$D/ex09-recon.py" scan "$S/carrier-A.tampered.hex" hex "$D/sigs-A-control.txt" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/1 tampered keccak scan found:',d['found'],'/',d['total'],'missing:',[r['selector'] for r in d['results'] if not r['offsets']])"
python3 "$D/ex09-recon.py" extract "$S/carrier-A.destfixed.hex" hex | python3 -c "
import json,sys; d=json.load(sys.stdin)
print('A/1 dest-repair chain:',[(c['selector'],c['dest'],c['landing']['is_jumpdest']) for c in d['dispatch_chain']])"
python3 "$D/ex09-recon.py" jumpdests "$S/carrier-A.destfixed.hex" hex 40 50 60