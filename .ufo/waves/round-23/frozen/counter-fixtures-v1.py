#!/usr/bin/env python3
"""Independent synthetic fixtures: no validator fixture builder or decision import.

All Git writes are confined to disposable clones under the lane runtime root.
Synthetic minimal envelopes are control inputs, never producer Evidence claims.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PREFIX = '.ufo/waves/round-23/evidence/c1/'
ENTRY = 'corpus/knowledge/control-r23-synthetic.md'


def run(root, counter, manifest):
    results = []
    runtime = root / '.ufo/waves/round-23/runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    fixture = json.loads((root/'.ufo/waves/round-23/frozen/fixture.json').read_text())
    def command(argv, cwd):
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, check=False)
        if p.returncode:
            raise RuntimeError(p.stderr)
        return p.stdout
    with tempfile.TemporaryDirectory(prefix='fixture-', dir=runtime) as directory:
        repo = Path(directory)/'repo'
        command(['git', 'clone', '--shared', '--no-checkout', str(root), str(repo)], root)
        command(['git', 'checkout', fixture['base']], repo)
        for name, expected in manifest['cases'].items():
            # Reset only this disposable clone, never the lane checkout/index.
            command(['git', 'reset', '--hard', fixture['base']], repo)
            command(['git', 'clean', '-fd'], repo)
            documents = copy.deepcopy(fixture['documents'])
            selected = ['inspect-signal-decoders']
            if name == 'all_six':
                selected = list(documents)
            if name == 'same_verb':
                selected = ['identify-flutter-build']
            if name == 'mention_only':
                selected = []
            evidence = repo / PREFIX
            evidence.mkdir(parents=True, exist_ok=True)
            text = 'source: S058 synthetic isolated control\nverified-at: fixture\nrecheck: selftest\n\n'
            for verb in selected:
                envelope = documents[verb]
                if name == 'refused_parent':
                    envelope['ok'] = False
                elif name == 'nested_refusal':
                    envelope['data']['normalized_result'] = {'errors': ['execution_failure']}
                elif name == 'wrong_command':
                    envelope['meta']['command'] = 'identify-flutter-build'
                elif name == 'wrong_operation':
                    envelope['data']['operation'] = 'identify_flutter_build'
                eid = envelope['data']['evidence_id']
                path = PREFIX+verb+'.json'
                raw = json.dumps(envelope)
                if name == 'duplicate_member':
                    raw = raw.replace('"ok": true', '"ok": false, "ok": true')
                (repo/path).write_text(raw+'\n')
                text += verb+' '+eid+' '+path+'\n'
            if name == 'mention_only':
                text += 'inspect-signal-decoders ev_'+'a'*64+'\n'
            if name == 'missing_source':
                text = text.replace('source: S058 synthetic isolated control', 'source: none')
            if name == 'old_source':
                text = text.replace('source: S058', 'source: S051')
            (repo/ENTRY).write_text(text)
            source = repo/'corpus/SOURCES.md'
            body = source.read_text()
            usedby = 'corpus/knowledge/not-this-entry.md' if name == 'wrong_usedby' else ENTRY
            row = '| S058 | isolated control | own-work | A | synthetic control only | fixture | control, not real Evidence | mined | 2026-10-21 | on-release | '+usedby+' |\n'
            body = body.replace('\n## Paths', '\n'+row+'\n## Paths', 1)
            if name == 'old_source':
                body = '\n'.join(line.rstrip().rstrip('|')+', '+ENTRY+' |' if line.startswith('| S051 |') else line for line in body.splitlines())+'\n'
            source.write_text(body)
            if name == 'helper_tamper':
                p = repo/'.ufo/waves/round-22/tools/count-c1.py'
                p.write_text(p.read_text()+'\n# changed control\n')
            if name == 'invalid_utf8':
                (evidence/'inspect-signal-decoders.json').write_bytes(b'\xff')
            command(['git', 'add', '--', ENTRY, 'corpus/SOURCES.md', PREFIX, '.ufo/waves/round-22/tools/count-c1.py'], repo)
            command(['git', '-c', 'user.name=isolated-fixture', '-c', 'user.email=fixture@invalid', 'commit', '-m', 'synthetic counter control'], repo)
            revision = command(['git', 'rev-parse', 'HEAD'], repo).strip()
            argv = [sys.executable, '-I', '-B', str(counter), '--root', str(repo), '--rev', revision]
            p = subprocess.run(argv, capture_output=True, text=True, check=False)
            try:
                out = json.loads(p.stdout)
            except ValueError:
                out = {}
            observed = {'exit': p.returncode, 'count': out.get('t1_exercised_count'), 'finding': out.get('finding')}
            passed = all(observed.get(key) == value for key, value in expected.items())
            results.append({'case': name, 'expected': expected, 'observed': observed, 'passed': passed,
                            'argv': argv, 'stdout': p.stdout, 'stderr': p.stderr})
    return {'finding': 'selftest_clean' if all(x['passed'] for x in results) else 'selftest_failed',
            'passed': sum(x['passed'] for x in results), 'total': len(results), 'cases': results}, 0 if all(x['passed'] for x in results) else 1
