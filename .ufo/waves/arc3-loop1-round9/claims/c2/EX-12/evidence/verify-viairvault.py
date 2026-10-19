import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'compiled-viairvault'
results = []

for version in ('0.8.36', '0.8.37'):
    directory = BASE / f'solc-{version}' / 'viair'
    receipt = json.loads((directory / 'compile-receipt.json').read_text())
    census = json.loads((directory / 'selector-census.json').read_text())
    suffix = version[-2:].zfill(3)
    envelope = json.loads((ROOT / f'probe-viairvault-{suffix}.json').read_text())
    data = envelope['data']
    normalized = data['normalized_result']
    functions = normalized['functions']
    expected = set(census['independentlyDerived'].values())
    observed = [item['selector'].removeprefix('0x') for item in functions]
    observedSet = set(observed)
    bytecode = normalized['bytecode']
    checks = {
        'envelope_ok': envelope.get('ok') is True,
        'provider_is_evmole_interface': data['provider']['id'] == 'evmole-interface',
        'provider_version_is_evmole_0_9_3': data['provider']['version'] == 'evmole@0.9.3',
        'decoded_sha256_matches_fresh_compile': bytecode['sha256'] == receipt['runtimeSha256'],
        'decoded_size_matches_fresh_compile': bytecode['bytes'] == receipt['runtimeBytes'],
        'function_count_matches_compiler_abi': len(functions) == receipt['abiFunctionCount'],
        'selector_set_matches_independent_keccak': observedSet == expected,
        'no_duplicate_reported_selectors': len(observed) == len(observedSet),
        'all_dispatch_abi': all(item['dispatch'] == 'abi' for item in functions),
        'confidence_inferred': data['confidence'] == 'inferred',
        'authority_shipped_artifact': data['authority'] == 'shipped-artifact',
        'no_runtime_execution': normalized['runtime_execution'] == 'not-performed',
        'discovery_completeness_stays_unknown': normalized['discovery_completeness'] == 'unknown',
        'terminal_compiler_metadata_matches': bytecode['metadata']['compiler_version']['value'] == version
    }
    results.append({
        'compiler': receipt['solcVersion'],
        'evidenceId': data['evidence_id'],
        'decodedBytecodeSha256': bytecode['sha256'],
        'decodedBytecodeBytes': bytecode['bytes'],
        'expectedSelectorCount': len(expected),
        'observedSelectorCount': len(observed),
        'selectors': sorted(observedSet),
        'missing': sorted(expected - observedSet),
        'extra': sorted(observedSet - expected),
        'discoveryCompleteness': normalized['discovery_completeness'],
        'runtimeExecution': normalized['runtime_execution'],
        'checks': checks,
        'pass': all(checks.values())
    })

report = {
    'reaCli': 'rea-agents@6.7.0',
    'provider': 'evmole@0.9.3',
    'sameSelectorSetAcrossVersions': results[0]['selectors'] == results[1]['selectors'],
    'results': results,
    'pass': all(item['pass'] for item in results)
}
(ROOT / 'probe-viairvault-verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if not report['pass']:
    raise SystemExit(1)
