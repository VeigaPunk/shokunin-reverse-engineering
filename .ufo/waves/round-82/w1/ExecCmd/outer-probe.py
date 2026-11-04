#!/usr/bin/env python3
"""Isolated outer CLI green/red fixtures; no lane mutations."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-82/w1/ExecCmd'
WORK = Path('/fast/scratch/hyaku/kaidoku-r82/ExecCmd')
REV = 'eb227c4694e16cb8fae74df0eea2f07643b46124'
SCRIPT = 'tools/round-82/printed-command.py'


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def assert_top(root):
    assert root.is_absolute() and root.is_relative_to(WORK)
    assert git(root, 'rev-parse', '--show-toplevel').decode().strip() == str(root)


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


assert os.environ.get('TMPDIR') == str(WORK / 'tmp')
(WORK / 'tmp').mkdir(parents=True)
fixture = WORK / 'outer-fixture'
fixture.mkdir()
try:
    subprocess.run(['git', '-C', str(fixture), 'init', '-q'], check=True)
    assert_top(fixture)
    git(fixture, 'fetch', '--quiet', '--no-tags', str(ROOT), REV)
    paths = [SCRIPT, 'tools/round-82/conjunction-gate.py',
             'tools/round-81/record-integration.py', 'tools/round-80/pointer-bind.py',
             'tools/round-76/plan-command.py', 'plans/round-82-claims.md',
             '.ufo/waves/round-82/claims.json', '.ufo/waves/round-82/pre/fixtures',
             'corpus/SOURCES.md', 'corpus/knowledge/2026-11-04-r82-conjunction-and-printed-commands.md',
             '.ufo/waves/round-81/l1/scores/c2-at-landing.json',
             '.ufo/waves/round-81/w1/ExecCounter/undersized-pristine.json',
             '.ufo/waves/round-81/w1/ExecCounter/dirty-pristine-summary.json']
    assert_top(fixture)
    git(fixture, 'checkout', REV, '--', *paths)
    original = (fixture / SCRIPT).read_text()
    # Reuse retained minimal actual-path repair by applying its literal hunk.
    patch = subprocess.run(['patch', '--batch', '--forward', '-p1', '-i', str(OUT / 'actual-argv-pin.patch')], cwd=fixture, text=True, capture_output=True, check=True)
    candidate = (fixture / SCRIPT).read_text().replace(
        '["git", "init", "-q"], cwd=scratch, env=env,',
        '["git", "-C", scratch, "init", "-q"], env=env,')
    candidate = candidate.replace(
        '        check("fixture-repo-top", toplevel == os.path.realpath(scratch))',
        '        if toplevel != os.path.realpath(scratch):\n            raise RuntimeError("fixture root mismatch")\n        check("fixture-repo-top", True)')
    (fixture / SCRIPT).write_text(candidate)
    (OUT / 'candidate-printed-command.py').write_text(candidate)
    (OUT / 'actual-argv-pin-with-fixture-guard.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True), candidate.splitlines(True), fromfile='a/' + SCRIPT, tofile='b/' + SCRIPT)))
    claims_path = fixture / '.ufo/waves/round-82/claims.json'
    claims = json.loads(claims_path.read_text())
    claims['instruments'][SCRIPT] = hashlib.sha256(candidate.encode()).hexdigest()
    claims_path.write_text(json.dumps(claims, indent=1) + '\n')
    # Preserve source history for BASE lookups, but commit only explicit fixture paths.
    assert_top(fixture)
    git(fixture, 'update-ref', 'HEAD', REV)
    assert_top(fixture)
    git(fixture, 'add', SCRIPT, '.ufo/waves/round-82/claims.json')
    assert_top(fixture)
    git(fixture, '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'candidate actual-path pin fixture')
    fixture_rev = git(fixture, 'rev-parse', 'HEAD').decode().strip()
    argv = [sys.executable, '-I', '-B', SCRIPT, '--battery', '--root', str(fixture), '--rev', fixture_rev, '--work', str(WORK / 'green'), '--json-out', str(OUT / 'outer-green.json')]
    green = subprocess.run(argv, cwd=fixture, text=True, capture_output=True, timeout=90)
    green_receipt = json.loads((OUT / 'outer-green.json').read_text())
    save('outer-green-execution.json', {'base_revision': REV, 'candidate_revision': fixture_rev, 'argv': argv, 'rc': green.returncode, 'stdout': green.stdout, 'stderr': green.stderr, 'finding_id': 'C2_ALL_ARMS_MET', 'assertion': green.returncode == 0 and green_receipt['arms_ok'] == 6 and green_receipt['arms_total'] == 6 and green_receipt['validate']['defects'] == []})
    # Dirty the actual C1 argv path without changing its pinned revision blob.
    target = fixture / 'tools/round-82/conjunction-gate.py'
    target.write_bytes(target.read_bytes() + b'\n# actual worktree mismatch\n')
    red_argv = [sys.executable, '-I', '-B', SCRIPT, '--run', '--plan', 'plans/round-82-claims.md', '--block', 'C1', '--root', str(fixture), '--rev', fixture_rev, '--work', str(WORK / 'red'), '--json-out', str(OUT / 'outer-red.json')]
    red = subprocess.run(red_argv, cwd=fixture, text=True, capture_output=True, timeout=90)
    red_receipt = json.loads((OUT / 'outer-red.json').read_text())
    defects = red_receipt['row']['defects']
    save('outer-red-execution.json', {'base_revision': REV, 'candidate_revision': fixture_rev, 'argv': red_argv, 'rc': red.returncode, 'stdout': red.stdout, 'stderr': red.stderr, 'finding_id': 'SCRIPT_PIN_MISMATCH', 'assertion': red.returncode == 1 and not red_receipt['row']['executed'] and any('SCRIPT_PIN_MISMATCH:' in d and 'executed path differs' in d for d in defects)})
finally:
    shutil.rmtree(WORK)
    save('outer-cleanup.json', {'removed': not WORK.exists(), 'scratch': str(WORK)})
