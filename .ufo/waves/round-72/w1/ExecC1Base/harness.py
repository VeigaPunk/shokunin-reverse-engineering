#!/usr/bin/python3
"""Independent checker observation; no lane probe imported or executed."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-72/w1/ExecC1Base'
S = Path('/fast/scratch/hyaku/kaidoku-r72/ExecC1Base')
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
NONCE = '20256a954f2613bef25019a6b8c260883cb5f852a624e3af7a5335005326822e'
RECEIPT = '.ufo/waves/round-71/w1/ExecC1/c1-route.json'

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

# Deliberately retain key names and the three assigned non-secret fields only.
# Other values (including credentials/session material) are never decoded or logged.
SHIM = '''#!/usr/bin/python3 -I
import json, os, sys
keys = []
fields = {}
with open('/proc/self/environ', 'rb') as source:
    for item in source.read().split(b'\\0'):
        if not item:
            continue
        key = item.split(b'=', 1)[0]
        keys.append(key.decode('utf-8', 'surrogateescape'))
        if key in (b'HOME', b'TMPDIR', b'KAIDOKU_ENV_CANARY'):
            fields[key.decode()] = item.split(b'=', 1)[1].decode('utf-8', 'surrogateescape')
record = {'tool': TOOL, 'argv': sys.argv[1:], 'keys': sorted(keys),
          'key_count': len(keys), 'canary_present': 'KAIDOKU_ENV_CANARY' in keys,
          'HOME': fields.get('HOME'), 'TMPDIR': fields.get('TMPDIR'),
          'KAIDOKU_ENV_CANARY': fields.get('KAIDOKU_ENV_CANARY')}
with open(LOG, 'a') as target:
    target.write(json.dumps(record, sort_keys=True) + '\\n')
os.execv(REAL, [REAL] + sys.argv[1:])
'''

S.mkdir(parents=True, exist_ok=True)
try:
    # The explicit copy is not executed in checker mode; retained pin evidence only.
    shutil.copy2('/usr/bin/upx', S / 'upx')
    pin = hashlib.sha256((S / 'upx').read_bytes()).hexdigest()
    results = {}
    def measure(round_number, revision):
        base = S / ('r' + str(round_number))
        shimdir = base / 'shims'
        work = base / 'work'
        shimdir.mkdir(parents=True)
        work.mkdir()
        log = base / 'shim.jsonl'
        for tool in ('git', 'readelf'):
            target = shimdir / tool
            target.write_text(SHIM.replace('TOOL', repr(tool)).replace('LOG', repr(str(log))).replace('REAL', repr('/usr/bin/' + tool)))
            target.chmod(0o700)
        env = os.environ.copy()
        env['PATH'] = str(shimdir) + os.pathsep + env.get('PATH', '/usr/bin')
        env['KAIDOKU_ENV_CANARY'] = 'ExecC1Base-r72-before'
        # Outside --work but still inside the one allowed scratch root.
        env['TMPDIR'] = str(S / 'caller-tmp')
        Path(env['TMPDIR']).mkdir(exist_ok=True)
        argv = ['/usr/bin/python3', '-I', '-B', 'tools/round-' + str(round_number) + '/packed-elf.py',
                '--root', '.', '--rev', revision, '--pkg', PKG, '--work', str(work),
                '--check-receipt', RECEIPT, '--nonce-commitment', NONCE]
        proc = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        prefix = 'r' + str(round_number)
        (OUT / (prefix + '.stdout.json')).write_text(proc.stdout)
        (OUT / (prefix + '.stderr.txt')).write_text(proc.stderr)
        records = [json.loads(row) for row in log.read_text().splitlines()] if log.exists() else []
        if log.exists():
            shutil.copy2(log, OUT / (prefix + '.shim.jsonl'))
        verdict = json.loads(proc.stdout) if proc.stdout.strip() else None
        result = {'argv': argv, 'cwd': str(ROOT), 'exit_code': proc.returncode,
                  'revision': revision, 'receipt': RECEIPT, 'verdict': verdict,
                  'observations': [{**r, 'keys': r['keys'][:20], 'keys_truncated': len(r['keys']) > 20,
                      'home_under_work': bool(r['HOME']) and Path(r['HOME']).is_relative_to(work),
                      'tmpdir_under_work': bool(r['TMPDIR']) and Path(r['TMPDIR']).is_relative_to(work)} for r in records],
                  'record_count': len(records),
                  'instrument_sha256': hashlib.sha256((ROOT / argv[3]).read_bytes()).hexdigest()}
        save(prefix + '.result.json', result)
        return prefix, result
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(measure, 71, 'b827a8b5d54f2885ec9be7786389f356c59226ce'),
                   pool.submit(measure, 72, '34fe7aa70b627d92e2d27dbce308d9f5bebda63d')]
        for future in futures:
            key, result = future.result()
            results[key] = result
    save('summary.json', {'axes': ['directness of observation', 'baseline reproducibility', 'producer-binding separation', 'secret minimization'],
         'upx_scratch_copy_sha256': pin, 'results': results,
         'note': 'r72 is a cross-producer rejection control, NOT R72-C1 landing evidence; no probe run.'})
    print(json.dumps({key: {'exit_code': val['exit_code'], 'record_count': val['record_count'],
           'verdict': val['verdict'], 'observations': val['observations']} for key, val in results.items()}, indent=2))
finally:
    shutil.rmtree(S)
