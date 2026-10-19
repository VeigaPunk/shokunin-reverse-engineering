import hashlib
import json
import pathlib

root = pathlib.Path(__file__).parent

MASK = (1 << 64) - 1
RC = (
    0x0000000000000001, 0x0000000000008082, 0x800000000000808A,
    0x8000000080008000, 0x000000000000808B, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008A,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000A,
    0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800A, 0x800000008000000A, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
)
ROT = (
    (0, 36, 3, 41, 18), (1, 44, 10, 45, 2), (62, 6, 43, 15, 61),
    (28, 55, 25, 21, 56), (27, 20, 39, 8, 14),
)


def rol(value, shift):
    if shift == 0:
        return value
    return ((value << shift) | (value >> (64 - shift))) & MASK


def keccak_f(state):
    for rc in RC:
        columns = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
        delta = [columns[(x - 1) % 5] ^ rol(columns[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                state[x + 5 * y] ^= delta[x]
        moved = [0] * 25
        for x in range(5):
            for y in range(5):
                moved[y + 5 * ((2 * x + 3 * y) % 5)] = rol(state[x + 5 * y], ROT[x][y])
        for x in range(5):
            for y in range(5):
                state[x + 5 * y] = moved[x + 5 * y] ^ ((~moved[(x + 1) % 5 + 5 * y]) & moved[(x + 2) % 5 + 5 * y])
        state[0] ^= rc


def keccak256(data):
    rate = 136
    padded = bytearray(data)
    padded.append(0x01)
    padded.extend(b"\x00" * ((rate - len(padded) % rate) % rate))
    padded[-1] |= 0x80
    state = [0] * 25
    for start in range(0, len(padded), rate):
        block = padded[start:start + rate]
        for index in range(rate // 8):
            state[index] ^= int.from_bytes(block[index * 8:index * 8 + 8], "little")
        keccak_f(state)
    return b"".join(value.to_bytes(8, "little") for value in state)[:32]


assert keccak256(b"").hex() == "c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470"
assert keccak256(b"transfer(address,uint256)").hex()[:8] == "a9059cbb"

for fork in ("london", "prague"):
    base = root / "compile" / fork
    abi = json.loads((base / "abi.json").read_text())
    method_ids = json.loads((base / "method_identifiers.json").read_text())
    functions = [entry for entry in abi if entry.get("type") == "function"]
    signatures = {
        entry["name"] + "(" + ",".join(arg["type"] for arg in entry["inputs"]) + ")"
        for entry in functions
    }
    expected = {signature: keccak256(signature.encode()).hex()[:8] for signature in signatures}
    compiler = {signature: selector.removeprefix("0x").lower().zfill(8) for signature, selector in method_ids.items()}
    assert expected == compiler, (fork, expected, compiler)
    raw_hex = (base / "runtime.hex").read_text().strip().removeprefix("0x")
    runtime = bytes.fromhex(raw_hex)
    runtime_sha = hashlib.sha256(runtime).hexdigest()
    assert runtime.startswith(bytes.fromhex("60003560e01c60026007820660011b") if fork == "london" else bytes.fromhex("5f3560e01c60026007820660011b"))
    boundaries = set()
    pc = 0
    while pc < len(runtime):
        boundaries.add(pc)
        opcode = runtime[pc]
        pc += 1 + (opcode - 0x5F if 0x60 <= opcode <= 0x7F else 0)
    targets = []
    for selector in expected.values():
        pattern = bytes.fromhex("63" + selector + "811861")
        matches = [
            offset for offset in boundaries
            if runtime.startswith(pattern, offset) and runtime[offset + 10:offset + 11] == b"\x57"
        ]
        assert len(matches) == 1, (fork, selector, matches)
        offset = matches[0]
        targets.append((selector, offset, int.from_bytes(runtime[offset + 8:offset + 10], "big")))
    probe = json.loads((root / "probe" / f"{fork}.json").read_text())
    raw_functions = probe["raw_result"]["functions"]
    normalized_functions = probe["normalized_result"]["functions"]
    decoded = probe["normalized_result"]["bytecode"]
    expected_selectors = set(expected.values())
    raw_selectors = {entry["selector"].removeprefix("0x").lower().zfill(8) for entry in raw_functions}
    normalized_selectors = {entry["selector"].removeprefix("0x").lower().zfill(8) for entry in normalized_functions}
    assert len(raw_functions) == len(normalized_functions) == len(expected)
    assert raw_selectors == normalized_selectors == expected_selectors
    assert all(entry["dispatch"] == "abi" for entry in raw_functions + normalized_functions)
    abi_mutability = {}
    for entry in functions:
        signature = entry["name"] + "(" + ",".join(arg["type"] for arg in entry["inputs"]) + ")"
        abi_mutability[expected[signature]] = entry["stateMutability"]
    inferred_mutability = {
        entry["selector"].removeprefix("0x").lower().zfill(8): entry["inferred_state_mutability"]
        for entry in normalized_functions
    }
    mutability_agreement = sum(abi_mutability[selector] == inferred_mutability[selector] for selector in expected_selectors)
    assert decoded["sha256"] == runtime_sha and decoded["bytes"] == len(runtime)
    carrier_sha = hashlib.sha256((base / "runtime.hex").read_bytes()).hexdigest()
    assert probe["subject"]["digest"]["sha256"] == carrier_sha
    print(f"{fork}: abi_functions={len(functions)} method_ids={len(method_ids)} independently_derived={len(expected)} runtime_bytes={len(runtime)} runtime_sha256={runtime_sha}")
    print(f"{fork}: signatures={','.join(sorted(expected))}")
    print(f"{fork}: selectors={','.join(expected[key] for key in sorted(expected))}")
    print(f"{fork}: head_hex={runtime[:17].hex()} selector_xor_legs={len(targets)}/{len(expected)} opcode_boundary_matches={len(targets)}/{len(expected)}")
    print(f"{fork}: selector_pcs_and_targets={','.join(f'{selector}@0x{offset:x}->0x{target:x}' for selector, offset, target in sorted(targets, key=lambda item: item[1]))}")
    print(f"{fork}: rea_evidence_id={probe['evidence_id']} raw={len(raw_functions)} normalized={len(normalized_functions)} selector_sets_match=True dispatch_abi={len(normalized_functions)}/{len(expected)} decoded_sha_matches=True decoded_bytes={decoded['bytes']} completeness={probe['normalized_result']['discovery_completeness']} runtime_execution={probe['normalized_result']['runtime_execution']}")
    abi_counts = {state: list(abi_mutability.values()).count(state) for state in sorted(set(abi_mutability.values()))}
    inferred_counts = {state: list(inferred_mutability.values()).count(state) for state in sorted(set(inferred_mutability.values()))}
    print(f"{fork}: abi_mutability={abi_counts} rea_inferred_mutability={inferred_counts} agreement={mutability_agreement}/{len(expected)}")
    print(f"{fork}: rea_hardfork={decoded['hardfork']} metadata_status={decoded['metadata']['status']} carrier_sha256={carrier_sha}")
