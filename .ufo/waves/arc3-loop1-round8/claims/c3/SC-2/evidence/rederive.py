import hashlib
import json
import pathlib
import sys

MASK = (1 << 64) - 1
RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
ROT = [
    [0, 1, 62, 28, 27],
    [36, 44, 6, 55, 20],
    [3, 10, 43, 25, 39],
    [41, 45, 15, 21, 8],
    [18, 2, 61, 56, 14],
]
NAMES = {
    0x14: "EQ", 0x15: "ISZERO", 0x18: "XOR", 0x19: "MUL",
    0x06: "MOD", 0x39: "CODECOPY", 0x56: "JUMP", 0x57: "JUMPI",
    0x5B: "JUMPDEST", 0x81: "DUP2", 0x80: "DUP1", 0x34: "CALLVALUE",
}


def rol(v, n):
    if not n:
        return v
    return ((v << n) | (v >> (64 - n))) & MASK


def keccak256(data):
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)
    while len(padded) % rate != rate - 1:
        padded.append(0)
    padded.append(0x80)
    state = [0] * 25
    for start in range(0, len(padded), rate):
        block = padded[start:start + rate]
        for i in range(rate // 8):
            state[i] ^= int.from_bytes(block[8 * i:8 * i + 8], "little")
        for rc in RC:
            c = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
            d = [c[(x - 1) % 5] ^ rol(c[(x + 1) % 5], 1) for x in range(5)]
            for y in range(5):
                for x in range(5):
                    state[x + 5 * y] ^= d[x]
            b = [0] * 25
            for y in range(5):
                for x in range(5):
                    b[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], ROT[y][x])
            for y in range(5):
                for x in range(5):
                    state[x + 5 * y] = b[x + 5 * y] ^ ((~b[(x + 1) % 5 + 5 * y]) & b[(x + 2) % 5 + 5 * y])
            state[0] ^= rc
    return b"".join(v.to_bytes(8, "little") for v in state[:rate // 8])[:32]


def decode(raw):
    text = raw.decode().strip()
    return bytes.fromhex(text.removeprefix("0x"))


def instructions(code):
    result = []
    pc = 0
    while pc < len(code):
        start = pc
        op = code[pc]
        pc += 1
        imm = b""
        if 0x60 <= op <= 0x7f:
            size = op - 0x5f
            imm = code[pc:pc + size]
            pc += size
        result.append((start, op, imm))
    return result


def opname(op):
    if 0x60 <= op <= 0x7f:
        return f"PUSH{op - 0x5f}"
    return NAMES.get(op, f"0x{op:02x}")


def main(root):
    abi = json.loads((root / "abi.json").read_text())
    methodids = json.loads((root / "method-identifiers.json").read_text())
    signatures = []
    for entry in abi:
        if entry.get("type") != "function":
            continue
        sig = entry["name"] + "(" + ",".join(arg["type"] for arg in entry.get("inputs", [])) + ")"
        signatures.append(sig)
    selectors = sorted(keccak256(sig.encode())[:4].hex() for sig in signatures)
    method_selectors = sorted(v.removeprefix("0x") for v in methodids.values())
    print("keccak_empty=" + keccak256(b"").hex())
    print("keccak_transfer=" + keccak256(b"transfer(address,uint256)").hex())
    print("abi_function_count=" + str(len(signatures)))
    print("abi_signatures=" + ",".join(signatures))
    print("independent_selector_count=" + str(len(selectors)))
    print("independent_selectors=" + ",".join(selectors))
    print("compiler_methodid_count=" + str(len(methodids)))
    print("selector_set_matches_methodids=" + str(selectors == method_selectors))
    for mode in ("gas", "noopt", "codesize"):
        carrier_path = root / f"{mode}.runtime.hex"
        carrier = carrier_path.read_bytes()
        code = decode(carrier)
        ins = instructions(code)
        counts = {}
        for _, op, _ in ins:
            counts[opname(op)] = counts.get(opname(op), 0) + 1
        rei = json.loads((root / f"probe-{mode}-6.7.0.json").read_text())
        functions = rei["normalized_result"]["functions"]
        result_selectors = sorted(f["selector"].removeprefix("0x") for f in functions)
        offsets = sorted(f["bytecode_offset"] for f in functions)
        push4_pc = {imm.hex(): pc for pc, op, imm in ins if op == 0x63}
        offset_deltas = sorted((f["selector"].removeprefix("0x"), f["bytecode_offset"] - push4_pc[f["selector"].removeprefix("0x")]) for f in functions if f["selector"].removeprefix("0x") in push4_pc)
        print(f"[{mode}]")
        print(f"carrier_bytes={len(carrier)} carrier_sha256={hashlib.sha256(carrier).hexdigest()}")
        print(f"runtime_bytes={len(code)} runtime_sha256={hashlib.sha256(code).hexdigest()}")
        print("opcode_counts=" + ",".join(f"{k}:{counts[k]}" for k in sorted(counts)))
        print(f"PUSH4_sites={[(pc, imm.hex()) for pc, op, imm in ins if op == 0x63]}")
        print("CODECOPY_pcs=" + str([pc for pc, op, _ in ins if op == 0x39]))
        print("EQ_count=" + str(counts.get("EQ", 0)) + " MOD_count=" + str(counts.get("MOD", 0)))
        print("REA_evidence_id=" + rei["evidence_id"])
        print("REA_provider=" + rei["provider"]["id"] + "/" + rei["provider"]["version"])
        dispatch_counts = {}
        for function in functions:
            dispatch = function.get("dispatch")
            dispatch_counts[dispatch] = dispatch_counts.get(dispatch, 0) + 1
        print("REA_function_count=" + str(len(functions)) + " unique_selector_count=" + str(len(set(result_selectors))))
        print("REA_dispatch_counts=" + str(dispatch_counts))
        print("REA_selectors=" + ",".join(result_selectors))
        print("REA_missing=" + str(sorted(set(selectors) - set(result_selectors))))
        print("REA_extra=" + str(sorted(set(result_selectors) - set(selectors))))
        print("REA_offsets=" + str(offsets))
        print("REA_offsets_opcodes=" + str([(o, code[o], opname(code[o])) for o in offsets]))
        print("REA_offset_deltas_from_selector_PUSH4=" + str(offset_deltas))
        print("REA_discovery_completeness=" + str(rei["normalized_result"].get("discovery_completeness")))
        if mode == "noopt":
            sites = [(idx, row) for idx, row in enumerate(ins) if row[1] == 0x63]
            good = []
            for idx, row in sites:
                seq = ins[idx:idx + 6]
                good.append([opname(x[1]) for x in seq] == ["PUSH4", "DUP2", "EQ", "ISZERO", "PUSH2", "JUMPI"])
            print("noopt_selector_chain_sites=" + str(len(sites)) + " all_expected_sequence=" + str(all(good)))
            print("noopt_distinct_offset_deltas=" + str(sorted({delta for _, delta in offset_deltas})))
        if mode == "codesize":
            first_copy = next(i for i, row in enumerate(ins) if row[1] == 0x39)
            size_ins, source_ins, dest_ins = ins[first_copy - 3:first_copy]
            if (size_ins[1], source_ins[1], dest_ins[1]) != (0x60, 0x61, 0x60):
                raise ValueError("first CODECOPY source tuple has an unexpected instruction shape")
            start = int.from_bytes(source_ins[2], "big")
            tail = code[start:]
            locations = {selector: [i for i in range(len(tail)) if tail.startswith(bytes.fromhex(selector), i)] for selector in selectors}
            if any(len(found) != 1 for found in locations.values()):
                raise ValueError("selector bytes are not uniquely located in the table tail")
            record_starts = sorted(found[0] for found in locations.values())
            header_size = record_starts[0]
            record_width, remainder = divmod(len(tail) - header_size, len(selectors))
            if remainder or record_starts != [header_size + i * record_width for i in range(len(selectors))]:
                raise ValueError("selector bytes do not occupy a fixed-width tail table")
            parsed = [(selector, int.from_bytes(tail[pos + 4:pos + 6], "big"), tail[pos + 6]) for selector, found in locations.items() for pos in found]
            print(f"codesize_table_start=0x{start:x} first_CODECOPY_size={int.from_bytes(size_ins[2], 'big')} table_bytes={len(tail)} header={tail[:header_size].hex()} header_bytes={header_size} record_width={record_width}")
            print("codesize_table_records=" + str(parsed))
            print("codesize_table_selectors_match=" + str(sorted(x[0] for x in parsed) == selectors))
            print("codesize_targets_are_jumpdest=" + str(all(code[x[1]] == 0x5b for x in parsed)))
            print("codesize_record_terminal_bytes=" + str(sorted(set(x[2] for x in parsed))))


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
