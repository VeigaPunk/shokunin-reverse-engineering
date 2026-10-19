import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'compiled-viairvault'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def disassemble(code, end):
    instructions = []
    pc = 0
    names = {
        0x03: 'SUB', 0x10: 'LT', 0x11: 'GT', 0x14: 'EQ', 0x15: 'ISZERO',
        0x1c: 'SHR', 0x35: 'CALLDATALOAD', 0x36: 'CALLDATASIZE',
        0x50: 'POP', 0x56: 'JUMP', 0x57: 'JUMPI', 0x5b: 'JUMPDEST',
        0x5f: 'PUSH0', 0x80: 'DUP1', 0x90: 'SWAP1'
    }
    while pc < end:
        start = pc
        opcode = code[pc]
        pc += 1
        immediate = None
        if 0x60 <= opcode <= 0x7f:
            width = opcode - 0x5f
            immediate = code[pc:pc + width]
            if len(immediate) != width:
                raise ValueError(f'truncated PUSH at {start}')
            pc += width
        instructions.append({
            'pc': start,
            'opcode': opcode,
            'name': f'PUSH{opcode - 0x5f}' if 0x60 <= opcode <= 0x7f else names.get(opcode, f'OP_{opcode:02x}'),
            'immediate': immediate.hex() if immediate is not None else None,
            'value': int.from_bytes(immediate, 'big') if immediate is not None else None
        })
    return instructions


def inspect(version):
    directory = BASE / f'solc-{version}' / 'viair'
    runtime = (directory / 'runtime.bin').read_bytes()
    receipt = json.loads((directory / 'compile-receipt.json').read_text())
    census = json.loads((directory / 'selector-census.json').read_text())
    selectors = set(census['independentlyDerived'].values())
    cbor_length = int.from_bytes(runtime[-2:], 'big')
    cbor_start = len(runtime) - 2 - cbor_length
    if cbor_start <= 0 or cbor_start >= len(runtime):
        raise ValueError('invalid terminal metadata length')
    code = runtime[:cbor_start]
    instructions = disassemble(runtime, cbor_start)
    by_pc = {item['pc']: item for item in instructions}
    push4_sites = [item for item in instructions if item['opcode'] == 0x63]
    selector_sites = [item for item in push4_sites if item['immediate'] in selectors]
    rows = []
    for site in selector_sites:
        index = instructions.index(site)
        tail = instructions[index + 1:index + 4]
        sequence = [item['opcode'] for item in tail]
        recognized = len(tail) == 3 and sequence in ([0x14, 0x61, 0x57], [0x03, 0x61, 0x57])
        destination = tail[1]['value'] if recognized else None
        rows.append({
            'pc': site['pc'],
            'selector': site['immediate'],
            'compare': tail[0]['name'] if recognized else None,
            'destination': destination,
            'destinationIsJumpdest': destination in by_pc and by_pc[destination]['opcode'] == 0x5b,
            'instructions': [site, *tail]
        })
    order = [item['selector'] for item in rows]
    compareCounts = {op: sum(item['compare'] == op for item in rows) for op in ('EQ', 'SUB')}
    firstSelectorIndex = next((i for i, item in enumerate(instructions)
                               if item['opcode'] == 0x63 and item['immediate'] in selectors),
                              len(instructions))
    bodyPrefix = instructions[:firstSelectorIndex]
    allKnownSites = len(selector_sites) == len(selectors) and set(order) == selectors
    sortedOrder = order == sorted(order)
    compareShape = all(item['compare'] in ('EQ', 'SUB') for item in rows)
    if allKnownSites and sortedOrder and compareShape and compareCounts['SUB'] == 1:
        dispatchClass = f'ascending selector chain ({compareCounts["EQ"]} EQ legs, final selector uses SUB)'
    elif allKnownSites and sortedOrder and compareShape and compareCounts['SUB'] == 0:
        dispatchClass = f'ascending selector chain ({compareCounts["EQ"]} EQ legs)'
    else:
        dispatchClass = 'other measured selector-comparison arrangement'
    return {
        'compiler': receipt['solcVersion'],
        'runtimeBytes': len(runtime),
        'runtimeSha256': sha256(runtime),
        'preMetadataCodeBytes': cbor_start,
        'terminalCborBytes': cbor_length,
        'preMetadataCodeSha256': sha256(code),
        'metadataLengthPrefix': runtime[-2:].hex(),
        'abiFunctionCount': receipt['abiFunctionCount'],
        'receiveEntryCount': receipt['receiveEntryCount'],
        'push4SiteCount': len(push4_sites),
        'push4Sites': [{'pc': item['pc'], 'value': item['immediate']} for item in push4_sites],
        'knownSelectorPush4SiteCount': len(selector_sites),
        'allSelectorsLocated': allKnownSites,
        'selectorOrderAscending': sortedOrder,
        'compareCounts': compareCounts,
        'allSelectorSitesUseRecognizedCompareJumpSequence': compareShape,
        'selectorSites': rows,
        'dispatchPrefix': bodyPrefix,
        'dispatchClass': dispatchClass,
        'sourceSha256': receipt['sourceSha256']
    }


results = [inspect(version) for version in ('0.8.36', '0.8.37')]
results[0]['crossVersionPreMetadataCodeEqualTo'] = results[1]['preMetadataCodeSha256']
results[1]['crossVersionPreMetadataCodeEqualTo'] = results[0]['preMetadataCodeSha256']
results[0]['crossVersionPreMetadataCodeEqual'] = results[0]['preMetadataCodeSha256'] == results[1]['preMetadataCodeSha256']
results[1]['crossVersionPreMetadataCodeEqual'] = results[0]['preMetadataCodeSha256'] == results[1]['preMetadataCodeSha256']
output = {
    'source': 'viairvault-input/ViaIrVault.sol',
    'method': 'opcode-boundary disassembly of fresh compiler runtime.bin; terminal CBOR length read from last two bytes',
    'results': results
}
(ROOT / 'dispatch-census-viairvault.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
