#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
sys.dont_write_bytecode = True
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bytewalk', ROOT / 'characterize.py')
bytewalk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bytewalk)
abi = json.loads((ROOT / 'K8.abi.json').read_text())
method_ids = json.loads((ROOT / 'K8.methodids.json').read_text())
expected = {v.lower().removeprefix('0x') for v in method_ids.values()}
assert len([x for x in abi if x.get('type') == 'function']) == 8
assert len(method_ids) == 8 and len(expected) == 8
print(f'ABI_FUNCTIONS={len([x for x in abi if x.get("type") == "function"])} METHOD_IDS={len(method_ids)}')
print(f'EXPECTED_SELECTORS={sorted(expected)}')

for tag in ('noopt', 'codesize'):
    runtime_path = ROOT / f'K8.{tag}.runtime.hex'
    code, ins = bytewalk.decode(runtime_path)
    code_sha = hashlib.sha256(code).hexdigest()
    names = [x[1] for x in ins]
    counts = Counter(names)
    probe = json.loads((ROOT / f'K8.{tag}.json').read_text())
    norm = probe['normalized_result']
    raw_functions = probe['raw_result']['functions']
    recovered = {x['selector'].lower().removeprefix('0x') for x in norm['functions']}
    raw_recovered = {x['selector'].lower().removeprefix('0x') for x in raw_functions}
    assert recovered == expected
    assert raw_recovered == expected
    assert len(norm['functions']) == len(raw_functions) == 8
    assert norm['bytecode']['sha256'] == code_sha
    print(f'{tag.upper()}_RUNTIME_BYTES={len(code)} BYTECODE_SHA256={code_sha}')
    print(f'{tag.upper()}_OP_COUNTS=' + ' '.join(f'{k}:{counts[k]}' for k in ('PUSH4','EQ','XOR','MOD','CODECOPY','JUMPDEST','JUMPI')))
    print(f'{tag.upper()}_PROBE_KK=True RAW_KK=True DECODED_SHA_MATCH=True EVIDENCE_ID={probe["evidence_id"]}')
    if tag == 'noopt':
        chain = []
        for i, (pc, name, imm, nxt) in enumerate(ins):
            if name != 'PUSH4':
                continue
            window = ins[i:i+6]
            if [x[1] for x in window] == ['PUSH4','DUP2','EQ','ISZERO','PUSH2','JUMPI']:
                chain.append((imm, pc, window[4][2]))
        assert {x[0] for x in chain} == expected and len(chain) == 8
        print(f'NOOPT_EQ_LEGS={len(chain)} FIRST_LEG={chain[0][0]}@{chain[0][1]:#x}->next-test-{chain[0][2]}')
    else:
        assert counts['PUSH4'] == 0 and counts['CODECOPY'] == 2 and counts['MOD'] == 1 and counts['EQ'] == 1
        targets = []
        for selector in sorted(expected):
            needle = bytes.fromhex(selector)
            positions = [i for i in range(len(code)) if code.startswith(needle, i)]
            assert len(positions) == 1
            pos = positions[0]
            target = int.from_bytes(code[pos+4:pos+6], 'big')
            assert code[pos+6] == 0x25 and code[target] == 0x5b
            targets.append((selector, pos, target))
        assert len(targets) == 8
        print(f'CODESIZE_PACKED_RECORDS={len(targets)} TABLE_RANGE=0x12b..0x167 TARGETS_ARE_JUMPDEST=True')
        print('CODESIZE_SELECTOR_TARGETS=' + ','.join(f'{s}:{t:#x}' for s,_,t in targets))
    offsets = [x.get('bytecode_offset') for x in norm['functions']]
    ins_at = {pc:name for pc,name,_,_ in ins}
    print(f'{tag.upper()}_PROBE_OFFSETS={sorted(set(offsets))} OFFSET_OPCODE_NAMES={sorted({ins_at.get(x, "not-opcode-boundary") for x in offsets})}')

noopt = (ROOT / 'K8.noopt.runtime.hex').read_bytes()
none = (ROOT / 'K8.none.runtime.hex').read_bytes()
assert noopt == none
print('NOOPT_EQUALS_O_NONE=YES')
