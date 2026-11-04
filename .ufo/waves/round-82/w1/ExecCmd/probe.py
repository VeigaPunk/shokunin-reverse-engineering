#!/usr/bin/env python3
"""Bounded R82 evidence; only private fixture mutations, with retained receipts."""
import contextlib
import difflib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-82/w1/ExecCmd'
WORK = Path('/fast/scratch/hyaku/kaidoku-r82/ExecCmd')
REV = '2d63e1a7d04d4dcff45c3908bb51be787a2f22e1'
SCRIPT = 'tools/round-82/printed-command.py'
REAL_RUN = subprocess.run


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def git(*args, cwd=ROOT):
    return subprocess.check_output(['git', '-C', str(cwd), *args])


def load(data, filename):
    namespace = {'__file__': str(filename), '__name__': 'bounded_probe_module'}
    exec(compile(data, str(filename), 'exec'), namespace)
    return namespace


def guarded_run(argv, *args, **kwargs):
    # The frozen selftest uses git init without -C. Normalize that one call;
    # require and assert an absolute private fixture root before add/commit.
    if argv[:2] == ['git', 'init']:
        cwd = Path(kwargs['cwd']).resolve()
        assert cwd.is_relative_to(WORK)
        argv = ['git', '-C', str(cwd), *argv[1:]]
    if argv and argv[0] == 'git' and any(x in argv for x in ('add', 'commit')):
        assert argv[1] == '-C'
        cwd = Path(argv[2]).resolve()
        assert cwd.is_relative_to(WORK)
        assert git('rev-parse', '--show-toplevel', cwd=cwd).decode().strip() == str(cwd)
    if len(argv) > 4 and argv[1:3] == ['-I', '-B'] and argv[3] == SCRIPT and '--selftest' in argv:
        argv = [argv[0], '-I', '-B', str(Path(__file__).resolve()), '--guarded-selftest', *argv[4:]]
    return REAL_RUN(argv, *args, **kwargs)


if '--guarded-selftest' in sys.argv:
    subprocess.run = guarded_run
    module = load(git('show', f'{REV}:{SCRIPT}'), ROOT / SCRIPT)
    sys.exit(module['selftest'](str(ROOT), REV, sys.argv[sys.argv.index('--json-out') + 1]))

assert os.environ.get('TMPDIR') == str(WORK / 'tmp')
WORK.mkdir(parents=True, exist_ok=True)
(WORK / 'tmp').mkdir(exist_ok=True)
try:
    frozen = git('show', f'{REV}:{SCRIPT}')
    actual = (ROOT / SCRIPT).read_bytes()
    save('byte-audit.json', {'rev': REV, 'frozen_sha256': digest(frozen),
         'worktree_sha256': digest(actual), 'equal': frozen == actual,
         'frozen_blob': git('rev-parse', f'{REV}:{SCRIPT}').decode().strip(),
         'worktree_blob': git('hash-object', str(ROOT / SCRIPT)).decode().strip(),
         'lsp': 'No LSP tool exposed in this seat; definitions read directly.'})
    module = load(frozen, ROOT / SCRIPT)
    subprocess.run = guarded_run
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        rc = module['battery'](str(ROOT), REV, str(WORK / 'battery'), str(OUT / 'battery.json'))
    (OUT / 'battery.stdout.txt').write_text(stdout.getvalue())
    (OUT / 'battery.stderr.txt').write_text(stderr.getvalue())
    save('battery-invocation.json', {'rc': rc, 'rev': REV,
         'execution': 'frozen battery() loaded from git blob; guarded selftest child dispatch, NOT exact printed CLI',
         'guard': 'git init normalized to git -C absolute; assert private toplevel before add/commit',
         'worktree_sha256_after': digest((ROOT / SCRIPT).read_bytes())})
    subprocess.run = REAL_RUN

    fixture = WORK / 'fixture'
    fixture.mkdir()
    REAL_RUN(['git', '-C', str(fixture), 'init', '-q'], check=True)
    assert git('rev-parse', '--show-toplevel', cwd=fixture).decode().strip() == str(fixture)
    member = fixture / 'member.py'
    clean = b"import json,sys\nfrom pathlib import Path\nPath(sys.argv[1]).write_text(json.dumps({'cases': 1, 'origin': 'pinned'}))\n"
    dirty = clean.replace(b"'pinned'", b"'WORKTREE_DIVERGENCE'")
    member.write_bytes(clean)
    REAL_RUN(['git', '-C', str(fixture), 'add', 'member.py'], check=True)
    assert git('rev-parse', '--show-toplevel', cwd=fixture).decode().strip() == str(fixture)
    REAL_RUN(['git', '-C', str(fixture), '-c', 'user.name=fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'bounded pinned fixture'], check=True)
    fixture_rev = git('rev-parse', 'HEAD', cwd=fixture).decode().strip()
    pins = {'member.py': digest(clean)}
    command = 'python3 -I -B member.py $OUT'
    baseline = module['run_block'](str(fixture), fixture_rev, command, str(WORK / 'clean'), str(WORK / 'clean/out.json'), 'cases', pins)
    member.write_bytes(dirty)
    attacked = module['run_block'](str(fixture), fixture_rev, command, str(WORK / 'dirty'), str(WORK / 'dirty/out.json'), 'cases', pins)
    save('divergence.json', {'frozen_blob_sha256': digest(git('show', f'{fixture_rev}:member.py', cwd=fixture)),
         'worktree_sha256': digest(dirty), 'baseline': baseline, 'dirty': attacked,
         'baseline_receipt': json.loads((WORK / 'clean/out.json').read_text()),
         'dirty_receipt': json.loads((WORK / 'dirty/out.json').read_text())})

    before = frozen.decode()
    after = before.replace('''    if sha256_bytes(data) != digest:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} bytes differ from the pin")
''', '''    if sha256_bytes(data) != digest:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} bytes differ from the pin")
    path = Path(root) / script
    if path.resolve() != Path(os.path.abspath(path)):
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} resolves through a symlink")
    try:
        actual = path.read_bytes()
    except OSError as exc:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} unreadable: {exc}") from exc
    if sha256_bytes(actual) != digest:
        raise Refused(f"SCRIPT_PIN_MISMATCH: {script} executed path differs from the pin")
''')
    assert before != after
    (OUT / 'actual-argv-pin.patch').write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='a/' + SCRIPT, tofile='b/' + SCRIPT)))
    patched = load(after.encode(), ROOT / SCRIPT)
    refused = patched['run_block'](str(fixture), fixture_rev, command, str(WORK / 'candidate'), str(WORK / 'candidate/out.json'), 'cases', pins)
    save('candidate-divergence.json', refused)
    save('tooling.json', {'installs': [], 'python': sys.version.split()[0], 'git': git('--version').decode().strip(), 'channel': 'pre-existing host tools', 'reason': 'assigned bounded C2 and divergence demonstrations'})
finally:
    subprocess.run = REAL_RUN
    shutil.rmtree(WORK)
    save('cleanup.json', {'scratch': str(WORK), 'removed': not WORK.exists()})
