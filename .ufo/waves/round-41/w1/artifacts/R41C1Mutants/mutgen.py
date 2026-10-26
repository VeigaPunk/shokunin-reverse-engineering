#!/usr/bin/env python3
"""R41C1Mutants: single-logic mutation testing of the exact-match prototype
applied to tools/round-40/c1-counter.py at lane base 49096c7e.

Sandbox clone: /fast/scratch/hyaku/kaidoku-r41/R41C1Mutants/lane (prototype
applied and committed as afd72359; the lane repo itself is never touched).
Each mutant is a full copy of the patched counter with exactly one logic
replacement (asserted single occurrence), run with --selftest.
"""
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

S = '/fast/scratch/hyaku/kaidoku-r41/R41C1Mutants'
LANE = os.path.join(S, 'lane')
PATCHED = os.path.join(LANE, 'tools', 'round-40', 'c1-counter.py')
XPIN = os.path.join(LANE, 'tools', 'round-27', 'xpin-attribute.mjs')
PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'

SRC = open(PATCHED, 'rb').read().decode()
XPIN_SRC = open(XPIN, 'rb').read()

# name -> (old, new); each must occur exactly once in the patched source.
MUTANTS = {
    # ---- exact-path matcher / extract-root derivation
    'M01-extract-rel-strip-all-leading': (
        "    if parts and parts[0].endswith('_extract'):\n        parts = parts[1:]",
        "    while parts and parts[0].endswith('_extract'):\n        parts = parts[1:]"),
    'M02-extract-rel-strip-unconditional': (
        "    if parts and parts[0].endswith('_extract'):\n        parts = parts[1:]",
        "    if parts and len(parts) > 1:\n        parts = parts[1:]"),
    'M03-extract-rel-keep-output-prefix': (
        "    p = path\n    while p.startswith('$output/'):\n        p = p[len('$output/'):]\n    parts",
        "    p = path\n    parts"),
    'M04-extract-rel-strip-anywhere': (
        "    if parts and parts[0].endswith('_extract'):\n        parts = parts[1:]",
        "    for _i, _x in enumerate(parts):\n        if _x.endswith('_extract'):\n"
        "            parts = parts[:_i] + parts[_i + 1:]\n            break"),
    'M05-same-rel-raw-equality-escape': (
        "    return bool(rel) and bool(candidate) and extract_rel(candidate) == rel",
        "    return bool(rel) and bool(candidate) and (extract_rel(candidate) == rel\n"
        "                                             or candidate == rel)"),
    # ---- oracle hit set equality
    'M07-oracle-hits-ge1': (
        "                d['oracle_hits_ok'] = (d['oracle_ok']\n"
        "                                       and d['oracle_hits'] == d['oracle_files'])",
        "                d['oracle_hits_ok'] = (d['oracle_ok']\n"
        "                                       and d['oracle_hits'] >= 1)"),
    'M08-oracle-hits-sha-only': (
        "        if any(sha == fs and same_rel(fp, rel) for fp, fs, _ in files):",
        "        if any(sha == fs for fp, fs, _ in files):"),
    'M09-oracle-hits-count-files': (
        "    for rel, sha in oracle:\n"
        "        if any(sha == fs and same_rel(fp, rel) for fp, fs, _ in files):\n"
        "            hits += 1",
        "    for rel, sha in oracle:\n"
        "        hits += sum(1 for fp, fs, _ in files\n"
        "                    if sha == fs and same_rel(fp, rel))"),
    'M10-oracle-hits-drop-oracle-ok': (
        "                d['oracle_hits_ok'] = (d['oracle_ok']\n"
        "                                       and d['oracle_hits'] == d['oracle_files'])",
        "                d['oracle_hits_ok'] = d['oracle_hits'] == d['oracle_files']"),
    # ---- non-regular unpublished
    'M11-nonreg-published-symlink-only': (
        "            if same_rel(fp, rel):\n                hits.append(fp)",
        "            if same_rel(fp, rel) and _kind == 'symlink':\n                hits.append(fp)"),
    'M12-nonreg-unpublished-dropped': (
        "                d['nonregular_unpublished_ok'] = not esc",
        "                d['nonregular_unpublished_ok'] = True"),
    # ---- gap rule counts
    'M13-gap-required-dropped': (
        "        need = required.get(kind, bool(allowed.get(kind)))",
        "        need = False"),
    'M14-gap-structural-ge': (
        "            if n > structural[k]}",
        "            if n >= structural[k]}"),
    'M15-gap-path-multi-ok': (
        "        if len(hits) != 1:",
        "        if len(hits) < 1:"),
    'M16-gap-allowance-ignored': (
        "        if kind not in allowed.get(entry_kind, []):",
        "        if False:"),
    # ---- handler
    'M17-handler-substring': (
        "                d['handler_ok'] = HANDLER in chunk_handlers(env)",
        "                d['handler_ok'] = any(isinstance(h, str) and HANDLER in h\n"
        "                                      for h in chunk_handlers(env))"),
    'M18-handler-any-chunk': (
        "                d['handler_ok'] = HANDLER in chunk_handlers(env)",
        "                d['handler_ok'] = bool(chunk_handlers(env))"),
    # ---- evidence id
    'M19-evidence-id-prefix-only': (
        "            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]\n"
        "                                   and ev[key][0].startswith('ev_'))",
        "            d['evidence_id_ok'] = (key in ev\n"
        "                                   and ev[key][0].startswith('ev_'))"),
    'M20-evidence-id-truncated': (
        "            d['evidence_id_ok'] = (key in ev and ev[key][0] == ev[key][1]\n"
        "                                   and ev[key][0].startswith('ev_'))",
        "            d['evidence_id_ok'] = (key in ev and ev[key][0][:24] == ev[key][1][:24]\n"
        "                                   and ev[key][0].startswith('ev_'))"),
    # ---- rerun projection
    'M21-projection-drop-diagnostics': (
        "PROJECTION_KEYS = ('subject_sha256', 'files', 'chunks', 'extraction_gaps',\n"
        "                   'unpublished_entries', 'diagnostics')",
        "PROJECTION_KEYS = ('subject_sha256', 'files', 'chunks', 'extraction_gaps',\n"
        "                   'unpublished_entries')"),
    'M22-replay-drop-depth': (
        "REPLAY_PARAMS = (('--max-depth', 'max_depth'),\n"
        "                 ('--max-output-bytes', 'max_output_bytes'),\n"
        "                 ('--max-output-files', 'max_output_files'))",
        "REPLAY_PARAMS = (('--max-output-bytes', 'max_output_bytes'),\n"
        "                 ('--max-output-files', 'max_output_files'))"),
    'M23-projection-diff-always-equal': (
        "    return not keys, keys, detail",
        "    return True, [], detail"),
    # ---- frozen-path drift
    'M25-drift-endpoints-only': (
        "    p = git(root, 'log', '--pretty=format:', '--name-only', '--no-renames',\n"
        "            f'{freeze}..{rev}', check=False)",
        "    p = git(root, 'diff', '--name-only', freeze, rev, check=False)"),
    'M26-drift-drop-counter-path': (
        "    'tools/round-40/c1-counter.py',\n", ""),
    'M27-drift-ignore-spec-carriers': (
        "    for c in spec.get('carriers') or []:\n"
        "        if not isinstance(c, dict):\n"
        "            continue\n"
        "        for key in ('path', 'oracle', 'nonregular'):\n"
        "            v = c.get(key)\n"
        "            if isinstance(v, str) and v:\n"
        "                frozen.add(v)",
        "    pass"),
    'M28-drift-whole-history': (
        "            f'{freeze}..{rev}', check=False)",
        "            rev, check=False)"),
    # ---- marker / LE-chain probe
    'M29-layout-drop-marker': (
        "    elif not d['marker']:", "    elif False:"),
    'M30-layout-drop-bytes-used-sane': (
        "    d['bytes_used_sane'] = 0 < d['bytes_used'] <= len(raw)",
        "    d['bytes_used_sane'] = d['bytes_used'] > 0"),
    'M31-layout-drop-version': (
        "    elif not d['version_v4']:", "    elif False:"),
    'M32-layout-drop-identity-tiebreak': (
        "        if d['le_identity'] and not d['be_identity']:", "        if True:"),
    'M34-layout-le-from-be': (
        "    d['le_plausible'] = 1 <= d['meta_len_le'] <= METADATA_MAX",
        "    d['le_plausible'] = 1 <= d['meta_len_be'] <= METADATA_MAX"),
    # ---- receipt freshness / provenance
    'M35-receipt-fresh-nonstrict': (
        "            d['receipt_fresh'] = bool(add) and add != freeze and is_ancestor(root, freeze, add)",
        "            d['receipt_fresh'] = bool(add) and is_ancestor(root, freeze, add)"),
    'M36-provenance-no-dotdot': (
        "    return '..' not in output_directory.split('/')", "    return True"),
    # ---- verdict conjunction
    'M38-verdict-drop-chunks-ok': (
        "           'operation_ok', 'handler_ok', 'chunks_ok', 'oracle_hits_ok',",
        "           'operation_ok', 'handler_ok', 'oracle_hits_ok',"),
    'M39-verdict-drop-carriers-unchanged': (
        "    res['met_target'] = bool(res['carriers_unchanged'] and res['gap_rule_unchanged']\n"
        "                             and res['carriers_matched'] == target\n"
        "                             and all(b[x] is True for x in BINDINGS))",
        "    res['met_target'] = bool(res['gap_rule_unchanged']\n"
        "                             and res['carriers_matched'] == target\n"
        "                             and all(b[x] is True for x in BINDINGS))"),
}


def build_mutant(name, old, new):
    n = SRC.count(old)
    if n != 1:
        return {'name': name, 'error': 'old string occurs %d times' % n}
    mutated = SRC.replace(old, new)
    d = os.path.join(S, 'mutants', name)
    os.makedirs(os.path.join(d, 'tools', 'round-27'), exist_ok=True)
    with open(os.path.join(d, 'c1-counter.py'), 'w') as fh:
        fh.write(mutated)
    with open(os.path.join(d, 'tools', 'round-27', 'xpin-attribute.mjs'), 'wb') as fh:
        fh.write(XPIN_SRC)
    diff = ''.join(difflib.unified_diff(
        SRC.splitlines(True), mutated.splitlines(True),
        'c1-counter.py.prototype', 'c1-counter.py.%s' % name, n=2))
    with open(os.path.join(d, 'mutant.diff'), 'w') as fh:
        fh.write(diff)
    return {'name': name, 'sha256': hashlib.sha256(mutated.encode()).hexdigest()}


def run_mutant(name):
    d = os.path.join(S, 'mutants', name)
    env = dict(os.environ)
    env['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
    env['TMPDIR'] = S
    env['C1_SELFTEST_DETAIL'] = '1'
    try:
        p = subprocess.run(
            ['python3', os.path.join(d, 'c1-counter.py'), '--selftest',
             '--pkg65', PKG65],
            capture_output=True, text=True, env=env, cwd=d, timeout=900)
    except subprocess.TimeoutExpired as e:
        return {'name': name, 'exit': 'timeout', 'verdict': 'KILLED',
                'killed_by': ['selftest timeout'], 'failures': []}
    out = p.stdout.strip().splitlines()
    js = {}
    for line in out:
        if line.startswith('{'):
            try:
                js = json.loads(line)
            except json.JSONDecodeError:
                pass
    failures = js.get('failures') or []
    killed_by = sorted({f.split(':', 1)[0].strip() for f in failures})
    detail = [l for l in p.stderr.splitlines() if l.startswith('DETAIL\t')]
    verdict = 'KILLED' if (failures or p.returncode != 0) else 'SURVIVED'
    if p.returncode not in (0, 1) and not failures:
        killed_by = ['selftest crashed exit %d' % p.returncode]
    return {'name': name, 'exit': p.returncode, 'verdict': verdict,
            'cases': js.get('cases'), 'green_ok': js.get('green_ok'),
            'red_ok': js.get('red_ok'), 'killed_by': killed_by,
            'failures': failures[:6], 'n_detail': len(detail),
            'stderr_tail': p.stderr.strip().splitlines()[-3:] if p.returncode not in (0, 1) else []}


def main():
    meta = [build_mutant(k, *v) for k, v in MUTANTS.items()]
    bad = [m for m in meta if 'error' in m]
    if bad:
        print(json.dumps({'build_errors': bad}, indent=1))
        return 2
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(run_mutant, sorted(MUTANTS)))
    results.sort(key=lambda r: r['name'])
    out = {'baseline_sha256': hashlib.sha256(SRC.encode()).hexdigest(),
           'pkg65': PKG65, 'results': results, 'build': meta}
    with open(os.path.join(S, 'results.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    surv = [r['name'] for r in results if r['verdict'] == 'SURVIVED']
    print(json.dumps({'mutants': len(results),
                      'killed': len(results) - len(surv),
                      'survived': surv}, indent=1))
    for r in results:
        print('%-40s %-9s exit=%s killed_by=%s' % (
            r['name'], r['verdict'], r['exit'], ','.join(r['killed_by'][:4])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
