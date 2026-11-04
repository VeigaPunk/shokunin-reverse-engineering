#!/usr/bin/env python3
"""Reproduce frozen A8/A9 expression acceptance, NOT a full CLI probe success.
Usage: python3 -I -B boundary-repro.py LANE_ROOT OWN_SCRATCH_ROOT
Creates only a temporary directory below OWN_SCRATCH_ROOT and removes it.
The fake process boundary is intentional: no child environment is observed.
"""
import ast
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types

sys.dont_write_bytecode = True
root, scratch = sys.argv[1:]
freeze = 'b827a8b5d54f2885ec9be7786389f356c59226ce'
source = subprocess.run(['git', '-C', root, 'show', freeze + ':tools/round-71/seam-probe.py'], capture_output=True, check=True).stdout.decode()
tree = ast.parse(source)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'check')
a = next(i for i, n in enumerate(fn.body) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'a8_dir' for t in n.targets))
b = next(i for i, n in enumerate(fn.body) if isinstance(n, ast.If) and isinstance(n.test, ast.BoolOp) and any(isinstance(v, ast.Name) and v.id == 'nonce_commitment' for v in n.test.values))
block = compile(ast.fix_missing_locations(ast.Module(body=fn.body[a:b], type_ignores=[])), 'frozen-A8-A9', 'exec')
keys = ['HOME', 'LANG', 'PATH', 'TMPDIR']
with tempfile.TemporaryDirectory(prefix='critic-boundary-', dir=scratch) as work:
    def fake_invoke(_instrument, _root, _rev, _pkg, parent, extra, **kwargs):
        rr = str(Path(parent) / 'precreated')
        Path(rr).mkdir()
        env = dict(HOME=rr + '-outside/home', TMPDIR=rr + '-outside/tmp', LANG='C', PATH='/usr/bin')
        records = [dict(argv=[name], env=env) for name in ('upx', 'node', 'readelf')]
        Path(extra[extra.index('--child-env-log') + 1]).write_text(''.join(json.dumps(r) + '\n' for r in records))
        obs = dict(records=3, all_allowlisted=True, canary_present=False, keys=keys)
        Path(extra[extra.index('--json-out') + 1]).write_text(json.dumps(dict(run_root=rr, child_env_observed=obs)))
        return dict(rc=0)

    class FakeProcess:
        serial = 0
        def __init__(self, argv, **kwargs):
            FakeProcess.serial += 1
            self.argv = argv
            self.rr = str(Path(argv[argv.index('--work') + 1]) / ('precreated-' + str(self.serial)))
            Path(self.rr).mkdir()
            self.returncode = 1 if '--skip-run' in argv else 0

        def communicate(self, **kwargs):
            if '--skip-run' not in self.argv:
                return json.dumps(dict(work_dir=self.rr)), ''
            record = dict(argv=['invented-child'], env=dict(HOME=self.rr + '-outside/home', TMPDIR=self.rr + '-outside/tmp'))
            Path(self.argv[self.argv.index('--child-env-log') + 1]).write_text(json.dumps(record) + '\n')
            Path(self.argv[self.argv.index('--json-out') + 1]).write_text(json.dumps(dict(run_root=self.rr, verdict_claimed=False)))
            return '', ''

    env = dict(os=os, tempfile=tempfile, json=json, sys=sys,
               subprocess=types.SimpleNamespace(Popen=FakeProcess, PIPE=subprocess.PIPE),
               work=work, instrument='UNEXECUTED', root=root, rev=freeze,
               tool='tools/round-71/packed-elf.py', pkg='UNEXECUTED', battery='UNEXECUTED',
               arms=[], CHILD_ENV_KEYS=keys, invoke=fake_invoke,
               arm=lambda aid, ok, obs: dict(id=aid, ok=bool(ok), observed=obs))
    exec(block, env)
    print(json.dumps(env['arms'], indent=2))
