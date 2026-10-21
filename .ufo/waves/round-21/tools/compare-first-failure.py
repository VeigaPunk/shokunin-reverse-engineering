#!/usr/bin/env python3
"""Compare kind/index only, requiring an explicit bounded extractor envelope.

0 match, 1 mismatch, 2 could-not-evaluate. Null means no qualifying failure
through last_line, never successful analysis. Extractor is caller-owned code,
not data or a sandbox; this tool never executes the analyzed carrier.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate_member: ' + key)
        result[key] = value
    return result


def decode(text):
    def constant(value):
        raise ValueError('nonfinite_number: ' + value)
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def validate_failure(value, where):
    if value is None:
        return
    if not isinstance(value, dict):
        raise ValueError(where + ': expected object or null')
    for field in ('kind', 'index', 'va', 'phase'):
        if field not in value:
            raise ValueError(where + ': missing_' + field)
    if not isinstance(value['kind'], str) or not value['kind']:
        raise ValueError(where + ': invalid_kind')
    for field in ('index', 'va'):
        item = value[field]
        if item is not None and type(item) is not int:
            raise ValueError(where + ': invalid_' + field)
    if not isinstance(value['phase'], str):
        raise ValueError(where + ': invalid_phase')


def evaluate(prediction, log, extractor):
    predicted = observed = None
    try:
        payload = decode(Path(prediction).read_text(encoding='utf-8'))
        if not isinstance(payload, dict) or not isinstance(payload.get('first_failure'), dict) or 'h1' not in payload['first_failure']:
            raise ValueError('prediction_missing_first_failure_h1')
        predicted = payload['first_failure']['h1']
        validate_failure(predicted, 'prediction')
        if not Path(log).is_file() or not Path(extractor).is_file():
            raise ValueError('input_missing')
        process = subprocess.run([sys.executable, '-I', '-B', str(extractor), str(log)], capture_output=True, text=True, timeout=120, check=False)
        if process.returncode != 0:
            raise ValueError('extractor_nonzero: ' + str(process.returncode))
        envelope = decode(process.stdout)
        if not isinstance(envelope, dict) or 'first_failure' not in envelope or 'last_line' not in envelope:
            raise ValueError('observation_envelope_required')
        bound = envelope['last_line']
        if type(bound) is not int or bound < 0:
            raise ValueError('invalid_last_line')
        observed = envelope['first_failure']
        validate_failure(observed, 'observation')
        match = (predicted is None and observed is None) if predicted is None or observed is None else (predicted['kind'], predicted['index']) == (observed['kind'], observed['index'])
        return {'finding': 'failure_match' if match else 'failure_mismatch', 'match': match, 'predicted': predicted, 'observed': observed, 'last_line': bound}, 0 if match else 1
    except (OSError, UnicodeError, ValueError, RecursionError, subprocess.SubprocessError) as error:
        return {'finding': 'comparison_unevaluable', 'match': None, 'predicted': predicted, 'observed': observed, 'error': str(error)}, 2


def selftest():
    failure = {'kind': 'eof', 'index': None, 'va': None, 'phase': 'analysis'}
    rows = [('bounded_null', None, {'first_failure': None, 'last_line': 0}, 0),
            ('nullable_eof', failure, {'first_failure': failure, 'last_line': 4}, 0),
            ('predicted_null', None, {'first_failure': failure, 'last_line': 4}, 1),
            ('observed_null', failure, {'first_failure': None, 'last_line': 4}, 1),
            ('kind_diff', failure, {'first_failure': dict(failure, kind='other'), 'last_line': 4}, 1),
            ('naked_null', None, None, 2),
            ('missing_bound', None, {'first_failure': None}, 2),
            ('boolean_bound', None, {'first_failure': None, 'last_line': True}, 2),
            ('missing_index', failure, {'first_failure': {'kind': 'eof', 'va': None, 'phase': 'analysis'}, 'last_line': 4}, 2)]
    results = []
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-compare-') as directory:
        root = Path(directory)
        stub = root / 'extractor.py'
        stub.write_text('import pathlib,sys\nprint(pathlib.Path(sys.argv[1]).read_text())\n', encoding='utf-8')
        for name, pred, obs, expected in rows:
            p, log = root/'prediction.json', root/'log.json'
            p.write_text(json.dumps({'first_failure': {'h1': pred}}), encoding='utf-8')
            log.write_text(json.dumps(obs), encoding='utf-8')
            proc = subprocess.run([sys.executable, '-I', '-B', __file__, '--prediction', str(p), '--log', str(log), '--extractor', str(stub)], capture_output=True, text=True, check=False)
            finding = json.loads(proc.stdout).get('finding')
            wanted = {0:'failure_match', 1:'failure_mismatch', 2:'comparison_unevaluable'}[expected]
            results.append({'id': name, 'exit': proc.returncode, 'finding': finding, 'ok': proc.returncode == expected and finding == wanted})
    print(json.dumps({'finding': 'selftest_clean' if all(r['ok'] for r in results) else 'selftest_failed', 'cases': results}, sort_keys=True))
    return 0 if all(r['ok'] for r in results) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prediction')
    parser.add_argument('--log')
    parser.add_argument('--extractor')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not all((args.prediction, args.log, args.extractor)):
        parser.error('--prediction, --log and --extractor required')
    result, code = evaluate(args.prediction, args.log, args.extractor)
    print(json.dumps(result, sort_keys=True))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
