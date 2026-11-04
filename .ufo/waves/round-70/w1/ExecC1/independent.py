"""Independent ExecC1 shape builder; does not import the declared battery."""
import copy
import hashlib
import json
from pathlib import Path
import shlex
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-70/w1/ExecC1'
SCRATCH = Path('/fast/scratch/hyaku/kaidoku-r70/ExecC1')
FREEZE = '4737a542ae3b1b910d8fe43efbd572bc578b07c6'
BASE = '5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d'
SOURCE = '.ufo/waves/round-69/l1/scores/c3-at-landing.json'

def invoke(argv):
    p = subprocess.run(argv, cwd=SCRATCH, text=True, capture_output=True, timeout=30)
    return {'argv': argv, 'rc': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr}

def main():
    SCRATCH.mkdir(parents=True, exist_ok=True)
    records = []
    pins = {}
    try:
        for label, revision, path in [('frozen', FREEZE, 'tools/round-70/packed-elf.py'), ('base', BASE, 'tools/round-69/packed-elf.py')]:
            argv = ['git', '-C', str(ROOT), 'show', f'{revision}:{path}']
            raw = subprocess.run(argv, check=True, capture_output=True).stdout
            (SCRATCH / f'{label}.py').write_bytes(raw)
            pins[label] = {'revision': revision, 'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'extraction_command': shlex.join(argv)}
        genuine_raw = (ROOT / SOURCE).read_bytes()
        original = json.loads(genuine_raw)
        (OUT / 'base-genuine.json').write_bytes(genuine_raw)
        shapes = []
        def shape(name, clause, field, value):
            obj = copy.deepcopy(original)
            parent = obj
            for key in field[:-1]:
                parent = parent[key]
            before = parent[field[-1]]
            parent[field[-1]] = value
            shapes.append((name, clause, obj, {'field': field, 'before': before, 'after': value}))
        shape('wrong-revision', 'rev ', ['rev'], '0' * 40)
        shape('zeroed-instrument', 'instrument.sha256', ['instrument', 'sha256'], '0' * 64)
        shape('relabelled-source', 'source ', ['carriers', 0, 'source'], '/usr/bin/exec-c1-relabelled')
        shape('underived-ratio', 'before_ceiling_ratio', ['carriers', 0, 'before_ceiling_ratio'], 0.5)
        shape('packed-over-ceiling', 'packed ', ['carriers', 0, 'packed_counts', 'procedure_count'], 11)
        shape('unknown-carrier', 'unknown carrier id', ['carriers', 0, 'id'], 'exec-c1-unknown')
        for name, clause, obj, mutation in [('base-genuine', None, original, None)] + shapes:
            receipt = SCRATCH / f'{name}.json'
            receipt.write_text(json.dumps(obj, indent=1) + '\n')
            if mutation:
                shutil.copyfile(receipt, OUT / receipt.name)
            row = {'name': name, 'declared_clause': clause, 'mutation': mutation}
            for label in ('frozen', 'base'):
                argv = ['python3', '-I', '-B', str(SCRATCH / f'{label}.py'), '--check-receipt', str(receipt)]
                if label == 'frozen':
                    argv += ['--root', str(ROOT), '--rev', FREEZE]
                result = invoke(argv)
                result['parsed'] = json.loads(result['stdout'])
                row[label] = result
            row['observed_expected'] = (row['frozen']['rc'] == 1 and (clause is None or any(clause in line for line in row['frozen']['parsed']['failing'])) and row['base']['rc'] == 0 and row['base']['parsed']['met'] is True)
            records.append(row)
        payload = {'source': SOURCE, 'source_sha256': hashlib.sha256(genuine_raw).hexdigest(), 'pins': pins, 'rows': records}
        (OUT / 'results.json').write_text(json.dumps(payload, indent=2) + '\n')
        lines = ['# ExecC1 independent R70-C1 re-derivation', '', 'Axes: base acceptance; frozen rejection; mutation-consistent named clauses; evidence reproducibility.', '', '## Method', '', 'Own six-shape builder, each a single-field mutation of the supplied round-69 genuine receipt. No declared forged-receipt battery was run or imported. Readers extracted with read-only git show at exact required revisions. No production code edited; no builds, linters, formatters, or unrelated tests run. No tools installed. LSP unavailable in mounted tools; no symbol refactor required.', '', '```sh', f'python3 -I -B {OUT / "independent.py"}', *[pin['extraction_command'] for pin in pins.values()], '```', '', '## Frozen bytes', '']
        for label, pin in pins.items():
            lines.append(f'- {label}: `{pin["sha256"]}` ({pin["revision"]}:{pin["path"]})')
        lines += ['', f'Source SHA256: `{payload["source_sha256"]}`.', '', '## Per-shape observations', '', '| Shape | Base rc / met | Frozen rc / met | Exact mutation-consistent clause |', '|---|---|---|---|']
        for row in records:
            clauses = row['frozen']['parsed']['failing']
            matched = [line for line in clauses if row['declared_clause'] and row['declared_clause'] in line]
            lines.append(f'| {row["name"]} | {row["base"]["rc"]} / {row["base"]["parsed"]["met"]} | {row["frozen"]["rc"]} / {row["frozen"]["parsed"]["met"]} | ' + '<br>'.join(matched) + ' |')
        lines += ['', '## Attribution limitation', '', 'The unmodified round-69 receipt is itself rejected by the frozen round-70 reader (producer binding and target/carrier-set migration). Therefore rejection alone is not isolated evidence for each mutation. The table records the required mutation-consistent clauses, with all ambient failures retained below and in results.json. This does not establish the full ten-shape predicate, identity-probe arms, battery pin/floor/work-dir/validate arms, or acceptance of a genuine four-carrier landing receipt. Those are outside this six-shape seat assignment. The supplied base genuine control passes the base reader.', '', '## Exact command transcripts', '']
        for row in records:
            lines += [f'### {row["name"]}', '', 'Mutation: `' + json.dumps(row['mutation']) + '`', '']
            for label in ('base', 'frozen'):
                result = row[label]
                lines += ['```text', '$ ' + shlex.join(result['argv']), f'exit: {result["rc"]}', 'stdout:', result['stdout'].rstrip(), 'stderr:', result['stderr'].rstrip(), '```', '']
        met = all(row['observed_expected'] for row in records)
        lines += ['## Evidence and handoff', '', 'Retained: independent.py; results.json (argv/rc/stdout/stderr for all 14 checks); base-genuine.json; six exact mutated receipts; this report. Scratch readers and fixtures removed in finally. No frozen instrument writes or git mutations. Parent should integrate this limited independent evidence with the full frozen predicate evaluation.', '', 'VERDICT: ' + ('met — six independent shapes accepted by base and rejected by frozen reader with mutation-consistent clauses; full R70-C1 not independently established.' if met else 'not-met — at least one required six-shape observation failed; see results.json.')]
        (OUT / 'rederive.md').write_text('\n'.join(lines) + '\n')
        print(json.dumps({'all_expected': met, 'rows': [{'name': r['name'], 'base_rc': r['base']['rc'], 'frozen_rc': r['frozen']['rc'], 'expected': r['observed_expected']} for r in records], 'report': str(OUT / 'rederive.md')}, indent=2))
    finally:
        shutil.rmtree(SCRATCH)

if __name__ == '__main__':
    main()
