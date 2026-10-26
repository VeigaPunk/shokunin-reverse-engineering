#!/usr/bin/env python3
"""R41C1Mutants case verification: insert the 11 proposed selftest cases into
(a) the pristine prototype counter and (b) each surviving mutant, run
--selftest on each, and record whether the new cases kill the mutant while
staying consistent on the pristine counter."""
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

S = '/fast/scratch/hyaku/kaidoku-r41/R41C1Mutants'
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
SRC = open(os.path.join(S, 'lane', 'tools', 'round-40', 'c1-counter.py'), 'rb').read().decode()
XPIN_SRC = open(os.path.join(S, 'lane', 'tools', 'round-27', 'xpin-attribute.mjs'), 'rb').read()
ANCHOR = "    # ---- freeze integrity\n"

CASES = '''    # ---- R41C1Mutants verification block: cases that kill the surviving mutants
    def raw_pub(e, rel, h, size=5):
        e['normalized_result']['files'].append({
            'relative_path': rel, 'path': '/x/' + rel, 'size': size, 'sha256': h})

    nested_file, nested_recs = build(
        env_over={'V2': lambda e: pub(e, 'core_extract/usr/bin/tool', fsha(11))},
        oracle_over={'V2': oracle_rows([('core_extract/usr/bin/tool', fsha(11), 5)])})
    add('nested extract root keeps the components after the first root',
        [nested_file, nested_recs], 0, 0, runner=same_run(nested_recs))
    m02_file, m02_recs = build(
        env_over={'V2': lambda e: [f.__setitem__('relative_path',
                                                  'carrier.out/var/info.txt')
                                   for f in e['normalized_result']['files']]})
    add('chunk dir without the _extract suffix does not resolve to the oracle row',
        [m02_file, m02_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(m02_recs))
    m03_file, m03_recs = build(
        env_over={'V2': lambda e: e['normalized_result']['files'][0].__setitem__(
            'relative_path', '$output/firmware.bin_extract/var/info.txt')})
    add('the $output prefix is stripped before the chunk extract root',
        [m03_file, m03_recs], 0, 0, runner=same_run(m03_recs))
    def m04_env(e):
        raw_pub(e, 'var/old_extract/link', fsha(12))
        entry(e, 'var/old_extract/link')
    m04_file, m04_recs = build(env_over={'V2': m04_env},
                               nonreg_over={'V2': 'var/old_extract/link\\tsymlink\\n'})
    add('a mid-path _extract component is not an extract root',
        [m04_file, m04_recs], 0, 1, want_fail='nonregular_unpublished_ok',
        runner=same_run(m04_recs))
    m05_file, m05_recs = build(
        env_over={'V2': lambda e: raw_pub(e, 'core_extract/tool.bin', fsha(13))},
        oracle_over={'V2': oracle_rows([('core_extract/tool.bin', fsha(13), 5)])})
    add('receipt path without the chunk extract root does not satisfy the oracle row',
        [m05_file, m05_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(m05_recs))
    m09_file, m09_recs = build(
        env_over={'V2': lambda e: e['normalized_result']['files'].append(
            dict(e['normalized_result']['files'][0]))})
    add('duplicate published row still satisfies the oracle row once',
        [m09_file, m09_recs], 0, 0, runner=same_run(m09_recs))
    m11_file, m11_recs = build(
        env_over={'L2': lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/dev/console',
            'path': '/x/dev/console', 'size': 3, 'sha256': fsha(14)})})
    add('regular file at the device entry path is a materialised entry',
        [m11_file, m11_recs], 0, 1, want_fail='nonregular_unpublished_ok',
        runner=same_run(m11_recs, 'L2'))
    def m15_env(e):
        e['normalized_result']['extraction_gaps'].append({
            'kind': 'unpublished-entry', 'handler': HANDLER,
            'relative_path': 'firmware.bin_extract/var/extra',
            'dependencies': []})
    m15_file, m15_recs = build(env_over={'V2': m15_env},
                               nonreg_over={'V2': 'var/extra\\tsymlink\\n'
                                            'var/extra\\tdevice\\n'})
    add('same path listed with two non-regular kinds resolves to no single entry',
        [m15_file, m15_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(m15_recs))
    m17_file, m17_recs = build(
        env_over={'L1': lambda e: e['normalized_result']['chunks'][0].__setitem__(
            'handler', 'xsquashfs_v4_be')})
    add('chunk handler matching is exact, not a substring test',
        [m17_file, m17_recs], 0, 1, want_fail='handler_ok',
        runner=same_run(m17_recs, 'L1'))
    m20_frozen, m20_recs = build()
    m20_forged = json.loads(m20_recs[receipt_path('L2')])
    m20_forged['evidence_id'] = m20_forged['evidence_id'][:24] + '0' * 40
    add('evidence id differing only after char 24 is stale',
        [m20_frozen, {**m20_recs, receipt_path('L2'): json.dumps(m20_forged)}],
        0, 1, want_fail='evidence_id_ok')
    v41 = bytearray(sb_carrier(GZIP_ID, b'V1-v41'))
    v41[30:32] = (1).to_bytes(2, 'big')
    add('superblock version 4.1 is not the AVM v4.0 layout',
        build(blob_over={'V1': bytes(v41)}), 0, 1, want_fail='layout_ok')
'''

SURVIVORS = ['M01-extract-rel-strip-all-leading', 'M02-extract-rel-strip-unconditional',
             'M03-extract-rel-keep-output-prefix', 'M04-extract-rel-strip-anywhere',
             'M05-same-rel-raw-equality-escape', 'M09-oracle-hits-count-files',
             'M11-nonreg-published-symlink-only', 'M15-gap-path-multi-ok',
             'M17-handler-substring', 'M20-evidence-id-truncated',
             'M31-layout-drop-version']
NEW_CASES = ('nested extract root keeps the components after the first root',
             'chunk dir without the _extract suffix does not resolve to the oracle row',
             'the $output prefix is stripped before the chunk extract root',
             'a mid-path _extract component is not an extract root',
             'receipt path without the chunk extract root does not satisfy the oracle row',
             'duplicate published row still satisfies the oracle row once',
             'regular file at the device entry path is a materialised entry',
             'same path listed with two non-regular kinds resolves to no single entry',
             'chunk handler matching is exact, not a substring test',
             'evidence id differing only after char 24 is stale',
             'superblock version 4.1 is not the AVM v4.0 layout')
CASE_FOR = dict(zip(SURVIVORS, NEW_CASES))


def prepare(name, source):
    assert SRC.count(ANCHOR) == 1
    assert source.count(ANCHOR) == 1, name
    text = source.replace(ANCHOR, CASES + ANCHOR)
    d = os.path.join(S, 'verify', name)
    os.makedirs(os.path.join(d, 'tools', 'round-27'), exist_ok=True)
    with open(os.path.join(d, 'c1-counter.py'), 'w') as fh:
        fh.write(text)
    with open(os.path.join(d, 'tools', 'round-27', 'xpin-attribute.mjs'), 'wb') as fh:
        fh.write(XPIN_SRC)
    return d


def run(name, d):
    env = dict(os.environ)
    env['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
    env['TMPDIR'] = S
    env['C1_SELFTEST_DETAIL'] = '1'
    p = subprocess.run(['python3', os.path.join(d, 'c1-counter.py'), '--selftest',
                        '--pkg65', PKG65],
                       capture_output=True, text=True, env=env, cwd=d, timeout=900)
    js = {}
    for line in p.stdout.strip().splitlines():
        if line.startswith('{'):
            try:
                js = json.loads(line)
            except json.JSONDecodeError:
                pass
    fails = js.get('failures') or []
    return {'name': name, 'exit': p.returncode, 'cases': js.get('cases'),
            'failures': fails}


def main():
    targets = {'pristine': SRC}
    for m in SURVIVORS:
        targets[m] = open(os.path.join(S, 'mutants', m, 'c1-counter.py')).read()
    dirs = {n: prepare(n, s) for n, s in targets.items()}
    with ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(lambda kv: run(kv[0], dirs[kv[0]]), sorted(dirs.items())))
    res.sort(key=lambda r: (r['name'] != 'pristine', r['name']))
    out = []
    for r in res:
        if r['name'] == 'pristine':
            out.append({'name': r['name'], 'exit': r['exit'], 'cases': r['cases'],
                        'failures': r['failures'],
                        'ok': r['exit'] == 0 and not r['failures']})
            continue
        new_fail = [f for f in r['failures']
                    if f.startswith(CASE_FOR[r['name']])]
        out.append({'name': r['name'], 'exit': r['exit'], 'cases': r['cases'],
                    'failures': r['failures'], 'new_case_failed': new_fail,
                    'killed_by_new_case': bool(new_fail),
                    'only_new_case_failed': len(r['failures']) == 1 and bool(new_fail)})
    with open(os.path.join(S, 'verify-results.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
