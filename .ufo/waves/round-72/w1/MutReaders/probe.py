#!/usr/bin/env python3
"""Seven frozen-reader mutation probes; writes only named receipts and own scratch."""
import concurrent.futures
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path('/home/vgpnk/Projects/shokunin/kaidoku-shokunin')
OUT = ROOT / '.ufo/waves/round-72/w1/MutReaders'
S = Path('/fast/scratch/hyaku/kaidoku-r72/MutReaders-3')
FREEZE = '34fe7aa70b627d92e2d27dbce308d9f5bebda63d'
AXES = ['behavioral discrimination', 'current selftest coverage', 'exact restoration', 'isolation']
FIXTURE = r'''import contextlib, hashlib, importlib.util, io, json, os, pathlib, sys
seat, code, root, freeze = sys.argv[1:]
p = pathlib.Path(seat)
sys.path.insert(0, str(p))
import capsule_audit as ca
spec = importlib.util.spec_from_file_location('packed', p / 'packed-elf.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def emit(ok, **details):
    print(json.dumps(dict(case=code, ok=ok, **details), sort_keys=True))
    sys.exit(0 if ok else 1)
work = p / 'fixture-work'
work.mkdir(exist_ok=True)
for sub in ('home', 'tmp'):
    (work / sub).mkdir(exist_ok=True)
if code == 'a':
    log = work / 'git-env.jsonl'
    env = m.build_child_env(str(work))
    got = m.git_blob_sha256(root, freeze, m.TOOL, env=env, capture=str(log))
    records = [json.loads(x) for x in log.read_text().splitlines()]
    ok = got is not None and len(records) == 1 and all(sorted(x['env']) == sorted(m.CHILD_ENV_KEYS) and 'KAIDOKU_ENV_CANARY' not in x['env'] and ca.under(str(work), x['env'].get('HOME', '')) for x in records)
    emit(ok, child_records=records, blob_sha256=got, expected='git child receives only allowlisted run-scoped environment')
if code in ('b', 'c'):
    receipt = json.loads((pathlib.Path(root) / '.ufo/waves/round-72/l1/pre/route-at-declaration.json').read_text())
    receipt['rev'] = freeze
    receipt['instrument']['sha256'] = m.git_blob_sha256(root, freeze, m.TOOL, env=m.build_child_env(str(work)))
    env = m.build_child_env(str(work))
    if code == 'c':
        raw = dict(env, EXTRA_KEY='polluted-raw-witness')
        capsule = work / 'capsule.jsonl'
        capsule.write_text(json.dumps({'argv': ['/usr/bin/git', 'show'], 'env': raw}) + '\n')
        receipt['child_env_observed'] = dict(log=str(capsule), records=1, keys=sorted(m.CHILD_ENV_KEYS), canary_present=False, home_under_run=True, tmpdir_under_run=True, children={'git': 1}, run_root=str(work))
    else:
        receipt['child_env_observed'] = {}
    rp = work / 'receipt.json'
    rp.write_text(json.dumps(receipt))
    log = work / 'checker-env.jsonl'
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        rc = m.check_receipt(str(rp), root, freeze, work=str(work), child_env_log=str(log))
    result = json.loads(output.getvalue())
    records = [json.loads(x) for x in log.read_text().splitlines()]
    if code == 'b':
        readers = [x for x in records if os.path.basename(x['argv'][0]) == 'readelf']
        ok = rc == 0 and bool(readers) and all(sorted(x['env']) == sorted(m.CHILD_ENV_KEYS) and 'KAIDOKU_ENV_CANARY' not in x['env'] and ca.under(str(work), x['env'].get('HOME', '')) for x in readers)
        emit(ok, checker_rc=rc, checker=result, readelf_records=readers, expected='checker readelf inherits allowlist, not caller canary or HOME')
    ok = rc == 1 and result['clauses']['receipt_capsule'] is False and any('receipt_capsule: keys' in x for x in result['failing'])
    emit(ok, checker_rc=rc, checker=result, expected='implicit observed.log resolves and rejects lying clean summary over polluted capsule')
if code in ('d', 'e', 'f'):
    env = {'HOME': str(work / 'home'), 'LANG': 'C', 'PATH': '/usr/bin', 'TMPDIR': str(work / 'tmp')}
    rows = [{'argv': ['/usr/bin/git'], 'env': env}]
    capsule = work / 'capsule.jsonl'
    capsule.write_text(json.dumps(rows[0]) + '\n')
    summary = dict(records=1, keys=list(ca.ALLOW), canary_present=False, children={'git': 1}, run_root=str(work))
    control = ca.audit(str(capsule), summary)
    if code == 'd':
        summary['canary_present'] = True
        clause = 'canary'
    elif code == 'e':
        env['HOME'] = str(work) + '-escaped/home'
        capsule.write_text(json.dumps(rows[0]) + '\n')
        clause = 'home_under_run'
    else:
        summary['records'] = 2
        clause = 'records'
    result = ca.audit(str(capsule), summary)
    emit(control['ok'] is True and result['ok'] is False and clause in result['failures'], control=control, audit=result, expected='clean control accepted; contradictory ' + clause + ' rejected')
if code == 'g':
    nonce = 'ab' * 32
    commitment = hashlib.sha256(nonce.encode()).hexdigest()
    receipt = dict(run_nonce=nonce, instrument={'sha256': 'cc' * 32}, carriers=[{'packed_sha256': 'dd' * 32}], run_root=str(work), child_env_observed={})
    receipt['run_binding'] = m.run_binding(nonce, 'cc' * 32, ['dd' * 32])
    control = m.nonce_verdict(receipt, commitment)
    receipt['run_binding'] = 'forged-but-present'
    bad = m.nonce_verdict(receipt, commitment)
    emit(control['binding_ok'] is True and bad['binding_ok'] is False, control=control, forged=bad, expected='nonempty forged binding is false in checker JSON clause')
'''

def sha(data):
    return hashlib.sha256(data).hexdigest()

def run(argv, env):
    p = subprocess.run(argv, cwd=ROOT, env=env, text=True, capture_output=True, timeout=90)
    return dict(argv=argv, rc=p.returncode, stdout=p.stdout, stderr=p.stderr)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    S.mkdir(parents=True, exist_ok=True)
    names = ['packed-elf.py', 'capsule-audit.py', 'capsule_audit.py']
    originals = {name: subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{FREEZE}:tools/round-72/{name}']) for name in names}
    cut = b'''    if capsule_path is None and isinstance(observed, dict) \\\n            and isinstance(observed.get("log"), str):
        cand = observed["log"]
        if not os.path.isabs(cand):
            cand = os.path.join(os.path.abspath(root), cand)
        if os.path.exists(cand):
            capsule_path = cand
'''
    mutations = [
        ('a', 'packed-elf.py', b'env=env, capture=capture)\n    except Unevaluable:\n        return None', b'env=None, capture=capture)\n    except Unevaluable:\n        return None', 'git-reader-allowlisted-exec'),
        ('b', 'packed-elf.py', b'run(["readelf", "-h", row["source"]], env=cenv, capture=capture)', b'run(["readelf", "-h", row["source"]], capture=capture)', 'checker-readelf-allowlisted-exec'),
        ('c', 'packed-elf.py', cut, b'', 'implicit-capsule-polluted-raw-log'),
        ('d', 'capsule_audit.py', b'\n        and want.get("canary_present") is not True', b'', 'summary-canary-contradiction'),
        ('e', 'capsule_audit.py', b'os.path.commonpath([root_abs, os.path.abspath(str(path))]) == root_abs', b'os.path.abspath(str(path)).startswith(root_abs)', 'sibling-prefix-escaped-HOME'),
        ('f', 'capsule_audit.py', b'        "records": want.get("records") == derived["records"],\n', b'', 'summary-record-count-mismatch'),
        ('g', 'packed-elf.py', b'binding_ok = bool(nonce_ok) and receipt.get("run_binding") == want', b'binding_ok = receipt.get("run_binding") is not None', 'forged-present-binding'),
    ]
    rows = []
    env = dict(os.environ, TMPDIR=str(S), KAIDOKU_ENV_CANARY='MutReaders-canary', HOME=str(S / 'caller-home'))
    (S / 'caller-home').mkdir(exist_ok=True)
    fixture = S / 'fixture.py'
    fixture.write_text(FIXTURE)
    def probe(mutation):
        key, target, old, new, case = mutation
        original = originals[target]
        assert original.count(old) == 1, (key, original.count(old), old)
        changed = original.replace(old, new, 1)
        patch = ''.join(difflib.unified_diff(original.decode().splitlines(True), changed.decode().splitlines(True), fromfile='a/tools/round-72/' + target, tofile='b/tools/round-72/' + target))
        (OUT / f'{key}.patch').write_text(patch)
        stages = {}
        seat = S / key
        seat.mkdir()
        for name, payload in originals.items():
            (seat / name).write_bytes(payload)
        before = sha((seat / target).read_bytes())
        for stage, payload in [('pristine', original), ('mutated', changed), ('restored', original)]:
            (seat / target).write_bytes(payload)
            stenv = dict(env, TMPDIR=str(seat))
            tool = 'capsule-audit.py' if target == 'capsule_audit.py' else 'packed-elf.py'
            args = ['python3', '-I', '-B', str(seat / tool), '--selftest']
            if tool == 'packed-elf.py':
                args += ['--work', str(seat)]
            stages[stage] = {'sha256': sha((seat / target).read_bytes()), 'selftest': run(args, stenv), 'behavior': run(['python3', '-I', '-B', str(fixture), str(seat), key, str(ROOT), FREEZE], stenv)}
            # Avoid appending captured records across the exact same detector run.
            shutil.rmtree(seat / 'fixture-work', ignore_errors=True)
        after = sha((seat / target).read_bytes())
        def verdict(detector):
            if stages['pristine'][detector]['rc'] != 0 or stages['restored'][detector]['rc'] != 0:
                return 'inconclusive'
            return 'killed' if stages['mutated'][detector]['rc'] != 0 else 'survived'
        row = dict(mutant=key, target=target, expected_detector=case, patch=f'{key}.patch', before_sha256=before, mutated_sha256=sha(changed), after_sha256=after, restored_exact=before == after, stages=stages, selftest_verdict=verdict('selftest'), behavioral_verdict=verdict('behavior'))
        (OUT / f'{key}.json').write_text(json.dumps(row, indent=2) + '\n')
        return row
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
            rows = list(pool.map(probe, mutations))
        result = dict(freeze=FREEZE, axes=AXES, originals={k: sha(v) for k, v in originals.items()}, mutants=rows, tools_installed=[], scratch=str(S), scratch_cleanup='finally shutil.rmtree', source_unchanged='Only frozen git-show bytes copied into seat scratch; no source edits')
        (OUT / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
        lines = ['# MutReaders — frozen round-72 reader mutations', '', 'Axes: ' + ', '.join(AXES) + '.', '', 'All seven defects were applied separately to isolated copies of operative-freeze bytes. Each stage ran the same bounded detector (90-second subprocess timeout), with a caller canary and caller HOME outside the checker run root. No production sources changed. No tool installation.', '', '| Mutant | Binding case | Selftest | Behavioral fixture | Exact restoration |', '|---|---|---|---|---|']
        for r in rows:
            lines.append(f"| {r['mutant']} | {r['expected_detector']} | {r['selftest_verdict']} | {r['behavioral_verdict']} | {r['restored_exact']} |")
        lines += ['', '## Actual outputs and restoration', '', 'Full argv, rc, stdout/stderr and pristine/mutated/restored SHA-256 values are in results.json and a.json–g.json. Unified defect patches are a.patch–g.patch. A nonzero pristine or restored detector is inconclusive, never counted as a kill.', '', '## Current test boundary', '', 'See results.json for observed selftest survivors. The new allowlisted-exec fixtures directly execute the git reader and checker readelf with raw child-environment capture; they are not part of current --selftest. The implicit-capsule fixture omits the explicit capsule argument, names an absolute observed.log, and supplies a clean claimed key set over a polluted raw record. Other cases isolate a contradictory claimed canary, sibling-prefix HOME escape, count lie, and forged present binding.', '', '## Scope and risks', '', 'Only the assigned selftests and new targeted behavioral fixtures were exercised. No full seam-probe/battery claim about all current integration tests is made. Existing A11 is a separate behavioral integration detector; whether it detects environment mutants is not inferred from selftest survival. Receipt fixtures reuse retained route evidence, replacing rev and producer digest with the frozen git blob solely to isolate checker clauses. Scratch is removed in finally before return.', '', '## Self-evaluation', '', 'Accuracy 4: exact outputs retained, but no full integration detector run. Completeness 4: seven requested defects and three-stage detectors; boundary limited to assigned probes. Clarity 4: table plus full machine receipts; large raw environment output is relegated to JSON. Actionability 4: named missing binding cases and exact patches; not integrated into production tests. Conciseness 4: summarized here, full receipts separate. Overall 4.0. Highest-impact improvement: add executable git/readelf environment and implicit-capsule cases to current selftest. User agreement check: results distinguish local selftest coverage from full integration coverage.', '', 'Report: .ufo/waves/round-72/w1/MutReaders/MutReaders.md', '']
        text = '\n'.join(lines)
        (OUT / 'MutReaders.md').write_text(text)
        (ROOT / '.ufo/waves/round-72/w1/MutReaders.md').write_text(text)
        print(json.dumps([dict(mutant=r['mutant'], selftest=r['selftest_verdict'], behavior=r['behavioral_verdict'], restored=r['restored_exact'], rc={stage: {d: r['stages'][stage][d]['rc'] for d in ('selftest', 'behavior')} for stage in ('pristine', 'mutated', 'restored')}) for r in rows], indent=2))
    finally:
        shutil.rmtree(S)

if __name__ == '__main__':
    main()
