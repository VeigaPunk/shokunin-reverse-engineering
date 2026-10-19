import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
legs = {
    'solc-0.8.28-viaIR': (root / 'out' / 'viair-opt200', root / 'probe' / 'viair-opt200.json'),
    'solc-0.8.28-standard': (root / 'out' / 'std-opt200', root / 'probe' / 'std-opt200.json'),
    'solc-0.8.37-viaIR': (root / 'out-0837' / 'viair-opt200', root / 'probe-0837' / 'viair-opt200.json'),
}

def digest(value):
    return hashlib.sha256(value).hexdigest()

def decode(data):
    out = []
    pc = 0
    while pc < len(data):
        start = pc
        op = data[pc]
        pc += 1
        if op == 0x5f:
            name, imm = 'PUSH0', None
        elif 0x60 <= op <= 0x7f:
            width = op - 0x5f
            imm = data[pc:pc + width]
            name = f'PUSH{width}'
            pc += width
        else:
            names = {
                0x03: 'SUB', 0x10: 'LT', 0x11: 'GT', 0x14: 'EQ', 0x15: 'ISZERO',
                0x1c: 'SHR', 0x35: 'CALLDATALOAD', 0x36: 'CALLDATASIZE',
                0x57: 'JUMPI', 0x5b: 'JUMPDEST', 0x80: 'DUP1', 0xfd: 'REVERT',
            }
            name, imm = names.get(op, f'OP_{op:02X}'), None
        out.append((start, name, int.from_bytes(imm, 'big') if imm is not None else None))
    return out

def characterize(folder, probe_path):
    code = (folder / 'runtime.bin').read_bytes()
    abi_selectors = json.loads((folder / 'selectors-derived.json').read_text())
    expected = sorted({selector for _, selector in abi_selectors})
    ins = decode(code)
    dispatch_start = None
    for i in range(len(ins) - 4):
        if [item[1] for item in ins[i:i + 5]] == ['PUSH0', 'CALLDATALOAD', 'PUSH1', 'SHR', 'DUP1'] and ins[i + 2][2] == 0xE0:
            dispatch_start = i + 5
            break
    if dispatch_start is None:
        raise RuntimeError(f'no selector prologue in {folder}')
    selectors = []
    opclasses = []
    idx = dispatch_start
    while idx + 3 < len(ins):
        first, compare, dst, jump = ins[idx:idx + 4]
        if first[1] == 'PUSH4' and compare[1] in ('EQ', 'GT', 'SUB') and dst[1] == 'PUSH2' and jump[1] == 'JUMPI':
            selectors.append(f'{first[2]:08x}')
            opclasses.append(compare[1])
        idx += 1
    guard = [item[1] for item in ins[:12]]
    metadata_size = int.from_bytes(code[-2:], 'big')
    metadata_start = len(code) - metadata_size - 2
    record = {
        'runtime_bytes': len(code),
        'runtime_sha256': digest(code),
        'metadata_start': metadata_start,
        'metadata_length': metadata_size,
        'metadata_sha256': digest(code[metadata_start:]),
        'code_prefix_sha256': digest(code[:metadata_start]),
        'initial_guard_opcodes': guard,
        'has_lt_iszero_guard': any(guard[i:i + 4] == ['PUSH1', 'CALLDATASIZE', 'LT', 'ISZERO'] for i in range(len(guard) - 3)),
        'dispatcher_compare_classes': {name: opclasses.count(name) for name in sorted(set(opclasses))},
        'dispatcher_selectors': selectors,
        'dispatcher_comparison_site_count': len(selectors),
        'dispatcher_selector_count': len(set(selectors)),
        'dispatcher_sorted': selectors == sorted(selectors),
        'dispatcher_set_matches_abi': sorted(set(selectors)) == expected,
        'abi_function_count': len(abi_selectors),
    }
    if probe_path is not None:
        probe = json.loads(probe_path.read_text())
        recovered = sorted({item['selector'].removeprefix('0x') for item in probe['normalized_result']['functions']})
        record.update({
            'rea_evidence_id': probe['evidence_id'],
            'rea_provider': probe['provider']['id'],
            'rea_version': probe['provider']['version'],
            'rea_confidence': probe['confidence'],
            'rea_authority': probe['authority'],
            'rea_runtime_execution': probe['normalized_result']['runtime_execution'],
            'rea_decoded_sha256': probe['normalized_result']['bytecode']['sha256'],
            'rea_function_count': len(probe['normalized_result']['functions']),
            'rea_set_matches_abi': recovered == expected,
            'rea_decoded_sha_matches_runtime': probe['normalized_result']['bytecode']['sha256'] == digest(code),
        })
    return record

results = {name: characterize(folder, probe) for name, (folder, probe) in legs.items()}
a = (root / 'out' / 'viair-opt200' / 'runtime.bin').read_bytes()
b = (root / 'out-0837' / 'viair-opt200' / 'runtime.bin').read_bytes()
start_a = results['solc-0.8.28-viaIR']['metadata_start']
start_b = results['solc-0.8.37-viaIR']['metadata_start']
results['cross-version-viaIR'] = {
    'source_sha256': digest((root / 'src' / 'ViaIrVault.sol').read_bytes()),
    'runtime_lengths_equal': len(a) == len(b),
    'metadata_starts_equal': start_a == start_b,
    'pre-metadata_bytes_equal': a[:start_a] == b[:start_b],
    'first_pre-metadata_difference': next((i for i, (x, y) in enumerate(zip(a[:start_a], b[:start_b])) if x != y), None),
    'solc-0.8.28': results['solc-0.8.28-viaIR'],
    'solc-0.8.37': results['solc-0.8.37-viaIR'],
}
print(json.dumps(results, indent=2, sort_keys=True))
