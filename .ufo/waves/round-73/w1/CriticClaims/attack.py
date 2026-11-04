"""Scoped critic experiments; prints key names/booleans, never environment values."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
import types

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
S = Path(os.environ['TMPDIR'])
BASE = '05bf065684e52d72ea25aad95f7acb71fcd7874c'

DECLARATION = 'da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b'

def frozen(path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show',
                                    DECLARATION + ':' + str(path.relative_to(ROOT))]).decode()

def load(name, path):
    mod = types.ModuleType(name)
    mod.__file__ = str(path)
    exec(compile(frozen(path), str(path), 'exec'), mod.__dict__)
    return mod

probe = load('critic_probe', ROOT / 'tools/round-73/seam-probe.py')
audit = load('critic_audit', ROOT / 'tools/round-73/record-audit.py')
allow = ['HOME', 'LANG', 'PATH', 'TMPDIR']
shim = S / 'shims'
shim.mkdir(exist_ok=True)
clean = {'HOME': str(S), 'LANG': 'C', 'PATH': '/usr/bin', 'TMPDIR': str(S)}
dirty = {**clean, 'KAIDOKU_ENV_CANARY': 'critic-local-canary'}
# Clean decoys advertise the watched argv identity; dirty real work does not.
processes = [subprocess.Popen([sys.executable, '-I', '-B', '-c',
             'import time; time.sleep(0.5)', str(shim / name)], env=clean)
             for name in ('git', 'readelf')]
real = subprocess.Popen(['/usr/bin/perl', '-e', 'select(undef,undef,undef,0.5);'], env=dirty)
try:
    actual = probe._proc_environ(real.pid)
    deadline = time.monotonic() + 0.3
    while 'KAIDOKU_ENV_CANARY' not in (actual or {}) and time.monotonic() < deadline:
        time.sleep(0.001)
        actual = probe._proc_environ(real.pid)
    samples = probe.kernel_witness(str(shim), threading.Event(), timeout=0.25)
finally:
    for process in [*processes, real]:
        process.wait(timeout=5)
named = probe._name_samples(samples, str(shim))
forged = {'kernel': named, 'shims': {name: {'keys': allow, 'canary_present': False}
                                  for name in ('git', 'readelf')}}
verdict = probe.a12_verdict({'rc': 0, 'kernel': named}, forged, allow)
c1 = {'attack': 'argv identity substitution with clean decoys and dirty unnamed real process',
      'real_keys': sorted(actual), 'real_canary_present': 'KAIDOKU_ENV_CANARY' in actual,
      'watched_samples': {name: {'keys': row['keys'], 'canary_present': row['canary_present']}
                          for name, row in named.items()}, 'verdict': verdict,
      'interpretation': 'observer blind to dirty real process; verdict fails closed, not a false green'}

# Prose-only D1 change: the correction repeats the WRONG hash but supplies no right hash.
original_show = audit.show
score = original_show(str(ROOT), BASE, audit.SCORECARD)
before = audit.atom_c2_evidence_hash(str(ROOT), BASE)
wrong = before['evidence']['wrong_tokens']
heading = audit.ROUND72_HEADING
marker = '\n' + audit.CORRECTION_MARK + '):** ' + ' '.join(wrong) + ' remains correct.\n'
head, body = score.split(heading, 1)
body_parts = body.split('\n## ', 1)
changed = head + heading + body_parts[0] + marker
if len(body_parts) == 2:
    changed += '\n## ' + body_parts[1]
audit.show = lambda root, rev, path: changed if path == audit.SCORECARD else original_show(root, rev, path)
after = audit.atom_c2_evidence_hash(str(ROOT), BASE)
audit.show = original_show
c2 = {'atom': before['id'], 'before': before, 'after_prose_only': after,
      'correction_text': marker.strip(), 'receipt_unchanged': True,
      'correct_hash_present_in_correction': before['evidence']['receipt_target_sha256'] in marker}

route_path = ROOT / 'tools/round-73/packed-elf.py'
source = frozen(route_path)
sys.path.insert(0, str(route_path.parent))
patches = {
 'git_checker_callsite_env_dropped': ('blob_sha = git_blob_sha256(root, rev, TOOL, env=cenv, capture=capture)',
                                    'blob_sha = git_blob_sha256(root, rev, TOOL, env=None, capture=capture)'),
 'readelf_checker_callsite_env_dropped': ('rh = readelf_header(row["source"], env=cenv, capture=capture)',
                                        'rh = readelf_header(row["source"], env=None, capture=capture)'),
 'implicit_checker_callsite_bypassed': ('implicit = implicit_capsule(observed, root)',
                                      'implicit = {"path": None, "absent": None, "skipped": None, "failures": []}'),
 'git_seam_PATH_only_inherited_rest': ('                   env=env, capture=capture)',
                                      '                   env={**os.environ, "PATH": env["PATH"]}, capture=capture)'),
}
c3 = []
for name, (old, new) in patches.items():
    assert source.count(old) == 1, (name, source.count(old))
    mutant = source.replace(old, new)
    mod = types.ModuleType('critic_' + name)
    mod.__file__ = str(route_path)
    exec(compile(mutant, str(route_path), 'exec'), mod.__dict__)
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        rc = mod.selftest(str(S))
    c3.append({'mutant': name, 'old': old, 'new': new, 'rc': rc,
               'selftest': json.loads(output.getvalue())})
print(json.dumps({'axes': ['coverage', 'calibration', 'operability'],
                  'declaration': DECLARATION,
                  'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                  'C1': c1, 'C2': c2, 'C3': c3}, indent=2))
