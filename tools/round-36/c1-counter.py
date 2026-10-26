#!/usr/bin/env python3
"""R36-C1 counter (coverage: sasquatch squashfs recursion, Frontier -> Core).

Predicate P36-C1 (frozen; same sentence in plans/round-36-claims.md):
  At the measured revision, for each of the four frozen carriers, the committed
  REA extract-firmware receipt run with sasquatch on PATH publishes every
  regular file of the frozen independent unsquashfs oracle (same relative path
  suffix, same sha256) with no sasquatch extraction gap, the paired committed
  no-sasquatch receipt publishes none of them and names sasquatch as a missing
  extractor dependency, both receipts recompute to their stored evidence id
  under the rea-agents 6.5.0 rule, and PROVINCE.md holds a round-36 Core row
  naming sasquatch that cites the round-36 knowledge entry, which cites a
  SOURCES.md row opened 2026-10-26 whose used-by lists that entry.

Target: carriers_matched == 4 and every binding true.

Usage:
  c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 REA650_PKG_ROOT [--json-out PATH]
  c1-counter.py --selftest --pkg65 REA650_PKG_ROOT
Exit: 0 target met, 1 target not met, 2 unevaluable (bad args, git/node failure).
Reads only git objects (git show REV:path); writes only a private scratch dir
under $HYAKU_SCRATCH (default /fast/scratch/hyaku)/kaidoku-r36 and --json-out.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

CARRIERS = 'corpus/evidence/round-36/c1/carriers.json'
EVDIR = 'corpus/evidence/round-36/c1'
ENTRY = 'corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md'
STEM = '2026-10-26-r36-sasquatch-squashfs-recursion'
CORE_HEADING = '## Round-36 additions to Core'
XPIN = 'tools/round-27/xpin-attribute.mjs'
OPENED = '2026-10-26'
TARGET = 4


class Unevaluable(Exception):
    pass


def git(root, *args, check=True):
    p = subprocess.run(['git', '-C', root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Unevaluable('git ' + ' '.join(args) + ': ' + p.stderr.decode(errors='replace').strip())
    return p


def show(root, rev, path):
    p = git(root, 'show', f'{rev}:{path}', check=False)
    return p.stdout if p.returncode == 0 else None


def scratch_root():
    d = os.path.join(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku'), 'kaidoku-r36')
    os.makedirs(d, exist_ok=True)
    return d


def section(text, heading):
    """Lines after an exact heading line up to the next line starting with '## '."""
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith('## '):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]


def sid_tokens(text):
    return set(re.findall(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])', text))


def evidence_ids(root, freeze, pkg65, envelopes, work):
    """Return {name: (stored, recomputed_650)} using the frozen xpin tool bytes."""
    tool = show(root, freeze, XPIN)
    if tool is None:
        raise Unevaluable('xpin tool absent at freeze')
    tpath = os.path.join(work, 'xpin-attribute.mjs')
    open(tpath, 'wb').write(tool)
    paths = []
    for name, env in envelopes.items():
        p = os.path.join(work, name.replace('/', '_') + '.wrapped.json')
        json.dump({'data': env}, open(p, 'w'))
        paths.append((name, p))
    if not paths:
        return {}
    r = subprocess.run(['node', tpath, '--pkg65', pkg65, '--pkg67', pkg65] + [p for _, p in paths],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Unevaluable('xpin: ' + r.stderr.strip())
    out = {}
    lines = r.stdout.splitlines()
    if len(lines) != len(paths):
        raise Unevaluable('xpin line count mismatch')
    for (name, _), line in zip(paths, lines):
        f = line.split('\t')
        out[name] = (f[1], f[2])
    return out


def load_oracle(raw):
    rows = []
    for line in raw.decode().splitlines():
        if not line:
            continue
        rel, sha, size = line.split('\t')
        rows.append((rel, sha))
    return rows


def published(env):
    nr = env.get('normalized_result') or {}
    return [(f.get('relative_path') or '', f.get('sha256') or '') for f in (nr.get('files') or [])]


def sasquatch_gap(env):
    nr = env.get('normalized_result') or {}
    for g in nr.get('extraction_gaps') or []:
        if g.get('kind') == 'missing-extractor-dependency' and 'sasquatch' in (g.get('dependencies') or []):
            return True
    return False


def matched(oracle, files):
    hits = 0
    for rel, sha in oracle:
        if any(sha == fs and (fp == rel or fp.endswith('/' + rel)) for fp, fs in files):
            hits += 1
    return hits


def measure(root, rev, freeze, pkg65):
    res = {'revision': rev, 'freeze': freeze, 'predicate': 'P36-C1', 'target': TARGET}
    git(root, 'cat-file', '-e', f'{rev}^{{commit}}')
    git(root, 'cat-file', '-e', f'{freeze}^{{commit}}')
    frozen = show(root, freeze, CARRIERS)
    if frozen is None:
        raise Unevaluable('carriers.json absent at freeze')
    cur = show(root, rev, CARRIERS)
    res['carriers_unchanged'] = cur == frozen
    spec = json.loads(frozen)
    ids = [c['id'] for c in spec['carriers']]
    work = tempfile.mkdtemp(prefix='c1-counter.', dir=scratch_root())
    try:
        per = {}
        envs = {}
        for c in spec['carriers']:
            k = c['id']
            d = {'id': k}
            o_freeze = show(root, freeze, f'{EVDIR}/{k}/oracle.tsv')
            o_rev = show(root, rev, f'{EVDIR}/{k}/oracle.tsv')
            d['oracle_frozen'] = o_freeze is not None and o_freeze == o_rev
            oracle = load_oracle(o_freeze) if o_freeze else []
            d['oracle_files'] = len(oracle)
            for mode in ('before', 'after'):
                raw = show(root, rev, f'{EVDIR}/{k}/{mode}.json')
                try:
                    env = json.loads(raw) if raw else None
                except json.JSONDecodeError:
                    env = None
                d[f'{mode}_present'] = isinstance(env, dict)
                if isinstance(env, dict):
                    envs[f'{k}/{mode}'] = env
                    d[f'{mode}_subject_ok'] = ((env.get('subject') or {}).get('digest') or {}).get('sha256') == c['sha256']
                    d[f'{mode}_operation_ok'] = env.get('operation') == 'extract_firmware' and (env.get('provider') or {}).get('id') == 'unblob'
                    d[f'{mode}_sasquatch_gap'] = sasquatch_gap(env)
                    d[f'{mode}_oracle_hits'] = matched(oracle, published(env))
            per[k] = d
        ev = evidence_ids(root, freeze, pkg65, envs, work)
        n = 0
        for k, d in per.items():
            for mode in ('before', 'after'):
                key = f'{k}/{mode}'
                d[f'{mode}_evidence_id_ok'] = key in ev and ev[key][0] == ev[key][1] and ev[key][0].startswith('ev_')
            ok = (d['oracle_frozen'] and d['oracle_files'] > 0
                  and d.get('before_present') and d.get('after_present')
                  and d.get('before_subject_ok') and d.get('after_subject_ok')
                  and d.get('before_operation_ok') and d.get('after_operation_ok')
                  and d.get('before_evidence_id_ok') and d.get('after_evidence_id_ok')
                  and d.get('before_sasquatch_gap') is True and d.get('before_oracle_hits') == 0
                  and d.get('after_sasquatch_gap') is False and d.get('after_oracle_hits') == d['oracle_files'])
            d['matched'] = bool(ok)
            n += bool(ok)
        res['carrier_ids'] = ids
        res['carriers'] = per
        res['carriers_matched'] = n
    finally:
        shutil.rmtree(work, ignore_errors=True)

    b = {}
    prov = show(root, rev, 'PROVINCE.md')
    sec = section(prov.decode(), CORE_HEADING) if prov else None
    b['province_core_section'] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith('|')]
    b['province_core_row'] = any(re.search(r'(?<![A-Za-z0-9-])sasquatch(?![A-Za-z0-9])', cells(r)[0]) and ENTRY in r for r in rows)
    ent = show(root, rev, ENTRY)
    b['entry_present'] = ent is not None
    src_ids = set()
    if ent:
        for line in ent.decode().splitlines():
            if line.startswith('source:'):
                src_ids |= sid_tokens(line)
    b['entry_source_ids'] = sorted(src_ids)
    reg = show(root, rev, 'corpus/SOURCES.md')
    ok_ids = []
    if reg:
        for line in reg.decode().splitlines():
            if not re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', line):
                continue
            c = cells(line)
            if len(c) != 11:
                continue
            used = [u.strip() for u in c[10].split(',')]
            if c[0] in src_ids and c[8] == OPENED and ENTRY in used:
                ok_ids.append(c[0])
    b['opened_source_rows'] = sorted(ok_ids)
    b['sourced'] = bool(ok_ids)
    readme = show(root, rev, 'corpus/README.md')
    cm = section(readme.decode(), '## Coverage map') if readme else None
    b['coverage_map_row'] = bool(cm) and any(STEM in l for l in cm if l.lstrip().startswith('|'))
    res['bindings'] = b
    bind_ok = all(b[x] for x in ('province_core_section', 'province_core_row', 'entry_present', 'sourced', 'coverage_map_row'))
    res['met_target'] = bool(res['carriers_unchanged'] and res['carriers_matched'] == TARGET and bind_ok)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--root')
    ap.add_argument('--rev')
    ap.add_argument('--freeze')
    ap.add_argument('--pkg65')
    ap.add_argument('--json-out')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.pkg65)
    if not (a.root and a.rev and a.freeze and a.pkg65):
        print('usage: --root --rev --freeze --pkg65 required', file=sys.stderr)
        return 2
    try:
        res = measure(a.root, a.rev, a.freeze, a.pkg65)
    except Unevaluable as e:
        res = {'unevaluable': str(e), 'argv': sys.argv}
        print(json.dumps(res, sort_keys=True))
        if a.json_out:
            json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
        return 2
    res['argv'] = sys.argv
    print(json.dumps({k: res[k] for k in ('revision', 'carriers_matched', 'carriers_unchanged', 'bindings', 'met_target')}, sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, 'w'), indent=1, sort_keys=True)
    return 0 if res['met_target'] else 1


# ---------------------------------------------------------------- selftest
def selftest(pkg65):
    """Fixture repos under scratch; every git call names -C <fixture>."""
    here = os.path.dirname(os.path.abspath(__file__))
    fx = os.path.join(here, 'selftest')
    before = json.load(open(os.path.join(fx, 'dev-before.json')))
    after = json.load(open(os.path.join(fx, 'dev-after.json')))
    oracle = open(os.path.join(fx, 'dev-oracle.tsv')).read()
    sha = after['subject']['digest']['sha256']
    xpin = open(os.path.join(here, '..', 'round-27', 'xpin-attribute.mjs'), 'rb').read()
    spec = {'carriers': [{'id': k, 'sha256': sha} for k in ('K1', 'K2', 'K3', 'K4')]}

    def province(row=True, heading=CORE_HEADING, cell='sasquatch'):
        r = f'| {cell} squashfs recursion | x | {ENTRY} |\n' if row else ''
        return f'# P\n\n{heading}\n\n| Surface | a | Entry |\n|---|---|---|\n{r}\n## Next\n'

    def entry(sid='S107'):
        return f'# E\n\nsource: {sid} — x\n'

    def registry(sid='S107', opened=OPENED, used=ENTRY):
        return ('# S\n\n## Registry\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
                '|---|---|---|---|---|---|---|---|---|---|---|\n'
                f'| {sid} | s | docs | A | s | a | t | mined | {opened} | 180d | {used} |\n')

    def readme(stem=STEM):
        return f'# R\n\n## Coverage map\n\n| a | b |\n|---|---|\n| x | `{stem}` |\n\n## Other\n'

    base_files = {XPIN: xpin, CARRIERS: json.dumps(spec)}
    for k in ('K1', 'K2', 'K3', 'K4'):
        base_files[f'{EVDIR}/{k}/oracle.tsv'] = oracle
    good = dict(base_files)
    for k in ('K1', 'K2', 'K3', 'K4'):
        good[f'{EVDIR}/{k}/before.json'] = json.dumps(before)
        good[f'{EVDIR}/{k}/after.json'] = json.dumps(after)
    good.update({'PROVINCE.md': province(), ENTRY: entry(), 'corpus/SOURCES.md': registry(), 'corpus/README.md': readme()})

    forged = json.loads(json.dumps(before))
    forged['normalized_result']['files'] = [{'relative_path': 'firmware.bin_extract/' + l.split('\t')[0], 'sha256': l.split('\t')[1]} for l in oracle.splitlines() if l]
    forged['normalized_result']['extraction_gaps'] = []

    def variant(**kw):
        v = dict(good)
        for k, val in kw.items():
            v[k] = val
        return v

    cases = [
        ('green', good, 0),
        ('do-nothing (freeze files only)', base_files, 1),
        ('after := before (no sasquatch)', variant(**{f'{EVDIR}/K2/after.json': json.dumps(before)}), 1),
        ('forged oracle-copy envelope', variant(**{f'{EVDIR}/K3/after.json': json.dumps(forged)}), 1),
        ('before := after', variant(**{f'{EVDIR}/K1/before.json': json.dumps(after)}), 1),
        ('oracle changed after freeze', variant(**{f'{EVDIR}/K4/oracle.tsv': oracle + 'x\t00\t1\n'}), 1),
        ('carriers changed after freeze', variant(**{CARRIERS: json.dumps({'carriers': spec['carriers'][:3]})}), 1),
        ('province row outside round-36 section', variant(**{'PROVINCE.md': province(heading='## Round-35 additions to Core')}), 1),
        ('province row without sasquatch in first cell', variant(**{'PROVINCE.md': province(cell='squashfs')}), 1),
        ('province row absent', variant(**{'PROVINCE.md': province(row=False)}), 1),
        ('S-id substring S1070', variant(**{ENTRY: entry('S1070')}), 1),
        ('source row opened earlier', variant(**{'corpus/SOURCES.md': registry(opened='2026-10-25')}), 1),
        ('used-by lacks entry', variant(**{'corpus/SOURCES.md': registry(used='corpus/lessons/round-36.md')}), 1),
        ('coverage map lacks stem', variant(**{'corpus/README.md': readme(stem='2026-10-26-r36-other')}), 1),
    ]
    sroot = scratch_root()
    green = red = 0
    fails = []
    for name, files, want in cases:
        d = tempfile.mkdtemp(prefix='c1-selftest.', dir=sroot)
        try:
            subprocess.run(['git', '-C', d, 'init', '-q'], check=True)
            top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
            if os.path.realpath(top) != os.path.realpath(d):
                raise SystemExit('fixture toplevel mismatch')
            env = dict(os.environ, GIT_AUTHOR_NAME='fixture', GIT_AUTHOR_EMAIL='fixture@invalid',
                       GIT_COMMITTER_NAME='fixture', GIT_COMMITTER_EMAIL='fixture@invalid')
            for p, c in base_files.items():
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'freeze'], check=True, env=env)
            fz = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            for p in list(base_files):
                if p not in files:
                    os.remove(os.path.join(d, p))
            for p, c in files.items():
                os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
                open(os.path.join(d, p), 'wb').write(c if isinstance(c, bytes) else c.encode())
            subprocess.run(['git', '-C', d, 'add', '-A'], check=True)
            subprocess.run(['git', '-C', d, 'commit', '-qm', 'data', '--allow-empty'], check=True, env=env)
            rv = subprocess.run(['git', '-C', d, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
            try:
                got = 0 if measure(d, rv, fz, pkg65)['met_target'] else 1
            except Unevaluable as e:
                got = 2
                fails.append(f'{name}: unevaluable {e}')
            if got == want:
                if want == 0:
                    green += 1
                else:
                    red += 1
            else:
                fails.append(f'{name}: want {want} got {got}')
        finally:
            shutil.rmtree(d, ignore_errors=True)
    print(json.dumps({'selftest': 'c1-counter', 'cases': len(cases), 'green_ok': green, 'red_ok': red, 'failures': fails}))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
