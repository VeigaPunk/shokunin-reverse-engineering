#!/usr/bin/python3
"""Independent /proc census. Never retain raw environment values."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-73/w1/ExecC1Verify'
S = Path(sys.argv[1])
DECL = 'da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b'
ALLOW = ['HOME', 'LANG', 'PATH', 'TMPDIR']

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def within(value, root):
    return bool(value) and Path(os.fsdecode(value)).is_relative_to(root)

def observe(command, env, wanted):
    # One synchronous producer; no service, worker, thread or background job.
    # stdout/stderr stay in scratch, because checker output can contain receipt
    # environment values. Only selected non-secret verdicts are retained.
    samples = {}
    with (S / 'stdout').open('wb') as stdout, (S / 'stderr').open('wb') as stderr:
        child = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
        deadline = time.monotonic() + 45
        try:
            while child.poll() is None:
                if time.monotonic() > deadline:
                    child.kill()
                    raise TimeoutError('producer exceeded 45 seconds')
                for proc in Path('/proc').iterdir():
                    if not proc.name.isdigit():
                        continue
                    try:
                        argv = (proc / 'cmdline').read_bytes().split(b'\0')
                        matched = next((name for name, shim in wanted.items()
                                        if len(argv) > 1 and os.fsencode(shim) == argv[1]), None)
                        if matched is None:
                            continue
                        stat = (proc / 'stat').read_text().rsplit(')', 1)[1].split()
                        ppid, start_ticks = int(stat[1]), int(stat[19])
                        raw = (proc / 'environ').read_bytes()
                        block = dict(item.split(b'=', 1) for item in raw.split(b'\0') if b'=' in item)
                        # Re-check argv and start time to avoid ordinary exec/PID races.
                        if (proc / 'cmdline').read_bytes().split(b'\0') != argv:
                            continue
                        stat_after = (proc / 'stat').read_text().rsplit(')', 1)[1].split()
                        if int(stat_after[19]) != start_ticks:
                            continue
                        key = (int(proc.name), start_ticks, matched)
                        if key in samples:
                            continue
                        samples[key] = {
                            'pid': int(proc.name), 'ppid': ppid,
                            'producer_pid': child.pid, 'direct_child': ppid == child.pid,
                            'start_ticks': start_ticks, 'class': matched,
                            'executable': os.readlink(proc / 'exe'),
                            'keys': sorted(os.fsdecode(k) for k in block),
                            'canary_present': b'KAIDOKU_ENV_CANARY' in block,
                            'home_under_work': within(block.get(b'HOME'), S),
                            'tmpdir_under_work': within(block.get(b'TMPDIR'), S),
                            'home_equals_work_home': block.get(b'HOME') == os.fsencode(S / 'home'),
                            'tmpdir_equals_work_tmp': block.get(b'TMPDIR') == os.fsencode(S / 'tmp'),
                            'path_starts_shims': block.get(b'PATH', b'').split(b':')[0] == os.fsencode(S / 'bin'),
                            'lang_is_C': block.get(b'LANG') == b'C',
                        }
                    except (OSError, ProcessLookupError, ValueError):
                        continue
                time.sleep(0.005)
        finally:
            if child.poll() is None:
                child.kill()
            rc = child.wait()
    return {'exit_code': rc, 'samples': list(samples.values())}

def main():
    (S / 'bin').mkdir()
    shims = {}
    for tool in ('git', 'readelf'):
        shim = S / 'bin' / tool
        shim.write_text('#!/usr/bin/perl\nselect(undef, undef, undef, 0.4);\nexec "/usr/bin/' + tool + '", @ARGV;\ndie "exec failed";\n')
        shim.chmod(0o700)
        shims[tool] = shim
    shutil.copy2('/usr/bin/upx', S / 'upx-pinned')
    pin = hashlib.sha256((S / 'upx-pinned').read_bytes()).hexdigest()
    save('packer-copy.json', {'sha256': pin, 'matches_pin': pin == 'cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969', 'used_by_checker': False})
    env = dict(os.environ)
    env['PATH'] = str(S / 'bin') + ':' + env.get('PATH', '/usr/bin')
    env['TMPDIR'] = str(S)
    env['KAIDOKU_ENV_CANARY'] = 'ExecC1Verify-census-only'
    commitment = (ROOT / '.ufo/waves/round-73/l1/nonce-commitment.txt').read_text().strip()
    command = ['/usr/bin/python3', '-I', '-B', str(ROOT / 'tools/round-73/packed-elf.py'), '--root', '.', '--rev', DECL, '--pkg', '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents', '--work', str(S), '--check-receipt', '.ufo/waves/round-73/pre/route-at-declaration.json', '--nonce-commitment', commitment]
    genuine = observe(command, env, shims)
    try:
        result = json.loads((S / 'stdout').read_text())
        genuine['checker_verdict'] = {k: result.get(k) for k in ('met', 'failing', 'clauses')}
    except (ValueError, OSError):
        genuine['checker_output_json'] = False
    genuine['classes'] = {name: {'count': sum(s['class'] == name for s in genuine['samples']), 'all_exact_keys': all(s['keys'] == ALLOW for s in genuine['samples'] if s['class'] == name)} for name in shims}
    save('genuine.json', genuine)

    # Deliberately dishonest producer writes only invented key names, not values.
    liar = S / 'lying-shim'
    fake = S / 'fabricated.json'
    liar.write_text('#!/usr/bin/perl\nopen(my $f, ">", "' + str(fake) + '") or die "open failed";\nprint $f \'{"keys":["HOME","LANG","PATH","TMPDIR"],"canary_present":false}\';\nclose($f);\nselect(undef, undef, undef, 0.4);\nexec "/usr/bin/true";\ndie "exec failed";\n')
    liar.chmod(0o700)
    fixture = S / 'producer.py'
    fixture.write_text('import subprocess\nimport sys\nsubprocess.run([sys.argv[1]], env=None, check=True)\n')
    forged = observe(['/usr/bin/python3', '-I', '-B', str(fixture), str(liar)], env, {'liar': liar})
    forged['fabricated_dump'] = json.loads(fake.read_text())
    save('forged.json', forged)
    good = (genuine['samples'] and all(v['count'] > 0 and v['all_exact_keys'] for v in genuine['classes'].values()) and all(not s['canary_present'] and s['home_equals_work_home'] and s['tmpdir_equals_work_tmp'] and s['direct_child'] for s in genuine['samples']))
    dirty = any(s['canary_present'] and s['keys'] != ALLOW and s['direct_child'] for s in forged['samples'])
    summary = {'axes': ['independent observation', 'environment isolation', 'forgery discrimination', 'secret-free retained evidence'], 'genuine_kernel_clean': bool(good), 'forged_kernel_dirty': dirty, 'forged_dump_clean': forged['fabricated_dump']['keys'] == ALLOW and forged['fabricated_dump']['canary_present'] is False, 'genuine_exit_code': genuine['exit_code'], 'forged_exit_code': forged['exit_code'], 'genuine_samples': len(genuine['samples']), 'forged_samples': len(forged['samples']), 'a12_invoked': False, 'twelve_arm_probe_invoked': False}
    save('summary.json', summary)
    print(json.dumps(summary, sort_keys=True))

main()
