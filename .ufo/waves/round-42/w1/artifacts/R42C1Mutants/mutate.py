#!/usr/bin/env python3
"""Mutation harness for tools/round-41/c1-counter.py (seat R42C1Mutants).

Detector (bounded, behavioral): `c1-counter.py --selftest` — offline,
deterministic, drives measure() in-process over ~90 fixture lanes and ~40
matcher/spec probes. The same detector runs on pristine bytes (baseline),
on each single-logic mutant, and on the restored bytes (final).

The harness only ever edits the file inside a disposable clone the caller
passes in; after every mutant the pristine bytes are written back and the
sha256 is re-verified against the recorded pristine hash.

Usage:
  mutate.py LANE ARTDIR --phase baseline
  mutate.py LANE ARTDIR --only M01,M02
  mutate.py LANE ARTDIR --phase final
"""
import argparse
import difflib
import hashlib
import json
import os
import subprocess
import sys
import time

PKG65 = '/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents'
TARGET = 'tools/round-41/c1-counter.py'

MUTANTS = [
    # ---- exact-path matcher / extract-root derivation --------------------
    {
        'id': 'M01',
        'area': 'extract-root derivation / exact-path matcher',
        'desc': ('extract_rel: whole-segment root equality replaced by a raw '
                 'string startswith — the non-segment-bounded prefix mutant '
                 '(a path `rootX/rest` is treated as inside `root`).'),
        'old': """    pret = root.split('/')
    if parts[:len(pret)] != pret:
        return None
    rest = parts[len(pret):]
    return '/'.join(rest) if rest else ''
""",
        'new': """    pret = root.split('/')
    joined = '/'.join(parts)
    pre = '/'.join(pret)
    if not joined.startswith(pre):
        return None
    return joined[len(pre):].lstrip('/')
""",
    },
    {
        'id': 'M02',
        'area': 'exact-path matcher',
        'desc': ('same_rel: exact root-mapped equality replaced by the '
                 'round-40 legacy suffix rule (R40-CL1 reintroduced).'),
        'old': """    if not rel:
        return False
    return extract_rel(candidate, root) == strip_rel(rel)
""",
        'new': """    if not rel:
        return False
    return legacy_same_rel(candidate, strip_rel(rel))
""",
    },
    {
        'id': 'M03',
        'area': 'extract-root derivation',
        'desc': ('subject_root: several squashfs_v4 roots no longer fail '
                 'closed; the deepest root is guessed.'),
        'old': """    if len(roots) == 1:
        return roots[0], 'single squashfs_v4 derivation root'
""",
        'new': """    if roots:
        return roots[0], 'single squashfs_v4 derivation root'
""",
    },
    {
        'id': 'M04',
        'area': 'extract-root derivation',
        'desc': ('subject_root: a frozen oracle_root hint is accepted without '
                 'checking it names an actual derivation root.'),
        'old': """    if hint is not None:
        if hint not in roots:
            return None, 'oracle_root %r not among %r' % (hint, roots)
        return hint, 'oracle_root from carriers.json'
""",
        'new': """    if hint is not None:
        return hint, 'oracle_root from carriers.json'
""",
    },
    {
        'id': 'M05',
        'area': 'exact-path matcher (path normalization)',
        'desc': ('path_parts: "." segments are no longer dropped, so a '
                 'receipt path containing `/./` no longer normalizes to the '
                 'oracle row path.'),
        'old': 'PLACEHOLDER-M05-OLD',
        'new': 'PLACEHOLDER-M05-NEW',
    },
    # ---- oracle hit-set equality ------------------------------------------
    {
        'id': 'M06',
        'area': 'oracle hit-set equality',
        'desc': ("oracle_hits_ok: full hit-set equality (hits == oracle rows) "
                 "relaxed to 'at least one oracle row published'."),
        'old': """                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and root_value is not None
                                       and d['oracle_hits'] == d['oracle_files'])
""",
        'new': """                d['oracle_hits_ok'] = (d['oracle_ok']
                                       and root_value is not None
                                       and d['oracle_hits'] > 0)
""",
    },
    # ---- non-regular unpublished -------------------------------------------
    {
        'id': 'M07',
        'area': 'non-regular unpublished',
        'desc': ('nonregular_published: exact matcher replaced by the legacy '
                 'suffix matcher, so a deeper file whose path ends with a '
                 'non-regular entry path counts as publishing it.'),
        'old': """    for fp, _, _ in files:
        for rel, _kind, _detail in nonreg:
            if same_rel(fp, rel, root):
                hits.append(fp)
""",
        'new': """    for fp, _, _ in files:
        for rel, _kind, _detail in nonreg:
            if legacy_same_rel(fp, strip_rel(rel)):
                hits.append(fp)
""",
    },
    # ---- gap-rule counts -----------------------------------------------------
    {
        'id': 'M08',
        'area': 'gap-rule counts (structural allowance)',
        'desc': ('disposition_check: structural per-kind allowance is read as '
                 'limit+1 (an off-by-one relaxation of the count rule).'),
        'old': """    over = {k: [n, structural[k]] for k, n in struct_count.items()
            if n > structural[k]}
""",
        'new': """    over = {k: [n, structural[k]] for k, n in struct_count.items()
            if n > structural[k] + 1}
""",
    },
    {
        'id': 'M09',
        'area': 'gap-rule counts (required default)',
        'desc': ('disposition_check: an entry kind with a non-empty allowed '
                 "list defaults to NOT required (need = required.get(kind, "
                 "False)), so materialised entries without an explicit "
                 '`required` block need no disposition.'),
        'old': """        need = required.get(kind, bool(allowed.get(kind)))
""",
        'new': """        need = required.get(kind, False)
""",
    },
    {
        'id': 'M10',
        'area': 'gap-rule counts (kind allowance)',
        'desc': ('disposition_check: any gap kind is accepted on an entry '
                 'whose kind has any allowance (membership test dropped).'),
        'old': """        entry_kind = by_rel[hits[0]][0]
        if kind not in allowed.get(entry_kind, []):
""",
        'new': """        entry_kind = by_rel[hits[0]][0]
        if not allowed.get(entry_kind):
""",
    },
    {
        'id': 'M22',
        'area': 'gap-rule counts (gap-to-entry resolution)',
        'desc': ('disposition_check: a gap path may match MULTIPLE non-regular '
                 'entries (uniqueness check `!= 1` relaxed to `not hits`); the '
                 'first match wins.'),
        'old': """        hits = [r for r, _k, _d in nonreg if same_rel(rp, r, root)]
        if len(hits) != 1:
""",
        'new': """        hits = [r for r, _k, _d in nonreg if same_rel(rp, r, root)]
        if not hits:
""",
    },
    # ---- handler binding -------------------------------------------------------
    {
        'id': 'M11',
        'area': 'handler binding (receipt clause)',
        'desc': ("handler_ok: exact handler name `squashfs_v4_be` accepted "
                 "for any handler with the `squashfs_v4` prefix."),
        'old': """                d['handler_ok'] = HANDLER in chunk_handlers(env)
""",
        'new': """                d['handler_ok'] = any(h and str(h).startswith('squashfs_v4')
                                      for h in chunk_handlers(env))
""",
    },
    {
        'id': 'M12',
        'area': 'handler binding (province row regex)',
        'desc': ('HANDLER_RE: segment-boundary lookarounds dropped — a token '
                 'like `xsquashfs_v4_bex` in a PROVINCE row cell now matches.'),
        'old': """HANDLER_RE = re.compile(r'(?<![A-Za-z0-9_-])' + HANDLER + r'(?![A-Za-z0-9_-])')
""",
        'new': """HANDLER_RE = re.compile(HANDLER)
""",
    },
    # ---- evidence id recompute ---------------------------------------------------
    {
        'id': 'M13',
        'area': 'evidence id recompute',
        'desc': ('evidence_ids: the stored id is compared to itself '
                 '((f[2], f[2])) — the recomputed id is never actually '
                 'checked, only the ev_ prefix is.'),
        'old': """        out[name] = (f[1], f[2])
""",
        'new': """        out[name] = (f[2], f[2])
""",
    },
    # ---- rerun projection ----------------------------------------------------------
    {
        'id': 'M14',
        'area': 'rerun projection (diagnostics identity)',
        'desc': ('projection: diagnostics projected as typename only (the '
                 'round-40 shape), so a rerun removing a different link '
                 'matches again — R41C1DevCore 7.3 reverted.'),
        'old': """        diags.append([typename, rel])
""",
        'new': """        diags.append([typename])
""",
    },
    {
        'id': 'M15',
        'area': 'rerun projection (parameter replay)',
        'desc': ('REPLAY_PARAMS: the recorded `--max-depth` is no longer '
                 'replayed to the rerun.'),
        'old': """REPLAY_PARAMS = (('--max-depth', 'max_depth'),
                 ('--max-output-bytes', 'max_output_bytes'),
                 ('--max-output-files', 'max_output_files'))
""",
        'new': """REPLAY_PARAMS = (('--max-output-bytes', 'max_output_bytes'),
                 ('--max-output-files', 'max_output_files'))
""",
    },
    {
        'id': 'M16',
        'area': 'rerun projection (real runner argv)',
        'desc': ('make_real_runner: REA pin changed to rea-agents@6.0.0 in '
                 'the rerun argv. --selftest injects every runner, so this '
                 'should survive unless the offline selftest inspects the '
                 'real runner.'),
        'old': """        argv = ['npx', '-y', REA_PIN, 'extract-firmware', '--format', 'json',
                '--full-output']
""",
        'new': """        argv = ['npx', '-y', 'rea-agents@6.0.0', 'extract-firmware', '--format', 'json',
                '--full-output']
""",
    },
    # ---- frozen-path drift -----------------------------------------------------------
    {
        'id': 'M17',
        'area': 'frozen-path drift (carrier table collection)',
        'desc': ('frozen_drift: carrier `path` entries are no longer added to '
                 'the frozen set — carrier bytes can change after the freeze '
                 'without a drift verdict.'),
        'old': """        for key in ('path', 'oracle', 'nonregular'):
""",
        'new': """        for key in ('oracle', 'nonregular'):
""",
    },
    {
        'id': 'M18',
        'area': 'frozen-path drift (endpoint equality)',
        'desc': ("met_target: the endpoint-equality clauses "
                 "(carriers_unchanged / gap_rule_unchanged) no longer gate "
                 "the verdict — only the drift log does."),
        'old': """    res['met_target'] = bool(res['carriers_unchanged'] and res['gap_rule_unchanged']
                             and res['carriers_matched'] == target
                             and all(b[x] is True for x in BINDINGS))
""",
        'new': """    res['met_target'] = bool(res['carriers_matched'] == target
                             and all(b[x] is True for x in BINDINGS))
""",
    },
    # ---- receipt exit codes -------------------------------------------------------------
    {
        'id': 'M19',
        'area': 'receipt exit codes (CLI verdict mapping)',
        'desc': ("main(): res['exit_code'] is hardcoded to 0 — a met/miss "
                 "receipt always exits 0."),
        'old': """    res['exit_code'] = 0 if res['met_target'] else 1
""",
        'new': """    res['exit_code'] = 0
""",
    },
    {
        'id': 'M20',
        'area': 'receipt exit codes (unevaluable mapping)',
        'desc': ('main(): an Unevaluable outcome exits 1 instead of 2 — '
                 'unevaluable and target-miss become indistinguishable at '
                 'the CLI.'),
        'old': """        if a.json_out:
            json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 2
    res['argv'] = sys.argv
""",
        'new': """        if a.json_out:
            json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 1
    res['argv'] = sys.argv
""",
    },
    {
        'id': 'M21',
        'area': 'receipt exit codes (selftest in-loop mapping)',
        'desc': ('selftest loop: a FrozenPathChanged exception is recorded as '
                 'exit 1 instead of 2 — drift cases (want 2) should catch it.'),
        'old': """            except FrozenPathChanged as e:
                got, why, res, failing = 2, e.reason, None, set()
""",
        'new': """            except FrozenPathChanged as e:
                got, why, res, failing = 1, e.reason, None, set()
""",
    },
]

# M05 fixed here to keep the table above free of quote-nesting mistakes.
MUTANTS[4]['old'] = "    return [x for x in p.split('/') if x not in ('', '.')]\n"
MUTANTS[4]['new'] = "    return [x for x in p.split('/') if x != '']\n"


def run_selftest(lane, outdir, tag):
    env = dict(os.environ)
    env['HYAKU_SCRATCH'] = '/fast/scratch/hyaku'
    env['TMPDIR'] = '/fast/scratch/hyaku'
    t0 = time.time()
    p = subprocess.run([sys.executable, os.path.join(lane, TARGET),
                        '--selftest', '--pkg65', PKG65],
                       capture_output=True, text=True, env=env, cwd=lane)
    dur = time.time() - t0
    with open(os.path.join(outdir, tag + '.out'), 'w') as fh:
        fh.write(p.stdout)
    with open(os.path.join(outdir, tag + '.err'), 'w') as fh:
        fh.write(p.stderr)
    summary = None
    for line in reversed(p.stdout.splitlines()):
        s = line.strip()
        if s.startswith('{'):
            try:
                summary = json.loads(s)
                break
            except json.JSONDecodeError:
                pass
    return {'tag': tag, 'exit': p.returncode, 'seconds': round(dur, 1),
            'cases': (summary or {}).get('cases'),
            'green_ok': (summary or {}).get('green_ok'),
            'red_ok': (summary or {}).get('red_ok'),
            'failures': (summary or {}).get('failures'),
            'stderr_head': p.stderr[:300]}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lane')
    ap.add_argument('artdir')
    ap.add_argument('--phase', choices=('baseline', 'final', 'mutants', 'restore'))
    ap.add_argument('--only', help='comma-separated mutant ids (phase=mutants)')
    a = ap.parse_args()
    runs = os.path.join(a.artdir, 'runs')
    os.makedirs(runs, exist_ok=True)
    src = os.path.join(a.lane, TARGET)
    pristine = open(src, 'rb').read()
    phash = sha(pristine)
    hashlog = os.path.join(a.artdir, 'hash-log.txt')

    def note(msg):
        with open(hashlog, 'a') as fh:
            fh.write(msg + '\n')

    if a.phase == 'restore':
        want = json.load(open(os.path.join(a.artdir, 'baseline.json')))['sha256']
        p = subprocess.run(['git', '-C', a.lane, 'cat-file', 'blob',
                            'HEAD:' + TARGET], capture_output=True, check=True)
        blob = p.stdout
        rec = {'phase': 'restore', 'git_blob_sha256': sha(blob), 'want': want,
               'restored': sha(blob) == want}
        if rec['restored']:
            with open(src, 'wb') as fh:
                fh.write(blob)
        rec['on_disk_after'] = sha(open(src, 'rb').read())
        note('restore %s -> %s (%s)' % (want, rec['on_disk_after'],
                                        'ok' if rec['restored'] else 'REFUSED'))
        print(json.dumps(rec, indent=1))
        return 0 if rec['restored'] else 1

    if a.phase in ('baseline', 'final'):
        r = run_selftest(a.lane, runs, a.phase)
        r['sha256'] = phash
        ok = (r['exit'] == 0 and not (r['failures'] or []))
        r['verdict'] = 'pass' if ok else 'BASELINE-FAIL'
        note('%s %s %s' % (a.phase, phash, r['verdict']))
        if a.phase == 'baseline':
            with open(os.path.join(a.artdir, 'baseline.json'), 'w') as fh:
                json.dump(r, fh, indent=1)
        print(json.dumps(r, indent=1))
        return 0 if ok else 1

    baseline = json.load(open(os.path.join(a.artdir, 'baseline.json')))
    base_ok = baseline['exit'] == 0 and not (baseline['failures'] or [])
    cur = sha(open(src, 'rb').read())
    if cur != baseline['sha256']:
        print(json.dumps({'error': 'clone file is not pristine before mutants',
                          'sha256': cur, 'want': baseline['sha256'],
                          'remedy': 'run --phase restore first'}))
        return 3
    ids = a.only.split(',') if a.only else [m['id'] for m in MUTANTS]
    by_id = {m['id']: m for m in MUTANTS}
    out = []
    for mid in ids:
        m = by_id[mid]
        body = pristine.decode()
        cnt = body.count(m['old'])
        rec = {'id': mid, 'area': m['area'], 'desc': m['desc'],
               'old_occurrences': cnt}
        if cnt != 1:
            rec['verdict'] = 'HARNESS-ERROR'
            rec['error'] = 'old-string count %d, want exactly 1' % cnt
            out.append(rec)
            print(json.dumps(rec), flush=True)
            continue
        with open(src, 'w') as fh:
            fh.write(body.replace(m['old'], m['new']))
        diff = '\n'.join(difflib.unified_diff(
            pristine.decode().splitlines(), body.replace(m['old'], m['new']).splitlines(),
            fromfile='pristine', tofile=mid, lineterm=''))
        with open(os.path.join(runs, mid + '.diff'), 'w') as fh:
            fh.write(diff + '\n')
        try:
            r = run_selftest(a.lane, runs, mid)
        finally:
            with open(src, 'wb') as fh:
                fh.write(pristine)
        restored_ok = sha(open(src, 'rb').read()) == phash
        killed = (r['exit'] != 0) or bool(r['failures'] or [])
        rec.update({
            'mutant_exit': r['exit'],
            'seconds': r['seconds'],
            'n_failures': len(r['failures'] or []),
            'failures_head': (r['failures'] or [])[:4],
            'killed': killed,
            'verdict': ('killed' if killed and base_ok
                        else 'SURVIVED' if base_ok else 'inconclusive'),
            'restored_sha256_matches': restored_ok,
        })
        if not base_ok:
            rec['verdict'] = 'inconclusive (baseline failed)'
        note('%s mutant %s sha-after-restore %s (%s)' % (mid, phash, phash,
                                                         'ok' if restored_ok else 'MISMATCH'))
        out.append(rec)
        print(json.dumps(rec), flush=True)
    with open(os.path.join(a.artdir, 'mutants-partial.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
