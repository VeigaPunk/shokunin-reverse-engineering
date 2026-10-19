#!/usr/bin/env python3
"""EX-04 (arc3-loop1-round4, C1) — byte-level dispatcher census for the Vyper
0.4.3 carrier.

Two independent readings of the same runtime bytes, neither using the compiler:

  1. A linear leg-chain disassembler over the dispatch region: decodes the
     modulo-indexed jump table at the tail, follows each bucket's chain of
     `JUMPDEST PUSH4 <sel> DUP2 XOR PUSH2 <next> JUMPI` legs, and derives
     (selector -> body entry) as the fall-through address of the matching leg.
  2. A minimal EVM that *executes* the real prologue + chain for a given
     selector and reports where it stops.

Then compares both against the probe envelope's reported `bytecode_offset`.

Usage: python3 dispatch-census.py <runtime.hex> [planted-K.json [probe.json]]
"""
import json
import re
import sys
from pathlib import Path

PUSH1, PUSH2, PUSH4, PUSH0 = 0x60, 0x61, 0x63, 0x5F
DUP1, DUP2, DUP3, DUP4 = 0x80, 0x81, 0x82, 0x83
SWAP1, SWAP2, SWAP3 = 0x90, 0x91, 0x92
SHR, SHL, MOD, ADD, SUB, XOR, EQ, ISZERO = 0x1C, 0x1B, 0x06, 0x01, 0x03, 0x18, 0x14, 0x15
CALLDATALOAD, CODECOPY, MLOAD, MSTORE = 0x35, 0x39, 0x51, 0x52
JUMP, JUMPI, JUMPDEST, REVERT, STOP, INVALID = 0x56, 0x57, 0x5B, 0xFD, 0x00, 0xFE
CALLDATASIZE, CALLER, CALLVALUE, SLOAD, POP, GT, LT = 0x36, 0x33, 0x34, 0x54, 0x50, 0x11, 0x10
OR, AND, NOT, RETURN = 0x17, 0x16, 0x19, 0xF3


def run(code, selector, max_steps=4000, cd_words=1, callvalue=0):
    """Execute the dispatch prologue + chain for `selector`. Returns a dict.

    cd_words / callvalue are the harness-supplied call context: Vyper 0.4.3
    bodies open with a fused `PUSH1 <4+32n> CALLDATASIZE LT CALLVALUE OR
    PUSH2 <revert> JUMPI` guard, so the calldata size must be realistic or
    every call reverts at the shared stub.
    """
    stack, mem = [], bytearray(256)
    # calldata word 0 is `selector || args`, i.e. the selector occupies the
    # FIRST 4 bytes of the word (ABI encoding), so `PUSH1 0xe0 SHR` recovers it.
    # word 0 is `selector || first arg`, zero-padded to 32 B: CALLDATALOAD reads
    # a full word and zero-extends past the end of calldata, so a 4-byte
    # (zero-arg) calldata must still yield the selector in the high 4 bytes.
    cd = selector.to_bytes(4, "big") + bytes(28 + 32 * cd_words)
    pc, steps, tail = 0, 0, []
    while steps < max_steps:
        steps += 1
        if pc >= len(code):
            return {"stop": "ran-off-code", "pc": pc, "tail": tail}
        op = code[pc]
        here = pc
        pc += 1
        if op == PUSH0:
            stack.append(0)
        elif op == PUSH1:
            stack.append(code[pc]); pc += 1
        elif op == PUSH2:
            stack.append(int.from_bytes(code[pc:pc + 2], "big")); pc += 2
        elif op == PUSH4:
            stack.append(int.from_bytes(code[pc:pc + 4], "big")); pc += 4
        elif DUP1 <= op <= DUP4:
            stack.append(stack[-(op - 0x7F)])
        elif SWAP1 <= op <= SWAP3:
            i = op - 0x8F
            stack[-1], stack[-1 - i] = stack[-1 - i], stack[-1]
        elif op == CALLDATALOAD:
            o = stack.pop(); stack.append(int.from_bytes(cd[o:o + 32], "big"))
        elif op == CALLDATASIZE:
            stack.append(len(cd))
        elif op == CALLVALUE:
            stack.append(callvalue)
        elif op == CALLER:
            stack.append(0)
        # EVM operand order: the first-popped value (top) is the LEFT operand,
        # so result = top OP second for every non-commutative binary op.
        elif op == SHR:
            shift = stack.pop(); val = stack.pop(); stack.append(val >> shift)
        elif op == SHL:
            shift = stack.pop(); val = stack.pop(); stack.append(val << shift)
        elif op == MOD:
            a = stack.pop(); b = stack.pop(); stack.append(0 if b == 0 else a % b)
        elif op == ADD:
            a = stack.pop(); b = stack.pop(); stack.append((a + b) & (2 ** 256 - 1))
        elif op == SUB:
            a = stack.pop(); b = stack.pop(); stack.append((a - b) & (2 ** 256 - 1))
        elif op == XOR:
            a = stack.pop(); b = stack.pop(); stack.append(a ^ b)
        elif op == EQ:
            a = stack.pop(); b = stack.pop(); stack.append(1 if a == b else 0)
        elif op == ISZERO:
            stack.append(1 if stack.pop() == 0 else 0)
        elif op == GT:
            a = stack.pop(); b = stack.pop(); stack.append(1 if a > b else 0)
        elif op == LT:
            a = stack.pop(); b = stack.pop(); stack.append(1 if a < b else 0)
        elif op == OR:
            a = stack.pop(); b = stack.pop(); stack.append(a | b)
        elif op == AND:
            a = stack.pop(); b = stack.pop(); stack.append(a & b)
        elif op == NOT:
            stack.append(~stack.pop() & (2 ** 256 - 1))
        elif op == RETURN:
            return {"stop": "body-return", "pc": here, "tail": tail}
        elif op == SLOAD:
            stack.pop(); stack.append(0)
        elif op == CODECOPY:
            d = stack.pop(); o = stack.pop(); ln = stack.pop()
            if d + ln > len(mem):
                mem.extend(bytes(d + ln - len(mem)))
            mem[d:d + ln] = code[o:o + ln].ljust(ln, b"\0")
        elif op == MLOAD:
            o = stack.pop(); stack.append(int.from_bytes(mem[o:o + 32], "big"))
        elif op == MSTORE:
            o = stack.pop(); v = stack.pop()
            mem[o:o + 32] = v.to_bytes(32, "big")
        elif op == POP:
            stack.pop()
        elif op == JUMP:
            t = stack.pop(); tail.append((here, f"JUMP {t:#x}")); pc = t
        elif op == JUMPI:
            t = stack.pop(); c = stack.pop()
            tail.append((here, f"JUMPI {t:#x} {'taken' if c else 'fall-through'}"))
            if c:
                pc = t
        elif op == JUMPDEST:
            pass
        elif op in (REVERT, INVALID):
            return {"stop": "revert", "pc": here, "tail": tail}
        elif op == STOP:
            return {"stop": "stop", "pc": here, "tail": tail}
        else:
            # first opcode outside the dispatch vocabulary: the body has begun
            return {"stop": f"body-opcode-{op:#04x}", "pc": here, "tail": tail}
    return {"stop": "step-limit", "pc": pc, "tail": tail}


def disassemble_chains(code, table_off, n_buckets):
    """Follow each bucket's leg chain; return {selector: body_entry} + legs."""
    table = [int.from_bytes(code[table_off + 2 * i: table_off + 2 * i + 2], "big")
             for i in range(n_buckets)]
    legs, derived, seen = [], {}, set()
    for bucket, start in enumerate(table):
        pc = start
        while pc not in seen:
            seen.add(pc)
            if pc + 12 > len(code):
                legs.append((bucket, pc, "OUT-OF-RANGE", None, None, None))
                break
            if code[pc] != JUMPDEST:
                legs.append((bucket, pc, "NOT-A-JUMPDEST", None, None, None))
                break
            if code[pc + 1] != PUSH4:
                # an empty bucket: JUMPDEST then straight into the default body
                legs.append((bucket, pc, "default-body", pc + 1, None, code[pc + 1] == JUMPDEST))
                break
            sel = int.from_bytes(code[pc + 2:pc + 6], "big")
            nxt = int.from_bytes(code[pc + 9:pc + 11], "big")
            shape_ok = (code[pc + 6] == DUP2 and code[pc + 7] == XOR
                        and code[pc + 8] == PUSH2 and code[pc + 11] == JUMPI)
            legs.append((bucket, pc, f"{sel:08x}", pc + 12, nxt, shape_ok))
            derived[f"{sel:08x}"] = {"bucket": bucket, "leg_pc": pc,
                                     "body_entry": pc + 12, "next_on_mismatch": nxt,
                                     "shape_ok": shape_ok}
            pc = nxt
    return table, legs, derived


def main():
    code = bytes.fromhex(Path(sys.argv[1]).read_text().strip())
    K = json.loads(Path(sys.argv[2]).read_text())["planted_selectors"] if len(sys.argv) > 2 else None
    probe = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else None

    print(f"runtime bytes: {len(code)}")
    # locate the table: the tail block whose entries all point at JUMPDESTs
    nb = 13
    table_off = len(code) - 2 * nb
    print(f"assumed jump table at {table_off:#x} ({nb} buckets x 2 B) -> tail {2*nb} B")

    table, legs, derived = disassemble_chains(code, table_off, nb)
    print("\n=== bucket table ===")
    for i, d in enumerate(table):
        tag = "empty (revert path)" if code[d] == JUMPDEST and code[d + 1] != PUSH4 else ""
        print(f"  [{i:2d}] -> {d:#06x}  rt[{d}]={code[d]:#04x} {tag}")

    print(f"\n=== leg chains ({len(legs)} legs) ===")
    for bucket, pc, sel, body, nxt, shape in legs:
        body_s = f"{body:#06x}" if body is not None else "-"
        nxt_s = f"{nxt:#06x}" if nxt is not None else "-"
        print(f"  bucket {bucket:2d} leg@{pc:#06x} sel={sel} body={body_s} next={nxt_s} shape_ok={shape}")

    print("\n=== derived (selector -> body) ===")
    for sel in sorted(derived):
        d = derived[sel]
        print(f"  {sel} bucket={d['bucket']:2d} body={d['body_entry']:#06x} JUMPDEST@body={code[d['body_entry']] == JUMPDEST}")

    print("\n=== executed dispatcher (mini-EVM) ===")
    if K:
        mism = []
        for sig, sel in sorted(K.items(), key=lambda kv: kv[1]):
            n_args = 0 if sig.endswith("()") else sig[sig.index("(") + 1:-1].count(",") + 1
            r = run(code, int(sel, 16), cd_words=n_args)
            body = derived.get(sel, {}).get("body_entry")
            reached = body is not None and r["pc"] >= body
            print(f"  {sel} {sig:<26} cd_words={n_args} stop={r['stop']:<16} pc={r['pc']:#06x} "
                  f"leg-body={body if body is None else hex(body)} reached-body={reached}")
            if not reached:
                mism.append((sel, sig, body, r["pc"], r["stop"]))
        print(f"  execution reached the leg-derived body: {len(K) - len(mism)}/{len(K)}")
        for m in mism:
            print(f"    MISMATCH {m}")
        # non-planted PUSH4 immediates: must NOT dispatch to a planted body
        imm = sorted({m.group(1).hex() for m in re.finditer(rb"\x63(....)", code)})
        extras = [s for s in imm if s not in K.values()]
        print(f"\n  non-planted PUSH4 immediates ({len(extras)}):")
        for s in extras:
            r = run(code, int(s, 16))
            print(f"    {s} stop={r['stop']} pc={r['pc']:#06x} derived={derived.get(s)}")

    if probe:
        print("\n=== probe bytecode_offset vs leg-derived body ===")
        ok = 0
        fns = probe["normalized_result"]["functions"]
        for f in sorted(fns, key=lambda x: x["selector"]):
            sel = f["selector"][2:]
            d = derived.get(sel, {})
            same = d.get("body_entry") == f["bytecode_offset"]
            ok += same
            print(f"  {sel} probe={f['bytecode_offset']:#06x} derived={d.get('body_entry', 0):#06x} "
                  f"match={same} JUMPDEST@probe={code[f['bytecode_offset']] == JUMPDEST}")
        print(f"  agreement: {ok}/{len(fns)}")
        recovered = {f["selector"][2:] for f in fns}
        print(f"  probe recovered {len(recovered)} selectors; leg chains carry {len(derived)}")
        print(f"  probe set == leg-chain set: {recovered == set(derived)}")
        print(f"  probe extras: {sorted(recovered - set(derived))}")
        print(f"  leg-chain only: {sorted(set(derived) - recovered)}")


if __name__ == "__main__":
    main()
