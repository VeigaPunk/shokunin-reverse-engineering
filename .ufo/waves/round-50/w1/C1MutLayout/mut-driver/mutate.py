#!/usr/bin/env python3
"""Single-point mutation driver for the round-41 counter selftest (scratch only)."""
import concurrent.futures as cf, hashlib, json, os, shutil, subprocess, sys, time

S = '/fast/scratch/hyaku/kaidoku-r50/C1MutLayout'
ORIG = os.path.join(S, 'c1-counter.orig.py')
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
XPIN_SRC = os.path.join(S, 'mut/tools/round-27/xpin-attribute.mjs')
OUT = os.path.join(S, 'mutants')

# (id, clause, anchor-substring (must occur exactly once), replacement)
M = [
 ('M01','magic: accept hsqs as BE magic',"d['be_magic'] = raw[0:4] == b'sqsh'","d['be_magic'] = raw[0:4] in (b'sqsh', b'hsqs')"),
 ('M02','magic: no magic test',"d['be_magic'] = raw[0:4] == b'sqsh'","d['be_magic'] = True"),
 ('M03','s_major/s_minor: version test drops minor',"d['version_v4'] = (d['major'], d['minor']) == (4, 0)","d['version_v4'] = d['major'] == 4"),
 ('M04','s_minor: wrong superblock offset',"d['minor'] = int.from_bytes(raw[30:32], 'big')","d['minor'] = int.from_bytes(raw[28:30], 'big')"),
 ('M05','compression id: little-endian read',"d['compression'] = int.from_bytes(raw[20:22], 'big')","d['compression'] = int.from_bytes(raw[20:22], 'little')"),
 ('M06','compression id: XZ set widened to 3,5',"XZ_IDS = (2, 4)","XZ_IDS = (2, 3, 4, 5)"),
 ('M07','compression id: GZIP id aliased to xz 4',"GZIP_ID = 1\n","GZIP_ID = 4\n"),
 ('M08','mkfs_time==bytes_used: >= instead of ==',"d['marker'] = d['mkfs_time'] == d['bytes_used']","d['marker'] = d['mkfs_time'] >= d['bytes_used']"),
 ('M09','mkfs_time: little-endian read',"d['mkfs_time'] = int.from_bytes(raw[8:12], 'big')","d['mkfs_time'] = int.from_bytes(raw[8:12], 'little')"),
 ('M10','bytes_used sanity: admits 4 KiB past EOF',"d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)","d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw) + 4096"),
 ('M11','metadata cap widened 8192->65536',"METADATA_MAX = 8192","METADATA_MAX = 65536"),
 ('M12','length endianness: identity branch ignores BE identity',"if d['le_identity'] and not d['be_identity']:","if d['le_identity']:"),
 ('M13','length endianness: plausibility branch ignores BE plausibility',"if d['le_plausible'] and not d['be_plausible']:","if d['le_plausible']:"),
 ('M14','length endianness: uncompressed flag mask wrong',"UNCOMPRESSED_FLAG = 0x8000","UNCOMPRESSED_FLAG = 0x4000"),
 ('M15','handler name: any squashfs_v4* accepted',"d['handler_ok'] = HANDLER in chunk_handlers(env)","d['handler_ok'] = any(isinstance(h, str) and h.startswith('squashfs_v4') for h in chunk_handlers(env))"),
 ('M16','handler name: only first chunk inspected',"d['handler_ok'] = HANDLER in chunk_handlers(env)","d['handler_ok'] = HANDLER in chunk_handlers(env)[:1]"),
 ('M17','extract-root mapping: suffix match (R40-CL1 regression)',"return extract_rel(candidate, root) == strip_rel(rel)","return (extract_rel(candidate, root) or '').endswith(strip_rel(rel)) and bool(strip_rel(rel))"),
 ('M18','extract-root mapping: root prefix from first segment only',"pret = root.split('/')\n    if parts[:len(pret)] != pret:","pret = root.split('/')[:1]\n    if parts[:len(pret)] != pret:"),
 ('M19','removal disposition: entry-kind check dropped',"if entry_kind not in removal_kinds:","if False:"),
 ('M20','removal disposition: gapped-and-removed check dropped',"if gapped.get(hits[0]):","if False:"),
 ('M21','removal disposition: silent row with no detail admitted',"    if detail is None:\n        return False","    if detail is None:\n        return True"),
 ('M22','rerun projection: diagnostics key dropped from core profile',"'unpublished_entries', 'diagnostics')","'unpublished_entries')"),
 ('M23','rerun projection: verdict forced true',"d['projection_ok'] = eq","d['projection_ok'] = True"),
 ('M24','evidence id: recomputed-equality dropped',"ev[key][0] == ev[key][1]","ev[key][0] != ''"),
 ('M25','evidence id: ev_ prefix test dropped (expected equivalent)',"and ev[key][0].startswith('ev_'))","and True)"),
 ('M26','target constant 4->3',"TARGET = 4\n","TARGET = 3\n"),
 ('M27','target comparison loosened to >= target-1',"and res['carriers_matched'] == target","and res['carriers_matched'] >= target - 1"),
 ('M28','freeze walk: rename detection not disabled',"'--name-only', '--no-renames',","'--name-only',"),
 ('M29','freeze walk: nonregular table not a frozen path',"for key in ('path', 'oracle', 'nonregular'):","for key in ('path', 'oracle'):"),
 ('M30','freeze walk: range includes the freeze commit',"f'{freeze}..{rev}'","f'{freeze}^..{rev}'"),
 ('M31','freeze walk: carriers_unchanged forced true',"res['carriers_unchanged'] = cur == frozen","res['carriers_unchanged'] = True"),
 ('M32','carrier_fresh_ok: prior pins ignored',"d['carrier_fresh_ok'] = (pin is not None and pin not in prior)","d['carrier_fresh_ok'] = (pin is not None)"),
 ('M33','provenance: .. climb not refused',"return '..' not in output_directory.split('/')","return True"),
 ('M34','carve_ok: file-size equality dropped',"and carve_len == bu == size)","and carve_len == bu)"),
 ('M35','carrier_pin_ok: sha256 comparison dropped',"hashlib.sha256(raw).hexdigest() == pin)","True)"),
]

def build(mid, clause, old, new):
    src = open(ORIG, encoding='utf-8').read()
    if old is None:
        out = src
    else:
        n = src.count(old)
        if n != 1:
            return None, 'anchor count %d' % n
        out = src.replace(old, new, 1)
    d = os.path.join(OUT, mid)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, 'tools/round-41'))
    os.makedirs(os.path.join(d, 'tools/round-27'))
    shutil.copy(XPIN_SRC, os.path.join(d, 'tools/round-27/xpin-attribute.mjs'))
    p = os.path.join(d, 'tools/round-41/c1-counter.py')
    open(p, 'w', encoding='utf-8').write(out)
    return p, None

def run(mid, clause, old, new):
    p, err = build(mid, clause, old, new)
    rec = {'id': mid, 'clause': clause}
    if err:
        rec.update(status='anchor-error', detail=err)
        return rec
    mut_sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    hs = os.path.join(S, 'hs', mid)
    os.makedirs(hs, exist_ok=True)
    env = dict(os.environ, HYAKU_SCRATCH=hs, TMPDIR=hs)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, p, '--selftest', '--pkg65', PKG65],
                           capture_output=True, text=True, timeout=600, env=env,
                           cwd=os.path.dirname(p))
        code, out, errt = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        code, out, errt = 124, '', 'timeout'
    rec.update(mutant_sha256=mut_sha, exit=code, stdout_sha256=hashlib.sha256(out.encode()).hexdigest(),
               seconds=round(time.time() - t0, 1), stderr_tail=errt[-300:])
    fails = []
    try:
        js = json.loads(out.strip().splitlines()[-1])
        fails = js.get('failures', [])
        rec.update(cases=js.get('cases'), failures_n=len(fails), failures_head=[f[:220] for f in fails[:3]])
    except Exception as e:
        rec.update(parse_error=str(e)[:200], failures_head=[])
    rec['status'] = 'SURVIVED' if code == 0 else ('KILLED' if code == 1 else 'CRASH')
    if 'Traceback' in errt:
        rec['status'] = 'CRASH' if code != 1 else rec['status']
        rec['traceback_tail'] = errt[-400:]
    return rec

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    jobs = [('M00', 'control: unmutated round-41 counter', None, None)] + M
    res = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(run, *j) for j in jobs]
        for f in cf.as_completed(futs):
            res.append(f.result())
    res.sort(key=lambda r: r['id'])
    json.dump(res, open(os.path.join(S, 'mutation-results.json'), 'w'), indent=1)
    for r in res:
        print(r['id'], r.get('status'), 'exit=%s' % r.get('exit'), 'cases=%s' % r.get('cases'),
              'fails=%s' % r.get('failures_n'), r['clause'][:70])
