"""Bounded synthetic counterexamples; never runs the lane battery."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import types

LANE = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
EVIDENCE = LANE / '.ufo/waves/round-82/w1/ReviewerC2'
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r82/ReviewerC2')
REV = '2d63e1a7d04d4dcff45c3908bb51be787a2f22e1'
SCRIPT = 'tools/round-82/printed-command.py'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    SCRATCH.mkdir(parents=True, exist_ok=False)
    os.environ['TMPDIR'] = str(SCRATCH)
    source = subprocess.check_output(['git', '-C', str(LANE), 'show', f'{REV}:{SCRIPT}'])
    m = types.ModuleType('frozen_printed_command')
    m.__file__ = str(LANE / SCRIPT)
    exec(compile(source, f'{REV}:{SCRIPT}', 'exec'), m.__dict__)
    result = {'axes': ['execution-byte identity', 'exact sourced-row binding', 'containment', 'runtime pin refusal'],
              'revision': REV, 'instrument_sha256': digest(source), 'cases': {}}
    try:
        repo = SCRATCH / 'fixture'
        repo.mkdir()
        subprocess.run(['git', '-C', str(repo), 'init', '-q'], check=True, capture_output=True)
        def git(*args):
            top = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', '--show-toplevel'], text=True).strip()
            assert top == str(repo), top
            return subprocess.check_output(['git', '-C', str(repo), *args])
        member = 'tools/round-82/conjunction-gate.py'
        target = repo / member
        target.parent.mkdir(parents=True)
        good = b"import json,sys\nfrom pathlib import Path\np=Path(sys.argv[sys.argv.index('--json-out')+1])\np.write_text(json.dumps({'refused':3,'origin':'pinned'}))\n"
        target.write_bytes(good)
        git('add', member)
        git('-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'pinned fixture')
        fixture_rev = git('rev-parse', 'HEAD').decode().strip()
        pins = {member: digest(good)}
        work = SCRATCH / 'work'
        work.mkdir()
        out = work / 'out.json'
        cmd = f'python3 -I -B {member} --json-out $OUT'
        bad = good.replace(b"'origin':'pinned'", b"'origin':'uncommitted-worktree'")
        target.write_bytes(bad)
        row = m.run_block(str(repo), fixture_rev, cmd, str(work), str(out), 'refused', pins)
        result['cases']['wrong_worktree_bytes'] = {'row': row, 'receipt': json.loads(out.read_text()),
            'pinned_sha256': digest(good), 'executed_worktree_sha256': digest(bad), 'fixture_rev': fixture_rev}
        mismatch = m.run_block(str(repo), fixture_rev, cmd, str(work), str(out), 'refused', {member:'0'*64})
        result['cases']['revision_pin_mismatch'] = mismatch
        result['cases']['unpinned_script'] = m.run_block(str(repo), fixture_rev,
            'python3 -I -B tools/round-82/not-pinned.py --json-out $OUT', str(work), str(out), 'refused', pins)
        target.write_bytes(good)
        outside = SCRATCH / 'outside-work.json'
        # The API's out is contained, but the printed argv uses a literal outside path.
        literal = f'python3 -I -B {member} --json-out {outside}'
        row = m.run_block(str(repo), fixture_rev, literal, str(work), str(out), 'refused', pins)
        result['cases']['literal_output_escape'] = {'row':row, 'outside_created':outside.exists(),
            'outside_receipt':json.loads(outside.read_text()), 'stale_contained_receipt':json.loads(out.read_text())}
        result['cases']['explicit_output_escape_refused'] = m.run_block(str(repo), fixture_rev,
            cmd, str(work), str(outside), 'refused', pins)
        link = work / 'link.json'
        link.symlink_to(outside)
        result['cases']['symlink_output_escape_refused'] = m.run_block(str(repo), fixture_rev,
            cmd, str(work), str(link), 'refused', pins)
        # Synthetic read_text only; production parser/arm is unchanged.
        read_original = m.read_text
        valid_row = '| S299 | docs | docs | A | scope | anchor | teaches | mined | 2026-11-04 | on-release | entry |'
        def sourced(row_text, entry, plan='S299'):
            def read(root, rev, path):
                if path == m.SOURCES:
                    return '' if rev == m.BASE else row_text
                if path == m.PLAN:
                    return plan
                if path == m.ENTRY:
                    return entry
                raise AssertionError(path)
            m.read_text = read
            try:
                return m.sourced_arm('synthetic', 'synthetic-revision')
            finally:
                m.read_text = read_original
        result['cases']['source_S2990'] = sourced(valid_row, 'source: S2990 — unrelated row')
        queued = valid_row.replace('| teaches | mined |', '| mined discussion only | queued |')
        result['cases']['mined_arbitrary_cell'] = {'input_row':queued, 'arm':sourced(queued, 'source: S299')}
        result['cases']['plan_S2990'] = sourced(valid_row, 'source: S299', plan='S2990')
        result['cases']['different_source_control'] = sourced(valid_row, 'source: S260')
        result['tool_versions'] = {'python':sys.version.split()[0], 'git':subprocess.check_output(['git','--version'],text=True).strip(), 'installs':[]}
        (EVIDENCE / 'counterexamples.json').write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps(result, indent=2))
    finally:
        shutil.rmtree(SCRATCH)
        print('scratch_removed=' + str(not SCRATCH.exists()))

main()
