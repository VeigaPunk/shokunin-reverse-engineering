import hashlib
import json
import re
from pathlib import Path

ROOT = Path.cwd()
BASE = Path('.ufo/waves')
HEX8 = re.compile(r'(?<![0-9a-fA-F])(?:0x)?([0-9a-fA-F]{8})(?![0-9a-fA-F])')


def data_bytes(path):
    path = Path(path)
    raw = path.read_bytes()
    if path.suffix == '.hex' or path.name == 'Smoke_sol_Smoke.bin':
        text = raw.decode('ascii').strip()
        if text.startswith(('0x', '0X')):
            text = text[2:]
        return raw, bytes.fromhex(text)
    return raw, raw


def normalize_selector(value):
    text = str(value).lower().removeprefix('0x')
    if re.fullmatch(r'[0-9a-f]{1,8}', text):
        return text.zfill(8)
    return None


def selectors_from(path):
    path = Path(path)
    raw = path.read_text()
    if path.suffix != '.json':
        return {m.group(1).lower() for m in HEX8.finditer(raw)}
    obj = json.loads(raw)
    vals = []
    if isinstance(obj, dict):
        if isinstance(obj.get('planted_selectors'), dict):
            vals = list(obj['planted_selectors'].values())
        elif isinstance(obj.get('selectors'), (list, dict)):
            vals = list(obj['selectors'].values()) if isinstance(obj['selectors'], dict) else obj['selectors']
        elif isinstance(obj.get('entries'), list):
            vals = [x.get('selector') for x in obj['entries'] if isinstance(x, dict)]
        elif isinstance(obj.get('functions'), list):
            vals = [x.get('selector', x.get('selectorHex')) for x in obj['functions'] if isinstance(x, dict)]
        elif isinstance(obj.get('push4_sites'), list):
            vals = [x.get('imm') for x in obj['push4_sites'] if isinstance(x, dict)]
        else:
            vals = list(obj.values())
    return {selector for v in vals if (selector := normalize_selector(v))}


def abi_method_selectors(abi_path, methods_path):
    abi = json.loads(Path(abi_path).read_text())
    methods = json.loads(Path(methods_path).read_text())
    signatures = []
    for item in abi:
        if item.get('type') == 'function':
            signatures.append(item['name'] + '(' + ','.join(i['type'] for i in item.get('inputs', [])) + ')')
    return {selector for sig in signatures if sig in methods and (selector := normalize_selector(methods[sig]))}


def probe_data(path):
    obj = json.loads(Path(path).read_text())
    nr = obj.get('normalized_result')
    rr = obj.get('raw_result')
    if isinstance(nr, dict):
        functions = nr.get('functions')
        bytecode = nr.get('bytecode') if isinstance(nr.get('bytecode'), dict) else {}
    else:
        functions, bytecode = None, {}
    if functions is None and isinstance(rr, dict):
        functions = rr.get('functions', [])
    if functions is None:
        functions = []
    selectors = {selector for x in functions if (selector := normalize_selector(x.get('selector', '')))}
    digest = bytecode.get('sha256')
    decoded_hex = bytecode.get('hex')
    if decoded_hex:
        decoded = bytes.fromhex(decoded_hex)
        computed = hashlib.sha256(decoded).hexdigest()
        digest_ok = computed == digest
    else:
        computed, digest_ok = 'n/a', 'n/a'
    offsets = []
    for f in functions:
        off = f.get('bytecode_offset', f.get('bytecodeOffset'))
        if isinstance(off, int):
            offsets.append((str(f.get('selector', '')).lower().removeprefix('0x'), off))
    return obj, selectors, len(functions), digest, computed, digest_ok, offsets


carriers = [
    ('r1 Rv2Token runtime hex', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex'),
    ('r1 Rv2Token runtime bin', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.bin'),
    ('r1 Rv2Token creation hex', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.creation.hex'),
    ('r1 Rv2Many runtime hex', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/Rv2Many.runtime.hex'),
    ('r1 KdxToken runtime hex', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/target-KdxToken.runtime.hex'),
    ('r1 KdxToken runtime bin', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-07/target-KdxToken.runtime.bin'),
    ('r1 Smoke creation bin', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/out/Smoke_sol_Smoke.bin'),
    ('r3 VaultB opt200 runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.hex'),
    ('r3 VaultB opt200 runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.bin'),
    ('r3 VaultB nopt runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.nopt.runtime.hex'),
    ('r3 VaultB nopt runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.nopt.runtime.bin'),
    ('r3 carrierB opt200 runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.hex'),
    ('r3 carrierB opt200 runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.bin'),
    ('r3 carrierB noopt runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-noopt.hex'),
    ('r3 carrierB noopt runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-noopt.bin'),
    ('r3 CarrierB runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.hex'),
    ('r3 CarrierB runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.bin'),
    ('r3 CarrierBErr runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/attack/out/CarrierBErr.runtime.hex'),
    ('r3 Rv2TokenOpt runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.runtime.hex'),
    ('r3 Rv2TokenOpt runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.runtime.bin'),
    ('r3 CarrierA runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/evidence/carrierA.runtime.hex'),
    ('r3 OptVault runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault.runtime.hex'),
    ('r3 OptVault runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault.runtime.bin'),
    ('r3 MutMix runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix.runtime.hex'),
    ('r3 MutMix runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix.runtime.bin'),
    ('r3 MutMixOpt runtime hex', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMixOpt.runtime.hex'),
    ('r3 MutMixOpt runtime bin', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMixOpt.runtime.bin'),
    ('r4 CarrierV runtime hex', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.hex'),
    ('r4 CarrierV runtime bin', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin'),
    ('r4 Ex09Vault runtime hex', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.hex'),
    ('r4 Ex09Vault runtime bin', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.bin'),
    ('r4 StewardToken runtime hex', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/runtime.hex'),
    ('r4 CarrierW runtime hex', '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.runtime.hex'),
    ('r4 Smoke runtime hex', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/Smoke.runtime.hex'),
]

sources = [
    ('r1 Rv2Token source', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.sol'),
    ('r1 KdxToken source', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/KdxToken.sol'),
    ('r1 Rv2Many source', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/Rv2Many.sol'),
    ('r1 Smoke source', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-02/smoke/Smoke.sol'),
    ('r3 VaultB source', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/VaultB.sol'),
    ('r3 carrierB source', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/carrierB.sol'),
    ('r3 CarrierB source', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/src/CarrierB.sol'),
    ('r3 CarrierBErr source', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/src/attack/CarrierBErr.sol'),
    ('r3 CarrierA source', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/carrierA.sol'),
    ('r3 OptVault source', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault.sol'),
    ('r3 MutMix source', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix.sol'),
    ('r4 CarrierV source', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/src/CarrierV.vy'),
    ('r4 Ex09Vault source', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/vyper/Ex09Vault.vy'),
    ('r4 StewardToken source', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/token.vy'),
    ('r4 CarrierW source', '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/src/CarrierW.vy'),
    ('r4 Smoke source', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/Smoke.vy'),
]

probes = [
    ('r1 Rv2Token', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt', [
        '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.7.0.json']),
    ('r1 Rv2Many', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/expected-many.txt', [
        '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/attack/probe-many.json']),
    ('r1 KdxToken', '.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/planted-K.json', [
        '.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round1/claims/c1/EX-06/evidence/run-raw-6.7.0.json']),
    ('r1 Smoke creation', None, ['.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-EX02-smoke-bin-6.4.0.json']),
    ('r1 Rv2Token creation', None, ['.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-creation-hex-6.4.0.json']),
    ('r3 VaultB opt200', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/planted-K.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-opt200-raw-6.7.0.json']),
    ('r3 VaultB nopt', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/planted-K.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-nopt-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-nopt-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-nopt-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/probe/probe-B-nopt-raw-6.7.0.json']),
    ('r3 carrierB EX04 opt200', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/planted-B-opt200.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-opt200-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-opt200-rawbin-6.4.0.json']),
    ('r3 carrierB EX04 opt200 raw-on-hex trap', None, [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-opt200-raw-6.4.0.json']),
    ('r3 carrierB EX04 noopt', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/planted-B-noopt.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-noopt-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-noopt-rawbin-6.4.0.json']),
    ('r3 carrierB EX04 noopt raw-on-hex trap', None, [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/probe/probe-noopt-raw-6.4.0.json']),
    ('r3 CarrierB', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/planted-K.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/probe/probe-runtime-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/probe/probe-runtime-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/probe/probe-runtime-raw-6.4.0.json']),
    ('r3 CarrierBErr', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/planted-K.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/attack/probe-runtime-hex-6.4.0.json']),
    ('r3 Rv2TokenOpt', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/Rv2TokenOpt.planted-K.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.5.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-raw-6.5.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/optB-raw-6.7.0.json']),
    ('r3 CarrierA secondary', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/evidence/carrierA.methodIdentifiers.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/evidence/probe-carrierA-bin-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/evidence/probe-carrierA-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/EX-02/evidence/probe-carrierA-hex-6.7.0.json']),
    ('r3 OptVault secondary', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/planted-K-pl1OptVault.json', [
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.4.0-hex.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.4.0-raw.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.7.0-hex.json']),
    ('r3 MutMix secondary', None, [
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix-6.4.0-hex.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix-6.4.0-raw.json',
        '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMix-6.7.0-hex.json']),
    ('r3 MutMixOpt secondary', None, ['.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/MutMixOpt-6.4.0-hex.json']),
    ('r4 CarrierV', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/planted-K.json', [
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-raw.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.7.0-hex.json']),
    ('r4 Ex09Vault', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/planted/planted-K.json', [
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-hex-6.4.0.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-raw-6.4.0.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-hex-6.7.0.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-raw-6.7.0.json']),
    ('r4 StewardToken', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-03/method-identifiers.json', [
        '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/EX03-6.4.0-hex.json']),
    ('r4 CarrierW', '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.method-identifiers.json', [
        '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/CarrierW-6.4.0-hex.json',
        '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/CarrierW-6.7.0-hex.json']),
    ('r4 Smoke', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-02/smoke/method-identifiers.txt', [
        '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/probe/Smoke-6.4.0-hex.json']),
]


def expected_for(label, path):
    if label == 'r4 StewardToken':
        return {selector for k, v in json.loads(Path(path).read_text()).items()
                if k != '__default__()' and (selector := normalize_selector(v))}
    if label == 'r4 CarrierW':
        return abi_method_selectors(
            '.ufo/waves/arc3-loop1-round4/claims/c1/PL-1/evidence/CarrierW.abi.json', path)
    if label in ('r3 OptVault secondary', 'r3 MutMix secondary', 'r3 MutMixOpt secondary'):
        from runpy import run_path
        helper = run_path('.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/keccak256.py')
        keccak256 = helper['keccak256']
        assert keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
        sig_path = ('OptVault' if label == 'r3 OptVault secondary' else 'MutMix')
        sig_file = Path(f'.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/sigs-{sig_path}.txt')
        return {keccak256(sig.encode()).hex()[:8] for sig in sig_file.read_text().splitlines() if sig}
    if path is None:
        return None
    return selectors_from(path)


def print_carriers():
    print('CARRIERS: stored_bytes decoded_bytes file_sha256 decoded_sha256')
    for label, path in carriers:
        raw, decoded = data_bytes(path)
        print(f'{label} | file={path} | stored={len(raw)} decoded={len(decoded)} file_sha256={hashlib.sha256(raw).hexdigest()} decoded_sha256={hashlib.sha256(decoded).hexdigest()}')


def print_sources():
    print('SOURCES: stored_bytes sha256')
    for label, path in sources:
        raw = Path(path).read_bytes()
        print(f'{label} | file={path} | stored={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}')


def print_probes():
    print('PROBES: count/distinct vs independent expected selector set; decoded digest recomputed from normalized bytecode.hex')
    for label, expected_path, paths in probes:
        expected = expected_for(label, expected_path)
        for path in paths:
            obj, observed, count, digest, computed, digest_ok, offsets = probe_data(path)
            if expected is None:
                match, missing, extra = 'n/a', [], []
            else:
                missing, extra = sorted(expected - observed), sorted(observed - expected)
                match = not missing and not extra and len(expected) == count
            jumptargets = 'n/a'
            if offsets and digest_ok is True:
                code = bytes.fromhex(obj['normalized_result']['bytecode']['hex'])
                jumptargets = f'{sum(off < len(code) and code[off] == 0x5b for _, off in offsets)}/{len(offsets)}'
            print(f'{label} | {path} | functions={count} distinct={len(observed)} expected={len(expected) if expected is not None else "n/a"} set_match={match} missing={missing} extra={extra} bytecode_sha256={digest} recomputed={computed} digest_ok={digest_ok} JUMPDEST_offsets={jumptargets}')


def instructions(data):
    result = []
    pc = 0
    while pc < len(data):
        op = data[pc]
        n = op - 0x5f if 0x60 <= op <= 0x7f else 0
        end = min(len(data), pc + 1 + n)
        imm = data[pc + 1:end] if n else b''
        result.append((pc, op, imm))
        pc += 1 + n
    return result


def cbor_code_end(data):
    if len(data) < 2:
        return len(data)
    metadata_len = int.from_bytes(data[-2:], 'big')
    end = len(data) - metadata_len - 2
    return end if 0 <= end <= len(data) - 2 else len(data)


def eq_push2_jumpi_sites(data):
    ins = instructions(data[:cbor_code_end(data)])
    return [(ins[i][0], ins[i][2].hex()) for i in range(len(ins) - 3)
            if ins[i][1] == 0x63 and ins[i + 1][1] == 0x14 and ins[i + 2][1] == 0x61 and ins[i + 3][1] == 0x57]


def print_r1_erratum():
    runtime_path = Path('.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.bin')
    runtime = runtime_path.read_bytes()
    creation_raw, creation = data_bytes('.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.creation.hex')
    code_end = cbor_code_end(runtime)
    creation_code_end = cbor_code_end(creation)
    embedded = creation.find(runtime[:code_end])
    marker = bytes.fromhex('16ee4b79')
    runtime_sites = [i for i in range(len(runtime)) if runtime.startswith(marker, i)]
    code_sites = [i for i in range(code_end) if runtime.startswith(marker, i)]
    expected = selectors_from('.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/expected-selectors.txt')
    push4s = [(pc, imm.hex()) for pc, op, imm in instructions(runtime[:code_end]) if op == 0x63]
    nonselectors = [(pc, imm) for pc, imm in push4s if imm not in expected]
    print('R1 ERRATUM:')
    print(f'Rv2Token runtime bytes={len(runtime)} code_end={code_end} creation decoded_bytes={len(creation)} creation_code_end={creation_code_end} runtime_code_embedded_at={embedded} eq_push2_jumpi={len(eq_push2_jumpi_sites(runtime))} creation_eq_push2_jumpi={len(eq_push2_jumpi_sites(creation))}')
    print(f'16ee4b79 full_runtime_offsets={runtime_sites} code_region_offsets={code_sites} decoded_code_PUSH4_nonselectors={nonselectors}')


def print_shape(label, path, is_vyper=False):
    _, data = data_bytes(path)
    end = len(data) if is_vyper else cbor_code_end(data)
    code = data[:end]
    ins = instructions(code)
    maps = {0x5f: 'PUSH0', 0x35: 'CALLDATALOAD', 0x60: 'PUSH1', 0x1c: 'SHR', 0x39: 'CODECOPY', 0x51: 'MLOAD', 0x56: 'JUMP', 0x06: 'MOD', 0x11: 'GT', 0x14: 'EQ', 0x18: 'XOR', 0x57: 'JUMPI'}
    occurrences = []
    for patt in ('5f3560e01c', '60003560e01c'):
        needle = bytes.fromhex(patt)
        locs = [i for i in range(len(code)) if code.startswith(needle, i)]
        if locs:
            occurrences.append(f'{patt}@{locs}')
    decoded = []
    for pc, op, imm in ins[:42]:
        name = maps.get(op, f'OP_{op:02x}')
        if 0x60 <= op <= 0x7f:
            name = f'PUSH{op - 0x5f}'
        elif 0x80 <= op <= 0x8f:
            name = f'DUP{op - 0x7f}'
        if imm:
            name += ':' + imm.hex()
        decoded.append(name)
    details = ''
    if is_vyper:
        mod_index = next(i for i, item in enumerate(ins) if item[1] == 0x06)
        bucket_count = int.from_bytes(ins[mod_index - 2][2], 'big')
        table_base = int.from_bytes(ins[mod_index + 3][2], 'big')
        table = [int.from_bytes(data[table_base + i:table_base + i + 2], 'big') for i in range(0, bucket_count * 2, 2)]
        dispatch_ins = instructions(data[:table_base])
        xor_sites = [(dispatch_ins[i][0], dispatch_ins[i][2].hex()) for i in range(len(dispatch_ins) - 4)
                     if dispatch_ins[i][1] == 0x63 and dispatch_ins[i + 1][1] == 0x81 and dispatch_ins[i + 2][1] == 0x18 and dispatch_ins[i + 3][1] == 0x61 and dispatch_ins[i + 4][1] == 0x57]
        details = f' table_base={hex(table_base)} buckets={bucket_count} table={[hex(x) for x in table]} sentinel_05e7={table.count(0x05e7)} XOR_chain_sites={len(xor_sites)}'
    print(f'SHAPE {label} | file={path} | prefix={code[:48].hex()} | prologue={";".join(occurrences)} | opcode_prefix={" ".join(decoded)}{details}')


def print_vyper_offsets(label, carrier_path, probe_path):
    _, data = data_bytes(carrier_path)
    ins = instructions(data)
    mod_index = next(i for i, item in enumerate(ins) if item[1] == 0x06)
    bucket_count = int.from_bytes(ins[mod_index - 2][2], 'big')
    table_base = int.from_bytes(ins[mod_index + 3][2], 'big')
    dispatch_ins = instructions(data[:table_base])
    sites = {dispatch_ins[i][2].hex(): dispatch_ins[i][0]
             for i in range(len(dispatch_ins) - 4)
             if dispatch_ins[i][1] == 0x63 and dispatch_ins[i + 1][1] == 0x81 and dispatch_ins[i + 2][1] == 0x18 and dispatch_ins[i + 3][1] == 0x61 and dispatch_ins[i + 4][1] == 0x57}
    obj, _, _, _, _, _, offsets = probe_data(probe_path)
    bytecode = bytes.fromhex(obj['normalized_result']['bytecode']['hex'])
    matched = [(selector, off, sites.get(selector)) for selector, off in offsets]
    relation = sum(pc is not None and off == pc + 11 for _, off, pc in matched)
    on_jumpdest = sum(off < len(bytecode) and bytecode[off] == 0x5b for _, off, _ in matched)
    before_push_jumpdest = sum(pc is not None and pc > 0 and bytecode[pc - 1] == 0x5b for _, _, pc in matched)
    print(f'VYPER OFFSETS {label} | buckets={bucket_count} probe_functions={len(offsets)} selector_push_pc_plus_11={relation}/{len(offsets)} bytecode_offset_is_JUMPDEST={on_jumpdest}/{len(offsets)} push4_preceded_by_JUMPDEST={before_push_jumpdest}/{len(offsets)}')


def print_creation_eq_histogram():
    base = Path('.ufo/waves/arc3-loop1-round3/claims/c1')
    groups = {}
    for path in sorted(base.rglob('*.creation.hex')):
        try:
            _, decoded = data_bytes(path)
        except (UnicodeDecodeError, ValueError):
            continue
        count = len(eq_push2_jumpi_sites(decoded))
        if count:
            groups.setdefault(count, []).append(str(path))
    print('R3 CREATION EQ;PUSH2;JUMPI histogram (all local *.creation.hex under round3):')
    for count in sorted(groups):
        print(f'{count}: {len(groups[count])} files: ' + ', '.join(groups[count]))


print(f'cwd={ROOT}')
print_sources()
print_carriers()
print_probes()
print_r1_erratum()
print_shape('r1 Rv2Token', '.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.bin')
print_shape('r3 VaultB opt200', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-10/out/VaultB.opt200.runtime.bin')
print_shape('r3 CarrierB EX04 opt200', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-04/evidence/carrierB.runtime-opt200.bin')
print_shape('r3 CarrierB EX05', '.ufo/waves/arc3-loop1-round3/claims/c1/EX-05/out/CarrierB.runtime.bin')
print_shape('r4 CarrierV', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin', True)
print_shape('r4 Ex09Vault', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.bin', True)
print_vyper_offsets('CarrierV', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/out/runtime.bin', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-04/evidence/probe/probe-6.4.0-hex.json')
print_vyper_offsets('Ex09Vault', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/carriers/Ex09Vault.runtime.bin', '.ufo/waves/arc3-loop1-round4/claims/c1/EX-09/probe/vy-runtime-hex-6.4.0.json')
print_creation_eq_histogram()
