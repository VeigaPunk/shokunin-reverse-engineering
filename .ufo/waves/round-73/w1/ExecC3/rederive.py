#!/usr/bin/env python3
"""Independent R73-C3 reproduction; no mutation battery patch table imported."""
import ast
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-73/w1/ExecC3'
S = Path('/fast/scratch/hyaku/kaidoku-r73/ExecC3')
BASE = '05bf065684e52d72ea25aad95f7acb71fcd7874c'
DECL = 'da6c17c1eb8dec0b780e276c7f1cb8d9b4fa4d4b'
CASES = dict(a='git-reader-allowlisted-exec', b='checker-readelf-allowlisted-exec', c='implicit-capsule-polluted-raw-log')

def blob(rev, path):
    return subprocess.run(['git', '-C', str(ROOT), 'show', f'{rev}:{path}'], check=True, capture_output=True).stdout

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def mutate(source, round_no, arm):
    """Locate semantic AST seams, then edit source spans, not battery strings."""
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if arm in ('a', 'b'):
        func = functions['git_blob_sha256' if arm == 'a' else ('readelf_header' if round_no == 73 else 'check_receipt')]
        candidates = []
        for n in ast.walk(func):
            if not isinstance(n, ast.Call) or not isinstance(n.func, ast.Name) or n.func.id != 'run' or not n.args:
                continue
            argv = n.args[0]
            if isinstance(argv, ast.List) and argv.elts and isinstance(argv.elts[0], ast.Constant) and argv.elts[0].value == ('git' if arm == 'a' else 'readelf'):
                candidates.append(n)
        assert len(candidates) == 1, (arm, len(candidates))
        kw = next(k for k in candidates[0].keywords if k.arg == 'env')
        assert kw.lineno == kw.end_lineno
        line = lines[kw.lineno - 1]
        if arm == 'a':
            lines[kw.lineno - 1] = line[:kw.value.col_offset] + 'None' + line[kw.value.end_col_offset:]
        else:
            assert line[kw.end_col_offset:kw.end_col_offset + 2] == ', '
            lines[kw.lineno - 1] = line[:kw.col_offset] + line[kw.end_col_offset + 2:]
    elif round_no == 72:
        # Original c.patch deletes implicit derivation. At base its hardened
        # equivalent is this elif body, including containment/file checks.
        func = functions['check_receipt']
        candidates = [n for n in ast.walk(func) if isinstance(n, ast.If) and ast.get_source_segment(source, n.test).startswith('isinstance(observed, dict)')]
        assert len(candidates) == 1
        node = candidates[0]
        assert lines[node.lineno - 1].lstrip().startswith('elif ')
        del lines[node.lineno - 1:node.end_lineno]
    else:
        # The same derivation moved into implicit_capsule. Remove its whole
        # resolving body; retain its existing empty-result initializer/return.
        func = functions['implicit_capsule']
        initializer = next(n for n in func.body if isinstance(n, ast.Assign))
        start = initializer.end_lineno
        lines[start:func.end_lineno] = ['    return out\n']
    result = ''.join(lines)
    ast.parse(result)
    return result

def run(argv):
    proc = subprocess.run(argv, cwd=S, env=ENV, capture_output=True, text=True, timeout=300)
    return {'argv': argv, 'rc': proc.returncode, 'stdout': proc.stdout, 'stderr': proc.stderr}

S.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
ENV = {'PATH': '/usr/bin:/bin', 'HOME': str(S / 'home'), 'LANG': 'C', 'TMPDIR': str(S), 'PYTHONCOERCECLOCALE': '0'}
(S / 'home').mkdir(exist_ok=True)
try:
    patches = {}
    for arm in CASES:
        data = blob(BASE, f'.ufo/waves/round-72/w1/MutReaders/{arm}.patch')
        (OUT / f'original-{arm}.patch').write_bytes(data)
        patches[arm] = hashlib.sha256(data).hexdigest()
    summary = {'axes': ['independent seam fidelity', 'named-case discrimination', 'pin enforcement', 'scope and secret safety'], 'base': BASE, 'declaration': DECL, 'patch_sha256': patches, 'selftests': [], 'batteries': [], 'lsp': 'Unavailable: no LSP tool mounted; AST used for independent symbol-local source surgery.', 'installs': []}
    for round_no, rev in [(72, BASE), (73, DECL)]:
        folder = S / f'r{round_no}'
        folder.mkdir()
        target = f'tools/round-{round_no}/packed-elf.py'
        data = blob(rev, target)
        source = data.decode()
        (folder / 'capsule_audit.py').write_bytes(blob(rev, f'tools/round-{round_no}/capsule_audit.py'))
        for arm in ['pristine', 'a', 'b', 'c']:
            retained = OUT / f'r{round_no}-{arm}.json'
            if retained.exists():
                result = json.loads(retained.read_text())
                summary['selftests'].append({k: result[k] for k in ('round', 'arm', 'rc', 'cases', 'failed', 'expected_case', 'source_sha256', 'mutant_sha256')})
                continue
            text = source if arm == 'pristine' else mutate(source, round_no, arm)
            path = folder / f'{arm}.py'
            path.write_text(text)
            if arm != 'pristine':
                (OUT / f'r{round_no}-{arm}.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True), text.splitlines(True), fromfile=target, tofile=f'{arm}/{target}')))
            result = run(['/usr/bin/python3', '-I', '-B', str(path), '--selftest', '--work', str(S)])
            payload = json.loads(result['stdout'])
            result.update(round=round_no, arm=arm, source_rev=rev, source_sha256=hashlib.sha256(data).hexdigest(), mutant_sha256=hashlib.sha256(text.encode()).hexdigest(), cases=payload['cases'], failed=payload['failed'], expected_case=CASES.get(arm))
            save(f'r{round_no}-{arm}.json', result)
            summary['selftests'].append({k: result[k] for k in ('round', 'arm', 'rc', 'cases', 'failed', 'expected_case', 'source_sha256', 'mutant_sha256')})
    battery = S / 'mutation-check.py'
    battery.write_bytes(blob(DECL, 'tools/round-73/mutation-check.py'))
    summary['battery_sha256'] = hashlib.sha256(battery.read_bytes()).hexdigest()
    summary['battery_dependency_comparison'] = {}
    for round_no in (72, 73):
        module_path = f'tools/round-{round_no}/capsule_audit.py'
        frozen = blob(DECL, module_path)
        current = (ROOT / module_path).read_bytes()
        summary['battery_dependency_comparison'][module_path] = {'frozen_sha256': hashlib.sha256(frozen).hexdigest(), 'working_sha256': hashlib.sha256(current).hexdigest(), 'equal': frozen == current}
    for patch_set, round_no in [('r73', 73), ('r73base', 72)]:
        tool = f'tools/round-{round_no}/packed-elf.py'
        digest = hashlib.sha256(blob(DECL, tool)).hexdigest()
        for pin_mode in ('correct', 'wrong'):
            pin = digest if pin_mode == 'correct' else '0' * 64
            argv = ['/usr/bin/python3', '-I', '-B', str(battery), '--root', str(ROOT), '--rev', DECL, '--tool', tool, '--patch-set', patch_set, '--work', str(S), '--expect-target-sha256', pin]
            if patch_set == 'r73':
                argv += ['--min-pristine-cases', '38']
            result = run(argv)
            save(f'battery-{patch_set}-{pin_mode}.json', result)
            payload = json.loads(result['stdout'] or result['stderr'])
            result['receipt'] = payload
            save(f'battery-{patch_set}-{pin_mode}.json', result)
            summary['batteries'].append({'patch_set': patch_set, 'pin_mode': pin_mode, 'rc': result['rc'], 'survivor_count': payload.get('survivor_count'), 'target_pin': payload.get('target_pin'), 'ok': payload.get('ok'), 'pristine': payload.get('pristine'), 'mutants': payload.get('mutants')})
    save('summary.json', summary)
    print(json.dumps(summary, indent=2))
finally:
    shutil.rmtree(S)
