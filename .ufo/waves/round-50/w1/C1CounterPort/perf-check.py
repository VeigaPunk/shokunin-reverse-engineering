#!/usr/bin/env python3
"""Seat-local perf check (not a counter instrument): times the receipt-side clause
functions of the round-50 counter and of the round-41 counter on a synthetic
receipt shaped like the L1's a7530 run (13,366 regular files, 852 unpublished
symlink entries). The round-41 functions are quadratic: they are timed at a
smaller size and extrapolated, never run at 13k.

usage: python3 -I -B perf-check.py R50_COUNTER R41_COUNTER
"""
import importlib.util, json, sys, time, hashlib


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def synth(n_files, n_links, handler, outdir):
    chunk = 'firmware.bin_extract'
    files, rows, gaps, unpub, nonreg = [], [], [], [], []
    for i in range(n_files):
        rel = 'usr/lib/d%03d/f%05d.bin' % (i % 400, i)
        sha = hashlib.sha256(b'%d' % i).hexdigest()
        files.append({'relative_path': chunk + '/' + rel, 'path': '/x/' + rel,
                      'size': i % 977, 'sha256': sha})
        rows.append((rel, sha, i % 977))
    for i in range(n_links):
        rel = 'bin/l%04d' % i
        gaps.append({'kind': 'unpublished-entry', 'relative_path': chunk + '/' + rel,
                     'dependencies': []})
        unpub.append({'relative_path': chunk + '/' + rel, 'kind': 'symlink'})
        nonreg.append((rel, 'symlink', 't%d' % i))
    env = {'normalized_result': {
        'files': files, 'extraction_gaps': gaps, 'unpublished_entries': unpub,
        'chunks': [{'handler': handler, 'extraction_failed': False,
                    'range': {'offset': 0, 'length': 1}}],
        'derivations': [{'parent_path': '$input', 'child_path': '$output/' + chunk,
                         'handler': handler}],
        'diagnostics': []},
        'parameters': {'output_directory': outdir},
        'subject': {'digest': {'sha256': 'a' * 64}}}
    return env, rows, nonreg


def timeit(fn):
    t = time.perf_counter()
    r = fn()
    return round(time.perf_counter() - t, 3), r


def main():
    n50 = load(sys.argv[1], 'c50')
    n41 = load(sys.argv[2], 'c41')
    out = {}
    env, rows, nonreg = synth(13366, 852, n50.HANDLER, '/fast/scratch/hyaku/kaidoku-r50/x/out')
    root, _ = n50.subject_root(env)
    files = n50.published(env)
    model = {'allowed': {'symlink': ['unpublished-entry']}, 'required': {'symlink': True},
             'structural': {}, 'removed': {}}
    nested = n50.nested_roots(env, root)
    t, hits = timeit(lambda: n50.oracle_hits(rows, files, root, nested))
    out['r50_oracle_hits_s'] = t; out['r50_hits'] = hits
    t, ex = timeit(lambda: n50.extra_published(rows, files, root, nested))
    out['r50_extra_s'] = t; out['r50_extra'] = len(ex)
    t, esc = timeit(lambda: n50.nonregular_published(files, nonreg, root))
    out['r50_nonregular_published_s'] = t
    t, dc = timeit(lambda: n50.disposition_check(n50.gaps(env), [], nonreg, model, root,
                                                 '/fast/scratch/hyaku/kaidoku-r50/x/out'))
    out['r50_disposition_s'] = t; out['r50_disposition'] = dc[0]
    t, pr = timeit(lambda: n50.projection(env, 'plus-extractor'))
    out['r50_projection_s'] = t
    t, sh = timeit(lambda: n50.path_shape_ok(env))
    out['r50_path_shape_s'] = t; out['r50_path_shape'] = sh[0]
    # round 41 at a smaller size: quadratic
    for n in (1000, 2000):
        env4, rows4, nonreg4 = synth(n, 85, n41.HANDLER, '/x/out')
        r4, _ = n41.subject_root(env4)
        f4 = n41.published(env4)
        rows41 = [(a, b) for a, b, _c in rows4]
        t, h = timeit(lambda: n41.oracle_hits(rows41, f4, r4))
        out['r41_oracle_hits_%d_files_s' % n] = t
        t, _ = timeit(lambda: n41.nonregular_published(f4, nonreg4, r4))
        out['r41_nonregular_published_%d_files_s' % n] = t
    a, b = out['r41_oracle_hits_1000_files_s'], out['r41_oracle_hits_2000_files_s']
    out['r41_oracle_hits_13366_extrapolated_s'] = round(b * (13366 / 2000) ** 2, 1)
    print(json.dumps(out, indent=1, sort_keys=True))


main()
