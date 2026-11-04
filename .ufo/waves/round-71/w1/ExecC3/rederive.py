"""Independent R71-C3 derivation; no imports from instruments under test."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-71/w1/ExecC3'
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r71/ExecC3')
BASE = '82c8e620c9222fb218aa0260570a3765da2afb44'
FREEZE = 'b827a8b5d54f2885ec9be7786389f356c59226ce'
OPEN = '<!-- instrument-registry v2 -->'
CLOSE = '<!-- /instrument-registry -->'


def git(*args: str) -> bytes:
    return subprocess.run(['git', '-C', str(ROOT), *args], check=True,
                          capture_output=True).stdout


def split_row(line: str) -> list[str]:
    # Locate pipe separators independently using a regex, not the census loop.
    body = line.strip()[1:-1]
    return [cell.replace(r'\|', '|').strip()
            for cell in re.split(r'(?<!\\)\|', body)]


def parse(text: str, inventory: set[str]) -> list[dict]:
    assert text.count(OPEN) == text.count(CLOSE) == 1
    active = False
    rows = []
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        if OPEN in line:
            active = True
            continue
        if CLOSE in line:
            active = False
        if not active or not line.lstrip().startswith('|'):
            continue
        assert line.rstrip().endswith('|')
        cells = split_row(line)
        if cells[0] == 'tool' or all(re.fullmatch(r':?-+:?', c) for c in cells):
            continue
        token = cells[0]
        path = token[1:-1] if token.startswith('`') and token.endswith('`') else ''
        pinned = '|'.join(cells[4:len(cells)-2]).strip()
        defects = []
        if len(cells) < 6:
            defects.append('cells<6')
        if not path or not re.fullmatch(r'[A-Za-z0-9._/-]+', path) or path.startswith('/') or '..' in path.split('/'):
            defects.append('path-invalid')
        if path not in inventory:
            defects.append('path-absent')
        if pinned in ('', '—'):
            defects.append('pinned-empty')
        rows.append(dict(line=number, cells=len(cells), path=path,
                         exists_at_base=path in inventory, pinned=pinned,
                         write=cells[-2], owner=cells[-1], defects=defects,
                         raw_line=line))
    assert rows
    return rows


def save(name: str, value) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def run(name: str, argv: list[str]) -> dict:
    environment = dict(os.environ, TMPDIR=str(SCRATCH), HYAKU_SCRATCH=str(SCRATCH))
    proc = subprocess.run(argv, capture_output=True, text=True,
                          cwd=SCRATCH, env=environment)
    (OUT / (name + '.stdout')).write_text(proc.stdout)
    (OUT / (name + '.stderr')).write_text(proc.stderr)
    return dict(name=name, argv=argv, cwd=str(SCRATCH), rc=proc.returncode,
                stdout=name + '.stdout', stderr=name + '.stderr')


def main() -> None:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    try:
        skill_bytes = git('show', BASE + ':SKILL.md')
        skill = skill_bytes.decode()
        inventory = set(git('ls-tree', '-r', '--name-only', BASE).decode().splitlines())
        before = parse(skill, inventory)
        r69 = [r for r in before if r['cells'] == 8]
        r70 = [r for r in before if r['cells'] == 6]
        assert len(r69) == 4 and all(r['path'].startswith('tools/round-69/') for r in r69)
        assert len(r70) == 6 and all(r['path'].startswith('tools/round-70/') for r in r70)
        assert all(r['cells'] in (6, 7, 8) and r['exists_at_base'] for r in before)
        assert [r['defects'] for r in before if r['defects']] == [['pinned-empty']] * 6
        save('independent-base.json', before)
        (SCRATCH / 'SKILL.base.md').write_bytes(skill_bytes)
        lines = skill.splitlines(keepends=True)
        for row in r70:
            old = lines[row['line'] - 1]
            assert old.endswith('|\n')
            lines[row['line'] - 1] = old[:-1] + ' kaidoku |\n'
        repaired = ''.join(lines)
        (SCRATCH / 'SKILL.repaired.md').write_text(repaired)
        after = parse(repaired, inventory)
        save('independent-repaired.json', after)
        assert not any(r['defects'] for r in after)
        assert len({r['path'] for r in after}) == len(after)
        save('six-row-repair.json', [dict(path=a['path'], old=b['raw_line'], new=a['raw_line'])
                                   for b, a in zip(before, after) if b['raw_line'] != a['raw_line']])
        before69 = ''.join(r['raw_line'] for r in before if r['path'].startswith('tools/round-69/'))
        after69 = ''.join(r['raw_line'] for r in after if r['path'].startswith('tools/round-69/'))
        (OUT / 'round69-base.lines').write_text(before69)
        (OUT / 'round69-repaired.lines').write_text(after69)
        tool = 'tools/round-71/registry-census.py'
        frozen = git('show', FREEZE + ':' + tool)
        container = json.loads(git('show', FREEZE + ':.ufo/waves/round-71/claims.json'))
        digest = hashlib.sha256(frozen).hexdigest()
        assert digest == container['instruments'][tool]
        executable = SCRATCH / 'registry-census.py'
        executable.write_bytes(frozen)
        legacy = SCRATCH / 'census3.py'
        legacy_bytes = git('show', BASE + ':tools/round-51/census3.py')
        legacy.write_bytes(legacy_bytes)
        commands = [
            ('census-base', [sys.executable, '-I', '-B', str(executable), '--root', str(ROOT), '--rev', BASE, '--generate', '--out', str(OUT / 'census-base.json')]),
            ('census-freeze', [sys.executable, '-I', '-B', str(executable), '--root', str(ROOT), '--rev', FREEZE, '--generate', '--out', str(OUT / 'census-freeze.json')]),
            ('census-selftest', [sys.executable, '-I', '-B', str(executable), '--selftest']),
            ('legacy-base', [sys.executable, '-I', '-B', str(legacy), '--root', str(ROOT), '--rev', BASE, '--check']),
            ('round69-diff', ['diff', '-u', str(OUT / 'round69-base.lines'), str(OUT / 'round69-repaired.lines')]),
        ]
        with ThreadPoolExecutor(max_workers=5) as pool:
            runs = list(pool.map(lambda item: run(*item), commands))
        save('commands.json', runs)
        summary = dict(axes=['operability', 'independent reproducibility', 'scope safety'],
                       base=BASE, freeze=FREEZE, python=sys.version, python_executable=sys.executable,
                       frozen_census_sha256=digest, pin_matches=True,
                       legacy_sha256=hashlib.sha256(legacy_bytes).hexdigest(),
                       base_skill_sha256=hashlib.sha256(skill_bytes).hexdigest(),
                       base_rows=len(before), base_cell_counts=dict(Counter(r['cells'] for r in before)),
                       base_paths=len({r['path'] for r in before}), base_absent=sum(not r['exists_at_base'] for r in before),
                       base_nonconformant=sum(bool(r['defects']) for r in before),
                       repaired_rows=len(after), repaired_paths=len({r['path'] for r in after}),
                       repaired_nonconformant=sum(bool(r['defects']) for r in after),
                       repaired_cells=dict(Counter(r['cells'] for r in after)),
                       round69_diff_rc=runs[-1]['rc'], round69_unchanged=before69 == after69,
                       changed_rows=sum(b['raw_line'] != a['raw_line'] for b, a in zip(before, after)),
                       runs=runs, tools_installed=[])
        save('summary.json', summary)
        print(json.dumps(summary, indent=2))
    finally:
        shutil.rmtree(SCRATCH)


if __name__ == '__main__':
    main()
