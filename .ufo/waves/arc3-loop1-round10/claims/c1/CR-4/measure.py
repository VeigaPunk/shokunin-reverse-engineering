#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys
from collections import Counter

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
        instructions.append((start, OPCODES.get(opcode, f'0x{opcode:02x}'), immediate))
    return code, instructions


def norm_selector(value):
    return str(value).lower().removeprefix('0x')


results = {}
for target in ('london', 'prague'):
    runtime = compile_dir / f'{target}.runtime.hex'
    code, all_instructions = decode(runtime)
    codecopy_index = next(i for i, row in enumerate(all_instructions) if row[1] == 'CODECOPY')
    assert codecopy_index >= 3
    table_offset_instruction = all_instructions[codecopy_index - 3]
    assert table_offset_instruction[1] == 'PUSH2'
    assert all_instructions[codecopy_index - 2][1] == 'ADD'
    assert all_instructions[codecopy_index - 1][1] == 'PUSH1'
    table_start = int.from_bytes(table_offset_instruction[2], 'big')
    assert 0 < table_start < len(code)
    table_bytes = code[table_start:]
    instructions = [row for row in all_instructions if row[0] < table_start]
    assert instructions[-1][0] + 1 + len(instructions[-1][2]) == table_start
    digest = hashlib.sha256(code).hexdigest()
    counts = Counter(name for _, name, _ in instructions)
    settings = json.loads((compile_dir / f'{target}.settings.json').read_text())
    abi = json.loads((compile_dir / f'{target}.abi.json').read_text())
    methods = json.loads((compile_dir / f'{target}.methodids.json').read_text())
    functions = [entry for entry in abi if entry.get('type') == 'function']
    method_selectors = {norm_selector(value) for value in methods.values()}
    probe = json.loads((probe_dir / f'{target}.json').read_text())
    normalized = probe['normalized_result']
    raw_functions = probe['raw_result']['functions']
    normalized_functions = normalized['functions']
    normalized_selectors = {norm_selector(row['selector']) for row in normalized_functions}
    raw_selectors = {norm_selector(row['selector']) for row in raw_functions}
    decoded_digest = normalized['bytecode']['sha256']
    assert len(functions) == len(methods) == len(normalized_functions) == len(raw_functions) == 8
    assert method_selectors == normalized_selectors == raw_selectors
    assert decoded_digest == digest
    results[target] = {
        'code': code,
        'instructions': instructions,
        'digest': digest,
        'selectors': method_selectors,
        'probe': probe,
        'settings': settings,
    }
    print(f'{target.upper()}_SETTINGS={json.dumps(settings, sort_keys=True)}')
    print(f'{target.upper()}_RUNTIME_BYTES={len(code)} SHA256={digest}')
    print(f'{target.upper()}_CODE_SECTION_BYTES={table_start} TABLE_START={table_start:#x} TABLE_BYTES={len(table_bytes)} TABLE_HEX={table_bytes.hex()}')
    print(f'{target.upper()}_CODE_OP_COUNTS=' + ' '.join(
        f'{name}:{counts[name]}' for name in
        ('PUSH0', 'PUSH1', 'PUSH4', 'EQ', 'XOR', 'MOD', 'CODECOPY', 'JUMPDEST', 'JUMPI')
    ))
    push4_sites = [(pc, immediate.hex()) for pc, name, immediate in instructions if name == 'PUSH4']
    selector_windows = []
    for index, (pc, name, immediate) in enumerate(instructions):
        if name == 'PUSH4' and [row[1] for row in instructions[index:index + 5]] == ['PUSH4', 'DUP2', 'XOR', 'PUSH2', 'JUMPI']:
            selector_windows.append((pc, immediate.hex()))
    assert len(push4_sites) == len(selector_windows) == 8
    assert {selector for _, selector in push4_sites} == method_selectors
    assert {selector for _, selector in selector_windows} == method_selectors
    print('SELECTOR_XOR_WINDOWS=' + ','.join(f'{selector}@{pc:#x}' for pc, selector in selector_windows))
    print(f'{target.upper()}_FUNCTIONS={len(functions)} METHODS={len(methods)} RAW_ROWS={len(raw_functions)} NORMALIZED_ROWS={len(normalized_functions)} SELECTOR_SET_MATCH=True DECODED_SHA_MATCH=True')
    print(f'{target.upper()}_REA_EVIDENCE_ID={probe.get("evidence_id", "missing")} PROVIDER={probe.get("provider", {}).get("id")} VERSION={probe.get("provider", {}).get("version")}')
    offsets = sorted({row['bytecode_offset'] for row in normalized_functions})
    names_by_pc = {pc: name for pc, name, _ in instructions}
    print(f'{target.upper()}_REA_OFFSETS={offsets} OFFSET_OPCODES={sorted({names_by_pc.get(pc, "not-opcode-boundary") for pc in offsets})}')

assert results['london']['selectors'] == results['prague']['selectors']
print('CROSS_TARGET_SELECTOR_SET_EQUAL=True')
print(f'CROSS_TARGET_RUNTIME_BYTES_EQUAL={results["london"]["code"] == results["prague"]["code"]}')
for target in ('london', 'prague'):
    instructions = results[target]['instructions']
    leading = ' '.join(f'{pc:04x}:{name}' + (f'({immediate.hex()})' if immediate else '')
                       for pc, name, immediate in instructions[:24])
    print(f'{target.upper()}_FIRST_24_INSTRUCTIONS={leading}')
