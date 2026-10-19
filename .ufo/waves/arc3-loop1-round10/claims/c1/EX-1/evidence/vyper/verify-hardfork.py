import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def disassemble(code):
    rows = []
    pc = 0
    while pc < len(code):
        start = pc
        opcode = code[pc]
        pc += 1
        immediate = None
        if 0x60 <= opcode <= 0x7F:
            width = opcode - 0x5F
            immediate = code[pc:pc + width]
            if len(immediate) != width:
                raise ValueError(f'truncated PUSH at {start}')
            pc += width
        rows.append({
            'pc': start,
            'opcode': opcode,
            'immediate': immediate.hex() if immediate is not None else None,
            'size': pc - start,
        })
    return rows


def inspect(target):
    compile_dir = ROOT / 'compile'
    abi = json.loads((compile_dir / f'{target}.abi.json').read_text())
    method_ids = json.loads((compile_dir / f'{target}.method-identifiers.json').read_text())
    settings = json.loads((compile_dir / f'{target}.settings.json').read_text())
    carrier = compile_dir / f'{target}.runtime.hex'
    carrier_bytes = carrier.read_bytes()
    runtime = bytes.fromhex(carrier.read_text().strip().removeprefix('0x'))
    no_metadata_hex = (compile_dir / f'{target}.no-metadata.runtime.hex').read_text().strip().removeprefix('0x')
    no_metadata_runtime = bytes.fromhex(no_metadata_hex)
    header = disassemble(runtime[:32])
    setup_pattern = [0x60, 0x60, 0x82, 0x06, 0x60, 0x1B, 0x61, 0x01, 0x60, 0x39]
    setup_sites = [
        i for i in range(len(header) - len(setup_pattern) + 1)
        if [row['opcode'] for row in header[i:i + len(setup_pattern)]] == setup_pattern
    ]
    if len(setup_sites) != 1:
        raise ValueError(f'{target} expected one modulo jump-table setup, found {len(setup_sites)}')
    setup = header[setup_sites[0]:setup_sites[0] + len(setup_pattern)]
    setup_constants_match = [setup[index]['immediate'] for index in (0, 1, 4, 8)] == ['02', '09', '01', '1e']
    slot_count = int(setup[1]['immediate'], 16)
    entry_width = 1 << int(setup[4]['immediate'], 16)
    table_offset = int(setup[6]['immediate'], 16)
    executable = runtime[:table_offset]
    jump_table = runtime[table_offset:]
    if len(jump_table) != slot_count * entry_width:
        raise ValueError(f'{target} table extent does not match its {slot_count} slots of {entry_width} bytes')
    instructions = disassemble(executable)
    opcode_walk_ends_at_table = bool(instructions) and instructions[-1]['pc'] + instructions[-1]['size'] == table_offset
    table_targets = [
        int.from_bytes(jump_table[offset:offset + entry_width], 'big')
        for offset in range(0, len(jump_table), entry_width)
    ]
    jumpdest_sites = {row['pc'] for row in instructions if row['opcode'] == 0x5B}
    table_targets_are_jumpdest = all(target_pc in jumpdest_sites for target_pc in table_targets)
    probe = json.loads((ROOT / 'probe' / f'{target}.json').read_text())

    signatures = [
        f"{item['name']}({','.join(arg['type'] for arg in item['inputs'])})"
        for item in abi if item.get('type') == 'function'
    ]
    abi_selectors = [method_ids[signature].removeprefix('0x').lower() for signature in signatures]
    push4_sites = [row for row in instructions if row['opcode'] == 0x63]
    selector_sites = []
    for index, row in enumerate(instructions):
        if row['opcode'] != 0x63:
            continue
        tail = instructions[index + 1:index + 5]
        pattern_matches = (
            len(tail) == 4 and
            [item['opcode'] for item in tail] == [0x81, 0x18, 0x61, 0x57]
        )
        selector_sites.append({
            'pc': row['pc'],
            'selector': row['immediate'],
            'xorCompareJumpPattern': pattern_matches,
            'fallthroughOffset': row['pc'] + 11 if pattern_matches else None,
        })

    rea_functions = probe['raw_result']['functions']
    rea_by_selector = {row['selector'].lower(): row for row in rea_functions}
    push_selectors = [row['selector'] for row in selector_sites]
    rea_selectors = list(rea_by_selector)
    offsets = []
    for site in selector_sites:
        result = rea_by_selector.get(site['selector'])
        offsets.append({
            'selector': site['selector'],
            'opcodePush4Pc': site['pc'],
            'reaBytecodeOffset': result['bytecodeOffset'] if result else None,
            'byteWalkFallthroughOffset': site['fallthroughOffset'],
            'match': result is not None and result['bytecodeOffset'] == site['fallthroughOffset'],
        })

    first_selector_pc = push4_sites[0]['pc'] if push4_sites else len(executable)
    names = {
        0x01: 'ADD', 0x02: 'MUL', 0x03: 'SUB', 0x06: 'MOD', 0x09: 'MULMOD',
        0x10: 'LT', 0x14: 'EQ', 0x18: 'XOR', 0x1B: 'SHL', 0x1C: 'SHR',
        0x35: 'CALLDATALOAD',
        0x36: 'CALLDATASIZE', 0x39: 'CODECOPY', 0x51: 'MLOAD', 0x52: 'MSTORE',
        0x56: 'JUMP', 0x57: 'JUMPI', 0x5B: 'JUMPDEST', 0x5F: 'PUSH0',
        0x81: 'DUP2', 0x82: 'DUP3', 0x90: 'SWAP1', 0xF3: 'RETURN', 0xFD: 'REVERT',
    }
    prologue = []
    for row in instructions:
        if row['pc'] >= first_selector_pc:
            break
        name = f"PUSH{row['opcode'] - 0x5F}" if 0x60 <= row['opcode'] <= 0x7F else names.get(row['opcode'], f"OP_{row['opcode']:02x}")
        prologue.append(name + (f' 0x{row["immediate"]}' if row['immediate'] is not None else ''))

    function_abi = [item for item in abi if item.get('type') == 'function']
    checks = {
        'compilerAbiKeysMatchMethodIdentifiers': set(method_ids) == set(signatures),
        'dispatcherSetupConstantsMatch': setup_constants_match,
        'compilerAbiAllView': bool(function_abi) and all(item.get('stateMutability') == 'view' for item in function_abi),
        'noMetadataRuntimeMatchesFullRuntime': runtime == no_metadata_runtime,
        'opcodeWalkEndsAtTableOffset': opcode_walk_ends_at_table,
        'jumpTableHasExpectedEntries': len(table_targets) == slot_count == 9,
        'jumpTableTargetsAreJumpdest': table_targets_are_jumpdest,
        'push4SelectorSetMatchesCompiler': sorted(push_selectors) == sorted(abi_selectors),
        'everyPush4IsXorCompareJump': len(selector_sites) == len(push4_sites) and all(row['xorCompareJumpPattern'] for row in selector_sites),
        'reaSelectorSetMatchesCompiler': sorted(rea_selectors) == sorted(abi_selectors),
        'reaAllDispatchAbi': all(row['dispatch'] == 'abi' for row in rea_functions),
        'reaDecodedDigestMatchesRuntime': probe['normalized_result']['bytecode']['sha256'] == sha256(runtime),
        'reaOffsetsMatchByteWalk': len(offsets) == len(rea_functions) and all(row['match'] for row in offsets),
    }
    return {
        'target': target,
        'compilerSettings': settings,
        'runtimeBytes': len(runtime),
        'runtimeSha256': sha256(runtime),
        'runtimeCodeBytes': len(executable),
        'runtimeCodeSha256': sha256(executable),
        'jumpTableOffset': table_offset,
        'jumpTableBytes': len(jump_table),
        'jumpTableHex': jump_table.hex(),
        'jumpTableSlots': slot_count,
        'jumpTableEntryWidthBytes': entry_width,
        'jumpTableTargets': table_targets,
        'jumpTableTargetsAreJumpdest': table_targets_are_jumpdest,
        'carrierHexSha256': sha256(carrier_bytes),
        'abiFunctionCount': len(signatures),
        'abiSignatures': signatures,
        'compilerAbiMutability': sorted({item.get('stateMutability') for item in function_abi}),
        'compilerSelectorCount': len(abi_selectors),
        'opcodeBoundaryPush4Count': len(push4_sites),
        'push4SelectorOrder': push_selectors,
        'dispatcherComparison': 'PUSH4; DUP2; XOR; PUSH2; JUMPI',
        'prologueOpcodes': prologue,
        'opcodeCounts': {
            'PUSH0': sum(row['opcode'] == 0x5F for row in instructions),
            'PUSH1_zero': sum(row['opcode'] == 0x60 and row['immediate'] == '00' for row in instructions),
            'ADD': sum(row['opcode'] == 0x01 for row in instructions),
            'MOD': sum(row['opcode'] == 0x06 for row in instructions),
            'CODECOPY': sum(row['opcode'] == 0x39 for row in instructions),
            'XOR': sum(row['opcode'] == 0x18 for row in instructions),
            'EQ': sum(row['opcode'] == 0x14 for row in instructions),
        },
        'selectorSites': selector_sites,
        'reaEvidenceId': probe['evidence_id'],
        'reaProvider': probe['provider'],
        'reaFunctionCount': len(rea_functions),
        'reaSelectorCount': len(rea_selectors),
        'reaMutabilityInference': sorted({row['stateMutability'] for row in rea_functions}),
        'reaDecodedBytecodeSha256': probe['normalized_result']['bytecode']['sha256'],
        'reaDiscoveryCompleteness': probe['normalized_result']['discovery_completeness'],
        'reaRuntimeExecution': probe['normalized_result']['runtime_execution'],
        'reaOffsets': offsets,
        'checks': checks,
    }


runs = [inspect(target) for target in ('cancun', 'paris')]
selector_sets_equal = sorted(runs[0]['push4SelectorOrder']) == sorted(runs[1]['push4SelectorOrder'])
cancun_offsets = {row['selector']: row['reaBytecodeOffset'] for row in runs[0]['reaOffsets']}
paris_offsets = {row['selector']: row['reaBytecodeOffset'] for row in runs[1]['reaOffsets']}
offset_deltas = {
    selector: paris_offsets[selector] - cancun_offsets[selector]
    for selector in sorted(cancun_offsets)
}
table_target_deltas = [
    paris - cancun
    for cancun, paris in zip(runs[0]['jumpTableTargets'], runs[1]['jumpTableTargets'])
]
result = {
    'sourceSha256': sha256((ROOT / 'source' / 'K8.vy').read_bytes()),
    'compilerIdentity': (ROOT / 'identity.txt').read_text().splitlines()[3:6],
    'method': 'fresh Vyper builds for explicit EVM targets, compiler ABI/method-id reconciliation, bounded opcode walk with jump-table boundary validation, and REA result/digest/offset reconciliation',
    'selectorSetsEqualAcrossTargets': selector_sets_equal,
    'runtimeBytesDeltaParisMinusCancun': runs[1]['runtimeBytes'] - runs[0]['runtimeBytes'],
    'runtimeCodeBytesDeltaParisMinusCancun': runs[1]['runtimeCodeBytes'] - runs[0]['runtimeCodeBytes'],
    'jumpTableBytesDeltaParisMinusCancun': runs[1]['jumpTableBytes'] - runs[0]['jumpTableBytes'],
    'reaOffsetDeltasParisMinusCancun': offset_deltas,
    'allReaOffsetsShiftByTwo': set(offset_deltas.values()) == {2},
    'jumpTableTargetDeltasParisMinusCancun': table_target_deltas,
    'allJumpTableTargetsShiftByTwo': len(table_target_deltas) == 9 and set(table_target_deltas) == {2},
    'runs': runs,
}
if (
    not selector_sets_equal or
    not result['allReaOffsetsShiftByTwo'] or
    not result['allJumpTableTargetsShiftByTwo'] or
    any(not all(run['checks'].values()) for run in runs)
):
    raise SystemExit('hardfork comparison checks failed')
print(json.dumps(result, indent=2))
