#!/usr/bin/env python3
"""Generate frozen-control receipts for R38-C1/C2 (scored with the frozen counters).

Usage:
  gen-controls.py c1-0 --root LANE --rev REV --freeze FREEZE --pkg65 PKG --out OUT
  gen-controls.py c1-1 --pkg65 PKG --out OUT
  gen-controls.py c1-2 --pkg65 PKG --out OUT
  gen-controls.py c2-0 --root LANE --rev REV --base BASE --out OUT
  gen-controls.py c2-1|c2-2|c2-3 --out OUT

Scratch under $HYAKU_SCRATCH/kaidoku-r38/controls-<kind>/ (removed on exit).
Exit: 0 if the control did NOT meet the target (expected), 1 if it did
(control meets target -> kill condition), 2 on internal errors.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
SCRATCH = os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')


def scratch_root(kind):
    d = os.path.join(SCRATCH, 'kaidoku-r38', 'controls-' + kind)
    os.makedirs(d, exist_ok=True)
    return d


def run_counter(script, args):
    r = subprocess.run(['python3', '-I', '-B', script] + args, capture_output=True, text=True)
    return r


def c1_fixture(kind, pkg65, drop='', wrong=False):
    """Mirror the c1 selftest green fixture, with one defect, in a scratch git repo."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('c1', os.path.join(HERE, 'c1-counter.py'))
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    sroot = scratch_root(kind)
    d = tempfile.mkdtemp(prefix='ctl.', dir=sroot)
    fx = os.path.join(HERE, 'selftest')
    after = json.load(open(os.path.join(fx, 'dev-after.json')))
    oracle = open(os.path.join(fx, 'dev-oracle.tsv')).read()
    sha = after['subject']['digest']['sha256']
    be_after = json.loads(json.dumps(after))
    for ch in be_after['normalized_result']['chunks']:
        ch['handler'] = c.HANDLER
    if wrong:
        for ch in be_after['normalized_result']['chunks']:
            ch['handler'] = 'squashfs_v4_le'

    def mint(env):
        p = os.path.join(d, 'mint.wrapped.json')
        json.dump({'data': env}, open(p, 'w'))
        r = subprocess.run(['node', os.path.join(HERE, '..', 'round-27', 'xpin-attribute.mjs'),
                            '--pkg65', pkg65, '--pkg67', pkg65, p], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit('xpin mint failed')
        env['evidence_id'] = r.stdout.splitlines()[0].split('\t')[2]
        return env

    be_after = mint(be_after)
    xpin = open(os.path.join(HERE, '..', 'round-27', 'xpin-attribute.mjs'), 'rb').read()
    specd = {'carriers': [{'id': k, 'sha256': sha} for k in ('K1', 'K2', 'K3', 'K4')]}
    base_files = {c.XPIN: xpin, c.CARRIERS: json.dumps(specd)}
    for k in ('K1', 'K2', 'K3', 'K4'):
        base_files[f'{c.ORADIR}/{k}/oracle.tsv'] = oracle
    good = dict(base_files)
    for k in ('K1', 'K2', 'K3', 'K4'):
        if drop == k:
            continue
        good[f'{c.AFTERDIR}/{k}/after.json'] = json.dumps(be_after)
    good.update({'PROVINCE.md': '# P\n\n## Round-38 additions to Core\n\n| x | a |\n|---|---|\n', c.ENTRY: '# E\n',
                 'corpus/SOURCES.md': '# S\n', 'corpus/README.md': '# R\n'})
    env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='f@i',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='f@i')
    for p, cc in base_files.items():
        os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
        open(os.path.join(d, p), 'wb').write(cc if isinstance(cc, bytes) else cc.encode())
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', d, 'commit', '-qm', 'freeze'], check=True, env=env)
    fz = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    for p in list(base_files):
        if p not in good:
            os.remove(os.path.join(d, p))
    for p, cc in good.items():
        os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
        open(os.path.join(d, p), 'wb').write(cc if isinstance(cc, bytes) else cc.encode())
    subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', d, 'commit', '-qm', 'data', '--allow-empty'], check=True, env=env)
    rv = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    return d, fz, rv, c


def c2_fixture(kind, defect):
    import importlib.util
    spec = importlib.util.spec_from_file_location('c2', os.path.join(HERE, 'c2-counter.py'))
    c = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(c)
    sroot = scratch_root(kind)
    d = tempfile.mkdtemp(prefix='ctl.', dir=sroot)

    def files(cov='3/3', depth='1/1', cal='2/2', box1n='1/1', craft='SKILL.md:3-5', adj='PROVINCE.md:15-17',
              cap_ptr='`docs/x.md`', drop_box=False, extra_ptr='', ptr2='`d/y.md`',
              prov_ptr='`docs/x.md`', prov_bad=''):
        sc = ('# S\n\n## Owned axes\n\n| Axis | s | o | e | r |\n|---|---|---|---|---|\n'
              f'| coverage | 10 | {cov} knowledge files mapped | `corpus/README.md` | r |\n'
              f'| depth | 10 | {depth} queue-drain rule blocks | `{craft}` | r |\n'
              f'| calibration | 10 | {cal} preselected reconciliation obligations | x | r |\n\n'
              '## Capabilities\n\n| Capability | w | e | r |\n|---|---|---|---|\n'
              f'| cap one | w | {cap_ptr} {extra_ptr} | r |\n\n## Saturation\n')
        sh = (f'# P\n\n- [~] {c.BOX1}\n  asserted `{craft}` {box1n} rule blocks\n'
              f'- [~] At least one end-to-end domain task\n  asserted {ptr2}\n')
        if not drop_box:
            sh += f'- [~] {c.BOX4} (PROVINCE.md still accurate)\n  asserted `{adj}`\n'
        prov = ('# P\n\n## Core\n\n| Surface | a | e |\n|---|---|---|\n'
                f'| REA MCP server | x | {prov_ptr} {prov_bad} |\n\n'
                '## Frontier\n\n| F | a |\n|---|---|\n| f | `docs/x.md` |\n\n## Adjacent\n\n- refuse\n\n### Sub\n')
        skill = '# K\n\n## Queue-drain craft (x)\n\n- **r1** `corpus/knowledge/2026-10-01-a.md:1-1`\n\n## Next\n'
        readme = '# R\n\n## Coverage map\n\n| `2026-10-01-a` | `2026-10-01-b` | `2026-10-01-c` |\n\n## End\n'
        res = json.dumps({'obligations': [{'status': 'aligned'}, {'status': 'aligned'}]})
        return {'SCORECARD.md': sc, 'SHONEN.md': sh, 'SKILL.md': skill, 'PROVINCE.md': prov, 'corpus/README.md': readme,
                'evidence/round-1-2026-10-15/result.json': res, 'corpus/knowledge/2026-10-01-a.md': 'a\n',
                'corpus/knowledge/2026-10-01-b.md': 'b\n', 'corpus/knowledge/2026-10-01-c.md': 'c\n',
                'docs/x.md': 'x\n', 'd/y.md': 'y\n', 'd/z/y.md': 'y\n',
                '.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt': 'd\n'}

    base = files(cov='2/2', cap_ptr='`x.md`', prov_ptr='`evidence/doctor/`')
    if defect == 'junk':
        fs = files(cov='999/999')
    elif defect == 'delete':
        fs = files(cap_ptr='')
    elif defect == 'substitute':
        fs = files(cap_ptr='`d/y.md`')
    else:
        fs = files(prov_ptr='`.ufo/waves/round-19/evidence/doctor/`')
    env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='f@i',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='f@i')
    subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
    revs = []
    for tree in (base, fs):
        for p in subprocess.run(['git', '-C', d, 'ls-files'], capture_output=True, text=True).stdout.split():
            os.remove(os.path.join(d, p))
        for p, cc in tree.items():
            os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
            open(os.path.join(d, p), 'w').write(cc)
        subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
        subprocess.run(['git', '-C', d, 'commit', '-qm', 'x', '--allow-empty'], check=True, env=env)
        revs.append(subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
    return d, revs[0], revs[1], c


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('kind')
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--base')
    ap.add_argument('--pkg65', default=PKG65)
    ap.add_argument('--out')
    a = ap.parse_args(argv)
    if not a.out:
        print('--out required', file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='f@i',
               GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='f@i')
    try:
        if a.kind == 'c1-0':
            r = run_counter(os.path.join(HERE, 'c1-counter.py'),
                            ['--root', a.root, '--rev', a.rev, '--freeze', a.freeze, '--pkg65', a.pkg65])
            res = {'control': a.kind, 'argv': sys.argv, 'exit': r.returncode}
            try:
                res['output'] = json.loads(r.stdout)
            except Exception:
                res['output_raw'] = r.stdout[:2000]
        elif a.kind in ('c1-1', 'c1-2'):
            d, fz, rv, c = c1_fixture(a.kind, a.pkg65, drop='K2' if a.kind == 'c1-1' else '', wrong=(a.kind == 'c1-2'))
            r = subprocess.run(['python3', '-I', '-B', os.path.join(HERE, 'c1-counter.py'),
                                '--root', d, '--rev', rv, '--freeze', fz, '--pkg65', a.pkg65],
                               capture_output=True, text=True)
            res = {'control': a.kind, 'argv': sys.argv, 'exit': r.returncode}
            try:
                res['output'] = json.loads(r.stdout)
            except Exception:
                res['output_raw'] = r.stdout[:2000]
            shutil.rmtree(d, ignore_errors=True)
        elif a.kind == 'c2-0':
            r = run_counter(os.path.join(HERE, 'c2-counter.py'),
                            ['--root', a.root, '--rev', a.rev, '--base', a.base])
            res = {'control': a.kind, 'argv': sys.argv, 'exit': r.returncode}
            try:
                res['output'] = json.loads(r.stdout)
            except Exception:
                res['output_raw'] = r.stdout[:2000]
        elif a.kind in ('c2-1', 'c2-2', 'c2-3'):
            d, b, rv, c = c2_fixture(a.kind, {'c2-1': 'junk', 'c2-2': 'delete', 'c2-3': 'substitute'}[a.kind])
            r = subprocess.run(['python3', '-I', '-B', os.path.join(HERE, 'c2-counter.py'),
                                '--root', d, '--rev', rv, '--base', b], capture_output=True, text=True)
            res = {'control': a.kind, 'argv': sys.argv, 'exit': r.returncode}
            try:
                res['output'] = json.loads(r.stdout)
            except Exception:
                res['output_raw'] = r.stdout[:2000]
            shutil.rmtree(d, ignore_errors=True)
        else:
            print('unknown kind', file=sys.stderr)
            return 2
    except Exception as e:
        res = {'control': a.kind, 'fatal': str(e)}
        json.dump(res, open(a.out, 'w'), indent=1, sort_keys=True)
        return 2
    json.dump(res, open(a.out, 'w'), indent=1, sort_keys=True)
    # control must NOT meet the target: counter exit != 0 is expected; exit 0 = control met target (kill condition).
    ok = res.get('exit') != 0
    print(json.dumps({'control': a.kind, 'counter_exit': res.get('exit'), 'kill': not ok}))
    return 0 if ok else 1
if __name__ == '__main__':
    sys.exit(main())
