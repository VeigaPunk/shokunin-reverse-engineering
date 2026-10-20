#!/usr/bin/env python3
"""Retained round-19 verification producer, not a general mutation framework.
Usage: python3 -I -B postfix-mutations.py SOURCE_COMMIT
One private clone; local commits only; emits actual pristine/mutated/restored
counter outputs and exits. Exit 0 means report emitted, not all mutants killed.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

LANE = Path(__file__).resolve().parents[3]
W = '.ufo/waves/round-19'
ENV = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'JJ_'))}
ENV.update(GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@local',
           GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@local')


def main():
    source = sys.argv[1]
    scratch = Path(tempfile.mkdtemp(prefix='kr19-postfix-', dir='/tmp'))
    repo = scratch / 'repo'
    try:
        subprocess.run(['git', 'clone', '-q', '--shared', str(LANE), str(repo)],
                       check=True, env=ENV)
        def git(*args):
            return subprocess.check_output(['git', '-C', str(repo), *args], env=ENV).decode().strip()
        git('checkout', '-q', '--detach', source)
        git('config', 'core.hooksPath', '/dev/null')
        def commit(message):
            git('add', '-A'); git('commit', '-q', '-m', message)
            return git('rev-parse', 'HEAD')
        def counter(rev, root=None, extra_env=None):
            argv = [sys.executable, '-I', '-B', str(repo / W / 'tools/routed-r18.py'),
                    '--root', root or str(repo), '--rev', rev, '--strict']
            p = subprocess.run(argv, cwd=repo, env={**ENV, **(extra_env or {})},
                               capture_output=True, text=True)
            try: doc = json.loads(p.stdout)
            except ValueError: doc = {'unparseable': p.stdout, 'stderr': p.stderr}
            return {'argv': argv, 'exit': p.returncode, 'result': doc}
        pristine = counter(source)
        results = []
        def probe(name, rel, change, defect):
            path = repo / rel
            original = path.read_bytes()
            candidate = change(original.decode())
            if candidate.encode() == original:
                raise RuntimeError('mutation changed nothing: ' + name)
            path.write_text(candidate)
            mutant = commit(name)
            red = counter(mutant)
            path.write_bytes(original)
            restored = commit('restore ' + name)
            green = counter(restored)
            expected_id = 'R18-' + defect
            opened = [d['id'] for d in red['result'].get('defects', [])
                      if not (d['named'] and d['substance'])]
            results.append({'name': name, 'mutated_revision': mutant,
                            'restored_revision': restored, 'path': rel,
                            'original_sha256': hashlib.sha256(original).hexdigest(),
                            'mutated': red, 'restored': green,
                            'target_open': expected_id in opened,
                            'killed': red['exit'] == 1 and expected_id in opened
                                      and green['exit'] == 0})
        def json_change(fn):
            def transform(text):
                d = json.loads(text); fn(d)
                return json.dumps(d, indent=2) + '\n'
            return transform
        strict = W + '/evidence/strict-baseline/9011581d8452'
        def forged_stdout(text):
            d = json.loads(text); d['open_count'] = 777; d['fabricated'] = True
            out = json.dumps(d, indent=2) + '\n'
            r = json.loads((repo / (strict + '.receipt.json')).read_text())
            r['stdout_sha256'] = hashlib.sha256(out.encode()).hexdigest()
            (repo / (strict + '.receipt.json')).write_text(json.dumps(r, indent=2))
            return out
        # This mutant changes a stdout/receipt pair; restore both exact bytes.
        receipt_original = (repo / (strict + '.receipt.json')).read_bytes()
        probe('strict-self-consistent-fabrication', strict + '.stdout.txt', forged_stdout,
              'STRICT-BASELINE')
        (repo / (strict + '.receipt.json')).write_bytes(receipt_original)
        commit('restore strict receipt companion')
        # The probe's immediate restoration remains red until the companion
        # receipt is restored; retain that rather than calling it a kill.
        results[-1]['restored_companion'] = counter(git('rev-parse', 'HEAD'))
        results[-1]['killed'] = (results[-1]['mutated']['exit'] == 1
                                and results[-1]['target_open']
                                and results[-1]['restored_companion']['exit'] == 0)
        probe('strict-wrong-producer', strict + '.receipt.json',
              json_change(lambda d: d.update(
                  tool_rev=source, tool_sha256=hashlib.sha256(
                      (repo / '.ufo/waves/round-18/tools/routed-defects.py').read_bytes()).hexdigest())),
              'STRICT-BASELINE')
        probe('fabricated-causes', W + '/evidence/r18-dead-seats.json',
              json_change(lambda d: [s.update(cause='unknown', source='SCORECARD.md:1')
                                     for s in d['seats']]), 'DEADSEAT-RECORD')
        def unrelated(text):
            lines = text.splitlines(True)
            for i, line in enumerate(lines):
                if line.startswith('| go-buildinfo-probe |'):
                    start = line.index('Pinned values:')
                    lines[i] = line[:start] + line[start:].replace(
                        '.ufo/waves/round-17/tools/buildinfo-probe.py', 'corpus/lessons/round-19.md')
            return ''.join(lines)
        probe('unrelated-pin-path', 'SKILL.md', unrelated, 'REGISTRY-PINNED')
        def swap(text):
            hashes = ['bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712',
                      '2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613']
            return text.replace(hashes[0], 'HASH_SWAP').replace(hashes[1], hashes[0]).replace('HASH_SWAP', hashes[1])
        probe('swapped-install-hashes', 'corpus/lessons/round-19.md', swap, 'INSTALL-RECORD')
        probe('missing-install-reason', 'corpus/lessons/round-19.md',
              lambda t: t.replace('- Reason:', '- Explanation:'), 'INSTALL-RECORD')
        probe('disconnected-digest-guard', '.ufo/waves/round-18/tools/routed-defects.py',
              lambda t: t.replace('vs_ok, vs_detail = _validator_pin(root, doc)',
                                  'vs_ok, vs_detail = True, "disconnected"'), 'VALIDATOR-DIGEST')
        probe('duplicated-remap-row', W + '/evidence/validate16-remap/digests.json',
              json_change(lambda d: d['copies'].__setitem__(-1, d['copies'][0])), 'VALIDATOR-DIGEST')
        probe('FETCH_HEAD-guard-removed', '.ufo/gates/citation-drift/citation-drift-probe.py',
              lambda t: t.replace('"ORIG_HEAD", "FETCH_HEAD",', '"ORIG_HEAD",'), 'HEAD-ALIASES')
        probe('required-midmap-flag-not-forwarded', '.ufo/waves/round-17/tools/receipt-validate.py',
              lambda t: t.replace('require_mid_maps=require_mid_maps', 'require_mid_maps=False'),
              'MIDMAP-LISTSTEP')
        relative = counter(git('rev-parse', 'HEAD'), root='.')
        report = {'source_revision': source, 'pristine': pristine, 'mutants': results,
                  'relative_root': relative, 'killed': sum(r['killed'] for r in results),
                  'survived': [r['name'] for r in results if not r['killed']],
                  'scope': 'trusted lane code; mkdtemp clone is not an OS security sandbox'}
        print(json.dumps(report, indent=2))
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
