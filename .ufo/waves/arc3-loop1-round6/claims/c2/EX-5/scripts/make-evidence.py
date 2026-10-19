"""Seat EX-5 round6: emit probe-summary.json + assertions.txt from the sealed envelopes."""
import hashlib
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from keccak import selector  # noqa: E402

ROOT = pathlib.Path('/var/tmp/ex05-r6')
OUT = ROOT / 'evidence'
SETS = {
    'K8': [selector(f'f{i}(uint256)') for i in range(8)],
    'Ex05Vault': [selector(s) for s in ['alpha(uint256)', 'beta(uint256)', 'gamma(uint256)',
                                        'delta(uint256)', 'epsilon()', 'zeta()', 'eta()']],
}
LEGS = [
    ('K8', 'gas', '6.4.0'), ('K8', 'gas', '6.7.0'),
    ('K8', 'noopt', '6.4.0'), ('K8', 'noopt', '6.7.0'),
    ('K8', 'codesize', '6.4.0'), ('K8', 'codesize', '6.7.0'),
    ('Ex05Vault', 'gas', '6.4.0'),
    ('Ex05Vault', 'noopt', '6.4.0'), ('Ex05Vault', 'noopt', '6.7.0'),
    ('Ex05Vault', 'codesize', '6.4.0'), ('Ex05Vault', 'codesize', '6.7.0'),
    ('K8', 'hf-paris', '6.4.0'), ('K8', 'hf-london', '6.4.0'), ('K8', 'hf-cancun', '6.4.0'),
]
TRAPS = [
    ('K8', 'codesize', 'creation.hex', '6.4.0'),
    ('K8', 'codesize', 'rawonhex', '6.4.0'),
]

summary = {'real_legs': [], 'trap_legs': [], 'assertions': []}
ok = True


def note(cond, line):
    global ok
    ok = ok and cond
    summary['assertions'].append(('PASS' if cond else 'FAIL') + ' ' + line)


for carrier, form, pin in LEGS:
    p = ROOT / f'probe/{carrier}.{form}.hex.{pin}.json'
    j = json.loads(p.read_text())
    d = j.get('data', j)
    nr = d['normalized_result']
    fns = nr['functions']
    sels = sorted(f['selector'].removeprefix('0x') for f in fns)
    want = sorted(SETS[carrier])
    rt = (ROOT / f'out/{carrier}.{form}.runtime.hex').read_text().strip().removeprefix('0x')
    rt_sha = hashlib.sha256(bytes.fromhex(rt)).hexdigest()
    row = {
        'carrier': carrier, 'form': form, 'rea_pin': pin,
        'evidence_id': d['evidence_id'],
        'subject_file_sha256': j['subject']['digest']['sha256'],
        'decoded_sha256': nr['bytecode']['sha256'],
        'runtime_sha256': rt_sha,
        'functions': len(fns),
        'selectors': sels,
        'dispatch_values': sorted({f['dispatch'] for f in fns}),
        'offsets': {f['selector'].removeprefix('0x'): f['bytecode_offset'] for f in fns},
        'mutability': {f['selector'].removeprefix('0x'): f['inferred_state_mutability'] for f in fns},
        'arguments': {f['selector'].removeprefix('0x'): f['inferred_arguments'] for f in fns},
    }
    summary['real_legs'].append(row)
    note(len(fns) == len(want) and sels == want,
         f'{carrier}/{form}@{pin}: K={len(fns)} selectors==selftest-derived set')
    note(nr['bytecode']['sha256'] == rt_sha,
         f'{carrier}/{form}@{pin}: decoded sha256 == runtime file sha256')
    note(row['dispatch_values'] == ['abi'],
         f'{carrier}/{form}@{pin}: dispatch values == [abi]')

for carrier, form, kind, pin in TRAPS:
    p = ROOT / f'probe/K8.{form}.{kind}.{pin}.json'
    j = json.loads(p.read_text())
    d = j.get('data', j)
    nr = d['normalized_result']
    subj = j['subject']['digest']['sha256']
    row = {
        'carrier': carrier, 'form': form, 'kind': kind, 'rea_pin': pin,
        'evidence_id': d['evidence_id'],
        'subject_file_sha256': subj,
        'decoded_sha256': nr['bytecode']['sha256'],
        'functions': len(nr['functions']),
    }
    summary['trap_legs'].append(row)
    note(len(nr['functions']) == 0, f'{carrier}/{form}/{kind}@{pin}: parsed-and-empty (0 functions)')
    if kind == 'creation.hex':
        cb = hashlib.sha256((ROOT / f'out/{carrier}.{form}.creation.bin').read_bytes()).hexdigest()
        note(nr['bytecode']['sha256'] == cb,
             f'{carrier}/{form}/{kind}@{pin}: decoded sha256 == creation.bin sha256 (not byte absence)')
    else:
        note(nr['bytecode']['sha256'] == subj,
             f'{carrier}/{form}/{kind}@{pin}: decoded sha256 == input file sha256 (not byte absence)')

(OUT / 'probe-summary.json').write_text(json.dumps(summary, indent=1) + '\n')
(OUT / 'assertions.txt').write_text('\n'.join(summary['assertions']) + '\n')
print('\n'.join(summary['assertions']))
print('ALL PASS' if ok else 'SOME FAIL')
