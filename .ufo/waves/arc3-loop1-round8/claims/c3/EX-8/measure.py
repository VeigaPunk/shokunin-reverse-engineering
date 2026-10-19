#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys
from collections import Counter
from Crypto.Hash import keccak

compile_dir = pathlib.Path(sys.argv[1])
probe_dir = pathlib.Path(sys.argv[2])

OPCODES = {
    0x00: 'STOP', 0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x04: 'DIV',
    0x05: 'SDIV', 0x06: 'MOD', 0x10: 'LT', 0x11: 'GT', 0x14: 'EQ',
    0x15: 'ISZERO', 0x16: 'AND', 0x17: 'OR', 0x18: 'XOR', 0x1b: 'SHL',
    0x1c: 'SHR', 0x30: 'ADDRESS', 0x31: 'BALANCE', 0x32: 'ORIGIN',
    0x33: 'CALLER', 0x34: 'CALLVALUE', 0x35: 'CALLDATALOAD',
    0x36: 'CALLDATASIZE', 0x37: 'CALLDATACOPY', 0x38: 'CODESIZE',
    0x39: 'CODECOPY', 0x40: 'BLOCKHASH', 0x41: 'COINBASE',
    0x42: 'TIMESTAMP', 0x43: 'NUMBER', 0x44: 'PREVRANDAO',
    0x45: 'GASLIMIT', 0x46: 'CHAINID', 0x47: 'SELFBALANCE',
    0x48: 'BASEFEE', 0x50: 'POP', 0x51: 'MLOAD', 0x52: 'MSTORE',
    0x53: 'MSTORE8', 0x54: 'SLOAD', 0x55: 'SSTORE', 0x56: 'JUMP',
    0x57: 'JUMPI', 0x58: 'PC', 0x5a: 'GAS', 0x5b: 'JUMPDEST',
    0x5f: 'PUSH0', 0xf0: 'CREATE', 0xf1: 'CALL', 0xf3: 'RETURN',
    0xfa: 'STATICCALL', 0xfd: 'REVERT', 0xfe: 'INVALID', 0xff: 'SELFDESTRUCT',
}
for opcode in range(0x60, 0x80):
    OPCODES[opcode] = f'PUSH{opcode - 0x5f}'
for opcode in range(0x80, 0x90):
    OPCODES[opcode] = f'DUP{opcode - 0x7f}'
for opcode in range(0x90, 0xa0):
    OPCODES[opcode] = f'SWAP{opcode - 0x8f}'


def decode(path):
    text = path.read_text().strip()
    if text.startswith('0x'):
        text = text[2:]
    code = bytes.fromhex(text)
    instructions = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        immediate = b''
        if 0x60 <= opcode <= 0x7f:
            size = opcode - 0x5f
            immediate = code[pc:pc + size]
            pc += size
        instructions.append((start, OPCODES.get(opcode, f'0x{opcode:02x}'), immediate, pc))
    return code, instructions


def selector(signature):
    digest = keccak.new(digest_bits=256)
    digest.update(signature.encode())
    return digest.hexdigest()[:8]


def norm_selector(value):
    return value.lower().removeprefix('0x')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


abi = json.loads((compile_dir / 'gas.abi.json').read_text())
abi_functions = [item for item in abi if item.get('type') == 'function']
signatures = {
    item['name'] + '(' + ','.join(arg['type'] for arg in item.get('inputs', [])) + ')'
    for item in abi_functions
}
expected = {selector(signature) for signature in signatures}
method_ids = json.loads((compile_dir / 'gas.methodids.json').read_text())
method_selector_set = {norm_selector(value) for value in method_ids.values()}
assert len(abi_functions) == len(signatures) == len(expected) == len(method_ids) == 8
assert expected == method_selector_set

print(f'ABI_FUNCTIONS={len(abi_functions)} METHOD_IDS={len(method_ids)}')
print('ABI_SIGNATURES=' + ','.join(sorted(signatures)))
print('INDEPENDENT_KECCAK_SELECTORS=' + ','.join(sorted(expected)))
print('METHOD_ID_SELECTORS=' + ','.join(sorted(method_selector_set)))

results = {}
for mode in ('gas', 'noopt', 'codesize'):
    code, instructions = decode(compile_dir / f'{mode}.runtime.hex')
    code_sha = sha256(code)
    counts = Counter(name for _, name, _, _ in instructions)
    compiler_abi = json.loads((compile_dir / f'{mode}.abi.json').read_text())
    compiler_methods = json.loads((compile_dir / f'{mode}.methodids.json').read_text())
    mode_functions = [item for item in compiler_abi if item.get('type') == 'function']
    mode_methods = {norm_selector(value) for value in compiler_methods.values()}
    assert len(mode_functions) == len(compiler_methods) == 8
    assert mode_methods == expected

    probe = json.loads((probe_dir / f'{mode}.json').read_text())
    normalized = probe['normalized_result']
    raw_functions = probe['raw_result']['functions']
    normalized_functions = normalized['functions']
    normalized_selectors = {norm_selector(row['selector']) for row in normalized_functions}
    raw_selectors = {norm_selector(row['selector']) for row in raw_functions}
    decoded_sha = normalized['bytecode']['sha256']
    assert len(normalized_functions) == len(raw_functions) == 8
    assert normalized_selectors == raw_selectors == expected
    assert decoded_sha == code_sha
    results[mode] = (code, instructions, probe, normalized_functions)

    print(f'{mode.upper()}_RUNTIME_BYTES={len(code)} SHA256={code_sha}')
    print(f'{mode.upper()}_OP_COUNTS=' + ' '.join(
        f'{name}:{counts[name]}' for name in
        ('PUSH4', 'EQ', 'XOR', 'MOD', 'CODECOPY', 'JUMPDEST', 'JUMPI')
    ))
    print(
        f'{mode.upper()}_REA_KK=True ROWS={len(normalized_functions)} '
        f'RAW_ROWS={len(raw_functions)} DECODED_SHA_MATCH=True '
        f'EVIDENCE_ID={probe.get("evidence_id", "missing")}'
    )
    provider = probe.get('provider', {})
    if provider:
        print(f'{mode.upper()}_PROVIDER={provider.get("id")} VERSION={provider.get("version")}')
    print(f'{mode.upper()}_RAW_JSON_SHA256={sha256((probe_dir / f"{mode}.json").read_bytes())}')

    abi_mutability = {
        item['name'] + '(' + ','.join(arg['type'] for arg in item.get('inputs', [])) + ')': item.get('stateMutability')
        for item in mode_functions
    }
    inferred_mutability = {
        row['selector']: row.get('inferred_state_mutability')
        for row in normalized_functions
    }
    if all(value is not None for value in inferred_mutability.values()):
        inferred_by_signature = {}
        selector_to_signature = {selector(signature): signature for signature in signatures}
        for sel, value in inferred_mutability.items():
            inferred_by_signature[selector_to_signature[norm_selector(sel)]] = value
        agreement = sum(abi_mutability[sig] == inferred_by_signature[sig] for sig in signatures)
        print(f'{mode.upper()}_ABI_MUTABILITY={abi_mutability}')
        print(f'{mode.upper()}_REA_INFERRED_MUTABILITY={inferred_by_signature}')
        print(f'{mode.upper()}_MUTABILITY_AGREEMENT={agreement}/{len(signatures)}')

for mode in ('gas', 'noopt', 'codesize'):
    _, instructions, probe, norm_functions = results[mode]
    offset_by_selector = {norm_selector(row['selector']): row['bytecode_offset'] for row in norm_functions}
    opcode_at = {pc: name for pc, name, _, _ in instructions}
    offsets = sorted(set(offset_by_selector.values()))
    print(f'{mode.upper()}_REA_OFFSETS={offsets} OFFSET_OPCODES={sorted({opcode_at.get(offset, "not-opcode-boundary") for offset in offsets})}')

noopt_code, noopt_instructions, _, noopt_functions = results['noopt']
noopt_offsets = {norm_selector(row['selector']): row['bytecode_offset'] for row in noopt_functions}
noopt_push4 = [(pc, immediate.hex()) for pc, name, immediate, _ in noopt_instructions if name == 'PUSH4']
noopt_windows = []
for index, (pc, name, immediate, _) in enumerate(noopt_instructions):
    if name == 'PUSH4':
        window = noopt_instructions[index:index + 6]
        if [item[1] for item in window] == ['PUSH4', 'DUP2', 'EQ', 'ISZERO', 'PUSH2', 'JUMPI']:
            noopt_windows.append((pc, immediate.hex(), window[4][2].hex()))
assert len(noopt_push4) == len(noopt_windows) == 8
assert {signature for _, signature in noopt_push4} == expected
assert {selector_value for _, selector_value, _ in noopt_windows} == expected
noopt_deltas = {noopt_offsets[sel] - pc for pc, sel in noopt_push4}
assert noopt_deltas == {12}
print('NOOPT_EQ_WINDOWS=' + ','.join(f'{sel}@{pc:#x}->next-{dst}' for pc, sel, dst in noopt_windows))
print('NOOPT_SELECTOR_OFFSETS=' + ','.join(f'{sel}:{noopt_offsets[sel]}' for sel in sorted(expected)))
print(f'NOOPT_OFFSET_DELTA_FROM_PUSH4={sorted(noopt_deltas)} OFFSET_OPCODE={noopt_instructions[[row[0] for row in noopt_instructions].index(min(noopt_offsets.values()))][1]}')

codesize_code, codesize_instructions, _, codesize_functions = results['codesize']
first_codecopy_index = next(i for i, item in enumerate(codesize_instructions) if item[1] == 'CODECOPY')
assert first_codecopy_index >= 2
source_instruction = codesize_instructions[first_codecopy_index - 2]
size_instruction = codesize_instructions[first_codecopy_index - 1]
assert source_instruction[1] == 'PUSH2' and size_instruction[1] == 'PUSH1'
table_start = int.from_bytes(source_instruction[2], 'big')
copy_size = int.from_bytes(size_instruction[2], 'big')
table = codesize_code[table_start:]
header_size = len(table) - len(expected) * 7
assert table_start == 0x12b and copy_size == 0x1b and header_size == 5 and len(table) == 61
header = table[:header_size]
records = []
for index in range((len(table) - header_size) // 7):
    record = table[header_size + index * 7:header_size + (index + 1) * 7]
    sel = record[:4].hex()
    target = int.from_bytes(record[4:6], 'big')
    marker = record[6]
    assert sel in expected and marker == 0x25 and codesize_code[target] == 0x5b
    records.append((sel, target, marker))
assert len(records) == 8 and {sel for sel, _, _ in records} == expected
codesize_offsets = {norm_selector(row['selector']): row['bytecode_offset'] for row in codesize_functions}
assert set(codesize_offsets.values()) == {65}
print(f'CODESIZE_TABLE_START={table_start:#x} HEADER={header.hex()} TABLE_BYTES={len(table)} RECORDS={len(records)}')
print('CODESIZE_SELECTOR_TARGETS=' + ','.join(f'{sel}:{target:#x}' for sel, target, _ in records))
print('CODESIZE_REA_OFFSETS=' + ','.join(f'{sel}:{codesize_offsets[sel]}' for sel in sorted(expected)))
print('CODESIZE_SHARED_OFFSET_OPCODE=' + {pc: name for pc, name, _, _ in codesize_instructions}[65])

assert (compile_dir / 'noopt.runtime.hex').read_bytes() == (compile_dir / 'none.runtime.hex').read_bytes()
assert (compile_dir / 'gas.runtime.hex').read_bytes() == (compile_dir / 'gas-explicit.runtime.hex').read_bytes()
print('NOOPT_EQUALS_O_NONE=YES')
print('DEFAULT_GAS_EQUALS_EXPLICIT_O_GAS=YES')
