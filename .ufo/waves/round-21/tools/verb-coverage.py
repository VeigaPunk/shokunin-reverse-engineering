#!/usr/bin/env python3
"""Bind exact Evidence id and operation in supported retained JSON records.

Not cryptographic authentication. Unsupported representations are unevaluable;
TOON substring co-occurrence is deliberately not a binding authority.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

REFUSALS = {'execution_failure', 'could_not_evaluate', 'invalid_request',
            'capability_unavailable', 'provider_timeout', 'unsupported_target',
            'VALIDATION_ERROR', 'failed', 'failure', 'error', 'refused',
            'provider_unavailable', 'unsupported_provider', 'invalid_input',
            'invalid_format', 'out_of_range'}
ID = re.compile(r'ev_[0-9a-fA-F]{64}\Z')


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


def refused(node):
    """Only structural error/status fields, never arbitrary quoted prose."""
    if not isinstance(node, dict):
        return False
    for key in ('error', 'errors'):
        if node.get(key):
            return True
    for key in ('code', 'status', 'completion_status'):
        value = node.get(key)
        if isinstance(value, str) and value in REFUSALS:
            return True
    if 'exit_code' in node and (type(node['exit_code']) is not int or node['exit_code'] != 0):
        return True
    for key in ('raw_result', 'normalized_result'):
        if refused(node.get(key)):
            return True
    return False


def records(node, inherited=False):
    """Supported carriers: record, list, evidence/records wrapper, result wrapper.

    Do not recursively discover putative records inside arbitrary metadata.
    An ancestor refusal applies to every record it encloses.
    """
    if isinstance(node, list):
        for item in node:
            yield from records(item, inherited)
    elif isinstance(node, dict):
        blocked = inherited or refused(node)
        if 'evidence_id' in node and 'operation' in node:
            yield node, blocked
        else:
            for key in ('evidence', 'evidences', 'records', 'result'):
                if key in node:
                    yield from records(node[key], blocked)


def bind(text, verb, evidence_id):
    try:
        if not ID.fullmatch(evidence_id):
            raise ValueError('invalid_evidence_id')
        payload = decode(text)
        entries = list(records(payload))
        if not entries:
            raise ValueError('unsupported_evidence_representation')
        operation = 'inspect_with_objdump' if verb == 'list-objdump-architectures' else verb.replace('-', '_')
        matching = []
        for record, blocked in entries:
            if record.get('evidence_id') != evidence_id or record.get('operation') != operation:
                continue
            if verb == 'list-objdump-architectures':
                params = record.get('parameters')
                if not isinstance(params, dict) or params.get('operation') != 'architectures':
                    continue
            matching.append((record, blocked))
        if not matching:
            return {'finding': 'evidence_unbound', 'bound': False}, 1
        if any(blocked for _, blocked in matching):
            return {'finding': 'evidence_refused', 'bound': False}, 1
        return {'finding': 'evidence_bound', 'bound': True, 'pathless': any(record.get('subject', 'absent') is None for record, _ in matching)}, 0
    except (UnicodeError, ValueError, RecursionError) as error:
        return {'finding': 'evidence_unevaluable', 'bound': None, 'error': str(error)}, 2


def legacy_helpers(root):
    path = Path(root) / '.ufo/waves/round-20/tools/verb-coverage.py'
    spec = importlib.util.spec_from_file_location('kaidoku_r20_mention_helpers', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(root, revision):
    old = legacy_helpers(root)
    try:
        return _measure(old, root, revision)
    except old.Refusal as error:
        raise ValueError(str(error)) from error


def _measure(old, root, revision):
    revision = old.resolve_revision(root, revision)
    tree = old.tree_entries(root, revision)
    paths = [path for path, _ in tree]
    # Fixed retained 6.5.0 catalog, not mutable installed JavaScript execution.
    catalog = decode(old.git_show(root, revision, '.ufo/waves/round-20/verify/round20/verb-coverage.json'))['cli_commands']
    if not isinstance(catalog, list) or len(catalog) != len(set(catalog)) or any(not isinstance(x, str) for x in catalog):
        raise ValueError('invalid_retained_catalog')
    texts = [old.git_show(root, revision, path) for path in paths if path.startswith(old.KNOWLEDGE_PREFIX)]
    per = {verb: sum(bool(old.command_pattern(verb).search(text)) for text in texts) for verb in catalog}
    targets = {}
    for verb in old.DEFAULT_TARGETS:
        relevant = [text for text in texts if old.command_pattern(verb).search(text)]
        witnesses, unevaluable = [], []
        for text in relevant:
            cited = old.cited_prefixes(text)
            ids = sorted(set(m.group(0) for m in old.HEX64.finditer(text)))
            for path in paths:
                if not path.startswith(old.EVIDENCE_PREFIX) or not old.is_cited(path, cited):
                    continue
                blob = old.git_show(root, revision, path)
                # Only candidate files carrying a cited ID need decoding.
                for ev in ids:
                    if ev not in blob:
                        continue
                    result, code = bind(blob, verb, ev)
                    if code == 0:
                        witnesses.append([ev, path])
                    elif code == 2:
                        unevaluable.append(path)
        targets[verb] = {'entries':len(relevant), 'exercised':bool(witnesses), 'bound_evidence':witnesses[:5], 'unsupported_candidates':sorted(set(unevaluable))}
    return {'rev':revision, 'package_version':'6.5.0', 'cli_commands':catalog, 'mentioned':[v for v in catalog if per[v]], 'zero':[v for v in catalog if not per[v]], 'per_command':per, 'targets':targets, 'limit':'local record binding only; no cryptographic authentication; unsupported candidates do not count'}


def selftest():
    ev = 'ev_' + 'a'*64
    valid = {'evidence_id':ev, 'operation':'inspect_wasm_artifact'}
    rows = [('positive', valid, 0, 'evidence_bound'),
            ('wrapper', {'result':{'evidence':valid}}, 0, 'evidence_bound'),
            ('notes', dict(valid, operation='inspect_artifact', notes='inspect_wasm_artifact'), 1, 'evidence_unbound'),
            ('refusal', dict(valid, error={'code':'execution_failure'}), 1, 'evidence_refused'),
            ('outer_refusal', {'error':{'code':'could_not_evaluate'}, 'result':{'evidence':valid}}, 1, 'evidence_refused'),
            ('split', [dict(valid, operation='inspect_artifact'), dict(valid, evidence_id='ev_'+'b'*64)], 1, 'evidence_unbound')]
    results=[]
    with tempfile.TemporaryDirectory(prefix='kaidoku-r21-bind-') as directory:
        path = Path(directory)/'evidence.json'
        for name, record, expected, finding in rows:
            path.write_text(json.dumps(record), encoding='utf-8')
            proc=subprocess.run([sys.executable,'-I','-B',__file__,'--evidence',str(path),'--verb','inspect-wasm-artifact','--evidence-id',ev], capture_output=True,text=True,check=False)
            actual=json.loads(proc.stdout).get('finding')
            results.append({'id':name,'exit':proc.returncode,'finding':actual,'ok':proc.returncode==expected and actual==finding})
    print(json.dumps({'finding':'selftest_clean' if all(r['ok'] for r in results) else 'selftest_failed','cases':results},sort_keys=True))
    return 0 if all(r['ok'] for r in results) else 1


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root')
    parser.add_argument('--rev')
    parser.add_argument('--evidence')
    parser.add_argument('--verb')
    parser.add_argument('--evidence-id')
    parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        if args.evidence:
            if not args.verb or not args.evidence_id:
                parser.error('--verb and --evidence-id required')
            result,code=bind(Path(args.evidence).read_text(encoding='utf-8'),args.verb,args.evidence_id)
        elif args.root and args.rev:
            result,code=measure(args.root,args.rev),0
        else:
            parser.error('use --evidence or --root and --rev')
        print(json.dumps(result,sort_keys=True))
        return code
    except (OSError,UnicodeError,ValueError,RecursionError) as error:
        print(json.dumps({'finding':'evidence_unevaluable','error':str(error)}))
        return 2


if __name__=='__main__':
    raise SystemExit(main())
