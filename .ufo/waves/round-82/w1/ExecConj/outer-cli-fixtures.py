#!/usr/bin/env python3
"""Bounded outer-CLI fixtures; writes only this seat's scratch/evidence."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
REV = 'eb227c4694e16cb8fae74df0eea2f07643b46124'
WORK = Path('/fast/scratch/hyaku/kaidoku-r82/ExecConj')
OUT = ROOT / '.ufo/waves/round-82/w1/ExecConj'
LANDING = '.ufo/waves/round-81/l1/scores/c2-at-landing.json'
GATE = 'tools/round-82/conjunction-gate.py'
PATHS = [GATE, 'tools/round-81/record-integration.py', 'tools/round-80/pointer-bind.py', LANDING, '.ufo/waves/round-81/w1/ExecCounter/undersized-pristine.json', '.ufo/waves/round-81/w1/ExecCounter/dirty-pristine-summary.json']

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / 'tmp').mkdir(exist_ok=True)
    env = os.environ.copy()
    env['TMPDIR'] = str(WORK / 'tmp')
    fixture = WORK / 'fixture'
    fixture.mkdir()
    def git(*args):
        return subprocess.check_output(['git', '-C', str(fixture), *args], env=env, stderr=subprocess.PIPE).decode().strip()
    results = []
    try:
        git('init', '-q')
        assert Path(git('rev-parse', '--show-toplevel')) == fixture
        for path in PATHS:
            data = subprocess.check_output(['git', '--no-optional-locks', '-C', str(ROOT), 'show', f'{REV}:{path}'])
            dest = fixture / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        original = json.loads((fixture / LANDING).read_text())
        cases = [('green-baseline', None, None, 0), ('red-binder', 'binder_sha256', '0' * 64, 1), ('summary-below-floor', 'summary', [1, 0], 1), ('summary-bool-population', 'summary', [True, 0], 1), ('summary-bool-failures', 'summary', [11, False], 1)]
        for name, field, value, expected in cases:
            record = json.loads(json.dumps(original))
            if field == 'binder_sha256':
                record[field] = value
            elif field:
                record['pristine'][field] = value
            (fixture / LANDING).write_text(json.dumps(record) + '\n')
            assert Path(git('rev-parse', '--show-toplevel')) == fixture
            git('add', '--force', '--', *PATHS)
            assert Path(git('rev-parse', '--show-toplevel')) == fixture
            git('-c', 'user.name=ExecConj Fixture', '-c', 'user.email=execconj@invalid', '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-qm', name)
            revision = git('rev-parse', 'HEAD')
            output = OUT / ('outer-' + name + '.json')
            argv = ['python3', '-I', '-B', str(fixture / GATE), '--battery', '--root', str(fixture), '--rev', revision, '--json-out', str(output)]
            p = subprocess.run(argv, cwd=WORK, env=env, capture_output=True, text=True, timeout=30)
            (OUT / ('outer-' + name + '.stdout.txt')).write_text(p.stdout)
            (OUT / ('outer-' + name + '.stderr.txt')).write_text(p.stderr)
            results.append({'case': name, 'source_revision': REV, 'fixture_revision': revision, 'argv': argv, 'expected_exit': expected, 'actual_exit': p.returncode, 'expectation_met': p.returncode == expected, 'finding_id': None if p.returncode == expected else 'R82-C1-SUMMARY-DOMAIN-001', 'gate_sha256': hashlib.sha256((fixture / GATE).read_bytes()).hexdigest()})
    finally:
        shutil.rmtree(WORK)
        (OUT / 'outer-cli-evidence.json').write_text(json.dumps({'results': results, 'scratch_removed': not WORK.exists()}, indent=2) + '\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
