"""Execute the instrument's unchanged --selftest with fixture git containment."""
import os
from pathlib import Path
import runpy
import subprocess
import sys

SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r82/MutationGates').resolve()
original_run = subprocess.run

def guarded_run(argv, *args, **kwargs):
    if isinstance(argv, list) and argv and argv[0] == 'git':
        argv = list(argv)
        if argv[1:2] != ['-C']:
            root = str(Path(kwargs['cwd']).resolve())
            argv[1:1] = ['-C', root]
        root = Path(argv[2]).resolve()
        if not root.is_relative_to(SCRATCH):
            raise RuntimeError('fixture git outside private scratch')
        if 'add' in argv or 'commit' in argv:
            top = original_run(['git', '-C', str(root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True, env=kwargs.get('env')).stdout.strip()
            if top != str(root):
                raise RuntimeError('fixture toplevel mismatch')
            print('FIXTURE_TOPLEVEL_OK before ' + ('commit' if 'commit' in argv else 'add'))
    return original_run(argv, *args, **kwargs)

subprocess.run = guarded_run
source = Path(sys.argv[1]).resolve()
if not source.is_relative_to(SCRATCH):
    raise RuntimeError('instrument outside private scratch')
if Path(os.environ['TMPDIR']).resolve() != SCRATCH / 'tmp':
    raise RuntimeError('TMPDIR not explicitly contained')
sys.argv = [str(source), '--selftest', '--work', str(SCRATCH)]
# C1 does not accept --work; its selftest performs no fixture writes.
if source.read_text().find('def conjunction(') != -1:
    sys.argv = [str(source), '--selftest']
runpy.run_path(str(source), run_name='__main__')
