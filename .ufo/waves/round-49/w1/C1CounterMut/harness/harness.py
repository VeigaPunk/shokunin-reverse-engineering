import os, sys, re, json, shutil, subprocess, hashlib, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutants
S = '/fast/scratch/hyaku/kaidoku-r49/C1CounterMut'
BASE = S + '/base'
PKG = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
PRISTINE = open(BASE + '/tools/round-49/c1-counter.py', encoding='utf-8').read()
PRIST_SHA = hashlib.sha256(PRISTINE.encode()).hexdigest()
CLAUSES_NAMES = ['carrier_present', 'carrier_pin_ok', 'carrier_size_ok', 'carrier_fresh_ok', 'layout_ok', 'carve_ok', 'oracle_ok', 'tree_ok', 'receipt_present', 'receipt_fresh', 'evidence_envelope_ok', 'subject_pin_ok', 'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok', 'gaps_ok', 'nonregular_unpublished_ok', 'path_shape_ok', 'run_provenance_ok', 'evidence_id_ok', 'projection_ok']

def clause_drop(name):
    m = re.search(r"^CLAUSES = \((.*?)\)\n", PRISTINE, re.S | re.M)
    block = m.group(0)
    q = "'%s'" % name
    assert block.count(q) == 1, (name, block.count(q))
    nb, k = re.subn(r"'%s',\s*" % name, '', block, count=1)
    if k == 0:
        nb, k = re.subn(r",\s*'%s'" % name, '', block, count=1)
    assert k == 1 and nb != block, name
    return [(block, nb, 1)]

def build_jobs():
    jobs = []
    for n in CLAUSES_NAMES:
        jobs.append(('D-' + n, 'CLAUSES drop: remove %s from the per-carrier conjunction' % n, clause_drop(n)))
    for id_, desc, edits in mutants.M:
        jobs.append((id_, desc, edits))
    return jobs

def apply(text, edits):
    out = text
    for old, new, cnt in edits:
        c = out.count(old)
        if c != cnt:
            return None, 'pattern count %d != %d for %r' % (c, cnt, old[:70])
        out = out.replace(old, new)
    return out, None

def sha(b):
    return hashlib.sha256(b).hexdigest()

def run_one(job):
    id_, desc, edits = job
    wd = S + '/mut/' + id_
    shutil.rmtree(wd, ignore_errors=True)
    os.makedirs(wd + '/tools/round-49'); os.makedirs(wd + '/tools/round-27')
    shutil.copy(BASE + '/tools/round-27/xpin-attribute.mjs', wd + '/tools/round-27/')
    text, err = apply(PRISTINE, edits)
    rec = {'id': id_, 'desc': desc}
    if text is None:
        rec.update(verdict='PATTERN-MISS', detail=err)
        return rec
    path = wd + '/tools/round-49/c1-counter.py'
    open(path, 'w', encoding='utf-8').write(text)
    rec['mutant_sha256'] = sha(text.encode())
    rec['mutant_bytes_differ'] = text != PRISTINE
    try:
        compile(text, path, 'exec')
    except SyntaxError as e:
        rec.update(verdict='SYNTAX', detail=str(e)); return rec
    work = wd + '/work'; os.makedirs(work)
    env = dict(os.environ, C1_SELFTEST_DETAIL='1', TMPDIR=wd, HYAKU_SCRATCH='/fast/scratch/hyaku')
    t0 = time.time()
    p = subprocess.run(['python3', '-I', '-B', path, '--selftest', '--pkg65', PKG, '--work', work],
                       capture_output=True, env=env, timeout=900)
    rec['wall_s'] = round(time.time() - t0, 1)
    out = p.stdout.decode(errors='replace'); errs = p.stderr.decode(errors='replace')
    rec['exit'] = p.returncode
    rec['stdout_sha256'] = sha(p.stdout)
    rec['stderr_sha256'] = sha(p.stderr)
    js = None
    for line in out.splitlines():
        if line.startswith('{') and '"selftest"' in line:
            js = json.loads(line)
    if js is None:
        tb = [l for l in errs.splitlines() if l.strip()]
        rec.update(verdict='CRASH', detail=(tb[-1] if tb else 'no output'))
    elif p.returncode == 0:
        rec.update(verdict='SURVIVED', detail='selftest green: %d cases, failures=%r' % (js['cases'], js['failures']))
    else:
        rec.update(verdict='KILLED', detail='%d failure(s): %s' % (len(js['failures']), '; '.join(js['failures'])[:600]))
    shutil.rmtree(work, ignore_errors=True)
    rec['_dir'] = wd
    return rec

if __name__ == '__main__':
    assert sha(PRISTINE.encode()) == 'd6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779'
    jobs = build_jobs()
    only = set(sys.argv[1:])
    if only: jobs = [j for j in jobs if j[0] in only]
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(run_one, jobs))
    json.dump(res, open(S + '/mut-results.json', 'w'), indent=1)
    for r in res:
        print(r['id'], r['verdict'], r.get('exit'), (r.get('detail') or '')[:150])
