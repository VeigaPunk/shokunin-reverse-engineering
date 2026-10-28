#!/usr/bin/env python3
# C1RunMut driver: every scenario = fresh mkclone clone (draft tools, dev freeze), receipts committed
# in that clone (throwaway identity, clone-only), counter scored there. Scratch only.
import os, sys, json, shutil, subprocess, hashlib, importlib.util, glob

S = '/fast/scratch/hyaku/kaidoku-r49/C1RunMut'
L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
DRAFT = L + '/.ufo/waves/round-49/draft'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
BASE_EV = S + '/evid-base'
IDS = ['v1le', 'v1be', 'v2le', 'v2be']
ENV = dict(os.environ, HYAKU_SCRATCH='/fast/scratch/hyaku', TMPDIR=S + '/tmp')
os.makedirs(S + '/tmp', exist_ok=True)
LOG = open(S + '/driver.log', 'a')
RESULTS = []


def log(*a):
    print(*a, file=LOG, flush=True)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, env=env or ENV)


def toplevel_ok(d):
    top = sh(['git', '-C', d, 'rev-parse', '--show-toplevel']).stdout.decode().strip()
    assert top == d, (top, d)


# counter module (identical bytes to the draft) for CLAUSES and mint_many
spec = importlib.util.spec_from_file_location('c1c', DRAFT + '/tools/round-49/c1-counter.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
CLAUSES = list(C.CLAUSES)


def mkclone(name):
    dest = f'{S}/c/{name}'
    p = sh(['bash', DRAFT + '/mkclone.sh', dest])
    assert p.returncode == 0, p.stderr
    freeze = [l.split('=', 1)[1].strip() for l in p.stdout.decode().splitlines()
              if l.startswith('DEV_FREEZE=')][0]
    toplevel_ok(dest)
    return dest, freeze


def stage(dest, name, srcs):
    toplevel_ok(dest)
    ev = dest + '/corpus/evidence/round-49/c1'
    shutil.rmtree(ev, ignore_errors=True)
    os.makedirs(ev, exist_ok=True)
    for k in IDS:
        shutil.copytree(srcs[k], f'{ev}/{k}', symlinks=True)
    assert sh(['git', '-C', dest, 'add', '-A', '--', 'corpus/evidence/round-49/c1']).returncode == 0
    p = sh(['git', '-C', dest, 'commit', '-q', '-m', 'receipts ' + name])
    assert p.returncode == 0, p.stderr
    return sh(['git', '-C', dest, 'rev-parse', 'HEAD']).stdout.decode().strip()


def score(dest, freeze, name):
    work = f'{S}/work/{name}'
    os.makedirs(work, exist_ok=True)
    rev = sh(['git', '-C', dest, 'rev-parse', 'HEAD']).stdout.decode().strip()
    out = f'{S}/out/{name}.json'
    os.makedirs(S + '/out', exist_ok=True)
    p = sh(['python3', '-I', '-B', dest + '/tools/round-49/c1-counter.py', '--root', dest,
            '--rev', rev, '--freeze', freeze, '--pkg65', PKG, '--work', work,
            '--json-out', out], cwd=dest)
    rec = {'name': name, 'rev': rev, 'exit': p.returncode,
           'stdout_sha256': sha(p.stdout), 'stdout': p.stdout.decode()[-400:],
           'stderr_tail': p.stderr.decode()[-300:]}
    try:
        j = json.load(open(out))
    except Exception as e:  # noqa
        rec['json_error'] = str(e)
        return rec
    rec['json_sha256'] = sha(open(out, 'rb').read())
    rec['carriers_matched'] = j.get('carriers_matched')
    rec['frozen_path_changed'] = j.get('frozen_path_changed')
    rec['per_carrier_failing'] = {k: [c for c in CLAUSES if v.get(c) is not True]
                                  for k, v in (j.get('carriers') or {}).items()}
    rec['per_carrier_evidence_path'] = {k: v.get('receipt_path') for k, v in (j.get('carriers') or {}).items()}
    rec['bindings_false'] = sorted(b for b, v in (j.get('bindings') or {}).items()
                                   if v is not True and isinstance(v, bool))
    return rec


def record(rec):
    RESULTS.append(rec)
    json.dump(RESULTS, open(S + '/results.json', 'w'), indent=1, sort_keys=True)
    log(json.dumps({k: rec.get(k) for k in ('name', 'exit', 'carriers_matched',
                                             'per_carrier_failing', 'stdout_sha256')}))


def fresh(name):
    base = f'{S}/mut/{name}'
    shutil.rmtree(base, ignore_errors=True)
    srcs = {}
    for k in IDS:
        srcs[k] = f'{base}/{k}'
        shutil.copytree(f'{BASE_EV}/{k}', srcs[k], symlinks=True)
    return srcs


def evpath(d):
    return L + '/corpus/evidence/round-49/c1/' + os.path.basename(d.rstrip('/'))


def mapvals(obj, key, fn):
    if isinstance(obj, dict):
        return {k: (fn(v) if k == key else mapvals(v, key, fn)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [mapvals(v, key, fn) for v in obj]
    return obj


def remint(d, mutate_env):
    p = d + '/after.json'
    env = json.load(open(p))
    mutate_env(env)
    work = f'{S}/work/mint'
    os.makedirs(work, exist_ok=True)
    xpin = DRAFT + '/../../../../' if False else None  # placeholder unused
    m = C.mint_many(work, CLONE_XPIN[0], PKG, {'x': env})
    env['evidence_id'] = m['x']
    with open(p, 'w') as fh:
        json.dump(env, fh, sort_keys=True, indent=2, ensure_ascii=False)
        fh.write('\n')


CLONE_XPIN = [None]
REPLAY_SRC = '''import os, sys, shutil
argv = sys.argv[1:]
fixture, outdir = argv[-2], argv[-1]
cid = {'v1-le--squashfs_v1.0_le.bin': 'v1le', 'v1-be--squashfs_v1.0_be.bin': 'v1be',
       'v2-le--squashfs_v2.0_le.bin': 'v2le', 'v2-be--squashfs_v2.0_be.bin': 'v2be'}[os.path.basename(fixture)]
src = '/fast/scratch/hyaku/kaidoku-r49/C1RunMut/evid-base/' + cid
os.makedirs(outdir, exist_ok=True)
shutil.copytree(src + '/firmware.bin_extract', os.path.join(outdir, 'firmware.bin_extract'), symlinks=True)
sys.stdout.buffer.write(open(src + '/stdout.log', 'rb').read())
'''


def set_outdir(path_of):
    def f(d, env_fn=None):
        pass
    return f


# ---------------- mutations on the verbatim-copied evidence tree -----------------
def m_drop_prov(d):
    os.remove(d + '/provenance.json')


def m_prov_lie(d):
    doc = json.load(open(d + '/provenance.json'))
    doc = mapvals(doc, 'output_directory', lambda v: evpath(d) if isinstance(v, str) else v)
    json.dump(doc, open(d + '/provenance.json', 'w'), sort_keys=True, indent=2)


def m_rev_wrong(d):
    doc = json.load(open(d + '/run.json'))
    doc = mapvals(doc, 'rev_at_run', lambda v: '0' * 40)
    json.dump(doc, open(d + '/run.json', 'w'), sort_keys=True, indent=2)


def m_drop_run(d):
    os.remove(d + '/run.json')


def m_tamper_tree(d):
    files = sorted(p for p in glob.glob(d + '/firmware.bin_extract/**/*', recursive=True)
                   if os.path.isfile(p) and not os.path.islink(p))
    f = files[0]
    b = bytearray(open(f, 'rb').read())
    b[0] ^= 0x01
    open(f, 'wb').write(bytes(b))


def m_rm_tree(d):
    shutil.rmtree(d + '/firmware.bin_extract')


def m_drop_env_log(d):
    os.remove(d + '/extract-env.json')
    os.remove(d + '/unblob.log')


def m_tamper_envelope_and_stdout(d):
    for n in ('envelope.json', 'stdout.log'):
        open(d + '/' + n, 'ab').write(b'\n')


def m_after_outdir(target):
    # target: 'evidence' | 'forged_scratch' | 'tmp_string' ; re-minted
    def f(d, reminted=True):
        pass
    return f


def after_set_outdir(d, value_fn, reminted):
    def mut(env):
        env['parameters']['output_directory'] = value_fn(os.path.basename(d.rstrip('/')))
    if reminted:
        remint(d, mut)
    else:
        p = d + '/after.json'
        env = json.load(open(p))
        mut(env)
        json.dump(env, open(p, 'w'), sort_keys=True, indent=2, ensure_ascii=False)


def m_outdir_evidence_remint(d):
    after_set_outdir(d, lambda cid: L + '/corpus/evidence/round-49/c1/' + cid, True)


def m_outdir_evidence_noremint(d):
    after_set_outdir(d, lambda cid: L + '/corpus/evidence/round-49/c1/' + cid, False)


def m_outdir_forged_scratch_remint(d):
    after_set_outdir(d, lambda cid: '/fast/scratch/hyaku/kaidoku-r49/forged/' + cid + '/rea-out', True)


def m_outdir_nonscratch_segment_remint(d):
    # the segment check is a substring test; the prefix is never checked
    after_set_outdir(d, lambda cid: '/tmp/c1-forged/kaidoku-r49/' + cid + '/rea-out', True)


def m_content_forged_remint(d):
    def mut(env):
        env['normalized_result']['files'][0]['sha256'] = 'f' * 64
    remint(d, mut)


# ---------------- scenarios -----------------
def run_runner(name, lane, carriers, extra, py=None, env_extra=None):
    ev = f'{S}/runs/{name}/ev'
    scr = f'{S}/runs/{name}/scr'
    os.makedirs(scr, exist_ok=True)
    cmd = ['bash', CLONE0 + '/tools/round-49/c1-run.sh', '--lane-root', lane,
           '--carriers', carriers, '--freeze', FREEZE0, '--evidence-root', ev,
           '--scratch', scr] + extra
    env = dict(ENV)
    if py:
        env['C1_RUN_PY'] = py
    env.update(env_extra or {})
    p = sh(cmd, cwd=S, env=env)
    log(f'runner {name} exit {p.returncode}')
    return ({k: f'{ev}/{k}' for k in IDS},
            {'name': name, 'runner_exit': p.returncode,
             'runner_stdout_sha256': sha(p.stdout),
             'runner_stderr_tail': p.stderr.decode()[-300:]})


def scenario(name, srcs_fn, pre=None, runner_info=None, lane_clone=None):
    dest, freeze = mkclone(name)
    srcs = srcs_fn
    rev = stage(dest, name, srcs)
    rec = score(dest, freeze, name)
    rec['freeze'] = freeze
    rec['receipt_commit'] = rev
    if runner_info:
        rec.update(runner_info)
    record(rec)


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    CLONE0 = S + '/clone0'
    FREEZE0 = sh(['git', '-C', CLONE0, 'rev-parse', 'HEAD']).stdout.decode().strip()
    CLONE_XPIN[0] = CLONE0 + '/tools/round-27/xpin-attribute.mjs'
    # mint self-check: re-minting the untouched baseline must reproduce its stored id
    base_env = json.load(open(BASE_EV + '/v1le/after.json'))
    chk = C.mint_many(S + '/work/mint', CLONE_XPIN[0], PKG, {'x': dict(base_env)})['x']
    log('mint self-check stored=%s reminted=%s equal=%s' % (
        base_env.get('evidence_id'), chk, chk == base_env.get('evidence_id')))
    RESULTS.append({'name': 'mint_selfcheck', 'stored': base_env.get('evidence_id'),
                    'reminted': chk, 'equal': chk == base_env.get('evidence_id')})

    # 0 baseline
    scenario('BASE', {k: f'{BASE_EV}/{k}' for k in IDS})

    # --- real runner options and code
    for nm, extra, py in [
        ('S1_rea_outdir_evidence', ['--rea-outdir-mode', 'evidence'], None),
        ('S2_scratch_base_named_kaidoku-r44', ['--scratch', S + '/runs/S2/kaidoku-r44'], None),
    ]:
        pass  # runner invoked below through run_runner (needs fresh freeze lane)

    # S1 / S2 / S3 / S5 need runner runs; their lanes are CLONE0 (dev freeze) and a base clone for S4.
    r1, i1 = run_runner('S1_rea_outdir_evidence', CLONE0, CLONE0 + '/tools/round-49/carriers.json',
                        ['--rea-outdir-mode', 'evidence'])
    scenario('S1_rea_outdir_evidence', r1, runner_info=i1)

    r2, i2 = run_runner('S2_scratch_base_named_kaidoku-r44', CLONE0,
                        CLONE0 + '/tools/round-49/carriers.json', ['--scratch', S + '/runs/S2/kaidoku-r44'])
    # the scratch base is a directory named kaidoku-r44 (the runner appends kaidoku-r49)
    scenario('S2_scratch_base_named_kaidoku-r44', r2, runner_info=i2)

    seg = open(CLONE0 + '/tools/round-49/c1-run.py').read()
    assert seg.count("ROUND_SEGMENT = 'kaidoku-r49'") == 1
    open(S + '/mut/c1-run-seg44.py', 'w').write(seg.replace("ROUND_SEGMENT = 'kaidoku-r49'",
                                                            "ROUND_SEGMENT = 'kaidoku-r44'"))
    r3, i3 = run_runner('S3_segment_code_kaidoku-r44', CLONE0,
                        CLONE0 + '/tools/round-49/carriers.json', [],
                        py=S + '/mut/c1-run-seg44.py')
    scenario('S3_segment_code_kaidoku-r44', r3, runner_info=i3)

    # S4: runner run at a PRE-FREEZE lane (base e4f2 checkout), receipts committed after the freeze
    cb = S + '/clone-base'
    shutil.rmtree(cb, ignore_errors=True)
    sh(['git', 'clone', '-q', '--shared', L, cb])
    toplevel_ok(cb)
    assert sh(['git', '-C', cb, 'checkout', '-q', '--detach',
               'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9']).returncode == 0
    r4, i4 = run_runner('S4_prefreeze_lane_rev_at_run', cb, CLONE0 + '/tools/round-49/carriers.json', [])
    scenario('S4_prefreeze_lane_rev_at_run', r4, runner_info=i4)

    # S5: REA replaced by a replay of an earlier real run's saved stdout and tree (no REA run)
    open(S + '/mut/replay.py', 'w').write(REPLAY_SRC)
    r5, i5 = run_runner('S5_replay_fake_rea', CLONE0, CLONE0 + '/tools/round-49/carriers.json',
                        ['--fake-rea', 'python3 -I -B ' + S + '/mut/replay.py'],
                        env_extra={})
    scenario('S5_replay_fake_rea', r5, runner_info=i5)

    # ----- post-run artifact mutations (the counter reads after.json only)
    muts = [
        ('P1_drop_provenance_json', m_drop_prov),
        ('P2_provenance_lies_evidence_path', m_prov_lie),
        ('P3_run_json_rev_at_run_zeros', m_rev_wrong),
        ('P4_drop_run_json', m_drop_run),
        ('P5_tamper_verbatim_tree_byte', m_tamper_tree),
        ('P6_remove_verbatim_tree', m_rm_tree),
        ('P7_drop_extract_env_and_unblob_log', m_drop_env_log),
        ('P8_tamper_envelope_and_stdout', m_tamper_envelope_and_stdout),
        ('P9_outdir_evidence_path_remint', m_outdir_evidence_remint),
        ('P10_outdir_evidence_path_no_remint', m_outdir_evidence_noremint),
        ('P11_outdir_forged_scratch_remint', m_outdir_forged_scratch_remint),
        ('P12_outdir_tmp_string_segment_remint', m_outdir_nonscratch_segment_remint),
        ('P13_content_forged_remint', m_content_forged_remint),
    ]
    for nm, fn in muts:
        srcs = fresh(nm)
        for k in IDS:
            fn(srcs[k]) if nm != 'P13_content_forged_remint' else None
        if nm == 'P13_content_forged_remint':
            fn(srcs['v1le'])
        scenario(nm, srcs)
    log('DONE')
