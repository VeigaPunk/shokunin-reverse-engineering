#!/usr/bin/env python3
"""QUALITY 84 pre-freeze dry run of the frozen C1 counter on FOUR DEVELOPMENT carriers of
the frozen shape (2 standard v3 OpenWrt 7.09, 2 DD-WRT ddwrt-variant), L1 KaidokuR42.
Runs the real fetch tool, oracle arm, after arm (REA) and counter in a sandbox clone."""
import hashlib, json, os, shutil, subprocess, sys
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r42/l1-dry/c1'
shutil.rmtree(S, ignore_errors=True)
os.makedirs(S + '/tmp')
env = dict(os.environ, TMPDIR=S + '/tmp')
D = S + '/lane'
def run(*a, **k):
    print('+', ' '.join(a)[:200], flush=True)
    return subprocess.run(list(a), env=env, **k)
def git(*a):
    return subprocess.run(['git', '-C', D, *a], capture_output=True, text=True, check=True).stdout.strip()
run('git', 'clone', '-q', '--shared', LANE, D, check=True)
assert git('rev-parse', '--show-toplevel') == D
for p in ('SKILL.md', 'plans/round-42-claims.md', 'tools/round-42', '.ufo/waves/round-42/c1/gap-rule.json'):
    src, dst = os.path.join(LANE, p), os.path.join(D, p)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
DEV = [
    ('DEV-OWATH', 'https://archive.openwrt.org/kamikaze/7.09/atheros-2.6/openwrt-atheros-2.6-root.squashfs', 0, 999424, 'squashfs_v3', 'sqsh', 'be', 'standard'),
    ('DEV-OWX86', 'https://archive.openwrt.org/kamikaze/7.09/x86-2.6/openwrt-x86-2.6-squashfs.image', 4677120, 786432, 'squashfs_v3', 'hsqs', 'le', 'standard'),
    ('DEV-DWMINI', 'https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Broadcom/Linksys/WRT54GL_1.0/dd-wrt.v24_mini_generic.bin', 923872, 2918624 - 923872, 'squashfs_v3_ddwrt', 'hsqt', 'le', 'ddwrt'),
    ('DEV-DWLS2', 'https://download1.dd-wrt.com/dd-wrtv2/downloads/v24/Atheros%20WiSoc/Ubiquiti%20Litestation%202/LS2.dd-wrt.bin', 852292, 3645764 - 852292, 'squashfs_v3_ddwrt', 'tqsh', 'be', 'ddwrt'),
]
img = S + '/img'; os.makedirs(img)
frozen = json.load(open(LANE + '/.ufo/waves/round-42/c1/carriers.json'))
spec = {'claim': 'R42-C1', 'target': 4, 'toolchain': frozen['toolchain'], 'carriers': []}
fspec = {'claim': 'R42-C1', 'target': 4, 'carriers': []}
tsha = hashlib.sha256(open(D + '/tools/round-42/fetch-carrier.py', 'rb').read()).hexdigest()
for cid, url, off, ln, h, mg, en, var in DEV:
    path = f'{img}/{cid}.img'
    r = subprocess.run(['curl', '-sS', '-o', path, '-w', '%{http_code} %{url_effective} %{num_redirects}', url], capture_output=True, text=True)
    code, eff, nred = r.stdout.split()
    data = open(path, 'rb').read()
    carve = data[off:off + ln]
    csha = hashlib.sha256(carve).hexdigest(); isha = hashlib.sha256(data).hexdigest()
    open(f'{img}/{cid}.carve', 'wb').write(carve)
    rel = f'.ufo/waves/round-42/c1/fetch-{cid}.json'
    spec['carriers'].append({'id': cid, 'kind': 'published', 'source_id': 'S131', 'sha256': csha, 'handler': h,
        'superblock': {'magic': mg, 'endianness': en, 'major': 3, 'minor': 0, 'variant': var, 'compression': 'lzma'},
        'fetch_receipt': rel,
        'external': {'url': url, 'image_sha256': isha, 'member': '(whole image)', 'member_sha256': isha, 'length': ln, 'offset': off},
        'oracle': f'corpus/evidence/round-42/c1/{cid}/oracle.tsv', 'nonregular': f'corpus/evidence/round-42/c1/{cid}/nonregular.tsv'})
    fspec['carriers'].append({'id': cid, 'url': url, 'image_sha256': isha, 'carve': {'offset': off, 'bytes_used': ln, 'sha256': csha}})
    os.makedirs(os.path.dirname(D + '/' + rel), exist_ok=True)
    json.dump({'url': url, 'final_url': eff, 'http_status': int(code), 'redirects': int(nred), 'content_length': len(data),
               'image_sha256': isha, 'member': '(whole image)', 'member_sha256': isha, 'offset': off, 'carve_len': ln, 'pin': csha,
               'tool_sha256': tsha}, open(D + '/' + rel, 'w'), indent=1)
    out = f'{D}/corpus/evidence/round-42/c1/{cid}'
    os.makedirs(out, exist_ok=True)
    rc = run('bash', D + '/tools/round-42/c1-run.sh', 'oracle', f'{img}/{cid}.carve', out, f'{S}/or-{cid}').returncode
    print(cid, 'oracle rc', rc, flush=True)
json.dump(spec, open(D + '/.ufo/waves/round-42/c1/carriers.json', 'w'), indent=1)
json.dump(fspec, open(D + '/.ufo/waves/round-42/c1/fetch-spec.json', 'w'), indent=1)
git('add', '-A'); git('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q', '-m', 'fx c1 freeze-like')
F = git('rev-parse', 'HEAD'); print('freeze-like', F, flush=True)
cache = S + '/cache'; os.makedirs(cache)
run('python3', '-I', '-B', D + '/tools/round-42/fetch-carrier.py', '--spec', D + '/.ufo/waves/round-42/c1/fetch-spec.json', '--cache', cache, '--work', S + '/tmp', '--json-out', S + '/fetch.json')
for cid, *_ in DEV:
    c = next(x for x in spec['carriers'] if x['id'] == cid)
    out = f'{D}/corpus/evidence/round-42/c1/{cid}'
    rc = run('bash', D + '/tools/round-42/c1-run.sh', 'after', f"{cache}/{c['sha256']}.bin", out, f'{S}/after-{cid}').returncode
    print(cid, 'after rc', rc, flush=True)
git('add', '-A'); git('-c', 'user.name=fx', '-c', 'user.email=fx@fx', 'commit', '-q', '-m', 'fx c1 data')
R = git('rev-parse', 'HEAD')
r = run('python3', '-I', '-B', D + '/tools/round-42/c1-counter.py', '--root', D, '--rev', R, '--freeze', F,
        '--pkg65', '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents', '--carrier-cache', cache,
        '--work', S + '/work', '--json-out', S + '/c1-dry.json')
print('counter rc', r.returncode, flush=True)
os.makedirs(LANE + '/.ufo/waves/round-42/l1', exist_ok=True)
shutil.copy(S + '/c1-dry.json', LANE + '/.ufo/waves/round-42/l1/dryrun-c1.json')
