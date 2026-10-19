import json
import pathlib
from Crypto.Hash import keccak

EVIDENCE = pathlib.Path(__file__).resolve().parent
abi = json.loads((EVIDENCE / 'abi.json').read_text())
method_ids = json.loads((EVIDENCE / 'method-identifiers.json').read_text())
functions = [item for item in abi if item.get('type') == 'function']

def canonical_type(item):
    typ = item['type']
    if typ.startswith('tuple'):
        suffix = typ[5:]
        return '(' + ','.join(canonical_type(x) for x in item['components']) + ')' + suffix
    return typ

selectors = {}
for fn in functions:
    signature = fn['name'] + '(' + ','.join(canonical_type(x) for x in fn.get('inputs', [])) + ')'
    h = keccak.new(digest_bits=256)
    h.update(signature.encode())
    selectors[signature] = h.digest()[:4].hex()

oracle = {value.removeprefix('0x') for value in method_ids.values()}
derived = set(selectors.values())
print(f'ABI functions={len(functions)} method_identifiers={len(method_ids)} independently_derived={len(derived)}')
print(f'ABI-Keccak == compiler method_identifiers: {derived == oracle}')
for signature, selector in sorted(selectors.items()):
    print(f'{selector} {signature}')
for form in ('gas', 'noopt', 'codesize'):
    evidence = json.loads((EVIDENCE / f'probe-durable-{form}.json').read_text())
    result = evidence.get('normalized_result', evidence)
    probe = {item['selector'].removeprefix('0x') for item in result['functions']}
    print(f'{form}: probe_K={len(probe)} probe_set==independent_Keccak={probe == derived} missing={sorted(derived-probe)} extra={sorted(probe-derived)} decoded_sha256={result["bytecode"]["sha256"]}')
