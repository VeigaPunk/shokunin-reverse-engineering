#!/usr/bin/env python3
# EX-06 (arc3-loop1-round3): independent linear disassembly of carrier-A.bin.
# Lists PUSH4 immediates (dispatch candidates), decoy immediates, prologue bytes.
import hashlib, sys, json
b = open(sys.argv[1], 'rb').read()
pc = 0; push4 = []; ops = {}
while pc < len(b):
    op = b[pc]; ops[op] = ops.get(op, 0) + 1
    if 0x60 <= op <= 0x7f:
        n = op - 0x5f
        if n == 4: push4.append((pc, b[pc+1:pc+5].hex()))
        pc += 1 + n
    else:
        pc += 1
out = {
    "file": sys.argv[1], "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
    "prologue": b[:12].hex(),
    "push4_sites": [{"pc": pc, "imm": imm} for pc, imm in push4],
    "dispatch_pcs": [pc for pc, imm in push4 if imm in ("a9059cbb","70a08231","095ea7b3")],
    "decoys_present": {d: any(i == d for _, i in push4) for d in ("deadbeef","ffffffff")},
    "opcode_histogram": {hex(k): v for k, v in sorted(ops.items())},
}
print(json.dumps(out, indent=1))
